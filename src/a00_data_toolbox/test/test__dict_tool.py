from copy import deepcopy as copy_deepcopy
from numpy import int64 as numpy_int64
from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import (
    add_headers_to_csv,
    add_nested_dict_if_missing,
    change_nested_key,
    create_2d_array_from_dict,
    create_l2nested_csv_dict,
    del_in_nested_dict,
    exists_in_nested_dict,
    extract_csv_headers,
    get_0_if_None,
    get_1_if_None,
    get_all_nondictionary_objs,
    get_csv_column1_column2_metrics,
    get_empty_str_if_None,
    get_from_nested_dict,
    get_max_key,
    get_nested_dict_key_by_level,
    get_nested_dict_keys_by_level,
    get_nested_keys_by_level,
    get_nested_non_dict_keys_by_level,
    get_nested_non_dict_keys_list,
    get_positional_dict,
    get_positive_int,
    get_sorted_list_of_dict_keys,
    get_str_in_all_sub_dict,
    get_str_in_sub_dict,
    is_2d_with_unique_keys,
    set_in_nested_dict,
    str_in_all_dict,
    str_in_all_dict_keys,
    str_in_all_dict_values,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
)


def test_get_1_if_None():
    # ESTABLISH / WHEN / THEN
    assert get_1_if_None(None) == 1
    assert get_1_if_None(2) == 2
    assert get_1_if_None(-3) == -3


def test_get_empty_str_if_None():
    # ESTABLISH / WHEN / THEN
    assert get_empty_str_if_None(None) == ""
    assert get_empty_str_if_None(2) == "2"
    assert get_empty_str_if_None(-3) == "-3"
    assert get_empty_str_if_None("Fay") == "Fay"


def test_get_0_if_None():
    # ESTABLISH / WHEN / THEN
    assert get_0_if_None(None) == 0
    assert get_0_if_None(2) == 2
    assert get_0_if_None(-3) == -3
    e7 = numpy_int64(7)
    assert str(type(get_0_if_None(e7))) != "<class 'numpy.int64'>"
    assert str(type(get_0_if_None(e7))) == "<class 'int'>"


def test_add_nested_dict_if_missing_CorrectAddsDict():
    # ESTABLISH
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    add_nested_dict_if_missing(x_dict=y_dict, x_keylist=[y_key1, y_key2, y_key3])

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3: {}}}}


def test_set_in_nested_dict_CorrectAddsDict():
    # ESTABLISH
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    fly_str = "flying"
    set_in_nested_dict(x_dict=y_dict, x_keylist=[y_key1, y_key2, y_key3], x_obj=fly_str)

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3: fly_str}}}


def test_exists_in_nested_dict_CorrectAddsDict():
    # ESTABLISH
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    y_keylist = [y_key1, y_key2, y_key3]
    fly_str = "flying"
    assert exists_in_nested_dict(x_dict=y_dict, x_keylist=y_keylist) is False

    # WHEN
    set_in_nested_dict(y_dict, y_keylist, x_obj=fly_str)

    # THEN
    assert exists_in_nested_dict(y_dict, y_keylist)


