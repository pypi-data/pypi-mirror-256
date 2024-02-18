from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="ecv-python-helpers",
    version="1.0.5",
    author="Warren Ezra Bruce Jaudian",
    author_email="warren.jaudian@ecloudvalley.com",
    packages=find_packages(),
    description="ECV Python Helpers Package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://git-codecommit.ap-southeast-1.amazonaws.com/v1/repos/ecv-python-helpers",
    license="MIT",
    python_requires=">=3.8",
    install_requires=["aws-lambda-powertools==2.5.0", "pytz==2022.7", "pydantic"],
    package_data={"ecv_helpers": ["ecv_helpers/*"], "ecv_database": ["ecv_database/*"]},
)
