# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope='session')
def env_file():
    return './tests/fixtures/.env.example'
