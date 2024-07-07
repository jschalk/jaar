from src._instrument.file import open_file, save_file
from src._instrument.python import (
    get_json_from_dict,
    get_dict_from_json,
    get_nested_value,
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


def normal_specs_text() -> str:
    return "normal_specs"


def normal_table_name_text() -> str:
    return "normal_table_name"


def columns_text() -> str:
    return "columns"


def sqlite_datatype_text() -> str:
    return "sqlite_datatype"


def python_type_text() -> str:
    return "python_type"


def nullable_text() -> str:
    return "nullable"


def required_args_text() -> str:
    return "required_args"


def optional_args_text() -> str:
    return "optional_args"


def worldunit_text() -> str:
    return "worldunit"


def world_charunit_text() -> str:
    return "world_charunit"


def world_char_beliefhold_text() -> str:
    return "world_char_beliefhold"


def world_ideaunit_text() -> str:
    return "world_ideaunit"


def world_idea_fiscallink_text() -> str:
    return "world_idea_fiscallink"


def world_idea_reasonunit_text() -> str:
    return "world_idea_reasonunit"


def world_idea_reason_premiseunit_text() -> str:
    return "world_idea_reason_premiseunit"


def world_idea_heldbelief_text() -> str:
    return "world_idea_heldbelief"


def world_idea_healerhold_text() -> str:
    return "world_idea_healerhold"


def world_idea_factunit_text() -> str:
    return "world_idea_factunit"


def get_atom_config_file_name() -> str:
    return "atom_config.json"


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/gift"


def get_atom_config_dict() -> dict:
    return get_dict_from_json(open_file(config_file_dir(), get_atom_config_file_name()))


def add_to_atom_table_columns(x_dict, atom_category, crud, arg_key, arg_value):
    x_dict[f"{atom_category}_{crud}_{arg_key}"] = arg_value.get("sqlite_datatype")


def get_flattened_atom_table_build() -> dict[str,]:
    atom_table_columns = {}
    atom_config = get_atom_config_dict()
    for atom_category, category_dict in atom_config.items():
        catergory_insert = category_dict.get(atom_insert())
        catergory_update = category_dict.get(atom_update())
        catergory_delete = category_dict.get(atom_delete())
        if catergory_insert != None:
            required_args = category_dict.get(required_args_text())
            optional_args = category_dict.get(optional_args_text())
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
        if catergory_update != None:
            required_args = category_dict.get(required_args_text())
            optional_args = category_dict.get(optional_args_text())
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
        if catergory_delete != None:
            required_args = category_dict.get(required_args_text())
            for required_arg, x_value in required_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_delete(),
                    required_arg,
                    x_value,
                )
    return atom_table_columns


def get_normalized_world_table_build() -> dict[str : dict[str,]]:
    normal_tables_dict = {}
    atom_config = get_atom_config_dict()
    for x_category, category_dict in atom_config.items():
        normal_tables_dict[x_category] = {}
        normal_table_dict = normal_tables_dict.get(x_category)

        normal_table_dict[columns_text()] = {}
        normal_columns_dict = normal_table_dict.get(columns_text())
        normal_columns_dict["uid"] = {
            sqlite_datatype_text(): "INTEGER",
            nullable_text(): False,
            "primary_key": True,
        }
        required_args = category_dict.get(required_args_text())
        optional_args = category_dict.get(optional_args_text())
        if required_args != None:
            for required_arg, x_value in required_args.items():
                normal_columns_dict[required_arg] = {
                    sqlite_datatype_text(): x_value.get(sqlite_datatype_text()),
                    nullable_text(): False,
                }

        if optional_args != None:
            for optional_arg, x_value in optional_args.items():
                normal_columns_dict[optional_arg] = {
                    sqlite_datatype_text(): x_value.get(sqlite_datatype_text()),
                    nullable_text(): True,
                }

        normal_table_dict[normal_specs_text()] = {}
        normal_specs_dict = normal_table_dict.get(normal_specs_text())
        config_normal_dict = category_dict.get(normal_specs_text())
        table_name = config_normal_dict.get(normal_table_name_text())
        normal_specs_dict[normal_table_name_text()] = table_name

    return normal_tables_dict


def save_atom_config_file(atom_config_dict):
    save_file(
        dest_dir=config_file_dir(),
        file_name=get_atom_config_file_name(),
        file_text=get_json_from_dict(atom_config_dict),
    )


def category_ref() -> set:
    return get_atom_config_dict().keys()


def is_category_ref(category_text: str) -> bool:
    return category_text in category_ref()


def get_atom_order(crud_text: str, category: str) -> int:
    return get_nested_value(get_atom_config_dict(), [category, crud_text, "atom_order"])


def get_normal_table_name(category: str) -> str:
    return get_nested_value(
        get_atom_config_dict(), [category, "normal_specs", "normal_table_name"]
    )


def set_mog(
    crud_text: str,
    category: str,
    atom_order_int: int,
) -> int:
    atom_config_dict = get_atom_config_dict()
    category_dict = atom_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    crud_dict["atom_order"] = atom_order_int
    save_atom_config_file(atom_config_dict)


def get_category_from_dict(x_row_dict: dict) -> str:
    x_category_ref = category_ref()
    for x_columnname in x_row_dict:
        for x_category in x_category_ref:
            if x_columnname.find(x_category) == 0:
                category_len = len(x_category)
                return x_category, x_columnname[category_len + 1 : category_len + 7]
