from src.a00_data_toolbox.dict_toolbox import (
    get_empty_dict_if_None,
    get_0_if_None,
    get_1_if_None,
    get_False_if_None,
    get_positive_int,
)
from src.a01_road_logic.road import (
    RoadUnit,
    TagUnit,
    is_sub_road,
    get_default_fisc_tag as root_tag,
    all_roadunits_between,
    create_road as road_create_road,
    default_bridge_if_None,
    replace_bridge,
    FiscTag,
    AcctName,
    GroupLabel,
    RoadUnit,
    rebuild_road,
    find_replace_road_key_dict,
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

from src.a04_reason_logic.reason_team import (
    TeamUnit,
    TeamHeir,
    teamunit_shop,
    teamheir_shop,
    teamunit_get_from_dict,
)
from src.a04_reason_logic.reason_item import (
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
    get_dict_from_factunits,
)
from src.a05_item_logic.healer import (
    HealerLink,
    healerlink_shop,
    healerlink_get_from_dict,
)

from src.a05_item_logic.origin import (
    OriginUnit,
    originunit_get_from_dict,
    originunit_shop,
)
from dataclasses import dataclass
from copy import deepcopy


class InvalidItemException(Exception):
    pass


class ItemGetDescendantsException(Exception):
    pass


class Item_root_TagNotEmptyException(Exception):
    pass


class ranged_fact_item_Exception(Exception):
    pass


@dataclass
class ItemAttrHolder:
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
    reason_base_item_active_requisite: str = None
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
    awardlink_del: GroupLabel = None
    is_expanded: bool = None
    problem_bool: bool = None

    def set_premise_range_attributes_influenced_by_premise_item(
        self,
        premise_open,
        premise_nigh,
        premise_denom,
    ):
        if self.reason_premise is not None:
            if self.reason_premise_open is None:
                self.reason_premise_open = premise_open
            if self.reason_premise_nigh is None:
                self.reason_premise_nigh = premise_nigh
            if self.reason_premise_divisor is None:
                self.reason_premise_divisor = premise_denom


def itemattrholder_shop(
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
    reason_base_item_active_requisite: str = None,
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
    awardlink_del: GroupLabel = None,
    is_expanded: bool = None,
    problem_bool: bool = None,
) -> ItemAttrHolder:
    return ItemAttrHolder(
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
        reason_base_item_active_requisite=reason_base_item_active_requisite,
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
class ItemUnit:
    item_tag: TagUnit = None
    mass: int = None
    parent_road: RoadUnit = None
    root: bool = None
    _kids: dict[RoadUnit,] = None
    fisc_tag: FiscTag = None
    _uid: int = None  # Calculated field?
    awardlinks: dict[GroupLabel, AwardLink] = None
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
    _factheirs: dict[RoadUnit, FactHeir] = None
    _fund_ratio: float = None
    fund_coin: FundCoin = None
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
        facts_dict = get_empty_dict_if_None(facts)
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
            raise ranged_fact_item_Exception(
                f"Cannot have fact for range inheritor '{self.get_road()}'. A ranged fact item must have _begin, _close attributes"
            )
        x_factheir = factheir_shop(x_fact.base, x_fact.pick, x_fact.fopen, x_fact.fnigh)
        self.delete_factunit_if_past(x_factheir)
        x_factheir = self.apply_factunit_moldations(x_factheir)
        self._factheirs[x_factheir.base] = x_factheir

    def apply_factunit_moldations(self, factheir: FactHeir) -> FactHeir:
        for factunit in self.factunits.values():
            if factunit.base == factheir.base:
                factheir.mold(factunit)
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

    def get_factunits_dict(self) -> dict[RoadUnit, str]:
        return get_dict_from_factunits(self.factunits)

    def set_factunit_to_complete(self, base_factunit: FactUnit):
        # if a item is considered a task then a factheir.fopen attribute can be increased to
        # a number <= factheir.fnigh so the item no longer is a task. This method finds
        # the minimal factheir.fopen to modify item._task is False. item_core._factheir cannot be straight up manipulated
        # so it is mandatory that item._factunit is different.
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
    ) -> dict[TagUnit,]:
        if x_gogo is None and x_stop is None:
            x_gogo = self.gogo_want
            x_gogo = self.stop_want
        elif x_gogo is not None and x_stop is None:
            x_stop = x_gogo

        if x_gogo is None and x_stop is None:
            return self._kids.values()

        x_dict = {}
        for x_item in self._kids.values():
            x_gogo_in_range = x_gogo >= x_item._gogo_calc and x_gogo < x_item._stop_calc
            x_stop_in_range = x_stop > x_item._gogo_calc and x_stop < x_item._stop_calc
            both_in_range = x_gogo <= x_item._gogo_calc and x_stop >= x_item._stop_calc

            if x_gogo_in_range or x_stop_in_range or both_in_range:
                x_dict[x_item.item_tag] = x_item
        return x_dict

    def get_obj_key(self) -> TagUnit:
        return self.item_tag

    def get_road(self) -> RoadUnit:
        if self.parent_road in (None, ""):
            return road_create_road(self.item_tag, bridge=self.bridge)
        else:
            return road_create_road(self.parent_road, self.item_tag, bridge=self.bridge)

    def clear_descendant_pledge_count(self):
        self._descendant_pledge_count = None

    def set_descendant_pledge_count_zero_if_None(self):
        if self._descendant_pledge_count is None:
            self._descendant_pledge_count = 0

    def add_to_descendant_pledge_count(self, x_int: int):
        self.set_descendant_pledge_count_zero_if_None()
        self._descendant_pledge_count += x_int

    def get_descendant_roads_from_kids(self) -> dict[RoadUnit, int]:
        descendant_roads = {}
        to_evaluate_items = list(self._kids.values())
        count_x = 0
        max_count = 1000
        while to_evaluate_items != [] and count_x < max_count:
            x_item = to_evaluate_items.pop()
            descendant_roads[x_item.get_road()] = -1
            to_evaluate_items.extend(x_item._kids.values())
            count_x += 1

        if count_x == max_count:
            raise ItemGetDescendantsException(
                f"Item '{self.get_road()}' either has an infinite loop or more than {max_count} descendants."
            )

        return descendant_roads

    def clear_all_acct_cred_debt(self):
        self._all_acct_cred = None
        self._all_acct_debt = None

    def set_level(self, parent_level):
        self._level = parent_level + 1

    def set_parent_road(self, parent_road):
        self.parent_road = parent_road

    def inherit_awardheirs(self, parent_awardheirs: dict[GroupLabel, AwardHeir] = None):
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

    def set_awardlines(self, child_awardlines: dict[GroupLabel, AwardLine] = None):
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

    def set_item_tag(self, item_tag: str):
        if (
            self.root
            and item_tag is not None
            and item_tag != self.fisc_tag
            and self.fisc_tag is not None
        ):
            raise Item_root_TagNotEmptyException(
                f"Cannot set itemroot to string different than '{self.fisc_tag}'"
            )
        elif self.root and self.fisc_tag is None:
            self.item_tag = root_tag()
        # elif item_tag is not None:
        else:
            self.item_tag = item_tag

    def set_bridge(self, new_bridge: str):
        old_bridge = deepcopy(self.bridge)
        if old_bridge is None:
            old_bridge = default_bridge_if_None()
        self.bridge = default_bridge_if_None(new_bridge)
        if old_bridge != self.bridge:
            self._find_replace_bridge(old_bridge)

    def _find_replace_bridge(self, old_bridge):
        self.parent_road = replace_bridge(self.parent_road, old_bridge, self.bridge)

        new_reasonunits = {}
        for reasonunit_road, reasonunit_obj in self.reasonunits.items():
            new_reasonunit_road = replace_bridge(
                road=reasonunit_road,
                old_bridge=old_bridge,
                new_bridge=self.bridge,
            )
            reasonunit_obj.set_bridge(self.bridge)
            new_reasonunits[new_reasonunit_road] = reasonunit_obj
        self.reasonunits = new_reasonunits

        new_factunits = {}
        for factunit_road, factunit_obj in self.factunits.items():
            new_base_road = replace_bridge(
                road=factunit_road,
                old_bridge=old_bridge,
                new_bridge=self.bridge,
            )
            factunit_obj.base = new_base_road
            new_pick_road = replace_bridge(
                road=factunit_obj.pick,
                old_bridge=old_bridge,
                new_bridge=self.bridge,
            )
            factunit_obj.set_attr(pick=new_pick_road)
            new_factunits[new_base_road] = factunit_obj
        self.factunits = new_factunits

    def set_originunit_empty_if_None(self):
        if self._originunit is None:
            self._originunit = originunit_shop()

    def get_originunit_dict(self) -> dict[str, str]:
        return self._originunit.get_dict()

    def _set_attrs_to_itemunit(self, item_attr: ItemAttrHolder):
        if item_attr.mass is not None:
            self.mass = item_attr.mass
        if item_attr.uid is not None:
            self._uid = item_attr.uid
        if item_attr.reason is not None:
            self.set_reasonunit(reason=item_attr.reason)
        if item_attr.reason_base is not None and item_attr.reason_premise is not None:
            self.set_reason_premise(
                base=item_attr.reason_base,
                premise=item_attr.reason_premise,
                open=item_attr.reason_premise_open,
                nigh=item_attr.reason_premise_nigh,
                divisor=item_attr.reason_premise_divisor,
            )
        if (
            item_attr.reason_base is not None
            and item_attr.reason_base_item_active_requisite is not None
        ):
            self.set_reason_base_item_active_requisite(
                base=item_attr.reason_base,
                base_item_active_requisite=item_attr.reason_base_item_active_requisite,
            )
        if item_attr.teamunit is not None:
            self.teamunit = item_attr.teamunit
        if item_attr.healerlink is not None:
            self.healerlink = item_attr.healerlink
        if item_attr.begin is not None:
            self.begin = item_attr.begin
        if item_attr.close is not None:
            self.close = item_attr.close
        if item_attr.gogo_want is not None:
            self.gogo_want = item_attr.gogo_want
        if item_attr.stop_want is not None:
            self.stop_want = item_attr.stop_want
        if item_attr.addin is not None:
            self.addin = item_attr.addin
        if item_attr.numor is not None:
            self.numor = item_attr.numor
        if item_attr.denom is not None:
            self.denom = item_attr.denom
        if item_attr.morph is not None:
            self.morph = item_attr.morph
        if item_attr.descendant_pledge_count is not None:
            self._descendant_pledge_count = item_attr.descendant_pledge_count
        if item_attr.all_acct_cred is not None:
            self._all_acct_cred = item_attr.all_acct_cred
        if item_attr.all_acct_debt is not None:
            self._all_acct_debt = item_attr.all_acct_debt
        if item_attr.awardlink is not None:
            self.set_awardlink(awardlink=item_attr.awardlink)
        if item_attr.awardlink_del is not None:
            self.del_awardlink(awardee_title=item_attr.awardlink_del)
        if item_attr.is_expanded is not None:
            self._is_expanded = item_attr.is_expanded
        if item_attr.pledge is not None:
            self.pledge = item_attr.pledge
        if item_attr.factunit is not None:
            self.set_factunit(item_attr.factunit)
        if item_attr.problem_bool is not None:
            self.problem_bool = item_attr.problem_bool

        self._del_reasonunit_all_cases(
            base=item_attr.reason_del_premise_base,
            premise=item_attr.reason_del_premise_need,
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
        r_item_numor = get_1_if_None(self.numor)
        r_item_denom = get_1_if_None(self.denom)
        r_item_addin = get_0_if_None(self.addin)

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
            self._gogo_calc = self._gogo_calc + r_item_addin
            self._stop_calc = self._stop_calc + r_item_addin
            self._gogo_calc = (self._gogo_calc * r_item_numor) / r_item_denom
            self._stop_calc = (self._stop_calc * r_item_numor) / r_item_denom
        self._range_evaluated = True

    def _del_reasonunit_all_cases(self, base: RoadUnit, premise: RoadUnit):
        if base is not None and premise is not None:
            self.del_reasonunit_premise(base=base, premise=premise)
            if len(self.reasonunits[base].premises) == 0:
                self.del_reasonunit_base(base=base)

    def set_reason_base_item_active_requisite(
        self, base: RoadUnit, base_item_active_requisite: str
    ):
        x_reasonunit = self._get_or_create_reasonunit(base=base)
        if base_item_active_requisite is False:
            x_reasonunit.base_item_active_requisite = False
        elif base_item_active_requisite == "Set to Ignore":
            x_reasonunit.base_item_active_requisite = None
        elif base_item_active_requisite:
            x_reasonunit.base_item_active_requisite = True

    def _get_or_create_reasonunit(self, base: RoadUnit) -> ReasonUnit:
        x_reasonunit = None
        try:
            x_reasonunit = self.reasonunits[base]
        except Exception:
            x_reasonunit = reasonunit_shop(base, bridge=self.bridge)
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
            raise InvalidItemException(f"No ReasonUnit at '{base}'") from e

    def del_reasonunit_premise(self, base: RoadUnit, premise: RoadUnit):
        reason_unit = self.reasonunits[base]
        reason_unit.del_premise(premise=premise)

    def add_kid(self, item_kid):
        self._kids[item_kid.item_tag] = item_kid
        self._kids = dict(sorted(self._kids.items()))

    def get_kid(self, item_kid_item_tag: TagUnit, if_missing_create=False):
        if if_missing_create is False:
            return self._kids.get(item_kid_item_tag)
        try:
            return self._kids[item_kid_item_tag]
        except Exception:
            KeyError
            self.add_kid(itemunit_shop(item_kid_item_tag))
            return_item = self._kids.get(item_kid_item_tag)
        return return_item

    def del_kid(self, item_kid_item_tag: TagUnit):
        self._kids.pop(item_kid_item_tag)

    def clear_kids(self):
        self._kids = {}

    def get_kids_mass_sum(self) -> float:
        return sum(x_kid.mass for x_kid in self._kids.values())

    def set_awardlink(self, awardlink: AwardLink):
        self.awardlinks[awardlink.awardee_title] = awardlink

    def get_awardlink(self, awardee_title: GroupLabel) -> AwardLink:
        return self.awardlinks.get(awardee_title)

    def del_awardlink(self, awardee_title: GroupLabel):
        try:
            self.awardlinks.pop(awardee_title)
        except KeyError as e:
            raise (f"Cannot delete awardlink '{awardee_title}'.") from e

    def awardlink_exists(self, x_awardee_title: GroupLabel) -> bool:
        return self.awardlinks.get(x_awardee_title) != None

    def set_reasonunit(self, reason: ReasonUnit):
        reason.bridge = self.bridge
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
        bud_groupunits: dict[GroupLabel, GroupUnit] = None,
        bud_owner_name: AcctName = None,
    ):
        prev_to_now_active = deepcopy(self._active)
        self._active = self._create_active_bool(bud_groupunits, bud_owner_name)
        self._set_item_task()
        self.record_active_hx(tree_traverse_count, prev_to_now_active, self._active)

    def _set_item_task(self):
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
            and self._teamheir._teamlinks != {}
        ):
            self._teamheir.set_owner_name_team(bud_groupunits, bud_owner_name)
            if self._teamheir._owner_name_team is False:
                active_bool = False
        return active_bool

    def set_range_factheirs(
        self, bud_item_dict: dict[RoadUnit,], range_inheritors: dict[RoadUnit, RoadUnit]
    ):
        for reason_base in self._reasonheirs.keys():
            if range_root_road := range_inheritors.get(reason_base):
                all_items = all_items_between(
                    bud_item_dict, range_root_road, reason_base
                )
                self._create_factheir(all_items, range_root_road, reason_base)

    def _create_factheir(
        self, all_items: list, range_root_road: RoadUnit, reason_base: RoadUnit
    ):
        range_root_factheir = self._factheirs.get(range_root_road)
        old_open = range_root_factheir.fopen
        old_nigh = range_root_factheir.fnigh
        x_rangeunit = items_calculated_range(all_items, old_open, old_nigh)
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
        self, bud_item_dict: dict[RoadUnit,], reasonheirs: dict[RoadUnit, ReasonCore]
    ):
        coalesced_reasons = self._coalesce_with_reasonunits(reasonheirs)
        self._reasonheirs = {}
        for old_reasonheir in coalesced_reasons.values():
            old_base = old_reasonheir.base
            old_active_requisite = old_reasonheir.base_item_active_requisite
            new_reasonheir = reasonheir_shop(old_base, None, old_active_requisite)
            new_reasonheir.inherit_from_reasonheir(old_reasonheir)

            if base_item := bud_item_dict.get(old_reasonheir.base):
                new_reasonheir.set_base_item_active_value(base_item._active)
            self._reasonheirs[new_reasonheir.base] = new_reasonheir

    def set_itemroot_inherit_reasonheirs(self):
        self._reasonheirs = {}
        for x_reasonunit in self.reasonunits.values():
            new_reasonheir = reasonheir_shop(x_reasonunit.base)
            new_reasonheir.inherit_from_reasonheir(x_reasonunit)
            self._reasonheirs[new_reasonheir.base] = new_reasonheir

    def get_reasonheir(self, base: RoadUnit) -> ReasonHeir:
        return self._reasonheirs.get(base)

    def get_reasonunits_dict(self):
        return {base: reason.get_dict() for base, reason in self.reasonunits.items()}

    def get_kids_dict(self) -> dict[GroupLabel,]:
        return {c_road: kid.get_dict() for c_road, kid in self._kids.items()}

    def get_awardlinks_dict(self) -> dict[GroupLabel, dict]:
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

        if self.item_tag is not None:
            x_dict["item_tag"] = self.item_tag
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

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        if is_sub_road(ref_road=self.parent_road, sub_road=old_road):
            self.parent_road = rebuild_road(self.parent_road, old_road, new_road)

        self.reasonunits == find_replace_road_key_dict(
            dict_x=self.reasonunits, old_road=old_road, new_road=new_road
        )

        self.factunits == find_replace_road_key_dict(
            dict_x=self.factunits, old_road=old_road, new_road=new_road
        )

    def set_teamunit_empty_if_None(self):
        if self.teamunit is None:
            self.teamunit = teamunit_shop()

    def set_teamheir(
        self,
        parent_teamheir: TeamHeir,
        bud_groupunits: dict[GroupLabel, GroupUnit],
    ):
        self._teamheir = teamheir_shop()
        self._teamheir.set_teamlinks(
            parent_teamheir=parent_teamheir,
            teamunit=self.teamunit,
            bud_groupunits=bud_groupunits,
        )

    def get_teamunit_dict(self) -> dict:
        return self.teamunit.get_dict()


