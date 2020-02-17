import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='axon-conabio2',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Machine Learning Admin system for Conabio',
    long_description=README,
    url='https://github.com/CONABIO-audio/axon',
    author='CONABIO, Dalia Camacho García Formentí, Gustavo Everardo Robredo Esquivelzeta, Santiago Martínez Balvanera',
    author_email='dcamacho@conabio.gob.mx, erobredo@conabio.gob.mx, smartinez@conabio.gob.mx',
    install_requires=[
        'mlflow',
        'luigi',
        'dvc',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
