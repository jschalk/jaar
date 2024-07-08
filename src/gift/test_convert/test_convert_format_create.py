from src._road.jaar_refer import sue_str, bob_str, yao_str
from src._world.beliefunit import beliefunit_shop
from src._world.char import charlink_shop
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.gift.convert import (
    jaar_format_0001_char_v0_0_0,
    jaar_format_0002_beliefhold_v0_0_0,
    jaar_format_0003_ideaunit_v0_0_0,
    get_convert_format_dict,
    create_convert_format,
)


def test_create_convert_format_Arg_jaar_format_0001_char_v0_0_0():
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
    x_convert_format = jaar_format_0001_char_v0_0_0()
    music_array2d_format = create_convert_format(sue_worldunit, x_convert_format)

    # THEN
    array_headers = music_array2d_format[0]
    convert_format_dict = get_convert_format_dict(x_convert_format)
    assert array_headers == list(convert_format_dict.keys())
    array_bob = music_array2d_format[1]
    assert array_bob[0] == music_real_id
    assert array_bob[1] == sue_worldunit._owner_id
    assert array_bob[2] == music_pool
    assert array_bob[3] == bob_text
    assert array_bob[4] == bob_credor_weight
    assert array_bob[5] == bob_debtor_weight

    array_sue = music_array2d_format[2]
    assert array_sue[0] == music_real_id
    assert array_sue[1] == sue_worldunit._owner_id
    assert array_sue[2] == music_pool
    assert array_sue[3] == sue_text
    assert array_sue[4] == sue_credor_weight
    assert array_sue[5] == sue_debtor_weight

    array_yao = music_array2d_format[3]
    assert array_yao[0] == music_real_id
    assert array_yao[1] == sue_worldunit._owner_id
    assert array_yao[2] == music_pool
    assert array_yao[3] == yao_text
    assert array_yao[4] == yao_credor_weight
    assert array_yao[5] == yao_debtor_weight

    assert len(music_array2d_format) == 4


# def test_create_convert_format_Arg_jaar_format_0002_beliefhold_v0_0_0():
#     # GIVEN
#     sue_text = sue_str()
#     bob_text = bob_str()
#     yao_text = yao_str()
#     music_real_id = "music56"
#     sue_worldunit = worldunit_shop(sue_text, music_real_id)
#     sue_worldunit.add_charunit(sue_text)
#     sue_worldunit.add_charunit(bob_text)
#     sue_worldunit.add_charunit(yao_text)
#     iowa_text = ",Iowa"
#     sue_iowa_credor_w = 37
#     bob_iowa_credor_w = 43
#     yao_iowa_credor_w = 51
#     sue_iowa_debtor_w = 57
#     bob_iowa_debtor_w = 61
#     yao_iowa_debtor_w = 67
#     ohio_text = ",Ohio"
#     yao_ohio_credor_w = 73
#     yao_ohio_debtor_w = 67
#     iowa_beliefunit = beliefunit_shop(iowa_text)
#     ohio_beliefunit = beliefunit_shop(ohio_text)
#     sue_iowa_charlink = charlink_shop(sue_text, sue_iowa_credor_w, sue_iowa_debtor_w)
#     bob_iowa_charlink = charlink_shop(bob_text, bob_iowa_credor_w, bob_iowa_debtor_w)
#     yao_iowa_charlink = charlink_shop(yao_text, yao_iowa_credor_w, yao_iowa_debtor_w)
#     yao_ohio_charlink = charlink_shop(yao_text, yao_ohio_credor_w, yao_ohio_debtor_w)
#     iowa_beliefunit.set_charlink(sue_iowa_charlink)
#     iowa_beliefunit.set_charlink(bob_iowa_charlink)
#     iowa_beliefunit.set_charlink(yao_iowa_charlink)
#     ohio_beliefunit.set_charlink(yao_ohio_charlink)
#     sue_worldunit.set_beliefunit(iowa_beliefunit)
#     sue_worldunit.set_beliefunit(ohio_beliefunit)

#     # WHEN
#     x_convert_format = jaar_format_0002_beliefhold_v0_0_0()
#     music_array2d_format = create_convert_format(sue_worldunit, x_convert_format)

