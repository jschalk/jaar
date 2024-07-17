from src._world.reason_idea import (
    FactUnit,
    factunit_shop,
    factheir_shop,
    FactCore,
    factunit_shop as c_factunit,
    factunits_get_from_dict,
)
from src._road.road import get_default_real_id_roadnode as root_label, create_road
from pytest import raises as pytest_raises


def test_FactUnit_exists():
    # ESTABLISH
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)

    # WHEN
    sunday_fact = FactUnit(base=weekday_road, pick=sunday_road, open=1.9, nigh=2.3)

    # THEN
    print(sunday_fact)
    assert sunday_fact != None
    assert sunday_fact.base == weekday_road
    assert sunday_fact.pick == sunday_road
    assert sunday_fact.open == 1.9
    assert sunday_fact.nigh == 2.3


def test_FactUnit_set_range_null_SetsAttrCorrectly_1():
    # ESTABLISH
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    weekday_fact = factunit_shop(weekday_road, weekday_road, open=1.0, nigh=5.0)
    assert weekday_fact.open == 1.0
    assert weekday_fact.nigh == 5.0

    # WHEN
    weekday_fact.set_range_null()

    # THEN
    assert weekday_fact.open is None
    assert weekday_fact.nigh is None


def test_FactUnit_set_pick_to_base_SetsAttr_1():
    # ESTABLISH
    floor_text = "floor"
    floor_road = create_road(root_label(), floor_text)
    dirty_text = "dirty"
    dirty_road = create_road(root_label(), dirty_text)
    floor_fact = factunit_shop(floor_road, dirty_road)
    assert floor_fact.base == floor_road
    assert floor_fact.pick == dirty_road

    # WHEN
    floor_fact.set_pick_to_base()

    # THEN
    assert floor_fact.base == floor_road
    assert floor_fact.pick == floor_road


def test_FactUnit_set_pick_to_base_SetsAttr_2():
    # ESTABLISH
    floor_text = "floor"
    floor_road = create_road(root_label(), floor_text)
    dirty_text = "dirty"
    dirty_road = create_road(root_label(), dirty_text)
    floor_fact = factunit_shop(floor_road, dirty_road, 1, 6)
    assert floor_fact.open != None
    assert floor_fact.nigh != None

    # WHEN
    floor_fact.set_pick_to_base()

    # THEN
    assert floor_fact.open is None
    assert floor_fact.nigh is None


def test_FactUnit_set_attr_SetsAttrCorrectly_2():
    # ESTABLISH
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    weekday_fact = factunit_shop(weekday_road, weekday_road, open=1.0, nigh=5.0)

    # WHEN
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    weekday_fact.set_attr(pick=sunday_road)
    # THEN
    assert weekday_fact.pick == sunday_road

    # WHEN
    weekday_fact.set_attr(open=45)
    # THEN
    assert weekday_fact.open == 45

    # WHEN
    weekday_fact.set_attr(nigh=65)
    # THEN
    assert weekday_fact.nigh == 65


def test_FactUnit_get_dict_ReturnsDict():
    # ESTABLISH
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    x_open = 35
    x_nigh = 50
    sunday_fact = factunit_shop(
        base=weekday_road, pick=sunday_road, open=x_open, nigh=x_nigh
    )
    print(sunday_fact)

    # WHEN
    fact_dict = sunday_fact.get_dict()

    # THEN
    assert fact_dict != None
    static_dict = {
        "base": weekday_road,
        "pick": sunday_road,
        "open": x_open,
        "nigh": x_nigh,
    }
    assert fact_dict == static_dict


def test_FactUnit_get_dict_ReturnsPartialDict():
    # ESTABLISH
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    sunday_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_fact)

    # WHEN
    fact_dict = sunday_fact.get_dict()

    # THEN
    assert fact_dict != None
    static_dict = {
        "base": weekday_road,
        "pick": sunday_road,
    }
    assert fact_dict == static_dict


