from src.f00_instrument.dict_tool import (
    get_json_from_dict,
    get_dict_from_json,
    get_1_if_None,
    get_0_if_None,
    get_False_if_None,
    get_empty_dict_if_none,
)
from src.f01_road.finance import (
    valid_finance_ratio,
    default_respect_bit_if_none,
    default_penny_if_none,
    default_fund_coin_if_none,
    validate_fund_pool,
    BitNum,
    RespectNum,
    PennyNum,
    FundCoin,
    FundNum,
    allot_scale,
    validate_respect_num,
    TimeLinePoint,
)
from src.f01_road.jaar_config import max_tree_traverse_default
from src.f01_road.road import (
    get_parent_road,
    is_sub_road,
    all_roadunits_between,
    road_validate,
    rebuild_road,
    get_terminus_node,
    get_root_node_from_road,
    get_ancestor_roads,
    get_default_fiscal_id_roadnode,
    get_all_road_nodes,
    get_forefather_roads,
    create_road,
    default_road_delimiter_if_none,
    RoadNode,
    RoadUnit,
    is_string_in_road,
    OwnerID,
    AcctID,
    HealerID,
    FiscalID,
    roadunit_valid_dir_path,
)
from src.f02_bud.acct import AcctUnit, acctunits_get_from_dict, acctunit_shop
from src.f02_bud.group import (
    AwardLink,
    GroupID,
    GroupBox,
    groupbox_shop,
    membership_shop,
)
from src.f02_bud.healer import HealerLink
from src.f02_bud.reason_item import (
    FactUnit,
    FactUnit,
    ReasonUnit,
    RoadUnit,
    factunit_shop,
)
from src.f02_bud.reason_team import TeamUnit
from src.f02_bud.tree_metrics import TreeMetrics, treemetrics_shop
from src.f02_bud.origin import originunit_get_from_dict, originunit_shop, OriginUnit
from src.f02_bud.item import (
    ItemUnit,
    itemunit_shop,
    itemattrholder_shop,
    ItemAttrHolder,
    get_obj_from_item_dict,
)
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class InvalidBudException(Exception):
    pass


class InvalidLabelException(Exception):
    pass


class NewDelimiterException(Exception):
    pass


class AcctUnitsCredorDebtorSumException(Exception):
    pass


class AcctMissingException(Exception):
    pass


class Exception_keeps_justified(Exception):
    pass


class _bit_RatioException(Exception):
    pass


class _last_gift_idException(Exception):
    pass


class healerlink_group_id_Exception(Exception):
    pass


class _gogo_calc_stop_calc_Exception(Exception):
    pass


