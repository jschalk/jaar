from src.f0_instrument.python_tool import (
    get_1_if_None,
    add_dict_if_missing,
    place_obj_in_dict,
    get_all_nondictionary_objs,
    get_nested_value,
    get_positive_int,
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    create_l2nested_csv_dict,
    get_positional_dict,
    add_headers_to_csv,
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
    fly_str = "flying"
    place_obj_in_dict(x_dict=y_dict, x_keylist=[y_key1, y_key2, y_key3], x_obj=fly_str)

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3: fly_str}}}


def test_get_all_nondictionary_objs_ReturnsCorrectDict():
    # ESTABLISH
    y_dict = {}
    sports_str = "sports"
    run_str = "running"
    run_list = [sports_str, run_str]
    fun_str = "fun running"
    fun_list = [sports_str, run_str, fun_str]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_str = "mountains"
    mount_list = [sports_str, run_str, mount_str]
    mount_obj = "hard"

    frank_str = "franklin mountain"
    day_str = "day"
    night_str = "night"
    day_list = [sports_str, run_str, frank_str, day_str]
    day_obj = "is hot"
    night_list = [sports_str, run_str, frank_str, night_str]
    night_obj = "is cool"
    rain_str = "raining"
    coat_str = "coat"
    fluf_str = "fluffy"
    button_str = "buttons"
    silver_obj = "silver"
    rain_list = [
        sports_str,
        run_str,
        frank_str,
        rain_str,
        coat_str,
        fluf_str,
        button_str,
    ]

    place_obj_in_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=day_list, x_obj=day_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=night_list, x_obj=night_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=rain_list, x_obj=silver_obj)
    print(y_dict)

    assert y_dict == {
        sports_str: {
            run_str: {
                fun_str: fun_obj,
                mount_str: mount_obj,
                frank_str: {
                    day_str: day_obj,
                    night_str: night_obj,
                    rain_str: {coat_str: {fluf_str: {button_str: silver_obj}}},
                },
            }
        }
    }

    # WHEN
    childless_objs = get_all_nondictionary_objs(y_dict)

    # THEN
    assert childless_objs == {
        sports_str: [fun_obj, mount_obj, day_obj, night_obj, silver_obj]
    }
    assert get_nested_value(y_dict, day_list) == day_obj
    assert get_nested_value(y_dict, mount_list) == mount_obj


def test_get_nested_value_RaisesReadableException():
    y_dict = {}
    sports_str = "sports"
    run_str = "running"
    run_list = [sports_str, run_str]
    fun_str = "fun running"
    fun_list = [sports_str, run_str, fun_str]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_str = "mountains"
    mount_list = [sports_str, run_str, mount_str]
    mount_obj = "hard"

    frank_str = "franklin mountain"
    day_str = "day"
    night_str = "night"
    day_list = [sports_str, run_str, frank_str, day_str]
    day_obj = "is hot"
    night_list = [sports_str, run_str, frank_str, night_str]
    night_obj = "is cool"

    place_obj_in_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=day_list, x_obj=day_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=night_list, x_obj=night_obj)
    assert get_nested_value(y_dict, day_list) == day_obj

    # WHEN / THEN
    swim_str = "swim"
    with pytest_raises(Exception) as excinfo:
        get_nested_value(y_dict, [swim_str])
    assert str(excinfo.value) == f"'{swim_str}' failed at level 0."

    # WHEN / THEN
    swim_str = "swim"
    with pytest_raises(Exception) as excinfo:
        get_nested_value(y_dict, [sports_str, swim_str])
    assert str(excinfo.value) == f"'{swim_str}' failed at level 1."

    # WHEN / THEN
    swim_str = "swim"
    with pytest_raises(Exception) as excinfo:
        get_nested_value(y_dict, [sports_str, swim_str, day_str])
    assert str(excinfo.value) == f"'{swim_str}' failed at level 1."


