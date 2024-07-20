from src.bud.examples.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
)
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.bud.lobby import awardlink_shop
from src.bud.graphic import display_ideatree


def test_BudUnit_set_tree_traverse_stage_CorrectlySetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_idea_dict = {1: 2, 2: 4}
    sue_bud._rational = x_rational
    sue_bud._tree_traverse_count = x_tree_traverse_count
    sue_bud._idea_dict = x_idea_dict
    sue_bud._offtrack_kids_weight_set = "example"
    assert sue_bud._rational == x_rational
    assert sue_bud._tree_traverse_count == x_tree_traverse_count
    assert sue_bud._idea_dict == x_idea_dict
    assert sue_bud._offtrack_kids_weight_set != set()

    # WHEN
    sue_bud._set_tree_traverse_stage()

    # THEN
    assert sue_bud._rational != x_rational
    assert not sue_bud._rational
    assert sue_bud._tree_traverse_count != x_tree_traverse_count
    assert sue_bud._tree_traverse_count == 0
    assert sue_bud._idea_dict != x_idea_dict
    assert sue_bud._idea_dict == {sue_bud._idearoot.get_road(): sue_bud._idearoot}
    assert sue_bud._offtrack_kids_weight_set == set()


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
    x_bud = get_budunit_with_4_levels()
    # test root status:
    casa_text = "casa"
    week_text = "weekdays"
    mon_text = "Monday"
    yrx = x_bud._idearoot
    assert yrx._descendant_pledge_count is None
    assert yrx._all_acct_cred is None
    assert yrx._all_acct_debt is None
    assert yrx._kids[casa_text]._descendant_pledge_count is None
    assert yrx._kids[casa_text]._all_acct_cred is None
    assert yrx._kids[casa_text]._all_acct_debt is None
    assert yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count is None
    assert yrx._kids[week_text]._kids[mon_text]._all_acct_cred is None
    assert yrx._kids[week_text]._kids[mon_text]._all_acct_debt is None

    yrx._descendant_pledge_count = -2
    yrx._all_acct_cred = -2
    yrx._all_acct_debt = -2
    yrx._kids[casa_text]._descendant_pledge_count = -2
    yrx._kids[casa_text]._all_acct_cred = -2
    yrx._kids[casa_text]._all_acct_debt = -2
    yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count = -2
    yrx._kids[week_text]._kids[mon_text]._all_acct_cred = -2
    yrx._kids[week_text]._kids[mon_text]._all_acct_debt = -2

    assert yrx._descendant_pledge_count == -2
    assert yrx._all_acct_cred == -2
    assert yrx._all_acct_debt == -2
    assert yrx._kids[casa_text]._descendant_pledge_count == -2
    assert yrx._kids[casa_text]._all_acct_cred == -2
    assert yrx._kids[casa_text]._all_acct_debt == -2
    assert yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count == -2
    assert yrx._kids[week_text]._kids[mon_text]._all_acct_cred == -2
    assert yrx._kids[week_text]._kids[mon_text]._all_acct_debt == -2

    # WHEN
    x_bud.settle_bud()

    # THEN
    assert yrx._descendant_pledge_count == 2
    assert yrx._kids[casa_text]._descendant_pledge_count == 0
    assert yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count == 0

    assert yrx._kids[week_text]._kids[mon_text]._all_acct_cred == True
    assert yrx._kids[week_text]._kids[mon_text]._all_acct_debt == True
    assert yrx._kids[casa_text]._all_acct_cred == True
    assert yrx._kids[casa_text]._all_acct_debt == True
    assert yrx._all_acct_cred == True
    assert yrx._all_acct_debt == True


