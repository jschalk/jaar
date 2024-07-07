from src._instrument.python import (
    get_empty_dict_if_none,
    get_1_if_None,
    get_0_if_None,
    get_False_if_None,
)
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
)
from src._world.meld import get_meld_default
from src._world.healer import HealerHold, healerhold_shop, healerhold_get_from_dict
from src._world.reason_culture import (
    CultureUnit,
    CultureHeir,
    cultureunit_shop,
    cultureheir_shop,
    cultureunit_get_from_dict,
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
    RoadUnit,
    rebuild_road,
    find_replace_road_key_dict,
    reasons_get_from_dict,
    factunits_get_from_dict,
)
from src._world.beliefunit import (
    FiscalHeir,
    FiscalLink,
    fiscallinks_get_from_dict,
    BeliefID,
    FiscalLine,
    fiscalline_shop,
    fiscalheir_shop,
    BeliefUnit,
)
from src._world.origin import OriginUnit, originunit_get_from_dict
from src._world.origin import originunit_shop
from src._world.meld import get_meld_weight, validate_meld_strategy
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
    cultureunit: CultureUnit = None
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
    fiscallink: FiscalLink = None
    fiscallink_del: BeliefID = None
    is_expanded: bool = None
    meld_strategy: str = None
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
    cultureunit: CultureUnit = None,
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
    fiscallink: FiscalLink = None,
    fiscallink_del: BeliefID = None,
    is_expanded: bool = None,
    meld_strategy: str = None,
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
        cultureunit=cultureunit,
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
        fiscallink=fiscallink,
        fiscallink_del=fiscallink_del,
        is_expanded=is_expanded,
        meld_strategy=meld_strategy,
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
    _kids: dict = None
    _world_real_id: RealID = None
    _uid: int = None  # Calculated field?
    _fiscallinks: dict[BeliefID, FiscalLink] = None
    _fiscalheirs: dict[BeliefID, FiscalHeir] = None  # Calculated field
    _fiscallines: dict[BeliefID, FiscalLine] = None  # Calculated field
    _reasonunits: dict[RoadUnit, ReasonUnit] = None
    _reasonheirs: dict[RoadUnit, ReasonHeir] = None  # Calculated field
    _cultureunit: CultureUnit = None
    _cultureheir: CultureHeir = None  # Calculated field
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
    _meld_strategy: str = None
    _problem_bool: bool = None
    # Calculated fields
    _level: int = None
    _kids_total_weight: int = None
    _world_importance: float = None
    _world_fund_onset: float = None
    _world_fund_cease: float = None
    _task: bool = None
    _active: bool = None
    _ancestor_pledge_count: int = None
    _descendant_pledge_count: int = None
    _all_char_cred: bool = None
    _all_char_debt: bool = None
    _is_expanded: bool = None
    _sibling_total_weight: int = None
    _active_hx: dict[int, bool] = None
    _road_delimiter: str = None
    _healerhold_importance: float = None

    def is_agenda_item(self, necessary_base: RoadUnit = None) -> bool:
        # bool_x = False
        return (
            self.pledge and self._active and self.base_reasonunit_exists(necessary_base)
        )

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

    def set_world_importance(
        self,
        fund_onset_x: float,
        parent_world_importance: float = None,
        parent_fund_cease: float = None,
    ):
        parent_world_importance = get_1_if_None(parent_world_importance)
        self.set_kids_total_weight()
        self._world_importance = None
        self._world_fund_onset = None
        self._world_fund_cease = None
        sibling_ratio = self._weight / self._sibling_total_weight
        self._world_importance = parent_world_importance * sibling_ratio
        self._world_fund_onset = fund_onset_x
        self._world_fund_cease = self._world_fund_onset + self._world_importance
        self._world_fund_cease = min(self._world_fund_cease, parent_fund_cease)
        self.set_fiscalheirs_world_cred_debt()

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

    def set_sibling_total_weight(self, parent_kids_total_weight):
        self._sibling_total_weight = parent_kids_total_weight

    def set_level(self, parent_level):
        self._level = parent_level + 1

    def set_parent_road(self, parent_road):
        self._parent_road = parent_road

    def inherit_fiscalheirs(
        self, parent_fiscalheirs: dict[BeliefID, FiscalHeir] = None
    ):
        if parent_fiscalheirs is None:
            parent_fiscalheirs = {}

        self._fiscalheirs = {}
        for ib in parent_fiscalheirs.values():
            fiscalheir = fiscalheir_shop(
                belief_id=ib.belief_id,
                credor_weight=ib.credor_weight,
                debtor_weight=ib.debtor_weight,
            )
            self._fiscalheirs[fiscalheir.belief_id] = fiscalheir

        for ib in self._fiscallinks.values():
            fiscalheir = fiscalheir_shop(
                belief_id=ib.belief_id,
                credor_weight=ib.credor_weight,
                debtor_weight=ib.debtor_weight,
            )
            self._fiscalheirs[fiscalheir.belief_id] = fiscalheir

    def set_kidless_fiscallines(self):
        # get fiscallines from self
        for bh in self._fiscalheirs.values():
            x_fiscalline = fiscalline_shop(
                belief_id=bh.belief_id,
                _world_cred=bh._world_cred,
                _world_debt=bh._world_debt,
            )
            self._fiscallines[x_fiscalline.belief_id] = x_fiscalline

    def set_fiscallines(self, child_fiscallines: dict[BeliefID, FiscalLine] = None):
        if child_fiscallines is None:
            child_fiscallines = {}

        # get fiscallines from child
        for bl in child_fiscallines.values():
            if self._fiscallines.get(bl.belief_id) is None:
                self._fiscallines[bl.belief_id] = fiscalline_shop(
                    belief_id=bl.belief_id,
                    _world_cred=0,
                    _world_debt=0,
                )

            self._fiscallines[bl.belief_id].add_world_cred_debt(
                world_cred=bl._world_cred, world_debt=bl._world_debt
            )

    def set_kids_total_weight(self):
        self._kids_total_weight = 0
        for x_idea in self._kids.values():
            self._kids_total_weight += x_idea._weight

    def get_fiscalheirs_credor_weight_sum(self) -> float:
        return sum(
            fiscallink.credor_weight for fiscallink in self._fiscalheirs.values()
        )

    def get_fiscalheirs_debtor_weight_sum(self) -> float:
        return sum(
            fiscallink.debtor_weight for fiscallink in self._fiscalheirs.values()
        )

    def set_fiscalheirs_world_cred_debt(self):
        fiscalheirs_credor_weight_sum = self.get_fiscalheirs_credor_weight_sum()
        fiscalheirs_debtor_weight_sum = self.get_fiscalheirs_debtor_weight_sum()
        for fiscalheir_x in self._fiscalheirs.values():
            fiscalheir_x.set_world_cred_debt(
                idea_world_importance=self._world_importance,
                fiscalheirs_credor_weight_sum=fiscalheirs_credor_weight_sum,
                fiscalheirs_debtor_weight_sum=fiscalheirs_debtor_weight_sum,
            )

    def clear_fiscallines(self):
        self._fiscallines = {}

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

    def _meld_reasonunits(self, exterior_idea):
        for lx in exterior_idea._reasonunits.values():
            if self._reasonunits.get(lx.base) is None:
                self._reasonunits[lx.base] = lx
            else:
                self._reasonunits.get(lx.base).meld(lx)

    def _meld_fiscallinks(self, exterior_idea):
        for bl in exterior_idea._fiscallinks.values():
            if self._fiscallinks.get(bl.belief_id) != None:
                self._fiscallinks.get(bl.belief_id).meld(
                    exterior_fiscallink=bl,
                    exterior_meld_strategy=exterior_idea._meld_strategy,
                    src_meld_strategy=self._meld_strategy,
                )
            else:
                self._fiscallinks[bl.belief_id] = bl

    def _meld_factunits(self, exterior_idea):
        for hc in exterior_idea._factunits.values():
            if self._factunits.get(hc.base) is None:
                self._factunits[hc.base] = hc
            else:
                self._factunits.get(hc.base).meld(hc)

    def meld(
        self,
        exterior_idea,
        _idearoot: bool = None,
        char_id: CharID = None,
        char_weight: float = None,
    ):
        if _idearoot and self._label != exterior_idea._label:
            raise InvalidIdeaException(
                f"Meld fail idearoot _label '{self._label}' not the equal as '{exterior_idea._label}'"
            )
        if _idearoot:
            self._weight = 1
        else:
            self._weight = get_meld_weight(
                src_weight=self._weight,
                src_meld_strategy=self._meld_strategy,
                exterior_weight=exterior_idea._weight,
                exterior_meld_strategy=exterior_idea._meld_strategy,
            )
        self._meld_reasonunits(exterior_idea=exterior_idea)
        self._meld_fiscallinks(exterior_idea=exterior_idea)
        self._meld_factunits(exterior_idea=exterior_idea)
        if exterior_idea._meld_strategy != "override":
            self._meld_attributes_that_must_be_equal(exterior_idea=exterior_idea)
        else:
            self._meld_attributes_overide(exterior_idea=exterior_idea)
        self._meld_originlinks(char_id, char_weight)

    def _meld_originlinks(self, char_id: CharID, char_weight: float):
        if char_id != None:
            self._originunit.set_originlink(char_id=char_id, weight=char_weight)

    def set_originunit_empty_if_none(self):
        if self._originunit is None:
            self._originunit = originunit_shop()

    def get_originunit_dict(self) -> dict[str, str]:
        return self._originunit.get_dict()

    def _meld_attributes_overide(self, exterior_idea):
        self._uid = exterior_idea._uid
        self._begin = exterior_idea._begin
        self._close = exterior_idea._close
        self._addin = exterior_idea._addin
        self._denom = exterior_idea._denom
        self._numor = exterior_idea._numor
        self._reest = exterior_idea._reest
        self._range_source_road = exterior_idea._range_source_road
        self._numeric_road = exterior_idea._numeric_road
        self.pledge = exterior_idea.pledge
        self._is_expanded = exterior_idea._is_expanded

    def _meld_attributes_that_must_be_equal(self, exterior_idea):
        to_be_equal_attributes = [
            ("_uid", self._uid, exterior_idea._uid),
            ("_begin", self._begin, exterior_idea._begin),
            ("_close", self._close, exterior_idea._close),
            ("_addin", self._addin, exterior_idea._addin),
            ("_denom", self._denom, exterior_idea._denom),
            ("_numor", self._numor, exterior_idea._numor),
            ("_reest", self._reest, exterior_idea._reest),
            (
                "_range_source_road",
                self._range_source_road,
                exterior_idea._range_source_road,
            ),
            ("_numeric_road", self._numeric_road, exterior_idea._numeric_road),
            ("pledge", self.pledge, exterior_idea.pledge),
            ("_is_expanded", self._is_expanded, exterior_idea._is_expanded),
        ]
        while to_be_equal_attributes != []:
            attrs = to_be_equal_attributes.pop()
            if attrs[1] != attrs[2]:
                raise InvalidIdeaException(
                    f"Meld fail idea={self.get_road()} {attrs[0]}:{attrs[1]} with {exterior_idea.get_road()} {attrs[0]}:{attrs[2]}"
                )

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
        if idea_attr.cultureunit != None:
            self._cultureunit = idea_attr.cultureunit
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
        if idea_attr.fiscallink != None:
            self.set_fiscallink(fiscallink=idea_attr.fiscallink)
        if idea_attr.fiscallink_del != None:
            self.del_fiscallink(belief_id=idea_attr.fiscallink_del)
        if idea_attr.is_expanded != None:
            self._is_expanded = idea_attr.is_expanded
        if idea_attr.pledge != None:
            self.pledge = idea_attr.pledge
        if idea_attr.meld_strategy != None:
            self._meld_strategy = validate_meld_strategy(idea_attr.meld_strategy)
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

    def set_fiscallink(self, fiscallink: FiscalLink):
        self._fiscallinks[fiscallink.belief_id] = fiscallink

    def del_fiscallink(self, belief_id: BeliefID):
        try:
            self._fiscallinks.pop(belief_id)
        except KeyError as e:
            raise (f"Cannot delete fiscallink '{belief_id}'.") from e

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
        world_beliefunits: dict[BeliefID, BeliefUnit] = None,
        world_owner_id: CharID = None,
    ):
        prev_to_now_active = deepcopy(self._active)
        self._active = self._create_active(world_beliefunits, world_owner_id)
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
        self, world_beliefunits: dict[BeliefID, BeliefUnit], world_owner_id: CharID
    ) -> bool:
        self.set_reasonheirs_status()
        x_bool = self._are_all_reasonheir_active_true()
        if (
            x_bool
            and world_beliefunits != {}
            and world_owner_id != None
            and self._cultureheir._heldbeliefs != {}
        ):
            self._cultureheir.set_owner_id_culture(world_beliefunits, world_owner_id)
            if self._cultureheir._owner_id_culture is False:
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

    def get_fiscallinks_dict(self):
        return {
            x_belief_id: fiscallink.get_dict()
            for x_belief_id, fiscallink in self._fiscallinks.items()
        }

    def is_kidless(self):
        return self._kids == {}

    def is_arithmetic(self):
        return self._begin != None and self._close != None

    def is_fiscalheirless(self):
        x_bool = None
        if self._fiscalheirs in [{}, None]:
            x_bool = True
        elif self._fiscalheirs != [{}, None]:
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
        if self._cultureunit not in [None, cultureunit_shop()]:
            x_dict["_cultureunit"] = self.get_cultureunit_dict()
        if self._healerhold not in [None, healerhold_shop()]:
            x_dict["_healerhold"] = self._healerhold.get_dict()
        if self._fiscallinks not in [{}, None]:
            x_dict["_fiscallinks"] = self.get_fiscallinks_dict()
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
        if self._meld_strategy != "default":
            x_dict["_meld_strategy"] = self._meld_strategy

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

    def set_cultureunit_empty_if_none(self):
        if self._cultureunit is None:
            self._cultureunit = cultureunit_shop()

    def set_cultureheir(
        self,
        parent_cultureheir: CultureHeir,
        world_beliefs: dict[BeliefID, BeliefUnit],
    ):
        self._cultureheir = cultureheir_shop()
        self._cultureheir.set_heldbeliefs(
            parent_cultureheir=parent_cultureheir,
            cultureunit=self._cultureunit,
            world_beliefs=world_beliefs,
        )

    def get_cultureunit_dict(self):
        return self._cultureunit.get_dict()


