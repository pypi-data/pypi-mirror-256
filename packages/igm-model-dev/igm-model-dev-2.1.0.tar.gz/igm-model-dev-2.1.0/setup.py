#!/usr/bin/env python
# Copyright (C) 2021-2022 Guillaume Jouvet <guillaume.jouvet@unil.ch>
# Published under the GNU GPL (Version 3)

from setuptools import setup, find_packages
import os
import subprocess


def package_files(directory):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="igm-model-dev",
    version="2.1.0",
    author="Guillaume Jouvet",
    author_email="guillaume.jouvet@unil.ch",
    url="https://github.com/jouvetg/igm",
    license="gpl-3.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["igm_run = igm.igm_run:main"]},
    package_data={"igm": package_files("igm/emulators")},
    description="IGM - a glacier evolution model",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires="<3.12",
    install_requires=[
        "tensorflow[and-cuda]",
        "matplotlib",
        "scipy",
        "netCDF4",
        "xarray",
        "rasterio",
        "pyproj",
        "geopandas",
        "oggm",
        "importlib_resources",
    ],
)