def test_BudUnit_settle_bud_RootOnlyCorrectlySetsDescendantAttributes():
    # ESTABLISH
    yao_bud = budunit_shop(_owner_id="Yao")
    assert yao_bud._idearoot._descendant_pledge_count is None
    assert yao_bud._idearoot._all_acct_cred is None
    assert yao_bud._idearoot._all_acct_debt is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud._idearoot._descendant_pledge_count == 0
    assert yao_bud._idearoot._all_acct_cred == True
    assert yao_bud._idearoot._all_acct_debt == True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_1():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels()
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
    assert x_idearoot._all_acct_cred is None
    assert x_idearoot._all_acct_debt is None
    assert x_idearoot._kids[casa_text]._descendant_pledge_count is None
    assert x_idearoot._kids[casa_text]._all_acct_cred is None
    assert x_idearoot._kids[casa_text]._all_acct_debt is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._descendant_pledge_count is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_acct_cred is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_acct_debt is None

    # WHEN
    x_bud.settle_bud()

    # THEN
    assert x_idearoot._descendant_pledge_count == 3
    assert x_idearoot._kids[casa_text]._descendant_pledge_count == 1
    assert x_idearoot._kids[casa_text]._kids[email_text]._descendant_pledge_count == 0
    assert x_idearoot._kids[week_text]._kids[mon_text]._descendant_pledge_count == 0
    assert x_idearoot._all_acct_cred == True
    assert x_idearoot._all_acct_debt == True
    assert x_idearoot._kids[casa_text]._all_acct_cred == True
    assert x_idearoot._kids[casa_text]._all_acct_debt == True
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_acct_cred == True
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_acct_debt == True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_2():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels()
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

    x_bud.add_acctunit(acct_id=sue_text)
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
    assert x_bud._idearoot._all_acct_cred is False
    assert x_bud._idearoot._all_acct_debt is False
    casa_idea = x_bud._idearoot._kids[casa_text]
    assert casa_idea._all_acct_cred is False
    assert casa_idea._all_acct_debt is False
    assert casa_idea._kids[email_text]._all_acct_cred is False
    assert casa_idea._kids[email_text]._all_acct_debt is False
    assert casa_idea._kids[vacuum_text]._all_acct_cred == True
    assert casa_idea._kids[vacuum_text]._all_acct_debt == True
    week_idea = x_bud._idearoot._kids[week_text]
    assert week_idea._all_acct_cred == True
    assert week_idea._all_acct_debt == True
    assert week_idea._kids[mon_text]._all_acct_cred == True
    assert week_idea._kids[mon_text]._all_acct_debt == True
    assert week_idea._kids[tue_text]._all_acct_cred == True
    assert week_idea._kids[tue_text]._all_acct_debt == True


def test_BudUnit_settle_bud_TreeTraverseSetsClearsAwardLineestorsCorrectly():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels()
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


def test_BudUnit_settle_bud_DoesNotKeepUnneeded_awardheirs():
    # ESTABLISH
    yao_text = "Yao"
    x_bud = budunit_shop(yao_text)
    zia_text = "Zia"
    Xio_text = "Xio"
    x_bud.add_acctunit(yao_text)
    x_bud.add_acctunit(zia_text)
    x_bud.add_acctunit(Xio_text)

    swim_text = "swim"
    swim_road = x_bud.make_l1_road(swim_text)

    x_bud.add_l1_idea(ideaunit_shop(swim_text))
    awardlink_yao = awardlink_shop(yao_text, give_weight=10)
    awardlink_zia = awardlink_shop(zia_text, give_weight=10)
    awardlink_Xio = awardlink_shop(Xio_text, give_weight=10)

    swim_idea = x_bud.get_idea_obj(swim_road)
    x_bud.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    x_bud.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    x_bud.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    assert len(swim_idea._awardlinks) == 3
    assert len(swim_idea._awardheirs) == 0

    # WHEN
    x_bud.settle_bud()

    # THEN
    assert len(swim_idea._awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    x_bud.edit_idea_attr(swim_road, awardlink_del=yao_text)
    assert len(swim_idea._awardlinks) == 2
    assert len(swim_idea._awardheirs) == 3

    # WHEN
    x_bud.settle_bud()

    # THEN
    assert len(swim_idea._awardlinks) == 2
    assert len(swim_idea._awardheirs) == 2


def test_BudUnit_get_idea_tree_ordered_road_list_ReturnsCorrectObj():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels()
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
    yao_bud = budunit_shop("Yao")

    # WHEN
    time = "timeline"
    yao_bud.add_l1_idea(ideaunit_shop(_label=time, _begin=0, _close=700))
    t_road = yao_bud.make_l1_road(time)
    week = "weeks"
    yao_bud.add_idea(ideaunit_shop(_label=week, _denom=7), parent_road=t_road)

    # THEN
    assert len(yao_bud.get_idea_tree_ordered_road_list()) == 3
    assert len(yao_bud.get_idea_tree_ordered_road_list(no_range_descendants=True)) == 2


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


def test_BudUnit_settle_bud_CreatesFullyPopulated_idea_dict():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._idea_dict) == 17


