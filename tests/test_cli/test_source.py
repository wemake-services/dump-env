def test_source_vars(monkeypatch, env_file, delegator):
    """Check that cli shows only source variables."""
    monkeypatch.setenv('NORMAL_KEY', '1')
    monkeypatch.setenv('EXTRA_VALUE', '2')

    variables = delegator('dump-env -s {0}'.format(env_file))
    assert variables == 'NORMAL_KEY=1\n'


def test_source_prefixes(monkeypatch, env_file, delegator):
    """Check that cli allows prefixes with source."""
    monkeypatch.setenv('NORMAL_KEY', '1')
    monkeypatch.setenv('EXTRA_VALUE', '2')

    variables = delegator('dump-env -p EXTRA_ -s {0}'.format(env_file))
    assert variables == 'NORMAL_KEY=1\nVALUE=2\n'


def test_source_strict(monkeypatch, env_file, delegator):
    """Check that cli works correctly with strict-source."""
    monkeypatch.setenv('NORMAL_KEY', '1')
    monkeypatch.setenv('EXTRA_VALUE', '2')

    variables = delegator(
        'dump-env --strict-source -s {0}'.format(env_file),
    )
    assert variables == 'NORMAL_KEY=1\n'


def test_source_strict_fail(monkeypatch, env_file, delegator):
    """Check that cli works correctly with strict-source missing keys."""
    monkeypatch.setenv('EXTRA_VALUE', '2')

    variables = delegator(
        'dump-env --strict-source -s {0}'.format(env_file),
    )
    assert variables == (1, 'Missing env vars: NORMAL_KEY\n')
