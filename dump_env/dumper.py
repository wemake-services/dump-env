# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import environ
from typing import Dict, List, Mapping, Optional

Store = Mapping[str, str]


def parse(source: str) -> Store:
    """
    Reads the source `.env` file and load key-values.

    Args:
        source (str): `.env` template filepath

    Returns:

    """
    parsed_data = {}

    with open(source) as env_file:
        for line in env_file:
            line = line.strip()

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


def dump(
    template: str = '',
    prefixes: Optional[List[str]] = None,
) -> Dict[str, str]:
    """
    This function is used to dump .env files.

    As a source you can use both:
    1. env.template file (`''` by default)
    2. env vars prefixed with some prefix (`''` by default)

    Args:
        template (str): The path of the `.env` template file,
           use an empty string when there is no template file.
        prefixes (List[str]): List of string prefixes to use only certain env
           variables, could be an empty string to use all available variables.

    Returns:
        OrderedDict: ordered key-value pairs.

    """
    if prefixes is None:
        prefixes = ['']
    store: Dict[str, str] = {}

    if template:
        # Loading env values from template file:
        store.update(parse(template))

    # Loading env variables from `os.environ`:
    for prefix in prefixes:
        store.update(_preload_existing_vars(prefix))

    # Sort keys and keep them ordered:
    return OrderedDict(sorted(store.items()))
