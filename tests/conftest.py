# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope='session')
def env_file():
    """Returns path for example env file."""
    return './tests/fixtures/.env.example'


@pytest.fixture()
def simple_environ():
    """Returns dict with example environment with given prefix and value."""
    def inner(prefix='', env_value='value'):  # noqa: Z430 it's a fabric
        return {
            '{0}key'.format(prefix): env_value,
            'a': 'b',
        }
    return inner
