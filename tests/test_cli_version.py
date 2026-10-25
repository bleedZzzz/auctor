from click.testing import CliRunner

from auctor.cli.main import main


def test_main_version_option_prints_package_version():
    result = CliRunner().invoke(main, ["--version"])

    assert result.exit_code == 0
    assert "version 0.1.0" in result.output
