#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from dump_env import dump


def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--template', default='',
                        type=str, help='Adds template path')
    parser.add_argument('-p', '--prefix', default='',
                        type=str, help='Adds prefix')
    return parser


def main():
    """
    Runs dump-env script.

    Examples:
        This example will dump all environ variables::

            $ dump-env

        This example will dump all environ variables starting with `PIP_`::

            $ dump-env -p 'PIP_'

        This example will dump everything from `.env.template` file
        and all env variables with `SECRET_` prefix into a `.env` file::

            $ dump-env -p 'SECRET_' -t .env.template > .env

    """
    parser = _create_parser()
    args = parser.parse_args()
    variables = dump(args.template, args.prefix)

    for key, value in variables.items():
        print('{0}={1}'.format(key, value))
