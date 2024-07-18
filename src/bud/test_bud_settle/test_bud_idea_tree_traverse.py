from src._instrument.python import get_False_if_None
from src._road.finance import default_fund_pool
from src.bud.examples.example_buds import (
    get_bud_with_4_levels as example_buds_get_bud_with_4_levels,
)
from src.bud.healer import healerhold_shop
from src.bud.char import CharID
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.bud.lobby import awardline_shop, awardlink_shop
from src.bud.graphic import display_ideatree
from pytest import raises as pytest_raises


def test_BudUnit_set_tree_traverse_stage_CorrectlySetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_idea_dict = {1: 2, 2: 4}
    sue_bud._rational = x_rational
    sue_bud._tree_traverse_count = x_tree_traverse_count
    sue_bud._idea_dict = x_idea_dict
    assert sue_bud._rational == x_rational
    assert sue_bud._tree_traverse_count == x_tree_traverse_count
    assert sue_bud._idea_dict == x_idea_dict

    # WHEN
    sue_bud._set_tree_traverse_stage()

    # THEN
    assert sue_bud._rational != x_rational
    assert not sue_bud._rational
    assert sue_bud._tree_traverse_count != x_tree_traverse_count
    assert sue_bud._tree_traverse_count == 0
    assert sue_bud._idea_dict != x_idea_dict
    assert sue_bud._idea_dict == {sue_bud._idearoot.get_road(): sue_bud._idearoot}


def test_BudUnit_clear_bud_base_metrics_CorrectlySetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    x_econ_justifed = False
    x_sum_healerhold_share = 140
    sue_bud._econs_justified = x_econ_justifed
    sue_bud._econs_buildable = "swimmers"
    sue_bud._sum_healerhold_share = x_sum_healerhold_share
    sue_bud._econ_dict = {"run": "run"}
    sue_bud._healers_dict = {"run": "run"}
    assert sue_bud._econs_justified == x_econ_justifed
    assert sue_bud._econs_buildable
    assert sue_bud._sum_healerhold_share == x_sum_healerhold_share
    assert sue_bud._econ_dict != {}
    assert sue_bud._healers_dict != {}

    # WHEN
    sue_bud._clear_bud_base_metrics()

    # THEN
    assert sue_bud._econs_justified != x_econ_justifed
    assert sue_bud._econs_justified
    assert sue_bud._econs_buildable is False
    assert sue_bud._sum_healerhold_share == 0
    assert not sue_bud._econ_dict
    assert not sue_bud._healers_dict


def test_BudUnit_settle_bud_ClearsDescendantAttributes():
    # ESTABLISH
    x_bud = example_buds_get_bud_with_4_levels()
    # test root status:
    casa_text = "casa"
    week_text = "weekdays"
    mon_text = "Monday"
    yrx = x_bud._idearoot
    assert yrx._descendant_pledge_count is None
    assert yrx._all_char_cred is None
    assert yrx._all_char_debt is None
    assert yrx._kids[casa_text]._descendant_pledge_count is None
    assert yrx._kids[casa_text]._all_char_cred is None
    assert yrx._kids[casa_text]._all_char_debt is None
    assert yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count is None
    assert yrx._kids[week_text]._kids[mon_text]._all_char_cred is None
    assert yrx._kids[week_text]._kids[mon_text]._all_char_debt is None

    yrx._descendant_pledge_count = -2
    yrx._all_char_cred = -2
    yrx._all_char_debt = -2
    yrx._kids[casa_text]._descendant_pledge_count = -2
    yrx._kids[casa_text]._all_char_cred = -2
    yrx._kids[casa_text]._all_char_debt = -2
    yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count = -2
    yrx._kids[week_text]._kids[mon_text]._all_char_cred = -2
    yrx._kids[week_text]._kids[mon_text]._all_char_debt = -2

    assert yrx._descendant_pledge_count == -2
    assert yrx._all_char_cred == -2
    assert yrx._all_char_debt == -2
    assert yrx._kids[casa_text]._descendant_pledge_count == -2
    assert yrx._kids[casa_text]._all_char_cred == -2
    assert yrx._kids[casa_text]._all_char_debt == -2
    assert yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count == -2
    assert yrx._kids[week_text]._kids[mon_text]._all_char_cred == -2
    assert yrx._kids[week_text]._kids[mon_text]._all_char_debt == -2

    # WHEN
    x_bud.settle_bud()

    # THEN
    assert yrx._descendant_pledge_count == 2
    assert yrx._kids[casa_text]._descendant_pledge_count == 0
    assert yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count == 0

    assert yrx._kids[week_text]._kids[mon_text]._all_char_cred == True
    assert yrx._kids[week_text]._kids[mon_text]._all_char_debt == True
    assert yrx._kids[casa_text]._all_char_cred == True
    assert yrx._kids[casa_text]._all_char_debt == True
    assert yrx._all_char_cred == True
    assert yrx._all_char_debt == True


