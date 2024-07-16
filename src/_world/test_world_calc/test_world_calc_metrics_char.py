from src._road.road import RoadUnit
from src._world.char import charunit_shop
from src._world.beliefbox import awardlink_shop
from src._world.examples.example_worlds import (
    world_v001 as examples_world_v001,
    world_v001_with_large_agenda as examples_world_v001_with_large_agenda,
)
from src._world.world import WorldUnit, worldunit_shop
from src._world.idea import ideaunit_shop, IdeaUnit
from dataclasses import dataclass


def test_WorldUnit_set_awardlink_CorrectlyCalculatesInheritedAwardLinkWorldImportance():
    # GIVEN
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_world.set_charunit(charunit_shop(yao_text))
    sue_world.set_charunit(charunit_shop(zia_text))
    sue_world.set_charunit(charunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(yao_text, credor_weight=20, debtor_weight=6)
    zia_awardlink = awardlink_shop(zia_text, credor_weight=10, debtor_weight=1)
    Xio_awardlink = awardlink_shop(Xio_text, credor_weight=10)
    sue_world._idearoot.set_awardlink(yao_awardlink)
    sue_world._idearoot.set_awardlink(zia_awardlink)
    sue_world._idearoot.set_awardlink(Xio_awardlink)
    assert len(sue_world._idearoot._awardlinks) == 3

    # WHEN
    idea_dict = sue_world.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=}")
    idea_prom = idea_dict.get(sue_world._real_id)
    assert len(idea_prom._awardheirs) == 3

    bheir_yao = idea_prom._awardheirs.get(yao_text)
    bheir_zia = idea_prom._awardheirs.get(zia_text)
    bheir_Xio = idea_prom._awardheirs.get(Xio_text)
    assert bheir_yao._world_cred == 0.5
    assert bheir_yao._world_debt == 0.75
    assert bheir_zia._world_cred == 0.25
    assert bheir_zia._world_debt == 0.125
    assert bheir_Xio._world_cred == 0.25
    assert bheir_Xio._world_debt == 0.125
    assert bheir_yao._world_cred + bheir_zia._world_cred + bheir_Xio._world_cred == 1
    assert bheir_yao._world_debt + bheir_zia._world_debt + bheir_Xio._world_debt == 1

    # world_cred_sum = 0
    # world_debt_sum = 0
    # for belief in x_world._idearoot._awardheirs.values():
    #     print(f"{belief=}")
    #     assert belief._world_cred != None
    #     assert belief._world_cred in [0.25, 0.5]
    #     assert belief._world_debt != None
    #     assert belief._world_debt in [0.75, 0.125]
    #     world_cred_sum += belief._world_cred
    #     world_debt_sum += belief._world_debt

    # assert world_cred_sum == 1
    # assert world_debt_sum == 1


