import click

from app_env_pass.libs.commands.main_proton_pass import execute as proton_pass
from app_env_pass.libs.commands.main_last_pass import execute as last_pass

@click.group()
def main_cli():
    """
    """

main_cli.add_command(proton_pass, name="ppass")
main_cli.add_command(last_pass, name="lpass")
if __name__ == "__main__":
    main_cli()