def test_del_in_nested_dict_CorrectSetsDict():
    # TODO apply suggestions from Sourery
    # -def add_dict_if_missing(x_dict: dict, x_keylist: list[any]):
    # +def add_nested_dict_if_missing(x_dict: dict, x_keylist: list[any]):
    # issue (complexity): Consider simplifying nested dictionary operations using built-in Python features and more efficient algorithms.

    # While the introduction of consistent nested dictionary operations can improve code readability, the current implementation adds unnecessary complexity. Consider the follow ing simplifications:

    # Use collections.defaultdict to simplify nested dictionary creation:
    # from collections import defaultdict

    # def nested_dict():
    #     return defaultdict(nested_dict)

    # # Usage
    # my_dict = nested_dict()
    # my_dict['a']['b']['c'] = 1  # No need for explicit nested creation
    # Simplify del_in_nested_dict by using a recursive approach:
    # def del_in_nested_dict(d, keys):
    #     if len(keys) == 1:
    #         del d[keys[0]]
    #     else:
    #         del_in_nested_dict(d[keys[0]], keys[1:])
    #         if not d[keys[0]]:  # Remove empty nested dicts
    #             del d[keys[0]]
    # Consider using functools.reduce for get_from_nested_dict:
    # from functools import reduce
    # import operator

    # def get_from_nested_dict(d, keys, default=None):
    #     try:
    #         return reduce(operator.get, keys, d)
    #     except (KeyError, TypeError):
    #         return default
    # These changes maintain the consistent interface while reducing code complexity and improving efficiency. The defaultdict approach eliminates the need for explicit nested dictionary creation, the simplified del_in_nested_dict is more readable and efficient, and the reduce-based get_from_nested_dict is more con_cise.
    # ESTABLISH
    y_dict = {}
    y_key1 = "sports"
    y_key2 = "running"
    y_key3_0 = "fun running"
    y_key3_1 = "rain running"
    y3_0_keylist = [y_key1, y_key2, y_key3_0]
    y3_1_keylist = [y_key1, y_key2, y_key3_1]
    fly_str = "flying"
    set_in_nested_dict(y_dict, y3_1_keylist, x_obj=fly_str)
    assert y_dict == {y_key1: {y_key2: {y_key3_1: fly_str}}}
    assert exists_in_nested_dict(y_dict, y3_0_keylist) is False
    assert exists_in_nested_dict(y_dict, y3_1_keylist)

    # WHEN
    del_in_nested_dict(y_dict, y3_0_keylist)

    # THEN
    assert exists_in_nested_dict(y_dict, y3_0_keylist) is False

    # ESTABLISH
    set_in_nested_dict(y_dict, y3_0_keylist, x_obj=fly_str)
    assert y_dict == {y_key1: {y_key2: {y_key3_0: fly_str, y_key3_1: fly_str}}}
    assert exists_in_nested_dict(y_dict, y3_0_keylist)
    assert exists_in_nested_dict(y_dict, y3_1_keylist)

    # WHEN
    del_in_nested_dict(y_dict, y3_0_keylist)

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3_1: fly_str}}}
    assert exists_in_nested_dict(y_dict, y3_0_keylist) is False
    assert exists_in_nested_dict(y_dict, y3_1_keylist)

    # WHEN
    del_in_nested_dict(y_dict, y3_1_keylist)

    # THEN
    assert not y_dict
    assert not get_from_nested_dict(y_dict, y3_0_keylist, True)


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
    _2pm_str = "_2pm"
    _1am_str = "_1am"
    _2pm_list = [sports_str, run_str, frank_str, _2pm_str]
    _2pm_obj = "is hot"
    _1am_list = [sports_str, run_str, frank_str, _1am_str]
    _1am_obj = "is cool"
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

    set_in_nested_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_2pm_list, x_obj=_2pm_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_1am_list, x_obj=_1am_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=rain_list, x_obj=silver_obj)
    print(y_dict)

    assert y_dict == {
        sports_str: {
            run_str: {
                fun_str: fun_obj,
                mount_str: mount_obj,
                frank_str: {
                    _2pm_str: _2pm_obj,
                    _1am_str: _1am_obj,
                    rain_str: {coat_str: {fluf_str: {button_str: silver_obj}}},
                },
            }
        }
    }

    # WHEN
    childless_objs = get_all_nondictionary_objs(y_dict)

    # THEN
    assert childless_objs == {
        sports_str: [fun_obj, mount_obj, _2pm_obj, _1am_obj, silver_obj]
    }
    assert get_from_nested_dict(y_dict, _2pm_list) == _2pm_obj
    assert get_from_nested_dict(y_dict, mount_list) == mount_obj


def test_get_from_nested_dict_RaisesNestedException():
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
    _2pm_str = "_2pm"
    _1am_str = "_1am"
    _2pm_list = [sports_str, run_str, frank_str, _2pm_str]
    _2pm_obj = "is hot"
    _1am_list = [sports_str, run_str, frank_str, _1am_str]
    _1am_obj = "is cool"

    set_in_nested_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_2pm_list, x_obj=_2pm_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_1am_list, x_obj=_1am_obj)
    assert get_from_nested_dict(y_dict, _2pm_list) == _2pm_obj

    # WHEN / THEN
    swim_str = "swim"
    with pytest_raises(Exception) as excinfo:
        get_from_nested_dict(y_dict, [swim_str])
    assert str(excinfo.value) == f"'{swim_str}' failed at level 0."

    # WHEN / THEN
    swim_str = "swim"
    with pytest_raises(Exception) as excinfo:
        get_from_nested_dict(y_dict, [sports_str, swim_str])
    assert str(excinfo.value) == f"'{swim_str}' failed at level 1."

    # WHEN / THEN
    swim_str = "swim"
    with pytest_raises(Exception) as excinfo:
        get_from_nested_dict(y_dict, [sports_str, swim_str, _2pm_str])
    assert str(excinfo.value) == f"'{swim_str}' failed at level 1."


