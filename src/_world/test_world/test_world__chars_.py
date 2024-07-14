from src._world.char import CharID, charlink_shop, charunit_shop
from src._world.beliefbox import (
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


def test_WorldUnit_set_char_CorrectlySets_chars_beliefs():
    # GIVEN
    x_bit = 5
    yao_world = worldunit_shop("Yao", _bit=x_bit)
    yao_world.calc_world_metrics()
    assert len(yao_world._chars) == 0
    assert len(yao_world._beliefs) == 0

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
    assert len(yao_world._beliefs) == 3
    assert yao_world._beliefs["Zia"]._char_mirror == True

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


def test_WorldUnit_get_char_belief_ids_ReturnsCorrectObj():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"
    yao_world.set_charunit(charunit_shop(zia_text))
    yao_world.set_charunit(charunit_shop(sue_text))
    yao_world.set_charunit(charunit_shop(xio_text))

    # WHEN / THEN
    assert yao_world.get_char_belief_ids(sue_text) == [sue_text]

    # WHEN / THEN
    swimmers = ",swimmers"
    swim_belief = beliefbox_shop(belief_id=swimmers)
    swim_belief.set_charlink(charlink_shop(sue_text))
    yao_world.set_beliefbox(swim_belief)
    assert yao_world.get_char_belief_ids(sue_text) == [sue_text, swimmers]


def test_WorldUnit_edit_charunit_char_id_CorrectlyModifiesCharUnit_char_id():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    yao_world.add_charunit(zia_text, credor_weight=13)
    yao_world.add_charunit("Sue")
    yao_world.add_charunit("Xio", credor_weight=17)
    assert len(yao_world._chars) == 3
    assert yao_world.get_char(zia_text) != None
    assert yao_world.get_char(zia_text).credor_weight == 13
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefbox(zia_text) != None
    assert yao_world.get_beliefbox(zia_text)._char_mirror == True

    # WHEN
    beto_text = "beta"
    yao_world.edit_charunit_char_id(
        old_char_id=zia_text,
        new_char_id=beto_text,
        allow_char_overwite=False,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_world.get_char(beto_text) != None
    assert yao_world.get_char(beto_text).credor_weight == 13
    assert yao_world.get_char(zia_text) is None
    assert len(yao_world._chars) == 3
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefbox(zia_text) is None
    assert yao_world.get_beliefbox(beto_text) != None
    assert yao_world.get_beliefbox(beto_text)._char_mirror == True


def test_WorldUnit_CharUnit_raiseErrorNewchar_idPreviouslyExists():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    yao_world.add_charunit(zia_text, credor_weight=13)
    sue_text = "Sue"
    yao_world.add_charunit(sue_text)
    yao_world.add_charunit("Xio", credor_weight=17)
    assert len(yao_world._chars) == 3
    assert yao_world.get_char(zia_text) != None
    assert yao_world.get_char(zia_text).credor_weight == 13
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefbox(zia_text) != None
    assert yao_world.get_beliefbox(zia_text)._char_mirror == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_charunit_char_id(
            old_char_id=zia_text,
            new_char_id=sue_text,
            allow_char_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Char '{zia_text}' modify to '{sue_text}' failed since '{sue_text}' exists."
    )


def test_WorldUnit_CharUnit_CorrectlyModifiesBeliefBoxCharLinks():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"
    yao_world.add_charunit(zia_text, credor_weight=13)
    yao_world.add_charunit(sue_text)
    yao_world.add_charunit(xio_text, credor_weight=17)

    swim_text = ",swimmers"
    sue_char_dict = {sue_text: charlink_shop(sue_text)}
    swim_belief = beliefbox_shop(belief_id=swim_text, _chars=sue_char_dict)
    swim_belief.set_charlink(charlink_shop(sue_text, credor_weight=5, debtor_weight=18))
    swim_belief.set_charlink(charlink_shop(zia_text, credor_weight=7, debtor_weight=30))
    yao_world.set_beliefbox(y_beliefbox=swim_belief)

    swim_belief = yao_world.get_beliefbox(swim_text)
    assert len(swim_belief._chars) == 2
    assert swim_belief.get_charlink(zia_text) != None
    assert swim_belief.get_charlink(zia_text).credor_weight == 7
    assert swim_belief.get_charlink(zia_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    yao_world.edit_charunit_char_id(
        old_char_id=zia_text,
        new_char_id=beto_text,
        allow_char_overwite=False,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert swim_belief.get_charlink(beto_text) != None
    assert swim_belief.get_charlink(beto_text).credor_weight == 7
    assert swim_belief.get_charlink(beto_text).debtor_weight == 30
    assert swim_belief.get_charlink(zia_text) is None
    assert len(swim_belief._chars) == 2


def test_WorldUnit_CharUnit_CorrectlyMergeschar_ids():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"
    yao_world.add_charunit(zia_text, credor_weight=13)
    yao_world.add_charunit(sue_text, credor_weight=3)
    yao_world.add_charunit(xio_text, credor_weight=17)

    swim_text = ",swimmers"
    sue_char_dict = {sue_text: charlink_shop(sue_text)}
    swim_belief = beliefbox_shop(belief_id=swim_text, _chars=sue_char_dict)
    swim_belief.set_charlink(
        charlink=charlink_shop(sue_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_charlink(
        charlink=charlink_shop(zia_text, credor_weight=7, debtor_weight=30)
    )
    yao_world.set_beliefbox(y_beliefbox=swim_belief)

    assert len(yao_world._chars) == 3
    assert yao_world.get_char(zia_text) != None
    assert yao_world.get_char(zia_text).credor_weight == 13
    assert yao_world.get_char(sue_text) != None
    assert yao_world.get_char(sue_text).credor_weight == 3

    # WHEN / THEN
    yao_world.edit_charunit_char_id(
        old_char_id=zia_text,
        new_char_id=sue_text,
        allow_char_overwite=True,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_world.get_char(sue_text) != None
    assert yao_world.get_char(sue_text).credor_weight == 16
    assert yao_world.get_char(zia_text) is None
    assert len(yao_world._chars) == 2


def test_WorldUnit_CharUnit_CorrectlyMergesBeliefBoxCharLinks():
    # GIVEN
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"
    yao_world.add_charunit(zia_text, credor_weight=13)
    yao_world.add_charunit(sue_text)
    yao_world.add_charunit(xio_text, credor_weight=17)

    swim_text = ",swimmers"
    sue_char_dict = {sue_text: charlink_shop(sue_text)}
    swim_belief = beliefbox_shop(belief_id=swim_text, _chars=sue_char_dict)
    swim_belief.set_charlink(
        charlink=charlink_shop(sue_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_charlink(
        charlink=charlink_shop(zia_text, credor_weight=7, debtor_weight=30)
    )
    yao_world.set_beliefbox(y_beliefbox=swim_belief)

    swim_belief = yao_world.get_beliefbox(swim_text)
    assert len(swim_belief._chars) == 2
    assert swim_belief.get_charlink(zia_text) != None
    assert swim_belief.get_charlink(zia_text).credor_weight == 7
    assert swim_belief.get_charlink(zia_text).debtor_weight == 30
    assert swim_belief.get_charlink(sue_text) != None
    assert swim_belief.get_charlink(sue_text).credor_weight == 5
    assert swim_belief.get_charlink(sue_text).debtor_weight == 18

    # WHEN
    yao_world.edit_charunit_char_id(
        old_char_id=zia_text,
        new_char_id=sue_text,
        allow_char_overwite=True,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert swim_belief.get_charlink(sue_text) != None
    assert swim_belief.get_charlink(sue_text).credor_weight == 12
    assert swim_belief.get_charlink(sue_text).debtor_weight == 48
    assert swim_belief.get_charlink(zia_text) is None
    assert len(swim_belief._chars) == 1


def test_WorldUnit_CharUnit_raiseErrorNewCharIDBeliefBoxPreviouslyExists():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    yao_world.add_charunit(zia_text, credor_weight=13)
    anna_text = "anna"
    yao_world.add_charunit(anna_text, credor_weight=17)
    sue_text = ",sue"
    sue_belief = beliefbox_shop(belief_id=sue_text)
    sue_belief.set_charlink(charlink=charlink_shop(zia_text))
    sue_belief.set_charlink(charlink=charlink_shop(anna_text))
    yao_world.set_beliefbox(y_beliefbox=sue_belief)
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_char(sue_text) is None
    assert yao_world.get_beliefbox(sue_text)._char_mirror is False
    assert len(yao_world.get_beliefbox(sue_text)._chars) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_charunit_char_id(
            old_char_id=zia_text,
            new_char_id=sue_text,
            allow_char_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Char '{zia_text}' modify to '{sue_text}' failed since non-single belief '{sue_text}' exists."
    )


# def test_WorldUnit_CharUnit_CorrectlyOverwriteNewCharIDBeliefBox():
#     # GIVEN
#     yao_world = worldunit_shop("Yao")
#     zia_text = "Zia"
#     yao_world.add_charunit(zia_text, credor_weight=13)
#     anna_text = "anna"
#     yao_world.add_charunit(anna_text, credor_weight=17)
#     sue_text = ",sue"
#     sue_belief = beliefbox_shop(belief_id=sue_text)
#     sue_belief.set_charlink(
#         charlink=charlink_shop(zia_text, credor_weight=3)
#     )
#     sue_belief.set_charlink(
#         charlink=charlink_shop(anna_text, credor_weight=5)
#     )
#     yao_world.set_beliefbox(y_beliefbox=sue_belief)
#     assert len(yao_world._beliefs) == 3
#     assert yao_world.get_char(zia_text) != None
#     assert yao_world.get_char(sue_text) is None
#     assert yao_world.get_beliefbox(sue_text)._char_mirror is False
#     assert len(yao_world.get_beliefbox(sue_text)._chars) == 2
#     assert (
#         yao_world.get_beliefbox(sue_text)._chars.get(anna_text).credor_weight
#         == 5
#     )
#     assert (
#         yao_world.get_beliefbox(sue_text)._chars.get(zia_text).credor_weight
#         == 3
#     )

#     # WHEN
#     yao_world.edit_charunit_char_id(
#         old_zia_text,
#         new_sue_text,
#         allow_char_overwite=False,
#         allow_nonsingle_belief_overwrite=True,
#     )

#     assert len(yao_world._beliefs) == 2
#     assert yao_world.get_char(zia_text) is None
#     assert yao_world.get_char(sue_text) != None
#     assert yao_world.get_beliefbox(sue_text)._char_mirror == True
#     assert len(yao_world.get_beliefbox(sue_text)._chars) == 1
#     assert yao_world.get_beliefbox(sue_text)._chars.get(zia_text) is None
#     assert (
#         yao_world.get_beliefbox(sue_text)._chars.get(sue_text).credor_weight
#         == 1
#     )


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


def test_WorldUnit_is_charunits_credor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"
    zia_credor_weight = 20
    sue_credor_weight = 30
    xio_credor_weight = 50
    yao_world.set_charunit(charunit_shop(zia_text, zia_credor_weight))
    yao_world.set_charunit(charunit_shop(sue_text, sue_credor_weight))
    yao_world.set_charunit(charunit_shop(xio_text, xio_credor_weight))
    # print(f"{yao_world._chars.keys()=}")
    # for x_charunit in yao_world._chars.values():
    #     print(f"{x_charunit.credor_weight=}")

    # WHEN / THEN
    assert yao_world.is_charunits_credor_weight_sum_correct()
    yao_world.set_char_credor_pool(13)
    assert yao_world.is_charunits_credor_weight_sum_correct() is False
    # WHEN / THEN
    yao_char_cred_pool = zia_credor_weight + sue_credor_weight + xio_credor_weight
    yao_world.set_char_credor_pool(yao_char_cred_pool)
    assert yao_world.is_charunits_credor_weight_sum_correct()


def test_WorldUnit_is_charunits_debtor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"
    zia_debtor_weight = 15
    sue_debtor_weight = 25
    xio_debtor_weight = 60
    yao_world.set_charunit(charunit_shop(zia_text, None, zia_debtor_weight))
    yao_world.set_charunit(charunit_shop(sue_text, None, sue_debtor_weight))
    yao_world.set_charunit(charunit_shop(xio_text, None, xio_debtor_weight))

    # WHEN / THEN
    yao_char_debt_pool = zia_debtor_weight + sue_debtor_weight + xio_debtor_weight
    assert yao_world.is_charunits_debtor_weight_sum_correct()
    yao_world.set_char_debtor_pool(yao_char_debt_pool + 1)
    assert yao_world.is_charunits_debtor_weight_sum_correct() is False
    # WHEN / THEN
    yao_world.set_char_debtor_pool(yao_char_debt_pool)
    assert yao_world.is_charunits_debtor_weight_sum_correct()
