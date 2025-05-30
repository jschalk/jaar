from copy import deepcopy as copy_deepcopy
from src.a01_term_logic.way import create_way
from src.a04_reason_logic.reason_concept import factunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a11_deal_cell_logic._test_util.a11_str import (
    ancestors_str,
    boss_facts_str,
    budadjust_str,
    budevent_facts_str,
    celldepth_str,
    deal_owner_name_str,
    found_facts_str,
    mandate_str,
)
from src.a11_deal_cell_logic._test_util.example_factunits import (
    example_casa_clean_factunit as clean_factunit,
)
from src.a11_deal_cell_logic._test_util.example_factunits import (
    example_casa_dirty_factunit as dirty_factunit,
)
from src.a11_deal_cell_logic._test_util.example_factunits import (
    example_casa_grimy_factunit as grimy_factunit,
)
from src.a11_deal_cell_logic._test_util.example_factunits import (
    example_sky_blue_factunit as sky_blue_factunit,
)
from src.a11_deal_cell_logic.cell import (
    CELLNODE_QUOTA_DEFAULT,
    CellUnit,
    cellunit_shop,
    create_child_cellunits,
)


def test_CELLNODE_QUOTA_DEFAULT_value():
    # ESTABLISH / WHEN / THEN
    assert CELLNODE_QUOTA_DEFAULT == 1000


def test_CellUnit_Exists():
    # ESTABLISH / WHEN
    x_cellunit = CellUnit()
    # THEN
    assert not x_cellunit.ancestors
    assert not x_cellunit.event_int
    assert not x_cellunit.celldepth
    assert not x_cellunit.deal_owner_name
    assert not x_cellunit.penny
    assert not x_cellunit.quota
    assert not x_cellunit.mandate
    assert not x_cellunit.budadjust
    assert not x_cellunit._reason_rcontexts
    assert not x_cellunit._acct_mandate_ledger
    assert not x_cellunit.budevent_facts
    assert not x_cellunit.found_facts
    assert not x_cellunit.boss_facts


def test_cellunit_shop_ReturnsObj_Scenario0_WithoutParameters():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    x_cellunit = cellunit_shop(bob_str)
    # THEN
    assert x_cellunit.deal_owner_name == bob_str
    assert x_cellunit.ancestors == []
    assert not x_cellunit.event_int
    assert x_cellunit.celldepth == 0
    assert x_cellunit.penny == 1
    assert x_cellunit.quota == CELLNODE_QUOTA_DEFAULT
    assert x_cellunit.mandate == CELLNODE_QUOTA_DEFAULT
    assert x_cellunit.budadjust.get_dict() == budunit_shop(bob_str).get_dict()
    assert x_cellunit.budevent_facts == {}
    assert x_cellunit._reason_rcontexts == set()
    assert x_cellunit._acct_mandate_ledger == {}
    assert x_cellunit.found_facts == {}
    assert x_cellunit.boss_facts == {}


def test_cellunit_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_event7 = 7
    bob_sue_deal_owner = yao_str
    bob_sue_celldepth3 = 3
    bob_sue_penny2 = 2
    bob_sue_quota300 = 300
    bob_sue_mandate = 444
    bob_sue_bud = budunit_shop(sue_str)
    bob_sue_bud.add_acctunit(bob_str, 7, 13)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_budevent_factunits = {clean_fact.fcontext: clean_fact}
    bob_sue_found_factunits = {dirty_fact.fcontext: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.fcontext: sky_blue_fact}

    # WHEN
    x_cellunit = cellunit_shop(
        bob_sue_deal_owner,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        bob_sue_bud,
        bob_sue_budevent_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
        bob_sue_mandate,
    )

    # THEN
    assert x_cellunit.ancestors == bob_sue_ancestors
    assert x_cellunit.event_int == bob_sue_event7
    assert x_cellunit.celldepth == bob_sue_celldepth3
    assert x_cellunit.deal_owner_name == bob_sue_deal_owner
    assert x_cellunit.penny == bob_sue_penny2
    assert x_cellunit.quota == bob_sue_quota300
    assert x_cellunit.mandate == bob_sue_mandate
    assert x_cellunit.budadjust == bob_sue_bud
    assert x_cellunit._reason_rcontexts == set()
    assert x_cellunit.budevent_facts == bob_sue_budevent_factunits
    assert x_cellunit.found_facts == bob_sue_found_factunits
    assert x_cellunit.boss_facts == bob_sue_boss_factunits


