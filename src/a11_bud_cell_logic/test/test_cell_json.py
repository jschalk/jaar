from src.a02_finance_logic.test._util.a02_str import quota_str
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.a06_str import penny_str
from src.a09_pack_logic.test._util.a09_str import event_int_str
from src.a11_bud_cell_logic.cell import cellunit_get_from_dict, cellunit_shop
from src.a11_bud_cell_logic.test._util.a11_str import (
    ancestors_str,
    boss_facts_str,
    bud_owner_name_str,
    celldepth_str,
    found_facts_str,
    mandate_str,
    planadjust_str,
    planevent_facts_str,
)
from src.a11_bud_cell_logic.test._util.example_factunits import (
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
)


def test_CellUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_event7 = 7
    bob_sue_bud_owner = yao_str
    bob_sue_celldepth3 = 3
    bob_sue_penny2 = 2
    bob_sue_quota300 = 300
    bob_sue_mandate444 = 444
    x_cellunit = cellunit_shop(
        bob_sue_bud_owner,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        mandate=bob_sue_mandate444,
    )

    # WHEN
    x_cell_dict = x_cellunit.get_dict()

    # THEN
    assert list(x_cell_dict.keys()) == [
        ancestors_str(),
        event_int_str(),
        celldepth_str(),
        bud_owner_name_str(),
        penny_str(),
        quota_str(),
        mandate_str(),
        planadjust_str(),
        planevent_facts_str(),
        found_facts_str(),
        boss_facts_str(),
    ]
    assert x_cell_dict.get(ancestors_str()) == bob_sue_ancestors
    assert x_cell_dict.get(event_int_str()) == bob_sue_event7
    assert x_cell_dict.get(celldepth_str()) == bob_sue_celldepth3
    assert x_cell_dict.get(bud_owner_name_str()) == bob_sue_bud_owner
    assert x_cell_dict.get(penny_str()) == bob_sue_penny2
    assert x_cell_dict.get(quota_str()) == bob_sue_quota300
    assert x_cell_dict.get(mandate_str()) == bob_sue_mandate444
    bob_sue_plan = planunit_shop(bob_sue_bud_owner)
    assert x_cell_dict.get(planadjust_str()) == bob_sue_plan.get_dict()
    assert x_cell_dict.get(planevent_facts_str()) == {}
    assert x_cell_dict.get(found_facts_str()) == {}
    assert x_cell_dict.get(boss_facts_str()) == {}


def test_CellUnit_get_dict_ReturnsObj_Scenario1_EmptyPlanAdjust():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_event7 = 7
    bob_sue_celldepth3 = 3
    bob_sue_penny2 = 2
    bob_sue_quota300 = 300
    bob_sue_mandate444 = 444
    x_cellunit = cellunit_shop(
        yao_str,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        mandate=bob_sue_mandate444,
    )
    x_cellunit.planadjust = None

    # WHEN
    x_cell_dict = x_cellunit.get_dict()

    # THEN
    assert list(x_cell_dict.keys()) == [
        ancestors_str(),
        event_int_str(),
        celldepth_str(),
        bud_owner_name_str(),
        penny_str(),
        quota_str(),
        mandate_str(),
        planadjust_str(),
        planevent_facts_str(),
        found_facts_str(),
        boss_facts_str(),
    ]
    assert x_cell_dict.get(ancestors_str()) == bob_sue_ancestors
    assert x_cell_dict.get(event_int_str()) == bob_sue_event7
    assert x_cell_dict.get(celldepth_str()) == bob_sue_celldepth3
    assert x_cell_dict.get(bud_owner_name_str()) == yao_str
    assert x_cell_dict.get(penny_str()) == bob_sue_penny2
    assert x_cell_dict.get(quota_str()) == bob_sue_quota300
    assert x_cell_dict.get(mandate_str()) == bob_sue_mandate444
    bob_sue_plan = planunit_shop(sue_str)
    assert x_cell_dict.get(planadjust_str()) == bob_sue_plan.get_dict()
    assert x_cell_dict.get(planevent_facts_str()) == {}
    assert x_cell_dict.get(found_facts_str()) == {}
    assert x_cell_dict.get(boss_facts_str()) == {}


