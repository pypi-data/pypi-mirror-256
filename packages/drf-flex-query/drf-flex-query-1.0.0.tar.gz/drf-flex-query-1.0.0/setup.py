#!/usr/bin/env python
from setuptools import setup
from codecs import open


def readme():
    with open("README.md", "r") as infile:
        return infile.read()


classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
setup(
    name="drf-flex-query",
    version="1.0.0",
    description="Flexible related objects quering for Django REST Framework.",
    author="Grigorii Novikov",
    author_email="genovikov93@gmail.com",
    packages=["flex_query"],
    url="https://github.com/Oper18/drf-flex-query",
    license="MIT",
    keywords="django rest api query",
    long_description=readme(),
    classifiers=classifiers,
    long_description_content_type="text/markdown",
)
