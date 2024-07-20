from src._road.finance import default_fund_pool
from src._road.road import RoadUnit
from src.bud.acct import acctunit_shop
from src.bud.lobby import awardlink_shop
from src.bud.examples.example_buds import (
    budunit_v001,
    budunit_v001_with_large_agenda as budunit_v001_with_large_agenda,
    get_budunit_1Task_1CE0MinutesReason_1Fact,
)
from src.bud.bud import BudUnit, budunit_shop
from src.bud.idea import ideaunit_shop, IdeaUnit
from pytest import raises as pytest_raises
from dataclasses import dataclass


def test_BudUnit_settle_bud_CorrectlyCalculates1LevelBudLobbyBudImportance():
    # ESTABLISH
    prom_text = "prom"
    x_bud = budunit_shop(prom_text)
    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    sue_text = "Sue"
    x_bud.set_acctunit(acctunit_shop(yao_text))
    x_bud.set_acctunit(acctunit_shop(zia_text))
    x_bud.set_acctunit(acctunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_weight=20, take_weight=6)
    zia_awardlink = awardlink_shop(zia_text, give_weight=10, take_weight=1)
    xio_awardlink = awardlink_shop(xio_text, give_weight=10)
    x_idearoot = x_bud.get_idea_obj(x_bud._real_id)
    x_idearoot.set_awardlink(awardlink=yao_awardlink)
    x_idearoot.set_awardlink(awardlink=zia_awardlink)
    x_idearoot.set_awardlink(awardlink=xio_awardlink)
    assert len(x_bud.get_lobby_ids_dict()) == 3

    # WHEN
    x_bud.settle_bud()

    # THEN
    yao_lobbybox = x_bud.get_lobbybox(yao_text)
    zia_lobbybox = x_bud.get_lobbybox(zia_text)
    xio_lobbybox = x_bud.get_lobbybox(xio_text)
    assert yao_lobbybox._fund_give == 0.5 * default_fund_pool()
    assert yao_lobbybox._fund_take == 0.75 * default_fund_pool()
    assert zia_lobbybox._fund_give == 0.25 * default_fund_pool()
    assert zia_lobbybox._fund_take == 0.125 * default_fund_pool()
    assert xio_lobbybox._fund_give == 0.25 * default_fund_pool()
    assert xio_lobbybox._fund_take == 0.125 * default_fund_pool()
    cred_sum1 = yao_lobbybox._fund_give
    cred_sum1 += zia_lobbybox._fund_give + xio_lobbybox._fund_give
    assert cred_sum1 == 1 * default_fund_pool()
    debt_sum1 = yao_lobbybox._fund_take
    debt_sum1 += zia_lobbybox._fund_take + xio_lobbybox._fund_take
    assert debt_sum1 == 1 * default_fund_pool()

    # ESTABLISH
    x_bud.set_acctunit(acctunit_shop(sue_text))
    sue_awardlink = awardlink_shop(sue_text, give_weight=37)
    x_idearoot.set_awardlink(sue_awardlink)
    assert len(x_idearoot._awardlinks) == 4
    assert len(x_bud.get_lobby_ids_dict()) == 4

    # WHEN
    x_bud.settle_bud()

    # THEN
    yao_lobbybox = x_bud.get_lobbybox(yao_text)
    zia_lobbybox = x_bud.get_lobbybox(zia_text)
    xio_lobbybox = x_bud.get_lobbybox(xio_text)
    sue_lobbybox = x_bud.get_lobbybox(sue_text)
    assert yao_lobbybox._fund_give != 0.5 * default_fund_pool()
    assert yao_lobbybox._fund_take != 0.75 * default_fund_pool()
    assert zia_lobbybox._fund_give != 0.25 * default_fund_pool()
    assert zia_lobbybox._fund_take != 0.125 * default_fund_pool()
    assert xio_lobbybox._fund_give != 0.25 * default_fund_pool()
    assert xio_lobbybox._fund_take != 0.125 * default_fund_pool()
    assert sue_lobbybox._fund_give is not None
    assert sue_lobbybox._fund_take is not None
    cred_sum1 = yao_lobbybox._fund_give + zia_lobbybox._fund_give
    cred_sum1 += xio_lobbybox._fund_give + sue_lobbybox._fund_give
    assert cred_sum1 == 1 * default_fund_pool()
    debt_sum1 = yao_lobbybox._fund_take + zia_lobbybox._fund_take
    debt_sum1 += xio_lobbybox._fund_take + sue_lobbybox._fund_take
    assert round(debt_sum1) == 1 * default_fund_pool()


