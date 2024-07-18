from src._instrument.python import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_False_if_None,
    get_positive_int,
)
from src._road.finance import FundCoin, FundNum
from src._road.road import (
    RoadUnit,
    RoadNode,
    is_sub_road,
    get_default_real_id_roadnode as root_label,
    create_road as road_create_road,
    default_road_delimiter_if_none,
    replace_road_delimiter,
    RealID,
    CharID,
    LobbyID,
    RoadUnit,
    rebuild_road,
    find_replace_road_key_dict,
)
from src._world.healer import HealerHold, healerhold_shop, healerhold_get_from_dict
from src._world.reason_doer import (
    DoerUnit,
    DoerHeir,
    doerunit_shop,
    doerheir_shop,
    doerunit_get_from_dict,
)
from src._world.reason_idea import (
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
from src._world.lobby import (
    AwardHeir,
    AwardLink,
    awardlinks_get_from_dict,
    AwardLine,
    awardline_shop,
    awardheir_shop,
    LobbyBox,
)
from src._world.origin import OriginUnit, originunit_get_from_dict
from src._world.origin import originunit_shop
from dataclasses import dataclass
from copy import deepcopy


class InvalidIdeaException(Exception):
    pass


class IdeaGetDescendantsException(Exception):
    pass


@dataclass
class IdeaAttrFilter:
    weight: int = None
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
    doerunit: DoerUnit = None
    healerhold: HealerHold = None
    begin: float = None
    close: float = None
    addin: float = None
    numor: float = None
    denom: float = None
    reest: bool = None
    numeric_road: RoadUnit = None
    range_source_road: float = None
    pledge: bool = None
    factunit: FactUnit = None
    descendant_pledge_count: int = None
    all_char_cred: bool = None
    all_char_debt: bool = None
    awardlink: AwardLink = None
    awardlink_del: LobbyID = None
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
        # premise_reest,
    ):
        if self.reason_premise != None:
            if self.reason_premise_open is None:
                self.reason_premise_open = premise_open
            if self.reason_premise_nigh is None:
                self.reason_premise_nigh = premise_nigh
            # if self.reason_premise_numor is None:
            #     numor_x = premise_numor
            if self.reason_premise_divisor is None:
                self.reason_premise_divisor = premise_denom
            # if self.reason_premise_reest is None:
            #     self.reason_premise_reest = premise_reest

    def has_numeric_attrs(self):
        return (
            self.begin != None
            or self.close != None
            or self.numor != None
            or self.numeric_road != None
            or self.addin != None
        )

    def has_ratio_attrs(self):
        return (
            self.denom != None or self.numor != None or self.reest or self.addin != None
        )

    def set_ratio_attr_defaults_if_none(self):
        if self.addin is None:
            self.addin = 0
        if self.denom is None:
            self.denom = 1
        if self.numor is None:
            self.numor = 1
        if self.reest is None:
            self.reest = False

    def has_reason_premise(self):
        return self.reason_premise != None


def ideaattrfilter_shop(
    weight: int = None,
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
    doerunit: DoerUnit = None,
    healerhold: HealerHold = None,
    begin: float = None,
    close: float = None,
    addin: float = None,
    numor: float = None,
    denom: float = None,
    reest: bool = None,
    numeric_road: RoadUnit = None,
    range_source_road: float = None,
    pledge: bool = None,
    factunit: FactUnit = None,
    descendant_pledge_count: int = None,
    all_char_cred: bool = None,
    all_char_debt: bool = None,
    awardlink: AwardLink = None,
    awardlink_del: LobbyID = None,
    is_expanded: bool = None,
    problem_bool: bool = None,
) -> IdeaAttrFilter:
    x_ideaattrfilter = IdeaAttrFilter(
        weight=weight,
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
        doerunit=doerunit,
        healerhold=healerhold,
        begin=begin,
        close=close,
        addin=addin,
        numor=numor,
        denom=denom,
        reest=reest,
        numeric_road=numeric_road,
        range_source_road=range_source_road,
        pledge=pledge,
        factunit=factunit,
        descendant_pledge_count=descendant_pledge_count,
        all_char_cred=all_char_cred,
        all_char_debt=all_char_debt,
        awardlink=awardlink,
        awardlink_del=awardlink_del,
        is_expanded=is_expanded,
        problem_bool=problem_bool,
    )
    if x_ideaattrfilter.has_ratio_attrs():
        x_ideaattrfilter.set_ratio_attr_defaults_if_none()
    return x_ideaattrfilter


