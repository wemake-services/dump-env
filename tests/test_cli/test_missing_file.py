from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tests.conftest import DelegatorFactory


def test_missing_template_reports_clean_error(
    delegator: 'DelegatorFactory',
) -> None:
    """Missing template file must be a clean error, not a traceback."""
    result = delegator('dump-env -t does-not-exist.env')

    assert isinstance(result, tuple)
    code, stderr = result
    assert code == 1
    assert 'does-not-exist.env' in stderr
    assert 'Traceback' not in stderr


def test_missing_source_reports_clean_error(
    delegator: 'DelegatorFactory',
) -> None:
    """Missing source file must be a clean error, not a traceback."""
    result = delegator('dump-env -s does-not-exist.env')

    assert isinstance(result, tuple)
    code, stderr = result
    assert code == 1
    assert 'does-not-exist.env' in stderr
    assert 'Traceback' not in stderr