def test_BudUnit_settle_bud_CorrectlyCalculates3levelBudLobbyBudImportance():
    # ESTABLISH
    prom_text = "prom"
    x_bud = budunit_shop(prom_text)
    swim_text = "swim"
    swim_road = x_bud.make_l1_road(swim_text)
    x_bud.add_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    x_bud.set_acctunit(acctunit_shop(yao_text))
    x_bud.set_acctunit(acctunit_shop(zia_text))
    x_bud.set_acctunit(acctunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_weight=20, take_weight=6)
    zia_awardlink = awardlink_shop(zia_text, give_weight=10, take_weight=1)
    parm_awardlink = awardlink_shop(xio_text, give_weight=10)
    swim_idea = x_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(yao_awardlink)
    swim_idea.set_awardlink(zia_awardlink)
    swim_idea.set_awardlink(parm_awardlink)
    assert len(x_bud.get_lobby_ids_dict()) == 3

    # WHEN
    x_bud.settle_bud()

    # THEN
    yao_lobbybox = x_bud.get_lobbybox(yao_text)
    zia_lobbybox = x_bud.get_lobbybox(zia_text)
    xio_lobbybox = x_bud.get_lobbybox(xio_text)
    assert yao_lobbybox._fund_give == 0.5 * default_fund_pool()
    assert yao_lobbybox._fund_take == 0.75 * default_fund_pool()
    assert zia_lobbybox._fund_give == 0.25 * default_fund_pool()
    assert zia_lobbybox._fund_take == 0.125 * default_fund_pool()
    assert xio_lobbybox._fund_give == 0.25 * default_fund_pool()
    assert xio_lobbybox._fund_take == 0.125 * default_fund_pool()
    assert (
        yao_lobbybox._fund_give + zia_lobbybox._fund_give + xio_lobbybox._fund_give
        == 1 * default_fund_pool()
    )
    assert (
        yao_lobbybox._fund_take + zia_lobbybox._fund_take + xio_lobbybox._fund_take
        == 1 * default_fund_pool()
    )


def test_BudUnit_settle_bud_CorrectlyCalculatesLobbyBudImportanceLWwithLobbyEmptyAncestors():
    # ESTABLISH
    prom_text = "prom"
    x_bud = budunit_shop(prom_text)
    swim_text = "swim"
    swim_road = x_bud.make_l1_road(swim_text)
    x_bud.add_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    x_bud.set_acctunit(acctunit_shop(yao_text))
    x_bud.set_acctunit(acctunit_shop(zia_text))
    x_bud.set_acctunit(acctunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_weight=20, take_weight=6)
    zia_awardlink = awardlink_shop(zia_text, give_weight=10, take_weight=1)
    parm_awardlink = awardlink_shop(xio_text, give_weight=10)
    swim_idea = x_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(yao_awardlink)
    swim_idea.set_awardlink(zia_awardlink)
    swim_idea.set_awardlink(parm_awardlink)

    # no awardlinks attached to this one
    x_bud.add_l1_idea(ideaunit_shop("hunt", _weight=3))

    # WHEN
    x_bud.settle_bud()

    # THEN
    x_idearoot = x_bud.get_idea_obj(x_bud._real_id)
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
    yao_lobbybox = x_bud.get_lobbybox(yao_text)
    zia_lobbybox = x_bud.get_lobbybox(zia_text)
    xio_lobbybox = x_bud.get_lobbybox(xio_text)
    assert yao_lobbybox._fund_give == 0.125 * default_fund_pool()
    assert yao_lobbybox._fund_take == 0.1875 * default_fund_pool()
    assert zia_lobbybox._fund_give == 0.0625 * default_fund_pool()
    assert zia_lobbybox._fund_take == 0.03125 * default_fund_pool()
    assert xio_lobbybox._fund_give == 0.0625 * default_fund_pool()
    assert xio_lobbybox._fund_take == 0.03125 * default_fund_pool()
    assert (
        yao_lobbybox._fund_give + zia_lobbybox._fund_give + xio_lobbybox._fund_give
        == 0.25 * default_fund_pool()
    )
    assert (
        yao_lobbybox._fund_take + zia_lobbybox._fund_take + xio_lobbybox._fund_take
        == 0.25 * default_fund_pool()
    )


