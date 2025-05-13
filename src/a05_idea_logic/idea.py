from src.a00_data_toolbox.dict_toolbox import (
    get_empty_dict_if_None,
    get_0_if_None,
    get_1_if_None,
    get_False_if_None,
    get_positive_int,
)
from src.a01_way_logic.way import (
    WayStr,
    TagStr,
    is_sub_way,
    get_default_fisc_tag as root_tag,
    all_waystrs_between,
    create_way,
    default_bridge_if_None,
    replace_bridge,
    FiscTag,
    AcctName,
    GroupLabel,
    WayStr,
    rebuild_way,
    find_replace_way_key_dict,
)
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import (
    FundCoin,
    FundNum,
    default_fund_coin_if_None,
)
from src.a02_finance_logic.test.range_toolbox import get_morphed_rangeunit, RangeUnit
from src.a03_group_logic.group import (
    AwardHeir,
    AwardLink,
    awardlinks_get_from_dict,
    AwardLine,
    awardline_shop,
    awardheir_shop,
    GroupUnit,
)

from src.a04_reason_logic.reason_labor import (
    LaborUnit,
    LaborHeir,
    laborunit_shop,
    laborheir_shop,
    laborunit_get_from_dict,
)
from src.a04_reason_logic.reason_idea import (
    FactCore,
    FactHeir,
    factheir_shop,
    ReasonCore,
    ReasonUnit,
    reasonunit_shop,
    WayStr,
    FactUnit,
    factunit_shop,
    ReasonHeir,
    reasonheir_shop,
    reasons_get_from_dict,
    factunits_get_from_dict,
    get_dict_from_factunits,
)
from src.a05_idea_logic.healer import (
    HealerLink,
    healerlink_shop,
    healerlink_get_from_dict,
)

from src.a05_idea_logic.origin import (
    OriginUnit,
    originunit_get_from_dict,
    originunit_shop,
)
from dataclasses import dataclass
from copy import deepcopy


class InvalidIdeaException(Exception):
    pass


class IdeaGetDescendantsException(Exception):
    pass


class Idea_root_TagNotEmptyException(Exception):
    pass


class ranged_fact_idea_Exception(Exception):
    pass


