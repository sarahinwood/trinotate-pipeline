#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


# load README.rst
def readme():
    with open('README.rst') as file:
        return file.read()


setup(
    name='trinotate_pipeline',
    version='0.0.1',
    description='python3 wrapper for Trinotate',
    long_description=readme(),
    url='https://github.com/sarahinwood/trinotate_pipeline',
    author='Sarah Inwood, Tom Harrop',
    author_email='sninwood@gmail.com, twharrop@gmail.com',
    license='GPL-3',
    packages=find_packages(),
    install_requires=[
        'biopython>=1.70',
        'numpy>=1.13.1',
        'snakemake>=4.0.0'
    ],
    scripts=[
        'trinotate_pipeline/src/rename_fasta_headers.py',
        'trinotate_pipeline/src/rename_gff.R'
    ],
    entry_points={
        'console_scripts': [
            'trinotate_pipeline = trinotate_pipeline.__main__:main'
            ],
    },
    package_data={
        'trinotate_pipeline': [
            'Snakefile',
            'README.rst'
        ],
    },
    zip_safe=False)
