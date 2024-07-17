from src._world.lobby import awardlink_shop
from src._world.examples.example_worlds import (
    get_world_1Task_1CE0MinutesReason_1Fact,
)
from src._world.char import charunit_shop
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_calc_world_metrics_CorrectlyCalculates1LevelWorldLobbyWorldImportance():
    # ESTABLISH
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    sue_text = "Sue"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, credor_weight=20, debtor_weight=6)
    zia_awardlink = awardlink_shop(zia_text, credor_weight=10, debtor_weight=1)
    xio_awardlink = awardlink_shop(xio_text, credor_weight=10)
    x_idearoot = x_world.get_idea_obj(x_world._real_id)
    x_idearoot.set_awardlink(awardlink=yao_awardlink)
    x_idearoot.set_awardlink(awardlink=zia_awardlink)
    x_idearoot.set_awardlink(awardlink=xio_awardlink)
    assert len(x_world.get_lobby_ids_dict()) == 3

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    yao_lobbybox = x_world.get_lobbybox(yao_text)
    zia_lobbybox = x_world.get_lobbybox(zia_text)
    xio_lobbybox = x_world.get_lobbybox(xio_text)
    assert yao_lobbybox._bud_give == 0.5
    assert yao_lobbybox._bud_take == 0.75
    assert zia_lobbybox._bud_give == 0.25
    assert zia_lobbybox._bud_take == 0.125
    assert xio_lobbybox._bud_give == 0.25
    assert xio_lobbybox._bud_take == 0.125
    cred_sum1 = yao_lobbybox._bud_give
    cred_sum1 += zia_lobbybox._bud_give + xio_lobbybox._bud_give
    assert cred_sum1 == 1
    debt_sum1 = yao_lobbybox._bud_take
    debt_sum1 += zia_lobbybox._bud_take + xio_lobbybox._bud_take
    assert debt_sum1 == 1

    # ESTABLISH
    x_world.set_charunit(charunit_shop(sue_text))
    sue_awardlink = awardlink_shop(sue_text, credor_weight=37)
    x_idearoot.set_awardlink(sue_awardlink)
    assert len(x_idearoot._awardlinks) == 4
    assert len(x_world.get_lobby_ids_dict()) == 4

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    yao_lobbybox = x_world.get_lobbybox(yao_text)
    zia_lobbybox = x_world.get_lobbybox(zia_text)
    xio_lobbybox = x_world.get_lobbybox(xio_text)
    sue_lobbybox = x_world.get_lobbybox(sue_text)
    assert yao_lobbybox._bud_give != 0.5
    assert yao_lobbybox._bud_take != 0.75
    assert zia_lobbybox._bud_give != 0.25
    assert zia_lobbybox._bud_take != 0.125
    assert xio_lobbybox._bud_give != 0.25
    assert xio_lobbybox._bud_take != 0.125
    assert sue_lobbybox._bud_give != None
    assert sue_lobbybox._bud_take != None
    cred_sum1 = yao_lobbybox._bud_give + zia_lobbybox._bud_give
    cred_sum1 += xio_lobbybox._bud_give + sue_lobbybox._bud_give
    assert cred_sum1 == 1
    debt_sum1 = yao_lobbybox._bud_take + zia_lobbybox._bud_take
    debt_sum1 += xio_lobbybox._bud_take + sue_lobbybox._bud_take
    assert round(debt_sum1) == 1


