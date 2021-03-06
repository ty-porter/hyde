#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.0.9'

with open("DESCRIPTION.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hyde-lang',
    author='Tyler Porter',
    author_email='tyler.b.porter@gmail.com',
    version=version,
    license='MIT',
    description='A Python-based interpretation of Lox',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ty-porter/hyde',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords=[
        'hyde',
        'programming languages'
    ],
    platforms='ANY',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hyde = hyde.__main__:run'
        ]
    },
    include_package_data=True
)