# -*- coding: utf-8 -*-

import pytest

from dump_env import dumper
from dump_env.dumper import Dumper, parse


@pytest.mark.usefixtures('env_file')
class TestParse(object):
    """Test parse function."""

    def test_parse_normal(self, env_file):
        """Ensures that given env keys are present in output."""
        parsed_data = parse(env_file)

        assert isinstance(parsed_data, dict)
        assert 'NORMAL_KEY' in parsed_data
        assert parsed_data['NORMAL_KEY'] == 'SOMEVALUE'

    def test_parse_exceptions(self, env_file):
        """Ensures that unknown env keys are not present in output."""
        parsed_data = parse(env_file)

        assert isinstance(parsed_data, dict)
        assert 'COMMENTED_KEY' not in parsed_data
        assert 'KEY_WITH_NO_ASSIGNMENT' not in parsed_data


def same_environ():
    """Returns dict with example environment with given prefix and value."""
    return {
        'NORMAL_KEY': 'test',
    }


def multiple_variables_with_prefix():
    """Returns dict with environment with multiple prefixed variables."""
    return {
        'SECRET_DJANGO_SECRET_KEY': 'test',
        'SECRET_SECRET_VALUE': 'value',
    }


@pytest.mark.usefixtures('monkeypatch', 'env_file')
class TestDumpRegression(object):
    """Test dump function (regression)."""

    def test_same_environ(self, monkeypatch, env_file):
        """Dumper should return unmodified environment variables by default."""
        monkeypatch.setattr(
            dumper, 'environ', same_environ(),
        )
        dumper_instance = Dumper(template=env_file)
        dump_result = dumper_instance.dump()

        # Should contain the value from env, not from template:
        assert dump_result['NORMAL_KEY'] == 'test'

    def test_multiple_vars_with_prefix(self, monkeypatch, env_file):
        """Dumper with prefix option should return all prefixed variables."""
        monkeypatch.setattr(
            dumper, 'environ', multiple_variables_with_prefix(),
        )
        dumper_instance = Dumper(template=env_file, prefixes=['SECRET_'])
        dump_result = dumper_instance.dump()

        # Only prefix should be changed, other parts should not:
        assert dump_result['DJANGO_SECRET_KEY'] == 'test'
        assert dump_result['SECRET_VALUE'] == 'value'
