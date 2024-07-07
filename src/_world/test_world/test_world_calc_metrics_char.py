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
    fiscallink_shop,
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


def test_WorldUnit_calc_world_metrics_CorrectlySetsCharLinkWorldCredAndDebt():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_charunit(charunit=charunit_shop(CharID(rico_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(carm_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(patr_text)))
    bl_rico = fiscallink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = fiscallink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = fiscallink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_world._idearoot.set_fiscallink(fiscallink=bl_rico)
    yao_world._idearoot.set_fiscallink(fiscallink=bl_carm)
    yao_world._idearoot.set_fiscallink(fiscallink=bl_patr)

    rico_beliefunit = yao_world.get_beliefunit(rico_text)
    carm_beliefunit = yao_world.get_beliefunit(carm_text)
    patr_beliefunit = yao_world.get_beliefunit(patr_text)
    rico_charlink = rico_beliefunit._chars.get(rico_text)
    carm_charlink = carm_beliefunit._chars.get(carm_text)
    patr_charlink = patr_beliefunit._chars.get(patr_text)
    rico_charlink._world_cred is None
    rico_charlink._world_debt is None
    carm_charlink._world_cred is None
    carm_charlink._world_debt is None
    patr_charlink._world_cred is None
    patr_charlink._world_debt is None

    # for belief in yao_world._beliefs.values():
    #     for charlink in belief._chars.values():
    #         assert charlink._world_cred is None
    #         assert charlink._world_debt is None

    yao_world.calc_world_metrics()

    # for fiscallink in yao_world._fiscalheirs.values():
    #     print(
    #         f"{yao_world._world_importance=} {fiscallink.belief_id=} {fiscallink._world_cred=} {fiscallink._world_debt=}"
    #     )

    assert rico_charlink._world_cred == 0.5
    assert rico_charlink._world_debt == 0.8
    assert carm_charlink._world_cred == 0.25
    assert carm_charlink._world_debt == 0.1
    assert patr_charlink._world_cred == 0.25
    assert patr_charlink._world_debt == 0.1

    # charlink_world_cred_sum = 0.0
    # charlink_world_debt_sum = 0.0
    # for belief in yao_world._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._chars=}")

    #     for charlink in belief._chars.values():
    #         assert charlink._world_cred != None
    #         assert charlink._world_cred in [0.25, 0.5]
    #         assert charlink._world_debt != None
    #         assert charlink._world_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {charlink._world_importance=} {belief._world_importance=}"
    #         # )
    #         charlink_world_cred_sum += charlink._world_cred
    #         charlink_world_debt_sum += charlink._world_debt

    #         # print(f"{charlink_world_importance_sum=}")
    # assert charlink_world_cred_sum == 1.0
    # assert charlink_world_debt_sum == 1.0

    assert (
        rico_charlink._world_cred
        + carm_charlink._world_cred
        + patr_charlink._world_cred
        == 1.0
    )
    assert (
        rico_charlink._world_debt
        + carm_charlink._world_debt
        + patr_charlink._world_debt
        == 1.0
    )

    # WHEN anothher pledge, check metrics are as expected
    selena_text = "selena"
    yao_world.set_charunit(charunit=charunit_shop(CharID(selena_text)))
    yao_world._idearoot.set_fiscallink(
        fiscallink=fiscallink_shop(
            belief_id=BeliefID(selena_text), credor_weight=20, debtor_weight=13
        )
    )
    yao_world.calc_world_metrics()

    # THEN
    selena_beliefunit = yao_world.get_beliefunit(selena_text)
    selena_charlink = selena_beliefunit._chars.get(selena_text)

    assert rico_charlink._world_cred != 0.25
    assert rico_charlink._world_debt != 0.8
    assert carm_charlink._world_cred != 0.25
    assert carm_charlink._world_debt != 0.1
    assert patr_charlink._world_cred != 0.5
    assert patr_charlink._world_debt != 0.1
    assert selena_charlink._world_cred != None
    assert selena_charlink._world_debt != None

    # charlink_world_cred_sum = 0.0
    # charlink_world_debt_sum = 0.0

    # for belief in yao_world._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._chars=}")

    #     for charlink in belief._chars.values():
    #         assert charlink._world_cred != None
    #         assert charlink._world_cred not in [0.25, 0.5]
    #         assert charlink._world_debt != None
    #         assert charlink._world_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {charlink._world_importance=} {belief._world_importance=}"
    #         # )
    #         charlink_world_cred_sum += charlink._world_cred
    #         charlink_world_debt_sum += charlink._world_debt

    #         # print(f"{charlink_world_importance_sum=}")
    # assert charlink_world_cred_sum == 1.0
    # assert charlink_world_debt_sum > 0.9999999
    # assert charlink_world_debt_sum < 1.00000001

    assert (
        rico_charlink._world_cred
        + carm_charlink._world_cred
        + patr_charlink._world_cred
        + selena_charlink._world_cred
        == 1.0
    )
    assert (
        rico_charlink._world_debt
        + carm_charlink._world_debt
        + patr_charlink._world_debt
        + selena_charlink._world_debt
        > 0.9999999
    )
    assert (
        rico_charlink._world_debt
        + carm_charlink._world_debt
        + patr_charlink._world_debt
        + selena_charlink._world_debt
        < 1.0
    )


def test_WorldUnit_calc_world_metrics_CorrectlySetsCharUnitWorldImportance():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    swim_text = "swim"
    yao_world.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_charunit(charunit=charunit_shop(CharID(rico_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(carm_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(patr_text)))
    bl_rico = fiscallink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = fiscallink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = fiscallink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_world._idearoot._kids.get(swim_text).set_fiscallink(fiscallink=bl_rico)
    yao_world._idearoot._kids.get(swim_text).set_fiscallink(fiscallink=bl_carm)
    yao_world._idearoot._kids.get(swim_text).set_fiscallink(fiscallink=bl_patr)

    rico_charunit = yao_world._chars.get(rico_text)
    carm_charunit = yao_world._chars.get(carm_text)
    patr_charunit = yao_world._chars.get(patr_text)

    assert rico_charunit._world_cred == 0
    assert rico_charunit._world_debt == 0
    assert carm_charunit._world_cred == 0
    assert carm_charunit._world_debt == 0
    assert patr_charunit._world_cred == 0
    assert patr_charunit._world_debt == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    charunit_world_cred_sum = 0.0
    charunit_world_debt_sum = 0.0

    assert rico_charunit._world_cred == 0.5
    assert rico_charunit._world_debt == 0.8
    assert carm_charunit._world_cred == 0.25
    assert carm_charunit._world_debt == 0.1
    assert patr_charunit._world_cred == 0.25
    assert patr_charunit._world_debt == 0.1

    assert (
        rico_charunit._world_cred
        + carm_charunit._world_cred
        + patr_charunit._world_cred
        == 1.0
    )
    assert (
        rico_charunit._world_debt
        + carm_charunit._world_debt
        + patr_charunit._world_debt
        == 1.0
    )

    # for charunit in yao_world._chars.values():
    #     assert charunit._world_cred != None
    #     assert charunit._world_cred in [0.25, 0.5]
    #     assert charunit._world_debt != None
    #     assert charunit._world_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {charunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{charunit.} {charunit._world_cred=} {charunit._world_debt=} ")
    #     # print(f"{charunit_world_cred_sum=}")
    #     # print(f"{charunit_world_debt_sum=}")
    #     charunit_world_cred_sum += charunit._world_cred
    #     charunit_world_debt_sum += charunit._world_debt

    # assert charunit_world_cred_sum == 1.0
    # assert charunit_world_debt_sum > 0.9999999
    # assert charunit_world_debt_sum < 1.00000001

    # WHEN anothher pledge, check metrics are as expected
    selena_text = "selena"
    yao_world.set_charunit(charunit=charunit_shop(CharID(selena_text)))
    yao_world._idearoot.set_fiscallink(
        fiscallink=fiscallink_shop(
            belief_id=selena_text, credor_weight=20, debtor_weight=10
        )
    )
    yao_world.calc_world_metrics()

    # THEN
    selena_charunit = yao_world._chars.get(selena_text)

    assert rico_charunit._world_cred != 0.5
    assert rico_charunit._world_debt != 0.8
    assert carm_charunit._world_cred != 0.25
    assert carm_charunit._world_debt != 0.1
    assert patr_charunit._world_cred != 0.25
    assert patr_charunit._world_debt != 0.1
    assert selena_charunit._world_cred != None
    assert selena_charunit._world_debt != None

    assert (
        rico_charunit._world_cred
        + carm_charunit._world_cred
        + patr_charunit._world_cred
        < 1.0
    )
    assert (
        rico_charunit._world_cred
        + carm_charunit._world_cred
        + patr_charunit._world_cred
        + selena_charunit._world_cred
        == 1.0
    )
    assert (
        rico_charunit._world_debt
        + carm_charunit._world_debt
        + patr_charunit._world_debt
        < 1.0
    )
    assert (
        rico_charunit._world_debt
        + carm_charunit._world_debt
        + patr_charunit._world_debt
        + selena_charunit._world_debt
        == 1.0
    )

    # charunit_world_cred_sum = 0.0
    # charunit_world_debt_sum = 0.0

    # for charunit in yao_world._chars.values():
    #     assert charunit._world_cred != None
    #     assert charunit._world_cred not in [0.25, 0.5]
    #     assert charunit._world_debt != None
    #     assert charunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {charunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{charunit.} {charunit._world_cred=} {charunit._world_debt=} ")
    #     # print(f"{charunit_world_cred_sum=}")
    #     # print(f"{charunit_world_debt_sum=}")
    #     charunit_world_cred_sum += charunit._world_cred
    #     charunit_world_debt_sum += charunit._world_debt

    # assert charunit_world_cred_sum == 1.0
    # assert charunit_world_debt_sum > 0.9999999
    # assert charunit_world_debt_sum < 1.00000001


def test_WorldUnit_calc_world_metrics_CorrectlySetsPartBeliefedLWCharUnitWorldImportance():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    swim_text = "swim"
    yao_world.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_charunit(charunit=charunit_shop(CharID(rico_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(carm_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(patr_text)))
    bl_rico = fiscallink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = fiscallink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = fiscallink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_world._idearoot._kids.get(swim_text).set_fiscallink(fiscallink=bl_rico)
    yao_world._idearoot._kids.get(swim_text).set_fiscallink(fiscallink=bl_carm)
    yao_world._idearoot._kids.get(swim_text).set_fiscallink(fiscallink=bl_patr)

    # no fiscallinks attached to this one
    hunt_text = "hunt"
    yao_world.add_l1_idea(ideaunit_shop(hunt_text, _weight=3))

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    rico_beliefunit = yao_world.get_beliefunit(rico_text)
    carm_beliefunit = yao_world.get_beliefunit(carm_text)
    patr_beliefunit = yao_world.get_beliefunit(patr_text)
    assert rico_beliefunit._world_cred != 0.5
    assert rico_beliefunit._world_debt != 0.8
    assert carm_beliefunit._world_cred != 0.25
    assert carm_beliefunit._world_debt != 0.1
    assert patr_beliefunit._world_cred != 0.25
    assert patr_beliefunit._world_debt != 0.1
    assert (
        rico_beliefunit._world_cred
        + carm_beliefunit._world_cred
        + patr_beliefunit._world_cred
        == 0.25
    )
    assert (
        rico_beliefunit._world_debt
        + carm_beliefunit._world_debt
        + patr_beliefunit._world_debt
        == 0.25
    )

    # beliefunit_world_cred_sum = 0.0
    # beliefunit_world_debt_sum = 0.0
    # for beliefunit in yao_world._beliefs.values():
    #     assert beliefunit._world_cred != None
    #     assert beliefunit._world_cred not in [0.25, 0.5]
    #     assert beliefunit._world_debt != None
    #     assert beliefunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {beliefunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{beliefunit.belief_id=} {beliefunit._world_cred=} {beliefunit._world_debt=} ")
    #     # print(f"{beliefunit_world_cred_sum=}")
    #     # print(f"{beliefunit_world_debt_sum=}")
    #     beliefunit_world_cred_sum += beliefunit._world_cred
    #     beliefunit_world_debt_sum += beliefunit._world_debt
    # assert beliefunit_world_cred_sum == 0.25
    # assert beliefunit_world_debt_sum == 0.25

    rico_charunit = yao_world._chars.get(rico_text)
    carm_charunit = yao_world._chars.get(carm_text)
    patr_charunit = yao_world._chars.get(patr_text)

    assert rico_charunit._world_cred == 0.375
    assert rico_charunit._world_debt == 0.45
    assert carm_charunit._world_cred == 0.3125
    assert carm_charunit._world_debt == 0.275
    assert patr_charunit._world_cred == 0.3125
    assert patr_charunit._world_debt == 0.275

    assert (
        rico_charunit._world_cred
        + carm_charunit._world_cred
        + patr_charunit._world_cred
        == 1.0
    )
    assert (
        rico_charunit._world_debt
        + carm_charunit._world_debt
        + patr_charunit._world_debt
        == 1.0
    )

    # charunit_world_cred_sum = 0.0
    # charunit_world_debt_sum = 0.0
    # for charunit in yao_world._chars.values():
    #     assert charunit._world_cred != None
    #     assert charunit._world_cred not in [0.25, 0.5]
    #     assert charunit._world_debt != None
    #     assert charunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {charunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{charunit.} {charunit._world_cred=} {charunit._world_debt=} ")
    #     # print(f"{charunit_world_cred_sum=}")
    #     # print(f"{charunit_world_debt_sum=}")
    #     charunit_world_cred_sum += charunit._world_cred
    #     charunit_world_debt_sum += charunit._world_debt
    # assert charunit_world_cred_sum == 1.0
    # assert charunit_world_debt_sum > 0.9999999
    # assert charunit_world_debt_sum < 1.00000001


def test_WorldUnit_calc_world_metrics_CorrectlySetsCharAttrs():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    yao_world.add_l1_idea(ideaunit_shop("swim"))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_charunit(charunit=charunit_shop(CharID(rico_text), credor_weight=8))
    yao_world.set_charunit(charunit=charunit_shop(CharID(carm_text)))
    yao_world.set_charunit(charunit=charunit_shop(CharID(patr_text)))
    rico_charunit = yao_world._chars.get(rico_text)
    carm_charunit = yao_world._chars.get(carm_text)
    patr_charunit = yao_world._chars.get(patr_text)
    assert rico_charunit._world_cred == 0
    assert rico_charunit._world_debt == 0
    assert carm_charunit._world_cred == 0
    assert carm_charunit._world_debt == 0
    assert patr_charunit._world_cred == 0
    assert patr_charunit._world_debt == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    assert (
        rico_charunit._world_cred
        + carm_charunit._world_cred
        + patr_charunit._world_cred
        == 1.0
    )
    assert (
        rico_charunit._world_debt
        + carm_charunit._world_debt
        + patr_charunit._world_debt
        == 1.0
    )
    # charunit_world_cred_sum = 0.0
    # charunit_world_debt_sum = 0.0
    # for charunit in yao_world._chars.values():
    #     assert charunit._world_cred != None
    #     assert charunit._world_cred not in [0.25, 0.5]
    #     assert charunit._world_debt != None
    #     assert charunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {charunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{charunit.} {charunit._world_cred=} {charunit._world_debt=} ")
    #     # print(f"{charunit_world_cred_sum=}")
    #     # print(f"{charunit_world_debt_sum=}")
    #     charunit_world_cred_sum += charunit._world_cred
    #     charunit_world_debt_sum += charunit._world_debt
    # assert charunit_world_cred_sum == 1.0
    # assert charunit_world_debt_sum > 0.9999999
    # assert charunit_world_debt_sum < 1.00000001


def test_WorldUnit_calc_world_metrics_RaisesErrorWhen_is_charunits_credor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_world = worldunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_credor_weight = 20
    carm_credor_weight = 30
    patr_credor_weight = 50
    yao_world.set_charunit(charunit_shop(rico_text, None, rico_credor_weight))
    yao_world.set_charunit(charunit_shop(carm_text, None, carm_credor_weight))
    yao_world.set_charunit(charunit_shop(patr_text, None, patr_credor_weight))
    assert yao_world._char_credor_pool is None
    assert yao_world.is_charunits_credor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_char_credor_pool(x_int)
    assert yao_world.is_charunits_credor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_world.calc_world_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_charunits_credor_weight_sum_correct is False. _char_credor_pool={x_int}. charunits_credor_weight_sum={yao_world.get_charunits_credor_weight_sum()}"
    )

    # WHEN / THEN
    yao_world.set_char_credor_pool(yao_world.get_charunits_credor_weight_sum())
    assert yao_world.calc_world_metrics() is None


def test_WorldUnit_calc_world_metrics_DoesNotRaiseError_char_credor_poolWhenCharSumIsZero():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    assert yao_world._char_credor_pool is None
    assert yao_world.is_charunits_credor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_char_credor_pool(x_int)

    # THEN
    assert yao_world.is_charunits_credor_weight_sum_correct()
    yao_world.calc_world_metrics()


def test_WorldUnit_calc_world_metrics_RaisesErrorWhen_is_charunits_debtor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_world = worldunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 40
    yao_world.set_charunit(charunit_shop(rico_text, rico_debtor_weight))
    yao_world.set_charunit(charunit_shop(carm_text, carm_debtor_weight))
    yao_world.set_charunit(charunit_shop(patr_text, patr_debtor_weight))
    assert yao_world._char_debtor_pool is None
    assert yao_world.is_charunits_debtor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_char_debtor_pool(x_int)
    assert yao_world.is_charunits_debtor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_world.calc_world_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_charunits_debtor_weight_sum_correct is False. _char_debtor_pool={x_int}. charunits_debtor_weight_sum={yao_world.get_charunits_debtor_weight_sum()}"
    )

    # WHEN / THEN
    yao_world.set_char_debtor_pool(yao_world.get_charunits_debtor_weight_sum())
    assert yao_world.calc_world_metrics() is None


def test_WorldUnit_calc_world_metrics_DoesNotRaiseError_char_debtor_poolWhenCharSumIsZero():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    assert yao_world._char_credor_pool is None
    assert yao_world.is_charunits_debtor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_char_debtor_pool(x_int)

    # THEN
    assert yao_world.is_charunits_debtor_weight_sum_correct()
    yao_world.calc_world_metrics()


def clear_all_charunits_beliefunits_world_agenda_cred_debt(x_world: WorldUnit):
    # DELETE world_agenda_debt and world_agenda_cred
    for beliefunit_x in x_world._beliefs.values():
        beliefunit_x.reset_world_cred_debt()
        # for charlink_x in beliefunit_x._chars.values():
        #     print(f"{beliefunit_x.belief_id=} {charlink_x.credor_weight=}  {charlink_x._world_cred:.6f} {charlink_x.debtor_weight=} {charlink_x._world_debt:.6f} {charlink_x.} ")

    # DELETE world_agenda_debt and world_agenda_cred
    for x_charunit in x_world._chars.values():
        x_charunit.reset_world_cred_debt()


@dataclass
class BeliefAgendaMetrics:
    sum_beliefunit_cred: float = 0
    sum_beliefunit_debt: float = 0
    sum_charlink_cred: float = 0
    sum_charlink_debt: float = 0
    charlink_count: int = 0

    def set_sums(self, x_world: WorldUnit):
        for beliefunit_x in x_world._beliefs.values():
            self.sum_beliefunit_cred += beliefunit_x._world_agenda_cred
            self.sum_beliefunit_debt += beliefunit_x._world_agenda_debt
            for charlink_x in beliefunit_x._chars.values():
                self.sum_charlink_cred += charlink_x._world_agenda_cred
                self.sum_charlink_debt += charlink_x._world_agenda_debt
                self.charlink_count += 1


@dataclass
class CharAgendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_sums(self, x_world: WorldUnit):
        for charunit in x_world._chars.values():
            self.sum_agenda_cred += charunit._world_agenda_cred
            self.sum_agenda_debt += charunit._world_agenda_debt
            self.sum_agenda_ratio_cred += charunit._world_agenda_ratio_cred
            self.sum_agenda_ratio_debt += charunit._world_agenda_ratio_debt


@dataclass
class FiscalAgendaMetrics:
    sum_world_agenda_importance = 0
    agenda_no_count = 0
    agenda_yes_count = 0
    agenda_no_world_i_sum = 0
    agenda_yes_world_i_sum = 0

    def set_sums(self, agenda_dict: dict[RoadUnit, IdeaUnit]):
        for agenda_item in agenda_dict.values():
            self.sum_world_agenda_importance += agenda_item._world_importance
            if agenda_item._fiscallines == {}:
                self.agenda_no_count += 1
                self.agenda_no_world_i_sum += agenda_item._world_importance
            else:
                self.agenda_yes_count += 1
                self.agenda_yes_world_i_sum += agenda_item._world_importance


def test_WorldUnit_agenda_cred_debt_IsCorrectlySet():
    # GIVEN
    x_world = examples_world_v001_with_large_agenda()
    clear_all_charunits_beliefunits_world_agenda_cred_debt(x_world=x_world)

    # TEST world_agenda_debt and world_agenda_cred are empty
    x_beliefagendametrics = BeliefAgendaMetrics()
    x_beliefagendametrics.set_sums(x_world=x_world)
    assert x_beliefagendametrics.sum_beliefunit_cred == 0
    assert x_beliefagendametrics.sum_beliefunit_debt == 0
    assert x_beliefagendametrics.sum_charlink_cred == 0
    assert x_beliefagendametrics.sum_charlink_debt == 0

    # TEST world_agenda_debt and world_agenda_cred are empty
    x_charagendametrics = CharAgendaMetrics()
    x_charagendametrics.set_sums(x_world=x_world)
    assert x_charagendametrics.sum_agenda_cred == 0
    assert x_charagendametrics.sum_agenda_debt == 0
    assert x_charagendametrics.sum_agenda_ratio_cred == 0
    assert x_charagendametrics.sum_agenda_ratio_debt == 0

    # WHEN
    agenda_dict = x_world.get_agenda_dict()

    # THEN
    assert len(agenda_dict) == 63
    x_fiscalagendametrics = FiscalAgendaMetrics()
    x_fiscalagendametrics.set_sums(agenda_dict=agenda_dict)
    # print(f"{sum_world_agenda_importance=}")
    assert x_fiscalagendametrics.agenda_no_count == 14
    assert x_fiscalagendametrics.agenda_yes_count == 49
    assert x_fiscalagendametrics.agenda_no_world_i_sum == 0.0037472680016539662
    assert x_fiscalagendametrics.agenda_yes_world_i_sum == 0.0027965049894874455
    assert are_equal(
        x_fiscalagendametrics.agenda_no_world_i_sum
        + x_fiscalagendametrics.agenda_yes_world_i_sum,
        x_fiscalagendametrics.sum_world_agenda_importance,
    )
    assert x_fiscalagendametrics.sum_world_agenda_importance == 0.006543772991141412

    x_beliefagendametrics = BeliefAgendaMetrics()
    x_beliefagendametrics.set_sums(x_world=x_world)
    assert x_beliefagendametrics.charlink_count == 81
    x_sum = 0.0027965049894874455
    assert are_equal(x_beliefagendametrics.sum_beliefunit_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_beliefunit_debt, x_sum)
    assert are_equal(x_beliefagendametrics.sum_charlink_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_charlink_debt, x_sum)
    assert are_equal(
        x_fiscalagendametrics.agenda_yes_world_i_sum,
        x_beliefagendametrics.sum_beliefunit_cred,
    )

    assert all_charunits_have_legitimate_values(x_world)

    x_charagendametrics = CharAgendaMetrics()
    x_charagendametrics.set_sums(x_world=x_world)
    assert are_equal(
        x_charagendametrics.sum_agenda_cred,
        x_fiscalagendametrics.sum_world_agenda_importance,
    )
    assert are_equal(
        x_charagendametrics.sum_agenda_debt,
        x_fiscalagendametrics.sum_world_agenda_importance,
    )
    assert are_equal(x_charagendametrics.sum_agenda_ratio_cred, 1)
    assert are_equal(x_charagendametrics.sum_agenda_ratio_debt, 1)

    # charunit_world_cred_sum = 0.0
    # charunit_world_debt_sum = 0.0

    # assert charunit_world_cred_sum == 1.0
    # assert charunit_world_debt_sum > 0.9999999
    # assert charunit_world_debt_sum < 1.00000001


def all_charunits_have_legitimate_values(x_world: WorldUnit):
    return not any(
        (
            charunit._world_cred is None
            or charunit._world_cred in [0.25, 0.5]
            or charunit._world_debt is None
            or charunit._world_debt in [0.8, 0.1]
        )
        for charunit in x_world._chars.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000000001
    return abs(x1 - x2) < e10


def test_WorldUnit_agenda_ratio_cred_debt_IsCorrectlySetWhenWorldIsEmpty():
    # GIVEN
    noa_world = worldunit_shop("Noa")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_char = charunit_shop(rico_text, credor_weight=0.5, debtor_weight=2)
    carm_char = charunit_shop(carm_text, credor_weight=1.5, debtor_weight=3)
    patr_char = charunit_shop(patr_text, credor_weight=8, debtor_weight=5)
    noa_world.set_charunit(charunit=rico_char)
    noa_world.set_charunit(charunit=carm_char)
    noa_world.set_charunit(charunit=patr_char)
    noa_world_rico_char = noa_world._chars.get(rico_text)
    noa_world_carm_char = noa_world._chars.get(carm_text)
    noa_world_patr_char = noa_world._chars.get(patr_text)

    assert noa_world_rico_char._world_agenda_cred in [0, None]
    assert noa_world_rico_char._world_agenda_debt in [0, None]
    assert noa_world_carm_char._world_agenda_cred in [0, None]
    assert noa_world_carm_char._world_agenda_debt in [0, None]
    assert noa_world_patr_char._world_agenda_cred in [0, None]
    assert noa_world_patr_char._world_agenda_debt in [0, None]
    assert noa_world_rico_char._world_agenda_ratio_cred != 0.05
    assert noa_world_rico_char._world_agenda_ratio_debt != 0.2
    assert noa_world_carm_char._world_agenda_ratio_cred != 0.15
    assert noa_world_carm_char._world_agenda_ratio_debt != 0.3
    assert noa_world_patr_char._world_agenda_ratio_cred != 0.8
    assert noa_world_patr_char._world_agenda_ratio_debt != 0.5

    # WHEN
    noa_world.calc_world_metrics()

    # THEN
    assert noa_world_rico_char._world_agenda_cred == 0
    assert noa_world_rico_char._world_agenda_debt == 0
    assert noa_world_carm_char._world_agenda_cred == 0
    assert noa_world_carm_char._world_agenda_debt == 0
    assert noa_world_patr_char._world_agenda_cred == 0
    assert noa_world_patr_char._world_agenda_debt == 0
    assert noa_world_rico_char._world_agenda_ratio_cred == 0.05
    assert noa_world_rico_char._world_agenda_ratio_debt == 0.2
    assert noa_world_carm_char._world_agenda_ratio_cred == 0.15
    assert noa_world_carm_char._world_agenda_ratio_debt == 0.3
    assert noa_world_patr_char._world_agenda_ratio_cred == 0.8
    assert noa_world_patr_char._world_agenda_ratio_debt == 0.5