@dataclass
class BudUnit:
    _fiscal_id: FiscalID = None
    _owner_id: OwnerID = None
    _last_gift_id: int = None
    tally: float = None
    _accts: dict[AcctID, AcctUnit] = None
    _itemroot: ItemUnit = None
    max_tree_traverse: int = None
    _road_delimiter: str = None
    fund_pool: FundNum = None
    fund_coin: FundCoin = None
    penny: PennyNum = None
    respect_bit: BitNum = None
    credor_respect: RespectNum = None
    debtor_respect: RespectNum = None
    purview_time_fid: TimeLinePoint = None
    _originunit: OriginUnit = None  # In job buds this shows source
    # settle_bud Calculated field begin
    _item_dict: dict[RoadUnit, ItemUnit] = None
    _keep_dict: dict[RoadUnit, ItemUnit] = None
    _healers_dict: dict[HealerID, dict[RoadUnit, ItemUnit]] = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _keeps_justified: bool = None
    _keeps_buildable: bool = None
    _sum_healerlink_share: float = None
    _groupboxs: dict[GroupID, GroupBox] = None
    _offtrack_kids_mass_set: set[RoadUnit] = None
    _offtrack_fund: float = None
    _reason_bases: set[RoadUnit] = None
    _range_inheritors: dict[RoadUnit, RoadUnit] = None
    # settle_bud Calculated field end

    def del_last_gift_id(self):
        self._last_gift_id = None

    def set_last_gift_id(self, x_last_gift_id: int):
        if self._last_gift_id is not None and x_last_gift_id < self._last_gift_id:
            exception_str = f"Cannot set _last_gift_id to {x_last_gift_id} because it is less than {self._last_gift_id}."
            raise _last_gift_idException(exception_str)
        self._last_gift_id = x_last_gift_id

    def set_purview_time_fid(self, x_purview_time_fid: TimeLinePoint):
        self.purview_time_fid = x_purview_time_fid

    def set_fund_pool(self, x_fund_pool):
        if valid_finance_ratio(x_fund_pool, self.fund_coin) is False:
            exception_str = f"Bud '{self._owner_id}' cannot set fund_pool='{x_fund_pool}'. It is not divisible by fund_coin '{self.fund_coin}'"
            raise _bit_RatioException(exception_str)

        self.fund_pool = validate_fund_pool(x_fund_pool)

    def set_acct_respect(self, x_acct_pool: int):
        self.set_credor_respect(x_acct_pool)
        self.set_debtor_respect(x_acct_pool)
        self.set_fund_pool(x_acct_pool)

    def set_credor_respect(self, new_credor_respect: int):
        if valid_finance_ratio(new_credor_respect, self.respect_bit) is False:
            exception_str = f"Bud '{self._owner_id}' cannot set credor_respect='{new_credor_respect}'. It is not divisible by bit '{self.respect_bit}'"
            raise _bit_RatioException(exception_str)
        self.credor_respect = new_credor_respect

    def set_debtor_respect(self, new_debtor_respect: int):
        if valid_finance_ratio(new_debtor_respect, self.respect_bit) is False:
            exception_str = f"Bud '{self._owner_id}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible by bit '{self.respect_bit}'"
            raise _bit_RatioException(exception_str)
        self.debtor_respect = new_debtor_respect

    def make_road(
        self,
        parent_road: RoadUnit = None,
        terminus_node: RoadNode = None,
    ) -> RoadUnit:
        x_road = create_road(
            parent_road=parent_road,
            terminus_node=terminus_node,
            delimiter=self._road_delimiter,
        )
        return road_validate(x_road, self._road_delimiter, self._fiscal_id)

    def make_l1_road(self, l1_node: RoadNode):
        return self.make_road(self._fiscal_id, l1_node)

    def set_road_delimiter(self, new_road_delimiter: str):
        self.settle_bud()
        if self._road_delimiter != new_road_delimiter:
            for x_item_road in self._item_dict.keys():
                if is_string_in_road(new_road_delimiter, x_item_road):
                    exception_str = f"Cannot modify delimiter to '{new_road_delimiter}' because it exists an item label '{x_item_road}'"
                    raise NewDelimiterException(exception_str)

            # modify all road attributes in itemunits
            self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)
            for x_item in self._item_dict.values():
                x_item.set_road_delimiter(self._road_delimiter)

    def set_fiscal_id(self, fiscal_id: str):
        old_fiscal_id = copy_deepcopy(self._fiscal_id)
        self.settle_bud()
        for item_obj in self._item_dict.values():
            item_obj._bud_fiscal_id = fiscal_id
        self._fiscal_id = fiscal_id
        self.edit_item_label(old_road=old_fiscal_id, new_label=self._fiscal_id)
        self.settle_bud()

    def set_max_tree_traverse(self, x_int: int):
        if x_int < 2 or not float(x_int).is_integer():
            raise InvalidBudException(
                f"set_max_tree_traverse: '{x_int}' must be number that is 2 or greater"
            )
        else:
            self.max_tree_traverse = x_int

    def _get_relevant_roads(self, roads: dict[RoadUnit,]) -> set[RoadUnit]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for x_road in roads:
            to_evaluate_list.append(x_road)
            to_evaluate_hx_dict[x_road] = "to_evaluate"
        evaluated_roads = set()

        # while roads_to_evaluate != [] and count_x <= tree_metrics.node_count:
        # Why count_x? because count_x might be wrong thing to measure
        # nice to avoid infinite loops from programming errors though...
        while to_evaluate_list != []:
            x_road = to_evaluate_list.pop()
            x_item = self.get_item_obj(x_road)
            for reasonunit_obj in x_item.reasonunits.values():
                reason_base = reasonunit_obj.base
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=reason_base,
                    road_type="reasonunit_base",
                )
            forefather_roads = get_forefather_roads(x_road)
            for forefather_road in forefather_roads:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=forefather_road,
                    road_type="forefather",
                )

            evaluated_roads.add(x_road)
        return evaluated_roads

    def _evaluate_relevancy(
        self,
        to_evaluate_list: list[RoadUnit],
        to_evaluate_hx_dict: dict[RoadUnit, int],
        to_evaluate_road: RoadUnit,
        road_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_road) is None:
            to_evaluate_list.append(to_evaluate_road)
            to_evaluate_hx_dict[to_evaluate_road] = road_type

            if road_type == "reasonunit_base":
                ru_base_item = self.get_item_obj(to_evaluate_road)
                for descendant_road in ru_base_item.get_descendant_roads_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_road=descendant_road,
                        road_type="reasonunit_descendant",
                    )

    def all_items_relevant_to_pledge_item(self, road: RoadUnit) -> bool:
        pledge_item_assoc_set = set(self._get_relevant_roads({road}))
        all_items_set = set(self.get_item_tree_ordered_road_list())
        return all_items_set == all_items_set.intersection(pledge_item_assoc_set)

    def get_awardlinks_metrics(self) -> dict[GroupID, AwardLink]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.awardlinks_metrics

    def add_to_groupbox_fund_give_fund_take(
        self,
        group_id: GroupID,
        awardheir_fund_give: float,
        awardheir_fund_take: float,
    ):
        x_groupbox = self.get_groupbox(group_id)
        if x_groupbox is not None:
            x_groupbox._fund_give += awardheir_fund_give
            x_groupbox._fund_take += awardheir_fund_take

    def add_to_groupbox_fund_agenda_give_take(
        self,
        group_id: GroupID,
        awardline_fund_give: float,
        awardline_fund_take: float,
    ):
        x_groupbox = self.get_groupbox(group_id)
        if awardline_fund_give is not None and awardline_fund_take is not None:
            x_groupbox._fund_agenda_give += awardline_fund_give
            x_groupbox._fund_agenda_take += awardline_fund_take

    def add_to_acctunit_fund_give_take(
        self,
        acctunit_acct_id: AcctID,
        fund_give,
        fund_take: float,
        fund_agenda_give: float,
        fund_agenda_take: float,
    ):
        x_acctunit = self.get_acct(acctunit_acct_id)
        x_acctunit.add_fund_give_take(
            fund_give=fund_give,
            fund_take=fund_take,
            fund_agenda_give=fund_agenda_give,
            fund_agenda_take=fund_agenda_take,
        )

    def del_acctunit(self, acct_id: str):
        self._accts.pop(acct_id)

    def add_acctunit(
        self, acct_id: AcctID, credit_belief: int = None, debtit_belief: int = None
    ):
        x_road_delimiter = self._road_delimiter
        acctunit = acctunit_shop(
            acct_id, credit_belief, debtit_belief, x_road_delimiter
        )
        self.set_acctunit(acctunit)

    def set_acctunit(self, x_acctunit: AcctUnit, auto_set_membership: bool = True):
        if x_acctunit._road_delimiter != self._road_delimiter:
            x_acctunit._road_delimiter = self._road_delimiter
        if x_acctunit._respect_bit != self.respect_bit:
            x_acctunit._respect_bit = self.respect_bit
        if auto_set_membership and x_acctunit.memberships_exist() is False:
            x_acctunit.add_membership(x_acctunit.acct_id)
        self._accts[x_acctunit.acct_id] = x_acctunit

    def acct_exists(self, acct_id: AcctID) -> bool:
        return self.get_acct(acct_id) is not None

    def edit_acctunit(
        self, acct_id: AcctID, credit_belief: int = None, debtit_belief: int = None
    ):
        if self._accts.get(acct_id) is None:
            raise AcctMissingException(f"AcctUnit '{acct_id}' does not exist.")
        x_acctunit = self.get_acct(acct_id)
        if credit_belief is not None:
            x_acctunit.set_credit_belief(credit_belief)
        if debtit_belief is not None:
            x_acctunit.set_debtit_belief(debtit_belief)
        self.set_acctunit(x_acctunit)

    def clear_acctunits_memberships(self):
        for x_acctunit in self._accts.values():
            x_acctunit.clear_memberships()

    def get_acct(self, acct_id: AcctID) -> AcctUnit:
        return self._accts.get(acct_id)

    def get_acctunit_group_ids_dict(self) -> dict[GroupID, set[AcctID]]:
        x_dict = {}
        for x_acctunit in self._accts.values():
            for x_group_id in x_acctunit._memberships.keys():
                acct_id_set = x_dict.get(x_group_id)
                if acct_id_set is None:
                    x_dict[x_group_id] = {x_acctunit.acct_id}
                else:
                    acct_id_set.add(x_acctunit.acct_id)
                    x_dict[x_group_id] = acct_id_set
        return x_dict

    def set_groupbox(self, x_groupbox: GroupBox):
        x_groupbox._fund_coin = self.fund_coin
        self._groupboxs[x_groupbox.group_id] = x_groupbox

    def groupbox_exists(self, group_id: GroupID) -> bool:
        return self._groupboxs.get(group_id) is not None

    def get_groupbox(self, x_group_id: GroupID) -> GroupBox:
        return self._groupboxs.get(x_group_id)

    def create_symmetry_groupbox(self, x_group_id: GroupID) -> GroupBox:
        x_groupbox = groupbox_shop(x_group_id)
        for x_acctunit in self._accts.values():
            x_membership = membership_shop(
                group_id=x_group_id,
                credit_vote=x_acctunit.credit_belief,
                debtit_vote=x_acctunit.debtit_belief,
                _acct_id=x_acctunit.acct_id,
            )
            x_groupbox.set_membership(x_membership)
        return x_groupbox

    def get_tree_traverse_generated_groupboxs(self) -> set[GroupID]:
        x_acctunit_group_ids = set(self.get_acctunit_group_ids_dict().keys())
        all_group_ids = set(self._groupboxs.keys())
        return all_group_ids.difference(x_acctunit_group_ids)

    def _is_item_rangeroot(self, item_road: RoadUnit) -> bool:
        if self._fiscal_id == item_road:
            raise InvalidBudException(
                "its difficult to foresee a scenario where itemroot is rangeroot"
            )
        parent_road = get_parent_road(item_road)
        parent_item = self.get_item_obj(parent_road)
        return not parent_item.is_math()

    def _get_rangeroot_factunits(self) -> list[FactUnit]:
        return [
            fact
            for fact in self._itemroot.factunits.values()
            if fact.fopen is not None
            and fact.fnigh is not None
            and self._is_item_rangeroot(item_road=fact.base)
        ]

    def set_fact(
        self,
        base: RoadUnit,
        pick: RoadUnit = None,
        fopen: float = None,
        fnigh: float = None,
        create_missing_items: bool = None,
    ):
        pick = base if pick is None else pick
        if create_missing_items:
            self._create_itemkid_if_empty(road=base)
            self._create_itemkid_if_empty(road=pick)

        fact_base_item = self.get_item_obj(base)
        x_itemroot = self.get_item_obj(self._fiscal_id)
        x_fopen = None
        if fnigh is not None and fopen is None:
            x_fopen = x_itemroot.factunits.get(base).fopen
        else:
            x_fopen = fopen
        x_fnigh = None
        if fopen is not None and fnigh is None:
            x_fnigh = x_itemroot.factunits.get(base).fnigh
        else:
            x_fnigh = fnigh
        x_factunit = factunit_shop(base=base, pick=pick, fopen=x_fopen, fnigh=x_fnigh)

        if fact_base_item.is_math() is False:
            x_itemroot.set_factunit(x_factunit)
        # if fact's item no range or is a "range-root" then allow fact to be set
        elif fact_base_item.is_math() and self._is_item_rangeroot(base) is False:
            raise InvalidBudException(
                f"Non range-root fact:{base} can only be set by range-root fact"
            )
        elif fact_base_item.is_math() and self._is_item_rangeroot(base):
            # WHEN item is "range-root" identify any reason.bases that are descendants
            # calculate and set those descendant facts
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendant
            # there exists a reason base "timeline,weeks" with premise.need = "timeline,weeks"
            # and (1,2) divisor=2 (every other week)
            #
            # should not set "timeline,weeks" fact, only "timeline" fact and
            # "timeline,weeks" should be set automatica_lly since there exists a reason
            # that has that base.
            x_itemroot.set_factunit(x_factunit)

    def get_fact(self, base: RoadUnit) -> FactUnit:
        return self._itemroot.factunits.get(base)

    def del_fact(self, base: RoadUnit):
        self._itemroot.del_factunit(base)

    def get_item_dict(self, problem: bool = None) -> dict[RoadUnit, ItemUnit]:
        self.settle_bud()
        if not problem:
            return self._item_dict
        if self._keeps_justified is False:
            exception_str = f"Cannot return problem set because _keeps_justified={self._keeps_justified}."
            raise Exception_keeps_justified(exception_str)

        x_items = self._item_dict.values()
        return {x_item.get_road(): x_item for x_item in x_items if x_item.problem_bool}

    def get_tree_metrics(self) -> TreeMetrics:
        self.settle_bud()
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_node(
            level=self._itemroot._level,
            reasons=self._itemroot.reasonunits,
            awardlinks=self._itemroot.awardlinks,
            uid=self._itemroot._uid,
            pledge=self._itemroot.pledge,
            item_road=self._itemroot.get_road(),
        )

        x_item_list = [self._itemroot]
        while x_item_list != []:
            parent_item = x_item_list.pop()
            for item_kid in parent_item._kids.values():
                self._eval_tree_metrics(
                    parent_item, item_kid, tree_metrics, x_item_list
                )
        return tree_metrics

    def _eval_tree_metrics(self, parent_item, item_kid, tree_metrics, x_item_list):
        item_kid._level = parent_item._level + 1
        tree_metrics.evaluate_node(
            level=item_kid._level,
            reasons=item_kid.reasonunits,
            awardlinks=item_kid.awardlinks,
            uid=item_kid._uid,
            pledge=item_kid.pledge,
            item_road=item_kid.get_road(),
        )
        x_item_list.append(item_kid)

    def get_item_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_item_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        item_uid_max = tree_metrics.uid_max
        item_uid_dict = tree_metrics.uid_dict

        for x_item in self.get_item_dict().values():
            if x_item._uid is None or item_uid_dict.get(x_item._uid) > 1:
                new_item_uid_max = item_uid_max + 1
                self.edit_item_attr(road=x_item.get_road(), uid=new_item_uid_max)
                item_uid_max = new_item_uid_max

    def get_level_count(self, level) -> int:
        tree_metrics = self.get_tree_metrics()
        level_count = None
        try:
            level_count = tree_metrics.level_count[level]
        except KeyError:
            level_count = 0
        return level_count

    def get_reason_bases(self) -> dict[RoadUnit, int]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.reason_bases

    def get_missing_fact_bases(self) -> dict[RoadUnit, int]:
        tree_metrics = self.get_tree_metrics()
        reason_bases = tree_metrics.reason_bases
        missing_bases = {}
        for base, base_count in reason_bases.items():
            try:
                self._itemroot.factunits[base]
            except KeyError:
                missing_bases[base] = base_count
        return missing_bases

    def add_item(
        self, item_road: RoadUnit, mass: float = None, pledge: bool = None
    ) -> ItemUnit:
        x_label = get_terminus_node(item_road, self._road_delimiter)
        x_parent_road = get_parent_road(item_road, self._road_delimiter)
        x_itemunit = itemunit_shop(x_label, mass=mass)
        if pledge:
            x_itemunit.pledge = True
        self.set_item(x_itemunit, x_parent_road)
        return x_itemunit

    def set_l1_item(
        self,
        item_kid: ItemUnit,
        create_missing_items: bool = None,
        get_rid_of_missing_awardlinks_awardee_ids: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.set_item(
            item_kid=item_kid,
            parent_road=self._fiscal_id,
            create_missing_items=create_missing_items,
            get_rid_of_missing_awardlinks_awardee_ids=get_rid_of_missing_awardlinks_awardee_ids,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def set_item(
        self,
        item_kid: ItemUnit,
        parent_road: RoadUnit,
        get_rid_of_missing_awardlinks_awardee_ids: bool = None,
        create_missing_items: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        if RoadNode(item_kid._label).is_node(self._road_delimiter) is False:
            x_str = f"set_item failed because '{item_kid._label}' is not a RoadNode."
            raise InvalidBudException(x_str)

        x_root_node = get_root_node_from_road(parent_road, self._road_delimiter)
        if self._itemroot._label != x_root_node:
            exception_str = f"set_item failed because parent_road '{parent_road}' has an invalid root node"
            raise InvalidBudException(exception_str)

        item_kid._road_delimiter = self._road_delimiter
        if item_kid._bud_fiscal_id != self._fiscal_id:
            item_kid._bud_fiscal_id = self._fiscal_id
        if item_kid._fund_coin != self.fund_coin:
            item_kid._fund_coin = self.fund_coin
        if not get_rid_of_missing_awardlinks_awardee_ids:
            item_kid = self._get_cleaned_awardlinks_item(item_kid)
        item_kid.set_parent_road(parent_road=parent_road)

        # create any missing items
        if not create_missing_ancestors and self.item_exists(parent_road) is False:
            x_str = f"set_item failed because '{parent_road}' item does not exist."
            raise InvalidBudException(x_str)
        parent_road_item = self.get_item_obj(parent_road, create_missing_ancestors)
        if parent_road_item._root is False:
            parent_road_item
        parent_road_item.add_kid(item_kid)

        kid_road = self.make_road(parent_road, item_kid._label)
        if adoptees is not None:
            mass_sum = 0
            for adoptee_label in adoptees:
                adoptee_road = self.make_road(parent_road, adoptee_label)
                adoptee_item = self.get_item_obj(adoptee_road)
                mass_sum += adoptee_item.mass
                new_adoptee_parent_road = self.make_road(kid_road, adoptee_label)
                self.set_item(adoptee_item, new_adoptee_parent_road)
                self.edit_item_attr(new_adoptee_parent_road, mass=adoptee_item.mass)
                self.del_item_obj(adoptee_road)

            if bundling:
                self.edit_item_attr(road=kid_road, mass=mass_sum)

        if create_missing_items:
            self._create_missing_items(road=kid_road)

    def _get_cleaned_awardlinks_item(self, x_item: ItemUnit) -> ItemUnit:
        _awardlinks_to_delete = [
            _awardlink_awardee_id
            for _awardlink_awardee_id in x_item.awardlinks.keys()
            if self.get_acctunit_group_ids_dict().get(_awardlink_awardee_id) is None
        ]
        for _awardlink_awardee_id in _awardlinks_to_delete:
            x_item.awardlinks.pop(_awardlink_awardee_id)

        if x_item.teamunit is not None:
            _teamlinks_to_delete = [
                _teamlink_team_id
                for _teamlink_team_id in x_item.teamunit._teamlinks
                if self.get_acctunit_group_ids_dict().get(_teamlink_team_id) is None
            ]
            for _teamlink_team_id in _teamlinks_to_delete:
                x_item.teamunit.del_teamlink(_teamlink_team_id)
        return x_item

    def _create_missing_items(self, road):
        self._set_item_dict()
        posted_item = self.get_item_obj(road)

        for reason_x in posted_item.reasonunits.values():
            self._create_itemkid_if_empty(road=reason_x.base)
            for premise_x in reason_x.premises.values():
                self._create_itemkid_if_empty(road=premise_x.need)

    def _create_itemkid_if_empty(self, road: RoadUnit):
        if self.item_exists(road) is False:
            self.add_item(road)

    def del_item_obj(self, road: RoadUnit, del_children: bool = True):
        if road == self._itemroot.get_road():
            raise InvalidBudException("Itemroot cannot be deleted")
        parent_road = get_parent_road(road)
        if self.item_exists(road):
            if not del_children:
                self._shift_item_kids(x_road=road)
            parent_item = self.get_item_obj(parent_road)
            parent_item.del_kid(get_terminus_node(road, self._road_delimiter))
        self.settle_bud()

    def _shift_item_kids(self, x_road: RoadUnit):
        parent_road = get_parent_road(x_road)
        d_temp_item = self.get_item_obj(x_road)
        for kid in d_temp_item._kids.values():
            self.set_item(kid, parent_road=parent_road)

    def set_owner_id(self, new_owner_id):
        self._owner_id = new_owner_id

    def edit_item_label(self, old_road: RoadUnit, new_label: RoadNode):
        if self._road_delimiter in new_label:
            exception_str = f"Cannot modify '{old_road}' because new_label {new_label} contains delimiter {self._road_delimiter}"
            raise InvalidLabelException(exception_str)
        if self.item_exists(old_road) is False:
            raise InvalidBudException(f"Item {old_road=} does not exist")

        parent_road = get_parent_road(road=old_road)
        new_road = (
            self.make_road(new_label)
            if parent_road == ""
            else self.make_road(parent_road, new_label)
        )
        if old_road != new_road:
            if parent_road == "":
                self._itemroot.set_label(new_label)
            else:
                self._non_root_item_label_edit(old_road, new_label, parent_road)
            self._itemroot_find_replace_road(old_road=old_road, new_road=new_road)

    def _non_root_item_label_edit(
        self, old_road: RoadUnit, new_label: RoadNode, parent_road: RoadUnit
    ):
        x_item = self.get_item_obj(old_road)
        x_item.set_label(new_label)
        x_item._parent_road = parent_road
        item_parent = self.get_item_obj(get_parent_road(old_road))
        item_parent._kids.pop(get_terminus_node(old_road, self._road_delimiter))
        item_parent._kids[x_item._label] = x_item

    def _itemroot_find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self._itemroot.find_replace_road(old_road=old_road, new_road=new_road)

        item_iter_list = [self._itemroot]
        while item_iter_list != []:
            listed_item = item_iter_list.pop()
            # add all item_children in item list
            if listed_item._kids is not None:
                for item_kid in listed_item._kids.values():
                    item_iter_list.append(item_kid)
                    if is_sub_road(item_kid._parent_road, sub_road=old_road):
                        item_kid._parent_road = rebuild_road(
                            subj_road=item_kid._parent_road,
                            old_road=old_road,
                            new_road=new_road,
                        )
                    item_kid.find_replace_road(old_road=old_road, new_road=new_road)

    def _set_itemattrholder_premise_ranges(self, x_itemattrholder: ItemAttrHolder):
        premise_item = self.get_item_obj(x_itemattrholder.reason_premise)
        x_itemattrholder.set_premise_range_attributes_influenced_by_premise_item(
            premise_open=premise_item.begin,
            premise_nigh=premise_item.close,
            premise_denom=premise_item.denom,
        )

    def edit_reason(
        self,
        road: RoadUnit,
        reason_base: RoadUnit = None,
        reason_premise: RoadUnit = None,
        reason_premise_open: float = None,
        reason_premise_nigh: float = None,
        reason_premise_divisor: int = None,
    ):
        self.edit_item_attr(
            road=road,
            reason_base=reason_base,
            reason_premise=reason_premise,
            reason_premise_open=reason_premise_open,
            reason_premise_nigh=reason_premise_nigh,
            reason_premise_divisor=reason_premise_divisor,
        )

    def edit_item_attr(
        self,
        road: RoadUnit,
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
        awardlink_del: GroupID = None,
        is_expanded: bool = None,
        problem_bool: bool = None,
    ):
        if healerlink is not None:
            for x_healer_id in healerlink._healer_ids:
                if self.get_acctunit_group_ids_dict().get(x_healer_id) is None:
                    exception_str = f"Item cannot edit healerlink because group_id '{x_healer_id}' does not exist as group in Bud"
                    raise healerlink_group_id_Exception(exception_str)

        x_itemattrholder = itemattrholder_shop(
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
            descendant_pledge_count=descendant_pledge_count,
            all_acct_cred=all_acct_cred,
            all_acct_debt=all_acct_debt,
            awardlink=awardlink,
            awardlink_del=awardlink_del,
            is_expanded=is_expanded,
            pledge=pledge,
            factunit=factunit,
            problem_bool=problem_bool,
        )
        if reason_premise is not None:
            self._set_itemattrholder_premise_ranges(x_itemattrholder)
        x_item = self.get_item_obj(road)
        x_item._set_attrs_to_itemunit(item_attr=x_itemattrholder)

    def get_agenda_dict(
        self, necessary_base: RoadUnit = None
    ) -> dict[RoadUnit, ItemUnit]:
        self.settle_bud()
        return {
            x_item.get_road(): x_item
            for x_item in self._item_dict.values()
            if x_item.is_agenda_item(necessary_base)
        }

    def get_all_pledges(self) -> dict[RoadUnit, ItemUnit]:
        self.settle_bud()
        all_items = self._item_dict.values()
        return {x_item.get_road(): x_item for x_item in all_items if x_item.pledge}

    def set_agenda_task_complete(self, task_road: RoadUnit, base: RoadUnit):
        pledge_item = self.get_item_obj(task_road)
        pledge_item.set_factunit_to_complete(self._itemroot.factunits[base])

    def get_credit_ledger_debtit_ledger(
        self,
    ) -> tuple[dict[str:float], dict[str:float]]:
        credit_ledger = {}
        debtit_ledger = {}
        for x_acctunit in self._accts.values():
            credit_ledger[x_acctunit.acct_id] = x_acctunit.credit_belief
            debtit_ledger[x_acctunit.acct_id] = x_acctunit.debtit_belief
        return credit_ledger, debtit_ledger

    def _allot_offtrack_fund(self):
        self._add_to_acctunits_fund_give_take(self._offtrack_fund)

    def get_acctunits_credit_belief_sum(self) -> float:
        return sum(acctunit.get_credit_belief() for acctunit in self._accts.values())

    def get_acctunits_debtit_belief_sum(self) -> float:
        return sum(acctunit.get_debtit_belief() for acctunit in self._accts.values())

    def _add_to_acctunits_fund_give_take(self, item_fund_share: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debtit_ledger()
        fund_give_allot = allot_scale(credor_ledger, item_fund_share, self.fund_coin)
        fund_take_allot = allot_scale(debtor_ledger, item_fund_share, self.fund_coin)
        for x_acct_id, acct_fund_give in fund_give_allot.items():
            self.get_acct(x_acct_id).add_fund_give(acct_fund_give)
        for x_acct_id, acct_fund_take in fund_take_allot.items():
            self.get_acct(x_acct_id).add_fund_take(acct_fund_take)

    def _add_to_acctunits_fund_agenda_give_take(self, item_fund_share: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debtit_ledger()
        fund_give_allot = allot_scale(credor_ledger, item_fund_share, self.fund_coin)
        fund_take_allot = allot_scale(debtor_ledger, item_fund_share, self.fund_coin)
        for x_acct_id, acct_fund_give in fund_give_allot.items():
            self.get_acct(x_acct_id).add_fund_agenda_give(acct_fund_give)
        for x_acct_id, acct_fund_take in fund_take_allot.items():
            self.get_acct(x_acct_id).add_fund_agenda_take(acct_fund_take)

    def _reset_groupboxs_fund_give_take(self):
        for groupbox_obj in self._groupboxs.values():
            groupbox_obj.clear_fund_give_take()

    def _set_groupboxs_fund_share(self, awardheirs: dict[GroupID, AwardLink]):
        for awardlink_obj in awardheirs.values():
            x_awardee_id = awardlink_obj.awardee_id
            if not self.groupbox_exists(x_awardee_id):
                self.set_groupbox(self.create_symmetry_groupbox(x_awardee_id))
            self.add_to_groupbox_fund_give_fund_take(
                group_id=awardlink_obj.awardee_id,
                awardheir_fund_give=awardlink_obj._fund_give,
                awardheir_fund_take=awardlink_obj._fund_take,
            )

    def _allot_fund_bud_agenda(self):
        for item in self._item_dict.values():
            # If there are no awardlines associated with item
            # allot fund_share via general acctunit
            # cred ratio and debt ratio
            # if item.is_agenda_item() and item._awardlines == {}:
            if item.is_agenda_item():
                if item.awardheir_exists():
                    for x_awardline in item._awardlines.values():
                        self.add_to_groupbox_fund_agenda_give_take(
                            group_id=x_awardline.awardee_id,
                            awardline_fund_give=x_awardline._fund_give,
                            awardline_fund_take=x_awardline._fund_take,
                        )
                else:
                    self._add_to_acctunits_fund_agenda_give_take(item.get_fund_share())

    def _allot_groupboxs_fund(self):
        for x_groupbox in self._groupboxs.values():
            x_groupbox._set_membership_fund_give_fund_take()
            for x_membership in x_groupbox._memberships.values():
                self.add_to_acctunit_fund_give_take(
                    acctunit_acct_id=x_membership._acct_id,
                    fund_give=x_membership._fund_give,
                    fund_take=x_membership._fund_take,
                    fund_agenda_give=x_membership._fund_agenda_give,
                    fund_agenda_take=x_membership._fund_agenda_take,
                )

    def _set_acctunits_fund_agenda_ratios(self):
        x_acctunit_credit_belief_sum = self.get_acctunits_credit_belief_sum()
        x_acctunit_debtit_belief_sum = self.get_acctunits_debtit_belief_sum()
        fund_agenda_ratio_give_sum = 0
        fund_agenda_ratio_take_sum = 0
        for x_acctunit in self._accts.values():
            fund_agenda_ratio_give_sum += x_acctunit._fund_agenda_give
            fund_agenda_ratio_take_sum += x_acctunit._fund_agenda_take
        for x_acctunit in self._accts.values():
            x_acctunit.set_fund_agenda_ratio_give_take(
                fund_agenda_ratio_give_sum=fund_agenda_ratio_give_sum,
                fund_agenda_ratio_take_sum=fund_agenda_ratio_take_sum,
                bud_acctunit_total_credit_belief=x_acctunit_credit_belief_sum,
                bud_acctunit_total_debtit_belief=x_acctunit_debtit_belief_sum,
            )

    def _reset_acctunit_fund_give_take(self):
        for acctunit in self._accts.values():
            acctunit.clear_fund_give_take()

    def item_exists(self, road: RoadUnit) -> bool:
        if road is None:
            return False
        root_road_label = get_root_node_from_road(road, delimiter=self._road_delimiter)
        if root_road_label != self._itemroot._label:
            return False

        nodes = get_all_road_nodes(road, delimiter=self._road_delimiter)
        root_road_label = nodes.pop(0)
        if nodes == []:
            return True

        item_label = nodes.pop(0)
        x_item = self._itemroot.get_kid(item_label)
        if x_item is None:
            return False
        while nodes != []:
            item_label = nodes.pop(0)
            x_item = x_item.get_kid(item_label)
            if x_item is None:
                return False
        return True

    def get_item_obj(self, road: RoadUnit, if_missing_create: bool = False) -> ItemUnit:
        if road is None:
            raise InvalidBudException("get_item_obj received road=None")
        if self.item_exists(road) is False and not if_missing_create:
            raise InvalidBudException(f"get_item_obj failed. no item at '{road}'")
        roadnodes = get_all_road_nodes(road, delimiter=self._road_delimiter)
        if len(roadnodes) == 1:
            return self._itemroot

        roadnodes.pop(0)
        item_label = roadnodes.pop(0)
        x_item = self._itemroot.get_kid(item_label, if_missing_create)
        while roadnodes != []:
            x_item = x_item.get_kid(roadnodes.pop(0), if_missing_create)

        return x_item

    def get_item_ranged_kids(
        self, item_road: str, x_gogo_calc: float = None, x_stop_calc: float = None
    ) -> dict[ItemUnit]:
        x_item = self.get_item_obj(item_road)
        return x_item.get_kids_in_range(x_gogo_calc, x_stop_calc)

    def get_inheritor_item_list(
        self, math_road: RoadUnit, inheritor_road: RoadUnit
    ) -> list[ItemUnit]:
        item_roads = all_roadunits_between(math_road, inheritor_road)
        return [self.get_item_obj(x_item_road) for x_item_road in item_roads]

    def _set_item_dict(self):
        item_list = [self.get_item_obj(self._fiscal_id)]
        while item_list != []:
            x_item = item_list.pop()
            x_item.clear_gogo_calc_stop_calc()
            for item_kid in x_item._kids.values():
                item_kid.set_parent_road(x_item.get_road())
                item_kid.set_level(x_item._level)
                item_list.append(item_kid)
            self._item_dict[x_item.get_road()] = x_item
            for x_reason_base in x_item.reasonunits.keys():
                self._reason_bases.add(x_reason_base)

    def _raise_gogo_calc_stop_calc_exception(self, item_road: RoadUnit):
        exception_str = f"Error has occurred, Item '{item_road}' is having _gogo_calc and _stop_calc attributes set twice"
        raise _gogo_calc_stop_calc_Exception(exception_str)

    def _distribute_math_attrs(self, math_item: ItemUnit):
        single_range_item_list = [math_item]
        while single_range_item_list != []:
            r_item = single_range_item_list.pop()
            if r_item._range_evaluated:
                self._raise_gogo_calc_stop_calc_exception(r_item.get_road())
            if r_item.is_math():
                r_item._gogo_calc = r_item.begin
                r_item._stop_calc = r_item.close
            else:
                parent_road = get_parent_road(r_item.get_road())
                parent_item = self.get_item_obj(parent_road)
                r_item._gogo_calc = parent_item._gogo_calc
                r_item._stop_calc = parent_item._stop_calc
                self._range_inheritors[r_item.get_road()] = math_item.get_road()
            r_item._mold_gogo_calc_stop_calc()

            single_range_item_list.extend(iter(r_item._kids.values()))

    def _set_itemtree_range_attrs(self):
        for x_item in self._item_dict.values():
            if x_item.is_math():
                self._distribute_math_attrs(x_item)

            if (
                not x_item.is_kidless()
                and x_item.get_kids_mass_sum() == 0
                and x_item.mass != 0
            ):
                self._offtrack_kids_mass_set.add(x_item.get_road())

    def _set_groupbox_acctunit_funds(self, keep_exceptions):
        for x_item in self._item_dict.values():
            x_item.set_awardheirs_fund_give_fund_take()
            if x_item.is_kidless():
                self._set_ancestors_pledge_fund_keep_attrs(
                    x_item.get_road(), keep_exceptions
                )
                self._allot_fund_share(x_item)

    def _set_ancestors_pledge_fund_keep_attrs(
        self, road: RoadUnit, keep_exceptions: bool = False
    ):
        x_descendant_pledge_count = 0
        child_awardlines = None
        group_everyone = None
        ancestor_roads = get_ancestor_roads(road)
        keep_justified_by_problem = True
        healerlink_count = 0

        while ancestor_roads != []:
            youngest_road = ancestor_roads.pop(0)
            x_item_obj = self.get_item_obj(youngest_road)
            x_item_obj.add_to_descendant_pledge_count(x_descendant_pledge_count)
            if x_item_obj.is_kidless():
                x_item_obj.set_kidless_awardlines()
                child_awardlines = x_item_obj._awardlines
            else:
                x_item_obj.set_awardlines(child_awardlines)

            if x_item_obj._task:
                x_descendant_pledge_count += 1

            if (
                group_everyone != False
                and x_item_obj._all_acct_cred != False
                and x_item_obj._all_acct_debt != False
                and x_item_obj._awardheirs != {}
            ) or (
                group_everyone != False
                and x_item_obj._all_acct_cred is False
                and x_item_obj._all_acct_debt is False
            ):
                group_everyone = False
            elif group_everyone != False:
                group_everyone = True
            x_item_obj._all_acct_cred = group_everyone
            x_item_obj._all_acct_debt = group_everyone

            if x_item_obj.healerlink.any_healer_id_exists():
                keep_justified_by_problem = False
                healerlink_count += 1
                self._sum_healerlink_share += x_item_obj.get_fund_share()
            if x_item_obj.problem_bool:
                keep_justified_by_problem = True

        if keep_justified_by_problem is False or healerlink_count > 1:
            if keep_exceptions:
                exception_str = f"ItemUnit '{road}' cannot sponsor ancestor keeps."
                raise Exception_keeps_justified(exception_str)
            self._keeps_justified = False

    def _clear_itemtree_fund_and_active_status_attrs(self):
        for x_item in self._item_dict.values():
            x_item.clear_awardlines()
            x_item.clear_descendant_pledge_count()
            x_item.clear_all_acct_cred_debt()

    def _set_kids_active_status_attrs(self, x_item: ItemUnit, parent_item: ItemUnit):
        x_item.set_reasonheirs(self._item_dict, parent_item._reasonheirs)
        x_item.set_range_factheirs(self._item_dict, self._range_inheritors)
        tt_count = self._tree_traverse_count
        x_item.set_active_attrs(tt_count, self._groupboxs, self._owner_id)

    def _allot_fund_share(self, item: ItemUnit):
        if item.awardheir_exists():
            self._set_groupboxs_fund_share(item._awardheirs)
        elif item.awardheir_exists() is False:
            self._add_to_acctunits_fund_give_take(item.get_fund_share())

    def _create_groupboxs_metrics(self):
        self._groupboxs = {}
        for group_id, acct_id_set in self.get_acctunit_group_ids_dict().items():
            x_groupbox = groupbox_shop(group_id, _road_delimiter=self._road_delimiter)
            for x_acct_id in acct_id_set:
                x_membership = self.get_acct(x_acct_id).get_membership(group_id)
                x_groupbox.set_membership(x_membership)
                self.set_groupbox(x_groupbox)

    def _set_acctunit_groupbox_respect_ledgers(self):
        self.credor_respect = validate_respect_num(self.credor_respect)
        self.debtor_respect = validate_respect_num(self.debtor_respect)
        credor_ledger, debtor_ledger = self.get_credit_ledger_debtit_ledger()
        credor_allot = allot_scale(credor_ledger, self.credor_respect, self.respect_bit)
        debtor_allot = allot_scale(debtor_ledger, self.debtor_respect, self.respect_bit)
        for x_acct_id, acct_credor_pool in credor_allot.items():
            self.get_acct(x_acct_id).set_credor_pool(acct_credor_pool)
        for x_acct_id, acct_debtor_pool in debtor_allot.items():
            self.get_acct(x_acct_id).set_debtor_pool(acct_debtor_pool)
        self._create_groupboxs_metrics()
        self._reset_acctunit_fund_give_take()

    def _clear_item_dict_and_bud_obj_settle_attrs(self):
        self._item_dict = {self._itemroot.get_road(): self._itemroot}
        self._rational = False
        self._tree_traverse_count = 0
        self._offtrack_kids_mass_set = set()
        self._reason_bases = set()
        self._range_inheritors = {}
        self._keeps_justified = True
        self._keeps_buildable = False
        self._sum_healerlink_share = 0
        self._keep_dict = {}
        self._healers_dict = {}

    def _set_itemtree_factheirs_teamheirs_awardheirs(self):
        for x_item in get_sorted_item_list(list(self._item_dict.values())):
            if x_item._root:
                x_item.set_factheirs(x_item.factunits)
                x_item.set_itemroot_inherit_reasonheirs()
                x_item.set_teamheir(None, self._groupboxs)
                x_item.inherit_awardheirs()
            else:
                parent_item = self.get_item_obj(x_item._parent_road)
                x_item.set_factheirs(parent_item._factheirs)
                x_item.set_teamheir(parent_item._teamheir, self._groupboxs)
                x_item.inherit_awardheirs(parent_item._awardheirs)
            x_item.set_awardheirs_fund_give_fund_take()

    def settle_bud(self, keep_exceptions: bool = False):
        self._clear_item_dict_and_bud_obj_settle_attrs()
        self._set_item_dict()
        self._set_itemtree_range_attrs()
        self._set_acctunit_groupbox_respect_ledgers()
        self._clear_acctunit_fund_attrs()
        self._clear_itemtree_fund_and_active_status_attrs()
        self._set_itemtree_factheirs_teamheirs_awardheirs()

        max_count = self.max_tree_traverse
        while not self._rational and self._tree_traverse_count < max_count:
            self._set_itemtree_active_status_attrs()
            self._set_rational_attr()
            self._tree_traverse_count += 1

        self._set_itemtree_fund_attrs(self._itemroot)
        self._set_groupbox_acctunit_funds(keep_exceptions)
        self._set_acctunit_fund_related_attrs()
        self._set_bud_keep_attrs()

    def _set_itemtree_active_status_attrs(self):
        for x_item in get_sorted_item_list(list(self._item_dict.values())):
            if x_item._root:
                tt_count = self._tree_traverse_count
                root_item = self._itemroot
                root_item.set_active_attrs(tt_count, self._groupboxs, self._owner_id)
            else:
                parent_item = self.get_item_obj(x_item._parent_road)
                self._set_kids_active_status_attrs(x_item, parent_item)

    def _set_itemtree_fund_attrs(self, root_item: ItemUnit):
        root_item.set_fund_attr(0, self.fund_pool, self.fund_pool)
        # no function recursion, recursion by iterateing over list that can be added to by iterations
        cache_item_list = [root_item]
        while cache_item_list != []:
            parent_item = cache_item_list.pop()
            kids_items = parent_item._kids.items()
            x_ledger = {x_road: item_kid.mass for x_road, item_kid in kids_items}
            parent_fund_num = parent_item._fund_cease - parent_item._fund_onset
            alloted_fund_num = allot_scale(x_ledger, parent_fund_num, self.fund_coin)

            fund_onset = None
            fund_cease = None
            for x_item in parent_item._kids.values():
                if fund_onset is None:
                    fund_onset = parent_item._fund_onset
                    fund_cease = fund_onset + alloted_fund_num.get(x_item._label)
                else:
                    fund_onset = fund_cease
                    fund_cease += alloted_fund_num.get(x_item._label)
                x_item.set_fund_attr(fund_onset, fund_cease, self.fund_pool)
                cache_item_list.append(x_item)

    def _set_rational_attr(self):
        any_item_active_status_has_altered = False
        for item in self._item_dict.values():
            if item._active_hx.get(self._tree_traverse_count) is not None:
                any_item_active_status_has_altered = True

        if any_item_active_status_has_altered is False:
            self._rational = True

    def _set_acctunit_fund_related_attrs(self):
        self.set_offtrack_fund()
        self._allot_offtrack_fund()
        self._allot_fund_bud_agenda()
        self._allot_groupboxs_fund()
        self._set_acctunits_fund_agenda_ratios()

    def _set_bud_keep_attrs(self):
        self._set_keep_dict()
        self._healers_dict = self._get_healers_dict()
        self._keeps_buildable = self._get_buildable_keeps()

    def _set_keep_dict(self):
        if self._keeps_justified is False:
            self._sum_healerlink_share = 0
        for x_item in self._item_dict.values():
            if self._sum_healerlink_share == 0:
                x_item._healerlink_ratio = 0
            else:
                x_sum = self._sum_healerlink_share
                x_item._healerlink_ratio = x_item.get_fund_share() / x_sum
            if self._keeps_justified and x_item.healerlink.any_healer_id_exists():
                self._keep_dict[x_item.get_road()] = x_item

    def _get_healers_dict(self) -> dict[HealerID, dict[RoadUnit, ItemUnit]]:
        _healers_dict = {}
        for x_keep_road, x_keep_item in self._keep_dict.items():
            for x_healer_id in x_keep_item.healerlink._healer_ids:
                x_groupbox = self.get_groupbox(x_healer_id)
                for x_acct_id in x_groupbox._memberships.keys():
                    if _healers_dict.get(x_acct_id) is None:
                        _healers_dict[x_acct_id] = {x_keep_road: x_keep_item}
                    else:
                        healer_dict = _healers_dict.get(x_acct_id)
                        healer_dict[x_keep_road] = x_keep_item
        return _healers_dict

    def _get_buildable_keeps(self) -> bool:
        return all(
            roadunit_valid_dir_path(keep_road, self._road_delimiter) != False
            for keep_road in self._keep_dict.keys()
        )

    def _clear_acctunit_fund_attrs(self):
        self._reset_groupboxs_fund_give_take()
        self._reset_acctunit_fund_give_take()

    def get_item_tree_ordered_road_list(
        self, no_range_descendants: bool = False
    ) -> list[RoadUnit]:
        item_list = list(self.get_item_dict().values())
        node_dict = {item.get_road().lower(): item.get_road() for item in item_list}
        node_lowercase_ordered_list = sorted(list(node_dict))
        node_orginalcase_ordered_list = [
            node_dict[node_l] for node_l in node_lowercase_ordered_list
        ]

        list_x = []
        for road in node_orginalcase_ordered_list:
            if not no_range_descendants:
                list_x.append(road)
            else:
                anc_list = get_ancestor_roads(road=road)
                if len(anc_list) == 1:
                    list_x.append(road)
                elif len(anc_list) == 2:
                    if self._itemroot.begin is None and self._itemroot.close is None:
                        list_x.append(road)
                else:
                    parent_item = self.get_item_obj(road=anc_list[1])
                    if parent_item.begin is None and parent_item.close is None:
                        list_x.append(road)

        return list_x

    def get_factunits_dict(self) -> dict[str, str]:
        x_dict = {}
        if self._itemroot.factunits is not None:
            for fact_road, fact_obj in self._itemroot.factunits.items():
                x_dict[fact_road] = fact_obj.get_dict()
        return x_dict

    def get_acctunits_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {}
        if self._accts is not None:
            for acct_id, acct_obj in self._accts.items():
                x_dict[acct_id] = acct_obj.get_dict(all_attrs)
        return x_dict

    def get_dict(self) -> dict[str, str]:
        x_dict = {
            "_accts": self.get_acctunits_dict(),
            "_originunit": self._originunit.get_dict(),
            "tally": self.tally,
            "fund_pool": self.fund_pool,
            "fund_coin": self.fund_coin,
            "respect_bit": self.respect_bit,
            "penny": self.penny,
            "_owner_id": self._owner_id,
            "_fiscal_id": self._fiscal_id,
            "max_tree_traverse": self.max_tree_traverse,
            "_road_delimiter": self._road_delimiter,
            "_itemroot": self._itemroot.get_dict(),
        }
        if self.credor_respect is not None:
            x_dict["credor_respect"] = self.credor_respect
        if self.debtor_respect is not None:
            x_dict["debtor_respect"] = self.debtor_respect
        if self._last_gift_id is not None:
            x_dict["_last_gift_id"] = self._last_gift_id

        return x_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())

    def set_dominate_pledge_item(self, item_kid: ItemUnit):
        item_kid.pledge = True
        self.set_item(
            item_kid=item_kid,
            parent_road=self.make_road(item_kid._parent_road),
            get_rid_of_missing_awardlinks_awardee_ids=True,
            create_missing_items=True,
        )

    def set_offtrack_fund(self) -> float:
        mass_set = self._offtrack_kids_mass_set
        self._offtrack_fund = sum(
            self.get_item_obj(x_roadunit).get_fund_share() for x_roadunit in mass_set
        )


def budunit_shop(
    _owner_id: OwnerID = None,
    _fiscal_id: FiscalID = None,
    _road_delimiter: str = None,
    fund_pool: FundNum = None,
    fund_coin: FundCoin = None,
    respect_bit: BitNum = None,
    penny: PennyNum = None,
    tally: float = None,
) -> BudUnit:
    _owner_id = "" if _owner_id is None else _owner_id
    _fiscal_id = get_default_fiscal_id_roadnode() if _fiscal_id is None else _fiscal_id
    x_bud = BudUnit(
        _owner_id=_owner_id,
        tally=get_1_if_None(tally),
        _fiscal_id=_fiscal_id,
        _accts=get_empty_dict_if_none(None),
        _groupboxs={},
        _item_dict=get_empty_dict_if_none(None),
        _keep_dict=get_empty_dict_if_none(None),
        _healers_dict=get_empty_dict_if_none(None),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        credor_respect=validate_respect_num(),
        debtor_respect=validate_respect_num(),
        fund_pool=validate_fund_pool(fund_pool),
        fund_coin=default_fund_coin_if_none(fund_coin),
        respect_bit=default_respect_bit_if_none(respect_bit),
        penny=default_penny_if_none(penny),
        _keeps_justified=get_False_if_None(),
        _keeps_buildable=get_False_if_None(),
        _sum_healerlink_share=get_0_if_None(),
        _offtrack_kids_mass_set=set(),
        _reason_bases=set(),
        _range_inheritors={},
    )
    x_bud._itemroot = itemunit_shop(
        _root=True,
        _uid=1,
        _level=0,
        _bud_fiscal_id=x_bud._fiscal_id,
        _road_delimiter=x_bud._road_delimiter,
        _fund_coin=x_bud.fund_coin,
        _parent_road="",
    )
    x_bud.set_max_tree_traverse(3)
    x_bud._rational = False
    x_bud._originunit = originunit_shop()
    return x_bud


def get_from_json(x_bud_json: str) -> BudUnit:
    return get_from_dict(get_dict_from_json(x_bud_json))


def get_from_dict(bud_dict: dict) -> BudUnit:
    x_bud = budunit_shop()
    x_bud.set_owner_id(obj_from_bud_dict(bud_dict, "_owner_id"))
    x_bud.tally = obj_from_bud_dict(bud_dict, "tally")
    x_bud.set_max_tree_traverse(obj_from_bud_dict(bud_dict, "max_tree_traverse"))
    x_bud._fiscal_id = obj_from_bud_dict(bud_dict, "_fiscal_id")
    x_bud._itemroot._label = obj_from_bud_dict(bud_dict, "_fiscal_id")
    bud_road_delimiter = obj_from_bud_dict(bud_dict, "_road_delimiter")
    x_bud._road_delimiter = default_road_delimiter_if_none(bud_road_delimiter)
    x_bud.fund_pool = validate_fund_pool(obj_from_bud_dict(bud_dict, "fund_pool"))
    x_bud.fund_coin = default_fund_coin_if_none(
        obj_from_bud_dict(bud_dict, "fund_coin")
    )
    x_bud.respect_bit = default_respect_bit_if_none(
        obj_from_bud_dict(bud_dict, "respect_bit")
    )
    x_bud.penny = default_penny_if_none(obj_from_bud_dict(bud_dict, "penny"))
    x_bud.credor_respect = obj_from_bud_dict(bud_dict, "credor_respect")
    x_bud.debtor_respect = obj_from_bud_dict(bud_dict, "debtor_respect")
    x_bud._last_gift_id = obj_from_bud_dict(bud_dict, "_last_gift_id")
    x_road_delimiter = x_bud._road_delimiter
    x_accts = obj_from_bud_dict(bud_dict, "_accts", x_road_delimiter).values()
    for x_acctunit in x_accts:
        x_bud.set_acctunit(x_acctunit)
    x_bud._originunit = obj_from_bud_dict(bud_dict, "_originunit")
    create_itemroot_from_bud_dict(x_bud, bud_dict)
    return x_bud


def create_itemroot_from_bud_dict(x_bud: BudUnit, bud_dict: dict):
    itemroot_dict = bud_dict.get("_itemroot")
    x_bud._itemroot = itemunit_shop(
        _root=True,
        _label=x_bud._fiscal_id,
        _parent_road="",
        _level=0,
        _uid=get_obj_from_item_dict(itemroot_dict, "_uid"),
        mass=get_obj_from_item_dict(itemroot_dict, "mass"),
        begin=get_obj_from_item_dict(itemroot_dict, "begin"),
        close=get_obj_from_item_dict(itemroot_dict, "close"),
        numor=get_obj_from_item_dict(itemroot_dict, "numor"),
        denom=get_obj_from_item_dict(itemroot_dict, "denom"),
        morph=get_obj_from_item_dict(itemroot_dict, "morph"),
        gogo_want=get_obj_from_item_dict(itemroot_dict, "gogo_want"),
        stop_want=get_obj_from_item_dict(itemroot_dict, "stop_want"),
        problem_bool=get_obj_from_item_dict(itemroot_dict, "problem_bool"),
        reasonunits=get_obj_from_item_dict(itemroot_dict, "reasonunits"),
        teamunit=get_obj_from_item_dict(itemroot_dict, "teamunit"),
        healerlink=get_obj_from_item_dict(itemroot_dict, "healerlink"),
        factunits=get_obj_from_item_dict(itemroot_dict, "factunits"),
        awardlinks=get_obj_from_item_dict(itemroot_dict, "awardlinks"),
        _is_expanded=get_obj_from_item_dict(itemroot_dict, "_is_expanded"),
        _road_delimiter=get_obj_from_item_dict(itemroot_dict, "_road_delimiter"),
        _bud_fiscal_id=x_bud._fiscal_id,
        _fund_coin=default_fund_coin_if_none(x_bud.fund_coin),
    )
    create_itemroot_kids_from_dict(x_bud, itemroot_dict)


def create_itemroot_kids_from_dict(x_bud: BudUnit, itemroot_dict: dict):
    to_evaluate_item_dicts = []
    parent_road_str = "parent_road"
    # for every kid dict, set parent_road in dict, add to to_evaluate_list
    for x_dict in get_obj_from_item_dict(itemroot_dict, "_kids").values():
        x_dict[parent_road_str] = x_bud._fiscal_id
        to_evaluate_item_dicts.append(x_dict)

    while to_evaluate_item_dicts != []:
        item_dict = to_evaluate_item_dicts.pop(0)
        # for every kid dict, set parent_road in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_item_dict(item_dict, "_kids").values():
            parent_road = get_obj_from_item_dict(item_dict, parent_road_str)
            kid_label = get_obj_from_item_dict(item_dict, "_label")
            kid_dict[parent_road_str] = x_bud.make_road(parent_road, kid_label)
            to_evaluate_item_dicts.append(kid_dict)
        x_itemkid = itemunit_shop(
            _label=get_obj_from_item_dict(item_dict, "_label"),
            mass=get_obj_from_item_dict(item_dict, "mass"),
            _uid=get_obj_from_item_dict(item_dict, "_uid"),
            begin=get_obj_from_item_dict(item_dict, "begin"),
            close=get_obj_from_item_dict(item_dict, "close"),
            numor=get_obj_from_item_dict(item_dict, "numor"),
            denom=get_obj_from_item_dict(item_dict, "denom"),
            morph=get_obj_from_item_dict(item_dict, "morph"),
            gogo_want=get_obj_from_item_dict(item_dict, "gogo_want"),
            stop_want=get_obj_from_item_dict(item_dict, "stop_want"),
            pledge=get_obj_from_item_dict(item_dict, "pledge"),
            problem_bool=get_obj_from_item_dict(item_dict, "problem_bool"),
            reasonunits=get_obj_from_item_dict(item_dict, "reasonunits"),
            teamunit=get_obj_from_item_dict(item_dict, "teamunit"),
            healerlink=get_obj_from_item_dict(item_dict, "healerlink"),
            _originunit=get_obj_from_item_dict(item_dict, "_originunit"),
            awardlinks=get_obj_from_item_dict(item_dict, "awardlinks"),
            factunits=get_obj_from_item_dict(item_dict, "factunits"),
            _is_expanded=get_obj_from_item_dict(item_dict, "_is_expanded"),
        )
        x_bud.set_item(x_itemkid, parent_road=item_dict[parent_road_str])


def obj_from_bud_dict(
    x_dict: dict[str, dict], dict_key: str, _road_delimiter: str = None
) -> any:
    if dict_key == "_originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else originunit_shop()
        )
    elif dict_key == "_accts":
        return acctunits_get_from_dict(x_dict[dict_key], _road_delimiter)
    elif dict_key == "_max_tree_traverse":
        return (
            x_dict[dict_key]
            if x_dict.get(dict_key) is not None
            else max_tree_traverse_default()
        )
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else None


def get_dict_of_bud_from_dict(x_dict: dict[str, dict]) -> dict[str, BudUnit]:
    budunits = {}
    for budunit_dict in x_dict.values():
        x_bud = get_from_dict(bud_dict=budunit_dict)
        budunits[x_bud._owner_id] = x_bud
    return budunits


def get_sorted_item_list(x_list: list[ItemUnit]) -> list[ItemUnit]:
    x_list.sort(key=lambda x: x.get_road(), reverse=False)
    return x_list
