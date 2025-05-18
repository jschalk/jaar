from src.a00_data_toolbox.dict_toolbox import get_empty_dict_if_None, get_0_if_None
from src.a01_way_logic.way import GroupTitle
from src.a04_reason_logic.reason_idea import ReasonUnit, WayStr
from src.a03_group_logic.group import AwardLink
from dataclasses import dataclass


@dataclass
class TreeMetrics:
    label_count: int = None
    level_count: dict[int, int] = None
    reason_rcontexts: dict[WayStr, int] = None
    awardlinks_metrics: dict[GroupTitle, AwardLink] = None
    uid_max: int = None
    uid_dict: dict[int, int] = None
    all_idea_uids_are_unique: bool = None
    last_evaluated_pledge_idea_way: WayStr = None

    def evaluate_label(
        self,
        level: int,
        reasons: dict[WayStr, ReasonUnit],
        awardlinks: dict[GroupTitle, AwardLink],
        uid: int,
        pledge: bool,
        idea_way: WayStr,
    ):
        self.label_count += 1
        self.evaluate_pledge(pledge=pledge, idea_way=idea_way)
        self.evaluate_level(level=level)
        self.evaluate_reasonunits(reasons=reasons)
        self.evaluate_awardlinks(awardlinks=awardlinks)
        self.evaluate_uid_max(uid=uid)

    def evaluate_pledge(self, pledge: bool, idea_way: WayStr):
        if pledge:
            self.last_evaluated_pledge_idea_way = idea_way

    def evaluate_level(self, level):
        if self.level_count.get(level) is None:
            self.level_count[level] = 1
        else:
            self.level_count[level] = self.level_count[level] + 1

    def evaluate_reasonunits(self, reasons: dict[WayStr, ReasonUnit]):
        reasons = {} if reasons is None else reasons
        for reason in reasons.values():
            if self.reason_rcontexts.get(reason.rcontext) is None:
                self.reason_rcontexts[reason.rcontext] = 1
            else:
                self.reason_rcontexts[reason.rcontext] = (
                    self.reason_rcontexts[reason.rcontext] + 1
                )

    def evaluate_awardlinks(self, awardlinks: dict[GroupTitle, AwardLink]):
        if awardlinks is not None:
            for awardlink in awardlinks.values():
                self.awardlinks_metrics[awardlink.awardee_title] = awardlink

    def evaluate_uid_max(self, uid):
        if uid is not None and self.uid_max < uid:
            self.uid_max = uid

        if self.uid_dict.get(uid) is None:
            self.uid_dict[uid] = 1
        else:
            self.uid_dict[uid] += 1
            self.all_idea_uids_are_unique = False


def treemetrics_shop(
    label_count: int = None,
    level_count: dict[int, int] = None,
    reason_rcontexts: dict[WayStr, int] = None,
    awardlinks_metrics: dict[GroupTitle, AwardLink] = None,
    uid_max: int = None,
    uid_dict: dict[int, int] = None,
) -> TreeMetrics:
    x_treemetrics = TreeMetrics(
        label_count=get_0_if_None(label_count),
        level_count=get_empty_dict_if_None(level_count),
        reason_rcontexts=get_empty_dict_if_None(reason_rcontexts),
        awardlinks_metrics=get_empty_dict_if_None(awardlinks_metrics),
        uid_dict=get_empty_dict_if_None(uid_dict),
        uid_max=get_0_if_None(uid_max),
    )
    if x_treemetrics.all_idea_uids_are_unique is None:
        x_treemetrics.all_idea_uids_are_unique = True
    return x_treemetrics
