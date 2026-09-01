from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import DelegatorFactory


def test_interpolate(
    monkeypatch: pytest.MonkeyPatch,
    delegator: 'DelegatorFactory',
) -> None:
    """Check that cli expands ${VAR} and $VAR references between values."""
    monkeypatch.setenv('SOME_TT_HOST', 'localhost')
    monkeypatch.setenv('SOME_TT_URL1', '${HOST}:123/${MISSING_VALUE}')
    monkeypatch.setenv('SOME_TT_URL2', '$HOST:123/$MISSING_VALUE')
    monkeypatch.setenv('SOME_TT_URL3', '${HOST}_SUFFIX:$HOST_SUFFIX')

    variables = delegator('dump-env -p SOME_TT_ --interpolate')
    assert 'URL1=localhost:123/${MISSING_VALUE}\n' in variables
    assert 'URL2=localhost:123/$MISSING_VALUE\n' in variables
    assert 'URL3=localhost_SUFFIX:$HOST_SUFFIX\n' in variables


def test_strict_interpolate_missing(
    monkeypatch: pytest.MonkeyPatch,
    delegator: 'DelegatorFactory',
) -> None:
    """Check that cli fails on undefined references in strict mode."""
    monkeypatch.setenv('SOME_TT_HOST', 'localhost')
    monkeypatch.setenv('SOME_TT_URL', '${HOST}:123/${MISSING_VALUE}')

    variables = delegator(
        'dump-env -p SOME_TT_ --interpolate --strict-interpolate',
    )
    assert variables == (1, "Unresolved references in: URL ('MISSING_VALUE')\n")
