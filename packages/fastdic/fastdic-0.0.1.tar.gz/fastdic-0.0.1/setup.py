#!/usr/bin/env python3
"""Setup script for the fastdi package."""

import sys

from setuptools import setup

MIN_MAJOR_VERSION = 3
MIN_MINOR_VERSION = 6

if sys.version_info < (MIN_MAJOR_VERSION, MIN_MINOR_VERSION):
    sys.exit(
        "Python {}.{} or higher is required".format(
            MIN_MAJOR_VERSION, MIN_MINOR_VERSION
        )
    )

setup(
    name="fastdic",
    version="0.0.1",
    description="FastDI is a simple and fast dependency injection container library for Python 3",
    author="Artsiom Praneuski",
    author_email="artsiom.praneuski@gmail.com",
    url="https://github.com/artempronevskiy/fastdi",
    packages=[
        "fastdi",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">={}.{}".format(MIN_MAJOR_VERSION, MIN_MINOR_VERSION),
    install_requires=[],
    entry_points={},
)
