from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import get_0_if_None, get_empty_dict_if_None
from src.a01_term_logic.term import GroupTitle
from src.a03_group_logic.group import AwardLink
from src.a04_reason_logic.reason_plan import ReasonUnit, RopeTerm


@dataclass
class TreeMetrics:
    label_count: int = None
    level_count: dict[int, int] = None
    reason_r_contexts: dict[RopeTerm, int] = None
    awardlinks_metrics: dict[GroupTitle, AwardLink] = None
    uid_max: int = None
    uid_dict: dict[int, int] = None
    all_plan_uids_are_unique: bool = None
    last_evaluated_task_plan_rope: RopeTerm = None

    def evaluate_label(
        self,
        level: int,
        reasons: dict[RopeTerm, ReasonUnit],
        awardlinks: dict[GroupTitle, AwardLink],
        uid: int,
        task: bool,
        plan_rope: RopeTerm,
    ):
        self.label_count += 1
        self.evaluate_task(task=task, plan_rope=plan_rope)
        self.evaluate_level(level=level)
        self.evaluate_reasonunits(reasons=reasons)
        self.evaluate_awardlinks(awardlinks=awardlinks)
        self.evaluate_uid_max(uid=uid)

    def evaluate_task(self, task: bool, plan_rope: RopeTerm):
        if task:
            self.last_evaluated_task_plan_rope = plan_rope

    def evaluate_level(self, level):
        if self.level_count.get(level) is None:
            self.level_count[level] = 1
        else:
            self.level_count[level] = self.level_count[level] + 1

    def evaluate_reasonunits(self, reasons: dict[RopeTerm, ReasonUnit]):
        reasons = {} if reasons is None else reasons
        for reason in reasons.values():
            if self.reason_r_contexts.get(reason.r_context) is None:
                self.reason_r_contexts[reason.r_context] = 1
            else:
                self.reason_r_contexts[reason.r_context] = (
                    self.reason_r_contexts[reason.r_context] + 1
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
            self.all_plan_uids_are_unique = False


def treemetrics_shop(
    label_count: int = None,
    level_count: dict[int, int] = None,
    reason_r_contexts: dict[RopeTerm, int] = None,
    awardlinks_metrics: dict[GroupTitle, AwardLink] = None,
    uid_max: int = None,
    uid_dict: dict[int, int] = None,
) -> TreeMetrics:
    x_treemetrics = TreeMetrics(
        label_count=get_0_if_None(label_count),
        level_count=get_empty_dict_if_None(level_count),
        reason_r_contexts=get_empty_dict_if_None(reason_r_contexts),
        awardlinks_metrics=get_empty_dict_if_None(awardlinks_metrics),
        uid_dict=get_empty_dict_if_None(uid_dict),
        uid_max=get_0_if_None(uid_max),
    )
    if x_treemetrics.all_plan_uids_are_unique is None:
        x_treemetrics.all_plan_uids_are_unique = True
    return x_treemetrics