def test_BudUnit_settle_bud_Resets_offtrack_kids_weight_set():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    sue_budunit._offtrack_kids_weight_set = set("ZZ")
    x_set = set()

    assert sue_budunit._offtrack_kids_weight_set != x_set

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_weight_set == x_set


def test_BudUnit_settle_bud_WhenIdeaRootHas_weightButAll_kidsHaveZero_weightAddTo_offtrack_kids_weight_set_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    casa_idea = ideaunit_shop(casa_text, _weight=0)
    sue_budunit.add_l1_idea(casa_idea)
    assert sue_budunit._offtrack_kids_weight_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_weight_set == {sue_budunit._real_id}

    # WHEN
    sue_budunit.edit_idea_attr(casa_road, weight=2)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_weight_set == set()


def test_BudUnit_settle_bud_WhenIdeaUnitHas_weightButAll_kidsHaveZero_weightAddTo_offtrack_kids_weight_set():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    casa_idea = ideaunit_shop(casa_text, _weight=1)

    swim_text = "swimming"
    swim_road = sue_budunit.make_road(casa_road, swim_text)
    swim_idea = ideaunit_shop(swim_text, _weight=8)

    clean_text = "cleaning"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    clean_idea = ideaunit_shop(clean_text, _weight=2)
    sue_budunit.add_idea(ideaunit_shop(clean_text), casa_road)

    sweep_text = "sweep"
    sweep_road = sue_budunit.make_road(clean_road, sweep_text)
    sweep_idea = ideaunit_shop(sweep_text, _weight=0)
    vaccum_text = "vaccum"
    vaccum_road = sue_budunit.make_road(clean_road, vaccum_text)
    vaccum_idea = ideaunit_shop(vaccum_text, _weight=0)

    sue_budunit.add_l1_idea(casa_idea)
    sue_budunit.add_idea(swim_idea, casa_road)
    sue_budunit.add_idea(clean_idea, casa_road)
    sue_budunit.add_idea(sweep_idea, clean_road)  # _weight=0
    sue_budunit.add_idea(vaccum_idea, clean_road)  # _weight=0

    assert sue_budunit._offtrack_kids_weight_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_weight_set == {clean_road}


def test_BudUnit_settle_bud_CreatesNewLobbyBoxsWhenNeeded_Scenario0():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)
    zia_text = "Zia"
    yao_credor_weight = 3
    yao_debtor_weight = 2
    zia_credor_weight = 4
    zia_debtor_weight = 5
    yao_bud.add_acctunit(yao_text, yao_credor_weight, yao_debtor_weight)
    yao_bud.add_acctunit(zia_text, zia_credor_weight, zia_debtor_weight)
    x_idearoot = yao_bud.get_idea_obj(yao_bud._real_id)
    x_idearoot.set_awardlink(awardlink_shop(yao_text))
    x_idearoot.set_awardlink(awardlink_shop(zia_text))
    xio_text = "Xio"
    x_idearoot.set_awardlink(awardlink_shop(xio_text))
    assert len(yao_bud.get_acctunit_lobby_ids_dict()) == 2
    assert not yao_bud.lobbybox_exists(yao_text)
    assert not yao_bud.lobbybox_exists(zia_text)
    assert not yao_bud.lobbybox_exists(xio_text)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.lobbybox_exists(yao_text)
    assert yao_bud.lobbybox_exists(zia_text)
    assert yao_bud.lobbybox_exists(xio_text)
    assert len(yao_bud.get_acctunit_lobby_ids_dict()) == 2
    assert len(yao_bud.get_acctunit_lobby_ids_dict()) != len(yao_bud._lobbyboxs)
    assert len(yao_bud._lobbyboxs) == 3
    xio_lobbybox = yao_bud.get_lobbybox(xio_text)
    xio_symmerty_lobbybox = yao_bud.create_symmetry_lobbybox(xio_text)
    assert xio_lobbybox._lobbyships.keys() == xio_symmerty_lobbybox._lobbyships.keys()
    assert xio_lobbybox.lobbyship_exists(yao_text)
    assert xio_lobbybox.lobbyship_exists(zia_text)
    assert not xio_lobbybox.lobbyship_exists(xio_text)
    yao_lobbyship = xio_lobbybox.get_lobbyship(yao_text)
    zia_lobbyship = xio_lobbybox.get_lobbyship(zia_text)
    assert yao_lobbyship.credor_weight == yao_credor_weight
    assert zia_lobbyship.credor_weight == zia_credor_weight
    assert yao_lobbyship.debtor_weight == yao_debtor_weight
    assert zia_lobbyship.debtor_weight == zia_debtor_weight


