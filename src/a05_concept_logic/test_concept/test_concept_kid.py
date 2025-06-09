from pytest import raises as pytest_raises
from src.a01_term_logic.way import create_way
from src.a05_concept_logic.concept import (
    conceptunit_shop,
    get_default_vow_label as root_label,
)


def test_get_kids_in_range_GetsCorrectConcepts():
    # ESTABLISH
    mon_str = "months"
    mon_concept = conceptunit_shop(mon_str, begin=0, close=366)
    jan_str = "Jan"
    feb_str = "Feb"
    mar_str = "Mar"
    mon_concept.add_kid(conceptunit_shop(jan_str))
    mon_concept.add_kid(conceptunit_shop(feb_str))
    mon_concept.add_kid(conceptunit_shop(mar_str))
    jan_concept = mon_concept._kids.get(jan_str)
    feb_concept = mon_concept._kids.get(feb_str)
    mar_concept = mon_concept._kids.get(mar_str)
    jan_concept._gogo_calc = 0
    jan_concept._stop_calc = 31
    feb_concept._gogo_calc = 31
    feb_concept._stop_calc = 60
    mar_concept._gogo_calc = 60
    mar_concept._stop_calc = 91

    # WHEN / THEN
    assert len(mon_concept.get_kids_in_range(x_gogo=100, x_stop=120)) == 0
    assert len(mon_concept.get_kids_in_range(x_gogo=0, x_stop=31)) == 1
    assert len(mon_concept.get_kids_in_range(x_gogo=5, x_stop=5)) == 1
    assert len(mon_concept.get_kids_in_range(x_gogo=0, x_stop=61)) == 3
    assert len(mon_concept.get_kids_in_range(x_gogo=31, x_stop=31)) == 1
    assert set(mon_concept.get_kids_in_range(x_gogo=31, x_stop=31).keys()) == {feb_str}
    assert list(mon_concept.get_kids_in_range(x_gogo=31, x_stop=31).values()) == [
        feb_concept
    ]


def test_get_kids_in_range_EmptyParametersReturnsAll_kids():
    # ESTABLISH
    mon_str = "366months"
    mon_concept = conceptunit_shop(mon_str)
    jan_str = "Jan"
    feb29_str = "Feb29"
    mar_str = "Mar"
    mon_concept.add_kid(conceptunit_shop(jan_str))
    mon_concept.add_kid(conceptunit_shop(feb29_str))
    mon_concept.add_kid(conceptunit_shop(mar_str))

    # WHEN / THEN
    assert len(mon_concept.get_kids_in_range()) == 3


def test_ConceptUnit_get_descendants_ReturnsNoWayTerms():
    # ESTABLISH
    nation_str = "nation"
    nation_concept = conceptunit_shop(nation_str, parent_way=root_label())

    # WHEN
    nation_descendants = nation_concept.get_descendant_ways_from_kids()

    # THEN
    assert nation_descendants == {}


def test_ConceptUnit_get_descendants_Returns3DescendantsWayTerms():
    # ESTABLISH
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    nation_concept = conceptunit_shop(nation_str, parent_way=root_label())

    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    usa_concept = conceptunit_shop(usa_str, parent_way=nation_way)
    nation_concept.add_kid(usa_concept)

    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    texas_concept = conceptunit_shop(texas_str, parent_way=usa_way)
    usa_concept.add_kid(texas_concept)

    iowa_str = "Iowa"
    iowa_way = create_way(usa_way, iowa_str)
    iowa_concept = conceptunit_shop(iowa_str, parent_way=usa_way)
    usa_concept.add_kid(iowa_concept)

    # WHEN
    nation_descendants = nation_concept.get_descendant_ways_from_kids()

    # THEN
    assert len(nation_descendants) == 3
    assert nation_descendants.get(usa_way) is not None
    assert nation_descendants.get(texas_way) is not None
    assert nation_descendants.get(iowa_way) is not None


def test_ConceptUnit_get_descendants_ErrorRaisedIfInfiniteLoop():
    # ESTABLISH
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    nation_concept = conceptunit_shop(nation_str, parent_way=root_label())
    nation_concept.add_kid(nation_concept)
    max_count = 1000

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        nation_concept.get_descendant_ways_from_kids()
    assert (
        str(excinfo.value)
        == f"Concept '{nation_concept.get_concept_way()}' either has an infinite loop or more than {max_count} descendants."
    )


def test_ConceptUnit_clear_kids_CorrectlySetsAttr():
    # ESTABLISH
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    nation_concept = conceptunit_shop(nation_str, parent_way=root_label())
    nation_concept.add_kid(conceptunit_shop("USA", parent_way=nation_way))
    nation_concept.add_kid(conceptunit_shop("France", parent_way=nation_way))
    assert len(nation_concept._kids) == 2

    # WHEN
    nation_concept.clear_kids()

    # THEN
    assert len(nation_concept._kids) == 0


def test_ConceptUnit_get_kid_ReturnsObj():
    # ESTABLISH
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    nation_concept = conceptunit_shop(nation_str, parent_way=root_label())

    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    nation_concept.add_kid(conceptunit_shop(usa_str, parent_way=nation_way))

    france_str = "France"
    france_way = create_way(nation_way, france_str)
    nation_concept.add_kid(conceptunit_shop(france_str, parent_way=nation_way))
    assert len(nation_concept._kids) == 2

    # WHEN
    france_concept = nation_concept.get_kid(france_str)

    # THEN
    assert france_concept.concept_label == france_str


def test_ConceptUnit_del_kid_CorrectModifiesAttr():
    # ESTABLISH
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    nation_concept = conceptunit_shop(nation_str, parent_way=root_label())

    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    nation_concept.add_kid(conceptunit_shop(usa_str, parent_way=nation_way))

    france_str = "France"
    france_way = create_way(nation_way, france_str)
    nation_concept.add_kid(conceptunit_shop(france_str, parent_way=nation_way))
    assert len(nation_concept._kids) == 2

    # WHEN
    nation_concept.del_kid(france_str)

    # THEN
    assert len(nation_concept._kids) == 1


def test_ConceptUnit_get_kids_mass_sum_ReturnsObj_Scenario0():
    # ESTABLISH
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    nation_concept = conceptunit_shop(nation_str, parent_way=root_label())
    usa_str = "USA"
    usa_concept = conceptunit_shop(usa_str, parent_way=nation_way)
    nation_concept.add_kid(usa_concept)
    france_str = "France"
    france_concept = conceptunit_shop(france_str, parent_way=nation_way)
    nation_concept.add_kid(france_concept)

    # WHEN / THEN
    assert nation_concept.get_kids_mass_sum() == 2


def test_ConceptUnit_get_kids_mass_sum_ReturnsObj_Scenario1():
    # ESTABLISH
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    nation_concept = conceptunit_shop(nation_str, parent_way=root_label())
    usa_str = "USA"
    usa_concept = conceptunit_shop(usa_str, mass=0, parent_way=nation_way)
    nation_concept.add_kid(usa_concept)
    france_str = "France"
    france_concept = conceptunit_shop(france_str, mass=0, parent_way=nation_way)
    nation_concept.add_kid(france_concept)

    # WHEN / THEN
    assert nation_concept.get_kids_mass_sum() == 0

    # WHEN
    france_str = "France"
    france_concept = conceptunit_shop(france_str, mass=3, parent_way=nation_way)
    nation_concept.add_kid(france_concept)

    # WHEN / THEN
    assert nation_concept.get_kids_mass_sum() == 3
