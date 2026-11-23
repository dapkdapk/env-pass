import importlib.metadata
import logging
import os
import re
import typing

import inquirer
from InquirerPy import inquirer as pyinquirer

"""
https://inquirerpy.readthedocs.io/en/latest/index.html
"""


class AKArgs:
    @staticmethod
    def PrintLogs(
        logging_level: int, *args
    ):  # PrintLog(logger.INFO, "a", ["b", "c"], "d\ne\nf")
        def _itr_args(args):
            _s = []
            _o = []
            for arg in args:
                _ln = str(arg).splitlines()
                # print(_ln)
                if isinstance(arg, str) and len(_ln) == 1:
                    _s.append(arg)
                elif isinstance(arg, list):
                    if len(_s) > 0:
                        _o.append(_s)
                        _s = []
                    _o.append(arg)
                elif len(_ln) > 0:
                    if len(_s) > 0:
                        _o.append(_s)
                        _s = []
                    for _n in _ln:
                        _o.append([_n])
                else:
                    if len(_s) > 0:
                        _o.append(_s)
                        _s = []

            if len(_s) > 0:
                _o.append(_s)
                _s = []
            return _o

        for _arg in _itr_args(args):
            getattr(logging, str(logging.getLevelName(logging_level)).lower())(
                " ".join(str(val) for val in _arg)
            )

    @staticmethod
    def GetVersionByPackageLibName(package_lib_name: str):
        return importlib.metadata.version(package_lib_name)

    @staticmethod
    def ArgUse(
        arg_value,
        config,
        key,
        expected_type,
        splitted: bool = False,
        default: typing.Any | None = None,
    ):
        if arg_value is not None:
            return (
                arg_value.split(",")
                if splitted is True and isinstance(arg_value, str)
                else arg_value
            )
        elif key in config and isinstance(config[key], expected_type):
            return config[key]
        else:
            return [] if expected_type == list else default

    @staticmethod
    def SaveFile(
        file_name,
        write_data,
        dry_run=False,
        cc=None,
        show_print=True,
        show_details=False,
    ) -> bool | None:
        success = None
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        if os.path.exists(file_name) is False:
            if dry_run is True:
                if show_print is True:
                    if cc is not None:
                        if show_details is True:
                            AKArgs.PrintLogs(
                                logging.INFO,
                                str(cc),
                                ">[DRY-RUN] Write file:",
                                file_name,
                            )
                    else:
                        if show_details is True:
                            AKArgs.PrintLogs(
                                logging.INFO, ">[DRY-RUN] Write file:", file_name
                            )
            else:
                if show_print is True:
                    if cc is not None:
                        if show_details is True:
                            AKArgs.PrintLogs(
                                logging.INFO, str(cc), ">Write file:", file_name
                            )
                    else:
                        if show_details is True:
                            AKArgs.PrintLogs(logging.INFO, ">Write file:", file_name)
                with open(file_name, "wb") as f:
                    f.write(write_data)
                    success = True if os.access(file_name, os.F_OK) else False
        else:
            if show_details is True:
                AKArgs.PrintLogs(
                    logging.DEBUG,
                    "\t!File already exists:",
                    os.path.basename(file_name),
                )
            success = True if os.access(file_name, os.F_OK) else False
        return success

    @staticmethod
    def ArgPromptText(
        input_inquire: typing.Any,
        message: str,
        validate: typing.Any | None = None,
        default: str | None = None,
    ):
        try:
            if input_inquire is None or (
                validate is not None and validate("", input_inquire) is False
            ):
                input_inquire = AKArgs.PromptText(
                    message=message, validate=validate, default=default
                )
            return input_inquire
        except:
            quit()

    @staticmethod
    def ArgPromptLong(
        input_inquire: typing.Any,
        message: str,
        validate: typing.Any | None = None,
        default: str = "",
    ):
        try:
            if input_inquire is None or (
                validate is not None and validate("", input_inquire) is False
            ):
                input_inquire = AKArgs.PromptLong(
                    message=message, validate=validate, default=default
                )
            return input_inquire
        except:
            quit()

    @staticmethod
    def ArgPromptChoice(
        input_inquire: typing.Any,
        message: str,
        choices: list,
        validate: typing.Any | None = None,
        default: str | None = None,
    ):
        try:
            if input_inquire is None or (
                validate is not None and validate("", input_inquire) is False
            ):
                input_inquire = AKArgs.PromptChoices(
                    message=message, choices=choices, validate=validate, default=default
                )
            return input_inquire
        except:
            quit()

    @staticmethod
    def ArgPromptConfirm(
        input_inquire: typing.Any,
        message: str,
        validate: typing.Any | None = None,
        default: bool = False,
    ):
        try:
            if input_inquire is None or (
                validate is not None and validate("", input_inquire) is False
            ):
                input_inquire = AKArgs.PromptConfirm(
                    message=message, validate=validate, default=default
                )
            return input_inquire
        except:
            quit()

    @staticmethod
    def PromptConfirm(message: str, name="item", **kwargs: typing.Any):
        question = [inquirer.Confirm(name=name, message=message, **kwargs)]
        return inquirer.prompt(questions=question)[name]

    @staticmethod
    def PromptText(message: str, name="item", **kwargs: typing.Any):
        question = [inquirer.Text(name=name, message=message, **kwargs)]
        return inquirer.prompt(questions=question)[name]

    @staticmethod
    def _ValidationFunc(result):
        return True

    @staticmethod
    def PromptLong(message: str, validate=None, default=""):
        return pyinquirer.text(message=message, validate=validate, default="").execute()

    @staticmethod
    def PromptChoices(message: str, choices: list, name="item", **kwargs: typing.Any):
        question = [
            inquirer.List(name=name, message=message, choices=choices, **kwargs)
        ]
        return inquirer.prompt(questions=question)[name]

    @staticmethod
    def TruncStr(string, width, justify: str = "right", dots: str = ".."):
        string = string.strip()
        if len(string) > width:
            if justify == "right":
                string = string[: width - len(dots)].strip() + dots
            elif justify == "left":
                string = dots + string[-(width + len(dots)) :].strip()
        return string

    @staticmethod
    def SetupLogging(logging_level: str):
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s|%(levelname)s| %(message)s", datefmt="%y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        handlers: list[logging.Handler] = [console_handler]

        if logging_level.upper() == "DEBUG":
            handlers.append(logging.FileHandler("debug.log"))
        logging.basicConfig(
            level=getattr(logging, logging_level.upper()),
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=handlers,
        )

    @staticmethod
    def ValidateStringOrNone(ans, curr):
        return True if isinstance(curr, str) or str(curr) == "" else False

    @staticmethod
    def ValidateString(ans, curr):
        return True if isinstance(curr, str) or str(curr) != "" else False

    @staticmethod
    def ValidatePath(ans, curr):
        return os.path.isdir(os.path.abspath(os.path.expanduser(curr)))

    @staticmethod
    def ValidateFileExists(ans, curr):
        return os.path.isfile(os.path.abspath(os.path.expanduser(curr)))

    @staticmethod
    def ValidateFolderName(ans, curr):
        def validate_filename(filename):
            if re.search(r'[/\\\*\?"<>|]', filename):
                return False
            if len(filename) > 255:
                return False
            if filename.startswith(" ") or filename.endswith(" "):
                return False
            return True

        return validate_filename(curr)

    @staticmethod
    def ValidateInteger(ans, curr):
        return str(curr).isdigit()

    @staticmethod
    def ValidateBool(ans, curr):
        try:
            bool(curr)
            return True
        except:
            return False
