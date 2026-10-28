import os
import re

import click

from app.libs.constants import DEFAULT_ENV_FILE_OUTPUT
from app.libs.env_pass_cls import EnvPass


@click.command()
@click.option(
    "-u",
    "--proton-pass-uri",
    prompt=True,
    type=click.STRING,
    required=True,
    help="set proton pass uri, eg. moz-extension://.../popup.html#/u/7/share/A...",
)
@click.option("-si", "--share-id", type=click.STRING, help="set proton pass share_id")
@click.option("-ii", "--item-id", type=click.STRING, help="set proton pass item_id")
@click.option(
    "-kv",
    "--key-values",
    type=click.STRING,
    help="set ENV-VARIABLE=JSON-PATH, eg. PASSWORD=item.login.password or TOKEN=item.content.extra_fields[].name (comma-seperated for more)",
)
@click.option(
    "-o",
    "--output-file",
    type=click.STRING,
    default=DEFAULT_ENV_FILE_OUTPUT,
    help="set output file. default is '{DEFAULT_ENV_FILE_OUTPUT}'",
)
@click.option("-s", "--show-json-paths", is_flag=True)
def main(proton_pass_uri, share_id, item_id, key_values, output_file, show_json_paths):
    _uri, _share, _item = EnvPass.GetSettings(proton_pass_uri, share_id, item_id)
    if EnvPass.IsPassCLILogged() is True and _share is not None and _item is not None:
        _env_names = EnvPass.GetEnvNames(_share, _item, key_values, show_json_paths)
        if len(_env_names) > 0:
            _script = EnvPass.GetEnvFileScript(_env_names, _share, _item)
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
        print(
            "Something goes wrong. Please check if URI or SHARE-ID and ITEM-ID is set."
        )


if __name__ == "__main__":
    main()
