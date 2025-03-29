from src.f00_instrument.file import open_json, save_json, create_path
from src.f00_instrument.dict_toolbox import get_from_nested_dict
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


def class_type_str() -> str:
    return "class_type"


def type_AcctName_str() -> str:
    return "NameUnit"


def type_LabelUnit_str() -> str:
    return "LabelUnit"


def type_RoadUnit_str() -> str:
    return "RoadUnit"


def type_TitleUnit_str() -> str:
    return "TitleUnit"


def nullable_str() -> str:
    return "nullable"


def nesting_order_str() -> str:
    return "nesting_order"


def jkeys_str() -> str:
    return "jkeys"


def jvalues_str() -> str:
    return "jvalues"


def column_order_str() -> str:
    return "column_order"


def dimen_str() -> str:
    return "dimen"


def crud_str() -> str:
    return "crud"


def face_name_str() -> str:
    return "face_name"


def event_int_str() -> str:
    return "event_int"


def credor_respect_str() -> str:
    return "credor_respect"


def debtor_respect_str() -> str:
    return "debtor_respect"


def fund_coin_str() -> str:
    return "fund_coin"


def penny_str() -> str:
    return "penny"


def respect_bit_str() -> str:
    return "respect_bit"


def acct_name_str() -> str:
    return "acct_name"


def awardee_tag_str() -> str:
    return "awardee_tag"


def give_force_str() -> str:
    return "give_force"


def take_force_str() -> str:
    return "take_force"


def group_label_str() -> str:
    return "group_label"


def team_tag_str() -> str:
    return "team_tag"


def healer_name_str() -> str:
    return "healer_name"


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


def item_title_str() -> str:
    return "item_title"


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


def get_atom_config_filename() -> str:
    return "atom_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "f04_stand")


def get_atom_config_dict() -> dict:
    return open_json(config_file_dir(), get_atom_config_filename())


def get_atom_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, jkeys_str()]
    return get_from_nested_dict(get_atom_config_dict(), jkeys_key_list)


def get_atom_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, jvalues_str()]
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
        "NameUnit",
        "bool",
        "float",
        "LabelUnit",
        "int",
        "TitleUnit",
        "RoadUnit",
        "TimeLinePoint",
    }


def get_atom_args_class_types() -> dict[str, str]:
    return {
        "acct_name": "NameUnit",
        "addin": "float",
        "awardee_tag": "LabelUnit",
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
        "group_label": "LabelUnit",
        "healer_name": "NameUnit",
        "item_title": "TitleUnit",
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
        "respect_bit": "float",
        "road": "RoadUnit",
        "stop_want": "float",
        "take_force": "float",
        "tally": "int",
        "team_tag": "LabelUnit",
    }


def get_sorted_jkey_keys(atom_dimen: str) -> list[str]:
    atom_config = get_atom_config_dict()
    atom_dimen_config = atom_config.get(atom_dimen)
    atom_jkeys_config = atom_dimen_config.get(jkeys_str())
    if len(atom_jkeys_config) == 1:
        return list(atom_jkeys_config.keys())
    nesting_order_dict = {
        required_key: required_dict.get(nesting_order_str())
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
        catergory_insert = dimen_dict.get(atom_insert())
        catergory_update = dimen_dict.get(atom_update())
        catergory_delete = dimen_dict.get(atom_delete())
        if catergory_insert is not None:
            jkeys = dimen_dict.get(jkeys_str())
            jvalues = dimen_dict.get(jvalues_str())
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    atom_insert(),
                    jkey,
                    x_value,
                )
            for jvalue, x_value in jvalues.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    atom_insert(),
                    jvalue,
                    x_value,
                )
        if catergory_update is not None:
            jkeys = dimen_dict.get(jkeys_str())
            jvalues = dimen_dict.get(jvalues_str())
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    atom_update(),
                    jkey,
                    x_value,
                )
            for jvalue, x_value in jvalues.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    atom_update(),
                    jvalue,
                    x_value,
                )
        if catergory_delete is not None:
            jkeys = dimen_dict.get(jkeys_str())
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    atom_delete(),
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

        normal_table_dict[columns_str()] = {}
        normal_columns_dict = normal_table_dict.get(columns_str())
        normal_columns_dict["uid"] = {
            sqlite_datatype_str(): "INTEGER",
            nullable_str(): False,
            "primary_key": True,
        }
        jkeys = dimen_dict.get(jkeys_str())
        jvalues = dimen_dict.get(jvalues_str())
        if jkeys is not None:
            for jkey, x_value in jkeys.items():
                normal_columns_dict[jkey] = {
                    sqlite_datatype_str(): x_value.get(sqlite_datatype_str()),
                    nullable_str(): False,
                }

        if jvalues is not None:
            for jvalue, x_value in jvalues.items():
                normal_columns_dict[jvalue] = {
                    sqlite_datatype_str(): x_value.get(sqlite_datatype_str()),
                    nullable_str(): True,
                }

        normal_table_dict[normal_specs_str()] = {}
        normal_specs_dict = normal_table_dict.get(normal_specs_str())
        config_normal_dict = dimen_dict.get(normal_specs_str())
        table_name = config_normal_dict.get(normal_table_name_str())
        normal_specs_dict[normal_table_name_str()] = table_name

    return normal_tables_dict


def save_atom_config_file(atom_config_dict):
    save_json(config_file_dir(), get_atom_config_filename(), atom_config_dict)


def get_bud_dimens() -> set:
    return {
        "budunit",
        "bud_acctunit",
        "bud_acct_membership",
        "bud_itemunit",
        "bud_item_awardlink",
        "bud_item_reasonunit",
        "bud_item_reason_premiseunit",
        "bud_item_teamlink",
        "bud_item_healerlink",
        "bud_item_factunit",
    }


def get_all_bud_dimen_keys() -> set:
    return {
        "acct_name",
        "awardee_tag",
        "base",
        "group_label",
        "healer_name",
        "item_title",
        "need",
        "owner_name",
        "parent_road",
        "road",
        "team_tag",
    }


def get_delete_key_name(key: str) -> str:
    return f"{key}_ERASE" if key else None


def get_all_bud_dimen_delete_keys() -> set:
    return {
        "acct_name_ERASE",
        "awardee_tag_ERASE",
        "base_ERASE",
        "group_label_ERASE",
        "healer_name_ERASE",
        "item_title_ERASE",
        "need_ERASE",
        "owner_name_ERASE",
        "parent_road_ERASE",
        "road_ERASE",
        "team_tag_ERASE",
    }


def is_bud_dimen(dimen_str: str) -> bool:
    return dimen_str in get_bud_dimens()


def get_atom_order(crud_str: str, dimen: str) -> int:
    return get_from_nested_dict(get_atom_config_dict(), [dimen, crud_str, "atom_order"])


def get_normal_table_name(dimen: str) -> str:
    nested_list = [dimen, normal_specs_str(), normal_table_name_str()]
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
