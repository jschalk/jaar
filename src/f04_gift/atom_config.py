from src.f00_instrument.file import open_file, save_file
from src.f00_instrument.dict_tool import (
    get_json_from_dict,
    get_dict_from_json,
    get_from_nested_dict,
)
from os import getcwd as os_getcwd


class CRUD_command(str):
    pass


def atom_update() -> CRUD_command:
    return "UPDATE"


def atom_insert() -> CRUD_command:
    return "INSERT"


def atom_delete() -> CRUD_command:
    return "DELETE"


def atom_hx_table_name() -> str:
    return "atom_hx"


def atom_mstr_table_name() -> str:
    return "atom_mstr"


def normal_specs_str() -> str:
    return "normal_specs"


def normal_table_name_str() -> str:
    return "normal_table_name"


def columns_str() -> str:
    return "columns"


def sqlite_datatype_str() -> str:
    return "sqlite_datatype"


def python_type_str() -> str:
    return "python_type"


def type_AcctID_str() -> str:
    return "AcctID"


def type_GroupID_str() -> str:
    return "GroupID"


def type_RoadUnit_str() -> str:
    return "RoadUnit"


def type_RoadNode_str() -> str:
    return "RoadNode"


def nullable_str() -> str:
    return "nullable"


def nesting_order_str() -> str:
    return "nesting_order"


def required_args_str() -> str:
    return "required_args"


def optional_args_str() -> str:
    return "optional_args"


def column_order_str() -> str:
    return "column_order"


def category_str() -> str:
    return "category"


def crud_str_str() -> str:
    return "crud_str"


def fiscal_id_str() -> str:
    return "fiscal_id"


def owner_id_str() -> str:
    return "owner_id"


def credor_respect_str() -> str:
    return "credor_respect"


def debtor_respect_str() -> str:
    return "debtor_respect"


def acct_id_str() -> str:
    return "acct_id"


def group_id_str() -> str:
    return "group_id"


def team_id_str() -> str:
    return "team_id"


def healer_id_str() -> str:
    return "healer_id"


def acct_pool_str() -> str:
    return "acct_pool"


def debtit_belief_str() -> str:
    return "debtit_belief"


def credit_belief_str() -> str:
    return "credit_belief"


def debtit_vote_str() -> str:
    return "debtit_vote"


def credit_vote_str() -> str:
    return "credit_vote"


def road_str() -> str:
    return "road"


def parent_road_str() -> str:
    return "parent_road"


def label_str() -> str:
    return "label"


def mass_str() -> str:
    return "mass"


def pledge_str() -> str:
    return "pledge"


def begin_str() -> str:
    return "begin"


def close_str() -> str:
    return "close"


def addin_str() -> str:
    return "addin"


def numor_str() -> str:
    return "numor"


def denom_str() -> str:
    return "denom"


def morph_str() -> str:
    return "morph"


def gogo_want_str() -> str:
    return "gogo_want"


def stop_want_str() -> str:
    return "stop_want"


def base_str() -> str:
    return "base"


def fopen_str() -> str:
    return "fopen"


def fnigh_str() -> str:
    return "fnigh"


def base_item_active_requisite_str() -> str:
    return "base_item_active_requisite"


def get_atom_config_file_name() -> str:
    return "atom_config.json"


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/f04_gift"


def get_atom_config_dict() -> dict:
    return get_dict_from_json(open_file(config_file_dir(), get_atom_config_file_name()))


def get_atom_config_required_args(x_cat: str) -> dict:
    required_args_key_list = [x_cat, required_args_str()]
    return get_from_nested_dict(get_atom_config_dict(), required_args_key_list)


def get_atom_config_optional_args(x_cat: str) -> dict:
    optional_args_key_list = [x_cat, optional_args_str()]
    return get_from_nested_dict(get_atom_config_dict(), optional_args_key_list)


def get_atom_config_args(x_category: str) -> dict[str, dict]:
    args_dict = get_atom_config_required_args(x_category)
    args_dict.update(get_atom_config_optional_args(x_category))
    return args_dict


def get_atom_args_category_mapping() -> dict[str, set[str]]:
    x_dict = {}
    for atom_category in get_atom_config_dict().keys():
        args_set = set(get_atom_config_args(atom_category))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {atom_category}
            else:
                x_category_set = x_dict.get(x_arg)
                x_category_set.add(atom_category)
                x_dict[x_arg] = x_category_set
    return x_dict


def get_allowed_python_types() -> set[str]:
    return {
        "AcctID",
        "bool",
        "float",
        "GroupID",
        "int",
        "RoadNode",
        "RoadUnit",
        "TimeLinePoint",
    }


def get_atom_args_python_types() -> dict[str, str]:
    return {
        "acct_id": "AcctID",
        "addin": "float",
        "base": "RoadUnit",
        "base_item_active_requisite": "bool",
        "begin": "float",
        "close": "float",
        "credit_belief": "int",
        "credit_vote": "int",
        "credor_respect": "int",
        "debtit_belief": "int",
        "debtit_vote": "int",
        "debtor_respect": "int",
        "denom": "int",
        "divisor": "int",
        "fnigh": "float",
        "fopen": "float",
        "fund_coin": "float",
        "fund_pool": "float",
        "give_force": "float",
        "gogo_want": "float",
        "group_id": "GroupID",
        "healer_id": "GroupID",
        "label": "RoadNode",
        "mass": "int",
        "max_tree_traverse": "int",
        "morph": "bool",
        "need": "RoadUnit",
        "nigh": "float",
        "numor": "int",
        "open": "float",
        "parent_road": "RoadUnit",
        "penny": "float",
        "pick": "RoadUnit",
        "pledge": "bool",
        "problem_bool": "bool",
        "purview_timestamp": "TimeLinePoint",
        "respect_bit": "float",
        "road": "RoadUnit",
        "stop_want": "float",
        "take_force": "float",
        "tally": "int",
        "team_id": "GroupID",
    }


