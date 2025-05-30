from src.a01_term_logic.way import create_way_from_labels
from src.a03_group_logic.group import awardlink_shop
from src.a03_group_logic.acct import acctunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._test_util.example_buds import budunit_v001


def test_BudUnit_get_tree_metrics_exists():
    # ESTABLISH
    zia_bud = budunit_shop(owner_name="Zia")

    # WHEN
    zia_bud_tree_metrics = zia_bud.get_tree_metrics()

    # THEN
    assert zia_bud_tree_metrics.label_count is not None
    assert zia_bud_tree_metrics.reason_rcontexts is not None
    assert zia_bud_tree_metrics.level_count is not None
    assert zia_bud_tree_metrics.awardlinks_metrics is not None


def test_BudUnit_get_tree_metrics_get_concept_uid_max_correctlyGetsMaxConceptUID():
    # ESTABLISH
    yao_bud = budunit_v001()

    # WHEN
    tree_metrics_x = yao_bud.get_tree_metrics()

    # THEN
    assert tree_metrics_x.uid_max == 279
    assert yao_bud.get_concept_uid_max() == 279


def test_BudUnit_get_tree_metrics_CorrectlySetsBoolean_all_concept_uids_are_unique():
    # ESTABLISH
    yao_bud = budunit_v001()

    # WHEN
    tree_metrics_x = yao_bud.get_tree_metrics()

    # THEN
    assert tree_metrics_x.all_concept_uids_are_unique is False
    assert len(tree_metrics_x.uid_dict) == 219


def test_BudUnit_get_tree_set_all_concept_uids_unique():
    # ESTABLISH
    yao_bud = budunit_v001()
    tree_metrics_before = yao_bud.get_tree_metrics()
    assert len(tree_metrics_before.uid_dict) == 219

    # WHEN
    yao_bud.set_all_concept_uids_unique()

    # THEN
    tree_metrics_after = yao_bud.get_tree_metrics()
    # for uid, uid_count in tree_metrics_after.uid_dict.items():
    #     # print(f"{uid=} {uid_count=} {len(yao_bud.get_concept_dict())=}")
    #     print(f"{uid=} {uid_count=} ")
    assert len(tree_metrics_after.uid_dict) == 252
    assert tree_metrics_after.all_concept_uids_are_unique is True


def test_BudUnit_set_all_concept_uids_unique_SetsUIDsCorrectly():
    # ESTABLISH
    zia_str = "Zia"
    zia_bud = budunit_shop(owner_name=zia_str)
    swim_str = "swim"
    sports_str = "sports"
    zia_bud.set_l1_concept(conceptunit_shop(swim_str, _uid=None))
    zia_bud.set_l1_concept(conceptunit_shop(sports_str, _uid=2))
    swim_way = zia_bud.make_l1_way(swim_str)
    assert zia_bud.get_concept_obj(swim_way)._uid is None

    # WHEN
    zia_bud.set_all_concept_uids_unique()

    # THEN
    assert zia_bud.get_concept_obj(swim_way)._uid is not None


def test_BudUnit_get_tree_metrics_ReturnsANone_pledge_ConceptWayTerm():
    # ESTABLISH
    nia_str = "Nia"
    nia_bud = budunit_shop(nia_str, tally=10)
    wkdays = "wkdays"
    nia_bud.set_l1_concept(conceptunit_shop(wkdays, mass=40))
    tree_metrics_before = nia_bud.get_tree_metrics()

    # WHEN / THEN
    assert tree_metrics_before.last_evaluated_pledge_concept_way is None


def test_BudUnit_get_tree_metrics_Returns_pledge_ConceptWayTerm():
    # ESTABLISH
    yao_bud = budunit_v001()
    yao_tree_metrics = yao_bud.get_tree_metrics()

    # WHEN / THEN
    traain_way = create_way_from_labels(
        [
            yao_bud.fisc_label,
            "ACME",
            "ACME Employee Responsiblities",
            "Know Abuse Deterrence and Reporting guildlines",
            "Accomplish Fall 2021 traaining",
        ]
    )
    assert yao_tree_metrics.last_evaluated_pledge_concept_way == traain_way


def test_BudUnit_get_tree_metrics_TracksReasonsThatHaveNoFactRcontexts():
    # ESTABLISH
    yao_budunit = budunit_v001()

    # WHEN
    yao_tree_metrics = yao_budunit.get_tree_metrics()

    # THEN
    print(f"{yao_tree_metrics.level_count=}")
    print(f"{yao_tree_metrics.reason_rcontexts=}")
    assert yao_tree_metrics is not None
    reason_rcontexts_x = yao_tree_metrics.reason_rcontexts
    assert reason_rcontexts_x is not None
    assert len(reason_rcontexts_x) > 0


def test_BudUnit_get_missing_fact_rcontexts_ReturnsAllRcontextsNotCoveredByFacts():
    # ESTABLISH
    yao_budunit = budunit_v001()
    missing_rcontexts = yao_budunit.get_missing_fact_rcontexts()
    assert missing_rcontexts is not None
    print(f"{missing_rcontexts=}")
    print(f"{len(missing_rcontexts)=}")
    assert len(missing_rcontexts) == 11

    yao_budunit.add_fact(
        yao_budunit.make_l1_way("day_minute"),
        fstate=yao_budunit.make_l1_way("day_minute"),
        fopen=0,
        fnigh=1439,
    )

    # WHEN
    missing_rcontexts = yao_budunit.get_missing_fact_rcontexts()

    # THEN
    assert len(missing_rcontexts) == 11


def test_BudUnit_3AdvocatesNoconceptunit_shop():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"

    zia_budunit = budunit_shop("Zia")
    yao_acctunit = acctunit_shop(acct_name=yao_str)
    sue_acctunit = acctunit_shop(acct_name=sue_str)
    zia_acctunit = acctunit_shop(acct_name=zia_str)
    # print(f"{yao=}")
    zia_budunit.set_acctunit(yao_acctunit)
    zia_budunit.set_acctunit(sue_acctunit)
    zia_budunit.set_acctunit(zia_acctunit)
    zia_budunit.conceptroot.set_awardlink(awardlink_shop(yao_str, give_force=10))
    zia_budunit.conceptroot.set_awardlink(awardlink_shop(sue_str, give_force=10))
    zia_budunit.conceptroot.set_awardlink(awardlink_shop(zia_str, give_force=10))

    # WHEN
    assert zia_budunit.get_awardlinks_metrics() is not None
    accts_metrics = zia_budunit.get_awardlinks_metrics()

    # THEN
    yao_awardlink = accts_metrics[yao_str]
    sue_awardlink = accts_metrics[sue_str]
    zia_awardlink = accts_metrics[zia_str]
    assert yao_awardlink.awardee_title is not None
    assert sue_awardlink.awardee_title is not None
    assert zia_awardlink.awardee_title is not None
    assert yao_awardlink.awardee_title == yao_str
    assert sue_awardlink.awardee_title == sue_str
    assert zia_awardlink.awardee_title == zia_str
