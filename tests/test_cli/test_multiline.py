def test_simple_multiline(monkeypatch, delegator):
    """Check that cli works with multiline inputs"""
    monkeypatch.setenv('MULTILINE_VALUE', '1\n2\n3')

    variables = delegator('dump-env -p MULTILINE_')
    assert variables == '''VALUE="1
2
3"
'''