def test_get_from_nested_dict_ReturnsNoneWhen_if_missing_return_None_True():
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
    _2pm_str = "_2pm"
    _1am_str = "_1am"
    _2pm_list = [sports_str, run_str, frank_str, _2pm_str]
    _2pm_obj = "is hot"
    _1am_list = [sports_str, run_str, frank_str, _1am_str]
    _1am_obj = "is cool"

    set_in_nested_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_2pm_list, x_obj=_2pm_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_1am_list, x_obj=_1am_obj)
    assert (
        get_from_nested_dict(y_dict, _2pm_list, if_missing_return_None=True) == _2pm_obj
    )

    # WHEN / THEN
    swim_str = "swim"
    assert get_from_nested_dict(y_dict, [swim_str], if_missing_return_None=True) is None

    # WHEN / THEN
    swim_str = "swim"
    x_value = get_from_nested_dict(
        y_dict, [sports_str, swim_str], if_missing_return_None=True
    )
    assert x_value is None

    # WHEN / THEN
    swim_str = "swim"
    x_value = get_from_nested_dict(
        y_dict, [sports_str, swim_str, _2pm_str], if_missing_return_None=True
    )
    assert x_value is None


def test_get_positive_int_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_positive_int(None) == 0
    assert get_positive_int("sports") == 0
    assert get_positive_int() == 0
    assert get_positive_int(10) == 10
    assert get_positive_int(10.0) == 10
    assert get_positive_int(10.8) == 10
    assert get_positive_int(-10.8) == 0


def test_extract_csv_headers_ReturnsObj_empty_list():
    # ESTABLISH
    x_csv = ""

    # WHEN
    x_headers = extract_csv_headers(x_csv)

    # THEN
    assert x_headers == []


def test_extract_csv_headers_ReturnsObj():
    # ESTABLISH
    x_csv = """x_id,y_id,w_id,u_id,z_id
amy,Sue,Bob,13,29
amy,Sue,Sue,11,23
amy,Sue,Yao,41,37
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
amy,Sue,Bob,13,29
amy,Sue,Sue,11,23
amy,Sue,Yao,41,37
"""

    # WHEN
    x_headers, new_csv = extract_csv_headers(x_csv)

    # THEN
    print(f"{new_csv=}")
    headerless_csv = """amy,Sue,Bob,13,29
amy,Sue,Sue,11,23
amy,Sue,Yao,41,37
"""
    assert new_csv == headerless_csv


def test_get_csv_column1_column2_metrics_ReturnsObj_empty_dict():
    # ESTABLISH
    headerless_csv = ""

    # WHEN
    x_dict = get_csv_column1_column2_metrics(headerless_csv=headerless_csv)

    # THEN
    assert x_dict == {}


def test_get_csv_column1_column2_metrics_ReturnsObj_Scenario1():
    # ESTABLISH
    x_id = "amy56"
    y_id = "Yao"
    headerless_csv = f"""{x_id},{y_id},Bob,13,29
"""

    # WHEN
    x_dict = get_csv_column1_column2_metrics(headerless_csv=headerless_csv)

    # THEN
    assert x_dict == {x_id: {y_id: 1}}


def test_get_csv_column1_column2_metrics_ReturnsObj_Scenario2():
    # ESTABLISH
    x_id = "amy56"
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
    x_id = "amy56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f""",,{x_id},{sue_str},Bob,13,29
,,{x_id},{sue_str},Sue,11,23
,,{x_id},{sue_str},Yao,41,37
,,{x_id},{sue_str},Zia,41,37
,,{x_id},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = create_l2nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f""",,{x_id},{sue_str},Bob,13,29
,,{x_id},{sue_str},Sue,11,23
,,{x_id},{sue_str},Yao,41,37
,,{x_id},{sue_str},Zia,41,37
"""
    static_bob_csv = f""",,{x_id},{bob_str},Yao,41,37
"""
    generated_sue_bob_dict = u_dict.get(x_id)
    assert generated_sue_bob_dict
    assert list(generated_sue_bob_dict.keys()) == [sue_str, bob_str]
    generated_bob_csv = generated_sue_bob_dict.get(bob_str)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_sue_bob_dict.get(sue_str)
    assert generated_sue_csv == static_sue_csv
    sue_bob_csv_dict = {sue_str: static_sue_csv, bob_str: static_bob_csv}
    assert u_dict == {x_id: sue_bob_csv_dict}