def test_CellUnit_get_dict_ReturnsObj_Scenario1_WithMoreParameters():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_event7 = 7
    bob_sue_bud_owner = yao_str
    bob_sue_celldepth3 = 3
    bob_sue_penny2 = 2
    bob_sue_quota300 = 300
    bob_sue_mandate444 = 444
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_planevent_factunits = {clean_fact.fcontext: clean_fact}
    bob_sue_found_factunits = {dirty_fact.fcontext: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.fcontext: sky_blue_fact}
    x_cellunit = cellunit_shop(
        bob_sue_bud_owner,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        None,
        bob_sue_planevent_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
        mandate=bob_sue_mandate444,
    )

    # WHEN
    x_cell_dict = x_cellunit.get_dict()

    # THEN
    assert list(x_cell_dict.keys()) == [
        ancestors_str(),
        event_int_str(),
        celldepth_str(),
        bud_owner_name_str(),
        penny_str(),
        quota_str(),
        mandate_str(),
        planadjust_str(),
        planevent_facts_str(),
        found_facts_str(),
        boss_facts_str(),
    ]
    assert x_cell_dict.get(ancestors_str()) == bob_sue_ancestors
    assert x_cell_dict.get(event_int_str()) == bob_sue_event7
    assert x_cell_dict.get(celldepth_str()) == bob_sue_celldepth3
    assert x_cell_dict.get(bud_owner_name_str()) == bob_sue_bud_owner
    assert x_cell_dict.get(penny_str()) == bob_sue_penny2
    assert x_cell_dict.get(quota_str()) == bob_sue_quota300
    assert x_cell_dict.get(mandate_str()) == bob_sue_mandate444
    assert (
        x_cell_dict.get(planadjust_str()) == planunit_shop(bob_sue_bud_owner).get_dict()
    )
    bob_sue_planevent_fact_dicts = {clean_fact.fcontext: clean_fact.get_dict()}
    bob_sue_found_fact_dicts = {dirty_fact.fcontext: dirty_fact.get_dict()}
    bob_sue_boss_fact_dicts = {sky_blue_fact.fcontext: sky_blue_fact.get_dict()}
    assert x_cell_dict.get(planevent_facts_str()) == bob_sue_planevent_fact_dicts
    assert x_cell_dict.get(found_facts_str()) == bob_sue_found_fact_dicts
    assert x_cell_dict.get(boss_facts_str()) == bob_sue_boss_fact_dicts
    assert len(x_cell_dict) == 11


def test_CellUnit_get_json_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_event7 = 7
    bob_sue_bud_owner = yao_str
    bob_sue_celldepth3 = 3
    bob_sue_penny2 = 2
    bob_sue_quota300 = 300
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_planevent_factunits = {clean_fact.fcontext: clean_fact}
    bob_sue_found_factunits = {dirty_fact.fcontext: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.fcontext: sky_blue_fact}
    bob_sue_plan = planunit_shop(bob_sue_bud_owner)
    bob_sue_plan.add_acctunit(sue_str)
    x_cellunit = cellunit_shop(
        bob_sue_bud_owner,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        bob_sue_plan,
        bob_sue_planevent_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
    )

    # WHEN
    x_cell_json = x_cellunit.get_json()

    # THEN
    assert len(x_cell_json) == 1235


def test_cellunit_get_from_dict_ReturnsObj_Scenario0_NoParameters():
    # ESTABLISH
    yao_str = "Yao"
    x_dict = {bud_owner_name_str(): yao_str}

    # WHEN
    gen_cellunit = cellunit_get_from_dict(x_dict)

    # THEN
    assert gen_cellunit == cellunit_shop(yao_str)


def test_cellunit_get_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_event7 = 7
    bob_sue_bud_owner = yao_str
    bob_sue_celldepth3 = 3
    bob_sue_penny2 = 2
    bob_sue_quota300 = 300
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_planevent_factunits = {clean_fact.fcontext: clean_fact}
    bob_sue_found_factunits = {dirty_fact.fcontext: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.fcontext: sky_blue_fact}
    bob_sue_plan = planunit_shop(bob_sue_bud_owner)
    bob_sue_plan.add_acctunit(sue_str)
    bob_sue_cellunit = cellunit_shop(
        bob_sue_bud_owner,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        bob_sue_plan,
        bob_sue_planevent_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
    )
    x_cell_dict = bob_sue_cellunit.get_dict()

    # WHEN
    gen_cellunit = cellunit_get_from_dict(x_cell_dict)

    # THEN
    assert gen_cellunit == bob_sue_cellunit