def test_WorldUnit_calc_world_metrics_CorrectlySetsBelieflinkWorldCredAndDebt():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_world.set_charunit(charunit_shop(sue_text))
    yao_world.set_charunit(charunit_shop(bob_text))
    yao_world.set_charunit(charunit_shop(zia_text))
    sue_awardlink = awardlink_shop(sue_text, 20, debtor_weight=40)
    bob_awardlink = awardlink_shop(bob_text, 10, debtor_weight=5)
    zia_awardlink = awardlink_shop(zia_text, 10, debtor_weight=5)
    yao_world.edit_idea_attr(yao_world._real_id, awardlink=sue_awardlink)
    yao_world.edit_idea_attr(yao_world._real_id, awardlink=bob_awardlink)
    yao_world.edit_idea_attr(yao_world._real_id, awardlink=zia_awardlink)

    sue_charunit = yao_world.get_char(sue_text)
    bob_charunit = yao_world.get_char(bob_text)
    zia_charunit = yao_world.get_char(zia_text)
    sue_sue_belieflink = sue_charunit.get_belieflink(sue_text)
    bob_bob_belieflink = bob_charunit.get_belieflink(bob_text)
    zia_zia_belieflink = zia_charunit.get_belieflink(zia_text)
    assert sue_sue_belieflink._world_cred is None
    assert sue_sue_belieflink._world_debt is None
    assert bob_bob_belieflink._world_cred is None
    assert bob_bob_belieflink._world_debt is None
    assert zia_zia_belieflink._world_cred is None
    assert zia_zia_belieflink._world_debt is None

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    assert sue_sue_belieflink._world_cred == 0.5
    assert sue_sue_belieflink._world_debt == 0.8
    assert bob_bob_belieflink._world_cred == 0.25
    assert bob_bob_belieflink._world_debt == 0.1
    assert zia_zia_belieflink._world_cred == 0.25
    assert zia_zia_belieflink._world_debt == 0.1

    belieflink_cred_sum = (
        sue_sue_belieflink._world_cred
        + bob_bob_belieflink._world_cred
        + zia_zia_belieflink._world_cred
    )
    assert belieflink_cred_sum == 1.0
    belieflink_debt_sum = (
        sue_sue_belieflink._world_debt
        + bob_bob_belieflink._world_debt
        + zia_zia_belieflink._world_debt
    )
    assert belieflink_debt_sum == 1.0

    # GIVEN anothher pledge, check metrics are as expected
    xio_text = "Xio"
    yao_world.set_charunit(charunit_shop(xio_text))
    yao_world._idearoot.set_awardlink(awardlink_shop(xio_text, 20, debtor_weight=13))

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    xio_beliefbox = yao_world.get_beliefbox(xio_text)
    xio_xio_belieflink = xio_beliefbox.get_belieflink(xio_text)
    sue_charunit = yao_world.get_char(sue_text)
    bob_charunit = yao_world.get_char(bob_text)
    zia_charunit = yao_world.get_char(zia_text)
    sue_sue_belieflink = sue_charunit.get_belieflink(sue_text)
    bob_bob_belieflink = bob_charunit.get_belieflink(bob_text)
    zia_zia_belieflink = zia_charunit.get_belieflink(zia_text)
    assert sue_sue_belieflink._world_cred != 0.25
    assert sue_sue_belieflink._world_debt != 0.8
    assert bob_bob_belieflink._world_cred != 0.25
    assert bob_bob_belieflink._world_debt != 0.1
    assert zia_zia_belieflink._world_cred != 0.5
    assert zia_zia_belieflink._world_debt != 0.1
    assert xio_xio_belieflink._world_cred != None
    assert xio_xio_belieflink._world_debt != None

    assert (
        sue_sue_belieflink._world_cred
        + bob_bob_belieflink._world_cred
        + zia_zia_belieflink._world_cred
        + xio_xio_belieflink._world_cred
        == 1.0
    )
    assert (
        sue_sue_belieflink._world_debt
        + bob_bob_belieflink._world_debt
        + zia_zia_belieflink._world_debt
        + xio_xio_belieflink._world_debt
        > 0.9999999
    )
    assert (
        sue_sue_belieflink._world_debt
        + bob_bob_belieflink._world_debt
        + zia_zia_belieflink._world_debt
        + xio_xio_belieflink._world_debt
        < 1.0
    )


