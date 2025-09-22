from copy import deepcopy as copy_deepcopy
from src.ch01_rope_logic.rope import create_rope
from src.ch05_reason_logic.reason import factunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch11_bud_logic._ref.ch11_terms import (
    ancestors_str,
    beliefadjust_str,
    beliefevent_facts_str,
    boss_facts_str,
    bud_belief_name_str,
    celldepth_str,
    found_facts_str,
    mandate_str,
)
from src.ch11_bud_logic.cell import (
    CELLNODE_QUOTA_DEFAULT,
    CellUnit,
    cellunit_shop,
    create_child_cellunits,
)
from src.ch11_bud_logic.test._util.example_factunits import (
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_casa_grimy_factunit as grimy_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
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
    assert not x_cellunit.bud_belief_name
    assert not x_cellunit.penny
    assert not x_cellunit.quota
    assert not x_cellunit.mandate
    assert not x_cellunit.beliefadjust
    assert not x_cellunit.reason_contexts
    assert not x_cellunit._voice_mandate_ledger
    assert not x_cellunit.beliefevent_facts
    assert not x_cellunit.found_facts
    assert not x_cellunit.boss_facts


def test_cellunit_shop_ReturnsObj_Scenario0_WithoutParameters():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    x_cellunit = cellunit_shop(bob_str)
    # THEN
    assert x_cellunit.bud_belief_name == bob_str
    assert x_cellunit.ancestors == []
    assert not x_cellunit.event_int
    assert x_cellunit.celldepth == 0
    assert x_cellunit.penny == 1
    assert x_cellunit.quota == CELLNODE_QUOTA_DEFAULT
    assert x_cellunit.mandate == CELLNODE_QUOTA_DEFAULT
    assert x_cellunit.beliefadjust.to_dict() == beliefunit_shop(bob_str).to_dict()
    assert x_cellunit.beliefevent_facts == {}
    assert x_cellunit.reason_contexts == set()
    assert x_cellunit._voice_mandate_ledger == {}
    assert x_cellunit.found_facts == {}
    assert x_cellunit.boss_facts == {}


def test_cellunit_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_event7 = 7
    bob_sue_bud_belief = yao_str
    bob_sue_celldepth3 = 3
    bob_sue_penny2 = 2
    bob_sue_quota300 = 300
    bob_sue_mandate = 444
    bob_sue_belief = beliefunit_shop(sue_str)
    bob_sue_belief.add_voiceunit(bob_str, 7, 13)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_beliefevent_factunits = {clean_fact.fact_context: clean_fact}
    bob_sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}

    # WHEN
    x_cellunit = cellunit_shop(
        bob_sue_bud_belief,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        bob_sue_belief,
        bob_sue_beliefevent_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
        bob_sue_mandate,
    )

    # THEN
    assert x_cellunit.ancestors == bob_sue_ancestors
    assert x_cellunit.event_int == bob_sue_event7
    assert x_cellunit.celldepth == bob_sue_celldepth3
    assert x_cellunit.bud_belief_name == bob_sue_bud_belief
    assert x_cellunit.penny == bob_sue_penny2
    assert x_cellunit.quota == bob_sue_quota300
    assert x_cellunit.mandate == bob_sue_mandate
    assert x_cellunit.beliefadjust == bob_sue_belief
    assert x_cellunit.reason_contexts == set()
    assert x_cellunit.beliefevent_facts == bob_sue_beliefevent_factunits
    assert x_cellunit.found_facts == bob_sue_found_factunits
    assert x_cellunit.boss_facts == bob_sue_boss_factunits


