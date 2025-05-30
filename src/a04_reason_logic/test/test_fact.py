from src.a01_term_logic.way import (
    get_default_fisc_label as root_label,
    create_way,
    get_default_fisc_way,
)
from src.a04_reason_logic.reason_concept import (
    FactUnit,
    factunit_shop,
    factheir_shop,
    FactCore,
    factunits_get_from_dict,
    get_factunit_from_tuple,
)


def test_FactUnit_exists():
    # ESTABLISH / WHEN
    x_fact = FactUnit()

    # THEN
    assert not x_fact.fcontext
    assert not x_fact.fstate
    assert not x_fact.fopen
    assert not x_fact.fnigh


def test_FactUnit_exists():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)

    # WHEN
    sunday_fact = FactUnit(fcontext=wkday_way, fstate=sunday_way, fopen=1.9, fnigh=2.3)

    # THEN
    print(sunday_fact)
    assert sunday_fact is not None
    assert sunday_fact.fcontext == wkday_way
    assert sunday_fact.fstate == sunday_way
    assert sunday_fact.fopen == 1.9
    assert sunday_fact.fnigh == 2.3


def test_FactUnit_set_range_null_SetsAttrCorrectly_1():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_way = create_way(root_label(), wkday_str)
    wkday_fact = factunit_shop(wkday_way, wkday_way, fopen=1.0, fnigh=5.0)
    assert wkday_fact.fopen == 1.0
    assert wkday_fact.fnigh == 5.0

    # WHEN
    wkday_fact.set_range_null()

    # THEN
    assert wkday_fact.fopen is None
    assert wkday_fact.fnigh is None


def test_FactUnit_set_fstate_to_fcontext_SetsAttr_1():
    # ESTABLISH
    floor_str = "floor"
    floor_way = create_way(root_label(), floor_str)
    dirty_str = "dirty"
    dirty_way = create_way(root_label(), dirty_str)
    floor_fact = factunit_shop(floor_way, dirty_way)
    assert floor_fact.fcontext == floor_way
    assert floor_fact.fstate == dirty_way

    # WHEN
    floor_fact.set_fstate_to_fcontext()

    # THEN
    assert floor_fact.fcontext == floor_way
    assert floor_fact.fstate == floor_way


def test_FactUnit_set_fstate_to_fcontext_SetsAttr_2():
    # ESTABLISH
    floor_str = "floor"
    floor_way = create_way(root_label(), floor_str)
    dirty_str = "dirty"
    dirty_way = create_way(root_label(), dirty_str)
    floor_fact = factunit_shop(floor_way, dirty_way, 1, 6)
    assert floor_fact.fopen is not None
    assert floor_fact.fnigh is not None

    # WHEN
    floor_fact.set_fstate_to_fcontext()

    # THEN
    assert floor_fact.fopen is None
    assert floor_fact.fnigh is None


def test_FactUnit_set_attr_SetsAttrCorrectly_2():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_way = create_way(root_label(), wkday_str)
    wkday_fact = factunit_shop(wkday_way, wkday_way, fopen=1.0, fnigh=5.0)

    # WHEN
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)
    wkday_fact.set_attr(fstate=sunday_way)
    # THEN
    assert wkday_fact.fstate == sunday_way

    # WHEN
    wkday_fact.set_attr(fopen=45)
    # THEN
    assert wkday_fact.fopen == 45

    # WHEN
    wkday_fact.set_attr(fnigh=65)
    # THEN
    assert wkday_fact.fnigh == 65


def test_FactUnit_get_dict_ReturnsDict():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)
    x_fopen = 35
    x_fnigh = 50
    sunday_fact = factunit_shop(
        fcontext=wkday_way,
        fstate=sunday_way,
        fopen=x_fopen,
        fnigh=x_fnigh,
    )
    print(sunday_fact)

    # WHEN
    fact_dict = sunday_fact.get_dict()

    # THEN
    assert fact_dict is not None
    static_dict = {
        "fcontext": wkday_way,
        "fstate": sunday_way,
        "fopen": x_fopen,
        "fnigh": x_fnigh,
    }
    assert fact_dict == static_dict


def test_FactUnit_get_dict_ReturnsPartialDict():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)
    sunday_fact = factunit_shop(fcontext=wkday_way, fstate=sunday_way)
    print(sunday_fact)

    # WHEN
    fact_dict = sunday_fact.get_dict()

    # THEN
    assert fact_dict is not None
    static_dict = {
        "fcontext": wkday_way,
        "fstate": sunday_way,
    }
    assert fact_dict == static_dict


def test_FactUnit_find_replace_way_SetsAttrCorrectly():
    # ESTABLISH
    wkday_str = "wkday"
    old_wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    old_sunday_way = create_way(old_wkday_way, sunday_str)
    sunday_fact = factunit_shop(fcontext=old_wkday_way, fstate=old_sunday_way)
    print(sunday_fact)
    assert sunday_fact.fcontext == old_wkday_way
    assert sunday_fact.fstate == old_sunday_way

    # WHEN
    old_way = get_default_fisc_way()
    new_way = create_way("fun")
    sunday_fact.find_replace_way(old_way=old_way, new_way=new_way)

    # THEN
    new_wkday_way = create_way(new_way, wkday_str)
    new_sunday_way = create_way(new_wkday_way, sunday_str)
    assert sunday_fact.fcontext == new_wkday_way
    assert sunday_fact.fstate == new_sunday_way