def test_WorldUnit_calc_world_metrics_CorrectlySetsCharUnitWorldImportance():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    swim_text = "swim"
    swim_road = yao_world.make_l1_road(swim_text)
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
    yao_world.get_idea_obj(swim_road).set_awardlink(bl_sue)
    yao_world.get_idea_obj(swim_road).set_awardlink(bl_bob)
    yao_world.get_idea_obj(swim_road).set_awardlink(bl_zia)

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
    xio_text = "Xio"
    yao_world.set_charunit(charunit_shop(xio_text))
    yao_world._idearoot.set_awardlink(awardlink_shop(xio_text, 20, debtor_weight=10))
    yao_world.calc_world_metrics()

    # THEN
    xio_charunit = yao_world.get_char(xio_text)

    assert sue_charunit._world_cred != 0.5
    assert sue_charunit._world_debt != 0.8
    assert bob_charunit._world_cred != 0.25
    assert bob_charunit._world_debt != 0.1
    assert zia_charunit._world_cred != 0.25
    assert zia_charunit._world_debt != 0.1
    assert xio_charunit._world_cred != None
    assert xio_charunit._world_debt != None

    assert (
        sue_charunit._world_cred + bob_charunit._world_cred + zia_charunit._world_cred
        < 1.0
    )
    assert (
        sue_charunit._world_cred
        + bob_charunit._world_cred
        + zia_charunit._world_cred
        + xio_charunit._world_cred
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
        + xio_charunit._world_debt
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
    swim_road = yao_world.make_l1_road(swim_text)
    yao_world.add_l1_idea(ideaunit_shop(swim_text))
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_world.set_charunit(charunit_shop(sue_text))
    yao_world.set_charunit(charunit_shop(bob_text))
    yao_world.set_charunit(charunit_shop(zia_text))
    sue_awardlink = awardlink_shop(sue_text, 20, debtor_weight=40)
    bob_awardlink = awardlink_shop(bob_text, 10, debtor_weight=5)
    zia_awardlink = awardlink_shop(zia_text, 10, debtor_weight=5)
    swim_idea = yao_world.get_idea_obj(swim_road)
    swim_idea.set_awardlink(sue_awardlink)
    swim_idea.set_awardlink(bob_awardlink)
    swim_idea.set_awardlink(zia_awardlink)

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
    for beliefbox_x in x_world._beliefboxs.values():
        beliefbox_x.reset_world_cred_debt()
        # for belieflink_x in beliefbox_x._chars.values():
        #     print(f"{beliefbox_x.} {belieflink_x.}  {belieflink_x._world_cred:.6f} {belieflink_x.debtor_weight=} {belieflink_x._world_debt:.6f} {belieflink_x.} ")

    # DELETE world_agenda_debt and world_agenda_cred
    for x_charunit in x_world._chars.values():
        x_charunit.reset_world_cred_debt()


@dataclass
class BeliefAgendaMetrics:
    sum_beliefbox_cred: float = 0
    sum_beliefbox_debt: float = 0
    sum_belieflink_cred: float = 0
    sum_belieflink_debt: float = 0
    belieflink_count: int = 0

    def set_sums(self, x_world: WorldUnit):
        for x_beliefbox in x_world._beliefboxs.values():
            self.sum_beliefbox_cred += x_beliefbox._world_agenda_cred
            self.sum_beliefbox_debt += x_beliefbox._world_agenda_debt
            for belieflink_x in x_beliefbox._belieflinks.values():
                self.sum_belieflink_cred += belieflink_x._world_agenda_cred
                self.sum_belieflink_debt += belieflink_x._world_agenda_debt
                self.belieflink_count += 1


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
    assert x_beliefagendametrics.sum_belieflink_cred == 0
    assert x_beliefagendametrics.sum_belieflink_debt == 0

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
    # assert x_awardagendametrics.agenda_no_count == 14
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
    assert x_beliefagendametrics.belieflink_count == 81
    x_sum = 0.0027965049894874455
    assert are_equal(x_beliefagendametrics.sum_beliefbox_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_beliefbox_debt, x_sum)
    assert are_equal(x_beliefagendametrics.sum_belieflink_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_belieflink_debt, x_sum)
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
    yao_world = worldunit_shop("Yao")
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    sue_charunit = charunit_shop(sue_text, 0.5, debtor_weight=2)
    bob_charunit = charunit_shop(bob_text, 1.5, debtor_weight=3)
    zia_charunit = charunit_shop(zia_text, 8, debtor_weight=5)
    yao_world.set_charunit(sue_charunit)
    yao_world.set_charunit(bob_charunit)
    yao_world.set_charunit(zia_charunit)
    yao_world_sue_char = yao_world.get_char(sue_text)
    yao_world_bob_char = yao_world.get_char(bob_text)
    yao_world_zia_char = yao_world.get_char(zia_text)

    assert yao_world_sue_char._world_agenda_cred in [0, None]
    assert yao_world_sue_char._world_agenda_debt in [0, None]
    assert yao_world_bob_char._world_agenda_cred in [0, None]
    assert yao_world_bob_char._world_agenda_debt in [0, None]
    assert yao_world_zia_char._world_agenda_cred in [0, None]
    assert yao_world_zia_char._world_agenda_debt in [0, None]
    assert yao_world_sue_char._world_agenda_ratio_cred != 0.05
    assert yao_world_sue_char._world_agenda_ratio_debt != 0.2
    assert yao_world_bob_char._world_agenda_ratio_cred != 0.15
    assert yao_world_bob_char._world_agenda_ratio_debt != 0.3
    assert yao_world_zia_char._world_agenda_ratio_cred != 0.8
    assert yao_world_zia_char._world_agenda_ratio_debt != 0.5

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    assert yao_world_sue_char._world_agenda_cred == 0
    assert yao_world_sue_char._world_agenda_debt == 0
    assert yao_world_bob_char._world_agenda_cred == 0
    assert yao_world_bob_char._world_agenda_debt == 0
    assert yao_world_zia_char._world_agenda_cred == 0
    assert yao_world_zia_char._world_agenda_debt == 0
    assert yao_world_sue_char._world_agenda_ratio_cred == 0.05
    assert yao_world_sue_char._world_agenda_ratio_debt == 0.2
    assert yao_world_bob_char._world_agenda_ratio_cred == 0.15
    assert yao_world_bob_char._world_agenda_ratio_debt == 0.3
    assert yao_world_zia_char._world_agenda_ratio_cred == 0.8
    assert yao_world_zia_char._world_agenda_ratio_debt == 0.5


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
    assert x_world._beliefboxs != None
    assert len(x_world._beliefboxs) == 34
    everyone_chars_len = None
    everyone_belief = x_world.get_beliefbox(",Everyone")
    everyone_chars_len = len(everyone_belief._belieflinks)
    assert everyone_chars_len == 22

    # WHEN
    x_world.calc_world_metrics()
    idea_dict = x_world._idea_dict

    # THEN
    # print(f"{len(idea_dict)=}")
    db_idea = idea_dict.get(x_world.make_l1_road("D&B"))
    # print(f"{db_idea._label=} {db_idea._awardlinks=}")
    assert len(db_idea._awardlinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._label == "D&B":
    #         print(f"{idea._label=} {idea._awardlinks=}")
    #         db_awardlink_len = len(idea._awardlinks)
    # assert db_awardlink_len == 3
