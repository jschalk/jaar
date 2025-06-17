from src.a01_term_logic.rope import to_rope
from src.a04_reason_logic.reason_concept import reasonunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic._util.example_plans import get_planunit_with_4_levels
from src.a06_plan_logic.plan import get_sorted_concept_list, planunit_shop
from src.a06_plan_logic.tree_metrics import TreeMetrics, treemetrics_shop


def test_TreeMetrics_Exists():
    # ESTABLISH / WHEN
    x_tree_metrics = TreeMetrics()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.label_count is None
    assert x_tree_metrics.level_count is None
    assert x_tree_metrics.reason_rcontexts is None
    assert x_tree_metrics.awardlinks_metrics is None
    assert x_tree_metrics.uid_max is None
    assert x_tree_metrics.uid_dict is None
    assert x_tree_metrics.all_concept_uids_are_unique is None


def test_treemetrics_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_tree_metrics = treemetrics_shop()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.label_count == 0
    assert x_tree_metrics.level_count == {}
    assert x_tree_metrics.reason_rcontexts == {}
    assert x_tree_metrics.awardlinks_metrics == {}
    assert x_tree_metrics.uid_max == 0
    assert x_tree_metrics.uid_dict == {}
    assert x_tree_metrics.all_concept_uids_are_unique

    # # could create tests for these methods?
    # def evaluate_label(
    # def evaluate_task(self, task: bool, concept_rope: RopeTerm):
    # def evaluate_level(self, level):
    # def evaluate_reasonunits(self, reasons: dict[RopeTerm, ReasonUnit]):
    # def evaluate_awardlinks(self, awardlinks: dict[GroupTitle, AwardLink]):
    # def evaluate_uid_max(self, uid):


def test_PlanUnit_set_concept_dict_Scenario0():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    root_rope = to_rope(yao_plan.vow_label)
    root_concept = yao_plan.get_concept_obj(root_rope)
    assert not root_concept.begin
    assert not root_concept.close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert yao_plan._concept_dict == {}
    assert yao_plan._reason_rcontexts == set()

    # WHEN
    yao_plan._set_concept_dict()

    # THEN
    assert not root_concept.begin
    assert not root_concept.close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert yao_plan._concept_dict == {root_concept.get_concept_rope(): root_concept}
    assert yao_plan._reason_rcontexts == set()


def test_PlanUnit_set_concept_dict_Scenario1():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    time0_begin = 7
    time0_close = 31
    root_rope = to_rope(yao_plan.vow_label)
    yao_plan.edit_concept_attr(root_rope, begin=time0_begin, close=time0_close)
    root_rope = to_rope(yao_plan.vow_label)
    root_concept = yao_plan.get_concept_obj(root_rope)
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc

    # WHEN
    yao_plan._set_concept_dict()

    # THEN
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc


def test_PlanUnit_set_concept_dict_Clears_gogo_calc_stop_calc():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    root_rope = to_rope(sue_plan.vow_label)
    root_concept = sue_plan.get_concept_obj(root_rope)
    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_plan.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = sue_plan.make_rope(usa_rope, texas_str)
    texas_concept = sue_plan.get_concept_obj(texas_rope)
    texas_concept._gogo_calc = 7
    texas_concept._stop_calc = 11
    texas_concept._range_evaluated = True
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert texas_concept._range_evaluated
    assert texas_concept._gogo_calc
    assert texas_concept._stop_calc

    # WHEN
    sue_plan._set_concept_dict()

    # THEN
    assert not root_concept.begin
    assert not root_concept.close
    assert not texas_concept._range_evaluated
    assert not texas_concept._gogo_calc
    assert not texas_concept._stop_calc


def test_PlanUnit_set_concept_dict_Sets_reason_rcontexts():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    polis_str = "polis"
    polis_rope = sue_plan.make_l1_rope(polis_str)
    sue_plan.add_concept(polis_rope)
    sue_plan.add_concept(nation_rope)
    sue_plan.edit_concept_attr(
        nation_rope, reason_rcontext=polis_rope, reason_premise=polis_rope
    )
    nation_concept = sue_plan.get_concept_obj(nation_rope)
    assert nation_concept.rcontext_reasonunit_exists(polis_rope)
    assert sue_plan._reason_rcontexts == set()

    # WHEN
    sue_plan._set_concept_dict()

    # THEN
    assert sue_plan._reason_rcontexts == {polis_rope}


def test_PlanUnit_set_concept_CreatesConceptUnitsUsedBy_reasonunits():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope("casa")
    cleaning_rope = sue_plan.make_rope(casa_rope, "cleaning")
    clean_cookery_str = "clean_cookery"
    clean_cookery_concept = conceptunit_shop(clean_cookery_str, mass=40, task=True)

    buildings_str = "buildings"
    buildings_rope = sue_plan.make_l1_rope(buildings_str)
    cookery_room_str = "cookery"
    cookery_room_rope = sue_plan.make_rope(buildings_rope, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_rope = sue_plan.make_rope(cookery_room_rope, cookery_dirty_str)
    cookery_reasonunit = reasonunit_shop(rcontext=cookery_room_rope)
    cookery_reasonunit.set_premise(premise=cookery_dirty_rope)
    clean_cookery_concept.set_reasonunit(cookery_reasonunit)

    assert sue_plan.concept_exists(buildings_rope) is False

    # WHEN
    sue_plan.set_concept(
        clean_cookery_concept, cleaning_rope, create_missing_concepts=True
    )

    # THEN
    assert sue_plan.concept_exists(buildings_rope)


def test_get_sorted_concept_list_ReturnsObj():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope("casa")
    cat_rope = sue_plan.make_l1_rope("cat have dinner")
    wk_rope = sue_plan.make_l1_rope("wkdays")
    sun_rope = sue_plan.make_rope(wk_rope, "Sunday")
    mon_rope = sue_plan.make_rope(wk_rope, "Monday")
    tue_rope = sue_plan.make_rope(wk_rope, "Tuesday")
    wed_rope = sue_plan.make_rope(wk_rope, "Wednesday")
    thu_rope = sue_plan.make_rope(wk_rope, "Thursday")
    fri_rope = sue_plan.make_rope(wk_rope, "Friday")
    sat_rope = sue_plan.make_rope(wk_rope, "Saturday")
    nation_rope = sue_plan.make_l1_rope("nation")
    usa_rope = sue_plan.make_rope(nation_rope, "USA")
    france_rope = sue_plan.make_rope(nation_rope, "France")
    brazil_rope = sue_plan.make_rope(nation_rope, "Brazil")
    texas_rope = sue_plan.make_rope(usa_rope, "Texas")
    oregon_rope = sue_plan.make_rope(usa_rope, "Oregon")
    sue_plan._set_concept_dict()

    # WHEN
    x_sorted_concept_list = get_sorted_concept_list(
        list(sue_plan._concept_dict.values())
    )

    # THEN
    assert x_sorted_concept_list is not None
    assert len(x_sorted_concept_list) == 17
    assert x_sorted_concept_list[0] == sue_plan.conceptroot
    assert x_sorted_concept_list[1] == sue_plan.get_concept_obj(casa_rope)
    assert x_sorted_concept_list[11] == sue_plan.get_concept_obj(mon_rope)