@dataclass
class IdeaUnit:
    _label: RoadNode = None
    _weight: int = None
    _parent_road: RoadUnit = None
    _root: bool = None
    _kids: dict[RoadUnit,] = None
    _world_real_id: RealID = None
    _uid: int = None  # Calculated field?
    _awardlinks: dict[LobbyID, AwardLink] = None
    _awardheirs: dict[LobbyID, AwardHeir] = None  # Calculated field
    _awardlines: dict[LobbyID, AwardLine] = None  # Calculated field
    _reasonunits: dict[RoadUnit, ReasonUnit] = None
    _reasonheirs: dict[RoadUnit, ReasonHeir] = None  # Calculated field
    _doerunit: DoerUnit = None
    _doerheir: DoerHeir = None  # Calculated field
    _factunits: dict[RoadUnit, FactUnit] = None
    _factheirs: dict[RoadUnit, FactHeir] = None  # Calculated field
    _healerhold: HealerHold = None
    _begin: float = None
    _close: float = None
    _addin: float = None
    _denom: int = None
    _numor: int = None
    _reest: bool = None
    _range_source_road: RoadUnit = None
    _numeric_road: RoadUnit = None
    pledge: bool = None
    _originunit: OriginUnit = None
    _problem_bool: bool = None
    # Calculated fields
    _level: int = None
    _fund_ratio: float = None
    _fund_coin: FundCoin = None
    _fund_onset: FundNum = None
    _fund_cease: FundNum = None
    _task: bool = None
    _active: bool = None
    _ancestor_pledge_count: int = None
    _descendant_pledge_count: int = None
    _all_char_cred: bool = None
    _all_char_debt: bool = None
    _is_expanded: bool = None
    _active_hx: dict[int, bool] = None
    _road_delimiter: str = None
    _healerhold_ratio: float = None

    def is_agenda_item(self, necessary_base: RoadUnit = None) -> bool:
        base_reasonunit_exists = self.base_reasonunit_exists(necessary_base)
        return self.pledge and self._active and base_reasonunit_exists

    def base_reasonunit_exists(self, necessary_base: RoadUnit = None) -> bool:
        return necessary_base is None or any(
            reason.base == necessary_base for reason in self._reasonunits.values()
        )

    def record_active_hx(
        self,
        tree_traverse_count: int,
        prev_active: bool,
        now_active: bool,
    ):
        if tree_traverse_count == 0:
            self._active_hx = {0: now_active}
        elif prev_active != now_active:
            self._active_hx[tree_traverse_count] = now_active

    def set_factheirs(self, facts: dict[RoadUnit, FactCore]):
        facts = get_empty_dict_if_none(x_dict=facts)
        self._factheirs = {}
        for h in facts.values():
            x_fact = factheir_shop(base=h.base, pick=h.pick, open=h.open, nigh=h.nigh)
            self.delete_factunit_if_past(factheir=x_fact)
            x_fact = self.apply_factunit_transformations(factheir=x_fact)
            self._factheirs[x_fact.base] = x_fact

    def apply_factunit_transformations(self, factheir: FactHeir) -> FactHeir:
        for factunit in self._factunits.values():
            if factunit.base == factheir.base:
                factheir.transform(factunit=factunit)
        return factheir

    def delete_factunit_if_past(self, factheir: FactHeir):
        delete_factunit = False
        for factunit in self._factunits.values():
            if (
                factunit.base == factheir.base
                and factunit.nigh != None
                and factheir.open != None
            ) and factunit.nigh < factheir.open:
                delete_factunit = True

        if delete_factunit:
            del self._factunits[factunit.base]

    def set_factunit(self, factunit: FactUnit):
        self._factunits[factunit.base] = factunit

    def get_factunits_dict(self) -> dict[RoadUnit, FactUnit]:
        return {hc.base: hc.get_dict() for hc in self._factunits.values()}

    def set_factunit_to_complete(self, base_factunit: FactUnit):
        # if a idea is considered a task then a factheir.open attribute can be increased to
        # a number <= factheir.nigh so the idea no longer is a task. This method finds
        # the minimal factheir.open to modify idea._task is False. idea_core._factheir cannot be straight up manipulated
        # so it is mandatory that idea._factunit is different.
        # self.set_factunits(base=fact, fact=base, open=premise_nigh, nigh=fact_nigh)
        self._factunits[base_factunit.base] = factunit_shop(
            base=base_factunit.base,
            pick=base_factunit.base,
            open=base_factunit.nigh,
            nigh=base_factunit.nigh,
        )

    def del_factunit(self, base: RoadUnit):
        self._factunits.pop(base)

    def _apply_any_range_source_road_connections(
        self,
        lemmas_dict: dict[RoadUnit, FactUnit],
        missing_facts: list[FactUnit],
    ):
        for active_fact in self._factunits.values():
            for lemma_fact in lemmas_dict.values():
                if lemma_fact.base == active_fact.base:
                    self.set_factunit(lemma_fact)

        for missing_fact in missing_facts:
            for lemma_fact in lemmas_dict.values():
                if lemma_fact.base == missing_fact:
                    self.set_factunit(lemma_fact)

    def set_fund_attr(
        self,
        x_fund_onset: FundNum,
        x_fund_cease: FundNum,
        total_fund_pool: FundNum,
    ):
        self._fund_onset = x_fund_onset
        self._fund_cease = x_fund_cease
        self._fund_ratio = (self._fund_cease - self._fund_onset) / total_fund_pool
        self.set_awardheirs_fund_give_fund_take()

    def get_fund_share(self) -> float:
        if self._fund_onset is None or self._fund_cease is None:
            return 0
        else:
            return self._fund_cease - self._fund_onset

    def get_kids_in_range(self, begin: float, close: float) -> list:
        return [
            x_idea
            for x_idea in self._kids.values()
            if (
                (begin >= x_idea._begin and begin < x_idea._close)
                or (close > x_idea._begin and close < x_idea._close)
                or (begin <= x_idea._begin and close >= x_idea._close)
            )
        ]

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

    def clear_all_char_cred_debt(self):
        self._all_char_cred = None
        self._all_char_debt = None

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

    def inherit_awardheirs(self, parent_awardheirs: dict[LobbyID, AwardHeir] = None):
        if parent_awardheirs is None:
            parent_awardheirs = {}

        self._awardheirs = {}
        for ib in parent_awardheirs.values():
            awardheir = awardheir_shop(
                lobby_id=ib.lobby_id,
                give_weight=ib.give_weight,
                take_weight=ib.take_weight,
            )
            self._awardheirs[awardheir.lobby_id] = awardheir

        for ib in self._awardlinks.values():
            awardheir = awardheir_shop(
                lobby_id=ib.lobby_id,
                give_weight=ib.give_weight,
                take_weight=ib.take_weight,
            )
            self._awardheirs[awardheir.lobby_id] = awardheir

    def set_kidless_awardlines(self):
        # get awardlines from self
        for bh in self._awardheirs.values():
            x_awardline = awardline_shop(
                lobby_id=bh.lobby_id,
                _fund_give=bh._fund_give,
                _fund_take=bh._fund_take,
            )
            self._awardlines[x_awardline.lobby_id] = x_awardline

    def set_awardlines(self, child_awardlines: dict[LobbyID, AwardLine] = None):
        if child_awardlines is None:
            child_awardlines = {}

        # get awardlines from child
        for bl in child_awardlines.values():
            if self._awardlines.get(bl.lobby_id) is None:
                self._awardlines[bl.lobby_id] = awardline_shop(
                    lobby_id=bl.lobby_id,
                    _fund_give=0,
                    _fund_take=0,
                )

            self._awardlines[bl.lobby_id].add_fund_give_take(
                fund_give=bl._fund_give, fund_take=bl._fund_take
            )

    def get_awardheirs_give_weight_sum(self) -> float:
        return sum(awardlink.give_weight for awardlink in self._awardheirs.values())

    def get_awardheirs_take_weight_sum(self) -> float:
        return sum(awardlink.take_weight for awardlink in self._awardheirs.values())

    def set_awardheirs_fund_give_fund_take(self):
        awardheirs_give_weight_sum = self.get_awardheirs_give_weight_sum()
        awardheirs_take_weight_sum = self.get_awardheirs_take_weight_sum()
        for awardheir_x in self._awardheirs.values():
            awardheir_x.set_fund_give_take(
                idea_fund_share=self.get_fund_share(),
                awardheirs_give_weight_sum=awardheirs_give_weight_sum,
                awardheirs_take_weight_sum=awardheirs_take_weight_sum,
            )

    def clear_awardlines(self):
        self._awardlines = {}

    def set_idea_label(self, _label: str):
        if (
            self._root
            and _label != None
            and _label != self._world_real_id
            and self._world_real_id != None
        ):
            raise Idea_root_LabelNotEmptyException(
                f"Cannot set idearoot to string different than '{self._world_real_id}'"
            )
        elif self._root and self._world_real_id is None:
            self._label = root_label()
        # elif _label != None:
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
            road=self._parent_road,
            old_delimiter=old_delimiter,
            new_delimiter=self._road_delimiter,
        )
        if self._numeric_road != None:
            self._numeric_road = replace_road_delimiter(
                road=self._numeric_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
        if self._range_source_road != None:
            self._range_source_road = replace_road_delimiter(
                road=self._range_source_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )

        new_reasonunits = {}
        for reasonunit_road, reasonunit_obj in self._reasonunits.items():
            new_reasonunit_road = replace_road_delimiter(
                road=reasonunit_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            reasonunit_obj.set_delimiter(self._road_delimiter)
            new_reasonunits[new_reasonunit_road] = reasonunit_obj
        self._reasonunits = new_reasonunits

        new_factunits = {}
        for factunit_road, factunit_obj in self._factunits.items():
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
        self._factunits = new_factunits

    def set_originunit_empty_if_none(self):
        if self._originunit is None:
            self._originunit = originunit_shop()

    def get_originunit_dict(self) -> dict[str, str]:
        return self._originunit.get_dict()

    def _set_idea_attr(self, idea_attr: IdeaAttrFilter):
        if idea_attr.weight != None:
            self._weight = idea_attr.weight
        if idea_attr.uid != None:
            self._uid = idea_attr.uid
        if idea_attr.reason != None:
            self.set_reasonunit(reason=idea_attr.reason)
        if idea_attr.reason_base != None and idea_attr.reason_premise != None:
            self.set_reason_premise(
                base=idea_attr.reason_base,
                premise=idea_attr.reason_premise,
                open=idea_attr.reason_premise_open,
                nigh=idea_attr.reason_premise_nigh,
                divisor=idea_attr.reason_premise_divisor,
            )
        if (
            idea_attr.reason_base != None
            and idea_attr.reason_base_idea_active_requisite != None
        ):
            self.set_reason_base_idea_active_requisite(
                base=idea_attr.reason_base,
                base_idea_active_requisite=idea_attr.reason_base_idea_active_requisite,
            )
        if idea_attr.doerunit != None:
            self._doerunit = idea_attr.doerunit
        if idea_attr.healerhold != None:
            self._healerhold = idea_attr.healerhold
        if idea_attr.begin != None:
            self._begin = idea_attr.begin
        if idea_attr.close != None:
            self._close = idea_attr.close
        if idea_attr.addin != None:
            self._addin = idea_attr.addin
        if idea_attr.numor != None:
            self._numor = idea_attr.numor
        if idea_attr.denom != None:
            self._denom = idea_attr.denom
        if idea_attr.reest != None:
            self._reest = idea_attr.reest
        if idea_attr.numeric_road != None:
            self._numeric_road = idea_attr.numeric_road
        if idea_attr.range_source_road != None:
            self._range_source_road = idea_attr.range_source_road
        if idea_attr.descendant_pledge_count != None:
            self._descendant_pledge_count = idea_attr.descendant_pledge_count
        if idea_attr.all_char_cred != None:
            self._all_char_cred = idea_attr.all_char_cred
        if idea_attr.all_char_debt != None:
            self._all_char_debt = idea_attr.all_char_debt
        if idea_attr.awardlink != None:
            self.set_awardlink(awardlink=idea_attr.awardlink)
        if idea_attr.awardlink_del != None:
            self.del_awardlink(lobby_id=idea_attr.awardlink_del)
        if idea_attr.is_expanded != None:
            self._is_expanded = idea_attr.is_expanded
        if idea_attr.pledge != None:
            self.pledge = idea_attr.pledge
        if idea_attr.factunit != None:
            self.set_factunit(idea_attr.factunit)
        if idea_attr.problem_bool != None:
            self._problem_bool = idea_attr.problem_bool

        self._del_reasonunit_all_cases(
            base=idea_attr.reason_del_premise_base,
            premise=idea_attr.reason_del_premise_need,
        )
        self._set_addin_to_zero_if_any_transformations_exist()

    def _set_addin_to_zero_if_any_transformations_exist(self):
        if (
            self._begin != None
            and self._close != None
            and (self._numor != None or self._denom != None)
            and self._addin is None
        ):
            self._addin = 0

    def _del_reasonunit_all_cases(self, base: RoadUnit, premise: RoadUnit):
        if base != None and premise != None:
            self.del_reasonunit_premise(base=base, premise=premise)
            if len(self._reasonunits[base].premises) == 0:
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
            x_reasonunit = self._reasonunits[base]
        except Exception:
            x_reasonunit = reasonunit_shop(base, delimiter=self._road_delimiter)
            self._reasonunits[base] = x_reasonunit
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
            self._reasonunits.pop(base)
        except KeyError as e:
            raise InvalidIdeaException(f"No ReasonUnit at '{base}'") from e

    def del_reasonunit_premise(self, base: RoadUnit, premise: RoadUnit):
        reason_unit = self._reasonunits[base]
        reason_unit.del_premise(premise=premise)

    def add_kid(self, idea_kid):
        if idea_kid._numor != None:
            # if idea_kid._denom != None:
            # if idea_kid._reest != None:
            if self._begin is None or self._close is None:
                raise InvalidIdeaException(
                    f"Idea {idea_kid.get_road()} cannot have numor,denom,reest if parent does not have begin/close range"
                )

            idea_kid._begin = self._begin * idea_kid._numor / idea_kid._denom
            idea_kid._close = self._close * idea_kid._numor / idea_kid._denom

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

    def set_awardlink(self, awardlink: AwardLink):
        self._awardlinks[awardlink.lobby_id] = awardlink

    def del_awardlink(self, lobby_id: LobbyID):
        try:
            self._awardlinks.pop(lobby_id)
        except KeyError as e:
            raise (f"Cannot delete awardlink '{lobby_id}'.") from e

    def set_reasonunit(self, reason: ReasonUnit):
        reason.delimiter = self._road_delimiter
        self._reasonunits[reason.base] = reason

    def get_reasonunit(self, base: RoadUnit) -> ReasonUnit:
        return self._reasonunits.get(base)

    def set_reasonheirs_status(self):
        self.clear_reasonheirs_status()
        for x_reasonheir in self._reasonheirs.values():
            x_reasonheir.set_status(factheirs=self._factheirs)

    def set_active(
        self,
        tree_traverse_count: int,
        world_lobbyboxs: dict[LobbyID, LobbyBox] = None,
        world_owner_id: CharID = None,
    ):
        prev_to_now_active = deepcopy(self._active)
        self._active = self._create_active(world_lobbyboxs, world_owner_id)
        self._set_idea_task()
        self.record_active_hx(
            tree_traverse_count=tree_traverse_count,
            prev_active=prev_to_now_active,
            now_active=self._active,
        )

    def _set_idea_task(self):
        self._task = False
        if self.pledge and self._active and self._reasonheirs_satisfied():
            self._task = True

    def _reasonheirs_satisfied(self) -> bool:
        return self._reasonheirs == {} or self._any_reasonheir_task_true()

    def _any_reasonheir_task_true(self) -> bool:
        return any(x_reasonheir._task for x_reasonheir in self._reasonheirs.values())

    def _create_active(
        self, world_lobbyboxs: dict[LobbyID, LobbyBox], world_owner_id: CharID
    ) -> bool:
        self.set_reasonheirs_status()
        x_bool = self._are_all_reasonheir_active_true()
        if (
            x_bool
            and world_lobbyboxs != {}
            and world_owner_id != None
            and self._doerheir._lobbyholds != {}
        ):
            self._doerheir.set_owner_id_doer(world_lobbyboxs, world_owner_id)
            if self._doerheir._owner_id_doer is False:
                x_bool = False
        return x_bool

    def _are_all_reasonheir_active_true(self) -> bool:
        return all(
            x_reasonheir._status != False for x_reasonheir in self._reasonheirs.values()
        )

    def clear_reasonheirs_status(self):
        for reason in self._reasonheirs.values():
            reason.clear_status()

    def _coalesce_with_reasonunits(self, reasonheirs: dict[RoadUnit, ReasonHeir]):
        reasonheirs_new = get_empty_dict_if_none(x_dict=deepcopy(reasonheirs))
        reasonheirs_new.update(self._reasonunits)
        return reasonheirs_new

    def set_reasonheirs(
        self,
        world_idea_dict: dict[RoadUnit,],
        reasonheirs: dict[RoadUnit, ReasonCore] = None,
    ):
        if reasonheirs is None:
            reasonheirs = self._reasonheirs
        coalesced_reasons = self._coalesce_with_reasonunits(reasonheirs)

        self._reasonheirs = {}
        for old_reasonheir in coalesced_reasons.values():
            new_reasonheir = reasonheir_shop(
                base=old_reasonheir.base,
                base_idea_active_requisite=old_reasonheir.base_idea_active_requisite,
            )
            new_reasonheir.inherit_from_reasonheir(old_reasonheir)

            # if world_idea_dict != None:
            base_idea = world_idea_dict.get(old_reasonheir.base)
            if base_idea != None:
                new_reasonheir.set_base_idea_active_value(base_idea._active)

            self._reasonheirs[new_reasonheir.base] = new_reasonheir

    def set_idearoot_inherit_reasonheirs(self):
        self._reasonheirs = {}
        for x_reasonunit in self._reasonunits.values():
            new_reasonheir = reasonheir_shop(x_reasonunit.base)
            new_reasonheir.inherit_from_reasonheir(x_reasonunit)
            self._reasonheirs[new_reasonheir.base] = new_reasonheir

    def get_reasonheir(self, base: RoadUnit) -> ReasonHeir:
        return self._reasonheirs.get(base)

    def get_reasonunits_dict(self):
        return {base: reason.get_dict() for base, reason in self._reasonunits.items()}

    def get_kids_dict(self):
        return {c_road: kid.get_dict() for c_road, kid in self._kids.items()}

    def get_awardlinks_dict(self):
        return {
            x_lobby_id: awardlink.get_dict()
            for x_lobby_id, awardlink in self._awardlinks.items()
        }

    def is_kidless(self):
        return self._kids == {}

    def is_arithmetic(self):
        return self._begin != None and self._close != None

    def is_awardheirless(self):
        x_bool = None
        if self._awardheirs in [{}, None]:
            x_bool = True
        elif self._awardheirs != [{}, None]:
            x_bool = False
        return x_bool

    def get_dict(self) -> dict[str, str]:
        x_dict = {"_weight": self._weight}

        if self._label != None:
            x_dict["_label"] = self._label
        if self._uid != None:
            x_dict["_uid"] = self._uid
        if self._kids not in [{}, None]:
            x_dict["_kids"] = self.get_kids_dict()
        if self._reasonunits not in [{}, None]:
            x_dict["_reasonunits"] = self.get_reasonunits_dict()
        if self._doerunit not in [None, doerunit_shop()]:
            x_dict["_doerunit"] = self.get_doerunit_dict()
        if self._healerhold not in [None, healerhold_shop()]:
            x_dict["_healerhold"] = self._healerhold.get_dict()
        if self._awardlinks not in [{}, None]:
            x_dict["_awardlinks"] = self.get_awardlinks_dict()
        if self._originunit not in [None, originunit_shop()]:
            x_dict["_originunit"] = self.get_originunit_dict()
        if self._begin != None:
            x_dict["_begin"] = self._begin
        if self._close != None:
            x_dict["_close"] = self._close
        if self._addin != None:
            x_dict["_addin"] = self._addin
        if self._numor != None:
            x_dict["_numor"] = self._numor
        if self._denom != None:
            x_dict["_denom"] = self._denom
        if self._reest != None:
            x_dict["_reest"] = self._reest
        if self._range_source_road != None:
            x_dict["_range_source_road"] = self._range_source_road
        if self._numeric_road != None:
            x_dict["_numeric_road"] = self._numeric_road
        if self.pledge:
            x_dict["pledge"] = self.pledge
        if self._problem_bool:
            x_dict["_problem_bool"] = self._problem_bool
        if self._factunits not in [{}, None]:
            x_dict["_factunits"] = self.get_factunits_dict()
        if self._is_expanded is False:
            x_dict["_is_expanded"] = self._is_expanded

        return x_dict

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        if is_sub_road(ref_road=self._parent_road, sub_road=old_road):
            self._parent_road = rebuild_road(self._parent_road, old_road, new_road)
        if is_sub_road(ref_road=self._range_source_road, sub_road=old_road):
            self._range_source_road = rebuild_road(
                self._range_source_road, old_road, new_road
            )
        if is_sub_road(ref_road=self._numeric_road, sub_road=old_road):
            self._numeric_road = rebuild_road(self._numeric_road, old_road, new_road)

        self._reasonunits == find_replace_road_key_dict(
            dict_x=self._reasonunits, old_road=old_road, new_road=new_road
        )

        self._factunits == find_replace_road_key_dict(
            dict_x=self._factunits, old_road=old_road, new_road=new_road
        )

    def set_doerunit_empty_if_none(self):
        if self._doerunit is None:
            self._doerunit = doerunit_shop()

    def set_doerheir(
        self,
        parent_doerheir: DoerHeir,
        world_lobbyboxs: dict[LobbyID, LobbyBox],
    ):
        self._doerheir = doerheir_shop()
        self._doerheir.set_lobbyholds(
            parent_doerheir=parent_doerheir,
            doerunit=self._doerunit,
            world_lobbyboxs=world_lobbyboxs,
        )

    def get_doerunit_dict(self):
        return self._doerunit.get_dict()


def ideaunit_shop(
    _label: RoadNode = None,
    _uid: int = None,  # Calculated field?
    _parent_road: RoadUnit = None,
    _kids: dict = None,
    _weight: int = 1,
    _awardlinks: dict[LobbyID, AwardLink] = None,
    _awardheirs: dict[LobbyID, AwardHeir] = None,  # Calculated field
    _awardlines: dict[LobbyID, AwardLink] = None,  # Calculated field
    _reasonunits: dict[RoadUnit, ReasonUnit] = None,
    _reasonheirs: dict[RoadUnit, ReasonHeir] = None,  # Calculated field
    _doerunit: DoerUnit = None,
    _doerheir: DoerHeir = None,  # Calculated field
    _factunits: dict[FactUnit] = None,
    _factheirs: dict[FactHeir] = None,  # Calculated field
    _healerhold: HealerHold = None,
    _begin: float = None,
    _close: float = None,
    _addin: float = None,
    _denom: int = None,
    _numor: int = None,
    _reest: bool = None,
    _range_source_road: RoadUnit = None,
    _numeric_road: RoadUnit = None,
    pledge: bool = None,
    _originunit: OriginUnit = None,
    _root: bool = None,
    _world_real_id: RealID = None,
    _problem_bool: bool = None,
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
    _all_char_cred: bool = None,
    _all_char_debt: bool = None,
    _is_expanded: bool = True,
    _active_hx: dict[int, bool] = None,
    _road_delimiter: str = None,
    _healerhold_ratio: float = None,
) -> IdeaUnit:
    _world_real_id = root_label() if _world_real_id is None else _world_real_id
    _healerhold = healerhold_shop() if _healerhold is None else _healerhold

    x_ideakid = IdeaUnit(
        _label=None,
        _uid=_uid,
        _parent_road=_parent_road,
        _kids=get_empty_dict_if_none(_kids),
        _weight=get_positive_int(_weight),
        _awardlinks=get_empty_dict_if_none(_awardlinks),
        _awardheirs=get_empty_dict_if_none(_awardheirs),
        _awardlines=get_empty_dict_if_none(_awardlines),
        _reasonunits=get_empty_dict_if_none(_reasonunits),
        _reasonheirs=get_empty_dict_if_none(_reasonheirs),
        _doerunit=_doerunit,
        _doerheir=_doerheir,
        _factunits=get_empty_dict_if_none(_factunits),
        _factheirs=get_empty_dict_if_none(_factheirs),
        _healerhold=_healerhold,
        _begin=_begin,
        _close=_close,
        _addin=_addin,
        _denom=_denom,
        _numor=_numor,
        _reest=_reest,
        _range_source_road=_range_source_road,
        _numeric_road=_numeric_road,
        pledge=get_False_if_None(pledge),
        _problem_bool=get_False_if_None(_problem_bool),
        _originunit=_originunit,
        _root=get_False_if_None(_root),
        _world_real_id=_world_real_id,
        # Calculated fields
        _level=_level,
        _fund_ratio=_fund_ratio,
        _fund_coin=_fund_coin,
        _fund_onset=_fund_onset,
        _fund_cease=_fund_cease,
        _task=_task,
        _active=_active,
        _ancestor_pledge_count=_ancestor_pledge_count,
        _descendant_pledge_count=_descendant_pledge_count,
        _all_char_cred=_all_char_cred,
        _all_char_debt=_all_char_debt,
        _is_expanded=_is_expanded,
        _active_hx=get_empty_dict_if_none(_active_hx),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _healerhold_ratio=get_0_if_None(_healerhold_ratio),
    )
    if x_ideakid._root:
        x_ideakid.set_idea_label(_label=_world_real_id)
    else:
        x_ideakid.set_idea_label(_label=_label)
    x_ideakid.set_doerunit_empty_if_none()
    x_ideakid.set_originunit_empty_if_none()
    return x_ideakid


class Idea_root_LabelNotEmptyException(Exception):
    pass


def get_obj_from_idea_dict(x_dict: dict[str,], dict_key: str) -> any:
    if dict_key == "_reasonunits":
        return (
            reasons_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else None
        )
    elif dict_key == "_doerunit":
        return (
            doerunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else doerunit_shop()
        )
    elif dict_key == "_healerhold":
        return (
            healerhold_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else healerhold_shop()
        )
    elif dict_key == "_originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else originunit_shop()
        )
    elif dict_key == "_factunits":
        return (
            factunits_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else factunits_get_from_dict({})
        )
    elif dict_key == "_awardlinks":
        return (
            awardlinks_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else awardlinks_get_from_dict({})
        )
    elif dict_key in {"_kids"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else {}
    elif dict_key in {"pledge", "_problem_bool"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    elif dict_key in {"_is_expanded"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else True
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None
