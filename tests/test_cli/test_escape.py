import json


def test_quote_escape(monkeypatch, delegator, snapshot):
    """Check that cli escapes."""
    multiline_value = {
        'key': 'value',
        'key2': 'multi\nline\nvalue',
    }
    monkeypatch.setenv('MULTILINE_VALUE', json.dumps(multiline_value, indent=4))

    variables = delegator('dump-env -p MULTILINE_')
    assert variables == snapshot