def test_BudUnit_IsAbleToEditFactUnitAnyAncestor_Idea_1():
    x_bud = get_budunit_1Task_1CE0MinutesReason_1Fact()
    ced_min_label = "CE0_minutes"
    ced_road = x_bud.make_l1_road(ced_min_label)
    x_bud.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)
    mail_road = x_bud.make_l1_road("obtain mail")
    idea_dict = x_bud.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task is False

    x_bud.set_fact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_dict = x_bud.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task == True


def test_BudUnit_set_awardlink_CorrectlyCalculatesInheritedAwardLinkBudImportance():
    # ESTABLISH
    sue_text = "Sue"
    sue_bud = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_bud.set_acctunit(acctunit_shop(yao_text))
    sue_bud.set_acctunit(acctunit_shop(zia_text))
    sue_bud.set_acctunit(acctunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_weight=20, take_weight=6)
    zia_awardlink = awardlink_shop(zia_text, give_weight=10, take_weight=1)
    Xio_awardlink = awardlink_shop(Xio_text, give_weight=10)
    sue_bud._idearoot.set_awardlink(yao_awardlink)
    sue_bud._idearoot.set_awardlink(zia_awardlink)
    sue_bud._idearoot.set_awardlink(Xio_awardlink)
    assert len(sue_bud._idearoot._awardlinks) == 3

    # WHEN
    idea_dict = sue_bud.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=}")
    idea_prom = idea_dict.get(sue_bud._real_id)
    assert len(idea_prom._awardheirs) == 3

    bheir_yao = idea_prom._awardheirs.get(yao_text)
    bheir_zia = idea_prom._awardheirs.get(zia_text)
    bheir_Xio = idea_prom._awardheirs.get(Xio_text)
    assert bheir_yao._fund_give == 0.5 * default_fund_pool()
    assert bheir_yao._fund_take == 0.75 * default_fund_pool()
    assert bheir_zia._fund_give == 0.25 * default_fund_pool()
    assert bheir_zia._fund_take == 0.125 * default_fund_pool()
    assert bheir_Xio._fund_give == 0.25 * default_fund_pool()
    assert bheir_Xio._fund_take == 0.125 * default_fund_pool()
    assert (
        bheir_yao._fund_give + bheir_zia._fund_give + bheir_Xio._fund_give
        == 1 * default_fund_pool()
    )
    assert (
        bheir_yao._fund_take + bheir_zia._fund_take + bheir_Xio._fund_take
        == 1 * default_fund_pool()
    )

    # fund_give_sum = 0
    # fund_take_sum = 0
    # for lobby in x_bud._idearoot._awardheirs.values():
    #     print(f"{lobby=}")
    #     assert lobby._fund_give is not None
    #     assert lobby._fund_give in [0.25, 0.5]
    #     assert lobby._fund_take is not None
    #     assert lobby._fund_take in [0.75, 0.125]
    #     fund_give_sum += lobby._fund_give
    #     fund_take_sum += lobby._fund_take

    # assert fund_give_sum == 1
    # assert fund_take_sum == 1


