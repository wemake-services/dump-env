# -*- coding: utf-8 -*-

import delegator


def test_help_option():
    """Check that cli shows help."""
    variables = delegator.run('dump-env --help')
    assert 'show this help message and exit' in variables.out
    assert '--template TEMPLATE' in variables.out
    assert '--prefix PREFIX' in variables.out
    assert variables.subprocess.returncode == 0


def test_simple_usage(monkeypatch):
    """Check that cli shows prefixed variables."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    variables = delegator.run('dump-env -p SOM_TT_')
    assert variables.out == 'VALUE=1\n'


def test_both_options(monkeypatch, env_file):
    """
    Check with template and prefix.

    CLI must show all prefixed variables by template.
    """
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    variables = delegator.run('dump-env -p SOM_TT_ -t {0}'.format(env_file))
    assert variables.out == 'NORMAL_KEY=SOMEVALUE\nVALUE=1\n'


def test_multiple_prefixes(monkeypatch):
    """
    Check that CLI with multiple prefixes.

    CLI must show all prefixed variables correctly.
    """
    monkeypatch.setenv('SOM_TT_VALUE', '1')
    monkeypatch.setenv('ANOTHER_TT_VALUE', '2')

    variables = delegator.run('dump-env -p SOM_TT_ -p ANOTHER_TT_')
    assert variables.out == 'VALUE=2\n'


def test_simple_usage_file_output(monkeypatch, tmpdir):
    """Check that CLI puts prefixed variables into file correctly."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    filename = tmpdir.mkdir('tests').join('.env').strpath

    delegator.run('dump-env -p SOM_TT_ > {0}'.format(filename))

    with open(filename) as env_file:
        assert env_file.read() == 'VALUE=1\n'


def test_strict_vars(monkeypatch):
    """Check that cli works correctly with strict vars."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')
    monkeypatch.setenv('SOM_TT_KEY', '2')

    variables = delegator.run('dump-env -p SOM_TT_ --strict=SOM_TT_KEY')
    assert variables.out == 'KEY=2\nVALUE=1\n'
    assert variables.subprocess.returncode == 0

    variables = delegator.run(
        'dump-env -p SOM_TT_ --strict=SOM_TT_KEY --strict=SOM_TT_VALUE',
    )
    assert variables.out == 'KEY=2\nVALUE=1\n'
    assert variables.subprocess.returncode == 0


def test_strict_missing_vars(monkeypatch):
    """Check that cli raises errors for missing strict keys."""
    variables = delegator.run('dump-env -p SOM_TT_ --strict=SOM_TT_KEY')
    assert variables.out == 'Missing env vars: SOM_TT_KEY\n'
    assert variables.subprocess.returncode == 1

    variables = delegator.run(
        'dump-env -p SOM_TT_ --strict=SOM_TT_KEY --strict=SOM_TT_VALUE',
    )
    assert 'SOM_TT_VALUE' in variables.out
    assert 'SOM_TT_KEY' in variables.out
    assert variables.subprocess.returncode == 1
