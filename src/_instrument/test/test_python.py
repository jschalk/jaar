from src._instrument.python_tool import (
    get_1_if_None,
    add_dict_if_missing,
    place_obj_in_dict,
    get_all_nondictionary_objs,
    get_nested_value,
    get_positive_int,
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    create_filtered_csv_dict,
    get_positional_dict,
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


def test_extract_csv_headers_ReturnsEmptyObj():
    # ESTABLISH
    x_csv = ""

    # WHEN
    x_headers = extract_csv_headers(x_csv)

    # THEN
    assert x_headers == []


def test_extract_csv_headers_ReturnsObj():
    # ESTABLISH
    x_csv = """x_id,y_id,w_id,u_id,z_id
music,Sue,Bob,13,29
music,Sue,Sue,11,23
music,Sue,Yao,41,37
"""

    # WHEN
    x_headers, x_csv = extract_csv_headers(x_csv)

    # THEN
    x_id_text = "x_id"
    y_id_text = "y_id"
    w_id_text = "w_id"
    u_id_text = "u_id"
    z_id_text = "z_id"
    assert x_headers == [
        x_id_text,
        y_id_text,
        w_id_text,
        u_id_text,
        z_id_text,
    ]


def test_extract_csv_headers_RemovesHeaders_csv():
    # ESTABLISH
    x_csv = """x_id,y_id,w_id,u_id,z_id
music,Sue,Bob,13,29
music,Sue,Sue,11,23
music,Sue,Yao,41,37
"""

    # WHEN
    x_headers, new_csv = extract_csv_headers(x_csv)

    # THEN
    print(f"{new_csv=}")
    headerless_csv = """music,Sue,Bob,13,29
music,Sue,Sue,11,23
music,Sue,Yao,41,37
"""
    assert new_csv == headerless_csv


def test_get_csv_column1_column2_metrics_ReturnsEmptyObj():
    # ESTABLISH
    headerless_csv = ""

    # WHEN
    x_dict = get_csv_column1_column2_metrics(headerless_csv=headerless_csv)

    # THEN
    assert x_dict == {}


def test_get_csv_column1_column2_metrics_ReturnsObj_Scenario1():
    # ESTABLISH
    x_id = "music56"
    y_id = "Yao"
    headerless_csv = f"""{x_id},{y_id},Bob,13,29
"""

    # WHEN
    x_dict = get_csv_column1_column2_metrics(headerless_csv=headerless_csv)

    # THEN
    assert x_dict == {x_id: {y_id: 1}}


def test_get_csv_column1_column2_metrics_ReturnsObj_Scenario2():
    # ESTABLISH
    x_id = "music56"
    sue_text = "Sue"
    bob_text = "Bob"
    headerless_csv = f"""{x_id},{sue_text},Bob,13,29
{x_id},{sue_text},Sue,11,23
{x_id},{sue_text},Yao,41,37
{x_id},{sue_text},Zia,41,37
{x_id},{bob_text},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_column1_column2_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {x_id: {sue_text: 1}}
    assert u_dict == {x_id: {sue_text: 4, bob_text: 1}}


def test_create_filtered_csv_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    x_id = "music56"
    sue_text = "Sue"
    bob_text = "Bob"
    headerless_csv = f"""{x_id},{sue_text},Bob,13,29
{x_id},{sue_text},Sue,11,23
{x_id},{sue_text},Yao,41,37
{x_id},{sue_text},Zia,41,37
{x_id},{bob_text},Yao,41,37
"""

    # WHEN
    u_dict = create_filtered_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f"""{x_id},{sue_text},Bob,13,29
{x_id},{sue_text},Sue,11,23
{x_id},{sue_text},Yao,41,37
{x_id},{sue_text},Zia,41,37
"""
    static_bob_csv = f"""{x_id},{bob_text},Yao,41,37
"""
    generated_owner_id_dict = u_dict.get(x_id)
    assert generated_owner_id_dict
    assert list(generated_owner_id_dict.keys()) == [sue_text, bob_text]
    generated_bob_csv = generated_owner_id_dict.get(bob_text)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_owner_id_dict.get(sue_text)
    assert generated_sue_csv == static_sue_csv
    owner_id_csv_dict = {sue_text: static_sue_csv, bob_text: static_bob_csv}
    assert u_dict == {x_id: owner_id_csv_dict}


def test_get_positional_dict_ReturnsObj():
    # ESTABLISH
    bob_text = "Bob"
    sue_text = "Sue"
    yao_text = "Yao"
    x_list = [bob_text, sue_text, yao_text]

    # WHEN / THEN
    assert get_positional_dict([]) == {}
    assert get_positional_dict([bob_text]) == {bob_text: 0}
    assert get_positional_dict(x_list) == {bob_text: 0, sue_text: 1, yao_text: 2}
