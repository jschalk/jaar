from src.a00_data_toolbox.dict_toolbox import (
    get_from_nested_dict,
    get_empty_list_if_None,
)
from src.a03_group_logic.acct import acctunit_shop
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._test_util.a06_str import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_conceptunit_str,
    bud_concept_awardlink_str,
    bud_concept_reasonunit_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_laborlink_str,
    bud_concept_healerlink_str,
    bud_concept_factunit_str,
    acct_name_str,
    awardee_title_str,
    group_title_str,
    concept_way_str,
    labor_title_str,
    healer_name_str,
    pledge_str,
    begin_str,
    close_str,
    mass_str,
    fcontext_str,
    fstate_str,
    fnigh_str,
    fopen_str,
    rcontext_concept_active_requisite_str,
    give_force_str,
    take_force_str,
)
from src.a06_bud_logic._test_util.example_buds import get_budunit_with_4_levels
from src.a08_bud_atom_logic.atom import atom_insert, atom_update, atom_delete
from src.a09_pack_logic.delta import BudDelta, buddelta_shop
from copy import deepcopy as copy_deepcopy


def print_budatom_keys(x_buddelta: BudDelta):
    for x_budatom in get_delete_budatom_list(x_buddelta):
        print(f"DELETE {x_budatom.dimen} {list(x_budatom.jkeys.values())}")
    for x_budatom in get_update_budatom_list(x_buddelta):
        print(f"UPDATE {x_budatom.dimen} {list(x_budatom.jkeys.values())}")
    for x_budatom in get_insert_budatom_list(x_buddelta):
        print(f"INSERT {x_budatom.dimen} {list(x_budatom.jkeys.values())}")


def get_delete_budatom_list(x_buddelta: BudDelta) -> list:
    return get_empty_list_if_None(
        x_buddelta._get_crud_budatoms_list().get(atom_delete())
    )


def get_insert_budatom_list(x_buddelta: BudDelta):
    return get_empty_list_if_None(
        x_buddelta._get_crud_budatoms_list().get(atom_insert())
    )


def get_update_budatom_list(x_buddelta: BudDelta):
    return get_empty_list_if_None(
        x_buddelta._get_crud_budatoms_list().get(atom_update())
    )


def get_budatom_total_count(x_buddelta: BudDelta) -> int:
    return (
        len(get_delete_budatom_list(x_buddelta))
        + len(get_insert_budatom_list(x_buddelta))
        + len(get_update_budatom_list(x_buddelta))
    )


