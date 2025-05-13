import json


def test_quote_escape(monkeypatch, delegator, snapshot):
    """Check that cli works with multiline inputs"""
    monkeypatch.setenv('MULTILINE_VALUE', json.dumps({
        'key': 'value',
        'key2': 'multi\nline\nvalue',
    }, indent=4))

    variables = delegator('dump-env -p MULTILINE_')
    assert variables == snapshot


def test_simple_multiline(monkeypatch, delegator, snapshot):
    """Check that cli works with multiline inputs"""
    monkeypatch.setenv('MULTILINE_VALUE', '1\n2\n3')

    variables = delegator('dump-env -p MULTILINE_')
    assert variables == snapshot
