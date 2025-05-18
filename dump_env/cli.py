import argparse
import sys
from typing import Final, NoReturn

from dump_env import dumper
from dump_env.exceptions import StrictEnvError

# Characters that require the value to be quoted
QUOTE_CHARS: Final = (' ', '\n', '=', '"', "'")


def needs_quotes(raw_env_value: str) -> bool:
    """
    Check if the value needs to be quoted.

    Args:
        raw_env_value (str): The value to check.

    Returns:
        bool: True if the value needs to be quoted, False otherwise.
    """
    if not raw_env_value:
        return False
    return any(char in raw_env_value for char in QUOTE_CHARS)


def escape(raw_env_value: str) -> str:
    """
    Escape the value for use in an environment variable.

    Args:
        raw_env_value (str): The value to escape.

    Returns:
        str: The escaped value.
    """
    return (
        raw_env_value
        # Backslashes need to be escaped
        .replace('\\', '\\\\')  # noqa: WPS348, WPS342
        # Quotes in the value need to be escaped
        .replace('"', '\\"')  # noqa: WPS348, WPS342
    )


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--prefix',
        type=str,
        action='append',
        help='Adds prefix',
    )
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
        action='append',
        help='Strict variables should exists in os envs',
    )
    parser.add_argument(
        '-s',
        '--source',
        default='',
        type=str,
        help='Source template path, restricts non-prefixed env vars',
    )
    parser.add_argument(
        '--strict-source',
        action='store_true',
        help='All source template variables should exist in os envs',
    )
    return parser


def main() -> NoReturn:
    """
    Runs dump-env script.

    Example::

        This example will dump all environ variables:

        .. code:: bash

            $ dump-env

        This example will dump all environ variables starting with ``PIP_``:

        .. code:: bash

            $ dump-env -p 'PIP_'

        This example will dump all environ variables starting with ``PIP_``
        and update them with variables starting with ``SECRET_``:

        .. code:: bash

            $ dump-env -p 'PIP_' -p 'SECRET_'

        This example will dump everything from ``.env.template`` file
        and all env variables with ``SECRET_`` prefix into a ``.env`` file:

        .. code:: bash

            $ dump-env -p 'SECRET_' -t .env.template > .env

        This example will fail if ``REQUIRED`` does not exist in environ:

        .. code:: bash

            $ dump-env --strict=REQUIRED

        This example will dump everything from a source ``.env.template`` file
        with only env variables that are defined in the file:

        .. code:: bash

            $ dump-env -s .env.template

        This example will fail if any keys in the source template do not exist
        in the environment:

        .. code:: bash

            $ dump-env -s .env.template --strict-source

    """
    args = _create_parser().parse_args()
    strict_vars = set(args.strict) if args.strict else None

    try:
        variables = dumper.dump(
            args.template,
            args.prefix,
            strict_vars,
            args.source,
            args.strict_source,
        )
    except StrictEnvError as exc:
        sys.stderr.write(f'{exc!s}\n')
        sys.exit(1)
    else:
        for env_name, env_value in variables.items():
            if needs_quotes(env_value):
                env_value = f'"{escape(env_value)}"'  # noqa: PLW2901
            sys.stdout.write(f'{env_name}={env_value}\n')
        sys.exit(0)
