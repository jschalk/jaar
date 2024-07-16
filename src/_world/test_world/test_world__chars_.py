from src._world.char import CharID, charlink_shop, charunit_shop
from src._world.beliefstory import (
    beliefbox_shop,
    awardlink_shop,
    get_intersection_of_chars,
)
from src._world.world import worldunit_shop
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_WorldUnit_set_charunit_SetObjCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_charunit = charunit_shop(yao_text)
    yao_charunit.add_belieflink(yao_text)
    deepcopy_yao_charunit = copy_deepcopy(yao_charunit)
    slash_text = "/"
    bob_world = worldunit_shop("Bob", _road_delimiter=slash_text)

    # WHEN
    bob_world.set_charunit(yao_charunit)

    # THEN
    assert bob_world._chars.get(yao_text)._road_delimiter == slash_text
    x_chars = {yao_charunit.char_id: deepcopy_yao_charunit}
    assert bob_world._chars != x_chars
    deepcopy_yao_charunit._road_delimiter = bob_world._road_delimiter
    assert bob_world._chars == x_chars


def test_WorldUnit_set_char_DoesNotSet_char_id_belieflink():
    # GIVEN
    x_bit = 5
    yao_world = worldunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"

    # WHEN
    yao_world.set_charunit(charunit_shop(zia_text), auto_set_belieflink=False)

    # THEN
    assert yao_world.get_char(zia_text).get_belieflink(zia_text) is None


def test_WorldUnit_set_char_DoesSet_char_id_belieflink():
    # GIVEN
    x_bit = 5
    yao_world = worldunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"

    # WHEN
    yao_world.set_charunit(charunit_shop(zia_text))

    # THEN
    zia_zia_belieflink = yao_world.get_char(zia_text).get_belieflink(zia_text)
    assert zia_zia_belieflink != None
    assert zia_zia_belieflink.credor_weight == 1
    assert zia_zia_belieflink.debtor_weight == 1


def test_WorldUnit_set_char_DoesNotOverRide_char_id_belieflink():
    # GIVEN
    x_bit = 5
    yao_world = worldunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"
    ohio_text = ",Ohio"
    zia_ohio_credor_w = 33
    zia_ohio_debtor_w = 44
    zia_charunit = charunit_shop(zia_text)
    zia_charunit.add_belieflink(ohio_text, zia_ohio_credor_w, zia_ohio_debtor_w)

    # WHEN
    yao_world.set_charunit(zia_charunit)

    # THEN
    zia_ohio_belieflink = yao_world.get_char(zia_text).get_belieflink(ohio_text)
    assert zia_ohio_belieflink != None
    assert zia_ohio_belieflink.credor_weight == zia_ohio_credor_w
    assert zia_ohio_belieflink.debtor_weight == zia_ohio_debtor_w
    zia_zia_belieflink = yao_world.get_char(zia_text).get_belieflink(zia_text)
    assert zia_zia_belieflink is None


def test_WorldUnit_set_char_CorrectlySets_chars_beliefs():
    # GIVEN
    x_bit = 5
    yao_world = worldunit_shop("Yao", _bit=x_bit)
    assert len(yao_world._chars) == 0
    assert len(yao_world.get_belief_ids_dict()) == 0

    # WHEN
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"
    yao_world.set_charunit(charunit_shop(zia_text))
    yao_world.set_charunit(charunit_shop(sue_text))
    yao_world.set_charunit(charunit_shop(xio_text))

    # THEN
    assert yao_world._chars.get(zia_text)._bit == x_bit
    assert len(yao_world._chars) == 3
    assert len(yao_world.get_belief_ids_dict()) == 3

    # WHEN
    zia_belief = zia_text
    sue_belief = sue_text
    xio_belief = xio_text
    yao_world._idearoot.set_awardlink(awardlink_shop(zia_belief, credor_weight=10))
    yao_world._idearoot.set_awardlink(awardlink_shop(sue_belief, credor_weight=10))
    yao_world._idearoot.set_awardlink(awardlink_shop(xio_belief, credor_weight=10))
    assert len(yao_world._idearoot._awardlinks) == 3


def test_WorldUnit_add_charunit_CorrectlySets_chars():
    # GIVEN
    x_bit = 6
    yao_world = worldunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"

    # WHEN
    yao_world.add_charunit(zia_text, credor_weight=13, debtor_weight=8)
    yao_world.add_charunit(sue_text, debtor_weight=5)
    yao_world.add_charunit(xio_text, credor_weight=17)

    # THEN
    assert len(yao_world._chars) == 3
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefbox(zia_text)._char_mirror == True
    assert yao_world._chars.get(xio_text).credor_weight == 17
    assert yao_world._chars.get(sue_text).debtor_weight == 5
    assert yao_world._chars.get(xio_text)._bit == x_bit


