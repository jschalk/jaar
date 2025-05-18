from src.a01_way_logic.way import to_way
from src.a04_reason_logic.reason_concept import reasonunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop, get_sorted_concept_list
from src.a06_bud_logic._utils.example_buds import get_budunit_with_4_levels


def test_BudUnit_set_concept_dict_Scenario0():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    root_way = to_way(yao_bud.fisc_label)
    root_concept = yao_bud.get_concept_obj(root_way)
    assert not root_concept.begin
    assert not root_concept.close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert yao_bud._concept_dict == {}
    assert yao_bud._reason_rcontexts == set()

    # WHEN
    yao_bud._set_concept_dict()

    # THEN
    assert not root_concept.begin
    assert not root_concept.close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert yao_bud._concept_dict == {root_concept.get_concept_way(): root_concept}
    assert yao_bud._reason_rcontexts == set()


def test_BudUnit_set_concept_dict_Scenario1():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 7
    time0_close = 31
    root_way = to_way(yao_bud.fisc_label)
    yao_bud.edit_concept_attr(root_way, begin=time0_begin, close=time0_close)
    root_way = to_way(yao_bud.fisc_label)
    root_concept = yao_bud.get_concept_obj(root_way)
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc

    # WHEN
    yao_bud._set_concept_dict()

    # THEN
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc


def test_BudUnit_set_concept_dict_Clears_gogo_calc_stop_calc():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    root_way = to_way(sue_bud.fisc_label)
    root_concept = sue_bud.get_concept_obj(root_way)
    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    usa_str = "USA"
    usa_way = sue_bud.make_way(states_way, usa_str)
    texas_str = "Texas"
    texas_way = sue_bud.make_way(usa_way, texas_str)
    texas_concept = sue_bud.get_concept_obj(texas_way)
    texas_concept._gogo_calc = 7
    texas_concept._stop_calc = 11
    texas_concept._range_evaluated = True
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert texas_concept._range_evaluated
    assert texas_concept._gogo_calc
    assert texas_concept._stop_calc

    # WHEN
    sue_bud._set_concept_dict()

    # THEN
    assert not root_concept.begin
    assert not root_concept.close
    assert not texas_concept._range_evaluated
    assert not texas_concept._gogo_calc
    assert not texas_concept._stop_calc


def test_BudUnit_set_concept_dict_Sets_reason_rcontexts():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    polis_str = "polis"
    polis_way = sue_bud.make_l1_way(polis_str)
    sue_bud.add_concept(polis_way)
    sue_bud.add_concept(states_way)
    sue_bud.edit_concept_attr(
        states_way, reason_rcontext=polis_way, reason_premise=polis_way
    )
    states_concept = sue_bud.get_concept_obj(states_way)
    assert states_concept.rcontext_reasonunit_exists(polis_way)
    assert sue_bud._reason_rcontexts == set()

    # WHEN
    sue_bud._set_concept_dict()

    # THEN
    assert sue_bud._reason_rcontexts == {polis_way}


def test_BudUnit_set_concept_CreatesConceptUnitsUsedBy_reasonunits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    cleaning_way = sue_bud.make_way(casa_way, "cleaning")
    clean_cookery_str = "clean_cookery"
    clean_cookery_concept = conceptunit_shop(clean_cookery_str, mass=40, pledge=True)

    buildings_str = "buildings"
    buildings_way = sue_bud.make_l1_way(buildings_str)
    cookery_room_str = "cookery"
    cookery_room_way = sue_bud.make_way(buildings_way, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_way = sue_bud.make_way(cookery_room_way, cookery_dirty_str)
    cookery_reasonunit = reasonunit_shop(rcontext=cookery_room_way)
    cookery_reasonunit.set_premise(premise=cookery_dirty_way)
    clean_cookery_concept.set_reasonunit(cookery_reasonunit)

    assert sue_bud.concept_exists(buildings_way) is False

    # WHEN
    sue_bud.set_concept(
        clean_cookery_concept, cleaning_way, create_missing_concepts=True
    )

    # THEN
    assert sue_bud.concept_exists(buildings_way)


def test_get_sorted_concept_list_ReturnsObj():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    cat_way = sue_bud.make_l1_way("cat have dinner")
    week_way = sue_bud.make_l1_way("weekdays")
    sun_way = sue_bud.make_way(week_way, "Sunday")
    mon_way = sue_bud.make_way(week_way, "Monday")
    tue_way = sue_bud.make_way(week_way, "Tuesday")
    wed_way = sue_bud.make_way(week_way, "Wednesday")
    thu_way = sue_bud.make_way(week_way, "Thursday")
    fri_way = sue_bud.make_way(week_way, "Friday")
    sat_way = sue_bud.make_way(week_way, "Saturday")
    states_way = sue_bud.make_l1_way("nation-state")
    usa_way = sue_bud.make_way(states_way, "USA")
    france_way = sue_bud.make_way(states_way, "France")
    brazil_way = sue_bud.make_way(states_way, "Brazil")
    texas_way = sue_bud.make_way(usa_way, "Texas")
    oregon_way = sue_bud.make_way(usa_way, "Oregon")
    sue_bud._set_concept_dict()

    # WHEN
    x_sorted_concept_list = get_sorted_concept_list(
        list(sue_bud._concept_dict.values())
    )

    # THEN
    assert x_sorted_concept_list is not None
    assert len(x_sorted_concept_list) == 17
    assert x_sorted_concept_list[0] == sue_bud.conceptroot
    assert x_sorted_concept_list[1] == sue_bud.get_concept_obj(casa_way)
    assert x_sorted_concept_list[11] == sue_bud.get_concept_obj(mon_way)
