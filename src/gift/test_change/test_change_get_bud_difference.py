from src.bud.acct import acctunit_shop
from src.bud.group import awardlink_shop
from src.bud.idea import ideaunit_shop
from src.bud.reason_idea import factunit_shop
from src.bud.bud import budunit_shop
from src.bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
)
from src.gift.atom_config import (
    acct_id_str,
    group_id_str,
    healer_id_str,
    parent_road_str,
    label_str,
    pledge_str,
    begin_str,
    close_str,
    mass_str,
    fopen_str,
    fnigh_str,
    base_idea_active_requisite_str,
)
from src.gift.atom import atom_insert, atom_update, atom_delete
from src.gift.change import ChangeUnit, changeunit_shop
from src.listen.examples.example_listen_buds import get_budunit_with_4_levels
from src._instrument.python_tool import get_nested_value, get_empty_list_if_None
from copy import deepcopy as copy_deepcopy


def print_atomunit_keys(x_changeunit: ChangeUnit):
    for x_atomunit in get_delete_atomunit_list(x_changeunit):
        print(f"DELETE {x_atomunit.category} {list(x_atomunit.required_args.values())}")
    for x_atomunit in get_update_atomunit_list(x_changeunit):
        print(f"UPDATE {x_atomunit.category} {list(x_atomunit.required_args.values())}")
    for x_atomunit in get_insert_atomunit_list(x_changeunit):
        print(f"INSERT {x_atomunit.category} {list(x_atomunit.required_args.values())}")


def get_delete_atomunit_list(x_changeunit: ChangeUnit) -> list:
    return get_empty_list_if_None(
        x_changeunit._get_crud_atomunits_list().get(atom_delete())
    )


def get_insert_atomunit_list(x_changeunit: ChangeUnit):
    return get_empty_list_if_None(
        x_changeunit._get_crud_atomunits_list().get(atom_insert())
    )


def get_update_atomunit_list(x_changeunit: ChangeUnit):
    return get_empty_list_if_None(
        x_changeunit._get_crud_atomunits_list().get(atom_update())
    )


def get_atomunit_total_count(x_changeunit: ChangeUnit) -> int:
    return (
        len(get_delete_atomunit_list(x_changeunit))
        + len(get_insert_atomunit_list(x_changeunit))
        + len(get_update_atomunit_list(x_changeunit))
    )


