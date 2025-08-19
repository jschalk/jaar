from copy import deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_False_if_None,
    get_positive_int,
)
from src.a01_term_logic.rope import (
    all_ropeterms_between,
    create_rope,
    find_replace_rope_key_dict,
    is_sub_rope,
    rebuild_rope,
    replace_knot,
)
from src.a01_term_logic.term import (
    BeliefLabel,
    GroupTitle,
    LabelTerm,
    PartnerName,
    RopeTerm,
    default_knot_if_None,
)
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import (
    FundIota,
    FundNum,
    default_fund_iota_if_None,
)
from src.a03_group_logic.group import (
    AwardHeir,
    AwardLine,
    AwardUnit,
    GroupUnit,
    awardheir_shop,
    awardline_shop,
    awardunits_get_from_dict,
)
from src.a03_group_logic.labor import (
    LaborHeir,
    LaborUnit,
    laborheir_shop,
    laborunit_get_from_dict,
    laborunit_shop,
)
from src.a04_reason_logic.reason_plan import (
    FactCore,
    FactHeir,
    FactUnit,
    ReasonCore,
    ReasonHeir,
    ReasonUnit,
    RopeTerm,
    factheir_shop,
    factunit_shop,
    factunits_get_from_dict,
    get_dict_from_factunits,
    reasonheir_shop,
    reasons_get_from_dict,
    reasonunit_shop,
)
from src.a05_plan_logic.healer import (
    HealerLink,
    healerlink_get_from_dict,
    healerlink_shop,
)
from src.a05_plan_logic.range_toolbox import RangeUnit, get_morphed_rangeunit


class InvalidPlanException(Exception):
    pass


class PlanGetDescendantsException(Exception):
    pass


def get_default_belief_label() -> BeliefLabel:
    return "ZZ"


class Plan_root_LabelNotEmptyException(Exception):
    pass


class ranged_fact_plan_Exception(Exception):
    pass


@dataclass
class PlanAttrHolder:
    star: int = None
    uid: int = None
    reason: ReasonUnit = None
    reason_context: RopeTerm = None
    reason_case: RopeTerm = None
    reason_lower: float = None
    reason_upper: float = None
    reason_divisor: int = None
    reason_del_case_reason_context: RopeTerm = None
    reason_del_case_reason_state: RopeTerm = None
    reason_plan_active_requisite: str = None
    laborunit: LaborUnit = None
    healerlink: HealerLink = None
    begin: float = None
    close: float = None
    gogo_want: float = None
    stop_want: float = None
    addin: float = None
    numor: float = None
    denom: float = None
    morph: bool = None
    task: bool = None
    factunit: FactUnit = None
    descendant_task_count: int = None
    all_partner_cred: bool = None
    all_partner_debt: bool = None
    awardunit: AwardUnit = None
    awardunit_del: GroupTitle = None
    is_expanded: bool = None
    problem_bool: bool = None

    def set_case_range_influenced_by_case_plan(
        self,
        reason_lower,
        reason_upper,
        case_denom,
    ):
        if self.reason_case is not None:
            if self.reason_lower is None:
                self.reason_lower = reason_lower
            if self.reason_upper is None:
                self.reason_upper = reason_upper
            if self.reason_divisor is None:
                self.reason_divisor = case_denom


def planattrholder_shop(
    star: int = None,
    uid: int = None,
    reason: ReasonUnit = None,
    reason_context: RopeTerm = None,
    reason_case: RopeTerm = None,
    reason_lower: float = None,
    reason_upper: float = None,
    reason_divisor: int = None,
    reason_del_case_reason_context: RopeTerm = None,
    reason_del_case_reason_state: RopeTerm = None,
    reason_plan_active_requisite: str = None,
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
    awardunit: AwardUnit = None,
    awardunit_del: GroupTitle = None,
    is_expanded: bool = None,
    problem_bool: bool = None,
) -> PlanAttrHolder:
    return PlanAttrHolder(
        star=star,
        uid=uid,
        reason=reason,
        reason_context=reason_context,
        reason_case=reason_case,
        reason_lower=reason_lower,
        reason_upper=reason_upper,
        reason_divisor=reason_divisor,
        reason_del_case_reason_context=reason_del_case_reason_context,
        reason_del_case_reason_state=reason_del_case_reason_state,
        reason_plan_active_requisite=reason_plan_active_requisite,
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
        task=task,
        factunit=factunit,
        descendant_task_count=descendant_task_count,
        all_partner_cred=all_partner_cred,
        all_partner_debt=all_partner_debt,
        awardunit=awardunit,
        awardunit_del=awardunit_del,
        is_expanded=is_expanded,
        problem_bool=problem_bool,
    )


