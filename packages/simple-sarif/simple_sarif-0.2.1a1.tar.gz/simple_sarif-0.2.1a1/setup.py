from setuptools import find_packages, setup

with open("README.md") as readme:
        description = readme.read()

setup(
    name='simple_sarif',
    version='0.2.1a1',
    packages=find_packages(),
    install_requires=[
        'jsonschema>=4.21.1'
    ],
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/scribe-security/simple-sarif',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)