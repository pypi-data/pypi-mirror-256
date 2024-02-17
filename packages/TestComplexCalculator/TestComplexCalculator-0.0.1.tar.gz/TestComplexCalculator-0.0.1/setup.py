#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:33:28 2024

@author: julie.ludwig
"""

from setuptools import setup
import setuptools

setup(
    name="TestComplexCalculator",
    version="0.0.1",
    author="Julie Ludwig",
    description="Test sur des calculs de nombres complexes",
    license="GNU GPLv3",
    python_requires=">=3.4",
    package_dir={"": "Package_Calculator"},
    packages=setuptools.find_namespace_packages(where="Calculator"),
)
