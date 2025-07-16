from src.a01_term_logic.rope import create_rope, get_default_central_label as root_label
from src.a04_reason_logic.reason_plan import (
    FactCore,
    FactUnit,
    factheir_shop,
    factunit_shop,
    factunits_get_from_dict,
    get_factunit_from_tuple,
)
from src.a04_reason_logic.test._util.a04_str import (
    f_context_str,
    f_lower_str,
    f_state_str,
    f_upper_str,
)


def test_FactUnit_Exists():
    # ESTABLISH / WHEN
    x_fact = FactUnit()

    # THEN
    assert not x_fact.f_context
    assert not x_fact.f_state
    assert not x_fact.f_lower
    assert not x_fact.f_upper
    obj_attrs = set(x_fact.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {f_context_str(), f_upper_str(), f_lower_str(), f_state_str()}


def test_FactUnit_DataClass_function():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_rope = create_rope(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)

    # WHEN
    sunday_fact = FactUnit(
        f_context=wkday_rope, f_state=sunday_rope, f_lower=1.9, f_upper=2.3
    )

    # THEN
    print(sunday_fact)
    assert sunday_fact is not None
    assert sunday_fact.f_context == wkday_rope
    assert sunday_fact.f_state == sunday_rope
    assert sunday_fact.f_lower == 1.9
    assert sunday_fact.f_upper == 2.3


def test_FactUnit_set_range_null_SetsAttrCorrectly_1():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_rope = create_rope(root_label(), wkday_str)
    wkday_fact = factunit_shop(wkday_rope, wkday_rope, f_lower=1.0, f_upper=5.0)
    assert wkday_fact.f_lower == 1.0
    assert wkday_fact.f_upper == 5.0

    # WHEN
    wkday_fact.set_range_null()

    # THEN
    assert wkday_fact.f_lower is None
    assert wkday_fact.f_upper is None


def test_FactUnit_set_f_state_to_f_context_SetsAttr_1():
    # ESTABLISH
    floor_str = "floor"
    floor_rope = create_rope(root_label(), floor_str)
    dirty_str = "dirty"
    dirty_rope = create_rope(root_label(), dirty_str)
    floor_fact = factunit_shop(floor_rope, dirty_rope)
    assert floor_fact.f_context == floor_rope
    assert floor_fact.f_state == dirty_rope

    # WHEN
    floor_fact.set_f_state_to_f_context()

    # THEN
    assert floor_fact.f_context == floor_rope
    assert floor_fact.f_state == floor_rope


def test_FactUnit_set_f_state_to_f_context_SetsAttr_2():
    # ESTABLISH
    floor_str = "floor"
    floor_rope = create_rope(root_label(), floor_str)
    dirty_str = "dirty"
    dirty_rope = create_rope(root_label(), dirty_str)
    floor_fact = factunit_shop(floor_rope, dirty_rope, 1, 6)
    assert floor_fact.f_lower is not None
    assert floor_fact.f_upper is not None

    # WHEN
    floor_fact.set_f_state_to_f_context()

    # THEN
    assert floor_fact.f_lower is None
    assert floor_fact.f_upper is None


def test_FactUnit_set_attr_SetsAttrCorrectly_2():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_rope = create_rope(root_label(), wkday_str)
    wkday_fact = factunit_shop(wkday_rope, wkday_rope, f_lower=1.0, f_upper=5.0)

    # WHEN
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)
    wkday_fact.set_attr(f_state=sunday_rope)
    # THEN
    assert wkday_fact.f_state == sunday_rope

    # WHEN
    wkday_fact.set_attr(f_lower=45)
    # THEN
    assert wkday_fact.f_lower == 45

    # WHEN
    wkday_fact.set_attr(f_upper=65)
    # THEN
    assert wkday_fact.f_upper == 65