def test_create_l2nested_csv_dict_ReturnsObj_Scenario1_Multiple1stLevels():
    # ESTABLISH
    amy3_id = "amy3"
    amy4_id = "amy4"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f""",,{amy3_id},{sue_str},Bob,13,29
,,{amy4_id},{sue_str},Sue,11,23
,,{amy4_id},{sue_str},Yao,41,37
,,{amy4_id},{sue_str},Zia,41,37
,,{amy4_id},{bob_str},Yao,41,37
"""

    # WHEN
    tiered_dict = create_l2nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    amy3_sue_csv = f""",,{amy3_id},{sue_str},Bob,13,29
"""
    amy4_sue_csv = f""",,{amy4_id},{sue_str},Sue,11,23
,,{amy4_id},{sue_str},Yao,41,37
,,{amy4_id},{sue_str},Zia,41,37
"""
    static_bob_csv = f""",,{amy4_id},{bob_str},Yao,41,37
"""
    amy3_dict = tiered_dict.get(amy3_id)
    amy4_dict = tiered_dict.get(amy4_id)
    assert amy3_dict
    assert amy4_dict
    assert list(amy3_dict.keys()) == [sue_str]
    assert list(amy4_dict.keys()) == [sue_str, bob_str]
    generated_bob_csv = amy4_dict.get(bob_str)
    assert generated_bob_csv == static_bob_csv
    generated3_sue_csv = amy3_dict.get(sue_str)
    generated4_sue_csv = amy4_dict.get(sue_str)
    print(f"{generated3_sue_csv=}")
    print(f"{generated4_sue_csv=}")
    assert generated3_sue_csv == amy3_sue_csv
    assert generated4_sue_csv == amy4_sue_csv
    people3_csv_dict = {sue_str: amy3_sue_csv}
    people4_csv_dict = {sue_str: amy4_sue_csv, bob_str: static_bob_csv}
    assert tiered_dict == {
        amy3_id: people3_csv_dict,
        amy4_id: people4_csv_dict,
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
    swim_str = "swim"
    six_str = "six"
    seven_str = "seven"
    headers = [swim_str, six_str, seven_str]
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
        == f"""{swim_str},{six_str},{seven_str}
{headerless_csv}"""
    )


def test_is_2d_with_unique_keys_ReturnsObj():
    # ESTABLISH
    casa_str = "casa"
    sue_str = "Sue"

    # WHEN / THEN
    assert is_2d_with_unique_keys({})
    assert is_2d_with_unique_keys({sue_str: {}})
    assert is_2d_with_unique_keys({sue_str: {}, "Bob": {}}) is False
    assert is_2d_with_unique_keys({"swim": 155, sue_str: {}, "Bob": {}}) is False
    assert is_2d_with_unique_keys({"swim": 155, sue_str: {}})
    assert is_2d_with_unique_keys({casa_str: {"clean": "Bob"}})
    assert is_2d_with_unique_keys({casa_str: {"clean": {"Bob": 13}}})
    assert (
        is_2d_with_unique_keys({casa_str: {"clean": {"Bob": 13}, "swim": {}}}) is False
    )
    assert is_2d_with_unique_keys({casa_str: {"clean": {"Bob": 13}}, "school": 14})
    assert (
        is_2d_with_unique_keys(
            {casa_str: {"clean": {"Bob": 3}}, "school": {"clean": 1}}
        )
        is False
    )
    assert is_2d_with_unique_keys({casa_str: {"school": {sue_str: {1: {}}}}})
    assert (
        is_2d_with_unique_keys(
            {casa_str: {"clean": {"Bob": 13}, "school": {"swim": 14}}}
        )
        is False
    )

    # No duplicate keys paired to dictionarys
    assert is_2d_with_unique_keys({casa_str: {"school": {casa_str: {1: {}}}}}) is False

    # No duplicate keys off levels
    assert is_2d_with_unique_keys({casa_str: {"school": {casa_str: {1: {}}}}}) is False
    assert is_2d_with_unique_keys({casa_str: {"school": {casa_str: 1}}}) is False


