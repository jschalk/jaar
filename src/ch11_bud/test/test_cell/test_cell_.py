from copy import deepcopy as copy_deepcopy
from src.ch03_rope.rope import create_rope
from src.ch05_reason.reason import factunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch11_bud.cell import (
    CELLNODE_QUOTA_DEFAULT,
    CellUnit,
    cellunit_shop,
    create_child_cellunits,
)
from src.ch11_bud.test._util.ch11_examples import (
    Ch11ExampleStrs as wx,
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_casa_grimy_factunit as grimy_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
)
from src.ref.keywords import Ch11Keywords as kw


def test_CELLNODE_QUOTA_DEFAULT_value():
    # ESTABLISH / WHEN / THEN
    assert CELLNODE_QUOTA_DEFAULT == 1000


def test_CellUnit_Exists():
    # ESTABLISH / WHEN
    x_cellunit = CellUnit()
    # THEN
    assert not x_cellunit.ancestors
    assert not x_cellunit.spark_num
    assert not x_cellunit.celldepth
    assert not x_cellunit.bud_belief_name
    assert not x_cellunit.money_grain
    assert not x_cellunit.quota
    assert not x_cellunit.mandate
    assert not x_cellunit.beliefadjust
    assert not x_cellunit.reason_contexts
    assert not x_cellunit._voice_mandate_ledger
    assert not x_cellunit.beliefspark_facts
    assert not x_cellunit.found_facts
    assert not x_cellunit.boss_facts


def test_cellunit_shop_ReturnsObj_Scenario0_WithoutParameters():
    # ESTABLISH / WHEN
    x_cellunit = cellunit_shop(wx.bob)
    # THEN
    assert x_cellunit.bud_belief_name == wx.bob
    assert x_cellunit.ancestors == []
    assert not x_cellunit.spark_num
    assert x_cellunit.celldepth == 0
    assert x_cellunit.money_grain == 1
    assert x_cellunit.quota == CELLNODE_QUOTA_DEFAULT
    assert x_cellunit.mandate == CELLNODE_QUOTA_DEFAULT
    assert x_cellunit.beliefadjust.to_dict() == beliefunit_shop(wx.bob).to_dict()
    assert x_cellunit.beliefspark_facts == {}
    assert x_cellunit.reason_contexts == set()
    assert x_cellunit._voice_mandate_ledger == {}
    assert x_cellunit.found_facts == {}
    assert x_cellunit.boss_facts == {}


def test_cellunit_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    bob_sue_ancestors = [wx.bob, wx.sue]
    bob_sue_spark7 = 7
    bob_sue_bud_belief = wx.yao
    bob_sue_celldepth3 = 3
    bob_sue_money_grain2 = 2
    bob_sue_quota300 = 300
    bob_sue_mandate = 444
    bob_sue_belief = beliefunit_shop(wx.sue)
    bob_sue_belief.add_voiceunit(wx.bob, 7, 13)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_beliefspark_factunits = {clean_fact.fact_context: clean_fact}
    bob_sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}

    # WHEN
    x_cellunit = cellunit_shop(
        bob_sue_bud_belief,
        bob_sue_ancestors,
        bob_sue_spark7,
        bob_sue_celldepth3,
        bob_sue_money_grain2,
        bob_sue_quota300,
        bob_sue_belief,
        bob_sue_beliefspark_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
        bob_sue_mandate,
    )

    # THEN
    assert x_cellunit.ancestors == bob_sue_ancestors
    assert x_cellunit.spark_num == bob_sue_spark7
    assert x_cellunit.celldepth == bob_sue_celldepth3
    assert x_cellunit.bud_belief_name == bob_sue_bud_belief
    assert x_cellunit.money_grain == bob_sue_money_grain2
    assert x_cellunit.quota == bob_sue_quota300
    assert x_cellunit.mandate == bob_sue_mandate
    assert x_cellunit.beliefadjust == bob_sue_belief
    assert x_cellunit.reason_contexts == set()
    assert x_cellunit.beliefspark_facts == bob_sue_beliefspark_factunits
    assert x_cellunit.found_facts == bob_sue_found_factunits
    assert x_cellunit.boss_facts == bob_sue_boss_factunits


