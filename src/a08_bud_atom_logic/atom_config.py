from src.a00_data_toolbox.file_toolbox import open_json, save_json, create_path
from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd


def get_atom_config_filename() -> str:
    return "atom_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "a08_bud_atom_logic")


def get_atom_config_dict() -> dict:
    return open_json(config_file_dir(), get_atom_config_filename())


def get_atom_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, "jkeys"]
    return get_from_nested_dict(get_atom_config_dict(), jkeys_key_list)


def get_atom_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, "jvalues"]
    return get_from_nested_dict(get_atom_config_dict(), jvalues_key_list)


def get_atom_config_args(x_dimen: str) -> dict[str, dict]:
    args_dict = get_atom_config_jkeys(x_dimen)
    args_dict.update(get_atom_config_jvalues(x_dimen))
    return args_dict


def get_atom_args_dimen_mapping() -> dict[str, set[str]]:
    x_dict = {}
    for atom_dimen in get_atom_config_dict().keys():
        args_set = set(get_atom_config_args(atom_dimen))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {atom_dimen}
            else:
                x_dimen_set = x_dict.get(x_arg)
                x_dimen_set.add(atom_dimen)
                x_dict[x_arg] = x_dimen_set
    return x_dict


def get_allowed_class_types() -> set[str]:
    return {
        "NameStr",
        "bool",
        "float",
        "TitleStr",
        "int",
        "WordStr",
        "WayStr",
        "TimeLinePoint",
    }


def get_atom_args_class_types() -> dict[str, str]:
    return {
        "acct_name": "NameStr",
        "addin": "float",
        "awardee_title": "TitleStr",
        "rcontext": "WayStr",
        "rcontext_idea_active_requisite": "bool",
        "begin": "float",
        "close": "float",
        "credit_belief": "float",
        "credit_vote": "float",
        "credor_respect": "float",
        "debtit_belief": "float",
        "debtit_vote": "float",
        "debtor_respect": "float",
        "denom": "int",
        "pdivisor": "int",
        "fcontext": "WayStr",
        "fnigh": "float",
        "fopen": "float",
        "fund_coin": "float",
        "fund_pool": "float",
        "give_force": "float",
        "gogo_want": "float",
        "group_title": "TitleStr",
        "healer_name": "NameStr",
        "mass": "int",
        "max_tree_traverse": "int",
        "morph": "bool",
        "pbranch": "WayStr",
        "pnigh": "float",
        "numor": "int",
        "popen": "float",
        "penny": "float",
        "fbranch": "WayStr",
        "pledge": "bool",
        "problem_bool": "bool",
        "respect_bit": "float",
        "idea_way": "WayStr",
        "stop_want": "float",
        "take_force": "float",
        "tally": "int",
        "labor_title": "TitleStr",
    }


def get_sorted_jkey_keys(atom_dimen: str) -> list[str]:
    atom_config = get_atom_config_dict()
    atom_dimen_config = atom_config.get(atom_dimen)
    atom_jkeys_config = atom_dimen_config.get("jkeys")
    if len(atom_jkeys_config) == 1:
        return list(atom_jkeys_config.keys())
    nesting_order_dict = {
        required_key: required_dict.get("nesting_order")
        for required_key, required_dict in atom_jkeys_config.items()
    }
    sorted_tuples = sorted(nesting_order_dict.items(), key=lambda x: x[1])
    return [x_tuple[0] for x_tuple in sorted_tuples]


def add_to_atom_table_columns(x_dict, atom_dimen, crud, arg_key, arg_value):
    x_dict[f"{atom_dimen}_{crud}_{arg_key}"] = arg_value.get("sqlite_datatype")


def get_flattened_atom_table_build() -> dict[str, any]:
    atom_table_columns = {}
    atom_config = get_atom_config_dict()
    for atom_dimen, dimen_dict in atom_config.items():
        catergory_insert = dimen_dict.get("INSERT")
        catergory_update = dimen_dict.get("UPDATE")
        catergory_delete = dimen_dict.get("DELETE")
        if catergory_insert is not None:
            jkeys = dimen_dict.get("jkeys")
            jvalues = dimen_dict.get("jvalues")
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "INSERT",
                    jkey,
                    x_value,
                )
            for jvalue, x_value in jvalues.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "INSERT",
                    jvalue,
                    x_value,
                )
        if catergory_update is not None:
            jkeys = dimen_dict.get("jkeys")
            jvalues = dimen_dict.get("jvalues")
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "UPDATE",
                    jkey,
                    x_value,
                )
            for jvalue, x_value in jvalues.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "UPDATE",
                    jvalue,
                    x_value,
                )
        if catergory_delete is not None:
            jkeys = dimen_dict.get("jkeys")
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "DELETE",
                    jkey,
                    x_value,
                )
    return atom_table_columns


