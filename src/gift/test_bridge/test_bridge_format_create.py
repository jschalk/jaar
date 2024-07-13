from src._road.jaar_refer import sue_str, bob_str, yao_str
from src._world.beliefbox import beliefbox_shop
from src._world.char import charlink_shop
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.gift.bridge import (
    jaar_format_0001_char_v0_0_0,
    jaar_format_0002_belieflink_v0_0_0,
    jaar_format_0003_ideaunit_v0_0_0,
    get_bridge_attribute_dict,
    create_bridge,
    real_id_str,
    owner_id_str,
    char_id_str,
    belief_id_str,
    parent_road_str,
    label_str,
    weight_str,
    pledge_str,
    char_pool_str,
    debtor_weight_str,
    credor_weight_str,
)


def test_create_bridge_Arg_jaar_format_0001_char_v0_0_0():
    # GIVEN
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    music_pool = 100
    sue_credor_weight = 11
    bob_credor_weight = 13
    yao_credor_weight = music_pool - sue_credor_weight - bob_credor_weight
    sue_debtor_weight = 23
    bob_debtor_weight = 29
    yao_debtor_weight = music_pool - sue_debtor_weight - bob_debtor_weight
    music_real_id = "music56"
    sue_worldunit = worldunit_shop(sue_text, music_real_id)
    sue_worldunit.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)
    sue_worldunit.add_charunit(bob_text, bob_credor_weight, bob_debtor_weight)
    sue_worldunit.add_charunit(yao_text, yao_credor_weight, yao_debtor_weight)
    sue_worldunit.set_char_pool(music_pool)

    # WHEN
    x_bridge = jaar_format_0001_char_v0_0_0()
    char_dataframe = create_bridge(sue_worldunit, x_bridge)

    # THEN
    array_headers = list(char_dataframe.columns)
    bridge_dict = get_bridge_attribute_dict(x_bridge)
    assert array_headers == list(bridge_dict.keys())
    assert char_dataframe.loc[0, real_id_str()] == music_real_id
    assert char_dataframe.loc[0, owner_id_str()] == sue_worldunit._owner_id
    assert char_dataframe.loc[0, char_pool_str()] == music_pool
    assert char_dataframe.loc[0, char_id_str()] == bob_text
    assert char_dataframe.loc[0, credor_weight_str()] == bob_credor_weight
    assert char_dataframe.loc[0, debtor_weight_str()] == bob_debtor_weight

    assert char_dataframe.loc[1, real_id_str()] == music_real_id
    assert char_dataframe.loc[1, owner_id_str()] == sue_worldunit._owner_id
    assert char_dataframe.loc[1, char_pool_str()] == music_pool
    assert char_dataframe.loc[1, char_id_str()] == sue_text
    assert char_dataframe.loc[1, credor_weight_str()] == sue_credor_weight
    assert char_dataframe.loc[1, debtor_weight_str()] == sue_debtor_weight

    assert char_dataframe.loc[2, real_id_str()] == music_real_id
    assert char_dataframe.loc[2, owner_id_str()] == sue_worldunit._owner_id
    assert char_dataframe.loc[2, char_pool_str()] == music_pool
    assert char_dataframe.loc[2, char_id_str()] == yao_text
    assert char_dataframe.loc[2, credor_weight_str()] == yao_credor_weight
    assert char_dataframe.loc[2, debtor_weight_str()] == yao_debtor_weight

    assert len(char_dataframe) == 3


