from src.f00_instrument.file import open_file, save_file, create_path
from src.f00_instrument.dict_toolbox import (
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


def jaar_type_str() -> str:
    return "jaar_type"


def type_AcctID_str() -> str:
    return "AcctID"


def type_GroupID_str() -> str:
    return "GroupID"


def type_RoadUnit_str() -> str:
    return "RoadUnit"


def type_IdeaUnit_str() -> str:
    return "IdeaUnit"


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


def category_str() -> str:
    return "category"


def crud_str() -> str:
    return "crud"


def face_id_str() -> str:
    return "face_id"


def deal_id_str() -> str:
    return "deal_id"


def owner_id_str() -> str:
    return "owner_id"


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


def acct_id_str() -> str:
    return "acct_id"


def awardee_id_str() -> str:
    return "awardee_id"


def give_force_str() -> str:
    return "give_force"


def take_force_str() -> str:
    return "take_force"


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


def lx_str() -> str:
    return "lx"


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
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "f04_gift")


def get_atom_config_dict() -> dict:
    return get_dict_from_json(open_file(config_file_dir(), get_atom_config_file_name()))


def get_atom_config_jkeys(x_cat: str) -> dict:
    jkeys_key_list = [x_cat, jkeys_str()]
    return get_from_nested_dict(get_atom_config_dict(), jkeys_key_list)


def get_atom_config_jvalues(x_cat: str) -> dict:
    jvalues_key_list = [x_cat, jvalues_str()]
    return get_from_nested_dict(get_atom_config_dict(), jvalues_key_list)


def get_atom_config_args(x_category: str) -> dict[str, dict]:
    args_dict = get_atom_config_jkeys(x_category)
    args_dict.update(get_atom_config_jvalues(x_category))
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


def get_allowed_jaar_types() -> set[str]:
    return {
        "AcctID",
        "bool",
        "float",
        "GroupID",
        "int",
        "IdeaUnit",
        "RoadUnit",
        "TimeLinePoint",
    }


def get_atom_args_jaar_types() -> dict[str, str]:
    return {
        "acct_id": "AcctID",
        "addin": "float",
        "awardee_id": "GroupID",
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
        "lx": "IdeaUnit",
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
        "purview_time_int": "TimeLinePoint",
        "respect_bit": "float",
        "road": "RoadUnit",
        "stop_want": "float",
        "take_force": "float",
        "tally": "int",
        "team_id": "GroupID",
    }


def get_sorted_jkey_keys(atom_category: str) -> list[str]:
    atom_config = get_atom_config_dict()
    atom_category_config = atom_config.get(atom_category)
    atom_jkeys_config = atom_category_config.get(jkeys_str())
    if len(atom_jkeys_config) == 1:
        return list(atom_jkeys_config.keys())
    nesting_order_dict = {
        required_key: required_dict.get(nesting_order_str())
        for required_key, required_dict in atom_jkeys_config.items()
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
            jkeys = category_dict.get(jkeys_str())
            jvalues = category_dict.get(jvalues_str())
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_insert(),
                    jkey,
                    x_value,
                )
            for jvalue, x_value in jvalues.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_insert(),
                    jvalue,
                    x_value,
                )
        if catergory_update is not None:
            jkeys = category_dict.get(jkeys_str())
            jvalues = category_dict.get(jvalues_str())
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_update(),
                    jkey,
                    x_value,
                )
            for jvalue, x_value in jvalues.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_update(),
                    jvalue,
                    x_value,
                )
        if catergory_delete is not None:
            jkeys = category_dict.get(jkeys_str())
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_delete(),
                    jkey,
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
        jkeys = category_dict.get(jkeys_str())
        jvalues = category_dict.get(jvalues_str())
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
        config_normal_dict = category_dict.get(normal_specs_str())
        table_name = config_normal_dict.get(normal_table_name_str())
        normal_specs_dict[normal_table_name_str()] = table_name

    return normal_tables_dict


def save_atom_config_file(atom_config_dict):
    x_file_str = get_json_from_dict(atom_config_dict)
    save_file(config_file_dir(), get_atom_config_file_name(), x_file_str)


def get_atom_categorys() -> set:
    return set(get_atom_config_dict().keys())


def is_atom_category(category_str: str) -> bool:
    return category_str in get_atom_categorys()


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
    x_get_atom_categorys = get_atom_categorys()
    for x_columnname in x_row_dict:
        for x_category in x_get_atom_categorys:
            if x_columnname.find(x_category) == 0:
                category_len = len(x_category)
                return x_category, x_columnname[category_len + 1 : category_len + 7]
