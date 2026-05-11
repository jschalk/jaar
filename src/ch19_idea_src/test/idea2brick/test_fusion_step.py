from ch19_idea_src.fusion_step import (
    fusion_add_ancestor_rope_rows,
    fusion_add_knot_from_rope,
    fusion_set_moment_rope_from_moment_label,
    fusion_set_plan_rope_from_health_label,
    fusion_set_pledge_to_one,
)
from pandas import DataFrame as pandas_DataFrame, testing as pandas_testing
from pytest import raises as pytest_raises


def make_df(**kwargs):
    return pandas_DataFrame({**kwargs})


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario01_AddsAllAncestorsForSingleRope():
    # ESTABLISH
    df = make_df(
        plan_rope=[";mmt01;sports;play soccer;"], pledge=[1], person_name=["Alice"]
    )
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    ropes = set(result["plan_rope"])
    assert ";mmt01;" in ropes
    assert ";mmt01;sports;" in ropes
    assert ";mmt01;sports;play soccer;" in ropes


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario02_AncestorRowsHavePledgeZero():
    # ESTABLISH
    df = make_df(
        plan_rope=[";mmt01;sports;play soccer;"], pledge=[1], person_name=["Alice"]
    )
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    ancestors = result[result["plan_rope"] != ";mmt01;sports;play soccer;"]
    assert (ancestors["pledge"] == 0).all()


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario03_OriginalRowPledgeUnchanged():
    # ESTABLISH
    df = make_df(
        plan_rope=[";mmt01;sports;play soccer;"], pledge=[1], person_name=["Alice"]
    )
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    original = result[result["plan_rope"] == ";mmt01;sports;play soccer;"]
    assert original["pledge"].iloc[0] == 1


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario04_NoDuplicateAncestorsAcrossRows():
    # ESTABLISH
    df = make_df(
        plan_rope=[";mmt01;sports;play soccer;", ";mmt01;sports;climb;"],
        pledge=[1, 1],
        person_name=["Alice", "Bob"],
    )
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    assert result["plan_rope"].value_counts()[";mmt01;"] == 1
    assert result["plan_rope"].value_counts()[";mmt01;sports;"] == 1


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario05_ExistingAncestorNotDuplicated():
    # ESTABLISH
    df = make_df(
        plan_rope=[";mmt01;sports;play soccer;", ";mmt01;sports;", ";mmt01;"],
        pledge=[1, 1, 1],
        person_name=["Alice", "Bob", "Carol"],
    )
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    assert result["plan_rope"].value_counts()[";mmt01;sports;"] == 1
    assert result["plan_rope"].value_counts()[";mmt01;"] == 1


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario06_NoPlanRopeColumnReturnsUnchanged():
    # ESTABLISH
    df = make_df(pledge=[1], person_name=["Alice"])
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    pandas_testing.assert_frame_equal(result, df)


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario07_NullRopeValuesSkipped():
    # ESTABLISH
    df = make_df(
        plan_rope=[None, ";mmt01;sports;"], pledge=[1, 1], person_name=["Alice", "Bob"]
    )
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    assert len(result[result["plan_rope"] == ";mmt01;"]) == 1


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario08_SingleSegmentRopeAddsNoAncestors():
    # ESTABLISH
    df = make_df(plan_rope=[";mmt01;"], pledge=[1], person_name=["Alice"])
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    assert len(result) == 1


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario09_OtherColumnsAreCopiedToAncestorRows():
    # ESTABLISH
    df = make_df(
        plan_rope=[";mmt01;sports;play soccer;"], pledge=[1], person_name=["Alice"]
    )
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    ancestors = result[result["plan_rope"] != ";mmt01;sports;play soccer;"]
    assert (ancestors["person_name"] == "Alice").all()


def test_fusion_add_ancestor_rope_rows_ReturnsDf_Scenario10_EmptyDataframeReturnsEmpty():
    # ESTABLISH
    df = pandas_DataFrame(columns=["plan_rope", "pledge", "person_name"])
    # WHEN
    result = fusion_add_ancestor_rope_rows(df, {})
    # THEN
    assert len(result) == 0
    assert list(result.columns) == ["plan_rope", "pledge", "person_name"]


def test_fusion_set_pledge_to_one_ReturnsDf_Scenario01_AddsPledgeColumnWhenAbsent():
    # ESTABLISH
    df = make_df(person_name=["Alice", "Bob"])
    # WHEN
    result = fusion_set_pledge_to_one(df, {})
    # THEN
    assert "pledge" in result.columns


def test_fusion_set_pledge_to_one_ReturnsDf_Scenario02_SetsPledgeToOneWhenColumnAbsent():
    # ESTABLISH
    df = make_df(person_name=["Alice", "Bob"])
    # WHEN
    result = fusion_set_pledge_to_one(df, {})
    # THEN
    assert (result["pledge"] == 1).all()


