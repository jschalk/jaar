from ch98_linter.style import find_matching_tests


def test_find_matching_tests_ReturnsObj_Scenario0_MatchesAnyFunctionNameWithSameScenario():
    # ESTABLISH
    tests = {
        "test_alpha_ReturnsObj_Scenario1_valid",
        "test_alpha_ReturnsObj_Scenario1_invalid",
        "test_beta_ReturnsObj_Scenario1_valid",  # different func → ignore
        "test_alpha_ReturnsObj_Scenario2_valid",  # single → ignore
    }
    # WHEN
    result = find_matching_tests(tests)
    # THEN
    assert set(result) == {
        "test_alpha_ReturnsObj_Scenario1_valid",
        "test_alpha_ReturnsObj_Scenario1_invalid",
    }


def test_find_matching_tests_ReturnsObj_Scenario1_SeparatesDifferentFunctionsSameScenario():
    # ESTABLISH
    tests = {
        "test_alpha_ReturnsObj_Scenario1_a",
        "test_alpha_ReturnsObj_Scenario1_b",
        "test_beta_ReturnsObj_Scenario1_a",
        "test_beta_ReturnsObj_Scenario1_b",
    }
    # WHEN
    result = find_matching_tests(tests)
    # THEN
    assert set(result) == {
        "test_alpha_ReturnsObj_Scenario1_a",
        "test_alpha_ReturnsObj_Scenario1_b",
        "test_beta_ReturnsObj_Scenario1_a",
        "test_beta_ReturnsObj_Scenario1_b",
    }


def test_find_matching_tests_ReturnsObj_Scenario2_IgnoresNonr_returns_objTests():
    # ESTABLISH
    tests = {
        "test_alpha_Scenario1_a",
        "test_alpha_Scenario1_b",
    }
    # WHEN
    result = find_matching_tests(tests)
    # THEN
    assert result == []


def test_find_matching_tests_ReturnsObj_Scenario3_IgnoresMissingScenario():
    # ESTABLISH
    tests = {
        "test_alpha_ReturnsObj_valid",
        "test_alpha_ReturnsObj_invalid",
    }
    # WHEN
    result = find_matching_tests(tests)
    # THEN
    assert result == []


def test_find_matching_tests_ReturnsObj_Scenario4_RequiresDuplicatesPerFunctionAndScenario():
    # ESTABLISH
    tests = {
        "test_alpha_ReturnsObj_Scenario1_a",
        "test_beta_ReturnsObj_Scenario1_a",
    }
    # WHEN
    result = find_matching_tests(tests)
    # THEN
    assert result == []


def test_find_matching_tests_ReturnsObj_Scenario5_multiple_valid_groups():
    # ESTABLISH
    tests = {
        "test_alpha_ReturnsObj_Scenario1_a",
        "test_alpha_ReturnsObj_Scenario1_b",
        "test_alpha_ReturnsObj_Scenario2_a",
        "test_alpha_ReturnsObj_Scenario2_b",
        "test_beta_ReturnsObj_Scenario1_a",
        "test_beta_ReturnsObj_Scenario1_b",
    }
    # WHEN
    result = find_matching_tests(tests)
    # THEN
    assert set(result) == tests