def test_FactUnit_find_replace_road_SetsAttrCorrectly():
    # ESTABLISH
    weekday_text = "weekday"
    old_weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    old_sunday_road = create_road(old_weekday_road, sunday_text)
    sunday_fact = factunit_shop(base=old_weekday_road, pick=old_sunday_road)
    print(sunday_fact)
    assert sunday_fact.base == old_weekday_road
    assert sunday_fact.pick == old_sunday_road

    # WHEN
    old_road = root_label()
    new_road = "fun"
    sunday_fact.find_replace_road(old_road=old_road, new_road=new_road)
    new_weekday_road = create_road(new_road, weekday_text)
    new_sunday_road = create_road(new_weekday_road, sunday_text)

    # THEN
    assert sunday_fact.base == new_weekday_road
    assert sunday_fact.pick == new_sunday_road


def test_FactHeir_IsModifiedByFactUnit():
    # ESTABLISH
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)
    ced_factheir = factheir_shop(min_road, min_road, 10.0, 30.0)
    ced_factunit = factunit_shop(min_road, min_road, 20.0, 30.0)
    assert ced_factheir.open == 10

    # WHEN
    ced_factheir.transform(factunit=ced_factunit)

    # THEN
    assert ced_factheir.open == 20

    # ESTABLISH
    ced_factheir = factheir_shop(min_road, min_road, 10.0, 30.0)
    ced_factunit = factunit_shop(min_road, min_road, 30.0, 30.0)
    assert ced_factheir.open == 10

    # WHEN
    ced_factheir.transform(factunit=ced_factunit)
    assert ced_factheir.open == 30

    # ESTABLISH
    ced_factheir = factheir_shop(min_road, min_road, 10.0, 30.0)
    ced_factunit = factunit_shop(min_road, min_road, 35.0, 57.0)
    assert ced_factheir.open == 10

    # WHEN
    ced_factheir.transform(factunit=ced_factunit)

    # THEN
    assert ced_factheir.open == 10

    # ESTABLISH
    ced_factheir = factheir_shop(min_road, min_road, 10.0, 30.0)
    ced_factunit = factunit_shop(min_road, min_road, 5.0, 7.0)
    assert ced_factheir.open == 10

    # WHEN
    ced_factheir.transform(factunit=ced_factunit)

    # THEN
    assert ced_factheir.open == 10


def test_FactHeir_is_range_ReturnsRangeStatus():
    # ESTABLISH
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)

    # WHEN
    x_factheir = factheir_shop(base=min_road, pick=min_road)
    assert x_factheir.is_range() is False

    # THEN
    x_factheir = factheir_shop(min_road, pick=min_road, open=10.0, nigh=30.0)
    assert x_factheir.is_range() == True


def test_factheir_is_range_ReturnsRangeStatus():
    # ESTABLISH
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)

    # WHEN
    x_factheir = factheir_shop(base=min_road, pick=min_road)

    # THEN
    assert x_factheir.is_range() is False

    # WHEN
    x_factheir = factheir_shop(min_road, pick=min_road, open=10.0, nigh=30.0)

    # THEN
    assert x_factheir.is_range() == True


def test_FactCore_get_obj_key_SetsAttrCorrectly():
    # ESTABLISH
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)
    secs_text = "secs"
    secs_road = create_road(min_road, secs_text)

    # WHEN
    x_factcore = FactCore(base=min_road, pick=secs_road)

    # THEN
    assert x_factcore.get_obj_key() == min_road


def test_factunits_get_from_dict_CorrectlyBuildsObj():
    # ESTABLISH
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    static_dict = {
        weekday_road: {
            "base": weekday_road,
            "pick": sunday_road,
            "open": None,
            "nigh": None,
        }
    }

    # WHEN
    facts_dict = factunits_get_from_dict(static_dict)

    # THEN
    assert len(facts_dict) == 1
    weekday_fact = facts_dict.get(weekday_road)
    assert weekday_fact == factunit_shop(base=weekday_road, pick=sunday_road)


def test_factunits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # ESTABLISH
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    static_dict = {
        weekday_road: {
            "base": weekday_road,
            "pick": sunday_road,
        }
    }

    # WHEN
    facts_dict = factunits_get_from_dict(static_dict)

    # THEN
    weekday_fact = facts_dict.get(weekday_road)
    assert weekday_fact == factunit_shop(base=weekday_road, pick=sunday_road)
