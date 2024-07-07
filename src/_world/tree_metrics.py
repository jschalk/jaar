from src._instrument.python import get_empty_dict_if_none, get_0_if_None
from src._world.reason_idea import ReasonUnit, RoadUnit
from src._world.beliefunit import FiscalLink, BeliefID
from dataclasses import dataclass


@dataclass
class TreeMetrics:
    node_count: int = None
    level_count: dict[int, int] = None
    reason_bases: dict[RoadUnit, int] = None
    fiscallinks_metrics: dict[BeliefID, FiscalLink] = None
    uid_max: int = None
    uid_dict: dict[int, int] = None
    all_idea_uids_are_unique: bool = None
    last_evaluated_pledge_idea_road: RoadUnit = None

    def evaluate_node(
        self,
        level: int,
        reasons: dict[RoadUnit, ReasonUnit],
        fiscallinks: dict[BeliefID, FiscalLink],
        uid: int,
        pledge: bool,
        idea_road: RoadUnit,
    ):
        self.node_count += 1
        self.evaluate_pledge(pledge=pledge, idea_road=idea_road)
        self.evaluate_level(level=level)
        self.evaluate_reasonunits(reasons=reasons)
        self.evaluate_fiscallinks(fiscallinks=fiscallinks)
        self.evaluate_uid_max(uid=uid)

    def evaluate_pledge(self, pledge: bool, idea_road: RoadUnit):
        if pledge:
            self.last_evaluated_pledge_idea_road = idea_road

    def evaluate_level(self, level):
        if self.level_count.get(level) is None:
            self.level_count[level] = 1
        else:
            self.level_count[level] = self.level_count[level] + 1

    def evaluate_reasonunits(self, reasons: dict[RoadUnit, ReasonUnit]):
        if reasons is None:
            reasons = {}
        for reason in reasons.values():
            if self.reason_bases.get(reason.base) is None:
                self.reason_bases[reason.base] = 1
            else:
                self.reason_bases[reason.base] = self.reason_bases[reason.base] + 1

    def evaluate_fiscallinks(self, fiscallinks: dict[BeliefID, FiscalLink]):
        if fiscallinks != None:
            for fiscallink in fiscallinks.values():
                self.fiscallinks_metrics[fiscallink.belief_id] = fiscallink

    def evaluate_uid_max(self, uid):
        if uid != None and self.uid_max < uid:
            self.uid_max = uid

        if self.uid_dict.get(uid) is None:
            self.uid_dict[uid] = 1
        else:
            self.uid_dict[uid] += 1
            self.all_idea_uids_are_unique = False


def treemetrics_shop(
    node_count: int = None,
    level_count: dict[int, int] = None,
    reason_bases: dict[RoadUnit, int] = None,
    fiscallinks_metrics: dict[BeliefID, FiscalLink] = None,
    uid_max: int = None,
    uid_dict: dict[int, int] = None,
) -> TreeMetrics:
    x_treemetrics = TreeMetrics(
        node_count=get_0_if_None(node_count),
        level_count=get_empty_dict_if_none(level_count),
        reason_bases=get_empty_dict_if_none(reason_bases),
        fiscallinks_metrics=get_empty_dict_if_none(fiscallinks_metrics),
        uid_dict=get_empty_dict_if_none(uid_dict),
        uid_max=get_0_if_None(uid_max),
    )
    if x_treemetrics.all_idea_uids_are_unique is None:
        x_treemetrics.all_idea_uids_are_unique = True
    return x_treemetrics