def test_get_nested_dict_keys_by_level_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"

    #  WHEN / THEN
    assert get_nested_dict_keys_by_level({}) == {}
    assert get_nested_dict_keys_by_level({sue_str: {}}) == {0: {sue_str}}
    x2_dict = {sue_str: {}, bob_str: {}}
    assert get_nested_dict_keys_by_level(x2_dict) == {0: {sue_str, bob_str}}
    x3_dict = {"swim": 155, sue_str: {}, bob_str: {}}
    assert get_nested_dict_keys_by_level(x3_dict) == {0: {sue_str, bob_str}}
    x4_dict = {"swim": 155, sue_str: {"zia": {}}, bob_str: {"yao": {}}}
    assert get_nested_dict_keys_by_level(x4_dict) == {
        0: {sue_str, bob_str},
        1: {"zia", "yao"},
    }


def test_get_nested_keys_by_level_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "yao"
    swim_str = "Swim"

    #  WHEN / THEN
    assert get_nested_keys_by_level({}) == {}
    assert get_nested_keys_by_level({sue_str: 1}) == {0: {sue_str}}
    assert get_nested_keys_by_level({sue_str: {}}) == {0: {sue_str}}
    x2_dict = {sue_str: {}, bob_str: {}}
    assert get_nested_keys_by_level(x2_dict) == {0: {sue_str, bob_str}}
    x3_dict = {swim_str: 155, sue_str: {}, bob_str: {}}
    assert get_nested_keys_by_level(x3_dict) == {0: {swim_str, sue_str, bob_str}}
    x4_dict = {swim_str: 155, sue_str: {"zia": {}}, bob_str: {yao_str: {swim_str: 1}}}
    assert get_nested_keys_by_level(x4_dict) == {
        0: {sue_str, bob_str, swim_str},
        1: {"zia", yao_str},
        2: {swim_str},
    }


def test_get_nested_non_dict_keys_by_level_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "yao"
    swim_str = "Swim"

    #  WHEN / THEN
    assert get_nested_non_dict_keys_by_level({}) == {}
    assert get_nested_non_dict_keys_by_level({sue_str: 1}) == {0: {sue_str}}
    assert get_nested_non_dict_keys_by_level({sue_str: {}}) == {0: set()}
    x2_dict = {sue_str: {}, bob_str: {}}
    assert get_nested_non_dict_keys_by_level(x2_dict) == {0: set()}
    x3_dict = {swim_str: 155, sue_str: {}, bob_str: {}}
    assert get_nested_non_dict_keys_by_level(x3_dict) == {0: {swim_str}}
    x4_dict = {swim_str: 155, sue_str: {"zia": {}}, bob_str: {yao_str: {swim_str: 1}}}
    assert get_nested_non_dict_keys_by_level(x4_dict) == {
        0: {swim_str},
        1: set(),
        2: {swim_str},
    }


def test_get_nested_non_dict_keys_list_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "yao"
    swim_str = "Swim"
    run_str = "Run"

    #  WHEN / THEN
    assert get_nested_non_dict_keys_list({}) == []
    assert get_nested_non_dict_keys_list({sue_str: 1}) == [sue_str]
    assert get_nested_non_dict_keys_list({sue_str: {}}) == []
    x2_dict = {sue_str: {}, bob_str: {}}
    assert get_nested_non_dict_keys_list(x2_dict) == []
    x3_dict = {swim_str: 155, sue_str: {}, bob_str: {}}
    assert get_nested_non_dict_keys_list(x3_dict) == [swim_str]
    x4_dict = {swim_str: 155, sue_str: {"zia": {}}, bob_str: {yao_str: {run_str: 1}}}
    assert get_nested_non_dict_keys_list(x4_dict) == [swim_str, run_str]
    x5_dict = {"casa": {"clean": {"Bob": 13}}, "school": 14}
    assert get_nested_non_dict_keys_list(x5_dict) == ["school", "Bob"]


def test_get_nested_dict_key_by_level_RaisesError_is_2d_with_unique_keys_IsFalse():
    # ESTABLISH / WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        get_nested_dict_key_by_level({"Sue": {}, "Bob": {}})
    exception_str = "dictionary is not 2d_with_unique_keys."
    assert str(excinfo.value) == exception_str