def test_cellunit_shop_ReturnsObj_Scenario2_Withreason_contexts():
    # ESTABLISH
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    clean_fact = clean_factunit()
    sue_belief.add_plan(clean_factunit().fact_state)
    sue_belief.add_plan(wx.mop_rope, pledge=True)
    sue_belief.edit_reason(wx.mop_rope, clean_fact.fact_context, clean_fact.fact_state)

    # WHEN
    x_cellunit = cellunit_shop(wx.sue, beliefadjust=sue_belief)

    # THEN
    assert x_cellunit.bud_belief_name == wx.sue
    assert x_cellunit.beliefadjust == sue_belief
    assert x_cellunit.reason_contexts == sue_belief.get_reason_contexts()
    assert len(x_cellunit.reason_contexts) == 1


def test_cellunit_shop_ReturnsObj_Scenario3_clear_facts():
    # ESTABLISH
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    clean_fact = clean_factunit()
    sue_belief.add_plan(clean_factunit().fact_state)
    sue_belief.add_plan(wx.mop_rope, pledge=True)
    sue_belief.edit_reason(wx.mop_rope, clean_fact.fact_context, clean_fact.fact_state)
    sue_belief.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    assert len(sue_belief.get_planroot_factunits_dict()) == 1

    # WHEN
    x_cellunit = cellunit_shop(wx.sue, beliefadjust=sue_belief)

    # THEN
    assert len(x_cellunit.beliefadjust.get_planroot_factunits_dict()) == 0
    assert x_cellunit.beliefadjust != sue_belief


def test_Cellunit_get_cell_belief_name_ReturnsObj_Scenario0_NoAncestors():
    # ESTABLISH
    root_cellunit = cellunit_shop(wx.yao, [])

    # WHEN / THEN
    assert root_cellunit.get_cell_belief_name() == wx.yao


def test_Cellunit_get_cell_belief_name_ReturnsObj_Scenario1_WithAncestors():
    # ESTABLISH
    bob_sue_ancestors = [wx.bob, wx.sue]
    bob_sue_bud_belief = wx.yao
    bob_sue_cellunit = cellunit_shop(bob_sue_bud_belief, bob_sue_ancestors)

    # WHEN
    bob_sue_cell_belief_name = bob_sue_cellunit.get_cell_belief_name()

    # THEN
    assert bob_sue_cell_belief_name == wx.sue


def test_CellUnit_eval_beliefspark_SetsAttr_Scenario0_ParameterIsNone():
    # ESTABLISH
    yao_cellunit = cellunit_shop(wx.yao)
    yao_cellunit.beliefadjust = "testing_place_holder"
    yao_cellunit.beliefspark_facts = "testing_place_holder"
    yao_cellunit.reason_contexts = "testing_place_holder"
    assert yao_cellunit.beliefadjust
    assert yao_cellunit.beliefspark_facts != {}
    assert yao_cellunit.reason_contexts != set()

    # WHEN
    yao_cellunit.eval_beliefspark(None)

    # THEN
    assert yao_cellunit.beliefadjust is None
    assert yao_cellunit.beliefspark_facts == {}
    assert yao_cellunit.reason_contexts == set()


def test_CellUnit_eval_beliefspark_SetsAttr_Scenario1():
    # ESTABLISH
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    clean_fact = clean_factunit()
    yao_belief.add_plan(clean_fact.fact_state)
    yao_belief.add_plan(wx.mop_rope, pledge=True)
    yao_belief.edit_reason(wx.mop_rope, clean_fact.fact_context, clean_fact.fact_state)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_cellunit = cellunit_shop(wx.yao)
    assert yao_cellunit.beliefspark_facts == {}
    assert yao_cellunit.reason_contexts == set()

    # WHEN
    yao_cellunit.eval_beliefspark(yao_belief)

    # THEN
    expected_factunits = {clean_fact.fact_context: clean_fact}
    assert yao_cellunit.beliefspark_facts == expected_factunits
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


