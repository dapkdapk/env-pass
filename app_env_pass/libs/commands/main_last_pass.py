import os

import click

from app_env_pass.libs.last_pass.constants_last_pass import \
    DEFAULT_ENV_FILE_OUTPUT
from app_env_pass.libs.last_pass.env_last_pass_cls import EnvLastPass


@click.command()
@click.option(
    "-id",
    "--last-pass-entry-id",
    prompt=True,
    type=click.STRING,
    required=True,
    help="set last pass entry id, eg. 7478234270784347397, eg. you'll find the entry-id under in the bottom of the edit dialog of the last pass browser extension.",
)
@click.option(
    "-kv",
    "--key-values",
    type=click.STRING,
    help="set ENV-VARIABLE=KEY-NAME, eg. USERNAME=Username,PASSWORD=Password,FIELD1=field1 (comma-seperated for more)",
)
@click.option(
    "-o",
    "--output-file",
    type=click.STRING,
    default=DEFAULT_ENV_FILE_OUTPUT,
    help="set output file. default is '{DEFAULT_ENV_FILE_OUTPUT}'",
)
@click.option("-s", "--show-last-pass-output", is_flag=True)
def execute(last_pass_entry_id, key_values, output_file, show_last_pass_output):
    if EnvLastPass.IsPassCLILogged() is True and last_pass_entry_id is not None:
        _env_names = EnvLastPass.GetEnvNames(
            last_pass_entry_id, key_values, show_last_pass_output
        )
        if len(_env_names) > 0:
            _script = EnvLastPass.GetEnvFileScript(
                _env_names=_env_names, last_pass_entry_id=last_pass_entry_id
            )
            print("-" * 144)
            print("ENV FILE FOR SOURCE")
            print("-" * 144)
            print(_script)
            print("-" * 144)
            write_file = os.path.expanduser(output_file)
            with open(write_file, "w") as f:
                f.write(_script)
            print(f"File '{write_file}' was written.")
    else:
        print("Something goes wrong. Please check if ENTRY-ID is set.")


if __name__ == "__main__":
    execute()
