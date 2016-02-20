#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from setuptools import setup, find_packages

import pip
requirements = pip.req.parse_requirements(
    "requirements.txt", session=pip.download.PipSession()
)

pip_requirements = [str(r.req) for r in requirements]

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name='parktain',
    author='Puneeth Chaganti',
    author_email='punchagan@muse-amuse.in',
    packages=find_packages(exclude=['tests*']),
    version='0.1',
    description='a slack bot for parkers',
    zip_safe=False,
    long_description=readme,
    license=license,

    entry_points={
        'console_scripts': [
            'parktain=parktain.main:main',
        ],
    }

)
