from src._road.road import RoadUnit
from src._world.char import charunit_shop
from src._world.lobby import awardlink_shop
from src._world.examples.example_worlds import (
    world_v001 as examples_world_v001,
    world_v001_with_large_agenda as examples_world_v001_with_large_agenda,
)
from src._world.world import WorldUnit, worldunit_shop
from src._world.idea import ideaunit_shop, IdeaUnit
from dataclasses import dataclass


def test_WorldUnit_set_awardlink_CorrectlyCalculatesInheritedAwardLinkWorldImportance():
    # ESTABLISH
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_world.set_charunit(charunit_shop(yao_text))
    sue_world.set_charunit(charunit_shop(zia_text))
    sue_world.set_charunit(charunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_weight=20, take_weight=6)
    zia_awardlink = awardlink_shop(zia_text, give_weight=10, take_weight=1)
    Xio_awardlink = awardlink_shop(Xio_text, give_weight=10)
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
    assert bheir_yao._bud_give == 0.5
    assert bheir_yao._bud_take == 0.75
    assert bheir_zia._bud_give == 0.25
    assert bheir_zia._bud_take == 0.125
    assert bheir_Xio._bud_give == 0.25
    assert bheir_Xio._bud_take == 0.125
    assert bheir_yao._bud_give + bheir_zia._bud_give + bheir_Xio._bud_give == 1
    assert bheir_yao._bud_take + bheir_zia._bud_take + bheir_Xio._bud_take == 1

    # bud_give_sum = 0
    # bud_take_sum = 0
    # for lobby in x_world._idearoot._awardheirs.values():
    #     print(f"{lobby=}")
    #     assert lobby._bud_give != None
    #     assert lobby._bud_give in [0.25, 0.5]
    #     assert lobby._bud_take != None
    #     assert lobby._bud_take in [0.75, 0.125]
    #     bud_give_sum += lobby._bud_give
    #     bud_take_sum += lobby._bud_take

    # assert bud_give_sum == 1
    # assert bud_take_sum == 1


def test_WorldUnit_calc_world_metrics_CorrectlySetsLobbylinkWorldCredAndDebt():
    # ESTABLISH
    yao_world = worldunit_shop("Yao")
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_world.set_charunit(charunit_shop(sue_text))
    yao_world.set_charunit(charunit_shop(bob_text))
    yao_world.set_charunit(charunit_shop(zia_text))
    sue_awardlink = awardlink_shop(sue_text, 20, take_weight=40)
    bob_awardlink = awardlink_shop(bob_text, 10, take_weight=5)
    zia_awardlink = awardlink_shop(zia_text, 10, take_weight=5)
    yao_world.edit_idea_attr(yao_world._real_id, awardlink=sue_awardlink)
    yao_world.edit_idea_attr(yao_world._real_id, awardlink=bob_awardlink)
    yao_world.edit_idea_attr(yao_world._real_id, awardlink=zia_awardlink)

    sue_charunit = yao_world.get_char(sue_text)
    bob_charunit = yao_world.get_char(bob_text)
    zia_charunit = yao_world.get_char(zia_text)
    sue_sue_lobbylink = sue_charunit.get_lobbylink(sue_text)
    bob_bob_lobbylink = bob_charunit.get_lobbylink(bob_text)
    zia_zia_lobbylink = zia_charunit.get_lobbylink(zia_text)
    assert sue_sue_lobbylink._bud_give is None
    assert sue_sue_lobbylink._bud_take is None
    assert bob_bob_lobbylink._bud_give is None
    assert bob_bob_lobbylink._bud_take is None
    assert zia_zia_lobbylink._bud_give is None
    assert zia_zia_lobbylink._bud_take is None

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    assert sue_sue_lobbylink._bud_give == 0.5
    assert sue_sue_lobbylink._bud_take == 0.8
    assert bob_bob_lobbylink._bud_give == 0.25
    assert bob_bob_lobbylink._bud_take == 0.1
    assert zia_zia_lobbylink._bud_give == 0.25
    assert zia_zia_lobbylink._bud_take == 0.1

    lobbylink_cred_sum = (
        sue_sue_lobbylink._bud_give
        + bob_bob_lobbylink._bud_give
        + zia_zia_lobbylink._bud_give
    )
    assert lobbylink_cred_sum == 1.0
    lobbylink_debt_sum = (
        sue_sue_lobbylink._bud_take
        + bob_bob_lobbylink._bud_take
        + zia_zia_lobbylink._bud_take
    )
    assert lobbylink_debt_sum == 1.0

    # ESTABLISH anothher pledge, check metrics are as expected
    xio_text = "Xio"
    yao_world.set_charunit(charunit_shop(xio_text))
    yao_world._idearoot.set_awardlink(awardlink_shop(xio_text, 20, take_weight=13))

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    xio_lobbybox = yao_world.get_lobbybox(xio_text)
    xio_xio_lobbylink = xio_lobbybox.get_lobbylink(xio_text)
    sue_charunit = yao_world.get_char(sue_text)
    bob_charunit = yao_world.get_char(bob_text)
    zia_charunit = yao_world.get_char(zia_text)
    sue_sue_lobbylink = sue_charunit.get_lobbylink(sue_text)
    bob_bob_lobbylink = bob_charunit.get_lobbylink(bob_text)
    zia_zia_lobbylink = zia_charunit.get_lobbylink(zia_text)
    assert sue_sue_lobbylink._bud_give != 0.25
    assert sue_sue_lobbylink._bud_take != 0.8
    assert bob_bob_lobbylink._bud_give != 0.25
    assert bob_bob_lobbylink._bud_take != 0.1
    assert zia_zia_lobbylink._bud_give != 0.5
    assert zia_zia_lobbylink._bud_take != 0.1
    assert xio_xio_lobbylink._bud_give != None
    assert xio_xio_lobbylink._bud_take != None

    assert (
        sue_sue_lobbylink._bud_give
        + bob_bob_lobbylink._bud_give
        + zia_zia_lobbylink._bud_give
        + xio_xio_lobbylink._bud_give
        == 1.0
    )
    assert (
        sue_sue_lobbylink._bud_take
        + bob_bob_lobbylink._bud_take
        + zia_zia_lobbylink._bud_take
        + xio_xio_lobbylink._bud_take
        > 0.9999999
    )
    assert (
        sue_sue_lobbylink._bud_take
        + bob_bob_lobbylink._bud_take
        + zia_zia_lobbylink._bud_take
        + xio_xio_lobbylink._bud_take
        < 1.0
    )


