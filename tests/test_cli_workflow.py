import glob
import json
from click.testing import CliRunner

from auctor.cli.main import main


def test_issue_creates_mandate_file(monkeypatch, tmp_path):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    init_res = runner.invoke(main, ["init"])
    assert init_res.exit_code == 0

    issue_res = runner.invoke(
        main, ["issue", "--subject", "agent_1", "--tool", "read_file"]
    )
    assert issue_res.exit_code == 0
    assert "Mandate saved to mandate_" in issue_res.output

    mandate_files = glob.glob("mandate_*.json")
    assert len(mandate_files) == 1
    with open(mandate_files[0], "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["subject"] == "agent_1"
    assert "read_file" in data["capabilities"]["tools"]
    assert "signature" in data


def test_run_exit_codes(monkeypatch, tmp_path):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    runner.invoke(main, ["init"])
    runner.invoke(
        main, ["issue", "--subject", "agent_1", "--tool", "read_file"]
    )
    mandate_file = glob.glob("mandate_*.json")[0]

    # Denied tool
    denied_res = runner.invoke(
        main, ["run", "--mandate-file", mandate_file, "--tool", "delete_file"]
    )
    assert denied_res.exit_code == 1
    assert "Denied" in denied_res.output

    # Authorized tool
    auth_res = runner.invoke(
        main, ["run", "--mandate-file", mandate_file, "--tool", "read_file"]
    )
    assert auth_res.exit_code == 0
    assert "Action authorized" in auth_res.output


def test_verify_exit_codes(monkeypatch, tmp_path):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    runner.invoke(main, ["init"])
    runner.invoke(
        main, ["issue", "--subject", "agent_1", "--tool", "read_file"]
    )
    mandate_file = glob.glob("mandate_*.json")[0]
    runner.invoke(
        main, ["run", "--mandate-file", mandate_file, "--tool", "read_file"]
    )
    receipt_file = glob.glob("receipt_*.json")[0]

    # Valid receipt
    valid_res = runner.invoke(main, ["verify", "--receipt-file", receipt_file])
    assert valid_res.exit_code == 0
    assert "Authorized: Receipt is authentic." in valid_res.output

    # Tampered receipt
    with open(receipt_file, "r", encoding="utf-8") as f:
        receipt_data = json.load(f)
    receipt_data["action"]["tool"] = "delete_file"
    with open("tampered_receipt.json", "w", encoding="utf-8") as f:
        json.dump(receipt_data, f)

    invalid_res = runner.invoke(
        main, ["verify", "--receipt-file", "tampered_receipt.json"]
    )
    assert invalid_res.exit_code == 1
    assert "Invalid Receipt Signature." in invalid_res.output
