from ch04_rope.rope import create_rope
from ch19_idea_src.fission_step import (
    fission_add_ancestor_rope_rows,
    fission_add_knot_from_rope,
    fission_set_moment_rope_from_moment_label,
    fission_set_plan_rope_from_health_label,
    fission_set_pledge_to_one,
    run_fission_steps,
)
from ch19_idea_src.idea_config import get_idea_config_dict
from ch99_glossary.ch_keyword import Ch19Keywords as kw, ExampleStrs as exx
from pandas import DataFrame as pandas_DataFrame, testing as pandas_testing
from pytest import raises as pytest_raises


def make_df(**kwargs) -> pandas_DataFrame:
    return pandas_DataFrame({**kwargs})


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario01_AddsAllAncestorsForSingleRope():
    # ESTABLISH
    soccer_rope = ";mmt01;sports;play soccer;"
    df = make_df(plan_rope=[soccer_rope], pledge=[1], person_name=["Alice"])
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    ropes = set(result["plan_rope"])
    assert ";mmt01;" in ropes
    assert ";mmt01;sports;" in ropes
    assert soccer_rope in ropes


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario02_AncestorRowsHavePledgeZero():
    # ESTABLISH
    soccer_rope = ";mmt01;sports;play soccer;"
    df = make_df(plan_rope=[soccer_rope], pledge=[1], person_name=["Alice"])
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    ancestors = result[result["plan_rope"] != soccer_rope]
    assert (ancestors["pledge"] == 0).all()


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario03_OriginalRowPledgeUnchanged():
    # ESTABLISH
    soccer_rope = ";mmt01;sports;play soccer;"
    df = make_df(plan_rope=[soccer_rope], pledge=[1], person_name=["Alice"])
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    original = result[result["plan_rope"] == soccer_rope]
    assert original["pledge"].iloc[0] == 1


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario04_NoDuplicateAncestorsAcrossRows():
    # ESTABLISH
    soccer_rope = ";mmt01;sports;play soccer;"
    df = make_df(
        plan_rope=[soccer_rope, ";mmt01;sports;climb;"],
        pledge=[1, 1],
        person_name=["Alice", "Bob"],
    )
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    assert result["plan_rope"].value_counts()[";mmt01;"] == 1
    assert result["plan_rope"].value_counts()[";mmt01;sports;"] == 1


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario05_ExistingAncestorNotDuplicated():
    # ESTABLISH
    soccer_rope = ";mmt01;sports;play soccer;"
    df = make_df(
        plan_rope=[soccer_rope, ";mmt01;sports;", ";mmt01;"],
        pledge=[1, 1, 1],
        person_name=["Alice", "Bob", "Carol"],
    )
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    assert result["plan_rope"].value_counts()[";mmt01;sports;"] == 1
    assert result["plan_rope"].value_counts()[";mmt01;"] == 1


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario06_NoPlanRopeColumnReturnsUnchanged():
    # ESTABLISH
    df = make_df(pledge=[1], person_name=["Alice"])
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    pandas_testing.assert_frame_equal(result, df)


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario07_NullRopeValuesSkipped():
    # ESTABLISH
    df = make_df(
        plan_rope=[None, ";mmt01;sports;"], pledge=[1, 1], person_name=["Alice", "Bob"]
    )
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    assert len(result[result["plan_rope"] == ";mmt01;"]) == 1


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario08_SingleSegmentRopeAddsNoAncestors():
    # ESTABLISH
    df = make_df(plan_rope=[";mmt01;"], pledge=[1], person_name=["Alice"])
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    assert len(result) == 1


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario09_OtherColumnsAreCopiedToAncestorRows():
    # ESTABLISH
    soccer_rope = ";mmt01;sports;play soccer;"
    df = make_df(plan_rope=[soccer_rope], pledge=[1], person_name=["Alice"])
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    ancestors = result[result["plan_rope"] != soccer_rope]
    assert (ancestors["person_name"] == "Alice").all()


