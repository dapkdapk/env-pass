import re
import subprocess

import inquirer

from app_env_pass.libs.last_pass.constants_last_pass import (TMPL_ENV_FILE,
                                                             TMPL_EXPORT_ITEM)


class EnvLastPass:
    def __init__(self):
        pass

    @staticmethod
    def GetEnvFileScript(_env_names: dict, last_pass_entry_id: str):
        _export_items = []
        for k, v in _env_names.items():
            _export_items.append(TMPL_EXPORT_ITEM.format(env_name=v, key_name=k))
        return TMPL_ENV_FILE.format(
            env_vars=" ".join(list(_env_names.values())),
            id=last_pass_entry_id,
            export_list="\n\t".join(_export_items),
        )

    @staticmethod
    def GetEnvNames(
        last_pass_entry_id: str, key_values: str, show_last_pass_output: bool = False
    ) -> dict:
        _cmd = f"$(which lpass) show {last_pass_entry_id}"
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
        _mylist = {}
        _i = 0
        for e in out.decode().splitlines():
            if _i == 0:
                s = re.findall(r"(?:__|[*#])|\[(.*?)\]", e)
                s = str(s[0]).split(":")
            else:
                s = str(e).split(":")
            _mylist.update({str(s[0]).strip(): str(s[1]).strip()})
            _i += 1
        if show_last_pass_output is True:
            for mk, mv in _mylist.items():
                if show_last_pass_output is True:
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
            "$(which lpass) status",
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        out, err = proc.communicate()
        if str(out.decode()).startswith("Not"):
            print(
                "lpass status not available, please login first, eg. 'lpass login USERNAME'"
            )
            return False
        else:
            return True
