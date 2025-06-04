from copy import deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_False_if_None,
    get_positive_int,
)
from src.a01_term_logic.term import AcctName, GroupTitle, LabelTerm
from src.a01_term_logic.way import (
    FiscLabel,
    LabelTerm,
    WayTerm,
    all_wayterms_between,
    create_way,
    default_bridge_if_None,
    find_replace_way_key_dict,
    get_default_fisc_label as root_label,
    is_sub_way,
    rebuild_way,
    replace_bridge,
)
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import (
    FundCoin,
    FundNum,
    default_fund_coin_if_None,
)
from src.a03_group_logic.group import (
    AwardHeir,
    AwardLine,
    AwardLink,
    GroupUnit,
    awardheir_shop,
    awardline_shop,
    awardlinks_get_from_dict,
)
from src.a04_reason_logic.reason_concept import (
    FactCore,
    FactHeir,
    FactUnit,
    ReasonCore,
    ReasonHeir,
    ReasonUnit,
    WayTerm,
    factheir_shop,
    factunit_shop,
    factunits_get_from_dict,
    get_dict_from_factunits,
    reasonheir_shop,
    reasons_get_from_dict,
    reasonunit_shop,
)
from src.a04_reason_logic.reason_labor import (
    LaborHeir,
    LaborUnit,
    laborheir_shop,
    laborunit_get_from_dict,
    laborunit_shop,
)
from src.a05_concept_logic.healer import (
    HealerLink,
    healerlink_get_from_dict,
    healerlink_shop,
)
from src.a05_concept_logic.origin import (
    OriginUnit,
    originunit_get_from_dict,
    originunit_shop,
)
from src.a05_concept_logic.range_toolbox import RangeUnit, get_morphed_rangeunit


class InvalidConceptException(Exception):
    pass


class ConceptGetDescendantsException(Exception):
    pass


class Concept_root_LabelNotEmptyException(Exception):
    pass


class ranged_fact_concept_Exception(Exception):
    pass


@dataclass
class ConceptAttrHolder:
    mass: int = None
    uid: int = None
    reason: ReasonUnit = None
    reason_rcontext: WayTerm = None
    reason_premise: WayTerm = None
    popen: float = None
    reason_pnigh: float = None
    pdivisor: int = None
    reason_del_premise_rcontext: WayTerm = None
    reason_del_premise_pstate: WayTerm = None
    reason_rconcept_active_requisite: str = None
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
    pledge: bool = None
    factunit: FactUnit = None
    descendant_pledge_count: int = None
    all_acct_cred: bool = None
    all_acct_debt: bool = None
    awardlink: AwardLink = None
    awardlink_del: GroupTitle = None
    is_expanded: bool = None
    problem_bool: bool = None

    def set_premise_range_influenced_by_premise_concept(
        self,
        popen,
        pnigh,
        premise_denom,
    ):
        if self.reason_premise is not None:
            if self.popen is None:
                self.popen = popen
            if self.reason_pnigh is None:
                self.reason_pnigh = pnigh
            if self.pdivisor is None:
                self.pdivisor = premise_denom


def conceptattrholder_shop(
    mass: int = None,
    uid: int = None,
    reason: ReasonUnit = None,
    reason_rcontext: WayTerm = None,
    reason_premise: WayTerm = None,
    popen: float = None,
    reason_pnigh: float = None,
    pdivisor: int = None,
    reason_del_premise_rcontext: WayTerm = None,
    reason_del_premise_pstate: WayTerm = None,
    reason_rconcept_active_requisite: str = None,
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
    pledge: bool = None,
    factunit: FactUnit = None,
    descendant_pledge_count: int = None,
    all_acct_cred: bool = None,
    all_acct_debt: bool = None,
    awardlink: AwardLink = None,
    awardlink_del: GroupTitle = None,
    is_expanded: bool = None,
    problem_bool: bool = None,
) -> ConceptAttrHolder:
    return ConceptAttrHolder(
        mass=mass,
        uid=uid,
        reason=reason,
        reason_rcontext=reason_rcontext,
        reason_premise=reason_premise,
        popen=popen,
        reason_pnigh=reason_pnigh,
        pdivisor=pdivisor,
        reason_del_premise_rcontext=reason_del_premise_rcontext,
        reason_del_premise_pstate=reason_del_premise_pstate,
        reason_rconcept_active_requisite=reason_rconcept_active_requisite,
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
        pledge=pledge,
        factunit=factunit,
        descendant_pledge_count=descendant_pledge_count,
        all_acct_cred=all_acct_cred,
        all_acct_debt=all_acct_debt,
        awardlink=awardlink,
        awardlink_del=awardlink_del,
        is_expanded=is_expanded,
        problem_bool=problem_bool,
    )


