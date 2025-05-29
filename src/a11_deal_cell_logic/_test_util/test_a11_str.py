from src.a11_deal_cell_logic._test_util.a11_str import (
    ancestors_str,
    celldepth_str,
    deal_owner_name_str,
    mandate_str,
    budadjust_str,
    budevent_facts_str,
    found_facts_str,
    boss_facts_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert ancestors_str() == "ancestors"
    assert celldepth_str() == "celldepth"
    assert deal_owner_name_str() == "deal_owner_name"
    assert mandate_str() == "mandate"
    assert budadjust_str() == "budadjust"
    assert budevent_facts_str() == "budevent_facts"
    assert found_facts_str() == "found_facts"
    assert boss_facts_str() == "boss_facts"
