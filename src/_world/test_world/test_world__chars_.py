from src._road.road import RoadUnit
from src._world.char import (
    CharID,
    charlink_shop,
    charunit_shop,
    CharUnitExternalMetrics,
)
from src._world.beliefunit import (
    BeliefID,
    beliefunit_shop,
    awardlink_shop,
    get_intersection_of_chars,
)
from src._world.examples.example_worlds import (
    world_v001 as examples_world_v001,
    world_v001_with_large_agenda as examples_world_v001_with_large_agenda,
)
from src._world.world import WorldUnit, worldunit_shop
from src._world.idea import ideaunit_shop, IdeaUnit
from pytest import raises as pytest_raises
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


def test_WorldUnit_set_charunit_SetObjCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_charunit = charunit_shop(yao_text)
    deepcopy_yao_charunit = copy_deepcopy(yao_charunit)
    slash_text = "/"
    bob_world = worldunit_shop("Bob", _road_delimiter=slash_text)

    # WHEN
    bob_world.set_charunit(charunit=yao_charunit)

    # THEN
    assert bob_world._chars.get(yao_text)._road_delimiter == slash_text
    x_chars = {yao_charunit.char_id: deepcopy_yao_charunit}
    assert bob_world._chars != x_chars
    deepcopy_yao_charunit._road_delimiter = bob_world._road_delimiter
    assert bob_world._chars == x_chars


def test_examples_world_v001_has_chars():
    # GIVEN / WHEN
    yao_world = examples_world_v001()

    # THEN
    assert yao_world._chars != None
    assert len(yao_world._chars) == 22


def test_WorldUnit_set_char_CorrectlySets_chars_beliefs():
    # GIVEN
    x_pixel = 0.5
    yao_world = worldunit_shop("Yao", _pixel=x_pixel)
    yao_world.calc_world_metrics()
    assert len(yao_world._chars) == 0
    assert len(yao_world._beliefs) == 0

    # WHEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_charunit(charunit=charunit_shop(CharID(rico_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(carm_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(patr_text)))

    # THEN
    assert yao_world._chars.get(rico_text)._pixel == x_pixel
    assert len(yao_world._chars) == 3
    assert len(yao_world._beliefs) == 3
    assert yao_world._beliefs["rico"]._char_mirror == True

    # WHEN
    rico_belief = rico_text
    carm_belief = carm_text
    patr_belief = patr_text
    yao_world._idearoot.set_awardlink(awardlink_shop(rico_belief, credor_weight=10))
    yao_world._idearoot.set_awardlink(awardlink_shop(carm_belief, credor_weight=10))
    yao_world._idearoot.set_awardlink(awardlink_shop(patr_belief, credor_weight=10))
    assert len(yao_world._idearoot._awardlinks) == 3


def test_WorldUnit_add_charunit_CorrectlySets_chars():
    # GIVEN
    x_pixel = 0.5
    yao_world = worldunit_shop("Yao", _pixel=x_pixel)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    # WHEN
    yao_world.add_charunit(rico_text, credor_weight=13, debtor_weight=8)
    yao_world.add_charunit(carm_text, debtor_weight=5)
    yao_world.add_charunit(patr_text, credor_weight=17)

    # THEN
    assert len(yao_world._chars) == 3
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefunit(rico_text)._char_mirror == True
    assert yao_world._chars.get(patr_text).credor_weight == 17
    assert yao_world._chars.get(carm_text).debtor_weight == 5
    assert yao_world._chars.get(patr_text)._pixel == x_pixel


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


def test_WorldUnit_set_char_CorrectlyUpdate_char_mirror_BeliefUnit():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    before_rico_credor = 7
    before_rico_debtor = 17
    yao_world.add_charunit(rico_text, before_rico_credor, before_rico_debtor)
    rico_beliefunit = yao_world.get_beliefunit(rico_text)
    rico_charlink = rico_beliefunit.get_charlink(rico_text)
    assert rico_charlink.credor_weight != before_rico_credor
    assert rico_charlink.debtor_weight != before_rico_debtor
    assert rico_charlink.credor_weight == 1
    assert rico_charlink.debtor_weight == 1

    # WHEN
    after_rico_credor = 11
    after_rico_debtor = 13
    yao_world.set_charunit(
        charunit_shop(rico_text, after_rico_credor, after_rico_debtor)
    )

    # THEN
    assert rico_charlink.credor_weight != after_rico_credor
    assert rico_charlink.debtor_weight != after_rico_debtor
    assert rico_charlink.credor_weight == 1
    assert rico_charlink.debtor_weight == 1


def test_WorldUnit_edit_char_RaiseExceptionWhenCharDoesNotExist():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    rico_credor_weight = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_charunit(rico_text, credor_weight=rico_credor_weight)
    assert str(excinfo.value) == f"CharUnit '{rico_text}' does not exist."


