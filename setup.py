#!/usr/bin/env python

import io
import os

from setuptools import setup

with io.open(os.path.join(os.path.dirname(__file__), 'README'), 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='adba',
    version='1.1.0',
    description='Python wrapper for the AniDB.net UDP API',
    long_description=long_description,
    url='https://github.com/pymedusa/adba',
    packages=['adba'],
    install_requires=[
        'configparser>=3.5.0,<4.0.0;python_version<"3"'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