def test_cellunit_shop_ReturnsObj_Scenario2_Withreason_contexts():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str, "amy23")
    casa_rope = sue_belief.make_l1_rope("casa")
    mop_rope = sue_belief.make_rope(casa_rope, "mop")
    clean_fact = clean_factunit()
    sue_belief.add_plan(clean_factunit().fact_state)
    sue_belief.add_plan(mop_rope, task=True)
    sue_belief.edit_reason(mop_rope, clean_fact.fact_context, clean_fact.fact_state)

    # WHEN
    x_cellunit = cellunit_shop(sue_str, beliefadjust=sue_belief)

    # THEN
    assert x_cellunit.bud_belief_name == sue_str
    assert x_cellunit.beliefadjust == sue_belief
    assert x_cellunit.reason_contexts == sue_belief.get_reason_contexts()
    assert len(x_cellunit.reason_contexts) == 1


def test_cellunit_shop_ReturnsObj_Scenario3_clear_facts():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str, "amy23")
    casa_rope = sue_belief.make_l1_rope("casa")
    mop_rope = sue_belief.make_rope(casa_rope, "mop")
    clean_fact = clean_factunit()
    sue_belief.add_plan(clean_factunit().fact_state)
    sue_belief.add_plan(mop_rope, task=True)
    sue_belief.edit_reason(mop_rope, clean_fact.fact_context, clean_fact.fact_state)
    sue_belief.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    assert len(sue_belief.get_factunits_dict()) == 1

    # WHEN
    x_cellunit = cellunit_shop(sue_str, beliefadjust=sue_belief)

    # THEN
    assert len(x_cellunit.beliefadjust.get_factunits_dict()) == 0
    assert x_cellunit.beliefadjust != sue_belief


def test_Cellunit_get_cell_belief_name_ReturnsObj_Scenario0_NoAncestors():
    # ESTABLISH
    yao_str = "Yao"
    root_cellunit = cellunit_shop(yao_str, [])

    # WHEN / THEN
    assert root_cellunit.get_cell_belief_name() == yao_str


def test_Cellunit_get_cell_belief_name_ReturnsObj_Scenario1_WithAncestors():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_bud_belief = yao_str
    bob_sue_cellunit = cellunit_shop(bob_sue_bud_belief, bob_sue_ancestors)

    # WHEN
    bob_sue_cell_belief_name = bob_sue_cellunit.get_cell_belief_name()

    # THEN
    assert bob_sue_cell_belief_name == sue_str


def test_CellUnit_eval_beliefevent_SetsAttr_Scenario0_ParameterIsNone():
    # ESTABLISH
    yao_str = "Yao"
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.beliefadjust = "testing_place_holder"
    yao_cellunit.beliefevent_facts = "testing_place_holder"
    yao_cellunit.reason_contexts = "testing_place_holder"
    assert yao_cellunit.beliefadjust
    assert yao_cellunit.beliefevent_facts != {}
    assert yao_cellunit.reason_contexts != set()

    # WHEN
    yao_cellunit.eval_beliefevent(None)

    # THEN
    assert yao_cellunit.beliefadjust is None
    assert yao_cellunit.beliefevent_facts == {}
    assert yao_cellunit.reason_contexts == set()


def test_CellUnit_eval_beliefevent_SetsAttr_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(yao_str, "amy23")
    casa_rope = yao_belief.make_l1_rope("casa")
    mop_rope = yao_belief.make_rope(casa_rope, "mop")
    clean_fact = clean_factunit()
    yao_belief.add_plan(clean_fact.fact_state)
    yao_belief.add_plan(mop_rope, task=True)
    yao_belief.edit_reason(mop_rope, clean_fact.fact_context, clean_fact.fact_state)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_cellunit = cellunit_shop(yao_str)
    assert yao_cellunit.beliefevent_facts == {}
    assert yao_cellunit.reason_contexts == set()

    # WHEN
    yao_cellunit.eval_beliefevent(yao_belief)

    # THEN
    expected_factunits = {clean_fact.fact_context: clean_fact}
    assert yao_cellunit.beliefevent_facts == expected_factunits
    assert yao_cellunit.reason_contexts == yao_belief.get_reason_contexts()
    assert len(yao_cellunit.reason_contexts) == 1
    expected_adjust_belief = copy_deepcopy(yao_belief)
    expected_adjust_belief.del_fact(clean_fact.fact_context)
    expected_adjust_belief.cashout()
    expected_planroot = expected_adjust_belief.planroot
    generated_planroot = yao_cellunit.beliefadjust.planroot
    assert yao_cellunit.beliefadjust.to_dict() != yao_belief.to_dict()
    assert generated_planroot.to_dict() == expected_planroot.to_dict()
    assert yao_cellunit.beliefadjust.to_dict() == expected_adjust_belief.to_dict()