def test_WorldUnit_edit_char_CorrectlyUpdatesObj():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    old_rico_credor_weight = 55
    old_rico_debtor_weight = 66
    yao_world.set_charunit(
        charunit_shop(
            rico_text,
            old_rico_credor_weight,
            old_rico_debtor_weight,
        )
    )
    rico_charunit = yao_world.get_char(rico_text)
    assert rico_charunit.credor_weight == old_rico_credor_weight
    assert rico_charunit.debtor_weight == old_rico_debtor_weight

    # WHEN
    new_rico_credor_weight = 22
    new_rico_debtor_weight = 33
    yao_world.edit_charunit(
        char_id=rico_text,
        credor_weight=new_rico_credor_weight,
        debtor_weight=new_rico_debtor_weight,
    )

    # THEN
    assert rico_charunit.credor_weight == new_rico_credor_weight
    assert rico_charunit.debtor_weight == new_rico_debtor_weight


def test_WorldUnit_get_char_ReturnsCorrectObj():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    yao_world.add_charunit(rico_text)
    yao_world.add_charunit(carm_text)

    # WHEN
    rico_char = yao_world.get_char(rico_text)
    carm_char = yao_world.get_char(carm_text)

    # THEN
    assert rico_char == yao_world._chars.get(rico_text)
    assert carm_char == yao_world._chars.get(carm_text)


