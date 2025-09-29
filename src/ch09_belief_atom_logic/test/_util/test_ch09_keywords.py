from src.ch09_belief_atom_logic._ref.ch09_keywords import (
    Ch09Keywords,
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


def test_Ch09Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch09Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert CRUD_command_str() == "CRUD_command"
    assert DELETE_str() == "DELETE"
    assert atom_str() == "atom"
    assert atom_hx_str() == "atom_hx"
    assert column_order_str() == "column_order"
    assert crud_str() == "crud"
    assert nesting_order_str() == "nesting_order"
    assert normal_specs_str() == "normal_specs"
    assert normal_table_name_str() == "normal_table_name"