def test_CellUnit_get_beliefevents_credit_ledger_ReturnsObj_Scenario0_NoBelief():
    # ESTABLISH
    yao_str = "Yao"
    yao_cellunit = cellunit_shop(yao_str)

    # WHEN
    gen_credit_ledger = yao_cellunit.get_beliefevents_credit_ledger()

    # THEN
    assert gen_credit_ledger == {}


def test_get_beliefevents_credit_ledger_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_voiceunit(sue_str, 3, 5)
    sue_belief.add_voiceunit(yao_str, 7, 2)
    sue_cell = cellunit_shop(yao_str, beliefadjust=sue_belief)

    # WHEN
    gen_credit_ledger = sue_cell.get_beliefevents_credit_ledger()

    # THEN
    expected_credit_ledger = {sue_str: 3, yao_str: 7}
    assert gen_credit_ledger == expected_credit_ledger


def test_CellUnit_get_beliefevents_quota_ledger_ReturnsObj_Scenario0_NoBelief():
    # ESTABLISH
    yao_str = "Yao"
    yao_cellunit = cellunit_shop(yao_str)

    # WHEN
    gen_credit_ledger = yao_cellunit.get_beliefevents_quota_ledger()

    # THEN
    assert gen_credit_ledger == {}


def test_get_beliefevents_quota_ledger_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_voiceunit(sue_str, 3, 5)
    sue_belief.add_voiceunit(yao_str, 7, 2)
    sue_cell = cellunit_shop(yao_str, quota=55, beliefadjust=sue_belief)

    # WHEN
    gen_credit_ledger = sue_cell.get_beliefevents_quota_ledger()

    # THEN
    expected_credit_ledger = {sue_str: 16, yao_str: 39}
    assert gen_credit_ledger == expected_credit_ledger


def test_CellUnit_set_found_facts_from_dict_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(yao_str, "amy23")
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    assert yao_cellunit.found_facts == {}

    # WHEN
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)

    # THEN
    expected_factunits = {clean_fact.fact_context: clean_fact}
    assert yao_cellunit.found_facts == expected_factunits


def test_CellUnit_set_beliefevent_facts_from_dict_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(yao_str, "amy23")
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    assert yao_cellunit.beliefevent_facts == {}

    # WHEN
    yao_cellunit.set_beliefevent_facts_from_dict(yao_found_fact_dict)

    # THEN
    expected_factunits = {clean_fact.fact_context: clean_fact}
    assert yao_cellunit.beliefevent_facts == expected_factunits


