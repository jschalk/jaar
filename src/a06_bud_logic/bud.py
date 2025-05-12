from src.a00_data_toolbox.dict_toolbox import (
    get_json_from_dict,
    get_dict_from_json,
    get_1_if_None,
    get_0_if_None,
    get_False_if_None,
    get_empty_dict_if_None,
)
from src.a01_way_logic.way import (
    get_parent_way,
    to_way,
    is_sub_way,
    all_waystrs_between,
    rebuild_way,
    get_terminus_tag,
    get_root_tag_from_way,
    get_ancestor_ways,
    get_default_fisc_tag,
    get_all_way_tags,
    get_forefather_ways,
    create_way,
    default_bridge_if_None,
    TagStr,
    WayStr,
    is_string_in_way,
    OwnerName,
    AcctName,
    HealerName,
    FiscTag,
    waystr_valid_dir_path,
)
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import (
    valid_finance_ratio,
    default_respect_bit_if_None,
    filter_penny,
    default_fund_coin_if_None,
    validate_fund_pool,
    BitNum,
    RespectNum,
    PennyNum,
    FundCoin,
    FundNum,
    validate_respect_num,
)
from src.a03_group_logic.acct import AcctUnit, acctunits_get_from_dict, acctunit_shop
from src.a03_group_logic.group import (
    AwardLink,
    GroupLabel,
    GroupUnit,
    groupunit_shop,
    membership_shop,
)
from src.a04_reason_logic.reason_idea import (
    FactUnit,
    FactUnit,
    ReasonUnit,
    WayStr,
    factunit_shop,
)
from src.a04_reason_logic.reason_team import TeamUnit
from src.a05_idea_logic.healer import HealerLink
from src.a05_idea_logic.idea import (
    IdeaUnit,
    ideaunit_shop,
    ideaattrholder_shop,
    IdeaAttrHolder,
    get_obj_from_idea_dict,
)
from src.a05_idea_logic.origin import (
    originunit_get_from_dict,
    originunit_shop,
    OriginUnit,
)
from src.a06_bud_logic.bud_config import max_tree_traverse_default
from src.a06_bud_logic.tree_metrics import TreeMetrics, treemetrics_shop
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class InvalidBudException(Exception):
    pass


class InvalidTagException(Exception):
    pass


class NewBridgeException(Exception):
    pass


class AcctUnitsCredorDebtorSumException(Exception):
    pass


class AcctMissingException(Exception):
    pass


class Exception_keeps_justified(Exception):
    pass


class _bit_RatioException(Exception):
    pass


class _last_pack_idException(Exception):
    pass


class healerlink_group_label_Exception(Exception):
    pass


class _gogo_calc_stop_calc_Exception(Exception):
    pass