def test_CellUnit_get_beliefsparks_credit_ledger_ReturnsObj_Scenario0_NoBelief():
    # ESTABLISH
    yao_cellunit = cellunit_shop(wx.yao)

    # WHEN
    gen_credit_ledger = yao_cellunit.get_beliefsparks_credit_ledger()

    # THEN
    assert gen_credit_ledger == {}


def test_get_beliefsparks_credit_ledger_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_voiceunit(wx.sue, 3, 5)
    sue_belief.add_voiceunit(wx.yao, 7, 2)
    sue_cell = cellunit_shop(wx.yao, beliefadjust=sue_belief)

    # WHEN
    gen_credit_ledger = sue_cell.get_beliefsparks_credit_ledger()

    # THEN
    expected_credit_ledger = {wx.sue: 3, wx.yao: 7}
    assert gen_credit_ledger == expected_credit_ledger


def test_CellUnit_get_beliefsparks_quota_ledger_ReturnsObj_Scenario0_NoBelief():
    # ESTABLISH
    yao_cellunit = cellunit_shop(wx.yao)

    # WHEN
    gen_credit_ledger = yao_cellunit.get_beliefsparks_quota_ledger()

    # THEN
    assert gen_credit_ledger == {}


def test_get_beliefsparks_quota_ledger_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_voiceunit(wx.sue, 3, 5)
    sue_belief.add_voiceunit(wx.yao, 7, 2)
    sue_cell = cellunit_shop(wx.yao, quota=55, beliefadjust=sue_belief)

    # WHEN
    gen_credit_ledger = sue_cell.get_beliefsparks_quota_ledger()

    # THEN
    expected_credit_ledger = {wx.sue: 16, wx.yao: 39}
    assert gen_credit_ledger == expected_credit_ledger


def test_CellUnit_set_found_facts_from_dict_SetsAttr():
    # ESTABLISH
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(wx.yao)
    assert yao_cellunit.found_facts == {}

    # WHEN
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)

    # THEN
    expected_factunits = {clean_fact.fact_context: clean_fact}
    assert yao_cellunit.found_facts == expected_factunits


def test_CellUnit_set_beliefspark_facts_from_dict_SetsAttr():
    # ESTABLISH
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(wx.yao)
    assert yao_cellunit.beliefspark_facts == {}

    # WHEN
    yao_cellunit.set_beliefspark_facts_from_dict(yao_found_fact_dict)

    # THEN
    expected_factunits = {clean_fact.fact_context: clean_fact}
    assert yao_cellunit.beliefspark_facts == expected_factunits


def test_CellUnit_set_boss_facts_from_other_facts_SetsAttr_Scenario0_found_facts_only():
    # ESTABLISH
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(wx.yao)
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


def test_CellUnit_set_boss_facts_from_other_facts_SetsAttr_Scenario1_beliefspark_facts_only():
    # ESTABLISH
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(wx.yao)
    yao_cellunit.set_beliefspark_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.beliefspark_facts) == 1
    assert yao_cellunit.found_facts == {}
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.set_boss_facts_from_other_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.beliefspark_facts
    assert yao_cellunit.boss_facts == {clean_fact.fact_context: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_set_boss_facts_from_other_facts_SetsAttr_Scenario2_beliefspark_facts_And_found_facts():
    # ESTABLISH
    clean_fact = clean_factunit()
    sky_fact = sky_blue_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_beliefspark_fact_dict = {sky_fact.fact_context: sky_fact.to_dict()}
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(wx.yao)
    yao_cellunit.set_beliefspark_facts_from_dict(yao_beliefspark_fact_dict)
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
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(wx.yao)
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


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario1_beliefspark_facts_only():
    # ESTABLISH
    clean_fact = clean_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(wx.yao)
    yao_cellunit.set_beliefspark_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.beliefspark_facts) == 1
    assert yao_cellunit.found_facts == {}
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.add_other_facts_to_boss_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.beliefspark_facts
    assert yao_cellunit.boss_facts == {clean_fact.fact_context: clean_fact}
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