def test_WorldUnit_calc_world_metrics_CorrectlyCalculates3levelWorldLobbyWorldImportance():
    # ESTABLISH
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    swim_text = "swim"
    swim_road = x_world.make_l1_road(swim_text)
    x_world.add_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, credor_weight=20, debtor_weight=6)
    zia_awardlink = awardlink_shop(zia_text, credor_weight=10, debtor_weight=1)
    parm_awardlink = awardlink_shop(xio_text, credor_weight=10)
    swim_idea = x_world.get_idea_obj(swim_road)
    swim_idea.set_awardlink(yao_awardlink)
    swim_idea.set_awardlink(zia_awardlink)
    swim_idea.set_awardlink(parm_awardlink)
    assert len(x_world.get_lobby_ids_dict()) == 3

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    yao_lobbybox = x_world.get_lobbybox(yao_text)
    zia_lobbybox = x_world.get_lobbybox(zia_text)
    xio_lobbybox = x_world.get_lobbybox(xio_text)
    assert yao_lobbybox._bud_give == 0.5
    assert yao_lobbybox._bud_take == 0.75
    assert zia_lobbybox._bud_give == 0.25
    assert zia_lobbybox._bud_take == 0.125
    assert xio_lobbybox._bud_give == 0.25
    assert xio_lobbybox._bud_take == 0.125
    assert yao_lobbybox._bud_give + zia_lobbybox._bud_give + xio_lobbybox._bud_give == 1
    assert yao_lobbybox._bud_take + zia_lobbybox._bud_take + xio_lobbybox._bud_take == 1


def test_WorldUnit_calc_world_metrics_CorrectlyCalculatesLobbyWorldImportanceLWwithLobbyEmptyAncestors():
    # ESTABLISH
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    swim_text = "swim"
    swim_road = x_world.make_l1_road(swim_text)
    x_world.add_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, credor_weight=20, debtor_weight=6)
    zia_awardlink = awardlink_shop(zia_text, credor_weight=10, debtor_weight=1)
    parm_awardlink = awardlink_shop(xio_text, credor_weight=10)
    swim_idea = x_world.get_idea_obj(swim_road)
    swim_idea.set_awardlink(yao_awardlink)
    swim_idea.set_awardlink(zia_awardlink)
    swim_idea.set_awardlink(parm_awardlink)

    # no awardlinks attached to this one
    x_world.add_l1_idea(ideaunit_shop("hunt", _weight=3))

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    x_idearoot = x_world.get_idea_obj(x_world._real_id)
    with pytest_raises(Exception) as excinfo:
        x_idearoot._awardlinks[yao_text]
    assert str(excinfo.value) == f"'{yao_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._awardlinks[zia_text]
    assert str(excinfo.value) == f"'{zia_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._awardlinks[xio_text]
    assert str(excinfo.value) == f"'{xio_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._kids["hunt"]._awardheirs[yao_text]
    assert str(excinfo.value) == f"'{yao_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._kids["hunt"]._awardheirs[zia_text]
    assert str(excinfo.value) == f"'{zia_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._kids["hunt"]._awardheirs[xio_text]
    assert str(excinfo.value) == f"'{xio_text}'"

    # THEN
    yao_lobbybox = x_world.get_lobbybox(yao_text)
    zia_lobbybox = x_world.get_lobbybox(zia_text)
    xio_lobbybox = x_world.get_lobbybox(xio_text)
    assert yao_lobbybox._bud_give == 0.125
    assert yao_lobbybox._bud_take == 0.1875
    assert zia_lobbybox._bud_give == 0.0625
    assert zia_lobbybox._bud_take == 0.03125
    assert xio_lobbybox._bud_give == 0.0625
    assert xio_lobbybox._bud_take == 0.03125
    assert (
        yao_lobbybox._bud_give + zia_lobbybox._bud_give + xio_lobbybox._bud_give == 0.25
    )
    assert (
        yao_lobbybox._bud_take + zia_lobbybox._bud_take + xio_lobbybox._bud_take == 0.25
    )


def test_WorldUnit_IsAbleToEditFactUnitAnyAncestor_Idea_1():
    x_world = get_world_1Task_1CE0MinutesReason_1Fact()
    ced_min_label = "CE0_minutes"
    ced_road = x_world.make_l1_road(ced_min_label)
    x_world.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)
    mail_road = x_world.make_l1_road("obtain mail")
    idea_dict = x_world.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task is False

    x_world.set_fact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_dict = x_world.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task == True