def test_WorldUnit_calc_world_metrics_CorrectlySetsCharUnitWorldImportance():
    # ESTABLISH
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
    bl_sue = awardlink_shop(sue_text, 20, take_weight=40)
    bl_bob = awardlink_shop(bob_text, 10, take_weight=5)
    bl_zia = awardlink_shop(zia_text, 10, take_weight=5)
    yao_world.get_idea_obj(swim_road).set_awardlink(bl_sue)
    yao_world.get_idea_obj(swim_road).set_awardlink(bl_bob)
    yao_world.get_idea_obj(swim_road).set_awardlink(bl_zia)

    sue_charunit = yao_world.get_char(sue_text)
    bob_charunit = yao_world.get_char(bob_text)
    zia_charunit = yao_world.get_char(zia_text)

    assert sue_charunit._bud_give == 0
    assert sue_charunit._bud_take == 0
    assert bob_charunit._bud_give == 0
    assert bob_charunit._bud_take == 0
    assert zia_charunit._bud_give == 0
    assert zia_charunit._bud_take == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    charunit_bud_give_sum = 0.0
    charunit_bud_take_sum = 0.0

    assert sue_charunit._bud_give == 0.5
    assert sue_charunit._bud_take == 0.8
    assert bob_charunit._bud_give == 0.25
    assert bob_charunit._bud_take == 0.1
    assert zia_charunit._bud_give == 0.25
    assert zia_charunit._bud_take == 0.1

    assert (
        sue_charunit._bud_give + bob_charunit._bud_give + zia_charunit._bud_give == 1.0
    )
    assert (
        sue_charunit._bud_take + bob_charunit._bud_take + zia_charunit._bud_take == 1.0
    )

    # WHEN anothher pledge, check metrics are as expected
    xio_text = "Xio"
    yao_world.set_charunit(charunit_shop(xio_text))
    yao_world._idearoot.set_awardlink(awardlink_shop(xio_text, 20, take_weight=10))
    yao_world.calc_world_metrics()

    # THEN
    xio_charunit = yao_world.get_char(xio_text)

    assert sue_charunit._bud_give != 0.5
    assert sue_charunit._bud_take != 0.8
    assert bob_charunit._bud_give != 0.25
    assert bob_charunit._bud_take != 0.1
    assert zia_charunit._bud_give != 0.25
    assert zia_charunit._bud_take != 0.1
    assert xio_charunit._bud_give != None
    assert xio_charunit._bud_take != None

    assert (
        sue_charunit._bud_give + bob_charunit._bud_give + zia_charunit._bud_give < 1.0
    )
    assert (
        sue_charunit._bud_give
        + bob_charunit._bud_give
        + zia_charunit._bud_give
        + xio_charunit._bud_give
        == 1.0
    )
    assert (
        sue_charunit._bud_take + bob_charunit._bud_take + zia_charunit._bud_take < 1.0
    )
    assert (
        sue_charunit._bud_take
        + bob_charunit._bud_take
        + zia_charunit._bud_take
        + xio_charunit._bud_take
        == 1.0
    )