def test_BudUnit_settle_bud_CorrectlySetsLobbyLinkBudCredAndDebt():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_text))
    yao_bud.set_acctunit(acctunit_shop(bob_text))
    yao_bud.set_acctunit(acctunit_shop(zia_text))
    sue_awardlink = awardlink_shop(sue_text, 20, take_weight=40)
    bob_awardlink = awardlink_shop(bob_text, 10, take_weight=5)
    zia_awardlink = awardlink_shop(zia_text, 10, take_weight=5)
    yao_bud.edit_idea_attr(yao_bud._real_id, awardlink=sue_awardlink)
    yao_bud.edit_idea_attr(yao_bud._real_id, awardlink=bob_awardlink)
    yao_bud.edit_idea_attr(yao_bud._real_id, awardlink=zia_awardlink)

    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)
    sue_sue_lobbyship = sue_acctunit.get_lobbyship(sue_text)
    bob_bob_lobbyship = bob_acctunit.get_lobbyship(bob_text)
    zia_zia_lobbyship = zia_acctunit.get_lobbyship(zia_text)
    assert sue_sue_lobbyship._fund_give is None
    assert sue_sue_lobbyship._fund_take is None
    assert bob_bob_lobbyship._fund_give is None
    assert bob_bob_lobbyship._fund_take is None
    assert zia_zia_lobbyship._fund_give is None
    assert zia_zia_lobbyship._fund_take is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert sue_sue_lobbyship._fund_give == 0.5 * default_fund_pool()
    assert sue_sue_lobbyship._fund_take == 0.8 * default_fund_pool()
    assert bob_bob_lobbyship._fund_give == 0.25 * default_fund_pool()
    assert bob_bob_lobbyship._fund_take == 0.1 * default_fund_pool()
    assert zia_zia_lobbyship._fund_give == 0.25 * default_fund_pool()
    assert zia_zia_lobbyship._fund_take == 0.1 * default_fund_pool()

    lobbyship_cred_sum = (
        sue_sue_lobbyship._fund_give
        + bob_bob_lobbyship._fund_give
        + zia_zia_lobbyship._fund_give
    )
    assert lobbyship_cred_sum == 1.0 * default_fund_pool()
    lobbyship_debt_sum = (
        sue_sue_lobbyship._fund_take
        + bob_bob_lobbyship._fund_take
        + zia_zia_lobbyship._fund_take
    )
    assert lobbyship_debt_sum == 1.0 * default_fund_pool()

    # ESTABLISH anothher pledge, check metrics are as expected
    xio_text = "Xio"
    yao_bud.set_acctunit(acctunit_shop(xio_text))
    yao_bud._idearoot.set_awardlink(awardlink_shop(xio_text, 20, take_weight=13))

    # WHEN
    yao_bud.settle_bud()

    # THEN
    xio_lobbybox = yao_bud.get_lobbybox(xio_text)
    xio_xio_lobbyship = xio_lobbybox.get_lobbyship(xio_text)
    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)
    sue_sue_lobbyship = sue_acctunit.get_lobbyship(sue_text)
    bob_bob_lobbyship = bob_acctunit.get_lobbyship(bob_text)
    zia_zia_lobbyship = zia_acctunit.get_lobbyship(zia_text)
    assert sue_sue_lobbyship._fund_give != 0.25 * default_fund_pool()
    assert sue_sue_lobbyship._fund_take != 0.8 * default_fund_pool()
    assert bob_bob_lobbyship._fund_give != 0.25 * default_fund_pool()
    assert bob_bob_lobbyship._fund_take != 0.1 * default_fund_pool()
    assert zia_zia_lobbyship._fund_give != 0.5 * default_fund_pool()
    assert zia_zia_lobbyship._fund_take != 0.1 * default_fund_pool()
    assert xio_xio_lobbyship._fund_give is not None
    assert xio_xio_lobbyship._fund_take is not None

    x_fund_give_sum = (
        sue_sue_lobbyship._fund_give
        + bob_bob_lobbyship._fund_give
        + zia_zia_lobbyship._fund_give
        + xio_xio_lobbyship._fund_give
    )
    print(f"{x_fund_give_sum=}")
    assert x_fund_give_sum == 1.0 * default_fund_pool()
    x_fund_take_sum = (
        sue_sue_lobbyship._fund_take
        + bob_bob_lobbyship._fund_take
        + zia_zia_lobbyship._fund_take
        + xio_xio_lobbyship._fund_take
    )
    assert x_fund_take_sum == 1.0 * default_fund_pool()


