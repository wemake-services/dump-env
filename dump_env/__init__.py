# -*- coding: utf-8 -*-

from os import environ
from collections import OrderedDict


def parse(source):
    """
    Reads the source `.env` file and load key-values.

    Args:
        source (str): `.env` template filepath

    Returns:

    """
    parsed_data = {}

    with open(source) as file_:
        for line in file_:
            line = line.strip()

            if not line or line.startswith('#') or '=' not in line:
                # Ignore comments and lines without assignment.
                continue

            # Remove whitespaces and quotes:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('\'"')
            parsed_data[key] = value

    return parsed_data


def _preload_existing_vars(prefix):
    if not prefix:
        # If prefix is empty just return all the env variables.
        return environ

    prefixed = {}

    # Prefix is not empty, do the search and replacement:
    for key, value in environ.items():
        if not key.startswith(prefix):
            # Skip vars with no prefix.
            continue

        prefixed[key.replace(prefix, '', 1)] = value

    return prefixed


def dump(template='', prefix=''):
    """
    This function is used to dump .env files.

    As a source you can use both:
    1. env.template file (`''` by default)
    2. env vars prefixed with some prefix (`''` by default)

    Args:
        template (str): The path of the `.env` template file,
           use an empty string when there is no template file.
        prefix (str): String prefix to use only certain env
           variables, could be an empty string to use all available variables.

    Returns:
        OrderedDict: ordered key-value pairs.

    """
    store = {}

    if template:
        # Loading env values from template file:
        store.update(parse(template))

    # Loading env variables from `os.environ`:
    store.update(_preload_existing_vars(prefix))

    # Sort keys and keep them ordered:
    return OrderedDict(sorted(store.items()))