def test_FactUnit_get_dict_ReturnsDict():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_rope = create_rope(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)
    x_f_lower = 35
    x_f_upper = 50
    sunday_fact = factunit_shop(
        f_context=wkday_rope,
        f_state=sunday_rope,
        f_lower=x_f_lower,
        f_upper=x_f_upper,
    )
    print(sunday_fact)

    # WHEN
    fact_dict = sunday_fact.get_dict()

    # THEN
    assert fact_dict is not None
    static_dict = {
        "f_context": wkday_rope,
        "f_state": sunday_rope,
        "f_lower": x_f_lower,
        "f_upper": x_f_upper,
    }
    assert fact_dict == static_dict


def test_FactUnit_get_dict_ReturnsPartialDict():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_rope = create_rope(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)
    sunday_fact = factunit_shop(f_context=wkday_rope, f_state=sunday_rope)
    print(sunday_fact)

    # WHEN
    fact_dict = sunday_fact.get_dict()

    # THEN
    assert fact_dict is not None
    static_dict = {
        "f_context": wkday_rope,
        "f_state": sunday_rope,
    }
    assert fact_dict == static_dict


def test_FactUnit_find_replace_rope_SetsAttrCorrectly():
    # ESTABLISH
    wkday_str = "wkday"
    old_rope = create_rope("old_new")
    old_wkday_rope = create_rope(old_rope, wkday_str)
    sunday_str = "Sunday"
    old_sunday_rope = create_rope(old_wkday_rope, sunday_str)
    sunday_fact = factunit_shop(f_context=old_wkday_rope, f_state=old_sunday_rope)
    print(sunday_fact)
    assert sunday_fact.f_context == old_wkday_rope
    assert sunday_fact.f_state == old_sunday_rope

    # WHEN
    new_rope = create_rope("new_fun")
    sunday_fact.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    # THEN
    new_wkday_rope = create_rope(new_rope, wkday_str)
    new_sunday_rope = create_rope(new_wkday_rope, sunday_str)
    assert sunday_fact.f_context == new_wkday_rope
    assert sunday_fact.f_state == new_sunday_rope


def test_FactUnit_get_tuple_ReturnsObj_Scenario0_r_context_f_state_only():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)
    sunday_fact = factunit_shop(f_context=wkday_rope, f_state=sunday_rope)

    # WHEN
    sunday_tuple = sunday_fact.get_tuple()

    # THEN
    assert sunday_tuple
    assert sunday_tuple == (wkday_rope, sunday_rope, None, None)


def test_FactUnit_get_tuple_ReturnsObj_Scenario1_ValuesIn_f_lower_f_upper():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)
    sun_f_lower = 6
    sun_f_upper = 9
    sunday_fact = factunit_shop(wkday_rope, sunday_rope, sun_f_lower, sun_f_upper)

    # WHEN
    sunday_tuple = sunday_fact.get_tuple()

    # THEN
    assert sunday_tuple
    assert sunday_tuple == (wkday_rope, sunday_rope, sun_f_lower, sun_f_upper)


def test_get_factunit_from_tuple_ReturnsObj_Scenario0_r_context_f_state_only():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)
    sunday_fact = factunit_shop(f_context=wkday_rope, f_state=sunday_rope)
    sunday_tuple = sunday_fact.get_tuple()

    # WHEN
    gen_sunday_factunit = get_factunit_from_tuple(sunday_tuple)

    # THEN
    assert gen_sunday_factunit
    assert gen_sunday_factunit == sunday_fact


def test_get_factunit_from_tuple_ReturnsObj_Scenario1_ValuesIn_f_lower_f_upper():
    # ESTABLISH
    wkday_str = "wkday"
    wkday_rope = create_rope(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)
    sun_f_lower = 6
    sun_f_upper = 9
    sunday_fact = factunit_shop(wkday_rope, sunday_rope, sun_f_lower, sun_f_upper)
    sunday_tuple = sunday_fact.get_tuple()

    # WHEN
    gen_sunday_factunit = get_factunit_from_tuple(sunday_tuple)

    # THEN
    assert gen_sunday_factunit
    assert gen_sunday_factunit == sunday_fact


