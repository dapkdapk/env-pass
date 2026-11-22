import json
import re
import subprocess

import inquirer

from app_env_pass.libs.proton_pass.constants_proton_pass import (TMPL_ENV_FILE,
                                         TMPL_EXPORT_ITEM,
                                         TMPL_EXPORT_ITEM_LIST)
from app_env_pass.libs.env_pass_cls import EnvPass

class EnvProtonPass:
    def __init__(self):
        pass

    @staticmethod
    def GetEnvFileScript(_env_names: dict, _share: str, _item: str):
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
        return TMPL_ENV_FILE.format(
            env_vars=" ".join(list(_env_names.values())),
            shared_id=_share,
            item_id=_item,
            export_list="\n\t".join(_export_items),
        )

    @staticmethod
    def GetEnvNames(
        _share: str, _item: str, key_values: str, show_json_paths: bool = False
    ) -> dict:
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
        _mylist = EnvPass._GetKeys(dict_obj)
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
        return _env_names

    @staticmethod
    def IsPassCLILogged():
        proc = subprocess.Popen(
            "$(which pass-cli) info",
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        out, err = proc.communicate()

        if out.decode() == "":
            print(
                "pass-cli login not available, please login first, eg. 'pass-cli login'"
            )
            return False
        else:
            return True

    @staticmethod
    def GetSettings(
        proton_pass_uri: str | None = None,
        proton_pass_share_id: str | None = None,
        proton_pass_item_id: str | None = None,
    ):
        if proton_pass_uri is None and (
            proton_pass_share_id is None or proton_pass_item_id is None
        ):
            print(
                "Please set proton_pass_uri or proton_pass_share_id and proton_pass_item_id!"
            )
        _proton_pass_uri = None
        _proton_pass_share_id = None
        _proton_pass_item_id = None
        if proton_pass_uri is not None:
            _proton_pass_uri = proton_pass_uri.split("/")
            _proton_pass_share_id = None
            _proton_pass_item_id = None
            for i, _u in enumerate(_proton_pass_uri):
                if _u == "share":
                    _proton_pass_share_id = EnvPass._ClearString(
                        _proton_pass_uri[i + 1]
                    )
                if _u == "item":
                    _proton_pass_item_id = EnvPass._ClearString(_proton_pass_uri[i + 1])
        _proton_pass_share_id = (
            proton_pass_share_id
            if proton_pass_share_id is not None
            else _proton_pass_share_id
        )
        _proton_pass_item_id = (
            proton_pass_item_id
            if proton_pass_item_id is not None
            else _proton_pass_item_id
        )
        return _proton_pass_uri, _proton_pass_share_id, _proton_pass_item_id


