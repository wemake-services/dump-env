# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import environ
from typing import Dict, List, Mapping, Set, Union

ENV_STORE = Dict[str, str]
OS_ENV_STORE = Mapping[str, str]

MISSING_ENV_MESSAGE = 'Environment variables for keys: {0} - does not set'
STRICT_ARGS_ERROR_MESSAGE = 'Either template or strict ' \
                            'variables or both should present in arguments.'


class StrictException(Exception):
    """Exception for strict dumper."""

    def __init__(self, message: str) -> None:
        """Init."""
        self.message = message

    def __str__(self) -> str:
        return self.message


def parse(source: str) -> ENV_STORE:
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


class Dumper(object):

    def __init__(self, template: str='', prefixes: List[str]=None) -> None:
        """
        :type template: string - The path of the `.env` template file,
           use an empty string when there is no template file.
        :type prefixes: List[str] - Prefixes to use only certain env
           variables, could be an empty string to use all available variables.
        """
        self.template = template
        self.prefixes: List[str] = prefixes or []

    def _preload_existing_vars(self) -> Union[OS_ENV_STORE, ENV_STORE]:
        if len(self.prefixes) == 0:
            # If prefix is empty just return all the env variables.
            return environ

        prefixed = {}

        # Prefix is not empty, do the search and replacement:
        for prefix in self.prefixes:
            for env_name, env_value in environ.items():
                if not env_name.startswith(prefix):
                    # Skip vars with no prefix.
                    continue

                prefixed[env_name.replace(prefix, '', 1)] = env_value
        return prefixed

    def _get_template_store(self) -> ENV_STORE:
        if self.template:
            # Parse env values from template file:
            return parse(self.template)
        return {}

    def dump(self) -> 'OrderedDict[str, str]':
        """
        This function is used to dump .env files.

        As a source you can use both:
        1. env.template file (`''` by default)
        2. env vars prefixed with some prefix (no prefixes by default)

        Returns:
            OrderedDict: ordered key-value pairs.

        """
        store: ENV_STORE = {}
        # Parse env values from template file:
        template_store = self._get_template_store()
        # Loading env variables from `os.environ`:
        os_store = self._preload_existing_vars()

        store.update(template_store)
        store.update(os_store)
        # Sort keys and keep them ordered:
        return OrderedDict(sorted(store.items()))


class StrictDumper(Dumper):

    def __init__(self, strict_envs: List[str]=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.strict_envs: List[str] = strict_envs or []

        if not self.template and len(self.strict_envs) == 0:
            raise StrictException(STRICT_ARGS_ERROR_MESSAGE)

    def _check_strict_variables(self, store: Union[ENV_STORE, OS_ENV_STORE],
                                env_names: Set[str]) -> None:
        store_env_names = set(store.keys())

        if not store_env_names.issuperset(env_names):
            missing_env_names = env_names.difference(store)
            error_msg = MISSING_ENV_MESSAGE.format(', '.join(missing_env_names))
            raise StrictException(error_msg)

    def dump(self) -> 'OrderedDict[str, str]':
        """
        This function is used to dump .env files.

        As a source you can use both:
        1. env.template file (`''` by default)
        2. env vars prefixed with some prefix (no prefixes by default)

        Unlike of Dumper.dump this function also checks
        that all strict variables exists in os.environment

        Returns:
            OrderedDict: ordered key-value pairs.

        """
        store: ENV_STORE = {}
        # Parse env values from template file:
        template_store = self._get_template_store()
        # Loading env variables from `os.environ`:
        os_store = self._preload_existing_vars()

        # create set with strict environment variable names
        if len(self.strict_envs) > 0:
            strict_env_names = set(self.strict_envs)
        else:
            strict_env_names = set(template_store.keys())
        # check that all strict environment variable exists in os store
        self._check_strict_variables(os_store, strict_env_names)

        store.update(template_store)
        store.update(os_store)
        # Sort keys and keep them ordered:
        return OrderedDict(sorted(store.items()))