def test_CellUnit_set_boss_facts_from_other_facts_SetsAttr_Scenario0_found_facts_only():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(yao_str, "amy23")
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    yao_cellunit.boss_facts = "testing_str"
    assert len(yao_cellunit.found_facts) == 1
    assert yao_cellunit.boss_facts == "testing_str"

    # WHEN
    yao_cellunit.set_boss_facts_from_other_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.found_facts
    assert yao_cellunit.boss_facts == {clean_fact.fact_context: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_set_boss_facts_from_other_facts_SetsAttr_Scenario1_beliefevent_facts_only():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(yao_str, "amy23")
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_beliefevent_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.beliefevent_facts) == 1
    assert yao_cellunit.found_facts == {}
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.set_boss_facts_from_other_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.beliefevent_facts
    assert yao_cellunit.boss_facts == {clean_fact.fact_context: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_set_boss_facts_from_other_facts_SetsAttr_Scenario2_beliefevent_facts_And_found_facts():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    sky_fact = sky_blue_factunit()
    yao_belief = beliefunit_shop(yao_str, "amy23")
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_beliefevent_fact_dict = {sky_fact.fact_context: sky_fact.to_dict()}
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_beliefevent_facts_from_dict(yao_beliefevent_fact_dict)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.found_facts) == 1
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.set_boss_facts_from_other_facts()

    # THEN
    expected_boss_facts = {
        clean_fact.fact_context: clean_fact,
        sky_fact.fact_context: sky_fact,
    }
    assert yao_cellunit.boss_facts == expected_boss_facts
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario0_found_facts_only():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(yao_str, "amy23")
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.found_facts) == 1
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.add_other_facts_to_boss_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.found_facts
    assert yao_cellunit.boss_facts == {clean_fact.fact_context: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario1_beliefevent_facts_only():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(yao_str, "amy23")
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_beliefevent_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.beliefevent_facts) == 1
    assert yao_cellunit.found_facts == {}
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.add_other_facts_to_boss_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.beliefevent_facts
    assert yao_cellunit.boss_facts == {clean_fact.fact_context: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario2_beliefevent_facts_And_found_facts():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    sky_fact = sky_blue_factunit()
    yao_belief = beliefunit_shop(yao_str, "amy23")
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    run_rope = yao_belief.make_l1_rope("run")
    run_fact = factunit_shop(run_rope, run_rope)
    run_facts = {run_fact.fact_context: run_fact}
    yao_beliefevent_fact_dict = {sky_fact.fact_context: sky_fact.to_dict()}
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_beliefevent_facts_from_dict(yao_beliefevent_fact_dict)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    yao_cellunit.boss_facts = run_facts
    assert len(yao_cellunit.found_facts) == 1
    assert set(yao_cellunit.boss_facts.keys()) == {run_rope}

    # WHEN
    yao_cellunit.add_other_facts_to_boss_facts()

    # THEN
    expected_boss_facts = {
        run_fact.fact_context: run_fact,
        clean_fact.fact_context: clean_fact,
        sky_fact.fact_context: sky_fact,
    }
    assert set(yao_cellunit.boss_facts.keys()) == set(expected_boss_facts.keys())
    assert yao_cellunit.boss_facts == expected_boss_facts
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario3_boss_facts_AreNotOverwritten():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str, "amy23")
    run_rope = yao_belief.make_l1_rope("run")
    fast_rope = yao_belief.make_rope(run_rope, "fast")
    run_fact = factunit_shop(run_rope, run_rope)
    fast_fact = factunit_shop(run_rope, fast_rope)
    run_facts = {run_fact.fact_context: run_fact}

    yao_beliefevent_fact_dict = {fast_fact.fact_context: fast_fact.to_dict()}
    yao_found_fact_dict = {fast_fact.fact_context: fast_fact.to_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_beliefevent_facts_from_dict(yao_beliefevent_fact_dict)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    yao_cellunit.boss_facts = run_facts
    assert len(yao_cellunit.found_facts) == 1
    assert set(yao_cellunit.boss_facts.keys()) == {run_rope}

    # WHEN
    yao_cellunit.add_other_facts_to_boss_facts()

    # THEN
    expected_boss_facts = {run_fact.fact_context: run_fact}
    assert set(yao_cellunit.boss_facts.keys()) == set(expected_boss_facts.keys())
    assert yao_cellunit.boss_facts == expected_boss_facts
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_filter_facts_by_reason_contexts_ReturnsObj_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_bud_belief = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    sue_beliefevent_factunits = {clean_fact.fact_context: clean_fact}
    sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        None,
        sue_beliefevent_factunits,
        sue_found_factunits,
        sue_boss_factunits,
    )
    sue_cell.reason_contexts = {clean_fact.fact_context, sky_blue_fact.fact_context}
    assert sue_cell.beliefevent_facts == sue_beliefevent_factunits
    assert sue_cell.found_facts == sue_found_factunits
    assert sue_cell.boss_facts == sue_boss_factunits

    # WHEN
    sue_cell.filter_facts_by_reason_contexts()

    # THEN
    assert sue_cell.beliefevent_facts == sue_beliefevent_factunits
    assert sue_cell.found_facts == sue_found_factunits
    assert sue_cell.boss_facts == sue_boss_factunits

    # WHEN
    sue_cell.reason_contexts = {clean_fact.fact_context}
    sue_cell.filter_facts_by_reason_contexts()

    # THEN
    assert sue_cell.beliefevent_facts == sue_beliefevent_factunits
    assert sue_cell.found_facts == sue_found_factunits
    assert sue_cell.boss_facts == {}

    # WHEN
    sue_cell.reason_contexts = {}
    sue_cell.filter_facts_by_reason_contexts()

    # THEN
    assert sue_cell.beliefevent_facts == {}
    assert sue_cell.found_facts == {}
    assert sue_cell.boss_facts == {}