def test_create_bridge_Arg_jaar_format_0002_belieflink_v0_0_0():
    # GIVEN
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    music_real_id = "music56"
    sue_worldunit = worldunit_shop(sue_text, music_real_id)
    sue_worldunit.add_charunit(sue_text)
    sue_worldunit.add_charunit(bob_text)
    sue_worldunit.add_charunit(yao_text)
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
    iowa_beliefbox = beliefbox_shop(iowa_text)
    ohio_beliefbox = beliefbox_shop(ohio_text)
    sue_iowa_charlink = charlink_shop(sue_text, sue_iowa_credor_w, sue_iowa_debtor_w)
    bob_iowa_charlink = charlink_shop(bob_text, bob_iowa_credor_w, bob_iowa_debtor_w)
    yao_iowa_charlink = charlink_shop(yao_text, yao_iowa_credor_w, yao_iowa_debtor_w)
    yao_ohio_charlink = charlink_shop(yao_text, yao_ohio_credor_w, yao_ohio_debtor_w)
    iowa_beliefbox.set_charlink(sue_iowa_charlink)
    iowa_beliefbox.set_charlink(bob_iowa_charlink)
    iowa_beliefbox.set_charlink(yao_iowa_charlink)
    ohio_beliefbox.set_charlink(yao_ohio_charlink)
    sue_worldunit.set_beliefbox(iowa_beliefbox)
    sue_worldunit.set_beliefbox(ohio_beliefbox)

    # WHEN
    x_bridge = jaar_format_0002_belieflink_v0_0_0()
    belieflink_dataframe = create_bridge(sue_worldunit, x_bridge)

    # THEN
    array_headers = list(belieflink_dataframe.columns)
    bridge_dict = get_bridge_attribute_dict(x_bridge)
    assert array_headers == list(bridge_dict.keys())
    assert belieflink_dataframe.loc[0, real_id_str()] == music_real_id
    assert belieflink_dataframe.loc[0, owner_id_str()] == sue_worldunit._owner_id
    assert belieflink_dataframe.loc[0, char_id_str()] == bob_text
    assert belieflink_dataframe.loc[0, belief_id_str()] == iowa_text
    assert belieflink_dataframe.loc[0, credor_weight_str()] == bob_iowa_credor_w
    assert belieflink_dataframe.loc[0, debtor_weight_str()] == bob_iowa_debtor_w

    assert belieflink_dataframe.loc[1, real_id_str()] == music_real_id
    assert belieflink_dataframe.loc[1, owner_id_str()] == sue_worldunit._owner_id
    assert belieflink_dataframe.loc[1, char_id_str()] == sue_text
    assert belieflink_dataframe.loc[1, belief_id_str()] == iowa_text
    assert belieflink_dataframe.loc[1, credor_weight_str()] == sue_iowa_credor_w
    assert belieflink_dataframe.loc[1, debtor_weight_str()] == sue_iowa_debtor_w

    assert belieflink_dataframe.loc[2, real_id_str()] == music_real_id
    assert belieflink_dataframe.loc[2, owner_id_str()] == sue_worldunit._owner_id
    assert belieflink_dataframe.loc[2, char_id_str()] == yao_text
    assert belieflink_dataframe.loc[2, belief_id_str()] == iowa_text
    assert belieflink_dataframe.loc[2, credor_weight_str()] == yao_iowa_credor_w
    assert belieflink_dataframe.loc[2, debtor_weight_str()] == yao_iowa_debtor_w

    assert belieflink_dataframe.loc[3, real_id_str()] == music_real_id
    assert belieflink_dataframe.loc[3, owner_id_str()] == sue_worldunit._owner_id
    assert belieflink_dataframe.loc[3, char_id_str()] == yao_text
    assert belieflink_dataframe.loc[3, belief_id_str()] == ohio_text
    assert belieflink_dataframe.loc[3, credor_weight_str()] == yao_ohio_credor_w
    assert belieflink_dataframe.loc[3, debtor_weight_str()] == yao_ohio_debtor_w
    assert len(belieflink_dataframe) == 4


def test_create_bridge_Arg_jaar_format_0003_ideaunit_v0_0_0():
    # GIVEN
    sue_text = sue_str()
    bob_text = bob_str()
    music_real_id = "music56"
    sue_worldunit = worldunit_shop(sue_text, music_real_id)
    casa_text = "casa"
    casa_road = sue_worldunit.make_l1_road(casa_text)
    casa_weight = 31
    sue_worldunit.add_l1_idea(ideaunit_shop(casa_text, _weight=casa_weight))
    clean_text = "clean"
    clean_road = sue_worldunit.make_road(casa_road, clean_text)
    sue_worldunit.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)

    # WHEN
    x_bridge = jaar_format_0003_ideaunit_v0_0_0()
    ideaunit_format = create_bridge(sue_worldunit, x_bridge)

    # THEN
    array_headers = list(ideaunit_format.columns)
    assert array_headers == list(get_bridge_attribute_dict(x_bridge).keys())

    assert ideaunit_format.loc[0, owner_id_str()] == sue_worldunit._owner_id
    assert ideaunit_format.loc[0, pledge_str()] == ""
    assert ideaunit_format.loc[0, real_id_str()] == music_real_id
    assert ideaunit_format.loc[0, parent_road_str()] == music_real_id
    assert ideaunit_format.loc[0, label_str()] == casa_text
    assert ideaunit_format.loc[0, weight_str()] == casa_weight

    assert ideaunit_format.loc[1, owner_id_str()] == sue_worldunit._owner_id
    assert ideaunit_format.loc[1, pledge_str()] == "Yes"
    assert ideaunit_format.loc[1, real_id_str()] == music_real_id
    assert ideaunit_format.loc[1, parent_road_str()] == casa_road
    assert ideaunit_format.loc[1, label_str()] == clean_text
    assert ideaunit_format.loc[1, weight_str()] == 1

    assert len(ideaunit_format) == 2