@dataclass
class ConceptUnit:
    concept_label: LabelTerm = None
    mass: int = None
    parent_way: WayTerm = None
    root: bool = None
    _kids: dict[WayTerm,] = None
    fisc_label: FiscLabel = None
    _uid: int = None  # Calculated field?
    awardlinks: dict[GroupTitle, AwardLink] = None
    reasonunits: dict[WayTerm, ReasonUnit] = None
    laborunit: LaborUnit = None
    factunits: dict[WayTerm, FactUnit] = None
    healerlink: HealerLink = None
    begin: float = None
    close: float = None
    addin: float = None
    denom: int = None
    numor: int = None
    morph: bool = None
    gogo_want: bool = None
    stop_want: bool = None
    pledge: bool = None
    _originunit: OriginUnit = None
    problem_bool: bool = None
    bridge: str = None
    _is_expanded: bool = None
    # Calculated fields
    _active: bool = None
    _active_hx: dict[int, bool] = None
    _all_acct_cred: bool = None
    _all_acct_debt: bool = None
    _awardheirs: dict[GroupTitle, AwardHeir] = None
    _awardlines: dict[GroupTitle, AwardLine] = None
    _descendant_pledge_count: int = None
    _factheirs: dict[WayTerm, FactHeir] = None
    _fund_ratio: float = None
    fund_coin: FundCoin = None
    _fund_onset: FundNum = None
    _fund_cease: FundNum = None
    _healerlink_ratio: float = None
    _level: int = None
    _range_evaluated: bool = None
    _reasonheirs: dict[WayTerm, ReasonHeir] = None
    _task: bool = None
    _laborheir: LaborHeir = None
    _gogo_calc: float = None
    _stop_calc: float = None

    def is_agenda_concept(self, necessary_rcontext: WayTerm = None) -> bool:
        rcontext_reasonunit_exists = self.rcontext_reasonunit_exists(necessary_rcontext)
        return self.pledge and self._active and rcontext_reasonunit_exists

    def rcontext_reasonunit_exists(self, necessary_rcontext: WayTerm = None) -> bool:
        x_reasons = self.reasonunits.values()
        x_rcontext = necessary_rcontext
        return x_rcontext is None or any(
            reason.rcontext == x_rcontext for reason in x_reasons
        )

    def record_active_hx(
        self, tree_traverse_count: int, prev_active: bool, now_active: bool
    ):
        if tree_traverse_count == 0:
            self._active_hx = {0: now_active}
        elif prev_active != now_active:
            self._active_hx[tree_traverse_count] = now_active

    def set_factheirs(self, facts: dict[WayTerm, FactCore]):
        facts_dict = get_empty_dict_if_None(facts)
        self._factheirs = {}
        for x_factcore in facts_dict.values():
            self._set_factheir(x_factcore)

    def _set_factheir(self, x_fact: FactCore):
        if (
            x_fact.fcontext == self.get_concept_way()
            and self._gogo_calc is not None
            and self._stop_calc is not None
            and self.begin is None
            and self.close is None
        ):
            raise ranged_fact_concept_Exception(
                f"Cannot have fact for range inheritor '{self.get_concept_way()}'. A ranged fact concept must have _begin, _close"
            )
        x_factheir = factheir_shop(
            x_fact.fcontext, x_fact.fstate, x_fact.fopen, x_fact.fnigh
        )
        self.delete_factunit_if_past(x_factheir)
        x_factheir = self.apply_factunit_moldations(x_factheir)
        self._factheirs[x_factheir.fcontext] = x_factheir

    def apply_factunit_moldations(self, factheir: FactHeir) -> FactHeir:
        for factunit in self.factunits.values():
            if factunit.fcontext == factheir.fcontext:
                factheir.mold(factunit)
        return factheir

    def delete_factunit_if_past(self, factheir: FactHeir):
        delete_factunit = False
        for factunit in self.factunits.values():
            if (
                factunit.fcontext == factheir.fcontext
                and factunit.fnigh is not None
                and factheir.fopen is not None
            ) and factunit.fnigh < factheir.fopen:
                delete_factunit = True

        if delete_factunit:
            del self.factunits[factunit.fcontext]

    def set_factunit(self, factunit: FactUnit):
        self.factunits[factunit.fcontext] = factunit

    def factunit_exists(self, x_fcontext: WayTerm) -> bool:
        return self.factunits.get(x_fcontext) != None

    def get_factunits_dict(self) -> dict[WayTerm, str]:
        return get_dict_from_factunits(self.factunits)

    def set_factunit_to_complete(self, fcontextunit: FactUnit):
        # if a concept is considered a task then a factheir.fopen attribute can be increased to
        # a number <= factheir.fnigh so the concept no longer is a task. This method finds
        # the minimal factheir.fopen to modify concept._task is False. concept_core._factheir cannot be straight up manipulated
        # so it is mandatory that concept._factunit is different.
        # self.set_factunits(rcontext=fact, fact=rcontext, popen=pnigh, pnigh=fnigh)
        self.factunits[fcontextunit.fcontext] = factunit_shop(
            fcontext=fcontextunit.fcontext,
            fstate=fcontextunit.fcontext,
            fopen=fcontextunit.fnigh,
            fnigh=fcontextunit.fnigh,
        )

    def del_factunit(self, fcontext: WayTerm):
        self.factunits.pop(fcontext)

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
        for x_concept in self._kids.values():
            x_gogo_in_range = (
                x_gogo >= x_concept._gogo_calc and x_gogo < x_concept._stop_calc
            )
            x_stop_in_range = (
                x_stop > x_concept._gogo_calc and x_stop < x_concept._stop_calc
            )
            both_in_range = (
                x_gogo <= x_concept._gogo_calc and x_stop >= x_concept._stop_calc
            )

            if x_gogo_in_range or x_stop_in_range or both_in_range:
                x_dict[x_concept.concept_label] = x_concept
        return x_dict

    def get_obj_key(self) -> LabelTerm:
        return self.concept_label

    def get_concept_way(self) -> WayTerm:
        if self.parent_way in (None, ""):
            return create_way(self.concept_label, bridge=self.bridge)
        else:
            return create_way(self.parent_way, self.concept_label, bridge=self.bridge)

    def clear_descendant_pledge_count(self):
        self._descendant_pledge_count = None

    def set_descendant_pledge_count_zero_if_None(self):
        if self._descendant_pledge_count is None:
            self._descendant_pledge_count = 0

    def add_to_descendant_pledge_count(self, x_int: int):
        self.set_descendant_pledge_count_zero_if_None()
        self._descendant_pledge_count += x_int

    def get_descendant_ways_from_kids(self) -> dict[WayTerm, int]:
        descendant_ways = {}
        to_evaluate_concepts = list(self._kids.values())
        count_x = 0
        max_count = 1000
        while to_evaluate_concepts != [] and count_x < max_count:
            x_concept = to_evaluate_concepts.pop()
            descendant_ways[x_concept.get_concept_way()] = -1
            to_evaluate_concepts.extend(x_concept._kids.values())
            count_x += 1

        if count_x == max_count:
            raise ConceptGetDescendantsException(
                f"Concept '{self.get_concept_way()}' either has an infinite loop or more than {max_count} descendants."
            )

        return descendant_ways

    def clear_all_acct_cred_debt(self):
        self._all_acct_cred = None
        self._all_acct_debt = None

    def set_level(self, parent_level):
        self._level = parent_level + 1

    def set_parent_way(self, parent_way):
        self.parent_way = parent_way

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

        for ib in self.awardlinks.values():
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
        give_allot = allot_scale(give_ledger, x_fund_share, self.fund_coin)
        take_allot = allot_scale(take_ledger, x_fund_share, self.fund_coin)
        for x_awardee_title, x_awardheir in self._awardheirs.items():
            x_awardheir._fund_give = give_allot.get(x_awardee_title)
            x_awardheir._fund_take = take_allot.get(x_awardee_title)

    def clear_awardlines(self):
        self._awardlines = {}

    def set_concept_label(self, concept_label: str):
        if (
            self.root
            and concept_label is not None
            and concept_label != self.fisc_label
            and self.fisc_label is not None
        ):
            raise Concept_root_LabelNotEmptyException(
                f"Cannot set conceptroot to string different than '{self.fisc_label}'"
            )
        elif self.root and self.fisc_label is None:
            self.concept_label = root_label()
        # elif concept_label is not None:
        else:
            self.concept_label = concept_label

    def set_bridge(self, new_bridge: str):
        old_bridge = deepcopy(self.bridge)
        if old_bridge is None:
            old_bridge = default_bridge_if_None()
        self.bridge = default_bridge_if_None(new_bridge)
        if old_bridge != self.bridge:
            self._find_replace_bridge(old_bridge)

    def _find_replace_bridge(self, old_bridge):
        self.parent_way = replace_bridge(self.parent_way, old_bridge, self.bridge)

        new_reasonunits = {}
        for reasonunit_way, reasonunit_obj in self.reasonunits.items():
            new_reasonunit_way = replace_bridge(
                way=reasonunit_way,
                old_bridge=old_bridge,
                new_bridge=self.bridge,
            )
            reasonunit_obj.set_bridge(self.bridge)
            new_reasonunits[new_reasonunit_way] = reasonunit_obj
        self.reasonunits = new_reasonunits

        new_factunits = {}
        for factunit_way, x_factunit in self.factunits.items():
            new_rcontext_way = replace_bridge(
                way=factunit_way,
                old_bridge=old_bridge,
                new_bridge=self.bridge,
            )
            x_factunit.fcontext = new_rcontext_way
            new_fstate_way = replace_bridge(
                way=x_factunit.fstate,
                old_bridge=old_bridge,
                new_bridge=self.bridge,
            )
            x_factunit.set_attr(fstate=new_fstate_way)
            new_factunits[new_rcontext_way] = x_factunit
        self.factunits = new_factunits

    def set_originunit_empty_if_None(self):
        if self._originunit is None:
            self._originunit = originunit_shop()

    def get_originunit_dict(self) -> dict[str, str]:
        return self._originunit.get_dict()

    def _set_attrs_to_conceptunit(self, concept_attr: ConceptAttrHolder):
        if concept_attr.mass is not None:
            self.mass = concept_attr.mass
        if concept_attr.uid is not None:
            self._uid = concept_attr.uid
        if concept_attr.reason is not None:
            self.set_reasonunit(reason=concept_attr.reason)
        if (
            concept_attr.reason_rcontext is not None
            and concept_attr.reason_premise is not None
        ):
            self.set_reason_premise(
                rcontext=concept_attr.reason_rcontext,
                premise=concept_attr.reason_premise,
                popen=concept_attr.popen,
                pnigh=concept_attr.reason_pnigh,
                pdivisor=concept_attr.pdivisor,
            )
        if (
            concept_attr.reason_rcontext is not None
            and concept_attr.reason_rconcept_active_requisite is not None
        ):
            self.set_reason_rconcept_active_requisite(
                rcontext=concept_attr.reason_rcontext,
                rconcept_active_requisite=concept_attr.reason_rconcept_active_requisite,
            )
        if concept_attr.laborunit is not None:
            self.laborunit = concept_attr.laborunit
        if concept_attr.healerlink is not None:
            self.healerlink = concept_attr.healerlink
        if concept_attr.begin is not None:
            self.begin = concept_attr.begin
        if concept_attr.close is not None:
            self.close = concept_attr.close
        if concept_attr.gogo_want is not None:
            self.gogo_want = concept_attr.gogo_want
        if concept_attr.stop_want is not None:
            self.stop_want = concept_attr.stop_want
        if concept_attr.addin is not None:
            self.addin = concept_attr.addin
        if concept_attr.numor is not None:
            self.numor = concept_attr.numor
        if concept_attr.denom is not None:
            self.denom = concept_attr.denom
        if concept_attr.morph is not None:
            self.morph = concept_attr.morph
        if concept_attr.descendant_pledge_count is not None:
            self._descendant_pledge_count = concept_attr.descendant_pledge_count
        if concept_attr.all_acct_cred is not None:
            self._all_acct_cred = concept_attr.all_acct_cred
        if concept_attr.all_acct_debt is not None:
            self._all_acct_debt = concept_attr.all_acct_debt
        if concept_attr.awardlink is not None:
            self.set_awardlink(awardlink=concept_attr.awardlink)
        if concept_attr.awardlink_del is not None:
            self.del_awardlink(awardee_title=concept_attr.awardlink_del)
        if concept_attr.is_expanded is not None:
            self._is_expanded = concept_attr.is_expanded
        if concept_attr.pledge is not None:
            self.pledge = concept_attr.pledge
        if concept_attr.factunit is not None:
            self.set_factunit(concept_attr.factunit)
        if concept_attr.problem_bool is not None:
            self.problem_bool = concept_attr.problem_bool

        self._del_reasonunit_all_cases(
            rcontext=concept_attr.reason_del_premise_rcontext,
            premise=concept_attr.reason_del_premise_pstate,
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
        r_concept_numor = get_1_if_None(self.numor)
        r_concept_denom = get_1_if_None(self.denom)
        r_concept_addin = get_0_if_None(self.addin)

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
            self._gogo_calc = self._gogo_calc + r_concept_addin
            self._stop_calc = self._stop_calc + r_concept_addin
            self._gogo_calc = (self._gogo_calc * r_concept_numor) / r_concept_denom
            self._stop_calc = (self._stop_calc * r_concept_numor) / r_concept_denom
        self._range_evaluated = True

    def _del_reasonunit_all_cases(self, rcontext: WayTerm, premise: WayTerm):
        if rcontext is not None and premise is not None:
            self.del_reasonunit_premise(rcontext=rcontext, premise=premise)
            if len(self.reasonunits[rcontext].premises) == 0:
                self.del_reasonunit_rcontext(rcontext=rcontext)

    def set_reason_rconcept_active_requisite(
        self, rcontext: WayTerm, rconcept_active_requisite: str
    ):
        x_reasonunit = self._get_or_create_reasonunit(rcontext=rcontext)
        if rconcept_active_requisite is False:
            x_reasonunit.rconcept_active_requisite = False
        elif rconcept_active_requisite == "Set to Ignore":
            x_reasonunit.rconcept_active_requisite = None
        elif rconcept_active_requisite:
            x_reasonunit.rconcept_active_requisite = True

    def _get_or_create_reasonunit(self, rcontext: WayTerm) -> ReasonUnit:
        x_reasonunit = None
        try:
            x_reasonunit = self.reasonunits[rcontext]
        except Exception:
            x_reasonunit = reasonunit_shop(rcontext, bridge=self.bridge)
            self.reasonunits[rcontext] = x_reasonunit
        return x_reasonunit

    def set_reason_premise(
        self,
        rcontext: WayTerm,
        premise: WayTerm,
        popen: float,
        pnigh: float,
        pdivisor: int,
    ):
        x_reasonunit = self._get_or_create_reasonunit(rcontext=rcontext)
        x_reasonunit.set_premise(
            premise=premise, popen=popen, pnigh=pnigh, pdivisor=pdivisor
        )

    def del_reasonunit_rcontext(self, rcontext: WayTerm):
        try:
            self.reasonunits.pop(rcontext)
        except KeyError as e:
            raise InvalidConceptException(f"No ReasonUnit at '{rcontext}'") from e

    def del_reasonunit_premise(self, rcontext: WayTerm, premise: WayTerm):
        reason_unit = self.reasonunits[rcontext]
        reason_unit.del_premise(premise=premise)

    def add_kid(self, concept_kid):
        self._kids[concept_kid.concept_label] = concept_kid
        self._kids = dict(sorted(self._kids.items()))

    def get_kid(self, concept_kid_concept_label: LabelTerm, if_missing_create=False):
        if if_missing_create is False:
            return self._kids.get(concept_kid_concept_label)
        try:
            return self._kids[concept_kid_concept_label]
        except Exception:
            KeyError
            self.add_kid(conceptunit_shop(concept_kid_concept_label))
            return_concept = self._kids.get(concept_kid_concept_label)
        return return_concept

    def del_kid(self, concept_kid_concept_label: LabelTerm):
        self._kids.pop(concept_kid_concept_label)

    def clear_kids(self):
        self._kids = {}

    def get_kids_mass_sum(self) -> float:
        return sum(x_kid.mass for x_kid in self._kids.values())

    def set_awardlink(self, awardlink: AwardLink):
        self.awardlinks[awardlink.awardee_title] = awardlink

    def get_awardlink(self, awardee_title: GroupTitle) -> AwardLink:
        return self.awardlinks.get(awardee_title)

    def del_awardlink(self, awardee_title: GroupTitle):
        try:
            self.awardlinks.pop(awardee_title)
        except KeyError as e:
            raise (f"Cannot delete awardlink '{awardee_title}'.") from e

    def awardlink_exists(self, x_awardee_title: GroupTitle) -> bool:
        return self.awardlinks.get(x_awardee_title) != None

    def set_reasonunit(self, reason: ReasonUnit):
        reason.bridge = self.bridge
        self.reasonunits[reason.rcontext] = reason

    def reasonunit_exists(self, x_rcontext: WayTerm) -> bool:
        return self.reasonunits.get(x_rcontext) != None

    def get_reasonunit(self, rcontext: WayTerm) -> ReasonUnit:
        return self.reasonunits.get(rcontext)

    def set_reasonheirs_status(self):
        self.clear_reasonheirs_status()
        for x_reasonheir in self._reasonheirs.values():
            x_reasonheir.set_status(factheirs=self._factheirs)

    def set_active_attrs(
        self,
        tree_traverse_count: int,
        groupunits: dict[GroupTitle, GroupUnit] = None,
        bud_owner_name: AcctName = None,
    ):
        prev_to_now_active = deepcopy(self._active)
        self._active = self._create_active_bool(groupunits, bud_owner_name)
        self._set_concept_task()
        self.record_active_hx(tree_traverse_count, prev_to_now_active, self._active)

    def _set_concept_task(self):
        self._task = False
        if self.pledge and self._active and self._reasonheirs_satisfied():
            self._task = True

    def _reasonheirs_satisfied(self) -> bool:
        return self._reasonheirs == {} or self._any_reasonheir_task_true()

    def _any_reasonheir_task_true(self) -> bool:
        return any(x_reasonheir._task for x_reasonheir in self._reasonheirs.values())

    def _create_active_bool(
        self, groupunits: dict[GroupTitle, GroupUnit], bud_owner_name: AcctName
    ) -> bool:
        self.set_reasonheirs_status()
        active_bool = self._are_all_reasonheir_active_true()
        if (
            active_bool
            and groupunits != {}
            and bud_owner_name is not None
            and self._laborheir._laborlinks != {}
        ):
            self._laborheir.set_owner_name_labor(groupunits, bud_owner_name)
            if self._laborheir._owner_name_labor is False:
                active_bool = False
        return active_bool

    def set_range_factheirs(
        self, bud_concept_dict: dict[WayTerm,], range_inheritors: dict[WayTerm, WayTerm]
    ):
        for reason_rcontext in self._reasonheirs.keys():
            if range_root_way := range_inheritors.get(reason_rcontext):
                all_concepts = all_concepts_between(
                    bud_concept_dict, range_root_way, reason_rcontext
                )
                self._create_factheir(all_concepts, range_root_way, reason_rcontext)

    def _create_factheir(
        self, all_concepts: list, range_root_way: WayTerm, reason_rcontext: WayTerm
    ):
        range_root_factheir = self._factheirs.get(range_root_way)
        old_popen = range_root_factheir.fopen
        old_pnigh = range_root_factheir.fnigh
        x_rangeunit = concepts_calculated_range(all_concepts, old_popen, old_pnigh)
        new_factheir_popen = x_rangeunit.gogo
        new_factheir_pnigh = x_rangeunit.stop
        new_factheir_obj = factheir_shop(reason_rcontext)
        new_factheir_obj.set_attr(
            reason_rcontext, new_factheir_popen, new_factheir_pnigh
        )
        self._set_factheir(new_factheir_obj)

    def _are_all_reasonheir_active_true(self) -> bool:
        x_reasonheirs = self._reasonheirs.values()
        return all(x_reasonheir._status != False for x_reasonheir in x_reasonheirs)

    def clear_reasonheirs_status(self):
        for reason in self._reasonheirs.values():
            reason.clear_status()

    def _coalesce_with_reasonunits(
        self, reasonheirs: dict[WayTerm, ReasonHeir]
    ) -> dict[WayTerm, ReasonHeir]:
        new_reasonheirs = deepcopy(reasonheirs)
        new_reasonheirs |= self.reasonunits
        return new_reasonheirs

    def set_reasonheirs(
        self, bud_concept_dict: dict[WayTerm,], reasonheirs: dict[WayTerm, ReasonCore]
    ):
        coalesced_reasons = self._coalesce_with_reasonunits(reasonheirs)
        self._reasonheirs = {}
        for old_reasonheir in coalesced_reasons.values():
            old_rcontext = old_reasonheir.rcontext
            old_active_requisite = old_reasonheir.rconcept_active_requisite
            new_reasonheir = reasonheir_shop(old_rcontext, None, old_active_requisite)
            new_reasonheir.inherit_from_reasonheir(old_reasonheir)

            if rcontext_concept := bud_concept_dict.get(old_reasonheir.rcontext):
                new_reasonheir.set_rconcept_active_value(rcontext_concept._active)
            self._reasonheirs[new_reasonheir.rcontext] = new_reasonheir

    def set_conceptroot_inherit_reasonheirs(self):
        self._reasonheirs = {}
        for x_reasonunit in self.reasonunits.values():
            new_reasonheir = reasonheir_shop(x_reasonunit.rcontext)
            new_reasonheir.inherit_from_reasonheir(x_reasonunit)
            self._reasonheirs[new_reasonheir.rcontext] = new_reasonheir

    def get_reasonheir(self, rcontext: WayTerm) -> ReasonHeir:
        return self._reasonheirs.get(rcontext)

    def get_reasonunits_dict(self):
        return {
            rcontext: reason.get_dict() for rcontext, reason in self.reasonunits.items()
        }

    def get_kids_dict(self) -> dict[GroupTitle,]:
        return {c_way: kid.get_dict() for c_way, kid in self._kids.items()}

    def get_awardlinks_dict(self) -> dict[GroupTitle, dict]:
        x_awardlinks = self.awardlinks.items()
        return {
            x_awardee_title: awardlink.get_dict()
            for x_awardee_title, awardlink in x_awardlinks
        }

    def is_kidless(self) -> bool:
        return self._kids == {}

    def is_math(self) -> bool:
        return self.begin is not None and self.close is not None

    def awardheir_exists(self) -> bool:
        return self._awardheirs != {}

    def get_dict(self) -> dict[str, str]:
        x_dict = {"mass": self.mass}

        if self.concept_label is not None:
            x_dict["concept_label"] = self.concept_label
        if self._uid is not None:
            x_dict["_uid"] = self._uid
        if self._kids not in [{}, None]:
            x_dict["_kids"] = self.get_kids_dict()
        if self.reasonunits not in [{}, None]:
            x_dict["reasonunits"] = self.get_reasonunits_dict()
        if self.laborunit not in [None, laborunit_shop()]:
            x_dict["laborunit"] = self.get_laborunit_dict()
        if self.healerlink not in [None, healerlink_shop()]:
            x_dict["healerlink"] = self.healerlink.get_dict()
        if self.awardlinks not in [{}, None]:
            x_dict["awardlinks"] = self.get_awardlinks_dict()
        if self._originunit not in [None, originunit_shop()]:
            x_dict["originunit"] = self.get_originunit_dict()
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
        if self.pledge:
            x_dict["pledge"] = self.pledge
        if self.problem_bool:
            x_dict["problem_bool"] = self.problem_bool
        if self.factunits not in [{}, None]:
            x_dict["factunits"] = self.get_factunits_dict()
        if self._is_expanded is False:
            x_dict["_is_expanded"] = self._is_expanded

        return x_dict

    def find_replace_way(self, old_way: WayTerm, new_way: WayTerm):
        if is_sub_way(ref_way=self.parent_way, sub_way=old_way):
            self.parent_way = rebuild_way(self.parent_way, old_way, new_way)

        self.reasonunits == find_replace_way_key_dict(
            dict_x=self.reasonunits, old_way=old_way, new_way=new_way
        )

        self.factunits == find_replace_way_key_dict(
            dict_x=self.factunits, old_way=old_way, new_way=new_way
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
        self._laborheir.set_laborlinks(
            parent_laborheir=parent_laborheir,
            laborunit=self.laborunit,
            groupunits=groupunits,
        )

    def get_laborunit_dict(self) -> dict:
        return self.laborunit.get_dict()


def conceptunit_shop(
    concept_label: LabelTerm = None,
    _uid: int = None,  # Calculated field?
    parent_way: WayTerm = None,
    _kids: dict = None,
    mass: int = 1,
    awardlinks: dict[GroupTitle, AwardLink] = None,
    _awardheirs: dict[GroupTitle, AwardHeir] = None,  # Calculated field
    _awardlines: dict[GroupTitle, AwardLink] = None,  # Calculated field
    reasonunits: dict[WayTerm, ReasonUnit] = None,
    _reasonheirs: dict[WayTerm, ReasonHeir] = None,  # Calculated field
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
    pledge: bool = None,
    _originunit: OriginUnit = None,
    root: bool = None,
    fisc_label: FiscLabel = None,
    problem_bool: bool = None,
    # Calculated fields
    _level: int = None,
    _fund_ratio: float = None,
    fund_coin: FundCoin = None,
    _fund_onset: FundNum = None,
    _fund_cease: FundNum = None,
    _task: bool = None,
    _active: bool = None,
    _descendant_pledge_count: int = None,
    _all_acct_cred: bool = None,
    _all_acct_debt: bool = None,
    _is_expanded: bool = True,
    _active_hx: dict[int, bool] = None,
    bridge: str = None,
    _healerlink_ratio: float = None,
) -> ConceptUnit:
    fisc_label = root_label() if fisc_label is None else fisc_label
    x_healerlink = healerlink_shop() if healerlink is None else healerlink

    x_conceptkid = ConceptUnit(
        concept_label=None,
        _uid=_uid,
        parent_way=parent_way,
        _kids=get_empty_dict_if_None(_kids),
        mass=get_positive_int(mass),
        awardlinks=get_empty_dict_if_None(awardlinks),
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
        pledge=get_False_if_None(pledge),
        problem_bool=get_False_if_None(problem_bool),
        _originunit=_originunit,
        root=get_False_if_None(root),
        fisc_label=fisc_label,
        # Calculated fields
        _level=_level,
        _fund_ratio=_fund_ratio,
        fund_coin=default_fund_coin_if_None(fund_coin),
        _fund_onset=_fund_onset,
        _fund_cease=_fund_cease,
        _task=_task,
        _active=_active,
        _descendant_pledge_count=_descendant_pledge_count,
        _all_acct_cred=_all_acct_cred,
        _all_acct_debt=_all_acct_debt,
        _is_expanded=_is_expanded,
        _active_hx=get_empty_dict_if_None(_active_hx),
        bridge=default_bridge_if_None(bridge),
        _healerlink_ratio=get_0_if_None(_healerlink_ratio),
    )
    if x_conceptkid.root:
        x_conceptkid.set_concept_label(concept_label=fisc_label)
    else:
        x_conceptkid.set_concept_label(concept_label=concept_label)
    x_conceptkid.set_laborunit_empty_if_None()
    x_conceptkid.set_originunit_empty_if_None()
    return x_conceptkid


def get_obj_from_concept_dict(x_dict: dict[str, dict], dict_key: str) -> any:
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
    elif dict_key == "originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else originunit_shop()
        )
    elif dict_key == "factunits":
        facts_dict = get_empty_dict_if_None(x_dict.get(dict_key))
        return factunits_get_from_dict(facts_dict)
    elif dict_key == "awardlinks":
        return (
            awardlinks_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else awardlinks_get_from_dict({})
        )
    elif dict_key in {"_kids"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else {}
    elif dict_key in {"pledge", "problem_bool"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else False
    elif dict_key in {"_is_expanded"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else True
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else None


def all_concepts_between(
    bud_concept_dict: dict[WayTerm, ConceptUnit],
    src_way: WayTerm,
    dst_rcontext: WayTerm,
) -> list[ConceptUnit]:
    all_ways = all_wayterms_between(src_way, dst_rcontext)
    return [bud_concept_dict.get(x_way) for x_way in all_ways]


def concepts_calculated_range(
    concept_list: list[ConceptUnit], x_gogo: float, x_stop: float
) -> RangeUnit:
    for x_concept in concept_list:
        if x_concept.addin:
            x_gogo += get_0_if_None(x_concept.addin)
            x_stop += get_0_if_None(x_concept.addin)
        if (x_concept.numor or x_concept.denom) and not x_concept.morph:
            x_gogo *= get_1_if_None(x_concept.numor) / get_1_if_None(x_concept.denom)
            x_stop *= get_1_if_None(x_concept.numor) / get_1_if_None(x_concept.denom)
        if x_concept.denom and x_concept.morph:
            x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, x_concept.denom)
            x_gogo = x_rangeunit.gogo
            x_stop = x_rangeunit.stop
    return RangeUnit(x_gogo, x_stop)
