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
from src.a01_term_logic.term import (
    AcctName,
    GroupTitle,
    HealerName,
    LabelTerm,
    OwnerName,
    VowLabel,
    WayTerm,
)
from src.a01_term_logic.way import (
    all_wayterms_between,
    create_way,
    default_bridge_if_None,
    get_all_way_labels,
    get_ancestor_ways,
    get_forefather_ways,
    get_parent_way,
    get_root_label_from_way,
    get_tail_label,
    is_string_in_way,
    is_sub_way,
    rebuild_way,
    to_way,
    wayterm_valid_dir_path,
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
from src.a03_group_logic.acct import AcctUnit, acctunit_shop, acctunits_get_from_dict
from src.a03_group_logic.group import (
    AwardLink,
    GroupUnit,
    groupunit_shop,
    membership_shop,
)
from src.a04_reason_logic.reason_concept import (
    FactUnit,
    ReasonUnit,
    WayTerm,
    factunit_shop,
)
from src.a04_reason_logic.reason_labor import LaborUnit
from src.a05_concept_logic.concept import (
    ConceptAttrHolder,
    ConceptUnit,
    conceptattrholder_shop,
    conceptunit_shop,
    get_default_vow_label,
    get_obj_from_concept_dict,
)
from src.a05_concept_logic.healer import HealerLink
from src.a06_plan_logic.plan_config import max_tree_traverse_default
from src.a06_plan_logic.tree_metrics import TreeMetrics, treemetrics_shop


class InvalidPlanException(Exception):
    pass


class InvalidLabelException(Exception):
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


class healerlink_group_title_Exception(Exception):
    pass


class _gogo_calc_stop_calc_Exception(Exception):
    pass


@dataclass
class PlanUnit:
    vow_label: VowLabel = None
    owner_name: OwnerName = None
    accts: dict[AcctName, AcctUnit] = None
    conceptroot: ConceptUnit = None
    tally: float = None
    fund_pool: FundNum = None
    fund_iota: FundIota = None
    penny: PennyNum = None
    credor_respect: RespectNum = None
    debtor_respect: RespectNum = None
    respect_bit: BitNum = None
    bridge: str = None
    max_tree_traverse: int = None
    last_pack_id: int = None
    # settle_plan Calculated field begin
    _concept_dict: dict[WayTerm, ConceptUnit] = None
    _keep_dict: dict[WayTerm, ConceptUnit] = None
    _healers_dict: dict[HealerName, dict[WayTerm, ConceptUnit]] = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _keeps_justified: bool = None
    _keeps_buildable: bool = None
    _sum_healerlink_share: float = None
    _groupunits: dict[GroupTitle, GroupUnit] = None
    _offtrack_kids_mass_set: set[WayTerm] = None
    _offtrack_fund: float = None
    _reason_rcontexts: set[WayTerm] = None
    _range_inheritors: dict[WayTerm, WayTerm] = None
    # settle_plan Calculated field end

    def del_last_pack_id(self):
        self.last_pack_id = None

    def set_last_pack_id(self, x_last_pack_id: int):
        if self.last_pack_id is not None and x_last_pack_id < self.last_pack_id:
            exception_str = f"Cannot set _last_pack_id to {x_last_pack_id} because it is less than {self.last_pack_id}."
            raise _last_pack_idException(exception_str)
        self.last_pack_id = x_last_pack_id

    def set_fund_pool(self, x_fund_pool):
        if valid_finance_ratio(x_fund_pool, self.fund_iota) is False:
            exception_str = f"Plan '{self.owner_name}' cannot set fund_pool='{x_fund_pool}'. It is not divisible by fund_iota '{self.fund_iota}'"
            raise _bit_RatioException(exception_str)

        self.fund_pool = validate_fund_pool(x_fund_pool)

    def set_acct_respect(self, x_acct_pool: int):
        self.set_credor_respect(x_acct_pool)
        self.set_debtor_respect(x_acct_pool)
        self.set_fund_pool(x_acct_pool)

    def set_credor_respect(self, new_credor_respect: int):
        if valid_finance_ratio(new_credor_respect, self.respect_bit) is False:
            exception_str = f"Plan '{self.owner_name}' cannot set credor_respect='{new_credor_respect}'. It is not divisible by bit '{self.respect_bit}'"
            raise _bit_RatioException(exception_str)
        self.credor_respect = new_credor_respect

    def set_debtor_respect(self, new_debtor_respect: int):
        if valid_finance_ratio(new_debtor_respect, self.respect_bit) is False:
            exception_str = f"Plan '{self.owner_name}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible by bit '{self.respect_bit}'"
            raise _bit_RatioException(exception_str)
        self.debtor_respect = new_debtor_respect

    def make_way(
        self,
        parent_way: WayTerm = None,
        tail_label: LabelTerm = None,
    ) -> WayTerm:
        return create_way(
            parent_way=parent_way,
            tail_label=tail_label,
            bridge=self.bridge,
        )

    def make_l1_way(self, l1_label: LabelTerm):
        return self.make_way(self.vow_label, l1_label)

    def set_bridge(self, new_bridge: str):
        self.settle_plan()
        if self.bridge != new_bridge:
            for x_concept_way in self._concept_dict.keys():
                if is_string_in_way(new_bridge, x_concept_way):
                    exception_str = f"Cannot modify bridge to '{new_bridge}' because it exists an concept concept_label '{x_concept_way}'"
                    raise NewBridgeException(exception_str)

            # modify all way attributes in conceptunits
            self.bridge = default_bridge_if_None(new_bridge)
            for x_concept in self._concept_dict.values():
                x_concept.set_bridge(self.bridge)

    def set_vow_label(self, vow_label: str):
        old_vow_label = copy_deepcopy(self.vow_label)
        self.settle_plan()
        for concept_obj in self._concept_dict.values():
            concept_obj.vow_label = vow_label
        self.vow_label = vow_label
        self.edit_concept_label(
            old_way=to_way(old_vow_label), new_concept_label=self.vow_label
        )
        self.settle_plan()

    def set_max_tree_traverse(self, x_int: int):
        if x_int < 2 or not float(x_int).is_integer():
            raise InvalidPlanException(
                f"set_max_tree_traverse: '{x_int}' must be number that is 2 or greater"
            )
        else:
            self.max_tree_traverse = x_int

    def _get_relevant_ways(self, ways: dict[WayTerm,]) -> set[WayTerm]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for x_way in ways:
            to_evaluate_list.append(x_way)
            to_evaluate_hx_dict[x_way] = "to_evaluate"
        evaluated_ways = set()

        # while ways_to_evaluate != [] and count_x <= tree_metrics.label_count:
        # Why count_x? because count_x might be wrong attr to measure
        # nice to avoid infinite loops from programming errors though...
        while to_evaluate_list != []:
            x_way = to_evaluate_list.pop()
            x_concept = self.get_concept_obj(x_way)
            for reasonunit_obj in x_concept.reasonunits.values():
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
        to_evaluate_list: list[WayTerm],
        to_evaluate_hx_dict: dict[WayTerm, int],
        to_evaluate_way: WayTerm,
        way_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_way) is None:
            to_evaluate_list.append(to_evaluate_way)
            to_evaluate_hx_dict[to_evaluate_way] = way_type

            if way_type == "reasonunit_rcontext":
                ru_rcontext_concept = self.get_concept_obj(to_evaluate_way)
                for (
                    descendant_way
                ) in ru_rcontext_concept.get_descendant_ways_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_way=descendant_way,
                        way_type="reasonunit_descendant",
                    )

    def all_concepts_relevant_to_task_concept(self, way: WayTerm) -> bool:
        task_concept_assoc_set = set(self._get_relevant_ways({way}))
        all_concepts_set = set(self.get_concept_tree_ordered_way_list())
        return all_concepts_set == all_concepts_set.intersection(task_concept_assoc_set)

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
        self, acct_name: AcctName, credit_score: int = None, debt_score: int = None
    ):
        x_bridge = self.bridge
        acctunit = acctunit_shop(acct_name, credit_score, debt_score, x_bridge)
        self.set_acctunit(acctunit)

    def set_acctunit(self, x_acctunit: AcctUnit, auto_set_membership: bool = True):
        if x_acctunit.bridge != self.bridge:
            x_acctunit.bridge = self.bridge
        if x_acctunit.respect_bit != self.respect_bit:
            x_acctunit.respect_bit = self.respect_bit
        if auto_set_membership and x_acctunit.memberships_exist() is False:
            x_acctunit.add_membership(x_acctunit.acct_name)
        self.accts[x_acctunit.acct_name] = x_acctunit

    def acct_exists(self, acct_name: AcctName) -> bool:
        return self.get_acct(acct_name) is not None

    def edit_acctunit(
        self, acct_name: AcctName, credit_score: int = None, debt_score: int = None
    ):
        if self.accts.get(acct_name) is None:
            raise AcctMissingException(f"AcctUnit '{acct_name}' does not exist.")
        x_acctunit = self.get_acct(acct_name)
        if credit_score is not None:
            x_acctunit.set_credit_score(credit_score)
        if debt_score is not None:
            x_acctunit.set_debt_score(debt_score)
        self.set_acctunit(x_acctunit)

    def clear_acctunits_memberships(self):
        for x_acctunit in self.accts.values():
            x_acctunit.clear_memberships()

    def get_acct(self, acct_name: AcctName) -> AcctUnit:
        return self.accts.get(acct_name)

    def get_acctunit_group_titles_dict(self) -> dict[GroupTitle, set[AcctName]]:
        x_dict = {}
        for x_acctunit in self.accts.values():
            for x_group_title in x_acctunit._memberships.keys():
                acct_name_set = x_dict.get(x_group_title)
                if acct_name_set is None:
                    x_dict[x_group_title] = {x_acctunit.acct_name}
                else:
                    acct_name_set.add(x_acctunit.acct_name)
                    x_dict[x_group_title] = acct_name_set
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
        for x_acctunit in self.accts.values():
            x_membership = membership_shop(
                group_title=x_group_title,
                credit_vote=x_acctunit.credit_score,
                debt_vote=x_acctunit.debt_score,
                acct_name=x_acctunit.acct_name,
            )
            x_groupunit.set_membership(x_membership)
        return x_groupunit

    def get_tree_traverse_generated_groupunits(self) -> set[GroupTitle]:
        x_acctunit_group_titles = set(self.get_acctunit_group_titles_dict().keys())
        all_group_titles = set(self._groupunits.keys())
        return all_group_titles.difference(x_acctunit_group_titles)

    def _is_concept_rangeroot(self, concept_way: WayTerm) -> bool:
        if self.vow_label == concept_way:
            raise InvalidPlanException(
                "its difficult to foresee a scenario where conceptroot is rangeroot"
            )
        parent_way = get_parent_way(concept_way)
        parent_concept = self.get_concept_obj(parent_way)
        return not parent_concept.is_math()

    def _get_rangeroot_factunits(self) -> list[FactUnit]:
        return [
            fact
            for fact in self.conceptroot.factunits.values()
            if fact.fopen is not None
            and fact.fnigh is not None
            and self._is_concept_rangeroot(concept_way=fact.fcontext)
        ]

    def add_fact(
        self,
        fcontext: WayTerm,
        fstate: WayTerm = None,
        fopen: float = None,
        fnigh: float = None,
        create_missing_concepts: bool = None,
    ):
        fstate = fcontext if fstate is None else fstate
        if create_missing_concepts:
            self._create_conceptkid_if_empty(way=fcontext)
            self._create_conceptkid_if_empty(way=fstate)

        fact_fcontext_concept = self.get_concept_obj(fcontext)
        x_conceptroot = self.get_concept_obj(to_way(self.vow_label))
        x_fopen = None
        if fnigh is not None and fopen is None:
            x_fopen = x_conceptroot.factunits.get(fcontext).fopen
        else:
            x_fopen = fopen
        x_fnigh = None
        if fopen is not None and fnigh is None:
            x_fnigh = x_conceptroot.factunits.get(fcontext).fnigh
        else:
            x_fnigh = fnigh
        x_factunit = factunit_shop(
            fcontext=fcontext,
            fstate=fstate,
            fopen=x_fopen,
            fnigh=x_fnigh,
        )

        if fact_fcontext_concept.is_math() is False:
            x_conceptroot.set_factunit(x_factunit)
        # if fact's concept no range or is a "range-root" then allow fact to be set
        elif (
            fact_fcontext_concept.is_math()
            and self._is_concept_rangeroot(fcontext) is False
        ):
            raise InvalidPlanException(
                f"Non range-root fact:{fcontext} can only be set by range-root fact"
            )
        elif fact_fcontext_concept.is_math() and self._is_concept_rangeroot(fcontext):
            # WHEN concept is "range-root" identify any reason.rcontexts that are descendants
            # calculate and set those descendant facts
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,wks" (spllt 10080) is range-descendant
            # there exists a reason rcontext "timeline,wks" with premise.pstate = "timeline,wks"
            # and (1,2) pdivisor=2 (every other wk)
            #
            # should not set "timeline,wks" fact, only "timeline" fact and
            # "timeline,wks" should be set automatica_lly since there exists a reason
            # that has that rcontext.
            x_conceptroot.set_factunit(x_factunit)

    def get_fact(self, fcontext: WayTerm) -> FactUnit:
        return self.conceptroot.factunits.get(fcontext)

    def del_fact(self, fcontext: WayTerm):
        self.conceptroot.del_factunit(fcontext)

    def get_concept_dict(self, problem: bool = None) -> dict[WayTerm, ConceptUnit]:
        self.settle_plan()
        if not problem:
            return self._concept_dict
        if self._keeps_justified is False:
            exception_str = f"Cannot return problem set because _keeps_justified={self._keeps_justified}."
            raise Exception_keeps_justified(exception_str)

        x_concepts = self._concept_dict.values()
        return {
            x_concept.get_concept_way(): x_concept
            for x_concept in x_concepts
            if x_concept.problem_bool
        }

    def get_tree_metrics(self) -> TreeMetrics:
        self.settle_plan()
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_label(
            level=self.conceptroot._level,
            reasons=self.conceptroot.reasonunits,
            awardlinks=self.conceptroot.awardlinks,
            uid=self.conceptroot._uid,
            task=self.conceptroot.task,
            concept_way=self.conceptroot.get_concept_way(),
        )

        x_concept_list = [self.conceptroot]
        while x_concept_list != []:
            parent_concept = x_concept_list.pop()
            for concept_kid in parent_concept._kids.values():
                self._eval_tree_metrics(
                    parent_concept, concept_kid, tree_metrics, x_concept_list
                )
        return tree_metrics

    def _eval_tree_metrics(
        self, parent_concept, concept_kid, tree_metrics, x_concept_list
    ):
        concept_kid._level = parent_concept._level + 1
        tree_metrics.evaluate_label(
            level=concept_kid._level,
            reasons=concept_kid.reasonunits,
            awardlinks=concept_kid.awardlinks,
            uid=concept_kid._uid,
            task=concept_kid.task,
            concept_way=concept_kid.get_concept_way(),
        )
        x_concept_list.append(concept_kid)

    def get_concept_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_concept_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        concept_uid_max = tree_metrics.uid_max
        concept_uid_dict = tree_metrics.uid_dict

        for x_concept in self.get_concept_dict().values():
            if x_concept._uid is None or concept_uid_dict.get(x_concept._uid) > 1:
                new_concept_uid_max = concept_uid_max + 1
                self.edit_concept_attr(
                    concept_way=x_concept.get_concept_way(), uid=new_concept_uid_max
                )
                concept_uid_max = new_concept_uid_max

    def get_level_count(self, level) -> int:
        tree_metrics = self.get_tree_metrics()
        level_count = None
        try:
            level_count = tree_metrics.level_count[level]
        except KeyError:
            level_count = 0
        return level_count

    def get_reason_rcontexts(self) -> set[WayTerm]:
        return set(self.get_tree_metrics().reason_rcontexts.keys())

    def get_missing_fact_rcontexts(self) -> dict[WayTerm, int]:
        tree_metrics = self.get_tree_metrics()
        reason_rcontexts = tree_metrics.reason_rcontexts
        missing_rcontexts = {}
        for rcontext, rcontext_count in reason_rcontexts.items():
            try:
                self.conceptroot.factunits[rcontext]
            except KeyError:
                missing_rcontexts[rcontext] = rcontext_count
        return missing_rcontexts

    def add_concept(
        self, concept_way: WayTerm, mass: float = None, task: bool = None
    ) -> ConceptUnit:
        x_concept_label = get_tail_label(concept_way, self.bridge)
        x_parent_way = get_parent_way(concept_way, self.bridge)
        x_conceptunit = conceptunit_shop(x_concept_label, mass=mass)
        if task:
            x_conceptunit.task = True
        self.set_concept(x_conceptunit, x_parent_way)
        return x_conceptunit

    def set_l1_concept(
        self,
        concept_kid: ConceptUnit,
        create_missing_concepts: bool = None,
        get_rid_of_missing_awardlinks_awardee_titles: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.set_concept(
            concept_kid=concept_kid,
            parent_way=self.vow_label,
            create_missing_concepts=create_missing_concepts,
            get_rid_of_missing_awardlinks_awardee_titles=get_rid_of_missing_awardlinks_awardee_titles,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def set_concept(
        self,
        concept_kid: ConceptUnit,
        parent_way: WayTerm,
        get_rid_of_missing_awardlinks_awardee_titles: bool = None,
        create_missing_concepts: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        parent_way = to_way(parent_way, self.bridge)
        if LabelTerm(concept_kid.concept_label).is_label(self.bridge) is False:
            x_str = f"set_concept failed because '{concept_kid.concept_label}' is not a LabelTerm."
            raise InvalidPlanException(x_str)

        x_root_label = get_root_label_from_way(parent_way, self.bridge)
        if self.conceptroot.concept_label != x_root_label:
            exception_str = f"set_concept failed because parent_way '{parent_way}' has an invalid root label. Should be {self.conceptroot.concept_label}."
            raise InvalidPlanException(exception_str)

        concept_kid.bridge = self.bridge
        if concept_kid.vow_label != self.vow_label:
            concept_kid.vow_label = self.vow_label
        if concept_kid.fund_iota != self.fund_iota:
            concept_kid.fund_iota = self.fund_iota
        if not get_rid_of_missing_awardlinks_awardee_titles:
            concept_kid = self._get_filtered_awardlinks_concept(concept_kid)
        concept_kid.set_parent_way(parent_way=parent_way)

        # create any missing concepts
        if not create_missing_ancestors and self.concept_exists(parent_way) is False:
            x_str = f"set_concept failed because '{parent_way}' concept does not exist."
            raise InvalidPlanException(x_str)
        parent_way_concept = self.get_concept_obj(parent_way, create_missing_ancestors)
        if parent_way_concept.root is False:
            parent_way_concept
        parent_way_concept.add_kid(concept_kid)

        kid_way = self.make_way(parent_way, concept_kid.concept_label)
        if adoptees is not None:
            mass_sum = 0
            for adoptee_concept_label in adoptees:
                adoptee_way = self.make_way(parent_way, adoptee_concept_label)
                adoptee_concept = self.get_concept_obj(adoptee_way)
                mass_sum += adoptee_concept.mass
                new_adoptee_parent_way = self.make_way(kid_way, adoptee_concept_label)
                self.set_concept(adoptee_concept, new_adoptee_parent_way)
                self.edit_concept_attr(
                    new_adoptee_parent_way, mass=adoptee_concept.mass
                )
                self.del_concept_obj(adoptee_way)

            if bundling:
                self.edit_concept_attr(kid_way, mass=mass_sum)

        if create_missing_concepts:
            self._create_missing_concepts(way=kid_way)

    def _get_filtered_awardlinks_concept(self, x_concept: ConceptUnit) -> ConceptUnit:
        _awardlinks_to_delete = [
            _awardlink_awardee_title
            for _awardlink_awardee_title in x_concept.awardlinks.keys()
            if self.get_acctunit_group_titles_dict().get(_awardlink_awardee_title)
            is None
        ]
        for _awardlink_awardee_title in _awardlinks_to_delete:
            x_concept.awardlinks.pop(_awardlink_awardee_title)
        if x_concept.laborunit is not None:
            _laborlinks_to_delete = [
                _laborlink_labor_title
                for _laborlink_labor_title in x_concept.laborunit._laborlinks
                if self.get_acctunit_group_titles_dict().get(_laborlink_labor_title)
                is None
            ]
            for _laborlink_labor_title in _laborlinks_to_delete:
                x_concept.laborunit.del_laborlink(_laborlink_labor_title)
        return x_concept

    def _create_missing_concepts(self, way):
        self._set_concept_dict()
        posted_concept = self.get_concept_obj(way)

        for x_reason in posted_concept.reasonunits.values():
            self._create_conceptkid_if_empty(way=x_reason.rcontext)
            for premise_x in x_reason.premises.values():
                self._create_conceptkid_if_empty(way=premise_x.pstate)

    def _create_conceptkid_if_empty(self, way: WayTerm):
        if self.concept_exists(way) is False:
            self.add_concept(way)

    def del_concept_obj(self, way: WayTerm, del_children: bool = True):
        if way == self.conceptroot.get_concept_way():
            raise InvalidPlanException("Conceptroot cannot be deleted")
        parent_way = get_parent_way(way)
        if self.concept_exists(way):
            if not del_children:
                self._shift_concept_kids(x_way=way)
            parent_concept = self.get_concept_obj(parent_way)
            parent_concept.del_kid(get_tail_label(way, self.bridge))
        self.settle_plan()

    def _shift_concept_kids(self, x_way: WayTerm):
        parent_way = get_parent_way(x_way)
        d_temp_concept = self.get_concept_obj(x_way)
        for kid in d_temp_concept._kids.values():
            self.set_concept(kid, parent_way=parent_way)

    def set_owner_name(self, new_owner_name):
        self.owner_name = new_owner_name

    def edit_concept_label(self, old_way: WayTerm, new_concept_label: LabelTerm):
        if self.bridge in new_concept_label:
            exception_str = f"Cannot modify '{old_way}' because new_concept_label {new_concept_label} contains bridge {self.bridge}"
            raise InvalidLabelException(exception_str)
        if self.concept_exists(old_way) is False:
            raise InvalidPlanException(f"Concept {old_way=} does not exist")

        parent_way = get_parent_way(way=old_way)
        new_way = (
            self.make_way(new_concept_label)
            if parent_way == ""
            else self.make_way(parent_way, new_concept_label)
        )
        if old_way != new_way:
            if parent_way == "":
                self.conceptroot.set_concept_label(new_concept_label)
            else:
                self._non_root_concept_label_edit(
                    old_way, new_concept_label, parent_way
                )
            self._conceptroot_find_replace_way(old_way=old_way, new_way=new_way)

    def _non_root_concept_label_edit(
        self, old_way: WayTerm, new_concept_label: LabelTerm, parent_way: WayTerm
    ):
        x_concept = self.get_concept_obj(old_way)
        x_concept.set_concept_label(new_concept_label)
        x_concept.parent_way = parent_way
        concept_parent = self.get_concept_obj(get_parent_way(old_way))
        concept_parent._kids.pop(get_tail_label(old_way, self.bridge))
        concept_parent._kids[x_concept.concept_label] = x_concept

    def _conceptroot_find_replace_way(self, old_way: WayTerm, new_way: WayTerm):
        self.conceptroot.find_replace_way(old_way=old_way, new_way=new_way)

        concept_iter_list = [self.conceptroot]
        while concept_iter_list != []:
            listed_concept = concept_iter_list.pop()
            # add all concept_children in concept list
            if listed_concept._kids is not None:
                for concept_kid in listed_concept._kids.values():
                    concept_iter_list.append(concept_kid)
                    if is_sub_way(concept_kid.parent_way, sub_way=old_way):
                        concept_kid.parent_way = rebuild_way(
                            subj_way=concept_kid.parent_way,
                            old_way=old_way,
                            new_way=new_way,
                        )
                    concept_kid.find_replace_way(old_way=old_way, new_way=new_way)

    def _set_conceptattrholder_premise_ranges(
        self, x_conceptattrholder: ConceptAttrHolder
    ):
        premise_concept = self.get_concept_obj(x_conceptattrholder.reason_premise)
        x_conceptattrholder.set_premise_range_influenced_by_premise_concept(
            popen=premise_concept.begin,
            pnigh=premise_concept.close,
            premise_denom=premise_concept.denom,
        )

    def edit_reason(
        self,
        concept_way: WayTerm,
        reason_rcontext: WayTerm = None,
        reason_premise: WayTerm = None,
        popen: float = None,
        reason_pnigh: float = None,
        pdivisor: int = None,
    ):
        self.edit_concept_attr(
            concept_way=concept_way,
            reason_rcontext=reason_rcontext,
            reason_premise=reason_premise,
            popen=popen,
            reason_pnigh=reason_pnigh,
            pdivisor=pdivisor,
        )

    def edit_concept_attr(
        self,
        concept_way: WayTerm,
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
        task: bool = None,
        factunit: FactUnit = None,
        descendant_task_count: int = None,
        all_acct_cred: bool = None,
        all_acct_debt: bool = None,
        awardlink: AwardLink = None,
        awardlink_del: GroupTitle = None,
        is_expanded: bool = None,
        problem_bool: bool = None,
    ):
        if healerlink is not None:
            for x_healer_name in healerlink._healer_names:
                if self.get_acctunit_group_titles_dict().get(x_healer_name) is None:
                    exception_str = f"Concept cannot edit healerlink because group_title '{x_healer_name}' does not exist as group in Plan"
                    raise healerlink_group_title_Exception(exception_str)

        x_conceptattrholder = conceptattrholder_shop(
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
            descendant_task_count=descendant_task_count,
            all_acct_cred=all_acct_cred,
            all_acct_debt=all_acct_debt,
            awardlink=awardlink,
            awardlink_del=awardlink_del,
            is_expanded=is_expanded,
            task=task,
            factunit=factunit,
            problem_bool=problem_bool,
        )
        if reason_premise is not None:
            self._set_conceptattrholder_premise_ranges(x_conceptattrholder)
        x_concept = self.get_concept_obj(concept_way)
        x_concept._set_attrs_to_conceptunit(concept_attr=x_conceptattrholder)

    def get_agenda_dict(
        self, necessary_rcontext: WayTerm = None
    ) -> dict[WayTerm, ConceptUnit]:
        self.settle_plan()
        return {
            x_concept.get_concept_way(): x_concept
            for x_concept in self._concept_dict.values()
            if x_concept.is_agenda_concept(necessary_rcontext)
        }

    def get_all_tasks(self) -> dict[WayTerm, ConceptUnit]:
        self.settle_plan()
        all_concepts = self._concept_dict.values()
        return {
            x_concept.get_concept_way(): x_concept
            for x_concept in all_concepts
            if x_concept.task
        }

    def set_agenda_chore_complete(self, chore_way: WayTerm, rcontext: WayTerm):
        task_concept = self.get_concept_obj(chore_way)
        task_concept.set_factunit_to_complete(self.conceptroot.factunits[rcontext])

    def get_credit_ledger_debt_ledger(
        self,
    ) -> tuple[dict[str, float], dict[str, float]]:
        credit_ledger = {}
        debt_ledger = {}
        for x_acctunit in self.accts.values():
            credit_ledger[x_acctunit.acct_name] = x_acctunit.credit_score
            debt_ledger[x_acctunit.acct_name] = x_acctunit.debt_score
        return credit_ledger, debt_ledger

    def _allot_offtrack_fund(self):
        self._add_to_acctunits_fund_give_take(self._offtrack_fund)

    def get_acctunits_credit_score_sum(self) -> float:
        return sum(acctunit.get_credit_score() for acctunit in self.accts.values())

    def get_acctunits_debt_score_sum(self) -> float:
        return sum(acctunit.get_debt_score() for acctunit in self.accts.values())

    def _add_to_acctunits_fund_give_take(self, concept_fund_share: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        fund_give_allot = allot_scale(credor_ledger, concept_fund_share, self.fund_iota)
        fund_take_allot = allot_scale(debtor_ledger, concept_fund_share, self.fund_iota)
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

    def _add_to_acctunits_fund_agenda_give_take(self, concept_fund_share: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        fund_give_allot = allot_scale(credor_ledger, concept_fund_share, self.fund_iota)
        fund_take_allot = allot_scale(debtor_ledger, concept_fund_share, self.fund_iota)
        for x_acct_name, acct_fund_give in fund_give_allot.items():
            self.get_acct(x_acct_name).add_fund_agenda_give(acct_fund_give)
        for x_acct_name, acct_fund_take in fund_take_allot.items():
            self.get_acct(x_acct_name).add_fund_agenda_take(acct_fund_take)

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

    def _allot_fund_plan_agenda(self):
        for concept in self._concept_dict.values():
            # If there are no awardlines associated with concept
            # allot fund_share via general acctunit
            # cred ratio and debt ratio
            # if concept.is_agenda_concept() and concept._awardlines == {}:
            if concept.is_agenda_concept():
                if concept.awardheir_exists():
                    for x_awardline in concept._awardlines.values():
                        self.add_to_groupunit_fund_agenda_give_take(
                            group_title=x_awardline.awardee_title,
                            awardline_fund_give=x_awardline._fund_give,
                            awardline_fund_take=x_awardline._fund_take,
                        )
                else:
                    self._add_to_acctunits_fund_agenda_give_take(
                        concept.get_fund_share()
                    )

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
        x_acctunits_credit_score_sum = self.get_acctunits_credit_score_sum()
        x_acctunits_debt_score_sum = self.get_acctunits_debt_score_sum()
        for x_acctunit in self.accts.values():
            x_acctunit.set_fund_agenda_ratio_give_take(
                fund_agenda_ratio_give_sum=fund_agenda_ratio_give_sum,
                fund_agenda_ratio_take_sum=fund_agenda_ratio_take_sum,
                acctunits_credit_score_sum=x_acctunits_credit_score_sum,
                acctunits_debt_score_sum=x_acctunits_debt_score_sum,
            )

    def _reset_acctunit_fund_give_take(self):
        for acctunit in self.accts.values():
            acctunit.clear_fund_give_take()

    def concept_exists(self, way: WayTerm) -> bool:
        if way in {"", None}:
            return False
        root_way_concept_label = get_root_label_from_way(way, self.bridge)
        if root_way_concept_label != self.conceptroot.concept_label:
            return False

        labels = get_all_way_labels(way, bridge=self.bridge)
        root_way_concept_label = labels.pop(0)
        if labels == []:
            return True

        concept_label = labels.pop(0)
        x_concept = self.conceptroot.get_kid(concept_label)
        if x_concept is None:
            return False
        while labels != []:
            concept_label = labels.pop(0)
            x_concept = x_concept.get_kid(concept_label)
            if x_concept is None:
                return False
        return True

    def get_concept_obj(
        self, way: WayTerm, if_missing_create: bool = False
    ) -> ConceptUnit:
        if way is None:
            raise InvalidPlanException("get_concept_obj received way=None")
        if self.concept_exists(way) is False and not if_missing_create:
            raise InvalidPlanException(f"get_concept_obj failed. no concept at '{way}'")
        labelterms = get_all_way_labels(way, bridge=self.bridge)
        if len(labelterms) == 1:
            return self.conceptroot

        labelterms.pop(0)
        concept_label = labelterms.pop(0)
        x_concept = self.conceptroot.get_kid(concept_label, if_missing_create)
        while labelterms != []:
            x_concept = x_concept.get_kid(labelterms.pop(0), if_missing_create)

        return x_concept

    def get_concept_ranged_kids(
        self, concept_way: str, x_gogo_calc: float = None, x_stop_calc: float = None
    ) -> dict[ConceptUnit]:
        x_concept = self.get_concept_obj(concept_way)
        return x_concept.get_kids_in_range(x_gogo_calc, x_stop_calc)

    def get_inheritor_concept_list(
        self, math_way: WayTerm, inheritor_way: WayTerm
    ) -> list[ConceptUnit]:
        concept_ways = all_wayterms_between(math_way, inheritor_way)
        return [self.get_concept_obj(x_concept_way) for x_concept_way in concept_ways]

    def _set_concept_dict(self):
        concept_list = [self.get_concept_obj(to_way(self.vow_label, self.bridge))]
        while concept_list != []:
            x_concept = concept_list.pop()
            x_concept.clear_gogo_calc_stop_calc()
            for concept_kid in x_concept._kids.values():
                concept_kid.set_parent_way(x_concept.get_concept_way())
                concept_kid.set_level(x_concept._level)
                concept_list.append(concept_kid)
            self._concept_dict[x_concept.get_concept_way()] = x_concept
            for x_reason_rcontext in x_concept.reasonunits.keys():
                self._reason_rcontexts.add(x_reason_rcontext)

    def _raise_gogo_calc_stop_calc_exception(self, concept_way: WayTerm):
        exception_str = f"Error has occurred, Concept '{concept_way}' is having _gogo_calc and _stop_calc attributes set twice"
        raise _gogo_calc_stop_calc_Exception(exception_str)

    def _distribute_math_attrs(self, math_concept: ConceptUnit):
        single_range_concept_list = [math_concept]
        while single_range_concept_list != []:
            r_concept = single_range_concept_list.pop()
            if r_concept._range_evaluated:
                self._raise_gogo_calc_stop_calc_exception(r_concept.get_concept_way())
            if r_concept.is_math():
                r_concept._gogo_calc = r_concept.begin
                r_concept._stop_calc = r_concept.close
            else:
                parent_way = get_parent_way(r_concept.get_concept_way())
                parent_concept = self.get_concept_obj(parent_way)
                r_concept._gogo_calc = parent_concept._gogo_calc
                r_concept._stop_calc = parent_concept._stop_calc
                self._range_inheritors[r_concept.get_concept_way()] = (
                    math_concept.get_concept_way()
                )
            r_concept._mold_gogo_calc_stop_calc()

            single_range_concept_list.extend(iter(r_concept._kids.values()))

    def _set_concepttree_range_attrs(self):
        for x_concept in self._concept_dict.values():
            if x_concept.is_math():
                self._distribute_math_attrs(x_concept)

            if (
                not x_concept.is_kidless()
                and x_concept.get_kids_mass_sum() == 0
                and x_concept.mass != 0
            ):
                self._offtrack_kids_mass_set.add(x_concept.get_concept_way())

    def _set_groupunit_acctunit_funds(self, keep_exceptions):
        for x_concept in self._concept_dict.values():
            x_concept.set_awardheirs_fund_give_fund_take()
            if x_concept.is_kidless():
                self._set_ancestors_task_fund_keep_attrs(
                    x_concept.get_concept_way(), keep_exceptions
                )
                self._allot_fund_share(x_concept)

    def _set_ancestors_task_fund_keep_attrs(
        self, way: WayTerm, keep_exceptions: bool = False
    ):
        x_descendant_task_count = 0
        child_awardlines = None
        group_everyone = None
        ancestor_ways = get_ancestor_ways(way, self.bridge)
        keep_justified_by_problem = True
        healerlink_count = 0

        while ancestor_ways != []:
            youngest_way = ancestor_ways.pop(0)
            x_concept_obj = self.get_concept_obj(youngest_way)
            x_concept_obj.add_to_descendant_task_count(x_descendant_task_count)
            if x_concept_obj.is_kidless():
                x_concept_obj.set_kidless_awardlines()
                child_awardlines = x_concept_obj._awardlines
            else:
                x_concept_obj.set_awardlines(child_awardlines)

            if x_concept_obj._chore:
                x_descendant_task_count += 1

            if (
                group_everyone != False
                and x_concept_obj._all_acct_cred != False
                and x_concept_obj._all_acct_debt != False
                and x_concept_obj._awardheirs != {}
            ) or (
                group_everyone != False
                and x_concept_obj._all_acct_cred is False
                and x_concept_obj._all_acct_debt is False
            ):
                group_everyone = False
            elif group_everyone != False:
                group_everyone = True
            x_concept_obj._all_acct_cred = group_everyone
            x_concept_obj._all_acct_debt = group_everyone

            if x_concept_obj.healerlink.any_healer_name_exists():
                keep_justified_by_problem = False
                healerlink_count += 1
                self._sum_healerlink_share += x_concept_obj.get_fund_share()
            if x_concept_obj.problem_bool:
                keep_justified_by_problem = True

        if keep_justified_by_problem is False or healerlink_count > 1:
            if keep_exceptions:
                exception_str = f"ConceptUnit '{way}' cannot sponsor ancestor keeps."
                raise Exception_keeps_justified(exception_str)
            self._keeps_justified = False

    def _clear_concepttree_fund_and_active_status_attrs(self):
        for x_concept in self._concept_dict.values():
            x_concept.clear_awardlines()
            x_concept.clear_descendant_task_count()
            x_concept.clear_all_acct_cred_debt()

    def _set_kids_active_status_attrs(
        self, x_concept: ConceptUnit, parent_concept: ConceptUnit
    ):
        x_concept.set_reasonheirs(self._concept_dict, parent_concept._reasonheirs)
        x_concept.set_range_factheirs(self._concept_dict, self._range_inheritors)
        tt_count = self._tree_traverse_count
        x_concept.set_active_attrs(tt_count, self._groupunits, self.owner_name)

    def _allot_fund_share(self, concept: ConceptUnit):
        if concept.awardheir_exists():
            self._set_groupunits_fund_share(concept._awardheirs)
        elif concept.awardheir_exists() is False:
            self._add_to_acctunits_fund_give_take(concept.get_fund_share())

    def _create_groupunits_metrics(self):
        self._groupunits = {}
        for (
            group_title,
            acct_name_set,
        ) in self.get_acctunit_group_titles_dict().items():
            x_groupunit = groupunit_shop(group_title, bridge=self.bridge)
            for x_acct_name in acct_name_set:
                x_membership = self.get_acct(x_acct_name).get_membership(group_title)
                x_groupunit.set_membership(x_membership)
                self.set_groupunit(x_groupunit)

    def _set_acctunit_groupunit_respect_ledgers(self):
        self.credor_respect = validate_respect_num(self.credor_respect)
        self.debtor_respect = validate_respect_num(self.debtor_respect)
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        credor_allot = allot_scale(credor_ledger, self.credor_respect, self.respect_bit)
        debtor_allot = allot_scale(debtor_ledger, self.debtor_respect, self.respect_bit)
        for x_acct_name, acct_credor_pool in credor_allot.items():
            self.get_acct(x_acct_name).set_credor_pool(acct_credor_pool)
        for x_acct_name, acct_debtor_pool in debtor_allot.items():
            self.get_acct(x_acct_name).set_debtor_pool(acct_debtor_pool)
        self._create_groupunits_metrics()
        self._reset_acctunit_fund_give_take()

    def _clear_concept_dict_and_plan_obj_settle_attrs(self):
        self._concept_dict = {self.conceptroot.get_concept_way(): self.conceptroot}
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

    def _set_concepttree_factheirs_laborheirs_awardheirs(self):
        for x_concept in get_sorted_concept_list(list(self._concept_dict.values())):
            if x_concept.root:
                x_concept.set_factheirs(x_concept.factunits)
                x_concept.set_conceptroot_inherit_reasonheirs()
                x_concept.set_laborheir(None, self._groupunits)
                x_concept.inherit_awardheirs()
            else:
                parent_concept = self.get_concept_obj(x_concept.parent_way)
                x_concept.set_factheirs(parent_concept._factheirs)
                x_concept.set_laborheir(parent_concept._laborheir, self._groupunits)
                x_concept.inherit_awardheirs(parent_concept._awardheirs)
            x_concept.set_awardheirs_fund_give_fund_take()

    def settle_plan(self, keep_exceptions: bool = False):
        self._clear_concept_dict_and_plan_obj_settle_attrs()
        self._set_concept_dict()
        self._set_concepttree_range_attrs()
        self._set_acctunit_groupunit_respect_ledgers()
        self._clear_acctunit_fund_attrs()
        self._clear_concepttree_fund_and_active_status_attrs()
        self._set_concepttree_factheirs_laborheirs_awardheirs()

        max_count = self.max_tree_traverse
        while not self._rational and self._tree_traverse_count < max_count:
            self._set_concepttree_active_status_attrs()
            self._set_rational_attr()
            self._tree_traverse_count += 1

        self._set_concepttree_fund_attrs(self.conceptroot)
        self._set_groupunit_acctunit_funds(keep_exceptions)
        self._set_acctunit_fund_related_attrs()
        self._set_plan_keep_attrs()

    def _set_concepttree_active_status_attrs(self):
        for x_concept in get_sorted_concept_list(list(self._concept_dict.values())):
            if x_concept.root:
                tt_count = self._tree_traverse_count
                root_concept = self.conceptroot
                root_concept.set_active_attrs(
                    tt_count, self._groupunits, self.owner_name
                )
            else:
                parent_concept = self.get_concept_obj(x_concept.parent_way)
                self._set_kids_active_status_attrs(x_concept, parent_concept)

    def _set_concepttree_fund_attrs(self, root_concept: ConceptUnit):
        root_concept.set_fund_attr(0, self.fund_pool, self.fund_pool)
        # no function recursion, recursion by iterateing over list that can be added to by iterations
        cache_concept_list = [root_concept]
        while cache_concept_list != []:
            parent_concept = cache_concept_list.pop()
            kids_concepts = parent_concept._kids.items()
            x_ledger = {x_way: concept_kid.mass for x_way, concept_kid in kids_concepts}
            parent_fund_num = parent_concept._fund_cease - parent_concept._fund_onset
            alloted_fund_num = allot_scale(x_ledger, parent_fund_num, self.fund_iota)

            fund_onset = None
            fund_cease = None
            for x_concept in parent_concept._kids.values():
                if fund_onset is None:
                    fund_onset = parent_concept._fund_onset
                    fund_cease = fund_onset + alloted_fund_num.get(
                        x_concept.concept_label
                    )
                else:
                    fund_onset = fund_cease
                    fund_cease += alloted_fund_num.get(x_concept.concept_label)
                x_concept.set_fund_attr(fund_onset, fund_cease, self.fund_pool)
                cache_concept_list.append(x_concept)

    def _set_rational_attr(self):
        any_concept_active_status_has_altered = False
        for concept in self._concept_dict.values():
            if concept._active_hx.get(self._tree_traverse_count) is not None:
                any_concept_active_status_has_altered = True

        if any_concept_active_status_has_altered is False:
            self._rational = True

    def _set_acctunit_fund_related_attrs(self):
        self.set_offtrack_fund()
        self._allot_offtrack_fund()
        self._allot_fund_plan_agenda()
        self._allot_groupunits_fund()
        self._set_acctunits_fund_agenda_ratios()

    def _set_plan_keep_attrs(self):
        self._set_keep_dict()
        self._healers_dict = self._get_healers_dict()
        self._keeps_buildable = self._get_buildable_keeps()

    def _set_keep_dict(self):
        if self._keeps_justified is False:
            self._sum_healerlink_share = 0
        for x_concept in self._concept_dict.values():
            if self._sum_healerlink_share == 0:
                x_concept._healerlink_ratio = 0
            else:
                x_sum = self._sum_healerlink_share
                x_concept._healerlink_ratio = x_concept.get_fund_share() / x_sum
            if self._keeps_justified and x_concept.healerlink.any_healer_name_exists():
                self._keep_dict[x_concept.get_concept_way()] = x_concept

    def _get_healers_dict(self) -> dict[HealerName, dict[WayTerm, ConceptUnit]]:
        _healers_dict = {}
        for x_keep_way, x_keep_concept in self._keep_dict.items():
            for x_healer_name in x_keep_concept.healerlink._healer_names:
                x_groupunit = self.get_groupunit(x_healer_name)
                for x_acct_name in x_groupunit._memberships.keys():
                    if _healers_dict.get(x_acct_name) is None:
                        _healers_dict[x_acct_name] = {x_keep_way: x_keep_concept}
                    else:
                        healer_dict = _healers_dict.get(x_acct_name)
                        healer_dict[x_keep_way] = x_keep_concept
        return _healers_dict

    def _get_buildable_keeps(self) -> bool:
        return all(
            wayterm_valid_dir_path(keep_way, self.bridge) != False
            for keep_way in self._keep_dict.keys()
        )

    def _clear_acctunit_fund_attrs(self):
        self._reset_groupunits_fund_give_take()
        self._reset_acctunit_fund_give_take()

    def get_concept_tree_ordered_way_list(
        self, no_range_descendants: bool = False
    ) -> list[WayTerm]:
        concept_list = list(self.get_concept_dict().values())
        label_dict = {
            concept.get_concept_way().lower(): concept.get_concept_way()
            for concept in concept_list
        }
        label_lowercase_ordered_list = sorted(list(label_dict))
        label_orginalcase_ordered_list = [
            label_dict[label_l] for label_l in label_lowercase_ordered_list
        ]

        list_x = []
        for way in label_orginalcase_ordered_list:
            if not no_range_descendants:
                list_x.append(way)
            else:
                anc_list = get_ancestor_ways(way=way)
                if len(anc_list) == 1:
                    list_x.append(way)
                elif len(anc_list) == 2:
                    if (
                        self.conceptroot.begin is None
                        and self.conceptroot.close is None
                    ):
                        list_x.append(way)
                else:
                    parent_concept = self.get_concept_obj(way=anc_list[1])
                    if parent_concept.begin is None and parent_concept.close is None:
                        list_x.append(way)

        return list_x

    def get_factunits_dict(self) -> dict[str, str]:
        x_dict = {}
        if self.conceptroot.factunits is not None:
            for fact_way, fact_obj in self.conceptroot.factunits.items():
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
            "tally": self.tally,
            "fund_pool": self.fund_pool,
            "fund_iota": self.fund_iota,
            "respect_bit": self.respect_bit,
            "penny": self.penny,
            "owner_name": self.owner_name,
            "vow_label": self.vow_label,
            "max_tree_traverse": self.max_tree_traverse,
            "bridge": self.bridge,
            "conceptroot": self.conceptroot.get_dict(),
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

    def set_dominate_task_concept(self, concept_kid: ConceptUnit):
        concept_kid.task = True
        self.set_concept(
            concept_kid=concept_kid,
            parent_way=self.make_way(concept_kid.parent_way),
            get_rid_of_missing_awardlinks_awardee_titles=True,
            create_missing_concepts=True,
        )

    def set_offtrack_fund(self) -> float:
        mass_set = self._offtrack_kids_mass_set
        self._offtrack_fund = sum(
            self.get_concept_obj(x_wayterm).get_fund_share() for x_wayterm in mass_set
        )


def planunit_shop(
    owner_name: OwnerName = None,
    vow_label: VowLabel = None,
    bridge: str = None,
    fund_pool: FundNum = None,
    fund_iota: FundIota = None,
    respect_bit: BitNum = None,
    penny: PennyNum = None,
    tally: float = None,
) -> PlanUnit:
    owner_name = "" if owner_name is None else owner_name
    vow_label = get_default_vow_label() if vow_label is None else vow_label
    x_plan = PlanUnit(
        owner_name=owner_name,
        tally=get_1_if_None(tally),
        vow_label=vow_label,
        accts=get_empty_dict_if_None(),
        _groupunits={},
        bridge=default_bridge_if_None(bridge),
        credor_respect=validate_respect_num(),
        debtor_respect=validate_respect_num(),
        fund_pool=validate_fund_pool(fund_pool),
        fund_iota=default_fund_iota_if_None(fund_iota),
        respect_bit=default_RespectBit_if_None(respect_bit),
        penny=filter_penny(penny),
        _concept_dict=get_empty_dict_if_None(),
        _keep_dict=get_empty_dict_if_None(),
        _healers_dict=get_empty_dict_if_None(),
        _keeps_justified=get_False_if_None(),
        _keeps_buildable=get_False_if_None(),
        _sum_healerlink_share=get_0_if_None(),
        _offtrack_kids_mass_set=set(),
        _reason_rcontexts=set(),
        _range_inheritors={},
    )
    x_plan.conceptroot = conceptunit_shop(
        root=True,
        _uid=1,
        _level=0,
        vow_label=x_plan.vow_label,
        bridge=x_plan.bridge,
        fund_iota=x_plan.fund_iota,
        parent_way="",
    )
    x_plan.set_max_tree_traverse(3)
    x_plan._rational = False
    return x_plan


def get_from_json(x_plan_json: str) -> PlanUnit:
    return get_from_dict(get_dict_from_json(x_plan_json))


def get_from_dict(plan_dict: dict) -> PlanUnit:
    x_plan = planunit_shop()
    x_plan.set_owner_name(obj_from_plan_dict(plan_dict, "owner_name"))
    x_plan.tally = obj_from_plan_dict(plan_dict, "tally")
    x_plan.set_max_tree_traverse(obj_from_plan_dict(plan_dict, "max_tree_traverse"))
    x_plan.vow_label = obj_from_plan_dict(plan_dict, "vow_label")
    x_plan.conceptroot.concept_label = obj_from_plan_dict(plan_dict, "vow_label")
    plan_bridge = obj_from_plan_dict(plan_dict, "bridge")
    x_plan.bridge = default_bridge_if_None(plan_bridge)
    x_plan.fund_pool = validate_fund_pool(obj_from_plan_dict(plan_dict, "fund_pool"))
    x_plan.fund_iota = default_fund_iota_if_None(
        obj_from_plan_dict(plan_dict, "fund_iota")
    )
    x_plan.respect_bit = default_RespectBit_if_None(
        obj_from_plan_dict(plan_dict, "respect_bit")
    )
    x_plan.penny = filter_penny(obj_from_plan_dict(plan_dict, "penny"))
    x_plan.credor_respect = obj_from_plan_dict(plan_dict, "credor_respect")
    x_plan.debtor_respect = obj_from_plan_dict(plan_dict, "debtor_respect")
    x_plan.last_pack_id = obj_from_plan_dict(plan_dict, "last_pack_id")
    x_bridge = x_plan.bridge
    x_accts = obj_from_plan_dict(plan_dict, "accts", x_bridge).values()
    for x_acctunit in x_accts:
        x_plan.set_acctunit(x_acctunit)
    create_conceptroot_from_plan_dict(x_plan, plan_dict)
    return x_plan


def create_conceptroot_from_plan_dict(x_plan: PlanUnit, plan_dict: dict):
    conceptroot_dict = plan_dict.get("conceptroot")
    x_plan.conceptroot = conceptunit_shop(
        root=True,
        concept_label=x_plan.vow_label,
        parent_way="",
        _level=0,
        _uid=get_obj_from_concept_dict(conceptroot_dict, "_uid"),
        mass=get_obj_from_concept_dict(conceptroot_dict, "mass"),
        begin=get_obj_from_concept_dict(conceptroot_dict, "begin"),
        close=get_obj_from_concept_dict(conceptroot_dict, "close"),
        numor=get_obj_from_concept_dict(conceptroot_dict, "numor"),
        denom=get_obj_from_concept_dict(conceptroot_dict, "denom"),
        morph=get_obj_from_concept_dict(conceptroot_dict, "morph"),
        gogo_want=get_obj_from_concept_dict(conceptroot_dict, "gogo_want"),
        stop_want=get_obj_from_concept_dict(conceptroot_dict, "stop_want"),
        problem_bool=get_obj_from_concept_dict(conceptroot_dict, "problem_bool"),
        reasonunits=get_obj_from_concept_dict(conceptroot_dict, "reasonunits"),
        laborunit=get_obj_from_concept_dict(conceptroot_dict, "laborunit"),
        healerlink=get_obj_from_concept_dict(conceptroot_dict, "healerlink"),
        factunits=get_obj_from_concept_dict(conceptroot_dict, "factunits"),
        awardlinks=get_obj_from_concept_dict(conceptroot_dict, "awardlinks"),
        _is_expanded=get_obj_from_concept_dict(conceptroot_dict, "_is_expanded"),
        bridge=x_plan.bridge,
        vow_label=x_plan.vow_label,
        fund_iota=default_fund_iota_if_None(x_plan.fund_iota),
    )
    create_conceptroot_kids_from_dict(x_plan, conceptroot_dict)


def create_conceptroot_kids_from_dict(x_plan: PlanUnit, conceptroot_dict: dict):
    to_evaluate_concept_dicts = []
    parent_way_str = "parent_way"
    # for every kid dict, set parent_way in dict, add to to_evaluate_list
    for x_dict in get_obj_from_concept_dict(conceptroot_dict, "_kids").values():
        x_dict[parent_way_str] = x_plan.vow_label
        to_evaluate_concept_dicts.append(x_dict)

    while to_evaluate_concept_dicts != []:
        concept_dict = to_evaluate_concept_dicts.pop(0)
        # for every kid dict, set parent_way in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_concept_dict(concept_dict, "_kids").values():
            parent_way = get_obj_from_concept_dict(concept_dict, parent_way_str)
            kid_concept_label = get_obj_from_concept_dict(concept_dict, "concept_label")
            kid_dict[parent_way_str] = x_plan.make_way(parent_way, kid_concept_label)
            to_evaluate_concept_dicts.append(kid_dict)
        x_conceptkid = conceptunit_shop(
            concept_label=get_obj_from_concept_dict(concept_dict, "concept_label"),
            mass=get_obj_from_concept_dict(concept_dict, "mass"),
            _uid=get_obj_from_concept_dict(concept_dict, "_uid"),
            begin=get_obj_from_concept_dict(concept_dict, "begin"),
            close=get_obj_from_concept_dict(concept_dict, "close"),
            numor=get_obj_from_concept_dict(concept_dict, "numor"),
            denom=get_obj_from_concept_dict(concept_dict, "denom"),
            morph=get_obj_from_concept_dict(concept_dict, "morph"),
            gogo_want=get_obj_from_concept_dict(concept_dict, "gogo_want"),
            stop_want=get_obj_from_concept_dict(concept_dict, "stop_want"),
            task=get_obj_from_concept_dict(concept_dict, "task"),
            problem_bool=get_obj_from_concept_dict(concept_dict, "problem_bool"),
            reasonunits=get_obj_from_concept_dict(concept_dict, "reasonunits"),
            laborunit=get_obj_from_concept_dict(concept_dict, "laborunit"),
            healerlink=get_obj_from_concept_dict(concept_dict, "healerlink"),
            awardlinks=get_obj_from_concept_dict(concept_dict, "awardlinks"),
            factunits=get_obj_from_concept_dict(concept_dict, "factunits"),
            _is_expanded=get_obj_from_concept_dict(concept_dict, "_is_expanded"),
        )
        x_plan.set_concept(x_conceptkid, parent_way=concept_dict[parent_way_str])


def obj_from_plan_dict(
    x_dict: dict[str, dict], dict_key: str, _bridge: str = None
) -> any:
    if dict_key == "accts":
        return acctunits_get_from_dict(x_dict[dict_key], _bridge)
    elif dict_key == "_max_tree_traverse":
        return (
            x_dict[dict_key]
            if x_dict.get(dict_key) is not None
            else max_tree_traverse_default()
        )
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else None


def get_dict_of_plan_from_dict(x_dict: dict[str, dict]) -> dict[str, PlanUnit]:
    planunits = {}
    for planunit_dict in x_dict.values():
        x_plan = get_from_dict(plan_dict=planunit_dict)
        planunits[x_plan.owner_name] = x_plan
    return planunits


def get_sorted_concept_list(x_list: list[ConceptUnit]) -> list[ConceptUnit]:
    x_list.sort(key=lambda x: x.get_concept_way(), reverse=False)
    return x_list
