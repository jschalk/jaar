from src._road.road import (
    get_parent_road,
    is_sub_road,
    road_validate,
    change_road,
    get_terminus_node,
    get_root_node_from_road,
    find_replace_road_key_dict,
    get_ancestor_roads,
    get_default_world_id_roadnode,
    get_all_road_nodes,
    get_forefather_roads,
    create_road,
    default_road_delimiter_if_none,
    RoadNode,
    RoadUnit,
    is_string_in_road,
    OwnerID,
    PartyID,
    HealerID,
    is_roadunit_convertible_to_path,
)
from src._road.finance import get_planck_valid, default_planck_if_none
from src.agenda.meld import (
    get_meld_weight,
    MeldStrategy,
    get_meld_default,
    validate_meld_strategy,
)
from src.agenda.party import (
    PartyUnit,
    PartyLink,
    partyunits_get_from_dict,
    partyunit_shop,
    partylink_shop,
    PartyUnitExternalMetrics,
)
from src.agenda.group import (
    BalanceLink,
    GroupID,
    GroupUnit,
    get_from_dict as groupunits_get_from_dict,
    groupunit_shop,
    balancelink_shop,
)
from src.agenda.healer import HealerHold
from src.agenda.reason_idea import (
    BeliefCore,
    BeliefUnit,
    BeliefUnit,
    ReasonUnit,
    RoadUnit,
    beliefunit_shop,
)
from src.agenda.reason_assign import AssignedUnit
from src.agenda.tree_metrics import TreeMetrics, treemetrics_shop
from src.agenda.idea import (
    IdeaUnit,
    ideaunit_shop,
    ideaattrfilter_shop,
    IdeaAttrFilter,
    get_obj_from_idea_dict,
    EconID,
)
from src.agenda.hreg_time import HregTimeIdeaSource as HregIdea
from src.agenda.lemma import lemmas_shop, Lemmas
from src.agenda.origin import originunit_get_from_dict, originunit_shop, OriginUnit
from src.instrument.python import (
    get_json_from_dict,
    get_dict_from_json,
    get_1_if_None,
    get_0_if_None,
    get_False_if_None,
    get_empty_dict_if_none,
)
from src.instrument.file import dir_files, open_file
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from datetime import datetime


class InvalidAgendaException(Exception):
    pass


class InvalidLabelException(Exception):
    pass


class AssignmentPartyException(Exception):
    pass


class NewDelimiterException(Exception):
    pass


class PartyunitsCreditorDebtorSumException(Exception):
    pass


class PartyMissingException(Exception):
    pass


class Exception_econs_justified(Exception):
    pass


class _planck_RatioException(Exception):
    pass


class _last_gift_idException(Exception):
    pass


class healerhold_group_id_Exception(Exception):
    pass