def test_WorldUnit_char_exists_ReturnsObj():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    yao_text = "Yao"

    # WHEN / THEN
    assert bob_world.char_exists(yao_text) is False

    # GIVEN
    bob_world.add_charunit(yao_text)

    # WHEN / THEN
    assert bob_world.char_exists(yao_text)


def test_WorldUnit_set_char_CorrectlyUpdate_char_mirror_BeliefBox():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    before_zia_credor = 7
    before_zia_debtor = 17
    yao_world.add_charunit(zia_text, before_zia_credor, before_zia_debtor)
    zia_beliefbox = yao_world.get_beliefbox(zia_text)
    zia_charlink = zia_beliefbox.get_charlink(zia_text)
    assert zia_charlink.credor_weight != before_zia_credor
    assert zia_charlink.debtor_weight != before_zia_debtor
    assert zia_charlink.credor_weight == 1
    assert zia_charlink.debtor_weight == 1

    # WHEN
    after_zia_credor = 11
    after_zia_debtor = 13
    yao_world.set_charunit(charunit_shop(zia_text, after_zia_credor, after_zia_debtor))

    # THEN
    assert zia_charlink.credor_weight != after_zia_credor
    assert zia_charlink.debtor_weight != after_zia_debtor
    assert zia_charlink.credor_weight == 1
    assert zia_charlink.debtor_weight == 1


def test_WorldUnit_edit_char_RaiseExceptionWhenCharDoesNotExist():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    zia_credor_weight = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_charunit(zia_text, credor_weight=zia_credor_weight)
    assert str(excinfo.value) == f"CharUnit '{zia_text}' does not exist."


def test_WorldUnit_edit_char_CorrectlyUpdatesObj():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    old_zia_credor_weight = 55
    old_zia_debtor_weight = 66
    yao_world.set_charunit(
        charunit_shop(
            zia_text,
            old_zia_credor_weight,
            old_zia_debtor_weight,
        )
    )
    zia_charunit = yao_world.get_char(zia_text)
    assert zia_charunit.credor_weight == old_zia_credor_weight
    assert zia_charunit.debtor_weight == old_zia_debtor_weight

    # WHEN
    new_zia_credor_weight = 22
    new_zia_debtor_weight = 33
    yao_world.edit_charunit(
        char_id=zia_text,
        credor_weight=new_zia_credor_weight,
        debtor_weight=new_zia_debtor_weight,
    )

    # THEN
    assert zia_charunit.credor_weight == new_zia_credor_weight
    assert zia_charunit.debtor_weight == new_zia_debtor_weight


def test_WorldUnit_get_char_ReturnsCorrectObj():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    sue_text = "Sue"
    yao_world.add_charunit(zia_text)
    yao_world.add_charunit(sue_text)

    # WHEN
    zia_char = yao_world.get_char(zia_text)
    sue_char = yao_world.get_char(sue_text)

    # THEN
    assert zia_char == yao_world._chars.get(zia_text)
    assert sue_char == yao_world._chars.get(sue_text)


def test_WorldUnit_get_charunits_char_id_list_ReturnsListOfCharUnits():
    # GIVEN
    noa_world = worldunit_shop("Noa")
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    noa_world.set_charunit(charunit_shop(sam_text))
    noa_world.set_charunit(charunit_shop(will_text))
    noa_world.set_charunit(charunit_shop(fry_text))
    fun_text = ",fun people"
    fun_belief = beliefbox_shop(belief_id=fun_text)
    fun_belief.set_charlink(charlink=charlink_shop(will_text))
    noa_world.set_beliefbox(y_beliefbox=fun_belief)
    assert len(noa_world._beliefs) == 4
    assert len(noa_world._chars) == 3

    # WHEN
    charunit_list_x = noa_world.get_charunits_char_id_list()

    # THEN
    assert len(charunit_list_x) == 4
    assert charunit_list_x[0] == ""
    assert charunit_list_x[1] == fry_text
    assert charunit_list_x[2] == sam_text
    assert charunit_list_x[3] == will_text


def test_get_intersection_of_chars_ReturnsUnionOfKeysOfTwoDictionarys_scenario1():
    # GIVEN
    bob_text = "Bob"
    bob_world = worldunit_shop(bob_text)

    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "Elu"
    bob_world.set_charunit(charunit_shop(bob_text))
    bob_world.set_charunit(charunit_shop(sam_text))
    bob_world.set_charunit(charunit_shop(wil_text))
    bob_world.set_charunit(charunit_shop(fry_text))

    y_world = worldunit_shop()
    y_world.set_charunit(charunit_shop(bob_text))
    y_world.set_charunit(charunit_shop(wil_text))
    y_world.set_charunit(charunit_shop(fry_text))
    y_world.set_charunit(charunit_shop(elu_text))

    # WHEN
    print(f"{len(bob_world._chars)=} {len(y_world._chars)=}")
    intersection_x = get_intersection_of_chars(bob_world._chars, y_world._chars)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}