def test_cellunit_shop_ReturnsObj_Scenario2_WithReasonRcontexts():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str, "accord23")
    casa_way = sue_bud.make_l1_way("casa")
    mop_way = sue_bud.make_way(casa_way, "mop")
    clean_fact = clean_factunit()
    sue_bud.add_concept(clean_factunit().fstate)
    sue_bud.add_concept(mop_way, pledge=True)
    sue_bud.edit_reason(mop_way, clean_fact.fcontext, clean_fact.fstate)

    # WHEN
    x_cellunit = cellunit_shop(sue_str, budadjust=sue_bud)

    # THEN
    assert x_cellunit.deal_owner_name == sue_str
    assert x_cellunit.budadjust == sue_bud
    assert x_cellunit._reason_rcontexts == sue_bud.get_reason_rcontexts()
    assert len(x_cellunit._reason_rcontexts) == 1


def test_cellunit_shop_ReturnsObj_Scenario3_clear_facts():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str, "accord23")
    casa_way = sue_bud.make_l1_way("casa")
    mop_way = sue_bud.make_way(casa_way, "mop")
    clean_fact = clean_factunit()
    sue_bud.add_concept(clean_factunit().fstate)
    sue_bud.add_concept(mop_way, pledge=True)
    sue_bud.edit_reason(mop_way, clean_fact.fcontext, clean_fact.fstate)
    sue_bud.add_fact(clean_fact.fcontext, clean_fact.fstate)
    assert len(sue_bud.get_factunits_dict()) == 1

    # WHEN
    x_cellunit = cellunit_shop(sue_str, budadjust=sue_bud)

    # THEN
    assert len(x_cellunit.budadjust.get_factunits_dict()) == 0
    assert x_cellunit.budadjust != sue_bud


def test_Cellunit_get_cell_owner_name_ReturnsObj_Scenario0_NoAncestors():
    # ESTABLISH
    yao_str = "Yao"
    root_cellunit = cellunit_shop(yao_str, [])

    # WHEN / THEN
    assert root_cellunit.get_cell_owner_name() == yao_str


def test_Cellunit_get_cell_owner_name_ReturnsObj_Scenario1_WithAncestors():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_deal_owner = yao_str
    bob_sue_cellunit = cellunit_shop(bob_sue_deal_owner, bob_sue_ancestors)

    # WHEN
    bob_sue_cell_owner_name = bob_sue_cellunit.get_cell_owner_name()

    # THEN
    assert bob_sue_cell_owner_name == sue_str


def test_CellUnit_eval_budevent_SetsAttr_Scenario0_ParameterIsNone():
    # ESTABLISH
    yao_str = "Yao"
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.budadjust = "testing_place_holder"
    yao_cellunit.budevent_facts = "testing_place_holder"
    yao_cellunit._reason_rcontexts = "testing_place_holder"
    assert yao_cellunit.budadjust
    assert yao_cellunit.budevent_facts != {}
    assert yao_cellunit._reason_rcontexts != set()

    # WHEN
    yao_cellunit.eval_budevent(None)

    # THEN
    assert yao_cellunit.budadjust is None
    assert yao_cellunit.budevent_facts == {}
    assert yao_cellunit._reason_rcontexts == set()


