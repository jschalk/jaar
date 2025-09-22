from src.ch01_data_toolbox.dict_toolbox import make_dict_safe_for_json


def test_make_dict_safe_for_json_ScenarioSimpleDict():
    # ESTABLISH
    obj = {"a": 1, "b": 2}
    expected = {"a": 1, "b": 2}
    # WHEN / THEN
    assert make_dict_safe_for_json(obj) == expected


def test_make_dict_safe_for_json_ScenarioNestedDict():
    # ESTABLISH
    obj = {"a": {"b": {"c": 3}}}
    expected = {"a": {"b": {"c": 3}}}
    # WHEN / THEN
    assert make_dict_safe_for_json(obj) == expected


def test_make_dict_safe_for_json_ScenarioListInsideDict():
    # ESTABLISH
    obj = {"a": [1, 2, {"b": 3}]}
    expected = {"a": [1, 2, {"b": 3}]}
    # WHEN / THEN
    assert make_dict_safe_for_json(obj) == expected


def test_make_dict_safe_for_json_ScenarioSetConversion():
    # ESTABLISH
    obj = {"a": {1, 2, 3}}
    # WHEN
    result = make_dict_safe_for_json(obj)
    # THEN
    assert isinstance(result["a"], list)
    assert sorted(result["a"]) == [1, 2, 3]


def test_make_dict_safe_for_json_ScenarioListOfSets():
    # ESTABLISH
    obj = [{"x": {1, 2}}, {"y": {3, 4}}]
    # WHEN
    result = make_dict_safe_for_json(obj)
    # THEN
    assert isinstance(result[0]["x"], list)
    assert sorted(result[0]["x"]) == [1, 2]
    assert sorted(result[1]["y"]) == [3, 4]


def test_make_dict_safe_for_json_ScenarioScalarValues():
    # ESTABLISH / WHEN / THEN
    assert make_dict_safe_for_json(42) == 42
    assert make_dict_safe_for_json("hello") == "hello"
    assert make_dict_safe_for_json(3.14) == 3.14
    assert make_dict_safe_for_json(True) is True
    assert make_dict_safe_for_json(None) is None


def test_make_dict_safe_for_json_ScenarioEmptyContainers():
    # ESTABLISH / WHEN / THEN
    assert make_dict_safe_for_json({}) == {}
    assert make_dict_safe_for_json([]) == []
    assert make_dict_safe_for_json(set()) == []


def test_make_dict_safe_for_json_ScenarioDictWithSetKeys():
    # ESTABLISH
    obj = {frozenset([1, 2]): "value"}
    # WHEN
    result = make_dict_safe_for_json(obj)
    # THEN
    assert list(result.keys())[0] == frozenset([1, 2])
    assert result[frozenset([1, 2])] == "value"
