from src.a17_idea_logic._util.a17_str import (
    allowed_crud_str,
    brick_raw_str,
    build_order_str,
    delete_insert_str,
    delete_insert_update_str,
    delete_update_str,
    idea_category_str,
    idea_number_str,
    insert_multiple_str,
    insert_one_time_str,
    insert_update_str,
    world_id_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert brick_raw_str() == "brick_raw"
    assert idea_number_str() == "idea_number"
    assert idea_category_str() == "idea_category"
    assert allowed_crud_str() == "allowed_crud"
    assert insert_one_time_str() == "insert_one_time"
    assert insert_multiple_str() == "insert_multiple"
    assert delete_insert_update_str() == "delete_insert_update"
    assert insert_update_str() == "insert_update"
    assert delete_insert_str() == "delete_insert"
    assert delete_update_str() == "delete_update"
    assert build_order_str() == "build_order"
    assert world_id_str() == "world_id"
