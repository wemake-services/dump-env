# -*- coding: utf-8 -*-

import delegator


def test_strict_vars1(monkeypatch):
    """Check that cli works correctly with strict vars."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')
    monkeypatch.setenv('SOM_TT_KEY', '2')

    variables = delegator.run('dump-env -p SOM_TT_ --strict=SOM_TT_KEY')
    assert variables.out == 'KEY=2\nVALUE=1\n'
    assert variables.subprocess.returncode == 0


def test_strict_vars2(monkeypatch):
    """Check that cli works correctly with strict vars."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')
    monkeypatch.setenv('SOM_TT_KEY', '2')

    variables = delegator.run(
        'dump-env -p SOM_TT_ --strict=SOM_TT_KEY --strict=SOM_TT_VALUE',
    )
    assert variables.out == 'KEY=2\nVALUE=1\n'
    assert variables.subprocess.returncode == 0


def test_strict_missing_vars1(monkeypatch):
    """Check that cli raises errors for missing strict keys."""
    variables = delegator.run('dump-env -p SOM_TT_ --strict=SOM_TT_KEY')
    assert variables.out == ''
    assert variables.err == 'Missing env vars: SOM_TT_KEY\n'
    assert variables.subprocess.returncode == 1


def test_strict_missing_vars2(monkeypatch):
    """Check that cli raises errors for missing strict keys."""
    variables = delegator.run(
        'dump-env -p SOM_TT_ --strict=SOM_TT_KEY --strict=SOM_TT_VALUE',
    )
    assert variables.out == ''
    assert 'SOM_TT_VALUE' in variables.err
    assert 'SOM_TT_KEY' in variables.err
    assert variables.subprocess.returncode == 1
