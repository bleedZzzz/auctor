import click
import json
from cryptography.hazmat.primitives import serialization
from auctor.identity.key import generate_identity, Identity
from auctor.protocol.mandate import Mandate
from auctor.engine.policy import PolicyEngine

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
@click.option("--chain-file", required=True, help="JSON file containing list of mandates")
@click.option("--tool", required=True)
def check(chain_file, tool):
    with open(chain_file, "r") as f:
        chain = json.load(f)

    if PolicyEngine.verify_chain(chain):
        # Verify tool is in the leaf mandate
        leaf_mandate = chain[-1]
        if PolicyEngine.validate_action(leaf_mandate, tool):
            click.echo(f"Authorized: Tool '{tool}' is permitted by the verified chain.")
        else:
            click.echo(f"Denied: Tool '{tool}' is NOT permitted.")
    else:
        click.echo("Denied: Invalid delegation chain or signature.")

if __name__ == "__main__":
    main()
