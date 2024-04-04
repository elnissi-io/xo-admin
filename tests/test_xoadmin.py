import pytest
import yaml
from click.testing import CliRunner

from xoadmin.cli.cli import cli
from xoadmin.cli.config import config_set  # Import your Click group or command
from xoadmin.cli.utils import DEFAULT_CONFIG_PATH, convert_value


@pytest.fixture
def runner():
    return CliRunner()


def test_config_set_full_command(runner: CliRunner, tmpdir):
    config_file = tmpdir.join("config.yaml")
    # Assume a basic config structure for the test
    config_file.write(
        """
        xoa:
          host: http://localhost
          verify_ssl: false
          username: admin
          password: secret
        """
    )

    result = runner.invoke(
        cli,
        ["config", "set", "verify_ssl", "true", "--config-path", str(config_file)],
    )
    assert result.exit_code == 0
    assert "Updated configuration" in result.output

    with open(config_file, "r") as f:
        config_content = yaml.safe_load(f)
        assert config_content["xoa"]["verify_ssl"] is True


@pytest.mark.parametrize(
    "input_value, target_type, expected_output",
    [
        ("true", "boolean", True),
        ("1", "integer", 1),
        ("3.14", "number", 3.14),
        ("sample", "string", "sample"),
        ("true", bool, True),  # Testing direct Python type
    ],
)
def test_convert_value(input_value, target_type, expected_output):
    assert convert_value(input_value, target_type) == expected_output


def test_convert_value_with_unsupported_type():
    with pytest.raises(ValueError):
        convert_value("test", "unsupported_type")


def test_config_set_success(runner, tmpdir):
    config_file = tmpdir.join("config.yaml")
    # Assume a basic config structure for the test
    config_file.write(
        """
    xoa:
      host: http://localhost
      verify_ssl: false
      username: admin
      password: secret
    """
    )

    result = runner.invoke(
        cli,
        ["config", "set", "verify_ssl", "true", "--config-path", str(config_file)],
    )
    assert result.exit_code == 0
    assert "Updated configuration 'verify_ssl' with new value." in result.output

    # Optionally, load the config file and assert the updated value
