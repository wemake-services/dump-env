# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import environ
from typing import Dict, List, Mapping, Optional, Set

from dump_env.exceptions import StrictEnvException

Store = Mapping[str, str]


def _parse(source: str) -> Store:
    """
    Reads the source ``.env`` file and load key-values.

    Args:
        source: ``.env`` template filepath

    Returns:
        Store with all keys and values.

    """
    parsed_data = {}

    with open(source) as env_file:
        for line in env_file:
            line = line.strip()  # noqa: WPS440

            if not line or line.startswith('#') or '=' not in line:
                # Ignore comments and lines without assignment.
                continue

            # Remove whitespaces and quotes:
            env_name, env_value = line.split('=', 1)
            env_name = env_name.strip()
            env_value = env_value.strip().strip('\'"')
            parsed_data[env_name] = env_value

    return parsed_data


def _preload_existing_vars(prefix: str) -> Store:
    """Preloads env vars from environ with the given prefix."""
    if not prefix:
        # If prefix is empty just return all the env variables.
        return environ

    prefixed = {}

    # Prefix is not empty, do the search and replacement:
    for env_name, env_value in environ.items():
        if not env_name.startswith(prefix):
            # Skip vars with no prefix.
            continue

        prefixed[env_name.replace(prefix, '', 1)] = env_value

    return prefixed


def _assert_envs_exist(strict_keys: Set[str]) -> None:
    """Checks that all variables from strict keys do exists."""
    missing_keys: List[str] = [
        strict_key
        for strict_key in strict_keys
        if strict_key not in environ
    ]

    if missing_keys:
        raise StrictEnvException(
            'Missing env vars: {0}'.format(', '.join(missing_keys)),
        )


def dump(
    template: str = '',
    prefixes: Optional[List[str]] = None,
    strict_keys: Optional[Set[str]] = None,
) -> Dict[str, str]:
    """
    This function is used to dump .env files.

    As a source you can use both:
    1. env.template file (``''`` by default)
    2. env vars prefixed with some prefix (``''`` by default)

    Args:
        template: The path of the `.env` template file,
           use an empty string when there is no template file.
        prefixes: List of string prefixes to use only certain env
           variables, could be an empty string to use all available variables.

    Returns:
        Ordered key-value pairs of dumped env and template variables.

    Raises:
        StrictEnvException: when some variable from template is missing.

    """
    if prefixes is None:
        prefixes = ['']

    if strict_keys:
        _assert_envs_exist(strict_keys)

    store: Dict[str, str] = {}

    if template:
        # Loading env values from template file:
        store.update(_parse(template))

    # Loading env variables from `os.environ`:
    for prefix in prefixes:
        store.update(_preload_existing_vars(prefix))

    # Sort keys and keep them ordered:
    return OrderedDict(sorted(store.items()))
