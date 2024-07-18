from src.bud.examples.example_buds import bud_v001
from src.bud.bud import budunit_shop
from src.bud.idea import ideaunit_shop
from src._road.road import create_road_from_nodes


def test_BudUnit_get_tree_metrics_exists():
    # ESTABLISH
    zia_bud = budunit_shop(_owner_id="Zia")

    # WHEN
    zia_bud_tree_metrics = zia_bud.get_tree_metrics()

    # THEN
    assert zia_bud_tree_metrics.node_count != None
    assert zia_bud_tree_metrics.reason_bases != None
    assert zia_bud_tree_metrics.level_count != None
    assert zia_bud_tree_metrics.awardlinks_metrics != None


def test_BudUnit_get_tree_metrics_get_idea_uid_max_correctlyGetsMaxIdeaUID():
    # ESTABLISH
    yao_bud = bud_v001()

    # WHEN
    tree_metrics_x = yao_bud.get_tree_metrics()

    # THEN
    assert tree_metrics_x.uid_max == 279
    assert yao_bud.get_idea_uid_max() == 279


def test_BudUnit_get_tree_metrics_CorrectlySetsBoolean_all_idea_uids_are_unique():
    # ESTABLISH
    yao_bud = bud_v001()

    # WHEN
    tree_metrics_x = yao_bud.get_tree_metrics()

    # THEN
    assert tree_metrics_x.all_idea_uids_are_unique is False
    assert len(tree_metrics_x.uid_dict) == 219


def test_BudUnit_get_tree_set_all_idea_uids_unique():
    # ESTABLISH
    yao_bud = bud_v001()
    tree_metrics_before = yao_bud.get_tree_metrics()
    assert len(tree_metrics_before.uid_dict) == 219

    # WHEN
    yao_bud.set_all_idea_uids_unique()

    # THEN
    tree_metrics_after = yao_bud.get_tree_metrics()
    # for uid, uid_count in tree_metrics_after.uid_dict.items():
    #     # print(f"{uid=} {uid_count=} {len(yao_bud.get_idea_dict())=}")
    #     print(f"{uid=} {uid_count=} ")
    assert len(tree_metrics_after.uid_dict) == 253
    assert tree_metrics_after.all_idea_uids_are_unique == True


def test_BudUnit_set_all_idea_uids_unique_SetsUIDsCorrectly():
    # ESTABLISH
    zia_text = "Zia"
    zia_bud = budunit_shop(_owner_id=zia_text)
    swim_text = "swim"
    sports_text = "sports"
    zia_bud.add_l1_idea(ideaunit_shop(swim_text, _uid=None))
    zia_bud.add_l1_idea(ideaunit_shop(sports_text, _uid=2))
    swim_road = zia_bud.make_l1_road(swim_text)
    assert zia_bud.get_idea_obj(swim_road)._uid is None

    # WHEN
    zia_bud.set_all_idea_uids_unique()

    # THEN
    assert zia_bud.get_idea_obj(swim_road)._uid != None


def test_BudUnit_get_tree_metrics_ReturnsANone_pledge_IdeaRoadUnit():
    # ESTABLISH
    nia_text = "Nia"
    nia_bud = budunit_shop(nia_text, _weight=10)
    weekdays = "weekdays"
    nia_bud.add_l1_idea(ideaunit_shop(weekdays, _weight=40))
    tree_metrics_before = nia_bud.get_tree_metrics()

    # WHEN/THEN
    assert tree_metrics_before.last_evaluated_pledge_idea_road is None


def test_BudUnit_get_tree_metrics_Returns_pledge_IdeaRoadUnit():
    # ESTABLISH
    yao_bud = bud_v001()
    yao_tree_metrics = yao_bud.get_tree_metrics()

    # WHEN/THEN
    train_road = create_road_from_nodes(
        [
            yao_bud._real_id,
            "ACME",
            "ACME Employee Responsiblities",
            "Know Abuse Prevention and Reporting guildlines",
            "Accomplish Fall 2021 training",
        ]
    )
    assert yao_tree_metrics.last_evaluated_pledge_idea_road == train_road