def test_BudDelta_create_budatoms_EmptyBuds():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_buddelta = buddelta_shop()
    assert sue_buddelta.budatoms == {}

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(sue_bud, sue_bud)

    # THEN
    assert sue_buddelta.budatoms == {}


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_acctunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    xio_str = "Xio"
    xio_credit_belief = 33
    xio_debtit_belief = 44
    xio_acctunit = acctunit_shop(xio_str, xio_credit_belief, xio_debtit_belief)
    after_sue_bud.set_acctunit(xio_acctunit, auto_set_membership=False)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    assert len(sue_buddelta.budatoms.get(atom_insert()).get(bud_acctunit_str())) == 1
    sue_insert_dict = sue_buddelta.budatoms.get(atom_insert())
    sue_acctunit_dict = sue_insert_dict.get(bud_acctunit_str())
    xio_budatom = sue_acctunit_dict.get(xio_str)
    assert xio_budatom.get_value(acct_name_str()) == xio_str
    assert xio_budatom.get_value("credit_belief") == xio_credit_belief
    assert xio_budatom.get_value("debtit_belief") == xio_debtit_belief

    print(f"{get_budatom_total_count(sue_buddelta)=}")
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_acctunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    before_sue_bud.add_acctunit("Yao")
    before_sue_bud.add_acctunit("Zia")

    after_sue_bud = copy_deepcopy(before_sue_bud)

    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    xio_budatom = get_from_nested_dict(
        sue_buddelta.budatoms, [atom_delete(), bud_acctunit_str(), xio_str]
    )
    assert xio_budatom.get_value(acct_name_str()) == xio_str

    print(f"{get_budatom_total_count(sue_buddelta)=}")
    print_budatom_keys(sue_buddelta)
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_acctunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    xio_credit_belief = 33
    xio_debtit_belief = 44
    after_sue_bud.add_acctunit(xio_str, xio_credit_belief, xio_debtit_belief)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    x_keylist = [atom_update(), bud_acctunit_str(), xio_str]
    xio_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert xio_budatom.get_value(acct_name_str()) == xio_str
    assert xio_budatom.get_value("credit_belief") == xio_credit_belief
    assert xio_budatom.get_value("debtit_belief") == xio_debtit_belief

    print(f"{get_budatom_total_count(sue_buddelta)=}")
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_BudUnit_simple_attrs_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    x_budunit_tally = 55
    x_fund_pool = 8000000
    x_fund_coin = 8
    x_respect_bit = 5
    x_max_tree_traverse = 66
    x_credor_respect = 770
    x_debtor_respect = 880
    after_sue_bud.tally = x_budunit_tally
    after_sue_bud.fund_pool = x_fund_pool
    after_sue_bud.fund_coin = x_fund_coin
    after_sue_bud.respect_bit = x_respect_bit
    after_sue_bud.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_bud.set_credor_respect(x_credor_respect)
    after_sue_bud.set_debtor_respect(x_debtor_respect)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    x_keylist = [atom_update(), budunit_str()]
    xio_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert xio_budatom.get_value("max_tree_traverse") == x_max_tree_traverse
    assert xio_budatom.get_value("credor_respect") == x_credor_respect
    assert xio_budatom.get_value("debtor_respect") == x_debtor_respect
    assert xio_budatom.get_value("tally") == x_budunit_tally
    assert xio_budatom.get_value("fund_pool") == x_fund_pool
    assert xio_budatom.get_value("fund_coin") == x_fund_coin
    assert xio_budatom.get_value("respect_bit") == x_respect_bit

    print(f"{get_budatom_total_count(sue_buddelta)=}")
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_acct_membership_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    yao_str = "Yao"
    zia_str = "Zia"
    temp_yao_acctunit = acctunit_shop(yao_str)
    temp_zia_acctunit = acctunit_shop(zia_str)
    after_sue_bud.set_acctunit(temp_yao_acctunit, auto_set_membership=False)
    after_sue_bud.set_acctunit(temp_zia_acctunit, auto_set_membership=False)
    after_yao_acctunit = after_sue_bud.get_acct(yao_str)
    after_zia_acctunit = after_sue_bud.get_acct(zia_str)
    run_str = ";runners"
    zia_run_credit_w = 77
    zia_run_debtit_w = 88
    after_zia_acctunit.add_membership(run_str, zia_run_credit_w, zia_run_debtit_w)
    print(f"{after_sue_bud.get_acctunit_group_titles_dict()=}")

    # WHEN
    sue_buddelta = buddelta_shop()
    print(f"{after_sue_bud.get_acct(zia_str)._memberships=}")
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)
    # print(f"{sue_buddelta.budatoms.get(atom_insert()).keys()=}")
    # print(
    #     sue_buddelta.budatoms.get(atom_insert()).get(bud_acct_membership_str()).keys()
    # )

    # THEN
    x_keylist = [atom_insert(), bud_acctunit_str(), yao_str]
    yao_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert yao_budatom.get_value(acct_name_str()) == yao_str

    x_keylist = [atom_insert(), bud_acctunit_str(), zia_str]
    zia_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert zia_budatom.get_value(acct_name_str()) == zia_str
    print(f"\n{sue_buddelta.budatoms=}")
    # print(f"\n{zia_budatom=}")

    x_keylist = [atom_insert(), bud_acct_membership_str(), zia_str, run_str]
    run_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert run_budatom.get_value(acct_name_str()) == zia_str
    assert run_budatom.get_value(group_title_str()) == run_str
    assert run_budatom.get_value("credit_vote") == zia_run_credit_w
    assert run_budatom.get_value("debtit_vote") == zia_run_debtit_w

    print_budatom_keys(sue_buddelta)
    print(f"{get_budatom_total_count(sue_buddelta)=}")
    assert len(get_delete_budatom_list(sue_buddelta)) == 0
    assert len(get_insert_budatom_list(sue_buddelta)) == 3
    assert len(get_delete_budatom_list(sue_buddelta)) == 0
    assert get_budatom_total_count(sue_buddelta) == 3


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_acct_membership_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    before_sue_bud.add_acctunit(xio_str)
    before_sue_bud.add_acctunit(zia_str)
    run_str = ";runners"
    before_xio_credit_w = 77
    before_xio_debtit_w = 88
    before_xio_acct = before_sue_bud.get_acct(xio_str)
    before_xio_acct.add_membership(run_str, before_xio_credit_w, before_xio_debtit_w)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_xio_acctunit = after_sue_bud.get_acct(xio_str)
    after_xio_credit_w = 55
    after_xio_debtit_w = 66
    after_xio_acctunit.add_membership(run_str, after_xio_credit_w, after_xio_debtit_w)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    # x_keylist = [atom_update(), bud_acctunit_str(), xio_str]
    # xio_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    # assert xio_budatom.get_value(acct_name_str()) == xio_str
    # print(f"\n{sue_buddelta.budatoms=}")
    # print(f"\n{xio_budatom=}")

    x_keylist = [atom_update(), bud_acct_membership_str(), xio_str, run_str]
    xio_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert xio_budatom.get_value(acct_name_str()) == xio_str
    assert xio_budatom.get_value(group_title_str()) == run_str
    assert xio_budatom.get_value("credit_vote") == after_xio_credit_w
    assert xio_budatom.get_value("debtit_vote") == after_xio_debtit_w

    print(f"{get_budatom_total_count(sue_buddelta)=}")
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_acct_membership_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_bud.add_acctunit(xio_str)
    before_sue_bud.add_acctunit(zia_str)
    before_sue_bud.add_acctunit(bob_str)
    before_xio_acctunit = before_sue_bud.get_acct(xio_str)
    before_zia_acctunit = before_sue_bud.get_acct(zia_str)
    before_bob_acctunit = before_sue_bud.get_acct(bob_str)
    run_str = ";runners"
    before_xio_acctunit.add_membership(run_str)
    before_zia_acctunit.add_membership(run_str)
    fly_str = ";flyers"
    before_xio_acctunit.add_membership(fly_str)
    before_zia_acctunit.add_membership(fly_str)
    before_bob_acctunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_bud.get_acctunit_group_titles_dict()

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_xio_acctunit = after_sue_bud.get_acct(xio_str)
    after_zia_acctunit = after_sue_bud.get_acct(zia_str)
    after_bob_acctunit = after_sue_bud.get_acct(bob_str)
    after_xio_acctunit.delete_membership(run_str)
    after_zia_acctunit.delete_membership(run_str)
    after_bob_acctunit.delete_membership(fly_str)
    after_group_titles_dict = after_sue_bud.get_acctunit_group_titles_dict()
    assert len(before_group_titles_dict.get(fly_str)) == 3
    assert len(before_group_titles_dict.get(run_str)) == 2
    assert len(after_group_titles_dict.get(fly_str)) == 2
    assert after_group_titles_dict.get(run_str) is None

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    x_keylist = [atom_delete(), bud_acct_membership_str(), bob_str, fly_str]
    xio_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert xio_budatom.get_value(acct_name_str()) == bob_str
    assert xio_budatom.get_value(group_title_str()) == fly_str

    print(f"{get_budatom_total_count(sue_buddelta)=}")
    print_budatom_keys(sue_buddelta)
    assert len(get_delete_budatom_list(sue_buddelta)) == 3
    assert len(get_insert_budatom_list(sue_buddelta)) == 0
    assert len(get_update_budatom_list(sue_buddelta)) == 0
    assert get_budatom_total_count(sue_buddelta) == 3


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    street_str = "street ball"
    street_way = before_sue_bud.make_way(ball_way, street_str)
    before_sue_bud.set_concept(conceptunit_shop(street_str), ball_way)
    disc_str = "Ultimate Disc"
    disc_way = before_sue_bud.make_way(sports_way, disc_str)
    accord45_str = "accord45"
    before_sue_bud.set_l1_concept(conceptunit_shop(accord45_str))
    before_sue_bud.set_concept(conceptunit_shop(disc_str), sports_way)
    # create after without ball_concept and street_concept
    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_sue_bud.del_concept_obj(ball_way)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    x_dimen = bud_conceptunit_str()
    print(f"{sue_buddelta.budatoms.get(atom_delete()).get(x_dimen).keys()=}")

    x_keylist = [atom_delete(), bud_conceptunit_str(), street_way]
    street_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert street_budatom.get_value(concept_way_str()) == street_way

    x_keylist = [atom_delete(), bud_conceptunit_str(), ball_way]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way

    print(f"{get_budatom_total_count(sue_buddelta)=}")
    assert get_budatom_total_count(sue_buddelta) == 2


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    street_str = "street ball"
    street_way = before_sue_bud.make_way(ball_way, street_str)
    before_sue_bud.set_concept(conceptunit_shop(street_str), ball_way)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    disc_str = "Ultimate Disc"
    disc_way = after_sue_bud.make_way(sports_way, disc_str)
    after_sue_bud.set_concept(conceptunit_shop(disc_str), sports_way)
    accord45_str = "accord45"
    accord_begin = 34
    accord_close = 78
    accord_mass = 55
    accord_pledge = True
    accord_way = after_sue_bud.make_l1_way(accord45_str)
    after_sue_bud.set_l1_concept(
        conceptunit_shop(
            accord45_str,
            begin=accord_begin,
            close=accord_close,
            mass=accord_mass,
            pledge=accord_pledge,
        )
    )

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print_budatom_keys(sue_buddelta)

    x_keylist = [atom_insert(), bud_conceptunit_str(), disc_way]
    street_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert street_budatom.get_value(concept_way_str()) == disc_way

    a45_way = after_sue_bud.make_l1_way(accord45_str)
    x_keylist = [atom_insert(), bud_conceptunit_str(), a45_way]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == a45_way
    assert ball_budatom.get_value(begin_str()) == accord_begin
    assert ball_budatom.get_value(close_str()) == accord_close
    assert ball_budatom.get_value(mass_str()) == accord_mass
    assert ball_budatom.get_value(pledge_str()) == accord_pledge

    assert get_budatom_total_count(sue_buddelta) == 2


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    accord45_str = "accord45"
    accord45_way = before_sue_bud.make_l1_way(accord45_str)
    before_accord_begin = 34
    before_accord_close = 78
    before_accord_mass = 55
    before_accord_pledge = True
    accord_way = before_sue_bud.make_l1_way(accord45_str)
    before_sue_bud.set_l1_concept(
        conceptunit_shop(
            accord45_str,
            begin=before_accord_begin,
            close=before_accord_close,
            mass=before_accord_mass,
            pledge=before_accord_pledge,
        )
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_accord_begin = 99
    after_accord_close = 111
    after_accord_mass = 22
    after_accord_pledge = False
    after_sue_bud.edit_concept_attr(
        accord_way,
        begin=after_accord_begin,
        close=after_accord_close,
        mass=after_accord_mass,
        pledge=after_accord_pledge,
    )

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print_budatom_keys(sue_buddelta)

    x_keylist = [atom_update(), bud_conceptunit_str(), accord45_way]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == accord45_way
    assert ball_budatom.get_value(begin_str()) == after_accord_begin
    assert ball_budatom.get_value(close_str()) == after_accord_close
    assert ball_budatom.get_value(mass_str()) == after_accord_mass
    assert ball_budatom.get_value(pledge_str()) == after_accord_pledge

    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_awardlink_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_au.add_acctunit(xio_str)
    before_sue_au.add_acctunit(zia_str)
    before_sue_au.add_acctunit(bob_str)
    xio_acctunit = before_sue_au.get_acct(xio_str)
    zia_acctunit = before_sue_au.get_acct(zia_str)
    bob_acctunit = before_sue_au.get_acct(bob_str)
    run_str = ";runners"
    xio_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    fly_str = ";flyers"
    xio_acctunit.add_membership(fly_str)
    zia_acctunit.add_membership(fly_str)
    bob_acctunit.add_membership(fly_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    disc_str = "Ultimate Disc"
    disc_way = before_sue_au.make_way(sports_way, disc_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    before_sue_au.set_concept(conceptunit_shop(disc_str), sports_way)
    before_sue_au.edit_concept_attr(ball_way, awardlink=awardlink_shop(run_str))
    before_sue_au.edit_concept_attr(ball_way, awardlink=awardlink_shop(fly_str))
    before_sue_au.edit_concept_attr(disc_way, awardlink=awardlink_shop(run_str))
    before_sue_au.edit_concept_attr(disc_way, awardlink=awardlink_shop(fly_str))

    after_sue_bud = copy_deepcopy(before_sue_au)
    after_sue_bud.edit_concept_attr(disc_way, awardlink_del=run_str)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_au, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")

    x_keylist = [atom_delete(), bud_concept_awardlink_str(), disc_way, run_str]
    run_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert run_budatom.get_value(concept_way_str()) == disc_way
    assert run_budatom.get_value(awardee_title_str()) == run_str

    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_awardlink_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_au.add_acctunit(xio_str)
    before_sue_au.add_acctunit(zia_str)
    before_sue_au.add_acctunit(bob_str)
    xio_acctunit = before_sue_au.get_acct(xio_str)
    zia_acctunit = before_sue_au.get_acct(zia_str)
    bob_acctunit = before_sue_au.get_acct(bob_str)
    run_str = ";runners"
    xio_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    fly_str = ";flyers"
    xio_acctunit.add_membership(fly_str)
    zia_acctunit.add_membership(fly_str)
    bob_acctunit.add_membership(fly_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    disc_str = "Ultimate Disc"
    disc_way = before_sue_au.make_way(sports_way, disc_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    before_sue_au.set_concept(conceptunit_shop(disc_str), sports_way)
    before_sue_au.edit_concept_attr(ball_way, awardlink=awardlink_shop(run_str))
    before_sue_au.edit_concept_attr(disc_way, awardlink=awardlink_shop(fly_str))
    after_sue_au = copy_deepcopy(before_sue_au)
    after_sue_au.edit_concept_attr(ball_way, awardlink=awardlink_shop(fly_str))
    after_run_give_force = 44
    after_run_take_force = 66
    x_awardlink = awardlink_shop(run_str, after_run_give_force, after_run_take_force)
    after_sue_au.edit_concept_attr(disc_way, awardlink=x_awardlink)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")

    x_keylist = [atom_insert(), bud_concept_awardlink_str(), disc_way, run_str]
    run_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert run_budatom.get_value(concept_way_str()) == disc_way
    assert run_budatom.get_value(awardee_title_str()) == run_str
    assert run_budatom.get_value(concept_way_str()) == disc_way
    assert run_budatom.get_value(awardee_title_str()) == run_str
    assert run_budatom.get_value(give_force_str()) == after_run_give_force
    assert run_budatom.get_value(take_force_str()) == after_run_take_force

    assert get_budatom_total_count(sue_buddelta) == 2


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_awardlink_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = budunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    before_sue_au.add_acctunit(xio_str)
    before_sue_au.add_acctunit(zia_str)
    xio_acctunit = before_sue_au.get_acct(xio_str)
    run_str = ";runners"
    xio_acctunit.add_membership(run_str)
    sports_str = "sports"
    sports_way = before_sue_au.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_au.make_way(sports_way, ball_str)
    before_sue_au.set_concept(conceptunit_shop(ball_str), sports_way)
    before_sue_au.edit_concept_attr(ball_way, awardlink=awardlink_shop(run_str))
    run_awardlink = before_sue_au.get_concept_obj(ball_way).awardlinks.get(run_str)

    after_sue_bud = copy_deepcopy(before_sue_au)
    after_give_force = 55
    after_take_force = 66
    after_sue_bud.edit_concept_attr(
        ball_way,
        awardlink=awardlink_shop(
            awardee_title=run_str,
            give_force=after_give_force,
            take_force=after_take_force,
        ),
    )
    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_au, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")

    x_keylist = [atom_update(), bud_concept_awardlink_str(), ball_way, run_str]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(awardee_title_str()) == run_str
    assert ball_budatom.get_value(give_force_str()) == after_give_force
    assert ball_budatom.get_value(take_force_str()) == after_take_force
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_factunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_bud.make_l1_way(knee_str)
    bend_str = "bendable"
    bend_way = before_sue_bud.make_way(knee_way, bend_str)
    before_sue_bud.set_concept(conceptunit_shop(bend_str), knee_way)
    damaged_str = "damaged mcl"
    damaged_way = before_sue_bud.make_way(knee_way, damaged_str)
    before_sue_bud.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_bud.set_concept(conceptunit_shop(damaged_str), knee_way)
    before_fopen = 11
    before_fnigh = 22
    before_fact = factunit_shop(knee_way, bend_way, before_fopen, before_fnigh)
    before_sue_bud.edit_concept_attr(ball_way, factunit=before_fact)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_fopen = 55
    after_fnigh = 66
    knee_fact = factunit_shop(knee_way, damaged_way, after_fopen, after_fnigh)
    after_sue_bud.edit_concept_attr(ball_way, factunit=knee_fact)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")

    x_keylist = [atom_update(), bud_concept_factunit_str(), ball_way, knee_way]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(fcontext_str()) == knee_way
    assert ball_budatom.get_value(fstate_str()) == damaged_way
    assert ball_budatom.get_value(fopen_str()) == after_fopen
    assert ball_budatom.get_value(fnigh_str()) == after_fnigh
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_factunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_bud.make_l1_way(knee_str)
    damaged_str = "damaged mcl"
    damaged_way = before_sue_bud.make_way(knee_way, damaged_str)
    before_sue_bud.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_bud.set_concept(conceptunit_shop(damaged_str), knee_way)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_fopen = 55
    after_fnigh = 66
    after_fact = factunit_shop(knee_way, damaged_way, after_fopen, after_fnigh)
    after_sue_bud.edit_concept_attr(ball_way, factunit=after_fact)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [atom_insert(), bud_concept_factunit_str(), ball_way, knee_way]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    print(f"{ball_budatom=}")
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(fcontext_str()) == knee_way
    assert ball_budatom.get_value(fstate_str()) == damaged_way
    assert ball_budatom.get_value(fopen_str()) == after_fopen
    assert ball_budatom.get_value(fnigh_str()) == after_fnigh
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_factunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_bud.make_l1_way(knee_str)
    damaged_str = "damaged mcl"
    damaged_way = before_sue_bud.make_way(knee_way, damaged_str)
    before_sue_bud.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_bud.set_concept(conceptunit_shop(damaged_str), knee_way)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    before_damaged_popen = 55
    before_damaged_pnigh = 66
    before_fact = factunit_shop(
        fcontext=knee_way,
        fstate=damaged_way,
        fopen=before_damaged_popen,
        fnigh=before_damaged_pnigh,
    )
    before_sue_bud.edit_concept_attr(ball_way, factunit=before_fact)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [atom_delete(), bud_concept_factunit_str(), ball_way, knee_way]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(fcontext_str()) == knee_way
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_reason_premiseunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_bud.make_l1_way(knee_str)
    before_sue_bud.set_l1_concept(conceptunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_way = before_sue_bud.make_way(knee_way, damaged_str)
    before_sue_bud.set_concept(conceptunit_shop(damaged_str), knee_way)
    bend_str = "bend"
    bend_way = before_sue_bud.make_way(knee_way, bend_str)
    before_sue_bud.set_concept(conceptunit_shop(bend_str), knee_way)
    before_sue_bud.edit_concept_attr(
        ball_way, reason_rcontext=knee_way, reason_premise=bend_way
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    damaged_popen = 45
    damaged_pnigh = 77
    damaged_pdivisor = 3
    after_sue_bud.edit_concept_attr(
        ball_way,
        reason_rcontext=knee_way,
        reason_premise=damaged_way,
        popen=damaged_popen,
        reason_pnigh=damaged_pnigh,
        pdivisor=damaged_pdivisor,
    )

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_insert(),
        bud_concept_reason_premiseunit_str(),
        ball_way,
        knee_way,
        damaged_way,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value("rcontext") == knee_way
    assert ball_budatom.get_value("pstate") == damaged_way
    assert ball_budatom.get_value("popen") == damaged_popen
    assert ball_budatom.get_value("pnigh") == damaged_pnigh
    assert ball_budatom.get_value("pdivisor") == damaged_pdivisor
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_reason_premiseunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_bud.make_l1_way(knee_str)
    before_sue_bud.set_l1_concept(conceptunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_way = before_sue_bud.make_way(knee_way, damaged_str)
    before_sue_bud.set_concept(conceptunit_shop(damaged_str), knee_way)
    bend_str = "bend"
    bend_way = before_sue_bud.make_way(knee_way, bend_str)
    before_sue_bud.set_concept(conceptunit_shop(bend_str), knee_way)
    before_sue_bud.edit_concept_attr(
        ball_way, reason_rcontext=knee_way, reason_premise=bend_way
    )
    damaged_popen = 45
    damaged_pnigh = 77
    damaged_pdivisor = 3
    before_sue_bud.edit_concept_attr(
        ball_way,
        reason_rcontext=knee_way,
        reason_premise=damaged_way,
        popen=damaged_popen,
        reason_pnigh=damaged_pnigh,
        pdivisor=damaged_pdivisor,
    )
    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_sue_bud.edit_concept_attr(
        ball_way,
        reason_del_premise_rcontext=knee_way,
        reason_del_premise_pstate=damaged_way,
    )

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_delete(),
        bud_concept_reason_premiseunit_str(),
        ball_way,
        knee_way,
        damaged_way,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value("rcontext") == knee_way
    assert ball_budatom.get_value("pstate") == damaged_way
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_reason_premiseunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_bud.make_l1_way(knee_str)
    before_sue_bud.set_l1_concept(conceptunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_way = before_sue_bud.make_way(knee_way, damaged_str)
    before_sue_bud.set_concept(conceptunit_shop(damaged_str), knee_way)
    bend_str = "bend"
    bend_way = before_sue_bud.make_way(knee_way, bend_str)
    before_sue_bud.set_concept(conceptunit_shop(bend_str), knee_way)
    before_sue_bud.edit_concept_attr(
        ball_way, reason_rcontext=knee_way, reason_premise=bend_way
    )
    before_damaged_popen = 111
    before_damaged_pnigh = 777
    before_damaged_pdivisor = 13
    before_sue_bud.edit_concept_attr(
        ball_way,
        reason_rcontext=knee_way,
        reason_premise=damaged_way,
        popen=before_damaged_popen,
        reason_pnigh=before_damaged_pnigh,
        pdivisor=before_damaged_pdivisor,
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_damaged_popen = 333
    after_damaged_pnigh = 555
    after_damaged_pdivisor = 78
    after_sue_bud.edit_concept_attr(
        ball_way,
        reason_rcontext=knee_way,
        reason_premise=damaged_way,
        popen=after_damaged_popen,
        reason_pnigh=after_damaged_pnigh,
        pdivisor=after_damaged_pdivisor,
    )

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_update(),
        bud_concept_reason_premiseunit_str(),
        ball_way,
        knee_way,
        damaged_way,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value("rcontext") == knee_way
    assert ball_budatom.get_value("pstate") == damaged_way
    assert ball_budatom.get_value("popen") == after_damaged_popen
    assert ball_budatom.get_value("pnigh") == after_damaged_pnigh
    assert ball_budatom.get_value("pdivisor") == after_damaged_pdivisor
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_reasonunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_bud.make_l1_way(knee_str)
    medical_str = "get medical attention"
    medical_way = before_sue_bud.make_way(knee_way, medical_str)
    before_sue_bud.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_bud.set_concept(conceptunit_shop(medical_str), knee_way)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_medical_rcontext_concept_active_requisite = False
    after_sue_bud.edit_concept_attr(
        ball_way,
        reason_rcontext=medical_way,
        reason_rcontext_concept_active_requisite=after_medical_rcontext_concept_active_requisite,
    )

    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_insert(),
        bud_concept_reasonunit_str(),
        ball_way,
        medical_way,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value("rcontext") == medical_way
    assert (
        ball_budatom.get_value(rcontext_concept_active_requisite_str())
        == after_medical_rcontext_concept_active_requisite
    )
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_reasonunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_bud.make_l1_way(knee_str)
    medical_str = "get medical attention"
    medical_way = before_sue_bud.make_way(knee_way, medical_str)
    before_sue_bud.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_bud.set_concept(conceptunit_shop(medical_str), knee_way)
    before_medical_rcontext_concept_active_requisite = True
    before_sue_bud.edit_concept_attr(
        ball_way,
        reason_rcontext=medical_way,
        reason_rcontext_concept_active_requisite=before_medical_rcontext_concept_active_requisite,
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_medical_rcontext_concept_active_requisite = False
    after_sue_bud.edit_concept_attr(
        ball_way,
        reason_rcontext=medical_way,
        reason_rcontext_concept_active_requisite=after_medical_rcontext_concept_active_requisite,
    )

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_update(),
        bud_concept_reasonunit_str(),
        ball_way,
        medical_way,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value("rcontext") == medical_way
    assert (
        ball_budatom.get_value(rcontext_concept_active_requisite_str())
        == after_medical_rcontext_concept_active_requisite
    )
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_reasonunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    knee_str = "knee"
    knee_way = before_sue_bud.make_l1_way(knee_str)
    medical_str = "get medical attention"
    medical_way = before_sue_bud.make_way(knee_way, medical_str)
    before_sue_bud.set_l1_concept(conceptunit_shop(knee_str))
    before_sue_bud.set_concept(conceptunit_shop(medical_str), knee_way)
    before_medical_rcontext_concept_active_requisite = True
    before_sue_bud.edit_concept_attr(
        ball_way,
        reason_rcontext=medical_way,
        reason_rcontext_concept_active_requisite=before_medical_rcontext_concept_active_requisite,
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_concept = after_sue_bud.get_concept_obj(ball_way)
    after_ball_concept.del_reasonunit_rcontext(medical_way)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_delete(),
        bud_concept_reasonunit_str(),
        ball_way,
        medical_way,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value("rcontext") == medical_way
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_laborlink_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_conceptunit = after_sue_bud.get_concept_obj(ball_way)
    after_ball_conceptunit.laborunit.set_laborlink(xio_str)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_insert(),
        bud_concept_laborlink_str(),
        ball_way,
        xio_str,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(labor_title_str()) == xio_str
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_laborlink_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    before_ball_conceptunit = before_sue_bud.get_concept_obj(ball_way)
    before_ball_conceptunit.laborunit.set_laborlink(xio_str)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_conceptunit = after_sue_bud.get_concept_obj(ball_way)
    after_ball_conceptunit.laborunit.del_laborlink(xio_str)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_delete(),
        bud_concept_laborlink_str(),
        ball_way,
        xio_str,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(labor_title_str()) == xio_str
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_healerlink_insert_ConceptUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_conceptunit = after_sue_bud.get_concept_obj(ball_way)
    after_ball_conceptunit.healerlink.set_healer_name(xio_str)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_insert(),
        bud_concept_healerlink_str(),
        ball_way,
        xio_str,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist)
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(healer_name_str()) == xio_str
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_healerlink_insert_ConceptUnitInsert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    after_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    after_ball_conceptunit = after_sue_bud.get_concept_obj(ball_way)
    after_ball_conceptunit.healerlink.set_healer_name(xio_str)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_insert(),
        bud_concept_healerlink_str(),
        ball_way,
        xio_str,
    ]
    ball_budatom = get_from_nested_dict(sue_buddelta.budatoms, x_keylist, True)
    assert ball_budatom
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(healer_name_str()) == xio_str
    assert get_budatom_total_count(sue_buddelta) == 3


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_healerlink_delete_ConceptUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    before_ball_conceptunit = before_sue_bud.get_concept_obj(ball_way)
    before_ball_conceptunit.healerlink.set_healer_name(xio_str)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_conceptunit = after_sue_bud.get_concept_obj(ball_way)
    after_ball_conceptunit.healerlink.del_healer_name(xio_str)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_delete(),
        bud_concept_healerlink_str(),
        ball_way,
        xio_str,
    ]
    ball_budatom = get_from_nested_dict(
        sue_buddelta.budatoms, x_keylist, if_missing_return_None=True
    )
    assert ball_budatom
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(healer_name_str()) == xio_str
    assert get_budatom_total_count(sue_buddelta) == 1


def test_BudDelta_add_all_different_budatoms_Creates_BudAtom_concept_healerlink_delete_ConceptUnitDelete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_way = before_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = before_sue_bud.make_way(sports_way, ball_str)
    before_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    before_ball_conceptunit = before_sue_bud.get_concept_obj(ball_way)
    before_ball_conceptunit.healerlink.set_healer_name(xio_str)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_sue_bud.del_concept_obj(ball_way)

    # WHEN
    sue_buddelta = buddelta_shop()
    sue_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_budatom_keys(sue_buddelta)=}")
    x_keylist = [
        atom_delete(),
        bud_concept_healerlink_str(),
        ball_way,
        xio_str,
    ]
    ball_budatom = get_from_nested_dict(
        sue_buddelta.budatoms, x_keylist, if_missing_return_None=True
    )
    assert ball_budatom
    assert ball_budatom.get_value(concept_way_str()) == ball_way
    assert ball_budatom.get_value(healer_name_str()) == xio_str
    assert get_budatom_total_count(sue_buddelta) == 2


def test_BudDelta_add_all_budatoms_CorrectlyCreates_BudAtoms():
    # ESTABLISH
    sue_str = "Sue"

    after_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    temp_xio_acctunit = acctunit_shop(xio_str)
    after_sue_bud.set_acctunit(temp_xio_acctunit, auto_set_membership=False)
    sports_str = "sports"
    sports_way = after_sue_bud.make_l1_way(sports_str)
    ball_str = "basketball"
    ball_way = after_sue_bud.make_way(sports_way, ball_str)
    after_sue_bud.set_concept(conceptunit_shop(ball_str), sports_way)
    after_ball_conceptunit = after_sue_bud.get_concept_obj(ball_way)
    after_ball_conceptunit.laborunit.set_laborlink(xio_str)

    before_sue_bud = budunit_shop(sue_str)
    sue1_buddelta = buddelta_shop()
    sue1_buddelta.add_all_different_budatoms(before_sue_bud, after_sue_bud)
    print(f"{sue1_buddelta.get_ordered_budatoms()}")
    assert len(sue1_buddelta.get_ordered_budatoms()) == 4

    # WHEN
    sue2_buddelta = buddelta_shop()
    sue2_buddelta.add_all_budatoms(after_sue_bud)

    # THEN
    assert len(sue2_buddelta.get_ordered_budatoms()) == 4
    assert sue2_buddelta == sue1_buddelta
