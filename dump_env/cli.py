#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
from typing import Union

from dump_env.dumper import Dumper, StrictDumper, StrictException


STRICT_WITHOUT_TEMPLATE_MSG = 'For --strict option either strict ' \
                              'variables or template should be given.\n'


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--template',
        default='',
        type=str,
        help='Adds template path',
    )
    parser.add_argument(
        '--strict',
        type=str,
        nargs='?',
        const=True,
        default=False,
        dest='strict',
        help='Strict variables should exists in os envs',
    )
    parser.add_argument('-p', '--prefix', action='append', help='Adds prefix')
    return parser


def main() -> None:
    """
    Runs dump-env script.

    Examples:
        This example will dump all environ variables::

            $ dump-env

        This example will dump all environ variables starting with `PIP_`::

            $ dump-env -p 'PIP_'

        This example will dump all environ variables starting with `PIP_`
        and update them with variables starting with `SECRET_`::

            $ dump-env -p 'PIP_' -p 'SECRET_'

        This example will dump everything from `.env.template` file
        and all env variables with `SECRET_` prefix into a `.env` file::

            $ dump-env -p 'SECRET_' -t .env.template > .env

    """
    parser = _create_parser()
    args = parser.parse_args()

    if args.strict is True and not args.template:
        sys.stderr.write(STRICT_WITHOUT_TEMPLATE_MSG)
        return

    strict: Union[bool, str] = args.strict

    if not strict:
        dumper = Dumper(template=args.template, prefixes=args.prefix)
    else:
        strict_envs = strict.split(',') if isinstance(strict, str) else []
        dumper = StrictDumper(
            template=args.template,
            prefixes=args.prefix,
            strict_envs=strict_envs
        )

    try:
        variables = dumper.dump()
    except StrictException as e:
        sys.stderr.write(str(e) + '\n')
        return

    for env_name, env_value in variables.items():
        sys.stdout.write('{0}={1}'.format(env_name, env_value) + '\n')
