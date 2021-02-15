import delegator


def test_source_vars(monkeypatch, env_file):
    """Check that cli shows only source variables."""
    monkeypatch.setenv('NORMAL_KEY', '1')
    monkeypatch.setenv('EXTRA_VALUE', '2')

    variables = delegator.run('dump-env -s {0}'.format(env_file))
    assert variables.out == 'NORMAL_KEY=1\n'
    assert variables.subprocess.returncode == 0


def test_source_prefixes(monkeypatch, env_file):
    """Check that cli allows prefixes with source."""
    monkeypatch.setenv('NORMAL_KEY', '1')
    monkeypatch.setenv('EXTRA_VALUE', '2')

    variables = delegator.run('dump-env -p EXTRA_ -s {0}'.format(env_file))
    assert variables.out == 'NORMAL_KEY=1\nVALUE=2\n'
    assert variables.subprocess.returncode == 0


def test_source_strict(monkeypatch, env_file):
    """Check that cli works correctly with strict-source."""
    monkeypatch.setenv('NORMAL_KEY', '1')
    monkeypatch.setenv('EXTRA_VALUE', '2')

    variables = delegator.run(
        'dump-env --strict-source -s {0}'.format(env_file),
    )
    assert variables.out == 'NORMAL_KEY=1\n'
    assert variables.subprocess.returncode == 0


def test_source_strict_fail(monkeypatch, env_file):
    """Check that cli works correctly with strict-source missing keys."""
    monkeypatch.setenv('EXTRA_VALUE', '2')

    variables = delegator.run(
        'dump-env --strict-source -s {0}'.format(env_file),
    )
    assert variables.err == 'Missing env vars: NORMAL_KEY\n'
    assert variables.subprocess.returncode == 1