def test_WorldUnit_get_char_belief_ids_ReturnsCorrectObj():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_charunit(charunit=charunit_shop(CharID(rico_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(carm_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(patr_text)))

    # WHEN / THEN
    assert yao_world.get_char_belief_ids(carm_text) == [carm_text]

    # WHEN / THEN
    swimmers = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swimmers)
    swim_belief.set_charlink(charlink_shop(carm_text))
    yao_world.set_beliefunit(swim_belief)
    assert yao_world.get_char_belief_ids(carm_text) == [carm_text, swimmers]


def test_WorldUnit_edit_charunit_char_id_CorrectlyModifiesCharUnit_char_id():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    yao_world.add_charunit(rico_text, credor_weight=13)
    yao_world.add_charunit("carmen")
    yao_world.add_charunit("patrick", credor_weight=17)
    assert len(yao_world._chars) == 3
    assert yao_world._chars.get(rico_text) != None
    assert yao_world._chars.get(rico_text).credor_weight == 13
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefunit(rico_text) != None
    assert yao_world.get_beliefunit(rico_text)._char_mirror == True

    # WHEN
    beto_text = "beta"
    yao_world.edit_charunit_char_id(
        old_char_id=rico_text,
        new_char_id=beto_text,
        allow_char_overwite=False,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_world._chars.get(beto_text) != None
    assert yao_world._chars.get(beto_text).credor_weight == 13
    assert yao_world._chars.get(rico_text) is None
    assert len(yao_world._chars) == 3
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefunit(rico_text) is None
    assert yao_world.get_beliefunit(beto_text) != None
    assert yao_world.get_beliefunit(beto_text)._char_mirror == True


def test_WorldUnit_CharUnit_raiseErrorNewchar_idPreviouslyExists():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    yao_world.add_charunit(rico_text, credor_weight=13)
    carmen_text = "carmen"
    yao_world.add_charunit(carmen_text)
    yao_world.add_charunit("patrick", credor_weight=17)
    assert len(yao_world._chars) == 3
    assert yao_world._chars.get(rico_text) != None
    assert yao_world._chars.get(rico_text).credor_weight == 13
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefunit(rico_text) != None
    assert yao_world.get_beliefunit(rico_text)._char_mirror == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_charunit_char_id(
            old_char_id=rico_text,
            new_char_id=carmen_text,
            allow_char_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Char '{rico_text}' modify to '{carmen_text}' failed since '{carmen_text}' exists."
    )


def test_WorldUnit_CharUnit_CorrectlyModifiesBeliefUnitCharLinks():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.add_charunit(rico_text, credor_weight=13)
    yao_world.add_charunit(carm_text)
    yao_world.add_charunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_char_dict = {CharID(carm_text): charlink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _chars=carmen_char_dict)
    swim_belief.set_charlink(
        charlink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_charlink(
        charlink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_world.set_beliefunit(y_beliefunit=swim_belief)

    swim_belief = yao_world.get_beliefunit(swim_text)
    assert len(swim_belief._chars) == 2
    assert swim_belief.get_charlink(rico_text) != None
    assert swim_belief.get_charlink(rico_text).credor_weight == 7
    assert swim_belief.get_charlink(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    yao_world.edit_charunit_char_id(
        old_char_id=rico_text,
        new_char_id=beto_text,
        allow_char_overwite=False,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert swim_belief.get_charlink(beto_text) != None
    assert swim_belief.get_charlink(beto_text).credor_weight == 7
    assert swim_belief.get_charlink(beto_text).debtor_weight == 30
    assert swim_belief.get_charlink(rico_text) is None
    assert len(swim_belief._chars) == 2


def test_WorldUnit_CharUnit_CorrectlyMergeschar_ids():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.add_charunit(rico_text, credor_weight=13)
    yao_world.add_charunit(carm_text, credor_weight=3)
    yao_world.add_charunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_char_dict = {CharID(carm_text): charlink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _chars=carmen_char_dict)
    swim_belief.set_charlink(
        charlink=charlink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_charlink(
        charlink=charlink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_world.set_beliefunit(y_beliefunit=swim_belief)

    assert len(yao_world._chars) == 3
    assert yao_world._chars.get(rico_text) != None
    assert yao_world._chars.get(rico_text).credor_weight == 13
    assert yao_world._chars.get(carm_text) != None
    assert yao_world._chars.get(carm_text).credor_weight == 3

    # WHEN / THEN
    yao_world.edit_charunit_char_id(
        old_char_id=rico_text,
        new_char_id=carm_text,
        allow_char_overwite=True,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_world._chars.get(carm_text) != None
    assert yao_world._chars.get(carm_text).credor_weight == 16
    assert yao_world._chars.get(rico_text) is None
    assert len(yao_world._chars) == 2


def test_WorldUnit_CharUnit_CorrectlyMergesBeliefUnitCharLinks():
    # GIVEN
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.add_charunit(rico_text, credor_weight=13)
    yao_world.add_charunit(carm_text)
    yao_world.add_charunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_char_dict = {CharID(carm_text): charlink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _chars=carmen_char_dict)
    swim_belief.set_charlink(
        charlink=charlink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_charlink(
        charlink=charlink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_world.set_beliefunit(y_beliefunit=swim_belief)

    swim_belief = yao_world.get_beliefunit(swim_text)
    assert len(swim_belief._chars) == 2
    assert swim_belief.get_charlink(rico_text) != None
    assert swim_belief.get_charlink(rico_text).credor_weight == 7
    assert swim_belief.get_charlink(rico_text).debtor_weight == 30
    assert swim_belief.get_charlink(carm_text) != None
    assert swim_belief.get_charlink(carm_text).credor_weight == 5
    assert swim_belief.get_charlink(carm_text).debtor_weight == 18

    # WHEN
    yao_world.edit_charunit_char_id(
        old_char_id=rico_text,
        new_char_id=carm_text,
        allow_char_overwite=True,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert swim_belief.get_charlink(carm_text) != None
    assert swim_belief.get_charlink(carm_text).credor_weight == 12
    assert swim_belief.get_charlink(carm_text).debtor_weight == 48
    assert swim_belief.get_charlink(rico_text) is None
    assert len(swim_belief._chars) == 1


def test_WorldUnit_CharUnit_raiseErrorNewCharIDBeliefUnitPreviouslyExists():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    yao_world.add_charunit(rico_text, credor_weight=13)
    anna_text = "anna"
    yao_world.add_charunit(anna_text, credor_weight=17)
    carmen_text = ",carmen"
    carmen_belief = beliefunit_shop(belief_id=carmen_text)
    carmen_belief.set_charlink(charlink=charlink_shop(rico_text))
    carmen_belief.set_charlink(charlink=charlink_shop(anna_text))
    yao_world.set_beliefunit(y_beliefunit=carmen_belief)
    assert len(yao_world._beliefs) == 3
    assert yao_world._chars.get(carmen_text) is None
    assert yao_world.get_beliefunit(carmen_text)._char_mirror is False
    assert len(yao_world.get_beliefunit(carmen_text)._chars) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_charunit_char_id(
            old_char_id=rico_text,
            new_char_id=carmen_text,
            allow_char_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Char '{rico_text}' modify to '{carmen_text}' failed since non-single belief '{carmen_text}' exists."
    )


# def test_WorldUnit_CharUnit_CorrectlyOverwriteNewCharIDBeliefUnit():
#     # GIVEN
#     yao_world = worldunit_shop("Yao")
#     rico_text = "rico"
#     yao_world.add_charunit(rico_text, credor_weight=13)
#     anna_text = "anna"
#     yao_world.add_charunit(anna_text, credor_weight=17)
#     carmen_text = ",carmen"
#     carmen_belief = beliefunit_shop(belief_id=carmen_text)
#     carmen_belief.set_charlink(
#         charlink=charlink_shop(rico_text, credor_weight=3)
#     )
#     carmen_belief.set_charlink(
#         charlink=charlink_shop(anna_text, credor_weight=5)
#     )
#     yao_world.set_beliefunit(y_beliefunit=carmen_belief)
#     assert len(yao_world._beliefs) == 3
#     assert yao_world._chars.get(rico_text) != None
#     assert yao_world._chars.get(carmen_text) is None
#     assert yao_world.get_beliefunit(carmen_text)._char_mirror is False
#     assert len(yao_world.get_beliefunit(carmen_text)._chars) == 2
#     assert (
#         yao_world.get_beliefunit(carmen_text)._chars.get(anna_text).credor_weight
#         == 5
#     )
#     assert (
#         yao_world.get_beliefunit(carmen_text)._chars.get(rico_text).credor_weight
#         == 3
#     )

#     # WHEN
#     yao_world.edit_charunit_char_id(
#         old_rico_text,
#         new_carmen_text,
#         allow_char_overwite=False,
#         allow_nonsingle_belief_overwrite=True,
#     )

#     assert len(yao_world._beliefs) == 2
#     assert yao_world._chars.get(rico_text) is None
#     assert yao_world._chars.get(carmen_text) != None
#     assert yao_world.get_beliefunit(carmen_text)._char_mirror == True
#     assert len(yao_world.get_beliefunit(carmen_text)._chars) == 1
#     assert yao_world.get_beliefunit(carmen_text)._chars.get(rico_text) is None
#     assert (
#         yao_world.get_beliefunit(carmen_text)._chars.get(carmen_text).credor_weight
#         == 1
#     )


def test_WorldUnit_get_charunits_char_id_list_ReturnsListOfCharUnits():
    # GIVEN
    noa_world = worldunit_shop("Noa")
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    noa_world.set_charunit(charunit=charunit_shop(sam_text))
    noa_world.set_charunit(charunit=charunit_shop(will_text))
    noa_world.set_charunit(charunit=charunit_shop(fry_text))
    fun_text = ",fun people"
    fun_belief = beliefunit_shop(belief_id=fun_text)
    fun_belief.set_charlink(charlink=charlink_shop(will_text))
    noa_world.set_beliefunit(y_beliefunit=fun_belief)
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
    bob_world.set_charunit(charunit=charunit_shop(bob_text))
    bob_world.set_charunit(charunit=charunit_shop(sam_text))
    bob_world.set_charunit(charunit=charunit_shop(wil_text))
    bob_world.set_charunit(charunit=charunit_shop(fry_text))

    y_world = worldunit_shop()
    y_world.set_charunit(charunit=charunit_shop(bob_text))
    y_world.set_charunit(charunit=charunit_shop(wil_text))
    y_world.set_charunit(charunit=charunit_shop(fry_text))
    y_world.set_charunit(charunit=charunit_shop(elu_text))

    # WHEN
    print(f"{len(bob_world._chars)=} {len(y_world._chars)=}")
    intersection_x = get_intersection_of_chars(bob_world._chars, y_world._chars)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}


def test_WorldUnit_is_charunits_credor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_credor_weight = 20
    carm_credor_weight = 30
    patr_credor_weight = 50
    yao_world.set_charunit(charunit_shop(rico_text, rico_credor_weight))
    yao_world.set_charunit(charunit_shop(carm_text, carm_credor_weight))
    yao_world.set_charunit(charunit_shop(patr_text, patr_credor_weight))
    # print(f"{yao_world._chars.keys()=}")
    # for x_charunit in yao_world._chars.values():
    #     print(f"{x_charunit.credor_weight=}")

    # WHEN / THEN
    assert yao_world.is_charunits_credor_weight_sum_correct()
    yao_world.set_char_credor_pool(13)
    assert yao_world.is_charunits_credor_weight_sum_correct() is False
    # WHEN / THEN
    yao_char_cred_pool = rico_credor_weight + carm_credor_weight + patr_credor_weight
    yao_world.set_char_credor_pool(yao_char_cred_pool)
    assert yao_world.is_charunits_credor_weight_sum_correct()


def test_WorldUnit_is_charunits_debtor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 60
    yao_world.set_charunit(charunit_shop(rico_text, None, rico_debtor_weight))
    yao_world.set_charunit(charunit_shop(carm_text, None, carm_debtor_weight))
    yao_world.set_charunit(charunit_shop(patr_text, None, patr_debtor_weight))

    # WHEN / THEN
    yao_char_debt_pool = rico_debtor_weight + carm_debtor_weight + patr_debtor_weight
    assert yao_world.is_charunits_debtor_weight_sum_correct()
    yao_world.set_char_debtor_pool(yao_char_debt_pool + 1)
    assert yao_world.is_charunits_debtor_weight_sum_correct() is False
    # WHEN / THEN
    yao_world.set_char_debtor_pool(yao_char_debt_pool)
    assert yao_world.is_charunits_debtor_weight_sum_correct()
