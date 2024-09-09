from src._instrument.python_tool import get_False_if_None
from src._road.finance import default_fund_pool
from src.bud.examples.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with7amCleanTableReason,
)
from src.bud.healer import healerlink_shop
from src.bud.acct import AcctID
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.bud.group import awardline_shop, awardlink_shop
from src.bud.graphic import display_ideatree
from pytest import raises as pytest_raises


def test_BudUnit_settle_bud_CorrectlySets_econs_justified_WhenBudUnitEmpty():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified


def test_BudUnit_settle_bud_CorrectlySets_econs_justified_WhenThereAreNotAny():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified


def test_BudUnit_settle_bud_CorrectlySets_econs_justified_WhenSingleIdeaUnit_healerlink_any_group_id_exists_IsTrue():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud.set_l1_idea(ideaunit_shop("Texas", _healerlink=healerlink_shop({"Yao"})))
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified is False


def test_BudUnit_settle_bud_CorrectlySets_econs_justified_WhenSingleProblemAndEcon():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_text = "Yao"
    sue_bud.add_acctunit(yao_text)
    yao_healerlink = healerlink_shop({yao_text})
    sue_bud.set_l1_idea(
        ideaunit_shop("Texas", _healerlink=yao_healerlink, problem_bool=True)
    )
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified


def test_BudUnit_settle_bud_CorrectlySets_econs_justified_WhenEconIsLevelAboveProblem():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_text = "Yao"
    sue_bud.add_acctunit(yao_text)
    yao_healerlink = healerlink_shop({yao_text})

    texas_text = "Texas"
    texas_road = sue_bud.make_l1_road(texas_text)
    sue_bud.set_l1_idea(ideaunit_shop(texas_text, problem_bool=True))
    ep_text = "El Paso"
    sue_bud.set_idea(ideaunit_shop(ep_text, _healerlink=yao_healerlink), texas_road)
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified


def test_BudUnit_settle_bud_CorrectlySets_econs_justified_WhenEconIsLevelBelowProblem():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_text = "Texas"
    texas_road = sue_bud.make_l1_road(texas_text)
    yao_healerlink = healerlink_shop({"Yao"})
    sue_bud.set_l1_idea(ideaunit_shop(texas_text, _healerlink=yao_healerlink))
    sue_bud.set_idea(ideaunit_shop("El Paso", problem_bool=True), texas_road)
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified is False


def test_BudUnit_settle_bud_CorrectlyRaisesErrorWhenEconIsLevelBelowProblem():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_text = "Texas"
    texas_road = sue_bud.make_l1_road(texas_text)
    yao_healerlink = healerlink_shop({"Yao"})
    texas_idea = ideaunit_shop(texas_text, _healerlink=yao_healerlink)
    sue_bud.set_l1_idea(texas_idea)
    elpaso_idea = ideaunit_shop("El Paso", problem_bool=True)
    sue_bud.set_idea(elpaso_idea, texas_road)
    assert sue_bud._econs_justified is False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.settle_bud(econ_exceptions=True)
    assert (
        str(excinfo.value)
        == f"IdeaUnit '{elpaso_idea.get_road()}' cannot sponsor ancestor econs."
    )


def test_BudUnit_settle_bud_CorrectlySets_econs_justified_WhenTwoEconsAreOneTheEqualLine():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_text = "Texas"
    texas_road = sue_bud.make_l1_road(texas_text)
    texas_idea = ideaunit_shop(
        texas_text, _healerlink=yao_healerlink, problem_bool=True
    )
    sue_bud.set_l1_idea(texas_idea)
    elpaso_idea = ideaunit_shop(
        "El Paso", _healerlink=yao_healerlink, problem_bool=True
    )
    sue_bud.set_idea(elpaso_idea, texas_road)
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified is False


def test_BudUnit_get_idea_dict_RaisesErrorWhen_econs_justified_IsFalse():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_text = "Texas"
    texas_road = sue_bud.make_l1_road(texas_text)
    texas_idea = ideaunit_shop(
        texas_text, _healerlink=yao_healerlink, problem_bool=True
    )
    sue_bud.set_l1_idea(texas_idea)
    elpaso_idea = ideaunit_shop(
        "El Paso", _healerlink=yao_healerlink, problem_bool=True
    )
    sue_bud.set_idea(elpaso_idea, texas_road)
    sue_bud.settle_bud()
    assert sue_bud._econs_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_idea_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because _econs_justified={sue_bud._econs_justified}."
    )
