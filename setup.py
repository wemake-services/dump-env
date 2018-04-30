#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError) as ex:
    print('Pandoc failed', ex)
    # Import the README and use it as the long-description.
    # Note: this will only work if 'README.rst' is
    # present in your MANIFEST.in file!
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='dump-env',
    version='0.2.1',
    description='A utility tool to create .env files',
    long_description=long_description,
    author='Nikita Sobolev',
    author_email='mail@sobolenv.me',
    url='https://github.com/sobolevn/dump-env',

    packages=find_packages(exclude=('tests', )),

    install_requires=[],
    include_package_data=True,
    zip_safe=False,

    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords=[
        'dotenv',
        '.env',
        'tempaltes',
        'secrets',
        'CI/CD',
    ],

    entry_points={
        'console_scripts': [
            'dump-env=dump_env.cli:main',
        ],
    },
)
