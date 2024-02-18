#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from ccstiet import __version__


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# the setup
setup(
    name='ccstiet',
    version=__version__,
    description='pip package for Creative Computing Society,Thapar University,Patiala,India',
    # long_description=read('README'),
    url='https://github.com/dgbkn/ccstiet_pip_package',
    author='dgbkn',
    author_email='anandrambkn@gmail.com',
    license='MIT',
    keywords='cctiet,creative,computing,society',
    packages=find_packages(exclude=('docs', 'tests', 'env', 'index.py')),
    include_package_data=True,
    install_requires=[
    ],
    extras_require={
    'dev': [],
    'docs': [],
    'testing': [],
    },
    classifiers=[],
    )
