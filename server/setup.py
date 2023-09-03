#!/usr/bin/env python

from setuptools import find_packages, setup

packages = [
    "numpy",
    "numpy-stl",
    "shapely",
    "rasterio",
    "fastapi",
    "uvicorn",
    "pymesh2",
    "google-api-python-client",
    "google-auth",
    "google-auth-oauthlib",
    "google-auth-httplib2",
]

test_packages = [
    "mock==4.0.3",
    "pytest==6.2.4",
]

linting_packages = [
    "pre-commit==2.9.3",
    "black==22.3.0",
    "flake8==3.8.4",
    "flake8-bugbear==20.1.4",
    "flake8-builtins==1.5.3",
    "flake8-comprehensions==3.2.3",
    "flake8-tidy-imports==4.2.1",
    "flake8-import-order==0.18.1",
]

setup(
    name="Terrain Viewer",
    version="1.0",
    description="returning STL files from a region",
    author="John Oram",
    author_email="john@oram.ca",
    packages=find_packages(),
    install_requires=packages,
    extras_require={
        "dev": test_packages + linting_packages,
    },
)
