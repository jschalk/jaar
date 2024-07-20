from src._instrument.python import (
    get_json_from_dict,
    get_dict_from_json,
    get_1_if_None,
    get_0_if_None,
    get_False_if_None,
    get_empty_dict_if_none,
)
from src._road.finance import (
    valid_finance_ratio,
    default_bit_if_none,
    default_penny_if_none,
    default_fund_coin_if_none,
    validate_fund_pool,
    BitNum,
    PennyNum,
    FundCoin,
    FundNum,
    allot_scale,
    validate_respect_num,
)
from src._road.jaar_config import max_tree_traverse_default
from src._road.road import (
    get_parent_road,
    is_sub_road,
    road_validate,
    rebuild_road,
    get_terminus_node,
    get_root_node_from_road,
    find_replace_road_key_dict,
    get_ancestor_roads,
    get_default_real_id_roadnode,
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
    RealID,
    roadunit_valid_dir_path,
)

from src.bud.acct import AcctUnit, acctunits_get_from_dict, acctunit_shop
from src.bud.lobby import AwardLink, LobbyID, LobbyBox, lobbybox_shop, lobbyship_shop
from src.bud.healer import HealerHold
from src.bud.reason_idea import FactUnit, FactUnit, ReasonUnit, RoadUnit, factunit_shop
from src.bud.reason_doer import DoerUnit
from src.bud.tree_metrics import TreeMetrics, treemetrics_shop
from src.bud.lemma import lemmas_shop, Lemmas
from src.bud.origin import originunit_get_from_dict, originunit_shop, OriginUnit
from src.bud.idea import (
    IdeaUnit,
    ideaunit_shop,
    ideaattrfilter_shop,
    IdeaAttrFilter,
    get_obj_from_idea_dict,
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


class Exception_econs_justified(Exception):
    pass


class _bit_RatioException(Exception):
    pass


class _last_gift_idException(Exception):
    pass


class healerhold_lobby_id_Exception(Exception):
    pass


@dataclass
class BudUnit:
    _real_id: RealID = None
    _owner_id: OwnerID = None
    _last_gift_id: int = None
    _weight: float = None
    _accts: dict[AcctID, AcctUnit] = None
    _idearoot: IdeaUnit = None
    _max_tree_traverse: int = None
    _road_delimiter: str = None
    _fund_pool: FundNum = None
    _fund_coin: FundCoin = None
    _bit: BitNum = None
    _penny: PennyNum = None
    _monetary_desc: str = None
    _credor_respect: int = None
    _debtor_respect: int = None
    _originunit: OriginUnit = None  # In job buds this shows source
    # settle_bud Calculated field begin
    _idea_dict: dict[RoadUnit, IdeaUnit] = None
    _econ_dict: dict[RoadUnit, IdeaUnit] = None
    _healers_dict: dict[HealerID, dict[RoadUnit, IdeaUnit]] = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _econs_justified: bool = None
    _econs_buildable: bool = None
    _sum_healerhold_share: bool = None
    _lobbyboxs: dict[LobbyID, LobbyBox] = None
    _offtrack_kids_weight_set: set[RoadUnit] = None
    _offtrack_fund: float = None
    # settle_bud Calculated field end

    def del_last_gift_id(self):
        self._last_gift_id = None

    def set_last_gift_id(self, x_last_gift_id: int):
        if self._last_gift_id is not None and x_last_gift_id < self._last_gift_id:
            raise _last_gift_idException(
                f"Cannot set _last_gift_id to {x_last_gift_id} because it is less than {self._last_gift_id}."
            )
        self._last_gift_id = x_last_gift_id

    def set_monetary_desc(self, x_monetary_desc: str):
        self._monetary_desc = x_monetary_desc

    def set_fund_pool(self, x_fund_pool):
        self._fund_pool = validate_fund_pool(x_fund_pool)

    def set_acct_respect(self, x_acct_pool: int):
        self.set_credor_respect(x_acct_pool)
        self.set_debtor_resepect(x_acct_pool)
        self.set_fund_pool(x_acct_pool)

    def set_credor_respect(self, new_credor_respect: int):
        if valid_finance_ratio(new_credor_respect, self._bit) is False:
            raise _bit_RatioException(
                f"Bud '{self._owner_id}' cannot set _credor_respect='{new_credor_respect}'. It is not divisible by bit '{self._bit}'"
            )
        self._credor_respect = new_credor_respect

    def set_debtor_resepect(self, new_debtor_respect: int):
        if valid_finance_ratio(new_debtor_respect, self._bit) is False:
            raise _bit_RatioException(
                f"Bud '{self._owner_id}' cannot set _debtor_respect='{new_debtor_respect}'. It is not divisible by bit '{self._bit}'"
            )
        self._debtor_respect = new_debtor_respect

    def _correct_any_debtor_bit_issues(self):
        if self.get_acctunits_debtor_weight_sum() != self._debtor_respect:
            missing_debtor_weight = (
                self._debtor_respect - self.get_acctunits_debtor_weight_sum()
            )
            if len(self._accts) > 0:
                acctunits = list(self._accts.values())
                # accts_count = len(self._accts)
                # bit_count = missing_debtor_weight / self._bit
                # if bit_count <= accts_count:
                for _ in range(0, missing_debtor_weight, self._bit):
                    x_acctunit = acctunits.pop()
                    x_acctunit.set_debtor_weight(x_acctunit.debtor_weight + self._bit)

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
        return road_validate(x_road, self._road_delimiter, self._real_id)

    def make_l1_road(self, l1_node: RoadNode):
        return self.make_road(self._real_id, l1_node)

    def set_road_delimiter(self, new_road_delimiter: str):
        self.settle_bud()
        if self._road_delimiter != new_road_delimiter:
            for x_idea_road in self._idea_dict.keys():
                if is_string_in_road(new_road_delimiter, x_idea_road):
                    raise NewDelimiterException(
                        f"Cannot modify delimiter to '{new_road_delimiter}' because it already exists an idea label '{x_idea_road}'"
                    )

            # modify all road attributes in ideaunits
            self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)
            for x_idea in self._idea_dict.values():
                x_idea.set_road_delimiter(self._road_delimiter)

    def set_real_id(self, real_id: str):
        old_real_id = copy_deepcopy(self._real_id)
        self._real_id = real_id

        self.settle_bud()
        for idea_obj in self._idea_dict.values():
            idea_obj._bud_real_id = self._real_id

        self.edit_idea_label(old_road=old_real_id, new_label=self._real_id)
        self.settle_bud()

    def set_max_tree_traverse(self, x_int: int):
        if x_int < 2 or not float(x_int).is_integer():
            raise InvalidBudException(
                f"set_max_tree_traverse: input '{x_int}' must be number that is 2 or greater"
            )
        else:
            self._max_tree_traverse = x_int

    def _get_relevant_roads(self, roads: dict[RoadUnit,]) -> dict[RoadUnit, str]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for road_x in roads:
            to_evaluate_list.append(road_x)
            to_evaluate_hx_dict[road_x] = "to_evaluate"
        evaluated_roads = {}

        # tree_metrics = self.get_tree_metrics()
        # while roads_to_evaluate != [] and count_x <= tree_metrics.node_count:
        # transited because count_x might be wrong thing to measure
        # nice to avoid infinite loops from programming errors though...
        while to_evaluate_list != []:
            road_x = to_evaluate_list.pop()
            x_idea = self.get_idea_obj(road_x)
            for reasonunit_obj in x_idea._reasonunits.values():
                reason_base = reasonunit_obj.base
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=reason_base,
                    road_type="reasonunit_base",
                )

            if x_idea._numeric_road is not None:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=x_idea._numeric_road,
                    road_type="numeric_road",
                )

            if x_idea._range_source_road is not None:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=x_idea._range_source_road,
                    road_type="range_source_road",
                )

            forefather_roads = get_forefather_roads(road_x)
            for forefather_road in forefather_roads:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=forefather_road,
                    road_type="forefather",
                )

            evaluated_roads[road_x] = -1
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
                ru_base_idea = self.get_idea_obj(to_evaluate_road)
                for descendant_road in ru_base_idea.get_descendant_roads_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_road=descendant_road,
                        road_type="reasonunit_descendant",
                    )

    def all_ideas_relevant_to_pledge_idea(self, road: RoadUnit) -> bool:
        pledge_idea_assoc_set = set(self._get_relevant_roads({road}))
        all_ideas_set = set(self.get_idea_tree_ordered_road_list())
        return all_ideas_set == all_ideas_set.intersection(pledge_idea_assoc_set)

    def get_awardlinks_metrics(self) -> dict[LobbyID, AwardLink]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.awardlinks_metrics

    def add_to_lobbybox_fund_give_take(
        self,
        lobby_id: LobbyID,
        awardheir_fund_give: float,
        awardheir_fund_take: float,
    ):
        x_lobbybox = self.get_lobbybox(lobby_id)
        if x_lobbybox is not None:
            x_lobbybox._fund_give += awardheir_fund_give
            x_lobbybox._fund_take += awardheir_fund_take

    def add_to_lobbybox_fund_agenda_give_take(
        self,
        lobby_id: LobbyID,
        awardline_fund_give: float,
        awardline_fund_take: float,
    ):
        x_lobbybox = self.get_lobbybox(lobby_id)
        if awardline_fund_give is not None and awardline_fund_take is not None:
            x_lobbybox._fund_agenda_give += awardline_fund_give
            x_lobbybox._fund_agenda_take += awardline_fund_take

    def add_to_acctunit_fund_give_take(
        self,
        acctunit_acct_id: AcctID,
        fund_give,
        fund_take: float,
        bud_agenda_cred: float,
        bud_agenda_debt: float,
    ):
        for acctunit in self._accts.values():
            if acctunit.acct_id == acctunit_acct_id:
                acctunit.add_fund_give_take(
                    fund_give=fund_give,
                    fund_take=fund_take,
                    bud_agenda_cred=bud_agenda_cred,
                    bud_agenda_debt=bud_agenda_debt,
                )

    def del_acctunit(self, acct_id: str):
        self._accts.pop(acct_id)

    def add_acctunit(
        self, acct_id: AcctID, credor_weight: int = None, debtor_weight: int = None
    ):
        acctunit = acctunit_shop(
            acct_id=acct_id,
            credor_weight=credor_weight,
            debtor_weight=debtor_weight,
            _road_delimiter=self._road_delimiter,
        )
        self.set_acctunit(acctunit)

    def set_acctunit(self, x_acctunit: AcctUnit, auto_set_lobbyship: bool = True):
        if x_acctunit._road_delimiter != self._road_delimiter:
            x_acctunit._road_delimiter = self._road_delimiter
        if x_acctunit._bit != self._bit:
            x_acctunit._bit = self._bit
        if auto_set_lobbyship and x_acctunit.lobbyships_exist() is False:
            x_acctunit.add_lobbyship(x_acctunit.acct_id)
        self._accts[x_acctunit.acct_id] = x_acctunit

    def acct_exists(self, acct_id: AcctID) -> bool:
        return self.get_acct(acct_id) is not None

    def edit_acctunit(
        self, acct_id: AcctID, credor_weight: int = None, debtor_weight: int = None
    ):
        if self._accts.get(acct_id) is None:
            raise AcctMissingException(f"AcctUnit '{acct_id}' does not exist.")
        x_acctunit = self.get_acct(acct_id)
        if credor_weight is not None:
            x_acctunit.set_credor_weight(credor_weight)
        if debtor_weight is not None:
            x_acctunit.set_debtor_weight(debtor_weight)
        self.set_acctunit(x_acctunit)

    def get_acct(self, acct_id: AcctID) -> AcctUnit:
        return self._accts.get(acct_id)

    def get_charunit_lobby_ids_dict(self) -> dict[LobbyID, set[AcctID]]:
        x_dict = {}
        for x_acctunit in self._accts.values():
            for x_lobby_id in x_acctunit._lobbyships.keys():
                acct_id_set = x_dict.get(x_lobby_id)
                if acct_id_set is None:
                    x_dict[x_lobby_id] = {x_acctunit.acct_id}
                else:
                    acct_id_set.add(x_acctunit.acct_id)
                    x_dict[x_lobby_id] = acct_id_set
        return x_dict

    def set_lobbybox(self, x_lobbybox: LobbyBox):
        self._lobbyboxs[x_lobbybox.lobby_id] = x_lobbybox

    def lobbybox_exists(self, lobby_id: LobbyID) -> bool:
        return self._lobbyboxs.get(lobby_id) != None

    def get_lobbybox(self, x_lobby_id: LobbyID) -> LobbyBox:
        return self._lobbyboxs.get(x_lobby_id)

    def create_symmetry_lobbybox(self, x_lobby_id: LobbyID) -> LobbyBox:
        x_lobbybox = lobbybox_shop(x_lobby_id)
        for x_acctunit in self._accts.values():
            x_lobbyship = lobbyship_shop(
                lobby_id=x_lobby_id,
                credor_weight=x_acctunit.credor_weight,
                debtor_weight=x_acctunit.debtor_weight,
                _acct_id=x_acctunit.acct_id,
            )
            x_lobbybox.set_lobbyship(x_lobbyship)
        return x_lobbybox

    def get_tree_traverse_generated_lobbyboxs(self) -> set[LobbyID]:
        x_acctunit_lobby_ids = set(self.get_charunit_lobby_ids_dict().keys())
        all_lobby_ids = set(self._lobbyboxs.keys())
        return all_lobby_ids.difference(x_acctunit_lobby_ids)

    def clear_acctunits_lobbyships(self):
        for x_acctunit in self._accts.values():
            x_acctunit.clear_lobbyships()

    def _is_idea_rangeroot(self, idea_road: RoadUnit) -> bool:
        if self._real_id == idea_road:
            raise InvalidBudException(
                "its difficult to foresee a scenario where idearoot is rangeroot"
            )
        parent_road = get_parent_road(idea_road)
        parent_idea = self.get_idea_obj(parent_road)
        x_idea = self.get_idea_obj(idea_road)
        return x_idea._numeric_road is None and not parent_idea.is_arithmetic()

    def _get_rangeroot_factunits(self) -> list[FactUnit]:
        return [
            fact
            for fact in self._idearoot._factunits.values()
            if fact.open is not None
            and fact.nigh is not None
            and self._is_idea_rangeroot(idea_road=fact.base)
        ]

    def _get_rangeroot_1stlevel_associates(
        self, ranged_factunits: list[IdeaUnit]
    ) -> Lemmas:
        x_lemmas = lemmas_shop()
        # lemma_ideas = {}
        for fact in ranged_factunits:
            fact_idea = self.get_idea_obj(fact.base)
            for kid in fact_idea._kids.values():
                x_lemmas.eval(x_idea=kid, src_fact=fact, src_idea=fact_idea)

            if fact_idea._range_source_road is not None:
                x_lemmas.eval(
                    x_idea=self.get_idea_obj(fact_idea._range_source_road),
                    src_fact=fact,
                    src_idea=fact_idea,
                )
        return x_lemmas

    def _get_lemma_factunits(self) -> dict[RoadUnit, FactUnit]:
        # get all range-root first level kids and range_source_road
        x_lemmas = self._get_rangeroot_1stlevel_associates(
            self._get_rangeroot_factunits()
        )

        # Now get associates (all their descendants and range_source_roads)
        lemma_factunits = {}  # fact.base : factUnit
        count_x = 0
        while count_x < 10000 and x_lemmas.is_lemmas_evaluated() is False:
            count_x += 1
            if count_x == 9998:
                raise InvalidBudException("lemma loop failed")

            y_lemma = x_lemmas.get_unevaluated_lemma()
            lemma_idea = y_lemma.x_idea
            fact_x = y_lemma.calc_fact

            road_x = self.make_road(lemma_idea._parent_road, lemma_idea._label)
            lemma_factunits[road_x] = fact_x

            for kid2 in lemma_idea._kids.values():
                x_lemmas.eval(x_idea=kid2, src_fact=fact_x, src_idea=lemma_idea)
            if lemma_idea._range_source_road not in [None, ""]:
                x_lemmas.eval(
                    x_idea=self.get_idea_obj(lemma_idea._range_source_road),
                    src_fact=fact_x,
                    src_idea=lemma_idea,
                )

        return lemma_factunits

    def set_fact(
        self,
        base: RoadUnit,
        pick: RoadUnit = None,
        open: float = None,
        nigh: float = None,
        create_missing_ideas: bool = None,
    ):
        pick = base if pick is None else pick
        if create_missing_ideas:
            self._set_ideakid_if_empty(road=base)
            self._set_ideakid_if_empty(road=pick)

        self._execute_tree_traverse()
        fact_base_idea = self.get_idea_obj(base)
        x_idearoot = self.get_idea_obj(self._real_id)
        x_open = None
        if nigh is not None and open is None:
            x_open = x_idearoot._factunits.get(base).open
        else:
            x_open = open
        x_nigh = None
        if open is not None and nigh is None:
            x_nigh = x_idearoot._factunits.get(base).nigh
        else:
            x_nigh = nigh
        x_factunit = factunit_shop(base=base, pick=pick, open=x_open, nigh=x_nigh)

        if fact_base_idea.is_arithmetic() is False:
            x_idearoot.set_factunit(x_factunit)

        # if fact's idea no range or is a "range-root" then allow fact to be set
        elif fact_base_idea.is_arithmetic() and self._is_idea_rangeroot(base) is False:
            raise InvalidBudException(
                f"Non range-root fact:{base} can only be set by range-root fact"
            )

        elif fact_base_idea.is_arithmetic() and self._is_idea_rangeroot(base):
            # WHEN idea is "range-root" identify any reason.bases that are descendants
            # calculate and set those descendant facts
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendant
            # there exists a reason base "timeline,weeks" with premise.need = "timeline,weeks"
            # and (1,2) divisor=2 (every othher week)
            #
            # should not set "timeline,weeks" fact, only "timeline" fact and
            # "timeline,weeks" should be set automatica_lly since there exists a reason
            # that has that base.
            x_idearoot.set_factunit(x_factunit)

            # Find all Fact descendants and any range_source_road connections "Lemmas"
            lemmas_dict = self._get_lemma_factunits()
            missing_facts = self.get_missing_fact_bases().keys()
            x_idearoot._apply_any_range_source_road_connections(
                lemmas_dict, missing_facts
            )

        self.settle_bud()

    def get_fact(self, base: RoadUnit) -> FactUnit:
        return self._idearoot._factunits.get(base)

    def del_fact(self, base: RoadUnit):
        self._idearoot.del_factunit(base)

    def get_idea_dict(self, problem: bool = None) -> dict[RoadUnit, IdeaUnit]:
        self.settle_bud()
        if not problem:
            return self._idea_dict
        if self._econs_justified is False:
            raise Exception_econs_justified(
                f"Cannot return problem set because _econs_justified={self._econs_justified}."
            )

        return {
            x_idea.get_road(): x_idea
            for x_idea in self._idea_dict.values()
            if x_idea._problem_bool
        }

    def get_tree_metrics(self) -> TreeMetrics:
        self.settle_bud()
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_node(
            level=self._idearoot._level,
            reasons=self._idearoot._reasonunits,
            awardlinks=self._idearoot._awardlinks,
            uid=self._idearoot._uid,
            pledge=self._idearoot.pledge,
            idea_road=self._idearoot.get_road(),
        )

        x_idea_list = [self._idearoot]
        while x_idea_list != []:
            parent_idea = x_idea_list.pop()
            for idea_kid in parent_idea._kids.values():
                self._eval_tree_metrics(
                    parent_idea, idea_kid, tree_metrics, x_idea_list
                )
        return tree_metrics

    def _eval_tree_metrics(self, parent_idea, idea_kid, tree_metrics, x_idea_list):
        idea_kid._level = parent_idea._level + 1
        tree_metrics.evaluate_node(
            level=idea_kid._level,
            reasons=idea_kid._reasonunits,
            awardlinks=idea_kid._awardlinks,
            uid=idea_kid._uid,
            pledge=idea_kid.pledge,
            idea_road=idea_kid.get_road(),
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
                self.edit_idea_attr(road=x_idea.get_road(), uid=new_idea_uid_max)
                idea_uid_max = new_idea_uid_max

    def get_idea_count(self) -> int:
        return len(self._idea_dict)

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
                self._idearoot._factunits[base]
            except KeyError:
                missing_bases[base] = base_count

        return missing_bases

    def add_l1_idea(
        self,
        idea_kid: IdeaUnit,
        create_missing_ideas: bool = None,
        filter_out_missing_awardlinks_lobby_ids: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.add_idea(
            idea_kid=idea_kid,
            parent_road=self._real_id,
            create_missing_ideas=create_missing_ideas,
            filter_out_missing_awardlinks_lobby_ids=filter_out_missing_awardlinks_lobby_ids,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def add_idea(
        self,
        idea_kid: IdeaUnit,
        parent_road: RoadUnit,
        filter_out_missing_awardlinks_lobby_ids: bool = None,
        create_missing_ideas: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        if RoadNode(idea_kid._label).is_node(self._road_delimiter) is False:
            raise InvalidBudException(
                f"add_idea failed because '{idea_kid._label}' is not a RoadNode."
            )

        if self._idearoot._label != get_root_node_from_road(
            parent_road, self._road_delimiter
        ):
            raise InvalidBudException(
                f"add_idea failed because parent_road '{parent_road}' has an invalid root node"
            )

        idea_kid._road_delimiter = self._road_delimiter
        if idea_kid._bud_real_id != self._real_id:
            idea_kid._bud_real_id = self._real_id
        if idea_kid._fund_coin != self._fund_coin:
            idea_kid._fund_coin = self._fund_coin
        if not filter_out_missing_awardlinks_lobby_ids:
            idea_kid = self._get_filtered_awardlinks_idea(idea_kid)
        idea_kid.set_parent_road(parent_road=parent_road)

        # create any missing ideas
        if not create_missing_ancestors and self.idea_exists(parent_road) is False:
            raise InvalidBudException(
                f"add_idea failed because '{parent_road}' idea does not exist."
            )
        parent_road_idea = self.get_idea_obj(parent_road, create_missing_ancestors)
        if parent_road_idea._root is False:
            parent_road_idea
        parent_road_idea.add_kid(idea_kid)

        kid_road = self.make_road(parent_road, idea_kid._label)
        if adoptees is not None:
            weight_sum = 0
            for adoptee_label in adoptees:
                adoptee_road = self.make_road(parent_road, adoptee_label)
                adoptee_idea = self.get_idea_obj(adoptee_road)
                weight_sum += adoptee_idea._weight
                new_adoptee_parent_road = self.make_road(kid_road, adoptee_label)
                self.add_idea(adoptee_idea, new_adoptee_parent_road)
                self.edit_idea_attr(
                    new_adoptee_parent_road, weight=adoptee_idea._weight
                )
                self.del_idea_obj(adoptee_road)

            if bundling:
                self.edit_idea_attr(road=kid_road, weight=weight_sum)

        if create_missing_ideas:
            self._create_missing_ideas(road=kid_road)

    def _get_filtered_awardlinks_idea(self, x_idea: IdeaUnit) -> IdeaUnit:
        _awardlinks_to_delete = [
            _awardlink_lobby_id
            for _awardlink_lobby_id in x_idea._awardlinks.keys()
            if self.get_charunit_lobby_ids_dict().get(_awardlink_lobby_id) is None
        ]
        for _awardlink_lobby_id in _awardlinks_to_delete:
            x_idea._awardlinks.pop(_awardlink_lobby_id)

        if x_idea._doerunit is not None:
            _lobbyholds_to_delete = [
                _lobbyhold_lobby_id
                for _lobbyhold_lobby_id in x_idea._doerunit._lobbyholds
                if self.get_charunit_lobby_ids_dict().get(_lobbyhold_lobby_id) is None
            ]
            for _lobbyhold_lobby_id in _lobbyholds_to_delete:
                x_idea._doerunit.del_lobbyhold(_lobbyhold_lobby_id)
        return x_idea

    def _create_missing_ideas(self, road):
        self.settle_bud()
        posted_idea = self.get_idea_obj(road)

        for reason_x in posted_idea._reasonunits.values():
            self._set_ideakid_if_empty(road=reason_x.base)
            for premise_x in reason_x.premises.values():
                self._set_ideakid_if_empty(road=premise_x.need)
        if posted_idea._range_source_road is not None:
            self._set_ideakid_if_empty(road=posted_idea._range_source_road)
        if posted_idea._numeric_road is not None:
            self._set_ideakid_if_empty(road=posted_idea._numeric_road)

    def _set_ideakid_if_empty(self, road: RoadUnit):
        if self.idea_exists(road) is False:
            self.add_idea(
                ideaunit_shop(get_terminus_node(road, self._road_delimiter)),
                parent_road=get_parent_road(road),
            )

    def del_idea_obj(self, road: RoadUnit, del_children: bool = True):
        if road == self._idearoot.get_road():
            raise InvalidBudException("Idearoot cannot be deleted")
        parent_road = get_parent_road(road)
        if self.idea_exists(road):
            if not del_children:
                self._shift_idea_kids(x_road=road)
            parent_idea = self.get_idea_obj(parent_road)
            parent_idea.del_kid(get_terminus_node(road, self._road_delimiter))
        self.settle_bud()

    def _shift_idea_kids(self, x_road: RoadUnit):
        parent_road = get_parent_road(x_road)
        d_temp_idea = self.get_idea_obj(x_road)
        for kid in d_temp_idea._kids.values():
            self.add_idea(kid, parent_road=parent_road)

    def set_owner_id(self, new_owner_id):
        self._owner_id = new_owner_id

    def edit_idea_label(
        self,
        old_road: RoadUnit,
        new_label: RoadNode,
    ):
        if self._road_delimiter in new_label:
            raise InvalidLabelException(
                f"Cannot modify '{old_road}' because new_label {new_label} contains delimiter {self._road_delimiter}"
            )
        if self.idea_exists(old_road) is False:
            raise InvalidBudException(f"Idea {old_road=} does not exist")

        parent_road = get_parent_road(road=old_road)
        new_road = (
            self.make_road(new_label)
            if parent_road == ""
            else self.make_road(parent_road, new_label)
        )
        if old_road != new_road:
            if parent_road == "":
                self._idearoot.set_idea_label(new_label)
            else:
                self._non_root_idea_label_edit(old_road, new_label, parent_road)
            self._idearoot_find_replace_road(old_road=old_road, new_road=new_road)
            self._idearoot._factunits = find_replace_road_key_dict(
                dict_x=self._idearoot._factunits,
                old_road=old_road,
                new_road=new_road,
            )

    def _non_root_idea_label_edit(
        self, old_road: RoadUnit, new_label: RoadNode, parent_road: RoadUnit
    ):
        x_idea = self.get_idea_obj(old_road)
        x_idea.set_idea_label(new_label)
        x_idea._parent_road = parent_road
        idea_parent = self.get_idea_obj(get_parent_road(old_road))
        idea_parent._kids.pop(get_terminus_node(old_road, self._road_delimiter))
        idea_parent._kids[x_idea._label] = x_idea

    def _idearoot_find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self._idearoot.find_replace_road(old_road=old_road, new_road=new_road)

        idea_iter_list = [self._idearoot]
        while idea_iter_list != []:
            listed_idea = idea_iter_list.pop()
            # put all idea_children in idea list
            if listed_idea._kids is not None:
                for idea_kid in listed_idea._kids.values():
                    idea_iter_list.append(idea_kid)
                    if is_sub_road(
                        ref_road=idea_kid._parent_road,
                        sub_road=old_road,
                    ):
                        idea_kid._parent_road = rebuild_road(
                            subj_road=idea_kid._parent_road,
                            old_road=old_road,
                            new_road=new_road,
                        )
                    idea_kid.find_replace_road(old_road=old_road, new_road=new_road)

    def _set_ideaattrfilter_premise_ranges(self, x_ideaattrfilter: IdeaAttrFilter):
        premise_idea = self.get_idea_obj(x_ideaattrfilter.get_premise_need())
        x_ideaattrfilter.set_premise_range_attributes_influenced_by_premise_idea(
            premise_open=premise_idea._begin,
            premise_nigh=premise_idea._close,
            # premise_numor=premise_idea.anc_numor,
            premise_denom=premise_idea._denom,
            # anc_reest=premise_idea.anc_reest,
        )

    def _set_ideaattrfilter_begin_close(
        self, ideaattrfilter: IdeaAttrFilter, idea_road: RoadUnit
    ) -> set[float, float]:
        x_iaf = ideaattrfilter
        anc_roads = get_ancestor_roads(road=idea_road)
        if (
            x_iaf.addin is not None
            or x_iaf.numor is not None
            or x_iaf.denom is not None
            or x_iaf.reest is not None
        ) and len(anc_roads) == 1:
            raise InvalidBudException("Root Idea cannot have numor denom reest.")
        parent_road = self._real_id if len(anc_roads) == 1 else anc_roads[1]

        parent_has_range = None
        parent_idea = self.get_idea_obj(parent_road)
        parent_begin = parent_idea._begin
        parent_close = parent_idea._close
        parent_has_range = parent_begin is not None and parent_close is not None

        numeric_begin = None
        numeric_close = None
        numeric_range = None
        if x_iaf.numeric_road is not None:
            numeric_idea = self.get_idea_obj(x_iaf.numeric_road)
            numeric_begin = numeric_idea._begin
            numeric_close = numeric_idea._close
            numeric_range = numeric_begin is not None and numeric_close is not None

        if parent_has_range and x_iaf.addin not in [None, 0]:
            parent_begin = parent_begin + x_iaf.addin
            parent_close = parent_close + x_iaf.addin

        x_begin, x_close = self._transform_begin_close(
            reest=x_iaf.reest,
            begin=x_iaf.begin,
            close=x_iaf.close,
            numor=x_iaf.numor,
            denom=x_iaf.denom,
            parent_has_range=parent_has_range,
            parent_begin=parent_begin,
            parent_close=parent_close,
            numeric_range=numeric_range,
            numeric_begin=numeric_begin,
            numeric_close=numeric_close,
        )

        if parent_has_range and numeric_range:
            raise InvalidBudException(
                "Idea has begin-close range parent, cannot have numeric_road"
            )
        elif not parent_has_range and not numeric_range and x_iaf.numor is not None:
            raise InvalidBudException(
                f"Idea cannot edit numor={x_iaf.numor}/denom/reest of '{idea_road}' if parent '{parent_road}' or ideaunit._numeric_road does not have begin/close range"
            )
        ideaattrfilter.begin = x_begin
        ideaattrfilter.close = x_close

    def _transform_begin_close(
        self,
        reest,
        begin: float,
        close: float,
        numor: float,
        denom: float,
        parent_has_range: float,
        parent_begin: float,
        parent_close: float,
        numeric_range: float,
        numeric_begin: float,
        numeric_close: float,
    ):  # sourcery skip: remove-redundant-if
        if not reest and parent_has_range and numor is not None:
            begin = parent_begin * numor / denom
            close = parent_close * numor / denom
        elif not reest and parent_has_range and numor is None:
            begin = parent_begin
            close = parent_close
        elif not reest and numeric_range and numor is not None:
            begin = numeric_begin * numor / denom
            close = numeric_close * numor / denom
        elif not reest and numeric_range and numor is None:
            begin = numeric_begin
            close = numeric_close
        elif reest and parent_has_range and numor is not None:
            begin = parent_begin * numor % denom
            close = parent_close * numor % denom
        elif reest and parent_has_range and numor is None:
            begin = 0
            close = parent_close - parent_begin
        elif reest and numeric_range and numor is not None:
            begin = numeric_begin * numor % denom
            close = numeric_close * numor % denom
        elif reest and numeric_range and numor is None:
            begin = 0
            close = parent_close - parent_begin
        else:
            begin = begin
            close = close

        return begin, close

    def edit_reason(
        self,
        road: RoadUnit,
        reason_base: RoadUnit = None,
        reason_premise: RoadUnit = None,
        reason_premise_open: float = None,
        reason_premise_nigh: float = None,
        reason_premise_divisor: int = None,
    ):
        self.edit_idea_attr(
            road=road,
            reason_base=reason_base,
            reason_premise=reason_premise,
            reason_premise_open=reason_premise_open,
            reason_premise_nigh=reason_premise_nigh,
            reason_premise_divisor=reason_premise_divisor,
        )

    def edit_idea_attr(
        self,
        road: RoadUnit,
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
        all_acct_cred: bool = None,
        all_acct_debt: bool = None,
        awardlink: AwardLink = None,
        awardlink_del: LobbyID = None,
        is_expanded: bool = None,
        problem_bool: bool = None,
    ):
        if healerhold is not None:
            for x_lobby_id in healerhold._lobby_ids:
                if self.get_charunit_lobby_ids_dict().get(x_lobby_id) is None:
                    raise healerhold_lobby_id_Exception(
                        f"Idea cannot edit healerhold because lobby_id '{x_lobby_id}' does not exist as lobby in Bud"
                    )

        x_ideaattrfilter = ideaattrfilter_shop(
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
        if x_ideaattrfilter.has_numeric_attrs():
            self._set_ideaattrfilter_begin_close(x_ideaattrfilter, road)
        if x_ideaattrfilter.has_reason_premise():
            self._set_ideaattrfilter_premise_ranges(x_ideaattrfilter)
        x_idea = self.get_idea_obj(road)
        x_idea._set_idea_attr(idea_attr=x_ideaattrfilter)

        # # deleting or setting a awardlink reqquires a tree traverse to correctly set awardheirs and awardlines
        # if awardlink_del is not None or awardlink is not None:
        #     self.settle_bud()

    def get_agenda_dict(
        self, necessary_base: RoadUnit = None
    ) -> dict[RoadUnit, IdeaUnit]:
        self.settle_bud()
        all_ideas = self._idea_dict.values()
        return {
            x_idea.get_road(): x_idea
            for x_idea in all_ideas
            if x_idea.is_agenda_item(necessary_base)
        }

    def get_all_pledges(self) -> dict[RoadUnit, IdeaUnit]:
        self.settle_bud()
        all_ideas = self._idea_dict.values()
        return {x_idea.get_road(): x_idea for x_idea in all_ideas if x_idea.pledge}

    def set_agenda_task_complete(self, task_road: RoadUnit, base: RoadUnit):
        pledge_item = self.get_idea_obj(task_road)
        pledge_item.set_factunit_to_complete(self._idearoot._factunits[base])

    def _allot_offtrack_fund(self):
        x_acctunits = self._accts.values()
        credor_ledger = {x_acct.acct_id: x_acct.credor_weight for x_acct in x_acctunits}
        debtor_ledger = {x_acct.acct_id: x_acct.debtor_weight for x_acct in x_acctunits}
        fund_give_allot = allot_scale(
            credor_ledger, self._offtrack_fund, self._fund_coin
        )
        fund_take_allot = allot_scale(
            debtor_ledger, self._offtrack_fund, self._fund_coin
        )
        for x_acct_id, acct_fund_give in fund_give_allot.items():
            self.get_acct(x_acct_id).add_fund_give(acct_fund_give)
        for x_acct_id, acct_fund_take in fund_take_allot.items():
            self.get_acct(x_acct_id).add_fund_take(acct_fund_take)

    def get_acctunits_credor_weight_sum(self) -> float:
        return sum(acctunit.get_credor_weight() for acctunit in self._accts.values())

    def get_acctunits_debtor_weight_sum(self) -> float:
        return sum(acctunit.get_debtor_weight() for acctunit in self._accts.values())

    def _add_to_acctunits_fund_give_take(self, idea_fund_share: float):
        sum_acctunit_credor_weight = self.get_acctunits_credor_weight_sum()
        sum_acctunit_debtor_weight = self.get_acctunits_debtor_weight_sum()

        for x_acctunit in self._accts.values():
            au_fund_give = (
                idea_fund_share * x_acctunit.get_credor_weight()
            ) / sum_acctunit_credor_weight

            au_fund_take = (
                idea_fund_share * x_acctunit.get_debtor_weight()
            ) / sum_acctunit_debtor_weight

            x_acctunit.add_fund_give_take(
                fund_give=au_fund_give,
                fund_take=au_fund_take,
                bud_agenda_cred=0,
                bud_agenda_debt=0,
            )

    def _add_to_acctunits_fund_agenda_give_take(self, idea_fund_share: float):
        sum_acctunit_credor_weight = self.get_acctunits_credor_weight_sum()
        sum_acctunit_debtor_weight = self.get_acctunits_debtor_weight_sum()

        for x_acctunit in self._accts.values():
            au_fund_agenda_give = (
                idea_fund_share * x_acctunit.get_credor_weight()
            ) / sum_acctunit_credor_weight

            au_fund_agenda_take = (
                idea_fund_share * x_acctunit.get_debtor_weight()
            ) / sum_acctunit_debtor_weight

            x_acctunit.add_fund_give_take(
                fund_give=0,
                fund_take=0,
                bud_agenda_cred=au_fund_agenda_give,
                bud_agenda_debt=au_fund_agenda_take,
            )

    def _set_acctunits_bud_agenda_share(self, bud_agenda_share: float):
        sum_acctunit_credor_weight = self.get_acctunits_credor_weight_sum()
        sum_acctunit_debtor_weight = self.get_acctunits_debtor_weight_sum()

        for x_acctunit in self._accts.values():
            au_fund_agenda_give = (
                bud_agenda_share * x_acctunit.get_credor_weight()
            ) / sum_acctunit_credor_weight

            au_fund_agenda_take = (
                bud_agenda_share * x_acctunit.get_debtor_weight()
            ) / sum_acctunit_debtor_weight

            x_acctunit.add_fund_agenda_give_take(
                bud_agenda_cred=au_fund_agenda_give,
                bud_agenda_debt=au_fund_agenda_take,
            )

    def _reset_lobbyboxs_fund_give_take(self):
        for lobbybox_obj in self._lobbyboxs.values():
            lobbybox_obj.reset_fund_give_take()

    def _set_lobbyboxs_fund_share(self, awardheirs: dict[LobbyID, AwardLink]):
        for awardlink_obj in awardheirs.values():
            x_lobby_id = awardlink_obj.lobby_id
            if not self.lobbybox_exists(x_lobby_id):
                self.set_lobbybox(self.create_symmetry_lobbybox(x_lobby_id))
            self.add_to_lobbybox_fund_give_take(
                lobby_id=awardlink_obj.lobby_id,
                awardheir_fund_give=awardlink_obj._fund_give,
                awardheir_fund_take=awardlink_obj._fund_take,
            )

    def _allot_fund_bud_agenda(self):
        for idea in self._idea_dict.values():
            # If there are no awardlines associated with idea
            # allot fund_share via general acctunit
            # cred ratio and debt ratio
            # if idea.is_agenda_item() and idea._awardlines == {}:
            if idea.is_agenda_item():
                if idea._awardlines == {}:
                    self._add_to_acctunits_fund_agenda_give_take(idea.get_fund_share())
                else:
                    for x_awardline in idea._awardlines.values():
                        self.add_to_lobbybox_fund_agenda_give_take(
                            lobby_id=x_awardline.lobby_id,
                            awardline_fund_give=x_awardline._fund_give,
                            awardline_fund_take=x_awardline._fund_take,
                        )

    def _allot_lobbyboxs_fund(self):
        for x_lobbybox in self._lobbyboxs.values():
            x_lobbybox._set_lobbyship_fund_give_take()
            for x_lobbyship in x_lobbybox._lobbyships.values():
                self.add_to_acctunit_fund_give_take(
                    acctunit_acct_id=x_lobbyship._acct_id,
                    fund_give=x_lobbyship._fund_give,
                    fund_take=x_lobbyship._fund_take,
                    bud_agenda_cred=x_lobbyship._fund_agenda_give,
                    bud_agenda_debt=x_lobbyship._fund_agenda_take,
                )

    def _set_acctunits_fund_ratios(self):
        fund_agenda_ratio_give_sum = 0
        fund_agenda_ratio_take_sum = 0
        x_acctunit_credor_weight_sum = self.get_acctunits_credor_weight_sum()
        x_acctunit_debtor_weight_sum = self.get_acctunits_debtor_weight_sum()

        for x_acctunit in self._accts.values():
            fund_agenda_ratio_give_sum += x_acctunit._fund_agenda_give
            fund_agenda_ratio_take_sum += x_acctunit._fund_agenda_take

        for x_acctunit in self._accts.values():
            x_acctunit.set_fund_agenda_ratio_give_take(
                fund_agenda_ratio_give_sum=fund_agenda_ratio_give_sum,
                fund_agenda_ratio_take_sum=fund_agenda_ratio_take_sum,
                bud_acctunit_total_credor_weight=x_acctunit_credor_weight_sum,
                bud_acctunit_total_debtor_weight=x_acctunit_debtor_weight_sum,
            )

    def _reset_acctunit_fund_give_take(self):
        for acctunit in self._accts.values():
            acctunit.reset_fund_give_take()

    def idea_exists(self, road: RoadUnit) -> bool:
        if road is None:
            return False
        root_road_label = get_root_node_from_road(road, delimiter=self._road_delimiter)
        if root_road_label != self._idearoot._label:
            return False

        nodes = get_all_road_nodes(road, delimiter=self._road_delimiter)
        root_road_label = nodes.pop(0)
        if nodes == []:
            return True

        idea_label = nodes.pop(0)
        x_idea = self._idearoot.get_kid(idea_label)
        if x_idea is None:
            return False
        while nodes != []:
            idea_label = nodes.pop(0)
            x_idea = x_idea.get_kid(idea_label)
            if x_idea is None:
                return False
        return True

    def get_idea_obj(self, road: RoadUnit, if_missing_create: bool = False) -> IdeaUnit:
        if road is None:
            raise InvalidBudException("get_idea_obj received road=None")
        if self.idea_exists(road) is False and not if_missing_create:
            raise InvalidBudException(f"get_idea_obj failed. no item at '{road}'")
        roadnodes = get_all_road_nodes(road, delimiter=self._road_delimiter)
        if len(roadnodes) == 1:
            return self._idearoot

        roadnodes.pop(0)
        idea_label = roadnodes.pop(0)
        x_idea = self._idearoot.get_kid(idea_label, if_missing_create)
        while roadnodes != []:
            x_idea = x_idea.get_kid(roadnodes.pop(0), if_missing_create)

        return x_idea

    def get_idea_ranged_kids(
        self, idea_road: str, begin: float = None, close: float = None
    ) -> dict[IdeaUnit]:
        parent_idea = self.get_idea_obj(idea_road)
        if begin is None and close is None:
            begin = parent_idea._begin
            close = parent_idea._close
        elif begin is not None and close is None:
            close = begin

        idea_list = parent_idea.get_kids_in_range(begin=begin, close=close)
        return {x_idea._label: x_idea for x_idea in idea_list}

    def _set_ancestors_metrics(self, road: RoadUnit, econ_exceptions: bool = False):
        task_count = 0
        child_awardlines = None
        lobby_everyone = None
        ancestor_roads = get_ancestor_roads(road=road)
        econ_justified_by_problem = True
        healerhold_count = 0

        while ancestor_roads != []:
            youngest_road = ancestor_roads.pop(0)
            # _set_non_root_ancestor_metrics(youngest_road, task_count, lobby_everyone)
            x_idea_obj = self.get_idea_obj(road=youngest_road)
            x_idea_obj.add_to_descendant_pledge_count(task_count)
            if x_idea_obj.is_kidless():
                x_idea_obj.set_kidless_awardlines()
                child_awardlines = x_idea_obj._awardlines
            else:
                x_idea_obj.set_awardlines(child_awardlines=child_awardlines)

            if x_idea_obj._task:
                task_count += 1

            if (
                lobby_everyone != False
                and x_idea_obj._all_acct_cred != False
                and x_idea_obj._all_acct_debt != False
                and x_idea_obj._awardheirs != {}
            ) or (
                lobby_everyone != False
                and x_idea_obj._all_acct_cred is False
                and x_idea_obj._all_acct_debt is False
            ):
                lobby_everyone = False
            elif lobby_everyone != False:
                lobby_everyone = True
            x_idea_obj._all_acct_cred = lobby_everyone
            x_idea_obj._all_acct_debt = lobby_everyone

            if x_idea_obj._healerhold.any_lobby_id_exists():
                econ_justified_by_problem = False
                healerhold_count += 1
                self._sum_healerhold_share += x_idea_obj.get_fund_share()
            if x_idea_obj._problem_bool:
                econ_justified_by_problem = True

        if econ_justified_by_problem is False or healerhold_count > 1:
            if econ_exceptions:
                raise Exception_econs_justified(
                    f"IdeaUnit '{road}' cannot sponsor ancestor econs."
                )
            self._econs_justified = False

    def _set_root_attributes(self, econ_exceptions: bool):
        self._idearoot._level = 0
        self._idearoot.set_parent_road("")
        self._idearoot.set_idearoot_inherit_reasonheirs()
        self._idearoot.set_doerheir(None, self._lobbyboxs)
        self._idearoot.set_factheirs(self._idearoot._factunits)
        self._idearoot.inherit_awardheirs()
        self._idearoot.clear_awardlines()
        self._idearoot._weight = 1
        tree_traverse_count = self._tree_traverse_count
        self._idearoot.set_active(tree_traverse_count, self._lobbyboxs, self._owner_id)
        self._idearoot.set_fund_attr(0, self._fund_pool, self._fund_pool)
        self._idearoot.set_awardheirs_fund_give_fund_take()
        self._idearoot.set_ancestor_pledge_count(0, False)
        self._idearoot.clear_descendant_pledge_count()
        self._idearoot.clear_all_acct_cred_debt()
        self._idearoot.pledge = False
        if self._idearoot.is_kidless():
            self._set_ancestors_metrics(self._idearoot.get_road(), econ_exceptions)
            self._allot_fund_share(idea=self._idearoot)
        if (
            self._tree_traverse_count == 1
            and not self._idearoot.is_kidless()
            and self._idearoot.get_kids_weight_sum() == 0
            and self._idearoot._weight != 0
        ):
            self._offtrack_kids_weight_set.add(self._idearoot.get_road())

    def _set_kids_attributes(
        self,
        idea_kid: IdeaUnit,
        fund_onset: float,
        fund_cease: float,
        parent_idea: IdeaUnit,
        econ_exceptions: bool,
    ):
        idea_kid.set_level(parent_idea._level)
        idea_kid.set_parent_road(parent_idea.get_road())
        idea_kid.set_factheirs(parent_idea._factheirs)
        idea_kid.set_reasonheirs(self._idea_dict, parent_idea._reasonheirs)
        idea_kid.set_doerheir(parent_idea._doerheir, self._lobbyboxs)
        idea_kid.inherit_awardheirs(parent_idea._awardheirs)
        idea_kid.clear_awardlines()
        tree_traverse_count = self._tree_traverse_count
        idea_kid.set_active(tree_traverse_count, self._lobbyboxs, self._owner_id)
        idea_kid.set_fund_attr(fund_onset, fund_cease, self._fund_pool)
        ancestor_pledge_count = parent_idea._ancestor_pledge_count
        idea_kid.set_ancestor_pledge_count(ancestor_pledge_count, parent_idea.pledge)
        idea_kid.clear_descendant_pledge_count()
        idea_kid.clear_all_acct_cred_debt()

        if idea_kid.is_kidless():
            # set idea's ancestor metrics using bud root as common source
            self._set_ancestors_metrics(idea_kid.get_road(), econ_exceptions)
            self._allot_fund_share(idea=idea_kid)
        if (
            self._tree_traverse_count == 1
            and idea_kid._weight != 0
            and not idea_kid.is_kidless()
            and idea_kid.get_kids_weight_sum() == 0
        ):
            self._offtrack_kids_weight_set.add(idea_kid.get_road())

    def _allot_fund_share(self, idea: IdeaUnit):
        # TODO manage situations where awardheir.credor_weight is None for all awardheirs
        # TODO manage situations where awardheir.debtor_weight is None for all awardheirs
        if idea.awardheir_exists() is False:
            self._set_lobbyboxs_fund_share(idea._awardheirs)
        elif idea.awardheir_exists():
            self._add_to_acctunits_fund_give_take(idea.get_fund_share())

    def get_fund_share(
        self, parent_fund_share: float, weight: int, sibling_total_weight: int
    ) -> float:
        sibling_ratio = weight / sibling_total_weight
        return parent_fund_share * sibling_ratio

    def _create_lobbyboxs_metrics(self):
        self._lobbyboxs = {}
        for lobby_id, acct_id_set in self.get_charunit_lobby_ids_dict().items():
            x_lobbybox = lobbybox_shop(lobby_id, _road_delimiter=self._road_delimiter)
            for x_acct_id in acct_id_set:
                x_lobbyship = self.get_acct(x_acct_id).get_lobbyship(lobby_id)
                x_lobbybox.set_lobbyship(x_lobbyship)
                self.set_lobbybox(x_lobbybox)

    def _calc_acctunit_metrics(self):
        self._credor_respect = validate_respect_num(self._credor_respect)
        self._debtor_respect = validate_respect_num(self._debtor_respect)
        x_acctunits = self._accts.values()
        credor_ledger = {x_acct.acct_id: x_acct.credor_weight for x_acct in x_acctunits}
        debtor_ledger = {x_acct.acct_id: x_acct.debtor_weight for x_acct in x_acctunits}
        credor_allot = allot_scale(credor_ledger, self._credor_respect, self._bit)
        debtor_allot = allot_scale(debtor_ledger, self._debtor_respect, self._bit)
        for x_acct_id, acct_credor_pool in credor_allot.items():
            self.get_acct(x_acct_id).set_credor_pool(acct_credor_pool)
        for x_acct_id, acct_debtor_pool in debtor_allot.items():
            self.get_acct(x_acct_id).set_debtor_pool(acct_debtor_pool)
        self._create_lobbyboxs_metrics()
        self._reset_acctunit_fund_give_take()

    def _set_tree_traverse_stage(self):
        self._rational = False
        self._tree_traverse_count = 0
        self._idea_dict = {self._idearoot.get_road(): self._idearoot}
        self._offtrack_kids_weight_set = set()

    def _clear_bud_base_metrics(self):
        self._econs_justified = True
        self._econs_buildable = False
        self._sum_healerhold_share = 0
        self._econ_dict = {}
        self._healers_dict = {}

    def settle_bud(self, econ_exceptions: bool = False):
        self._calc_acctunit_metrics()
        self._set_tree_traverse_stage()
        max_count = self._max_tree_traverse

        while not self._rational and self._tree_traverse_count < max_count:
            self._clear_bud_base_metrics()
            self._execute_tree_traverse(econ_exceptions)
            self._check_if_any_idea_active_status_has_altered()
            self._tree_traverse_count += 1
        self._after_all_tree_traverses_set_cred_debt()
        self._after_all_tree_traverses_set_healerhold_share()

    def _execute_tree_traverse(self, econ_exceptions: bool = False):
        self._pre_tree_traverse_cred_debt_reset()
        self._set_root_attributes(econ_exceptions)

        x_idearoot_kids_items = self._idearoot._kids.items()
        kids_ledger = {x_road: kid._weight for x_road, kid in x_idearoot_kids_items}
        root_fund_num = self._idearoot._fund_cease - self._idearoot._fund_onset
        alloted_fund_num = allot_scale(kids_ledger, root_fund_num, self._fund_coin)
        x_idearoot_kid_fund_onset = None
        x_idearoot_kid_fund_cease = None

        cache_idea_list = []
        for kid_label, idea_kid in self._idearoot._kids.items():
            idearoot_kid_fund_num = alloted_fund_num.get(kid_label)
            if x_idearoot_kid_fund_onset is None:
                x_idearoot_kid_fund_onset = self._idearoot._fund_onset
                x_idearoot_kid_fund_cease = (
                    self._idearoot._fund_onset + idearoot_kid_fund_num
                )
            else:
                x_idearoot_kid_fund_onset = x_idearoot_kid_fund_cease
                x_idearoot_kid_fund_cease += idearoot_kid_fund_num
            self._set_kids_attributes(
                idea_kid=idea_kid,
                fund_onset=x_idearoot_kid_fund_onset,
                fund_cease=x_idearoot_kid_fund_cease,
                parent_idea=self._idearoot,
                econ_exceptions=econ_exceptions,
            )
            cache_idea_list.append(idea_kid)

        # no function recursion, recursion by iterateing over list that can be added to by iterations
        while cache_idea_list != []:
            parent_idea = cache_idea_list.pop()

            if self._tree_traverse_count == 0:
                self._idea_dict[parent_idea.get_road()] = parent_idea

            kids_items = parent_idea._kids.items()
            x_ledger = {x_road: idea_kid._weight for x_road, idea_kid in kids_items}
            parent_fund_num = parent_idea._fund_cease - parent_idea._fund_onset
            alloted_fund_num = allot_scale(x_ledger, parent_fund_num, self._fund_coin)

            if parent_idea._kids is not None:
                fund_onset = None
                fund_cease = None
                for idea_kid in parent_idea._kids.values():
                    if fund_onset is None:
                        fund_onset = parent_idea._fund_onset
                        fund_cease = fund_onset + alloted_fund_num.get(idea_kid._label)
                    else:
                        fund_onset = fund_cease
                        fund_cease += alloted_fund_num.get(idea_kid._label)
                    self._set_kids_attributes(
                        idea_kid=idea_kid,
                        fund_onset=fund_onset,
                        fund_cease=fund_cease,
                        parent_idea=parent_idea,
                        econ_exceptions=econ_exceptions,
                    )
                    cache_idea_list.append(idea_kid)

    def _check_if_any_idea_active_status_has_altered(self):
        any_idea_active_status_has_altered = False
        for idea in self._idea_dict.values():
            if idea._active_hx.get(self._tree_traverse_count) is not None:
                any_idea_active_status_has_altered = True

        if any_idea_active_status_has_altered is False:
            self._rational = True

    def _after_all_tree_traverses_set_cred_debt(self):
        self.set_offtrack_fund()
        self._allot_offtrack_fund()
        self._allot_fund_bud_agenda()
        self._allot_lobbyboxs_fund()
        self._set_acctunits_fund_ratios()

    def _after_all_tree_traverses_set_healerhold_share(self):
        self._set_econ_dict()
        self._healers_dict = self._get_healers_dict()
        self._econs_buildable = self._get_buildable_econs()

    def _set_econ_dict(self):
        if self._econs_justified is False:
            self._sum_healerhold_share = 0
        for x_idea in self._idea_dict.values():
            if self._sum_healerhold_share == 0:
                x_idea._healerhold_ratio = 0
            else:
                x_sum = self._sum_healerhold_share
                x_idea._healerhold_ratio = x_idea.get_fund_share() / x_sum
            if self._econs_justified and x_idea._healerhold.any_lobby_id_exists():
                self._econ_dict[x_idea.get_road()] = x_idea

    def _get_healers_dict(self) -> dict[HealerID, dict[RoadUnit, IdeaUnit]]:
        _healers_dict = {}
        for x_econ_road, x_econ_idea in self._econ_dict.items():
            for x_lobby_id in x_econ_idea._healerhold._lobby_ids:
                x_lobbybox = self.get_lobbybox(x_lobby_id)
                for x_acct_id in x_lobbybox._lobbyships.keys():
                    if _healers_dict.get(x_acct_id) is None:
                        _healers_dict[x_acct_id] = {x_econ_road: x_econ_idea}
                    else:
                        healer_dict = _healers_dict.get(x_acct_id)
                        healer_dict[x_econ_road] = x_econ_idea
        return _healers_dict

    def _get_buildable_econs(self) -> bool:
        return all(
            roadunit_valid_dir_path(econ_road, self._road_delimiter) != False
            for econ_road in self._econ_dict.keys()
        )

    def _pre_tree_traverse_cred_debt_reset(self):
        self._reset_lobbyboxs_fund_give_take()
        self._reset_acctunit_fund_give_take()

    def get_idea_tree_ordered_road_list(
        self, no_range_descendants: bool = False
    ) -> list[RoadUnit]:
        idea_list = list(self.get_idea_dict().values())
        node_dict = {idea.get_road().lower(): idea.get_road() for idea in idea_list}
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
                    if self._idearoot._begin is None and self._idearoot._close is None:
                        list_x.append(road)
                else:
                    parent_idea = self.get_idea_obj(road=anc_list[1])
                    if parent_idea._begin is None and parent_idea._close is None:
                        list_x.append(road)

        return list_x

    def get_factunits_dict(self) -> dict[str, str]:
        x_dict = {}
        if self._idearoot._factunits is not None:
            for fact_road, fact_obj in self._idearoot._factunits.items():
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
            "_weight": self._weight,
            "_fund_pool": self._fund_pool,
            "_fund_coin": self._fund_coin,
            "_bit": self._bit,
            "_penny": self._penny,
            "_owner_id": self._owner_id,
            "_real_id": self._real_id,
            "_max_tree_traverse": self._max_tree_traverse,
            "_road_delimiter": self._road_delimiter,
            "_idearoot": self._idearoot.get_dict(),
        }
        if self._credor_respect is not None:
            x_dict["_credor_respect"] = self._credor_respect
        if self._debtor_respect is not None:
            x_dict["_debtor_respect"] = self._debtor_respect
        if self._last_gift_id is not None:
            x_dict["_last_gift_id"] = self._last_gift_id

        return x_dict

    def get_json(self) -> str:
        x_dict = self.get_dict()
        return get_json_from_dict(dict_x=x_dict)

    def set_dominate_pledge_idea(self, idea_kid: IdeaUnit):
        idea_kid.pledge = True
        self.add_idea(
            idea_kid=idea_kid,
            parent_road=self.make_road(idea_kid._parent_road),
            filter_out_missing_awardlinks_lobby_ids=True,
            create_missing_ideas=True,
        )

    def get_idea_list_without_idearoot(self) -> list[IdeaUnit]:
        self.settle_bud()
        x_list = list(self._idea_dict.values())
        x_list.pop(0)
        return x_list

    def set_offtrack_fund(self) -> float:
        self._offtrack_fund = sum(
            self.get_idea_obj(x_roadunit).get_fund_share()
            for x_roadunit in self._offtrack_kids_weight_set
        )


def budunit_shop(
    _owner_id: OwnerID = None,
    _real_id: RealID = None,
    _road_delimiter: str = None,
    _fund_pool: FundNum = None,
    _fund_coin: FundCoin = None,
    _bit: BitNum = None,
    _penny: PennyNum = None,
    _weight: float = None,
) -> BudUnit:
    _owner_id = "" if _owner_id is None else _owner_id
    _real_id = get_default_real_id_roadnode() if _real_id is None else _real_id
    x_bud = BudUnit(
        _owner_id=_owner_id,
        _weight=get_1_if_None(_weight),
        _real_id=_real_id,
        _accts=get_empty_dict_if_none(None),
        _lobbyboxs={},
        _idea_dict=get_empty_dict_if_none(None),
        _econ_dict=get_empty_dict_if_none(None),
        _healers_dict=get_empty_dict_if_none(None),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _credor_respect=validate_respect_num(),
        _debtor_respect=validate_respect_num(),
        _fund_pool=validate_fund_pool(_fund_pool),
        _fund_coin=default_fund_coin_if_none(_fund_coin),
        _bit=default_bit_if_none(_bit),
        _penny=default_penny_if_none(_penny),
        _econs_justified=get_False_if_None(),
        _econs_buildable=get_False_if_None(),
        _sum_healerhold_share=get_0_if_None(),
        _offtrack_kids_weight_set=set(),
    )
    x_bud._idearoot = ideaunit_shop(
        _root=True,
        _uid=1,
        _level=0,
        _bud_real_id=x_bud._real_id,
        _road_delimiter=x_bud._road_delimiter,
        _fund_coin=x_bud._fund_coin,
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
    x_bud._weight = obj_from_bud_dict(bud_dict, "_weight")
    x_bud.set_max_tree_traverse(obj_from_bud_dict(bud_dict, "_max_tree_traverse"))
    x_bud.set_real_id(obj_from_bud_dict(bud_dict, "_real_id"))
    bud_road_delimiter = obj_from_bud_dict(bud_dict, "_road_delimiter")
    x_bud._road_delimiter = default_road_delimiter_if_none(bud_road_delimiter)
    x_bud._fund_pool = validate_fund_pool(obj_from_bud_dict(bud_dict, "_fund_pool"))
    x_bud._fund_coin = default_fund_coin_if_none(
        obj_from_bud_dict(bud_dict, "_fund_coin")
    )
    x_bud._bit = default_bit_if_none(obj_from_bud_dict(bud_dict, "_bit"))
    x_bud._penny = default_penny_if_none(obj_from_bud_dict(bud_dict, "_penny"))
    x_bud._credor_respect = obj_from_bud_dict(bud_dict, "_credor_respect")
    x_bud._debtor_respect = obj_from_bud_dict(bud_dict, "_debtor_respect")
    x_bud._last_gift_id = obj_from_bud_dict(bud_dict, "_last_gift_id")
    x_road_delimiter = x_bud._road_delimiter
    x_accts = obj_from_bud_dict(bud_dict, "_accts", x_road_delimiter).values()
    for x_acctunit in x_accts:
        x_bud.set_acctunit(x_acctunit)
    x_bud._originunit = obj_from_bud_dict(bud_dict, "_originunit")
    set_idearoot_from_bud_dict(x_bud, bud_dict)
    return x_bud


def set_idearoot_from_bud_dict(x_bud: BudUnit, bud_dict: dict):
    idearoot_dict = bud_dict.get("_idearoot")
    x_bud._idearoot = ideaunit_shop(
        _root=True,
        _label=x_bud._real_id,
        _parent_road="",
        _uid=get_obj_from_idea_dict(idearoot_dict, "_uid"),
        _weight=get_obj_from_idea_dict(idearoot_dict, "_weight"),
        _begin=get_obj_from_idea_dict(idearoot_dict, "_begin"),
        _close=get_obj_from_idea_dict(idearoot_dict, "_close"),
        _numor=get_obj_from_idea_dict(idearoot_dict, "_numor"),
        _denom=get_obj_from_idea_dict(idearoot_dict, "_denom"),
        _reest=get_obj_from_idea_dict(idearoot_dict, "_reest"),
        _problem_bool=get_obj_from_idea_dict(idearoot_dict, "_problem_bool"),
        _range_source_road=get_obj_from_idea_dict(idearoot_dict, "_range_source_road"),
        _numeric_road=get_obj_from_idea_dict(idearoot_dict, "_numeric_road"),
        _reasonunits=get_obj_from_idea_dict(idearoot_dict, "_reasonunits"),
        _doerunit=get_obj_from_idea_dict(idearoot_dict, "_doerunit"),
        _healerhold=get_obj_from_idea_dict(idearoot_dict, "_healerhold"),
        _factunits=get_obj_from_idea_dict(idearoot_dict, "_factunits"),
        _awardlinks=get_obj_from_idea_dict(idearoot_dict, "_awardlinks"),
        _is_expanded=get_obj_from_idea_dict(idearoot_dict, "_is_expanded"),
        _road_delimiter=get_obj_from_idea_dict(idearoot_dict, "_road_delimiter"),
        _bud_real_id=x_bud._real_id,
        _fund_coin=default_fund_coin_if_none(x_bud._fund_coin),
    )
    set_idearoot_kids_from_dict(x_bud, idearoot_dict)


def set_idearoot_kids_from_dict(x_bud: BudUnit, idearoot_dict: dict):
    to_evaluate_idea_dicts = []
    parent_road_text = "parent_road"
    # for every kid dict, set parent_road in dict, add to to_evaluate_list
    for x_dict in get_obj_from_idea_dict(idearoot_dict, "_kids").values():
        x_dict[parent_road_text] = x_bud._real_id
        to_evaluate_idea_dicts.append(x_dict)

    while to_evaluate_idea_dicts != []:
        idea_dict = to_evaluate_idea_dicts.pop(0)
        # for every kid dict, set parent_road in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_idea_dict(idea_dict, "_kids").values():
            parent_road = get_obj_from_idea_dict(idea_dict, parent_road_text)
            kid_label = get_obj_from_idea_dict(idea_dict, "_label")
            kid_dict[parent_road_text] = x_bud.make_road(parent_road, kid_label)
            to_evaluate_idea_dicts.append(kid_dict)
        x_ideakid = ideaunit_shop(
            _label=get_obj_from_idea_dict(idea_dict, "_label"),
            _weight=get_obj_from_idea_dict(idea_dict, "_weight"),
            _uid=get_obj_from_idea_dict(idea_dict, "_uid"),
            _begin=get_obj_from_idea_dict(idea_dict, "_begin"),
            _close=get_obj_from_idea_dict(idea_dict, "_close"),
            _numor=get_obj_from_idea_dict(idea_dict, "_numor"),
            _denom=get_obj_from_idea_dict(idea_dict, "_denom"),
            _reest=get_obj_from_idea_dict(idea_dict, "_reest"),
            pledge=get_obj_from_idea_dict(idea_dict, "pledge"),
            _problem_bool=get_obj_from_idea_dict(idea_dict, "_problem_bool"),
            _reasonunits=get_obj_from_idea_dict(idea_dict, "_reasonunits"),
            _doerunit=get_obj_from_idea_dict(idea_dict, "_doerunit"),
            _healerhold=get_obj_from_idea_dict(idea_dict, "_healerhold"),
            _originunit=get_obj_from_idea_dict(idea_dict, "_originunit"),
            _awardlinks=get_obj_from_idea_dict(idea_dict, "_awardlinks"),
            _factunits=get_obj_from_idea_dict(idea_dict, "_factunits"),
            _is_expanded=get_obj_from_idea_dict(idea_dict, "_is_expanded"),
            _range_source_road=get_obj_from_idea_dict(idea_dict, "_range_source_road"),
            _numeric_road=get_obj_from_idea_dict(idea_dict, "_numeric_road"),
            # _bud_real_id=x_bud._real_id,
        )
        x_bud.add_idea(x_ideakid, parent_road=idea_dict[parent_road_text])


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