def test_get_nested_dict_key_by_level_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"

    #  WHEN / THEN
    assert get_nested_dict_key_by_level({}) == []
    assert get_nested_dict_key_by_level({"Sue": {}}) == [sue_str]
    x4_dict = {"swim": 155, sue_str: {bob_str: {"yao": {}}}}
    assert get_nested_dict_key_by_level(x4_dict) == [sue_str, bob_str, "yao"]


def test_create_2d_array_from_dict_RaisesError_is_2d_with_unique_keys_IsFalse():
    # ESTABLISH / WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_2d_array_from_dict({"Sue": {}, "Bob": {}})
    exception_str = "dictionary is not 2d_with_unique_keys."
    assert str(excinfo.value) == exception_str


def test_create_2d_array_from_dict_ReturnsObj_Scenario0_Simple():
    # ESTABLISH
    sue_str = "Sue"
    x1_int = 1

    # WHEN / THEN
    assert create_2d_array_from_dict({}) == [[], []]
    assert create_2d_array_from_dict({sue_str: x1_int}) == [[sue_str], [x1_int]]
    assert create_2d_array_from_dict({sue_str: {}}) == [[], []]
    x0_2d_array = [["swim"], [155]]
    assert create_2d_array_from_dict({"swim": 155, sue_str: {}}) == x0_2d_array
    x1_2d_array = [["clean"], ["Bob"]]
    assert create_2d_array_from_dict({"casa": {"clean": "Bob"}}) == x1_2d_array
    x2_2d_array = [["Bob"], [13]]
    assert create_2d_array_from_dict({"casa": {"clean": {"Bob": 13}}}) == x2_2d_array
    x2_2d_dict = {"casa": {"clean": {"Bob": 13}}, "school": 14}
    x2_2d_array = [["school", "Bob"], [14, 13]]
    assert create_2d_array_from_dict(x2_2d_dict) == x2_2d_array


def test_str_in_dict_keys_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_dict_keys("", {}) is False
    assert str_in_dict_keys("", {"": "Sue"})
    assert str_in_dict_keys("", {"Sue": "Sue"})
    assert str_in_dict_keys("Sue", {"Sue": "Bob"})
    assert str_in_dict_keys("Sue", {"Zia": "Bob"}) is False
    assert str_in_dict_keys("Sue", {"SueAndZia": "Bob"})
    assert str_in_dict_keys("Sue", {"Zia": "Bob"}) is False
    assert str_in_dict_keys("Sue", {"Bob": "SueAndZia"}) is False
    assert str_in_dict_keys("Sue", {"Bob": "Zia"}) is False


def test_str_in_dict_values_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_dict_values("", {}) is False
    assert str_in_dict_values("", {"": "Sue"})
    assert str_in_dict_values("", {"Sue": "Sue"})
    assert str_in_dict_values("Sue", {"Sue": "Bob"}) is False
    assert str_in_dict_values("Sue", {"Zia": "Bob"}) is False
    assert str_in_dict_values("Sue", {"SueAndZia": "Bob"}) is False
    assert str_in_dict_values("Sue", {"Zia": "Bob"}) is False
    assert str_in_dict_values("Sue", {"Bob": "SueAndZia"})
    assert str_in_dict_values("Sue", {"Bob": "Zia"}) is False


def test_str_in_dict_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_dict("", {}) is False
    assert str_in_dict("", {"": "Sue"})
    assert str_in_dict("", {"Sue": "Sue"})
    assert str_in_dict("Sue", {"Sue": "Bob"})
    assert str_in_dict("Sue", {"Zia": "Bob"}) is False
    assert str_in_dict("Sue", {"SueAndZia": "Bob"})
    assert str_in_dict("Sue", {"Zia": "Bob"}) is False
    assert str_in_dict("Sue", {"Bob": "SueAndZia"})
    assert str_in_dict("Sue", {"Bob": "Zia"}) is False


