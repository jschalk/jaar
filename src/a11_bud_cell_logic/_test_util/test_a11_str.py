from src.a11_bud_cell_logic._test_util.a11_str import (
    ancestors_str,
    boss_facts_str,
    bud_owner_name_str,
    celldepth_str,
    found_facts_str,
    mandate_str,
    planadjust_str,
    planevent_facts_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert ancestors_str() == "ancestors"
    assert celldepth_str() == "celldepth"
    assert bud_owner_name_str() == "bud_owner_name"
    assert mandate_str() == "mandate"
    assert planadjust_str() == "planadjust"
    assert planevent_facts_str() == "planevent_facts"
    assert found_facts_str() == "found_facts"
    assert boss_facts_str() == "boss_facts"
