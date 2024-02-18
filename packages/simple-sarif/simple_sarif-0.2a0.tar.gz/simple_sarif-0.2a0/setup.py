from setuptools import find_packages, setup

with open("README.md") as readme:
        description = readme.read()

setup(
    name='simple_sarif',
    version='0.2-alpha',
    packages=find_packages(),
    install_requires=[
        'jsonschema>=4.21.1'
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)