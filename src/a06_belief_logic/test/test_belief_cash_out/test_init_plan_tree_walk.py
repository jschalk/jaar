from src.a01_term_logic.rope import to_rope
from src.a04_reason_logic.reason import reasonunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop, get_sorted_plan_list
from src.a06_belief_logic.test._util.example_beliefs import get_beliefunit_with_4_levels
from src.a06_belief_logic.tree_metrics import TreeMetrics, treemetrics_shop


def test_TreeMetrics_Exists():
    # ESTABLISH / WHEN
    x_tree_metrics = TreeMetrics()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.label_count is None
    assert x_tree_metrics.level_count is None
    assert x_tree_metrics.reason_contexts is None
    assert x_tree_metrics.awardunits_metrics is None
    assert x_tree_metrics.uid_max is None
    assert x_tree_metrics.uid_dict is None
    assert x_tree_metrics.all_plan_uids_are_unique is None


def test_treemetrics_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_tree_metrics = treemetrics_shop()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.label_count == 0
    assert x_tree_metrics.level_count == {}
    assert x_tree_metrics.reason_contexts == {}
    assert x_tree_metrics.awardunits_metrics == {}
    assert x_tree_metrics.uid_max == 0
    assert x_tree_metrics.uid_dict == {}
    assert x_tree_metrics.all_plan_uids_are_unique

    # # could create tests for these methods?
    # def evaluate_label(
    # def evaluate_task(self, task: bool, plan_rope: RopeTerm):
    # def evaluate_level(self, level):
    # def evaluate_reasonunits(self, reasons: dict[RopeTerm, ReasonUnit]):
    # def evaluate_awardunits(self, awardunits: dict[GroupTitle, AwardUnit]):
    # def evaluate_uid_max(self, uid):


def test_BeliefUnit_set_plan_dict_Scenario0():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    root_rope = to_rope(yao_belief.moment_label)
    root_plan = yao_belief.get_plan_obj(root_rope)
    assert not root_plan.begin
    assert not root_plan.close
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert yao_belief._plan_dict == {}
    assert yao_belief._reason_contexts == set()

    # WHEN
    yao_belief._set_plan_dict()

    # THEN
    assert not root_plan.begin
    assert not root_plan.close
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert yao_belief._plan_dict == {root_plan.get_plan_rope(): root_plan}
    assert yao_belief._reason_contexts == set()


def test_BeliefUnit_set_plan_dict_Scenario1():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    ziet0_begin = 7
    ziet0_close = 31
    root_rope = to_rope(yao_belief.moment_label)
    yao_belief.edit_plan_attr(root_rope, begin=ziet0_begin, close=ziet0_close)
    root_rope = to_rope(yao_belief.moment_label)
    root_plan = yao_belief.get_plan_obj(root_rope)
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc

    # WHEN
    yao_belief._set_plan_dict()

    # THEN
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc


def test_BeliefUnit_set_plan_dict_Clears_gogo_calc_stop_calc():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    root_rope = to_rope(sue_belief.moment_label)
    root_plan = sue_belief.get_plan_obj(root_rope)
    nation_str = "nation"
    nation_rope = sue_belief.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_belief.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = sue_belief.make_rope(usa_rope, texas_str)
    texas_plan = sue_belief.get_plan_obj(texas_rope)
    texas_plan._gogo_calc = 7
    texas_plan._stop_calc = 11
    texas_plan._range_evaluated = True
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert texas_plan._range_evaluated
    assert texas_plan._gogo_calc
    assert texas_plan._stop_calc

    # WHEN
    sue_belief._set_plan_dict()

    # THEN
    assert not root_plan.begin
    assert not root_plan.close
    assert not texas_plan._range_evaluated
    assert not texas_plan._gogo_calc
    assert not texas_plan._stop_calc


def test_BeliefUnit_set_plan_dict_Sets_reason_contexts():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    nation_str = "nation"
    nation_rope = sue_belief.make_l1_rope(nation_str)
    polis_str = "polis"
    polis_rope = sue_belief.make_l1_rope(polis_str)
    sue_belief.add_plan(polis_rope)
    sue_belief.add_plan(nation_rope)
    sue_belief.edit_plan_attr(
        nation_rope, reason_context=polis_rope, reason_case=polis_rope
    )
    nation_plan = sue_belief.get_plan_obj(nation_rope)
    assert nation_plan.reason_context_reasonunit_exists(polis_rope)
    assert sue_belief._reason_contexts == set()

    # WHEN
    sue_belief._set_plan_dict()

    # THEN
    assert sue_belief._reason_contexts == {polis_rope}


def test_BeliefUnit_set_plan_CreatesPlanUnitsUsedBy_reasonunits():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_rope = sue_belief.make_l1_rope("casa")
    cleaning_rope = sue_belief.make_rope(casa_rope, "cleaning")
    clean_cookery_str = "clean_cookery"
    clean_cookery_plan = planunit_shop(clean_cookery_str, star=40, task=True)

    buildings_str = "buildings"
    buildings_rope = sue_belief.make_l1_rope(buildings_str)
    cookery_room_str = "cookery"
    cookery_room_rope = sue_belief.make_rope(buildings_rope, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_rope = sue_belief.make_rope(cookery_room_rope, cookery_dirty_str)
    cookery_reasonunit = reasonunit_shop(reason_context=cookery_room_rope)
    cookery_reasonunit.set_case(case=cookery_dirty_rope)
    clean_cookery_plan.set_reasonunit(cookery_reasonunit)

    assert sue_belief.plan_exists(buildings_rope) is False

    # WHEN
    sue_belief.set_plan(clean_cookery_plan, cleaning_rope, create_missing_plans=True)

    # THEN
    assert sue_belief.plan_exists(buildings_rope)


def test_get_sorted_plan_list_ReturnsObj():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_rope = sue_belief.make_l1_rope("casa")
    cat_rope = sue_belief.make_l1_rope("cat have dinner")
    wk_rope = sue_belief.make_l1_rope("sem_jours")
    sun_rope = sue_belief.make_rope(wk_rope, "Sun")
    mon_rope = sue_belief.make_rope(wk_rope, "Mon")
    tue_rope = sue_belief.make_rope(wk_rope, "Tue")
    wed_rope = sue_belief.make_rope(wk_rope, "Wed")
    thu_rope = sue_belief.make_rope(wk_rope, "Thur")
    fri_rope = sue_belief.make_rope(wk_rope, "Fri")
    sat_rope = sue_belief.make_rope(wk_rope, "Sat")
    nation_rope = sue_belief.make_l1_rope("nation")
    usa_rope = sue_belief.make_rope(nation_rope, "USA")
    france_rope = sue_belief.make_rope(nation_rope, "France")
    brazil_rope = sue_belief.make_rope(nation_rope, "Brazil")
    texas_rope = sue_belief.make_rope(usa_rope, "Texas")
    oregon_rope = sue_belief.make_rope(usa_rope, "Oregon")
    sue_belief._set_plan_dict()

    # WHEN
    x_sorted_plan_list = get_sorted_plan_list(list(sue_belief._plan_dict.values()))

    # THEN
    assert x_sorted_plan_list is not None
    assert len(x_sorted_plan_list) == 17
    assert x_sorted_plan_list[0] == sue_belief.planroot
    assert x_sorted_plan_list[1] == sue_belief.get_plan_obj(casa_rope)
    assert x_sorted_plan_list[11] == sue_belief.get_plan_obj(mon_rope)
