import json

import pytest
from click.testing import CliRunner

from auctor.cli.main import main


@pytest.mark.parametrize(
    ("args", "mandate"),
    [
        (["issue", "--subject", "agent"], None),
        (
            ["run", "--mandate-file", "mandate.json", "--tool", "read_file"],
            {"id": "test", "capabilities": {"tools": ["read_file"]}},
        ),
    ],
)
def test_missing_identity_shows_helpful_error(
    args, mandate, monkeypatch, tmp_path
):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    if mandate is not None:
        with open("mandate.json", "w", encoding="utf-8") as file:
            json.dump(mandate, file)

    result = runner.invoke(main, args)

    assert result.exit_code == 1
    assert result.output.strip() == (
        "Error: Identity not found. Run 'auctor init' first."
    )
    assert "Traceback" not in result.output
