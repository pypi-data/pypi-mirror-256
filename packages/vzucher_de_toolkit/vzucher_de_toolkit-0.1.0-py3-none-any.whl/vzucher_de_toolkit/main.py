import click
from .vm import cli as vm_cli  # Import the CLI group from vm.py with a different name to avoid conflict

@click.group()
def cli():
    """Your main CLI group"""
    pass

# Add the VM CLI commands to the main CLI group
cli.add_command(vm_cli, name="vm")  # Use a different name for the group of commands from vm.py

if __name__ == '__main__':
    cli()
