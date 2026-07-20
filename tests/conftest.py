import subprocess
from typing import Protocol, TypeAlias

import pytest

CommandResult: TypeAlias = str | tuple[int, str]


class DelegatorFactory(Protocol):
    """Protocol for the test command runner fixture."""

    def __call__(self, command: str) -> CommandResult:
        """Runs a shell command and returns stdout or failure details."""


@pytest.fixture(scope='session')
def env_file() -> str:
    """Returns path for example env file."""
    return './tests/fixtures/.env.example'


@pytest.fixture(scope='session')
def delegator() -> DelegatorFactory:
    """Mimics the old `delegator` dependency's API."""

    def factory(command: str) -> CommandResult:
        try:
            return subprocess.check_output(  # ruff:ignore[subprocess-popen-with-shell-equals-true]
                command,
                universal_newlines=True,
                shell=True,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:
            return (exc.returncode, exc.stderr)

    return factory