def test_ChangeUnit_create_atomunits_CorrectHandlesEmptyBuds():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_changeunit = changeunit_shop()
    assert sue_changeunit.atomunits == {}

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(sue_bud, sue_bud)

    # THEN
    assert sue_changeunit.atomunits == {}


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_acctunit_insert():
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
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    assert len(sue_changeunit.atomunits.get(atom_insert()).get(bud_acctunit_str())) == 1
    sue_insert_dict = sue_changeunit.atomunits.get(atom_insert())
    sue_acctunit_dict = sue_insert_dict.get(bud_acctunit_str())
    xio_atomunit = sue_acctunit_dict.get(xio_str)
    assert xio_atomunit.get_value(acct_id_str()) == xio_str
    assert xio_atomunit.get_value("credit_belief") == xio_credit_belief
    assert xio_atomunit.get_value("debtit_belief") == xio_debtit_belief

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_acctunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    before_sue_bud.add_acctunit("Yao")
    before_sue_bud.add_acctunit("Zia")

    after_sue_bud = copy_deepcopy(before_sue_bud)

    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    xio_atomunit = get_nested_value(
        sue_changeunit.atomunits, [atom_delete(), bud_acctunit_str(), xio_str]
    )
    assert xio_atomunit.get_value(acct_id_str()) == xio_str

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    print_atomunit_keys(sue_changeunit)
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_acctunit_update():
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
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    x_keylist = [atom_update(), bud_acctunit_str(), xio_str]
    xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert xio_atomunit.get_value(acct_id_str()) == xio_str
    assert xio_atomunit.get_value("credit_belief") == xio_credit_belief
    assert xio_atomunit.get_value("debtit_belief") == xio_debtit_belief

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_BudUnit_simple_attrs_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    x_budunit_tally = 55
    x_fund_pool = 8000000
    x_fund_coin = 8
    x_bit = 5
    x_max_tree_traverse = 66
    x_monetary_desc = "dragon dollars"
    x_credor_respect = 770
    x_debtor_respect = 880
    after_sue_bud._tally = x_budunit_tally
    after_sue_bud._fund_pool = x_fund_pool
    after_sue_bud._fund_coin = x_fund_coin
    after_sue_bud._bit = x_bit
    after_sue_bud.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_bud.set_monetary_desc(x_monetary_desc)
    after_sue_bud.set_credor_respect(x_credor_respect)
    after_sue_bud.set_debtor_respect(x_debtor_respect)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    x_keylist = [atom_update(), budunit_str()]
    xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert xio_atomunit.get_value("max_tree_traverse") == x_max_tree_traverse
    assert xio_atomunit.get_value("monetary_desc") == x_monetary_desc
    assert xio_atomunit.get_value("credor_respect") == x_credor_respect
    assert xio_atomunit.get_value("debtor_respect") == x_debtor_respect
    assert xio_atomunit.get_value("tally") == x_budunit_tally
    assert xio_atomunit.get_value("fund_pool") == x_fund_pool
    assert xio_atomunit.get_value("fund_coin") == x_fund_coin
    assert xio_atomunit.get_value("bit") == x_bit

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_acct_membership_insert():
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
    print(f"{after_sue_bud.get_acctunit_group_ids_dict()=}")

    # WHEN
    sue_changeunit = changeunit_shop()
    print(f"{after_sue_bud.get_acct(zia_str)._memberships=}")
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)
    # print(f"{sue_changeunit.atomunits.get(atom_insert()).keys()=}")
    # print(
    #     sue_changeunit.atomunits.get(atom_insert()).get(bud_acct_membership_str()).keys()
    # )

    # THEN
    x_keylist = [atom_insert(), bud_acctunit_str(), yao_str]
    yao_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert yao_atomunit.get_value(acct_id_str()) == yao_str

    x_keylist = [atom_insert(), bud_acctunit_str(), zia_str]
    zia_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert zia_atomunit.get_value(acct_id_str()) == zia_str
    print(f"\n{sue_changeunit.atomunits=}")
    # print(f"\n{zia_atomunit=}")

    x_keylist = [atom_insert(), bud_acct_membership_str(), zia_str, run_str]
    run_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert run_atomunit.get_value(acct_id_str()) == zia_str
    assert run_atomunit.get_value(group_id_str()) == run_str
    assert run_atomunit.get_value("credit_vote") == zia_run_credit_w
    assert run_atomunit.get_value("debtit_vote") == zia_run_debtit_w

    print_atomunit_keys(sue_changeunit)
    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert len(get_delete_atomunit_list(sue_changeunit)) == 0
    assert len(get_insert_atomunit_list(sue_changeunit)) == 3
    assert len(get_delete_atomunit_list(sue_changeunit)) == 0
    assert get_atomunit_total_count(sue_changeunit) == 3


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_acct_membership_update():
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
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    # x_keylist = [atom_update(), bud_acctunit_str(), xio_str]
    # xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    # assert xio_atomunit.get_value(acct_id_str()) == xio_str
    # print(f"\n{sue_changeunit.atomunits=}")
    # print(f"\n{xio_atomunit=}")

    x_keylist = [atom_update(), bud_acct_membership_str(), xio_str, run_str]
    xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert xio_atomunit.get_value(acct_id_str()) == xio_str
    assert xio_atomunit.get_value(group_id_str()) == run_str
    assert xio_atomunit.get_value("credit_vote") == after_xio_credit_w
    assert xio_atomunit.get_value("debtit_vote") == after_xio_debtit_w

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_acct_membership_delete():
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
    before_group_ids_dict = before_sue_bud.get_acctunit_group_ids_dict()

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_xio_acctunit = after_sue_bud.get_acct(xio_str)
    after_zia_acctunit = after_sue_bud.get_acct(zia_str)
    after_bob_acctunit = after_sue_bud.get_acct(bob_str)
    after_xio_acctunit.delete_membership(run_str)
    after_zia_acctunit.delete_membership(run_str)
    after_bob_acctunit.delete_membership(fly_str)
    after_group_ids_dict = after_sue_bud.get_acctunit_group_ids_dict()
    assert len(before_group_ids_dict.get(fly_str)) == 3
    assert len(before_group_ids_dict.get(run_str)) == 2
    assert len(after_group_ids_dict.get(fly_str)) == 2
    assert after_group_ids_dict.get(run_str) is None

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    x_keylist = [atom_delete(), bud_acct_membership_str(), bob_str, fly_str]
    xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert xio_atomunit.get_value(acct_id_str()) == bob_str
    assert xio_atomunit.get_value(group_id_str()) == fly_str

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    print_atomunit_keys(sue_changeunit)
    assert len(get_delete_atomunit_list(sue_changeunit)) == 3
    assert len(get_insert_atomunit_list(sue_changeunit)) == 0
    assert len(get_update_atomunit_list(sue_changeunit)) == 0
    assert get_atomunit_total_count(sue_changeunit) == 3


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    street_str = "street ball"
    street_road = before_sue_bud.make_road(ball_road, street_str)
    before_sue_bud.set_idea(ideaunit_shop(street_str), ball_road)
    disc_str = "Ultimate Disc"
    disc_road = before_sue_bud.make_road(sports_road, disc_str)
    music_str = "music"
    before_sue_bud.set_l1_idea(ideaunit_shop(music_str))
    before_sue_bud.set_idea(ideaunit_shop(disc_str), sports_road)
    # create after without ball_idea and street_idea
    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_sue_bud.del_idea_obj(ball_road)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    x_category = bud_ideaunit_str()
    print(f"{sue_changeunit.atomunits.get(atom_delete()).get(x_category).keys()=}")

    x_keylist = [atom_delete(), bud_ideaunit_str(), ball_road, street_str]
    street_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert street_atomunit.get_value(parent_road_str()) == ball_road
    assert street_atomunit.get_value(label_str()) == street_str

    x_keylist = [atom_delete(), bud_ideaunit_str(), sports_road, ball_str]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value(parent_road_str()) == sports_road
    assert ball_atomunit.get_value(label_str()) == ball_str

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    street_str = "street ball"
    street_road = before_sue_bud.make_road(ball_road, street_str)
    before_sue_bud.set_idea(ideaunit_shop(street_str), ball_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    disc_str = "Ultimate Disc"
    disc_road = after_sue_bud.make_road(sports_road, disc_str)
    after_sue_bud.set_idea(ideaunit_shop(disc_str), sports_road)
    music_str = "music"
    music_begin = 34
    music_close = 78
    music_mass = 55
    music_pledge = True
    music_road = after_sue_bud.make_l1_road(music_str)
    after_sue_bud.set_l1_idea(
        ideaunit_shop(
            music_str,
            begin=music_begin,
            close=music_close,
            mass=music_mass,
            pledge=music_pledge,
        )
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print_atomunit_keys(sue_changeunit)

    x_keylist = [atom_insert(), bud_ideaunit_str(), sports_road, disc_str]
    street_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert street_atomunit.get_value(parent_road_str()) == sports_road
    assert street_atomunit.get_value(label_str()) == disc_str

    x_keylist = [
        atom_insert(),
        bud_ideaunit_str(),
        after_sue_bud._pecun_id,
        music_str,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value(label_str()) == music_str
    assert ball_atomunit.get_value(parent_road_str()) == after_sue_bud._pecun_id
    assert ball_atomunit.get_value(begin_str()) == music_begin
    assert ball_atomunit.get_value(close_str()) == music_close
    assert ball_atomunit.get_value(mass_str()) == music_mass
    assert ball_atomunit.get_value(pledge_str()) == music_pledge

    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    music_str = "music"
    before_music_begin = 34
    before_music_close = 78
    before_music_mass = 55
    before_music_pledge = True
    music_road = before_sue_bud.make_l1_road(music_str)
    before_sue_bud.set_l1_idea(
        ideaunit_shop(
            music_str,
            begin=before_music_begin,
            close=before_music_close,
            mass=before_music_mass,
            pledge=before_music_pledge,
        )
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_music_begin = 99
    after_music_close = 111
    after_music_mass = 22
    after_music_pledge = False
    after_sue_bud.edit_idea_attr(
        music_road,
        begin=after_music_begin,
        close=after_music_close,
        mass=after_music_mass,
        pledge=after_music_pledge,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print_atomunit_keys(sue_changeunit)

    x_keylist = [
        atom_update(),
        bud_ideaunit_str(),
        after_sue_bud._pecun_id,
        music_str,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value(parent_road_str()) == after_sue_bud._pecun_id
    assert ball_atomunit.get_value(label_str()) == music_str
    assert ball_atomunit.get_value(begin_str()) == after_music_begin
    assert ball_atomunit.get_value(close_str()) == after_music_close
    assert ball_atomunit.get_value(mass_str()) == after_music_mass
    assert ball_atomunit.get_value(pledge_str()) == after_music_pledge

    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_awardlink_delete():
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
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    disc_str = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_str)
    before_sue_au.set_idea(ideaunit_shop(ball_str), sports_road)
    before_sue_au.set_idea(ideaunit_shop(disc_str), sports_road)
    before_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(run_str))
    before_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(fly_str))
    before_sue_au.edit_idea_attr(disc_road, awardlink=awardlink_shop(run_str))
    before_sue_au.edit_idea_attr(disc_road, awardlink=awardlink_shop(fly_str))

    after_sue_bud = copy_deepcopy(before_sue_au)
    after_sue_bud.edit_idea_attr(disc_road, awardlink_del=run_str)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_au, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_delete(), bud_idea_awardlink_str(), disc_road, run_str]
    run_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert run_atomunit.get_value("road") == disc_road
    assert run_atomunit.get_value(group_id_str()) == run_str

    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_awardlink_insert():
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
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    disc_str = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_str)
    before_sue_au.set_idea(ideaunit_shop(ball_str), sports_road)
    before_sue_au.set_idea(ideaunit_shop(disc_str), sports_road)
    before_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(run_str))
    before_sue_au.edit_idea_attr(disc_road, awardlink=awardlink_shop(fly_str))
    after_sue_au = copy_deepcopy(before_sue_au)
    after_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(fly_str))
    after_run_give_force = 44
    after_run_take_force = 66
    x_awardlink = awardlink_shop(run_str, after_run_give_force, after_run_take_force)
    after_sue_au.edit_idea_attr(disc_road, awardlink=x_awardlink)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_insert(), bud_idea_awardlink_str(), disc_road, run_str]
    run_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert run_atomunit.get_value("road") == disc_road
    assert run_atomunit.get_value(group_id_str()) == run_str
    assert run_atomunit.get_value("road") == disc_road
    assert run_atomunit.get_value(group_id_str()) == run_str
    assert run_atomunit.get_value("give_force") == after_run_give_force
    assert run_atomunit.get_value("take_force") == after_run_take_force

    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_awardlink_update():
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
    sports_road = before_sue_au.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_str)
    before_sue_au.set_idea(ideaunit_shop(ball_str), sports_road)
    before_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(run_str))
    run_awardlink = before_sue_au.get_idea_obj(ball_road).awardlinks.get(run_str)

    after_sue_bud = copy_deepcopy(before_sue_au)
    after_give_force = 55
    after_take_force = 66
    after_sue_bud.edit_idea_attr(
        ball_road,
        awardlink=awardlink_shop(
            group_id=run_str,
            give_force=after_give_force,
            take_force=after_take_force,
        ),
    )
    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_au, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_update(), bud_idea_awardlink_str(), ball_road, run_str]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value(group_id_str()) == run_str
    assert ball_atomunit.get_value("give_force") == after_give_force
    assert ball_atomunit.get_value("take_force") == after_take_force
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_factunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_str)
    bend_str = "bendable"
    bend_road = before_sue_bud.make_road(knee_road, bend_str)
    before_sue_bud.set_idea(ideaunit_shop(bend_str), knee_road)
    broken_str = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_str)
    before_sue_bud.set_l1_idea(ideaunit_shop(knee_str))
    before_sue_bud.set_idea(ideaunit_shop(broken_str), knee_road)
    before_fopen = 11
    before_fnigh = 22
    before_fact = factunit_shop(knee_road, bend_road, before_fopen, before_fnigh)
    before_sue_bud.edit_idea_attr(ball_road, factunit=before_fact)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_fopen = 55
    after_fnigh = 66
    knee_fact = factunit_shop(knee_road, broken_road, after_fopen, after_fnigh)
    after_sue_bud.edit_idea_attr(ball_road, factunit=knee_fact)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_update(), bud_idea_factunit_str(), ball_road, knee_road]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("pick") == broken_road
    assert ball_atomunit.get_value(fopen_str()) == after_fopen
    assert ball_atomunit.get_value(fnigh_str()) == after_fnigh
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_factunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_str)
    broken_str = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_str)
    before_sue_bud.set_l1_idea(ideaunit_shop(knee_str))
    before_sue_bud.set_idea(ideaunit_shop(broken_str), knee_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_fopen = 55
    after_fnigh = 66
    after_fact = factunit_shop(knee_road, broken_road, after_fopen, after_fnigh)
    after_sue_bud.edit_idea_attr(road=ball_road, factunit=after_fact)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [atom_insert(), bud_idea_factunit_str(), ball_road, knee_road]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("pick") == broken_road
    assert ball_atomunit.get_value(fopen_str()) == after_fopen
    assert ball_atomunit.get_value(fnigh_str()) == after_fnigh
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_factunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_str)
    broken_str = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_str)
    before_sue_bud.set_l1_idea(ideaunit_shop(knee_str))
    before_sue_bud.set_idea(ideaunit_shop(broken_str), knee_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    before_broken_open = 55
    before_broken_nigh = 66
    before_fact = factunit_shop(
        base=knee_road,
        pick=broken_road,
        fopen=before_broken_open,
        fnigh=before_broken_nigh,
    )
    before_sue_bud.edit_idea_attr(road=ball_road, factunit=before_fact)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [atom_delete(), bud_idea_factunit_str(), ball_road, knee_road]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reason_premiseunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_str)
    before_sue_bud.set_l1_idea(ideaunit_shop(knee_str))
    broken_str = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_str)
    before_sue_bud.set_idea(ideaunit_shop(broken_str), knee_road)
    bend_str = "bend"
    bend_road = before_sue_bud.make_road(knee_road, bend_str)
    before_sue_bud.set_idea(ideaunit_shop(bend_str), knee_road)
    before_sue_bud.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    after_sue_bud.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=broken_open,
        reason_premise_nigh=broken_nigh,
        reason_premise_divisor=broken_divisor,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_insert(),
        bud_idea_reason_premiseunit_str(),
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("need") == broken_road
    assert ball_atomunit.get_value("open") == broken_open
    assert ball_atomunit.get_value("nigh") == broken_nigh
    assert ball_atomunit.get_value("divisor") == broken_divisor
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reason_premiseunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_str)
    before_sue_bud.set_l1_idea(ideaunit_shop(knee_str))
    broken_str = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_str)
    before_sue_bud.set_idea(ideaunit_shop(broken_str), knee_road)
    bend_str = "bend"
    bend_road = before_sue_bud.make_road(knee_road, bend_str)
    before_sue_bud.set_idea(ideaunit_shop(bend_str), knee_road)
    before_sue_bud.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    before_sue_bud.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=broken_open,
        reason_premise_nigh=broken_nigh,
        reason_premise_divisor=broken_divisor,
    )
    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_sue_bud.edit_idea_attr(
        ball_road,
        reason_del_premise_base=knee_road,
        reason_del_premise_need=broken_road,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_delete(),
        bud_idea_reason_premiseunit_str(),
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("need") == broken_road
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reason_premiseunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_str)
    before_sue_bud.set_l1_idea(ideaunit_shop(knee_str))
    broken_str = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_str)
    before_sue_bud.set_idea(ideaunit_shop(broken_str), knee_road)
    bend_str = "bend"
    bend_road = before_sue_bud.make_road(knee_road, bend_str)
    before_sue_bud.set_idea(ideaunit_shop(bend_str), knee_road)
    before_sue_bud.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )
    before_broken_open = 111
    before_broken_nigh = 777
    before_broken_divisor = 13
    before_sue_bud.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=before_broken_open,
        reason_premise_nigh=before_broken_nigh,
        reason_premise_divisor=before_broken_divisor,
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_broken_open = 333
    after_broken_nigh = 555
    after_broken_divisor = 78
    after_sue_bud.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=after_broken_open,
        reason_premise_nigh=after_broken_nigh,
        reason_premise_divisor=after_broken_divisor,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_update(),
        bud_idea_reason_premiseunit_str(),
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("need") == broken_road
    assert ball_atomunit.get_value("open") == after_broken_open
    assert ball_atomunit.get_value("nigh") == after_broken_nigh
    assert ball_atomunit.get_value("divisor") == after_broken_divisor
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reasonunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_str)
    medical_str = "get medical attention"
    medical_road = before_sue_bud.make_road(knee_road, medical_str)
    before_sue_bud.set_l1_idea(ideaunit_shop(knee_str))
    before_sue_bud.set_idea(ideaunit_shop(medical_str), knee_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_medical_base_idea_active_requisite = False
    after_sue_bud.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_base_idea_active_requisite=after_medical_base_idea_active_requisite,
    )

    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_insert(),
        bud_idea_reasonunit_str(),
        ball_road,
        medical_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == medical_road
    assert (
        ball_atomunit.get_value(base_idea_active_requisite_str())
        == after_medical_base_idea_active_requisite
    )
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reasonunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_str)
    medical_str = "get medical attention"
    medical_road = before_sue_bud.make_road(knee_road, medical_str)
    before_sue_bud.set_l1_idea(ideaunit_shop(knee_str))
    before_sue_bud.set_idea(ideaunit_shop(medical_str), knee_road)
    before_medical_base_idea_active_requisite = True
    before_sue_bud.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_base_idea_active_requisite=before_medical_base_idea_active_requisite,
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_medical_base_idea_active_requisite = False
    after_sue_bud.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_base_idea_active_requisite=after_medical_base_idea_active_requisite,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_update(),
        bud_idea_reasonunit_str(),
        ball_road,
        medical_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == medical_road
    assert (
        ball_atomunit.get_value(base_idea_active_requisite_str())
        == after_medical_base_idea_active_requisite
    )
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reasonunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    knee_str = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_str)
    medical_str = "get medical attention"
    medical_road = before_sue_bud.make_road(knee_road, medical_str)
    before_sue_bud.set_l1_idea(ideaunit_shop(knee_str))
    before_sue_bud.set_idea(ideaunit_shop(medical_str), knee_road)
    before_medical_base_idea_active_requisite = True
    before_sue_bud.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_base_idea_active_requisite=before_medical_base_idea_active_requisite,
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_idea = after_sue_bud.get_idea_obj(ball_road)
    after_ball_idea.del_reasonunit_base(medical_road)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_delete(),
        bud_idea_reasonunit_str(),
        ball_road,
        medical_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == medical_road
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_teamlink_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_ideaunit = after_sue_bud.get_idea_obj(ball_road)
    after_ball_ideaunit.teamunit.set_teamlink(xio_str)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_insert(),
        bud_idea_teamlink_str(),
        ball_road,
        xio_str,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value(group_id_str()) == xio_str
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_teamlink_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    before_ball_ideaunit = before_sue_bud.get_idea_obj(ball_road)
    before_ball_ideaunit.teamunit.set_teamlink(xio_str)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_ideaunit = after_sue_bud.get_idea_obj(ball_road)
    after_ball_ideaunit.teamunit.del_teamlink(xio_str)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_delete(),
        bud_idea_teamlink_str(),
        ball_road,
        xio_str,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value(group_id_str()) == xio_str
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_healerlink_insert_IdeaUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_ideaunit = after_sue_bud.get_idea_obj(ball_road)
    after_ball_ideaunit.healerlink.set_healer_id(xio_str)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_insert(),
        bud_idea_healerlink_str(),
        ball_road,
        xio_str,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value(healer_id_str()) == xio_str
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_healerlink_insert_IdeaUnitInsert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    after_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    after_ball_ideaunit = after_sue_bud.get_idea_obj(ball_road)
    after_ball_ideaunit.healerlink.set_healer_id(xio_str)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_insert(),
        bud_idea_healerlink_str(),
        ball_road,
        xio_str,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist, True)
    assert ball_atomunit
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value(healer_id_str()) == xio_str
    assert get_atomunit_total_count(sue_changeunit) == 3


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_healerlink_delete_IdeaUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    before_ball_ideaunit = before_sue_bud.get_idea_obj(ball_road)
    before_ball_ideaunit.healerlink.set_healer_id(xio_str)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_ideaunit = after_sue_bud.get_idea_obj(ball_road)
    after_ball_ideaunit.healerlink.del_healer_id(xio_str)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_delete(),
        bud_idea_healerlink_str(),
        ball_road,
        xio_str,
    ]
    ball_atomunit = get_nested_value(
        sue_changeunit.atomunits, x_keylist, if_missing_return_None=True
    )
    assert ball_atomunit
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value(healer_id_str()) == xio_str
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_healerlink_delete_IdeaUnitDelete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_bud.add_acctunit(xio_str)
    sports_str = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_str)
    before_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    before_ball_ideaunit = before_sue_bud.get_idea_obj(ball_road)
    before_ball_ideaunit.healerlink.set_healer_id(xio_str)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_sue_bud.del_idea_obj(ball_road)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_delete(),
        bud_idea_healerlink_str(),
        ball_road,
        xio_str,
    ]
    ball_atomunit = get_nested_value(
        sue_changeunit.atomunits, x_keylist, if_missing_return_None=True
    )
    assert ball_atomunit
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value(healer_id_str()) == xio_str
    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_atomunits_CorrectlyCreates_AtomUnits():
    # ESTABLISH
    sue_str = "Sue"

    after_sue_bud = budunit_shop(sue_str)
    xio_str = "Xio"
    temp_xio_acctunit = acctunit_shop(xio_str)
    after_sue_bud.set_acctunit(temp_xio_acctunit, auto_set_membership=False)
    sports_str = "sports"
    sports_road = after_sue_bud.make_l1_road(sports_str)
    ball_str = "basketball"
    ball_road = after_sue_bud.make_road(sports_road, ball_str)
    after_sue_bud.set_idea(ideaunit_shop(ball_str), sports_road)
    after_ball_ideaunit = after_sue_bud.get_idea_obj(ball_road)
    after_ball_ideaunit.teamunit.set_teamlink(xio_str)

    before_sue_bud = budunit_shop(sue_str)
    sue1_changeunit = changeunit_shop()
    sue1_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)
    print(f"{sue1_changeunit.get_ordered_atomunits()}")
    assert len(sue1_changeunit.get_ordered_atomunits()) == 4

    # WHEN
    sue2_changeunit = changeunit_shop()
    sue2_changeunit.add_all_atomunits(after_sue_bud)

    # THEN
    assert len(sue2_changeunit.get_ordered_atomunits()) == 4
    assert sue2_changeunit == sue1_changeunit