def test_BudUnit_settle_bud_RootOnlyCorrectlySetsDescendantAttributes():
    # ESTABLISH
    tim_bud = budunit_shop(_owner_id="Tim")
    assert tim_bud._idearoot._descendant_pledge_count is None
    assert tim_bud._idearoot._all_char_cred is None
    assert tim_bud._idearoot._all_char_debt is None

    # WHEN
    tim_bud.settle_bud()

    # THEN
    assert tim_bud._idearoot._descendant_pledge_count == 0
    assert tim_bud._idearoot._all_char_cred == True
    assert tim_bud._idearoot._all_char_debt == True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_1():
    # ESTABLISH
    x_bud = example_buds_get_bud_with_4_levels()
    casa_text = "casa"
    casa_road = x_bud.make_l1_road(casa_text)
    week_text = "weekdays"
    mon_text = "Monday"

    email_text = "email"
    email_idea = ideaunit_shop(_label=email_text, pledge=True)
    x_bud.add_idea(email_idea, parent_road=casa_road)

    # test root status:
    x_idearoot = x_bud.get_idea_obj(x_bud._real_id)
    assert x_idearoot._descendant_pledge_count is None
    assert x_idearoot._all_char_cred is None
    assert x_idearoot._all_char_debt is None
    assert x_idearoot._kids[casa_text]._descendant_pledge_count is None
    assert x_idearoot._kids[casa_text]._all_char_cred is None
    assert x_idearoot._kids[casa_text]._all_char_debt is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._descendant_pledge_count is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_char_cred is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_char_debt is None

    # WHEN
    x_bud.settle_bud()

    # THEN
    assert x_idearoot._descendant_pledge_count == 3
    assert x_idearoot._kids[casa_text]._descendant_pledge_count == 1
    assert x_idearoot._kids[casa_text]._kids[email_text]._descendant_pledge_count == 0
    assert x_idearoot._kids[week_text]._kids[mon_text]._descendant_pledge_count == 0
    assert x_idearoot._all_char_cred == True
    assert x_idearoot._all_char_debt == True
    assert x_idearoot._kids[casa_text]._all_char_cred == True
    assert x_idearoot._kids[casa_text]._all_char_debt == True
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_char_cred == True
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_char_debt == True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_2():
    # ESTABLISH
    x_bud = example_buds_get_bud_with_4_levels()
    email_text = "email"
    casa_text = "casa"
    week_text = "weekdays"
    mon_text = "Monday"
    tue_text = "Tuesday"
    vacuum_text = "vacuum"
    sue_text = "Sue"

    casa_road = x_bud.make_l1_road(casa_text)
    email_idea = ideaunit_shop(_label=email_text, pledge=True)
    x_bud.add_idea(email_idea, parent_road=casa_road)
    vacuum_idea = ideaunit_shop(_label=vacuum_text, pledge=True)
    x_bud.add_idea(vacuum_idea, parent_road=casa_road)

    x_bud.add_charunit(char_id=sue_text)
    x_awardlink = awardlink_shop(lobby_id=sue_text)

    x_bud._idearoot._kids[casa_text]._kids[email_text].set_awardlink(
        awardlink=x_awardlink
    )
    # print(x_bud._kids[casa_text]._kids[email_text])
    # print(x_bud._kids[casa_text]._kids[email_text]._awardlink)

    # WHEN
    x_bud.settle_bud()
    # print(x_bud._kids[casa_text]._kids[email_text])
    # print(x_bud._kids[casa_text]._kids[email_text]._awardlink)

    # THEN
    assert x_bud._idearoot._all_char_cred is False
    assert x_bud._idearoot._all_char_debt is False
    casa_idea = x_bud._idearoot._kids[casa_text]
    assert casa_idea._all_char_cred is False
    assert casa_idea._all_char_debt is False
    assert casa_idea._kids[email_text]._all_char_cred is False
    assert casa_idea._kids[email_text]._all_char_debt is False
    assert casa_idea._kids[vacuum_text]._all_char_cred == True
    assert casa_idea._kids[vacuum_text]._all_char_debt == True
    week_idea = x_bud._idearoot._kids[week_text]
    assert week_idea._all_char_cred == True
    assert week_idea._all_char_debt == True
    assert week_idea._kids[mon_text]._all_char_cred == True
    assert week_idea._kids[mon_text]._all_char_debt == True
    assert week_idea._kids[tue_text]._all_char_cred == True
    assert week_idea._kids[tue_text]._all_char_debt == True