def test_CellUnit_eval_budevent_SetsAttr_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    casa_way = yao_bud.make_l1_way("casa")
    mop_way = yao_bud.make_way(casa_way, "mop")
    clean_fact = clean_factunit()
    yao_bud.add_concept(clean_fact.fstate)
    yao_bud.add_concept(mop_way, pledge=True)
    yao_bud.edit_reason(mop_way, clean_fact.fcontext, clean_fact.fstate)
    yao_bud.add_fact(
        clean_fact.fcontext, clean_fact.fstate, create_missing_concepts=True
    )
    yao_cellunit = cellunit_shop(yao_str)
    assert yao_cellunit.budevent_facts == {}
    assert yao_cellunit._reason_rcontexts == set()

    # WHEN
    yao_cellunit.eval_budevent(yao_bud)

    # THEN
    expected_factunits = {clean_fact.fcontext: clean_fact}
    assert yao_cellunit.budevent_facts == expected_factunits
    assert yao_cellunit._reason_rcontexts == yao_bud.get_reason_rcontexts()
    assert len(yao_cellunit._reason_rcontexts) == 1
    expected_adjust_bud = copy_deepcopy(yao_bud)
    expected_adjust_bud.del_fact(clean_fact.fcontext)
    expected_adjust_bud.settle_bud()
    expected_conceptroot = expected_adjust_bud.conceptroot
    generated_conceptroot = yao_cellunit.budadjust.conceptroot
    assert yao_cellunit.budadjust.get_dict() != yao_bud.get_dict()
    assert generated_conceptroot.get_dict() == expected_conceptroot.get_dict()
    assert yao_cellunit.budadjust.get_dict() == expected_adjust_bud.get_dict()


def test_CellUnit_get_budevents_credit_ledger_ReturnsObj_Scenario0_NoBud():
    # ESTABLISH
    yao_str = "Yao"
    yao_cellunit = cellunit_shop(yao_str)

    # WHEN
    gen_credit_ledger = yao_cellunit.get_budevents_credit_ledger()

    # THEN
    assert gen_credit_ledger == {}


def test_get_budevents_credit_ledger_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_acctunit(sue_str, 3, 5)
    sue_bud.add_acctunit(yao_str, 7, 2)
    sue_cell = cellunit_shop(yao_str, budadjust=sue_bud)

    # WHEN
    gen_credit_ledger = sue_cell.get_budevents_credit_ledger()

    # THEN
    expected_credit_ledger = {sue_str: 3, yao_str: 7}
    assert gen_credit_ledger == expected_credit_ledger


def test_CellUnit_get_budevents_quota_ledger_ReturnsObj_Scenario0_NoBud():
    # ESTABLISH
    yao_str = "Yao"
    yao_cellunit = cellunit_shop(yao_str)

    # WHEN
    gen_credit_ledger = yao_cellunit.get_budevents_quota_ledger()

    # THEN
    assert gen_credit_ledger == {}


def test_get_budevents_quota_ledger_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_acctunit(sue_str, 3, 5)
    sue_bud.add_acctunit(yao_str, 7, 2)
    sue_cell = cellunit_shop(yao_str, quota=55, budadjust=sue_bud)

    # WHEN
    gen_credit_ledger = sue_cell.get_budevents_quota_ledger()

    # THEN
    expected_credit_ledger = {sue_str: 16, yao_str: 39}
    assert gen_credit_ledger == expected_credit_ledger


def test_CellUnit_set_found_facts_from_dict_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(
        clean_fact.fcontext, clean_fact.fstate, create_missing_concepts=True
    )
    yao_found_fact_dict = {clean_fact.fcontext: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    assert yao_cellunit.found_facts == {}

    # WHEN
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)

    # THEN
    expected_factunits = {clean_fact.fcontext: clean_fact}
    assert yao_cellunit.found_facts == expected_factunits