def test_FactUnit_get_tuple_ReturnsObj_Scenario0_rcontext_fstate_only():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)
    sunday_fact = factunit_shop(fcontext=wkday_way, fstate=sunday_way)

    # WHEN
    sunday_tuple = sunday_fact.get_tuple()

    # THEN
    assert sunday_tuple
    assert sunday_tuple == (wkday_way, sunday_way, None, None)


def test_FactUnit_get_tuple_ReturnsObj_Scenario1_ValuesIn_fopen_fnigh():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)
    sun_fopen = 6
    sun_fnigh = 9
    sunday_fact = factunit_shop(wkday_way, sunday_way, sun_fopen, sun_fnigh)

    # WHEN
    sunday_tuple = sunday_fact.get_tuple()

    # THEN
    assert sunday_tuple
    assert sunday_tuple == (wkday_way, sunday_way, sun_fopen, sun_fnigh)


def test_get_factunit_from_tuple_ReturnsObj_Scenario0_rcontext_fstate_only():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)
    sunday_fact = factunit_shop(fcontext=wkday_way, fstate=sunday_way)
    sunday_tuple = sunday_fact.get_tuple()

    # WHEN
    gen_sunday_factunit = get_factunit_from_tuple(sunday_tuple)

    # THEN
    assert gen_sunday_factunit
    assert gen_sunday_factunit == sunday_fact


def test_get_factunit_from_tuple_ReturnsObj_Scenario1_ValuesIn_fopen_fnigh():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)
    sun_fopen = 6
    sun_fnigh = 9
    sunday_fact = factunit_shop(wkday_way, sunday_way, sun_fopen, sun_fnigh)
    sunday_tuple = sunday_fact.get_tuple()

    # WHEN
    gen_sunday_factunit = get_factunit_from_tuple(sunday_tuple)

    # THEN
    assert gen_sunday_factunit
    assert gen_sunday_factunit == sunday_fact


def test_FactHeir_IsModifiedByFactUnit():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_way = create_way(root_label(), ced_min_str)
    ced_factheir = factheir_shop(min_way, min_way, 10.0, 30.0)
    ced_factunit = factunit_shop(min_way, min_way, 20.0, 30.0)
    assert ced_factheir.fopen == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)

    # THEN
    assert ced_factheir.fopen == 20

    # ESTABLISH
    ced_factheir = factheir_shop(min_way, min_way, 10.0, 30.0)
    ced_factunit = factunit_shop(min_way, min_way, 30.0, 30.0)
    assert ced_factheir.fopen == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)
    assert ced_factheir.fopen == 30

    # ESTABLISH
    ced_factheir = factheir_shop(min_way, min_way, 10.0, 30.0)
    ced_factunit = factunit_shop(min_way, min_way, 35.0, 57.0)
    assert ced_factheir.fopen == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)

    # THEN
    assert ced_factheir.fopen == 10

    # ESTABLISH
    ced_factheir = factheir_shop(min_way, min_way, 10.0, 30.0)
    ced_factunit = factunit_shop(min_way, min_way, 5.0, 7.0)
    assert ced_factheir.fopen == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)

    # THEN
    assert ced_factheir.fopen == 10


def test_FactHeir_is_range_Returns_is_range_Status():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_way = create_way(root_label(), ced_min_str)

    # WHEN
    x_factheir = factheir_shop(fcontext=min_way, fstate=min_way)
    assert x_factheir.is_range() is False

    # THEN
    x_factheir = factheir_shop(min_way, fstate=min_way, fopen=10.0, fnigh=30.0)
    assert x_factheir.is_range() is True


def test_factheir_is_range_Returns_is_range_Status():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_way = create_way(root_label(), ced_min_str)

    # WHEN
    x_factheir = factheir_shop(fcontext=min_way, fstate=min_way)

    # THEN
    assert x_factheir.is_range() is False

    # WHEN
    x_factheir = factheir_shop(min_way, fstate=min_way, fopen=10.0, fnigh=30.0)

    # THEN
    assert x_factheir.is_range() is True


def test_FactCore_get_obj_key_SetsAttrCorrectly():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_way = create_way(root_label(), ced_min_str)
    secs_str = "secs"
    secs_way = create_way(min_way, secs_str)

    # WHEN
    x_factcore = FactCore(fcontext=min_way, fstate=secs_way)

    # THEN
    assert x_factcore.get_obj_key() == min_way


def test_factunits_get_from_dict_CorrectlyBuildsObj():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)
    static_dict = {
        wkday_way: {
            "fcontext": wkday_way,
            "fstate": sunday_way,
            "fopen": None,
            "fnigh": None,
        }
    }

    # WHEN
    facts_dict = factunits_get_from_dict(static_dict)

    # THEN
    assert len(facts_dict) == 1
    wkday_fact = facts_dict.get(wkday_way)
    assert wkday_fact == factunit_shop(fcontext=wkday_way, fstate=sunday_way)


def test_factunits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_way = create_way(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_way = create_way(wkday_way, sunday_str)
    static_dict = {
        wkday_way: {
            "fcontext": wkday_way,
            "fstate": sunday_way,
        }
    }

    # WHEN
    facts_dict = factunits_get_from_dict(static_dict)

    # THEN
    wkday_fact = facts_dict.get(wkday_way)
    assert wkday_fact == factunit_shop(fcontext=wkday_way, fstate=sunday_way)
