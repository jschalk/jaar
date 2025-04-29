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