def test_BudUnit_settle_bud_CorrectlySetsAcctUnitBudImportance():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    swim_text = "swim"
    swim_road = yao_bud.make_l1_road(swim_text)
    yao_bud.add_l1_idea(ideaunit_shop(swim_text))
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_text))
    yao_bud.set_acctunit(acctunit_shop(bob_text))
    yao_bud.set_acctunit(acctunit_shop(zia_text))
    bl_sue = awardlink_shop(sue_text, 20, take_weight=40)
    bl_bob = awardlink_shop(bob_text, 10, take_weight=5)
    bl_zia = awardlink_shop(zia_text, 10, take_weight=5)
    yao_bud.get_idea_obj(swim_road).set_awardlink(bl_sue)
    yao_bud.get_idea_obj(swim_road).set_awardlink(bl_bob)
    yao_bud.get_idea_obj(swim_road).set_awardlink(bl_zia)

    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)

    assert sue_acctunit._fund_give == 0
    assert sue_acctunit._fund_take == 0
    assert bob_acctunit._fund_give == 0
    assert bob_acctunit._fund_take == 0
    assert zia_acctunit._fund_give == 0
    assert zia_acctunit._fund_take == 0

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert sue_acctunit._fund_give == 0.5 * default_fund_pool()
    assert sue_acctunit._fund_take == 0.8 * default_fund_pool()
    assert bob_acctunit._fund_give == 0.25 * default_fund_pool()
    assert bob_acctunit._fund_take == 0.1 * default_fund_pool()
    assert zia_acctunit._fund_give == 0.25 * default_fund_pool()
    assert zia_acctunit._fund_take == 0.1 * default_fund_pool()

    assert (
        sue_acctunit._fund_give + bob_acctunit._fund_give + zia_acctunit._fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_acctunit._fund_take + bob_acctunit._fund_take + zia_acctunit._fund_take
        == 1.0 * default_fund_pool()
    )

    # WHEN anothher pledge, check metrics are as expected
    xio_text = "Xio"
    yao_bud.set_acctunit(acctunit_shop(xio_text))
    yao_bud._idearoot.set_awardlink(awardlink_shop(xio_text, 20, take_weight=10))
    yao_bud.settle_bud()

    # THEN
    xio_acctunit = yao_bud.get_acct(xio_text)

    assert sue_acctunit._fund_give != 0.5 * default_fund_pool()
    assert sue_acctunit._fund_take != 0.8 * default_fund_pool()
    assert bob_acctunit._fund_give != 0.25 * default_fund_pool()
    assert bob_acctunit._fund_take != 0.1 * default_fund_pool()
    assert zia_acctunit._fund_give != 0.25 * default_fund_pool()
    assert zia_acctunit._fund_take != 0.1 * default_fund_pool()
    assert xio_acctunit._fund_give is not None
    assert xio_acctunit._fund_take is not None

    sum_acctunit_fund_give = (
        sue_acctunit._fund_give + bob_acctunit._fund_give + zia_acctunit._fund_give
    )
    assert sum_acctunit_fund_give < 1.0 * default_fund_pool()
    assert (
        sue_acctunit._fund_give
        + bob_acctunit._fund_give
        + zia_acctunit._fund_give
        + xio_acctunit._fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_acctunit._fund_take + bob_acctunit._fund_take + zia_acctunit._fund_take
        < 1.0 * default_fund_pool()
    )
    assert (
        sue_acctunit._fund_take
        + bob_acctunit._fund_take
        + zia_acctunit._fund_take
        + xio_acctunit._fund_take
        == 1.0 * default_fund_pool()
    )


def test_BudUnit_settle_bud_CorrectlySetsPartLobbyedLWAcctUnitBudImportance():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    swim_text = "swim"
    swim_road = yao_bud.make_l1_road(swim_text)
    yao_bud.add_l1_idea(ideaunit_shop(swim_text))
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_text))
    yao_bud.set_acctunit(acctunit_shop(bob_text))
    yao_bud.set_acctunit(acctunit_shop(zia_text))
    sue_awardlink = awardlink_shop(sue_text, 20, take_weight=40)
    bob_awardlink = awardlink_shop(bob_text, 10, take_weight=5)
    zia_awardlink = awardlink_shop(zia_text, 10, take_weight=5)
    swim_idea = yao_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(sue_awardlink)
    swim_idea.set_awardlink(bob_awardlink)
    swim_idea.set_awardlink(zia_awardlink)

    # no awardlinks attached to this one
    hunt_text = "hunt"
    yao_bud.add_l1_idea(ideaunit_shop(hunt_text, _weight=3))

    # WHEN
    yao_bud.settle_bud()

    # THEN
    sue_lobbybox = yao_bud.get_lobbybox(sue_text)
    bob_lobbybox = yao_bud.get_lobbybox(bob_text)
    zia_lobbybox = yao_bud.get_lobbybox(zia_text)
    assert sue_lobbybox._fund_give != 0.5 * default_fund_pool()
    assert sue_lobbybox._fund_take != 0.8 * default_fund_pool()
    assert bob_lobbybox._fund_give != 0.25 * default_fund_pool()
    assert bob_lobbybox._fund_take != 0.1 * default_fund_pool()
    assert zia_lobbybox._fund_give != 0.25 * default_fund_pool()
    assert zia_lobbybox._fund_take != 0.1 * default_fund_pool()
    assert (
        sue_lobbybox._fund_give + bob_lobbybox._fund_give + zia_lobbybox._fund_give
        == 0.25 * default_fund_pool()
    )
    assert (
        sue_lobbybox._fund_take + bob_lobbybox._fund_take + zia_lobbybox._fund_take
        == 0.25 * default_fund_pool()
    )

    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)

    assert sue_acctunit._fund_give == 0.375 * default_fund_pool()
    assert sue_acctunit._fund_take == 0.45 * default_fund_pool()
    assert bob_acctunit._fund_give == 0.3125 * default_fund_pool()
    assert bob_acctunit._fund_take == 0.275 * default_fund_pool()
    assert zia_acctunit._fund_give == 0.3125 * default_fund_pool()
    assert zia_acctunit._fund_take == 0.275 * default_fund_pool()

    assert (
        sue_acctunit._fund_give + bob_acctunit._fund_give + zia_acctunit._fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_acctunit._fund_take + bob_acctunit._fund_take + zia_acctunit._fund_take
        == 1.0 * default_fund_pool()
    )


