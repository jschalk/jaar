from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.owner_tool import (
    owner_plan_factunit_get_obj,
    owner_plan_reason_premiseunit_get_obj as premiseunit_get_obj,
    owner_plan_reasonunit_get_obj,
)
from src.a06_owner_logic.test._util.a06_str import (
    acct_debt_points_str,
    acct_name_str,
    addin_str,
    awardee_title_str,
    begin_str,
    close_str,
    denom_str,
    fcontext_str,
    fopen_str,
    give_force_str,
    gogo_want_str,
    group_debt_points_str,
    group_title_str,
    healer_name_str,
    mass_str,
    morph_str,
    numor_str,
    owner_acct_membership_str,
    owner_acctunit_str,
    owner_plan_awardlink_str,
    owner_plan_factunit_str,
    owner_plan_healerlink_str,
    owner_plan_laborlink_str,
    owner_plan_reason_premiseunit_str,
    owner_plan_reasonunit_str,
    owner_planunit_str,
    ownerunit_str,
    parent_rope_str,
    plan_label_str,
    plan_rope_str,
    rcontext_str,
    rplan_active_requisite_str,
    stop_want_str,
    take_force_str,
    task_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop, sift_owneratom
from src.a08_owner_atom_logic.test._util.a08_str import INSERT_str, UPDATE_str


def test_sift_atom_ReturnsNoneIfGivenOwnerAtomIsUPDATE():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    sue_owner.add_plan(casa_rope)
    casa_atom = owneratom_shop(owner_planunit_str(), UPDATE_str())
    casa_atom.set_arg(parent_rope_str(), sue_owner.belief_label)
    casa_atom.set_arg(plan_label_str(), casa_str)
    casa_atom.set_arg(mass_str(), 8)
    # THEN
    new_casa_atom = sift_owneratom(sue_owner, casa_atom)

    # THEN
    assert not new_casa_atom


def test_sift_atom_ReturnsObj_OwnerAtom_UPDATE_ownerunit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    sue_bit = 34
    sue_credor_respect = 44
    sue_debtor_respect = 54
    sue_fund_iota = 66
    sue_fund_pool = 69
    sue_max_tree_traverse = 72
    sue_penny = 2
    sue_tally = 100
    zia_atom = owneratom_shop(ownerunit_str(), INSERT_str())
    zia_atom.set_arg("respect_bit", sue_bit)
    zia_atom.set_arg("credor_respect", sue_credor_respect)
    zia_atom.set_arg("debtor_respect", sue_debtor_respect)
    zia_atom.set_arg("fund_iota", sue_fund_iota)
    zia_atom.set_arg("fund_pool", sue_fund_pool)
    zia_atom.set_arg("max_tree_traverse", sue_max_tree_traverse)
    zia_atom.set_arg("penny", sue_penny)
    zia_atom.set_arg("tally", sue_tally)

    # WHEN
    new_zia_owneratom = sift_owneratom(sue_owner, zia_atom)

    # THEN
    assert new_zia_owneratom
    assert new_zia_owneratom.crud_str == UPDATE_str()
    assert new_zia_owneratom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_owneratom.get_jvalues_dict()
    assert zia_jvalues == {
        "respect_bit": sue_bit,
        "credor_respect": sue_credor_respect,
        "debtor_respect": sue_debtor_respect,
        "fund_iota": sue_fund_iota,
        "fund_pool": sue_fund_pool,
        "max_tree_traverse": sue_max_tree_traverse,
        "penny": sue_penny,
        "tally": sue_tally,
    }


def test_sift_atom_ReturnsObj_OwnerAtom_UPDATE_owner_acctunit():
    # ESTABLISH
    zia_str = "Zia"
    zia_acct_debt_points = 51
    sue_owner = ownerunit_shop("Sue")
    sue_owner.add_acctunit(zia_str)

    zia_atom = owneratom_shop(owner_acctunit_str(), INSERT_str())
    zia_atom.set_arg(acct_name_str(), zia_str)
    zia_atom.set_arg(acct_debt_points_str(), zia_acct_debt_points)

    # WHEN
    new_zia_owneratom = sift_owneratom(sue_owner, zia_atom)

    # THEN
    assert new_zia_owneratom
    assert new_zia_owneratom.crud_str == UPDATE_str()
    assert new_zia_owneratom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_owneratom.get_jvalues_dict()
    assert zia_jvalues == {acct_debt_points_str(): 51}


def test_sift_atom_ReturnsObj_OwnerAtom_UPDATE_owner_acct_membership():
    # ESTABLISH
    zia_str = "Zia"
    run_str = ";run"
    zia_run_group_debt_points = 76
    sue_owner = ownerunit_shop("Sue")
    sue_owner.add_acctunit(zia_str)
    sue_owner.get_acct(zia_str).add_membership(run_str)

    zia_atom = owneratom_shop(owner_acct_membership_str(), INSERT_str())
    zia_atom.set_arg(acct_name_str(), zia_str)
    zia_atom.set_arg(group_title_str(), run_str)
    zia_atom.set_arg(group_debt_points_str(), zia_run_group_debt_points)

    # WHEN
    new_zia_owneratom = sift_owneratom(sue_owner, zia_atom)

    # THEN
    assert new_zia_owneratom
    assert new_zia_owneratom.crud_str == UPDATE_str()
    assert new_zia_owneratom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_owneratom.get_jvalues_dict()
    assert zia_jvalues == {group_debt_points_str(): zia_run_group_debt_points}


def test_sift_atom_ReturnsObj_OwnerAtom_UPDATE_owner_planunit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    sue_owner.add_plan(casa_rope)

    sue_addin = 23
    sue_begin = 37
    sue_close = 43
    sue_denom = 47
    sue_gogo_want = 59
    sue_mass = 67
    sue_morph = 79
    sue_numor = 83
    sue_task = 97
    sue_problem_bool = True
    sue_stop_want = 107
    old_casa_atom = owneratom_shop(owner_planunit_str(), INSERT_str())
    old_casa_atom.set_arg(plan_rope_str(), casa_rope)
    old_casa_atom.set_arg(addin_str(), sue_addin)
    old_casa_atom.set_arg(begin_str(), sue_begin)
    old_casa_atom.set_arg(close_str(), sue_close)
    old_casa_atom.set_arg(denom_str(), sue_denom)
    old_casa_atom.set_arg(gogo_want_str(), sue_gogo_want)
    old_casa_atom.set_arg(mass_str(), sue_mass)
    old_casa_atom.set_arg(morph_str(), sue_morph)
    old_casa_atom.set_arg(numor_str(), sue_numor)
    old_casa_atom.set_arg(task_str(), sue_task)
    old_casa_atom.set_arg("problem_bool", sue_problem_bool)
    old_casa_atom.set_arg(stop_want_str(), sue_stop_want)
    # THEN
    new_casa_atom = sift_owneratom(sue_owner, old_casa_atom)

    # THEN
    assert new_casa_atom
    assert new_casa_atom.crud_str == UPDATE_str()
    assert new_casa_atom.get_jvalues_dict()
    zia_jvalues = new_casa_atom.get_jvalues_dict()
    assert zia_jvalues.get(addin_str()) == sue_addin
    assert zia_jvalues.get(begin_str()) == sue_begin
    assert zia_jvalues.get(close_str()) == sue_close
    assert zia_jvalues.get(denom_str()) == sue_denom
    assert zia_jvalues.get(gogo_want_str()) == sue_gogo_want
    assert zia_jvalues.get(mass_str()) == sue_mass
    assert zia_jvalues.get(morph_str()) == sue_morph
    assert zia_jvalues.get(numor_str()) == sue_numor
    assert zia_jvalues.get(task_str()) == sue_task
    assert zia_jvalues.get("problem_bool") == sue_problem_bool
    assert zia_jvalues.get(stop_want_str()) == sue_stop_want


def test_sift_atom_ReturnsObj_OwnerAtom_UPDATE_owner_plan_awardlink():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    sue_owner.add_plan(casa_rope)
    run_str = ";run"
    zia_run_give_force = 72
    zia_run_take_force = 76
    sue_owner.get_plan_obj(casa_rope).set_awardlink(awardlink_shop(run_str, 2, 3))

    zia_atom = owneratom_shop(owner_plan_awardlink_str(), INSERT_str())
    zia_atom.set_arg(plan_rope_str(), casa_rope)
    zia_atom.set_arg(awardee_title_str(), run_str)
    zia_atom.set_arg(give_force_str(), zia_run_give_force)
    zia_atom.set_arg(take_force_str(), zia_run_take_force)

    # WHEN
    new_zia_owneratom = sift_owneratom(sue_owner, zia_atom)

    # THEN
    assert new_zia_owneratom
    assert new_zia_owneratom.crud_str == UPDATE_str()
    assert new_zia_owneratom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_owneratom.get_jvalues_dict()
    assert zia_jvalues.get(give_force_str()) == zia_run_give_force
    assert zia_jvalues.get(take_force_str()) == zia_run_take_force


def test_sift_atom_ReturnsObj_OwnerAtom_UPDATE_owner_plan_reasonunit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    week_str = "week"
    week_rope = sue_owner.make_l1_rope(casa_str)
    sue_owner.add_plan(casa_rope)
    sue_owner.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(week_rope))

    new_rplan_active_requisite = True
    casa_atom = owneratom_shop(owner_plan_reasonunit_str(), INSERT_str())
    casa_atom.set_arg(plan_rope_str(), casa_rope)
    casa_atom.set_arg(rcontext_str(), week_rope)
    casa_atom.set_arg(rplan_active_requisite_str(), new_rplan_active_requisite)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_reasonunit = owner_plan_reasonunit_get_obj(sue_owner, casa_jkeys)
    assert casa_reasonunit.rplan_active_requisite != new_rplan_active_requisite
    assert casa_reasonunit.rplan_active_requisite is None

    # WHEN
    new_zia_owneratom = sift_owneratom(sue_owner, casa_atom)

    # THEN
    assert new_zia_owneratom
    assert new_zia_owneratom.crud_str == UPDATE_str()
    assert new_zia_owneratom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_owneratom.get_jvalues_dict()
    zia_requisite_value = zia_jvalues.get(rplan_active_requisite_str())
    assert zia_requisite_value == new_rplan_active_requisite


