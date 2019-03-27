# -*- coding: utf-8 -*-

import pytest

import dump_env
from dump_env import dump, parse


@pytest.mark.usefixtures('env_file')
class TestParse(object):
    def test_parse_normal(self, env_file):
        parsed_data = parse(env_file)

        assert isinstance(parsed_data, dict)
        assert 'NORMAL_KEY' in parsed_data
        assert parsed_data['NORMAL_KEY'] == 'SOMEVALUE'

    def test_parse_exceptions(self, env_file):
        parsed_data = parse(env_file)

        assert isinstance(parsed_data, dict)
        assert 'COMMENTED_KEY' not in parsed_data
        assert 'KEY_WITH_NO_ASSIGNMENT' not in parsed_data


@pytest.mark.usefixtures('monkeypatch', 'env_file')
class TestDump(object):
    @staticmethod
    def simple_environ(prefix='', value='value'):
        return {
            '{0}key'.format(prefix): value,
            'a': 'b',
        }

    def test_with_default_arguments(self, monkeypatch):
        monkeypatch.setattr(dump_env, 'environ', self.simple_environ())
        result = dump()

        assert list(result.keys()) == ['a', 'key']
        assert result['key'] == 'value'
        assert result['a'] == 'b'

    def test_with_prefix(self, monkeypatch):
        prefix = 'P_'
        monkeypatch.setattr(
            dump_env, 'environ', self.simple_environ(prefix=prefix),
        )
        result = dump(prefixes=[prefix])

        assert len(result.keys()) == 1
        assert result['key'] == 'value'

    def test_with_template(self, monkeypatch, env_file):
        monkeypatch.setattr(dump_env, 'environ', self.simple_environ())
        result = dump(template=env_file)

        assert list(result.keys()) == ['NORMAL_KEY', 'a', 'key']
        assert result['key'] == 'value'
        assert result['a'] == 'b'
        assert result['NORMAL_KEY'] == 'SOMEVALUE'

    def test_with_two_options(self, monkeypatch, env_file):
        prefix = 'P_'
        monkeypatch.setattr(
            dump_env, 'environ', self.simple_environ(prefix=prefix),
        )
        result = dump(template=env_file, prefixes=[prefix])

        assert list(result.keys()) == ['NORMAL_KEY', 'key']
        assert result['key'] == 'value'
        assert result['NORMAL_KEY'] == 'SOMEVALUE'

    def test_with_multiple_prefixes(self, monkeypatch):
        first_prefix = 'P1_'
        monkeypatch.setattr(
            dump_env, 'environ', self.simple_environ(prefix=first_prefix),
        )
        second_prefix = 'P2_'
        monkeypatch.setattr(
            dump_env, 'environ', self.simple_environ(
                prefix=second_prefix, value='another_value',
            ),
        )
        result = dump(prefixes=[first_prefix, second_prefix])

        assert len(result.keys()) == 1
        assert result['key'] == 'another_value'


@pytest.mark.usefixtures('monkeypatch', 'env_file')
class TestDumpRegression(object):
    @staticmethod
    def same_environ():
        return {
            'NORMAL_KEY': 'test',
        }

    @staticmethod
    def multiple_prefix():
        return {
            'SECRET_DJANGO_SECRET_KEY': 'test',
            'SECRET_SECRET_VALUE': 'value',
        }

    def test_same_environ(self, monkeypatch, env_file):
        monkeypatch.setattr(
            dump_env, 'environ', self.same_environ(),
        )
        result = dump(template=env_file)

        # Should contain the value from env, not from template:
        assert result['NORMAL_KEY'] == 'test'

    def test_multiple_prefix(self, monkeypatch, env_file):
        monkeypatch.setattr(
            dump_env, 'environ', self.multiple_prefix(),
        )
        result = dump(template=env_file, prefixes=['SECRET_'])

        # Only prefix should be changed, other parts should not:
        assert result['DJANGO_SECRET_KEY'] == 'test'
        assert result['SECRET_VALUE'] == 'value'