def test_WorldUnit_calc_world_metrics_CorrectlySetsPartLobbyedLWCharUnitWorldImportance():
    # ESTABLISH
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
    sue_awardlink = awardlink_shop(sue_text, 20, take_weight=40)
    bob_awardlink = awardlink_shop(bob_text, 10, take_weight=5)
    zia_awardlink = awardlink_shop(zia_text, 10, take_weight=5)
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
    sue_lobbybox = yao_world.get_lobbybox(sue_text)
    bob_lobbybox = yao_world.get_lobbybox(bob_text)
    zia_lobbybox = yao_world.get_lobbybox(zia_text)
    assert sue_lobbybox._bud_give != 0.5
    assert sue_lobbybox._bud_take != 0.8
    assert bob_lobbybox._bud_give != 0.25
    assert bob_lobbybox._bud_take != 0.1
    assert zia_lobbybox._bud_give != 0.25
    assert zia_lobbybox._bud_take != 0.1
    assert (
        sue_lobbybox._bud_give + bob_lobbybox._bud_give + zia_lobbybox._bud_give == 0.25
    )
    assert (
        sue_lobbybox._bud_take + bob_lobbybox._bud_take + zia_lobbybox._bud_take == 0.25
    )

    sue_charunit = yao_world.get_char(sue_text)
    bob_charunit = yao_world.get_char(bob_text)
    zia_charunit = yao_world.get_char(zia_text)

    assert sue_charunit._bud_give == 0.375
    assert sue_charunit._bud_take == 0.45
    assert bob_charunit._bud_give == 0.3125
    assert bob_charunit._bud_take == 0.275
    assert zia_charunit._bud_give == 0.3125
    assert zia_charunit._bud_take == 0.275

    assert (
        sue_charunit._bud_give + bob_charunit._bud_give + zia_charunit._bud_give == 1.0
    )
    assert (
        sue_charunit._bud_take + bob_charunit._bud_take + zia_charunit._bud_take == 1.0
    )


def test_WorldUnit_calc_world_metrics_CorrectlySetsCharAttrs():
    # ESTABLISH
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
    assert sue_charunit._bud_give == 0
    assert sue_charunit._bud_take == 0
    assert bob_charunit._bud_give == 0
    assert bob_charunit._bud_take == 0
    assert zia_charunit._bud_give == 0
    assert zia_charunit._bud_take == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    assert (
        sue_charunit._bud_give + bob_charunit._bud_give + zia_charunit._bud_give == 1.0
    )
    assert (
        sue_charunit._bud_take + bob_charunit._bud_take + zia_charunit._bud_take == 1.0
    )


# def test_WorldUnit_calc_world_metrics_DoesNotRaiseError_credor_respectWhenCharSumIsZero():
#     # ESTABLISH
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
#     # ESTABLISH
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


def clear_all_charunits_lobbyboxs_bud_agenda_give_take(x_world: WorldUnit):
    # DELETE world_agenda_debt and world_agenda_cred
    for lobbybox_x in x_world._lobbyboxs.values():
        lobbybox_x.reset_bud_give_take()
        # for lobbylink_x in lobbybox_x._chars.values():
        #     print(f"{lobbybox_x.} {lobbylink_x.}  {lobbylink_x._bud_give:.6f} {lobbylink_x.debtor_weight=} {lobbylink__bud_take:t:.6f} {lobbylink_x.} ")

    # DELETE world_agenda_debt and world_agenda_cred
    for x_charunit in x_world._chars.values():
        x_charunit.reset_bud_give_take()


@dataclass
class LobbyAgendaMetrics:
    sum_lobbybox_cred: float = 0
    sum_lobbybox_debt: float = 0
    sum_lobbylink_cred: float = 0
    sum_lobbylink_debt: float = 0
    lobbylink_count: int = 0

    def set_sums(self, x_world: WorldUnit):
        for x_lobbybox in x_world._lobbyboxs.values():
            self.sum_lobbybox_cred += x_lobbybox._bud_agenda_give
            self.sum_lobbybox_debt += x_lobbybox._bud_agenda_take
            for lobbylink_x in x_lobbybox._lobbylinks.values():
                self.sum_lobbylink_cred += lobbylink_x._bud_agenda_give
                self.sum_lobbylink_debt += lobbylink_x._bud_agenda_take
                self.lobbylink_count += 1


