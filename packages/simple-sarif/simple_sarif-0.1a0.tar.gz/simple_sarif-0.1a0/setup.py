from setuptools import find_packages, setup

setup(
    name='simple_sarif',
    version='0.1-alpha',
    packages=find_packages(),
    install_requires=[
        'jsonschema>=4.21.1'
    ],
)