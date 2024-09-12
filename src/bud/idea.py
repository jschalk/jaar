from src._instrument.python_tool import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_1_if_None,
    get_False_if_None,
    get_positive_int,
)
from src._road.finance import FundCoin, FundNum, allot_scale, default_fund_coin_if_none
from src._road.range_toolbox import get_morphed_rangeunit, RangeUnit
from src._road.road import (
    RoadUnit,
    RoadNode,
    is_sub_road,
    get_default_pecun_id_roadnode as root_label,
    all_roadunits_between,
    create_road as road_create_road,
    default_road_delimiter_if_none,
    replace_road_delimiter,
    PecunID,
    AcctID,
    GroupID,
    RoadUnit,
    rebuild_road,
    find_replace_road_key_dict,
)
from src.bud.healer import HealerLink, healerlink_shop, healerlink_get_from_dict
from src.bud.reason_team import (
    TeamUnit,
    TeamHeir,
    teamunit_shop,
    teamheir_shop,
    teamunit_get_from_dict,
)
from src.bud.reason_idea import (
    FactCore,
    FactHeir,
    factheir_shop,
    ReasonCore,
    ReasonUnit,
    reasonunit_shop,
    RoadUnit,
    FactUnit,
    factunit_shop,
    ReasonHeir,
    reasonheir_shop,
    reasons_get_from_dict,
    factunits_get_from_dict,
)
from src.bud.group import (
    AwardHeir,
    AwardLink,
    awardlinks_get_from_dict,
    AwardLine,
    awardline_shop,
    awardheir_shop,
    GroupBox,
)
from src.bud.origin import OriginUnit, originunit_get_from_dict
from src.bud.origin import originunit_shop
from dataclasses import dataclass
from copy import deepcopy


class InvalidIdeaException(Exception):
    pass


class IdeaGetDescendantsException(Exception):
    pass


class Idea_root_LabelNotEmptyException(Exception):
    pass


class ranged_fact_idea_Exception(Exception):
    pass


@dataclass
class IdeaAttrFilter:
    mass: int = None
    uid: int = None
    reason: ReasonUnit = None
    reason_base: RoadUnit = None
    reason_premise: RoadUnit = None
    reason_premise_open: float = None
    reason_premise_nigh: float = None
    reason_premise_divisor: int = None
    reason_del_premise_base: RoadUnit = None
    reason_del_premise_need: RoadUnit = None
    reason_base_idea_active_requisite: str = None
    teamunit: TeamUnit = None
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
    awardlink_del: GroupID = None
    is_expanded: bool = None
    problem_bool: bool = None

    def get_premise_need(self):
        return self.reason_premise

    def set_premise_range_attributes_influenced_by_premise_idea(
        self,
        premise_open,
        premise_nigh,
        # premise_numor,
        premise_denom,
        # premise_morph,
    ):
        if self.reason_premise is not None:
            if self.reason_premise_open is None:
                self.reason_premise_open = premise_open
            if self.reason_premise_nigh is None:
                self.reason_premise_nigh = premise_nigh
            # if self.reason_premise_numor is None:
            #     numor_x = premise_numor
            if self.reason_premise_divisor is None:
                self.reason_premise_divisor = premise_denom
            # if self.reason_premise_morph is None:
            #     self.reason_premise_morph = premise_morph

    def has_reason_premise(self):
        return self.reason_premise is not None