def test_CellUnit_set_budevent_facts_from_dict_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(
        clean_fact.fcontext, clean_fact.fstate, create_missing_concepts=True
    )
    yao_found_fact_dict = {clean_fact.fcontext: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    assert yao_cellunit.budevent_facts == {}

    # WHEN
    yao_cellunit.set_budevent_facts_from_dict(yao_found_fact_dict)

    # THEN
    expected_factunits = {clean_fact.fcontext: clean_fact}
    assert yao_cellunit.budevent_facts == expected_factunits


def test_CellUnit_set_boss_facts_from_other_facts_SetsAttr_Scenario0_found_facts_only():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(
        clean_fact.fcontext, clean_fact.fstate, create_missing_concepts=True
    )
    yao_found_fact_dict = {clean_fact.fcontext: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    yao_cellunit.boss_facts = "testing_str"
    assert len(yao_cellunit.found_facts) == 1
    assert yao_cellunit.boss_facts == "testing_str"

    # WHEN
    yao_cellunit.set_boss_facts_from_other_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.found_facts
    assert yao_cellunit.boss_facts == {clean_fact.fcontext: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_set_boss_facts_from_other_facts_SetsAttr_Scenario1_budevent_facts_only():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(
        clean_fact.fcontext, clean_fact.fstate, create_missing_concepts=True
    )
    yao_found_fact_dict = {clean_fact.fcontext: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_budevent_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.budevent_facts) == 1
    assert yao_cellunit.found_facts == {}
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.set_boss_facts_from_other_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.budevent_facts
    assert yao_cellunit.boss_facts == {clean_fact.fcontext: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_set_boss_facts_from_other_facts_SetsAttr_Scenario2_budevent_facts_And_found_facts():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    sky_fact = sky_blue_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(
        clean_fact.fcontext, clean_fact.fstate, create_missing_concepts=True
    )
    yao_budevent_fact_dict = {sky_fact.fcontext: sky_fact.get_dict()}
    yao_found_fact_dict = {clean_fact.fcontext: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_budevent_facts_from_dict(yao_budevent_fact_dict)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.found_facts) == 1
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.set_boss_facts_from_other_facts()

    # THEN
    expected_boss_facts = {clean_fact.fcontext: clean_fact, sky_fact.fcontext: sky_fact}
    assert yao_cellunit.boss_facts == expected_boss_facts
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario0_found_facts_only():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(
        clean_fact.fcontext, clean_fact.fstate, create_missing_concepts=True
    )
    yao_found_fact_dict = {clean_fact.fcontext: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.found_facts) == 1
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.add_other_facts_to_boss_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.found_facts
    assert yao_cellunit.boss_facts == {clean_fact.fcontext: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario1_budevent_facts_only():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(
        clean_fact.fcontext, clean_fact.fstate, create_missing_concepts=True
    )
    yao_found_fact_dict = {clean_fact.fcontext: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_budevent_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.budevent_facts) == 1
    assert yao_cellunit.found_facts == {}
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.add_other_facts_to_boss_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.budevent_facts
    assert yao_cellunit.boss_facts == {clean_fact.fcontext: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario2_budevent_facts_And_found_facts():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    sky_fact = sky_blue_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(
        clean_fact.fcontext, clean_fact.fstate, create_missing_concepts=True
    )
    run_way = yao_bud.make_l1_way("run")
    run_fact = factunit_shop(run_way, run_way)
    run_facts = {run_fact.fcontext: run_fact}
    yao_budevent_fact_dict = {sky_fact.fcontext: sky_fact.get_dict()}
    yao_found_fact_dict = {clean_fact.fcontext: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_budevent_facts_from_dict(yao_budevent_fact_dict)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    yao_cellunit.boss_facts = run_facts
    assert len(yao_cellunit.found_facts) == 1
    assert set(yao_cellunit.boss_facts.keys()) == {run_way}

    # WHEN
    yao_cellunit.add_other_facts_to_boss_facts()

    # THEN
    expected_boss_facts = {
        run_fact.fcontext: run_fact,
        clean_fact.fcontext: clean_fact,
        sky_fact.fcontext: sky_fact,
    }
    assert set(yao_cellunit.boss_facts.keys()) == set(expected_boss_facts.keys())
    assert yao_cellunit.boss_facts == expected_boss_facts
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario3_boss_facts_AreNotOverwritten():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str, "accord23")
    run_way = yao_bud.make_l1_way("run")
    fast_way = yao_bud.make_way(run_way, "fast")
    run_fact = factunit_shop(run_way, run_way)
    fast_fact = factunit_shop(run_way, fast_way)
    run_facts = {run_fact.fcontext: run_fact}

    yao_budevent_fact_dict = {fast_fact.fcontext: fast_fact.get_dict()}
    yao_found_fact_dict = {fast_fact.fcontext: fast_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_budevent_facts_from_dict(yao_budevent_fact_dict)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    yao_cellunit.boss_facts = run_facts
    assert len(yao_cellunit.found_facts) == 1
    assert set(yao_cellunit.boss_facts.keys()) == {run_way}

    # WHEN
    yao_cellunit.add_other_facts_to_boss_facts()

    # THEN
    expected_boss_facts = {run_fact.fcontext: run_fact}
    assert set(yao_cellunit.boss_facts.keys()) == set(expected_boss_facts.keys())
    assert yao_cellunit.boss_facts == expected_boss_facts
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_filter_facts_by_reason_rcontexts_ReturnsObj_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_deal_owner = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    sue_budevent_factunits = {clean_fact.fcontext: clean_fact}
    sue_found_factunits = {dirty_fact.fcontext: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fcontext: sky_blue_fact}
    sue_cell = cellunit_shop(
        sue_deal_owner,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        None,
        sue_budevent_factunits,
        sue_found_factunits,
        sue_boss_factunits,
    )
    sue_cell._reason_rcontexts = {clean_fact.fcontext, sky_blue_fact.fcontext}
    assert sue_cell.budevent_facts == sue_budevent_factunits
    assert sue_cell.found_facts == sue_found_factunits
    assert sue_cell.boss_facts == sue_boss_factunits

    # WHEN
    sue_cell.filter_facts_by_reason_rcontexts()

    # THEN
    assert sue_cell.budevent_facts == sue_budevent_factunits
    assert sue_cell.found_facts == sue_found_factunits
    assert sue_cell.boss_facts == sue_boss_factunits

    # WHEN
    sue_cell._reason_rcontexts = {clean_fact.fcontext}
    sue_cell.filter_facts_by_reason_rcontexts()

    # THEN
    assert sue_cell.budevent_facts == sue_budevent_factunits
    assert sue_cell.found_facts == sue_found_factunits
    assert sue_cell.boss_facts == {}

    # WHEN
    sue_cell._reason_rcontexts = {}
    sue_cell.filter_facts_by_reason_rcontexts()

    # THEN
    assert sue_cell.budevent_facts == {}
    assert sue_cell.found_facts == {}
    assert sue_cell.boss_facts == {}


def test_CellUnit_set_budadjust_facts_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_deal_owner = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_cell = cellunit_shop(
        sue_deal_owner,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        budadjust=sue_bud,
    )
    assert sue_cell.budadjust.get_factunits_dict() == {}

    # WHEN
    sue_cell.set_budadjust_facts()

    # THEN
    assert sue_cell.budadjust.get_factunits_dict() == {}


def test_CellUnit_set_budadjust_facts_ReturnsObj_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_deal_owner = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    casa_clean_fact = clean_factunit()
    clean_facts = {casa_clean_fact.fcontext: casa_clean_fact}
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_concept(casa_clean_fact.fstate)
    sue_cell = cellunit_shop(
        sue_deal_owner,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        budadjust=sue_bud,
        budevent_facts=clean_facts,
    )
    assert sue_cell.budadjust.get_factunits_dict() == {}

    # WHEN
    sue_cell.set_budadjust_facts()

    # THEN
    assert sue_cell.budadjust.get_factunits_dict() != {}
    sue_bud_facts = sue_cell.budadjust.get_factunits_dict()
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    sue_bud_casa_fact_dict = sue_bud_facts.get(casa_way)
    assert sue_bud_casa_fact_dict.get("fstate") == casa_clean_fact.fstate


def test_CellUnit_set_budadjust_facts_ReturnsObj_Scenario2():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_deal_owner = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    casa_clean_fact = clean_factunit()
    casa_dirty_fact = dirty_factunit()
    clean_facts = {casa_clean_fact.fcontext: casa_clean_fact}
    dirty_facts = {casa_dirty_fact.fcontext: casa_dirty_fact}
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_concept(casa_clean_fact.fstate)
    sue_bud.add_concept(casa_dirty_fact.fstate)
    sue_cell = cellunit_shop(
        sue_deal_owner,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        budadjust=sue_bud,
        budevent_facts=clean_facts,
        found_facts=dirty_facts,
    )
    assert sue_cell.budadjust.get_factunits_dict() == {}

    # WHEN
    sue_cell.set_budadjust_facts()

    # THEN
    assert sue_cell.budadjust.get_factunits_dict() != {}
    sue_bud_facts = sue_cell.budadjust.get_factunits_dict()
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    sue_bud_casa_fact_dict = sue_bud_facts.get(casa_way)
    assert sue_bud_casa_fact_dict.get("fstate") == casa_dirty_fact.fstate


def test_CellUnit_set_budadjust_facts_ReturnsObj_Scenario3():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_deal_owner = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    casa_clean_fact = clean_factunit()
    casa_dirty_fact = dirty_factunit()
    casa_grimy_fact = grimy_factunit()
    clean_facts = {casa_clean_fact.fcontext: casa_clean_fact}
    dirty_facts = {casa_dirty_fact.fcontext: casa_dirty_fact}
    grimy_facts = {casa_grimy_fact.fcontext: casa_grimy_fact}
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_concept(casa_clean_fact.fstate)
    sue_bud.add_concept(casa_dirty_fact.fstate)
    sue_bud.add_concept(casa_grimy_fact.fstate)
    sue_cell = cellunit_shop(
        sue_deal_owner,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        budadjust=sue_bud,
        budevent_facts=clean_facts,
        found_facts=dirty_facts,
        boss_facts=grimy_facts,
    )
    assert sue_cell.budadjust.get_factunits_dict() == {}

    # WHEN
    sue_cell.set_budadjust_facts()

    # THEN
    assert sue_cell.budadjust.get_factunits_dict() != {}
    sue_bud_facts = sue_cell.budadjust.get_factunits_dict()
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    sue_bud_casa_fact_dict = sue_bud_facts.get(casa_way)
    assert sue_bud_casa_fact_dict.get("fstate") == casa_grimy_fact.fstate


def test_CellUnit_set_acct_mandate_ledger_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        budadjust=sue_bud,
        mandate=sue_mandate,
    )
    assert sue_cell.budadjust.fund_pool != sue_quota300
    assert sue_cell.budadjust.fund_pool != sue_mandate
    assert sue_cell._acct_mandate_ledger == {}

    # WHEN
    sue_cell._set_acct_mandate_ledger()

    # THEN
    assert sue_cell.budadjust.fund_pool != sue_quota300
    assert sue_cell.budadjust.fund_pool == sue_mandate
    assert sue_cell._acct_mandate_ledger == {sue_str: sue_mandate}


def test_CellUnit_set_acct_mandate_ledger_ReturnsObj_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_acctunit(sue_str, 3, 5)
    sue_bud.add_acctunit(yao_str, 7, 2)
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        budadjust=sue_bud,
        mandate=sue_mandate,
    )
    assert sue_cell.budadjust.fund_pool != sue_quota300
    assert sue_cell.budadjust.fund_pool != sue_mandate
    assert sue_cell._acct_mandate_ledger == {}

    # WHEN
    sue_cell._set_acct_mandate_ledger()

    # THEN
    assert sue_cell.budadjust.fund_pool != sue_quota300
    assert sue_cell.budadjust.fund_pool == sue_mandate
    assert sue_cell._acct_mandate_ledger != {}
    assert sue_cell._acct_mandate_ledger == {yao_str: 311, sue_str: 133}


def test_CellUnit_calc_acct_mandate_ledger_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_acctunit(sue_str, 3, 5)
    sue_bud.add_acctunit(yao_str, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_bud.add_concept(clean_fact.fstate)
    sue_bud.add_concept(dirty_fact.fstate)
    casa_way = sue_bud.make_l1_way("casa")
    mop_way = sue_bud.make_way(casa_way, "mop")
    sue_bud.add_concept(mop_way, 1, pledge=True)
    sue_bud.edit_reason(mop_way, dirty_fact.fcontext, dirty_fact.fstate)
    sue_bud.add_fact(
        dirty_fact.fcontext, dirty_fact.fstate, create_missing_concepts=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_budevent_factunits = {clean_fact.fcontext: clean_fact}
    sue_found_factunits = {dirty_fact.fcontext: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fcontext: sky_blue_fact}
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        budadjust=sue_bud,
        budevent_facts=sue_budevent_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell._reason_rcontexts = set()
    assert not sue_cell._reason_rcontexts
    assert sue_cell.boss_facts == {sky_blue_fact.fcontext: sky_blue_fact}
    assert sue_cell.budadjust.get_factunits_dict() == {}
    assert sue_cell._acct_mandate_ledger == {}

    # WHEN
    sue_cell.calc_acct_mandate_ledger()

    # THEN
    assert sue_cell._reason_rcontexts == {clean_fact.fcontext}
    assert sue_cell.boss_facts == {}
    assert sue_cell.budadjust.get_factunits_dict() != {}
    assert set(sue_cell.budadjust.get_factunits_dict().keys()) == {clean_fact.fcontext}
    # concept_dict = sue_cell.budadjust.get_concept_dict()
    # for concept_way, concept_obj in concept_dict.items():
    #     print(f"{concept_way=} {concept_obj._fund_onset=} {concept_obj._fund_cease}")
    assert sue_cell._acct_mandate_ledger != {}
    assert sue_cell._acct_mandate_ledger == {yao_str: 311, sue_str: 133}


def test_create_child_cellunits_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    bob_str = "Bob"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_acctunit(sue_str, 3, 5)
    sue_bud.add_acctunit(yao_str, 7, 2)
    sue_bud.add_acctunit(bob_str, 0, 2)
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        budadjust=sue_bud,
        mandate=sue_mandate,
    )

    # WHEN
    sue_child_cellunits = create_child_cellunits(sue_cell)

    # THEN
    assert len(sue_child_cellunits) == 2
    sue_sue_cell = sue_child_cellunits[0]
    assert sue_sue_cell.deal_owner_name == yao_str
    assert sue_sue_cell.ancestors == [sue_str, sue_str]
    assert sue_sue_cell.event_int == sue_event7
    assert sue_sue_cell.celldepth == sue_celldepth3 - 1
    assert sue_sue_cell.penny == sue_penny2
    assert sue_sue_cell.mandate == 133
    # assert not sue_sue_cell.budadjust
    assert sue_sue_cell.budevent_facts == {}
    assert sue_sue_cell.found_facts == {}
    assert sue_sue_cell.boss_facts == {}

    sue_yao_cell = sue_child_cellunits[1]
    assert sue_yao_cell.deal_owner_name == yao_str
    assert sue_yao_cell.ancestors == [sue_str, yao_str]
    assert sue_yao_cell.event_int == sue_event7
    assert sue_yao_cell.celldepth == sue_celldepth3 - 1
    assert sue_yao_cell.penny == sue_penny2
    assert sue_yao_cell.mandate == 311
    # assert sue_yao_cell.budadjust
    assert sue_yao_cell.budevent_facts == {}
    assert sue_yao_cell.found_facts == {}
    assert sue_yao_cell.boss_facts == {}


def test_create_child_cellunits_ReturnsObj_Scenario1_DealDepth0():
    # ESTABLISH
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    bob_str = "Bob"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth = 0
    sue_penny2 = 2
    sue_quota300 = 300
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_acctunit(sue_str, 3, 5)
    sue_bud.add_acctunit(yao_str, 7, 2)
    sue_bud.add_acctunit(bob_str, 0, 2)
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth,
        sue_penny2,
        sue_quota300,
        budadjust=sue_bud,
    )

    # WHEN
    sue_child_cellunits = create_child_cellunits(sue_cell)

    # THEN
    assert sue_child_cellunits == []


def test_create_child_cellunits_ReturnsObj_Scenario2_boss_facts():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    yao_celldepth = 3
    yao_quota = 320
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_acctunit(sue_str, 3, 5)
    yao_bud.add_acctunit(yao_str, 7, 2)
    yao_bud.add_acctunit(bob_str, 0, 2)
    casa_way = yao_bud.make_l1_way("casa")
    mop_way = yao_bud.make_way(casa_way, "mop")
    clean_fact = clean_factunit()
    yao_bud.add_concept(casa_way, 1)
    yao_bud.add_concept(mop_way, 1, pledge=True)
    yao_bud.add_concept(clean_fact.fstate)
    yao_bud.add_concept(dirty_fact.fstate)
    yao_bud.edit_reason(mop_way, dirty_fact.fcontext, dirty_fact.fstate)
    yao_cell = cellunit_shop(
        yao_str, celldepth=yao_celldepth, quota=yao_quota, budadjust=yao_bud
    )
    yao_cell.budevent_facts = {dirty_fact.fcontext: dirty_fact}
    # sue_cell._acct_mandate_ledger = {yao_str: 210, sue_str: 90, bob_str: 0}

    # WHEN
    sue_child_cellunits = create_child_cellunits(yao_cell)

    # THEN
    assert len(sue_child_cellunits) == 2
    sue_yao_cell = sue_child_cellunits[1]
    assert sue_yao_cell.budevent_facts == {}
    assert sue_yao_cell.found_facts == {}
    assert sue_yao_cell.boss_facts == {dirty_fact.fcontext: dirty_fact}

    sue_sue_cell = sue_child_cellunits[0]
    assert sue_sue_cell.budevent_facts == {}
    assert sue_sue_cell.found_facts == {}
    assert sue_sue_cell.boss_facts == {dirty_fact.fcontext: dirty_fact}


def test_create_child_cellunits_ReturnsObj_Scenario3_StateOfCellAdjustIsReset():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_mandate = 444
    sue_bud = budunit_shop(sue_str, "accord23")
    sue_bud.add_acctunit(sue_str, 3, 5)
    sue_bud.add_acctunit(yao_str, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_bud.add_concept(clean_fact.fstate)
    sue_bud.add_concept(dirty_fact.fstate)
    casa_way = sue_bud.make_l1_way("casa")
    mop_way = sue_bud.make_way(casa_way, "mop")
    sue_bud.add_concept(mop_way, 1, pledge=True)
    sue_bud.edit_reason(mop_way, dirty_fact.fcontext, dirty_fact.fstate)
    sue_bud.add_fact(
        dirty_fact.fcontext, dirty_fact.fstate, create_missing_concepts=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_budevent_factunits = {clean_fact.fcontext: clean_fact}
    sue_found_factunits = {dirty_fact.fcontext: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fcontext: sky_blue_fact}
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        budadjust=sue_bud,
        budevent_facts=sue_budevent_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell._reason_rcontexts = set()
    assert not sue_cell._reason_rcontexts
    assert sue_cell.boss_facts == {sky_blue_fact.fcontext: sky_blue_fact}
    assert sue_cell.budadjust.get_factunits_dict() == {}
    assert sue_cell._acct_mandate_ledger == {}

    # WHEN
    sue_child_cellunits = create_child_cellunits(sue_cell)

    # # WHEN
    # sue_cell.calc_acct_mandate_ledger()

    # # THEN
    assert sue_cell._reason_rcontexts == {dirty_fact.fcontext}
    assert sue_cell.boss_facts == {}
    assert sue_cell.budadjust.get_factunits_dict() != {}
    assert set(sue_cell.budadjust.get_factunits_dict().keys()) == {dirty_fact.fcontext}
    # concept_dict = sue_cell.budadjust.get_concept_dict()
    # for concept_way, concept_obj in concept_dict.items():
    #     print(f"{concept_way=} {concept_obj._fund_onset=} {concept_obj._fund_cease}")
    assert sue_cell._acct_mandate_ledger != {}
    assert sue_cell._acct_mandate_ledger == {yao_str: 311, sue_str: 133}

    # THEN
    assert len(sue_child_cellunits) == 2
    sue_yao_cell = sue_child_cellunits[1]
    assert sue_yao_cell.budevent_facts == {}
    assert sue_yao_cell.found_facts == {}
    assert sue_yao_cell.boss_facts == {dirty_fact.fcontext: dirty_fact}
    assert sue_yao_cell.mandate == 311

    sue_sue_cell = sue_child_cellunits[0]
    assert sue_sue_cell.budevent_facts == {}
    assert sue_sue_cell.found_facts == {}
    assert sue_sue_cell.boss_facts == {dirty_fact.fcontext: dirty_fact}
    assert sue_sue_cell.mandate == 133