def test_FactHeir_IsModifiedByFactUnit():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_rope = create_rope(root_label(), ced_min_str)
    ced_factheir = factheir_shop(min_rope, min_rope, 10.0, 30.0)
    ced_factunit = factunit_shop(min_rope, min_rope, 20.0, 30.0)
    assert ced_factheir.f_lower == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)

    # THEN
    assert ced_factheir.f_lower == 20

    # ESTABLISH
    ced_factheir = factheir_shop(min_rope, min_rope, 10.0, 30.0)
    ced_factunit = factunit_shop(min_rope, min_rope, 30.0, 30.0)
    assert ced_factheir.f_lower == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)
    assert ced_factheir.f_lower == 30

    # ESTABLISH
    ced_factheir = factheir_shop(min_rope, min_rope, 10.0, 30.0)
    ced_factunit = factunit_shop(min_rope, min_rope, 35.0, 57.0)
    assert ced_factheir.f_lower == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)

    # THEN
    assert ced_factheir.f_lower == 10

    # ESTABLISH
    ced_factheir = factheir_shop(min_rope, min_rope, 10.0, 30.0)
    ced_factunit = factunit_shop(min_rope, min_rope, 5.0, 7.0)
    assert ced_factheir.f_lower == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)

    # THEN
    assert ced_factheir.f_lower == 10


def test_FactHeir_is_range_Returns_is_range_Status():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_rope = create_rope(root_label(), ced_min_str)

    # WHEN
    x_factheir = factheir_shop(f_context=min_rope, f_state=min_rope)
    assert x_factheir.is_range() is False

    # THEN
    x_factheir = factheir_shop(min_rope, f_state=min_rope, f_lower=10.0, f_upper=30.0)
    assert x_factheir.is_range() is True


def test_factheir_is_range_Returns_is_range_Status():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_rope = create_rope(root_label(), ced_min_str)

    # WHEN
    x_factheir = factheir_shop(f_context=min_rope, f_state=min_rope)

    # THEN
    assert x_factheir.is_range() is False

    # WHEN
    x_factheir = factheir_shop(min_rope, f_state=min_rope, f_lower=10.0, f_upper=30.0)

    # THEN
    assert x_factheir.is_range() is True


def test_FactCore_get_obj_key_SetsAttrCorrectly():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_rope = create_rope(root_label(), ced_min_str)
    secs_str = "secs"
    secs_rope = create_rope(min_rope, secs_str)

    # WHEN
    x_factcore = FactCore(f_context=min_rope, f_state=secs_rope)

    # THEN
    assert x_factcore.get_obj_key() == min_rope


def test_factunits_get_from_dict_CorrectlyBuildsObj():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_rope = create_rope(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)
    static_dict = {
        wkday_rope: {
            "f_context": wkday_rope,
            "f_state": sunday_rope,
            "f_lower": None,
            "f_upper": None,
        }
    }

    # WHEN
    facts_dict = factunits_get_from_dict(static_dict)

    # THEN
    assert len(facts_dict) == 1
    wkday_fact = facts_dict.get(wkday_rope)
    assert wkday_fact == factunit_shop(f_context=wkday_rope, f_state=sunday_rope)


def test_factunits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # ESTABLISH
    wkday_str = "wkdays"
    wkday_rope = create_rope(root_label(), wkday_str)
    sunday_str = "Sunday"
    sunday_rope = create_rope(wkday_rope, sunday_str)
    static_dict = {
        wkday_rope: {
            "f_context": wkday_rope,
            "f_state": sunday_rope,
        }
    }

    # WHEN
    facts_dict = factunits_get_from_dict(static_dict)

    # THEN
    wkday_fact = facts_dict.get(wkday_rope)
    assert wkday_fact == factunit_shop(f_context=wkday_rope, f_state=sunday_rope)