def test_fission_add_ancestor_rope_rows_ReturnsDf_Scenario10_EmptyDataframeReturnsEmpty():
    # ESTABLISH
    df = pandas_DataFrame(columns=["plan_rope", "pledge", "person_name"])
    # WHEN
    result = fission_add_ancestor_rope_rows(df)
    # THEN
    assert len(result) == 0
    assert list(result.columns) == ["plan_rope", "pledge", "person_name"]


def test_fission_set_pledge_to_one_ReturnsDf_Scenario01_AddsPledgeColumnWhenAbsent():
    # ESTABLISH
    df = make_df(person_name=["Alice", "Bob"])
    # WHEN
    result = fission_set_pledge_to_one(df)
    # THEN
    assert "pledge" in result.columns


def test_fission_set_pledge_to_one_ReturnsDf_Scenario02_SetsPledgeToOneWhenColumnAbsent():
    # ESTABLISH
    df = make_df(person_name=["Alice", "Bob"])
    # WHEN
    result = fission_set_pledge_to_one(df)
    # THEN
    assert (result["pledge"] == 1).all()


def test_fission_set_pledge_to_one_ReturnsDf_Scenario03_OverwritesExistingPledgeValues():
    # ESTABLISH
    df = make_df(person_name=["Alice", "Bob"], pledge=[0, 99])
    # WHEN
    result = fission_set_pledge_to_one(df)
    # THEN
    assert (result["pledge"] == 1).all()


def test_fission_set_pledge_to_one_ReturnsDf_Scenario04_OtherColumnsUnchanged():
    # ESTABLISH
    df = make_df(person_name=["Alice", "Bob"], pledge=[0, 0])
    # WHEN
    result = fission_set_pledge_to_one(df)
    # THEN
    assert list(result["person_name"]) == ["Alice", "Bob"]


def test_fission_set_pledge_to_one_ReturnsDf_Scenario05_DoesNotMutateInputDf():
    # ESTABLISH
    df = make_df(person_name=["Alice"], pledge=[0])
    # WHEN
    fission_set_pledge_to_one(df)
    # THEN
    assert df["pledge"].iloc[0] == 0


def test_fission_set_pledge_to_one_ReturnsDf_Scenario06_EmptyDataframeReturnsPledgeColumn():
    # ESTABLISH
    df = pandas_DataFrame(columns=["person_name"])
    # WHEN
    result = fission_set_pledge_to_one(df)
    # THEN
    assert "pledge" in result.columns
    assert len(result) == 0


def test_fission_set_plan_rope_from_health_label_ReturnsDf_Scenario01_BuildsCorrectPlanRope():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"], health_label=["cardio"])
    # WHEN
    result = fission_set_plan_rope_from_health_label(df)
    # THEN
    assert result["plan_rope"].iloc[0] == ";mmt01;sports;health;cardio;"


def test_fission_set_plan_rope_from_health_label_ReturnsDf_Scenario02_MultipleRowsAllCorrect():
    # ESTABLISH
    df = make_df(
        moment_rope=[";mmt01;sports;", ";mmt01;rest;"], health_label=["cardio", "sleep"]
    )
    # WHEN
    result = fission_set_plan_rope_from_health_label(df)
    # THEN
    assert result["plan_rope"].iloc[0] == ";mmt01;sports;health;cardio;"
    assert result["plan_rope"].iloc[1] == ";mmt01;rest;health;sleep;"


def test_fission_set_plan_rope_from_health_label_ReturnsDf_Scenario03_DoesNotMutateInputDf():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"], health_label=["cardio"])
    # WHEN
    fission_set_plan_rope_from_health_label(df)
    # THEN
    assert "plan_rope" not in df.columns


def test_fission_set_plan_rope_from_health_label_ReturnsDf_Scenario04_OtherColumnsUnchanged():
    # ESTABLISH
    df = make_df(
        moment_rope=[";mmt01;sports;"], health_label=["cardio"], person_name=["Alice"]
    )
    # WHEN
    result = fission_set_plan_rope_from_health_label(df)
    # THEN
    assert result["person_name"].iloc[0] == "Alice"


def test_fission_set_plan_rope_from_health_label_RaisesValueError_Scenario05_MissingMomentRopeColumn():
    # ESTABLISH
    df = make_df(health_label=["cardio"])
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_rope"):
        fission_set_plan_rope_from_health_label(df)