def test_CellUnit_set_beliefadjust_facts_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_bud_belief = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        beliefadjust=sue_belief,
    )
    assert sue_cell.beliefadjust.get_factunits_dict() == {}

    # WHEN
    sue_cell.set_beliefadjust_facts()

    # THEN
    assert sue_cell.beliefadjust.get_factunits_dict() == {}


def test_CellUnit_set_beliefadjust_facts_ReturnsObj_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_bud_belief = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    casa_clean_fact = clean_factunit()
    clean_facts = {casa_clean_fact.fact_context: casa_clean_fact}
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_plan(casa_clean_fact.fact_state)
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        beliefadjust=sue_belief,
        beliefevent_facts=clean_facts,
    )
    assert sue_cell.beliefadjust.get_factunits_dict() == {}

    # WHEN
    sue_cell.set_beliefadjust_facts()

    # THEN
    assert sue_cell.beliefadjust.get_factunits_dict() != {}
    sue_belief_facts = sue_cell.beliefadjust.get_factunits_dict()
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    sue_belief_casa_fact_dict = sue_belief_facts.get(casa_rope)
    assert sue_belief_casa_fact_dict.get("fact_state") == casa_clean_fact.fact_state


def test_CellUnit_set_beliefadjust_facts_ReturnsObj_Scenario2():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_bud_belief = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    casa_clean_fact = clean_factunit()
    casa_dirty_fact = dirty_factunit()
    clean_facts = {casa_clean_fact.fact_context: casa_clean_fact}
    dirty_facts = {casa_dirty_fact.fact_context: casa_dirty_fact}
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_plan(casa_clean_fact.fact_state)
    sue_belief.add_plan(casa_dirty_fact.fact_state)
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        beliefadjust=sue_belief,
        beliefevent_facts=clean_facts,
        found_facts=dirty_facts,
    )
    assert sue_cell.beliefadjust.get_factunits_dict() == {}

    # WHEN
    sue_cell.set_beliefadjust_facts()

    # THEN
    assert sue_cell.beliefadjust.get_factunits_dict() != {}
    sue_belief_facts = sue_cell.beliefadjust.get_factunits_dict()
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    sue_belief_casa_fact_dict = sue_belief_facts.get(casa_rope)
    assert sue_belief_casa_fact_dict.get("fact_state") == casa_dirty_fact.fact_state


