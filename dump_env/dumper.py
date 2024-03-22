from collections import OrderedDict
from os import environ
from typing import Dict, Final, List, Mapping, Optional, Set

from dump_env.exceptions import StrictEnvError

Store = Mapping[str, str]

EMPTY_STRING: Final = ''


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


def _preload_specific_vars(env_keys: Set[str]) -> Store:
    """Preloads env vars from environ in the given set."""
    specified = {}

    for env_name, env_value in environ.items():
        if env_name not in env_keys:
            # Skip vars that have not been requested.
            continue

        specified[env_name] = env_value

    return specified


def _assert_envs_exist(strict_keys: Set[str]) -> None:
    """Checks that all variables from strict keys do exists."""
    missing_keys: List[str] = [
        strict_key
        for strict_key in strict_keys
        if strict_key not in environ
    ]

    if missing_keys:
        raise StrictEnvError(
            'Missing env vars: {0}'.format(', '.join(missing_keys)),
        )


def _source(source: str, strict_source: bool) -> Store:
    """Applies vars and assertions from source template ``.env`` file."""
    sourced: Dict[str, str] = {}
    sourced.update(_parse(source))

    if strict_source:
        _assert_envs_exist(set(sourced.keys()))

    sourced.update(_preload_specific_vars(set(sourced.keys())))
    return sourced


def dump(
    template: str = EMPTY_STRING,
    prefixes: Optional[List[str]] = None,
    strict_keys: Optional[Set[str]] = None,
    source: str = EMPTY_STRING,
    strict_source: bool = False,
) -> Dict[str, str]:
    """
    This function is used to dump ``.env`` files.

    As a source you can use both:
    1. env.template file (``''`` by default)
    2. env vars prefixed with some prefix (``''`` by default)

    Args:
        template: The path of the ``.env`` template file,
           use an empty string when there is no template file.

        prefixes: List of string prefixes to use only certain env
           variables, could be an empty string to use all available variables.

        strict_keys: List of keys that must be presented in env vars.

        source: The path of the ``.env`` template file,
           defines the base list of env vars that should be checked,
           disables the fetching of non-prefixed env vars,
           use an empty string when there is no source file.

        strict_source: Whether all keys in source template must also be
           presented in env vars.

    Returns:
        Ordered key-value pairs of dumped env and template variables.

    Raises:
        StrictEnvError: when some variable from template is missing.

    """
    if prefixes is None:
        prefixes = [] if source else [EMPTY_STRING]

    if strict_keys:
        _assert_envs_exist(strict_keys)

    store: Dict[str, str] = {}

    if source:
        # Loading env values from source template file:
        store.update(_source(source, strict_source))

    if template:
        # Loading env values from template file:
        store.update(_parse(template))

    # Loading env variables from `os.environ`:
    for prefix in prefixes:
        store.update(_preload_existing_vars(prefix))

    # Sort keys and keep them ordered:
    return OrderedDict(sorted(store.items()))