def get_sorted_required_arg_keys(atom_category: str) -> list[str]:
    atom_config = get_atom_config_dict()
    atom_category_config = atom_config.get(atom_category)
    atom_required_args_config = atom_category_config.get(required_args_str())
    if len(atom_required_args_config) == 1:
        return list(atom_required_args_config.keys())
    nesting_order_dict = {
        required_key: required_dict.get(nesting_order_str())
        for required_key, required_dict in atom_required_args_config.items()
    }
    sorted_tuples = sorted(nesting_order_dict.items(), key=lambda x: x[1])
    return [x_tuple[0] for x_tuple in sorted_tuples]


def add_to_atom_table_columns(x_dict, atom_category, crud, arg_key, arg_value):
    x_dict[f"{atom_category}_{crud}_{arg_key}"] = arg_value.get("sqlite_datatype")


def get_flattened_atom_table_build() -> dict[str, any]:
    atom_table_columns = {}
    atom_config = get_atom_config_dict()
    for atom_category, category_dict in atom_config.items():
        catergory_insert = category_dict.get(atom_insert())
        catergory_update = category_dict.get(atom_update())
        catergory_delete = category_dict.get(atom_delete())
        if catergory_insert is not None:
            required_args = category_dict.get(required_args_str())
            optional_args = category_dict.get(optional_args_str())
            for required_arg, x_value in required_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_insert(),
                    required_arg,
                    x_value,
                )
            for optional_arg, x_value in optional_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_insert(),
                    optional_arg,
                    x_value,
                )
        if catergory_update is not None:
            required_args = category_dict.get(required_args_str())
            optional_args = category_dict.get(optional_args_str())
            for required_arg, x_value in required_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_update(),
                    required_arg,
                    x_value,
                )
            for optional_arg, x_value in optional_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_update(),
                    optional_arg,
                    x_value,
                )
        if catergory_delete is not None:
            required_args = category_dict.get(required_args_str())
            for required_arg, x_value in required_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_delete(),
                    required_arg,
                    x_value,
                )
    return atom_table_columns


def get_normalized_bud_table_build() -> dict[str : dict[str, any]]:
    normal_tables_dict = {}
    atom_config = get_atom_config_dict()
    for x_category, category_dict in atom_config.items():
        normal_tables_dict[x_category] = {}
        normal_table_dict = normal_tables_dict.get(x_category)

        normal_table_dict[columns_str()] = {}
        normal_columns_dict = normal_table_dict.get(columns_str())
        normal_columns_dict["uid"] = {
            sqlite_datatype_str(): "INTEGER",
            nullable_str(): False,
            "primary_key": True,
        }
        required_args = category_dict.get(required_args_str())
        optional_args = category_dict.get(optional_args_str())
        if required_args is not None:
            for required_arg, x_value in required_args.items():
                normal_columns_dict[required_arg] = {
                    sqlite_datatype_str(): x_value.get(sqlite_datatype_str()),
                    nullable_str(): False,
                }

        if optional_args is not None:
            for optional_arg, x_value in optional_args.items():
                normal_columns_dict[optional_arg] = {
                    sqlite_datatype_str(): x_value.get(sqlite_datatype_str()),
                    nullable_str(): True,
                }

        normal_table_dict[normal_specs_str()] = {}
        normal_specs_dict = normal_table_dict.get(normal_specs_str())
        config_normal_dict = category_dict.get(normal_specs_str())
        table_name = config_normal_dict.get(normal_table_name_str())
        normal_specs_dict[normal_table_name_str()] = table_name

    return normal_tables_dict


def save_atom_config_file(atom_config_dict):
    x_file_str = get_json_from_dict(atom_config_dict)
    save_file(config_file_dir(), get_atom_config_file_name(), x_file_str)


def category_ref() -> set:
    return get_atom_config_dict().keys()


def is_category_ref(category_str: str) -> bool:
    return category_str in category_ref()


def get_atom_order(crud_str: str, category: str) -> int:
    return get_from_nested_dict(
        get_atom_config_dict(), [category, crud_str, "atom_order"]
    )


def get_normal_table_name(category: str) -> str:
    nested_list = [category, normal_specs_str(), normal_table_name_str()]
    return get_from_nested_dict(get_atom_config_dict(), nested_list)


def set_mog(
    crud_str: str,
    category: str,
    atom_order_int: int,
) -> int:
    atom_config_dict = get_atom_config_dict()
    category_dict = atom_config_dict.get(category)
    crud_dict = category_dict.get(crud_str)
    crud_dict["atom_order"] = atom_order_int
    save_atom_config_file(atom_config_dict)


def get_category_from_dict(x_row_dict: dict) -> str:
    x_category_ref = category_ref()
    for x_columnname in x_row_dict:
        for x_category in x_category_ref:
            if x_columnname.find(x_category) == 0:
                category_len = len(x_category)
                return x_category, x_columnname[category_len + 1 : category_len + 7]
