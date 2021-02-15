import pytest


@pytest.fixture(scope='session')
def env_file():
    """Returns path for example env file."""
    return './tests/fixtures/.env.example'
