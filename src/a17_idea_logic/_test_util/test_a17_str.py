from src.a17_idea_logic._test_util.a17_str import (
    idea_number_str,
    idea_category_str,
    allowed_crud_str,
    dimens_str,
    attributes_str,
    insert_one_time_str,
    insert_multiple_str,
    delete_insert_update_str,
    insert_update_str,
    delete_insert_str,
    delete_update_str,
    build_order_str,
    brick_raw_str,
    brick_agg_str,
    brick_valid_str,
    sound_raw_str,
    sound_agg_str,
    voice_raw_str,
    voice_agg_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert idea_number_str() == "idea_number"
    assert idea_category_str() == "idea_category"
    assert allowed_crud_str() == "allowed_crud"
    assert dimens_str() == "dimens"
    assert attributes_str() == "attributes"
    assert insert_one_time_str() == "insert_one_time"
    assert insert_multiple_str() == "insert_multiple"
    assert delete_insert_update_str() == "delete_insert_update"
    assert insert_update_str() == "insert_update"
    assert delete_insert_str() == "delete_insert"
    assert delete_update_str() == "delete_update"
    assert build_order_str() == "build_order"
    assert brick_raw_str() == "brick_raw"
    assert brick_agg_str() == "brick_agg"
    assert brick_valid_str() == "brick_valid"
    assert sound_raw_str() == "sound_raw"
    assert sound_agg_str() == "sound_agg"
    assert voice_raw_str() == "voice_raw"
    assert voice_agg_str() == "voice_agg"
