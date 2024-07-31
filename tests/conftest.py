import subprocess

import pytest


@pytest.fixture(scope='session')
def env_file():
    """Returns path for example env file."""
    return './tests/fixtures/.env.example'


@pytest.fixture(scope='session')
def env_file_with_template():
    """Returns path for example env file with template var."""
    return './tests/fixtures/.env_with_template.example'


@pytest.fixture(scope='session')
def delegator():
    """Mimics the old `delegator` dependency's API."""
    def factory(command):
        try:
            return subprocess.check_output(
                command,
                universal_newlines=True,
                shell=True,  # noqa: S602
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:
            return (exc.returncode, exc.stderr)
    return factory
