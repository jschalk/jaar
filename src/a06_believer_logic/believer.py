from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_dict_from_json,
    get_empty_dict_if_None,
    get_False_if_None,
    get_json_from_dict,
)
from src.a01_term_logic.rope import (
    all_ropeterms_between,
    create_rope,
    default_knot_if_None,
    get_all_rope_labels,
    get_ancestor_ropes,
    get_forefather_ropes,
    get_parent_rope,
    get_root_label_from_rope,
    get_tail_label,
    is_string_in_rope,
    is_sub_rope,
    rebuild_rope,
    ropeterm_valid_dir_path,
    to_rope,
)
from src.a01_term_logic.term import (
    BeliefLabel,
    BelieverName,
    GroupTitle,
    HealerName,
    LabelTerm,
    PartnerName,
    RopeTerm,
)
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import (
    BitNum,
    FundIota,
    FundNum,
    PennyNum,
    RespectNum,
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
    valid_finance_ratio,
    validate_fund_pool,
    validate_respect_num,
)
from src.a03_group_logic.group import (
    AwardLink,
    GroupUnit,
    groupunit_shop,
    membership_shop,
)
from src.a03_group_logic.partner import (
    PartnerUnit,
    partnerunit_shop,
    partnerunits_get_from_dict,
)
from src.a04_reason_logic.reason_labor import LaborUnit
from src.a04_reason_logic.reason_plan import (
    FactUnit,
    ReasonUnit,
    RopeTerm,
    factunit_shop,
)
from src.a05_plan_logic.healer import HealerLink
from src.a05_plan_logic.plan import (
    PlanAttrHolder,
    PlanUnit,
    get_default_belief_label,
    get_obj_from_plan_dict,
    planattrholder_shop,
    planunit_shop,
)
from src.a06_believer_logic.believer_config import max_tree_traverse_default
from src.a06_believer_logic.tree_metrics import TreeMetrics, treemetrics_shop


class InvalidBelieverException(Exception):
    pass


class InvalidLabelException(Exception):
    pass


class NewKnotException(Exception):
    pass


class PartnerUnitsCredorDebtorSumException(Exception):
    pass


class PartnerMissingException(Exception):
    pass


class Exception_keeps_justified(Exception):
    pass


class _bit_RatioException(Exception):
    pass


class _last_pack_idException(Exception):
    pass


class healerlink_group_title_Exception(Exception):
    pass


class _gogo_calc_stop_calc_Exception(Exception):
    pass