@dataclass
class PlanUnit:
    """
    Represents a planual unit within jaar. Can represent a task, a chore, a different plan's
    reason or fact, a parent plan of other plans.
    Funds: Funds come from the parent plan and go to the child plans.
    Awards: Desribes whom the funding comes from and whome it goes to.
    Tasks: A plan can declare itself a task. It can be active or not active.
      Task Reason: A plan can require that all reasons be active to be active. (No reasons=active)
      Task Fact: Each reason checks facts to determine if it is active.


    funding, and hierarchical relationships.

    Attributes
    ----------
    plan_label : LabelTerm of plan.
    parent_rope : RopeTerm that this plan stems from. Empty string for root plans.
    root : bool at Indicates whether this is a root plan.
    belief_label : BeliefLabel that is root plan LabelTerm.
    knot : str Identifier or label for bridging plans.
    optional:
    star : int weight that is arbitrary used by parent plan to calculated relative importance.
    _kids : dict[RopeTerm], Internal mapping of child plans by their LabelTerm
    _uid : int Unique identifier, forgot how I use this.
    awardunits : dict[GroupTitle, AwardUnit] that describe who funds and who is funded
    reasonunits : dict[RopeTerm, ReasonUnit] that stores all reasons
    laborunit : LaborUnit that describes whom this task is for
    factunits : dict[RopeTerm, FactUnit] that stores all facts
    healerlink : HealerLink, if a ancestor plan is a problem, this can donote a healing plan.
    begin : float that describes the begin of a numberical range if it exists
    close : float that describes the close of a numberical range if it exists
    addin : float that describes addition to parent range calculations
    denom : int that describes denominator to parent range calculations
    numor : int that describes numerator to parent range calculations
    morph : bool that describes how to change parent range in calculations.
    gogo_want : bool
    stop_want : bool
    task : bool that describes if the plan is a task.
    problem_bool : bool that describes if the plan is a problem.
    _is_expanded : bool Internal flag for whether the plan is expanded.

    _active : bool that describes if the plan task is active, calculated by BeliefUnit.
    _active_hx : dict[int, bool] Historical record of active state, used to calcualte if changes have occured
    _all_partner_cred : bool Flag indicating there are not explicitley defined awardunits
    _all_partner_debt : bool Flag indicating there are not explicitley defined awardunits
    _awardheirs : dict[GroupTitle, AwardHeir] parent plan provided awards.
    _awardlines : dict[GroupTitle, AwardLine] child plan provided awards.
    _descendant_task_count : int Count of descendant plans marked as tasks.
    _factheirs : dict[RopeTerm, FactHeir] parent plan provided facts.
    _fund_ratio : float
    fund_iota : FundIota Smallest indivisible funding component.
    _fund_onset : FundNum Point at which funding onsets inside BeliefUnit funding range
    _fund_cease : FundNum Point at which funding ceases inside BeliefUnit funding range
    _healerlink_ratio : float
    _level : int that describes Depth level in plan hierarchy.
    _range_evaluated : bool Flag indicating whether range has been evaluated.
    _reasonheirs : dict[RopeTerm, ReasonHeir] parent plan provided reasoning branches.
    _chore : bool describes if a unit can be changed to inactive with fact range change.
    _laborheir : LaborHeir parent plan provided labor relationships
    _gogo_calc : float
    _stop_calc : float
    """

    plan_label: LabelTerm = None
    belief_label: BeliefLabel = None
    parent_rope: RopeTerm = None
    _kids: dict[RopeTerm,] = None
    root: bool = None
    star: int = None
    _uid: int = None  # Calculated field?
    awardunits: dict[GroupTitle, AwardUnit] = None
    reasonunits: dict[RopeTerm, ReasonUnit] = None
    laborunit: LaborUnit = None
    factunits: dict[RopeTerm, FactUnit] = None
    healerlink: HealerLink = None
    begin: float = None
    close: float = None
    addin: float = None
    denom: int = None
    numor: int = None
    morph: bool = None
    gogo_want: float = None
    stop_want: float = None
    task: bool = None
    problem_bool: bool = None
    knot: str = None
    _is_expanded: bool = None
    # Calculated fields
    _active: bool = None
    _active_hx: dict[int, bool] = None
    _all_partner_cred: bool = None
    _all_partner_debt: bool = None
    _awardheirs: dict[GroupTitle, AwardHeir] = None
    _awardlines: dict[GroupTitle, AwardLine] = None
    _descendant_task_count: int = None
    _factheirs: dict[RopeTerm, FactHeir] = None
    _fund_ratio: float = None
    fund_iota: FundIota = None
    _fund_onset: FundNum = None
    _fund_cease: FundNum = None
    _healerlink_ratio: float = None
    _level: int = None
    _range_evaluated: bool = None
    _reasonheirs: dict[RopeTerm, ReasonHeir] = None
    _chore: bool = None
    _laborheir: LaborHeir = None
    _gogo_calc: float = None
    _stop_calc: float = None

    def is_agenda_plan(self, necessary_reason_context: RopeTerm = None) -> bool:
        reason_context_reasonunit_exists = self.reason_context_reasonunit_exists(
            necessary_reason_context
        )
        return self.task and self._active and reason_context_reasonunit_exists

    def reason_context_reasonunit_exists(
        self, necessary_reason_context: RopeTerm = None
    ) -> bool:
        x_reasons = self.reasonunits.values()
        x_reason_context = necessary_reason_context
        return x_reason_context is None or any(
            reason.reason_context == x_reason_context for reason in x_reasons
        )

    def record_active_hx(
        self, tree_traverse_count: int, prev_active: bool, now_active: bool
    ):
        if tree_traverse_count == 0:
            self._active_hx = {0: now_active}
        elif prev_active != now_active:
            self._active_hx[tree_traverse_count] = now_active

    def set_factheirs(self, facts: dict[RopeTerm, FactCore]):
        facts_dict = get_empty_dict_if_None(facts)
        self._factheirs = {}
        for x_factcore in facts_dict.values():
            self._set_factheir(x_factcore)

    def _set_factheir(self, x_fact: FactCore):
        if (
            x_fact.fact_context == self.get_plan_rope()
            and self._gogo_calc is not None
            and self._stop_calc is not None
            and self.begin is None
            and self.close is None
        ):
            raise ranged_fact_plan_Exception(
                f"Cannot have fact for range inheritor '{self.get_plan_rope()}'. A ranged fact plan must have _begin, _close"
            )
        x_factheir = factheir_shop(
            x_fact.fact_context, x_fact.fact_state, x_fact.fact_lower, x_fact.fact_upper
        )
        self.delete_factunit_if_past(x_factheir)
        x_factheir = self.apply_factunit_moldations(x_factheir)
        self._factheirs[x_factheir.fact_context] = x_factheir

    def apply_factunit_moldations(self, factheir: FactHeir) -> FactHeir:
        for factunit in self.factunits.values():
            if factunit.fact_context == factheir.fact_context:
                factheir.mold(factunit)
        return factheir

    def delete_factunit_if_past(self, factheir: FactHeir):
        delete_factunit = False
        for factunit in self.factunits.values():
            if (
                factunit.fact_context == factheir.fact_context
                and factunit.fact_upper is not None
                and factheir.fact_lower is not None
            ) and factunit.fact_upper < factheir.fact_lower:
                delete_factunit = True

        if delete_factunit:
            del self.factunits[factunit.fact_context]

    def set_factunit(self, factunit: FactUnit):
        self.factunits[factunit.fact_context] = factunit

    def factunit_exists(self, x_fact_context: RopeTerm) -> bool:
        return self.factunits.get(x_fact_context) != None

    def get_factunits_dict(self) -> dict[RopeTerm, str]:
        return get_dict_from_factunits(self.factunits)

    def set_factunit_to_complete(self, fact_contextunit: FactUnit):
        # if a plan is considered a chore then a factheir.fact_lower attribute can be increased to
        # a number <= factheir.fact_upper so the plan no longer is a chore. This method finds
        # the minimal factheir.fact_lower to modify plan._chore is False. plan_core._factheir cannot be straight up manipulated
        # so it is mandatory that plan._factunit is different.
        # self.set_factunits(reason_context=fact, fact=reason_context, reason_lower=reason_upper, reason_upper=fact_upper)
        self.factunits[fact_contextunit.fact_context] = factunit_shop(
            fact_context=fact_contextunit.fact_context,
            fact_state=fact_contextunit.fact_context,
            fact_lower=fact_contextunit.fact_upper,
            fact_upper=fact_contextunit.fact_upper,
        )

    def del_factunit(self, fact_context: RopeTerm):
        self.factunits.pop(fact_context)

    def set_fund_attr(
        self,
        x_fund_onset: FundNum,
        x_fund_cease: FundNum,
        _fund_pool: FundNum,
    ):
        self._fund_onset = x_fund_onset
        self._fund_cease = x_fund_cease
        self._fund_ratio = self.get_fund_share() / _fund_pool
        self.set_awardheirs_fund_give_fund_take()

    def get_fund_share(self) -> float:
        """Return plan fund share from different of _fund_cease and _fund_onset"""
        if self._fund_onset is None or self._fund_cease is None:
            return 0
        else:
            return self._fund_cease - self._fund_onset

    def get_kids_in_range(
        self, x_gogo: float = None, x_stop: float = None
    ) -> dict[LabelTerm,]:
        if x_gogo is None and x_stop is None:
            x_gogo = self.gogo_want
            x_gogo = self.stop_want
        elif x_gogo is not None and x_stop is None:
            x_stop = x_gogo

        if x_gogo is None and x_stop is None:
            return self._kids.values()

        x_dict = {}
        for x_plan in self._kids.values():
            x_gogo_in_range = x_gogo >= x_plan._gogo_calc and x_gogo < x_plan._stop_calc
            x_stop_in_range = x_stop > x_plan._gogo_calc and x_stop < x_plan._stop_calc
            both_in_range = x_gogo <= x_plan._gogo_calc and x_stop >= x_plan._stop_calc

            if x_gogo_in_range or x_stop_in_range or both_in_range:
                x_dict[x_plan.plan_label] = x_plan
        return x_dict

    def get_obj_key(self) -> LabelTerm:
        return self.plan_label

    def get_plan_rope(self) -> RopeTerm:
        if self.parent_rope in (None, ""):
            return create_rope(self.plan_label, knot=self.knot)
        else:
            return create_rope(self.parent_rope, self.plan_label, knot=self.knot)

    def clear_descendant_task_count(self):
        self._descendant_task_count = None

    def set_descendant_task_count_zero_if_None(self):
        if self._descendant_task_count is None:
            self._descendant_task_count = 0

    def add_to_descendant_task_count(self, x_int: int):
        self.set_descendant_task_count_zero_if_None()
        self._descendant_task_count += x_int

    def get_descendant_ropes_from_kids(self) -> dict[RopeTerm, int]:
        descendant_ropes = {}
        to_evaluate_plans = list(self._kids.values())
        count_x = 0
        max_count = 1000
        while to_evaluate_plans != [] and count_x < max_count:
            x_plan = to_evaluate_plans.pop()
            descendant_ropes[x_plan.get_plan_rope()] = -1
            to_evaluate_plans.extend(x_plan._kids.values())
            count_x += 1

        if count_x == max_count:
            raise PlanGetDescendantsException(
                f"Plan '{self.get_plan_rope()}' either has an infinite loop or more than {max_count} descendants."
            )

        return descendant_ropes

    def clear_all_partner_cred_debt(self):
        self._all_partner_cred = None
        self._all_partner_debt = None

    def set_level(self, parent_level):
        self._level = parent_level + 1

    def set_parent_rope(self, parent_rope):
        self.parent_rope = parent_rope

    def inherit_awardheirs(self, parent_awardheirs: dict[GroupTitle, AwardHeir] = None):
        parent_awardheirs = {} if parent_awardheirs is None else parent_awardheirs
        self._awardheirs = {}
        for ib in parent_awardheirs.values():
            awardheir = awardheir_shop(
                awardee_title=ib.awardee_title,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self._awardheirs[awardheir.awardee_title] = awardheir

        for ib in self.awardunits.values():
            awardheir = awardheir_shop(
                awardee_title=ib.awardee_title,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self._awardheirs[awardheir.awardee_title] = awardheir

    def set_kidless_awardlines(self):
        # get awardlines from self
        for bh in self._awardheirs.values():
            x_awardline = awardline_shop(
                awardee_title=bh.awardee_title,
                _fund_give=bh._fund_give,
                _fund_take=bh._fund_take,
            )
            self._awardlines[x_awardline.awardee_title] = x_awardline

    def set_awardlines(self, child_awardlines: dict[GroupTitle, AwardLine] = None):
        if child_awardlines is None:
            child_awardlines = {}

        # get awardlines from child
        for bl in child_awardlines.values():
            if self._awardlines.get(bl.awardee_title) is None:
                self._awardlines[bl.awardee_title] = awardline_shop(
                    awardee_title=bl.awardee_title,
                    _fund_give=0,
                    _fund_take=0,
                )

            self._awardlines[bl.awardee_title].add_fund_give_take(
                fund_give=bl._fund_give, fund_take=bl._fund_take
            )

    def set_awardheirs_fund_give_fund_take(self):
        give_ledger = {}
        take_ledger = {}
        for x_awardee_title, x_awardheir in self._awardheirs.items():
            give_ledger[x_awardee_title] = x_awardheir.give_force
            take_ledger[x_awardee_title] = x_awardheir.take_force
        x_fund_share = self.get_fund_share()
        give_allot = allot_scale(give_ledger, x_fund_share, self.fund_iota)
        take_allot = allot_scale(take_ledger, x_fund_share, self.fund_iota)
        for x_awardee_title, x_awardheir in self._awardheirs.items():
            x_awardheir._fund_give = give_allot.get(x_awardee_title)
            x_awardheir._fund_take = take_allot.get(x_awardee_title)

    def clear_awardlines(self):
        self._awardlines = {}

    def set_plan_label(self, plan_label: str):
        if (
            self.root
            and plan_label is not None
            and plan_label != self.belief_label
            and self.belief_label is not None
        ):
            raise Plan_root_LabelNotEmptyException(
                f"Cannot set planroot to string different than '{self.belief_label}'"
            )
        else:
            self.plan_label = plan_label

    def set_knot(self, new_knot: str):
        old_knot = deepcopy(self.knot)
        if old_knot is None:
            old_knot = default_knot_if_None()
        self.knot = default_knot_if_None(new_knot)
        if old_knot != self.knot:
            self._find_replace_knot(old_knot)

    def _find_replace_knot(self, old_knot):
        self.parent_rope = replace_knot(self.parent_rope, old_knot, self.knot)

        new_reasonunits = {}
        for reasonunit_rope, reasonunit_obj in self.reasonunits.items():
            new_reasonunit_rope = replace_knot(
                rope=reasonunit_rope,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            reasonunit_obj.set_knot(self.knot)
            new_reasonunits[new_reasonunit_rope] = reasonunit_obj
        self.reasonunits = new_reasonunits

        new_factunits = {}
        for factunit_rope, x_factunit in self.factunits.items():
            new_reason_context_rope = replace_knot(
                rope=factunit_rope,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            x_factunit.fact_context = new_reason_context_rope
            new_fact_state_rope = replace_knot(
                rope=x_factunit.fact_state,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            x_factunit.set_attr(fact_state=new_fact_state_rope)
            new_factunits[new_reason_context_rope] = x_factunit
        self.factunits = new_factunits

    def _set_attrs_to_planunit(self, plan_attr: PlanAttrHolder):
        if plan_attr.star is not None:
            self.star = plan_attr.star
        if plan_attr.uid is not None:
            self._uid = plan_attr.uid
        if plan_attr.reason is not None:
            self.set_reasonunit(reason=plan_attr.reason)
        if plan_attr.reason_context is not None and plan_attr.reason_case is not None:
            self.set_reason_case(
                reason_context=plan_attr.reason_context,
                case=plan_attr.reason_case,
                reason_lower=plan_attr.reason_lower,
                reason_upper=plan_attr.reason_upper,
                reason_divisor=plan_attr.reason_divisor,
            )
        if (
            plan_attr.reason_context is not None
            and plan_attr.reason_plan_active_requisite is not None
        ):
            self.set_reason_plan_active_requisite(
                reason_context=plan_attr.reason_context,
                reason_active_requisite=plan_attr.reason_plan_active_requisite,
            )
        if plan_attr.laborunit is not None:
            self.laborunit = plan_attr.laborunit
        if plan_attr.healerlink is not None:
            self.healerlink = plan_attr.healerlink
        if plan_attr.begin is not None:
            self.begin = plan_attr.begin
        if plan_attr.close is not None:
            self.close = plan_attr.close
        if plan_attr.gogo_want is not None:
            self.gogo_want = plan_attr.gogo_want
        if plan_attr.stop_want is not None:
            self.stop_want = plan_attr.stop_want
        if plan_attr.addin is not None:
            self.addin = plan_attr.addin
        if plan_attr.numor is not None:
            self.numor = plan_attr.numor
        if plan_attr.denom is not None:
            self.denom = plan_attr.denom
        if plan_attr.morph is not None:
            self.morph = plan_attr.morph
        if plan_attr.descendant_task_count is not None:
            self._descendant_task_count = plan_attr.descendant_task_count
        if plan_attr.all_partner_cred is not None:
            self._all_partner_cred = plan_attr.all_partner_cred
        if plan_attr.all_partner_debt is not None:
            self._all_partner_debt = plan_attr.all_partner_debt
        if plan_attr.awardunit is not None:
            self.set_awardunit(awardunit=plan_attr.awardunit)
        if plan_attr.awardunit_del is not None:
            self.del_awardunit(awardee_title=plan_attr.awardunit_del)
        if plan_attr.is_expanded is not None:
            self._is_expanded = plan_attr.is_expanded
        if plan_attr.task is not None:
            self.task = plan_attr.task
        if plan_attr.factunit is not None:
            self.set_factunit(plan_attr.factunit)
        if plan_attr.problem_bool is not None:
            self.problem_bool = plan_attr.problem_bool

        self._del_reasonunit_all_cases(
            reason_context=plan_attr.reason_del_case_reason_context,
            case=plan_attr.reason_del_case_reason_state,
        )
        self._set_addin_to_zero_if_any_moldations_exist()

    def _set_addin_to_zero_if_any_moldations_exist(self):
        if (
            self.begin is not None
            and self.close is not None
            and (self.numor is not None or self.denom is not None)
            and self.addin is None
        ):
            self.addin = 0

    def clear_gogo_calc_stop_calc(self):
        self._range_evaluated = False
        self._gogo_calc = None
        self._stop_calc = None

    def _mold_gogo_calc_stop_calc(self):
        r_plan_numor = get_1_if_None(self.numor)
        r_plan_denom = get_1_if_None(self.denom)
        r_plan_addin = get_0_if_None(self.addin)

        if self._gogo_calc is None or self._stop_calc is None:
            pass
        elif self.gogo_want != None and self.stop_want != None:
            stop_want_less_than_gogo_calc = self.stop_want < self._gogo_calc
            gogo_want_greater_than_stop_calc = self.gogo_want > self._stop_calc
            if stop_want_less_than_gogo_calc or gogo_want_greater_than_stop_calc:
                self._gogo_calc = None
                self._stop_calc = None
            else:
                self._gogo_calc = max(self._gogo_calc, self.gogo_want)
                self._stop_calc = min(self._stop_calc, self.stop_want)
        elif get_False_if_None(self.morph):
            x_gogo = self._gogo_calc
            x_stop = self._stop_calc
            x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, self.denom)
            self._gogo_calc = x_rangeunit.gogo
            self._stop_calc = x_rangeunit.stop
        else:
            self._gogo_calc = self._gogo_calc + r_plan_addin
            self._stop_calc = self._stop_calc + r_plan_addin
            self._gogo_calc = (self._gogo_calc * r_plan_numor) / r_plan_denom
            self._stop_calc = (self._stop_calc * r_plan_numor) / r_plan_denom
        self._range_evaluated = True

    def _del_reasonunit_all_cases(self, reason_context: RopeTerm, case: RopeTerm):
        if reason_context is not None and case is not None:
            self.del_reasonunit_case(reason_context=reason_context, case=case)
            if len(self.reasonunits[reason_context].cases) == 0:
                self.del_reasonunit_reason_context(reason_context=reason_context)

    def set_reason_plan_active_requisite(
        self, reason_context: RopeTerm, reason_active_requisite: str
    ):
        x_reasonunit = self._get_or_create_reasonunit(reason_context=reason_context)
        if reason_active_requisite is False:
            x_reasonunit.reason_active_requisite = False
        elif reason_active_requisite == "Set to Ignore":
            x_reasonunit.reason_active_requisite = None
        elif reason_active_requisite:
            x_reasonunit.reason_active_requisite = True

    def _get_or_create_reasonunit(self, reason_context: RopeTerm) -> ReasonUnit:
        x_reasonunit = None
        try:
            x_reasonunit = self.reasonunits[reason_context]
        except Exception:
            x_reasonunit = reasonunit_shop(reason_context, knot=self.knot)
            self.reasonunits[reason_context] = x_reasonunit
        return x_reasonunit

    def set_reason_case(
        self,
        reason_context: RopeTerm,
        case: RopeTerm,
        reason_lower: float,
        reason_upper: float,
        reason_divisor: int,
    ):
        x_reasonunit = self._get_or_create_reasonunit(reason_context=reason_context)
        x_reasonunit.set_case(
            case=case,
            reason_lower=reason_lower,
            reason_upper=reason_upper,
            reason_divisor=reason_divisor,
        )

    def del_reasonunit_reason_context(self, reason_context: RopeTerm):
        try:
            self.reasonunits.pop(reason_context)
        except KeyError as e:
            raise InvalidPlanException(f"No ReasonUnit at '{reason_context}'") from e

    def del_reasonunit_case(self, reason_context: RopeTerm, case: RopeTerm):
        reason_unit = self.reasonunits[reason_context]
        reason_unit.del_case(case=case)

    def add_kid(self, plan_kid):
        self._kids[plan_kid.plan_label] = plan_kid
        self._kids = dict(sorted(self._kids.items()))

    def get_kid(self, plan_kid_plan_label: LabelTerm, if_missing_create=False):
        if if_missing_create is False:
            return self._kids.get(plan_kid_plan_label)
        try:
            return self._kids[plan_kid_plan_label]
        except Exception:
            KeyError
            self.add_kid(planunit_shop(plan_kid_plan_label))
            return_plan = self._kids.get(plan_kid_plan_label)
        return return_plan

    def del_kid(self, plan_kid_plan_label: LabelTerm):
        self._kids.pop(plan_kid_plan_label)

    def clear_kids(self):
        self._kids = {}

    def get_kids_star_sum(self) -> float:
        return sum(x_kid.star for x_kid in self._kids.values())

    def set_awardunit(self, awardunit: AwardUnit):
        self.awardunits[awardunit.awardee_title] = awardunit

    def get_awardunit(self, awardee_title: GroupTitle) -> AwardUnit:
        return self.awardunits.get(awardee_title)

    def del_awardunit(self, awardee_title: GroupTitle):
        try:
            self.awardunits.pop(awardee_title)
        except KeyError as e:
            raise (f"Cannot delete awardunit '{awardee_title}'.") from e

    def awardunit_exists(self, x_awardee_title: GroupTitle) -> bool:
        return self.awardunits.get(x_awardee_title) != None

    def set_reasonunit(self, reason: ReasonUnit):
        reason.knot = self.knot
        self.reasonunits[reason.reason_context] = reason

    def reasonunit_exists(self, x_reason_context: RopeTerm) -> bool:
        return self.reasonunits.get(x_reason_context) != None

    def get_reasonunit(self, reason_context: RopeTerm) -> ReasonUnit:
        return self.reasonunits.get(reason_context)

    def set_reasonheirs_status(self):
        self.clear_reasonheirs_status()
        for x_reasonheir in self._reasonheirs.values():
            x_reasonheir.set_status(factheirs=self._factheirs)

    def set_active_attrs(
        self,
        tree_traverse_count: int,
        groupunits: dict[GroupTitle, GroupUnit] = None,
        believer_name: PartnerName = None,
    ):
        prev_to_now_active = deepcopy(self._active)
        self._active = self._create_active_bool(groupunits, believer_name)
        self._set_plan_chore()
        self.record_active_hx(tree_traverse_count, prev_to_now_active, self._active)

    def _set_plan_chore(self):
        self._chore = False
        if self.task and self._active and self._reasonheirs_satisfied():
            self._chore = True

    def _reasonheirs_satisfied(self) -> bool:
        return self._reasonheirs == {} or self._any_reasonheir_chore_true()

    def _any_reasonheir_chore_true(self) -> bool:
        return any(x_reasonheir._chore for x_reasonheir in self._reasonheirs.values())

    def _create_active_bool(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        believer_name: PartnerName,
    ) -> bool:
        self.set_reasonheirs_status()
        active_bool = self._are_all_reasonheir_active_true()
        if active_bool and groupunits != {} and believer_name is not None:
            self._laborheir.set_believer_name_is_labor(groupunits, believer_name)
            if self._laborheir._believer_name_is_labor is False:
                active_bool = False
        return active_bool

    def set_range_factheirs(
        self,
        believer_plan_dict: dict[RopeTerm,],
        range_inheritors: dict[RopeTerm, RopeTerm],
    ):
        for reason_context in self._reasonheirs.keys():
            if range_root_rope := range_inheritors.get(reason_context):
                all_plans = all_plans_between(
                    believer_plan_dict, range_root_rope, reason_context, self.knot
                )
                self._create_factheir(all_plans, range_root_rope, reason_context)

    def _create_factheir(
        self, all_plans: list, range_root_rope: RopeTerm, reason_context: RopeTerm
    ):
        range_root_factheir = self._factheirs.get(range_root_rope)
        old_reason_lower = range_root_factheir.fact_lower
        old_reason_upper = range_root_factheir.fact_upper
        x_rangeunit = plans_calculated_range(
            all_plans, old_reason_lower, old_reason_upper
        )
        new_factheir_reason_lower = x_rangeunit.gogo
        new_factheir_reason_upper = x_rangeunit.stop
        new_factheir_obj = factheir_shop(reason_context)
        new_factheir_obj.set_attr(
            reason_context, new_factheir_reason_lower, new_factheir_reason_upper
        )
        self._set_factheir(new_factheir_obj)

    def _are_all_reasonheir_active_true(self) -> bool:
        x_reasonheirs = self._reasonheirs.values()
        return all(x_reasonheir._status != False for x_reasonheir in x_reasonheirs)

    def clear_reasonheirs_status(self):
        for reason in self._reasonheirs.values():
            reason.clear_status()

    def _coalesce_with_reasonunits(
        self, reasonheirs: dict[RopeTerm, ReasonHeir]
    ) -> dict[RopeTerm, ReasonHeir]:
        new_reasonheirs = deepcopy(reasonheirs)
        new_reasonheirs |= self.reasonunits
        return new_reasonheirs

    def set_reasonheirs(
        self,
        believer_plan_dict: dict[RopeTerm,],
        reasonheirs: dict[RopeTerm, ReasonCore],
    ):
        coalesced_reasons = self._coalesce_with_reasonunits(reasonheirs)
        self._reasonheirs = {}
        for old_reasonheir in coalesced_reasons.values():
            old_reason_context = old_reasonheir.reason_context
            old_active_requisite = old_reasonheir.reason_active_requisite
            new_reasonheir = reasonheir_shop(
                old_reason_context, None, old_active_requisite
            )
            new_reasonheir.inherit_from_reasonheir(old_reasonheir)

            if reason_context_plan := believer_plan_dict.get(
                old_reasonheir.reason_context
            ):
                new_reasonheir.set_rplan_active_value(reason_context_plan._active)
            self._reasonheirs[new_reasonheir.reason_context] = new_reasonheir

    def set_planroot_inherit_reasonheirs(self):
        self._reasonheirs = {}
        for x_reasonunit in self.reasonunits.values():
            new_reasonheir = reasonheir_shop(x_reasonunit.reason_context)
            new_reasonheir.inherit_from_reasonheir(x_reasonunit)
            self._reasonheirs[new_reasonheir.reason_context] = new_reasonheir

    def get_reasonheir(self, reason_context: RopeTerm) -> ReasonHeir:
        return self._reasonheirs.get(reason_context)

    def get_reasonunits_dict(self):
        return {
            reason_context: reason.to_dict()
            for reason_context, reason in self.reasonunits.items()
        }

    def get_kids_dict(self) -> dict[GroupTitle,]:
        return {c_rope: kid.to_dict() for c_rope, kid in self._kids.items()}

    def get_awardunits_dict(self) -> dict[GroupTitle, dict]:
        x_awardunits = self.awardunits.items()
        return {
            x_awardee_title: awardunit.to_dict()
            for x_awardee_title, awardunit in x_awardunits
        }

    def is_kidless(self) -> bool:
        return self._kids == {}

    def is_math(self) -> bool:
        return self.begin is not None and self.close is not None

    def awardheir_exists(self) -> bool:
        return self._awardheirs != {}

    def to_dict(self) -> dict[str, str]:
        x_dict = {"star": self.star}

        if self.plan_label is not None:
            x_dict["plan_label"] = self.plan_label
        if self._uid is not None:
            x_dict["_uid"] = self._uid
        if self._kids not in [{}, None]:
            x_dict["_kids"] = self.get_kids_dict()
        if self.reasonunits not in [{}, None]:
            x_dict["reasonunits"] = self.get_reasonunits_dict()
        if self.laborunit not in [None, laborunit_shop()]:
            x_dict["laborunit"] = self.get_laborunit_dict()
        if self.healerlink not in [None, healerlink_shop()]:
            x_dict["healerlink"] = self.healerlink.to_dict()
        if self.awardunits not in [{}, None]:
            x_dict["awardunits"] = self.get_awardunits_dict()
        if self.begin is not None:
            x_dict["begin"] = self.begin
        if self.close is not None:
            x_dict["close"] = self.close
        if self.addin is not None:
            x_dict["addin"] = self.addin
        if self.numor is not None:
            x_dict["numor"] = self.numor
        if self.denom is not None:
            x_dict["denom"] = self.denom
        if self.morph is not None:
            x_dict["morph"] = self.morph
        if self.gogo_want is not None:
            x_dict["gogo_want"] = self.gogo_want
        if self.stop_want is not None:
            x_dict["stop_want"] = self.stop_want
        if self.task:
            x_dict["task"] = self.task
        if self.problem_bool:
            x_dict["problem_bool"] = self.problem_bool
        if self.factunits not in [{}, None]:
            x_dict["factunits"] = self.get_factunits_dict()
        if self._is_expanded is False:
            x_dict["_is_expanded"] = self._is_expanded

        return x_dict

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        if is_sub_rope(ref_rope=self.parent_rope, sub_rope=old_rope):
            self.parent_rope = rebuild_rope(self.parent_rope, old_rope, new_rope)

        self.reasonunits == find_replace_rope_key_dict(
            dict_x=self.reasonunits, old_rope=old_rope, new_rope=new_rope
        )

        self.factunits == find_replace_rope_key_dict(
            dict_x=self.factunits, old_rope=old_rope, new_rope=new_rope
        )

    def set_laborunit_empty_if_None(self):
        if self.laborunit is None:
            self.laborunit = laborunit_shop()

    def set_laborheir(
        self,
        parent_laborheir: LaborHeir,
        groupunits: dict[GroupTitle, GroupUnit],
    ):
        self._laborheir = laborheir_shop()
        self._laborheir.set_partys(
            parent_laborheir=parent_laborheir,
            laborunit=self.laborunit,
            groupunits=groupunits,
        )

    def get_laborunit_dict(self) -> dict:
        return self.laborunit.to_dict()


def planunit_shop(
    plan_label: LabelTerm = None,
    _uid: int = None,  # Calculated field?
    parent_rope: RopeTerm = None,
    _kids: dict = None,
    star: int = 1,
    awardunits: dict[GroupTitle, AwardUnit] = None,
    _awardheirs: dict[GroupTitle, AwardHeir] = None,  # Calculated field
    _awardlines: dict[GroupTitle, AwardUnit] = None,  # Calculated field
    reasonunits: dict[RopeTerm, ReasonUnit] = None,
    _reasonheirs: dict[RopeTerm, ReasonHeir] = None,  # Calculated field
    laborunit: LaborUnit = None,
    _laborheir: LaborHeir = None,  # Calculated field
    factunits: dict[FactUnit] = None,
    _factheirs: dict[FactHeir] = None,  # Calculated field
    healerlink: HealerLink = None,
    begin: float = None,
    close: float = None,
    gogo_want: float = None,
    stop_want: float = None,
    addin: float = None,
    denom: int = None,
    numor: int = None,
    morph: bool = None,
    task: bool = None,
    root: bool = None,
    belief_label: BeliefLabel = None,
    problem_bool: bool = None,
    # Calculated fields
    _level: int = None,
    _fund_ratio: float = None,
    fund_iota: FundIota = None,
    _fund_onset: FundNum = None,
    _fund_cease: FundNum = None,
    _chore: bool = None,
    _active: bool = None,
    _descendant_task_count: int = None,
    _all_partner_cred: bool = None,
    _all_partner_debt: bool = None,
    _is_expanded: bool = True,
    _active_hx: dict[int, bool] = None,
    knot: str = None,
    _healerlink_ratio: float = None,
) -> PlanUnit:
    belief_label = get_default_belief_label() if belief_label is None else belief_label
    x_healerlink = healerlink_shop() if healerlink is None else healerlink

    x_plankid = PlanUnit(
        plan_label=None,
        _uid=_uid,
        parent_rope=parent_rope,
        _kids=get_empty_dict_if_None(_kids),
        star=get_positive_int(star),
        awardunits=get_empty_dict_if_None(awardunits),
        _awardheirs=get_empty_dict_if_None(_awardheirs),
        _awardlines=get_empty_dict_if_None(_awardlines),
        reasonunits=get_empty_dict_if_None(reasonunits),
        _reasonheirs=get_empty_dict_if_None(_reasonheirs),
        laborunit=laborunit,
        _laborheir=_laborheir,
        factunits=get_empty_dict_if_None(factunits),
        _factheirs=get_empty_dict_if_None(_factheirs),
        healerlink=x_healerlink,
        begin=begin,
        close=close,
        gogo_want=gogo_want,
        stop_want=stop_want,
        addin=addin,
        denom=denom,
        numor=numor,
        morph=morph,
        task=get_False_if_None(task),
        problem_bool=get_False_if_None(problem_bool),
        root=get_False_if_None(root),
        belief_label=belief_label,
        # Calculated fields
        _level=_level,
        _fund_ratio=_fund_ratio,
        fund_iota=default_fund_iota_if_None(fund_iota),
        _fund_onset=_fund_onset,
        _fund_cease=_fund_cease,
        _chore=_chore,
        _active=_active,
        _descendant_task_count=_descendant_task_count,
        _all_partner_cred=_all_partner_cred,
        _all_partner_debt=_all_partner_debt,
        _is_expanded=_is_expanded,
        _active_hx=get_empty_dict_if_None(_active_hx),
        knot=default_knot_if_None(knot),
        _healerlink_ratio=get_0_if_None(_healerlink_ratio),
    )
    if x_plankid.root:
        x_plankid.set_plan_label(plan_label=belief_label)
    else:
        x_plankid.set_plan_label(plan_label=plan_label)
    x_plankid.set_laborunit_empty_if_None()
    return x_plankid


def get_obj_from_plan_dict(x_dict: dict[str, dict], dict_key: str) -> any:
    if dict_key == "reasonunits":
        return (
            reasons_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else None
        )
    elif dict_key == "laborunit":
        return (
            laborunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else laborunit_shop()
        )
    elif dict_key == "healerlink":
        return (
            healerlink_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else healerlink_shop()
        )
    elif dict_key == "factunits":
        facts_dict = get_empty_dict_if_None(x_dict.get(dict_key))
        return factunits_get_from_dict(facts_dict)
    elif dict_key == "awardunits":
        return (
            awardunits_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else awardunits_get_from_dict({})
        )
    elif dict_key in {"_kids"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else {}
    elif dict_key in {"task", "problem_bool"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else False
    elif dict_key in {"_is_expanded"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else True
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else None


def all_plans_between(
    believer_plan_dict: dict[RopeTerm, PlanUnit],
    src_rope: RopeTerm,
    dst_reason_context: RopeTerm,
    knot: str,
) -> list[PlanUnit]:
    all_ropes = all_ropeterms_between(src_rope, dst_reason_context, knot)
    return [believer_plan_dict.get(x_rope) for x_rope in all_ropes]


def plans_calculated_range(
    plan_list: list[PlanUnit], x_gogo: float, x_stop: float
) -> RangeUnit:
    for x_plan in plan_list:
        if x_plan.addin:
            x_gogo += get_0_if_None(x_plan.addin)
            x_stop += get_0_if_None(x_plan.addin)
        if (x_plan.numor or x_plan.denom) and not x_plan.morph:
            x_gogo *= get_1_if_None(x_plan.numor) / get_1_if_None(x_plan.denom)
            x_stop *= get_1_if_None(x_plan.numor) / get_1_if_None(x_plan.denom)
        if x_plan.denom and x_plan.morph:
            x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, x_plan.denom)
            x_gogo = x_rangeunit.gogo
            x_stop = x_rangeunit.stop
    return RangeUnit(x_gogo, x_stop)
