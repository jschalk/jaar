from src.ch17_idea_logic._ref.ch17_terms import (
    allowed_crud_str,
    build_order_str,
    delete_insert_str,
    delete_insert_update_str,
    delete_update_str,
    error_message_str,
    idea_category_str,
    idea_number_str,
    insert_multiple_str,
    insert_one_time_str,
    insert_update_str,
    world_name_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert allowed_crud_str() == "allowed_crud"
    assert build_order_str() == "build_order"
    assert delete_insert_str() == "delete_insert"
    assert delete_insert_update_str() == "delete_insert_update"
    assert delete_update_str() == "delete_update"
    assert error_message_str() == "error_message"
    assert idea_number_str() == "idea_number"
    assert idea_category_str() == "idea_category"
    assert insert_one_time_str() == "insert_one_time"
    assert insert_multiple_str() == "insert_multiple"
    assert insert_update_str() == "insert_update"
    assert world_name_str() == "world_name"
