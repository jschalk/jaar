from json import loads as json_loads, dumps as json_dumps
from copy import deepcopy as copy_deepcopy


def get_empty_dict_if_none(x_dict: dict) -> dict:
    return {} if x_dict is None else x_dict


def get_empty_set_if_none(x_set: set) -> set:
    return set() if x_set is None else x_set


def get_1_if_None(x_obj):
    return 1 if x_obj is None else x_obj


def get_0_if_None(x_obj=None):
    return 0 if x_obj is None else x_obj


def get_empty_list_if_None(x_obj=None):
    return [] if x_obj is None else x_obj


def get_False_if_None(x_obj=None):
    return False if x_obj is None else x_obj


def get_positive_int(x_obj: any = None):
    try:
        x_int = int(x_obj)
    except Exception:
        x_int = 0
    return max(x_int, 0)


def add_dict_if_missing(x_dict: dict, x_keylist: list[any]):
    for x_key in x_keylist:
        if x_dict.get(x_key) is None:
            x_dict[x_key] = {}
        x_dict = x_dict.get(x_key)


def place_obj_in_dict(x_dict: dict, x_keylist: list[any], x_obj: any):
    x_keylist = copy_deepcopy(x_keylist)
    last_key = x_keylist.pop(-1)
    add_dict_if_missing(x_dict, x_keylist=x_keylist)
    last_dict = x_dict
    for x_key in x_keylist:
        last_dict = last_dict[x_key]
    last_dict[last_key] = x_obj


def x_is_json(json_x: str) -> bool:
    try:
        get_dict_from_json(json_x)
    except ValueError as e:
        return False
    return True


class NestedValueException(Exception):
    pass


def get_nested_value(
    x_dict: dict, x_keylist: list, if_missing_return_None: bool = False
) -> any:
    if not if_missing_return_None:
        return _sub_get_nested_value(x_dict, x_keylist)
    try:
        return _sub_get_nested_value(x_dict, x_keylist)
    except Exception:
        return None


def _sub_get_nested_value(x_dict: dict, x_keylist: list) -> any:
    last_key = x_keylist.pop(-1)
    temp_dict = x_dict
    x_count = 0
    for x_key in x_keylist:
        if temp_dict.get(x_key) is None:
            raise NestedValueException(f"'{x_key}' failed at level {x_count}.")
        x_count += 1
        temp_dict = temp_dict.get(x_key)

    if temp_dict.get(last_key) is None:
        raise NestedValueException(f"'{last_key}' failed at level {x_count}.")
    return temp_dict[last_key]


def get_all_nondictionary_objs(x_dict: dict) -> dict[str : list[any]]:
    level1_keys = x_dict.keys()
    output_dict = {}
    for level1_key in level1_keys:
        output_dict[level1_key] = []
        level1_list = output_dict.get(level1_key)
        eval_items = list(x_dict.get(level1_key).values())
        while eval_items != []:
            eval_item = eval_items.pop(0)
            if type(eval_item) == type({}):
                eval_items.extend(eval_item.values())
            else:
                level1_list.append(eval_item)
    return output_dict


def get_json_from_dict(dict_x: dict) -> str:
    return json_dumps(obj=dict_x)


def get_dict_from_json(json_x: str) -> dict[str,]:
    return json_loads(json_x)
