import json
import os
import re
import subprocess

import click
import inquirer
import jmespath

OBJ_KEY_TMP = "obj"

TMPL_ENV_FILE = """declare -a vars=({env_vars})
pass_to_get=0
if ! $(pass-cli info -o json | jq '.username' > /dev/null 2>&1)
then
        echo "Logging into proton pass..."
        pass-cli login
        pass_to_get=1
else
        echo "Valid proton pass token found."
        pass_to_get=1
fi

if [[ "$pass_to_get" == 1 ]]; then
        json=$(pass-cli item view --output json --share-id {shared_id} --item-id {item_id})
        {export_list}
fi
"""
TMPL_EXPORT_ITEM = '''export {env_name}="$(echo $json | jq -Rnr '[inputs] | join("") | fromjson | .{json_path}')"'''
TMPL_EXPORT_ITEM_LIST = '''export {env_name}="$(echo $json | jq -Rnr '[inputs] | join("") | fromjson | .{json_path} | select(.name == "{name}") | .content.Text')"'''
DEFAULT_ENV_FILE_OUTPUT = "./sample.env"


@click.command()
@click.option(
    "-u",
    "--proton-pass-uri",
    prompt=True,
    type=click.STRING,
    required=True,
    help="set proton pass uri, eg. moz-extension://.../popup.html#/u/7/share/A...",
)
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
def main(proton_pass_uri, key_values, output_file, show_json_paths):
    _uri = proton_pass_uri.split("/")
    _share = None
    _item = None
    for i, _u in enumerate(_uri):
        if _u == "share":
            _share = _clr(_uri[i + 1])
        if _u == "item":
            _item = _clr(_uri[i + 1])

    proc = subprocess.Popen(
        "$(which pass-cli) info",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    out, err = proc.communicate()

    if out.decode() == "":
        print("pass-cli login not available, please login first, eg. 'pass-cli login'")
        exit(1)
    _cmd = f"$(which pass-cli) item view --output json --share-id {_share} --item-id {_item}"
    print("-" * 144)
    print(f"Execute: {_cmd}")
    print("-" * 144)
    proc = subprocess.Popen(
        _cmd,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    out, err = proc.communicate()
    dict_obj = json.loads(out.decode())
    _mylist = getKeys(dict_obj)
    if show_json_paths is True:
        for mk, mv in _mylist.items():
            if show_json_paths is True:
                print(mk, "=", mv)
        exit(1)

    _env_names = {}
    if key_values is None:
        _selection = []
        for mk, mv in _mylist.items():
            _selection.append(mk + " = " + mv)

        questions_path = [
            inquirer.Checkbox(
                "values",
                message="Select (secret) values you needed",
                choices=_selection,
            ),
        ]

        answers_path = inquirer.prompt(questions_path)
        _choosen = []
        for ans in answers_path["values"]:
            _name = str(ans.split(" = ")[0]).strip()
            _choosen.append(
                inquirer.Text(
                    _name, message=f"Set environment variable name for '{_name}'"
                )
            )
        questions_env_name = _choosen

        _env_names = inquirer.prompt(questions_env_name)
        for k, v in _env_names.items():
            _env_names[k] = v.upper()
    else:
        _kv = key_values.split(",")
        for kv in _kv:
            _kvs = kv.split("=")
            _env_names[str(_kvs[1]).strip()] = str(_kvs[0]).strip().upper()

    if len(_env_names) > 0:
        _export_items = []
        for k, v in _env_names.items():
            _iss = k.split(".")
            _m = False
            for _is in _iss:
                if len(re.findall(r"\[\]", _is)) > 0:
                    _m = True
                    break

            if _m is True:
                _iss_val = _iss.pop()
                _export_items.append(
                    TMPL_EXPORT_ITEM_LIST.format(
                        env_name=v, json_path=".".join(_iss), name=_iss_val
                    )
                )
            else:
                _export_items.append(TMPL_EXPORT_ITEM.format(env_name=v, json_path=k))
        _script = TMPL_ENV_FILE.format(
            env_vars=" ".join(list(_env_names.values())),
            shared_id=_share,
            item_id=_item,
            export_list="\n\t".join(_export_items),
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


def getKeys(obj):
    _mlist = []

    def _gk(obj, parent=OBJ_KEY_TMP):
        # global _mlist
        for i in obj.keys():
            _mlist.append(parent + "." + i)
            try:
                _gk(obj[i], parent + "." + i)
            except AttributeError:
                pass

    _gk(obj)
    _mobj = {}
    for mi in _mlist:
        _val = jmespath.search(mi[len(OBJ_KEY_TMP) + 1 :], obj)
        if isinstance(_val, str):
            _mobj[mi[len(OBJ_KEY_TMP) + 1 :]] = _val
        elif (
            isinstance(_val, list)
            and len(_val) > 0
            and isinstance(_val[0], dict)
            and "name" in _val[0]
        ):
            _mobj[mi[len(OBJ_KEY_TMP) + 1 :] + "[]" + f".{_val[0]['name']}"] = _val[0][
                "content"
            ]["Text"]

    return _mobj


def _clr(s):
    if len(re.findall(r"\?", s)) > 0:
        return s.split("?")[0]
    return s


if __name__ == "__main__":
    main()
