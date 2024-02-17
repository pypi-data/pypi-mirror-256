import click
import subprocess


@click.group()
def cli():
    """VM control toolkit"""
    pass

@click.command()

def start():
    "Starting your Virtual Machine"
    print("Starting VM...")
    subprocess.run(["gcloud", "compute", "instances", "start", "--zone=southamerica-east1-a", "lewagon-data-eng-vm-vzucher"], check=True)


@click.command()

def stop():
    "Stopping your Virtual Machine"
    print("Stopping VM...")
    subprocess.run(["gcloud", "compute", "instances", "stop", "--zone=southamerica-east1-a", "lewagon-data-eng-vm-vzucher"], check=True)


@click.command()

def connect():
    "Connecting your Virtual Machine to ~/home/vzucher/code/vzucher"
    # print accordingly to the user
    print("Connecting to VM...")
    subprocess.run(["code", "--folder-uri", "vscode-remote://ssh-remote+vzucher@34.151.249.165/home/vzucher/code/vzucher/"], check=True)


cli.add_command(start)
cli.add_command(stop)
cli.add_command(connect)

if __name__ == "__main__":
    cli()
