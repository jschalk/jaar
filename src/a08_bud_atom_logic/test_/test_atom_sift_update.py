from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_item import reasonunit_shop, factunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_tool import (
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str,
    bud_item_factunit_str,
    bud_item_reasonunit_get_obj,
    bud_item_reason_premiseunit_get_obj as premiseunit_get_obj,
    bud_item_factunit_get_obj,
    budunit_str,
)
from src.a08_bud_atom_logic.atom import (
    atom_insert,
    atom_update,
    budatom_shop,
    sift_budatom,
)
from src.a08_bud_atom_logic.atom_config import (
    acct_name_str,
    awardee_tag_str,
    group_label_str,
    healer_name_str,
    parent_road_str,
    item_title_str,
    road_str,
    base_str,
    debtit_belief_str,
    debtit_vote_str,
    addin_str,
    begin_str,
    close_str,
    denom_str,
    gogo_want_str,
    mass_str,
    morph_str,
    numor_str,
    pledge_str,
    stop_want_str,
    base_item_active_requisite_str,
    fopen_str,
    give_force_str,
    take_force_str,
)


def test_sift_atom_ReturnsNoneIfGivenBudAtomIsUPDATE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_item(casa_road)
    casa_atom = budatom_shop(bud_itemunit_str(), atom_update())
    casa_atom.set_arg(parent_road_str(), sue_bud.fisc_title)
    casa_atom.set_arg(item_title_str(), casa_str)
    casa_atom.set_arg(mass_str(), 8)
    # THEN
    new_casa_atom = sift_budatom(sue_bud, casa_atom)

    # THEN
    assert not new_casa_atom


def test_sift_atom_ReturnsObj_BudAtom_UPDATE_budunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bit = 34
    sue_credor_respect = 44
    sue_debtor_respect = 54
    sue_fund_coin = 66
    sue_fund_pool = 69
    sue_max_tree_traverse = 72
    sue_penny = 2
    sue_tally = 100
    zia_atom = budatom_shop(budunit_str(), atom_insert())
    zia_atom.set_arg("respect_bit", sue_bit)
    zia_atom.set_arg("credor_respect", sue_credor_respect)
    zia_atom.set_arg("debtor_respect", sue_debtor_respect)
    zia_atom.set_arg("fund_coin", sue_fund_coin)
    zia_atom.set_arg("fund_pool", sue_fund_pool)
    zia_atom.set_arg("max_tree_traverse", sue_max_tree_traverse)
    zia_atom.set_arg("penny", sue_penny)
    zia_atom.set_arg("tally", sue_tally)

    # WHEN
    new_zia_budatom = sift_budatom(sue_bud, zia_atom)

    # THEN
    assert new_zia_budatom
    assert new_zia_budatom.crud_str == atom_update()
    assert new_zia_budatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_budatom.get_jvalues_dict()
    assert zia_jvalues == {
        "respect_bit": sue_bit,
        "credor_respect": sue_credor_respect,
        "debtor_respect": sue_debtor_respect,
        "fund_coin": sue_fund_coin,
        "fund_pool": sue_fund_pool,
        "max_tree_traverse": sue_max_tree_traverse,
        "penny": sue_penny,
        "tally": sue_tally,
    }


def test_sift_atom_ReturnsObj_BudAtom_UPDATE_bud_acctunit():
    # ESTABLISH
    zia_str = "Zia"
    zia_debtit_belief = 51
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(zia_str)

    zia_atom = budatom_shop(bud_acctunit_str(), atom_insert())
    zia_atom.set_arg(acct_name_str(), zia_str)
    zia_atom.set_arg(debtit_belief_str(), zia_debtit_belief)

    # WHEN
    new_zia_budatom = sift_budatom(sue_bud, zia_atom)

    # THEN
    assert new_zia_budatom
    assert new_zia_budatom.crud_str == atom_update()
    assert new_zia_budatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_budatom.get_jvalues_dict()
    assert zia_jvalues == {debtit_belief_str(): 51}