def test_BudUnit_settle_bud_CorrectlySetsAcctAttrs():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    yao_bud.add_l1_idea(ideaunit_shop("swim"))
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_text, 8))
    yao_bud.set_acctunit(acctunit_shop(bob_text))
    yao_bud.set_acctunit(acctunit_shop(zia_text))
    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)
    assert sue_acctunit._fund_give == 0
    assert sue_acctunit._fund_take == 0
    assert bob_acctunit._fund_give == 0
    assert bob_acctunit._fund_take == 0
    assert zia_acctunit._fund_give == 0
    assert zia_acctunit._fund_take == 0

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert (
        sue_acctunit._fund_give + bob_acctunit._fund_give + zia_acctunit._fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_acctunit._fund_take + bob_acctunit._fund_take + zia_acctunit._fund_take
        == 1.0 * default_fund_pool()
    )


def clear_all_acctunits_lobbyboxs_fund_agenda_give_take(x_bud: BudUnit):
    # DELETE bud_agenda_debt and bud_agenda_cred
    for lobbybox_x in x_bud._lobbyboxs.values():
        lobbybox_x.reset_fund_give_take()
        # for lobbyship_x in lobbybox_x._accts.values():
        #     print(f"{lobbybox_x.} {lobbyship_x.}  {lobbyship_x._fund_give:.6f} {lobbyship_x.debtor_weight=} {lobbyship__fund_take:t:.6f} {lobbyship_x.} ")

    # DELETE bud_agenda_debt and bud_agenda_cred
    for x_acctunit in x_bud._accts.values():
        x_acctunit.reset_fund_give_take()


@dataclass
class LobbyAgendaMetrics:
    sum_lobbybox_cred: float = 0
    sum_lobbybox_debt: float = 0
    sum_lobbyship_cred: float = 0
    sum_lobbyship_debt: float = 0
    lobbyship_count: int = 0

    def set_sums(self, x_bud: BudUnit):
        for x_lobbybox in x_bud._lobbyboxs.values():
            self.sum_lobbybox_cred += x_lobbybox._fund_agenda_give
            self.sum_lobbybox_debt += x_lobbybox._fund_agenda_take
            for lobbyship_x in x_lobbybox._lobbyships.values():
                self.sum_lobbyship_cred += lobbyship_x._fund_agenda_give
                self.sum_lobbyship_debt += lobbyship_x._fund_agenda_take
                self.lobbyship_count += 1


@dataclass
class AcctAgendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_sums(self, x_bud: BudUnit):
        for acctunit in x_bud._accts.values():
            self.sum_agenda_cred += acctunit._fund_agenda_give
            self.sum_agenda_debt += acctunit._fund_agenda_take
            self.sum_agenda_ratio_cred += acctunit._fund_agenda_ratio_give
            self.sum_agenda_ratio_debt += acctunit._fund_agenda_ratio_take


