#!/usr/bin/env python3

"""
{{docstring}}
"""

from setuptools import setup, find_packages


setup(
    name='remove_overlap',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pandas==1.5.0',
        'pylint==3.0.2',
        'autopep8==1.7.0',
        'ortools==9.4.1874',
        'igraph==0.10.4',
        'matplotlib',
        'pytictoc'
    ]
)
