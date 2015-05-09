#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-walking-settings.
# https://github.com/rflorianobr/django-walking-settings

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Rafael Floriano da Silva <rflorianobr@gmail.com>

from setuptools import setup, find_packages
from walking_settings import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
    'nose_focus',
]

setup(
    name='django-walking-settings',
    version=__version__,
    description='a live settings setter for django',
    long_description='''
A live settings setter for django.
Django walking-settings provide a model to set settings variables in database.
You can create or change settings by django-admin.
Enjoy it ;)
''',
    keywords='django walking settings live',
    author='Rafael Floriano da Silva',
    author_email='rflorianobr@gmail.com',
    url='https://github.com/rflorianobr/django-walking-settings',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'django',
    ],
    extras_require={
        'tests': tests_require,
    },
)