def test_CellUnit_add_other_facts_to_boss_facts_SetsAttr_Scenario2_beliefspark_facts_And_found_facts():
    # ESTABLISH
    clean_fact = clean_factunit()
    sky_fact = sky_blue_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    yao_belief.add_fact(
        clean_fact.fact_context, clean_fact.fact_state, create_missing_plans=True
    )
    run_rope = yao_belief.make_l1_rope("run")
    run_fact = factunit_shop(run_rope, run_rope)
    run_facts = {run_fact.fact_context: run_fact}
    yao_beliefspark_fact_dict = {sky_fact.fact_context: sky_fact.to_dict()}
    yao_found_fact_dict = {clean_fact.fact_context: clean_fact.to_dict()}
    yao_cellunit = cellunit_shop(wx.yao)
    yao_cellunit.set_beliefspark_facts_from_dict(yao_beliefspark_fact_dict)
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
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    run_rope = yao_belief.make_l1_rope("run")
    fast_rope = yao_belief.make_rope(run_rope, "fast")
    run_fact = factunit_shop(run_rope, run_rope)
    fast_fact = factunit_shop(run_rope, fast_rope)
    run_facts = {run_fact.fact_context: run_fact}

    yao_beliefspark_fact_dict = {fast_fact.fact_context: fast_fact.to_dict()}
    yao_found_fact_dict = {fast_fact.fact_context: fast_fact.to_dict()}
    yao_cellunit = cellunit_shop(wx.yao)
    yao_cellunit.set_beliefspark_facts_from_dict(yao_beliefspark_fact_dict)
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
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_bud_belief = wx.yao
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_quota300 = 300
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    sue_beliefspark_factunits = {clean_fact.fact_context: clean_fact}
    sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
        sue_quota300,
        None,
        sue_beliefspark_factunits,
        sue_found_factunits,
        sue_boss_factunits,
    )
    sue_cell.reason_contexts = {clean_fact.fact_context, sky_blue_fact.fact_context}
    assert sue_cell.beliefspark_facts == sue_beliefspark_factunits
    assert sue_cell.found_facts == sue_found_factunits
    assert sue_cell.boss_facts == sue_boss_factunits

    # WHEN
    sue_cell.filter_facts_by_reason_contexts()

    # THEN
    assert sue_cell.beliefspark_facts == sue_beliefspark_factunits
    assert sue_cell.found_facts == sue_found_factunits
    assert sue_cell.boss_facts == sue_boss_factunits

    # WHEN
    sue_cell.reason_contexts = {clean_fact.fact_context}
    sue_cell.filter_facts_by_reason_contexts()

    # THEN
    assert sue_cell.beliefspark_facts == sue_beliefspark_factunits
    assert sue_cell.found_facts == sue_found_factunits
    assert sue_cell.boss_facts == {}

    # WHEN
    sue_cell.reason_contexts = {}
    sue_cell.filter_facts_by_reason_contexts()

    # THEN
    assert sue_cell.beliefspark_facts == {}
    assert sue_cell.found_facts == {}
    assert sue_cell.boss_facts == {}


def test_CellUnit_set_beliefadjust_facts_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_bud_belief = wx.yao
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_quota300 = 300
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
        sue_quota300,
        beliefadjust=sue_belief,
    )
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() == {}

    # WHEN
    sue_cell.set_beliefadjust_facts()

    # THEN
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() == {}


def test_CellUnit_set_beliefadjust_facts_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_bud_belief = wx.yao
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_quota300 = 300
    casa_clean_fact = clean_factunit()
    clean_facts = {casa_clean_fact.fact_context: casa_clean_fact}
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_plan(casa_clean_fact.fact_state)
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
        sue_quota300,
        beliefadjust=sue_belief,
        beliefspark_facts=clean_facts,
    )
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() == {}

    # WHEN
    sue_cell.set_beliefadjust_facts()

    # THEN
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() != {}
    sue_belief_facts = sue_cell.beliefadjust.get_planroot_factunits_dict()
    sue_belief_casa_fact_dict = sue_belief_facts.get(wx.casa_rope)
    assert sue_belief_casa_fact_dict.get(kw.fact_state) == casa_clean_fact.fact_state


