import jmespath
import re
from app_env_pass.libs.constants import OBJ_KEY_TMP

class EnvPass:
    def __init__(self):
        pass
    @staticmethod
    def _ClearString(s):
        if len(re.findall(r"\?", s)) > 0:
            return s.split("?")[0]
        return s

    @staticmethod
    def _GetKeys(obj):
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
                _mobj[mi[len(OBJ_KEY_TMP) + 1 :] + "[]" + f".{_val[0]['name']}"] = _val[
                    0
                ]["content"]["Text"]

        return _mobj
