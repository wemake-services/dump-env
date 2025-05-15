from pathlib import Path


def test_simple_usage(monkeypatch, delegator):
    """Check that cli shows prefixed variables."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    variables = delegator('dump-env -p SOM_TT_')
    assert variables == 'VALUE=1\n'


def test_both_options(monkeypatch, env_file, delegator):
    """
    Check with template and prefix.

    CLI must show all prefixed variables by template.
    """
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    variables = delegator(f'dump-env -p SOM_TT_ -t {env_file}')
    assert variables == 'NORMAL_KEY=SOMEVALUE\nVALUE=1\n'


def test_multiple_prefixes(monkeypatch, delegator):
    """
    Check that CLI with multiple prefixes.

    CLI must show all prefixed variables correctly.
    """
    monkeypatch.setenv('SOM_TT_VALUE', '1')
    monkeypatch.setenv('ANOTHER_TT_VALUE', '2')

    variables = delegator('dump-env -p SOM_TT_ -p ANOTHER_TT_')
    assert variables == 'VALUE=2\n'


def test_simple_usage_file_output(monkeypatch, tmpdir, delegator):
    """Check that CLI puts prefixed variables into file correctly."""
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    filename = tmpdir.mkdir('tests').join('.env').strpath

    delegator(f'dump-env -p SOM_TT_ > {filename}')
    assert Path(filename).read_text(encoding='utf-8') == 'VALUE=1\n'
