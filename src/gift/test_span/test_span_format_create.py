from src._road.jaar_refer import sue_str, bob_str, yao_str
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.gift.span import (
    jaar_format_0001_acct_v0_0_0,
    jaar_format_0002_lobbyship_v0_0_0,
    jaar_format_0003_ideaunit_v0_0_0,
    create_span,
    real_id_str,
    owner_id_str,
    acct_id_str,
    lobby_id_str,
    parent_road_str,
    label_str,
    weight_str,
    pledge_str,
    debtor_weight_str,
    credor_weight_str,
    get_spanref,
)


def test_create_span_Arg_jaar_format_0001_acct_v0_0_0():
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    sue_credor_weight = 11
    bob_credor_weight = 13
    yao_credor_weight = 41
    sue_debtor_weight = 23
    bob_debtor_weight = 29
    yao_debtor_weight = 37
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    sue_budunit.add_acctunit(sue_text, sue_credor_weight, sue_debtor_weight)
    sue_budunit.add_acctunit(bob_text, bob_credor_weight, bob_debtor_weight)
    sue_budunit.add_acctunit(yao_text, yao_credor_weight, yao_debtor_weight)

    # WHEN
    x_span_name = jaar_format_0001_acct_v0_0_0()
    acct_dataframe = create_span(sue_budunit, x_span_name)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_spanref = get_spanref(x_span_name)
    assert array_headers == acct_spanref.get_headers_list()
    assert acct_dataframe.loc[0, real_id_str()] == music_real_id
    assert acct_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[0, acct_id_str()] == bob_text
    assert acct_dataframe.loc[0, credor_weight_str()] == bob_credor_weight
    assert acct_dataframe.loc[0, debtor_weight_str()] == bob_debtor_weight

    assert acct_dataframe.loc[1, real_id_str()] == music_real_id
    assert acct_dataframe.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[1, acct_id_str()] == sue_text
    assert acct_dataframe.loc[1, credor_weight_str()] == sue_credor_weight
    assert acct_dataframe.loc[1, debtor_weight_str()] == sue_debtor_weight

    assert acct_dataframe.loc[2, real_id_str()] == music_real_id
    assert acct_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[2, acct_id_str()] == yao_text
    assert acct_dataframe.loc[2, credor_weight_str()] == yao_credor_weight
    assert acct_dataframe.loc[2, debtor_weight_str()] == yao_debtor_weight

    assert len(acct_dataframe) == 3