@dataclass
class IdeaAttrHolder:
    mass: int = None
    uid: int = None
    reason: ReasonUnit = None
    reason_rcontext: WayStr = None
    reason_premise: WayStr = None
    popen: float = None
    reason_pnigh: float = None
    pdivisor: int = None
    reason_del_premise_rcontext: WayStr = None
    reason_del_premise_pbranch: WayStr = None
    reason_rcontext_idea_active_requisite: str = None
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
    awardlink_del: GroupLabel = None
    is_expanded: bool = None
    problem_bool: bool = None

    def set_premise_range_attributes_influenced_by_premise_idea(
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


def ideaattrholder_shop(
    mass: int = None,
    uid: int = None,
    reason: ReasonUnit = None,
    reason_rcontext: WayStr = None,
    reason_premise: WayStr = None,
    popen: float = None,
    reason_pnigh: float = None,
    pdivisor: int = None,
    reason_del_premise_rcontext: WayStr = None,
    reason_del_premise_pbranch: WayStr = None,
    reason_rcontext_idea_active_requisite: str = None,
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
    awardlink_del: GroupLabel = None,
    is_expanded: bool = None,
    problem_bool: bool = None,
) -> IdeaAttrHolder:
    return IdeaAttrHolder(
        mass=mass,
        uid=uid,
        reason=reason,
        reason_rcontext=reason_rcontext,
        reason_premise=reason_premise,
        popen=popen,
        reason_pnigh=reason_pnigh,
        pdivisor=pdivisor,
        reason_del_premise_rcontext=reason_del_premise_rcontext,
        reason_del_premise_pbranch=reason_del_premise_pbranch,
        reason_rcontext_idea_active_requisite=reason_rcontext_idea_active_requisite,
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
class IdeaUnit:
    idea_tag: TagStr = None
    mass: int = None
    parent_way: WayStr = None
    root: bool = None
    _kids: dict[WayStr,] = None
    fisc_tag: FiscTag = None
    _uid: int = None  # Calculated field?
    awardlinks: dict[GroupLabel, AwardLink] = None
    reasonunits: dict[WayStr, ReasonUnit] = None
    laborunit: LaborUnit = None
    factunits: dict[WayStr, FactUnit] = None
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
    _awardheirs: dict[GroupLabel, AwardHeir] = None
    _awardlines: dict[GroupLabel, AwardLine] = None
    _descendant_pledge_count: int = None
    _factheirs: dict[WayStr, FactHeir] = None
    _fund_ratio: float = None
    fund_coin: FundCoin = None
    _fund_onset: FundNum = None
    _fund_cease: FundNum = None
    _healerlink_ratio: float = None
    _level: int = None
    _range_evaluated: bool = None
    _reasonheirs: dict[WayStr, ReasonHeir] = None
    _task: bool = None
    _laborheir: LaborHeir = None
    _gogo_calc: float = None
    _stop_calc: float = None

    def is_agenda_idea(self, necessary_rcontext: WayStr = None) -> bool:
        rcontext_reasonunit_exists = self.rcontext_reasonunit_exists(necessary_rcontext)
        return self.pledge and self._active and rcontext_reasonunit_exists

    def rcontext_reasonunit_exists(self, necessary_rcontext: WayStr = None) -> bool:
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

    def set_factheirs(self, facts: dict[WayStr, FactCore]):
        facts_dict = get_empty_dict_if_None(facts)
        self._factheirs = {}
        for x_factcore in facts_dict.values():
            self._set_factheir(x_factcore)

    def _set_factheir(self, x_fact: FactCore):
        if (
            x_fact.fcontext == self.get_idea_way()
            and self._gogo_calc is not None
            and self._stop_calc is not None
            and self.begin is None
            and self.close is None
        ):
            raise ranged_fact_idea_Exception(
                f"Cannot have fact for range inheritor '{self.get_idea_way()}'. A ranged fact idea must have _begin, _close attributes"
            )
        x_factheir = factheir_shop(
            x_fact.fcontext, x_fact.fbranch, x_fact.fopen, x_fact.fnigh
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

    def factunit_exists(self, x_fcontext: WayStr) -> bool:
        return self.factunits.get(x_fcontext) != None

    def get_factunits_dict(self) -> dict[WayStr, str]:
        return get_dict_from_factunits(self.factunits)

    def set_factunit_to_complete(self, fcontextunit: FactUnit):
        # if a idea is considered a task then a factheir.fopen attribute can be increased to
        # a number <= factheir.fnigh so the idea no longer is a task. This method finds
        # the minimal factheir.fopen to modify idea._task is False. idea_core._factheir cannot be straight up manipulated
        # so it is mandatory that idea._factunit is different.
        # self.set_factunits(rcontext=fact, fact=rcontext, popen=pnigh, pnigh=fnigh)
        self.factunits[fcontextunit.fcontext] = factunit_shop(
            fcontext=fcontextunit.fcontext,
            fbranch=fcontextunit.fcontext,
            fopen=fcontextunit.fnigh,
            fnigh=fcontextunit.fnigh,
        )

    def del_factunit(self, fcontext: WayStr):
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
    ) -> dict[TagStr,]:
        if x_gogo is None and x_stop is None:
            x_gogo = self.gogo_want
            x_gogo = self.stop_want
        elif x_gogo is not None and x_stop is None:
            x_stop = x_gogo

        if x_gogo is None and x_stop is None:
            return self._kids.values()

        x_dict = {}
        for x_idea in self._kids.values():
            x_gogo_in_range = x_gogo >= x_idea._gogo_calc and x_gogo < x_idea._stop_calc
            x_stop_in_range = x_stop > x_idea._gogo_calc and x_stop < x_idea._stop_calc
            both_in_range = x_gogo <= x_idea._gogo_calc and x_stop >= x_idea._stop_calc

            if x_gogo_in_range or x_stop_in_range or both_in_range:
                x_dict[x_idea.idea_tag] = x_idea
        return x_dict

    def get_obj_key(self) -> TagStr:
        return self.idea_tag

    def get_idea_way(self) -> WayStr:
        if self.parent_way in (None, ""):
            return create_way(self.idea_tag, bridge=self.bridge)
        else:
            return create_way(self.parent_way, self.idea_tag, bridge=self.bridge)

    def clear_descendant_pledge_count(self):
        self._descendant_pledge_count = None

    def set_descendant_pledge_count_zero_if_None(self):
        if self._descendant_pledge_count is None:
            self._descendant_pledge_count = 0

    def add_to_descendant_pledge_count(self, x_int: int):
        self.set_descendant_pledge_count_zero_if_None()
        self._descendant_pledge_count += x_int

    def get_descendant_ways_from_kids(self) -> dict[WayStr, int]:
        descendant_ways = {}
        to_evaluate_ideas = list(self._kids.values())
        count_x = 0
        max_count = 1000
        while to_evaluate_ideas != [] and count_x < max_count:
            x_idea = to_evaluate_ideas.pop()
            descendant_ways[x_idea.get_idea_way()] = -1
            to_evaluate_ideas.extend(x_idea._kids.values())
            count_x += 1

        if count_x == max_count:
            raise IdeaGetDescendantsException(
                f"Idea '{self.get_idea_way()}' either has an infinite loop or more than {max_count} descendants."
            )

        return descendant_ways

    def clear_all_acct_cred_debt(self):
        self._all_acct_cred = None
        self._all_acct_debt = None

    def set_level(self, parent_level):
        self._level = parent_level + 1

    def set_parent_way(self, parent_way):
        self.parent_way = parent_way

    def inherit_awardheirs(self, parent_awardheirs: dict[GroupLabel, AwardHeir] = None):
        parent_awardheirs = {} if parent_awardheirs is None else parent_awardheirs
        self._awardheirs = {}
        for ib in parent_awardheirs.values():
            awardheir = awardheir_shop(
                awardee_label=ib.awardee_label,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self._awardheirs[awardheir.awardee_label] = awardheir

        for ib in self.awardlinks.values():
            awardheir = awardheir_shop(
                awardee_label=ib.awardee_label,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self._awardheirs[awardheir.awardee_label] = awardheir

    def set_kidless_awardlines(self):
        # get awardlines from self
        for bh in self._awardheirs.values():
            x_awardline = awardline_shop(
                awardee_label=bh.awardee_label,
                _fund_give=bh._fund_give,
                _fund_take=bh._fund_take,
            )
            self._awardlines[x_awardline.awardee_label] = x_awardline

    def set_awardlines(self, child_awardlines: dict[GroupLabel, AwardLine] = None):
        if child_awardlines is None:
            child_awardlines = {}

        # get awardlines from child
        for bl in child_awardlines.values():
            if self._awardlines.get(bl.awardee_label) is None:
                self._awardlines[bl.awardee_label] = awardline_shop(
                    awardee_label=bl.awardee_label,
                    _fund_give=0,
                    _fund_take=0,
                )

            self._awardlines[bl.awardee_label].add_fund_give_take(
                fund_give=bl._fund_give, fund_take=bl._fund_take
            )

    def set_awardheirs_fund_give_fund_take(self):
        give_ledger = {}
        take_ledger = {}
        for x_awardee_label, x_awardheir in self._awardheirs.items():
            give_ledger[x_awardee_label] = x_awardheir.give_force
            take_ledger[x_awardee_label] = x_awardheir.take_force
        x_fund_share = self.get_fund_share()
        give_allot = allot_scale(give_ledger, x_fund_share, self.fund_coin)
        take_allot = allot_scale(take_ledger, x_fund_share, self.fund_coin)
        for x_awardee_label, x_awardheir in self._awardheirs.items():
            x_awardheir._fund_give = give_allot.get(x_awardee_label)
            x_awardheir._fund_take = take_allot.get(x_awardee_label)

    def clear_awardlines(self):
        self._awardlines = {}

    def set_idea_tag(self, idea_tag: str):
        if (
            self.root
            and idea_tag is not None
            and idea_tag != self.fisc_tag
            and self.fisc_tag is not None
        ):
            raise Idea_root_TagNotEmptyException(
                f"Cannot set idearoot to string different than '{self.fisc_tag}'"
            )
        elif self.root and self.fisc_tag is None:
            self.idea_tag = root_tag()
        # elif idea_tag is not None:
        else:
            self.idea_tag = idea_tag

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
            new_fbranch_way = replace_bridge(
                way=x_factunit.fbranch,
                old_bridge=old_bridge,
                new_bridge=self.bridge,
            )
            x_factunit.set_attr(fbranch=new_fbranch_way)
            new_factunits[new_rcontext_way] = x_factunit
        self.factunits = new_factunits

    def set_originunit_empty_if_None(self):
        if self._originunit is None:
            self._originunit = originunit_shop()

    def get_originunit_dict(self) -> dict[str, str]:
        return self._originunit.get_dict()

    def _set_attrs_to_ideaunit(self, idea_attr: IdeaAttrHolder):
        if idea_attr.mass is not None:
            self.mass = idea_attr.mass
        if idea_attr.uid is not None:
            self._uid = idea_attr.uid
        if idea_attr.reason is not None:
            self.set_reasonunit(reason=idea_attr.reason)
        if (
            idea_attr.reason_rcontext is not None
            and idea_attr.reason_premise is not None
        ):
            self.set_reason_premise(
                rcontext=idea_attr.reason_rcontext,
                premise=idea_attr.reason_premise,
                popen=idea_attr.popen,
                pnigh=idea_attr.reason_pnigh,
                pdivisor=idea_attr.pdivisor,
            )
        if (
            idea_attr.reason_rcontext is not None
            and idea_attr.reason_rcontext_idea_active_requisite is not None
        ):
            self.set_reason_rcontext_idea_active_requisite(
                rcontext=idea_attr.reason_rcontext,
                rcontext_idea_active_requisite=idea_attr.reason_rcontext_idea_active_requisite,
            )
        if idea_attr.laborunit is not None:
            self.laborunit = idea_attr.laborunit
        if idea_attr.healerlink is not None:
            self.healerlink = idea_attr.healerlink
        if idea_attr.begin is not None:
            self.begin = idea_attr.begin
        if idea_attr.close is not None:
            self.close = idea_attr.close
        if idea_attr.gogo_want is not None:
            self.gogo_want = idea_attr.gogo_want
        if idea_attr.stop_want is not None:
            self.stop_want = idea_attr.stop_want
        if idea_attr.addin is not None:
            self.addin = idea_attr.addin
        if idea_attr.numor is not None:
            self.numor = idea_attr.numor
        if idea_attr.denom is not None:
            self.denom = idea_attr.denom
        if idea_attr.morph is not None:
            self.morph = idea_attr.morph
        if idea_attr.descendant_pledge_count is not None:
            self._descendant_pledge_count = idea_attr.descendant_pledge_count
        if idea_attr.all_acct_cred is not None:
            self._all_acct_cred = idea_attr.all_acct_cred
        if idea_attr.all_acct_debt is not None:
            self._all_acct_debt = idea_attr.all_acct_debt
        if idea_attr.awardlink is not None:
            self.set_awardlink(awardlink=idea_attr.awardlink)
        if idea_attr.awardlink_del is not None:
            self.del_awardlink(awardee_label=idea_attr.awardlink_del)
        if idea_attr.is_expanded is not None:
            self._is_expanded = idea_attr.is_expanded
        if idea_attr.pledge is not None:
            self.pledge = idea_attr.pledge
        if idea_attr.factunit is not None:
            self.set_factunit(idea_attr.factunit)
        if idea_attr.problem_bool is not None:
            self.problem_bool = idea_attr.problem_bool

        self._del_reasonunit_all_cases(
            rcontext=idea_attr.reason_del_premise_rcontext,
            premise=idea_attr.reason_del_premise_pbranch,
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
        r_idea_numor = get_1_if_None(self.numor)
        r_idea_denom = get_1_if_None(self.denom)
        r_idea_addin = get_0_if_None(self.addin)

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
            self._gogo_calc = self._gogo_calc + r_idea_addin
            self._stop_calc = self._stop_calc + r_idea_addin
            self._gogo_calc = (self._gogo_calc * r_idea_numor) / r_idea_denom
            self._stop_calc = (self._stop_calc * r_idea_numor) / r_idea_denom
        self._range_evaluated = True

    def _del_reasonunit_all_cases(self, rcontext: WayStr, premise: WayStr):
        if rcontext is not None and premise is not None:
            self.del_reasonunit_premise(rcontext=rcontext, premise=premise)
            if len(self.reasonunits[rcontext].premises) == 0:
                self.del_reasonunit_rcontext(rcontext=rcontext)

    def set_reason_rcontext_idea_active_requisite(
        self, rcontext: WayStr, rcontext_idea_active_requisite: str
    ):
        x_reasonunit = self._get_or_create_reasonunit(rcontext=rcontext)
        if rcontext_idea_active_requisite is False:
            x_reasonunit.rcontext_idea_active_requisite = False
        elif rcontext_idea_active_requisite == "Set to Ignore":
            x_reasonunit.rcontext_idea_active_requisite = None
        elif rcontext_idea_active_requisite:
            x_reasonunit.rcontext_idea_active_requisite = True

    def _get_or_create_reasonunit(self, rcontext: WayStr) -> ReasonUnit:
        x_reasonunit = None
        try:
            x_reasonunit = self.reasonunits[rcontext]
        except Exception:
            x_reasonunit = reasonunit_shop(rcontext, bridge=self.bridge)
            self.reasonunits[rcontext] = x_reasonunit
        return x_reasonunit

    def set_reason_premise(
        self,
        rcontext: WayStr,
        premise: WayStr,
        popen: float,
        pnigh: float,
        pdivisor: int,
    ):
        x_reasonunit = self._get_or_create_reasonunit(rcontext=rcontext)
        x_reasonunit.set_premise(
            premise=premise, popen=popen, pnigh=pnigh, pdivisor=pdivisor
        )

    def del_reasonunit_rcontext(self, rcontext: WayStr):
        try:
            self.reasonunits.pop(rcontext)
        except KeyError as e:
            raise InvalidIdeaException(f"No ReasonUnit at '{rcontext}'") from e

    def del_reasonunit_premise(self, rcontext: WayStr, premise: WayStr):
        reason_unit = self.reasonunits[rcontext]
        reason_unit.del_premise(premise=premise)

    def add_kid(self, idea_kid):
        self._kids[idea_kid.idea_tag] = idea_kid
        self._kids = dict(sorted(self._kids.items()))

    def get_kid(self, idea_kid_idea_tag: TagStr, if_missing_create=False):
        if if_missing_create is False:
            return self._kids.get(idea_kid_idea_tag)
        try:
            return self._kids[idea_kid_idea_tag]
        except Exception:
            KeyError
            self.add_kid(ideaunit_shop(idea_kid_idea_tag))
            return_idea = self._kids.get(idea_kid_idea_tag)
        return return_idea

    def del_kid(self, idea_kid_idea_tag: TagStr):
        self._kids.pop(idea_kid_idea_tag)

    def clear_kids(self):
        self._kids = {}

    def get_kids_mass_sum(self) -> float:
        return sum(x_kid.mass for x_kid in self._kids.values())

    def set_awardlink(self, awardlink: AwardLink):
        self.awardlinks[awardlink.awardee_label] = awardlink

    def get_awardlink(self, awardee_label: GroupLabel) -> AwardLink:
        return self.awardlinks.get(awardee_label)

    def del_awardlink(self, awardee_label: GroupLabel):
        try:
            self.awardlinks.pop(awardee_label)
        except KeyError as e:
            raise (f"Cannot delete awardlink '{awardee_label}'.") from e

    def awardlink_exists(self, x_awardee_label: GroupLabel) -> bool:
        return self.awardlinks.get(x_awardee_label) != None

    def set_reasonunit(self, reason: ReasonUnit):
        reason.bridge = self.bridge
        self.reasonunits[reason.rcontext] = reason

    def reasonunit_exists(self, x_rcontext: WayStr) -> bool:
        return self.reasonunits.get(x_rcontext) != None

    def get_reasonunit(self, rcontext: WayStr) -> ReasonUnit:
        return self.reasonunits.get(rcontext)

    def set_reasonheirs_status(self):
        self.clear_reasonheirs_status()
        for x_reasonheir in self._reasonheirs.values():
            x_reasonheir.set_status(factheirs=self._factheirs)

    def set_active_attrs(
        self,
        tree_traverse_count: int,
        bud_groupunits: dict[GroupLabel, GroupUnit] = None,
        bud_owner_name: AcctName = None,
    ):
        prev_to_now_active = deepcopy(self._active)
        self._active = self._create_active_bool(bud_groupunits, bud_owner_name)
        self._set_idea_task()
        self.record_active_hx(tree_traverse_count, prev_to_now_active, self._active)

    def _set_idea_task(self):
        self._task = False
        if self.pledge and self._active and self._reasonheirs_satisfied():
            self._task = True

    def _reasonheirs_satisfied(self) -> bool:
        return self._reasonheirs == {} or self._any_reasonheir_task_true()

    def _any_reasonheir_task_true(self) -> bool:
        return any(x_reasonheir._task for x_reasonheir in self._reasonheirs.values())

    def _create_active_bool(
        self, bud_groupunits: dict[GroupLabel, GroupUnit], bud_owner_name: AcctName
    ) -> bool:
        self.set_reasonheirs_status()
        active_bool = self._are_all_reasonheir_active_true()
        if (
            active_bool
            and bud_groupunits != {}
            and bud_owner_name is not None
            and self._laborheir._laborlinks != {}
        ):
            self._laborheir.set_owner_name_labor(bud_groupunits, bud_owner_name)
            if self._laborheir._owner_name_labor is False:
                active_bool = False
        return active_bool

    def set_range_factheirs(
        self, bud_idea_dict: dict[WayStr,], range_inheritors: dict[WayStr, WayStr]
    ):
        for reason_rcontext in self._reasonheirs.keys():
            if range_root_way := range_inheritors.get(reason_rcontext):
                all_ideas = all_ideas_between(
                    bud_idea_dict, range_root_way, reason_rcontext
                )
                self._create_factheir(all_ideas, range_root_way, reason_rcontext)

    def _create_factheir(
        self, all_ideas: list, range_root_way: WayStr, reason_rcontext: WayStr
    ):
        range_root_factheir = self._factheirs.get(range_root_way)
        old_popen = range_root_factheir.fopen
        old_pnigh = range_root_factheir.fnigh
        x_rangeunit = ideas_calculated_range(all_ideas, old_popen, old_pnigh)
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
        self, reasonheirs: dict[WayStr, ReasonHeir]
    ) -> dict[WayStr, ReasonHeir]:
        new_reasonheirs = deepcopy(reasonheirs)
        new_reasonheirs |= self.reasonunits
        return new_reasonheirs

    def set_reasonheirs(
        self, bud_idea_dict: dict[WayStr,], reasonheirs: dict[WayStr, ReasonCore]
    ):
        coalesced_reasons = self._coalesce_with_reasonunits(reasonheirs)
        self._reasonheirs = {}
        for old_reasonheir in coalesced_reasons.values():
            old_rcontext = old_reasonheir.rcontext
            old_active_requisite = old_reasonheir.rcontext_idea_active_requisite
            new_reasonheir = reasonheir_shop(old_rcontext, None, old_active_requisite)
            new_reasonheir.inherit_from_reasonheir(old_reasonheir)

            if rcontext_idea := bud_idea_dict.get(old_reasonheir.rcontext):
                new_reasonheir.set_rcontext_idea_active_value(rcontext_idea._active)
            self._reasonheirs[new_reasonheir.rcontext] = new_reasonheir

    def set_idearoot_inherit_reasonheirs(self):
        self._reasonheirs = {}
        for x_reasonunit in self.reasonunits.values():
            new_reasonheir = reasonheir_shop(x_reasonunit.rcontext)
            new_reasonheir.inherit_from_reasonheir(x_reasonunit)
            self._reasonheirs[new_reasonheir.rcontext] = new_reasonheir

    def get_reasonheir(self, rcontext: WayStr) -> ReasonHeir:
        return self._reasonheirs.get(rcontext)

    def get_reasonunits_dict(self):
        return {
            rcontext: reason.get_dict() for rcontext, reason in self.reasonunits.items()
        }

    def get_kids_dict(self) -> dict[GroupLabel,]:
        return {c_way: kid.get_dict() for c_way, kid in self._kids.items()}

    def get_awardlinks_dict(self) -> dict[GroupLabel, dict]:
        x_awardlinks = self.awardlinks.items()
        return {
            x_awardee_label: awardlink.get_dict()
            for x_awardee_label, awardlink in x_awardlinks
        }

    def is_kidless(self) -> bool:
        return self._kids == {}

    def is_math(self) -> bool:
        return self.begin is not None and self.close is not None

    def awardheir_exists(self) -> bool:
        return self._awardheirs != {}

    def get_dict(self) -> dict[str, str]:
        x_dict = {"mass": self.mass}

        if self.idea_tag is not None:
            x_dict["idea_tag"] = self.idea_tag
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

    def find_replace_way(self, old_way: WayStr, new_way: WayStr):
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
        bud_groupunits: dict[GroupLabel, GroupUnit],
    ):
        self._laborheir = laborheir_shop()
        self._laborheir.set_laborlinks(
            parent_laborheir=parent_laborheir,
            laborunit=self.laborunit,
            bud_groupunits=bud_groupunits,
        )

    def get_laborunit_dict(self) -> dict:
        return self.laborunit.get_dict()


def ideaunit_shop(
    idea_tag: TagStr = None,
    _uid: int = None,  # Calculated field?
    parent_way: WayStr = None,
    _kids: dict = None,
    mass: int = 1,
    awardlinks: dict[GroupLabel, AwardLink] = None,
    _awardheirs: dict[GroupLabel, AwardHeir] = None,  # Calculated field
    _awardlines: dict[GroupLabel, AwardLink] = None,  # Calculated field
    reasonunits: dict[WayStr, ReasonUnit] = None,
    _reasonheirs: dict[WayStr, ReasonHeir] = None,  # Calculated field
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
    fisc_tag: FiscTag = None,
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
) -> IdeaUnit:
    fisc_tag = root_tag() if fisc_tag is None else fisc_tag
    x_healerlink = healerlink_shop() if healerlink is None else healerlink

    x_ideakid = IdeaUnit(
        idea_tag=None,
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
        fisc_tag=fisc_tag,
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
    if x_ideakid.root:
        x_ideakid.set_idea_tag(idea_tag=fisc_tag)
    else:
        x_ideakid.set_idea_tag(idea_tag=idea_tag)
    x_ideakid.set_laborunit_empty_if_None()
    x_ideakid.set_originunit_empty_if_None()
    return x_ideakid


def get_obj_from_idea_dict(x_dict: dict[str, dict], dict_key: str) -> any:
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


def all_ideas_between(
    bud_idea_dict: dict[WayStr, IdeaUnit], src_way: WayStr, dst_rcontext: WayStr
) -> list[IdeaUnit]:
    all_ways = all_waystrs_between(src_way, dst_rcontext)
    return [bud_idea_dict.get(x_way) for x_way in all_ways]


def ideas_calculated_range(
    idea_list: list[IdeaUnit], x_gogo: float, x_stop: float
) -> RangeUnit:
    for x_idea in idea_list:
        if x_idea.addin:
            x_gogo += get_0_if_None(x_idea.addin)
            x_stop += get_0_if_None(x_idea.addin)
        if (x_idea.numor or x_idea.denom) and not x_idea.morph:
            x_gogo *= get_1_if_None(x_idea.numor) / get_1_if_None(x_idea.denom)
            x_stop *= get_1_if_None(x_idea.numor) / get_1_if_None(x_idea.denom)
        if x_idea.denom and x_idea.morph:
            x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, x_idea.denom)
            x_gogo = x_rangeunit.gogo
            x_stop = x_rangeunit.stop
    return RangeUnit(x_gogo, x_stop)