@dataclass
class BudUnit:
    fisc_tag: FiscTag = None
    owner_name: OwnerName = None
    accts: dict[AcctName, AcctUnit] = None
    idearoot: IdeaUnit = None
    tally: float = None
    fund_pool: FundNum = None
    fund_coin: FundCoin = None
    penny: PennyNum = None
    credor_respect: RespectNum = None
    debtor_respect: RespectNum = None
    respect_bit: BitNum = None
    bridge: str = None
    max_tree_traverse: int = None
    last_pack_id: int = None
    originunit: OriginUnit = None  # In plan buds this shows source
    # settle_bud Calculated field begin
    _idea_dict: dict[WayStr, IdeaUnit] = None
    _keep_dict: dict[WayStr, IdeaUnit] = None
    _healers_dict: dict[HealerName, dict[WayStr, IdeaUnit]] = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _keeps_justified: bool = None
    _keeps_buildable: bool = None
    _sum_healerlink_share: float = None
    _groupunits: dict[GroupLabel, GroupUnit] = None
    _offtrack_kids_mass_set: set[WayStr] = None
    _offtrack_fund: float = None
    _reason_rcontexts: set[WayStr] = None
    _range_inheritors: dict[WayStr, WayStr] = None
    # settle_bud Calculated field end

    def del_last_pack_id(self):
        self.last_pack_id = None

    def set_last_pack_id(self, x_last_pack_id: int):
        if self.last_pack_id is not None and x_last_pack_id < self.last_pack_id:
            exception_str = f"Cannot set _last_pack_id to {x_last_pack_id} because it is less than {self.last_pack_id}."
            raise _last_pack_idException(exception_str)
        self.last_pack_id = x_last_pack_id

    def set_fund_pool(self, x_fund_pool):
        if valid_finance_ratio(x_fund_pool, self.fund_coin) is False:
            exception_str = f"Bud '{self.owner_name}' cannot set fund_pool='{x_fund_pool}'. It is not divisible by fund_coin '{self.fund_coin}'"
            raise _bit_RatioException(exception_str)

        self.fund_pool = validate_fund_pool(x_fund_pool)

    def set_acct_respect(self, x_acct_pool: int):
        self.set_credor_respect(x_acct_pool)
        self.set_debtor_respect(x_acct_pool)
        self.set_fund_pool(x_acct_pool)

    def set_credor_respect(self, new_credor_respect: int):
        if valid_finance_ratio(new_credor_respect, self.respect_bit) is False:
            exception_str = f"Bud '{self.owner_name}' cannot set credor_respect='{new_credor_respect}'. It is not divisible by bit '{self.respect_bit}'"
            raise _bit_RatioException(exception_str)
        self.credor_respect = new_credor_respect

    def set_debtor_respect(self, new_debtor_respect: int):
        if valid_finance_ratio(new_debtor_respect, self.respect_bit) is False:
            exception_str = f"Bud '{self.owner_name}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible by bit '{self.respect_bit}'"
            raise _bit_RatioException(exception_str)
        self.debtor_respect = new_debtor_respect

    def make_way(
        self,
        parent_way: WayStr = None,
        terminus_tag: TagStr = None,
    ) -> WayStr:
        return create_way(
            parent_way=parent_way,
            terminus_tag=terminus_tag,
            bridge=self.bridge,
        )

    def make_l1_way(self, l1_tag: TagStr):
        return self.make_way(self.fisc_tag, l1_tag)

    def set_bridge(self, new_bridge: str):
        self.settle_bud()
        if self.bridge != new_bridge:
            for x_idea_way in self._idea_dict.keys():
                if is_string_in_way(new_bridge, x_idea_way):
                    exception_str = f"Cannot modify bridge to '{new_bridge}' because it exists an idea idea_tag '{x_idea_way}'"
                    raise NewBridgeException(exception_str)

            # modify all way attributes in ideaunits
            self.bridge = default_bridge_if_None(new_bridge)
            for x_idea in self._idea_dict.values():
                x_idea.set_bridge(self.bridge)

    def set_fisc_tag(self, fisc_tag: str):
        old_fisc_tag = copy_deepcopy(self.fisc_tag)
        self.settle_bud()
        for idea_obj in self._idea_dict.values():
            idea_obj.fisc_tag = fisc_tag
        self.fisc_tag = fisc_tag
        self.edit_idea_tag(old_way=to_way(old_fisc_tag), new_idea_tag=self.fisc_tag)
        self.settle_bud()

    def set_max_tree_traverse(self, x_int: int):
        if x_int < 2 or not float(x_int).is_integer():
            raise InvalidBudException(
                f"set_max_tree_traverse: '{x_int}' must be number that is 2 or greater"
            )
        else:
            self.max_tree_traverse = x_int

    def _get_relevant_ways(self, ways: dict[WayStr,]) -> set[WayStr]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for x_way in ways:
            to_evaluate_list.append(x_way)
            to_evaluate_hx_dict[x_way] = "to_evaluate"
        evaluated_ways = set()

        # while ways_to_evaluate != [] and count_x <= tree_metrics.tag_count:
        # Why count_x? because count_x might be wrong attr to measure
        # nice to avoid infinite loops from programming errors though...
        while to_evaluate_list != []:
            x_way = to_evaluate_list.pop()
            x_idea = self.get_idea_obj(x_way)
            for reasonunit_obj in x_idea.reasonunits.values():
                reason_rcontext = reasonunit_obj.rcontext
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_way=reason_rcontext,
                    way_type="reasonunit_rcontext",
                )
            forefather_ways = get_forefather_ways(x_way)
            for forefather_way in forefather_ways:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_way=forefather_way,
                    way_type="forefather",
                )

            evaluated_ways.add(x_way)
        return evaluated_ways

    def _evaluate_relevancy(
        self,
        to_evaluate_list: list[WayStr],
        to_evaluate_hx_dict: dict[WayStr, int],
        to_evaluate_way: WayStr,
        way_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_way) is None:
            to_evaluate_list.append(to_evaluate_way)
            to_evaluate_hx_dict[to_evaluate_way] = way_type

            if way_type == "reasonunit_rcontext":
                ru_rcontext_idea = self.get_idea_obj(to_evaluate_way)
                for descendant_way in ru_rcontext_idea.get_descendant_ways_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_way=descendant_way,
                        way_type="reasonunit_descendant",
                    )

    def all_ideas_relevant_to_pledge_idea(self, way: WayStr) -> bool:
        pledge_idea_assoc_set = set(self._get_relevant_ways({way}))
        all_ideas_set = set(self.get_idea_tree_ordered_way_list())
        return all_ideas_set == all_ideas_set.intersection(pledge_idea_assoc_set)

    def get_awardlinks_metrics(self) -> dict[GroupLabel, AwardLink]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.awardlinks_metrics

    def add_to_groupunit_fund_give_fund_take(
        self,
        group_label: GroupLabel,
        awardheir_fund_give: float,
        awardheir_fund_take: float,
    ):
        x_groupunit = self.get_groupunit(group_label)
        if x_groupunit is not None:
            x_groupunit._fund_give += awardheir_fund_give
            x_groupunit._fund_take += awardheir_fund_take

    def add_to_groupunit_fund_agenda_give_take(
        self,
        group_label: GroupLabel,
        awardline_fund_give: float,
        awardline_fund_take: float,
    ):
        x_groupunit = self.get_groupunit(group_label)
        if awardline_fund_give is not None and awardline_fund_take is not None:
            x_groupunit._fund_agenda_give += awardline_fund_give
            x_groupunit._fund_agenda_take += awardline_fund_take

    def add_to_acctunit_fund_give_take(
        self,
        acctunit_acct_name: AcctName,
        fund_give,
        fund_take: float,
        fund_agenda_give: float,
        fund_agenda_take: float,
    ):
        x_acctunit = self.get_acct(acctunit_acct_name)
        x_acctunit.add_fund_give_take(
            fund_give=fund_give,
            fund_take=fund_take,
            fund_agenda_give=fund_agenda_give,
            fund_agenda_take=fund_agenda_take,
        )

    def del_acctunit(self, acct_name: str):
        self.accts.pop(acct_name)

    def add_acctunit(
        self, acct_name: AcctName, credit_belief: int = None, debtit_belief: int = None
    ):
        x_bridge = self.bridge
        acctunit = acctunit_shop(acct_name, credit_belief, debtit_belief, x_bridge)
        self.set_acctunit(acctunit)

    def set_acctunit(self, x_acctunit: AcctUnit, auto_set_membership: bool = True):
        if x_acctunit.bridge != self.bridge:
            x_acctunit.bridge = self.bridge
        if x_acctunit._respect_bit != self.respect_bit:
            x_acctunit._respect_bit = self.respect_bit
        if auto_set_membership and x_acctunit.memberships_exist() is False:
            x_acctunit.add_membership(x_acctunit.acct_name)
        self.accts[x_acctunit.acct_name] = x_acctunit

    def acct_exists(self, acct_name: AcctName) -> bool:
        return self.get_acct(acct_name) is not None

    def edit_acctunit(
        self, acct_name: AcctName, credit_belief: int = None, debtit_belief: int = None
    ):
        if self.accts.get(acct_name) is None:
            raise AcctMissingException(f"AcctUnit '{acct_name}' does not exist.")
        x_acctunit = self.get_acct(acct_name)
        if credit_belief is not None:
            x_acctunit.set_credit_belief(credit_belief)
        if debtit_belief is not None:
            x_acctunit.set_debtit_belief(debtit_belief)
        self.set_acctunit(x_acctunit)

    def clear_acctunits_memberships(self):
        for x_acctunit in self.accts.values():
            x_acctunit.clear_memberships()

    def get_acct(self, acct_name: AcctName) -> AcctUnit:
        return self.accts.get(acct_name)

    def get_acctunit_group_labels_dict(self) -> dict[GroupLabel, set[AcctName]]:
        x_dict = {}
        for x_acctunit in self.accts.values():
            for x_group_label in x_acctunit._memberships.keys():
                acct_name_set = x_dict.get(x_group_label)
                if acct_name_set is None:
                    x_dict[x_group_label] = {x_acctunit.acct_name}
                else:
                    acct_name_set.add(x_acctunit.acct_name)
                    x_dict[x_group_label] = acct_name_set
        return x_dict

    def set_groupunit(self, x_groupunit: GroupUnit):
        x_groupunit.fund_coin = self.fund_coin
        self._groupunits[x_groupunit.group_label] = x_groupunit

    def groupunit_exists(self, group_label: GroupLabel) -> bool:
        return self._groupunits.get(group_label) is not None

    def get_groupunit(self, x_group_label: GroupLabel) -> GroupUnit:
        return self._groupunits.get(x_group_label)

    def create_symmetry_groupunit(self, x_group_label: GroupLabel) -> GroupUnit:
        x_groupunit = groupunit_shop(x_group_label)
        for x_acctunit in self.accts.values():
            x_membership = membership_shop(
                group_label=x_group_label,
                credit_vote=x_acctunit.credit_belief,
                debtit_vote=x_acctunit.debtit_belief,
                acct_name=x_acctunit.acct_name,
            )
            x_groupunit.set_membership(x_membership)
        return x_groupunit

    def get_tree_traverse_generated_groupunits(self) -> set[GroupLabel]:
        x_acctunit_group_labels = set(self.get_acctunit_group_labels_dict().keys())
        all_group_labels = set(self._groupunits.keys())
        return all_group_labels.difference(x_acctunit_group_labels)

    def _is_idea_rangeroot(self, idea_way: WayStr) -> bool:
        if self.fisc_tag == idea_way:
            raise InvalidBudException(
                "its difficult to foresee a scenario where idearoot is rangeroot"
            )
        parent_way = get_parent_way(idea_way)
        parent_idea = self.get_idea_obj(parent_way)
        return not parent_idea.is_math()

    def _get_rangeroot_factunits(self) -> list[FactUnit]:
        return [
            fact
            for fact in self.idearoot.factunits.values()
            if fact.fopen is not None
            and fact.fnigh is not None
            and self._is_idea_rangeroot(idea_way=fact.fcontext)
        ]

    def add_fact(
        self,
        fcontext: WayStr,
        fbranch: WayStr = None,
        fopen: float = None,
        fnigh: float = None,
        create_missing_ideas: bool = None,
    ):
        fbranch = fcontext if fbranch is None else fbranch
        if create_missing_ideas:
            self._create_ideakid_if_empty(way=fcontext)
            self._create_ideakid_if_empty(way=fbranch)

        fact_fcontext_idea = self.get_idea_obj(fcontext)
        x_idearoot = self.get_idea_obj(to_way(self.fisc_tag))
        x_fopen = None
        if fnigh is not None and fopen is None:
            x_fopen = x_idearoot.factunits.get(fcontext).fopen
        else:
            x_fopen = fopen
        x_fnigh = None
        if fopen is not None and fnigh is None:
            x_fnigh = x_idearoot.factunits.get(fcontext).fnigh
        else:
            x_fnigh = fnigh
        x_factunit = factunit_shop(
            fcontext=fcontext, fbranch=fbranch, fopen=x_fopen, fnigh=x_fnigh
        )

        if fact_fcontext_idea.is_math() is False:
            x_idearoot.set_factunit(x_factunit)
        # if fact's idea no range or is a "range-root" then allow fact to be set
        elif (
            fact_fcontext_idea.is_math() and self._is_idea_rangeroot(fcontext) is False
        ):
            raise InvalidBudException(
                f"Non range-root fact:{fcontext} can only be set by range-root fact"
            )
        elif fact_fcontext_idea.is_math() and self._is_idea_rangeroot(fcontext):
            # WHEN idea is "range-root" identify any reason.rcontexts that are descendants
            # calculate and set those descendant facts
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendant
            # there exists a reason rcontext "timeline,weeks" with premise.pbranch = "timeline,weeks"
            # and (1,2) pdivisor=2 (every other week)
            #
            # should not set "timeline,weeks" fact, only "timeline" fact and
            # "timeline,weeks" should be set automatica_lly since there exists a reason
            # that has that rcontext.
            x_idearoot.set_factunit(x_factunit)

    def get_fact(self, fcontext: WayStr) -> FactUnit:
        return self.idearoot.factunits.get(fcontext)

    def del_fact(self, fcontext: WayStr):
        self.idearoot.del_factunit(fcontext)

    def get_idea_dict(self, problem: bool = None) -> dict[WayStr, IdeaUnit]:
        self.settle_bud()
        if not problem:
            return self._idea_dict
        if self._keeps_justified is False:
            exception_str = f"Cannot return problem set because _keeps_justified={self._keeps_justified}."
            raise Exception_keeps_justified(exception_str)

        x_ideas = self._idea_dict.values()
        return {
            x_idea.get_idea_way(): x_idea for x_idea in x_ideas if x_idea.problem_bool
        }

    def get_tree_metrics(self) -> TreeMetrics:
        self.settle_bud()
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_tag(
            level=self.idearoot._level,
            reasons=self.idearoot.reasonunits,
            awardlinks=self.idearoot.awardlinks,
            uid=self.idearoot._uid,
            pledge=self.idearoot.pledge,
            idea_way=self.idearoot.get_idea_way(),
        )

        x_idea_list = [self.idearoot]
        while x_idea_list != []:
            parent_idea = x_idea_list.pop()
            for idea_kid in parent_idea._kids.values():
                self._eval_tree_metrics(
                    parent_idea, idea_kid, tree_metrics, x_idea_list
                )
        return tree_metrics

    def _eval_tree_metrics(self, parent_idea, idea_kid, tree_metrics, x_idea_list):
        idea_kid._level = parent_idea._level + 1
        tree_metrics.evaluate_tag(
            level=idea_kid._level,
            reasons=idea_kid.reasonunits,
            awardlinks=idea_kid.awardlinks,
            uid=idea_kid._uid,
            pledge=idea_kid.pledge,
            idea_way=idea_kid.get_idea_way(),
        )
        x_idea_list.append(idea_kid)

    def get_idea_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_idea_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        idea_uid_max = tree_metrics.uid_max
        idea_uid_dict = tree_metrics.uid_dict

        for x_idea in self.get_idea_dict().values():
            if x_idea._uid is None or idea_uid_dict.get(x_idea._uid) > 1:
                new_idea_uid_max = idea_uid_max + 1
                self.edit_idea_attr(
                    idea_way=x_idea.get_idea_way(), uid=new_idea_uid_max
                )
                idea_uid_max = new_idea_uid_max

    def get_level_count(self, level) -> int:
        tree_metrics = self.get_tree_metrics()
        level_count = None
        try:
            level_count = tree_metrics.level_count[level]
        except KeyError:
            level_count = 0
        return level_count

    def get_reason_rcontexts(self) -> set[WayStr]:
        return set(self.get_tree_metrics().reason_rcontexts.keys())

    def get_missing_fact_rcontexts(self) -> dict[WayStr, int]:
        tree_metrics = self.get_tree_metrics()
        reason_rcontexts = tree_metrics.reason_rcontexts
        missing_rcontexts = {}
        for rcontext, rcontext_count in reason_rcontexts.items():
            try:
                self.idearoot.factunits[rcontext]
            except KeyError:
                missing_rcontexts[rcontext] = rcontext_count
        return missing_rcontexts

    def add_idea(
        self, idea_way: WayStr, mass: float = None, pledge: bool = None
    ) -> IdeaUnit:
        x_idea_tag = get_terminus_tag(idea_way, self.bridge)
        x_parent_way = get_parent_way(idea_way, self.bridge)
        x_ideaunit = ideaunit_shop(x_idea_tag, mass=mass)
        if pledge:
            x_ideaunit.pledge = True
        self.set_idea(x_ideaunit, x_parent_way)
        return x_ideaunit

    def set_l1_idea(
        self,
        idea_kid: IdeaUnit,
        create_missing_ideas: bool = None,
        get_rid_of_missing_awardlinks_awardee_labels: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.set_idea(
            idea_kid=idea_kid,
            parent_way=self.fisc_tag,
            create_missing_ideas=create_missing_ideas,
            get_rid_of_missing_awardlinks_awardee_labels=get_rid_of_missing_awardlinks_awardee_labels,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def set_idea(
        self,
        idea_kid: IdeaUnit,
        parent_way: WayStr,
        get_rid_of_missing_awardlinks_awardee_labels: bool = None,
        create_missing_ideas: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        parent_way = to_way(parent_way, self.bridge)
        if TagStr(idea_kid.idea_tag).is_tag(self.bridge) is False:
            x_str = f"set_idea failed because '{idea_kid.idea_tag}' is not a TagStr."
            raise InvalidBudException(x_str)

        x_root_tag = get_root_tag_from_way(parent_way, self.bridge)
        if self.idearoot.idea_tag != x_root_tag:
            exception_str = f"set_idea failed because parent_way '{parent_way}' has an invalid root tag. Should be {self.idearoot.idea_tag}."
            raise InvalidBudException(exception_str)

        idea_kid.bridge = self.bridge
        if idea_kid.fisc_tag != self.fisc_tag:
            idea_kid.fisc_tag = self.fisc_tag
        if idea_kid.fund_coin != self.fund_coin:
            idea_kid.fund_coin = self.fund_coin
        if not get_rid_of_missing_awardlinks_awardee_labels:
            idea_kid = self._get_filtered_awardlinks_idea(idea_kid)
        idea_kid.set_parent_way(parent_way=parent_way)

        # create any missing ideas
        if not create_missing_ancestors and self.idea_exists(parent_way) is False:
            x_str = f"set_idea failed because '{parent_way}' idea does not exist."
            raise InvalidBudException(x_str)
        parent_way_idea = self.get_idea_obj(parent_way, create_missing_ancestors)
        if parent_way_idea.root is False:
            parent_way_idea
        parent_way_idea.add_kid(idea_kid)

        kid_way = self.make_way(parent_way, idea_kid.idea_tag)
        if adoptees is not None:
            mass_sum = 0
            for adoptee_idea_tag in adoptees:
                adoptee_way = self.make_way(parent_way, adoptee_idea_tag)
                adoptee_idea = self.get_idea_obj(adoptee_way)
                mass_sum += adoptee_idea.mass
                new_adoptee_parent_way = self.make_way(kid_way, adoptee_idea_tag)
                self.set_idea(adoptee_idea, new_adoptee_parent_way)
                self.edit_idea_attr(new_adoptee_parent_way, mass=adoptee_idea.mass)
                self.del_idea_obj(adoptee_way)

            if bundling:
                self.edit_idea_attr(kid_way, mass=mass_sum)

        if create_missing_ideas:
            self._create_missing_ideas(way=kid_way)

    def _get_filtered_awardlinks_idea(self, x_idea: IdeaUnit) -> IdeaUnit:
        _awardlinks_to_delete = [
            _awardlink_awardee_label
            for _awardlink_awardee_label in x_idea.awardlinks.keys()
            if self.get_acctunit_group_labels_dict().get(_awardlink_awardee_label)
            is None
        ]
        for _awardlink_awardee_label in _awardlinks_to_delete:
            x_idea.awardlinks.pop(_awardlink_awardee_label)
        if x_idea.teamunit is not None:
            _teamlinks_to_delete = [
                _teamlink_team_label
                for _teamlink_team_label in x_idea.teamunit._teamlinks
                if self.get_acctunit_group_labels_dict().get(_teamlink_team_label)
                is None
            ]
            for _teamlink_team_label in _teamlinks_to_delete:
                x_idea.teamunit.del_teamlink(_teamlink_team_label)
        return x_idea

    def _create_missing_ideas(self, way):
        self._set_idea_dict()
        posted_idea = self.get_idea_obj(way)

        for x_reason in posted_idea.reasonunits.values():
            self._create_ideakid_if_empty(way=x_reason.rcontext)
            for premise_x in x_reason.premises.values():
                self._create_ideakid_if_empty(way=premise_x.pbranch)

    def _create_ideakid_if_empty(self, way: WayStr):
        if self.idea_exists(way) is False:
            self.add_idea(way)

    def del_idea_obj(self, way: WayStr, del_children: bool = True):
        if way == self.idearoot.get_idea_way():
            raise InvalidBudException("Idearoot cannot be deleted")
        parent_way = get_parent_way(way)
        if self.idea_exists(way):
            if not del_children:
                self._shift_idea_kids(x_way=way)
            parent_idea = self.get_idea_obj(parent_way)
            parent_idea.del_kid(get_terminus_tag(way, self.bridge))
        self.settle_bud()

    def _shift_idea_kids(self, x_way: WayStr):
        parent_way = get_parent_way(x_way)
        d_temp_idea = self.get_idea_obj(x_way)
        for kid in d_temp_idea._kids.values():
            self.set_idea(kid, parent_way=parent_way)

    def set_owner_name(self, new_owner_name):
        self.owner_name = new_owner_name

    def edit_idea_tag(self, old_way: WayStr, new_idea_tag: TagStr):
        if self.bridge in new_idea_tag:
            exception_str = f"Cannot modify '{old_way}' because new_idea_tag {new_idea_tag} contains bridge {self.bridge}"
            raise InvalidTagException(exception_str)
        if self.idea_exists(old_way) is False:
            raise InvalidBudException(f"Idea {old_way=} does not exist")

        parent_way = get_parent_way(way=old_way)
        new_way = (
            self.make_way(new_idea_tag)
            if parent_way == ""
            else self.make_way(parent_way, new_idea_tag)
        )
        if old_way != new_way:
            if parent_way == "":
                self.idearoot.set_idea_tag(new_idea_tag)
            else:
                self._non_root_idea_tag_edit(old_way, new_idea_tag, parent_way)
            self._idearoot_find_replace_way(old_way=old_way, new_way=new_way)

    def _non_root_idea_tag_edit(
        self, old_way: WayStr, new_idea_tag: TagStr, parent_way: WayStr
    ):
        x_idea = self.get_idea_obj(old_way)
        x_idea.set_idea_tag(new_idea_tag)
        x_idea.parent_way = parent_way
        idea_parent = self.get_idea_obj(get_parent_way(old_way))
        idea_parent._kids.pop(get_terminus_tag(old_way, self.bridge))
        idea_parent._kids[x_idea.idea_tag] = x_idea

    def _idearoot_find_replace_way(self, old_way: WayStr, new_way: WayStr):
        self.idearoot.find_replace_way(old_way=old_way, new_way=new_way)

        idea_iter_list = [self.idearoot]
        while idea_iter_list != []:
            listed_idea = idea_iter_list.pop()
            # add all idea_children in idea list
            if listed_idea._kids is not None:
                for idea_kid in listed_idea._kids.values():
                    idea_iter_list.append(idea_kid)
                    if is_sub_way(idea_kid.parent_way, sub_way=old_way):
                        idea_kid.parent_way = rebuild_way(
                            subj_way=idea_kid.parent_way,
                            old_way=old_way,
                            new_way=new_way,
                        )
                    idea_kid.find_replace_way(old_way=old_way, new_way=new_way)

    def _set_ideaattrholder_premise_ranges(self, x_ideaattrholder: IdeaAttrHolder):
        premise_idea = self.get_idea_obj(x_ideaattrholder.reason_premise)
        x_ideaattrholder.set_premise_range_attributes_influenced_by_premise_idea(
            premise_open=premise_idea.begin,
            pnigh=premise_idea.close,
            premise_denom=premise_idea.denom,
        )

    def edit_reason(
        self,
        idea_way: WayStr,
        reason_rcontext: WayStr = None,
        reason_premise: WayStr = None,
        reason_premise_open: float = None,
        reason_pnigh: float = None,
        pdivisor: int = None,
    ):
        self.edit_idea_attr(
            idea_way=idea_way,
            reason_rcontext=reason_rcontext,
            reason_premise=reason_premise,
            reason_premise_open=reason_premise_open,
            reason_pnigh=reason_pnigh,
            pdivisor=pdivisor,
        )

    def edit_idea_attr(
        self,
        idea_way: WayStr,
        mass: int = None,
        uid: int = None,
        reason: ReasonUnit = None,
        reason_rcontext: WayStr = None,
        reason_premise: WayStr = None,
        reason_premise_open: float = None,
        reason_pnigh: float = None,
        pdivisor: int = None,
        reason_del_premise_rcontext: WayStr = None,
        reason_del_premise_pbranch: WayStr = None,
        reason_rcontext_idea_active_requisite: str = None,
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
    ):
        if healerlink is not None:
            for x_healer_name in healerlink._healer_names:
                if self.get_acctunit_group_labels_dict().get(x_healer_name) is None:
                    exception_str = f"Idea cannot edit healerlink because group_label '{x_healer_name}' does not exist as group in Bud"
                    raise healerlink_group_label_Exception(exception_str)

        x_ideaattrholder = ideaattrholder_shop(
            mass=mass,
            uid=uid,
            reason=reason,
            reason_rcontext=reason_rcontext,
            reason_premise=reason_premise,
            reason_premise_open=reason_premise_open,
            reason_pnigh=reason_pnigh,
            pdivisor=pdivisor,
            reason_del_premise_rcontext=reason_del_premise_rcontext,
            reason_del_premise_pbranch=reason_del_premise_pbranch,
            reason_rcontext_idea_active_requisite=reason_rcontext_idea_active_requisite,
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
            self._set_ideaattrholder_premise_ranges(x_ideaattrholder)
        x_idea = self.get_idea_obj(idea_way)
        x_idea._set_attrs_to_ideaunit(idea_attr=x_ideaattrholder)

    def get_agenda_dict(
        self, necessary_rcontext: WayStr = None
    ) -> dict[WayStr, IdeaUnit]:
        self.settle_bud()
        return {
            x_idea.get_idea_way(): x_idea
            for x_idea in self._idea_dict.values()
            if x_idea.is_agenda_idea(necessary_rcontext)
        }

    def get_all_pledges(self) -> dict[WayStr, IdeaUnit]:
        self.settle_bud()
        all_ideas = self._idea_dict.values()
        return {x_idea.get_idea_way(): x_idea for x_idea in all_ideas if x_idea.pledge}

    def set_agenda_task_complete(self, task_way: WayStr, rcontext: WayStr):
        pledge_idea = self.get_idea_obj(task_way)
        pledge_idea.set_factunit_to_complete(self.idearoot.factunits[rcontext])

    def get_credit_ledger_debtit_ledger(
        self,
    ) -> tuple[dict[str, float], dict[str, float]]:
        credit_ledger = {}
        debtit_ledger = {}
        for x_acctunit in self.accts.values():
            credit_ledger[x_acctunit.acct_name] = x_acctunit.credit_belief
            debtit_ledger[x_acctunit.acct_name] = x_acctunit.debtit_belief
        return credit_ledger, debtit_ledger

    def _allot_offtrack_fund(self):
        self._add_to_acctunits_fund_give_take(self._offtrack_fund)

    def get_acctunits_credit_belief_sum(self) -> float:
        return sum(acctunit.get_credit_belief() for acctunit in self.accts.values())

    def get_acctunits_debtit_belief_sum(self) -> float:
        return sum(acctunit.get_debtit_belief() for acctunit in self.accts.values())

    def _add_to_acctunits_fund_give_take(self, idea_fund_share: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debtit_ledger()
        fund_give_allot = allot_scale(credor_ledger, idea_fund_share, self.fund_coin)
        fund_take_allot = allot_scale(debtor_ledger, idea_fund_share, self.fund_coin)
        for x_acct_name, acct_fund_give in fund_give_allot.items():
            self.get_acct(x_acct_name).add_fund_give(acct_fund_give)
            # if there is no differentiated agenda (what factunits exist do not change agenda)
            if not self._reason_rcontexts:
                self.get_acct(x_acct_name).add_fund_agenda_give(acct_fund_give)
        for x_acct_name, acct_fund_take in fund_take_allot.items():
            self.get_acct(x_acct_name).add_fund_take(acct_fund_take)
            # if there is no differentiated agenda (what factunits exist do not change agenda)
            if not self._reason_rcontexts:
                self.get_acct(x_acct_name).add_fund_agenda_take(acct_fund_take)

    def _add_to_acctunits_fund_agenda_give_take(self, idea_fund_share: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debtit_ledger()
        fund_give_allot = allot_scale(credor_ledger, idea_fund_share, self.fund_coin)
        fund_take_allot = allot_scale(debtor_ledger, idea_fund_share, self.fund_coin)
        for x_acct_name, acct_fund_give in fund_give_allot.items():
            self.get_acct(x_acct_name).add_fund_agenda_give(acct_fund_give)
        for x_acct_name, acct_fund_take in fund_take_allot.items():
            self.get_acct(x_acct_name).add_fund_agenda_take(acct_fund_take)

    def _reset_groupunits_fund_give_take(self):
        for groupunit_obj in self._groupunits.values():
            groupunit_obj.clear_fund_give_take()

    def _set_groupunits_fund_share(self, awardheirs: dict[GroupLabel, AwardLink]):
        for awardlink_obj in awardheirs.values():
            x_awardee_label = awardlink_obj.awardee_label
            if not self.groupunit_exists(x_awardee_label):
                self.set_groupunit(self.create_symmetry_groupunit(x_awardee_label))
            self.add_to_groupunit_fund_give_fund_take(
                group_label=awardlink_obj.awardee_label,
                awardheir_fund_give=awardlink_obj._fund_give,
                awardheir_fund_take=awardlink_obj._fund_take,
            )

    def _allot_fund_bud_agenda(self):
        for idea in self._idea_dict.values():
            # If there are no awardlines associated with idea
            # allot fund_share via general acctunit
            # cred ratio and debt ratio
            # if idea.is_agenda_idea() and idea._awardlines == {}:
            if idea.is_agenda_idea():
                if idea.awardheir_exists():
                    for x_awardline in idea._awardlines.values():
                        self.add_to_groupunit_fund_agenda_give_take(
                            group_label=x_awardline.awardee_label,
                            awardline_fund_give=x_awardline._fund_give,
                            awardline_fund_take=x_awardline._fund_take,
                        )
                else:
                    self._add_to_acctunits_fund_agenda_give_take(idea.get_fund_share())

    def _allot_groupunits_fund(self):
        for x_groupunit in self._groupunits.values():
            x_groupunit._set_membership_fund_give_fund_take()
            for x_membership in x_groupunit._memberships.values():
                self.add_to_acctunit_fund_give_take(
                    acctunit_acct_name=x_membership.acct_name,
                    fund_give=x_membership._fund_give,
                    fund_take=x_membership._fund_take,
                    fund_agenda_give=x_membership._fund_agenda_give,
                    fund_agenda_take=x_membership._fund_agenda_take,
                )

    def _set_acctunits_fund_agenda_ratios(self):
        fund_agenda_ratio_give_sum = sum(
            x_acctunit._fund_agenda_give for x_acctunit in self.accts.values()
        )
        fund_agenda_ratio_take_sum = sum(
            x_acctunit._fund_agenda_take for x_acctunit in self.accts.values()
        )
        x_acctunit_credit_belief_sum = self.get_acctunits_credit_belief_sum()
        x_acctunit_debtit_belief_sum = self.get_acctunits_debtit_belief_sum()
        for x_acctunit in self.accts.values():
            x_acctunit.set_fund_agenda_ratio_give_take(
                fund_agenda_ratio_give_sum=fund_agenda_ratio_give_sum,
                fund_agenda_ratio_take_sum=fund_agenda_ratio_take_sum,
                bud_acctunit_total_credit_belief=x_acctunit_credit_belief_sum,
                bud_acctunit_total_debtit_belief=x_acctunit_debtit_belief_sum,
            )

    def _reset_acctunit_fund_give_take(self):
        for acctunit in self.accts.values():
            acctunit.clear_fund_give_take()

    def idea_exists(self, way: WayStr) -> bool:
        if way in {"", None}:
            return False
        root_way_idea_tag = get_root_tag_from_way(way, self.bridge)
        if root_way_idea_tag != self.idearoot.idea_tag:
            return False

        tags = get_all_way_tags(way, bridge=self.bridge)
        root_way_idea_tag = tags.pop(0)
        if tags == []:
            return True

        idea_tag = tags.pop(0)
        x_idea = self.idearoot.get_kid(idea_tag)
        if x_idea is None:
            return False
        while tags != []:
            idea_tag = tags.pop(0)
            x_idea = x_idea.get_kid(idea_tag)
            if x_idea is None:
                return False
        return True

    def get_idea_obj(self, way: WayStr, if_missing_create: bool = False) -> IdeaUnit:
        if way is None:
            raise InvalidBudException("get_idea_obj received way=None")
        if self.idea_exists(way) is False and not if_missing_create:
            raise InvalidBudException(f"get_idea_obj failed. no idea at '{way}'")
        tagstrs = get_all_way_tags(way, bridge=self.bridge)
        if len(tagstrs) == 1:
            return self.idearoot

        tagstrs.pop(0)
        idea_tag = tagstrs.pop(0)
        x_idea = self.idearoot.get_kid(idea_tag, if_missing_create)
        while tagstrs != []:
            x_idea = x_idea.get_kid(tagstrs.pop(0), if_missing_create)

        return x_idea

    def get_idea_ranged_kids(
        self, idea_way: str, x_gogo_calc: float = None, x_stop_calc: float = None
    ) -> dict[IdeaUnit]:
        x_idea = self.get_idea_obj(idea_way)
        return x_idea.get_kids_in_range(x_gogo_calc, x_stop_calc)

    def get_inheritor_idea_list(
        self, math_way: WayStr, inheritor_way: WayStr
    ) -> list[IdeaUnit]:
        idea_ways = all_waystrs_between(math_way, inheritor_way)
        return [self.get_idea_obj(x_idea_way) for x_idea_way in idea_ways]

    def _set_idea_dict(self):
        idea_list = [self.get_idea_obj(to_way(self.fisc_tag, self.bridge))]
        while idea_list != []:
            x_idea = idea_list.pop()
            x_idea.clear_gogo_calc_stop_calc()
            for idea_kid in x_idea._kids.values():
                idea_kid.set_parent_way(x_idea.get_idea_way())
                idea_kid.set_level(x_idea._level)
                idea_list.append(idea_kid)
            self._idea_dict[x_idea.get_idea_way()] = x_idea
            for x_reason_rcontext in x_idea.reasonunits.keys():
                self._reason_rcontexts.add(x_reason_rcontext)

    def _raise_gogo_calc_stop_calc_exception(self, idea_way: WayStr):
        exception_str = f"Error has occurred, Idea '{idea_way}' is having _gogo_calc and _stop_calc attributes set twice"
        raise _gogo_calc_stop_calc_Exception(exception_str)

    def _distribute_math_attrs(self, math_idea: IdeaUnit):
        single_range_idea_list = [math_idea]
        while single_range_idea_list != []:
            r_idea = single_range_idea_list.pop()
            if r_idea._range_evaluated:
                self._raise_gogo_calc_stop_calc_exception(r_idea.get_idea_way())
            if r_idea.is_math():
                r_idea._gogo_calc = r_idea.begin
                r_idea._stop_calc = r_idea.close
            else:
                parent_way = get_parent_way(r_idea.get_idea_way())
                parent_idea = self.get_idea_obj(parent_way)
                r_idea._gogo_calc = parent_idea._gogo_calc
                r_idea._stop_calc = parent_idea._stop_calc
                self._range_inheritors[r_idea.get_idea_way()] = math_idea.get_idea_way()
            r_idea._mold_gogo_calc_stop_calc()

            single_range_idea_list.extend(iter(r_idea._kids.values()))

    def _set_ideatree_range_attrs(self):
        for x_idea in self._idea_dict.values():
            if x_idea.is_math():
                self._distribute_math_attrs(x_idea)

            if (
                not x_idea.is_kidless()
                and x_idea.get_kids_mass_sum() == 0
                and x_idea.mass != 0
            ):
                self._offtrack_kids_mass_set.add(x_idea.get_idea_way())

    def _set_groupunit_acctunit_funds(self, keep_exceptions):
        for x_idea in self._idea_dict.values():
            x_idea.set_awardheirs_fund_give_fund_take()
            if x_idea.is_kidless():
                self._set_ancestors_pledge_fund_keep_attrs(
                    x_idea.get_idea_way(), keep_exceptions
                )
                self._allot_fund_share(x_idea)

    def _set_ancestors_pledge_fund_keep_attrs(
        self, way: WayStr, keep_exceptions: bool = False
    ):
        x_descendant_pledge_count = 0
        child_awardlines = None
        group_everyone = None
        ancestor_ways = get_ancestor_ways(way, self.bridge)
        keep_justified_by_problem = True
        healerlink_count = 0

        while ancestor_ways != []:
            youngest_way = ancestor_ways.pop(0)
            x_idea_obj = self.get_idea_obj(youngest_way)
            x_idea_obj.add_to_descendant_pledge_count(x_descendant_pledge_count)
            if x_idea_obj.is_kidless():
                x_idea_obj.set_kidless_awardlines()
                child_awardlines = x_idea_obj._awardlines
            else:
                x_idea_obj.set_awardlines(child_awardlines)

            if x_idea_obj._task:
                x_descendant_pledge_count += 1

            if (
                group_everyone != False
                and x_idea_obj._all_acct_cred != False
                and x_idea_obj._all_acct_debt != False
                and x_idea_obj._awardheirs != {}
            ) or (
                group_everyone != False
                and x_idea_obj._all_acct_cred is False
                and x_idea_obj._all_acct_debt is False
            ):
                group_everyone = False
            elif group_everyone != False:
                group_everyone = True
            x_idea_obj._all_acct_cred = group_everyone
            x_idea_obj._all_acct_debt = group_everyone

            if x_idea_obj.healerlink.any_healer_name_exists():
                keep_justified_by_problem = False
                healerlink_count += 1
                self._sum_healerlink_share += x_idea_obj.get_fund_share()
            if x_idea_obj.problem_bool:
                keep_justified_by_problem = True

        if keep_justified_by_problem is False or healerlink_count > 1:
            if keep_exceptions:
                exception_str = f"IdeaUnit '{way}' cannot sponsor ancestor keeps."
                raise Exception_keeps_justified(exception_str)
            self._keeps_justified = False

    def _clear_ideatree_fund_and_active_status_attrs(self):
        for x_idea in self._idea_dict.values():
            x_idea.clear_awardlines()
            x_idea.clear_descendant_pledge_count()
            x_idea.clear_all_acct_cred_debt()

    def _set_kids_active_status_attrs(self, x_idea: IdeaUnit, parent_idea: IdeaUnit):
        x_idea.set_reasonheirs(self._idea_dict, parent_idea._reasonheirs)
        x_idea.set_range_factheirs(self._idea_dict, self._range_inheritors)
        tt_count = self._tree_traverse_count
        x_idea.set_active_attrs(tt_count, self._groupunits, self.owner_name)

    def _allot_fund_share(self, idea: IdeaUnit):
        if idea.awardheir_exists():
            self._set_groupunits_fund_share(idea._awardheirs)
        elif idea.awardheir_exists() is False:
            self._add_to_acctunits_fund_give_take(idea.get_fund_share())

    def _create_groupunits_metrics(self):
        self._groupunits = {}
        for (
            group_label,
            acct_name_set,
        ) in self.get_acctunit_group_labels_dict().items():
            x_groupunit = groupunit_shop(group_label, bridge=self.bridge)
            for x_acct_name in acct_name_set:
                x_membership = self.get_acct(x_acct_name).get_membership(group_label)
                x_groupunit.set_membership(x_membership)
                self.set_groupunit(x_groupunit)

    def _set_acctunit_groupunit_respect_ledgers(self):
        self.credor_respect = validate_respect_num(self.credor_respect)
        self.debtor_respect = validate_respect_num(self.debtor_respect)
        credor_ledger, debtor_ledger = self.get_credit_ledger_debtit_ledger()
        credor_allot = allot_scale(credor_ledger, self.credor_respect, self.respect_bit)
        debtor_allot = allot_scale(debtor_ledger, self.debtor_respect, self.respect_bit)
        for x_acct_name, acct_credor_pool in credor_allot.items():
            self.get_acct(x_acct_name).set_credor_pool(acct_credor_pool)
        for x_acct_name, acct_debtor_pool in debtor_allot.items():
            self.get_acct(x_acct_name).set_debtor_pool(acct_debtor_pool)
        self._create_groupunits_metrics()
        self._reset_acctunit_fund_give_take()

    def _clear_idea_dict_and_bud_obj_settle_attrs(self):
        self._idea_dict = {self.idearoot.get_idea_way(): self.idearoot}
        self._rational = False
        self._tree_traverse_count = 0
        self._offtrack_kids_mass_set = set()
        self._reason_rcontexts = set()
        self._range_inheritors = {}
        self._keeps_justified = True
        self._keeps_buildable = False
        self._sum_healerlink_share = 0
        self._keep_dict = {}
        self._healers_dict = {}

    def _set_ideatree_factheirs_teamheirs_awardheirs(self):
        for x_idea in get_sorted_idea_list(list(self._idea_dict.values())):
            if x_idea.root:
                x_idea.set_factheirs(x_idea.factunits)
                x_idea.set_idearoot_inherit_reasonheirs()
                x_idea.set_teamheir(None, self._groupunits)
                x_idea.inherit_awardheirs()
            else:
                parent_idea = self.get_idea_obj(x_idea.parent_way)
                x_idea.set_factheirs(parent_idea._factheirs)
                x_idea.set_teamheir(parent_idea._teamheir, self._groupunits)
                x_idea.inherit_awardheirs(parent_idea._awardheirs)
            x_idea.set_awardheirs_fund_give_fund_take()

    def settle_bud(self, keep_exceptions: bool = False):
        self._clear_idea_dict_and_bud_obj_settle_attrs()
        self._set_idea_dict()
        self._set_ideatree_range_attrs()
        self._set_acctunit_groupunit_respect_ledgers()
        self._clear_acctunit_fund_attrs()
        self._clear_ideatree_fund_and_active_status_attrs()
        self._set_ideatree_factheirs_teamheirs_awardheirs()

        max_count = self.max_tree_traverse
        while not self._rational and self._tree_traverse_count < max_count:
            self._set_ideatree_active_status_attrs()
            self._set_rational_attr()
            self._tree_traverse_count += 1

        self._set_ideatree_fund_attrs(self.idearoot)
        self._set_groupunit_acctunit_funds(keep_exceptions)
        self._set_acctunit_fund_related_attrs()
        self._set_bud_keep_attrs()

    def _set_ideatree_active_status_attrs(self):
        for x_idea in get_sorted_idea_list(list(self._idea_dict.values())):
            if x_idea.root:
                tt_count = self._tree_traverse_count
                root_idea = self.idearoot
                root_idea.set_active_attrs(tt_count, self._groupunits, self.owner_name)
            else:
                parent_idea = self.get_idea_obj(x_idea.parent_way)
                self._set_kids_active_status_attrs(x_idea, parent_idea)

    def _set_ideatree_fund_attrs(self, root_idea: IdeaUnit):
        root_idea.set_fund_attr(0, self.fund_pool, self.fund_pool)
        # no function recursion, recursion by iterateing over list that can be added to by iterations
        cache_idea_list = [root_idea]
        while cache_idea_list != []:
            parent_idea = cache_idea_list.pop()
            kids_ideas = parent_idea._kids.items()
            x_ledger = {x_way: idea_kid.mass for x_way, idea_kid in kids_ideas}
            parent_fund_num = parent_idea._fund_cease - parent_idea._fund_onset
            alloted_fund_num = allot_scale(x_ledger, parent_fund_num, self.fund_coin)

            fund_onset = None
            fund_cease = None
            for x_idea in parent_idea._kids.values():
                if fund_onset is None:
                    fund_onset = parent_idea._fund_onset
                    fund_cease = fund_onset + alloted_fund_num.get(x_idea.idea_tag)
                else:
                    fund_onset = fund_cease
                    fund_cease += alloted_fund_num.get(x_idea.idea_tag)
                x_idea.set_fund_attr(fund_onset, fund_cease, self.fund_pool)
                cache_idea_list.append(x_idea)

    def _set_rational_attr(self):
        any_idea_active_status_has_altered = False
        for idea in self._idea_dict.values():
            if idea._active_hx.get(self._tree_traverse_count) is not None:
                any_idea_active_status_has_altered = True

        if any_idea_active_status_has_altered is False:
            self._rational = True

    def _set_acctunit_fund_related_attrs(self):
        self.set_offtrack_fund()
        self._allot_offtrack_fund()
        self._allot_fund_bud_agenda()
        self._allot_groupunits_fund()
        self._set_acctunits_fund_agenda_ratios()

    def _set_bud_keep_attrs(self):
        self._set_keep_dict()
        self._healers_dict = self._get_healers_dict()
        self._keeps_buildable = self._get_buildable_keeps()

    def _set_keep_dict(self):
        if self._keeps_justified is False:
            self._sum_healerlink_share = 0
        for x_idea in self._idea_dict.values():
            if self._sum_healerlink_share == 0:
                x_idea._healerlink_ratio = 0
            else:
                x_sum = self._sum_healerlink_share
                x_idea._healerlink_ratio = x_idea.get_fund_share() / x_sum
            if self._keeps_justified and x_idea.healerlink.any_healer_name_exists():
                self._keep_dict[x_idea.get_idea_way()] = x_idea

    def _get_healers_dict(self) -> dict[HealerName, dict[WayStr, IdeaUnit]]:
        _healers_dict = {}
        for x_keep_way, x_keep_idea in self._keep_dict.items():
            for x_healer_name in x_keep_idea.healerlink._healer_names:
                x_groupunit = self.get_groupunit(x_healer_name)
                for x_acct_name in x_groupunit._memberships.keys():
                    if _healers_dict.get(x_acct_name) is None:
                        _healers_dict[x_acct_name] = {x_keep_way: x_keep_idea}
                    else:
                        healer_dict = _healers_dict.get(x_acct_name)
                        healer_dict[x_keep_way] = x_keep_idea
        return _healers_dict

    def _get_buildable_keeps(self) -> bool:
        return all(
            waystr_valid_dir_path(keep_way, self.bridge) != False
            for keep_way in self._keep_dict.keys()
        )

    def _clear_acctunit_fund_attrs(self):
        self._reset_groupunits_fund_give_take()
        self._reset_acctunit_fund_give_take()

    def get_idea_tree_ordered_way_list(
        self, no_range_descendants: bool = False
    ) -> list[WayStr]:
        idea_list = list(self.get_idea_dict().values())
        tag_dict = {
            idea.get_idea_way().lower(): idea.get_idea_way() for idea in idea_list
        }
        tag_lowercase_ordered_list = sorted(list(tag_dict))
        tag_orginalcase_ordered_list = [
            tag_dict[tag_l] for tag_l in tag_lowercase_ordered_list
        ]

        list_x = []
        for way in tag_orginalcase_ordered_list:
            if not no_range_descendants:
                list_x.append(way)
            else:
                anc_list = get_ancestor_ways(way=way)
                if len(anc_list) == 1:
                    list_x.append(way)
                elif len(anc_list) == 2:
                    if self.idearoot.begin is None and self.idearoot.close is None:
                        list_x.append(way)
                else:
                    parent_idea = self.get_idea_obj(way=anc_list[1])
                    if parent_idea.begin is None and parent_idea.close is None:
                        list_x.append(way)

        return list_x

    def get_factunits_dict(self) -> dict[str, str]:
        x_dict = {}
        if self.idearoot.factunits is not None:
            for fact_way, fact_obj in self.idearoot.factunits.items():
                x_dict[fact_way] = fact_obj.get_dict()
        return x_dict

    def get_acctunits_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {}
        if self.accts is not None:
            for acct_name, acct_obj in self.accts.items():
                x_dict[acct_name] = acct_obj.get_dict(all_attrs)
        return x_dict

    def get_dict(self) -> dict[str, str]:
        x_dict = {
            "accts": self.get_acctunits_dict(),
            "originunit": self.originunit.get_dict(),
            "tally": self.tally,
            "fund_pool": self.fund_pool,
            "fund_coin": self.fund_coin,
            "respect_bit": self.respect_bit,
            "penny": self.penny,
            "owner_name": self.owner_name,
            "fisc_tag": self.fisc_tag,
            "max_tree_traverse": self.max_tree_traverse,
            "bridge": self.bridge,
            "idearoot": self.idearoot.get_dict(),
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

    def set_dominate_pledge_idea(self, idea_kid: IdeaUnit):
        idea_kid.pledge = True
        self.set_idea(
            idea_kid=idea_kid,
            parent_way=self.make_way(idea_kid.parent_way),
            get_rid_of_missing_awardlinks_awardee_labels=True,
            create_missing_ideas=True,
        )

    def set_offtrack_fund(self) -> float:
        mass_set = self._offtrack_kids_mass_set
        self._offtrack_fund = sum(
            self.get_idea_obj(x_waystr).get_fund_share() for x_waystr in mass_set
        )


def budunit_shop(
    owner_name: OwnerName = None,
    fisc_tag: FiscTag = None,
    bridge: str = None,
    fund_pool: FundNum = None,
    fund_coin: FundCoin = None,
    respect_bit: BitNum = None,
    penny: PennyNum = None,
    tally: float = None,
) -> BudUnit:
    owner_name = "" if owner_name is None else owner_name
    fisc_tag = get_default_fisc_tag() if fisc_tag is None else fisc_tag
    x_bud = BudUnit(
        owner_name=owner_name,
        tally=get_1_if_None(tally),
        fisc_tag=fisc_tag,
        accts=get_empty_dict_if_None(),
        _groupunits={},
        bridge=default_bridge_if_None(bridge),
        credor_respect=validate_respect_num(),
        debtor_respect=validate_respect_num(),
        fund_pool=validate_fund_pool(fund_pool),
        fund_coin=default_fund_coin_if_None(fund_coin),
        respect_bit=default_respect_bit_if_None(respect_bit),
        penny=filter_penny(penny),
        _idea_dict=get_empty_dict_if_None(),
        _keep_dict=get_empty_dict_if_None(),
        _healers_dict=get_empty_dict_if_None(),
        _keeps_justified=get_False_if_None(),
        _keeps_buildable=get_False_if_None(),
        _sum_healerlink_share=get_0_if_None(),
        _offtrack_kids_mass_set=set(),
        _reason_rcontexts=set(),
        _range_inheritors={},
    )
    x_bud.idearoot = ideaunit_shop(
        root=True,
        _uid=1,
        _level=0,
        fisc_tag=x_bud.fisc_tag,
        bridge=x_bud.bridge,
        fund_coin=x_bud.fund_coin,
        parent_way="",
    )
    x_bud.set_max_tree_traverse(3)
    x_bud._rational = False
    x_bud.originunit = originunit_shop()
    return x_bud


def get_from_json(x_bud_json: str) -> BudUnit:
    return get_from_dict(get_dict_from_json(x_bud_json))


def get_from_dict(bud_dict: dict) -> BudUnit:
    x_bud = budunit_shop()
    x_bud.set_owner_name(obj_from_bud_dict(bud_dict, "owner_name"))
    x_bud.tally = obj_from_bud_dict(bud_dict, "tally")
    x_bud.set_max_tree_traverse(obj_from_bud_dict(bud_dict, "max_tree_traverse"))
    x_bud.fisc_tag = obj_from_bud_dict(bud_dict, "fisc_tag")
    x_bud.idearoot.idea_tag = obj_from_bud_dict(bud_dict, "fisc_tag")
    bud_bridge = obj_from_bud_dict(bud_dict, "bridge")
    x_bud.bridge = default_bridge_if_None(bud_bridge)
    x_bud.fund_pool = validate_fund_pool(obj_from_bud_dict(bud_dict, "fund_pool"))
    x_bud.fund_coin = default_fund_coin_if_None(
        obj_from_bud_dict(bud_dict, "fund_coin")
    )
    x_bud.respect_bit = default_respect_bit_if_None(
        obj_from_bud_dict(bud_dict, "respect_bit")
    )
    x_bud.penny = filter_penny(obj_from_bud_dict(bud_dict, "penny"))
    x_bud.credor_respect = obj_from_bud_dict(bud_dict, "credor_respect")
    x_bud.debtor_respect = obj_from_bud_dict(bud_dict, "debtor_respect")
    x_bud.last_pack_id = obj_from_bud_dict(bud_dict, "last_pack_id")
    x_bridge = x_bud.bridge
    x_accts = obj_from_bud_dict(bud_dict, "accts", x_bridge).values()
    for x_acctunit in x_accts:
        x_bud.set_acctunit(x_acctunit)
    x_bud.originunit = obj_from_bud_dict(bud_dict, "originunit")
    create_idearoot_from_bud_dict(x_bud, bud_dict)
    return x_bud


def create_idearoot_from_bud_dict(x_bud: BudUnit, bud_dict: dict):
    idearoot_dict = bud_dict.get("idearoot")
    x_bud.idearoot = ideaunit_shop(
        root=True,
        idea_tag=x_bud.fisc_tag,
        parent_way="",
        _level=0,
        _uid=get_obj_from_idea_dict(idearoot_dict, "_uid"),
        mass=get_obj_from_idea_dict(idearoot_dict, "mass"),
        begin=get_obj_from_idea_dict(idearoot_dict, "begin"),
        close=get_obj_from_idea_dict(idearoot_dict, "close"),
        numor=get_obj_from_idea_dict(idearoot_dict, "numor"),
        denom=get_obj_from_idea_dict(idearoot_dict, "denom"),
        morph=get_obj_from_idea_dict(idearoot_dict, "morph"),
        gogo_want=get_obj_from_idea_dict(idearoot_dict, "gogo_want"),
        stop_want=get_obj_from_idea_dict(idearoot_dict, "stop_want"),
        problem_bool=get_obj_from_idea_dict(idearoot_dict, "problem_bool"),
        reasonunits=get_obj_from_idea_dict(idearoot_dict, "reasonunits"),
        teamunit=get_obj_from_idea_dict(idearoot_dict, "teamunit"),
        healerlink=get_obj_from_idea_dict(idearoot_dict, "healerlink"),
        factunits=get_obj_from_idea_dict(idearoot_dict, "factunits"),
        awardlinks=get_obj_from_idea_dict(idearoot_dict, "awardlinks"),
        _is_expanded=get_obj_from_idea_dict(idearoot_dict, "_is_expanded"),
        bridge=x_bud.bridge,
        fisc_tag=x_bud.fisc_tag,
        fund_coin=default_fund_coin_if_None(x_bud.fund_coin),
    )
    create_idearoot_kids_from_dict(x_bud, idearoot_dict)


def create_idearoot_kids_from_dict(x_bud: BudUnit, idearoot_dict: dict):
    to_evaluate_idea_dicts = []
    parent_way_str = "parent_way"
    # for every kid dict, set parent_way in dict, add to to_evaluate_list
    for x_dict in get_obj_from_idea_dict(idearoot_dict, "_kids").values():
        x_dict[parent_way_str] = x_bud.fisc_tag
        to_evaluate_idea_dicts.append(x_dict)

    while to_evaluate_idea_dicts != []:
        idea_dict = to_evaluate_idea_dicts.pop(0)
        # for every kid dict, set parent_way in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_idea_dict(idea_dict, "_kids").values():
            parent_way = get_obj_from_idea_dict(idea_dict, parent_way_str)
            kid_idea_tag = get_obj_from_idea_dict(idea_dict, "idea_tag")
            kid_dict[parent_way_str] = x_bud.make_way(parent_way, kid_idea_tag)
            to_evaluate_idea_dicts.append(kid_dict)
        x_ideakid = ideaunit_shop(
            idea_tag=get_obj_from_idea_dict(idea_dict, "idea_tag"),
            mass=get_obj_from_idea_dict(idea_dict, "mass"),
            _uid=get_obj_from_idea_dict(idea_dict, "_uid"),
            begin=get_obj_from_idea_dict(idea_dict, "begin"),
            close=get_obj_from_idea_dict(idea_dict, "close"),
            numor=get_obj_from_idea_dict(idea_dict, "numor"),
            denom=get_obj_from_idea_dict(idea_dict, "denom"),
            morph=get_obj_from_idea_dict(idea_dict, "morph"),
            gogo_want=get_obj_from_idea_dict(idea_dict, "gogo_want"),
            stop_want=get_obj_from_idea_dict(idea_dict, "stop_want"),
            pledge=get_obj_from_idea_dict(idea_dict, "pledge"),
            problem_bool=get_obj_from_idea_dict(idea_dict, "problem_bool"),
            reasonunits=get_obj_from_idea_dict(idea_dict, "reasonunits"),
            teamunit=get_obj_from_idea_dict(idea_dict, "teamunit"),
            healerlink=get_obj_from_idea_dict(idea_dict, "healerlink"),
            _originunit=get_obj_from_idea_dict(idea_dict, "originunit"),
            awardlinks=get_obj_from_idea_dict(idea_dict, "awardlinks"),
            factunits=get_obj_from_idea_dict(idea_dict, "factunits"),
            _is_expanded=get_obj_from_idea_dict(idea_dict, "_is_expanded"),
        )
        x_bud.set_idea(x_ideakid, parent_way=idea_dict[parent_way_str])


def obj_from_bud_dict(
    x_dict: dict[str, dict], dict_key: str, _bridge: str = None
) -> any:
    if dict_key == "originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else originunit_shop()
        )
    elif dict_key == "accts":
        return acctunits_get_from_dict(x_dict[dict_key], _bridge)
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
        budunits[x_bud.owner_name] = x_bud
    return budunits


def get_sorted_idea_list(x_list: list[IdeaUnit]) -> list[IdeaUnit]:
    x_list.sort(key=lambda x: x.get_idea_way(), reverse=False)
    return x_list
