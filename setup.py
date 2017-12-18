#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

REQUIRED = []
TESTS_REQUIRE = [
    'six',

    # pytest plugins:
    'pytest-cov',
    'pytest-isort',

    # Linting:
    'flake8-builtins',
    'flake8-commas',
    'flake8-quotes',
    'flake8-pep3101',
    'flake8-bugbear',
    'flake8-comprehensions',
    'flake8-blind-except',
    'flake8-docstrings',
    'pep8-naming',
    'flake8',
    'pytest-flake8',

    'pytest',
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name='dump-env',
    version='0.0.1',
    description='A utility tool to create .env files',
    long_description=long_description,
    author='Nikita Sobolev',
    author_email='mail@sobolenv.me',
    url='https://github.com/sobolevn/dump-env',

    packages=find_packages(exclude=('tests', )),

    install_requires=REQUIRED,
    include_package_data=True,

    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
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

    entry_points={
        'console_scripts': ['dump_env=dump_env:cli'],
    },
    cmdclass={
        'upload': UploadCommand,
    },
)
