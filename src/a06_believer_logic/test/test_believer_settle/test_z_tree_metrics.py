from src.a01_term_logic.rope import create_rope_from_labels
from src.a03_group_logic.group import awardunit_shop
from src.a03_group_logic.partner import partnerunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.example_believers import believerunit_v001


def test_BelieverUnit_get_tree_metrics_Exists():
    # ESTABLISH
    zia_believer = believerunit_shop(believer_name="Zia")

    # WHEN
    zia_believer_tree_metrics = zia_believer.get_tree_metrics()

    # THEN
    assert zia_believer_tree_metrics.label_count is not None
    assert zia_believer_tree_metrics.reason_contexts is not None
    assert zia_believer_tree_metrics.level_count is not None
    assert zia_believer_tree_metrics.awardunits_metrics is not None


def test_BelieverUnit_get_tree_metrics_get_plan_uid_max_GetsMaxPlanUID():
    # ESTABLISH
    yao_believer = believerunit_v001()

    # WHEN
    tree_metrics_x = yao_believer.get_tree_metrics()

    # THEN
    assert tree_metrics_x.uid_max == 279
    assert yao_believer.get_plan_uid_max() == 279


def test_BelieverUnit_get_tree_metrics_SetsBoolean_all_plan_uids_are_unique():
    # ESTABLISH
    yao_believer = believerunit_v001()

    # WHEN
    tree_metrics_x = yao_believer.get_tree_metrics()

    # THEN
    assert tree_metrics_x.all_plan_uids_are_unique is False
    assert len(tree_metrics_x.uid_dict) == 219


def test_BelieverUnit_get_tree_set_all_plan_uids_unique():
    # ESTABLISH
    yao_believer = believerunit_v001()
    tree_metrics_before = yao_believer.get_tree_metrics()
    assert len(tree_metrics_before.uid_dict) == 219

    # WHEN
    yao_believer.set_all_plan_uids_unique()

    # THEN
    tree_metrics_after = yao_believer.get_tree_metrics()
    # for uid, uid_count in tree_metrics_after.uid_dict.items():
    #     # print(f"{uid=} {uid_count=} {len(yao_believer.get_plan_dict())=}")
    #     print(f"{uid=} {uid_count=} ")
    assert len(tree_metrics_after.uid_dict) == 252
    assert tree_metrics_after.all_plan_uids_are_unique is True


def test_BelieverUnit_set_all_plan_uids_unique_SetsUIDs():
    # ESTABLISH
    zia_str = "Zia"
    zia_believer = believerunit_shop(believer_name=zia_str)
    swim_str = "swim"
    sports_str = "sports"
    zia_believer.set_l1_plan(planunit_shop(swim_str, _uid=None))
    zia_believer.set_l1_plan(planunit_shop(sports_str, _uid=2))
    swim_rope = zia_believer.make_l1_rope(swim_str)
    assert zia_believer.get_plan_obj(swim_rope)._uid is None

    # WHEN
    zia_believer.set_all_plan_uids_unique()

    # THEN
    assert zia_believer.get_plan_obj(swim_rope)._uid is not None


def test_BelieverUnit_get_tree_metrics_ReturnsANone_task_PlanRopeTerm():
    # ESTABLISH
    nia_str = "Nia"
    nia_believer = believerunit_shop(nia_str, tally=10)
    wk = "wk"
    nia_believer.set_l1_plan(planunit_shop(wk, star=40))
    tree_metrics_before = nia_believer.get_tree_metrics()

    # WHEN / THEN
    assert tree_metrics_before.last_evaluated_task_plan_rope is None


def test_BelieverUnit_get_tree_metrics_Returns_task_PlanRopeTerm():
    # ESTABLISH
    yao_believer = believerunit_v001()
    yao_tree_metrics = yao_believer.get_tree_metrics()

    # WHEN / THEN
    traain_rope = create_rope_from_labels(
        [
            yao_believer.coin_label,
            "ACME",
            "ACME Employee Responsiblities",
            "Know Abuse Deterrence and Reporting guildlines",
            "Accomplish Fall 2021 traaining",
        ]
    )
    assert yao_tree_metrics.last_evaluated_task_plan_rope == traain_rope


def test_BelieverUnit_get_tree_metrics_TracksReasonsThatHaveNoFactreason_contexts():
    # ESTABLISH
    yao_believerunit = believerunit_v001()

    # WHEN
    yao_tree_metrics = yao_believerunit.get_tree_metrics()

    # THEN
    print(f"{yao_tree_metrics.level_count=}")
    print(f"{yao_tree_metrics.reason_contexts=}")
    assert yao_tree_metrics is not None
    reason_contexts_x = yao_tree_metrics.reason_contexts
    assert reason_contexts_x is not None
    assert len(reason_contexts_x) > 0


def test_BelieverUnit_get_missing_fact_reason_contexts_ReturnsAllreason_contextsNotCoveredByFacts():
    # ESTABLISH
    yao_believerunit = believerunit_v001()
    missing_reason_contexts = yao_believerunit.get_missing_fact_reason_contexts()
    assert missing_reason_contexts is not None
    print(f"{missing_reason_contexts=}")
    print(f"{len(missing_reason_contexts)=}")
    assert len(missing_reason_contexts) == 11

    yao_believerunit.add_fact(
        yao_believerunit.make_l1_rope("jour_minute"),
        fact_state=yao_believerunit.make_l1_rope("jour_minute"),
        fact_lower=0,
        fact_upper=1439,
    )

    # WHEN
    missing_reason_contexts = yao_believerunit.get_missing_fact_reason_contexts()

    # THEN
    assert len(missing_reason_contexts) == 11


def test_BelieverUnit_3AdvocatesNoplanunit_shop():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"

    zia_believerunit = believerunit_shop("Zia")
    yao_partnerunit = partnerunit_shop(partner_name=yao_str)
    sue_partnerunit = partnerunit_shop(partner_name=sue_str)
    zia_partnerunit = partnerunit_shop(partner_name=zia_str)
    # print(f"{yao=}")
    zia_believerunit.set_partnerunit(yao_partnerunit)
    zia_believerunit.set_partnerunit(sue_partnerunit)
    zia_believerunit.set_partnerunit(zia_partnerunit)
    zia_believerunit.planroot.set_awardunit(awardunit_shop(yao_str, give_force=10))
    zia_believerunit.planroot.set_awardunit(awardunit_shop(sue_str, give_force=10))
    zia_believerunit.planroot.set_awardunit(awardunit_shop(zia_str, give_force=10))

    # WHEN
    assert zia_believerunit.get_awardunits_metrics() is not None
    partners_metrics = zia_believerunit.get_awardunits_metrics()

    # THEN
    yao_awardunit = partners_metrics[yao_str]
    sue_awardunit = partners_metrics[sue_str]
    zia_awardunit = partners_metrics[zia_str]
    assert yao_awardunit.awardee_title is not None
    assert sue_awardunit.awardee_title is not None
    assert zia_awardunit.awardee_title is not None
    assert yao_awardunit.awardee_title == yao_str
    assert sue_awardunit.awardee_title == sue_str
    assert zia_awardunit.awardee_title == zia_str
