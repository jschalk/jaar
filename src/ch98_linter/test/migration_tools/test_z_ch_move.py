from ch98_linter.ch_move1 import replace_valid_ch
from copy import deepcopy as copy_deepcopy


def test_replace_valid_ch_ReplacesValue_Scenario0_ExactMatch():
    # GIVEN
    data = {
        "Example": {"valid_ch": "19"},
        "Other": {"valid_ch": "13:"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result["Example"]["valid_ch"] == "23"
    assert result["Other"]["valid_ch"] == "13:"


def test_replace_valid_ch_DoesNotReplace_Scenario1_PartialMatch():
    # GIVEN
    data = {
        "Example": {"valid_ch": "19:"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result["Example"]["valid_ch"] == "23:"


def test_replace_valid_ch_ReplacesMultiple_Scenario2_MultipleExactMatches():
    # GIVEN
    data = {
        "A": {"valid_ch": "19"},
        "B": {"valid_ch": "19"},
        "C": {"valid_ch": "20"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result["A"]["valid_ch"] == "23"
    assert result["B"]["valid_ch"] == "23"
    assert result["C"]["valid_ch"] == "20"


def test_replace_valid_ch_DoesNothing_Scenario3_NoMatches():
    # GIVEN
    data = {
        "A": {"valid_ch": "11"},
        "B": {"valid_ch": "12"},
    }

    original_data = copy_deepcopy(data)

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result == original_data


def test_replace_valid_ch_SkipsMissingValidCh_Scenario4_KeyMissing():
    # GIVEN
    data = {
        "A": {"semantic_type": "str"},
        "B": {"valid_ch": "19"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result["A"] == {"semantic_type": "str"}
    assert result["B"]["valid_ch"] == "23"


def test_replace_valid_ch_ReturnsSameObject_Scenario5_MutatesInput():
    # GIVEN
    data = {
        "A": {"valid_ch": "19"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result is data