def test_sift_atom_ReturnsObj_OwnerAtom_UPDATE_owner_plan_reason_premiseunit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_owner.make_l1_rope(week_str)
    thur_str = "thur"
    thur_rope = sue_owner.make_rope(week_rope, thur_str)
    sue_owner.add_plan(clean_rope)
    sue_owner.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(week_rope))
    clean_plan = sue_owner.get_plan_obj(clean_rope)
    clean_plan.set_reasonunit(reasonunit_shop(week_rope))
    clean_plan.get_reasonunit(week_rope).set_premise(thur_rope)

    thur_pdivisor = 39
    thur_atom = owneratom_shop(owner_plan_reason_premiseunit_str(), INSERT_str())
    thur_atom.set_arg(plan_rope_str(), clean_rope)
    thur_atom.set_arg(rcontext_str(), week_rope)
    thur_atom.set_arg("pstate", thur_rope)
    assert thur_atom.is_valid()
    thur_atom.set_arg("pdivisor", thur_pdivisor)
    thur_jkeys = thur_atom.get_jkeys_dict()
    thur_premiseunit = premiseunit_get_obj(sue_owner, thur_jkeys)
    assert thur_premiseunit.pdivisor != thur_pdivisor
    assert thur_premiseunit.pdivisor is None

    # WHEN
    new_zia_owneratom = sift_owneratom(sue_owner, thur_atom)

    # THEN
    assert new_zia_owneratom
    assert new_zia_owneratom.crud_str == UPDATE_str()
    assert new_zia_owneratom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_owneratom.get_jvalues_dict()
    assert zia_jvalues.get("pdivisor") == thur_pdivisor


def test_sift_atom_ReturnsObj_OwnerAtom_UPDATE_owner_plan_factunit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    week_str = "week"
    week_rope = sue_owner.make_l1_rope(casa_str)
    sue_owner.add_plan(casa_rope)
    sue_owner.get_plan_obj(casa_rope).set_factunit(factunit_shop(week_rope))

    casa_fopen = 32
    casa_atom = owneratom_shop(owner_plan_factunit_str(), INSERT_str())
    casa_atom.set_arg(plan_rope_str(), casa_rope)
    casa_atom.set_arg(fcontext_str(), week_rope)
    casa_atom.set_arg(fopen_str(), casa_fopen)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_factunit = owner_plan_factunit_get_obj(sue_owner, casa_jkeys)
    assert casa_factunit.fopen != casa_fopen
    assert casa_factunit.fopen is None

    # WHEN
    new_zia_owneratom = sift_owneratom(sue_owner, casa_atom)

    # THEN
    assert new_zia_owneratom
    assert new_zia_owneratom.crud_str == UPDATE_str()
    assert new_zia_owneratom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_owneratom.get_jvalues_dict()
    assert zia_jvalues.get(fopen_str()) == casa_fopen
