from src.a08_bud_atom_logic._test_util.a08_str import (
    atom_insert,
    atom_delete,
    atom_update,
    dimen_str,
    column_order_str,
    crud_str,
    class_type_str,
    jkeys_str,
    jvalues_str,
    nesting_order_str,
    normal_specs_str,
    normal_table_name_str,
    sqlite_datatype_str,
)


def test_str_functions_ReturnsObj():
    assert atom_insert() == "INSERT"
    assert atom_update() == "UPDATE"
    assert atom_delete() == "DELETE"
    assert dimen_str() == "dimen"
    assert column_order_str() == "column_order"
    assert crud_str() == "crud"
    assert class_type_str() == "class_type"
    assert jkeys_str() == "jkeys"
    assert jvalues_str() == "jvalues"
    assert nesting_order_str() == "nesting_order"
    assert normal_specs_str() == "normal_specs"
    assert normal_table_name_str() == "normal_table_name"
    assert sqlite_datatype_str() == "sqlite_datatype"
