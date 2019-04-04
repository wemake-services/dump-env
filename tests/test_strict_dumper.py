# -*- coding: utf-8 -*-

import pytest

from dump_env import dumper
from dump_env.dumper import StrictDumper, StrictException


def strict_environ(prefix='', env_value='value'):
    """Returns environment for strict template."""
    return {
        '{0}KEY'.format(prefix): env_value,
        'a': 'b',
    }


def empty_environ():
    """Returns empty environment representation."""
    return {}


@pytest.mark.usefixtures('monkeypatch', 'env_file')
class TestStrictDump(object):
    """Test StrictDumper class."""

    def test_with_default_arguments(self):
        """Strict Dumper without options throw an error."""
        with pytest.raises(StrictException):
            StrictDumper(strict_envs=[])

    def test_with_prefix(self):
        """Strict Dumper only with prefix throw an error."""
        with pytest.raises(StrictException):
            StrictDumper(prefixes=['P_'])

    def test_with_template(self, monkeypatch, env_file):
        """
        Strict Dumper with template option.

        Should check all variables from template exists.
        """
        monkeypatch.setattr(dumper, 'environ', strict_environ(prefix='NORMAL_'))
        dumper_instance = StrictDumper(template=env_file)
        dump_result = dumper_instance.dump()

        assert list(dump_result.keys()) == ['NORMAL_KEY', 'a']
        assert dump_result['a'] == 'b'
        assert dump_result['NORMAL_KEY'] == 'value'

    def test_with_template_without_os_variables(self, monkeypatch, env_file):
        """
        Strict Dumper with template option.

        Should check all variables from template exists.
        """
        monkeypatch.setattr(dumper, 'environ', empty_environ())
        dumper_instance = StrictDumper(template=env_file)
        with pytest.raises(StrictException):
            dumper_instance.dump()

    def test_with_strict_envs(self, monkeypatch, simple_environ):
        """Strict dumper with given variables should check them exists."""
        monkeypatch.setattr(dumper, 'environ', simple_environ())
        dumper_instance = StrictDumper(strict_envs=['key'])
        dump_result = dumper_instance.dump()

        assert dump_result == {'key': 'value', 'a': 'b'}
