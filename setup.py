#!/usr/bin/env python
# coding: utf-8

import setuptools
import os
import sys

this_directory = os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_directory)

with open(os.path.join(this_directory, 'README.md'), 'r', encoding='utf-8') as fh:
    readme = fh.read()

tabugen_version = '0.7.1'

install_requires = [
    'et-xmlfile>=1.0.1',
    'jdcal>=1.4.1',
    'openpyxl>=2.6.3',
    'PyMySQL>=0.9.3',
]

setuptools.setup(
    name='tabugen',
    version=tabugen_version,
    license='Apache License 2.0',
    author='qchencc',
    author_email='ichenq@outlook.com',
    url='https://github.com/qchencc/tabugen',
    description=u'a spreedsheet export and code generate tool for rapid game development',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            "tabugen = tabugen.cli:main"
        ]
    }
)