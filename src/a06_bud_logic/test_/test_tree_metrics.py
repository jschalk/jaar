from src.a06_bud_logic.tree_metrics import TreeMetrics, treemetrics_shop


def test_TreeMetrics_Exists():
    # ESTABLISH / WHEN
    x_tree_metrics = TreeMetrics()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.label_count is None
    assert x_tree_metrics.level_count is None
    assert x_tree_metrics.reason_rcontexts is None
    assert x_tree_metrics.awardlinks_metrics is None
    assert x_tree_metrics.uid_max is None
    assert x_tree_metrics.uid_dict is None
    assert x_tree_metrics.all_concept_uids_are_unique is None


def test_treemetrics_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_tree_metrics = treemetrics_shop()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.label_count == 0
    assert x_tree_metrics.level_count == {}
    assert x_tree_metrics.reason_rcontexts == {}
    assert x_tree_metrics.awardlinks_metrics == {}
    assert x_tree_metrics.uid_max == 0
    assert x_tree_metrics.uid_dict == {}
    assert x_tree_metrics.all_concept_uids_are_unique

    # # could create tests for these methods?
    # def evaluate_label(
    # def evaluate_pledge(self, pledge: bool, concept_way: WayStr):
    # def evaluate_level(self, level):
    # def evaluate_reasonunits(self, reasons: dict[WayStr, ReasonUnit]):
    # def evaluate_awardlinks(self, awardlinks: dict[GroupTitle, AwardLink]):
    # def evaluate_uid_max(self, uid):
