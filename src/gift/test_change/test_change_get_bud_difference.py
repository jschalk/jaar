from src.bud.char import charunit_shop
from src.bud.lobby import awardlink_shop
from src.bud.idea import ideaunit_shop
from src.bud.reason_idea import factunit_shop
from src.bud.bud import budunit_shop
from src.gift.atom import atom_insert, atom_update, atom_delete
from src.gift.change import ChangeUnit, changeunit_shop
from src.listen.examples.example_listen_buds import get_bud_with_4_levels
from src._instrument.python import get_nested_value, get_empty_list_if_None
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
    sue_bud = get_bud_with_4_levels()
    sue_changeunit = changeunit_shop()
    assert sue_changeunit.atomunits == {}

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(sue_bud, sue_bud)

    # THEN
    assert sue_changeunit.atomunits == {}


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_charunit_insert():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    xio_text = "Xio"
    xio_credor_weight = 33
    xio_debtor_weight = 44
    xio_charunit = charunit_shop(xio_text, xio_credor_weight, xio_debtor_weight)
    after_sue_bud.set_charunit(xio_charunit, auto_set_lobbyship=False)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    assert len(sue_changeunit.atomunits.get(atom_insert()).get("bud_charunit")) == 1
    sue_insert_dict = sue_changeunit.atomunits.get(atom_insert())
    sue_charunit_dict = sue_insert_dict.get("bud_charunit")
    xio_atomunit = sue_charunit_dict.get(xio_text)
    assert xio_atomunit.get_value("char_id") == xio_text
    assert xio_atomunit.get_value("credor_weight") == xio_credor_weight
    assert xio_atomunit.get_value("debtor_weight") == xio_debtor_weight

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_charunit_delete():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    before_sue_bud.add_charunit("Yao")
    before_sue_bud.add_charunit("Zia")

    after_sue_bud = copy_deepcopy(before_sue_bud)

    xio_text = "Xio"
    before_sue_bud.add_charunit(xio_text)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    xio_atomunit = get_nested_value(
        sue_changeunit.atomunits, [atom_delete(), "bud_charunit", xio_text]
    )
    assert xio_atomunit.get_value("char_id") == xio_text

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    print_atomunit_keys(sue_changeunit)
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_charunit_update():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    xio_text = "Xio"
    before_sue_bud.add_charunit(xio_text)
    xio_credor_weight = 33
    xio_debtor_weight = 44
    after_sue_bud.add_charunit(xio_text, xio_credor_weight, xio_debtor_weight)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    x_keylist = [atom_update(), "bud_charunit", xio_text]
    xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert xio_atomunit.get_value("char_id") == xio_text
    assert xio_atomunit.get_value("credor_weight") == xio_credor_weight
    assert xio_atomunit.get_value("debtor_weight") == xio_debtor_weight

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_BudUnit_simple_attrs_update():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    x_budUnit_weight = 55
    x_fund_pool = 8000000
    x_fund_coin = 8
    x_bit = 5
    x_max_tree_traverse = 66
    x_monetary_desc = "dragon dollars"
    x_credor_respect = 770
    x_debtor_respect = 880
    after_sue_bud._weight = x_budUnit_weight
    after_sue_bud._fund_pool = x_fund_pool
    after_sue_bud._fund_coin = x_fund_coin
    after_sue_bud._bit = x_bit
    after_sue_bud.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_bud.set_monetary_desc(x_monetary_desc)
    after_sue_bud.set_credor_respect(x_credor_respect)
    after_sue_bud.set_debtor_resepect(x_debtor_respect)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    x_keylist = [atom_update(), "budunit"]
    xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert xio_atomunit.get_value("_max_tree_traverse") == x_max_tree_traverse
    assert xio_atomunit.get_value("_monetary_desc") == x_monetary_desc
    assert xio_atomunit.get_value("_credor_respect") == x_credor_respect
    assert xio_atomunit.get_value("_debtor_respect") == x_debtor_respect
    assert xio_atomunit.get_value("_weight") == x_budUnit_weight
    assert xio_atomunit.get_value("_fund_pool") == x_fund_pool
    assert xio_atomunit.get_value("_fund_coin") == x_fund_coin
    assert xio_atomunit.get_value("_bit") == x_bit

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_char_lobbyship_insert():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    yao_text = "Yao"
    zia_text = "Zia"
    temp_yao_charunit = charunit_shop(yao_text)
    temp_zia_charunit = charunit_shop(zia_text)
    after_sue_bud.set_charunit(temp_yao_charunit, auto_set_lobbyship=False)
    after_sue_bud.set_charunit(temp_zia_charunit, auto_set_lobbyship=False)
    after_yao_charunit = after_sue_bud.get_char(yao_text)
    after_zia_charunit = after_sue_bud.get_char(zia_text)
    run_text = ",runners"
    zia_run_credor_w = 77
    zia_run_debtor_w = 88
    after_zia_charunit.add_lobbyship(run_text, zia_run_credor_w, zia_run_debtor_w)
    print(f"{after_sue_bud.get_lobby_ids_dict()=}")

    # WHEN
    sue_changeunit = changeunit_shop()
    print(f"{after_sue_bud.get_char(zia_text)._lobbyships=}")
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)
    # print(f"{sue_changeunit.atomunits.get(atom_insert()).keys()=}")
    # print(
    #     sue_changeunit.atomunits.get(atom_insert()).get("bud_char_lobbyship").keys()
    # )

    # THEN
    x_keylist = [atom_insert(), "bud_charunit", yao_text]
    yao_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert yao_atomunit.get_value("char_id") == yao_text

    x_keylist = [atom_insert(), "bud_charunit", zia_text]
    zia_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert zia_atomunit.get_value("char_id") == zia_text
    print(f"\n{sue_changeunit.atomunits=}")
    # print(f"\n{zia_atomunit=}")

    x_keylist = [atom_insert(), "bud_char_lobbyship", zia_text, run_text]
    run_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert run_atomunit.get_value("char_id") == zia_text
    assert run_atomunit.get_value("lobby_id") == run_text
    assert run_atomunit.get_value("credor_weight") == zia_run_credor_w
    assert run_atomunit.get_value("debtor_weight") == zia_run_debtor_w

    print_atomunit_keys(sue_changeunit)
    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert len(get_delete_atomunit_list(sue_changeunit)) == 0
    assert len(get_insert_atomunit_list(sue_changeunit)) == 3
    assert len(get_delete_atomunit_list(sue_changeunit)) == 0
    assert get_atomunit_total_count(sue_changeunit) == 3


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_char_lobbyship_update():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    xio_text = "Xio"
    zia_text = "Zia"
    before_sue_bud.add_charunit(xio_text)
    before_sue_bud.add_charunit(zia_text)
    run_text = ",runners"
    before_xio_credor_w = 77
    before_xio_debtor_w = 88
    before_xio_char = before_sue_bud.get_char(xio_text)
    before_xio_char.add_lobbyship(run_text, before_xio_credor_w, before_xio_debtor_w)
    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_xio_charunit = after_sue_bud.get_char(xio_text)
    after_xio_credor_w = 55
    after_xio_debtor_w = 66
    after_xio_charunit.add_lobbyship(run_text, after_xio_credor_w, after_xio_debtor_w)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    # x_keylist = [atom_update(), "bud_charunit", xio_text]
    # xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    # assert xio_atomunit.get_value("char_id") == xio_text
    # print(f"\n{sue_changeunit.atomunits=}")
    # print(f"\n{xio_atomunit=}")

    x_keylist = [atom_update(), "bud_char_lobbyship", xio_text, run_text]
    xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert xio_atomunit.get_value("char_id") == xio_text
    assert xio_atomunit.get_value("lobby_id") == run_text
    assert xio_atomunit.get_value("credor_weight") == after_xio_credor_w
    assert xio_atomunit.get_value("debtor_weight") == after_xio_debtor_w

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_char_lobbyship_delete():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    xio_text = "Xio"
    zia_text = "Zia"
    bob_text = "Bob"
    before_sue_bud.add_charunit(xio_text)
    before_sue_bud.add_charunit(zia_text)
    before_sue_bud.add_charunit(bob_text)
    before_xio_charunit = before_sue_bud.get_char(xio_text)
    before_zia_charunit = before_sue_bud.get_char(zia_text)
    before_bob_charunit = before_sue_bud.get_char(bob_text)
    run_text = ",runners"
    before_xio_charunit.add_lobbyship(run_text)
    before_zia_charunit.add_lobbyship(run_text)
    fly_text = ",flyers"
    before_xio_charunit.add_lobbyship(fly_text)
    before_zia_charunit.add_lobbyship(fly_text)
    before_bob_charunit.add_lobbyship(fly_text)
    before_lobby_ids_dict = before_sue_bud.get_lobby_ids_dict()

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_xio_charunit = after_sue_bud.get_char(xio_text)
    after_zia_charunit = after_sue_bud.get_char(zia_text)
    after_bob_charunit = after_sue_bud.get_char(bob_text)
    after_xio_charunit.delete_lobbyship(run_text)
    after_zia_charunit.delete_lobbyship(run_text)
    after_bob_charunit.delete_lobbyship(fly_text)
    after_lobby_ids_dict = after_sue_bud.get_lobby_ids_dict()
    assert len(before_lobby_ids_dict.get(fly_text)) == 3
    assert len(before_lobby_ids_dict.get(run_text)) == 2
    assert len(after_lobby_ids_dict.get(fly_text)) == 2
    assert after_lobby_ids_dict.get(run_text) is None

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    x_keylist = [atom_delete(), "bud_char_lobbyship", bob_text, fly_text]
    xio_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert xio_atomunit.get_value("char_id") == bob_text
    assert xio_atomunit.get_value("lobby_id") == fly_text

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    print_atomunit_keys(sue_changeunit)
    assert len(get_delete_atomunit_list(sue_changeunit)) == 3
    assert len(get_insert_atomunit_list(sue_changeunit)) == 0
    assert len(get_update_atomunit_list(sue_changeunit)) == 0
    assert get_atomunit_total_count(sue_changeunit) == 3


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_delete():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    street_text = "street ball"
    street_road = before_sue_bud.make_road(ball_road, street_text)
    before_sue_bud.add_idea(ideaunit_shop(street_text), ball_road)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_bud.make_road(sports_road, disc_text)
    music_text = "music"
    before_sue_bud.add_l1_idea(ideaunit_shop(music_text))
    before_sue_bud.add_idea(ideaunit_shop(disc_text), sports_road)
    # create after without ball_idea and street_idea
    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_sue_bud.del_idea_obj(ball_road)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    x_category = "bud_ideaunit"
    print(f"{sue_changeunit.atomunits.get(atom_delete()).get(x_category).keys()=}")

    x_keylist = [atom_delete(), "bud_ideaunit", ball_road, street_text]
    street_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert street_atomunit.get_value("parent_road") == ball_road
    assert street_atomunit.get_value("label") == street_text

    x_keylist = [atom_delete(), "bud_ideaunit", sports_road, ball_text]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("parent_road") == sports_road
    assert ball_atomunit.get_value("label") == ball_text

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_insert():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    street_text = "street ball"
    street_road = before_sue_bud.make_road(ball_road, street_text)
    before_sue_bud.add_idea(ideaunit_shop(street_text), ball_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    disc_text = "Ultimate Disc"
    disc_road = after_sue_bud.make_road(sports_road, disc_text)
    after_sue_bud.add_idea(ideaunit_shop(disc_text), sports_road)
    music_text = "music"
    music_begin = 34
    music_close = 78
    music_weight = 55
    music_pledge = True
    music_road = after_sue_bud.make_l1_road(music_text)
    after_sue_bud.add_l1_idea(
        ideaunit_shop(
            music_text,
            _begin=music_begin,
            _close=music_close,
            _weight=music_weight,
            pledge=music_pledge,
        )
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print_atomunit_keys(sue_changeunit)

    x_keylist = [atom_insert(), "bud_ideaunit", sports_road, disc_text]
    street_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert street_atomunit.get_value("parent_road") == sports_road
    assert street_atomunit.get_value("label") == disc_text

    x_keylist = [
        atom_insert(),
        "bud_ideaunit",
        after_sue_bud._real_id,
        music_text,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("label") == music_text
    assert ball_atomunit.get_value("parent_road") == after_sue_bud._real_id
    assert ball_atomunit.get_value("_begin") == music_begin
    assert ball_atomunit.get_value("_close") == music_close
    assert ball_atomunit.get_value("_weight") == music_weight
    assert ball_atomunit.get_value("pledge") == music_pledge

    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_update():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    music_text = "music"
    before_music_begin = 34
    before_music_close = 78
    before_music_weight = 55
    before_music_pledge = True
    music_road = before_sue_bud.make_l1_road(music_text)
    before_sue_bud.add_l1_idea(
        ideaunit_shop(
            music_text,
            _begin=before_music_begin,
            _close=before_music_close,
            _weight=before_music_weight,
            pledge=before_music_pledge,
        )
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_music_begin = 99
    after_music_close = 111
    after_music_weight = 22
    after_music_pledge = False
    after_sue_bud.edit_idea_attr(
        music_road,
        begin=after_music_begin,
        close=after_music_close,
        weight=after_music_weight,
        pledge=after_music_pledge,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print_atomunit_keys(sue_changeunit)

    x_keylist = [
        atom_update(),
        "bud_ideaunit",
        after_sue_bud._real_id,
        music_text,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("parent_road") == after_sue_bud._real_id
    assert ball_atomunit.get_value("label") == music_text
    assert ball_atomunit.get_value("_begin") == after_music_begin
    assert ball_atomunit.get_value("_close") == after_music_close
    assert ball_atomunit.get_value("_weight") == after_music_weight
    assert ball_atomunit.get_value("pledge") == after_music_pledge

    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_awardlink_delete():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    xio_text = "Xio"
    zia_text = "Zia"
    bob_text = "Bob"
    before_sue_au.add_charunit(xio_text)
    before_sue_au.add_charunit(zia_text)
    before_sue_au.add_charunit(bob_text)
    xio_charunit = before_sue_au.get_char(xio_text)
    zia_charunit = before_sue_au.get_char(zia_text)
    bob_charunit = before_sue_au.get_char(bob_text)
    run_text = ",runners"
    xio_charunit.add_lobbyship(run_text)
    zia_charunit.add_lobbyship(run_text)
    fly_text = ",flyers"
    xio_charunit.add_lobbyship(fly_text)
    zia_charunit.add_lobbyship(fly_text)
    bob_charunit.add_lobbyship(fly_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.add_idea(ideaunit_shop(disc_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(run_text))
    before_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(fly_text))
    before_sue_au.edit_idea_attr(disc_road, awardlink=awardlink_shop(run_text))
    before_sue_au.edit_idea_attr(disc_road, awardlink=awardlink_shop(fly_text))

    after_sue_bud = copy_deepcopy(before_sue_au)
    after_sue_bud.edit_idea_attr(disc_road, awardlink_del=run_text)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_au, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_delete(), "bud_idea_awardlink", disc_road, run_text]
    run_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert run_atomunit.get_value("road") == disc_road
    assert run_atomunit.get_value("lobby_id") == run_text

    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_awardlink_insert():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    xio_text = "Xio"
    zia_text = "Zia"
    bob_text = "Bob"
    before_sue_au.add_charunit(xio_text)
    before_sue_au.add_charunit(zia_text)
    before_sue_au.add_charunit(bob_text)
    xio_charunit = before_sue_au.get_char(xio_text)
    zia_charunit = before_sue_au.get_char(zia_text)
    bob_charunit = before_sue_au.get_char(bob_text)
    run_text = ",runners"
    xio_charunit.add_lobbyship(run_text)
    zia_charunit.add_lobbyship(run_text)
    fly_text = ",flyers"
    xio_charunit.add_lobbyship(fly_text)
    zia_charunit.add_lobbyship(fly_text)
    bob_charunit.add_lobbyship(fly_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.add_idea(ideaunit_shop(disc_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(run_text))
    before_sue_au.edit_idea_attr(disc_road, awardlink=awardlink_shop(fly_text))
    after_sue_au = copy_deepcopy(before_sue_au)
    after_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(fly_text))
    after_run_give_weight = 44
    after_run_take_weight = 66
    x_awardlink = awardlink_shop(run_text, after_run_give_weight, after_run_take_weight)
    after_sue_au.edit_idea_attr(disc_road, awardlink=x_awardlink)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_insert(), "bud_idea_awardlink", disc_road, run_text]
    run_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert run_atomunit.get_value("road") == disc_road
    assert run_atomunit.get_value("lobby_id") == run_text
    assert run_atomunit.get_value("road") == disc_road
    assert run_atomunit.get_value("lobby_id") == run_text
    assert run_atomunit.get_value("give_weight") == after_run_give_weight
    assert run_atomunit.get_value("take_weight") == after_run_take_weight

    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_awardlink_update():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_au = budunit_shop(sue_text)
    xio_text = "Xio"
    zia_text = "Zia"
    before_sue_au.add_charunit(xio_text)
    before_sue_au.add_charunit(zia_text)
    xio_charunit = before_sue_au.get_char(xio_text)
    run_text = ",runners"
    xio_charunit.add_lobbyship(run_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, awardlink=awardlink_shop(run_text))
    run_awardlink = before_sue_au.get_idea_obj(ball_road)._awardlinks.get(run_text)

    after_sue_bud = copy_deepcopy(before_sue_au)
    after_give_weight = 55
    after_take_weight = 66
    after_sue_bud.edit_idea_attr(
        ball_road,
        awardlink=awardlink_shop(
            lobby_id=run_text,
            give_weight=after_give_weight,
            take_weight=after_take_weight,
        ),
    )
    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_au, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_update(), "bud_idea_awardlink", ball_road, run_text]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("lobby_id") == run_text
    assert ball_atomunit.get_value("give_weight") == after_give_weight
    assert ball_atomunit.get_value("take_weight") == after_take_weight
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_factunit_update():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_text)
    bend_text = "bendable"
    bend_road = before_sue_bud.make_road(knee_road, bend_text)
    before_sue_bud.add_idea(ideaunit_shop(bend_text), knee_road)
    broken_text = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_text)
    before_sue_bud.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_bud.add_idea(ideaunit_shop(broken_text), knee_road)
    before_broken_open = 11
    before_broken_nigh = 22
    before_sue_bud.edit_idea_attr(
        ball_road,
        factunit=factunit_shop(
            knee_road, bend_road, before_broken_open, before_broken_nigh
        ),
    )

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_broken_open = 55
    after_broken_nigh = 66
    after_sue_bud.edit_idea_attr(
        ball_road,
        factunit=factunit_shop(
            knee_road, broken_road, after_broken_open, after_broken_nigh
        ),
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_update(), "bud_idea_factunit", ball_road, knee_road]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("pick") == broken_road
    assert ball_atomunit.get_value("open") == after_broken_open
    assert ball_atomunit.get_value("nigh") == after_broken_nigh
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_factunit_insert():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_text)
    before_sue_bud.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_bud.add_idea(ideaunit_shop(broken_text), knee_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_broken_open = 55
    after_broken_nigh = 66
    after_sue_bud.edit_idea_attr(
        road=ball_road,
        factunit=factunit_shop(
            base=knee_road,
            pick=broken_road,
            open=after_broken_open,
            nigh=after_broken_nigh,
        ),
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [atom_insert(), "bud_idea_factunit", ball_road, knee_road]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("pick") == broken_road
    assert ball_atomunit.get_value("open") == after_broken_open
    assert ball_atomunit.get_value("nigh") == after_broken_nigh
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_factunit_delete():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_text)
    before_sue_bud.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_bud.add_idea(ideaunit_shop(broken_text), knee_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    before_broken_open = 55
    before_broken_nigh = 66
    before_sue_bud.edit_idea_attr(
        road=ball_road,
        factunit=factunit_shop(
            base=knee_road,
            pick=broken_road,
            open=before_broken_open,
            nigh=before_broken_nigh,
        ),
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [atom_delete(), "bud_idea_factunit", ball_road, knee_road]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reason_premiseunit_insert():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_text)
    before_sue_bud.add_l1_idea(ideaunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_text)
    before_sue_bud.add_idea(ideaunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_bud.make_road(knee_road, bend_text)
    before_sue_bud.add_idea(ideaunit_shop(bend_text), knee_road)
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
        "bud_idea_reason_premiseunit",
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
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_text)
    before_sue_bud.add_l1_idea(ideaunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_text)
    before_sue_bud.add_idea(ideaunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_bud.make_road(knee_road, bend_text)
    before_sue_bud.add_idea(ideaunit_shop(bend_text), knee_road)
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
        "bud_idea_reason_premiseunit",
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
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_text)
    before_sue_bud.add_l1_idea(ideaunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_bud.make_road(knee_road, broken_text)
    before_sue_bud.add_idea(ideaunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_bud.make_road(knee_road, bend_text)
    before_sue_bud.add_idea(ideaunit_shop(bend_text), knee_road)
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
        "bud_idea_reason_premiseunit",
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
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_bud.make_road(knee_road, medical_text)
    before_sue_bud.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_bud.add_idea(ideaunit_shop(medical_text), knee_road)

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
        "bud_idea_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == medical_road
    assert (
        ball_atomunit.get_value("base_idea_active_requisite")
        == after_medical_base_idea_active_requisite
    )
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reasonunit_update():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_bud.make_road(knee_road, medical_text)
    before_sue_bud.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_bud.add_idea(ideaunit_shop(medical_text), knee_road)
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
        "bud_idea_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == medical_road
    assert (
        ball_atomunit.get_value("base_idea_active_requisite")
        == after_medical_base_idea_active_requisite
    )
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reasonunit_delete():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_bud.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_bud.make_road(knee_road, medical_text)
    before_sue_bud.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_bud.add_idea(ideaunit_shop(medical_text), knee_road)
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
        "bud_idea_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == medical_road
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_lobbyhold_insert():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    xio_text = "Xio"
    before_sue_bud.add_charunit(xio_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_ideaunit = after_sue_bud.get_idea_obj(ball_road)
    after_ball_ideaunit._doerunit.set_lobbyhold(xio_text)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_insert(),
        "bud_idea_lobbyhold",
        ball_road,
        xio_text,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("lobby_id") == xio_text
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_lobbyhold_delete():
    # ESTABLISH
    sue_text = "Sue"
    before_sue_bud = budunit_shop(sue_text)
    xio_text = "Xio"
    before_sue_bud.add_charunit(xio_text)
    sports_text = "sports"
    sports_road = before_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_bud.make_road(sports_road, ball_text)
    before_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_bud.get_idea_obj(ball_road)
    before_ball_ideaunit._doerunit.set_lobbyhold(xio_text)

    after_sue_bud = copy_deepcopy(before_sue_bud)
    after_ball_ideaunit = after_sue_bud.get_idea_obj(ball_road)
    after_ball_ideaunit._doerunit.del_lobbyhold(xio_text)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_bud, after_sue_bud)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_delete(),
        "bud_idea_lobbyhold",
        ball_road,
        xio_text,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("lobby_id") == xio_text
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_atomunits_CorrectlyCreates_AtomUnits():
    # ESTABLISH
    sue_text = "Sue"

    after_sue_bud = budunit_shop(sue_text)
    xio_text = "Xio"
    temp_xio_charunit = charunit_shop(xio_text)
    after_sue_bud.set_charunit(temp_xio_charunit, auto_set_lobbyship=False)
    sports_text = "sports"
    sports_road = after_sue_bud.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = after_sue_bud.make_road(sports_road, ball_text)
    after_sue_bud.add_idea(ideaunit_shop(ball_text), sports_road)
    after_ball_ideaunit = after_sue_bud.get_idea_obj(ball_road)
    after_ball_ideaunit._doerunit.set_lobbyhold(xio_text)

    before_sue_bud = budunit_shop(sue_text)
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