@dataclass
class AgendaUnit:
    _world_id: str = None
    _owner_id: OwnerID = None
    _last_gift_id: int = None
    _weight: float = None
    _partys: dict[PartyID:PartyUnit] = None
    _groups: dict[GroupID:GroupUnit] = None
    _idearoot: IdeaUnit = None
    _max_tree_traverse: int = None
    _road_delimiter: str = None
    _planck: float = None
    _money_desc: str = None
    _party_creditor_pool: int = None
    _party_debtor_pool: int = None
    _auto_output_job_to_forum: bool = None
    _meld_strategy: MeldStrategy = None
    _originunit: OriginUnit = None  # created by ClerkUnit process
    # set_agenda_metrics Calculated field begin
    _idea_dict: dict[RoadUnit:IdeaUnit] = None
    _econ_dict: dict[RoadUnit:IdeaUnit] = None
    _healers_dict: dict[HealerID : dict[RoadUnit:IdeaUnit]] = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _econs_justified: bool = None
    _econs_buildable: bool = None
    _sum_healerhold_importance: bool = None
    # set_agenda_metrics Calculated field end

    def del_last_gift_id(self):
        self._last_gift_id = None

    def set_last_gift_id(self, x_last_gift_id: int):
        if self._last_gift_id != None and x_last_gift_id < self._last_gift_id:
            raise _last_gift_idException(
                f"Cannot set _last_gift_id to {x_last_gift_id} because it is less than {self._last_gift_id}."
            )
        self._last_gift_id = x_last_gift_id

    def set_money_desc(self, x_money_desc: str):
        self._money_desc = x_money_desc

    def set_party_pool(self, x_party_pool: int):
        self.set_party_creditor_pool(
            new_party_creditor_pool=x_party_pool,
            update_partys_creditor_weight=True,
            correct_planck_issues=True,
        )
        self.set_party_debtor_pool(
            new_party_debtor_pool=x_party_pool,
            update_partys_debtor_weight=True,
            correct_planck_issues=True,
        )

    def set_party_creditor_pool(
        self,
        new_party_creditor_pool: int,
        update_partys_creditor_weight: bool = False,
        correct_planck_issues: bool = False,
    ):
        if (new_party_creditor_pool / self._planck).is_integer() == False:
            raise _planck_RatioException(
                f"Agenda '{self._owner_id}' cannot set _party_creditor_pool='{new_party_creditor_pool}'. It is not divisible by planck '{self._planck}'"
            )

        if update_partys_creditor_weight:
            old_party_creditor_pool = self.get_partyunits_creditor_weight_sum()
            if old_party_creditor_pool != 0:
                x_ratio = new_party_creditor_pool / old_party_creditor_pool
                for x_party in self._partys.values():
                    new_party_creditor_weight = get_planck_valid(
                        num=x_party.creditor_weight * x_ratio, planck=x_party._planck
                    )
                    x_party.set_creditor_weight(new_party_creditor_weight)

        self._party_creditor_pool = new_party_creditor_pool
        if correct_planck_issues:
            self._correct_any_creditor_planck_issues()

    def _correct_any_creditor_planck_issues(self):
        if self.get_partyunits_creditor_weight_sum() != self._party_creditor_pool:
            missing_creditor_weight = (
                self._party_creditor_pool - self.get_partyunits_creditor_weight_sum()
            )
            if len(self._partys) > 0:
                partyunits = list(self._partys.values())
                # partys_count = len(self._partys)
                # planck_count = missing_creditor_weight / self._planck
                # if planck_count <= partys_count:
                for _ in range(0, missing_creditor_weight, self._planck):
                    x_partyunit = partyunits.pop()
                    x_partyunit.set_creditor_weight(
                        x_partyunit.creditor_weight + self._planck
                    )

    def set_party_debtor_pool(
        self,
        new_party_debtor_pool: int,
        update_partys_debtor_weight: bool = False,
        correct_planck_issues: bool = False,
    ):
        if (new_party_debtor_pool / self._planck).is_integer() == False:
            raise _planck_RatioException(
                f"Agenda '{self._owner_id}' cannot set _party_debtor_pool='{new_party_debtor_pool}'. It is not divisible by planck '{self._planck}'"
            )

        if update_partys_debtor_weight:
            old_party_debtor_pool = self.get_partyunits_debtor_weight_sum()
            if old_party_debtor_pool != 0:
                x_ratio = new_party_debtor_pool / old_party_debtor_pool
                for x_party in self._partys.values():
                    new_party_debtor_weight = get_planck_valid(
                        num=x_party.debtor_weight * x_ratio, planck=x_party._planck
                    )
                    x_party.set_debtor_weight(new_party_debtor_weight)
        self._party_debtor_pool = new_party_debtor_pool
        if correct_planck_issues:
            self._correct_any_debtor_planck_issues()

    def _correct_any_debtor_planck_issues(self):
        if self.get_partyunits_debtor_weight_sum() != self._party_debtor_pool:
            missing_debtor_weight = (
                self._party_debtor_pool - self.get_partyunits_debtor_weight_sum()
            )
            if len(self._partys) > 0:
                partyunits = list(self._partys.values())
                # partys_count = len(self._partys)
                # planck_count = missing_debtor_weight / self._planck
                # if planck_count <= partys_count:
                for _ in range(0, missing_debtor_weight, self._planck):
                    x_partyunit = partyunits.pop()
                    x_partyunit.set_debtor_weight(
                        x_partyunit.debtor_weight + self._planck
                    )

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
        return road_validate(x_road, self._road_delimiter, self._world_id)

    def make_l1_road(self, l1_node: RoadNode):
        return self.make_road(self._world_id, l1_node)

    def set_partys_output_agenda_meld_order(self):
        sort_partys_list = list(self._partys.values())
        sort_partys_list.sort(key=lambda x: x.party_id.lower(), reverse=False)
        for count_x, x_partyunit in enumerate(sort_partys_list):
            x_partyunit.set_output_agenda_meld_order(count_x)

    def clear_partys_output_agenda_meld_order(self):
        for x_partyunit in self._partys.values():
            x_partyunit.clear_output_agenda_meld_order()

    def set_road_delimiter(self, new_road_delimiter: str):
        self.set_agenda_metrics()
        if self._road_delimiter != new_road_delimiter:
            for x_idea_road in self._idea_dict.keys():
                if is_string_in_road(new_road_delimiter, x_idea_road):
                    raise NewDelimiterException(
                        f"Cannot change delimiter to '{new_road_delimiter}' because it already exists an idea label '{x_idea_road}'"
                    )

            # Grab pointers to every idea
            idea_pointers = {
                x_idea_road: self.get_idea_obj(x_idea_road)
                for x_idea_road in self._idea_dict.keys()
            }

            # change all road attributes in idea
            # old_road_delimiter = copy_deepcopy(self._road_delimiter)
            self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)
            for x_idea in idea_pointers.values():
                x_idea.set_road_delimiter(self._road_delimiter)

    def set_world_id(self, world_id: str):
        old_world_id = copy_deepcopy(self._world_id)
        self._world_id = world_id

        self.set_agenda_metrics()
        for idea_obj in self._idea_dict.values():
            idea_obj._agenda_world_id = self._world_id

        self.edit_idea_label(old_road=old_world_id, new_label=self._world_id)
        self.set_agenda_metrics()

    def set_partyunit_external_metrics(
        self, external_metrics: PartyUnitExternalMetrics
    ):
        party_x = self.get_party(external_metrics.internal_party_id)
        party_x._creditor_operational = external_metrics.creditor_operational
        party_x._debtor_operational = external_metrics.debtor_operational
        # self.set_partyunit(partyunit=party_x)

    def set_max_tree_traverse(self, int_x: int):
        if int_x < 2:
            raise InvalidAgendaException(
                f"set_max_tree_traverse: input '{int_x}' must be number that is 2 or greater"
            )
        else:
            self._max_tree_traverse = int_x

    def get_agenda_sprung_from_single_idea(self, road: RoadUnit) -> any:
        self.set_agenda_metrics()
        x_idea = self.get_idea_obj(road)
        new_weight = self._weight * x_idea._agenda_importance
        x_agenda = agendaunit_shop(_owner_id=self._idearoot._label, _weight=new_weight)

        for road_assc in sorted(list(self._get_relevant_roads({road}))):
            src_yx = self.get_idea_obj(road_assc)
            new_yx = copy_deepcopy(src_yx)
            if new_yx._parent_road != "":
                x_agenda.add_idea(new_yx, parent_road=new_yx._parent_road)
            x_agenda.set_agenda_metrics()

        # TODO grab groups
        # TODO grab all group partys
        # TODO grab beliefs
        return x_agenda

    def _get_relevant_roads(self, roads: dict[RoadUnit:]) -> dict[RoadUnit:str]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for road_x in roads:
            to_evaluate_list.append(road_x)
            to_evaluate_hx_dict[road_x] = "given"
        evaluated_roads = {}

        # tree_metrics = self.get_tree_metrics()
        # while roads_to_evaluate != [] and count_x <= tree_metrics.node_count:
        # changed because count_x might be wrong thing to measure
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

            if x_idea._numeric_road != None:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=x_idea._numeric_road,
                    road_type="numeric_road",
                )

            if x_idea._range_source_road != None:
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
        to_evaluate_hx_dict: dict[RoadUnit:int],
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

    def all_ideas_relevant_to_promise_idea(self, road: RoadUnit) -> bool:
        promise_idea_assoc_set = set(self._get_relevant_roads({road}))
        all_ideas_set = set(self.get_idea_tree_ordered_road_list())
        return all_ideas_set == all_ideas_set.intersection(promise_idea_assoc_set)

    def _are_all_partys_groups_are_in_idea_kid(self, road: RoadUnit) -> bool:
        idea_kid = self.get_idea_obj(road)
        # get dict of all idea balanceheirs
        balanceheir_list = idea_kid._balanceheirs.keys()
        balanceheir_dict = {
            balanceheir_group_id: 1 for balanceheir_group_id in balanceheir_list
        }
        non_single_groupunits = {
            groupunit.group_id: groupunit
            for groupunit in self._groups.values()
            if groupunit._party_mirror != True
        }
        # check all non_party_mirror_groupunits are in balanceheirs
        for non_single_group in non_single_groupunits.values():
            if balanceheir_dict.get(non_single_group.group_id) is None:
                return False

        # get dict of all partylinks that are in all balanceheirs
        balanceheir_partyunits = {}
        for balanceheir_party_id in balanceheir_dict:
            groupunit = self.get_groupunit(balanceheir_party_id)
            for partylink in groupunit._partys.values():
                balanceheir_partyunits[partylink.party_id] = self.get_party(
                    partylink.party_id
                )

        # check all agenda._partys are in balanceheir_partyunits
        return len(self._partys) == len(balanceheir_partyunits)

    def get_time_min_from_dt(self, dt: datetime) -> float:
        x_hregidea = HregIdea(self._road_delimiter)
        return x_hregidea.get_time_min_from_dt(dt=dt)

    def get_time_c400_from_min(self, min: int) -> int:
        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")
        c400_road = self.make_road(tech_road, "400 year cycle")
        c400_idea = self.get_idea_obj(c400_road)
        c400_min = c400_idea._close
        return int(min / c400_min), c400_idea, min % c400_min

    def get_time_c400yr_from_min(self, min: int):
        # GIVEN int minutes within 400 year range return year and remainder minutes
        c400_count, c400_idea, c400yr_min = self.get_time_c400_from_min(min=min)
        c100_4_96y = c400_idea.get_kids_in_range(begin=c400yr_min, close=c400yr_min)[0]
        cXXXyr_min = c400yr_min - c100_4_96y._begin

        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")

        # identify which range the time is in
        if c100_4_96y._close - c100_4_96y._begin in (
            50492160,
            52596000,
        ):  # 96 year and 100 year ideas
            yr4_1461_road = self.make_road(tech_road, "4year with leap")
            yr4_1461_idea = self.get_idea_obj(yr4_1461_road)
            yr4_cycles = int(cXXXyr_min / yr4_1461_idea._close)
            cXyr_min = cXXXyr_min % yr4_1461_idea._close
            yr1_idea = yr4_1461_idea.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[
                0
            ]
        elif c100_4_96y._close - c100_4_96y._begin == 2102400:
            yr4_1460_road = self.make_road(tech_road, "4year wo leap")
            yr4_1460_idea = self.get_idea_obj(yr4_1460_road)
            yr4_cycles = 0
            yr1_idea = yr4_1460_idea.get_kids_in_range(cXXXyr_min, cXXXyr_min)[0]
            cXyr_min = cXXXyr_min % yr4_1460_idea._close

        yr1_rem_min = cXyr_min - yr1_idea._begin
        yr1_idea_begin = int(yr1_idea._label.split("-")[0]) - 1

        c100_4_96y_begin = int(c100_4_96y._label.split("-")[0])
        year_num = c100_4_96y_begin + (4 * yr4_cycles) + yr1_idea_begin
        return year_num, yr1_idea, yr1_rem_min

    def get_time_month_from_min(self, min: int):
        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")

        year_num, yr1_idea, yr1_idea_rem_min = self.get_time_c400yr_from_min(min=min)
        yrx = None
        if yr1_idea._close - yr1_idea._begin == 525600:
            yr365_road = self.make_road(tech_road, "365 year")
            yrx = self.get_idea_obj(yr365_road)
        elif yr1_idea._close - yr1_idea._begin == 527040:
            yr366_road = self.make_road(tech_road, "366 year")
            yrx = self.get_idea_obj(yr366_road)
        mon_x = yrx.get_kids_in_range(begin=yr1_idea_rem_min, close=yr1_idea_rem_min)[0]
        month_rem_min = yr1_idea_rem_min - mon_x._begin
        month_num = int(mon_x._label.split("-")[0])
        day_road = self.make_road(tech_road, "day")
        day_x = self.get_idea_obj(day_road)
        day_num = int(month_rem_min / day_x._close)
        day_rem_min = month_rem_min % day_x._close
        return month_num, day_num, day_rem_min, day_x

    def get_time_hour_from_min(self, min: int) -> set[int, int, list[int]]:
        month_num, day_num, day_rem_min, day_x = self.get_time_month_from_min(min=min)
        hr_x = day_x.get_kids_in_range(begin=day_rem_min, close=day_rem_min)[0]
        hr_rem_min = day_rem_min - hr_x._begin
        hr_num = int(hr_x._label.split("-")[0])
        min_num = int(hr_rem_min % (hr_x._close - hr_x._begin))
        return hr_num, min_num, hr_x

    def get_time_dt_from_min(self, min: int) -> datetime:
        year_x = (
            400 * self.get_time_c400_from_min(min=min)[0]
        ) + self.get_time_c400yr_from_min(min=min)[0]
        month_num = self.get_time_month_from_min(min=min)[0]
        day_num = self.get_time_month_from_min(min=min)[1] + 1
        hr_num, min_num, hr_x = self.get_time_hour_from_min(min=min)
        return datetime(
            year=year_x, month=month_num, day=day_num, hour=hr_num, minute=min_num
        )

    def get_jajatime_legible_one_time_event(self, jajatime_min: int) -> str:
        dt_x = self.get_time_dt_from_min(min=jajatime_min)
        x_hregidea = HregIdea(self._road_delimiter)
        return x_hregidea.get_jajatime_legible_from_dt(dt=dt_x)

    def get_jajatime_repeating_legible_text(
        self, open: float = None, nigh: float = None, divisor: float = None
    ) -> str:
        x_hregidea = HregIdea(self._road_delimiter)
        str_x = "test3"
        if divisor is None:
            str_x = self.get_jajatime_legible_one_time_event(jajatime_min=open)
        elif divisor != None and divisor % 10080 == 0:
            str_x = self._get_jajatime_week_legible_text(open, divisor)
        elif divisor != None and divisor % 1440 == 0:
            if divisor == 1440:
                str_x = (
                    f"every day at {x_hregidea.convert1440toReadableTime(min1440=open)}"
                )
            else:
                num_days = int(divisor / 1440)
                num_with_letter_ending = x_hregidea.get_number_with_letter_ending(
                    num=num_days
                )
                str_x = f"every {num_with_letter_ending} day at {x_hregidea.convert1440toReadableTime(min1440=open)}"
        else:
            str_x = "unknown"
        return str_x

    def _get_jajatime_week_legible_text(self, open: int, divisor: int) -> str:
        x_hregidea = HregIdea(self._road_delimiter)
        open_in_week = open % divisor
        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")
        week_road = self.make_road(tech_road, "week")
        weekday_ideas_dict = self.get_idea_ranged_kids(
            idea_road=week_road, begin=open_in_week
        )
        weekday_idea_node = None
        for idea in weekday_ideas_dict.values():
            weekday_idea_node = idea

        if divisor == 10080:
            return f"every {weekday_idea_node._label} at {x_hregidea.convert1440toReadableTime(min1440=open % 1440)}"
        num_with_letter_ending = x_hregidea.get_number_with_letter_ending(
            num=divisor // 10080
        )
        return f"every {num_with_letter_ending} {weekday_idea_node._label} at {x_hregidea.convert1440toReadableTime(min1440=open % 1440)}"

    def get_partys_metrics(self) -> dict[GroupID:BalanceLink]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.balancelinks_metrics

    def add_to_group_agenda_credit_debt(
        self,
        group_id: GroupID,
        balanceheir_agenda_credit: float,
        balanceheir_agenda_debt: float,
    ):
        for group in self._groups.values():
            if group.group_id == group_id:
                group._agenda_credit += balanceheir_agenda_credit
                group._agenda_debt += balanceheir_agenda_debt

    def add_to_group_agenda_intent_credit_debt(
        self,
        group_id: GroupID,
        balanceline_agenda_credit: float,
        balanceline_agenda_debt: float,
    ):
        for group in self._groups.values():
            if (
                group.group_id == group_id
                and balanceline_agenda_credit != None
                and balanceline_agenda_debt != None
            ):
                group._agenda_intent_credit += balanceline_agenda_credit
                group._agenda_intent_debt += balanceline_agenda_debt

    def add_to_partyunit_agenda_credit_debt(
        self,
        partyunit_party_id: PartyID,
        agenda_credit,
        agenda_debt: float,
        agenda_intent_credit: float,
        agenda_intent_debt: float,
    ):
        for partyunit in self._partys.values():
            if partyunit.party_id == partyunit_party_id:
                partyunit.add_agenda_credit_debt(
                    agenda_credit=agenda_credit,
                    agenda_debt=agenda_debt,
                    agenda_intent_credit=agenda_intent_credit,
                    agenda_intent_debt=agenda_intent_debt,
                )

    def del_partyunit(self, party_id: str):
        self._groups.pop(party_id)
        self._partys.pop(party_id)

    def add_partyunit(
        self,
        party_id: PartyID,
        creditor_weight: int = None,
        debtor_weight: int = None,
        depotlink_type: str = None,
    ):
        partyunit = partyunit_shop(
            party_id=party_id,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            depotlink_type=depotlink_type,
        )
        self.set_partyunit(partyunit=partyunit)

    def set_partyunit(self, partyunit: PartyUnit):
        # future: if party is new check existance of group with party party_id
        if partyunit._road_delimiter != self._road_delimiter:
            partyunit._road_delimiter = self._road_delimiter
        if partyunit._planck != self._planck:
            partyunit._planck = self._planck
        self._partys[partyunit.party_id] = partyunit

        try:
            self._groups[partyunit.party_id]
        except KeyError:
            partylink = partylink_shop(
                party_id=PartyID(partyunit.party_id), creditor_weight=1, debtor_weight=1
            )
            partylinks = {partylink.party_id: partylink}
            group_unit = groupunit_shop(
                partyunit.party_id, _party_mirror=True, _partys=partylinks
            )
            self.set_groupunit(y_groupunit=group_unit)

    def edit_partyunit_party_id(
        self,
        old_party_id: PartyID,
        new_party_id: PartyID,
        allow_party_overwite: bool,
        allow_nonsingle_group_overwrite: bool,
    ):
        # Handle scenarios: some are unacceptable
        old_party_id_creditor_weight = self.get_party(old_party_id).creditor_weight
        new_party_id_groupunit = self.get_groupunit(new_party_id)
        new_party_id_partyunit = self.get_party(new_party_id)
        if not allow_party_overwite and new_party_id_partyunit != None:
            raise InvalidAgendaException(
                f"Party '{old_party_id}' change to '{new_party_id}' failed since '{new_party_id}' exists."
            )
        elif (
            not allow_nonsingle_group_overwrite
            and new_party_id_groupunit != None
            and new_party_id_groupunit._party_mirror == False
        ):
            raise InvalidAgendaException(
                f"Party '{old_party_id}' change to '{new_party_id}' failed since non-single group '{new_party_id}' exists."
            )
        elif (
            allow_nonsingle_group_overwrite
            and new_party_id_groupunit != None
            and new_party_id_groupunit._party_mirror == False
        ):
            self.del_groupunit(group_id=new_party_id)
        elif self.get_party(new_party_id) != None:
            old_party_id_creditor_weight += new_party_id_partyunit.creditor_weight

        # upsert new partyunit
        self.add_partyunit(
            party_id=new_party_id, creditor_weight=old_party_id_creditor_weight
        )
        # change all influenced groupunits partylinks
        for old_party_group_id in self.get_party_group_ids(old_party_id):
            old_party_groupunit = self.get_groupunit(old_party_group_id)
            old_party_groupunit._shift_partylink(old_party_id, new_party_id)
        self.del_partyunit(party_id=old_party_id)

    def edit_partyunit(
        self,
        party_id: PartyID,
        creditor_weight: int = None,
        debtor_weight: int = None,
        depotlink_type: str = None,
    ):
        if self._partys.get(party_id) is None:
            raise PartyMissingException(f"PartyUnit '{party_id}' does not exist.")
        x_partyunit = self.get_party(party_id)
        if creditor_weight != None:
            x_partyunit.set_creditor_weight(creditor_weight)
        if debtor_weight != None:
            x_partyunit.set_debtor_weight(debtor_weight)
        if depotlink_type != None:
            x_partyunit.set_depotlink_type(depotlink_type)
        self.set_partyunit(x_partyunit)

    def get_party(self, party_id: PartyID) -> PartyUnit:
        return self._partys.get(party_id)

    def get_partyunits_party_id_list(self) -> dict[PartyID]:
        party_id_list = list(self._partys.keys())
        party_id_list.append("")
        party_id_dict = {party_id.lower(): party_id for party_id in party_id_list}
        party_id_lowercase_ordered_list = sorted(list(party_id_dict))
        return [
            party_id_dict[party_id_l] for party_id_l in party_id_lowercase_ordered_list
        ]

    def get_partys_depotlink_count(self) -> int:
        return sum(party_x.depotlink_type != None for party_x in self._partys.values())

    def set_groupunit(
        self,
        y_groupunit: GroupUnit,
        create_missing_partys: bool = None,
        replace: bool = True,
        add_partylinks: bool = None,
    ):
        if replace is None:
            replace = False
        if add_partylinks is None:
            add_partylinks = False
        if (
            self.get_groupunit(y_groupunit.group_id) is None
            or replace
            and not add_partylinks
        ):
            self._groups[y_groupunit.group_id] = y_groupunit

        if add_partylinks:
            x_groupunit = self.get_groupunit(y_groupunit.group_id)
            for x_partylink in y_groupunit._partys.values():
                x_groupunit.set_partylink(x_partylink)

        if create_missing_partys:
            self._create_missing_partys(partylinks=y_groupunit._partys)

    def get_groupunit(self, x_group_id: GroupID) -> GroupUnit:
        return self._groups.get(x_group_id)

    def _create_missing_partys(self, partylinks: dict[PartyID:PartyLink]):
        for partylink_x in partylinks.values():
            if self.get_party(partylink_x.party_id) is None:
                self.set_partyunit(
                    partyunit=partyunit_shop(
                        party_id=partylink_x.party_id,
                        creditor_weight=partylink_x.creditor_weight,
                        debtor_weight=partylink_x.debtor_weight,
                    )
                )

    def del_groupunit(self, group_id: GroupID):
        self._groups.pop(group_id)

    def edit_groupunit_group_id(
        self, old_group_id: GroupID, new_group_id: GroupID, allow_group_overwite: bool
    ):
        if not allow_group_overwite and self.get_groupunit(new_group_id) != None:
            raise InvalidAgendaException(
                f"Group '{old_group_id}' change to '{new_group_id}' failed since '{new_group_id}' exists."
            )
        elif self.get_groupunit(new_group_id) != None:
            old_groupunit = self.get_groupunit(old_group_id)
            old_groupunit.set_group_id(group_id=new_group_id)
            self.get_groupunit(new_group_id).merge(other_group=old_groupunit)
            self.del_groupunit(group_id=old_group_id)
        elif self.get_groupunit(new_group_id) is None:
            old_groupunit = self.get_groupunit(old_group_id)
            groupunit_x = groupunit_shop(
                new_group_id, old_groupunit._party_mirror, old_groupunit._partys
            )
            self.set_groupunit(y_groupunit=groupunit_x)
            self.del_groupunit(group_id=old_group_id)

        self._edit_balancelinks_group_id(
            old_group_id=old_group_id,
            new_group_id=new_group_id,
            allow_group_overwite=allow_group_overwite,
        )

    def _edit_balancelinks_group_id(
        self,
        old_group_id: GroupID,
        new_group_id: GroupID,
        allow_group_overwite: bool,
    ):
        for x_idea in self.get_idea_dict().values():
            if (
                x_idea._balancelinks.get(new_group_id) != None
                and x_idea._balancelinks.get(old_group_id) != None
            ):
                old_balancelink = x_idea._balancelinks.get(old_group_id)
                old_balancelink.group_id = new_group_id
                x_idea._balancelinks.get(new_group_id).meld(
                    other_balancelink=old_balancelink,
                    other_meld_strategy="sum",
                    src_meld_strategy="sum",
                )

                x_idea.del_balancelink(group_id=old_group_id)
            elif (
                x_idea._balancelinks.get(new_group_id) is None
                and x_idea._balancelinks.get(old_group_id) != None
            ):
                old_balancelink = x_idea._balancelinks.get(old_group_id)
                new_balancelink = balancelink_shop(
                    group_id=new_group_id,
                    creditor_weight=old_balancelink.creditor_weight,
                    debtor_weight=old_balancelink.debtor_weight,
                )
                x_idea.set_balancelink(balancelink=new_balancelink)
                x_idea.del_balancelink(group_id=old_group_id)

    def set_time_beliefs(self, open: datetime = None, nigh: datetime = None) -> None:
        open_minutes = self.get_time_min_from_dt(dt=open) if open != None else None
        nigh_minutes = self.get_time_min_from_dt(dt=nigh) if nigh != None else None
        time_road = self.make_l1_road("time")
        minutes_belief = self.make_road(time_road, "jajatime")
        self.set_belief(
            base=minutes_belief,
            pick=minutes_belief,
            open=open_minutes,
            nigh=nigh_minutes,
        )

    def _is_idea_rangeroot(self, idea_road: RoadUnit) -> bool:
        if self._world_id == idea_road:
            raise InvalidAgendaException(
                "its difficult to foresee a scenario where idearoot is rangeroot"
            )
        parent_road = get_parent_road(idea_road)
        parent_idea = self.get_idea_obj(parent_road)
        x_idea = self.get_idea_obj(idea_road)
        return x_idea._numeric_road is None and not parent_idea.is_arithmetic()

    def _get_rangeroot_beliefunits(self) -> list[BeliefUnit]:
        return [
            belief
            for belief in self._idearoot._beliefunits.values()
            if belief.open != None
            and belief.nigh != None
            and self._is_idea_rangeroot(idea_road=belief.base)
        ]

    def _get_rangeroot_1stlevel_associates(
        self, ranged_beliefunits: list[IdeaUnit]
    ) -> Lemmas:
        x_lemmas = lemmas_shop()
        # lemma_ideas = {}
        for belief in ranged_beliefunits:
            belief_idea = self.get_idea_obj(belief.base)
            for kid in belief_idea._kids.values():
                x_lemmas.eval(x_idea=kid, src_belief=belief, src_idea=belief_idea)

            if belief_idea._range_source_road != None:
                x_lemmas.eval(
                    x_idea=self.get_idea_obj(belief_idea._range_source_road),
                    src_belief=belief,
                    src_idea=belief_idea,
                )
        return x_lemmas

    def _get_lemma_beliefunits(self) -> dict[RoadUnit:BeliefUnit]:
        # get all range-root first level kids and range_source_road
        x_lemmas = self._get_rangeroot_1stlevel_associates(
            self._get_rangeroot_beliefunits()
        )

        # Now get associates (all their descendants and range_source_roads)
        lemma_beliefunits = {}  # belief.base : beliefUnit
        count_x = 0
        while x_lemmas.is_lemmas_evaluated() == False or count_x > 10000:
            count_x += 1
            if count_x == 9998:
                raise InvalidAgendaException("lemma loop failed")

            y_lemma = x_lemmas.get_unevaluated_lemma()
            lemma_idea = y_lemma.x_idea
            belief_x = y_lemma.calc_belief

            road_x = self.make_road(lemma_idea._parent_road, lemma_idea._label)
            lemma_beliefunits[road_x] = belief_x

            for kid2 in lemma_idea._kids.values():
                x_lemmas.eval(x_idea=kid2, src_belief=belief_x, src_idea=lemma_idea)
            if lemma_idea._range_source_road not in [None, ""]:
                x_lemmas.eval(
                    x_idea=self.get_idea_obj(lemma_idea._range_source_road),
                    src_belief=belief_x,
                    src_idea=lemma_idea,
                )

        return lemma_beliefunits

    def set_belief(
        self,
        base: RoadUnit,
        pick: RoadUnit = None,
        open: float = None,
        nigh: float = None,
        create_missing_ideas: bool = None,
    ):
        if pick is None:
            pick = base
        if create_missing_ideas:
            self._set_ideakid_if_empty(road=base)
            self._set_ideakid_if_empty(road=pick)

        self._execute_tree_traverse()
        belief_base_idea = self.get_idea_obj(base)
        x_idearoot = self.get_idea_obj(self._world_id)
        x_open = None
        if nigh != None and open is None:
            x_open = x_idearoot._beliefunits.get(base).open
        else:
            x_open = open
        x_nigh = None
        if open != None and nigh is None:
            x_nigh = x_idearoot._beliefunits.get(base).nigh
        else:
            x_nigh = nigh
        x_beliefunit = beliefunit_shop(base=base, pick=pick, open=x_open, nigh=x_nigh)

        if belief_base_idea.is_arithmetic() == False:
            x_idearoot.set_beliefunit(x_beliefunit)

        # if belief's idea no range or is a "range-root" then allow belief to be set by user
        elif (
            belief_base_idea.is_arithmetic() and self._is_idea_rangeroot(base) == False
        ):
            raise InvalidAgendaException(
                f"Non range-root belief:{base} can only be set by range-root belief"
            )

        elif belief_base_idea.is_arithmetic() and self._is_idea_rangeroot(base):
            # WHEN idea is "range-root" identify any reason.bases that are descendants
            # calculate and set those descendant beliefs
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendant
            # there exists a reason base "timeline,weeks" with premise.need = "timeline,weeks"
            # and (1,2) divisor=2 (every other week)
            #
            # user should not set "timeline,weeks" belief, only "timeline" belief and
            # "timeline,weeks" should be set automatica_lly since there exists a reason
            # that has that base.
            x_idearoot.set_beliefunit(x_beliefunit)

            # Find all Belief descendants and any range_source_road connections "Lemmas"
            lemmas_dict = self._get_lemma_beliefunits()
            missing_beliefs = self.get_missing_belief_bases().keys()
            x_idearoot._apply_any_range_source_road_connections(
                lemmas_dict, missing_beliefs
            )

        self.set_agenda_metrics()

    def get_beliefunits_base_and_belief_list(self) -> list:
        belief_list = list(self._idearoot._beliefunits.values())
        node_dict = {belief_x.base.lower(): belief_x for belief_x in belief_list}
        node_lowercase_ordered_list = sorted(list(node_dict))
        node_orginalcase_ordered_list = [
            node_dict[node_l] for node_l in node_lowercase_ordered_list
        ]

        list_x = [["", ""]]
        list_x.extend(
            [belief_x.base, belief_x.pick] for belief_x in node_orginalcase_ordered_list
        )
        return list_x

    def del_belief(self, base: RoadUnit):
        self._idearoot.del_beliefunit(base)

    def get_idea_dict(self, problem: bool = None) -> dict[RoadUnit:IdeaUnit]:
        self.set_agenda_metrics()
        if not problem:
            return self._idea_dict
        if self._econs_justified == False:
            raise Exception_econs_justified(
                f"Cannot return problem set because _econs_justified={self._econs_justified}."
            )

        return {
            x_idea.get_road(): x_idea
            for x_idea in self._idea_dict.values()
            if x_idea._problem_bool
        }

    def get_tree_metrics(self) -> TreeMetrics:
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_node(
            level=self._idearoot._level,
            reasons=self._idearoot._reasonunits,
            balancelinks=self._idearoot._balancelinks,
            uid=self._idearoot._uid,
            promise=self._idearoot.promise,
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
            balancelinks=idea_kid._balancelinks,
            uid=idea_kid._uid,
            promise=idea_kid.promise,
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

    def get_reason_bases(self) -> dict[RoadUnit:int]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.reason_bases

    def get_missing_belief_bases(self) -> dict[RoadUnit:int]:
        tree_metrics = self.get_tree_metrics()
        reason_bases = tree_metrics.reason_bases
        missing_bases = {}
        for base, base_count in reason_bases.items():
            try:
                self._idearoot._beliefunits[base]
            except KeyError:
                missing_bases[base] = base_count

        return missing_bases

    def add_l1_idea(
        self,
        idea_kid: IdeaUnit,
        create_missing_ideas_groups: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.add_idea(
            idea_kid=idea_kid,
            parent_road=self._world_id,
            create_missing_ideas_groups=create_missing_ideas_groups,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def add_idea(
        self,
        idea_kid: IdeaUnit,
        parent_road: RoadUnit,
        create_missing_ideas_groups: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        if self._idearoot._label != get_root_node_from_road(
            parent_road, self._road_delimiter
        ):
            raise InvalidAgendaException(
                f"add_idea failed because parent_road '{parent_road}' has an invalid root node"
            )

        idea_kid._road_delimiter = self._road_delimiter
        if idea_kid._agenda_world_id != self._world_id:
            idea_kid._agenda_world_id = self._world_id
        if not create_missing_ideas_groups:
            idea_kid = self._get_filtered_balancelinks_idea(idea_kid)
        idea_kid.set_parent_road(parent_road=parent_road)

        # create any missing ideas
        if not create_missing_ancestors and self.idea_exists(parent_road) == False:
            raise InvalidAgendaException(
                f"add_idea failed because '{parent_road}' idea does not exist."
            )
        parent_road_idea = self.get_idea_obj(parent_road, create_missing_ancestors)
        parent_road_idea.add_kid(idea_kid)

        kid_road = self.make_road(parent_road, idea_kid._label)
        if adoptees != None:
            weight_sum = 0
            for adoptee_label in adoptees:
                adoptee_road = self.make_road(parent_road, adoptee_label)
                adoptee_idea = self.get_idea_obj(adoptee_road)
                weight_sum += adoptee_idea._weight
                new_adoptee_parent_road = self.make_road(kid_road, adoptee_label)
                self.add_idea(adoptee_idea, new_adoptee_parent_road)
                self.edit_idea_attr(
                    road=new_adoptee_parent_road, weight=adoptee_idea._weight
                )
                self.del_idea_obj(adoptee_road)

            if bundling:
                self.edit_idea_attr(road=kid_road, weight=weight_sum)

        if create_missing_ideas_groups:
            self._create_missing_ideas(road=kid_road)
            self._create_missing_groups_partys(balancelinks=idea_kid._balancelinks)

    def _get_filtered_balancelinks_idea(self, x_idea: IdeaUnit) -> IdeaUnit:
        _balancelinks_to_delete = [
            _balancelink_group_id
            for _balancelink_group_id in x_idea._balancelinks.keys()
            if self.get_groupunit(_balancelink_group_id) is None
        ]
        for _balancelink_group_id in _balancelinks_to_delete:
            x_idea._balancelinks.pop(_balancelink_group_id)

        if x_idea._assignedunit != None:
            _suffgroups_to_delete = [
                _suffgroup_group_id
                for _suffgroup_group_id in x_idea._assignedunit._suffgroups.keys()
                if self.get_groupunit(_suffgroup_group_id) is None
            ]
            for _suffgroup_group_id in _suffgroups_to_delete:
                x_idea._assignedunit.del_suffgroup(_suffgroup_group_id)

        return x_idea

    def _create_missing_groups_partys(self, balancelinks: dict[GroupID:BalanceLink]):
        for balancelink_x in balancelinks.values():
            if self.get_groupunit(balancelink_x.group_id) is None:
                groupunit_x = groupunit_shop(
                    group_id=balancelink_x.group_id, _partys={}
                )
                self.set_groupunit(y_groupunit=groupunit_x)

    def _create_missing_ideas(self, road):
        self.set_agenda_metrics()
        posted_idea = self.get_idea_obj(road)

        for reason_x in posted_idea._reasonunits.values():
            self._set_ideakid_if_empty(road=reason_x.base)
            for premise_x in reason_x.premises.values():
                self._set_ideakid_if_empty(road=premise_x.need)
        if posted_idea._range_source_road != None:
            self._set_ideakid_if_empty(road=posted_idea._range_source_road)
        if posted_idea._numeric_road != None:
            self._set_ideakid_if_empty(road=posted_idea._numeric_road)

    def _set_ideakid_if_empty(self, road: RoadUnit):
        if self.idea_exists(road) == False:
            self.add_idea(
                ideaunit_shop(get_terminus_node(road, self._road_delimiter)),
                parent_road=get_parent_road(road),
            )

    def del_idea_obj(self, road: RoadUnit, del_children: bool = True):
        if road == self._idearoot.get_road():
            raise InvalidAgendaException("Idearoot cannot be deleted")
        parent_road = get_parent_road(road)
        if self.idea_exists(road):
            if not del_children:
                self._shift_idea_kids(x_road=road)
            parent_idea = self.get_idea_obj(parent_road)
            parent_idea.del_kid(get_terminus_node(road, self._road_delimiter))
        self.set_agenda_metrics()

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
                f"Cannot change '{old_road}' because new_label {new_label} contains delimiter {self._road_delimiter}"
            )
        if self.idea_exists(old_road) == False:
            raise InvalidAgendaException(f"Idea {old_road=} does not exist")

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
            self._idearoot._beliefunits = find_replace_road_key_dict(
                dict_x=self._idearoot._beliefunits,
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
            if listed_idea._kids != None:
                for idea_kid in listed_idea._kids.values():
                    idea_iter_list.append(idea_kid)
                    if is_sub_road(
                        ref_road=idea_kid._parent_road,
                        sub_road=old_road,
                    ):
                        idea_kid._parent_road = change_road(
                            current_road=idea_kid._parent_road,
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
            x_iaf.addin != None
            or x_iaf.numor != None
            or x_iaf.denom != None
            or x_iaf.reest != None
        ) and len(anc_roads) == 1:
            raise InvalidAgendaException("Root Idea cannot have numor denom reest.")
        parent_road = self._world_id if len(anc_roads) == 1 else anc_roads[1]

        parent_has_range = None
        parent_idea = self.get_idea_obj(parent_road)
        parent_begin = parent_idea._begin
        parent_close = parent_idea._close
        parent_has_range = parent_begin is not None and parent_close is not None

        numeric_begin = None
        numeric_close = None
        numeric_range = None
        if x_iaf.numeric_road != None:
            numeric_idea = self.get_idea_obj(x_iaf.numeric_road)
            numeric_begin = numeric_idea._begin
            numeric_close = numeric_idea._close
            numeric_range = numeric_begin != None and numeric_close != None

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
            raise InvalidAgendaException(
                "Idea has begin-close range parent, cannot have numeric_road"
            )
        elif not parent_has_range and not numeric_range and x_iaf.numor != None:
            raise InvalidAgendaException(
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
    ):
        if not reest and parent_has_range and numor != None:
            begin = parent_begin * numor / denom
            close = parent_close * numor / denom
        elif not reest and parent_has_range and numor is None:
            begin = parent_begin
            close = parent_close
        elif not reest and numeric_range and numor != None:
            begin = numeric_begin * numor / denom
            close = numeric_close * numor / denom
        elif not reest and numeric_range and numor is None:
            begin = numeric_begin
            close = numeric_close
        elif reest and parent_has_range and numor != None:
            begin = parent_begin * numor % denom
            close = parent_close * numor % denom
        elif reest and parent_has_range and numor is None:
            begin = 0
            close = parent_close - parent_begin
        elif reest and numeric_range and numor != None:
            begin = numeric_begin * numor % denom
            close = numeric_close * numor % denom
        elif reest and numeric_range and numor is None:
            begin = 0
            close = parent_close - parent_begin
        else:
            begin = begin
            close = close

        return begin, close

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
        reason_suff_idea_active: str = None,
        assignedunit: AssignedUnit = None,
        healerhold: HealerHold = None,
        begin: float = None,
        close: float = None,
        addin: float = None,
        numor: float = None,
        denom: float = None,
        reest: bool = None,
        numeric_road: RoadUnit = None,
        range_source_road: float = None,
        promise: bool = None,
        beliefunit: BeliefUnit = None,
        descendant_promise_count: int = None,
        all_party_credit: bool = None,
        all_party_debt: bool = None,
        balancelink: BalanceLink = None,
        balancelink_del: GroupID = None,
        is_expanded: bool = None,
        meld_strategy: MeldStrategy = None,
        problem_bool: bool = None,
    ):
        if healerhold != None:
            for x_group_id in healerhold._group_ids:
                if self._groups.get(x_group_id) is None:
                    raise healerhold_group_id_Exception(
                        f"Idea cannot edit healerhold because group_id '{x_group_id}' does not exist as group in Agenda"
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
            reason_suff_idea_active=reason_suff_idea_active,
            assignedunit=assignedunit,
            healerhold=healerhold,
            begin=begin,
            close=close,
            addin=addin,
            numor=numor,
            denom=denom,
            reest=reest,
            numeric_road=numeric_road,
            range_source_road=range_source_road,
            descendant_promise_count=descendant_promise_count,
            all_party_credit=all_party_credit,
            all_party_debt=all_party_debt,
            balancelink=balancelink,
            balancelink_del=balancelink_del,
            is_expanded=is_expanded,
            promise=promise,
            beliefunit=beliefunit,
            meld_strategy=meld_strategy,
            problem_bool=problem_bool,
        )
        if x_ideaattrfilter.has_numeric_attrs():
            self._set_ideaattrfilter_begin_close(x_ideaattrfilter, road)
        if x_ideaattrfilter.has_reason_premise():
            self._set_ideaattrfilter_premise_ranges(x_ideaattrfilter)
        x_idea = self.get_idea_obj(road)
        x_idea._set_idea_attr(idea_attr=x_ideaattrfilter)

        # deleting or setting a balancelink reqquires a tree traverse to correctly set balanceheirs and balancelines
        if balancelink_del != None or balancelink != None:
            self.set_agenda_metrics()

    def get_intent_dict(
        self,
        base: RoadUnit = None,
        intent_enterprise: bool = True,
        intent_state: bool = True,
    ) -> dict[RoadUnit:IdeaUnit]:
        self.set_agenda_metrics()
        return {
            x_idea.get_road(): x_idea
            for x_idea in self._idea_dict.values()
            if x_idea.is_intent_item(necessary_base=base)
        }

    def set_intent_task_complete(self, task_road: RoadUnit, base: RoadUnit):
        promise_item = self.get_idea_obj(task_road)
        promise_item.set_beliefunit_to_complete(self._idearoot._beliefunits[base])

    def is_partyunits_creditor_weight_sum_correct(self) -> bool:
        x_sum = self.get_partyunits_creditor_weight_sum()
        return (
            x_sum in (0, self._party_creditor_pool) or self._party_creditor_pool is None
        )

    def is_partyunits_debtor_weight_sum_correct(self) -> bool:
        x_sum = self.get_partyunits_debtor_weight_sum()
        return self._party_debtor_pool is None or x_sum in (self._party_debtor_pool, 0)

    def get_partyunits_creditor_weight_sum(self) -> float:
        return sum(
            partyunit.get_creditor_weight() for partyunit in self._partys.values()
        )

    def get_partyunits_debtor_weight_sum(self) -> float:
        return sum(partyunit.get_debtor_weight() for partyunit in self._partys.values())

    def _add_to_partyunits_agenda_credit_debt(self, idea_agenda_importance: float):
        sum_partyunit_creditor_weight = self.get_partyunits_creditor_weight_sum()
        sum_partyunit_debtor_weight = self.get_partyunits_debtor_weight_sum()

        for x_partyunit in self._partys.values():
            au_agenda_credit = (
                idea_agenda_importance * x_partyunit.get_creditor_weight()
            ) / sum_partyunit_creditor_weight

            au_agenda_debt = (
                idea_agenda_importance * x_partyunit.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            x_partyunit.add_agenda_credit_debt(
                agenda_credit=au_agenda_credit,
                agenda_debt=au_agenda_debt,
                agenda_intent_credit=0,
                agenda_intent_debt=0,
            )

    def _add_to_partyunits_agenda_intent_credit_debt(
        self, idea_agenda_importance: float
    ):
        sum_partyunit_creditor_weight = self.get_partyunits_creditor_weight_sum()
        sum_partyunit_debtor_weight = self.get_partyunits_debtor_weight_sum()

        for x_partyunit in self._partys.values():
            au_agenda_intent_credit = (
                idea_agenda_importance * x_partyunit.get_creditor_weight()
            ) / sum_partyunit_creditor_weight

            au_agenda_intent_debt = (
                idea_agenda_importance * x_partyunit.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            x_partyunit.add_agenda_credit_debt(
                agenda_credit=0,
                agenda_debt=0,
                agenda_intent_credit=au_agenda_intent_credit,
                agenda_intent_debt=au_agenda_intent_debt,
            )

    def _set_partyunits_agenda_intent_importance(self, agenda_intent_importance: float):
        sum_partyunit_creditor_weight = self.get_partyunits_creditor_weight_sum()
        sum_partyunit_debtor_weight = self.get_partyunits_debtor_weight_sum()

        for x_partyunit in self._partys.values():
            au_agenda_intent_credit = (
                agenda_intent_importance * x_partyunit.get_creditor_weight()
            ) / sum_partyunit_creditor_weight

            au_agenda_intent_debt = (
                agenda_intent_importance * x_partyunit.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            x_partyunit.add_agenda_intent_credit_debt(
                agenda_intent_credit=au_agenda_intent_credit,
                agenda_intent_debt=au_agenda_intent_debt,
            )

    def _reset_groupunits_agenda_credit_debt(self):
        for balancelink_obj in self._groups.values():
            balancelink_obj.reset_agenda_credit_debt()

    def _set_groupunits_agenda_importance(
        self, balanceheirs: dict[GroupID:BalanceLink]
    ):
        for balancelink_obj in balanceheirs.values():
            self.add_to_group_agenda_credit_debt(
                group_id=balancelink_obj.group_id,
                balanceheir_agenda_credit=balancelink_obj._agenda_credit,
                balanceheir_agenda_debt=balancelink_obj._agenda_debt,
            )

    def _distribute_agenda_intent_importance(self):
        for idea in self._idea_dict.values():
            # If there are no balancelines associated with idea
            # distribute agenda_importance via general partyunit
            # credit ratio and debt ratio
            # if idea.is_intent_item() and idea._balancelines == {}:
            if idea.is_intent_item():
                if idea._balancelines == {}:
                    self._add_to_partyunits_agenda_intent_credit_debt(
                        idea._agenda_importance
                    )
                else:
                    for x_balanceline in idea._balancelines.values():
                        self.add_to_group_agenda_intent_credit_debt(
                            group_id=x_balanceline.group_id,
                            balanceline_agenda_credit=x_balanceline._agenda_credit,
                            balanceline_agenda_debt=x_balanceline._agenda_debt,
                        )

    def _distribute_groups_agenda_importance(self):
        for group_obj in self._groups.values():
            group_obj._set_partylink_agenda_credit_debt()
            for partylink in group_obj._partys.values():
                self.add_to_partyunit_agenda_credit_debt(
                    partyunit_party_id=partylink.party_id,
                    agenda_credit=partylink._agenda_credit,
                    agenda_debt=partylink._agenda_debt,
                    agenda_intent_credit=partylink._agenda_intent_credit,
                    agenda_intent_debt=partylink._agenda_intent_debt,
                )

    def _set_agenda_intent_ratio_credit_debt(self):
        agenda_intent_ratio_credit_sum = 0
        agenda_intent_ratio_debt_sum = 0

        for x_partyunit in self._partys.values():
            agenda_intent_ratio_credit_sum += x_partyunit._agenda_intent_credit
            agenda_intent_ratio_debt_sum += x_partyunit._agenda_intent_debt

        for x_partyunit in self._partys.values():
            x_partyunit.set_agenda_intent_ratio_credit_debt(
                agenda_intent_ratio_credit_sum=agenda_intent_ratio_credit_sum,
                agenda_intent_ratio_debt_sum=agenda_intent_ratio_debt_sum,
                agenda_partyunit_total_creditor_weight=self.get_partyunits_creditor_weight_sum(),
                agenda_partyunit_total_debtor_weight=self.get_partyunits_debtor_weight_sum(),
            )

    def get_party_group_ids(self, party_id: PartyID) -> list[GroupID]:
        return [
            x_groupunit.group_id
            for x_groupunit in self._groups.values()
            if x_groupunit.partylink_exists(party_id)
        ]

    def _reset_partyunit_agenda_credit_debt(self):
        for partyunit in self._partys.values():
            partyunit.reset_agenda_credit_debt()

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
            raise InvalidAgendaException("get_idea_obj received road=None")
        if self.idea_exists(road) == False and not if_missing_create:
            raise InvalidAgendaException(f"get_idea_obj failed. no item at '{road}'")
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
        elif begin != None and close is None:
            close = begin

        idea_list = parent_idea.get_kids_in_range(begin=begin, close=close)
        return {x_idea._label: x_idea for x_idea in idea_list}

    def _set_ancestors_metrics(self, road: RoadUnit, econ_exceptions: bool = False):
        task_count = 0
        child_balancelines = None
        group_everyone = None
        ancestor_roads = get_ancestor_roads(road=road)
        econ_justified_by_problem = True
        healerhold_count = 0

        while ancestor_roads != []:
            youngest_road = ancestor_roads.pop(0)
            # _set_non_root_ancestor_metrics(youngest_road, task_count, group_everyone)
            x_idea_obj = self.get_idea_obj(road=youngest_road)
            x_idea_obj.add_to_descendant_promise_count(task_count)
            if x_idea_obj.is_kidless():
                x_idea_obj.set_kidless_balancelines()
                child_balancelines = x_idea_obj._balancelines
            else:
                x_idea_obj.set_balancelines(child_balancelines=child_balancelines)

            if x_idea_obj._task:
                task_count += 1

            if (
                group_everyone != False
                and x_idea_obj._all_party_credit != False
                and x_idea_obj._all_party_debt != False
                and x_idea_obj._balanceheirs != {}
            ) or (
                group_everyone != False
                and x_idea_obj._all_party_credit == False
                and x_idea_obj._all_party_debt == False
            ):
                group_everyone = False
            elif group_everyone != False:
                group_everyone = True
            x_idea_obj._all_party_credit = group_everyone
            x_idea_obj._all_party_debt = group_everyone

            if x_idea_obj._healerhold.any_group_id_exists():
                econ_justified_by_problem = False
                healerhold_count += 1
                self._sum_healerhold_importance += x_idea_obj._agenda_importance
            if x_idea_obj._problem_bool:
                econ_justified_by_problem = True

        if econ_justified_by_problem == False or healerhold_count > 1:
            if econ_exceptions:
                raise Exception_econs_justified(
                    f"IdeaUnit '{road}' cannot sponsor ancestor econs."
                )
            self._econs_justified = False

    def _set_root_attributes(self, econ_exceptions: bool):
        x_idearoot = self._idearoot
        x_idearoot._level = 0
        x_idearoot.set_parent_road(parent_road="")
        x_idearoot.set_idearoot_inherit_reasonheirs()
        x_idearoot.set_assignedheir(parent_assignheir=None, agenda_groups=self._groups)
        x_idearoot.set_beliefheirs(beliefs=self._idearoot._beliefunits)
        x_idearoot.inherit_balanceheirs()
        x_idearoot.clear_balancelines()
        x_idearoot._weight = 1
        x_idearoot.set_kids_total_weight()
        x_idearoot.set_sibling_total_weight(1)
        x_idearoot.set_active(
            tree_traverse_count=self._tree_traverse_count,
            agenda_groupunits=self._groups,
            agenda_owner_id=self._owner_id,
        )
        x_idearoot.set_agenda_importance(coin_onset_x=0, parent_coin_cease=1)
        x_idearoot.set_balanceheirs_agenda_credit_debt()
        x_idearoot.set_ancestor_promise_count(0, False)
        x_idearoot.clear_descendant_promise_count()
        x_idearoot.clear_all_party_credit_debt()
        x_idearoot.promise = False

        if x_idearoot.is_kidless():
            self._set_ancestors_metrics(self._idearoot.get_road(), econ_exceptions)
            self._distribute_agenda_importance(idea=self._idearoot)

    def _set_kids_attributes(
        self,
        idea_kid: IdeaUnit,
        coin_onset: float,
        parent_coin_cease: float,
        parent_idea: IdeaUnit,
        econ_exceptions: bool,
    ):
        idea_kid.set_level(parent_level=parent_idea._level)
        idea_kid.set_parent_road(parent_idea.get_road())
        idea_kid.set_beliefheirs(beliefs=parent_idea._beliefheirs)
        idea_kid.set_reasonheirs(self._idea_dict, parent_idea._reasonheirs)
        idea_kid.set_assignedheir(parent_idea._assignedheir, self._groups)
        idea_kid.inherit_balanceheirs(parent_idea._balanceheirs)
        idea_kid.clear_balancelines()
        idea_kid.set_active(
            tree_traverse_count=self._tree_traverse_count,
            agenda_groupunits=self._groups,
            agenda_owner_id=self._owner_id,
        )
        idea_kid.set_sibling_total_weight(parent_idea._kids_total_weight)
        idea_kid.set_agenda_importance(
            coin_onset_x=coin_onset,
            parent_agenda_importance=parent_idea._agenda_importance,
            parent_coin_cease=parent_coin_cease,
        )
        idea_kid.set_ancestor_promise_count(
            parent_idea._ancestor_promise_count, parent_idea.promise
        )
        idea_kid.clear_descendant_promise_count()
        idea_kid.clear_all_party_credit_debt()

        if idea_kid.is_kidless():
            # set idea's ancestor metrics using agenda root as common reference
            self._set_ancestors_metrics(idea_kid.get_road(), econ_exceptions)
            self._distribute_agenda_importance(idea=idea_kid)

    def _distribute_agenda_importance(self, idea: IdeaUnit):
        # TODO manage situations where balanceheir.creditor_weight is None for all balanceheirs
        # TODO manage situations where balanceheir.debtor_weight is None for all balanceheirs
        if idea.is_balanceheirless() == False:
            self._set_groupunits_agenda_importance(idea._balanceheirs)
        elif idea.is_balanceheirless():
            self._add_to_partyunits_agenda_credit_debt(idea._agenda_importance)

    def get_agenda_importance(
        self, parent_agenda_importance: float, weight: int, sibling_total_weight: int
    ) -> float:
        sibling_ratio = weight / sibling_total_weight
        return parent_agenda_importance * sibling_ratio

    def _set_tree_traverse_starting_point(self):
        self._rational = False
        self._tree_traverse_count = 0
        self._idea_dict = {self._idearoot.get_road(): self._idearoot}

    def _clear_agenda_base_metrics(self):
        self._econs_justified = True
        self._econs_buildable = False
        self._sum_healerhold_importance = 0
        self._econ_dict = {}
        self._healers_dict = {}

    def set_agenda_metrics(self, econ_exceptions: bool = False):
        self._set_tree_traverse_starting_point()

        while (
            not self._rational and self._tree_traverse_count < self._max_tree_traverse
        ):
            self._clear_agenda_base_metrics()
            self._execute_tree_traverse(econ_exceptions)
            self._check_if_any_idea_active_has_changed()
            self._tree_traverse_count += 1
        self._after_all_tree_traverses_set_credit_debt()
        self._after_all_tree_traverses_set_healerhold_importance()

    def _execute_tree_traverse(self, econ_exceptions: bool = False):
        self._pre_tree_traverse_credit_debt_reset()
        self._set_root_attributes(econ_exceptions)

        coin_onset = self._idearoot._agenda_coin_onset
        parent_coin_cease = self._idearoot._agenda_coin_cease

        cache_idea_list = []
        for idea_kid in self._idearoot._kids.values():
            self._set_kids_attributes(
                idea_kid=idea_kid,
                coin_onset=coin_onset,
                parent_coin_cease=parent_coin_cease,
                parent_idea=self._idearoot,
                econ_exceptions=econ_exceptions,
            )
            cache_idea_list.append(idea_kid)
            coin_onset += idea_kid._agenda_importance

        # no function recursion, recursion by iterateing over list that can be added to by iterations
        while cache_idea_list != []:
            parent_idea = cache_idea_list.pop()
            if self._tree_traverse_count == 0:
                self._idea_dict[parent_idea.get_road()] = parent_idea

            if parent_idea._kids != None:
                coin_onset = parent_idea._agenda_coin_onset
                parent_coin_cease = parent_idea._agenda_coin_cease
                for idea_kid in parent_idea._kids.values():
                    self._set_kids_attributes(
                        idea_kid=idea_kid,
                        coin_onset=coin_onset,
                        parent_coin_cease=parent_coin_cease,
                        parent_idea=parent_idea,
                        econ_exceptions=econ_exceptions,
                    )
                    cache_idea_list.append(idea_kid)
                    coin_onset += idea_kid._agenda_importance

    def _check_if_any_idea_active_has_changed(self):
        any_idea_active_changed = False
        for idea in self._idea_dict.values():
            if idea._active_hx.get(self._tree_traverse_count) != None:
                any_idea_active_changed = True

        if any_idea_active_changed == False:
            self._rational = True

    def _after_all_tree_traverses_set_credit_debt(self):
        self._distribute_agenda_intent_importance()
        self._distribute_groups_agenda_importance()
        self._set_agenda_intent_ratio_credit_debt()

    def _after_all_tree_traverses_set_healerhold_importance(self):
        self._set_econ_dict()
        self._healers_dict = self._get_healers_dict()
        self._econs_buildable = self._get_econs_buildable()

    def _set_econ_dict(self):
        if self._econs_justified == False:
            self._sum_healerhold_importance = 0
        for x_idea in self._idea_dict.values():
            if self._sum_healerhold_importance == 0:
                x_idea._healerhold_importance = 0
            else:
                x_idea._healerhold_importance = (
                    x_idea._agenda_importance / self._sum_healerhold_importance
                )
            if self._econs_justified and x_idea._healerhold.any_group_id_exists():
                self._econ_dict[x_idea.get_road()] = x_idea

    def _get_healers_dict(self) -> dict[HealerID : dict[RoadUnit:IdeaUnit]]:
        _healers_dict = {}
        for x_econ_road, x_econ_idea in self._econ_dict.items():
            for x_group_id in x_econ_idea._healerhold._group_ids:
                x_groupunit = self.get_groupunit(x_group_id)
                for x_party_id in x_groupunit._partys.keys():
                    if _healers_dict.get(x_party_id) is None:
                        _healers_dict[x_party_id] = {x_econ_road: x_econ_idea}
                    else:
                        healer_dict = _healers_dict.get(x_party_id)
                        healer_dict[x_econ_road] = x_econ_idea
        return _healers_dict

    def _get_econs_buildable(self) -> bool:
        return all(
            is_roadunit_convertible_to_path(econ_road, delimiter=self._road_delimiter)
            != False
            for econ_road in self._econ_dict.keys()
        )

    def _pre_tree_traverse_credit_debt_reset(self):
        if self.is_partyunits_creditor_weight_sum_correct() == False:
            raise PartyunitsCreditorDebtorSumException(
                f"'{self._owner_id}' is_partyunits_creditor_weight_sum_correct is False. _party_creditor_pool={self._party_creditor_pool}. partyunits_creditor_weight_sum={self.get_partyunits_creditor_weight_sum()}"
            )
        if self.is_partyunits_debtor_weight_sum_correct() == False:
            raise PartyunitsCreditorDebtorSumException(
                f"'{self._owner_id}' is_partyunits_debtor_weight_sum_correct is False. _party_debtor_pool={self._party_debtor_pool}. partyunits_debtor_weight_sum={self.get_partyunits_debtor_weight_sum()}"
            )
        self._reset_groupunits_agenda_credit_debt()
        self._reset_groupunits_agenda_credit_debt()
        self._reset_partyunit_agenda_credit_debt()

    def get_heir_road_list(self, x_road: RoadUnit) -> list[RoadUnit]:
        return [
            idea_road
            for idea_road in self.get_idea_tree_ordered_road_list()
            if is_sub_road(idea_road, x_road)
        ]

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

    def get_beliefunits_dict(self) -> dict[str:str]:
        x_dict = {}
        if self._idearoot._beliefunits != None:
            for belief_road, belief_obj in self._idearoot._beliefunits.items():
                x_dict[belief_road] = belief_obj.get_dict()
        return x_dict

    def get_partys_dict(self, all_attrs: bool = False) -> dict[str:str]:
        x_dict = {}
        if self._partys != None:
            for party_id, party_obj in self._partys.items():
                x_dict[party_id] = party_obj.get_dict(all_attrs)
        return x_dict

    def get_groupunits_dict(self) -> dict[str:str]:
        return {
            group_group_id: group_obj.get_dict()
            for group_group_id, group_obj in self._groups.items()
            if group_obj._party_mirror == False
        }

    def get_dict(self) -> dict[str:str]:
        x_dict = {
            "_partys": self.get_partys_dict(),
            "_groups": self.get_groupunits_dict(),
            "_originunit": self._originunit.get_dict(),
            "_weight": self._weight,
            "_owner_id": self._owner_id,
            "_world_id": self._world_id,
            "_max_tree_traverse": self._max_tree_traverse,
            "_auto_output_job_to_forum": self._auto_output_job_to_forum,
            "_road_delimiter": self._road_delimiter,
            "_idearoot": self._idearoot.get_dict(),
        }
        if self._party_creditor_pool != None:
            x_dict["_party_creditor_pool"] = self._party_creditor_pool
        if self._party_debtor_pool != None:
            x_dict["_party_debtor_pool"] = self._party_debtor_pool
        if self._meld_strategy != get_meld_default():
            x_dict["_meld_strategy"] = self._meld_strategy
        if self._last_gift_id != None:
            x_dict["_last_gift_id"] = self._last_gift_id

        return x_dict

    def get_json(self) -> str:
        x_dict = self.get_dict()
        return get_json_from_dict(dict_x=x_dict)

    def set_time_hreg_ideas(self, c400_count: int):
        x_hregidea = HregIdea(self._road_delimiter)
        ideabase_list = x_hregidea._get_time_hreg_src_idea(c400_count=c400_count)
        while len(ideabase_list) != 0:
            yb = ideabase_list.pop(0)
            range_source_road_x = None
            if yb.sr != None:
                range_source_road_x = self.make_l1_road(yb.sr)

            x_idea = ideaunit_shop(
                _label=yb.n,
                _begin=yb.b,
                _close=yb.c,
                _weight=yb.weight,
                _is_expanded=False,
                _addin=yb.a,
                _numor=yb.mn,
                _denom=yb.md,
                _reest=yb.mr,
                _range_source_road=range_source_road_x,
            )
            road_x = self.make_l1_road(yb.rr)
            self.add_idea(x_idea, parent_road=road_x)

            numeric_road_x = None
            if yb.nr != None:
                numeric_road_x = self.make_l1_road(yb.nr)
                self.edit_idea_attr(
                    road=self.make_road(road_x, yb.n), numeric_road=numeric_road_x
                )
            if yb.a != None:
                self.edit_idea_attr(
                    road=self.make_road(road_x, yb.n),
                    addin=yb.a,
                    denom=yb.md,
                    numor=yb.mn,
                )

        self.set_agenda_metrics()

    def get_agenda4party(self, party_id: PartyID, beliefs: dict[RoadUnit:BeliefCore]):
        self.set_agenda_metrics()
        agenda4party = agendaunit_shop(_owner_id=party_id)
        agenda4party._idearoot._agenda_importance = self._idearoot._agenda_importance
        # get party's partys: partyzone

        # get partyzone groups
        party_groups = self.get_party_group_ids(party_id=party_id)

        # set agenda4party by traversing the idea tree and selecting associated groups
        # set root
        not_included_agenda_importance = 0
        agenda4party._idearoot.clear_kids()
        for ykx in self._idearoot._kids.values():
            y4a_included = any(
                group_ancestor.group_id in party_groups
                for group_ancestor in ykx._balancelines.values()
            )

            if y4a_included:
                y4a_new = ideaunit_shop(
                    _label=ykx._label,
                    _agenda_importance=ykx._agenda_importance,
                    _reasonunits=ykx._reasonunits,
                    _balancelinks=ykx._balancelinks,
                    _begin=ykx._begin,
                    _close=ykx._close,
                    promise=ykx.promise,
                    _task=ykx._task,
                )
                agenda4party._idearoot._kids[ykx._label] = y4a_new
            else:
                not_included_agenda_importance += ykx._agenda_importance

        if not_included_agenda_importance > 0:
            y4a_other = ideaunit_shop(
                _label="__other__",
                _agenda_importance=not_included_agenda_importance,
            )
            agenda4party._idearoot._kids[y4a_other._label] = y4a_other

        return agenda4party

    def set_dominate_promise_idea(self, idea_kid: IdeaUnit):
        idea_kid.promise = True
        self.add_idea(
            idea_kid=idea_kid,
            parent_road=self.make_road(idea_kid._parent_road),
            create_missing_ideas_groups=True,
        )

    def get_idea_list_without_idearoot(self) -> list[IdeaUnit]:
        self.set_agenda_metrics()
        x_list = list(self._idea_dict.values())
        x_list.pop(0)
        return x_list

    def set_meld_strategy(self, x_meld_strategy: MeldStrategy):
        self._meld_strategy = validate_meld_strategy(x_meld_strategy)

    def meld(self, other_agenda, party_weight: float = None):
        self._meld_ideas(other_agenda, party_weight)
        self._meld_beliefs(other_agenda)
        self._weight = get_meld_weight(
            src_weight=self._weight,
            src_meld_strategy="default",
            other_weight=other_agenda._weight,
            other_meld_strategy="default",
        )
        self._meld_originlinks(other_agenda._owner_id, party_weight)

    def _meld_ideas(self, other_agenda, party_weight: float):
        # meld idearoot
        self._idearoot.meld(other_idea=other_agenda._idearoot, _idearoot=True)

        # meld all other ideas
        party_id = other_agenda._owner_id
        o_idea_list = other_agenda.get_idea_list_without_idearoot()
        for o_idea in o_idea_list:
            o_road = road_validate(
                self.make_road(o_idea._parent_road, o_idea._label),
                self._road_delimiter,
                self._world_id,
            )
            try:
                main_idea = self.get_idea_obj(o_road)
                main_idea.meld(o_idea, False, party_id, party_weight)
            except Exception:
                self.add_idea(idea_kid=o_idea, parent_road=o_idea._parent_road)
                main_idea = self.get_idea_obj(o_road)
                main_idea._originunit.set_originlink(party_id, party_weight)

    def _meld_partys(self, other_agenda):
        for partyunit in other_agenda._partys.values():
            if self.get_party(partyunit.party_id) is None:
                self.set_partyunit(partyunit=partyunit)
            else:
                self.get_party(partyunit.party_id).meld(partyunit)

    def _meld_beliefs(self, other_agenda):
        for hx in other_agenda._idearoot._beliefunits.values():
            if self._idearoot._beliefunits.get(hx.base) is None:
                self.set_belief(
                    base=hx.base, belief=hx.belief, open=hx.open, nigh=hx.nigh
                )
            else:
                self._idearoot._beliefunits.get(hx.base).meld(hx)

    def _meld_originlinks(self, party_id: PartyID, party_weight: float):
        if party_id != None:
            self._originunit.set_originlink(party_id, party_weight)

    def get_assignment(
        self,
        agenda_x,
        assignor_partys: dict[PartyID:PartyUnit],
        assignor_party_id: PartyID,
    ):
        self.set_agenda_metrics()
        self._set_assignment_partys(agenda_x, assignor_partys, assignor_party_id)
        self._set_assignment_groups(agenda_x)
        assignor_promises = self._get_assignor_promise_ideas(
            agenda_x, assignor_party_id
        )
        relevant_roads = self._get_relevant_roads(assignor_promises)
        self._set_assignment_ideas(agenda_x, relevant_roads)
        return agenda_x

    def _set_assignment_ideas(self, x_agenda, relevant_roads: dict[RoadUnit:str]):
        sorted_relevants = sorted(list(relevant_roads))
        # difficult to know how to manage root idea attributes...
        if sorted_relevants != []:
            root_road = sorted_relevants.pop(0)

        for relevant_road in sorted_relevants:
            relevant_idea = copy_deepcopy(self.get_idea_obj(relevant_road))
            relevant_idea.find_replace_road(
                old_road=get_root_node_from_road(relevant_road, self._road_delimiter),
                new_road=x_agenda._world_id,
            )
            relevant_idea.clear_kids()
            x_agenda.add_idea(relevant_idea, parent_road=relevant_idea._parent_road)

        for afu in self._idearoot._beliefunits.values():
            if relevant_roads.get(afu.base) != None:
                x_agenda.set_belief(
                    base=change_road(afu.base, self._world_id, x_agenda._world_id),
                    pick=change_road(afu.pick, self._world_id, x_agenda._world_id),
                    open=afu.open,
                    nigh=afu.nigh,
                )

    def _set_assignment_partys(
        self,
        agenda_x,
        assignor_partys: dict[PartyID:PartyUnit],
        assignor_party_id: PartyID,
    ):
        if self.get_party(assignor_party_id) != None:
            # get all partys that are both in self._partys and assignor_known_partys
            partys_set = get_intersection_of_partys(self._partys, assignor_partys)
            for party_id_x in partys_set:
                agenda_x.set_partyunit(partyunit=self.get_party(party_id_x))
        return agenda_x

    def _set_assignment_groups(self, agenda_x):
        revelant_groups = get_partys_relevant_groups(self._groups, agenda_x._partys)
        for group_group_id, group_partys in revelant_groups.items():
            if agenda_x._groups.get(group_group_id) is None:
                group_x = groupunit_shop(group_id=group_group_id)
                for party_id in group_partys:
                    group_x.set_partylink(partylink_shop(party_id=party_id))
                agenda_x.set_groupunit(group_x)

    def _get_assignor_promise_ideas(
        self, agenda_x, assignor_party_id: GroupID
    ) -> dict[RoadUnit:int]:
        assignor_groups = get_party_relevant_groups(agenda_x._groups, assignor_party_id)
        return {
            idea_road: -1
            for idea_road, x_idea in self._idea_dict.items()
            if (x_idea.assignor_in(assignor_groups) and x_idea.promise)
        }

    def _set_auto_output_job_to_forum(self, bool_x: bool):
        if bool_x is None and self._auto_output_job_to_forum is None:
            self._auto_output_job_to_forum = False
        elif bool_x is not None or not self._auto_output_job_to_forum:
            self._auto_output_job_to_forum = bool_x is not None and bool_x


def agendaunit_shop(
    _owner_id: OwnerID = None,
    _world_id: EconID = None,
    _weight: float = None,
    _auto_output_job_to_forum: bool = None,
    _road_delimiter: str = None,
    _planck: float = None,
    _meld_strategy: MeldStrategy = None,
) -> AgendaUnit:
    if _owner_id is None:
        _owner_id = ""
    if _world_id is None:
        _world_id = get_default_world_id_roadnode()
    if _meld_strategy is None:
        _meld_strategy = get_meld_default()

    x_agenda = AgendaUnit(
        _owner_id=_owner_id,
        _weight=get_1_if_None(_weight),
        _auto_output_job_to_forum=get_False_if_None(_auto_output_job_to_forum),
        _world_id=_world_id,
        _partys=get_empty_dict_if_none(None),
        _groups=get_empty_dict_if_none(None),
        _idea_dict=get_empty_dict_if_none(None),
        _econ_dict=get_empty_dict_if_none(None),
        _healers_dict=get_empty_dict_if_none(None),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _planck=default_planck_if_none(_planck),
        _meld_strategy=validate_meld_strategy(_meld_strategy),
        _econs_justified=get_False_if_None(),
        _econs_buildable=get_False_if_None(),
        _sum_healerhold_importance=get_0_if_None(),
    )
    x_agenda._idearoot = ideaunit_shop(
        _root=True, _uid=1, _level=0, _agenda_world_id=x_agenda._world_id
    )
    x_agenda._idearoot._road_delimiter = x_agenda._road_delimiter
    x_agenda.set_max_tree_traverse(3)
    x_agenda._rational = False
    x_agenda._originunit = originunit_shop()
    return x_agenda


def get_from_json(x_agenda_json: str) -> AgendaUnit:
    return get_from_dict(get_dict_from_json(x_agenda_json))


def get_from_dict(agenda_dict: dict) -> AgendaUnit:
    x_agenda = agendaunit_shop()
    x_agenda.set_owner_id(get_obj_from_agenda_dict(agenda_dict, "_owner_id"))
    x_agenda._weight = get_obj_from_agenda_dict(agenda_dict, "_weight")
    x_agenda._auto_output_job_to_forum = get_obj_from_agenda_dict(
        agenda_dict, "_auto_output_job_to_forum"
    )
    x_agenda.set_max_tree_traverse(
        get_obj_from_agenda_dict(agenda_dict, "_max_tree_traverse")
    )
    x_agenda.set_world_id(get_obj_from_agenda_dict(agenda_dict, "_world_id"))
    x_agenda._road_delimiter = default_road_delimiter_if_none(
        get_obj_from_agenda_dict(agenda_dict, "_road_delimiter")
    )
    x_agenda._party_creditor_pool = get_obj_from_agenda_dict(
        agenda_dict, "_party_creditor_pool"
    )
    x_agenda._party_debtor_pool = get_obj_from_agenda_dict(
        agenda_dict, "_party_debtor_pool"
    )
    if get_obj_from_agenda_dict(agenda_dict, "_meld_strategy") is None:
        x_agenda._meld_strategy = get_meld_default()
    else:
        x_agenda._meld_strategy = get_obj_from_agenda_dict(
            agenda_dict, "_meld_strategy"
        )
    x_agenda._last_gift_id = get_obj_from_agenda_dict(agenda_dict, "_last_gift_id")
    for x_partyunit in get_obj_from_agenda_dict(agenda_dict, "_partys").values():
        x_agenda.set_partyunit(x_partyunit)
    for x_groupunit in get_obj_from_agenda_dict(agenda_dict, "_groups").values():
        x_agenda.set_groupunit(x_groupunit)
    x_agenda._originunit = get_obj_from_agenda_dict(agenda_dict, "_originunit")

    set_idearoot_from_agenda_dict(x_agenda, agenda_dict)
    x_agenda.set_agenda_metrics()  # clean up tree traverse defined fields
    return x_agenda


def set_idearoot_from_agenda_dict(x_agenda: AgendaUnit, agenda_dict: dict):
    idearoot_dict = agenda_dict.get("_idearoot")
    x_agenda._idearoot = ideaunit_shop(
        _root=True,
        _label=x_agenda._world_id,
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
        _assignedunit=get_obj_from_idea_dict(idearoot_dict, "_assignedunit"),
        _healerhold=get_obj_from_idea_dict(idearoot_dict, "_healerhold"),
        _beliefunits=get_obj_from_idea_dict(idearoot_dict, "_beliefunits"),
        _balancelinks=get_obj_from_idea_dict(idearoot_dict, "_balancelinks"),
        _is_expanded=get_obj_from_idea_dict(idearoot_dict, "_is_expanded"),
        _road_delimiter=get_obj_from_idea_dict(idearoot_dict, "_road_delimiter"),
        _agenda_world_id=x_agenda._world_id,
    )
    set_idearoot_kids_from_dict(x_agenda, idearoot_dict)


def set_idearoot_kids_from_dict(x_agenda: AgendaUnit, idearoot_dict: dict):
    to_evaluate_idea_dicts = []
    parent_road_text = "parent_road"
    # for every kid dict, set parent_road in dict, add to to_evaluate_list
    for x_dict in get_obj_from_idea_dict(idearoot_dict, "_kids").values():
        x_dict[parent_road_text] = x_agenda._world_id
        to_evaluate_idea_dicts.append(x_dict)

    while to_evaluate_idea_dicts != []:
        idea_dict = to_evaluate_idea_dicts.pop(0)
        # for every kid dict, set parent_road in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_idea_dict(idea_dict, "_kids").values():
            parent_road = get_obj_from_idea_dict(idea_dict, parent_road_text)
            kid_label = get_obj_from_idea_dict(idea_dict, "_label")
            kid_dict[parent_road_text] = x_agenda.make_road(parent_road, kid_label)
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
            promise=get_obj_from_idea_dict(idea_dict, "promise"),
            _problem_bool=get_obj_from_idea_dict(idea_dict, "_problem_bool"),
            _reasonunits=get_obj_from_idea_dict(idea_dict, "_reasonunits"),
            _assignedunit=get_obj_from_idea_dict(idea_dict, "_assignedunit"),
            _healerhold=get_obj_from_idea_dict(idea_dict, "_healerhold"),
            _originunit=get_obj_from_idea_dict(idea_dict, "_originunit"),
            _balancelinks=get_obj_from_idea_dict(idea_dict, "_balancelinks"),
            _beliefunits=get_obj_from_idea_dict(idea_dict, "_beliefunits"),
            _is_expanded=get_obj_from_idea_dict(idea_dict, "_is_expanded"),
            _range_source_road=get_obj_from_idea_dict(idea_dict, "_range_source_road"),
            _numeric_road=get_obj_from_idea_dict(idea_dict, "_numeric_road"),
            _agenda_world_id=x_agenda._world_id,
        )
        x_agenda.add_idea(x_ideakid, parent_road=idea_dict[parent_road_text])


def get_obj_from_agenda_dict(x_dict: dict[str:], dict_key: str) -> any:
    if dict_key == "_originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else originunit_shop()
        )
    elif dict_key == "_partys":
        return (
            partyunits_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else partyunits_get_from_dict(x_dict[dict_key])
        )
    elif dict_key == "_groups":
        return (
            groupunits_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else groupunits_get_from_dict(x_dict[dict_key])
        )
    elif dict_key == "_max_tree_traverse":
        return x_dict[dict_key] if x_dict.get(dict_key) != None else 20
    elif dict_key == "_auto_output_job_to_forum":
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def get_dict_of_agenda_from_dict(x_dict: dict[str:dict]) -> dict[str:AgendaUnit]:
    agendaunits = {}
    for agendaunit_dict in x_dict.values():
        x_agenda = get_from_dict(agenda_dict=agendaunit_dict)
        agendaunits[x_agenda._owner_id] = x_agenda
    return agendaunits


@dataclass
class MeldeeOrderUnit:
    owner_id: OwnerID
    voice_rank: int
    voice_hx_lowest_rank: int
    file_name: str


def get_meldeeorderunit(
    primary_agenda: AgendaUnit, meldee_file_name: str
) -> MeldeeOrderUnit:
    file_src_owner_id = meldee_file_name.replace(".json", "")
    primary_meldee_partyunit = primary_agenda.get_party(file_src_owner_id)

    default_voice_rank = 0
    default_voice_hx_lowest_rank = 0
    if primary_meldee_partyunit is None:
        primary_voice_rank_for_meldee = default_voice_rank
        primary_voice_hx_lowest_rank_for_meldee = default_voice_hx_lowest_rank
    else:
        primary_voice_rank_for_meldee = primary_meldee_partyunit._treasury_voice_rank
        primary_voice_hx_lowest_rank_for_meldee = (
            primary_meldee_partyunit._treasury_voice_hx_lowest_rank
        )
        if primary_voice_rank_for_meldee is None:
            primary_voice_rank_for_meldee = default_voice_rank
            primary_voice_hx_lowest_rank_for_meldee = default_voice_hx_lowest_rank

    return MeldeeOrderUnit(
        owner_id=file_src_owner_id,
        voice_rank=primary_voice_rank_for_meldee,
        voice_hx_lowest_rank=primary_voice_hx_lowest_rank_for_meldee,
        file_name=meldee_file_name,
    )


def get_file_names_in_voice_rank_order(primary_agenda, meldees_dir) -> list[str]:
    agenda_voice_ranks = {}
    for meldee_file_name in dir_files(dir_path=meldees_dir):
        meldee_orderunit = get_meldeeorderunit(primary_agenda, meldee_file_name)
        agenda_voice_ranks[meldee_orderunit.owner_id] = meldee_orderunit
    agendas_voice_rank_ordered_list = list(agenda_voice_ranks.values())
    agendas_voice_rank_ordered_list.sort(
        key=lambda x: (x.voice_rank * -1, x.voice_hx_lowest_rank * -1, x.owner_id)
    )
    return [
        x_meldeeorderunit.file_name
        for x_meldeeorderunit in agendas_voice_rank_ordered_list
    ]


def get_meld_of_agenda_files(
    primary_agenda: AgendaUnit, meldees_dir: str
) -> AgendaUnit:
    for x_filename in get_file_names_in_voice_rank_order(primary_agenda, meldees_dir):
        primary_agenda.meld(get_from_json(open_file(meldees_dir, x_filename)))
    primary_agenda.set_agenda_metrics()
    return primary_agenda


def get_intersection_of_partys(
    partys_x: dict[PartyID:PartyUnit], partys_y: dict[PartyID:PartyUnit]
) -> dict[PartyID:-1]:
    x_set = set(partys_x)
    y_set = set(partys_y)
    intersection_x = x_set.intersection(y_set)
    return {party_id_x: -1 for party_id_x in intersection_x}


def get_partys_relevant_groups(
    groups_x: dict[GroupID:GroupUnit], partys_x: dict[PartyID:PartyUnit]
) -> dict[GroupID:{PartyID: -1}]:
    relevant_groups = {}
    for party_id_x in partys_x:
        for group_x in groups_x.values():
            if group_x._partys.get(party_id_x) != None:
                if relevant_groups.get(group_x.group_id) is None:
                    relevant_groups[group_x.group_id] = {}
                relevant_groups.get(group_x.group_id)[party_id_x] = -1

    return relevant_groups


def get_party_relevant_groups(
    groups_x: dict[GroupID:GroupUnit], party_id_x: PartyID
) -> dict[GroupID:-1]:
    return {
        group_x.group_id: -1
        for group_x in groups_x.values()
        if group_x._partys.get(party_id_x) != None
    }
