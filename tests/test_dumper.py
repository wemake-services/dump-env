# -*- coding: utf-8 -*-

import pytest

from dump_env import dumper
from dump_env.dumper import Dumper


@pytest.mark.usefixtures('monkeypatch', 'env_file')
class TestDump(object):
    """Test Dumper class."""

    def test_with_default_arguments(self, monkeypatch, simple_environ):
        """Dumper without options return unmodified environment variables."""
        monkeypatch.setattr(dumper, 'environ', simple_environ())
        dumper_instance = Dumper()
        dump_result = dumper_instance.dump()

        assert list(dump_result.keys()) == ['a', 'key']
        assert dump_result['key'] == 'value'
        assert dump_result['a'] == 'b'

    def test_with_prefix(self, monkeypatch, simple_environ):
        """Dumper with prefix option should return requested variables."""
        prefix = 'P_'
        monkeypatch.setattr(
            dumper, 'environ', simple_environ(prefix=prefix),
        )
        dumper_instance = Dumper(prefixes=[prefix])
        dump_result = dumper_instance.dump()

        assert len(dump_result.keys()) == 1
        assert dump_result['key'] == 'value'

    def test_with_template(self, monkeypatch, env_file, simple_environ):
        """Dumper with template option return variables for given template."""
        monkeypatch.setattr(dumper, 'environ', simple_environ())
        dumper_instance = Dumper(template=env_file)
        dump_result = dumper_instance.dump()

        assert list(dump_result.keys()) == ['NORMAL_KEY', 'a', 'key']
        assert dump_result['key'] == 'value'
        assert dump_result['a'] == 'b'
        assert dump_result['NORMAL_KEY'] == 'SOMEVALUE'

    def test_with_two_options(self, monkeypatch, env_file, simple_environ):
        """Check both prefix and template options works together."""
        prefix = 'P_'
        monkeypatch.setattr(
            dumper, 'environ', simple_environ(prefix=prefix),
        )
        dumper_instance = Dumper(template=env_file, prefixes=[prefix])
        dump_result = dumper_instance.dump()

        assert list(dump_result.keys()) == ['NORMAL_KEY', 'key']
        assert dump_result['key'] == 'value'
        assert dump_result['NORMAL_KEY'] == 'SOMEVALUE'

    def test_with_multiple_prefixes(self, monkeypatch, simple_environ):
        """With multiple prefixes further prefixed variable replace previous."""
        first_prefix = 'P1_'
        monkeypatch.setattr(
            dumper, 'environ', simple_environ(prefix=first_prefix),
        )
        second_prefix = 'P2_'
        monkeypatch.setattr(
            dumper, 'environ', simple_environ(
                prefix=second_prefix, env_value='another_value',
            ),
        )
        dumper_instance = Dumper(prefixes=[first_prefix, second_prefix])
        dump_result = dumper_instance.dump()

        assert len(dump_result.keys()) == 1
        assert dump_result['key'] == 'another_value'