def ideaunit_shop(
    _label: RoadNode = None,
    _uid: int = None,  # Calculated field?
    _parent_road: RoadUnit = None,
    _kids: dict = None,
    _weight: int = 1,
    _fiscallinks: dict[BeliefID, FiscalLink] = None,
    _fiscalheirs: dict[BeliefID, FiscalHeir] = None,  # Calculated field
    _fiscallines: dict[BeliefID, FiscalLink] = None,  # Calculated field
    _reasonunits: dict[RoadUnit, ReasonUnit] = None,
    _reasonheirs: dict[RoadUnit, ReasonHeir] = None,  # Calculated field
    _cultureunit: CultureUnit = None,
    _cultureheir: CultureHeir = None,  # Calculated field
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
    _meld_strategy: str = None,
    _root: bool = None,
    _world_real_id: RealID = None,
    _problem_bool: bool = None,
    # Calculated fields
    _level: int = None,
    _kids_total_weight: int = None,
    _world_importance: float = None,
    _world_fund_onset: float = None,
    _world_fund_cease: float = None,
    _task: bool = None,
    _active: bool = None,
    _ancestor_pledge_count: int = None,
    _descendant_pledge_count: int = None,
    _all_char_cred: bool = None,
    _all_char_debt: bool = None,
    _is_expanded: bool = True,
    _sibling_total_weight: int = None,
    _active_hx: dict[int, bool] = None,
    _road_delimiter: str = None,
    _healerhold_importance: float = None,
) -> IdeaUnit:
    if _meld_strategy is None:
        _meld_strategy = get_meld_default()
    if _world_real_id is None:
        _world_real_id = root_label()
    if _healerhold is None:
        _healerhold = healerhold_shop()

    x_ideakid = IdeaUnit(
        _label=None,
        _uid=_uid,
        _parent_road=_parent_road,
        _kids=get_empty_dict_if_none(_kids),
        _weight=_weight,
        _fiscallinks=get_empty_dict_if_none(_fiscallinks),
        _fiscalheirs=get_empty_dict_if_none(_fiscalheirs),
        _fiscallines=get_empty_dict_if_none(_fiscallines),
        _reasonunits=get_empty_dict_if_none(_reasonunits),
        _reasonheirs=get_empty_dict_if_none(_reasonheirs),
        _cultureunit=_cultureunit,
        _cultureheir=_cultureheir,
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
        _meld_strategy=_meld_strategy,
        _root=get_False_if_None(_root),
        _world_real_id=_world_real_id,
        # Calculated fields
        _level=_level,
        _kids_total_weight=get_0_if_None(_kids_total_weight),
        _world_importance=_world_importance,
        _world_fund_onset=_world_fund_onset,
        _world_fund_cease=_world_fund_cease,
        _task=_task,
        _active=_active,
        _ancestor_pledge_count=_ancestor_pledge_count,
        _descendant_pledge_count=_descendant_pledge_count,
        _all_char_cred=_all_char_cred,
        _all_char_debt=_all_char_debt,
        _is_expanded=_is_expanded,
        _sibling_total_weight=_sibling_total_weight,
        _active_hx=get_empty_dict_if_none(_active_hx),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _healerhold_importance=get_0_if_None(_healerhold_importance),
    )
    if x_ideakid._root:
        x_ideakid.set_idea_label(_label=_world_real_id)
    else:
        x_ideakid.set_idea_label(_label=_label)
    x_ideakid.set_cultureunit_empty_if_none()
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
    elif dict_key == "_cultureunit":
        return (
            cultureunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else cultureunit_shop()
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
    elif dict_key == "_fiscallinks":
        return (
            fiscallinks_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else fiscallinks_get_from_dict({})
        )
    elif dict_key in {"_kids"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else {}
    elif dict_key in {"pledge", "_problem_bool"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    elif dict_key in {"_is_expanded"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else True
    # elif dict_key == "_meld_strategy":
    #     return x_dict[dict_key] if x_dict.get(dict_key) != None else "default"
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None
