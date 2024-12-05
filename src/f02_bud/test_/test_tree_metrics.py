from src.f02_bud.tree_metrics import TreeMetrics, treemetrics_shop


def test_TreeMetrics_Exists():
    # ESTABLISH / WHEN
    x_tree_metrics = TreeMetrics()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.idea_count is None
    assert x_tree_metrics.level_count is None
    assert x_tree_metrics.reason_bases is None
    assert x_tree_metrics.awardlinks_metrics is None
    assert x_tree_metrics.uid_max is None
    assert x_tree_metrics.uid_dict is None
    assert x_tree_metrics.all_item_uids_are_unique is None


def test_treemetrics_shop_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    x_tree_metrics = treemetrics_shop()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.idea_count == 0
    assert x_tree_metrics.level_count == {}
    assert x_tree_metrics.reason_bases == {}
    assert x_tree_metrics.awardlinks_metrics == {}
    assert x_tree_metrics.uid_max == 0
    assert x_tree_metrics.uid_dict == {}
    assert x_tree_metrics.all_item_uids_are_unique

    # # could create tests for these methods?
    # def evaluate_idea(
    # def evaluate_pledge(self, pledge: bool, item_road: RoadUnit):
    # def evaluate_level(self, level):
    # def evaluate_reasonunits(self, reasons: dict[RoadUnit, ReasonUnit]):
    # def evaluate_awardlinks(self, awardlinks: dict[GroupID, AwardLink]):
    # def evaluate_uid_max(self, uid):