#     # THEN
#     array_headers = music_array2d_format[0]
#     convert_format_dict = get_convert_format_dict(x_convert_format)
#     assert array_headers == list(convert_format_dict.keys())
#     array_bob_iowa = music_array2d_format[1]
#     assert array_bob_iowa[0] == music_real_id
#     assert array_bob_iowa[1] == sue_worldunit._owner_id
#     assert array_bob_iowa[2] == bob_text
#     assert array_bob_iowa[3] == iowa_text
#     assert array_bob_iowa[4] == bob_iowa_credor_w
#     assert array_bob_iowa[5] == bob_iowa_debtor_w

#     array_sue_iowa = music_array2d_format[2]
#     assert array_sue_iowa[0] == music_real_id
#     assert array_sue_iowa[1] == sue_worldunit._owner_id
#     assert array_sue_iowa[2] == sue_text
#     assert array_sue_iowa[3] == iowa_text
#     assert array_sue_iowa[4] == sue_iowa_credor_w
#     assert array_sue_iowa[5] == sue_iowa_debtor_w

#     array_yao_iowa = music_array2d_format[3]
#     assert array_yao_iowa[0] == music_real_id
#     assert array_yao_iowa[1] == sue_worldunit._owner_id
#     assert array_yao_iowa[2] == yao_text
#     assert array_yao_iowa[3] == iowa_text
#     assert array_yao_iowa[4] == yao_iowa_credor_w
#     assert array_yao_iowa[5] == yao_iowa_debtor_w

#     array_yao_ohio = music_array2d_format[4]
#     assert array_yao_ohio[0] == music_real_id
#     assert array_yao_ohio[1] == sue_worldunit._owner_id
#     assert array_yao_ohio[2] == yao_text
#     assert array_yao_ohio[3] == ohio_text
#     assert array_yao_ohio[4] == yao_ohio_credor_w
#     assert array_yao_ohio[5] == yao_ohio_debtor_w

#     assert len(music_array2d_format) == 5


# def test_create_convert_format_Arg_jaar_format_0003_ideaunit_v0_0_0():
#     # GIVEN
#     sue_text = sue_str()
#     bob_text = bob_str()
#     yao_text = yao_str()
#     music_real_id = "music56"
#     sue_worldunit = worldunit_shop(sue_text, music_real_id)
#     casa_text = "casa"
#     casa_road = sue_worldunit.make_l1_road(casa_text)
#     casa_weight = 31
#     sue_worldunit.add_l1_idea(ideaunit_shop(casa_text, _weight=casa_weight))
#     clean_text = "clean"
#     clean_road = sue_worldunit.make_road(casa_road, clean_text)
#     sue_worldunit.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)

#     # WHEN
#     x_convert_format = jaar_format_0003_ideaunit_v0_0_0()
#     music_array2d_format = create_convert_format(sue_worldunit, x_convert_format)

#     # THEN
#     array_headers = music_array2d_format[0]
#     convert_format_dict = get_convert_format_dict(x_convert_format)
#     assert array_headers == list(convert_format_dict.keys())

#     # idearoot_array = music_array2d_format[1]
#     # idearoot = sue_worldunit.get_idea_obj(music_real_id)
#     # assert idearoot_array[0] == music_real_id
#     # assert idearoot_array[1] == sue_worldunit._owner_id
#     # assert idearoot_array[2] == idearoot.get_road()
#     # assert idearoot_array[3] == idearoot._weight
#     # assert idearoot_array[4] == ""

#     casa_ideaunit_array = music_array2d_format[1]
#     casa_ideaunit_obj = sue_worldunit.get_idea_obj(casa_road)
#     assert casa_ideaunit_array[0] == music_real_id
#     assert casa_ideaunit_array[1] == sue_worldunit._owner_id
#     assert casa_ideaunit_array[2] == casa_ideaunit_obj.get_road()
#     assert casa_ideaunit_array[3] == casa_ideaunit_obj._weight
#     assert casa_ideaunit_array[3] == casa_weight
#     assert casa_ideaunit_array[4] == ""

#     clean_ideaunit_array = music_array2d_format[2]
#     clean_ideaunit_obj = sue_worldunit.get_idea_obj(clean_road)
#     assert clean_ideaunit_array[0] == music_real_id
#     assert clean_ideaunit_array[1] == sue_worldunit._owner_id
#     assert clean_ideaunit_array[2] == clean_ideaunit_obj.get_road()
#     assert clean_ideaunit_array[3] == clean_ideaunit_obj._weight
#     assert clean_ideaunit_array[4] == "Yes"

#     assert len(music_array2d_format) == 3