def test_CellUnit_set_beliefadjust_facts_ReturnsObj_Scenario3():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_bud_belief = yao_str
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    casa_clean_fact = clean_factunit()
    casa_dirty_fact = dirty_factunit()
    casa_grimy_fact = grimy_factunit()
    clean_facts = {casa_clean_fact.fact_context: casa_clean_fact}
    dirty_facts = {casa_dirty_fact.fact_context: casa_dirty_fact}
    grimy_facts = {casa_grimy_fact.fact_context: casa_grimy_fact}
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_plan(casa_clean_fact.fact_state)
    sue_belief.add_plan(casa_dirty_fact.fact_state)
    sue_belief.add_plan(casa_grimy_fact.fact_state)
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        beliefadjust=sue_belief,
        beliefevent_facts=clean_facts,
        found_facts=dirty_facts,
        boss_facts=grimy_facts,
    )
    assert sue_cell.beliefadjust.get_factunits_dict() == {}

    # WHEN
    sue_cell.set_beliefadjust_facts()

    # THEN
    assert sue_cell.beliefadjust.get_factunits_dict() != {}
    sue_belief_facts = sue_cell.beliefadjust.get_factunits_dict()
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    sue_belief_casa_fact_dict = sue_belief_facts.get(casa_rope)
    assert sue_belief_casa_fact_dict.get("fact_state") == casa_grimy_fact.fact_state


def test_CellUnit_set_voice_mandate_ledger_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        beliefadjust=sue_belief,
        mandate=sue_mandate,
    )
    assert sue_cell.beliefadjust.fund_pool != sue_quota300
    assert sue_cell.beliefadjust.fund_pool != sue_mandate
    assert sue_cell._voice_mandate_ledger == {}

    # WHEN
    sue_cell._set_voice_mandate_ledger()

    # THEN
    assert sue_cell.beliefadjust.fund_pool != sue_quota300
    assert sue_cell.beliefadjust.fund_pool == sue_mandate
    assert sue_cell._voice_mandate_ledger == {sue_str: sue_mandate}


def test_CellUnit_set_voice_mandate_ledger_ReturnsObj_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_voiceunit(sue_str, 3, 5)
    sue_belief.add_voiceunit(yao_str, 7, 2)
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        beliefadjust=sue_belief,
        mandate=sue_mandate,
    )
    assert sue_cell.beliefadjust.fund_pool != sue_quota300
    assert sue_cell.beliefadjust.fund_pool != sue_mandate
    assert sue_cell._voice_mandate_ledger == {}

    # WHEN
    sue_cell._set_voice_mandate_ledger()

    # THEN
    assert sue_cell.beliefadjust.fund_pool != sue_quota300
    assert sue_cell.beliefadjust.fund_pool == sue_mandate
    assert sue_cell._voice_mandate_ledger != {}
    assert sue_cell._voice_mandate_ledger == {yao_str: 311, sue_str: 133}


