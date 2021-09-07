import json
import keyword
from typing import Union

class_format = """
class {classname}():
    def __init__(self):
{variables}
"""

def _json_unmarshall(target_class, data: dict):
    c = target_class()
    if data is None:
        return None
    for key, val in data.items():
        key = __escape_python_keyword(key)
        c_val = c.__dict__.get(key)
        if c_val is None:
            continue
        if isinstance(c_val, list):
            data[key] = [_json_unmarshall(c_val[0], d) for d in data[key]]
            continue
        data[key] = _json_unmarshall(c_val, data[key])
    c.__dict__ = data
    return c


def json_unmarshall(target_class, data):
    if isinstance(data, str):
        data = json.loads(data)
    return _json_unmarshall(target_class,data)


def _json_marshall(src_object):
    data = {}
    c = src_object.__class__()
    for c_key, c_val in c.__dict__.items():
        key = __unescape_python_keyword(c_key)
        if c_val is None:
            data[key] = src_object.__dict__[c_key]
            continue
        if isinstance(c_val, list):
            data[key] = [_json_marshall(obj) for obj in src_object.__dict__[c_key]]
            continue
        data[key] = _json_marshall(src_object.__dict__[c_key])
    return data

def json_marshall(src_object):
    return _json_marshall(src_object)

def __make_class_name(mainclass, *subclass):
    return mainclass + "".join([c.capitalize() for c in subclass])

def __escape_python_keyword(key):
    if keyword.iskeyword(key):
        return "{}_{}".format(key,key)
    return key

def __unescape_python_keyword(key):
    keys = key.split("_")
    if len(keys) >1 and keyword.iskeyword(keys[0]) and keys[0] == keys[1]:
        return keys[0]
    return key

def _json_convert_class(classname, data: dict,
                        indent,
                        cur_depth,depth):
    class_list = []
    variable_list = []
    for key, val in data.items():
        safe_key = __escape_python_keyword(key)
        if cur_depth >= depth:
            variable_list.append("self.{} = None".format(safe_key))
            continue
        if isinstance(val, list):
            if len(val) == 0:
                subclsname = __make_class_name(classname, key)
                class_list.append(_json_convert_class(subclsname,{},indent,
                                                      cur_depth+1,depth))
            else:
                if isinstance(val[0],dict):
                    subclsname = __make_class_name(classname, key)
                    class_list.append(_json_convert_class(subclsname,val[0],indent,
                                                          cur_depth+1,depth))
                    variable_list.append("self.{} = [{}]".format(safe_key, subclsname))
                else:
                    variable_list.append("self.{} = None".format(safe_key))
            continue
        if isinstance(val, dict):
            subclsname = __make_class_name(classname, key)
            class_list.append(_json_convert_class(subclsname,val,indent,
                                                  cur_depth+1,depth))
            variable_list.append("self.{} = {}".format(safe_key,subclsname))
            continue
        variable_list.append("self.{} = None".format(safe_key))
    if len(variable_list) == 0:
        variable_list.append("pass")
    variable_str = "\n".join(["{}{}".format(" "*indent,v) for v in variable_list])
    class_str = class_format.format(classname=classname,variables=variable_str)
    class_list.append(class_str)
    return "\n".join(class_list)


def json_convert_class(classname, data: Union[dict, str],indent=8,depth=1024):
    if isinstance(data, str):
        data = json.loads(data)
    return _json_convert_class(classname, data,
                               indent,
                               0,depth)
