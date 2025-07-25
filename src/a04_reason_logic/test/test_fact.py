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
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)

    # WHEN
    sun_fact = FactUnit(f_context=wk_rope, f_state=sun_rope, f_lower=1.9, f_upper=2.3)

    # THEN
    print(sun_fact)
    assert sun_fact is not None
    assert sun_fact.f_context == wk_rope
    assert sun_fact.f_state == sun_rope
    assert sun_fact.f_lower == 1.9
    assert sun_fact.f_upper == 2.3


def test_FactUnit_set_range_null_SetsAttrCorrectly_1():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_fact = factunit_shop(wk_rope, wk_rope, f_lower=1.0, f_upper=5.0)
    assert wk_fact.f_lower == 1.0
    assert wk_fact.f_upper == 5.0

    # WHEN
    wk_fact.set_range_null()

    # THEN
    assert wk_fact.f_lower is None
    assert wk_fact.f_upper is None


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
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_fact = factunit_shop(wk_rope, wk_rope, f_lower=1.0, f_upper=5.0)

    # WHEN
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    wk_fact.set_attr(f_state=sun_rope)
    # THEN
    assert wk_fact.f_state == sun_rope

    # WHEN
    wk_fact.set_attr(f_lower=45)
    # THEN
    assert wk_fact.f_lower == 45

    # WHEN
    wk_fact.set_attr(f_upper=65)
    # THEN
    assert wk_fact.f_upper == 65


def test_FactUnit_get_dict_ReturnsDict():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    x_f_lower = 35
    x_f_upper = 50
    sun_fact = factunit_shop(
        f_context=wk_rope,
        f_state=sun_rope,
        f_lower=x_f_lower,
        f_upper=x_f_upper,
    )
    print(sun_fact)

    # WHEN
    fact_dict = sun_fact.get_dict()

    # THEN
    assert fact_dict is not None
    static_dict = {
        "f_context": wk_rope,
        "f_state": sun_rope,
        "f_lower": x_f_lower,
        "f_upper": x_f_upper,
    }
    assert fact_dict == static_dict


def test_FactUnit_get_dict_ReturnsPartialDict():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_fact = factunit_shop(f_context=wk_rope, f_state=sun_rope)
    print(sun_fact)

    # WHEN
    fact_dict = sun_fact.get_dict()

    # THEN
    assert fact_dict is not None
    static_dict = {
        "f_context": wk_rope,
        "f_state": sun_rope,
    }
    assert fact_dict == static_dict


def test_FactUnit_find_replace_rope_SetsAttrCorrectly():
    # ESTABLISH
    wk_str = "wk"
    old_rope = create_rope("old_new")
    old_wk_rope = create_rope(old_rope, wk_str)
    sun_str = "Sun"
    old_sun_rope = create_rope(old_wk_rope, sun_str)
    sun_fact = factunit_shop(f_context=old_wk_rope, f_state=old_sun_rope)
    print(sun_fact)
    assert sun_fact.f_context == old_wk_rope
    assert sun_fact.f_state == old_sun_rope

    # WHEN
    new_rope = create_rope("new_fun")
    sun_fact.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    # THEN
    new_wk_rope = create_rope(new_rope, wk_str)
    new_sun_rope = create_rope(new_wk_rope, sun_str)
    assert sun_fact.f_context == new_wk_rope
    assert sun_fact.f_state == new_sun_rope


def test_FactUnit_get_tuple_ReturnsObj_Scenario0_r_context_f_state_only():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_fact = factunit_shop(f_context=wk_rope, f_state=sun_rope)

    # WHEN
    sun_tuple = sun_fact.get_tuple()

    # THEN
    assert sun_tuple
    assert sun_tuple == (wk_rope, sun_rope, None, None)


def test_FactUnit_get_tuple_ReturnsObj_Scenario1_ValuesIn_f_lower_f_upper():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_f_lower = 6
    sun_f_upper = 9
    sun_fact = factunit_shop(wk_rope, sun_rope, sun_f_lower, sun_f_upper)

    # WHEN
    sun_tuple = sun_fact.get_tuple()

    # THEN
    assert sun_tuple
    assert sun_tuple == (wk_rope, sun_rope, sun_f_lower, sun_f_upper)


def test_get_factunit_from_tuple_ReturnsObj_Scenario0_r_context_f_state_only():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_fact = factunit_shop(f_context=wk_rope, f_state=sun_rope)
    sun_tuple = sun_fact.get_tuple()

    # WHEN
    gen_sun_factunit = get_factunit_from_tuple(sun_tuple)

    # THEN
    assert gen_sun_factunit
    assert gen_sun_factunit == sun_fact


def test_get_factunit_from_tuple_ReturnsObj_Scenario1_ValuesIn_f_lower_f_upper():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_f_lower = 6
    sun_f_upper = 9
    sun_fact = factunit_shop(wk_rope, sun_rope, sun_f_lower, sun_f_upper)
    sun_tuple = sun_fact.get_tuple()

    # WHEN
    gen_sun_factunit = get_factunit_from_tuple(sun_tuple)

    # THEN
    assert gen_sun_factunit
    assert gen_sun_factunit == sun_fact


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
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    static_dict = {
        wk_rope: {
            "f_context": wk_rope,
            "f_state": sun_rope,
            "f_lower": None,
            "f_upper": None,
        }
    }

    # WHEN
    facts_dict = factunits_get_from_dict(static_dict)

    # THEN
    assert len(facts_dict) == 1
    wk_fact = facts_dict.get(wk_rope)
    assert wk_fact == factunit_shop(f_context=wk_rope, f_state=sun_rope)


def test_factunits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    static_dict = {
        wk_rope: {
            "f_context": wk_rope,
            "f_state": sun_rope,
        }
    }

    # WHEN
    facts_dict = factunits_get_from_dict(static_dict)

    # THEN
    wk_fact = facts_dict.get(wk_rope)
    assert wk_fact == factunit_shop(f_context=wk_rope, f_state=sun_rope)