def test_CellUnit_calc_voice_mandate_ledger_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_voiceunit(sue_str, 3, 5)
    sue_belief.add_voiceunit(yao_str, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_belief.add_plan(clean_fact.fact_state)
    sue_belief.add_plan(dirty_fact.fact_state)
    casa_rope = sue_belief.make_l1_rope("casa")
    mop_rope = sue_belief.make_rope(casa_rope, "mop")
    sue_belief.add_plan(mop_rope, 1, task=True)
    sue_belief.edit_reason(mop_rope, dirty_fact.fact_context, dirty_fact.fact_state)
    sue_belief.add_fact(
        dirty_fact.fact_context, dirty_fact.fact_state, create_missing_plans=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_beliefevent_factunits = {clean_fact.fact_context: clean_fact}
    sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        beliefadjust=sue_belief,
        beliefevent_facts=sue_beliefevent_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell.reason_contexts = set()
    assert not sue_cell.reason_contexts
    assert sue_cell.boss_facts == {sky_blue_fact.fact_context: sky_blue_fact}
    assert sue_cell.beliefadjust.get_factunits_dict() == {}
    assert sue_cell._voice_mandate_ledger == {}

    # WHEN
    sue_cell.calc_voice_mandate_ledger()

    # THEN
    assert sue_cell.reason_contexts == {clean_fact.fact_context}
    assert sue_cell.boss_facts == {}
    assert sue_cell.beliefadjust.get_factunits_dict() != {}
    assert set(sue_cell.beliefadjust.get_factunits_dict().keys()) == {
        clean_fact.fact_context
    }
    # plan_dict = sue_cell.beliefadjust.get_plan_dict()
    # for plan_rope, plan_obj in plan_dict.items():
    #     print(f"{plan_rope=} {plan_obj.fund_onset=} {plan_obj.fund_cease}")
    assert sue_cell._voice_mandate_ledger != {}
    assert sue_cell._voice_mandate_ledger == {yao_str: 311, sue_str: 133}


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
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_voiceunit(sue_str, 3, 5)
    sue_belief.add_voiceunit(yao_str, 7, 2)
    sue_belief.add_voiceunit(bob_str, 0, 2)
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        sue_quota300,
        beliefadjust=sue_belief,
        mandate=sue_mandate,
    )

    # WHEN
    sue_child_cellunits = create_child_cellunits(sue_cell)

    # THEN
    assert len(sue_child_cellunits) == 2
    sue_sue_cell = sue_child_cellunits[0]
    assert sue_sue_cell.bud_belief_name == yao_str
    assert sue_sue_cell.ancestors == [sue_str, sue_str]
    assert sue_sue_cell.event_int == sue_event7
    assert sue_sue_cell.celldepth == sue_celldepth3 - 1
    assert sue_sue_cell.penny == sue_penny2
    assert sue_sue_cell.mandate == 133
    # assert not sue_sue_cell.beliefadjust
    assert sue_sue_cell.beliefevent_facts == {}
    assert sue_sue_cell.found_facts == {}
    assert sue_sue_cell.boss_facts == {}

    sue_yao_cell = sue_child_cellunits[1]
    assert sue_yao_cell.bud_belief_name == yao_str
    assert sue_yao_cell.ancestors == [sue_str, yao_str]
    assert sue_yao_cell.event_int == sue_event7
    assert sue_yao_cell.celldepth == sue_celldepth3 - 1
    assert sue_yao_cell.penny == sue_penny2
    assert sue_yao_cell.mandate == 311
    # assert sue_yao_cell.beliefadjust
    assert sue_yao_cell.beliefevent_facts == {}
    assert sue_yao_cell.found_facts == {}
    assert sue_yao_cell.boss_facts == {}


def test_create_child_cellunits_ReturnsObj_Scenario1_BudDepth0():
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
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_voiceunit(sue_str, 3, 5)
    sue_belief.add_voiceunit(yao_str, 7, 2)
    sue_belief.add_voiceunit(bob_str, 0, 2)
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth,
        sue_penny2,
        sue_quota300,
        beliefadjust=sue_belief,
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
    yao_belief = beliefunit_shop(yao_str, "amy23")
    yao_belief.add_voiceunit(sue_str, 3, 5)
    yao_belief.add_voiceunit(yao_str, 7, 2)
    yao_belief.add_voiceunit(bob_str, 0, 2)
    casa_rope = yao_belief.make_l1_rope("casa")
    mop_rope = yao_belief.make_rope(casa_rope, "mop")
    clean_fact = clean_factunit()
    yao_belief.add_plan(casa_rope, 1)
    yao_belief.add_plan(mop_rope, 1, task=True)
    yao_belief.add_plan(clean_fact.fact_state)
    yao_belief.add_plan(dirty_fact.fact_state)
    yao_belief.edit_reason(mop_rope, dirty_fact.fact_context, dirty_fact.fact_state)
    yao_cell = cellunit_shop(
        yao_str, celldepth=yao_celldepth, quota=yao_quota, beliefadjust=yao_belief
    )
    yao_cell.beliefevent_facts = {dirty_fact.fact_context: dirty_fact}
    # sue_cell._voice_mandate_ledger = {yao_str: 210, sue_str: 90, bob_str: 0}

    # WHEN
    sue_child_cellunits = create_child_cellunits(yao_cell)

    # THEN
    assert len(sue_child_cellunits) == 2
    sue_yao_cell = sue_child_cellunits[1]
    assert sue_yao_cell.beliefevent_facts == {}
    assert sue_yao_cell.found_facts == {}
    assert sue_yao_cell.boss_facts == {dirty_fact.fact_context: dirty_fact}

    sue_sue_cell = sue_child_cellunits[0]
    assert sue_sue_cell.beliefevent_facts == {}
    assert sue_sue_cell.found_facts == {}
    assert sue_sue_cell.boss_facts == {dirty_fact.fact_context: dirty_fact}


def test_create_child_cellunits_ReturnsObj_Scenario3_StateOfCellAdjustIsReset():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_mandate = 444
    sue_belief = beliefunit_shop(sue_str, "amy23")
    sue_belief.add_voiceunit(sue_str, 3, 5)
    sue_belief.add_voiceunit(yao_str, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_belief.add_plan(clean_fact.fact_state)
    sue_belief.add_plan(dirty_fact.fact_state)
    casa_rope = sue_belief.make_l1_rope("casa")
    mop_rope = sue_belief.make_rope(casa_rope, "mop")
    sue_belief.add_plan(mop_rope, 1, task=True)
    sue_belief.edit_reason(mop_rope, dirty_fact.fact_context, dirty_fact.fact_state)
    sue_belief.add_fact(
        dirty_fact.fact_context, dirty_fact.fact_state, create_missing_plans=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_beliefevent_factunits = {clean_fact.fact_context: clean_fact}
    sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    sue_cell = cellunit_shop(
        yao_str,
        sue_ancestors,
        sue_event7,
        sue_celldepth3,
        sue_penny2,
        beliefadjust=sue_belief,
        beliefevent_facts=sue_beliefevent_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell.reason_contexts = set()
    assert not sue_cell.reason_contexts
    assert sue_cell.boss_facts == {sky_blue_fact.fact_context: sky_blue_fact}
    assert sue_cell.beliefadjust.get_factunits_dict() == {}
    assert sue_cell._voice_mandate_ledger == {}

    # WHEN
    sue_child_cellunits = create_child_cellunits(sue_cell)

    # # WHEN
    # sue_cell.calc_voice_mandate_ledger()

    # # THEN
    assert sue_cell.reason_contexts == {dirty_fact.fact_context}
    assert sue_cell.boss_facts == {}
    assert sue_cell.beliefadjust.get_factunits_dict() != {}
    assert set(sue_cell.beliefadjust.get_factunits_dict().keys()) == {
        dirty_fact.fact_context
    }
    # plan_dict = sue_cell.beliefadjust.get_plan_dict()
    # for plan_rope, plan_obj in plan_dict.items():
    #     print(f"{plan_rope=} {plan_obj.fund_onset=} {plan_obj.fund_cease}")
    assert sue_cell._voice_mandate_ledger != {}
    assert sue_cell._voice_mandate_ledger == {yao_str: 311, sue_str: 133}

    # THEN
    assert len(sue_child_cellunits) == 2
    sue_yao_cell = sue_child_cellunits[1]
    assert sue_yao_cell.beliefevent_facts == {}
    assert sue_yao_cell.found_facts == {}
    assert sue_yao_cell.boss_facts == {dirty_fact.fact_context: dirty_fact}
    assert sue_yao_cell.mandate == 311

    sue_sue_cell = sue_child_cellunits[0]
    assert sue_sue_cell.beliefevent_facts == {}
    assert sue_sue_cell.found_facts == {}
    assert sue_sue_cell.boss_facts == {dirty_fact.fact_context: dirty_fact}
    assert sue_sue_cell.mandate == 133
