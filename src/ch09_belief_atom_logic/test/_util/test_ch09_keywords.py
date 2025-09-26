from src.ch09_belief_atom_logic._ref.ch09_keywords import (
    CRUD_command_str,
    DELETE_str,
    atom_hx_str,
    atom_str,
    column_order_str,
    crud_str,
    nesting_order_str,
    normal_specs_str,
    normal_table_name_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert CRUD_command_str() == "CRUD_command"
    assert atom_str() == "atom"
    assert atom_hx_str() == "atom_hx"
    assert DELETE_str() == "DELETE"
    assert column_order_str() == "column_order"
    assert crud_str() == "crud"
    assert nesting_order_str() == "nesting_order"
    assert normal_specs_str() == "normal_specs"
    assert normal_table_name_str() == "normal_table_name"