def test_BudUnit_settle_bud_Sets_fund_ratio_WithSomeIdeasOfZero_weightScenario0():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = sue_bud.make_road(casa_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, pledge=True)
    sue_bud.add_idea(floor_idea, casa_road)
    sue_bud.add_l1_idea(ideaunit_shop("unimportant"))

    status_text = "cleaniness status"
    status_road = sue_bud.make_road(casa_road, status_text)
    sue_bud.add_idea(ideaunit_shop(status_text, _weight=0), casa_road)

    non_text = "not clean"
    yes_text = "yes clean"
    non_road = sue_bud.make_road(status_road, non_text)
    yes_road = sue_bud.make_road(status_road, yes_text)
    sue_bud.add_idea(ideaunit_shop(non_text), status_road)
    sue_bud.add_idea(ideaunit_shop(yes_text, _weight=2), status_road)

    assert sue_bud.get_idea_obj(casa_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(floor_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(status_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(non_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(yes_road)._fund_ratio is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud._fund_pool=}")
    assert sue_bud.get_idea_obj(casa_road)._fund_ratio == 0.5
    assert sue_bud.get_idea_obj(floor_road)._fund_ratio == 0.5
    assert sue_bud.get_idea_obj(status_road)._fund_ratio == 0.0
    assert sue_bud.get_idea_obj(non_road)._fund_ratio == 0.0
    assert sue_bud.get_idea_obj(yes_road)._fund_ratio == 0.0


def test_BudUnit_settle_bud_Sets_fund_ratio_WithSomeIdeasOfZero_weightScenario1():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = sue_bud.make_road(casa_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, pledge=True)
    sue_bud.add_idea(floor_idea, casa_road)
    sue_bud.add_l1_idea(ideaunit_shop("unimportant"))

    status_text = "cleaniness status"
    status_road = sue_bud.make_road(casa_road, status_text)
    sue_bud.add_idea(ideaunit_shop(status_text), casa_road)

    status_idea = sue_bud.get_idea_obj(status_road)
    print(f"{status_idea._weight=}")
    print("This should raise error: 'Ideaunit._'")

    clean_text = "clean"
    clean_road = sue_bud.make_road(status_road, clean_text)
    very_text = "very_much"
    mod_text = "moderately"
    dirty_text = "dirty"

    sue_bud.add_idea(ideaunit_shop(clean_text, _weight=0), status_road)
    sue_bud.add_idea(ideaunit_shop(very_text), clean_road)
    sue_bud.add_idea(ideaunit_shop(mod_text, _weight=2), clean_road)
    sue_bud.add_idea(ideaunit_shop(dirty_text), clean_road)

    very_road = sue_bud.make_road(clean_road, very_text)
    mod_road = sue_bud.make_road(clean_road, mod_text)
    dirty_road = sue_bud.make_road(clean_road, dirty_text)
    assert sue_bud.get_idea_obj(casa_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(floor_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(status_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(clean_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(very_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(mod_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(dirty_road)._fund_ratio is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud._fund_pool=}")
    assert sue_bud.get_idea_obj(casa_road)._fund_ratio == 0.5
    assert sue_bud.get_idea_obj(floor_road)._fund_ratio == 0.25
    assert sue_bud.get_idea_obj(status_road)._fund_ratio == 0.25
    assert sue_bud.get_idea_obj(clean_road)._fund_ratio == 0
    assert sue_bud.get_idea_obj(very_road)._fund_ratio == 0
    assert sue_bud.get_idea_obj(mod_road)._fund_ratio == 0
    assert sue_bud.get_idea_obj(dirty_road)._fund_ratio == 0


def test_BudUnit_settle_bud_TreeTraverseSetsClearsAwardLineestorsCorrectly():
    # ESTABLISH
    x_bud = example_buds_get_bud_with_4_levels()
    x_bud.settle_bud()
    # idea tree has no awardlinks
    assert x_bud._idearoot._awardlines == {}
    x_bud._idearoot._awardlines = {1: "testtest"}
    assert x_bud._idearoot._awardlines != {}

    # WHEN
    x_bud.settle_bud()

    # THEN
    assert not x_bud._idearoot._awardlines

    # WHEN
    # test for level 1 and level n
    casa_text = "casa"
    casa_idea = x_bud._idearoot._kids[casa_text]
    casa_idea._awardlines = {1: "testtest"}
    assert casa_idea._awardlines != {}
    x_bud.settle_bud()

    # THEN
    assert not x_bud._idearoot._kids[casa_text]._awardlines


def test_BudUnit_settle_bud_TreeTraverseSetsAwardLineestorFromRootCorrectly():
    # ESTABLISH
    x_bud = example_buds_get_bud_with_4_levels()
    x_bud.settle_bud()
    # idea tree has no awardlinks
    assert x_bud._idearoot._awardlines == {}
    sue_text = "Sue"
    week_text = "weekdays"
    nation_text = "nation-state"
    sue_awardlink = awardlink_shop(lobby_id=sue_text)
    x_bud.add_charunit(char_id=sue_text)
    x_bud._idearoot.set_awardlink(awardlink=sue_awardlink)
    # idea tree has awardlines
    assert x_bud._idearoot._awardheirs.get(sue_text) is None

    # WHEN
    x_bud.settle_bud()

    # THEN
    assert x_bud._idearoot._awardheirs.get(sue_text) is not None
    assert x_bud._idearoot._awardheirs.get(sue_text).lobby_id == sue_text
    assert x_bud._idearoot._awardlines != {}
    root_idea = x_bud.get_idea_obj(road=x_bud._idearoot._label)
    sue_awardline = x_bud._idearoot._awardlines.get(sue_text)
    print(f"{sue_awardline._fund_give=} {root_idea._fund_ratio=} ")
    print(f"  {sue_awardline._fund_take=} {root_idea._fund_ratio=} ")
    sum_x = 0
    cat_road = x_bud.make_l1_road("cat have dinner")
    cat_idea = x_bud.get_idea_obj(cat_road)
    week_road = x_bud.make_l1_road(week_text)
    week_idea = x_bud.get_idea_obj(week_road)
    casa_text = "casa"
    casa_road = x_bud.make_l1_road(casa_text)
    casa_idea = x_bud.get_idea_obj(casa_road)
    nation_road = x_bud.make_l1_road(nation_text)
    nation_idea = x_bud.get_idea_obj(nation_road)
    sum_x = cat_idea._fund_ratio
    print(f"{cat_idea._fund_ratio=} {sum_x} ")
    sum_x += week_idea._fund_ratio
    print(f"{week_idea._fund_ratio=} {sum_x} ")
    sum_x += casa_idea._fund_ratio
    print(f"{casa_idea._fund_ratio=} {sum_x} ")
    sum_x += nation_idea._fund_ratio
    print(f"{nation_idea._fund_ratio=} {sum_x} ")
    assert sum_x >= 1.0
    assert sum_x < 1.00000000001

    # for kid_idea in root_idea._kids.values():
    #     sum_x += kid_idea._fund_ratio
    #     print(f"  {kid_idea._fund_ratio=} {sum_x=} {kid_idea.get_road()=}")
    assert round(sue_awardline._fund_give, 15) == default_fund_pool()
    assert round(sue_awardline._fund_take, 15) == default_fund_pool()
    x_awardline = awardline_shop(
        lobby_id=sue_text,
        _fund_give=default_fund_pool(),
        _fund_take=default_fund_pool(),
    )
    assert x_bud._idearoot._awardlines == {x_awardline.lobby_id: x_awardline}


def test_BudUnit_settle_bud_TreeTraverseSetsAwardLineestorFromNonRootCorrectly():
    # ESTABLISH
    x_bud = example_buds_get_bud_with_4_levels()
    x_bud.settle_bud()
    # idea tree has no awardlinks
    sue_text = "Sue"
    assert x_bud._idearoot._awardlines == {}
    x_bud.add_charunit(char_id=sue_text)
    x_awardlink = awardlink_shop(lobby_id=sue_text)
    casa_text = "casa"
    email_text = "email"
    x_bud._idearoot._kids[casa_text].set_awardlink(awardlink=x_awardlink)

    # WHEN
    # idea tree has awardlinks
    x_bud.settle_bud()

    # THEN
    assert x_bud._idearoot._awardlines != {}
    print(f"{x_bud._idearoot._awardlines=}")
    x_awardline = awardline_shop(
        lobby_id=sue_text,
        _fund_give=0.230769231 * default_fund_pool(),
        _fund_take=0.230769231 * default_fund_pool(),
    )
    assert x_bud._idearoot._awardlines == {x_awardline.lobby_id: x_awardline}
    assert x_bud._idearoot._kids[casa_text]._awardlines != {}
    assert x_bud._idearoot._kids[casa_text]._awardlines == {
        x_awardline.lobby_id: x_awardline
    }


def test_BudUnit_get_idea_tree_ordered_road_list_ReturnsCorrectObj():
    # ESTABLISH
    x_bud = example_buds_get_bud_with_4_levels()
    week_text = "weekdays"
    assert x_bud.get_idea_tree_ordered_road_list()

    # WHEN
    ordered_node_list = x_bud.get_idea_tree_ordered_road_list()

    # THEN
    assert len(ordered_node_list) == 17
    x_1st_road_in_ordered_list = x_bud.get_idea_tree_ordered_road_list()[0]
    assert x_1st_road_in_ordered_list == x_bud._real_id
    x_8th_road_in_ordered_list = x_bud.get_idea_tree_ordered_road_list()[9]
    assert x_8th_road_in_ordered_list == x_bud.make_l1_road(week_text)

    # WHEN
    y_bud = budunit_shop()

    # THEN
    y_1st_road_in_ordered_list = y_bud.get_idea_tree_ordered_road_list()[0]
    assert y_1st_road_in_ordered_list == x_bud._real_id


def test_BudUnit_get_idea_tree_ordered_road_list_CorrectlyFiltersRangedIdeaRoadUnits():
    # ESTABLISH
    tim_bud = budunit_shop("Tim")

    # WHEN
    time = "timeline"
    tim_bud.add_l1_idea(ideaunit_shop(_label=time, _begin=0, _close=700))
    t_road = tim_bud.make_l1_road(time)
    week = "weeks"
    tim_bud.add_idea(ideaunit_shop(_label=week, _denom=7), parent_road=t_road)

    # THEN
    assert len(tim_bud.get_idea_tree_ordered_road_list()) == 3
    assert len(tim_bud.get_idea_tree_ordered_road_list(no_range_descendants=True)) == 2


def test_BudUnit_get_idea_dict_ReturnsCorrectObjWhenSingle():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_text = "Texas"
    sue_bud.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    casa_text = "casa"
    sue_bud.add_l1_idea(ideaunit_shop(casa_text))

    # WHEN
    problems_dict = sue_bud.get_idea_dict(problem=True)

    # THEN
    assert sue_bud._econs_justified
    texas_road = sue_bud.make_l1_road(texas_text)
    texas_idea = sue_bud.get_idea_obj(texas_road)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_road: texas_idea}


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
    sue_bud = example_buds_get_bud_with_4_levels()
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified


def test_BudUnit_settle_bud_CorrectlySets_econs_justified_WhenSingleIdeaUnit_healerhold_any_lobby_id_exists_IsTrue():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud.add_l1_idea(ideaunit_shop("Texas", _healerhold=healerhold_shop({"Yao"})))
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified is False


def test_BudUnit_settle_bud_CorrectlySets_econs_justified_WhenSingleProblemAndEcon():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_text = "Yao"
    sue_bud.add_charunit(yao_text)
    yao_healerhold = healerhold_shop({yao_text})
    sue_bud.add_l1_idea(
        ideaunit_shop("Texas", _healerhold=yao_healerhold, _problem_bool=True)
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
    sue_bud.add_charunit(yao_text)
    yao_healerhold = healerhold_shop({yao_text})

    texas_text = "Texas"
    texas_road = sue_bud.make_l1_road(texas_text)
    sue_bud.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    ep_text = "El Paso"
    sue_bud.add_idea(ideaunit_shop(ep_text, _healerhold=yao_healerhold), texas_road)
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
    yao_healerhold = healerhold_shop({"Yao"})
    sue_bud.add_l1_idea(ideaunit_shop(texas_text, _healerhold=yao_healerhold))
    sue_bud.add_idea(ideaunit_shop("El Paso", _problem_bool=True), texas_road)
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
    yao_healerhold = healerhold_shop({"Yao"})
    texas_idea = ideaunit_shop(texas_text, _healerhold=yao_healerhold)
    sue_bud.add_l1_idea(texas_idea)
    elpaso_idea = ideaunit_shop("El Paso", _problem_bool=True)
    sue_bud.add_idea(elpaso_idea, texas_road)
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
    yao_healerhold = healerhold_shop({"Yao"})
    texas_text = "Texas"
    texas_road = sue_bud.make_l1_road(texas_text)
    texas_idea = ideaunit_shop(
        texas_text, _healerhold=yao_healerhold, _problem_bool=True
    )
    sue_bud.add_l1_idea(texas_idea)
    elpaso_idea = ideaunit_shop(
        "El Paso", _healerhold=yao_healerhold, _problem_bool=True
    )
    sue_bud.add_idea(elpaso_idea, texas_road)
    assert sue_bud._econs_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._econs_justified is False


def test_BudUnit_get_idea_dict_RaisesErrorWhen_econs_justified_IsFalse():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_healerhold = healerhold_shop({"Yao"})
    texas_text = "Texas"
    texas_road = sue_bud.make_l1_road(texas_text)
    texas_idea = ideaunit_shop(
        texas_text, _healerhold=yao_healerhold, _problem_bool=True
    )
    sue_bud.add_l1_idea(texas_idea)
    elpaso_idea = ideaunit_shop(
        "El Paso", _healerhold=yao_healerhold, _problem_bool=True
    )
    sue_bud.add_idea(elpaso_idea, texas_road)
    sue_bud.settle_bud()
    assert sue_bud._econs_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_idea_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because _econs_justified={sue_bud._econs_justified}."
    )