def get_normalized_bud_table_build() -> dict[str : dict[str, any]]:
    normal_tables_dict = {}
    atom_config = get_atom_config_dict()
    for x_dimen, dimen_dict in atom_config.items():
        normal_tables_dict[x_dimen] = {}
        normal_table_dict = normal_tables_dict.get(x_dimen)

        normal_table_dict["columns"] = {}
        normal_columns_dict = normal_table_dict.get("columns")
        normal_columns_dict["uid"] = {
            "sqlite_datatype": "INTEGER",
            "nullable": False,
            "primary_key": True,
        }
        jkeys = dimen_dict.get("jkeys")
        jvalues = dimen_dict.get("jvalues")
        if jkeys is not None:
            for jkey, x_value in jkeys.items():
                normal_columns_dict[jkey] = {
                    "sqlite_datatype": x_value.get("sqlite_datatype"),
                    "nullable": False,
                }

        if jvalues is not None:
            for jvalue, x_value in jvalues.items():
                normal_columns_dict[jvalue] = {
                    "sqlite_datatype": x_value.get("sqlite_datatype"),
                    "nullable": True,
                }

        normal_table_dict["normal_specs"] = {}
        normal_specs_dict = normal_table_dict.get("normal_specs")
        config_normal_dict = dimen_dict.get("normal_specs")
        table_name = config_normal_dict.get("normal_table_name")
        normal_specs_dict["normal_table_name"] = table_name

    return normal_tables_dict


def save_atom_config_file(atom_config_dict):
    save_json(config_file_dir(), get_atom_config_filename(), atom_config_dict)


def get_bud_dimens() -> set:
    return {
        "budunit",
        "bud_acctunit",
        "bud_acct_membership",
        "bud_ideaunit",
        "bud_idea_awardlink",
        "bud_idea_reasonunit",
        "bud_idea_reason_premiseunit",
        "bud_idea_laborlink",
        "bud_idea_healerlink",
        "bud_idea_factunit",
    }


def get_all_bud_dimen_keys() -> set:
    return {
        "acct_name",
        "awardee_title",
        "rcontext",
        "fcontext",
        "group_title",
        "healer_name",
        "pbranch",
        "owner_name",
        "idea_way",
        "labor_title",
    }


def get_delete_key_name(key: str) -> str:
    return f"{key}_ERASE" if key else None


def get_all_bud_dimen_delete_keys() -> set:
    return {
        "acct_name_ERASE",
        "awardee_title_ERASE",
        "rcontext_ERASE",
        "fcontext_ERASE",
        "group_title_ERASE",
        "healer_name_ERASE",
        "pbranch_ERASE",
        "owner_name_ERASE",
        "idea_way_ERASE",
        "labor_title_ERASE",
    }


def is_bud_dimen(dimen_str: str) -> bool:
    return dimen_str in get_bud_dimens()


def get_atom_order(crud_str: str, dimen: str) -> int:
    return get_from_nested_dict(get_atom_config_dict(), [dimen, crud_str, "atom_order"])


def get_normal_table_name(dimen: str) -> str:
    nested_list = [dimen, "normal_specs", "normal_table_name"]
    return get_from_nested_dict(get_atom_config_dict(), nested_list)


def set_mog(
    crud_str: str,
    dimen: str,
    atom_order_int: int,
) -> int:
    atom_config_dict = get_atom_config_dict()
    dimen_dict = atom_config_dict.get(dimen)
    crud_dict = dimen_dict.get(crud_str)
    crud_dict["atom_order"] = atom_order_int
    save_atom_config_file(atom_config_dict)


def get_dimen_from_dict(x_row_dict: dict) -> str:
    x_get_bud_dimens = get_bud_dimens()
    for x_columnname in x_row_dict:
        for x_dimen in x_get_bud_dimens:
            if x_columnname.find(x_dimen) == 0:
                dimen_len = len(x_dimen)
                return x_dimen, x_columnname[dimen_len + 1 : dimen_len + 7]