def test_BudUnit_settle_bud_CreatesNewLobbyBoxsWhenNeeded_Scenario1():
    # ESTABLISH
    yao_text = "yao"
    yao_bud = budunit_shop(yao_text)
    swim_text = "swim"
    swim_road = yao_bud.make_l1_road(swim_text)
    yao_bud.add_l1_idea(ideaunit_shop(swim_text))
    zia_text = "Zia"
    yao_bud.add_acctunit(yao_text)
    yao_bud.add_acctunit(zia_text)
    swim_idea = yao_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(awardlink_shop(yao_text))
    swim_idea.set_awardlink(awardlink_shop(zia_text))
    xio_text = "Xio"
    swim_idea.set_awardlink(awardlink_shop(xio_text))
    assert len(yao_bud.get_acctunit_lobby_ids_dict()) == 2
    assert not yao_bud.lobbybox_exists(yao_text)
    assert not yao_bud.lobbybox_exists(zia_text)
    assert not yao_bud.lobbybox_exists(xio_text)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.lobbybox_exists(yao_text)
    assert yao_bud.lobbybox_exists(zia_text)
    assert yao_bud.lobbybox_exists(xio_text)
    assert len(yao_bud.get_acctunit_lobby_ids_dict()) == 2
    assert len(yao_bud.get_acctunit_lobby_ids_dict()) != len(yao_bud._lobbyboxs)
    assert len(yao_bud._lobbyboxs) == 3
    xio_lobbybox = yao_bud.get_lobbybox(xio_text)
    xio_symmerty_lobbybox = yao_bud.create_symmetry_lobbybox(xio_text)
    assert xio_lobbybox._lobbyships.keys() == xio_symmerty_lobbybox._lobbyships.keys()
    assert xio_lobbybox.lobbyship_exists(yao_text)
    assert xio_lobbybox.lobbyship_exists(zia_text)
    assert not xio_lobbybox.lobbyship_exists(xio_text)


def test_BudUnit_get_tree_traverse_generated_lobbyboxs_ReturnsObj():
    # ESTABLISH
    yao_text = "yao"
    yao_bud = budunit_shop(yao_text)
    swim_text = "swim"
    swim_road = yao_bud.make_l1_road(swim_text)
    yao_bud.add_l1_idea(ideaunit_shop(swim_text))
    zia_text = "Zia"
    yao_bud.add_acctunit(yao_text)
    yao_bud.add_acctunit(zia_text)
    swim_idea = yao_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(awardlink_shop(yao_text))
    swim_idea.set_awardlink(awardlink_shop(zia_text))
    xio_text = "Xio"
    swim_idea.set_awardlink(awardlink_shop(xio_text))
    yao_bud.settle_bud()
    assert yao_bud.lobbybox_exists(yao_text)
    assert yao_bud.lobbybox_exists(zia_text)
    assert yao_bud.lobbybox_exists(xio_text)
    assert len(yao_bud.get_acctunit_lobby_ids_dict()) == 2
    assert len(yao_bud.get_acctunit_lobby_ids_dict()) != len(yao_bud._lobbyboxs)

    # WHEN
    symmerty_lobby_ids = yao_bud.get_tree_traverse_generated_lobbyboxs()

    # THEN
    assert len(symmerty_lobby_ids) == 1
    assert symmerty_lobby_ids == {xio_text}

    # ESTABLISH
    run_text = ",Run"
    swim_idea.set_awardlink(awardlink_shop(run_text))
    assert not yao_bud.lobbybox_exists(run_text)
    yao_bud.settle_bud()
    assert yao_bud.lobbybox_exists(run_text)

    # WHEN
    symmerty_lobby_ids = yao_bud.get_tree_traverse_generated_lobbyboxs()

    # THEN
    assert len(symmerty_lobby_ids) == 2
    assert symmerty_lobby_ids == {xio_text, run_text}
