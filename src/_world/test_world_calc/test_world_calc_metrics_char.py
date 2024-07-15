from src._road.road import RoadUnit
from src._world.char import charunit_shop
from src._world.beliefstory import awardlink_shop
from src._world.examples.example_worlds import (
    world_v001 as examples_world_v001,
    world_v001_with_large_agenda as examples_world_v001_with_large_agenda,
)
from src._world.world import WorldUnit, worldunit_shop
from src._world.idea import ideaunit_shop, IdeaUnit
from pytest import raises as pytest_raises
from dataclasses import dataclass


def test_WorldUnit_calc_world_metrics_CorrectlySetsCharLinkWorldCredAndDebt():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_world.set_charunit(charunit_shop(sue_text))
    yao_world.set_charunit(charunit_shop(bob_text))
    yao_world.set_charunit(charunit_shop(zia_text))
    bl_sue = awardlink_shop(sue_text, 20, debtor_weight=40)
    bl_bob = awardlink_shop(bob_text, 10, debtor_weight=5)
    bl_zia = awardlink_shop(zia_text, 10, debtor_weight=5)
    yao_world._idearoot.set_awardlink(bl_sue)
    yao_world._idearoot.set_awardlink(bl_bob)
    yao_world._idearoot.set_awardlink(bl_zia)

    sue_beliefbox = yao_world.get_beliefbox(sue_text)
    bob_beliefbox = yao_world.get_beliefbox(bob_text)
    zia_beliefbox = yao_world.get_beliefbox(zia_text)
    sue_charlink = sue_beliefbox._chars.get(sue_text)
    bob_charlink = bob_beliefbox._chars.get(bob_text)
    zia_charlink = zia_beliefbox._chars.get(zia_text)
    sue_charlink._world_cred is None
    sue_charlink._world_debt is None
    bob_charlink._world_cred is None
    bob_charlink._world_debt is None
    zia_charlink._world_cred is None
    zia_charlink._world_debt is None

    # for belief in yao_world._beliefs.values():
    #     for charlink in belief._chars.values():
    #         assert charlink._world_cred is None
    #         assert charlink._world_debt is None

    yao_world.calc_world_metrics()

    # for awardlink in yao_world._awardheirs.values():
    #     print(
    #         f"{yao_world._bud_share=} {awardlink.} {awardlink._world_cred=} {awardlink._world_debt=}"
    #     )

    assert sue_charlink._world_cred == 0.5
    assert sue_charlink._world_debt == 0.8
    assert bob_charlink._world_cred == 0.25
    assert bob_charlink._world_debt == 0.1
    assert zia_charlink._world_cred == 0.25
    assert zia_charlink._world_debt == 0.1

    # charlink_world_cred_sum = 0.0
    # charlink_world_debt_sum = 0.0
    # for belief in yao_world._beliefs.values():
    #     # print(f"{belief.} {belief._chars=}")

    #     for charlink in belief._chars.values():
    #         assert charlink._world_cred != None
    #         assert charlink._world_cred in [0.25, 0.5]
    #         assert charlink._world_debt != None
    #         assert charlink._world_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.} {charlink._bud_share=} {belief._bud_share=}"
    #         # )
    #         charlink_world_cred_sum += charlink._world_cred
    #         charlink_world_debt_sum += charlink._world_debt

    #         # print(f"{charlink_bud_share_sum=}")
    # assert charlink_world_cred_sum == 1.0
    # assert charlink_world_debt_sum == 1.0

    assert (
        sue_charlink._world_cred + bob_charlink._world_cred + zia_charlink._world_cred
        == 1.0
    )
    assert (
        sue_charlink._world_debt + bob_charlink._world_debt + zia_charlink._world_debt
        == 1.0
    )

    # WHEN anothher pledge, check metrics are as expected
    selena_text = "selena"
    yao_world.set_charunit(charunit_shop(selena_text))
    yao_world._idearoot.set_awardlink(awardlink_shop(selena_text, 20, debtor_weight=13))
    yao_world.calc_world_metrics()

    # THEN
    selena_beliefbox = yao_world.get_beliefbox(selena_text)
    selena_charlink = selena_beliefbox._chars.get(selena_text)

    assert sue_charlink._world_cred != 0.25
    assert sue_charlink._world_debt != 0.8
    assert bob_charlink._world_cred != 0.25
    assert bob_charlink._world_debt != 0.1
    assert zia_charlink._world_cred != 0.5
    assert zia_charlink._world_debt != 0.1
    assert selena_charlink._world_cred != None
    assert selena_charlink._world_debt != None

    # charlink_world_cred_sum = 0.0
    # charlink_world_debt_sum = 0.0

    # for belief in yao_world._beliefs.values():
    #     # print(f"{belief.} {belief._chars=}")

    #     for charlink in belief._chars.values():
    #         assert charlink._world_cred != None
    #         assert charlink._world_cred not in [0.25, 0.5]
    #         assert charlink._world_debt != None
    #         assert charlink._world_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.} {charlink._bud_share=} {belief._bud_share=}"
    #         # )
    #         charlink_world_cred_sum += charlink._world_cred
    #         charlink_world_debt_sum += charlink._world_debt

    #         # print(f"{charlink_bud_share_sum=}")
    # assert charlink_world_cred_sum == 1.0
    # assert charlink_world_debt_sum > 0.9999999
    # assert charlink_world_debt_sum < 1.00000001

    assert (
        sue_charlink._world_cred
        + bob_charlink._world_cred
        + zia_charlink._world_cred
        + selena_charlink._world_cred
        == 1.0
    )
    assert (
        sue_charlink._world_debt
        + bob_charlink._world_debt
        + zia_charlink._world_debt
        + selena_charlink._world_debt
        > 0.9999999
    )
    assert (
        sue_charlink._world_debt
        + bob_charlink._world_debt
        + zia_charlink._world_debt
        + selena_charlink._world_debt
        < 1.0
    )