@dataclass
class AwardAgendaMetrics:
    sum_bud_agenda_share = 0
    agenda_no_count = 0
    agenda_yes_count = 0
    agenda_no_bud_i_sum = 0
    agenda_yes_bud_i_sum = 0

    def set_sums(self, agenda_dict: dict[RoadUnit, IdeaUnit]):
        for agenda_item in agenda_dict.values():
            self.sum_bud_agenda_share += agenda_item.get_fund_share()
            if agenda_item._awardlines == {}:
                self.agenda_no_count += 1
                self.agenda_no_bud_i_sum += agenda_item.get_fund_share()
            else:
                self.agenda_yes_count += 1
                self.agenda_yes_bud_i_sum += agenda_item.get_fund_share()


def test_BudUnit_agenda_cred_debt_IsCorrectlySet():
    # ESTABLISH
    x_bud = budunit_v001_with_large_agenda()
    clear_all_acctunits_lobbyboxs_fund_agenda_give_take(x_bud=x_bud)

    # TEST bud_agenda_debt and bud_agenda_cred are empty
    x_lobbyagendametrics = LobbyAgendaMetrics()
    x_lobbyagendametrics.set_sums(x_bud=x_bud)
    assert x_lobbyagendametrics.sum_lobbybox_cred == 0
    assert x_lobbyagendametrics.sum_lobbybox_debt == 0
    assert x_lobbyagendametrics.sum_lobbyship_cred == 0
    assert x_lobbyagendametrics.sum_lobbyship_debt == 0

    # TEST bud_agenda_debt and bud_agenda_cred are empty
    x_acctagendametrics = AcctAgendaMetrics()
    x_acctagendametrics.set_sums(x_bud=x_bud)
    assert x_acctagendametrics.sum_agenda_cred == 0
    assert x_acctagendametrics.sum_agenda_debt == 0
    assert x_acctagendametrics.sum_agenda_ratio_cred == 0
    assert x_acctagendametrics.sum_agenda_ratio_debt == 0

    # WHEN
    agenda_dict = x_bud.get_agenda_dict()

    # THEN
    assert len(agenda_dict) == 63
    x_awardagendametrics = AwardAgendaMetrics()
    x_awardagendametrics.set_sums(agenda_dict=agenda_dict)
    # print(f"{sum_bud_agenda_share=}")
    # assert x_awardagendametrics.agenda_no_count == 14
    assert x_awardagendametrics.agenda_yes_count == 49
    assert x_awardagendametrics.agenda_no_bud_i_sum == 0.003747268 * default_fund_pool()
    assert (
        x_awardagendametrics.agenda_yes_bud_i_sum == 0.002796505 * default_fund_pool()
    )
    assert are_equal(
        x_awardagendametrics.agenda_no_bud_i_sum
        + x_awardagendametrics.agenda_yes_bud_i_sum,
        x_awardagendametrics.sum_bud_agenda_share,
    )
    assert (
        x_awardagendametrics.sum_bud_agenda_share == 0.006543773 * default_fund_pool()
    )

    x_lobbyagendametrics = LobbyAgendaMetrics()
    x_lobbyagendametrics.set_sums(x_bud=x_bud)
    assert x_lobbyagendametrics.lobbyship_count == 81
    x_sum = 2796504.9999999995
    print(f"{x_lobbyagendametrics.sum_lobbybox_cred=}")
    assert are_equal(x_lobbyagendametrics.sum_lobbybox_cred, x_sum)
    assert are_equal(x_lobbyagendametrics.sum_lobbybox_debt, x_sum)
    assert are_equal(x_lobbyagendametrics.sum_lobbyship_cred, x_sum)
    assert are_equal(x_lobbyagendametrics.sum_lobbyship_debt, x_sum)
    assert are_equal(
        x_awardagendametrics.agenda_yes_bud_i_sum,
        x_lobbyagendametrics.sum_lobbybox_cred,
    )

    assert all_acctunits_have_legitimate_values(x_bud)

    x_acctagendametrics = AcctAgendaMetrics()
    x_acctagendametrics.set_sums(x_bud=x_bud)
    assert are_equal(
        x_acctagendametrics.sum_agenda_cred,
        x_awardagendametrics.sum_bud_agenda_share,
    )
    assert are_equal(
        x_acctagendametrics.sum_agenda_debt,
        x_awardagendametrics.sum_bud_agenda_share,
    )
    assert are_equal(x_acctagendametrics.sum_agenda_ratio_cred, 1)
    assert are_equal(x_acctagendametrics.sum_agenda_ratio_debt, 1)

    # acctunit_fund_give_sum = 0.0
    # acctunit_fund_take_sum = 0.0

    # assert acctunit_fund_give_sum == 1.0
    # assert acctunit_fund_take_sum > 0.9999999
    # assert acctunit_fund_take_sum < 1.00000001


