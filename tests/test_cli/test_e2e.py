import json
from pathlib import Path
from dotenv import dotenv_values


def test_complex_variables_compatibility(monkeypatch, tmpdir, delegator):
    """Test that dump-env output is compatible with python-dotenv loading."""
    # Set up complex environment variables
    complex_vars = {
        'MULTILINE_VAR': 'line1\nline2\nline3',
        'SPECIAL_CHARS': '!@#$%^&*()_+{}|:"<>?',
        'EQUALS_IN_VALUE': 'key=value',
        'QUOTED_VAR': '"double quoted" and \'single quoted\'',
        'SPACES_VAR': '  spaces  around  ',
        'EMPTY_VAR': '',
        'JSON_VAR': json.dumps({
            'key': 'value',
            'key2': 'multi\nline\nvalue',
        }, indent=4),
        'BACKSLASH_VAR': '\\\\',
    }

    prefix = 'MY_PREFIX_'

    # Set environment variables
    for key, value in complex_vars.items():
        monkeypatch.setenv(f'{prefix}{key}', value)

    # Create temporary .env file
    env_file = Path(tmpdir) / '.env'

    # Dump environment variables to file
    delegator(f'dump-env -p {prefix} > {env_file}')

    # Load variables using python-dotenv
    loaded_vars = dotenv_values(env_file)

    # Compare the loaded variables with original ones
    for key, value in complex_vars.items():
        assert key in loaded_vars, f"Key {key} not found in loaded variables"
        assert loaded_vars[key] == value, f"Value mismatch for key {key}"