def itemunit_shop(
    item_tag: TagUnit = None,
    _uid: int = None,  # Calculated field?
    parent_road: RoadUnit = None,
    _kids: dict = None,
    mass: int = 1,
    awardlinks: dict[GroupLabel, AwardLink] = None,
    _awardheirs: dict[GroupLabel, AwardHeir] = None,  # Calculated field
    _awardlines: dict[GroupLabel, AwardLink] = None,  # Calculated field
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
) -> ItemUnit:
    fisc_tag = root_tag() if fisc_tag is None else fisc_tag
    x_healerlink = healerlink_shop() if healerlink is None else healerlink

    x_itemkid = ItemUnit(
        item_tag=None,
        _uid=_uid,
        parent_road=parent_road,
        _kids=get_empty_dict_if_None(_kids),
        mass=get_positive_int(mass),
        awardlinks=get_empty_dict_if_None(awardlinks),
        _awardheirs=get_empty_dict_if_None(_awardheirs),
        _awardlines=get_empty_dict_if_None(_awardlines),
        reasonunits=get_empty_dict_if_None(reasonunits),
        _reasonheirs=get_empty_dict_if_None(_reasonheirs),
        teamunit=teamunit,
        _teamheir=_teamheir,
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
    if x_itemkid.root:
        x_itemkid.set_item_tag(item_tag=fisc_tag)
    else:
        x_itemkid.set_item_tag(item_tag=item_tag)
    x_itemkid.set_teamunit_empty_if_None()
    x_itemkid.set_originunit_empty_if_None()
    return x_itemkid


def get_obj_from_item_dict(x_dict: dict[str, dict], dict_key: str) -> any:
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


def all_items_between(
    bud_item_dict: dict[RoadUnit, ItemUnit], src_road: RoadUnit, dst_base: RoadUnit
) -> list[ItemUnit]:
    all_roads = all_roadunits_between(src_road, dst_base)
    return [bud_item_dict.get(x_road) for x_road in all_roads]


def items_calculated_range(
    item_list: list[ItemUnit], x_gogo: float, x_stop: float
) -> RangeUnit:
    for x_item in item_list:
        if x_item.addin:
            x_gogo += get_0_if_None(x_item.addin)
            x_stop += get_0_if_None(x_item.addin)
        if (x_item.numor or x_item.denom) and not x_item.morph:
            x_gogo *= get_1_if_None(x_item.numor) / get_1_if_None(x_item.denom)
            x_stop *= get_1_if_None(x_item.numor) / get_1_if_None(x_item.denom)
        if x_item.denom and x_item.morph:
            x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, x_item.denom)
            x_gogo = x_rangeunit.gogo
            x_stop = x_rangeunit.stop
    return RangeUnit(x_gogo, x_stop)