def test_fusion_set_pledge_to_one_ReturnsDf_Scenario03_OverwritesExistingPledgeValues():
    # ESTABLISH
    df = make_df(person_name=["Alice", "Bob"], pledge=[0, 99])
    # WHEN
    result = fusion_set_pledge_to_one(df, {})
    # THEN
    assert (result["pledge"] == 1).all()


def test_fusion_set_pledge_to_one_ReturnsDf_Scenario04_OtherColumnsUnchanged():
    # ESTABLISH
    df = make_df(person_name=["Alice", "Bob"], pledge=[0, 0])
    # WHEN
    result = fusion_set_pledge_to_one(df, {})
    # THEN
    assert list(result["person_name"]) == ["Alice", "Bob"]


def test_fusion_set_pledge_to_one_ReturnsDf_Scenario05_DoesNotMutateInputDf():
    # ESTABLISH
    df = make_df(person_name=["Alice"], pledge=[0])
    # WHEN
    fusion_set_pledge_to_one(df, {})
    # THEN
    assert df["pledge"].iloc[0] == 0


def test_fusion_set_pledge_to_one_ReturnsDf_Scenario06_EmptyDataframeReturnsPledgeColumn():
    # ESTABLISH
    df = pandas_DataFrame(columns=["person_name"])
    # WHEN
    result = fusion_set_pledge_to_one(df, {})
    # THEN
    assert "pledge" in result.columns
    assert len(result) == 0


def test_fusion_set_plan_rope_from_health_label_ReturnsDf_Scenario01_BuildsCorrectPlanRope():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"], health_label=["cardio"])
    # WHEN
    result = fusion_set_plan_rope_from_health_label(df, {})
    # THEN
    assert result["plan_rope"].iloc[0] == ";mmt01;sports;health;cardio;"


def test_fusion_set_plan_rope_from_health_label_ReturnsDf_Scenario02_MultipleRowsAllCorrect():
    # ESTABLISH
    df = make_df(
        moment_rope=[";mmt01;sports;", ";mmt01;rest;"], health_label=["cardio", "sleep"]
    )
    # WHEN
    result = fusion_set_plan_rope_from_health_label(df, {})
    # THEN
    assert result["plan_rope"].iloc[0] == ";mmt01;sports;health;cardio;"
    assert result["plan_rope"].iloc[1] == ";mmt01;rest;health;sleep;"


def test_fusion_set_plan_rope_from_health_label_ReturnsDf_Scenario03_DoesNotMutateInputDf():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"], health_label=["cardio"])
    # WHEN
    fusion_set_plan_rope_from_health_label(df, {})
    # THEN
    assert "plan_rope" not in df.columns


def test_fusion_set_plan_rope_from_health_label_ReturnsDf_Scenario04_OtherColumnsUnchanged():
    # ESTABLISH
    df = make_df(
        moment_rope=[";mmt01;sports;"], health_label=["cardio"], person_name=["Alice"]
    )
    # WHEN
    result = fusion_set_plan_rope_from_health_label(df, {})
    # THEN
    assert result["person_name"].iloc[0] == "Alice"


def test_fusion_set_plan_rope_from_health_label_RaisesValueError_Scenario05_MissingMomentRopeColumn():
    # ESTABLISH
    df = make_df(health_label=["cardio"])
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_rope"):
        fusion_set_plan_rope_from_health_label(df, {})


def test_fusion_set_plan_rope_from_health_label_RaisesValueError_Scenario06_MissingHealthLabelColumn():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"])
    # WHEN / THEN
    with pytest_raises(ValueError, match="health_label"):
        fusion_set_plan_rope_from_health_label(df, {})


def test_fusion_set_plan_rope_from_health_label_RaisesValueError_Scenario07_NullMomentRopeValue():
    # ESTABLISH
    df = make_df(
        moment_rope=[None, ";mmt01;sports;"], health_label=["cardio", "cardio"]
    )
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_rope.*indices.*\\[0\\]"):
        fusion_set_plan_rope_from_health_label(df, {})


def test_fusion_set_plan_rope_from_health_label_RaisesValueError_Scenario08_NullHealthLabelValue():
    # ESTABLISH
    df = make_df(
        moment_rope=[";mmt01;sports;", ";mmt01;rest;"], health_label=["cardio", None]
    )
    # WHEN / THEN
    with pytest_raises(ValueError, match="health_label.*indices.*\\[1\\]"):
        fusion_set_plan_rope_from_health_label(df, {})


def test_fusion_set_moment_rope_from_moment_label_ReturnsDf_Scenario01_BuildsCorrectMomentRope():
    # ESTABLISH
    df = make_df(moment_label=["sports"])
    # WHEN
    result = fusion_set_moment_rope_from_moment_label(df, {})
    # THEN
    assert result["moment_rope"].iloc[0] == ";sports;"


def test_fusion_set_moment_rope_from_moment_label_ReturnsDf_Scenario02_MultipleRowsAllCorrect():
    # ESTABLISH
    df = make_df(moment_label=["sports", "rest", "work"])
    # WHEN
    result = fusion_set_moment_rope_from_moment_label(df, {})
    # THEN
    assert result["moment_rope"].iloc[0] == ";sports;"
    assert result["moment_rope"].iloc[1] == ";rest;"
    assert result["moment_rope"].iloc[2] == ";work;"