def test_fission_set_plan_rope_from_health_label_RaisesValueError_Scenario06_MissingHealthLabelColumn():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"])
    # WHEN / THEN
    with pytest_raises(ValueError, match="health_label"):
        fission_set_plan_rope_from_health_label(df)


def test_fission_set_plan_rope_from_health_label_RaisesValueError_Scenario07_NullMomentRopeValue():
    # ESTABLISH
    df = make_df(
        moment_rope=[None, ";mmt01;sports;"], health_label=["cardio", "cardio"]
    )
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_rope.*indices.*\\[0\\]"):
        fission_set_plan_rope_from_health_label(df)


def test_fission_set_plan_rope_from_health_label_RaisesValueError_Scenario08_NullHealthLabelValue():
    # ESTABLISH
    df = make_df(
        moment_rope=[";mmt01;sports;", ";mmt01;rest;"], health_label=["cardio", None]
    )
    # WHEN / THEN
    with pytest_raises(ValueError, match="health_label.*indices.*\\[1\\]"):
        fission_set_plan_rope_from_health_label(df)


def test_fission_set_moment_rope_from_moment_label_ReturnsDf_Scenario01_BuildsCorrectMomentRope():
    # ESTABLISH
    df = make_df(moment_label=["sports"])
    # WHEN
    result = fission_set_moment_rope_from_moment_label(df)
    # THEN
    assert result["moment_rope"].iloc[0] == ";sports;"


def test_fission_set_moment_rope_from_moment_label_ReturnsDf_Scenario02_MultipleRowsAllCorrect():
    # ESTABLISH
    df = make_df(moment_label=["sports", "rest", "work"])
    # WHEN
    result = fission_set_moment_rope_from_moment_label(df)
    # THEN
    assert result["moment_rope"].iloc[0] == ";sports;"
    assert result["moment_rope"].iloc[1] == ";rest;"
    assert result["moment_rope"].iloc[2] == ";work;"


def test_fission_set_moment_rope_from_moment_label_ReturnsDf_Scenario03_DoesNotMutateInputDf():
    # ESTABLISH
    df = make_df(moment_label=["sports"])
    # WHEN
    fission_set_moment_rope_from_moment_label(df)
    # THEN
    assert "moment_rope" not in df.columns


def test_fission_set_moment_rope_from_moment_label_ReturnsDf_Scenario04_OtherColumnsUnchanged():
    # ESTABLISH
    df = make_df(moment_label=["sports"], person_name=["Alice"])
    # WHEN
    result = fission_set_moment_rope_from_moment_label(df)
    # THEN
    assert result["person_name"].iloc[0] == "Alice"


def test_fission_set_moment_rope_from_moment_label_ReturnsDf_Scenario05_OverwritesExistingMomentRope():
    # ESTABLISH
    df = make_df(moment_label=["sports"], moment_rope=[";old_value;"])
    # WHEN
    result = fission_set_moment_rope_from_moment_label(df)
    # THEN
    assert result["moment_rope"].iloc[0] == ";sports;"


def test_fission_set_moment_rope_from_moment_label_RaisesValueError_Scenario06_MissingMomentLabelColumn():
    # ESTABLISH
    df = make_df(person_name=["Alice"])
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_label"):
        fission_set_moment_rope_from_moment_label(df)


def test_fission_set_moment_rope_from_moment_label_RaisesValueError_Scenario07_NullMomentLabelValue():
    # ESTABLISH
    df = make_df(moment_label=[None, "sports"])
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_label.*indices.*\\[0\\]"):
        fission_set_moment_rope_from_moment_label(df)


def test_fission_set_moment_rope_from_moment_label_RaisesValueError_Scenario08_MultipleNullMomentLabelValues():
    # ESTABLISH
    df = make_df(moment_label=[None, "sports", None])
    # WHEN / THEN
    with pytest_raises(ValueError, match="moment_label.*indices.*\\[0, 2\\]"):
        fission_set_moment_rope_from_moment_label(df)


