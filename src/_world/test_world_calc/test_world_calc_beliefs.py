from src._world.beliefstory import awardlink_shop
from src._world.examples.example_worlds import (
    get_world_1Task_1CE0MinutesReason_1Fact,
)
from src._world.char import charunit_shop
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_calc_world_metrics_CorrectlyCalculates1LevelWorldBeliefWorldImportance():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_text = "Sue"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(yao_text, credor_weight=20, debtor_weight=6)
    zia_awardlink = awardlink_shop(zia_text, credor_weight=10, debtor_weight=1)
    Xio_awardlink = awardlink_shop(Xio_text, credor_weight=10)
    x_world._idearoot.set_awardlink(awardlink=yao_awardlink)
    x_world._idearoot.set_awardlink(awardlink=zia_awardlink)
    x_world._idearoot.set_awardlink(awardlink=Xio_awardlink)

    assert len(x_world._beliefs) == 3

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    belief_yao = x_world.get_beliefbox(yao_text)
    belief_zia = x_world.get_beliefbox(zia_text)
    belief_Xio = x_world.get_beliefbox(Xio_text)
    assert belief_yao._world_cred == 0.5
    assert belief_yao._world_debt == 0.75
    assert belief_zia._world_cred == 0.25
    assert belief_zia._world_debt == 0.125
    assert belief_Xio._world_cred == 0.25
    assert belief_Xio._world_debt == 0.125
    assert belief_yao._world_cred + belief_zia._world_cred + belief_Xio._world_cred == 1
    assert belief_yao._world_debt + belief_zia._world_debt + belief_Xio._world_debt == 1

    # WHEN
    x_world.set_charunit(charunit_shop(sue_text))
    bl_sue = awardlink_shop(sue_text, credor_weight=37)
    x_world._idearoot.set_awardlink(awardlink=bl_sue)
    assert len(x_world._beliefs) == 4
    x_world.calc_world_metrics()

    # THEN
    belief_sue = x_world.get_beliefbox(sue_text)
    assert belief_yao._world_cred != 0.5
    assert belief_yao._world_debt != 0.75
    assert belief_zia._world_cred != 0.25
    assert belief_zia._world_debt != 0.125
    assert belief_Xio._world_cred != 0.25
    assert belief_Xio._world_debt != 0.125
    assert belief_sue._world_cred != None
    assert belief_sue._world_debt != None
    assert (
        belief_yao._world_cred
        + belief_zia._world_cred
        + belief_Xio._world_cred
        + belief_sue._world_cred
        == 1
    )
    assert (
        belief_yao._world_debt
        + belief_zia._world_debt
        + belief_Xio._world_debt
        + belief_sue._world_debt
        == 1
    )


def test_WorldUnit_calc_world_metrics_CorrectlyCalculates3levelWorldBeliefWorldImportance():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    swim_text = "swim"
    x_world.add_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(
        belief_id=yao_text, credor_weight=20, debtor_weight=6
    )
    zia_awardlink = awardlink_shop(
        belief_id=zia_text, credor_weight=10, debtor_weight=1
    )
    parm_awardlink = awardlink_shop(Xio_text, credor_weight=10)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=yao_awardlink)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=zia_awardlink)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=parm_awardlink)
    assert len(x_world._beliefs) == 3

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    belief_yao = x_world.get_beliefbox(yao_text)
    belief_zia = x_world.get_beliefbox(zia_text)
    belief_Xio = x_world.get_beliefbox(Xio_text)
    assert belief_yao._world_cred == 0.5
    assert belief_yao._world_debt == 0.75
    assert belief_zia._world_cred == 0.25
    assert belief_zia._world_debt == 0.125
    assert belief_Xio._world_cred == 0.25
    assert belief_Xio._world_debt == 0.125
    assert belief_yao._world_cred + belief_zia._world_cred + belief_Xio._world_cred == 1
    assert belief_yao._world_debt + belief_zia._world_debt + belief_Xio._world_debt == 1


def test_WorldUnit_calc_world_metrics_CorrectlyCalculatesBeliefWorldImportanceLWwithBeliefEmptyAncestors():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    swim_text = "swim"
    x_world.add_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(
        belief_id=yao_text, credor_weight=20, debtor_weight=6
    )
    zia_awardlink = awardlink_shop(
        belief_id=zia_text, credor_weight=10, debtor_weight=1
    )
    parm_awardlink = awardlink_shop(Xio_text, credor_weight=10)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=yao_awardlink)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=zia_awardlink)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=parm_awardlink)

    # no awardlinks attached to this one
    x_world.add_l1_idea(ideaunit_shop("hunt", _weight=3))

    # WHEN
    x_world.calc_world_metrics()

    # THEN

    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._awardlinks[yao_text]
    assert str(excinfo.value) == f"'{yao_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._awardlinks[zia_text]
    assert str(excinfo.value) == f"'{zia_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._awardlinks[Xio_text]
    assert str(excinfo.value) == f"'{Xio_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._kids["hunt"]._awardheirs[yao_text]
    assert str(excinfo.value) == f"'{yao_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._kids["hunt"]._awardheirs[zia_text]
    assert str(excinfo.value) == f"'{zia_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._kids["hunt"]._awardheirs[Xio_text]
    assert str(excinfo.value) == f"'{Xio_text}'"

    # THEN
    belief_yao = x_world.get_beliefbox(yao_text)
    belief_zia = x_world.get_beliefbox(zia_text)
    belief_Xio = x_world.get_beliefbox(Xio_text)
    assert belief_yao._world_cred == 0.125
    assert belief_yao._world_debt == 0.1875
    assert belief_zia._world_cred == 0.0625
    assert belief_zia._world_debt == 0.03125
    assert belief_Xio._world_cred == 0.0625
    assert belief_Xio._world_debt == 0.03125
    assert (
        belief_yao._world_cred + belief_zia._world_cred + belief_Xio._world_cred == 0.25
    )
    assert (
        belief_yao._world_debt + belief_zia._world_debt + belief_Xio._world_debt == 0.25
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