def all_acctunits_have_legitimate_values(x_bud: BudUnit):
    return not any(
        (
            acctunit._fund_give is None
            or acctunit._fund_give in [0.25, 0.5]
            or acctunit._fund_take is None
            or acctunit._fund_take in [0.8, 0.1]
        )
        for acctunit in x_bud._accts.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000001
    return abs(x1 - x2) < e10


def test_BudUnit_agenda_ratio_cred_debt_IsCorrectlySetWhenBudIsEmpty():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    sue_acctunit = acctunit_shop(sue_text, 0.5, debtor_weight=2)
    bob_acctunit = acctunit_shop(bob_text, 1.5, debtor_weight=3)
    zia_acctunit = acctunit_shop(zia_text, 8, debtor_weight=5)
    yao_bud.set_acctunit(sue_acctunit)
    yao_bud.set_acctunit(bob_acctunit)
    yao_bud.set_acctunit(zia_acctunit)
    yao_bud_sue_acct = yao_bud.get_acct(sue_text)
    yao_bud_bob_acct = yao_bud.get_acct(bob_text)
    yao_bud_zia_acct = yao_bud.get_acct(zia_text)

    assert yao_bud_sue_acct._fund_agenda_give in [0, None]
    assert yao_bud_sue_acct._fund_agenda_take in [0, None]
    assert yao_bud_bob_acct._fund_agenda_give in [0, None]
    assert yao_bud_bob_acct._fund_agenda_take in [0, None]
    assert yao_bud_zia_acct._fund_agenda_give in [0, None]
    assert yao_bud_zia_acct._fund_agenda_take in [0, None]
    assert yao_bud_sue_acct._fund_agenda_ratio_give != 0.05
    assert yao_bud_sue_acct._fund_agenda_ratio_take != 0.2
    assert yao_bud_bob_acct._fund_agenda_ratio_give != 0.15
    assert yao_bud_bob_acct._fund_agenda_ratio_take != 0.3
    assert yao_bud_zia_acct._fund_agenda_ratio_give != 0.8
    assert yao_bud_zia_acct._fund_agenda_ratio_take != 0.5

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud_sue_acct._fund_agenda_give == 0
    assert yao_bud_sue_acct._fund_agenda_take == 0
    assert yao_bud_bob_acct._fund_agenda_give == 0
    assert yao_bud_bob_acct._fund_agenda_take == 0
    assert yao_bud_zia_acct._fund_agenda_give == 0
    assert yao_bud_zia_acct._fund_agenda_take == 0
    assert yao_bud_sue_acct._fund_agenda_ratio_give == 0.05
    assert yao_bud_sue_acct._fund_agenda_ratio_take == 0.2
    assert yao_bud_bob_acct._fund_agenda_ratio_give == 0.15
    assert yao_bud_bob_acct._fund_agenda_ratio_take == 0.3
    assert yao_bud_zia_acct._fund_agenda_ratio_give == 0.8
    assert yao_bud_zia_acct._fund_agenda_ratio_take == 0.5


def test_BudUnit_settle_bud_CreatesLobbyBoxWith_budunit_v001():
    # ESTABLISH / WHEN
    x_bud = budunit_v001()
    x_bud.settle_bud()

    # THEN
    assert x_bud._lobbyboxs is not None
    assert len(x_bud._lobbyboxs) == 34
    everyone_accts_len = None
    everyone_lobby = x_bud.get_lobbybox(",Everyone")
    everyone_accts_len = len(everyone_lobby._lobbyships)
    assert everyone_accts_len == 22

    # WHEN
    x_bud.settle_bud()
    idea_dict = x_bud._idea_dict

    # THEN
    # print(f"{len(idea_dict)=}")
    db_idea = idea_dict.get(x_bud.make_l1_road("D&B"))
    assert len(db_idea._awardlinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._label == "D&B":
    #         print(f"{idea._label=} {idea._awardlinks=}")
    #         db_awardlink_len = len(idea._awardlinks)
    # assert db_awardlink_len == 3
