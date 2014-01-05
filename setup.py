#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as file:
    long_description = file.read()

setup(
    name='envauth',
    version='1.0.0',
    url='https://github.com/waawal/envauth',
    license='MIT',
    author='Daniel Waardal',
    author_email='waawal@boom.ws',
    description='Authentication based on the ENVAUTH environment variable',
    long_description=long_description,
    py_modules=['envauth'],
    zip_safe=True,
    platforms='any',
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Systems Administration',

    ]
)