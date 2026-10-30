import json

from click.testing import CliRunner

from auctor.cli.main import main
from auctor.identity.key import generate_identity
from auctor.protocol.receipt import Receipt


def _write_signed_receipt(path, tamper=False):
    identity = generate_identity()
    receipt = Receipt(
        "mandate-id", "read_file", {"path": "notes.txt"}, {"content": "ok"}
    )
    signed_receipt = receipt.sign(identity)

    if tamper:
        signed_receipt["outcome"]["output_hash"] = "tampered"

    with path.open("w", encoding="utf-8") as file:
        json.dump(signed_receipt, file)


def test_verify_accepts_valid_receipt(tmp_path):
    receipt_path = tmp_path / "receipt.json"
    _write_signed_receipt(receipt_path)

    result = CliRunner().invoke(
        main, ["verify", "--receipt-file", str(receipt_path)]
    )

    assert result.exit_code == 0
    assert result.output.strip() == "Authorized: Receipt is authentic."


def test_verify_rejects_tampered_receipt(tmp_path):
    receipt_path = tmp_path / "receipt.json"
    _write_signed_receipt(receipt_path, tamper=True)

    result = CliRunner().invoke(
        main, ["verify", "--receipt-file", str(receipt_path)]
    )

    assert result.exit_code == 1
    assert result.output.strip() == "Invalid Receipt Signature."