def test_get_str_in_sub_dict_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_str_in_sub_dict("", {}) == {}
    assert get_str_in_sub_dict("", {"": "Sue"}) == {"": "Sue"}
    assert get_str_in_sub_dict("", {"Sue": "Sue"}) == {"Sue": "Sue"}
    assert get_str_in_sub_dict("Sue", {"Sue": "Bob"}) == {"Sue": "Bob"}
    assert get_str_in_sub_dict("Sue", {"Zia": "Bob"}) == {}
    assert get_str_in_sub_dict("Sue", {"SueAndZia": "Bob"}) == {"SueAndZia": "Bob"}
    assert get_str_in_sub_dict("Sue", {"Zia": "Bob"}) == {}
    assert get_str_in_sub_dict("Sue", {"Bob": "SueAndZia"}) == {"Bob": "SueAndZia"}
    assert get_str_in_sub_dict("Sue", {"Bob": "Zia"}) == {}

    xio_sue_dict = {"Xio": "Xio", "Sue": "Bob"}
    assert get_str_in_sub_dict("Sue", xio_sue_dict) == {"Sue": "Bob"}
    xio_sueandzia_dict = {"Xio": "Xio", "SueAndZia": "Bob"}
    assert get_str_in_sub_dict("Sue", xio_sueandzia_dict) == {"SueAndZia": "Bob"}
    xio_bob_dict = {"Xio": "Xio", "Bob": "SueAndZia"}
    assert get_str_in_sub_dict("Sue", xio_bob_dict) == {"Bob": "SueAndZia"}


def test_str_in_all_dict_keys_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_all_dict_keys("", {})
    assert str_in_all_dict_keys("", {"": "Sue"})
    assert str_in_all_dict_keys("", {"Sue": "Sue"})
    assert str_in_all_dict_keys("Sue", {"Bob": "Sue"}) is False
    assert str_in_all_dict_keys("Sue", {"Sue": "Zia", "Bob": "Bob"}) is False
    assert str_in_all_dict_keys("Sue", {"Zia": "Bob", "SueAndZia": "Bob"}) is False
    assert str_in_all_dict_keys("Sue", {"Sue": "Bob", "SueAndZia": ""})
    assert str_in_all_dict_keys("Sue", {"Bob": "Zia"}) is False


def test_str_in_all_dict_values_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_all_dict_values("", {})
    assert str_in_all_dict_values("", {"": "Sue"})
    assert str_in_all_dict_values("", {"Sue": "Sue"})
    assert str_in_all_dict_values("Sue", {"Bob": "Sue"})
    assert str_in_all_dict_values("Sue", {"Zia": "Sue", "Sue": "Bob"}) is False
    assert str_in_all_dict_values("Sue", {"Zia": "Sue", "SueAndZia": "Bob"}) is False
    assert str_in_all_dict_values("Sue", {"Zia": "Sue", "Bob": "SueAndZia"})
    assert str_in_all_dict_values("Sue", {"Bob": "Zia"}) is False


def test_str_in_all_dict_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_all_dict("", {})
    assert str_in_all_dict("", {"": "Sue"})
    assert str_in_all_dict("", {"Sue": "Sue"})
    assert str_in_all_dict("Sue", {"Sue": "Bob"}) is False
    assert str_in_all_dict("Sue", {"Zia": "Sue", "Sue": "Bob"}) is False
    assert str_in_all_dict("Sue", {"Sue": "Sue", "SueZia": "SueBob"})
    assert str_in_all_dict("Sue", {"Zia": "Sue", "SueZia": "SueZia"}) is False
    assert str_in_all_dict("Sue", {"Bob": "Zia"}) is False


def test_get_str_not_in_sub_dict_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_str_in_all_sub_dict("", {}) == {}
    assert get_str_in_all_sub_dict("", {"": "Sue"}) == {}
    assert get_str_in_all_sub_dict("", {"Sue": "Sue"}) == {}
    assert get_str_in_all_sub_dict("Sue", {"Sue": "Bob"}) == {"Sue": "Bob"}
    assert get_str_in_all_sub_dict("Sue", {"Zia": "Bob"}) == {"Zia": "Bob"}
    assert get_str_in_all_sub_dict("Sue", {"Sue": "SueAndZia"}) == {}
    assert get_str_in_all_sub_dict("Sue", {"SueAndZia": "Bob"}) == {"SueAndZia": "Bob"}
    assert get_str_in_all_sub_dict("Sue", {"Zia": "Bob"}) == {"Zia": "Bob"}
    x_dict = {"Bob": "SueZia", "Sue": "Sue"}
    assert get_str_in_all_sub_dict("Sue", x_dict) == {"Bob": "SueZia"}
    assert get_str_in_all_sub_dict("Sue", {"Bob": "Zia"}) == {"Bob": "Zia"}

    suezia_sue_dict = {"SueZia": "SueZia", "Sue": "Bob"}
    assert get_str_in_all_sub_dict("Sue", suezia_sue_dict) == {"Sue": "Bob"}
    suezia_sueandzia_dict = {"SueZia": "SueZia", "SueAndZia": "Bob"}
    assert get_str_in_all_sub_dict("Sue", suezia_sueandzia_dict) == {"SueAndZia": "Bob"}
    suezia_bob_dict = {"SueZia": "SueZia", "Bob": "SueAndZia"}
    assert get_str_in_all_sub_dict("Sue", suezia_bob_dict) == {"Bob": "SueAndZia"}


