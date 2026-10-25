import click
import json
from cryptography.hazmat.primitives import serialization
from auctor.identity.key import generate_identity, Identity
from auctor.protocol.mandate import Mandate
from auctor.engine.policy import PolicyEngine
from auctor.protocol.receipt import Receipt

@click.group()
def main():
    pass

@main.command()
def init():
    identity = generate_identity()
    pub = identity.get_public_bytes().hex()
    priv = identity._private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    ).hex()

    click.echo(f"Identity generated. Public Key: {pub}")
    with open("identity.json", "w") as f:
        json.dump({"pub": pub, "priv": priv}, f)

@main.command()
@click.option("--subject", required=True)
@click.option("--tool", multiple=True)
@click.option("--parent-file", help="Path to parent mandate JSON")
def issue(subject, tool, parent_file):
    with open("identity.json", "r") as f:
        creds = json.load(f)

    from cryptography.hazmat.primitives.asymmetric import ed25519
    priv_bytes = bytes.fromhex(creds["priv"])
    priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_bytes)
    identity = Identity(priv_key)

    parent_id = None
    if parent_file:
        with open(parent_file, "r") as f:
            parent_mandate = json.load(f)
            parent_id = parent_mandate["id"]

    mandate = Mandate(creds["pub"], subject, list(tool), parent_id=parent_id)
    signed_mandate = mandate.sign(identity)

    filename = f"mandate_{mandate.data['id']}.json"
    click.echo(json.dumps(signed_mandate, indent=2))
    with open(filename, "w") as f:
        json.dump(signed_mandate, f)
    click.echo(f"Mandate saved to {filename}")

@main.command()
@click.option("--mandate-file", required=True)
@click.option("--tool", required=True)
def run(mandate_file, tool):
    """Simulate tool execution and generate receipt"""
    with open(mandate_file, "r") as f:
        mandate = json.load(f)

    # Simplified enforcement
    if not PolicyEngine.validate_action(mandate, tool):
        click.echo("Denied")
        return

    # Simulate execution
    input_data = {"test": "data"}
    output_data = {"result": "success"}

    # Sign receipt
    with open("identity.json", "r") as f:
        creds = json.load(f)
    from cryptography.hazmat.primitives.asymmetric import ed25519
    priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(creds["priv"]))
    identity = Identity(priv_key)

    receipt = Receipt(mandate["id"], tool, input_data, output_data)
    signed_receipt = receipt.sign(identity)

    filename = f"receipt_{mandate['id']}_{tool}.json"
    with open(filename, "w") as f:
        json.dump(signed_receipt, f)
    click.echo(f"Action authorized. Receipt saved to {filename}")

@main.command()
@click.option("--receipt-file", required=True)
def verify(receipt_file):
    """Verify an evidence receipt"""
    import jcs
    with open(receipt_file, "r") as f:
        receipt = json.load(f)

    # Verify signature
    sig_data = receipt.pop("signature")
    payload = jcs.canonicalize(receipt)
    pub_bytes = bytes.fromhex(sig_data["pubkey"])
    sig_bytes = bytes.fromhex(sig_data["value"])

    from cryptography.hazmat.primitives.asymmetric import ed25519
    try:
        pub_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
        pub_key.verify(sig_bytes, payload)
        click.echo("Authorized: Receipt is authentic.")
    except Exception:
        click.echo("Invalid Receipt Signature.")

if __name__ == "__main__":
    main()