def test_WorldUnit_calc_world_metrics_CorrectlySetsCharUnitWorldImportance():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    swim_text = "swim"
    yao_world.add_l1_idea(ideaunit_shop(swim_text))
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_world.set_charunit(charunit_shop(sue_text))
    yao_world.set_charunit(charunit_shop(bob_text))
    yao_world.set_charunit(charunit_shop(zia_text))
    bl_sue = awardlink_shop(sue_text, 20, debtor_weight=40)
    bl_bob = awardlink_shop(bob_text, 10, debtor_weight=5)
    bl_zia = awardlink_shop(zia_text, 10, debtor_weight=5)
    yao_world._idearoot._kids.get(swim_text).set_awardlink(bl_sue)
    yao_world._idearoot._kids.get(swim_text).set_awardlink(bl_bob)
    yao_world._idearoot._kids.get(swim_text).set_awardlink(bl_zia)

    sue_charunit = yao_world.get_char(sue_text)
    bob_charunit = yao_world.get_char(bob_text)
    zia_charunit = yao_world.get_char(zia_text)

    assert sue_charunit._world_cred == 0
    assert sue_charunit._world_debt == 0
    assert bob_charunit._world_cred == 0
    assert bob_charunit._world_debt == 0
    assert zia_charunit._world_cred == 0
    assert zia_charunit._world_debt == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    charunit_world_cred_sum = 0.0
    charunit_world_debt_sum = 0.0

    assert sue_charunit._world_cred == 0.5
    assert sue_charunit._world_debt == 0.8
    assert bob_charunit._world_cred == 0.25
    assert bob_charunit._world_debt == 0.1
    assert zia_charunit._world_cred == 0.25
    assert zia_charunit._world_debt == 0.1

    assert (
        sue_charunit._world_cred + bob_charunit._world_cred + zia_charunit._world_cred
        == 1.0
    )
    assert (
        sue_charunit._world_debt + bob_charunit._world_debt + zia_charunit._world_debt
        == 1.0
    )

    # for charunit in yao_world._chars.values():
    #     assert charunit._world_cred != None
    #     assert charunit._world_cred in [0.25, 0.5]
    #     assert charunit._world_debt != None
    #     assert charunit._world_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.} {charunit._world_credor=} {belief._world_credor=}"
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
    yao_world.set_charunit(charunit_shop(selena_text))
    yao_world._idearoot.set_awardlink(awardlink_shop(selena_text, 20, debtor_weight=10))
    yao_world.calc_world_metrics()

    # THEN
    selena_charunit = yao_world.get_char(selena_text)

    assert sue_charunit._world_cred != 0.5
    assert sue_charunit._world_debt != 0.8
    assert bob_charunit._world_cred != 0.25
    assert bob_charunit._world_debt != 0.1
    assert zia_charunit._world_cred != 0.25
    assert zia_charunit._world_debt != 0.1
    assert selena_charunit._world_cred != None
    assert selena_charunit._world_debt != None

    assert (
        sue_charunit._world_cred + bob_charunit._world_cred + zia_charunit._world_cred
        < 1.0
    )
    assert (
        sue_charunit._world_cred
        + bob_charunit._world_cred
        + zia_charunit._world_cred
        + selena_charunit._world_cred
        == 1.0
    )
    assert (
        sue_charunit._world_debt + bob_charunit._world_debt + zia_charunit._world_debt
        < 1.0
    )
    assert (
        sue_charunit._world_debt
        + bob_charunit._world_debt
        + zia_charunit._world_debt
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
    #     #     f"{belief.} {charunit._world_credor=} {belief._world_credor=}"
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
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_world.set_charunit(charunit_shop(sue_text))
    yao_world.set_charunit(charunit_shop(bob_text))
    yao_world.set_charunit(charunit_shop(zia_text))
    bl_sue = awardlink_shop(sue_text, 20, debtor_weight=40)
    bl_bob = awardlink_shop(bob_text, 10, debtor_weight=5)
    bl_zia = awardlink_shop(zia_text, 10, debtor_weight=5)
    yao_world._idearoot._kids.get(swim_text).set_awardlink(bl_sue)
    yao_world._idearoot._kids.get(swim_text).set_awardlink(bl_bob)
    yao_world._idearoot._kids.get(swim_text).set_awardlink(bl_zia)

    # no awardlinks attached to this one
    hunt_text = "hunt"
    yao_world.add_l1_idea(ideaunit_shop(hunt_text, _weight=3))

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    sue_beliefbox = yao_world.get_beliefbox(sue_text)
    bob_beliefbox = yao_world.get_beliefbox(bob_text)
    zia_beliefbox = yao_world.get_beliefbox(zia_text)
    assert sue_beliefbox._world_cred != 0.5
    assert sue_beliefbox._world_debt != 0.8
    assert bob_beliefbox._world_cred != 0.25
    assert bob_beliefbox._world_debt != 0.1
    assert zia_beliefbox._world_cred != 0.25
    assert zia_beliefbox._world_debt != 0.1
    assert (
        sue_beliefbox._world_cred
        + bob_beliefbox._world_cred
        + zia_beliefbox._world_cred
        == 0.25
    )
    assert (
        sue_beliefbox._world_debt
        + bob_beliefbox._world_debt
        + zia_beliefbox._world_debt
        == 0.25
    )

    # beliefbox_world_cred_sum = 0.0
    # beliefbox_world_debt_sum = 0.0
    # for beliefbox in yao_world._beliefs.values():
    #     assert beliefbox._world_cred != None
    #     assert beliefbox._world_cred not in [0.25, 0.5]
    #     assert beliefbox._world_debt != None
    #     assert beliefbox._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.} {beliefbox._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{beliefbox.} {beliefbox._world_cred=} {beliefbox._world_debt=} ")
    #     # print(f"{beliefbox_world_cred_sum=}")
    #     # print(f"{beliefbox_world_debt_sum=}")
    #     beliefbox_world_cred_sum += beliefbox._world_cred
    #     beliefbox_world_debt_sum += beliefbox._world_debt
    # assert beliefbox_world_cred_sum == 0.25
    # assert beliefbox_world_debt_sum == 0.25

    sue_charunit = yao_world.get_char(sue_text)
    bob_charunit = yao_world.get_char(bob_text)
    zia_charunit = yao_world.get_char(zia_text)

    assert sue_charunit._world_cred == 0.375
    assert sue_charunit._world_debt == 0.45
    assert bob_charunit._world_cred == 0.3125
    assert bob_charunit._world_debt == 0.275
    assert zia_charunit._world_cred == 0.3125
    assert zia_charunit._world_debt == 0.275

    assert (
        sue_charunit._world_cred + bob_charunit._world_cred + zia_charunit._world_cred
        == 1.0
    )
    assert (
        sue_charunit._world_debt + bob_charunit._world_debt + zia_charunit._world_debt
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
    #     #     f"{belief.} {charunit._world_credor=} {belief._world_credor=}"
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
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_world.set_charunit(charunit_shop(sue_text, 8))
    yao_world.set_charunit(charunit_shop(bob_text))
    yao_world.set_charunit(charunit_shop(zia_text))
    sue_charunit = yao_world.get_char(sue_text)
    bob_charunit = yao_world.get_char(bob_text)
    zia_charunit = yao_world.get_char(zia_text)
    assert sue_charunit._world_cred == 0
    assert sue_charunit._world_debt == 0
    assert bob_charunit._world_cred == 0
    assert bob_charunit._world_debt == 0
    assert zia_charunit._world_cred == 0
    assert zia_charunit._world_debt == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    assert (
        sue_charunit._world_cred + bob_charunit._world_cred + zia_charunit._world_cred
        == 1.0
    )
    assert (
        sue_charunit._world_debt + bob_charunit._world_debt + zia_charunit._world_debt
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
    #     #     f"{belief.} {charunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{charunit.} {charunit._world_cred=} {charunit._world_debt=} ")
    #     # print(f"{charunit_world_cred_sum=}")
    #     # print(f"{charunit_world_debt_sum=}")
    #     charunit_world_cred_sum += charunit._world_cred
    #     charunit_world_debt_sum += charunit._world_debt
    # assert charunit_world_cred_sum == 1.0
    # assert charunit_world_debt_sum > 0.9999999
    # assert charunit_world_debt_sum < 1.00000001


# def test_WorldUnit_calc_world_metrics_DoesNotRaiseError_credor_respectWhenCharSumIsZero():
#     # GIVEN
#     yao_world = worldunit_shop("Yao")
#     assert yao_world._credor_respect is None
#     assert yao_world.is_charunits_credor_weight_sum_correct()
#     assert yao_world.calc_world_metrics() is None

#     # WHEN
#     x_int = 13
#     yao_world.set_credor_respect(x_int)

#     # THEN
#     assert yao_world.is_charunits_credor_weight_sum_correct()
#     yao_world.calc_world_metrics()


# def test_WorldUnit_calc_world_metrics_DoesNotRaiseError_debtor_respectWhenCharSumIsZero():
#     # GIVEN
#     yao_world = worldunit_shop("Yao")
#     assert yao_world._credor_respect is None
#     assert yao_world.is_charunits_debtor_weight_sum_correct()
#     assert yao_world.calc_world_metrics() is None

#     # WHEN
#     x_int = 13
#     yao_world.set_debtor_resepect(x_int)

#     # THEN
#     assert yao_world.is_charunits_debtor_weight_sum_correct()
#     yao_world.calc_world_metrics()


def clear_all_charunits_beliefboxs_world_agenda_cred_debt(x_world: WorldUnit):
    # DELETE world_agenda_debt and world_agenda_cred
    for beliefbox_x in x_world._beliefs.values():
        beliefbox_x.reset_world_cred_debt()
        # for charlink_x in beliefbox_x._chars.values():
        #     print(f"{beliefbox_x.} {charlink_x.}  {charlink_x._world_cred:.6f} {charlink_x.debtor_weight=} {charlink_x._world_debt:.6f} {charlink_x.} ")

    # DELETE world_agenda_debt and world_agenda_cred
    for x_charunit in x_world._chars.values():
        x_charunit.reset_world_cred_debt()


@dataclass
class BeliefAgendaMetrics:
    sum_beliefbox_cred: float = 0
    sum_beliefbox_debt: float = 0
    sum_charlink_cred: float = 0
    sum_charlink_debt: float = 0
    charlink_count: int = 0

    def set_sums(self, x_world: WorldUnit):
        for beliefbox_x in x_world._beliefs.values():
            self.sum_beliefbox_cred += beliefbox_x._world_agenda_cred
            self.sum_beliefbox_debt += beliefbox_x._world_agenda_debt
            for charlink_x in beliefbox_x._chars.values():
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
class AwardAgendaMetrics:
    sum_world_agenda_share = 0
    agenda_no_count = 0
    agenda_yes_count = 0
    agenda_no_world_i_sum = 0
    agenda_yes_world_i_sum = 0

    def set_sums(self, agenda_dict: dict[RoadUnit, IdeaUnit]):
        for agenda_item in agenda_dict.values():
            self.sum_world_agenda_share += agenda_item._bud_ratio
            if agenda_item._awardlines == {}:
                self.agenda_no_count += 1
                self.agenda_no_world_i_sum += agenda_item._bud_ratio
            else:
                self.agenda_yes_count += 1
                self.agenda_yes_world_i_sum += agenda_item._bud_ratio


def test_WorldUnit_agenda_cred_debt_IsCorrectlySet():
    # GIVEN
    x_world = examples_world_v001_with_large_agenda()
    clear_all_charunits_beliefboxs_world_agenda_cred_debt(x_world=x_world)

    # TEST world_agenda_debt and world_agenda_cred are empty
    x_beliefagendametrics = BeliefAgendaMetrics()
    x_beliefagendametrics.set_sums(x_world=x_world)
    assert x_beliefagendametrics.sum_beliefbox_cred == 0
    assert x_beliefagendametrics.sum_beliefbox_debt == 0
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
    x_awardagendametrics = AwardAgendaMetrics()
    x_awardagendametrics.set_sums(agenda_dict=agenda_dict)
    # print(f"{sum_world_agenda_share=}")
    assert x_awardagendametrics.agenda_no_count == 14
    assert x_awardagendametrics.agenda_yes_count == 49
    assert x_awardagendametrics.agenda_no_world_i_sum == 0.0037472699999999996
    assert x_awardagendametrics.agenda_yes_world_i_sum == 0.002796505000000001
    assert are_equal(
        x_awardagendametrics.agenda_no_world_i_sum
        + x_awardagendametrics.agenda_yes_world_i_sum,
        x_awardagendametrics.sum_world_agenda_share,
    )
    assert x_awardagendametrics.sum_world_agenda_share == 0.006543775000000002

    x_beliefagendametrics = BeliefAgendaMetrics()
    x_beliefagendametrics.set_sums(x_world=x_world)
    assert x_beliefagendametrics.charlink_count == 81
    x_sum = 0.0027965049894874455
    assert are_equal(x_beliefagendametrics.sum_beliefbox_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_beliefbox_debt, x_sum)
    assert are_equal(x_beliefagendametrics.sum_charlink_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_charlink_debt, x_sum)
    assert are_equal(
        x_awardagendametrics.agenda_yes_world_i_sum,
        x_beliefagendametrics.sum_beliefbox_cred,
    )

    assert all_charunits_have_legitimate_values(x_world)

    x_charagendametrics = CharAgendaMetrics()
    x_charagendametrics.set_sums(x_world=x_world)
    assert are_equal(
        x_charagendametrics.sum_agenda_cred,
        x_awardagendametrics.sum_world_agenda_share,
    )
    assert are_equal(
        x_charagendametrics.sum_agenda_debt,
        x_awardagendametrics.sum_world_agenda_share,
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
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    sue_charunit = charunit_shop(sue_text, 0.5, debtor_weight=2)
    bob_charunit = charunit_shop(bob_text, 1.5, debtor_weight=3)
    zia_charunit = charunit_shop(zia_text, 8, debtor_weight=5)
    noa_world.set_charunit(sue_charunit)
    noa_world.set_charunit(bob_charunit)
    noa_world.set_charunit(zia_charunit)
    noa_world_sue_char = noa_world.get_char(sue_text)
    noa_world_bob_char = noa_world.get_char(bob_text)
    noa_world_zia_char = noa_world.get_char(zia_text)

    assert noa_world_sue_char._world_agenda_cred in [0, None]
    assert noa_world_sue_char._world_agenda_debt in [0, None]
    assert noa_world_bob_char._world_agenda_cred in [0, None]
    assert noa_world_bob_char._world_agenda_debt in [0, None]
    assert noa_world_zia_char._world_agenda_cred in [0, None]
    assert noa_world_zia_char._world_agenda_debt in [0, None]
    assert noa_world_sue_char._world_agenda_ratio_cred != 0.05
    assert noa_world_sue_char._world_agenda_ratio_debt != 0.2
    assert noa_world_bob_char._world_agenda_ratio_cred != 0.15
    assert noa_world_bob_char._world_agenda_ratio_debt != 0.3
    assert noa_world_zia_char._world_agenda_ratio_cred != 0.8
    assert noa_world_zia_char._world_agenda_ratio_debt != 0.5

    # WHEN
    noa_world.calc_world_metrics()

    # THEN
    assert noa_world_sue_char._world_agenda_cred == 0
    assert noa_world_sue_char._world_agenda_debt == 0
    assert noa_world_bob_char._world_agenda_cred == 0
    assert noa_world_bob_char._world_agenda_debt == 0
    assert noa_world_zia_char._world_agenda_cred == 0
    assert noa_world_zia_char._world_agenda_debt == 0
    assert noa_world_sue_char._world_agenda_ratio_cred == 0.05
    assert noa_world_sue_char._world_agenda_ratio_debt == 0.2
    assert noa_world_bob_char._world_agenda_ratio_cred == 0.15
    assert noa_world_bob_char._world_agenda_ratio_debt == 0.3
    assert noa_world_zia_char._world_agenda_ratio_cred == 0.8
    assert noa_world_zia_char._world_agenda_ratio_debt == 0.5


def test_examples_world_v001_has_chars():
    # GIVEN / WHEN
    yao_world = examples_world_v001()

    # THEN
    assert yao_world._chars != None
    assert len(yao_world._chars) == 22


def test_examples_world_v001_HasBeliefs():
    # GIVEN / WHEN
    x_world = examples_world_v001()

    # THEN
    assert x_world._beliefs != None
    assert len(x_world._beliefs) == 34
    everyone_chars_len = None
    everyone_belief = x_world.get_beliefbox(",Everyone")
    everyone_chars_len = len(everyone_belief._chars)
    assert everyone_chars_len == 22

    # WHEN
    x_world.calc_world_metrics()
    idea_dict = x_world._idea_dict

    # THEN
    print(f"{len(idea_dict)=}")
    db_idea = idea_dict.get(x_world.make_l1_road("D&B"))
    print(f"{db_idea._label=} {db_idea._awardlinks=}")
    assert len(db_idea._awardlinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._label == "D&B":
    #         print(f"{idea._label=} {idea._awardlinks=}")
    #         db_awardlink_len = len(idea._awardlinks)
    # assert db_awardlink_len == 3
