# -*- coding: utf-8 -*-
"""Setup script."""
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='{{ name }}',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='{{ description }}',
    long_description=README,
    url='{{ url }}',
    author='{{ author }}',
    author_email='{{ author_email }}',
    install_requires=[
        'mlflow',
        'dvc',
        'tensorflow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