def test_create_span_Arg_jaar_format_0002_lobbyship_v0_0_0():
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    sue_budunit.add_acctunit(sue_text)
    sue_budunit.add_acctunit(bob_text)
    sue_budunit.add_acctunit(yao_text)
    iowa_text = ",Iowa"
    sue_iowa_credor_w = 37
    bob_iowa_credor_w = 43
    yao_iowa_credor_w = 51
    sue_iowa_debtor_w = 57
    bob_iowa_debtor_w = 61
    yao_iowa_debtor_w = 67
    ohio_text = ",Ohio"
    yao_ohio_credor_w = 73
    yao_ohio_debtor_w = 67
    sue_acctunit = sue_budunit.get_acct(sue_text)
    bob_acctunit = sue_budunit.get_acct(bob_text)
    yao_acctunit = sue_budunit.get_acct(yao_text)
    sue_acctunit.add_lobbyship(iowa_text, sue_iowa_credor_w, sue_iowa_debtor_w)
    bob_acctunit.add_lobbyship(iowa_text, bob_iowa_credor_w, bob_iowa_debtor_w)
    yao_acctunit.add_lobbyship(iowa_text, yao_iowa_credor_w, yao_iowa_debtor_w)
    yao_acctunit.add_lobbyship(ohio_text, yao_ohio_credor_w, yao_ohio_debtor_w)

    # WHEN
    x_span_name = jaar_format_0002_lobbyship_v0_0_0()
    lobbyship_dataframe = create_span(sue_budunit, x_span_name)

    # THEN
    array_headers = list(lobbyship_dataframe.columns)
    acct_spanref = get_spanref(x_span_name)
    print(f"{len(lobbyship_dataframe)=}")
    assert array_headers == acct_spanref.get_headers_list()
    assert lobbyship_dataframe.loc[0, real_id_str()] == music_real_id
    assert lobbyship_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert lobbyship_dataframe.loc[0, acct_id_str()] == bob_text
    assert lobbyship_dataframe.loc[0, lobby_id_str()] == iowa_text
    assert lobbyship_dataframe.loc[0, credor_weight_str()] == bob_iowa_credor_w
    assert lobbyship_dataframe.loc[0, debtor_weight_str()] == bob_iowa_debtor_w

    assert lobbyship_dataframe.loc[2, real_id_str()] == music_real_id
    assert lobbyship_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert lobbyship_dataframe.loc[2, acct_id_str()] == sue_text
    assert lobbyship_dataframe.loc[2, lobby_id_str()] == iowa_text
    assert lobbyship_dataframe.loc[2, credor_weight_str()] == sue_iowa_credor_w
    assert lobbyship_dataframe.loc[2, debtor_weight_str()] == sue_iowa_debtor_w

    assert lobbyship_dataframe.loc[4, real_id_str()] == music_real_id
    assert lobbyship_dataframe.loc[4, owner_id_str()] == sue_budunit._owner_id
    assert lobbyship_dataframe.loc[4, acct_id_str()] == yao_text
    assert lobbyship_dataframe.loc[4, lobby_id_str()] == iowa_text
    assert lobbyship_dataframe.loc[4, credor_weight_str()] == yao_iowa_credor_w
    assert lobbyship_dataframe.loc[4, debtor_weight_str()] == yao_iowa_debtor_w

    assert lobbyship_dataframe.loc[5, real_id_str()] == music_real_id
    assert lobbyship_dataframe.loc[5, owner_id_str()] == sue_budunit._owner_id
    assert lobbyship_dataframe.loc[5, acct_id_str()] == yao_text
    assert lobbyship_dataframe.loc[5, lobby_id_str()] == ohio_text
    assert lobbyship_dataframe.loc[5, credor_weight_str()] == yao_ohio_credor_w
    assert lobbyship_dataframe.loc[5, debtor_weight_str()] == yao_ohio_debtor_w
    assert len(lobbyship_dataframe) == 7


def test_create_span_Arg_jaar_format_0003_ideaunit_v0_0_0():
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    casa_weight = 31
    sue_budunit.add_l1_idea(ideaunit_shop(casa_text, _weight=casa_weight))
    clean_text = "clean"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    sue_budunit.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)

    # WHEN
    x_span_name = jaar_format_0003_ideaunit_v0_0_0()
    ideaunit_format = create_span(sue_budunit, x_span_name)

    # THEN
    array_headers = list(ideaunit_format.columns)
    assert array_headers == get_spanref(x_span_name).get_headers_list()

    assert ideaunit_format.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert ideaunit_format.loc[0, pledge_str()] == ""
    assert ideaunit_format.loc[0, real_id_str()] == music_real_id
    assert ideaunit_format.loc[0, label_str()] == casa_text
    assert ideaunit_format.loc[0, weight_str()] == casa_weight
    assert ideaunit_format.loc[0, parent_road_str()] == music_real_id

    assert ideaunit_format.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert ideaunit_format.loc[1, pledge_str()] == "Yes"
    assert ideaunit_format.loc[1, real_id_str()] == music_real_id
    assert ideaunit_format.loc[1, parent_road_str()] == casa_road
    assert ideaunit_format.loc[1, label_str()] == clean_text
    assert ideaunit_format.loc[1, weight_str()] == 1

    assert len(ideaunit_format) == 2