@dataclass
class BelieverUnit:
    belief_label: BeliefLabel = None
    believer_name: BelieverName = None
    partners: dict[PartnerName, PartnerUnit] = None
    planroot: PlanUnit = None
    tally: float = None
    fund_pool: FundNum = None
    fund_iota: FundIota = None
    penny: PennyNum = None
    credor_respect: RespectNum = None
    debtor_respect: RespectNum = None
    respect_bit: BitNum = None
    knot: str = None
    max_tree_traverse: int = None
    last_pack_id: int = None
    # settle_believer Calculated field begin
    _plan_dict: dict[RopeTerm, PlanUnit] = None
    _keep_dict: dict[RopeTerm, PlanUnit] = None
    _healers_dict: dict[HealerName, dict[RopeTerm, PlanUnit]] = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _keeps_justified: bool = None
    _keeps_buildable: bool = None
    _sum_healerlink_share: float = None
    _groupunits: dict[GroupTitle, GroupUnit] = None
    _offtrack_kids_mass_set: set[RopeTerm] = None
    _offtrack_fund: float = None
    _reason_r_contexts: set[RopeTerm] = None
    _range_inheritors: dict[RopeTerm, RopeTerm] = None
    # settle_believer Calculated field end

    def del_last_pack_id(self):
        self.last_pack_id = None

    def set_last_pack_id(self, x_last_pack_id: int):
        if self.last_pack_id is not None and x_last_pack_id < self.last_pack_id:
            exception_str = f"Cannot set _last_pack_id to {x_last_pack_id} because it is less than {self.last_pack_id}."
            raise _last_pack_idException(exception_str)
        self.last_pack_id = x_last_pack_id

    def set_fund_pool(self, x_fund_pool):
        if valid_finance_ratio(x_fund_pool, self.fund_iota) is False:
            exception_str = f"Believer '{self.believer_name}' cannot set fund_pool='{x_fund_pool}'. It is not divisible by fund_iota '{self.fund_iota}'"
            raise _bit_RatioException(exception_str)

        self.fund_pool = validate_fund_pool(x_fund_pool)

    def set_partner_respect(self, x_partner_pool: int):
        self.set_credor_respect(x_partner_pool)
        self.set_debtor_respect(x_partner_pool)
        self.set_fund_pool(x_partner_pool)

    def set_credor_respect(self, new_credor_respect: int):
        if valid_finance_ratio(new_credor_respect, self.respect_bit) is False:
            exception_str = f"Believer '{self.believer_name}' cannot set credor_respect='{new_credor_respect}'. It is not divisible by bit '{self.respect_bit}'"
            raise _bit_RatioException(exception_str)
        self.credor_respect = new_credor_respect

    def set_debtor_respect(self, new_debtor_respect: int):
        if valid_finance_ratio(new_debtor_respect, self.respect_bit) is False:
            exception_str = f"Believer '{self.believer_name}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible by bit '{self.respect_bit}'"
            raise _bit_RatioException(exception_str)
        self.debtor_respect = new_debtor_respect

    def make_rope(
        self,
        parent_rope: RopeTerm = None,
        tail_label: LabelTerm = None,
    ) -> RopeTerm:
        return create_rope(
            parent_rope=parent_rope,
            tail_label=tail_label,
            knot=self.knot,
        )

    def make_l1_rope(self, l1_label: LabelTerm):
        return self.make_rope(self.belief_label, l1_label)

    def set_knot(self, new_knot: str):
        self.settle_believer()
        if self.knot != new_knot:
            for x_plan_rope in self._plan_dict.keys():
                if is_string_in_rope(new_knot, x_plan_rope):
                    exception_str = f"Cannot modify knot to '{new_knot}' because it exists an plan plan_label '{x_plan_rope}'"
                    raise NewKnotException(exception_str)

            # modify all rope attributes in planunits
            self.knot = default_knot_if_None(new_knot)
            for x_plan in self._plan_dict.values():
                x_plan.set_knot(self.knot)

    def set_belief_label(self, belief_label: str):
        old_belief_label = copy_deepcopy(self.belief_label)
        self.settle_believer()
        for plan_obj in self._plan_dict.values():
            plan_obj.belief_label = belief_label
        self.belief_label = belief_label
        self.edit_plan_label(
            old_rope=to_rope(old_belief_label), new_plan_label=self.belief_label
        )
        self.settle_believer()

    def set_max_tree_traverse(self, x_int: int):
        if x_int < 2 or not float(x_int).is_integer():
            raise InvalidBelieverException(
                f"set_max_tree_traverse: '{x_int}' must be number that is 2 or greater"
            )
        else:
            self.max_tree_traverse = x_int

    def _get_relevant_ropes(self, ropes: dict[RopeTerm,]) -> set[RopeTerm]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for x_rope in ropes:
            to_evaluate_list.append(x_rope)
            to_evaluate_hx_dict[x_rope] = "to_evaluate"
        evaluated_ropes = set()

        # while ropes_to_evaluate != [] and count_x <= tree_metrics.label_count:
        # Why count_x? because count_x might be wrong attr to measure
        # nice to avoid infinite loops from programming errors though...
        while to_evaluate_list != []:
            x_rope = to_evaluate_list.pop()
            x_plan = self.get_plan_obj(x_rope)
            for reasonunit_obj in x_plan.reasonunits.values():
                reason_r_context = reasonunit_obj.r_context
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_rope=reason_r_context,
                    rope_type="reasonunit_r_context",
                )
            forefather_ropes = get_forefather_ropes(x_rope)
            for forefather_rope in forefather_ropes:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_rope=forefather_rope,
                    rope_type="forefather",
                )

            evaluated_ropes.add(x_rope)
        return evaluated_ropes

    def _evaluate_relevancy(
        self,
        to_evaluate_list: list[RopeTerm],
        to_evaluate_hx_dict: dict[RopeTerm, int],
        to_evaluate_rope: RopeTerm,
        rope_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_rope) is None:
            to_evaluate_list.append(to_evaluate_rope)
            to_evaluate_hx_dict[to_evaluate_rope] = rope_type

            if rope_type == "reasonunit_r_context":
                ru_r_context_plan = self.get_plan_obj(to_evaluate_rope)
                for (
                    descendant_rope
                ) in ru_r_context_plan.get_descendant_ropes_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_rope=descendant_rope,
                        rope_type="reasonunit_descendant",
                    )

    def all_plans_relevant_to_task_plan(self, rope: RopeTerm) -> bool:
        task_plan_assoc_set = set(self._get_relevant_ropes({rope}))
        all_plans_set = set(self.get_plan_tree_ordered_rope_list())
        return all_plans_set == all_plans_set.intersection(task_plan_assoc_set)

    def get_awardlinks_metrics(self) -> dict[GroupTitle, AwardLink]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.awardlinks_metrics

    def add_to_groupunit_fund_give_fund_take(
        self,
        group_title: GroupTitle,
        awardheir_fund_give: float,
        awardheir_fund_take: float,
    ):
        x_groupunit = self.get_groupunit(group_title)
        if x_groupunit is not None:
            x_groupunit._fund_give += awardheir_fund_give
            x_groupunit._fund_take += awardheir_fund_take

    def add_to_groupunit_fund_agenda_give_take(
        self,
        group_title: GroupTitle,
        awardline_fund_give: float,
        awardline_fund_take: float,
    ):
        x_groupunit = self.get_groupunit(group_title)
        if awardline_fund_give is not None and awardline_fund_take is not None:
            x_groupunit._fund_agenda_give += awardline_fund_give
            x_groupunit._fund_agenda_take += awardline_fund_take

    def add_to_partnerunit_fund_give_take(
        self,
        partnerunit_partner_name: PartnerName,
        fund_give,
        fund_take: float,
        fund_agenda_give: float,
        fund_agenda_take: float,
    ):
        x_partnerunit = self.get_partner(partnerunit_partner_name)
        x_partnerunit.add_fund_give_take(
            fund_give=fund_give,
            fund_take=fund_take,
            fund_agenda_give=fund_agenda_give,
            fund_agenda_take=fund_agenda_take,
        )

    def del_partnerunit(self, partner_name: str):
        self.partners.pop(partner_name)

    def add_partnerunit(
        self,
        partner_name: PartnerName,
        partner_cred_points: int = None,
        partner_debt_points: int = None,
    ):
        x_knot = self.knot
        partnerunit = partnerunit_shop(
            partner_name, partner_cred_points, partner_debt_points, x_knot
        )
        self.set_partnerunit(partnerunit)

    def set_partnerunit(
        self, x_partnerunit: PartnerUnit, auto_set_membership: bool = True
    ):
        if x_partnerunit.knot != self.knot:
            x_partnerunit.knot = self.knot
        if x_partnerunit.respect_bit != self.respect_bit:
            x_partnerunit.respect_bit = self.respect_bit
        if auto_set_membership and x_partnerunit.memberships_exist() is False:
            x_partnerunit.add_membership(x_partnerunit.partner_name)
        self.partners[x_partnerunit.partner_name] = x_partnerunit

    def partner_exists(self, partner_name: PartnerName) -> bool:
        return self.get_partner(partner_name) is not None

    def edit_partnerunit(
        self,
        partner_name: PartnerName,
        partner_cred_points: int = None,
        partner_debt_points: int = None,
    ):
        if self.partners.get(partner_name) is None:
            raise PartnerMissingException(
                f"PartnerUnit '{partner_name}' does not exist."
            )
        x_partnerunit = self.get_partner(partner_name)
        if partner_cred_points is not None:
            x_partnerunit.set_partner_cred_points(partner_cred_points)
        if partner_debt_points is not None:
            x_partnerunit.set_partner_debt_points(partner_debt_points)
        self.set_partnerunit(x_partnerunit)

    def clear_partnerunits_memberships(self):
        for x_partnerunit in self.partners.values():
            x_partnerunit.clear_memberships()

    def get_partner(self, partner_name: PartnerName) -> PartnerUnit:
        return self.partners.get(partner_name)

    def get_partnerunit_group_titles_dict(self) -> dict[GroupTitle, set[PartnerName]]:
        x_dict = {}
        for x_partnerunit in self.partners.values():
            for x_group_title in x_partnerunit._memberships.keys():
                partner_name_set = x_dict.get(x_group_title)
                if partner_name_set is None:
                    x_dict[x_group_title] = {x_partnerunit.partner_name}
                else:
                    partner_name_set.add(x_partnerunit.partner_name)
                    x_dict[x_group_title] = partner_name_set
        return x_dict

    def set_groupunit(self, x_groupunit: GroupUnit):
        x_groupunit.fund_iota = self.fund_iota
        self._groupunits[x_groupunit.group_title] = x_groupunit

    def groupunit_exists(self, group_title: GroupTitle) -> bool:
        return self._groupunits.get(group_title) is not None

    def get_groupunit(self, x_group_title: GroupTitle) -> GroupUnit:
        return self._groupunits.get(x_group_title)

    def create_symmetry_groupunit(self, x_group_title: GroupTitle) -> GroupUnit:
        x_groupunit = groupunit_shop(x_group_title)
        for x_partnerunit in self.partners.values():
            x_membership = membership_shop(
                group_title=x_group_title,
                group_cred_points=x_partnerunit.partner_cred_points,
                group_debt_points=x_partnerunit.partner_debt_points,
                partner_name=x_partnerunit.partner_name,
            )
            x_groupunit.set_membership(x_membership)
        return x_groupunit

    def get_tree_traverse_generated_groupunits(self) -> set[GroupTitle]:
        x_partnerunit_group_titles = set(
            self.get_partnerunit_group_titles_dict().keys()
        )
        all_group_titles = set(self._groupunits.keys())
        return all_group_titles.difference(x_partnerunit_group_titles)

    def _is_plan_rangeroot(self, plan_rope: RopeTerm) -> bool:
        if self.belief_label == plan_rope:
            raise InvalidBelieverException(
                "its difficult to foresee a scenario where planroot is rangeroot"
            )
        parent_rope = get_parent_rope(plan_rope)
        parent_plan = self.get_plan_obj(parent_rope)
        return not parent_plan.is_math()

    def _get_rangeroot_factunits(self) -> list[FactUnit]:
        return [
            fact
            for fact in self.planroot.factunits.values()
            if fact.f_lower is not None
            and fact.f_upper is not None
            and self._is_plan_rangeroot(plan_rope=fact.f_context)
        ]

    def add_fact(
        self,
        f_context: RopeTerm,
        f_state: RopeTerm = None,
        f_lower: float = None,
        f_upper: float = None,
        create_missing_plans: bool = None,
    ):
        f_state = f_context if f_state is None else f_state
        if create_missing_plans:
            self._create_plankid_if_empty(rope=f_context)
            self._create_plankid_if_empty(rope=f_state)

        fact_f_context_plan = self.get_plan_obj(f_context)
        x_planroot = self.get_plan_obj(to_rope(self.belief_label))
        x_f_lower = None
        if f_upper is not None and f_lower is None:
            x_f_lower = x_planroot.factunits.get(f_context).f_lower
        else:
            x_f_lower = f_lower
        x_f_upper = None
        if f_lower is not None and f_upper is None:
            x_f_upper = x_planroot.factunits.get(f_context).f_upper
        else:
            x_f_upper = f_upper
        x_factunit = factunit_shop(
            f_context=f_context,
            f_state=f_state,
            f_lower=x_f_lower,
            f_upper=x_f_upper,
        )

        if fact_f_context_plan.is_math() is False:
            x_planroot.set_factunit(x_factunit)
        # if fact's plan no range or is a "range-root" then allow fact to be set
        elif (
            fact_f_context_plan.is_math()
            and self._is_plan_rangeroot(f_context) is False
        ):
            raise InvalidBelieverException(
                f"Non range-root fact:{f_context} can only be set by range-root fact"
            )
        elif fact_f_context_plan.is_math() and self._is_plan_rangeroot(f_context):
            # WHEN plan is "range-root" identify any reason.r_contexts that are descendants
            # calculate and set those descendant facts
            # example: zietline range (0-, 1.5e9) is range-root
            # example: "zietline,wks" (spllt 10080) is range-descendant
            # there exists a reason r_context "zietline,wks" with case.r_state = "zietline,wks"
            # and (1,2) r_divisor=2 (every other wk)
            #
            # should not set "zietline,wks" fact, only "zietline" fact and
            # "zietline,wks" should be set automatica_lly since there exists a reason
            # that has that r_context.
            x_planroot.set_factunit(x_factunit)

    def get_fact(self, f_context: RopeTerm) -> FactUnit:
        return self.planroot.factunits.get(f_context)

    def del_fact(self, f_context: RopeTerm):
        self.planroot.del_factunit(f_context)

    def get_plan_dict(self, problem: bool = None) -> dict[RopeTerm, PlanUnit]:
        self.settle_believer()
        if not problem:
            return self._plan_dict
        if self._keeps_justified is False:
            exception_str = f"Cannot return problem set because _keeps_justified={self._keeps_justified}."
            raise Exception_keeps_justified(exception_str)

        x_plans = self._plan_dict.values()
        return {
            x_plan.get_plan_rope(): x_plan for x_plan in x_plans if x_plan.problem_bool
        }

    def get_tree_metrics(self) -> TreeMetrics:
        self.settle_believer()
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_label(
            level=self.planroot._level,
            reasons=self.planroot.reasonunits,
            awardlinks=self.planroot.awardlinks,
            uid=self.planroot._uid,
            task=self.planroot.task,
            plan_rope=self.planroot.get_plan_rope(),
        )

        x_plan_list = [self.planroot]
        while x_plan_list != []:
            parent_plan = x_plan_list.pop()
            for plan_kid in parent_plan._kids.values():
                self._eval_tree_metrics(
                    parent_plan, plan_kid, tree_metrics, x_plan_list
                )
        return tree_metrics

    def _eval_tree_metrics(self, parent_plan, plan_kid, tree_metrics, x_plan_list):
        plan_kid._level = parent_plan._level + 1
        tree_metrics.evaluate_label(
            level=plan_kid._level,
            reasons=plan_kid.reasonunits,
            awardlinks=plan_kid.awardlinks,
            uid=plan_kid._uid,
            task=plan_kid.task,
            plan_rope=plan_kid.get_plan_rope(),
        )
        x_plan_list.append(plan_kid)

    def get_plan_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_plan_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        plan_uid_max = tree_metrics.uid_max
        plan_uid_dict = tree_metrics.uid_dict

        for x_plan in self.get_plan_dict().values():
            if x_plan._uid is None or plan_uid_dict.get(x_plan._uid) > 1:
                new_plan_uid_max = plan_uid_max + 1
                self.edit_plan_attr(
                    plan_rope=x_plan.get_plan_rope(), uid=new_plan_uid_max
                )
                plan_uid_max = new_plan_uid_max

    def get_level_count(self, level) -> int:
        tree_metrics = self.get_tree_metrics()
        level_count = None
        try:
            level_count = tree_metrics.level_count[level]
        except KeyError:
            level_count = 0
        return level_count

    def get_reason_r_contexts(self) -> set[RopeTerm]:
        return set(self.get_tree_metrics().reason_r_contexts.keys())

    def get_missing_fact_r_contexts(self) -> dict[RopeTerm, int]:
        tree_metrics = self.get_tree_metrics()
        reason_r_contexts = tree_metrics.reason_r_contexts
        missing_r_contexts = {}
        for r_context, r_context_count in reason_r_contexts.items():
            try:
                self.planroot.factunits[r_context]
            except KeyError:
                missing_r_contexts[r_context] = r_context_count
        return missing_r_contexts

    def add_plan(
        self, plan_rope: RopeTerm, mass: float = None, task: bool = None
    ) -> PlanUnit:
        x_plan_label = get_tail_label(plan_rope, self.knot)
        x_parent_rope = get_parent_rope(plan_rope, self.knot)
        x_planunit = planunit_shop(x_plan_label, mass=mass)
        if task:
            x_planunit.task = True
        self.set_plan(x_planunit, x_parent_rope)
        return x_planunit

    def set_l1_plan(
        self,
        plan_kid: PlanUnit,
        create_missing_plans: bool = None,
        get_rid_of_missing_awardlinks_awardee_titles: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.set_plan(
            plan_kid=plan_kid,
            parent_rope=self.belief_label,
            create_missing_plans=create_missing_plans,
            get_rid_of_missing_awardlinks_awardee_titles=get_rid_of_missing_awardlinks_awardee_titles,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def set_plan(
        self,
        plan_kid: PlanUnit,
        parent_rope: RopeTerm,
        get_rid_of_missing_awardlinks_awardee_titles: bool = None,
        create_missing_plans: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        parent_rope = to_rope(parent_rope, self.knot)
        if LabelTerm(plan_kid.plan_label).is_label(self.knot) is False:
            x_str = (
                f"set_plan failed because '{plan_kid.plan_label}' is not a LabelTerm."
            )
            raise InvalidBelieverException(x_str)

        x_root_label = get_root_label_from_rope(parent_rope, self.knot)
        if self.planroot.plan_label != x_root_label:
            exception_str = f"set_plan failed because parent_rope '{parent_rope}' has an invalid root label. Should be {self.planroot.plan_label}."
            raise InvalidBelieverException(exception_str)

        plan_kid.knot = self.knot
        if plan_kid.belief_label != self.belief_label:
            plan_kid.belief_label = self.belief_label
        if plan_kid.fund_iota != self.fund_iota:
            plan_kid.fund_iota = self.fund_iota
        if not get_rid_of_missing_awardlinks_awardee_titles:
            plan_kid = self._get_filtered_awardlinks_plan(plan_kid)
        plan_kid.set_parent_rope(parent_rope=parent_rope)

        # create any missing plans
        if not create_missing_ancestors and self.plan_exists(parent_rope) is False:
            x_str = f"set_plan failed because '{parent_rope}' plan does not exist."
            raise InvalidBelieverException(x_str)
        parent_rope_plan = self.get_plan_obj(parent_rope, create_missing_ancestors)
        if parent_rope_plan.root is False:
            parent_rope_plan
        parent_rope_plan.add_kid(plan_kid)

        kid_rope = self.make_rope(parent_rope, plan_kid.plan_label)
        if adoptees is not None:
            mass_sum = 0
            for adoptee_plan_label in adoptees:
                adoptee_rope = self.make_rope(parent_rope, adoptee_plan_label)
                adoptee_plan = self.get_plan_obj(adoptee_rope)
                mass_sum += adoptee_plan.mass
                new_adoptee_parent_rope = self.make_rope(kid_rope, adoptee_plan_label)
                self.set_plan(adoptee_plan, new_adoptee_parent_rope)
                self.edit_plan_attr(new_adoptee_parent_rope, mass=adoptee_plan.mass)
                self.del_plan_obj(adoptee_rope)

            if bundling:
                self.edit_plan_attr(kid_rope, mass=mass_sum)

        if create_missing_plans:
            self._create_missing_plans(rope=kid_rope)

    def _get_filtered_awardlinks_plan(self, x_plan: PlanUnit) -> PlanUnit:
        _awardlinks_to_delete = [
            _awardlink_awardee_title
            for _awardlink_awardee_title in x_plan.awardlinks.keys()
            if self.get_partnerunit_group_titles_dict().get(_awardlink_awardee_title)
            is None
        ]
        for _awardlink_awardee_title in _awardlinks_to_delete:
            x_plan.awardlinks.pop(_awardlink_awardee_title)
        if x_plan.laborunit is not None:
            _laborlinks_to_delete = [
                _laborlink_labor_title
                for _laborlink_labor_title in x_plan.laborunit._laborlinks
                if self.get_partnerunit_group_titles_dict().get(_laborlink_labor_title)
                is None
            ]
            for _laborlink_labor_title in _laborlinks_to_delete:
                x_plan.laborunit.del_laborlink(_laborlink_labor_title)
        return x_plan

    def _create_missing_plans(self, rope):
        self._set_plan_dict()
        posted_plan = self.get_plan_obj(rope)

        for x_reason in posted_plan.reasonunits.values():
            self._create_plankid_if_empty(rope=x_reason.r_context)
            for case_x in x_reason.cases.values():
                self._create_plankid_if_empty(rope=case_x.r_state)

    def _create_plankid_if_empty(self, rope: RopeTerm):
        if self.plan_exists(rope) is False:
            self.add_plan(rope)

    def del_plan_obj(self, rope: RopeTerm, del_children: bool = True):
        if rope == self.planroot.get_plan_rope():
            raise InvalidBelieverException("Planroot cannot be deleted")
        parent_rope = get_parent_rope(rope)
        if self.plan_exists(rope):
            if not del_children:
                self._shift_plan_kids(x_rope=rope)
            parent_plan = self.get_plan_obj(parent_rope)
            parent_plan.del_kid(get_tail_label(rope, self.knot))
        self.settle_believer()

    def _shift_plan_kids(self, x_rope: RopeTerm):
        parent_rope = get_parent_rope(x_rope)
        d_temp_plan = self.get_plan_obj(x_rope)
        for kid in d_temp_plan._kids.values():
            self.set_plan(kid, parent_rope=parent_rope)

    def set_believer_name(self, new_believer_name):
        self.believer_name = new_believer_name

    def edit_plan_label(self, old_rope: RopeTerm, new_plan_label: LabelTerm):
        if self.knot in new_plan_label:
            exception_str = f"Cannot modify '{old_rope}' because new_plan_label {new_plan_label} contains knot {self.knot}"
            raise InvalidLabelException(exception_str)
        if self.plan_exists(old_rope) is False:
            raise InvalidBelieverException(f"Plan {old_rope=} does not exist")

        parent_rope = get_parent_rope(rope=old_rope)
        new_rope = (
            self.make_rope(new_plan_label)
            if parent_rope == ""
            else self.make_rope(parent_rope, new_plan_label)
        )
        if old_rope != new_rope:
            if parent_rope == "":
                self.planroot.set_plan_label(new_plan_label)
            else:
                self._non_root_plan_label_edit(old_rope, new_plan_label, parent_rope)
            self._planroot_find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    def _non_root_plan_label_edit(
        self, old_rope: RopeTerm, new_plan_label: LabelTerm, parent_rope: RopeTerm
    ):
        x_plan = self.get_plan_obj(old_rope)
        x_plan.set_plan_label(new_plan_label)
        x_plan.parent_rope = parent_rope
        plan_parent = self.get_plan_obj(get_parent_rope(old_rope))
        plan_parent._kids.pop(get_tail_label(old_rope, self.knot))
        plan_parent._kids[x_plan.plan_label] = x_plan

    def _planroot_find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.planroot.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

        plan_iter_list = [self.planroot]
        while plan_iter_list != []:
            listed_plan = plan_iter_list.pop()
            # add all plan_children in plan list
            if listed_plan._kids is not None:
                for plan_kid in listed_plan._kids.values():
                    plan_iter_list.append(plan_kid)
                    if is_sub_rope(plan_kid.parent_rope, sub_rope=old_rope):
                        plan_kid.parent_rope = rebuild_rope(
                            subj_rope=plan_kid.parent_rope,
                            old_rope=old_rope,
                            new_rope=new_rope,
                        )
                    plan_kid.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    def _set_planattrholder_case_ranges(self, x_planattrholder: PlanAttrHolder):
        case_plan = self.get_plan_obj(x_planattrholder.reason_case)
        x_planattrholder.set_case_range_influenced_by_case_plan(
            r_lower=case_plan.begin,
            r_upper=case_plan.close,
            case_denom=case_plan.denom,
        )

    def edit_reason(
        self,
        plan_rope: RopeTerm,
        reason_r_context: RopeTerm = None,
        reason_case: RopeTerm = None,
        r_lower: float = None,
        reason_r_upper: float = None,
        r_divisor: int = None,
    ):
        self.edit_plan_attr(
            plan_rope=plan_rope,
            reason_r_context=reason_r_context,
            reason_case=reason_case,
            r_lower=r_lower,
            reason_r_upper=reason_r_upper,
            r_divisor=r_divisor,
        )

    def edit_plan_attr(
        self,
        plan_rope: RopeTerm,
        mass: int = None,
        uid: int = None,
        reason: ReasonUnit = None,
        reason_r_context: RopeTerm = None,
        reason_case: RopeTerm = None,
        r_lower: float = None,
        reason_r_upper: float = None,
        r_divisor: int = None,
        reason_del_case_r_context: RopeTerm = None,
        reason_del_case_r_state: RopeTerm = None,
        reason_r_plan_active_requisite: str = None,
        laborunit: LaborUnit = None,
        healerlink: HealerLink = None,
        begin: float = None,
        close: float = None,
        gogo_want: float = None,
        stop_want: float = None,
        addin: float = None,
        numor: float = None,
        denom: float = None,
        morph: bool = None,
        task: bool = None,
        factunit: FactUnit = None,
        descendant_task_count: int = None,
        all_partner_cred: bool = None,
        all_partner_debt: bool = None,
        awardlink: AwardLink = None,
        awardlink_del: GroupTitle = None,
        is_expanded: bool = None,
        problem_bool: bool = None,
    ):
        if healerlink is not None:
            for x_healer_name in healerlink._healer_names:
                if self.get_partnerunit_group_titles_dict().get(x_healer_name) is None:
                    exception_str = f"Plan cannot edit healerlink because group_title '{x_healer_name}' does not exist as group in Believer"
                    raise healerlink_group_title_Exception(exception_str)

        x_planattrholder = planattrholder_shop(
            mass=mass,
            uid=uid,
            reason=reason,
            reason_r_context=reason_r_context,
            reason_case=reason_case,
            r_lower=r_lower,
            reason_r_upper=reason_r_upper,
            r_divisor=r_divisor,
            reason_del_case_r_context=reason_del_case_r_context,
            reason_del_case_r_state=reason_del_case_r_state,
            reason_r_plan_active_requisite=reason_r_plan_active_requisite,
            laborunit=laborunit,
            healerlink=healerlink,
            begin=begin,
            close=close,
            gogo_want=gogo_want,
            stop_want=stop_want,
            addin=addin,
            numor=numor,
            denom=denom,
            morph=morph,
            descendant_task_count=descendant_task_count,
            all_partner_cred=all_partner_cred,
            all_partner_debt=all_partner_debt,
            awardlink=awardlink,
            awardlink_del=awardlink_del,
            is_expanded=is_expanded,
            task=task,
            factunit=factunit,
            problem_bool=problem_bool,
        )
        if reason_case is not None:
            self._set_planattrholder_case_ranges(x_planattrholder)
        x_plan = self.get_plan_obj(plan_rope)
        x_plan._set_attrs_to_planunit(plan_attr=x_planattrholder)

    def get_agenda_dict(
        self, necessary_r_context: RopeTerm = None
    ) -> dict[RopeTerm, PlanUnit]:
        self.settle_believer()
        return {
            x_plan.get_plan_rope(): x_plan
            for x_plan in self._plan_dict.values()
            if x_plan.is_agenda_plan(necessary_r_context)
        }

    def get_all_tasks(self) -> dict[RopeTerm, PlanUnit]:
        self.settle_believer()
        all_plans = self._plan_dict.values()
        return {x_plan.get_plan_rope(): x_plan for x_plan in all_plans if x_plan.task}

    def set_agenda_chore_complete(self, chore_rope: RopeTerm, r_context: RopeTerm):
        task_plan = self.get_plan_obj(chore_rope)
        task_plan.set_factunit_to_complete(self.planroot.factunits[r_context])

    def get_credit_ledger_debt_ledger(
        self,
    ) -> tuple[dict[str, float], dict[str, float]]:
        credit_ledger = {}
        debt_ledger = {}
        for x_partnerunit in self.partners.values():
            credit_ledger[x_partnerunit.partner_name] = (
                x_partnerunit.partner_cred_points
            )
            debt_ledger[x_partnerunit.partner_name] = x_partnerunit.partner_debt_points
        return credit_ledger, debt_ledger

    def _allot_offtrack_fund(self):
        self._add_to_partnerunits_fund_give_take(self._offtrack_fund)

    def get_partnerunits_partner_cred_points_sum(self) -> float:
        return sum(
            partnerunit.get_partner_cred_points()
            for partnerunit in self.partners.values()
        )

    def get_partnerunits_partner_debt_points_sum(self) -> float:
        return sum(
            partnerunit.get_partner_debt_points()
            for partnerunit in self.partners.values()
        )

    def _add_to_partnerunits_fund_give_take(self, plan_fund_share: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        fund_give_allot = allot_scale(credor_ledger, plan_fund_share, self.fund_iota)
        fund_take_allot = allot_scale(debtor_ledger, plan_fund_share, self.fund_iota)
        for x_partner_name, partner_fund_give in fund_give_allot.items():
            self.get_partner(x_partner_name).add_fund_give(partner_fund_give)
            # if there is no differentiated agenda (what factunits exist do not change agenda)
            if not self._reason_r_contexts:
                self.get_partner(x_partner_name).add_fund_agenda_give(partner_fund_give)
        for x_partner_name, partner_fund_take in fund_take_allot.items():
            self.get_partner(x_partner_name).add_fund_take(partner_fund_take)
            # if there is no differentiated agenda (what factunits exist do not change agenda)
            if not self._reason_r_contexts:
                self.get_partner(x_partner_name).add_fund_agenda_take(partner_fund_take)

    def _add_to_partnerunits_fund_agenda_give_take(self, plan_fund_share: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        fund_give_allot = allot_scale(credor_ledger, plan_fund_share, self.fund_iota)
        fund_take_allot = allot_scale(debtor_ledger, plan_fund_share, self.fund_iota)
        for x_partner_name, partner_fund_give in fund_give_allot.items():
            self.get_partner(x_partner_name).add_fund_agenda_give(partner_fund_give)
        for x_partner_name, partner_fund_take in fund_take_allot.items():
            self.get_partner(x_partner_name).add_fund_agenda_take(partner_fund_take)

    def _reset_groupunits_fund_give_take(self):
        for groupunit_obj in self._groupunits.values():
            groupunit_obj.clear_fund_give_take()

    def _set_groupunits_fund_share(self, awardheirs: dict[GroupTitle, AwardLink]):
        for awardlink_obj in awardheirs.values():
            x_awardee_title = awardlink_obj.awardee_title
            if not self.groupunit_exists(x_awardee_title):
                self.set_groupunit(self.create_symmetry_groupunit(x_awardee_title))
            self.add_to_groupunit_fund_give_fund_take(
                group_title=awardlink_obj.awardee_title,
                awardheir_fund_give=awardlink_obj._fund_give,
                awardheir_fund_take=awardlink_obj._fund_take,
            )

    def _allot_fund_believer_agenda(self):
        for plan in self._plan_dict.values():
            # If there are no awardlines associated with plan
            # allot fund_share via general partnerunit
            # cred ratio and debt ratio
            # if plan.is_agenda_plan() and plan._awardlines == {}:
            if plan.is_agenda_plan():
                if plan.awardheir_exists():
                    for x_awardline in plan._awardlines.values():
                        self.add_to_groupunit_fund_agenda_give_take(
                            group_title=x_awardline.awardee_title,
                            awardline_fund_give=x_awardline._fund_give,
                            awardline_fund_take=x_awardline._fund_take,
                        )
                else:
                    self._add_to_partnerunits_fund_agenda_give_take(
                        plan.get_fund_share()
                    )

    def _allot_groupunits_fund(self):
        for x_groupunit in self._groupunits.values():
            x_groupunit._set_membership_fund_give_fund_take()
            for x_membership in x_groupunit._memberships.values():
                self.add_to_partnerunit_fund_give_take(
                    partnerunit_partner_name=x_membership.partner_name,
                    fund_give=x_membership._fund_give,
                    fund_take=x_membership._fund_take,
                    fund_agenda_give=x_membership._fund_agenda_give,
                    fund_agenda_take=x_membership._fund_agenda_take,
                )

    def _set_partnerunits_fund_agenda_ratios(self):
        fund_agenda_ratio_give_sum = sum(
            x_partnerunit._fund_agenda_give for x_partnerunit in self.partners.values()
        )
        fund_agenda_ratio_take_sum = sum(
            x_partnerunit._fund_agenda_take for x_partnerunit in self.partners.values()
        )
        x_partnerunits_partner_cred_points_sum = (
            self.get_partnerunits_partner_cred_points_sum()
        )
        x_partnerunits_partner_debt_points_sum = (
            self.get_partnerunits_partner_debt_points_sum()
        )
        for x_partnerunit in self.partners.values():
            x_partnerunit.set_fund_agenda_ratio_give_take(
                fund_agenda_ratio_give_sum=fund_agenda_ratio_give_sum,
                fund_agenda_ratio_take_sum=fund_agenda_ratio_take_sum,
                partnerunits_partner_cred_points_sum=x_partnerunits_partner_cred_points_sum,
                partnerunits_partner_debt_points_sum=x_partnerunits_partner_debt_points_sum,
            )

    def _reset_partnerunit_fund_give_take(self):
        for partnerunit in self.partners.values():
            partnerunit.clear_fund_give_take()

    def plan_exists(self, rope: RopeTerm) -> bool:
        if rope in {"", None}:
            return False
        root_rope_plan_label = get_root_label_from_rope(rope, self.knot)
        if root_rope_plan_label != self.planroot.plan_label:
            return False

        labels = get_all_rope_labels(rope, knot=self.knot)
        root_rope_plan_label = labels.pop(0)
        if labels == []:
            return True

        plan_label = labels.pop(0)
        x_plan = self.planroot.get_kid(plan_label)
        if x_plan is None:
            return False
        while labels != []:
            plan_label = labels.pop(0)
            x_plan = x_plan.get_kid(plan_label)
            if x_plan is None:
                return False
        return True

    def get_plan_obj(self, rope: RopeTerm, if_missing_create: bool = False) -> PlanUnit:
        if rope is None:
            raise InvalidBelieverException("get_plan_obj received rope=None")
        if self.plan_exists(rope) is False and not if_missing_create:
            raise InvalidBelieverException(f"get_plan_obj failed. no plan at '{rope}'")
        labelterms = get_all_rope_labels(rope, knot=self.knot)
        if len(labelterms) == 1:
            return self.planroot

        labelterms.pop(0)
        plan_label = labelterms.pop(0)
        x_plan = self.planroot.get_kid(plan_label, if_missing_create)
        while labelterms != []:
            x_plan = x_plan.get_kid(labelterms.pop(0), if_missing_create)

        return x_plan

    def get_plan_ranged_kids(
        self, plan_rope: str, x_gogo_calc: float = None, x_stop_calc: float = None
    ) -> dict[PlanUnit]:
        x_plan = self.get_plan_obj(plan_rope)
        return x_plan.get_kids_in_range(x_gogo_calc, x_stop_calc)

    def get_inheritor_plan_list(
        self, math_rope: RopeTerm, inheritor_rope: RopeTerm
    ) -> list[PlanUnit]:
        plan_ropes = all_ropeterms_between(math_rope, inheritor_rope)
        return [self.get_plan_obj(x_plan_rope) for x_plan_rope in plan_ropes]

    def _set_plan_dict(self):
        plan_list = [self.get_plan_obj(to_rope(self.belief_label, self.knot))]
        while plan_list != []:
            x_plan = plan_list.pop()
            x_plan.clear_gogo_calc_stop_calc()
            for plan_kid in x_plan._kids.values():
                plan_kid.set_parent_rope(x_plan.get_plan_rope())
                plan_kid.set_level(x_plan._level)
                plan_list.append(plan_kid)
            self._plan_dict[x_plan.get_plan_rope()] = x_plan
            for x_reason_r_context in x_plan.reasonunits.keys():
                self._reason_r_contexts.add(x_reason_r_context)

    def _raise_gogo_calc_stop_calc_exception(self, plan_rope: RopeTerm):
        exception_str = f"Error has occurred, Plan '{plan_rope}' is having _gogo_calc and _stop_calc attributes set twice"
        raise _gogo_calc_stop_calc_Exception(exception_str)

    def _distribute_math_attrs(self, math_plan: PlanUnit):
        single_range_plan_list = [math_plan]
        while single_range_plan_list != []:
            r_plan = single_range_plan_list.pop()
            if r_plan._range_evaluated:
                self._raise_gogo_calc_stop_calc_exception(r_plan.get_plan_rope())
            if r_plan.is_math():
                r_plan._gogo_calc = r_plan.begin
                r_plan._stop_calc = r_plan.close
            else:
                parent_rope = get_parent_rope(
                    rope=r_plan.get_plan_rope(), knot=r_plan.knot
                )
                parent_plan = self.get_plan_obj(parent_rope)
                r_plan._gogo_calc = parent_plan._gogo_calc
                r_plan._stop_calc = parent_plan._stop_calc
                self._range_inheritors[r_plan.get_plan_rope()] = (
                    math_plan.get_plan_rope()
                )
            r_plan._mold_gogo_calc_stop_calc()
            single_range_plan_list.extend(iter(r_plan._kids.values()))

    def _set_plantree_range_attrs(self):
        for x_plan in self._plan_dict.values():
            if x_plan.is_math():
                self._distribute_math_attrs(x_plan)

            if (
                not x_plan.is_kidless()
                and x_plan.get_kids_mass_sum() == 0
                and x_plan.mass != 0
            ):
                self._offtrack_kids_mass_set.add(x_plan.get_plan_rope())

    def _set_groupunit_partnerunit_funds(self, keep_exceptions):
        for x_plan in self._plan_dict.values():
            x_plan.set_awardheirs_fund_give_fund_take()
            if x_plan.is_kidless():
                self._set_ancestors_task_fund_keep_attrs(
                    x_plan.get_plan_rope(), keep_exceptions
                )
                self._allot_fund_share(x_plan)

    def _set_ancestors_task_fund_keep_attrs(
        self, rope: RopeTerm, keep_exceptions: bool = False
    ):
        x_descendant_task_count = 0
        child_awardlines = None
        group_everyone = None
        ancestor_ropes = get_ancestor_ropes(rope, self.knot)
        keep_justified_by_problem = True
        healerlink_count = 0

        while ancestor_ropes != []:
            youngest_rope = ancestor_ropes.pop(0)
            x_plan_obj = self.get_plan_obj(youngest_rope)
            x_plan_obj.add_to_descendant_task_count(x_descendant_task_count)
            if x_plan_obj.is_kidless():
                x_plan_obj.set_kidless_awardlines()
                child_awardlines = x_plan_obj._awardlines
            else:
                x_plan_obj.set_awardlines(child_awardlines)

            if x_plan_obj._chore:
                x_descendant_task_count += 1

            if (
                group_everyone != False
                and x_plan_obj._all_partner_cred != False
                and x_plan_obj._all_partner_debt != False
                and x_plan_obj._awardheirs != {}
            ) or (
                group_everyone != False
                and x_plan_obj._all_partner_cred is False
                and x_plan_obj._all_partner_debt is False
            ):
                group_everyone = False
            elif group_everyone != False:
                group_everyone = True
            x_plan_obj._all_partner_cred = group_everyone
            x_plan_obj._all_partner_debt = group_everyone

            if x_plan_obj.healerlink.any_healer_name_exists():
                keep_justified_by_problem = False
                healerlink_count += 1
                self._sum_healerlink_share += x_plan_obj.get_fund_share()
            if x_plan_obj.problem_bool:
                keep_justified_by_problem = True

        if keep_justified_by_problem is False or healerlink_count > 1:
            if keep_exceptions:
                exception_str = f"PlanUnit '{rope}' cannot sponsor ancestor keeps."
                raise Exception_keeps_justified(exception_str)
            self._keeps_justified = False

    def _clear_plantree_fund_and_active_status_attrs(self):
        for x_plan in self._plan_dict.values():
            x_plan.clear_awardlines()
            x_plan.clear_descendant_task_count()
            x_plan.clear_all_partner_cred_debt()

    def _set_kids_active_status_attrs(self, x_plan: PlanUnit, parent_plan: PlanUnit):
        x_plan.set_reasonheirs(self._plan_dict, parent_plan._reasonheirs)
        x_plan.set_range_factheirs(self._plan_dict, self._range_inheritors)
        tt_count = self._tree_traverse_count
        x_plan.set_active_attrs(tt_count, self._groupunits, self.believer_name)

    def _allot_fund_share(self, plan: PlanUnit):
        if plan.awardheir_exists():
            self._set_groupunits_fund_share(plan._awardheirs)
        elif plan.awardheir_exists() is False:
            self._add_to_partnerunits_fund_give_take(plan.get_fund_share())

    def _create_groupunits_metrics(self):
        self._groupunits = {}
        for (
            group_title,
            partner_name_set,
        ) in self.get_partnerunit_group_titles_dict().items():
            x_groupunit = groupunit_shop(group_title, knot=self.knot)
            for x_partner_name in partner_name_set:
                x_membership = self.get_partner(x_partner_name).get_membership(
                    group_title
                )
                x_groupunit.set_membership(x_membership)
                self.set_groupunit(x_groupunit)

    def _set_partnerunit_groupunit_respect_ledgers(self):
        self.credor_respect = validate_respect_num(self.credor_respect)
        self.debtor_respect = validate_respect_num(self.debtor_respect)
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        credor_allot = allot_scale(credor_ledger, self.credor_respect, self.respect_bit)
        debtor_allot = allot_scale(debtor_ledger, self.debtor_respect, self.respect_bit)
        for x_partner_name, partner_credor_pool in credor_allot.items():
            self.get_partner(x_partner_name).set_credor_pool(partner_credor_pool)
        for x_partner_name, partner_debtor_pool in debtor_allot.items():
            self.get_partner(x_partner_name).set_debtor_pool(partner_debtor_pool)
        self._create_groupunits_metrics()
        self._reset_partnerunit_fund_give_take()

    def _clear_plan_dict_and_believer_obj_settle_attrs(self):
        self._plan_dict = {self.planroot.get_plan_rope(): self.planroot}
        self._rational = False
        self._tree_traverse_count = 0
        self._offtrack_kids_mass_set = set()
        self._reason_r_contexts = set()
        self._range_inheritors = {}
        self._keeps_justified = True
        self._keeps_buildable = False
        self._sum_healerlink_share = 0
        self._keep_dict = {}
        self._healers_dict = {}

    def _set_plantree_factheirs_laborheirs_awardheirs(self):
        for x_plan in get_sorted_plan_list(list(self._plan_dict.values())):
            if x_plan.root:
                x_plan.set_factheirs(x_plan.factunits)
                x_plan.set_planroot_inherit_reasonheirs()
                x_plan.set_laborheir(None, self._groupunits)
                x_plan.inherit_awardheirs()
            else:
                parent_plan = self.get_plan_obj(x_plan.parent_rope)
                x_plan.set_factheirs(parent_plan._factheirs)
                x_plan.set_laborheir(parent_plan._laborheir, self._groupunits)
                x_plan.inherit_awardheirs(parent_plan._awardheirs)
            x_plan.set_awardheirs_fund_give_fund_take()

    def settle_believer(self, keep_exceptions: bool = False):
        self._clear_plan_dict_and_believer_obj_settle_attrs()
        self._set_plan_dict()
        self._set_plantree_range_attrs()
        self._set_partnerunit_groupunit_respect_ledgers()
        self._clear_partnerunit_fund_attrs()
        self._clear_plantree_fund_and_active_status_attrs()
        self._set_plantree_factheirs_laborheirs_awardheirs()

        max_count = self.max_tree_traverse
        while not self._rational and self._tree_traverse_count < max_count:
            self._set_plantree_active_status_attrs()
            self._set_rational_attr()
            self._tree_traverse_count += 1

        self._set_plantree_fund_attrs(self.planroot)
        self._set_groupunit_partnerunit_funds(keep_exceptions)
        self._set_partnerunit_fund_related_attrs()
        self._set_believer_keep_attrs()

    def _set_plantree_active_status_attrs(self):
        for x_plan in get_sorted_plan_list(list(self._plan_dict.values())):
            if x_plan.root:
                tt_count = self._tree_traverse_count
                root_plan = self.planroot
                root_plan.set_active_attrs(
                    tt_count, self._groupunits, self.believer_name
                )
            else:
                parent_plan = self.get_plan_obj(x_plan.parent_rope)
                self._set_kids_active_status_attrs(x_plan, parent_plan)

    def _set_plantree_fund_attrs(self, root_plan: PlanUnit):
        root_plan.set_fund_attr(0, self.fund_pool, self.fund_pool)
        # no function recursion, recursion by iterateing over list that can be added to by iterations
        cache_plan_list = [root_plan]
        while cache_plan_list != []:
            parent_plan = cache_plan_list.pop()
            kids_plans = parent_plan._kids.items()
            x_ledger = {x_rope: plan_kid.mass for x_rope, plan_kid in kids_plans}
            parent_fund_num = parent_plan._fund_cease - parent_plan._fund_onset
            alloted_fund_num = allot_scale(x_ledger, parent_fund_num, self.fund_iota)

            fund_onset = None
            fund_cease = None
            for x_plan in parent_plan._kids.values():
                if fund_onset is None:
                    fund_onset = parent_plan._fund_onset
                    fund_cease = fund_onset + alloted_fund_num.get(x_plan.plan_label)
                else:
                    fund_onset = fund_cease
                    fund_cease += alloted_fund_num.get(x_plan.plan_label)
                x_plan.set_fund_attr(fund_onset, fund_cease, self.fund_pool)
                cache_plan_list.append(x_plan)

    def _set_rational_attr(self):
        any_plan_active_status_has_altered = False
        for plan in self._plan_dict.values():
            if plan._active_hx.get(self._tree_traverse_count) is not None:
                any_plan_active_status_has_altered = True

        if any_plan_active_status_has_altered is False:
            self._rational = True

    def _set_partnerunit_fund_related_attrs(self):
        self.set_offtrack_fund()
        self._allot_offtrack_fund()
        self._allot_fund_believer_agenda()
        self._allot_groupunits_fund()
        self._set_partnerunits_fund_agenda_ratios()

    def _set_believer_keep_attrs(self):
        self._set_keep_dict()
        self._healers_dict = self._get_healers_dict()
        self._keeps_buildable = self._get_buildable_keeps()

    def _set_keep_dict(self):
        if self._keeps_justified is False:
            self._sum_healerlink_share = 0
        for x_plan in self._plan_dict.values():
            if self._sum_healerlink_share == 0:
                x_plan._healerlink_ratio = 0
            else:
                x_sum = self._sum_healerlink_share
                x_plan._healerlink_ratio = x_plan.get_fund_share() / x_sum
            if self._keeps_justified and x_plan.healerlink.any_healer_name_exists():
                self._keep_dict[x_plan.get_plan_rope()] = x_plan

    def _get_healers_dict(self) -> dict[HealerName, dict[RopeTerm, PlanUnit]]:
        _healers_dict = {}
        for x_keep_rope, x_keep_plan in self._keep_dict.items():
            for x_healer_name in x_keep_plan.healerlink._healer_names:
                x_groupunit = self.get_groupunit(x_healer_name)
                for x_partner_name in x_groupunit._memberships.keys():
                    if _healers_dict.get(x_partner_name) is None:
                        _healers_dict[x_partner_name] = {x_keep_rope: x_keep_plan}
                    else:
                        healer_dict = _healers_dict.get(x_partner_name)
                        healer_dict[x_keep_rope] = x_keep_plan
        return _healers_dict

    def _get_buildable_keeps(self) -> bool:
        return all(
            ropeterm_valid_dir_path(keep_rope, self.knot) != False
            for keep_rope in self._keep_dict.keys()
        )

    def _clear_partnerunit_fund_attrs(self):
        self._reset_groupunits_fund_give_take()
        self._reset_partnerunit_fund_give_take()

    def get_plan_tree_ordered_rope_list(
        self, no_range_descendants: bool = False
    ) -> list[RopeTerm]:
        plan_list = list(self.get_plan_dict().values())
        label_dict = {
            plan.get_plan_rope().lower(): plan.get_plan_rope() for plan in plan_list
        }
        label_same_capitalization_ordered_list = sorted(list(label_dict))
        label_orginalcapitalization_ordered_list = [
            label_dict[label_l] for label_l in label_same_capitalization_ordered_list
        ]

        list_x = []
        for rope in label_orginalcapitalization_ordered_list:
            if not no_range_descendants:
                list_x.append(rope)
            else:
                anc_list = get_ancestor_ropes(rope=rope)
                if len(anc_list) == 1:
                    list_x.append(rope)
                elif len(anc_list) == 2:
                    if self.planroot.begin is None and self.planroot.close is None:
                        list_x.append(rope)
                else:
                    parent_plan = self.get_plan_obj(rope=anc_list[1])
                    if parent_plan.begin is None and parent_plan.close is None:
                        list_x.append(rope)

        return list_x

    def get_factunits_dict(self) -> dict[str, str]:
        x_dict = {}
        if self.planroot.factunits is not None:
            for fact_rope, fact_obj in self.planroot.factunits.items():
                x_dict[fact_rope] = fact_obj.get_dict()
        return x_dict

    def get_partnerunits_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {}
        if self.partners is not None:
            for partner_name, partner_obj in self.partners.items():
                x_dict[partner_name] = partner_obj.get_dict(all_attrs)
        return x_dict

    def get_dict(self) -> dict[str, str]:
        x_dict = {
            "partners": self.get_partnerunits_dict(),
            "tally": self.tally,
            "fund_pool": self.fund_pool,
            "fund_iota": self.fund_iota,
            "respect_bit": self.respect_bit,
            "penny": self.penny,
            "believer_name": self.believer_name,
            "belief_label": self.belief_label,
            "max_tree_traverse": self.max_tree_traverse,
            "knot": self.knot,
            "planroot": self.planroot.get_dict(),
        }
        if self.credor_respect is not None:
            x_dict["credor_respect"] = self.credor_respect
        if self.debtor_respect is not None:
            x_dict["debtor_respect"] = self.debtor_respect
        if self.last_pack_id is not None:
            x_dict["last_pack_id"] = self.last_pack_id

        return x_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())

    def set_dominate_task_plan(self, plan_kid: PlanUnit):
        plan_kid.task = True
        self.set_plan(
            plan_kid=plan_kid,
            parent_rope=self.make_rope(plan_kid.parent_rope),
            get_rid_of_missing_awardlinks_awardee_titles=True,
            create_missing_plans=True,
        )

    def set_offtrack_fund(self) -> float:
        mass_set = self._offtrack_kids_mass_set
        self._offtrack_fund = sum(
            self.get_plan_obj(x_ropeterm).get_fund_share() for x_ropeterm in mass_set
        )


def believerunit_shop(
    believer_name: BelieverName = None,
    belief_label: BeliefLabel = None,
    knot: str = None,
    fund_pool: FundNum = None,
    fund_iota: FundIota = None,
    respect_bit: BitNum = None,
    penny: PennyNum = None,
    tally: float = None,
) -> BelieverUnit:
    believer_name = "" if believer_name is None else believer_name
    belief_label = get_default_belief_label() if belief_label is None else belief_label
    x_believer = BelieverUnit(
        believer_name=believer_name,
        tally=get_1_if_None(tally),
        belief_label=belief_label,
        partners=get_empty_dict_if_None(),
        _groupunits={},
        knot=default_knot_if_None(knot),
        credor_respect=validate_respect_num(),
        debtor_respect=validate_respect_num(),
        fund_pool=validate_fund_pool(fund_pool),
        fund_iota=default_fund_iota_if_None(fund_iota),
        respect_bit=default_RespectBit_if_None(respect_bit),
        penny=filter_penny(penny),
        _plan_dict=get_empty_dict_if_None(),
        _keep_dict=get_empty_dict_if_None(),
        _healers_dict=get_empty_dict_if_None(),
        _keeps_justified=get_False_if_None(),
        _keeps_buildable=get_False_if_None(),
        _sum_healerlink_share=get_0_if_None(),
        _offtrack_kids_mass_set=set(),
        _reason_r_contexts=set(),
        _range_inheritors={},
    )
    x_believer.planroot = planunit_shop(
        root=True,
        _uid=1,
        _level=0,
        belief_label=x_believer.belief_label,
        knot=x_believer.knot,
        fund_iota=x_believer.fund_iota,
        parent_rope="",
    )
    x_believer.set_max_tree_traverse(3)
    x_believer._rational = False
    return x_believer


def get_from_json(x_believer_json: str) -> BelieverUnit:
    return get_from_dict(get_dict_from_json(x_believer_json))


def get_from_dict(believer_dict: dict) -> BelieverUnit:
    x_believer = believerunit_shop()
    x_believer.set_believer_name(obj_from_believer_dict(believer_dict, "believer_name"))
    x_believer.tally = obj_from_believer_dict(believer_dict, "tally")
    x_believer.set_max_tree_traverse(
        obj_from_believer_dict(believer_dict, "max_tree_traverse")
    )
    x_believer.belief_label = obj_from_believer_dict(believer_dict, "belief_label")
    x_believer.planroot.plan_label = obj_from_believer_dict(
        believer_dict, "belief_label"
    )
    believer_knot = obj_from_believer_dict(believer_dict, "knot")
    x_believer.knot = default_knot_if_None(believer_knot)
    x_believer.fund_pool = validate_fund_pool(
        obj_from_believer_dict(believer_dict, "fund_pool")
    )
    x_believer.fund_iota = default_fund_iota_if_None(
        obj_from_believer_dict(believer_dict, "fund_iota")
    )
    x_believer.respect_bit = default_RespectBit_if_None(
        obj_from_believer_dict(believer_dict, "respect_bit")
    )
    x_believer.penny = filter_penny(obj_from_believer_dict(believer_dict, "penny"))
    x_believer.credor_respect = obj_from_believer_dict(believer_dict, "credor_respect")
    x_believer.debtor_respect = obj_from_believer_dict(believer_dict, "debtor_respect")
    x_believer.last_pack_id = obj_from_believer_dict(believer_dict, "last_pack_id")
    x_knot = x_believer.knot
    x_partners = obj_from_believer_dict(believer_dict, "partners", x_knot).values()
    for x_partnerunit in x_partners:
        x_believer.set_partnerunit(x_partnerunit)
    create_planroot_from_believer_dict(x_believer, believer_dict)
    return x_believer


def create_planroot_from_believer_dict(x_believer: BelieverUnit, believer_dict: dict):
    planroot_dict = believer_dict.get("planroot")
    x_believer.planroot = planunit_shop(
        root=True,
        plan_label=x_believer.belief_label,
        parent_rope="",
        _level=0,
        _uid=get_obj_from_plan_dict(planroot_dict, "_uid"),
        mass=get_obj_from_plan_dict(planroot_dict, "mass"),
        begin=get_obj_from_plan_dict(planroot_dict, "begin"),
        close=get_obj_from_plan_dict(planroot_dict, "close"),
        numor=get_obj_from_plan_dict(planroot_dict, "numor"),
        denom=get_obj_from_plan_dict(planroot_dict, "denom"),
        morph=get_obj_from_plan_dict(planroot_dict, "morph"),
        gogo_want=get_obj_from_plan_dict(planroot_dict, "gogo_want"),
        stop_want=get_obj_from_plan_dict(planroot_dict, "stop_want"),
        problem_bool=get_obj_from_plan_dict(planroot_dict, "problem_bool"),
        reasonunits=get_obj_from_plan_dict(planroot_dict, "reasonunits"),
        laborunit=get_obj_from_plan_dict(planroot_dict, "laborunit"),
        healerlink=get_obj_from_plan_dict(planroot_dict, "healerlink"),
        factunits=get_obj_from_plan_dict(planroot_dict, "factunits"),
        awardlinks=get_obj_from_plan_dict(planroot_dict, "awardlinks"),
        _is_expanded=get_obj_from_plan_dict(planroot_dict, "_is_expanded"),
        knot=x_believer.knot,
        belief_label=x_believer.belief_label,
        fund_iota=default_fund_iota_if_None(x_believer.fund_iota),
    )
    create_planroot_kids_from_dict(x_believer, planroot_dict)


def create_planroot_kids_from_dict(x_believer: BelieverUnit, planroot_dict: dict):
    to_evaluate_plan_dicts = []
    parent_rope_str = "parent_rope"
    # for every kid dict, set parent_rope in dict, add to to_evaluate_list
    for x_dict in get_obj_from_plan_dict(planroot_dict, "_kids").values():
        x_dict[parent_rope_str] = x_believer.belief_label
        to_evaluate_plan_dicts.append(x_dict)

    while to_evaluate_plan_dicts != []:
        plan_dict = to_evaluate_plan_dicts.pop(0)
        # for every kid dict, set parent_rope in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_plan_dict(plan_dict, "_kids").values():
            parent_rope = get_obj_from_plan_dict(plan_dict, parent_rope_str)
            kid_plan_label = get_obj_from_plan_dict(plan_dict, "plan_label")
            kid_dict[parent_rope_str] = x_believer.make_rope(
                parent_rope, kid_plan_label
            )
            to_evaluate_plan_dicts.append(kid_dict)
        x_plankid = planunit_shop(
            plan_label=get_obj_from_plan_dict(plan_dict, "plan_label"),
            mass=get_obj_from_plan_dict(plan_dict, "mass"),
            _uid=get_obj_from_plan_dict(plan_dict, "_uid"),
            begin=get_obj_from_plan_dict(plan_dict, "begin"),
            close=get_obj_from_plan_dict(plan_dict, "close"),
            numor=get_obj_from_plan_dict(plan_dict, "numor"),
            denom=get_obj_from_plan_dict(plan_dict, "denom"),
            morph=get_obj_from_plan_dict(plan_dict, "morph"),
            gogo_want=get_obj_from_plan_dict(plan_dict, "gogo_want"),
            stop_want=get_obj_from_plan_dict(plan_dict, "stop_want"),
            task=get_obj_from_plan_dict(plan_dict, "task"),
            problem_bool=get_obj_from_plan_dict(plan_dict, "problem_bool"),
            reasonunits=get_obj_from_plan_dict(plan_dict, "reasonunits"),
            laborunit=get_obj_from_plan_dict(plan_dict, "laborunit"),
            healerlink=get_obj_from_plan_dict(plan_dict, "healerlink"),
            awardlinks=get_obj_from_plan_dict(plan_dict, "awardlinks"),
            factunits=get_obj_from_plan_dict(plan_dict, "factunits"),
            _is_expanded=get_obj_from_plan_dict(plan_dict, "_is_expanded"),
        )
        x_believer.set_plan(x_plankid, parent_rope=plan_dict[parent_rope_str])


def obj_from_believer_dict(
    x_dict: dict[str, dict], dict_key: str, _knot: str = None
) -> any:
    if dict_key == "partners":
        return partnerunits_get_from_dict(x_dict[dict_key], _knot)
    elif dict_key == "_max_tree_traverse":
        return (
            x_dict[dict_key]
            if x_dict.get(dict_key) is not None
            else max_tree_traverse_default()
        )
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else None


def get_dict_of_believer_from_dict(x_dict: dict[str, dict]) -> dict[str, BelieverUnit]:
    believerunits = {}
    for believerunit_dict in x_dict.values():
        x_believer = get_from_dict(believer_dict=believerunit_dict)
        believerunits[x_believer.believer_name] = x_believer
    return believerunits


def get_sorted_plan_list(x_list: list[PlanUnit]) -> list[PlanUnit]:
    x_list.sort(key=lambda x: x.get_plan_rope(), reverse=False)
    return x_list
