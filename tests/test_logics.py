import pytest

from dump_env import dumper


def simple_environ(prefix='', env_value='value'):
    """Returns dict with example environment with given prefix and value."""
    return {
        '{0}key'.format(prefix): env_value,
        'a': 'b',
    }


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


@pytest.mark.usefixtures('env_file')
class TestParse:
    """Test parse function."""

    def test_parse_normal(self, env_file):
        """Ensures that given env keys are present in output."""
        parsed_data = dumper._parse(env_file)  # noqa: WPS437

        assert isinstance(parsed_data, dict)
        assert 'NORMAL_KEY' in parsed_data
        assert parsed_data['NORMAL_KEY'] == 'SOMEVALUE'

    def test_parse_exceptions(self, env_file):
        """Ensures that unknown env keys are not present in output."""
        parsed_data = dumper._parse(env_file)  # noqa: WPS437

        assert isinstance(parsed_data, dict)
        assert 'COMMENTED_KEY' not in parsed_data
        assert 'KEY_WITH_NO_ASSIGNMENT' not in parsed_data


@pytest.mark.usefixtures('env_file')
class TestFill:
    """Test fill function."""

    def test_fill_template_var(self, env_file_with_template):
        """Ensures that given env keys are fill template env var."""
        parsed_data = dumper._parse(env_file_with_template)  # noqa: WPS437
        filled_data = dumper._fill(parsed_data)  # noqa: WPS437
        assert 'VAR_TEMPLATE' in filled_data
        assert filled_data['VAR_TEMPLATE'] == 'value1 value2'

    def test_parse_variable_names(self):
        """Test template variable parser."""
        template = '${FIRST_VALUE} ${SECOND_VALUE}'
        variable_names = dumper._parse_variable_names(template)  # noqa: WPS437
        assert variable_names == ['FIRST_VALUE', 'SECOND_VALUE']

    def test_fill_wrong_template(self, env_file_with_wrong_template):
        """Ensures that an incorrectly filled template is not filled in."""
        parsed_data = dumper._parse(  # noqa: WPS437
            env_file_with_wrong_template,
        )
        filled_data = dumper._fill(parsed_data)  # noqa: WPS437
        assert parsed_data == filled_data


@pytest.mark.usefixtures('monkeypatch', 'env_file')
class TestDump:
    """Test dump function."""

    def test_with_default_arguments(self, monkeypatch):
        """Dumper without options return unmodified environment variables."""
        monkeypatch.setattr(dumper, 'environ', simple_environ())
        dump_result = dumper.dump()

        assert list(dump_result.keys()) == ['a', 'key']
        assert dump_result['key'] == 'value'
        assert dump_result['a'] == 'b'

    def test_with_prefix(self, monkeypatch):
        """Dumper with prefix option should return requested variables."""
        prefix = 'P_'
        monkeypatch.setattr(
            dumper, 'environ', simple_environ(prefix=prefix),
        )
        dump_result = dumper.dump(prefixes=[prefix])

        assert len(dump_result.keys()) == 1
        assert dump_result['key'] == 'value'

    def test_with_template(self, monkeypatch, env_file):
        """Dumper with template option return variables for given template."""
        monkeypatch.setattr(dumper, 'environ', simple_environ())
        dump_result = dumper.dump(template=env_file)

        assert list(dump_result.keys()) == ['NORMAL_KEY', 'a', 'key']
        assert dump_result['key'] == 'value'
        assert dump_result['a'] == 'b'
        assert dump_result['NORMAL_KEY'] == 'SOMEVALUE'

    def test_with_two_options(self, monkeypatch, env_file):
        """Check both prefix and template options works together."""
        prefix = 'P_'
        monkeypatch.setattr(
            dumper, 'environ', simple_environ(prefix=prefix),
        )
        dump_result = dumper.dump(template=env_file, prefixes=[prefix])

        assert list(dump_result.keys()) == ['NORMAL_KEY', 'key']
        assert dump_result['key'] == 'value'
        assert dump_result['NORMAL_KEY'] == 'SOMEVALUE'

    def test_with_multiple_prefixes(self, monkeypatch):
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
        dump_result = dumper.dump(prefixes=[first_prefix, second_prefix])

        assert len(dump_result.keys()) == 1
        assert dump_result['key'] == 'another_value'

    def test_dump_with_fill_argument(self, env_file_with_template):
        """Check fill arguments works."""
        dump_result = dumper.dump(template=env_file_with_template, fill=True)
        assert dump_result['VAR_TEMPLATE'] == 'value1 value2'


@pytest.mark.usefixtures('monkeypatch', 'env_file')
class TestDumpRegression:
    """Test dump function (regression)."""

    def test_same_environ(self, monkeypatch, env_file):
        """Dumper should return unmodified environment variables by default."""
        monkeypatch.setattr(
            dumper, 'environ', same_environ(),
        )
        dump_result = dumper.dump(template=env_file)

        # Should contain the value from env, not from template:
        assert dump_result['NORMAL_KEY'] == 'test'

    def test_multiple_vars_with_prefix(self, monkeypatch, env_file):
        """Dumper with prefix option should return all prefixed variables."""
        monkeypatch.setattr(
            dumper, 'environ', multiple_variables_with_prefix(),
        )
        dump_result = dumper.dump(template=env_file, prefixes=['SECRET_'])

        # Only prefix should be changed, other parts should not:
        assert dump_result['DJANGO_SECRET_KEY'] == 'test'
        assert dump_result['SECRET_VALUE'] == 'value'