def test_fission_add_knot_from_rope_ReturnsDf_Scenario01_SetsDefaultKnotWhenNoRopeColumns():
    # ESTABLISH
    df = make_df(person_name=["Alice"])
    # WHEN
    result = fission_add_knot_from_rope(df)
    # THEN
    assert result["knot"].iloc[0] == ";"


def test_fission_add_knot_from_rope_ReturnsDf_Scenario02_InfersKnotFromMomentRope():
    # ESTABLISH
    df = make_df(moment_rope=["|mmt01|sports|"])
    # WHEN
    result = fission_add_knot_from_rope(df)
    # THEN
    assert result["knot"].iloc[0] == "|"


def test_fission_add_knot_from_rope_ReturnsDf_Scenario03_InfersKnotFromPlanRopeWhenNoMomentRope():
    # ESTABLISH
    df = make_df(plan_rope=["|mmt01|sports|health|cardio|"])
    # WHEN
    result = fission_add_knot_from_rope(df)
    # THEN
    assert result["knot"].iloc[0] == "|"


def test_fission_add_knot_from_rope_ReturnsDf_Scenario04_MomentRopeTakesPriorityOverPlanRope():
    # ESTABLISH
    df = make_df(
        moment_rope=["|mmt01|sports|"], plan_rope=[";mmt01;sports;health;cardio;"]
    )
    # WHEN
    result = fission_add_knot_from_rope(df)
    # THEN
    assert result["knot"].iloc[0] == "|"


def test_fission_add_knot_from_rope_ReturnsDf_Scenario05_ReturnsUnchangedWhenKnotAlreadyExists():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"], knot=["!"])
    # WHEN
    result = fission_add_knot_from_rope(df)
    # THEN
    assert result["knot"].iloc[0] == "!"


def test_fission_add_knot_from_rope_ReturnsDf_Scenario06_SkipsNullMomentRopeFallsBackToPlanRope():
    # ESTABLISH
    df = make_df(moment_rope=[None], plan_rope=["|mmt01|sports|"])
    # WHEN
    result = fission_add_knot_from_rope(df)
    # THEN
    assert result["knot"].iloc[0] == "|"


def test_fission_add_knot_from_rope_ReturnsDf_Scenario07_SetsDefaultKnotWhenAllRopeValuesNull():
    # ESTABLISH
    df = make_df(moment_rope=[None], plan_rope=[None])
    # WHEN
    result = fission_add_knot_from_rope(df)
    # THEN
    assert result["knot"].iloc[0] == ";"


def test_fission_add_knot_from_rope_ReturnsDf_Scenario08_DoesNotMutateInputDf():
    # ESTABLISH
    df = make_df(moment_rope=[";mmt01;sports;"])
    # WHEN
    fission_add_knot_from_rope(df)
    # THEN
    assert "knot" not in df.columns


# TODO reactivate, edit and pass
# def test_run_fission_steps_ReturnsObj_Scenario00_OutputColumnsMatchBrickSchema():
#     # ESTABLISH
#     idea_config_dict = get_idea_config_dict()
#     ii00502_config = idea_config_dict.get("ii00502")
#     clean_rope = create_rope(exx.a23, exx.clean)
#     mop_rope = create_rope(clean_rope, exx.mop)
#     star2 = 2
#     ii00502_columns = [
#         kw.spark_face,
#         kw.moment_rope,
#         kw.person_name,
#         kw.plan_rope,
#         kw.star,
#         kw.knot,
#     ]

#     ii00502_rows = [[exx.sue, exx.a23, exx.yao, mop_rope, star2, ";"]]
#     ii00502_df = pandas_DataFrame(ii00502_rows, columns=ii00502_columns)
#     # WHEN
#     fissioned_df = run_fission_steps(ii00502_df, ii00502_config)
#     # THEN
#     fissioned_columns = list(fissioned_df.columns.array)
#     print(f"{fissioned_columns=}")
#     assert fissioned_columns == [
#         kw.spark_num,
#         kw.spark_face,
#         kw.moment_rope,
#         kw.person_name,
#         kw.plan_rope,
#         kw.star,
#         kw.pledge,
#         kw.knot,
#     ]
#     assert len(fissioned_columns) == 3