def test_get_nested_value_ReturnsNoneWhen_if_missing_return_None_True():
    y_dict = {}
    sports_str = "sports"
    run_str = "running"
    run_list = [sports_str, run_str]
    fun_str = "fun running"
    fun_list = [sports_str, run_str, fun_str]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_str = "mountains"
    mount_list = [sports_str, run_str, mount_str]
    mount_obj = "hard"

    frank_str = "franklin mountain"
    day_str = "day"
    night_str = "night"
    day_list = [sports_str, run_str, frank_str, day_str]
    day_obj = "is hot"
    night_list = [sports_str, run_str, frank_str, night_str]
    night_obj = "is cool"

    place_obj_in_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=day_list, x_obj=day_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=night_list, x_obj=night_obj)
    assert get_nested_value(y_dict, day_list, if_missing_return_None=True) == day_obj

    # WHEN / THEN
    swim_str = "swim"
    assert get_nested_value(y_dict, [swim_str], if_missing_return_None=True) is None

    # WHEN / THEN
    swim_str = "swim"
    x_value = get_nested_value(
        y_dict, [sports_str, swim_str], if_missing_return_None=True
    )
    assert x_value is None

    # WHEN / THEN
    swim_str = "swim"
    x_value = get_nested_value(
        y_dict, [sports_str, swim_str, day_str], if_missing_return_None=True
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
    x_id_str = "x_id"
    y_id_str = "y_id"
    w_id_str = "w_id"
    u_id_str = "u_id"
    z_id_str = "z_id"
    assert x_headers == [
        x_id_str,
        y_id_str,
        w_id_str,
        u_id_str,
        z_id_str,
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
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""{x_id},{sue_str},Bob,13,29
{x_id},{sue_str},Sue,11,23
{x_id},{sue_str},Yao,41,37
{x_id},{sue_str},Zia,41,37
{x_id},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_column1_column2_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {x_id: {sue_str: 1}}
    assert u_dict == {x_id: {sue_str: 4, bob_str: 1}}


def test_create_l2nested_csv_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    x_id = "music56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""{x_id},{sue_str},Bob,13,29
{x_id},{sue_str},Sue,11,23
{x_id},{sue_str},Yao,41,37
{x_id},{sue_str},Zia,41,37
{x_id},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = create_l2nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f"""{x_id},{sue_str},Bob,13,29
{x_id},{sue_str},Sue,11,23
{x_id},{sue_str},Yao,41,37
{x_id},{sue_str},Zia,41,37
"""
    static_bob_csv = f"""{x_id},{bob_str},Yao,41,37
"""
    generated_owner_id_dict = u_dict.get(x_id)
    assert generated_owner_id_dict
    assert list(generated_owner_id_dict.keys()) == [sue_str, bob_str]
    generated_bob_csv = generated_owner_id_dict.get(bob_str)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_owner_id_dict.get(sue_str)
    assert generated_sue_csv == static_sue_csv
    owner_id_csv_dict = {sue_str: static_sue_csv, bob_str: static_bob_csv}
    assert u_dict == {x_id: owner_id_csv_dict}


def test_create_l2nested_csv_dict_ReturnsObj_Scenario1_Multiple1stLevels():
    # ESTABLISH
    music3_id = "music3"
    music4_id = "music4"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""{music3_id},{sue_str},Bob,13,29
{music4_id},{sue_str},Sue,11,23
{music4_id},{sue_str},Yao,41,37
{music4_id},{sue_str},Zia,41,37
{music4_id},{bob_str},Yao,41,37
"""

    # WHEN
    filtered_dict = create_l2nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    music3_sue_csv = f"""{music3_id},{sue_str},Bob,13,29
"""
    music4_sue_csv = f"""{music4_id},{sue_str},Sue,11,23
{music4_id},{sue_str},Yao,41,37
{music4_id},{sue_str},Zia,41,37
"""
    static_bob_csv = f"""{music4_id},{bob_str},Yao,41,37
"""
    music3_dict = filtered_dict.get(music3_id)
    music4_dict = filtered_dict.get(music4_id)
    assert music3_dict
    assert music4_dict
    assert list(music3_dict.keys()) == [sue_str]
    assert list(music4_dict.keys()) == [sue_str, bob_str]
    generated_bob_csv = music4_dict.get(bob_str)
    assert generated_bob_csv == static_bob_csv
    generated3_sue_csv = music3_dict.get(sue_str)
    generated4_sue_csv = music4_dict.get(sue_str)
    print(f"{generated3_sue_csv=}")
    print(f"{generated4_sue_csv=}")
    assert generated3_sue_csv == music3_sue_csv
    assert generated4_sue_csv == music4_sue_csv
    owner_id3_csv_dict = {sue_str: music3_sue_csv}
    owner_id4_csv_dict = {sue_str: music4_sue_csv, bob_str: static_bob_csv}
    assert filtered_dict == {
        music3_id: owner_id3_csv_dict,
        music4_id: owner_id4_csv_dict,
    }


def test_get_positional_dict_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    x_list = [bob_str, sue_str, yao_str]

    # WHEN / THEN
    assert get_positional_dict([]) == {}
    assert get_positional_dict([bob_str]) == {bob_str: 0}
    assert get_positional_dict(x_list) == {bob_str: 0, sue_str: 1, yao_str: 2}


def test_add_headers_to_csv_ReturnsObj():
    # ESTABLISH
    swim_text = "swim"
    six_text = "six"
    seven_text = "seven"
    headers = [swim_text, six_text, seven_text]
    headerless_csv = """Bob,13,29
Sue,11,23
Yao,41,37
Zia,41,37
Yao,41,37
"""

    # WHEN
    gen_csv = add_headers_to_csv(headers, headerless_csv)

    # THEN
    assert gen_csv
    assert (
        gen_csv
        == f"""{swim_text},{six_text},{seven_text}
{headerless_csv}"""
    )
