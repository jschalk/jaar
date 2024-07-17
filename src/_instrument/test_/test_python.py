from src._instrument.python import (
    get_1_if_None,
    add_dict_if_missing,
    place_obj_in_dict,
    get_all_nondictionary_objs,
    get_nested_value,
    get_positive_int,
)
from pytest import raises as pytest_raises


def test_get_1_if_None():
    # ESTABLISH / WHEN / THEN
    assert get_1_if_None(None) == 1
    assert get_1_if_None(2) == 2
    assert get_1_if_None(-3) == -3


def test_add_dict_if_missing_CorrectAddsDict():
    # ESTABLISH
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    add_dict_if_missing(x_dict=y_dict, x_keylist=[y_key1, y_key2, y_key3])

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3: {}}}}


def test_place_obj_in_dict_CorrectAddsDict():
    # ESTABLISH
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    fly_text = "flying"
    place_obj_in_dict(x_dict=y_dict, x_keylist=[y_key1, y_key2, y_key3], x_obj=fly_text)

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3: fly_text}}}


def test_get_all_nondictionary_objs_ReturnsCorrectDict():
    # ESTABLISH
    y_dict = {}
    sports_text = "sports"
    run_text = "running"
    run_list = [sports_text, run_text]
    fun_text = "fun running"
    fun_list = [sports_text, run_text, fun_text]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_text = "mountains"
    mount_list = [sports_text, run_text, mount_text]
    mount_obj = "hard"

    frank_text = "franklin mountain"
    day_text = "day"
    night_text = "night"
    day_list = [sports_text, run_text, frank_text, day_text]
    day_obj = "is hot"
    night_list = [sports_text, run_text, frank_text, night_text]
    night_obj = "is cool"
    rain_text = "raining"
    coat_text = "coat"
    fluf_text = "fluffy"
    button_text = "buttons"
    silver_obj = "silver"
    rain_list = [
        sports_text,
        run_text,
        frank_text,
        rain_text,
        coat_text,
        fluf_text,
        button_text,
    ]

    place_obj_in_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=day_list, x_obj=day_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=night_list, x_obj=night_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=rain_list, x_obj=silver_obj)
    print(y_dict)

    assert y_dict == {
        sports_text: {
            run_text: {
                fun_text: fun_obj,
                mount_text: mount_obj,
                frank_text: {
                    day_text: day_obj,
                    night_text: night_obj,
                    rain_text: {coat_text: {fluf_text: {button_text: silver_obj}}},
                },
            }
        }
    }

    # WHEN
    childless_objs = get_all_nondictionary_objs(y_dict)

    # THEN
    assert childless_objs == {
        sports_text: [fun_obj, mount_obj, day_obj, night_obj, silver_obj]
    }
    assert get_nested_value(y_dict, day_list) == day_obj
    assert get_nested_value(y_dict, mount_list) == mount_obj


def test_get_nested_value_RaisesReadableException():
    y_dict = {}
    sports_text = "sports"
    run_text = "running"
    run_list = [sports_text, run_text]
    fun_text = "fun running"
    fun_list = [sports_text, run_text, fun_text]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_text = "mountains"
    mount_list = [sports_text, run_text, mount_text]
    mount_obj = "hard"

    frank_text = "franklin mountain"
    day_text = "day"
    night_text = "night"
    day_list = [sports_text, run_text, frank_text, day_text]
    day_obj = "is hot"
    night_list = [sports_text, run_text, frank_text, night_text]
    night_obj = "is cool"

    place_obj_in_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=day_list, x_obj=day_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=night_list, x_obj=night_obj)
    assert get_nested_value(y_dict, day_list) == day_obj

    # WHEN / THEN
    swim_text = "swim"
    with pytest_raises(Exception) as excinfo:
        get_nested_value(y_dict, [swim_text])
    assert str(excinfo.value) == f"'{swim_text}' failed at level 0."

    # WHEN / THEN
    swim_text = "swim"
    with pytest_raises(Exception) as excinfo:
        get_nested_value(y_dict, [sports_text, swim_text])
    assert str(excinfo.value) == f"'{swim_text}' failed at level 1."

    # WHEN / THEN
    swim_text = "swim"
    with pytest_raises(Exception) as excinfo:
        get_nested_value(y_dict, [sports_text, swim_text, day_text])
    assert str(excinfo.value) == f"'{swim_text}' failed at level 1."


def test_get_nested_value_ReturnsNoneWhen_if_missing_return_None_True():
    y_dict = {}
    sports_text = "sports"
    run_text = "running"
    run_list = [sports_text, run_text]
    fun_text = "fun running"
    fun_list = [sports_text, run_text, fun_text]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_text = "mountains"
    mount_list = [sports_text, run_text, mount_text]
    mount_obj = "hard"

    frank_text = "franklin mountain"
    day_text = "day"
    night_text = "night"
    day_list = [sports_text, run_text, frank_text, day_text]
    day_obj = "is hot"
    night_list = [sports_text, run_text, frank_text, night_text]
    night_obj = "is cool"

    place_obj_in_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=day_list, x_obj=day_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=night_list, x_obj=night_obj)
    assert get_nested_value(y_dict, day_list, if_missing_return_None=True) == day_obj

    # WHEN / THEN
    swim_text = "swim"
    assert get_nested_value(y_dict, [swim_text], if_missing_return_None=True) is None

    # WHEN / THEN
    swim_text = "swim"
    x_value = get_nested_value(
        y_dict, [sports_text, swim_text], if_missing_return_None=True
    )
    assert x_value is None

    # WHEN / THEN
    swim_text = "swim"
    x_value = get_nested_value(
        y_dict, [sports_text, swim_text, day_text], if_missing_return_None=True
    )
    assert x_value is None


def test_get_positive_int_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert get_positive_int(None) == 0
    assert get_positive_int("sports") == 0
    assert get_positive_int() == 0
    assert get_positive_int(10) == 10
    assert get_positive_int(10.0) == 10
    assert get_positive_int(10.8) == 10
    assert get_positive_int(-10.8) == 0
