from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    atom_hx_str,
    class_type_str,
    column_order_str,
    crud_str,
    jvalues_str,
    nesting_order_str,
    normal_specs_str,
    normal_table_name_str,
)


def test_str_functions_ReturnsObj():
    assert atom_hx_str() == "atom_hx"
    assert DELETE_str() == "DELETE"
    assert column_order_str() == "column_order"
    assert crud_str() == "crud"
    assert class_type_str() == "class_type"
    assert jvalues_str() == "jvalues"
    assert nesting_order_str() == "nesting_order"
    assert normal_specs_str() == "normal_specs"
    assert normal_table_name_str() == "normal_table_name"