def test_get_sorted_list_of_dict_keys_ReturnsObj_WhenEmptyDict():
    # ESTABLISH / WHEN / THEN
    assert get_sorted_list_of_dict_keys({}, "age") == []


def test_get_sorted_list_of_dict_keys_ReturnsObj_WhenValues():
    # ESTABLISH
    x_dict = {
        "Sue": {"name": "Sue", "age": 55, "city": "NYC"},
        "Bob": {"name": "Bob", "age": 30, "city": "Dallas"},
        "Yao": {"name": "Yao", "age": 35, "city": "Paris"},
    }

    # WHEN
    x_list = get_sorted_list_of_dict_keys(x_dict, "age")

    # THEN
    assert x_list == ["Bob", "Yao", "Sue"]


def test_get_sorted_list_of_dict_keys_ReturnsObj_WithValues():
    # ESTABLISH
    x_dict = {
        "Sue": {"name": "Sue", "age": 55, "city": "NYC"},
        "Bob": {"name": "Bob", "age": 30, "city": "Dallas"},
        "Yao": {"name": "Yao", "age": 35, "city": "Paris"},
    }

    # WHEN
    x_list = get_sorted_list_of_dict_keys(x_dict, "age", include_sort_values=True)

    # THEN
    assert x_list == [["Bob", 30], ["Yao", 35], ["Sue", 55]]


def test_get_max_key_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    x_dict = {}
    # WHEN / THEN
    assert not get_max_key(x_dict)


def test_get_max_key_ReturnsObj_Scenario1_Simple():
    x_dict = {
        (1, "b", 3, "z"): 2.5,
        (1, "a", 2, "x"): 3.4,
        (3, "c", 5, "w"): 1.8,
    }
    # WHEN / THEN
    assert get_max_key(x_dict) == (1, "a", 2, "x")


def test_get_max_key_ReturnsObj_Scenario2_TupleOrdering():
    x_dict = {
        (1, "b", 3, "z"): 2.5,
        (2, "a", 1, "y"): 3.4,
        (1, "a", 2, "x"): 3.4,
        (3, "c", 5, "w"): 1.8,
    }
    # WHEN / THEN
    assert get_max_key(x_dict) == (1, "a", 2, "x")


def test_change_nested_key_Scenario0():
    d = {"a": {"b": {"c": 123}}}
    expected = {"a": {"b": {"new_c": 123}}}
    result = change_nested_key(copy_deepcopy(d), ["a", "b", "c"], "new_c")
    assert result == expected


def test_change_nested_key_Scenario1():
    d = {"old": "value"}
    expected = {"new": "value"}
    result = change_nested_key(copy_deepcopy(d), ["old"], "new")
    assert result == expected


def test_change_nested_key_Scenario2():
    d = {"a": {"b": {"c": 123}}}
    original = copy_deepcopy(d)
    result = change_nested_key(d, ["a", "b", "missing_key"], "new_key")
    # Should be unchanged
    assert result == original


def test_change_nested_key_Scenario3():
    d = {"x": {"y": {"z": {"target": "val"}}}}
    expected = {"x": {"y": {"z": {"renamed": "val"}}}}
    result = change_nested_key(copy_deepcopy(d), ["x", "y", "z", "target"], "renamed")
    assert result == expected


def test_change_nested_key_Scenario4():
    d = {"a": {"b": 123}}
    original = copy_deepcopy(d)
    result = change_nested_key(d, ["a", "b", "c"], "d")
    # Should not raise error, but should not modify
    assert result == original