@dataclass
class CharAgendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_sums(self, x_world: WorldUnit):
        for charunit in x_world._chars.values():
            self.sum_agenda_cred += charunit._bud_agenda_give
            self.sum_agenda_debt += charunit._bud_agenda_take
            self.sum_agenda_ratio_cred += charunit._bud_agenda_ratio_give
            self.sum_agenda_ratio_debt += charunit._bud_agenda_ratio_take


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
    # ESTABLISH
    x_world = examples_world_v001_with_large_agenda()
    clear_all_charunits_lobbyboxs_bud_agenda_give_take(x_world=x_world)

    # TEST world_agenda_debt and world_agenda_cred are empty
    x_lobbyagendametrics = LobbyAgendaMetrics()
    x_lobbyagendametrics.set_sums(x_world=x_world)
    assert x_lobbyagendametrics.sum_lobbybox_cred == 0
    assert x_lobbyagendametrics.sum_lobbybox_debt == 0
    assert x_lobbyagendametrics.sum_lobbylink_cred == 0
    assert x_lobbyagendametrics.sum_lobbylink_debt == 0

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

    x_lobbyagendametrics = LobbyAgendaMetrics()
    x_lobbyagendametrics.set_sums(x_world=x_world)
    assert x_lobbyagendametrics.lobbylink_count == 81
    x_sum = 0.0027965049894874455
    assert are_equal(x_lobbyagendametrics.sum_lobbybox_cred, x_sum)
    assert are_equal(x_lobbyagendametrics.sum_lobbybox_debt, x_sum)
    assert are_equal(x_lobbyagendametrics.sum_lobbylink_cred, x_sum)
    assert are_equal(x_lobbyagendametrics.sum_lobbylink_debt, x_sum)
    assert are_equal(
        x_awardagendametrics.agenda_yes_world_i_sum,
        x_lobbyagendametrics.sum_lobbybox_cred,
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

    # charunit_bud_give_sum = 0.0
    # charunit_bud_take_sum = 0.0

    # assert charunit_bud_give_sum == 1.0
    # assert charunit_bud_take_sum > 0.9999999
    # assert charunit_bud_take_sum < 1.00000001


def all_charunits_have_legitimate_values(x_world: WorldUnit):
    return not any(
        (
            charunit._bud_give is None
            or charunit._bud_give in [0.25, 0.5]
            or charunit._bud_take is None
            or charunit._bud_take in [0.8, 0.1]
        )
        for charunit in x_world._chars.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000000001
    return abs(x1 - x2) < e10


def test_WorldUnit_agenda_ratio_cred_debt_IsCorrectlySetWhenWorldIsEmpty():
    # ESTABLISH
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

    assert yao_world_sue_char._bud_agenda_give in [0, None]
    assert yao_world_sue_char._bud_agenda_take in [0, None]
    assert yao_world_bob_char._bud_agenda_give in [0, None]
    assert yao_world_bob_char._bud_agenda_take in [0, None]
    assert yao_world_zia_char._bud_agenda_give in [0, None]
    assert yao_world_zia_char._bud_agenda_take in [0, None]
    assert yao_world_sue_char._bud_agenda_ratio_give != 0.05
    assert yao_world_sue_char._bud_agenda_ratio_take != 0.2
    assert yao_world_bob_char._bud_agenda_ratio_give != 0.15
    assert yao_world_bob_char._bud_agenda_ratio_take != 0.3
    assert yao_world_zia_char._bud_agenda_ratio_give != 0.8
    assert yao_world_zia_char._bud_agenda_ratio_take != 0.5

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    assert yao_world_sue_char._bud_agenda_give == 0
    assert yao_world_sue_char._bud_agenda_take == 0
    assert yao_world_bob_char._bud_agenda_give == 0
    assert yao_world_bob_char._bud_agenda_take == 0
    assert yao_world_zia_char._bud_agenda_give == 0
    assert yao_world_zia_char._bud_agenda_take == 0
    assert yao_world_sue_char._bud_agenda_ratio_give == 0.05
    assert yao_world_sue_char._bud_agenda_ratio_take == 0.2
    assert yao_world_bob_char._bud_agenda_ratio_give == 0.15
    assert yao_world_bob_char._bud_agenda_ratio_take == 0.3
    assert yao_world_zia_char._bud_agenda_ratio_give == 0.8
    assert yao_world_zia_char._bud_agenda_ratio_take == 0.5


def test_examples_world_v001_has_chars():
    # ESTABLISH / WHEN
    yao_world = examples_world_v001()

    # THEN
    assert yao_world._chars != None
    assert len(yao_world._chars) == 22


def test_examples_world_v001_HasLobbys():
    # ESTABLISH / WHEN
    x_world = examples_world_v001()
    x_world.calc_world_metrics()

    # THEN
    assert x_world._lobbyboxs != None
    assert len(x_world._lobbyboxs) == 34
    everyone_chars_len = None
    everyone_lobby = x_world.get_lobbybox(",Everyone")
    everyone_chars_len = len(everyone_lobby._lobbylinks)
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
