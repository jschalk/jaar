from src._world.tree_metrics import TreeMetrics, treemetrics_shop


def test_TreeMetrics_Exists():
    # GIVEN / WHEN
    x_tree_metrics = TreeMetrics()

    # THEN
    assert x_tree_metrics != None
    assert x_tree_metrics.node_count is None
    assert x_tree_metrics.level_count is None
    assert x_tree_metrics.reason_bases is None
    assert x_tree_metrics.fiscallinks_metrics is None
    assert x_tree_metrics.uid_max is None
    assert x_tree_metrics.uid_dict is None
    assert x_tree_metrics.all_idea_uids_are_unique is None


def test_treemetrics_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_tree_metrics = treemetrics_shop()

    # THEN
    assert x_tree_metrics != None
    assert x_tree_metrics.node_count == 0
    assert x_tree_metrics.level_count == {}
    assert x_tree_metrics.reason_bases == {}
    assert x_tree_metrics.fiscallinks_metrics == {}
    assert x_tree_metrics.uid_max == 0
    assert x_tree_metrics.uid_dict == {}
    assert x_tree_metrics.all_idea_uids_are_unique

    # # could create tests for these methods?
    # def evaluate_node(
    # def evaluate_pledge(self, pledge: bool, idea_road: RoadUnit):
    # def evaluate_level(self, level):
    # def evaluate_reasonunits(self, reasons: dict[RoadUnit, ReasonUnit]):
    # def evaluate_fiscallinks(self, fiscallinks: dict[BeliefID, FiscalLink]):
    # def evaluate_uid_max(self, uid):
