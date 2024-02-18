from __future__ import annotations

import json

from aws_lambda_powertools.middleware_factory import (
    lambda_handler_decorator,  # type: ignore
)
from aws_lambda_powertools.utilities.typing import LambdaContext
from cerberus import Validator  # type: ignore
from typing_extensions import Any, Callable, Literal

from .exceptions import RequestValidationException
from .handler import app
from .logger import log


@lambda_handler_decorator
def validate_function_source(
    handler: Callable[..., dict[Any, Any]],
    event: dict[Any, Any],
    context: LambdaContext,
) -> dict[Any, Any]:
    if _skip_warmup_call(event):
        return {}

    response = handler(event, context)
    print(response)  # check if this is necessary
    return response


@lambda_handler_decorator
def validate_web_request(
    handler: Callable[..., dict[Any, Any]],
    event: dict[Any, Any],
    context: LambdaContext,
    schema: dict[Any, Any] | Any,
) -> dict[Any, Any]:
    if _skip_warmup_call(event):
        return {}

    if isinstance(schema, dict):
        schema_param = schema
    else:
        schema_param = schema.SCHEMA

    validator = Validator(schema_param, purge_unknown=True)  # type: ignore

    body: dict[Any, Any] = {}
    if event["body"]:
        body = json.loads(event["body"])

    if event["queryStringParameters"]:
        body = {**body, **event["queryStringParameters"]}

    if event["pathParameters"]:
        body = {**body, **event["pathParameters"]}

    log("UNVALIDATED_BODY", data=body)

    result = validator.validate(body)  # type: ignore
    payload = {**validator.document}  # type: ignore
    setattr(app, "validated_body", payload)

    if not result:
        return {
            "body": json.dumps(
                {
                    "error": {
                        "code": RequestValidationException.ERROR_CODE,
                        "message": RequestValidationException.ERROR_MESSAGE,
                        "error_details": _restructure_validation_message(validator.errors),  # type: ignore
                    }
                },
                default=str,
            ),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Header": "*",
            },
            "status_code": RequestValidationException.STATUS_CODE,
        }

    response = handler(event, context)
    print(response)  # check if this is necessary

    return response


def _skip_warmup_call(event: dict[Any, Any]) -> Literal[True] | None:
    if event.get("source") == "serverless-plugin-warmup":
        log("LAMBDA_WARMER_INVOCATION")
        return True


def _restructure_validation_message(
    validated_data: dict[Any, Any]
) -> list[dict[str, Any]]:
    error_message_list: list[dict[Any, Any]] = []
    for key, items in validated_data.items():
        for sub_key in items:
            temp_dict: dict[Any, Any] = {}
            if isinstance(sub_key, str):
                temp_dict["field"] = key
                temp_dict["error"] = " ".join(items)
                temp_dict["error_message"] = " ".join(items)
                error_message_list.append(temp_dict)
                break
            elif isinstance(sub_key, dict):
                for dict_key, dict_items in sub_key.items():  # type: ignore
                    for dict_sub_key in dict_items:  # type: ignore
                        if isinstance(dict_sub_key, dict):
                            dict_sub_key: dict[str, Any]
                            for list_sub_key, list_sub_items in dict_sub_key.items():
                                if isinstance(list_sub_items, list):
                                    temp_dict = {}
                                    temp_dict["field"] = (
                                        f"{key}[{dict_key}].{list_sub_key}"
                                    )
                                    temp_dict["error"] = "\n".join(list_sub_items)  # type: ignore
                                    temp_dict["error_message"] = "\n".join(
                                        list_sub_items  # type: ignore
                                    )
                                    error_message_list.append(temp_dict)
                        elif isinstance(dict_sub_key, str):
                            temp_dict = {}
                            temp_dict["field"] = f"{dict_key}"
                            temp_dict["error"] = dict_sub_key
                            temp_dict["error_message"] = dict_sub_key
                            error_message_list.append(temp_dict)

    return error_message_list
