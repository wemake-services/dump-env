from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import DelegatorFactory


def test_missing_template_file_exits_cleanly(
    delegator: 'DelegatorFactory',
) -> None:
    """Missing template file must fail with a one-line error, no traceback."""
    result = delegator('dump-env -t ./does-not-exist.env')

    assert isinstance(result, tuple)
    status, stderr = result
    assert status == 1
    assert 'does-not-exist.env' in stderr
    assert 'Traceback' not in stderr


@pytest.mark.parametrize('flag', ['-t', '-s'])
def test_missing_template_and_source_files_exit_cleanly(
    delegator: 'DelegatorFactory',
    flag: str,
) -> None:
    """Both --template and --source must handle a missing file the same way."""
    result = delegator(f'dump-env {flag} ./does-not-exist.env')

    assert isinstance(result, tuple)
    status, stderr = result
    assert status == 1
    assert 'does-not-exist.env' in stderr
    assert 'Traceback' not in stderr
