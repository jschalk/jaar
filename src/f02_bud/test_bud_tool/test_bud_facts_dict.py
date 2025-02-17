from src.f01_road.road import create_road
from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import get_bud_root_facts_dict


def test_get_bud_root_facts_dict_ReturnsObj_Scenario0_No_factunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    # WHEN / THEN
    assert get_bud_root_facts_dict(sue_bud) == {}
    assert get_bud_root_facts_dict(sue_bud) == sue_bud.get_factunits_dict()


def test_get_bud_root_facts_dict_ReturnsObj_Scenario1_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    casa_road = sue_bud.make_l1_road("case")
    clean_road = sue_bud.make_l1_road("clean")
    dirty_road = sue_bud.make_l1_road("dirty")
    sue_bud.add_fact(casa_road, dirty_road, create_missing_items=True)

    # WHEN
    sue_fact_dict = get_bud_root_facts_dict(sue_bud)

    # THEN
    assert sue_fact_dict.get(casa_road) != None
    casa_fact_dict = sue_fact_dict.get(casa_road)
    assert casa_fact_dict.get("base") == casa_road
    assert casa_fact_dict.get("pick") == dirty_road
    expected_sue_fact_dict = {casa_road: {"base": casa_road, "pick": dirty_road}}
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_get_bud_root_facts_dict_ReturnsObj_Scenario2_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    casa_road = sue_bud.make_l1_road("case")
    clean_road = sue_bud.make_l1_road("clean")
    dirty_road = sue_bud.make_l1_road("dirty")
    dirty_open = 10
    dirty_nigh = 13
    sue_bud.add_fact(casa_road, dirty_road, dirty_open, dirty_nigh, True)

    # WHEN
    sue_fact_dict = get_bud_root_facts_dict(sue_bud)

    # THEN
    assert sue_fact_dict.get(casa_road) != None
    casa_fact_dict = sue_fact_dict.get(casa_road)
    assert casa_fact_dict.get("base") == casa_road
    assert casa_fact_dict.get("pick") == dirty_road
    assert casa_fact_dict.get("fopen") == dirty_open
    assert casa_fact_dict.get("fnigh") == dirty_nigh
    expected_sue_fact_dict = {
        casa_road: {
            "base": casa_road,
            "pick": dirty_road,
            "fopen": dirty_open,
            "fnigh": dirty_nigh,
        }
    }
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict
