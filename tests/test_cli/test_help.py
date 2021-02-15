import delegator


def test_help_option():
    """Check that cli shows help."""
    variables = delegator.run('dump-env --help')
    assert 'show this help message and exit' in variables.out
    assert '--template TEMPLATE' in variables.out
    assert '--prefix PREFIX' in variables.out
    assert '--strict' in variables.out
    assert variables.subprocess.returncode == 0
