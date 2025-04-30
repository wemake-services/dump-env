import json


def test_quote_escape(monkeypatch, delegator):
    """Check that cli works with multiline inputs"""
    monkeypatch.setenv('MULTILINE_VALUE', json.dumps({
        'key': 'value',
        'key2': 'multi\nline\nvalue',
    }, indent=4))

    variables = delegator('dump-env -p MULTILINE_')
    assert variables == '''VALUE="{
    \\"key\\": \\"value\\",
    \\"key2\\": \\"multi\\\\nline\\\\nvalue\\"
}"
'''