def test_CellUnit_set_beliefadjust_facts_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_bud_belief = wx.yao
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_quota300 = 300
    casa_clean_fact = clean_factunit()
    casa_dirty_fact = dirty_factunit()
    clean_facts = {casa_clean_fact.fact_context: casa_clean_fact}
    dirty_facts = {casa_dirty_fact.fact_context: casa_dirty_fact}
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_plan(casa_clean_fact.fact_state)
    sue_belief.add_plan(casa_dirty_fact.fact_state)
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
        sue_quota300,
        beliefadjust=sue_belief,
        beliefspark_facts=clean_facts,
        found_facts=dirty_facts,
    )
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() == {}

    # WHEN
    sue_cell.set_beliefadjust_facts()

    # THEN
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() != {}
    sue_belief_facts = sue_cell.beliefadjust.get_planroot_factunits_dict()
    sue_belief_casa_fact_dict = sue_belief_facts.get(wx.casa_rope)
    assert sue_belief_casa_fact_dict.get(kw.fact_state) == casa_dirty_fact.fact_state


def test_CellUnit_set_beliefadjust_facts_ReturnsObj_Scenario3():
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_bud_belief = wx.yao
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_quota300 = 300
    casa_clean_fact = clean_factunit()
    casa_dirty_fact = dirty_factunit()
    casa_grimy_fact = grimy_factunit()
    clean_facts = {casa_clean_fact.fact_context: casa_clean_fact}
    dirty_facts = {casa_dirty_fact.fact_context: casa_dirty_fact}
    grimy_facts = {casa_grimy_fact.fact_context: casa_grimy_fact}
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_plan(casa_clean_fact.fact_state)
    sue_belief.add_plan(casa_dirty_fact.fact_state)
    sue_belief.add_plan(casa_grimy_fact.fact_state)
    sue_cell = cellunit_shop(
        sue_bud_belief,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
        sue_quota300,
        beliefadjust=sue_belief,
        beliefspark_facts=clean_facts,
        found_facts=dirty_facts,
        boss_facts=grimy_facts,
    )
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() == {}

    # WHEN
    sue_cell.set_beliefadjust_facts()

    # THEN
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() != {}
    sue_belief_facts = sue_cell.beliefadjust.get_planroot_factunits_dict()
    sue_belief_casa_fact_dict = sue_belief_facts.get(wx.casa_rope)
    assert sue_belief_casa_fact_dict.get(kw.fact_state) == casa_grimy_fact.fact_state


