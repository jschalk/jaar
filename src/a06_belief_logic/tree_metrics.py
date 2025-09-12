from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import get_0_if_None, get_empty_dict_if_None
from src.a01_rope_logic.term import GroupTitle
from src.a03_group_logic.group import AwardUnit
from src.a04_reason_logic.reason import ReasonUnit, RopeTerm


@dataclass
class TreeMetrics:
    label_count: int = None
    tree_level_count: dict[int, int] = None
    reason_contexts: dict[RopeTerm, int] = None
    awardunits_metrics: dict[GroupTitle, AwardUnit] = None
    uid_max: int = None
    uid_dict: dict[int, int] = None
    all_plan_uids_are_unique: bool = None
    last_evaluated_task_plan_rope: RopeTerm = None

    def evaluate_label(
        self,
        tree_level: int,
        reasons: dict[RopeTerm, ReasonUnit],
        awardunits: dict[GroupTitle, AwardUnit],
        uid: int,
        task: bool,
        plan_rope: RopeTerm,
    ):
        self.label_count += 1
        self.evaluate_task(task=task, plan_rope=plan_rope)
        self.evaluate_level(tree_level=tree_level)
        self.evaluate_reasonunits(reasons=reasons)
        self.evaluate_awardunits(awardunits=awardunits)
        self.evaluate_uid_max(uid=uid)

    def evaluate_task(self, task: bool, plan_rope: RopeTerm):
        if task:
            self.last_evaluated_task_plan_rope = plan_rope

    def evaluate_level(self, tree_level):
        if self.tree_level_count.get(tree_level) is None:
            self.tree_level_count[tree_level] = 1
        else:
            self.tree_level_count[tree_level] += 1

    def evaluate_reasonunits(self, reasons: dict[RopeTerm, ReasonUnit]):
        reasons = {} if reasons is None else reasons
        for reason in reasons.values():
            if self.reason_contexts.get(reason.reason_context) is None:
                self.reason_contexts[reason.reason_context] = 1
            else:
                self.reason_contexts[reason.reason_context] = (
                    self.reason_contexts[reason.reason_context] + 1
                )

    def evaluate_awardunits(self, awardunits: dict[GroupTitle, AwardUnit]):
        if awardunits is not None:
            for awardunit in awardunits.values():
                self.awardunits_metrics[awardunit.awardee_title] = awardunit

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
    reason_contexts: dict[RopeTerm, int] = None,
    awardunits_metrics: dict[GroupTitle, AwardUnit] = None,
    uid_max: int = None,
    uid_dict: dict[int, int] = None,
) -> TreeMetrics:
    x_treemetrics = TreeMetrics(
        label_count=get_0_if_None(label_count),
        tree_level_count=get_empty_dict_if_None(level_count),
        reason_contexts=get_empty_dict_if_None(reason_contexts),
        awardunits_metrics=get_empty_dict_if_None(awardunits_metrics),
        uid_dict=get_empty_dict_if_None(uid_dict),
        uid_max=get_0_if_None(uid_max),
    )
    if x_treemetrics.all_plan_uids_are_unique is None:
        x_treemetrics.all_plan_uids_are_unique = True
    return x_treemetrics
