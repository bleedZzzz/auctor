import click
import json
from auctor.identity.key import generate_identity
from auctor.protocol.mandate import Mandate

@click.group()
def main():
    pass

@main.command()
def init():
    identity = generate_identity()
    click.echo(f"Identity generated. Public Key: {identity.get_public_bytes().hex()}")
    # Save to file
    with open("identity.json", "w") as f:
        json.dump({"pub": identity.get_public_bytes().hex()}, f)

@main.command()
@click.option("--issuer", required=True)
@click.option("--subject", required=True)
@click.option("--tool", multiple=True)
def issue(issuer, subject, tool):
    # This is simplified - real signing needs the private key
    mandate = Mandate(issuer, subject, list(tool))
    click.echo(json.dumps(mandate.data, indent=2))

if __name__ == "__main__":
    main()