def test_CellUnit_set_voice_mandate_ledger_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_cell = cellunit_shop(
        wx.yao,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
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
    assert sue_cell._voice_mandate_ledger == {wx.sue: sue_mandate}


def test_CellUnit_set_voice_mandate_ledger_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_voiceunit(wx.sue, 3, 5)
    sue_belief.add_voiceunit(wx.yao, 7, 2)
    sue_cell = cellunit_shop(
        wx.yao,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
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
    assert sue_cell._voice_mandate_ledger == {wx.yao: 311, wx.sue: 133}


def test_CellUnit_calc_voice_mandate_ledger_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_voiceunit(wx.sue, 3, 5)
    sue_belief.add_voiceunit(wx.yao, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_belief.add_plan(clean_fact.fact_state)
    sue_belief.add_plan(dirty_fact.fact_state)
    sue_belief.add_plan(wx.mop_rope, 1, pledge=True)
    sue_belief.edit_reason(wx.mop_rope, dirty_fact.fact_context, dirty_fact.fact_state)
    sue_belief.add_fact(
        dirty_fact.fact_context, dirty_fact.fact_state, create_missing_plans=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_beliefspark_factunits = {clean_fact.fact_context: clean_fact}
    sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    sue_cell = cellunit_shop(
        wx.yao,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
        sue_quota300,
        beliefadjust=sue_belief,
        beliefspark_facts=sue_beliefspark_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell.reason_contexts = set()
    assert not sue_cell.reason_contexts
    assert sue_cell.boss_facts == {sky_blue_fact.fact_context: sky_blue_fact}
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() == {}
    assert sue_cell._voice_mandate_ledger == {}

    # WHEN
    sue_cell.calc_voice_mandate_ledger()

    # THEN
    assert sue_cell.reason_contexts == {clean_fact.fact_context}
    assert sue_cell.boss_facts == {}
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() != {}
    assert set(sue_cell.beliefadjust.get_planroot_factunits_dict().keys()) == {
        clean_fact.fact_context
    }
    # plan_dict = sue_cell.beliefadjust.get_plan_dict()
    # for plan_rope, plan_obj in plan_dict.items():
    #     print(f"{plan_rope=} {plan_obj.fund_onset=} {plan_obj.fund_cease}")
    assert sue_cell._voice_mandate_ledger != {}
    assert sue_cell._voice_mandate_ledger == {wx.yao: 311, wx.sue: 133}


def test_create_child_cellunits_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_voiceunit(wx.sue, 3, 5)
    sue_belief.add_voiceunit(wx.yao, 7, 2)
    sue_belief.add_voiceunit(wx.bob, 0, 2)
    sue_cell = cellunit_shop(
        wx.yao,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
        sue_quota300,
        beliefadjust=sue_belief,
        mandate=sue_mandate,
    )

    # WHEN
    sue_child_cellunits = create_child_cellunits(sue_cell)

    # THEN
    assert len(sue_child_cellunits) == 2
    sue_sue_cell = sue_child_cellunits[0]
    assert sue_sue_cell.bud_belief_name == wx.yao
    assert sue_sue_cell.ancestors == [wx.sue, wx.sue]
    assert sue_sue_cell.spark_num == sue_spark7
    assert sue_sue_cell.celldepth == sue_celldepth3 - 1
    assert sue_sue_cell.money_grain == sue_money_grain2
    assert sue_sue_cell.mandate == 133
    # assert not sue_sue_cell.beliefadjust
    assert sue_sue_cell.beliefspark_facts == {}
    assert sue_sue_cell.found_facts == {}
    assert sue_sue_cell.boss_facts == {}

    sue_yao_cell = sue_child_cellunits[1]
    assert sue_yao_cell.bud_belief_name == wx.yao
    assert sue_yao_cell.ancestors == [wx.sue, wx.yao]
    assert sue_yao_cell.spark_num == sue_spark7
    assert sue_yao_cell.celldepth == sue_celldepth3 - 1
    assert sue_yao_cell.money_grain == sue_money_grain2
    assert sue_yao_cell.mandate == 311
    # assert sue_yao_cell.beliefadjust
    assert sue_yao_cell.beliefspark_facts == {}
    assert sue_yao_cell.found_facts == {}
    assert sue_yao_cell.boss_facts == {}


def test_create_child_cellunits_ReturnsObj_Scenario1_BudDepth0():
    # ESTABLISH
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_celldepth = 0
    sue_money_grain2 = 2
    sue_quota300 = 300
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_voiceunit(wx.sue, 3, 5)
    sue_belief.add_voiceunit(wx.yao, 7, 2)
    sue_belief.add_voiceunit(wx.bob, 0, 2)
    sue_cell = cellunit_shop(
        wx.yao,
        sue_ancestors,
        sue_spark7,
        sue_celldepth,
        sue_money_grain2,
        sue_quota300,
        beliefadjust=sue_belief,
    )

    # WHEN
    sue_child_cellunits = create_child_cellunits(sue_cell)

    # THEN
    assert sue_child_cellunits == []


def test_create_child_cellunits_ReturnsObj_Scenario2_boss_facts():
    # ESTABLISH
    yao_celldepth = 3
    yao_quota = 320
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    yao_belief = beliefunit_shop(wx.yao, wx.a23)
    yao_belief.add_voiceunit(wx.sue, 3, 5)
    yao_belief.add_voiceunit(wx.yao, 7, 2)
    yao_belief.add_voiceunit(wx.bob, 0, 2)
    clean_fact = clean_factunit()
    yao_belief.add_plan(wx.casa_rope, 1)
    yao_belief.add_plan(wx.mop_rope, 1, pledge=True)
    yao_belief.add_plan(clean_fact.fact_state)
    yao_belief.add_plan(dirty_fact.fact_state)
    yao_belief.edit_reason(wx.mop_rope, dirty_fact.fact_context, dirty_fact.fact_state)
    yao_cell = cellunit_shop(
        wx.yao, celldepth=yao_celldepth, quota=yao_quota, beliefadjust=yao_belief
    )
    yao_cell.beliefspark_facts = {dirty_fact.fact_context: dirty_fact}
    # sue_cell._voice_mandate_ledger = {wx.yao: 210, wx.sue: 90, wx.bob: 0}

    # WHEN
    sue_child_cellunits = create_child_cellunits(yao_cell)

    # THEN
    assert len(sue_child_cellunits) == 2
    sue_yao_cell = sue_child_cellunits[1]
    assert sue_yao_cell.beliefspark_facts == {}
    assert sue_yao_cell.found_facts == {}
    assert sue_yao_cell.boss_facts == {dirty_fact.fact_context: dirty_fact}

    sue_sue_cell = sue_child_cellunits[0]
    assert sue_sue_cell.beliefspark_facts == {}
    assert sue_sue_cell.found_facts == {}
    assert sue_sue_cell.boss_facts == {dirty_fact.fact_context: dirty_fact}


def test_create_child_cellunits_ReturnsObj_Scenario3_StateOfCellAdjustIsReset():
    # ESTABLISH
    sue_ancestors = [wx.sue]
    sue_spark7 = 7
    sue_celldepth3 = 3
    sue_money_grain2 = 2
    sue_mandate = 444
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_voiceunit(wx.sue, 3, 5)
    sue_belief.add_voiceunit(wx.yao, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_belief.add_plan(clean_fact.fact_state)
    sue_belief.add_plan(dirty_fact.fact_state)
    sue_belief.add_plan(wx.mop_rope, 1, pledge=True)
    sue_belief.edit_reason(wx.mop_rope, dirty_fact.fact_context, dirty_fact.fact_state)
    sue_belief.add_fact(
        dirty_fact.fact_context, dirty_fact.fact_state, create_missing_plans=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_beliefspark_factunits = {clean_fact.fact_context: clean_fact}
    sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    sue_cell = cellunit_shop(
        wx.yao,
        sue_ancestors,
        sue_spark7,
        sue_celldepth3,
        sue_money_grain2,
        beliefadjust=sue_belief,
        beliefspark_facts=sue_beliefspark_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell.reason_contexts = set()
    assert not sue_cell.reason_contexts
    assert sue_cell.boss_facts == {sky_blue_fact.fact_context: sky_blue_fact}
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() == {}
    assert sue_cell._voice_mandate_ledger == {}

    # WHEN
    sue_child_cellunits = create_child_cellunits(sue_cell)

    # # WHEN
    # sue_cell.calc_voice_mandate_ledger()

    # # THEN
    assert sue_cell.reason_contexts == {dirty_fact.fact_context}
    assert sue_cell.boss_facts == {}
    assert sue_cell.beliefadjust.get_planroot_factunits_dict() != {}
    assert set(sue_cell.beliefadjust.get_planroot_factunits_dict().keys()) == {
        dirty_fact.fact_context
    }
    # plan_dict = sue_cell.beliefadjust.get_plan_dict()
    # for plan_rope, plan_obj in plan_dict.items():
    #     print(f"{plan_rope=} {plan_obj.fund_onset=} {plan_obj.fund_cease}")
    assert sue_cell._voice_mandate_ledger != {}
    assert sue_cell._voice_mandate_ledger == {wx.yao: 311, wx.sue: 133}

    # THEN
    assert len(sue_child_cellunits) == 2
    sue_yao_cell = sue_child_cellunits[1]
    assert sue_yao_cell.beliefspark_facts == {}
    assert sue_yao_cell.found_facts == {}
    assert sue_yao_cell.boss_facts == {dirty_fact.fact_context: dirty_fact}
    assert sue_yao_cell.mandate == 311

    sue_sue_cell = sue_child_cellunits[0]
    assert sue_sue_cell.beliefspark_facts == {}
    assert sue_sue_cell.found_facts == {}
    assert sue_sue_cell.boss_facts == {dirty_fact.fact_context: dirty_fact}
    assert sue_sue_cell.mandate == 133