def test_sift_atom_ReturnsObj_BudAtom_UPDATE_bud_acct_membership():
    # ESTABLISH
    zia_str = "Zia"
    run_str = ";run"
    zia_run_debtit_vote = 76
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(zia_str)
    sue_bud.get_acct(zia_str).add_membership(run_str)

    zia_atom = budatom_shop(bud_acct_membership_str(), atom_insert())
    zia_atom.set_arg(acct_name_str(), zia_str)
    zia_atom.set_arg(group_label_str(), run_str)
    zia_atom.set_arg(debtit_vote_str(), zia_run_debtit_vote)

    # WHEN
    new_zia_budatom = sift_budatom(sue_bud, zia_atom)

    # THEN
    assert new_zia_budatom
    assert new_zia_budatom.crud_str == atom_update()
    assert new_zia_budatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_budatom.get_jvalues_dict()
    assert zia_jvalues == {debtit_vote_str(): zia_run_debtit_vote}


def test_sift_atom_ReturnsObj_BudAtom_UPDATE_bud_itemunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_item(casa_road)

    sue_addin = 23
    sue_begin = 37
    sue_close = 43
    sue_denom = 47
    sue_gogo_want = 59
    sue_mass = 67
    sue_morph = 79
    sue_numor = 83
    sue_pledge = 97
    sue_problem_bool = True
    sue_stop_want = 107
    old_casa_atom = budatom_shop(bud_itemunit_str(), atom_insert())
    old_casa_atom.set_arg(parent_road_str(), sue_bud.fisc_title)
    old_casa_atom.set_arg(item_title_str(), casa_str)
    old_casa_atom.set_arg(addin_str(), sue_addin)
    old_casa_atom.set_arg(begin_str(), sue_begin)
    old_casa_atom.set_arg(close_str(), sue_close)
    old_casa_atom.set_arg(denom_str(), sue_denom)
    old_casa_atom.set_arg(gogo_want_str(), sue_gogo_want)
    old_casa_atom.set_arg(mass_str(), sue_mass)
    old_casa_atom.set_arg(morph_str(), sue_morph)
    old_casa_atom.set_arg(numor_str(), sue_numor)
    old_casa_atom.set_arg(pledge_str(), sue_pledge)
    old_casa_atom.set_arg("problem_bool", sue_problem_bool)
    old_casa_atom.set_arg(stop_want_str(), sue_stop_want)
    # THEN
    new_casa_atom = sift_budatom(sue_bud, old_casa_atom)

    # THEN
    assert new_casa_atom
    assert new_casa_atom.crud_str == atom_update()
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
    assert zia_jvalues.get(pledge_str()) == sue_pledge
    assert zia_jvalues.get("problem_bool") == sue_problem_bool
    assert zia_jvalues.get(stop_want_str()) == sue_stop_want


def test_sift_atom_ReturnsObj_BudAtom_UPDATE_bud_item_awardlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_item(casa_road)
    run_str = ";run"
    zia_run_give_force = 72
    zia_run_take_force = 76
    sue_bud.get_item_obj(casa_road).set_awardlink(awardlink_shop(run_str, 2, 3))

    zia_atom = budatom_shop(bud_item_awardlink_str(), atom_insert())
    zia_atom.set_arg(road_str(), casa_road)
    zia_atom.set_arg(awardee_tag_str(), run_str)
    zia_atom.set_arg(give_force_str(), zia_run_give_force)
    zia_atom.set_arg(take_force_str(), zia_run_take_force)

    # WHEN
    new_zia_budatom = sift_budatom(sue_bud, zia_atom)

    # THEN
    assert new_zia_budatom
    assert new_zia_budatom.crud_str == atom_update()
    assert new_zia_budatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_budatom.get_jvalues_dict()
    assert zia_jvalues.get(give_force_str()) == zia_run_give_force
    assert zia_jvalues.get(take_force_str()) == zia_run_take_force


