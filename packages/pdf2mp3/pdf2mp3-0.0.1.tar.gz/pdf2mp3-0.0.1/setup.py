#!/usr/bin/env python
import codecs
import os
import re

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md") as f:
    long_description = f.read()


def read(*parts):
    return codecs.open(os.path.join(here, *parts), "r").read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="pdf2mp3",
    version=find_version("pdf2mp3", "__init__.py"),
    description="CLI to converts PDF to MP3 using Google Text-to-Speech.",
    package_dir={"": "pdf2mp3"},
    packages=find_packages(where="pdf2mp3"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andreyrcdias/pdf2mp3",
    author="Andrey dos Reis Cadima Dias",
    author_email="andreyrcdias@gmail.com",
    keywords="pdf mp3 gtts",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "gtts >= 2.5.1",
        "rich >= 13.7.0",
        "pypdf2 >= 3.0.1",
        "langdetect >= 1.0.9",
    ],
    extra_require={
        "dev": [
            "black = ^24.1.1",
            "isort = ^5.13.2",
            "ruff = ^0.2.1",
            "pyclean = ^2.7.6",
        ]
    },
    python_requires=">=3.12",
    entry_points={},
)