def ideaattrfilter_shop(
    mass: int = None,
    uid: int = None,
    reason: ReasonUnit = None,
    reason_base: RoadUnit = None,
    reason_premise: RoadUnit = None,
    reason_premise_open: float = None,
    reason_premise_nigh: float = None,
    reason_premise_divisor: int = None,
    reason_del_premise_base: RoadUnit = None,
    reason_del_premise_need: RoadUnit = None,
    reason_base_idea_active_requisite: str = None,
    teamunit: TeamUnit = None,
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
    awardlink_del: GroupID = None,
    is_expanded: bool = None,
    problem_bool: bool = None,
) -> IdeaAttrFilter:
    return IdeaAttrFilter(
        mass=mass,
        uid=uid,
        reason=reason,
        reason_base=reason_base,
        reason_premise=reason_premise,
        reason_premise_open=reason_premise_open,
        reason_premise_nigh=reason_premise_nigh,
        reason_premise_divisor=reason_premise_divisor,
        reason_del_premise_base=reason_del_premise_base,
        reason_del_premise_need=reason_del_premise_need,
        reason_base_idea_active_requisite=reason_base_idea_active_requisite,
        teamunit=teamunit,
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
    _label: RoadNode = None
    mass: int = None
    _parent_road: RoadUnit = None
    _root: bool = None
    _kids: dict[RoadUnit,] = None
    _bud_pecun_id: PecunID = None
    _uid: int = None  # Calculated field?
    awardlinks: dict[GroupID, AwardLink] = None
    reasonunits: dict[RoadUnit, ReasonUnit] = None
    teamunit: TeamUnit = None
    factunits: dict[RoadUnit, FactUnit] = None
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
    _road_delimiter: str = None
    _is_expanded: bool = None
    # Calculated fields
    _active: bool = None
    _active_hx: dict[int, bool] = None
    _all_acct_cred: bool = None
    _all_acct_debt: bool = None
    _ancestor_pledge_count: int = None
    _awardheirs: dict[GroupID, AwardHeir] = None
    _awardlines: dict[GroupID, AwardLine] = None
    _descendant_pledge_count: int = None
    _factheirs: dict[RoadUnit, FactHeir] = None
    _fund_ratio: float = None
    _fund_coin: FundCoin = None
    _fund_onset: FundNum = None
    _fund_cease: FundNum = None
    _healerlink_ratio: float = None
    _level: int = None
    _range_evaluated: bool = None
    _reasonheirs: dict[RoadUnit, ReasonHeir] = None
    _task: bool = None
    _teamheir: TeamHeir = None
    _gogo_calc: float = None
    _stop_calc: float = None

    def is_agenda_item(self, necessary_base: RoadUnit = None) -> bool:
        base_reasonunit_exists = self.base_reasonunit_exists(necessary_base)
        return self.pledge and self._active and base_reasonunit_exists

    def base_reasonunit_exists(self, necessary_base: RoadUnit = None) -> bool:
        x_reasons = self.reasonunits.values()
        x_base = necessary_base
        return x_base is None or any(reason.base == x_base for reason in x_reasons)

    def record_active_hx(
        self, tree_traverse_count: int, prev_active: bool, now_active: bool
    ):
        if tree_traverse_count == 0:
            self._active_hx = {0: now_active}
        elif prev_active != now_active:
            self._active_hx[tree_traverse_count] = now_active

    def set_factheirs(self, facts: dict[RoadUnit, FactCore]):
        facts_dict = get_empty_dict_if_none(facts)
        self._factheirs = {}
        for x_factcore in facts_dict.values():
            self._set_factheir(x_factcore)

    def _set_factheir(self, x_fact: FactCore):
        if (
            x_fact.base == self.get_road()
            and self._gogo_calc is not None
            and self._stop_calc is not None
            and self.begin is None
            and self.close is None
        ):
            raise ranged_fact_idea_Exception(
                f"Cannot have fact for range inheritor '{self.get_road()}'. A ranged fact idea must have _begin, _close attributes"
            )
        x_factheir = factheir_shop(x_fact.base, x_fact.pick, x_fact.fopen, x_fact.fnigh)
        self.delete_factunit_if_past(x_factheir)
        x_factheir = self.apply_factunit_transformations(x_factheir)
        self._factheirs[x_factheir.base] = x_factheir

    def apply_factunit_transformations(self, factheir: FactHeir) -> FactHeir:
        for factunit in self.factunits.values():
            if factunit.base == factheir.base:
                factheir.transform(factunit)
        return factheir

    def delete_factunit_if_past(self, factheir: FactHeir):
        delete_factunit = False
        for factunit in self.factunits.values():
            if (
                factunit.base == factheir.base
                and factunit.fnigh is not None
                and factheir.fopen is not None
            ) and factunit.fnigh < factheir.fopen:
                delete_factunit = True

        if delete_factunit:
            del self.factunits[factunit.base]

    def set_factunit(self, factunit: FactUnit):
        self.factunits[factunit.base] = factunit

    def factunit_exists(self, x_base: RoadUnit) -> bool:
        return self.factunits.get(x_base) != None

    def get_factunits_dict(self) -> dict[RoadUnit, FactUnit]:
        return {hc.base: hc.get_dict() for hc in self.factunits.values()}

    def set_factunit_to_complete(self, base_factunit: FactUnit):
        # if a idea is considered a task then a factheir.fopen attribute can be increased to
        # a number <= factheir.fnigh so the idea no longer is a task. This method finds
        # the minimal factheir.fopen to modify idea._task is False. idea_core._factheir cannot be straight up manipulated
        # so it is mandatory that idea._factunit is different.
        # self.set_factunits(base=fact, fact=base, open=premise_nigh, nigh=fact_nigh)
        self.factunits[base_factunit.base] = factunit_shop(
            base=base_factunit.base,
            pick=base_factunit.base,
            fopen=base_factunit.fnigh,
            fnigh=base_factunit.fnigh,
        )

    def del_factunit(self, base: RoadUnit):
        self.factunits.pop(base)

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
    ) -> dict[RoadNode,]:
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
                x_dict[x_idea._label] = x_idea
        return x_dict

    def get_obj_key(self) -> RoadNode:
        return self._label

    def get_road(self) -> RoadUnit:
        if self._parent_road in (None, ""):
            return road_create_road(self._label, delimiter=self._road_delimiter)
        else:
            return road_create_road(
                self._parent_road, self._label, delimiter=self._road_delimiter
            )

    def clear_descendant_pledge_count(self):
        self._descendant_pledge_count = None

    def set_descendant_pledge_count_zero_if_none(self):
        if self._descendant_pledge_count is None:
            self._descendant_pledge_count = 0

    def add_to_descendant_pledge_count(self, x_int: int):
        self.set_descendant_pledge_count_zero_if_none()
        self._descendant_pledge_count += x_int

    def get_descendant_roads_from_kids(self) -> dict[RoadUnit, int]:
        descendant_roads = {}
        to_evaluate_ideas = list(self._kids.values())
        count_x = 0
        max_count = 1000
        while to_evaluate_ideas != [] and count_x < max_count:
            x_idea = to_evaluate_ideas.pop()
            descendant_roads[x_idea.get_road()] = -1
            to_evaluate_ideas.extend(x_idea._kids.values())
            count_x += 1

        if count_x == max_count:
            raise IdeaGetDescendantsException(
                f"Idea '{self.get_road()}' either has an infinite loop or more than {max_count} descendants."
            )

        return descendant_roads

    def clear_all_acct_cred_debt(self):
        self._all_acct_cred = None
        self._all_acct_debt = None

    def set_ancestor_pledge_count(
        self, parent_ancestor_pledge_count: int, parent_pledge: bool
    ):
        x_int = 0
        x_int = 1 if parent_pledge else 0
        self._ancestor_pledge_count = parent_ancestor_pledge_count + x_int

    def set_level(self, parent_level):
        self._level = parent_level + 1

    def set_parent_road(self, parent_road):
        self._parent_road = parent_road

    def inherit_awardheirs(self, parent_awardheirs: dict[GroupID, AwardHeir] = None):
        parent_awardheirs = {} if parent_awardheirs is None else parent_awardheirs
        self._awardheirs = {}
        for ib in parent_awardheirs.values():
            awardheir = awardheir_shop(
                group_id=ib.group_id,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self._awardheirs[awardheir.group_id] = awardheir

        for ib in self.awardlinks.values():
            awardheir = awardheir_shop(
                group_id=ib.group_id,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self._awardheirs[awardheir.group_id] = awardheir

    def set_kidless_awardlines(self):
        # get awardlines from self
        for bh in self._awardheirs.values():
            x_awardline = awardline_shop(
                group_id=bh.group_id,
                _fund_give=bh._fund_give,
                _fund_take=bh._fund_take,
            )
            self._awardlines[x_awardline.group_id] = x_awardline

    def set_awardlines(self, child_awardlines: dict[GroupID, AwardLine] = None):
        if child_awardlines is None:
            child_awardlines = {}

        # get awardlines from child
        for bl in child_awardlines.values():
            if self._awardlines.get(bl.group_id) is None:
                self._awardlines[bl.group_id] = awardline_shop(
                    group_id=bl.group_id,
                    _fund_give=0,
                    _fund_take=0,
                )

            self._awardlines[bl.group_id].add_fund_give_take(
                fund_give=bl._fund_give, fund_take=bl._fund_take
            )

    def set_awardheirs_fund_give_fund_take(self):
        give_ledger = {}
        take_ledger = {}
        for x_group_id, x_awardheir in self._awardheirs.items():
            give_ledger[x_group_id] = x_awardheir.give_force
            take_ledger[x_group_id] = x_awardheir.take_force
        x_fund_share = self.get_fund_share()
        give_allot = allot_scale(give_ledger, x_fund_share, self._fund_coin)
        take_allot = allot_scale(take_ledger, x_fund_share, self._fund_coin)
        for x_group_id, x_awardheir in self._awardheirs.items():
            x_awardheir._fund_give = give_allot.get(x_group_id)
            x_awardheir._fund_take = take_allot.get(x_group_id)

    def clear_awardlines(self):
        self._awardlines = {}

    def set_label(self, _label: str):
        if (
            self._root
            and _label is not None
            and _label != self._bud_pecun_id
            and self._bud_pecun_id is not None
        ):
            raise Idea_root_LabelNotEmptyException(
                f"Cannot set idearoot to string different than '{self._bud_pecun_id}'"
            )
        elif self._root and self._bud_pecun_id is None:
            self._label = root_label()
        # elif _label is not None:
        else:
            self._label = _label

    def set_road_delimiter(self, new_road_delimiter: str):
        old_delimiter = deepcopy(self._road_delimiter)
        if old_delimiter is None:
            old_delimiter = default_road_delimiter_if_none()
        self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)
        if old_delimiter != self._road_delimiter:
            self._find_replace_road_delimiter(old_delimiter)

    def _find_replace_road_delimiter(self, old_delimiter):
        self._parent_road = replace_road_delimiter(
            self._parent_road, old_delimiter, self._road_delimiter
        )

        new_reasonunits = {}
        for reasonunit_road, reasonunit_obj in self.reasonunits.items():
            new_reasonunit_road = replace_road_delimiter(
                road=reasonunit_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            reasonunit_obj.set_delimiter(self._road_delimiter)
            new_reasonunits[new_reasonunit_road] = reasonunit_obj
        self.reasonunits = new_reasonunits

        new_factunits = {}
        for factunit_road, factunit_obj in self.factunits.items():
            new_base_road = replace_road_delimiter(
                road=factunit_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            factunit_obj.base = new_base_road
            new_pick_road = replace_road_delimiter(
                road=factunit_obj.pick,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            factunit_obj.set_attr(pick=new_pick_road)
            new_factunits[new_base_road] = factunit_obj
        self.factunits = new_factunits

    def set_originunit_empty_if_none(self):
        if self._originunit is None:
            self._originunit = originunit_shop()

    def get_originunit_dict(self) -> dict[str, str]:
        return self._originunit.get_dict()

    def _set_attrs_to_ideaunit(self, idea_attr: IdeaAttrFilter):
        if idea_attr.mass is not None:
            self.mass = idea_attr.mass
        if idea_attr.uid is not None:
            self._uid = idea_attr.uid
        if idea_attr.reason is not None:
            self.set_reasonunit(reason=idea_attr.reason)
        if idea_attr.reason_base is not None and idea_attr.reason_premise is not None:
            self.set_reason_premise(
                base=idea_attr.reason_base,
                premise=idea_attr.reason_premise,
                open=idea_attr.reason_premise_open,
                nigh=idea_attr.reason_premise_nigh,
                divisor=idea_attr.reason_premise_divisor,
            )
        if (
            idea_attr.reason_base is not None
            and idea_attr.reason_base_idea_active_requisite is not None
        ):
            self.set_reason_base_idea_active_requisite(
                base=idea_attr.reason_base,
                base_idea_active_requisite=idea_attr.reason_base_idea_active_requisite,
            )
        if idea_attr.teamunit is not None:
            self.teamunit = idea_attr.teamunit
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
            self.del_awardlink(group_id=idea_attr.awardlink_del)
        if idea_attr.is_expanded is not None:
            self._is_expanded = idea_attr.is_expanded
        if idea_attr.pledge is not None:
            self.pledge = idea_attr.pledge
        if idea_attr.factunit is not None:
            self.set_factunit(idea_attr.factunit)
        if idea_attr.problem_bool is not None:
            self.problem_bool = idea_attr.problem_bool

        self._del_reasonunit_all_cases(
            base=idea_attr.reason_del_premise_base,
            premise=idea_attr.reason_del_premise_need,
        )
        self._set_addin_to_zero_if_any_transformations_exist()

    def _set_addin_to_zero_if_any_transformations_exist(self):
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

    def _transform_gogo_calc_stop_calc(self):
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

    def _del_reasonunit_all_cases(self, base: RoadUnit, premise: RoadUnit):
        if base is not None and premise is not None:
            self.del_reasonunit_premise(base=base, premise=premise)
            if len(self.reasonunits[base].premises) == 0:
                self.del_reasonunit_base(base=base)

    def set_reason_base_idea_active_requisite(
        self, base: RoadUnit, base_idea_active_requisite: str
    ):
        x_reasonunit = self._get_or_create_reasonunit(base=base)
        if base_idea_active_requisite is False:
            x_reasonunit.base_idea_active_requisite = False
        elif base_idea_active_requisite == "Set to Ignore":
            x_reasonunit.base_idea_active_requisite = None
        elif base_idea_active_requisite:
            x_reasonunit.base_idea_active_requisite = True

    def _get_or_create_reasonunit(self, base: RoadUnit) -> ReasonUnit:
        x_reasonunit = None
        try:
            x_reasonunit = self.reasonunits[base]
        except Exception:
            x_reasonunit = reasonunit_shop(base, delimiter=self._road_delimiter)
            self.reasonunits[base] = x_reasonunit
        return x_reasonunit

    def set_reason_premise(
        self,
        base: RoadUnit,
        premise: RoadUnit,
        open: float,
        nigh: float,
        divisor: int,
    ):
        x_reasonunit = self._get_or_create_reasonunit(base=base)
        x_reasonunit.set_premise(premise=premise, open=open, nigh=nigh, divisor=divisor)

    def del_reasonunit_base(self, base: RoadUnit):
        try:
            self.reasonunits.pop(base)
        except KeyError as e:
            raise InvalidIdeaException(f"No ReasonUnit at '{base}'") from e

    def del_reasonunit_premise(self, base: RoadUnit, premise: RoadUnit):
        reason_unit = self.reasonunits[base]
        reason_unit.del_premise(premise=premise)

    def add_kid(self, idea_kid):
        self._kids[idea_kid._label] = idea_kid
        self._kids = dict(sorted(self._kids.items()))

    def get_kid(self, idea_kid_label: RoadNode, if_missing_create=False):
        if if_missing_create is False:
            return self._kids.get(idea_kid_label)
        try:
            return self._kids[idea_kid_label]
        except Exception:
            KeyError
            self.add_kid(ideaunit_shop(idea_kid_label))
            return_idea = self._kids.get(idea_kid_label)
        return return_idea

    def del_kid(self, idea_kid_label: RoadNode):
        self._kids.pop(idea_kid_label)

    def clear_kids(self):
        self._kids = {}

    def get_kids_mass_sum(self) -> float:
        return sum(x_kid.mass for x_kid in self._kids.values())

    def set_awardlink(self, awardlink: AwardLink):
        self.awardlinks[awardlink.group_id] = awardlink

    def get_awardlink(self, group_id: GroupID) -> AwardLink:
        return self.awardlinks.get(group_id)

    def del_awardlink(self, group_id: GroupID):
        try:
            self.awardlinks.pop(group_id)
        except KeyError as e:
            raise (f"Cannot delete awardlink '{group_id}'.") from e

    def awardlink_exists(self, x_group_id: GroupID) -> bool:
        return self.awardlinks.get(x_group_id) != None

    def set_reasonunit(self, reason: ReasonUnit):
        reason.delimiter = self._road_delimiter
        self.reasonunits[reason.base] = reason

    def reasonunit_exists(self, x_base: RoadUnit) -> bool:
        return self.reasonunits.get(x_base) != None

    def get_reasonunit(self, base: RoadUnit) -> ReasonUnit:
        return self.reasonunits.get(base)

    def set_reasonheirs_status(self):
        self.clear_reasonheirs_status()
        for x_reasonheir in self._reasonheirs.values():
            x_reasonheir.set_status(factheirs=self._factheirs)

    def set_active_attrs(
        self,
        tree_traverse_count: int,
        bud_groupboxs: dict[GroupID, GroupBox] = None,
        bud_owner_id: AcctID = None,
    ):
        prev_to_now_active = deepcopy(self._active)
        self._active = self._create_active_bool(bud_groupboxs, bud_owner_id)
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
        self, bud_groupboxs: dict[GroupID, GroupBox], bud_owner_id: AcctID
    ) -> bool:
        self.set_reasonheirs_status()
        active_bool = self._are_all_reasonheir_active_true()
        if (
            active_bool
            and bud_groupboxs != {}
            and bud_owner_id is not None
            and self._teamheir._teamlinks != {}
        ):
            self._teamheir.set_owner_id_team(bud_groupboxs, bud_owner_id)
            if self._teamheir._owner_id_team is False:
                active_bool = False
        return active_bool

    def set_range_factheirs(
        self, bud_idea_dict: dict[RoadUnit,], range_inheritors: dict[RoadUnit, RoadUnit]
    ):
        for reason_base in self._reasonheirs.keys():
            if range_root_road := range_inheritors.get(reason_base):
                all_ideas = all_ideas_between(
                    bud_idea_dict, range_root_road, reason_base
                )
                self._create_factheir(all_ideas, range_root_road, reason_base)

    def _create_factheir(
        self, all_ideas: list, range_root_road: RoadUnit, reason_base: RoadUnit
    ):
        range_root_factheir = self._factheirs.get(range_root_road)
        old_open = range_root_factheir.fopen
        old_nigh = range_root_factheir.fnigh
        x_rangeunit = ideas_calculated_range(all_ideas, old_open, old_nigh)
        new_factheir_open = x_rangeunit.gogo
        new_factheir_nigh = x_rangeunit.stop
        new_factheir_obj = factheir_shop(reason_base)
        new_factheir_obj.set_attr(reason_base, new_factheir_open, new_factheir_nigh)
        self._set_factheir(new_factheir_obj)

    def _are_all_reasonheir_active_true(self) -> bool:
        x_reasonheirs = self._reasonheirs.values()
        return all(x_reasonheir._status != False for x_reasonheir in x_reasonheirs)

    def clear_reasonheirs_status(self):
        for reason in self._reasonheirs.values():
            reason.clear_status()

    def _coalesce_with_reasonunits(
        self, reasonheirs: dict[RoadUnit, ReasonHeir]
    ) -> dict[RoadUnit, ReasonHeir]:
        new_reasonheirs = deepcopy(reasonheirs)
        new_reasonheirs |= self.reasonunits
        return new_reasonheirs

    def set_reasonheirs(
        self, bud_idea_dict: dict[RoadUnit,], reasonheirs: dict[RoadUnit, ReasonCore]
    ):
        coalesced_reasons = self._coalesce_with_reasonunits(reasonheirs)
        self._reasonheirs = {}
        for old_reasonheir in coalesced_reasons.values():
            old_base = old_reasonheir.base
            old_active_requisite = old_reasonheir.base_idea_active_requisite
            new_reasonheir = reasonheir_shop(old_base, None, old_active_requisite)
            new_reasonheir.inherit_from_reasonheir(old_reasonheir)

            if base_idea := bud_idea_dict.get(old_reasonheir.base):
                new_reasonheir.set_base_idea_active_value(base_idea._active)
            self._reasonheirs[new_reasonheir.base] = new_reasonheir

    def set_idearoot_inherit_reasonheirs(self):
        self._reasonheirs = {}
        for x_reasonunit in self.reasonunits.values():
            new_reasonheir = reasonheir_shop(x_reasonunit.base)
            new_reasonheir.inherit_from_reasonheir(x_reasonunit)
            self._reasonheirs[new_reasonheir.base] = new_reasonheir

    def get_reasonheir(self, base: RoadUnit) -> ReasonHeir:
        return self._reasonheirs.get(base)

    def get_reasonunits_dict(self):
        return {base: reason.get_dict() for base, reason in self.reasonunits.items()}

    def get_kids_dict(self) -> dict[GroupID,]:
        return {c_road: kid.get_dict() for c_road, kid in self._kids.items()}

    def get_awardlinks_dict(self) -> dict[GroupID, dict]:
        x_awardlinks = self.awardlinks.items()
        return {
            x_group_id: awardlink.get_dict() for x_group_id, awardlink in x_awardlinks
        }

    def is_kidless(self) -> bool:
        return self._kids == {}

    def is_math(self) -> bool:
        return self.begin is not None and self.close is not None

    def awardheir_exists(self) -> bool:
        return self._awardheirs != {}

    def get_dict(self) -> dict[str, str]:
        x_dict = {"mass": self.mass}

        if self._label is not None:
            x_dict["_label"] = self._label
        if self._uid is not None:
            x_dict["_uid"] = self._uid
        if self._kids not in [{}, None]:
            x_dict["_kids"] = self.get_kids_dict()
        if self.reasonunits not in [{}, None]:
            x_dict["reasonunits"] = self.get_reasonunits_dict()
        if self.teamunit not in [None, teamunit_shop()]:
            x_dict["teamunit"] = self.get_teamunit_dict()
        if self.healerlink not in [None, healerlink_shop()]:
            x_dict["healerlink"] = self.healerlink.get_dict()
        if self.awardlinks not in [{}, None]:
            x_dict["awardlinks"] = self.get_awardlinks_dict()
        if self._originunit not in [None, originunit_shop()]:
            x_dict["_originunit"] = self.get_originunit_dict()
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

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        if is_sub_road(ref_road=self._parent_road, sub_road=old_road):
            self._parent_road = rebuild_road(self._parent_road, old_road, new_road)

        self.reasonunits == find_replace_road_key_dict(
            dict_x=self.reasonunits, old_road=old_road, new_road=new_road
        )

        self.factunits == find_replace_road_key_dict(
            dict_x=self.factunits, old_road=old_road, new_road=new_road
        )

    def set_teamunit_empty_if_none(self):
        if self.teamunit is None:
            self.teamunit = teamunit_shop()

    def set_teamheir(
        self,
        parent_teamheir: TeamHeir,
        bud_groupboxs: dict[GroupID, GroupBox],
    ):
        self._teamheir = teamheir_shop()
        self._teamheir.set_teamlinks(
            parent_teamheir=parent_teamheir,
            teamunit=self.teamunit,
            bud_groupboxs=bud_groupboxs,
        )

    def get_teamunit_dict(self) -> dict:
        return self.teamunit.get_dict()


def ideaunit_shop(
    _label: RoadNode = None,
    _uid: int = None,  # Calculated field?
    _parent_road: RoadUnit = None,
    _kids: dict = None,
    mass: int = 1,
    awardlinks: dict[GroupID, AwardLink] = None,
    _awardheirs: dict[GroupID, AwardHeir] = None,  # Calculated field
    _awardlines: dict[GroupID, AwardLink] = None,  # Calculated field
    reasonunits: dict[RoadUnit, ReasonUnit] = None,
    _reasonheirs: dict[RoadUnit, ReasonHeir] = None,  # Calculated field
    teamunit: TeamUnit = None,
    _teamheir: TeamHeir = None,  # Calculated field
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
    _root: bool = None,
    _bud_pecun_id: PecunID = None,
    problem_bool: bool = None,
    # Calculated fields
    _level: int = None,
    _fund_ratio: float = None,
    _fund_coin: FundCoin = None,
    _fund_onset: FundNum = None,
    _fund_cease: FundNum = None,
    _task: bool = None,
    _active: bool = None,
    _ancestor_pledge_count: int = None,
    _descendant_pledge_count: int = None,
    _all_acct_cred: bool = None,
    _all_acct_debt: bool = None,
    _is_expanded: bool = True,
    _active_hx: dict[int, bool] = None,
    _road_delimiter: str = None,
    _healerlink_ratio: float = None,
) -> IdeaUnit:
    _bud_pecun_id = root_label() if _bud_pecun_id is None else _bud_pecun_id
    x_healerlink = healerlink_shop() if healerlink is None else healerlink

    x_ideakid = IdeaUnit(
        _label=None,
        _uid=_uid,
        _parent_road=_parent_road,
        _kids=get_empty_dict_if_none(_kids),
        mass=get_positive_int(mass),
        awardlinks=get_empty_dict_if_none(awardlinks),
        _awardheirs=get_empty_dict_if_none(_awardheirs),
        _awardlines=get_empty_dict_if_none(_awardlines),
        reasonunits=get_empty_dict_if_none(reasonunits),
        _reasonheirs=get_empty_dict_if_none(_reasonheirs),
        teamunit=teamunit,
        _teamheir=_teamheir,
        factunits=get_empty_dict_if_none(factunits),
        _factheirs=get_empty_dict_if_none(_factheirs),
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
        _root=get_False_if_None(_root),
        _bud_pecun_id=_bud_pecun_id,
        # Calculated fields
        _level=_level,
        _fund_ratio=_fund_ratio,
        _fund_coin=default_fund_coin_if_none(_fund_coin),
        _fund_onset=_fund_onset,
        _fund_cease=_fund_cease,
        _task=_task,
        _active=_active,
        _ancestor_pledge_count=_ancestor_pledge_count,
        _descendant_pledge_count=_descendant_pledge_count,
        _all_acct_cred=_all_acct_cred,
        _all_acct_debt=_all_acct_debt,
        _is_expanded=_is_expanded,
        _active_hx=get_empty_dict_if_none(_active_hx),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _healerlink_ratio=get_0_if_None(_healerlink_ratio),
    )
    if x_ideakid._root:
        x_ideakid.set_label(_label=_bud_pecun_id)
    else:
        x_ideakid.set_label(_label=_label)
    x_ideakid.set_teamunit_empty_if_none()
    x_ideakid.set_originunit_empty_if_none()
    return x_ideakid


def get_obj_from_idea_dict(x_dict: dict[str, dict], dict_key: str) -> any:
    if dict_key == "reasonunits":
        return (
            reasons_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else None
        )
    elif dict_key == "teamunit":
        return (
            teamunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else teamunit_shop()
        )
    elif dict_key == "healerlink":
        return (
            healerlink_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else healerlink_shop()
        )
    elif dict_key == "_originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else originunit_shop()
        )
    elif dict_key == "factunits":
        return (
            factunits_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else factunits_get_from_dict({})
        )
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
    bud_idea_dict: dict[RoadUnit, IdeaUnit], src_road: RoadUnit, dst_base: RoadUnit
) -> list[IdeaUnit]:
    all_roads = all_roadunits_between(src_road, dst_base)
    return [bud_idea_dict.get(x_road) for x_road in all_roads]


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