def test_sift_atom_ReturnsObj_BudAtom_UPDATE_bud_item_reasonunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_str = "week"
    week_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_item(casa_road)
    sue_bud.get_item_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

    new_base_item_active_requisite = True
    casa_atom = budatom_shop(bud_item_reasonunit_str(), atom_insert())
    casa_atom.set_arg(road_str(), casa_road)
    casa_atom.set_arg(base_str(), week_road)
    casa_atom.set_arg(base_item_active_requisite_str(), new_base_item_active_requisite)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_reasonunit = bud_item_reasonunit_get_obj(sue_bud, casa_jkeys)
    assert casa_reasonunit.base_item_active_requisite != new_base_item_active_requisite
    assert casa_reasonunit.base_item_active_requisite is None

    # WHEN
    new_zia_budatom = sift_budatom(sue_bud, casa_atom)

    # THEN
    assert new_zia_budatom
    assert new_zia_budatom.crud_str == atom_update()
    assert new_zia_budatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_budatom.get_jvalues_dict()
    zia_requisite_value = zia_jvalues.get(base_item_active_requisite_str())
    assert zia_requisite_value == new_base_item_active_requisite


def test_sift_atom_ReturnsObj_BudAtom_UPDATE_bud_item_reason_premiseunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    week_str = "week"
    week_road = sue_bud.make_l1_road(week_str)
    thur_str = "thur"
    thur_road = sue_bud.make_road(week_road, thur_str)
    sue_bud.add_item(clean_road)
    sue_bud.get_item_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))
    clean_item = sue_bud.get_item_obj(clean_road)
    clean_item.set_reasonunit(reasonunit_shop(week_road))
    clean_item.get_reasonunit(week_road).set_premise(thur_road)

    thur_divisor = 39
    thur_atom = budatom_shop(bud_item_reason_premiseunit_str(), atom_insert())
    thur_atom.set_arg(road_str(), clean_road)
    thur_atom.set_arg(base_str(), week_road)
    thur_atom.set_arg("need", thur_road)
    assert thur_atom.is_valid()
    thur_atom.set_arg("divisor", thur_divisor)
    thur_jkeys = thur_atom.get_jkeys_dict()
    thur_premiseunit = premiseunit_get_obj(sue_bud, thur_jkeys)
    assert thur_premiseunit.divisor != thur_divisor
    assert thur_premiseunit.divisor is None

    # WHEN
    new_zia_budatom = sift_budatom(sue_bud, thur_atom)

    # THEN
    assert new_zia_budatom
    assert new_zia_budatom.crud_str == atom_update()
    assert new_zia_budatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_budatom.get_jvalues_dict()
    assert zia_jvalues.get("divisor") == thur_divisor


def test_sift_atom_ReturnsObj_BudAtom_UPDATE_bud_item_factunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_str = "week"
    week_road = sue_bud.make_l1_road(casa_str)
    sue_bud.add_item(casa_road)
    sue_bud.get_item_obj(casa_road).set_factunit(factunit_shop(week_road))

    casa_fopen = 32
    casa_atom = budatom_shop(bud_item_factunit_str(), atom_insert())
    casa_atom.set_arg(road_str(), casa_road)
    casa_atom.set_arg(base_str(), week_road)
    casa_atom.set_arg(fopen_str(), casa_fopen)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_factunit = bud_item_factunit_get_obj(sue_bud, casa_jkeys)
    assert casa_factunit.fopen != casa_fopen
    assert casa_factunit.fopen is None

    # WHEN
    new_zia_budatom = sift_budatom(sue_bud, casa_atom)

    # THEN
    assert new_zia_budatom
    assert new_zia_budatom.crud_str == atom_update()
    assert new_zia_budatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_budatom.get_jvalues_dict()
    assert zia_jvalues.get(fopen_str()) == casa_fopen