def test_fusion_set_moment_rope_from_moment_label_ReturnsDf_Scenario03_DoesNotMutateInputDf():
    # ESTABLISH
    df = make_df(moment_label=["sports"])
    # WHEN
    fusion_set_moment_rope_from_moment_label(df, {})
    # THEN
    assert "moment_rope" not in df.columns


def test_fusion_set_moment_rope_from_moment_label_ReturnsDf_Scenario04_OtherColumnsUnchanged():
    # ESTABLISH
    df = make_df(moment_label=["sports"], person_name=["Alice"])
    # WHEN
    result = fusion_set_moment_rope_from_moment_label(df, {})
    # THEN
    assert result["person_name"].iloc[0] == "Alice"


def test_fusion_set_moment_rope_from_moment_label_ReturnsDf_Scenario05_OverwritesExistingMomentRope():
    # ESTABLISH
    df = make_df(moment_label=["sports"], moment_rope=[";old_value;"])
    # WHEN
    result = fusion_set_moment_rope_from_moment_label(df, {})
    # THEN
    assert result["moment_rope"].iloc[0] == ";sports;"


def test_fusion_set_moment_rope_from_moment_label_RaisesValueError_Scenario06_MissingMomentLabelColumn():
    # ESTABLISH
    df = make_df(person_name=["Alice"])
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_label"):
        fusion_set_moment_rope_from_moment_label(df, {})


def test_fusion_set_moment_rope_from_moment_label_RaisesValueError_Scenario07_NullMomentLabelValue():
    # ESTABLISH
    df = make_df(moment_label=[None, "sports"])
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_label.*indices.*\\[0\\]"):
        fusion_set_moment_rope_from_moment_label(df, {})


def test_fusion_set_moment_rope_from_moment_label_RaisesValueError_Scenario08_MultipleNullMomentLabelValues():
    # ESTABLISH
    df = make_df(moment_label=[None, "sports", None])
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_label.*indices.*\\[0, 2\\]"):
        fusion_set_moment_rope_from_moment_label(df, {})


def test_fusion_add_knot_from_rope_ReturnsDf_Scenario01_SetsDefaultKnotWhenNoRopeColumns():
    # ESTABLISH
    df = make_df(person_name=["Alice"])
    # WHEN
    result = fusion_add_knot_from_rope(df, {})
    # THEN
    assert result["knot"].iloc[0] == ";"


def test_fusion_add_knot_from_rope_ReturnsDf_Scenario02_InfersKnotFromMomentRope():
    # ESTABLISH
    df = make_df(moment_rope=["|mmt01|sports|"])
    # WHEN
    result = fusion_add_knot_from_rope(df, {})
    # THEN
    assert result["knot"].iloc[0] == "|"


def test_fusion_add_knot_from_rope_ReturnsDf_Scenario03_InfersKnotFromPlanRopeWhenNoMomentRope():
    # ESTABLISH
    df = make_df(plan_rope=["|mmt01|sports|health|cardio|"])
    # WHEN
    result = fusion_add_knot_from_rope(df, {})
    # THEN
    assert result["knot"].iloc[0] == "|"


def test_fusion_add_knot_from_rope_ReturnsDf_Scenario04_MomentRopeTakesPriorityOverPlanRope():
    # ESTABLISH
    df = make_df(
        moment_rope=["|mmt01|sports|"], plan_rope=[";mmt01;sports;health;cardio;"]
    )
    # WHEN
    result = fusion_add_knot_from_rope(df, {})
    # THEN
    assert result["knot"].iloc[0] == "|"


def test_fusion_add_knot_from_rope_ReturnsDf_Scenario05_ReturnsUnchangedWhenKnotAlreadyExists():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"], knot=["!"])
    # WHEN
    result = fusion_add_knot_from_rope(df, {})
    # THEN
    assert result["knot"].iloc[0] == "!"


def test_fusion_add_knot_from_rope_ReturnsDf_Scenario06_SkipsNullMomentRopeFallsBackToPlanRope():
    # ESTABLISH
    df = make_df(moment_rope=[None], plan_rope=["|mmt01|sports|"])
    # WHEN
    result = fusion_add_knot_from_rope(df, {})
    # THEN
    assert result["knot"].iloc[0] == "|"


def test_fusion_add_knot_from_rope_ReturnsDf_Scenario07_SetsDefaultKnotWhenAllRopeValuesNull():
    # ESTABLISH
    df = make_df(moment_rope=[None], plan_rope=[None])
    # WHEN
    result = fusion_add_knot_from_rope(df, {})
    # THEN
    assert result["knot"].iloc[0] == ";"


def test_fusion_add_knot_from_rope_ReturnsDf_Scenario08_DoesNotMutateInputDf():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"])
    # WHEN
    fusion_add_knot_from_rope(df, {})
    # THEN
    assert "knot" not in df.columns
