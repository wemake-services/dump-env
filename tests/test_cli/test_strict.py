def test_strict_vars1(monkeypatch, delegator):
    """Check that cli works correctly with strict vars."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')
    monkeypatch.setenv('SOM_TT_KEY', '2')

    variables = delegator('dump-env -p SOM_TT_ --strict=SOM_TT_KEY')
    assert variables == 'KEY=2\nVALUE=1\n'


def test_strict_vars2(monkeypatch, delegator):
    """Check that cli works correctly with strict vars."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')
    monkeypatch.setenv('SOM_TT_KEY', '2')

    variables = delegator(
        'dump-env -p SOM_TT_ --strict=SOM_TT_KEY --strict=SOM_TT_VALUE',
    )
    assert variables == 'KEY=2\nVALUE=1\n'


def test_strict_missing_vars1(delegator):
    """Check that cli raises errors for missing strict keys."""
    variables = delegator('dump-env -p SOM_TT_ --strict=SOM_TT_KEY')
    assert variables == (1, 'Missing env vars: SOM_TT_KEY\n')


def test_strict_missing_vars2(delegator):
    """Check that cli raises errors for missing strict keys."""
    variables = delegator(
        'dump-env -p SOM_TT_ --strict=SOM_TT_KEY --strict=SOM_TT_VALUE',
    )
    assert variables[0] == 1
    variables_err = variables[1]
    assert 'SOM_TT_VALUE' in variables_err
    assert 'SOM_TT_KEY' in variables_err
