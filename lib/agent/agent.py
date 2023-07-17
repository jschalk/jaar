import dataclasses
import json
from datetime import datetime
from lib.agent.ally import (
    AllyName,
    AllyUnit,
    AllyLink,
    allyunits_get_from_dict,
    allyunit_shop,
    allylink_shop,
    AllyUnitExternalMetrics,
)
from lib.agent.brand import (
    BrandLink,
    BrandName,
    BrandUnit,
    brandlinks_get_from_dict,
    get_from_dict as brandunits_get_from_dict,
    brandunit_shop,
    brandlink_shop,
)
from lib.agent.required import (
    AcptFactCore,
    AcptFactUnit,
    AcptFactUnit,
    RequiredHeir,
    RequiredUnit,
    Road,
    acptfactunits_get_from_dict,
    acptfactunit_shop,
    acptfactunits_get_from_dict,
    requireds_get_from_dict,
    sufffactunit_shop,
)
from lib.agent.tree_metrics import TreeMetrics
from lib.agent.x_func import x_get_json
from lib.agent.idea import IdeaCore, IdeaKid, IdeaRoot, IdeaAttrHolder
from lib.agent.hreg_time import (
    _get_time_hreg_src_idea,
    get_time_min_from_dt as hreg_get_time_min_from_dt,
    convert1440toReadableTime,
    get_number_with_postfix,
    get_jajatime_readable_from_dt,
)
from lib.agent.lemma import Lemmas
from lib.agent.road import (
    get_walk_from_road,
    is_sub_road_in_src_road,
    road_validate,
    change_road,
    get_terminus_node_from_road,
    find_replace_road_key_dict,
    get_ancestor_roads,
)
from copy import deepcopy as copy_deepcopy
from lib.agent.x_func import (
    save_file as x_func_save_file,
    dir_files as x_func_dir_files,
    open_file as x_func_open_file,
    get_meld_weight,
)


class InvalidAgentException(Exception):
    pass


@dataclasses.dataclass
class AgentUnit:
    _desc: str = None
    _weight: float = None
    _allys: dict[AllyName:AllyUnit] = None
    _brands: dict[BrandName:BrandUnit] = None
    _idearoot: IdeaRoot = None
    _idea_dict: dict[Road:IdeaCore] = None
    _max_tree_traverse: int = 3
    _tree_traverse_count: int = None
    _rational: bool = False

    def __init__(self, _weight: float = None, _desc=None) -> None:
        if _weight is None:
            _weight = 1
        self._weight = _weight
        if _desc is None:
            _desc = ""
        self._idearoot = IdeaRoot(_desc=_desc, _uid=1)
        self._desc = _desc

    def set_banking_attr_allyunits(self, river_tallys: dict):
        for allyunit_x in self._allys.values():
            allyunit_x.clear_banking_data()
            river_tally = river_tallys.get(allyunit_x.name)
            if river_tally != None:
                allyunit_x.set_banking_data(river_tally.tax_total, river_tally.tax_diff)

    def import_external_allyunit_metrics(
        self, external_metrics: AllyUnitExternalMetrics
    ):
        ally_x = self._allys.get(external_metrics.internal_name)
        ally_x._creditor_active = external_metrics.creditor_active
        ally_x._debtor_active = external_metrics.debtor_active
        # self.set_allyunit(allyunit=ally_x)

    def set_max_tree_traverse(self, int_x: int):
        if int_x < 2:
            raise InvalidAgentException(
                f"set_max_tree_traverse: input '{int_x}' must be number that is 2 or greater"
            )
        else:
            self._max_tree_traverse = int_x

    def get_bond_status(self) -> bool:
        self.set_agent_metrics()
        tree_metrics_x = self.get_tree_metrics()
        if tree_metrics_x.bond_promise_count != 1:
            return False

        promise_idea_road = tree_metrics_x.an_promise_idea_road
        if self._are_all_allys_brands_are_in_idea_kid(road=promise_idea_road) == False:
            return False

        return self.all_ideas_relevant_to_promise_idea(road=promise_idea_road) != False

    def export_all_bonds(self, dir: str):
        self.set_all_idea_uids_unique()
        self.set_agent_metrics()
        # dict_x = {}
        for yx in self.get_idea_list():
            if yx.promise:
                cx = self.get_agent_sprung_from_single_idea(yx.get_road())
                file_name = f"{yx._uid}.json"
                x_func_save_file(
                    dest_dir=dir,
                    file_name=file_name,
                    file_text=cx.get_json(),
                    replace=True,
                )
        return {}

    def get_agent_sprung_from_single_idea(self, road: Road):
        self.set_agent_metrics()
        idea_x = self.get_idea_kid(road=road)
        new_weight = self._weight * idea_x._agent_importance
        cx = AgentUnit(_desc=self._idearoot._desc, _weight=new_weight)

        for road_assc in sorted(list(self._get_all_idea_assoc_roads(road))):
            src_yx = self.get_idea_kid(road=road_assc)
            new_yx = copy_deepcopy(src_yx)
            if new_yx._walk != "":
                cx.add_idea(idea_kid=new_yx, walk=new_yx._walk)
            cx.set_agent_metrics()

        # TODO grab brands
        # TODO grab all brand allys
        # TODO grab acptfacts
        return cx

    def _get_all_idea_assoc_roads(self, road: Road) -> set[Road]:
        idea_ancestor_list = get_ancestor_roads(road=road)
        idea_x = self.get_idea_kid(road=road)
        requiredunit_base_road_list = []

        for requiredunit_obj in idea_x._requiredunits.values():
            required_base = requiredunit_obj.base
            requiredunit_base_road_list.extend(get_ancestor_roads(required_base))
            requiredunit_base_road_list.extend(self.get_heir_road_list(required_base))

        idea_assoc_list = [road]
        idea_assoc_list.extend(idea_ancestor_list)
        idea_assoc_list.extend(requiredunit_base_road_list)
        return set(idea_assoc_list)

    def all_ideas_relevant_to_promise_idea(self, road: Road) -> bool:
        promise_idea_assoc_set = set(self._get_all_idea_assoc_roads(road=road))
        all_ideas_set = set(self.get_idea_tree_ordered_road_list())
        return all_ideas_set == all_ideas_set.intersection(promise_idea_assoc_set)

    def _are_all_allys_brands_are_in_idea_kid(self, road: Road) -> bool:
        idea_kid = self.get_idea_kid(road=road)
        # get dict of all idea brandheirs
        brandheir_list = idea_kid._brandheirs.keys()
        brandheir_dict = {brandheir_name: 1 for brandheir_name in brandheir_list}
        non_single_brandunits = {
            brandunit.name: brandunit
            for brandunit in self._brands.values()
            if brandunit._single_ally != True
        }
        # check all non_single_ally_brandunits are in brandheirs
        for non_single_brand in non_single_brandunits.values():
            if brandheir_dict.get(non_single_brand.name) is None:
                return False

        # get dict of all allylinks that are in all brandheirs
        brandheir_allyunits = {}
        for brandheir_name in brandheir_dict:
            brandunit = self._brands.get(brandheir_name)
            for allylink in brandunit._allys.values():
                brandheir_allyunits[allylink.name] = self._allys.get(allylink.name)

        # check all agent._allys are in brandheir_allyunits
        return len(self._allys) == len(brandheir_allyunits)

    def get_time_min_from_dt(self, dt: datetime) -> float:
        return hreg_get_time_min_from_dt(dt=dt)

    def get_time_c400_from_min(self, min: int) -> int:
        c400_idea = self.get_idea_kid(f"{self._desc},time,tech,400 year cycle")
        c400_min = c400_idea._close
        return int(min / c400_min), c400_idea, min % c400_min

    def get_time_c400yr_from_min(self, min: int):
        # given int minutes within 400 year range return year and remainder minutes
        c400_count, c400_idea, c400yr_min = self.get_time_c400_from_min(min=min)
        c100_4_96y = c400_idea.get_kids_in_range(begin=c400yr_min, close=c400yr_min)[0]
        cXXXyr_min = c400yr_min - c100_4_96y._begin

        # identify which range the time is in
        if c100_4_96y._close - c100_4_96y._begin in (
            50492160,
            52596000,
        ):  # 96 year and 100 year spans
            yr4_1461 = self.get_idea_kid(f"{self._desc},time,tech,4year with leap")
            yr4_cycles = int(cXXXyr_min / yr4_1461._close)
            cXyr_min = cXXXyr_min % yr4_1461._close
            yr1_idea = yr4_1461.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[0]
        elif c100_4_96y._close - c100_4_96y._begin == 2102400:
            yr4_1460 = self.get_idea_kid(f"{self._desc},time,tech,4year wo leap")
            yr4_cycles = 0
            yr1_idea = yr4_1460.get_kids_in_range(begin=cXXXyr_min, close=cXXXyr_min)[0]
            cXyr_min = cXXXyr_min % yr4_1460._close

        yr1_rem_min = cXyr_min - yr1_idea._begin
        yr1_idea_begin = int(yr1_idea._desc.split("-")[0]) - 1

        c100_4_96y_begin = int(c100_4_96y._desc.split("-")[0])
        year_num = c100_4_96y_begin + (4 * yr4_cycles) + yr1_idea_begin
        return year_num, yr1_idea, yr1_rem_min

    def get_time_month_from_min(self, min: int):
        year_num, yr1_idea, yr1_idea_rem_min = self.get_time_c400yr_from_min(min=min)
        yrx = None
        if yr1_idea._close - yr1_idea._begin == 525600:
            yrx = self.get_idea_kid(f"{self._desc},time,tech,365 year")
        elif yr1_idea._close - yr1_idea._begin == 527040:
            yrx = self.get_idea_kid(f"{self._desc},time,tech,366 year")
        mon_x = yrx.get_kids_in_range(begin=yr1_idea_rem_min, close=yr1_idea_rem_min)[0]
        month_rem_min = yr1_idea_rem_min - mon_x._begin
        month_num = int(mon_x._desc.split("-")[0])
        day_x = self.get_idea_kid(f"{self._desc},time,tech,day")
        day_num = int(month_rem_min / day_x._close)
        day_rem_min = month_rem_min % day_x._close
        return month_num, day_num, day_rem_min, day_x

    def get_time_hour_from_min(self, min: int):
        month_num, day_num, day_rem_min, day_x = self.get_time_month_from_min(min=min)
        hr_x = day_x.get_kids_in_range(begin=day_rem_min, close=day_rem_min)[0]
        hr_rem_min = day_rem_min - hr_x._begin
        hr_num = int(hr_x._desc.split("-")[0])
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

    def get_jajatime_readable_one_time_event(self, jajatime_min: int) -> str:
        dt_x = self.get_time_dt_from_min(min=jajatime_min)
        return get_jajatime_readable_from_dt(dt=dt_x)

    def get_jajatime_repeating_readable_text(
        self, open: float = None, nigh: float = None, divisor: float = None
    ) -> str:
        str_x = "test3"
        if divisor is None:
            str_x = self.get_jajatime_readable_one_time_event(jajatime_min=open)
            # str_x = f"Weekday, monthname monthday year"
        elif divisor != None and divisor % 10080 == 0:
            str_x = self._get_jajatime_week_readable_text(open, divisor)
        elif divisor != None and divisor % 1440 == 0:
            if divisor == 1440:
                str_x = f"every day at {convert1440toReadableTime(min1440=open)}"
            else:
                num_days = int(divisor / 1440)
                num_with_postfix = get_number_with_postfix(num=num_days)
                str_x = f"every {num_with_postfix} day at {convert1440toReadableTime(min1440=open)}"
        else:
            str_x = "unkonwn"

        return str_x

    def _get_jajatime_week_readable_text(self, open: int, divisor: int) -> str:
        open_in_week = open % divisor
        week_road = f"{self._desc},time,tech,week"
        weekday_ideas_dict = self.get_idea_ranged_kids(
            idea_road=week_road, begin=open_in_week
        )
        weekday_idea_node = None
        for idea in weekday_ideas_dict.values():
            weekday_idea_node = idea

        if divisor == 10080:
            return f"every {weekday_idea_node._desc} at {convert1440toReadableTime(min1440=open % 1440)}"
        num_with_postfix = get_number_with_postfix(num=divisor // 10080)
        return f"every {num_with_postfix} {weekday_idea_node._desc} at {convert1440toReadableTime(min1440=open % 1440)}"

    def get_allys_metrics(self):
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.brandlinks_metrics

    def set_allys_empty_if_null(self):
        if self._allys is None:
            self._allys = {}

    def add_to_brand_agent_credit_debt(
        self,
        brandname: BrandName,
        brandheir_agent_credit: float,
        brandheir_agent_debt: float,
    ):
        for brand in self._brands.values():
            if brand.name == brandname:
                brand.set_empty_agent_credit_debt_to_zero()
                brand._agent_credit += brandheir_agent_credit
                brand._agent_debt += brandheir_agent_debt

    def add_to_brand_agent_agenda_credit_debt(
        self,
        brandname: BrandName,
        brandline_agent_credit: float,
        brandline_agent_debt: float,
    ):
        for brand in self._brands.values():
            if (
                brand.name == brandname
                and brandline_agent_credit != None
                and brandline_agent_debt != None
            ):
                brand.set_empty_agent_credit_debt_to_zero()
                brand._agent_agenda_credit += brandline_agent_credit
                brand._agent_agenda_debt += brandline_agent_debt

    def add_to_allyunit_agent_credit_debt(
        self,
        allyunit_name: AllyName,
        agent_credit,
        agent_debt: float,
        agent_agenda_credit: float,
        agent_agenda_debt: float,
    ):
        for allyunit in self._allys.values():
            if allyunit.name == allyunit_name:
                allyunit.add_agent_credit_debt(
                    agent_credit=agent_credit,
                    agent_debt=agent_debt,
                    agent_agenda_credit=agent_agenda_credit,
                    agent_agenda_debt=agent_agenda_debt,
                )

    def set_brandunits_empty_if_null(self):
        if self._brands is None:
            self._brands = {}

    def del_allyunit(self, name: str):
        self._brands.pop(name)
        self._allys.pop(name)

    def add_allyunit(
        self,
        name: str,
        uid: int = None,
        creditor_weight: int = None,
        debtor_weight: int = None,
    ):
        allyunit = allyunit_shop(
            name=AllyName(name),
            uid=uid,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        self.set_allyunit(allyunit=allyunit)

    def set_allyunit(self, allyunit: AllyUnit):
        self.set_allys_empty_if_null()
        self.set_brandunits_empty_if_null()
        # future: if ally is new check brand does not already have that name

        self._allys[allyunit.name] = allyunit

        existing_brand = None
        try:
            existing_brand = self._brands[allyunit.name]
        except KeyError:
            allylink = allylink_shop(
                name=AllyName(allyunit.name), creditor_weight=1, debtor_weight=1
            )
            allylinks = {allylink.name: allylink}
            brand_unit = brandunit_shop(
                name=allyunit.name,
                _single_ally=True,
                _allys=allylinks,
                uid=None,
                single_member_ally_id=None,
            )
            self.set_brandunit(brandunit=brand_unit)

    def edit_allyunit_name(
        self,
        old_name: str,
        new_name: str,
        allow_ally_overwite: bool,
        allow_nonsingle_brand_overwrite: bool,
    ):
        old_name_creditor_weight = self._allys.get(old_name).creditor_weight
        if not allow_ally_overwite and self._allys.get(new_name) != None:
            raise InvalidAgentException(
                f"Ally '{old_name}' change to '{new_name}' failed since it already exists."
            )
        elif (
            not allow_nonsingle_brand_overwrite
            and self._brands.get(new_name) != None
            and self._brands.get(new_name)._single_ally == False
        ):
            raise InvalidAgentException(
                f"Ally '{old_name}' change to '{new_name}' failed since non-single brand '{new_name}' already exists."
            )
        elif (
            allow_nonsingle_brand_overwrite
            and self._brands.get(new_name) != None
            and self._brands.get(new_name)._single_ally == False
        ):
            self.del_brandunit(brandname=new_name)
        elif self._allys.get(new_name) != None:
            old_name_creditor_weight += self._allys.get(new_name).creditor_weight

        self.add_allyunit(name=new_name, creditor_weight=old_name_creditor_weight)
        brands_affected_list = []
        for brand in self._brands.values():
            brands_affected_list.extend(
                brand.name
                for ally_x in brand._allys.values()
                if ally_x.name == old_name
            )
        for brand_x in brands_affected_list:
            allylink_creditor_weight = (
                self._brands.get(brand_x)._allys.get(old_name).creditor_weight
            )
            allylink_debtor_weight = (
                self._brands.get(brand_x)._allys.get(old_name).debtor_weight
            )
            if self._brands.get(brand_x)._allys.get(new_name) != None:
                allylink_creditor_weight += (
                    self._brands.get(brand_x)._allys.get(new_name).creditor_weight
                )
                allylink_debtor_weight += (
                    self._brands.get(brand_x)._allys.get(new_name).debtor_weight
                )

            self._brands.get(brand_x).set_allylink(
                allylink=allylink_shop(
                    name=new_name,
                    creditor_weight=allylink_creditor_weight,
                    debtor_weight=allylink_debtor_weight,
                )
            )
            self._brands.get(brand_x).del_allylink(name=old_name)

        self.del_allyunit(name=old_name)

    def get_allyunits_name_list(self):
        allyname_list = list(self._allys.keys())
        allyname_list.append("")
        allyname_dict = {allyname.lower(): allyname for allyname in allyname_list}
        allyname_lowercase_ordered_list = sorted(list(allyname_dict))
        return [
            allyname_dict[allyname_l] for allyname_l in allyname_lowercase_ordered_list
        ]

    def get_allyunits_uid_max(self) -> int:
        uid_max = 1
        for allyunit_x in self._allys.values():
            if allyunit_x.uid != None and allyunit_x.uid > uid_max:
                uid_max = allyunit_x.uid
        return uid_max

    def get_allyunits_uid_dict(self) -> dict[int:int]:
        uid_dict = {}
        for allyunit_x in self._allys.values():
            if uid_dict.get(allyunit_x.uid) is None:
                uid_dict[allyunit_x.uid] = 1
            else:
                uid_dict[allyunit_x.uid] += 1
        return uid_dict

    def set_all_allyunits_uids_unique(self) -> int:
        uid_max = self.get_allyunits_uid_max()
        uid_dict = self.get_allyunits_uid_dict()
        for allyunit_x in self._allys.values():
            if uid_dict.get(allyunit_x.uid) > 0:
                new_uid_max = uid_max + 1
                allyunit_x.uid = new_uid_max
                uid_max = allyunit_x.uid

    def all_allyunits_uids_are_unique(self):
        uid_dict = self.get_allyunits_uid_dict()
        return not any(
            uid_count > 1 or uid is None for uid, uid_count in uid_dict.items()
        )

    def get_brandunits_uid_max(self) -> int:
        uid_max = 1
        for brandunit_x in self._brands.values():
            if brandunit_x.uid != None and brandunit_x.uid > uid_max:
                uid_max = brandunit_x.uid
        return uid_max

    def get_brandunits_uid_dict(self) -> dict[int:int]:
        uid_dict = {}
        for brandunit_x in self._brands.values():
            if uid_dict.get(brandunit_x.uid) is None:
                uid_dict[brandunit_x.uid] = 1
            else:
                uid_dict[brandunit_x.uid] += 1
        return uid_dict

    def set_all_brandunits_uids_unique(self) -> int:
        uid_max = self.get_brandunits_uid_max()
        uid_dict = self.get_brandunits_uid_dict()
        for brandunit_x in self._brands.values():
            if uid_dict.get(brandunit_x.uid) > 0:
                new_uid_max = uid_max + 1
                brandunit_x.uid = new_uid_max
                uid_max = brandunit_x.uid

    def all_brandunits_uids_are_unique(self):
        uid_dict = self.get_brandunits_uid_dict()
        return not any(
            uid_count > 1 or uid is None for uid, uid_count in uid_dict.items()
        )

    def set_brandunit(self, brandunit: BrandUnit, create_missing_allys: bool = None):
        self.set_brandunits_empty_if_null()
        brandunit._set_allylinks_empty_if_null()
        self._brands[brandunit.name] = brandunit

        if create_missing_allys:
            self._create_missing_allys(allylinks=brandunit._allys)

    def _create_missing_allys(self, allylinks: dict[AllyName:AllyLink]):
        for allylink_x in allylinks.values():
            if self._allys.get(allylink_x.name) is None:
                self.set_allyunit(
                    allyunit=allyunit_shop(
                        name=allylink_x.name,
                        creditor_weight=allylink_x.creditor_weight,
                        debtor_weight=allylink_x.debtor_weight,
                    )
                )

    def del_brandunit(self, brandname: BrandName):
        self._brands.pop(brandname)

    def edit_brandunit_name(
        self, old_name: BrandName, new_name: BrandName, allow_brand_overwite: bool
    ):
        if not allow_brand_overwite and self._brands.get(new_name) != None:
            raise InvalidAgentException(
                f"Brand '{old_name}' change to '{new_name}' failed since it already exists."
            )
        elif self._brands.get(new_name) != None:
            old_brandunit = self._brands.get(old_name)
            old_brandunit.edit_attr(name=new_name)
            self._brands.get(new_name).meld(other_brand=old_brandunit)
            self.del_brandunit(brandname=old_name)
        elif self._brands.get(new_name) is None:
            old_brandunit = self._brands.get(old_name)
            brandunit_x = brandunit_shop(
                name=new_name,
                uid=old_brandunit.uid,
                _allys=old_brandunit._allys,
                single_member_ally_id=old_brandunit.single_member_ally_id,
                _single_ally=old_brandunit._single_ally,
            )
            self.set_brandunit(brandunit=brandunit_x)
            self.del_brandunit(brandname=old_name)

        self._edit_brandlinks_name(
            old_name=old_name,
            new_name=new_name,
            allow_brand_overwite=allow_brand_overwite,
        )

    def _edit_brandlinks_name(
        self,
        old_name: BrandName,
        new_name: BrandName,
        allow_brand_overwite: bool,
    ):
        for idea_x in self.get_idea_list():
            if (
                idea_x._brandlinks.get(new_name) != None
                and idea_x._brandlinks.get(old_name) != None
            ):
                old_brandlink = idea_x._brandlinks.get(old_name)
                old_brandlink.name = new_name
                idea_x._brandlinks.get(new_name).meld(
                    other_brandlink=old_brandlink,
                    other_on_meld_weight_action="sum",
                    src_on_meld_weight_action="sum",
                )

                idea_x.del_brandlink(brandname=old_name)
            elif (
                idea_x._brandlinks.get(new_name) is None
                and idea_x._brandlinks.get(old_name) != None
            ):
                old_brandlink = idea_x._brandlinks.get(old_name)
                new_brandlink = brandlink_shop(
                    name=new_name,
                    creditor_weight=old_brandlink.creditor_weight,
                    debtor_weight=old_brandlink.debtor_weight,
                )
                idea_x.set_brandlink(brandlink=new_brandlink)
                idea_x.del_brandlink(brandname=old_name)

    def get_brandunits_name_list(self):
        brandname_list = list(self._brands.keys())
        brandname_list.append("")
        brandname_dict = {brandname.lower(): brandname for brandname in brandname_list}
        brandname_lowercase_ordered_list = sorted(list(brandname_dict))
        return [brandname_dict[brand_l] for brand_l in brandname_lowercase_ordered_list]

    def set_time_acptfacts(self, open: datetime = None, nigh: datetime = None) -> None:
        open_minutes = self.get_time_min_from_dt(dt=open) if open != None else None
        nigh_minutes = self.get_time_min_from_dt(dt=nigh) if nigh != None else None
        minutes_acptfact = f"{self._desc},time,jajatime"
        self.set_acptfact(
            base=minutes_acptfact,
            pick=minutes_acptfact,
            open=open_minutes,
            nigh=nigh_minutes,
        )

    def _is_idea_rangeroot(self, idea_road: Road):
        anc_roads = get_ancestor_roads(road=idea_road)
        parent_road = self._desc if len(anc_roads) == 1 else anc_roads[1]

        # figure out if parent is range
        parent_range = None
        if len(parent_road.split(",")) == 1:
            parent_range = False
        else:
            parent_idea = self.get_idea_kid(road=parent_road)
            parent_range = parent_idea._begin != None and parent_idea._close != None

        # figure out if numeric source exists
        idea_x = self.get_idea_kid(road=idea_road)
        numeric_src_road = None
        numeric_src_road = idea_x._numeric_road != None

        return not numeric_src_road and not parent_range

    def _get_rangeroot_acptfactunits(self):
        return [
            acptfact
            for acptfact in self._idearoot._acptfactunits.values()
            if acptfact.open != None
            and acptfact.nigh != None
            and self._is_idea_rangeroot(idea_road=acptfact.base)
        ]

    def _get_rangeroot_1stlevel_associates(self, ranged_acptfactunits: list[IdeaCore]):
        lemmas_x = Lemmas()
        lemmas_x.set_empty_if_null()
        # lemma_ideas = {}
        for acptfact in ranged_acptfactunits:
            acptfact_idea = self.get_idea_kid(road=acptfact.base)
            for kid in acptfact_idea._kids.values():
                lemmas_x.eval(idea_x=kid, src_acptfact=acptfact, src_idea=acptfact_idea)

            if acptfact_idea._special_road != None:
                lemmas_x.eval(
                    idea_x=self.get_idea_kid(road=acptfact_idea._special_road),
                    src_acptfact=acptfact,
                    src_idea=acptfact_idea,
                )
        return lemmas_x

    def _get_lemma_acptfactunits(self) -> dict:
        # get all range-root first level kids and special_road
        lemmas_x = self._get_rangeroot_1stlevel_associates(
            self._get_rangeroot_acptfactunits()
        )

        # Now collect associates (all their descendents and special_roads)
        lemma_acptfactunits = {}  # acptfact.base : acptfactUnit
        count_x = 0
        while lemmas_x.is_lemmas_evaluated() == False or count_x > 10000:
            count_x += 1
            if count_x == 9998:
                raise InvalidAgentException("lemma loop failed")

            lemma_y = lemmas_x.get_unevaluated_lemma()
            idea_x = lemma_y.idea_x
            acptfact_x = lemma_y.calc_acptfact

            road_x = f"{idea_x._walk},{idea_x._desc}"
            lemma_acptfactunits[road_x] = acptfact_x

            for kid2 in idea_x._kids.values():
                lemmas_x.eval(idea_x=kid2, src_acptfact=acptfact_x, src_idea=idea_x)
            if idea_x._special_road not in [None, ""]:
                lemmas_x.eval(
                    idea_x=self.get_idea_kid(road=idea_x._special_road),
                    src_acptfact=acptfact_x,
                    src_idea=idea_x,
                )

        return lemma_acptfactunits

    def set_acptfact(
        self,
        base: Road,
        pick: Road,
        open: float = None,
        nigh: float = None,
        create_missing_ideas: bool = None,
    ):
        if create_missing_ideas:
            self._set_ideakid_if_empty(road=base)
            self._set_ideakid_if_empty(road=pick)

        self._set_acptfacts_empty_if_null()
        self._execute_tree_traverse()
        acptfact_idea = self.get_idea_kid(road=base)

        if acptfact_idea._begin is None and acptfact_idea._close is None:
            self._edit_set_idearoot_acptfactunits(
                base=base, pick=pick, open=open, nigh=nigh
            )

        # if acptfact's idea no range or is a "range-root" then allow acptfact to be set by user
        elif (
            acptfact_idea._begin != None
            and acptfact_idea._close != None
            and self._is_idea_rangeroot(idea_road=base) == False
        ):
            raise InvalidAgentException(
                f"Non range-root acptfact:{base} can only be set by range-root acptfact"
            )

        elif (
            acptfact_idea._begin != None
            and acptfact_idea._close != None
            and self._is_idea_rangeroot(idea_road=base) == True
        ):
            # when idea is "range-root" identify any required.bases that are descendents
            # calculate and set those descendent acptfacts
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendent
            # there exists a required base "timeline,weeks" with sufffact.need = "timeline,weeks"
            # and (1,2) divisor=2 (every other week)
            #
            # user should not set "timeline,weeks" acptfact, only "timeline" acptfact and
            # "timeline,weeks" should be set automatically since there exists a required
            # that has that base.
            self._edit_set_idearoot_acptfactunits(
                base=base, pick=pick, open=open, nigh=nigh
            )

            # Find all AcptFact descendents and any special_road connections "Lemmas"
            lemmas_dict = self._get_lemma_acptfactunits()
            for current_acptfact in self._idearoot._acptfactunits.values():
                for lemma_acptfact in lemmas_dict.values():
                    if lemma_acptfact.base == current_acptfact.base:
                        self._edit_set_idearoot_acptfactunits(
                            base=lemma_acptfact.base,
                            pick=lemma_acptfact.pick,
                            open=lemma_acptfact.open,
                            nigh=lemma_acptfact.nigh,
                        )
                        self._idearoot._acptfactunits[
                            lemma_acptfact.base
                        ] = lemma_acptfact

            for missing_acptfact in self.get_missing_acptfact_bases().keys():
                for lemma_acptfact in lemmas_dict.values():
                    if lemma_acptfact.base == missing_acptfact:
                        self._idearoot._acptfactunits[
                            lemma_acptfact.base
                        ] = lemma_acptfact

        self.set_agent_metrics()

    def _edit_set_idearoot_acptfactunits(
        self, pick: Road, base: Road, open: float, nigh: float
    ):
        acptfactunit = acptfactunit_shop(base=base, pick=pick, open=open, nigh=nigh)
        try:
            acptfact_obj = self._idearoot._acptfactunits[base]
            if pick != None:
                acptfact_obj.set_attr(pick=pick)
            if open != None:
                acptfact_obj.set_attr(open=open)
            if nigh != None:
                acptfact_obj.set_attr(nigh=nigh)
        except KeyError as e:
            self._idearoot._acptfactunits[acptfactunit.base] = acptfactunit

    def get_acptfactunits_base_and_acptfact_list(self):
        acptfact_list = list(self._idearoot._acptfactunits.values())
        node_dict = {
            acptfact_x.base.lower(): acptfact_x for acptfact_x in acptfact_list
        }
        node_lowercase_ordered_list = sorted(list(node_dict))
        node_orginalcase_ordered_list = [
            node_dict[node_l] for node_l in node_lowercase_ordered_list
        ]

        list_x = [["", ""]]
        list_x.extend(
            [acptfact_x.base, acptfact_x.pick]
            for acptfact_x in node_orginalcase_ordered_list
        )
        return list_x

    def del_acptfact(self, base: Road):
        self._set_acptfacts_empty_if_null()
        self._idearoot._acptfactunits.pop(base)

    def get_tree_metrics(self) -> TreeMetrics:
        tree_metrics = TreeMetrics()
        self._idearoot._level = 0
        tree_metrics.evaluate_node(
            level=self._idearoot._level,
            requireds=self._idearoot._requiredunits,
            brandlinks=self._idearoot._brandlinks,
            uid=self._idearoot._uid,
            promise=self._idearoot.promise,
            idea_road=self._idearoot.get_road(),
        )

        idea_list = [self._idearoot]
        while idea_list != []:
            idea_x = idea_list.pop()
            if idea_x._kids != None:
                for idea_kid in idea_x._kids.values():
                    self._eval_tree_metrics(idea_x, idea_kid, tree_metrics, idea_list)
        return tree_metrics

    def _eval_tree_metrics(self, idea_x, idea_kid, tree_metrics, idea_list):
        idea_kid._level = idea_x._level + 1
        tree_metrics.evaluate_node(
            level=idea_kid._level,
            requireds=idea_kid._requiredunits,
            brandlinks=idea_kid._brandlinks,
            uid=idea_kid._uid,
            promise=idea_kid.promise,
            idea_road=idea_kid.get_road(),
        )
        idea_list.append(idea_kid)

    def get_idea_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_idea_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        idea_uid_max = tree_metrics.uid_max
        idea_uid_dict = tree_metrics.uid_dict

        for idea_x in self.get_idea_list():
            if idea_x._uid is None or idea_uid_dict.get(idea_x._uid) > 1:
                new_idea_uid_max = idea_uid_max + 1
                self.edit_idea_attr(road=idea_x.get_road(), uid=new_idea_uid_max)
                idea_uid_max = new_idea_uid_max

    def get_node_count(self):
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.nodeCount

    def get_level_count(self, level):
        tree_metrics = self.get_tree_metrics()
        levelCount = None
        try:
            levelCount = tree_metrics.levelCount[level]
        except KeyError:
            levelCount = 0
        return levelCount

    def get_required_bases(self) -> dict[Road:int]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.required_bases

    def get_missing_acptfact_bases(self):
        tree_metrics = self.get_tree_metrics()
        required_bases = tree_metrics.required_bases
        missing_bases = {}
        if self._idearoot._acptfactunits is None:
            missing_bases = required_bases
        elif self._idearoot._acptfactunits != None:
            for base, base_count in required_bases.items():
                try:
                    levelCount = self._idearoot._acptfactunits[base]
                except KeyError:
                    missing_bases[base] = base_count

        return missing_bases

    def add_idea(
        self,
        idea_kid: IdeaCore,
        walk: Road,
        create_missing_ideas_brands: bool = None,
    ):
        temp_idea = self._idearoot
        _road = walk.split(",")
        temp_road = _road.pop(0)

        # idearoot cannot be replaced
        if temp_road == self._desc and _road == []:
            idea_kid.set_road(parent_road=Road(self._desc))
        else:
            parent_road = [temp_road]
            while _road != []:
                temp_road = _road.pop(0)
                temp_idea = self._get_or_create_leveln_idea(
                    parent_idea=temp_idea, idea_desc=temp_road
                )
                parent_road.append(temp_road)

            idea_kid.set_road(parent_road=",".join(parent_road))

        temp_idea.add_kid(idea_kid)

        if create_missing_ideas_brands:
            self._create_missing_ideas(road=Road(f"{walk},{idea_kid._desc}"))
            self._create_missing_brands_allys(brandlinks=idea_kid._brandlinks)

    def _create_missing_brands_allys(self, brandlinks: dict[BrandName:BrandLink]):
        for brandlink_x in brandlinks.values():
            if self._brands.get(brandlink_x.name) is None:
                brandunit_x = brandunit_shop(name=brandlink_x.name, _allys={})
                self.set_brandunit(brandunit=brandunit_x)

    def _create_missing_ideas(self, road):
        self.set_agent_metrics()
        posted_idea = self.get_idea_kid(road)

        for required_x in posted_idea._requiredunits.values():
            self._set_ideakid_if_empty(road=required_x.base)
            for sufffact_x in required_x.sufffacts.values():
                self._set_ideakid_if_empty(road=sufffact_x.need)
        if posted_idea._special_road != None:
            self._set_ideakid_if_empty(road=posted_idea._special_road)
        if posted_idea._numeric_road != None:
            self._set_ideakid_if_empty(road=posted_idea._numeric_road)

    def _set_ideakid_if_empty(self, road: Road):
        try:
            self.get_idea_kid(road)
        except InvalidAgentException:
            base_idea = IdeaKid(
                _desc=get_terminus_node_from_road(road=road),
                _walk=get_walk_from_road(road=road),
            )
            self.add_idea(idea_kid=base_idea, walk=base_idea._walk)

    # def _get_or_create_level1_idea(self, idea_desc: str) -> IdeaKid:
    #     return_idea = None
    #     try:
    #         return_idea = self._kids[idea_desc]
    #     except Exception:
    #         KeyError
    #         self.add_kid(IdeaKid(_desc=idea_desc))
    #         return_idea = self._kids[idea_desc]

    #     return return_idea

    def _get_or_create_leveln_idea(self, parent_idea: IdeaCore, idea_desc: str):
        return_idea = None
        try:
            return_idea = parent_idea._kids[idea_desc]
        except Exception:
            KeyError
            parent_idea.add_kid(IdeaKid(_desc=idea_desc))
            return_idea = parent_idea._kids[idea_desc]

        return return_idea

    def del_idea_kid(self, road: Road, del_children: bool = True):
        x_road = road.split(",")
        temp_desc = x_road.pop(0)
        temps_d = [temp_desc]

        if x_road == []:
            raise InvalidAgentException("Object cannot delete itself")
        temp_desc = x_road.pop(0)
        temps_d.append(temp_desc)

        if x_road == []:
            if not del_children:
                d_temp_idea = self.get_idea_kid(road=",".join(temps_d))
                for kid in d_temp_idea._kids.values():
                    self.add_idea(idea_kid=kid, walk=",".join(temps_d[:-1]))
            self._idearoot._kids.pop(temp_desc)
        elif x_road != []:
            i_temp_idea = self._idearoot._kids[temp_desc]
            while x_road != []:
                temp_desc = x_road.pop(0)
                parent_temp_idea = i_temp_idea
                i_temp_idea = i_temp_idea._kids[temp_desc]

            parent_temp_idea._kids.pop(temp_desc)
        self.set_agent_metrics()

    def agent_and_idearoot_desc_edit(self, new_desc):
        self._desc = new_desc
        self.edit_idea_desc(old_road=self._idearoot._desc, new_desc=new_desc)

    def edit_idea_desc(
        self,
        old_road: Road,
        new_desc: str,
    ):
        # confirm idea exists
        if self.get_idea_kid(road=old_road) is None:
            raise InvalidAgentException(f"Idea {old_road=} does not exist")

        walk = get_walk_from_road(road=old_road)
        new_road = road_validate(Road(f"{walk},{new_desc}"))

        if old_road != new_road:
            # if root _desc is changed
            if walk == "":
                self._idearoot._desc = new_desc
                self._idearoot._walk = walk
            else:
                self._non_root_idea_desc_edit(old_road, new_desc, walk)
            self._idearoot_find_replace_road(old_road=old_road, new_road=new_road)
            self._set_acptfacts_empty_if_null()
            self._idearoot._acptfactunits = find_replace_road_key_dict(
                dict_x=self._idearoot._acptfactunits,
                old_road=old_road,
                new_road=new_road,
            )

    def _non_root_idea_desc_edit(self, old_road, new_desc, walk):
        idea_z = self.get_idea_kid(road=old_road)
        idea_z._desc = new_desc
        idea_z._walk = walk
        idea_parent = self.get_idea_kid(road=get_walk_from_road(old_road))
        idea_parent._kids.pop(get_terminus_node_from_road(old_road))
        idea_parent._kids[idea_z._desc] = idea_z

    def _idearoot_find_replace_road(self, old_road, new_road):
        self._idearoot.find_replace_road(old_road=old_road, new_road=new_road)

        idea_iter_list = [self._idearoot]
        while idea_iter_list != []:
            listed_idea = idea_iter_list.pop()
            # put all idea_children in idea list
            if listed_idea._kids != None:
                for idea_kid in listed_idea._kids.values():
                    idea_iter_list.append(idea_kid)
                    if is_sub_road_in_src_road(
                        src_road=idea_kid._walk,
                        sub_road=old_road,
                    ):
                        idea_kid._walk = change_road(
                            current_road=idea_kid._walk,
                            old_road=old_road,
                            new_road=new_road,
                        )
                    idea_kid.find_replace_road(old_road=old_road, new_road=new_road)

    def get_begin_close_if_denom_or_numeric_road(
        self,
        begin: float,
        close: float,
        addin: float,
        numor: float,
        denom: float,
        reest: bool,
        idea_road: Road,
        numeric_road: Road,
    ):
        anc_roads = get_ancestor_roads(road=idea_road)
        if (addin != None or numor != None or denom != None or reest != None) and len(
            anc_roads
        ) == 1:
            raise InvalidAgentException("Root Idea cannot have numor denom reest.")
        parent_road = self._desc if len(anc_roads) == 1 else anc_roads[1]

        parent_has_range = None
        parent_idea_x = self.get_idea_kid(road=parent_road)
        parent_begin = parent_idea_x._begin
        parent_close = parent_idea_x._close
        parent_has_range = parent_begin is not None and parent_close is not None

        numeric_begin = None
        numeric_close = None
        numeric_range = None
        if numeric_road != None:
            numeric_idea_x = self.get_idea_kid(road=numeric_road)
            numeric_begin = numeric_idea_x._begin
            numeric_close = numeric_idea_x._close
            numeric_range = numeric_begin != None and numeric_close != None

        if parent_has_range and addin not in [None, 0]:
            parent_begin = parent_begin + addin
            parent_close = parent_close + addin

        begin, close = self._transform_begin_close(
            reest=reest,
            begin=begin,
            close=close,
            numor=numor,
            denom=denom,
            parent_has_range=parent_has_range,
            parent_begin=parent_begin,
            parent_close=parent_close,
            numeric_range=numeric_range,
            numeric_begin=numeric_begin,
            numeric_close=numeric_close,
        )

        if parent_has_range and numeric_range:
            raise InvalidAgentException(
                "Idea has begin-close range parent, cannot have numeric_road"
            )
        elif not parent_has_range and not numeric_range and numor != None:
            raise InvalidAgentException(
                f"Idea cannot edit {numor=}/denom/reest of '{idea_road}' if parent '{parent_road}' or ideacore._numeric_road does not have begin/close range"
            )
        return begin, close

    def _transform_begin_close(
        self,
        reest,
        begin,
        close,
        numor,
        denom,
        parent_has_range,
        parent_begin,
        parent_close,
        numeric_range,
        numeric_begin,
        numeric_close,
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
        road: Road,
        weight: int = None,
        uid: int = None,
        required: RequiredUnit = None,
        required_base: Road = None,
        required_sufffact: Road = None,
        required_sufffact_open: float = None,
        required_sufffact_nigh: float = None,
        required_sufffact_divisor: int = None,
        required_del_sufffact_base: Road = None,
        required_del_sufffact_need: Road = None,
        required_suff_idea_active_status: str = None,
        begin: float = None,
        close: float = None,
        addin: float = None,
        numor: float = None,
        denom: float = None,
        reest: bool = None,
        numeric_road: Road = None,
        special_road: float = None,
        promise: bool = None,
        problem_bool: bool = None,
        acptfactunit: AcptFactUnit = None,
        descendant_promise_count: int = None,
        all_ally_credit: bool = None,
        all_ally_debt: bool = None,
        brandlink: BrandLink = None,
        brandlink_del: BrandName = None,
        is_expanded: bool = None,
        on_meld_weight_action: str = None,
    ):
        if denom != None or numor != None or reest or addin != None:
            if addin is None:
                addin = 0
            if denom is None:
                denom = 1
            if numor is None:
                numor = 1
            if reest is None:
                reest = False

        if (
            begin != None
            or close != None
            or numor != None
            or numeric_road != None
            or addin != None
        ):
            begin, close = self.get_begin_close_if_denom_or_numeric_road(
                begin=begin,
                close=close,
                addin=addin,
                numor=numor,
                denom=denom,
                reest=reest,
                idea_road=road,
                numeric_road=numeric_road,
            )

        required_sufffact_numor = None
        required_sufffact_denom = required_sufffact_divisor
        required_sufffact_reest = None

        (
            required_sufffact_open,
            required_sufffact_nigh,
            required_sufffact_numor,
            required_sufffact_denom,
            required_sufffact_reest,
        ) = self.get_idea_defined_required_attributes(
            base=required_base,
            sufffact=required_sufffact,
            open=required_sufffact_open,
            nigh=required_sufffact_nigh,
            numor=required_sufffact_numor,
            denom=required_sufffact_denom,
            reest=required_sufffact_reest,
        )

        temp_idea = self.get_idea_kid(road=road)
        idea_attr = IdeaAttrHolder(
            weight=weight,
            uid=uid,
            required=required,
            required_base=required_base,
            required_sufffact=required_sufffact,
            required_sufffact_open=required_sufffact_open,
            required_sufffact_nigh=required_sufffact_nigh,
            required_sufffact_divisor=required_sufffact_denom,
            required_del_sufffact_base=required_del_sufffact_base,
            required_del_sufffact_need=required_del_sufffact_need,
            required_suff_idea_active_status=required_suff_idea_active_status,
            begin=begin,
            close=close,
            addin=addin,
            numor=numor,
            denom=denom,
            reest=reest,
            numeric_road=numeric_road,
            special_road=special_road,
            descendant_promise_count=descendant_promise_count,
            all_ally_credit=all_ally_credit,
            all_ally_debt=all_ally_debt,
            brandlink=brandlink,
            brandlink_del=brandlink_del,
            is_expanded=is_expanded,
            promise=promise,
            problem_bool=problem_bool,
            on_meld_weight_action=on_meld_weight_action,
        )
        temp_idea._set_idea_attr(idea_attr=idea_attr)
        if f"{type(temp_idea)}".find("'.idea.IdeaRoot'>") <= 0:
            temp_idea._set_ideakid_attr(acptfactunit=acptfactunit)

        # deleting a brandlink reqquires a tree traverse to correctly set brandheirs and brandlines
        if brandlink_del != None or brandlink != None:
            self.set_agent_metrics()

    def get_idea_defined_required_attributes(
        self,
        base: Road,
        sufffact: Road,
        open: float,
        nigh: float,
        numor: int,
        denom: int,
        reest: bool,
    ):
        # this might be XXXX simplier after #51: spllts automatically set idea open and nigh
        # thus there cannot exist a idea with a spllt but no open/nigh.
        open_x = open
        nigh_x = nigh
        numor_x = numor
        denom_x = denom
        reest_x = reest

        anc_open = None
        anc_nigh = None
        anc_numor = None
        anc_denom = None
        anc_reest = None
        # if base != None and sufffact != None:
        #     # evaluate all ideas between base and sufffact, get deepest non-none data
        #     base_roads = get_ancestor_roads(road=base)
        #     sufffact_roads = get_ancestor_roads(road=sufffact)
        #     between_roads = [x for x in sufffact_roads if x not in base_roads]
        #     between_roads.append(base)

        #     # while between_roads != []:
        #     #     x_road = between_roads.pop()
        #     #     x_idea = self.get_idea_kid(road=x_road)
        #     #     if x_idea._spllt != None:
        #     #         anc_divisor = x_idea._spllt
        #     #         if x_idea._begin != None:
        #     #             anc_open = 0
        #     #         if x_idea._close != None:
        #     #             anc_nigh = x_idea._spllt

        #     #     if x_idea._begin != None:
        #     #         anc_open = x_idea._begin
        #     #     if x_idea._close != None:
        #     #         anc_nigh = x_idea._close
        if sufffact != None:
            x_idea = self.get_idea_kid(road=sufffact)
            anc_open = x_idea._begin
            anc_nigh = x_idea._close
            anc_numor = x_idea._numor
            anc_denom = x_idea._denom
            anc_reest = x_idea._reest

        if open_x is None:
            open_x = anc_open
        if nigh_x is None:
            nigh_x = anc_nigh
        if numor_x is None:
            numor_x = anc_numor
        if denom_x is None:
            denom_x = anc_denom
        if reest_x is None:
            reest_x = anc_reest

        return open_x, nigh_x, numor_x, denom_x, reest_x

    def del_idea_required_sufffact(
        self, road: Road, required_base: Road, required_sufffact: Road
    ):
        self.edit_idea_attr(
            road=road,
            required_del_sufffact_base=required_base,
            required_del_sufffact_need=required_sufffact,
        )

    def _set_acptfacts_empty_if_null(self):
        self._idearoot.set_acptfactunits_empty_if_null()

    def get_agenda_items(
        self, base: Road = None, agenda_todo: bool = True, agenda_state: bool = True
    ) -> list[IdeaCore]:
        return [
            idea for idea in self.get_idea_list() if idea.is_agenda_item(base_x=base)
        ]

    def set_agenda_task_complete(self, task_road: Road, base: Road):
        promise_item = self.get_idea_kid(road=task_road)
        promise_item.set_acptfactunit_to_complete(
            base_acptfactunit=self._idearoot._acptfactunits[base]
        )

    def get_allyunit_total_creditor_weight(self):
        return sum(allyunit.get_creditor_weight() for allyunit in self._allys.values())

    def get_allyunit_total_debtor_weight(self):
        return sum(allyunit.get_debtor_weight() for allyunit in self._allys.values())

    def _add_to_allyunits_agent_credit_debt(self, idea_agent_importance: float):
        sum_allyunit_creditor_weight = self.get_allyunit_total_creditor_weight()
        sum_allyunit_debtor_weight = self.get_allyunit_total_debtor_weight()

        for allyunit_x in self._allys.values():
            au_agent_credit = (
                idea_agent_importance * allyunit_x.get_creditor_weight()
            ) / sum_allyunit_creditor_weight

            au_agent_debt = (
                idea_agent_importance * allyunit_x.get_debtor_weight()
            ) / sum_allyunit_debtor_weight

            allyunit_x.add_agent_credit_debt(
                agent_credit=au_agent_credit,
                agent_debt=au_agent_debt,
                agent_agenda_credit=0,
                agent_agenda_debt=0,
            )

    def _add_to_allyunits_agent_agenda_credit_debt(self, idea_agent_importance: float):
        sum_allyunit_creditor_weight = self.get_allyunit_total_creditor_weight()
        sum_allyunit_debtor_weight = self.get_allyunit_total_debtor_weight()

        for allyunit_x in self._allys.values():
            au_agent_agenda_credit = (
                idea_agent_importance * allyunit_x.get_creditor_weight()
            ) / sum_allyunit_creditor_weight

            au_agent_agenda_debt = (
                idea_agent_importance * allyunit_x.get_debtor_weight()
            ) / sum_allyunit_debtor_weight

            allyunit_x.add_agent_credit_debt(
                agent_credit=0,
                agent_debt=0,
                agent_agenda_credit=au_agent_agenda_credit,
                agent_agenda_debt=au_agent_agenda_debt,
            )

    def _set_allyunits_agent_agenda_importance(self, agent_agenda_importance: float):
        sum_allyunit_creditor_weight = self.get_allyunit_total_creditor_weight()
        sum_allyunit_debtor_weight = self.get_allyunit_total_debtor_weight()

        for allyunit_x in self._allys.values():
            au_agent_agenda_credit = (
                agent_agenda_importance * allyunit_x.get_creditor_weight()
            ) / sum_allyunit_creditor_weight

            au_agent_agenda_debt = (
                agent_agenda_importance * allyunit_x.get_debtor_weight()
            ) / sum_allyunit_debtor_weight

            allyunit_x.add_agent_agenda_credit_debt(
                agent_agenda_credit=au_agent_agenda_credit,
                agent_agenda_debt=au_agent_agenda_debt,
            )

    def _reset_brandunits_agent_credit_debt(self):
        self.set_brandunits_empty_if_null()
        for brandlink_obj in self._brands.values():
            brandlink_obj.reset_agent_credit_debt()

    def _set_brandunits_agent_importance(self, brandheirs: dict[BrandName:BrandLink]):
        self.set_brandunits_empty_if_null()
        for brandlink_obj in brandheirs.values():
            self.add_to_brand_agent_credit_debt(
                brandname=brandlink_obj.name,
                brandheir_agent_credit=brandlink_obj._agent_credit,
                brandheir_agent_debt=brandlink_obj._agent_debt,
            )

    def _distribute_agent_agenda_importance(self):
        for idea in self._idea_dict.values():
            # If there are no brandlines associated with idea
            # distribute agent_importance via general allyunit
            # credit ratio and debt ratio
            # if idea.is_agenda_item() and idea._brandlines == {}:
            if idea.is_agenda_item():
                if idea._brandlines == {}:
                    self._add_to_allyunits_agent_agenda_credit_debt(
                        idea._agent_importance
                    )
                else:
                    for brandline_x in idea._brandlines.values():
                        self.add_to_brand_agent_agenda_credit_debt(
                            brandname=brandline_x.name,
                            brandline_agent_credit=brandline_x._agent_credit,
                            brandline_agent_debt=brandline_x._agent_debt,
                        )

    def _distribute_brands_agent_importance(self):
        for brand_obj in self._brands.values():
            brand_obj._set_allylink_agent_credit_debt()
            for allylink in brand_obj._allys.values():
                self.add_to_allyunit_agent_credit_debt(
                    allyunit_name=allylink.name,
                    agent_credit=allylink._agent_credit,
                    agent_debt=allylink._agent_debt,
                    agent_agenda_credit=allylink._agent_agenda_credit,
                    agent_agenda_debt=allylink._agent_agenda_debt,
                )

    def _set_agent_agenda_ratio_credit_debt(self):
        agent_agenda_ratio_credit_sum = 0
        agent_agenda_ratio_debt_sum = 0

        for allyunit_x in self._allys.values():
            agent_agenda_ratio_credit_sum += allyunit_x._agent_agenda_credit
            agent_agenda_ratio_debt_sum += allyunit_x._agent_agenda_debt

        for allyunit_x in self._allys.values():
            allyunit_x.set_agent_agenda_ratio_credit_debt(
                agent_agenda_ratio_credit_sum=agent_agenda_ratio_credit_sum,
                agent_agenda_ratio_debt_sum=agent_agenda_ratio_debt_sum,
                agent_allyunit_total_creditor_weight=self.get_allyunit_total_creditor_weight(),
                agent_allyunit_total_debtor_weight=self.get_allyunit_total_debtor_weight(),
            )

    def get_ally_brands(self, ally_name: AllyName):
        brands = []
        for brand in self._brands.values():
            brands.extend(
                brand.name
                for allylink in brand._allys.values()
                if allylink.name == ally_name
            )

        return brands

    def _reset_allyunit_agent_credit_debt(self):
        self.set_allys_empty_if_null()
        for allyunit in self._allys.values():
            allyunit.reset_agent_credit_debt()

    def _idearoot_inherit_requiredheirs(self):
        self._idearoot.set_requiredunits_empty_if_null()
        x_dict = {}
        for required in self._idearoot._requiredunits.values():
            x_required = RequiredHeir(base=required.base, sufffacts=None)
            x_sufffacts = {}
            for w in required.sufffacts.values():
                sufffact_x = sufffactunit_shop(
                    need=w.need,
                    open=w.open,
                    nigh=w.nigh,
                    divisor=w.divisor,
                )
                x_sufffacts[sufffact_x.need] = sufffact_x
            x_required.sufffacts = x_sufffacts
            x_dict[x_required.base] = x_required
        self._idearoot._requiredheirs = x_dict

    def get_idea_kid(self, road: Road) -> IdeaKid:
        if road is None:
            raise InvalidAgentException("get_idea_kid received road=None")
        nodes = road.split(",")
        src = nodes.pop(0)
        temp_idea = None

        if nodes == [] and src == self._idearoot._desc:
            temp_idea = self._idearoot
            # raise InvalidAgentException(f"Cannot return root '{src}'")
        else:
            idea_desc = src if nodes == [] else nodes.pop(0)
            try:
                temp_idea = self._idearoot._kids.get(idea_desc)

                while nodes != []:
                    idea_desc = nodes.pop(0)
                    temp_idea = temp_idea._kids[idea_desc]
                if temp_idea is None:
                    raise InvalidAgentException(
                        f"Temp_idea is None {idea_desc=}. No item at '{road}'"
                    )
            except:
                raise InvalidAgentException(
                    f"Getting {idea_desc=} failed no item at '{road}'"
                )

        return temp_idea

    def get_idea_ranged_kids(
        self, idea_road: str, begin: float = None, close: float = None
    ) -> dict[IdeaCore]:
        parent_idea = self.get_idea_kid(road=idea_road)
        if begin is None and close is None:
            begin = parent_idea._begin
            close = parent_idea._close
        elif begin != None and close is None:
            close = begin

        idea_list = parent_idea.get_kids_in_range(begin=begin, close=close)
        return {idea_x._desc: idea_x for idea_x in idea_list}

    def _set_ancestor_metrics(self, road: Road):
        da_count = 0
        child_brandlines = None
        if road is None:
            road = ""

        brand_everyone = None
        if len(road.split(",")) <= 1:
            brand_everyone = self._idearoot._brandheirs in [None, {}]
        else:
            ancestor_roads = get_ancestor_roads(road=road)
            # remove root road
            ancestor_roads.pop(len(ancestor_roads) - 1)

            while ancestor_roads != []:
                # youngest_untouched_idea
                yu_idea_obj = self.get_idea_kid(road=ancestor_roads.pop(0))

                yu_idea_obj.set_descendant_promise_count_zero_if_null()
                yu_idea_obj._descendant_promise_count += da_count
                if yu_idea_obj.is_kidless():
                    yu_idea_obj.set_kidless_brandlines()
                    child_brandlines = yu_idea_obj._brandlines
                else:
                    yu_idea_obj.set_brandlines(child_brandlines=child_brandlines)

                if yu_idea_obj._task == True:
                    da_count += 1

                if (
                    brand_everyone != False
                    and yu_idea_obj._all_ally_credit != False
                    and yu_idea_obj._all_ally_debt != False
                    and yu_idea_obj._brandheirs != {}
                    or brand_everyone != False
                    and yu_idea_obj._all_ally_credit == False
                    and yu_idea_obj._all_ally_debt == False
                ):
                    brand_everyone = False
                elif brand_everyone != False:
                    brand_everyone = True
                yu_idea_obj._all_ally_credit = brand_everyone
                yu_idea_obj._all_ally_debt = brand_everyone

            if (
                brand_everyone != False
                and self._idearoot._all_ally_credit != False
                and self._idearoot._all_ally_debt != False
                and self._idearoot._brandheirs != {}
                or brand_everyone != False
                and self._idearoot._all_ally_credit == False
                and self._idearoot._all_ally_debt == False
            ):
                brand_everyone = False
            elif brand_everyone != False and yu_idea_obj._brandheirs == {}:
                brand_everyone = True
        self._idearoot._all_ally_credit = brand_everyone
        self._idearoot._all_ally_debt = brand_everyone

        if self._idearoot.is_kidless():
            self._idearoot.set_kidless_brandlines()
        else:
            self._idearoot.set_brandlines(child_brandlines=child_brandlines)
        self._idearoot.set_descendant_promise_count_zero_if_null()
        self._idearoot._descendant_promise_count += da_count

    def _set_root_attributes(self):
        self._idearoot._level = 0
        self._idearoot.set_road(parent_road="")
        self._idearoot.set_requiredheirs(
            requiredheirs=self._idearoot._requiredunits, agent_idea_dict=self._idea_dict
        )
        self._idearoot.inherit_brandheirs()
        self._idearoot.clear_brandlines()
        self._idearoot.set_acptfactunits_empty_if_null()
        self._idearoot._weight = 1
        self._idearoot._kids_total_weight = 0
        self._idearoot.set_kids_total_weight()
        self._idearoot.set_sibling_total_weight(1)
        self._idearoot.set_agent_importance(coin_onset_x=0, parent_coin_cease=1)
        self._idearoot.set_brandheirs_agent_credit_debit()
        self._idearoot.set_ancestor_promise_count(0, False)
        self._idearoot.clear_descendant_promise_count()
        self._idearoot.clear_all_ally_credit_debt()
        self._idearoot.promise = False

        if self._idearoot.is_kidless():
            self._set_ancestor_metrics(road=self._idearoot._walk)
            self._distribute_agent_importance(idea=self._idearoot)

    def _set_kids_attributes(
        self,
        idea_kid: IdeaKid,
        coin_onset: float,
        parent_coin_cease: float,
        parent_idea: IdeaKid = None,
    ) -> IdeaKid:
        parent_acptfacts = None
        parent_requiredheirs = None

        if parent_idea is None:
            parent_idea = self._idearoot
            parent_acptfacts = self._idearoot._acptfactunits
            parent_requiredheirs = self._idearoot_inherit_requiredheirs()
        else:
            parent_acptfacts = parent_idea._acptfactheirs
            parent_requiredheirs = parent_idea._requiredheirs

        idea_kid.set_level(parent_level=parent_idea._level)
        idea_kid.set_road(parent_road=parent_idea._walk, parent_desc=parent_idea._desc)
        idea_kid.set_acptfactunits_empty_if_null()
        idea_kid.set_acptfactheirs(acptfacts=parent_acptfacts)
        idea_kid.set_requiredheirs(parent_requiredheirs, self._idea_dict)
        idea_kid.inherit_brandheirs(parent_brandheirs=parent_idea._brandheirs)
        idea_kid.clear_brandlines()
        idea_kid.set_active_status(tree_traverse_count=self._tree_traverse_count)
        idea_kid.set_sibling_total_weight(parent_idea._kids_total_weight)
        # idea_kid.set_agent_importance(
        #     parent_agent_importance=parent_idea._agent_importance,
        #     coin_onset_x=coin_onset_x,
        #     parent_coin_cease=parent_idea._agent_coin_cease,
        # )
        idea_kid.set_agent_importance(
            coin_onset_x=coin_onset,
            parent_agent_importance=parent_idea._agent_importance,
            parent_coin_cease=parent_coin_cease,
        )
        idea_kid.set_ancestor_promise_count(
            parent_idea._ancestor_promise_count, parent_idea.promise
        )
        idea_kid.clear_descendant_promise_count()
        idea_kid.clear_all_ally_credit_debt()

        if idea_kid.is_kidless():
            # set idea's ancestor metrics using agent root as common reference
            self._set_ancestor_metrics(road=idea_kid.get_road())
            self._distribute_agent_importance(idea=idea_kid)

    def _distribute_agent_importance(self, idea: IdeaCore):
        # TODO manage situations where brandheir.creditor_weight is None for all brandheirs
        # TODO manage situations where brandheir.debtor_weight is None for all brandheirs
        if idea.is_brandheirless() == False:
            self._set_brandunits_agent_importance(brandheirs=idea._brandheirs)
        elif idea.is_brandheirless():
            self._add_to_allyunits_agent_credit_debt(
                idea_agent_importance=idea._agent_importance
            )

    def get_agent_importance(
        self, parent_agent_importance: float, weight: int, sibling_total_weight: int
    ):
        sibling_ratio = weight / sibling_total_weight
        return parent_agent_importance * sibling_ratio

    def get_idea_list(self):
        self.set_agent_metrics()
        return list(self._idea_dict.values())

    def set_agent_metrics(self):
        self._set_acptfacts_empty_if_null()

        self._rational = False
        self._tree_traverse_count = 0
        self._idea_dict = {self._idearoot.get_road(): self._idearoot}

        while (
            not self._rational and self._tree_traverse_count < self._max_tree_traverse
        ):
            self._execute_tree_traverse()
            self._run_after_each_tree_traverse()
            self._tree_traverse_count += 1
        self._run_after_idea_all_tree_traverses()

    def _execute_tree_traverse(self):
        self._run_before_idea_tree_traverse()
        self._set_root_attributes()

        coin_onset = self._idearoot._agent_coin_onset
        parent_coin_cease = self._idearoot._agent_coin_cease

        cache_idea_list = []
        for idea_kid in self._idearoot._kids.values():
            self._set_kids_attributes(
                idea_kid=idea_kid,
                coin_onset=coin_onset,
                parent_coin_cease=parent_coin_cease,
            )
            cache_idea_list.append(idea_kid)
            coin_onset += idea_kid._agent_importance

        # no function recursion, recursion by iterateing over list that can be added to by iterations
        while cache_idea_list != []:
            parent_idea = cache_idea_list.pop()
            if self._tree_traverse_count == 0:
                self._idea_dict[parent_idea.get_road()] = parent_idea

            if parent_idea._kids != None:
                coin_onset = parent_idea._agent_coin_onset
                parent_coin_cease = parent_idea._agent_coin_cease
                for idea_kid in parent_idea._kids.values():
                    self._set_kids_attributes(
                        idea_kid=idea_kid,
                        coin_onset=coin_onset,
                        parent_coin_cease=parent_coin_cease,
                        parent_idea=parent_idea,
                    )
                    cache_idea_list.append(idea_kid)
                    coin_onset += idea_kid._agent_importance

    def _run_after_each_tree_traverse(self):
        any_idea_active_status_changed = False
        for idea in self._idea_dict.values():
            idea.set_active_status_hx_empty_if_null()
            if idea._active_status_hx.get(self._tree_traverse_count) != None:
                any_idea_active_status_changed = True

        if any_idea_active_status_changed == False:
            self._rational = True

    def _run_after_idea_all_tree_traverses(self):
        self._distribute_agent_agenda_importance()
        self._distribute_brands_agent_importance()
        self._set_agent_agenda_ratio_credit_debt()

    def _run_before_idea_tree_traverse(self):
        self._reset_brandunits_agent_credit_debt()
        self._reset_brandunits_agent_credit_debt()
        self._reset_allyunit_agent_credit_debt()

    def get_heir_road_list(self, src_road: Road):
        # create list of all idea roads (road+desc)
        return [
            road
            for road in self.get_idea_tree_ordered_road_list()
            if road.find(src_road) == 0
        ]

    def get_idea_tree_ordered_road_list(self, no_range_descendents: bool = False):
        idea_list = self.get_idea_list()
        node_dict = {idea.get_road().lower(): idea.get_road() for idea in idea_list}
        node_lowercase_ordered_list = sorted(list(node_dict))
        node_orginalcase_ordered_list = [
            node_dict[node_l] for node_l in node_lowercase_ordered_list
        ]

        list_x = []
        for road in node_orginalcase_ordered_list:
            if not no_range_descendents:
                list_x.append(road)
            else:
                anc_list = get_ancestor_roads(road=road)
                if len(anc_list) == 1:
                    list_x.append(road)
                elif len(anc_list) == 2:
                    if self._idearoot._begin is None and self._idearoot._close is None:
                        list_x.append(road)
                else:
                    parent_idea = self.get_idea_kid(road=anc_list[1])
                    if parent_idea._begin is None and parent_idea._close is None:
                        list_x.append(road)

        return list_x

    def get_acptfactunits_dict(self):
        x_dict = {}
        if self._idearoot._acptfactunits != None:
            for acptfact_road, acptfact_obj in self._idearoot._acptfactunits.items():
                x_dict[acptfact_road] = acptfact_obj.get_dict()
        return x_dict

    def get_allys_dict(self):
        x_dict = {}
        if self._allys != None:
            for ally_name, ally_obj in self._allys.items():
                x_dict[ally_name] = ally_obj.get_dict()
        return x_dict

    def brandunit_shops_dict(self):
        x_dict = {}
        if self._brands != None:
            for brand_name, brand_obj in self._brands.items():
                x_dict[brand_name] = brand_obj.get_dict()
        return x_dict

    def get_dict(self):
        self.set_agent_metrics()
        return {
            "_kids": self._idearoot.get_kids_dict(),
            "_requiredunits": self._idearoot.get_requiredunits_dict(),
            "_acptfactunits": self.get_acptfactunits_dict(),
            "_allys": self.get_allys_dict(),
            "_brands": self.brandunit_shops_dict(),
            "_brandlinks": self._idearoot.get_brandlinks_dict(),
            "_weight": self._weight,
            "_desc": self._desc,
            "_uid": self._idearoot._uid,
            "_begin": self._idearoot._begin,
            "_close": self._idearoot._close,
            "_addin": self._idearoot._addin,
            "_numor": self._idearoot._numor,
            "_denom": self._idearoot._denom,
            "_reest": self._idearoot._reest,
            "_problem_bool": self._idearoot._problem_bool,
            "_is_expanded": self._idearoot._is_expanded,
            "_special_road": self._idearoot._special_road,
            "_numeric_road": self._idearoot._numeric_road,
            "_on_meld_weight_action": self._idearoot._on_meld_weight_action,
            "_max_tree_traverse": self._max_tree_traverse,
        }

    def get_json(self):
        x_dict = self.get_dict()
        return x_get_json(dict_x=x_dict)

    def set_time_hreg_ideas(self, c400_count):
        ideabase_list = _get_time_hreg_src_idea(c400_count=c400_count)
        while len(ideabase_list) != 0:
            yb = ideabase_list.pop(0)
            special_road_x = None
            if yb.sr != None:
                special_road_x = f"{self._desc},{yb.sr}"

            idea_x = IdeaKid(
                _desc=yb.n,
                _begin=yb.b,
                _close=yb.c,
                _weight=yb.weight,
                _is_expanded=False,
                _addin=yb.a,
                _numor=yb.mn,
                _denom=yb.md,
                _reest=yb.mr,
                _special_road=special_road_x,
            )
            road_x = f"{self._desc},{yb.rr}"
            self.add_idea(idea_kid=idea_x, walk=road_x)

            numeric_road_x = None
            if yb.nr != None:
                numeric_road_x = f"{self._desc},{yb.nr}"
                self.edit_idea_attr(
                    road=f"{road_x},{yb.n}", numeric_road=numeric_road_x
                )
            if yb.a != None:
                self.edit_idea_attr(
                    road=f"{road_x},{yb.n}", addin=yb.a, denom=yb.md, numor=yb.mn
                )

        self.set_agent_metrics()

    def get_agent4ally(self, ally_name: AllyName, acptfacts: dict[Road:AcptFactCore]):
        self.set_agent_metrics()
        agent4ally = AgentUnit(_desc=ally_name)
        agent4ally._idearoot._agent_importance = self._idearoot._agent_importance
        # get ally's allys: allyzone

        # get allyzone brands
        ally_brands = self.get_ally_brands(ally_name=ally_name)

        # set agent4ally by traversing the idea tree and selecting associated brands
        # set root
        not_included_agent_importance = 0
        agent4ally._idearoot._kids = {}
        for ykx in self._idearoot._kids.values():
            y4a_included = any(
                brand_ancestor.name in ally_brands
                for brand_ancestor in ykx._brandlines.values()
            )

            if y4a_included:
                y4a_new = IdeaKid(
                    _desc=ykx._desc,
                    _agent_importance=ykx._agent_importance,
                    _requiredunits=ykx._requiredunits,
                    _brandlinks=ykx._brandlinks,
                    _begin=ykx._begin,
                    _close=ykx._close,
                    promise=ykx.promise,
                    _task=ykx._task,
                )
                agent4ally._idearoot._kids[ykx._desc] = y4a_new
            else:
                not_included_agent_importance += ykx._agent_importance

        if not_included_agent_importance > 0:
            y4a_other = IdeaKid(
                _desc="__other__",
                _agent_importance=not_included_agent_importance,
            )
            agent4ally._idearoot._kids[y4a_other._desc] = y4a_other

        return agent4ally

    # def get_agenda_items(
    #     self, agenda_todo: bool = True, agenda_state: bool = True, base: Road = None
    # ) -> list[IdeaCore]:
    #     return list(self.get_agenda_items(base=base))

    def set_dominate_promise_idea(self, idea_kid: IdeaKid):
        idea_kid.promise = True
        self.add_idea(
            idea_kid=idea_kid,
            walk=Road(f"{idea_kid._walk}"),
            create_missing_ideas_brands=True,
        )

    def get_idea_list_without_idearoot(self):
        x_list = self.get_idea_list()
        x_list.pop(0)
        return x_list

    def make_meldable(self, starting_digest_agent):
        self.edit_idea_desc(
            old_road=Road(f"{self._idearoot._desc}"),
            new_desc=starting_digest_agent._idearoot._desc,
        )

    def meld(self, other_agent):
        self.meld_brands(other_agent=other_agent)
        self.meld_allys(other_agent=other_agent)
        self.meld_idearoot(other_agent=other_agent)
        self.meld_acptfacts(other_agent=other_agent)
        self._weight = get_meld_weight(
            src_weight=self._weight,
            src_on_meld_weight_action="default",
            other_weight=other_agent._weight,
            other_on_meld_weight_action="default",
        )

    def meld_idearoot(self, other_agent):
        self._idearoot.meld(other_idea=other_agent._idearoot, _idearoot=True)
        o_idea_list = other_agent.get_idea_list_without_idearoot()
        for oyx in o_idea_list:
            o_road = road_validate(f"{oyx._walk},{oyx._desc}")
            try:
                main_idea = self.get_idea_kid(o_road)
                main_idea.meld(other_idea=oyx)
            except Exception:
                self.add_idea(walk=oyx._walk, idea_kid=oyx)

    def meld_allys(self, other_agent):
        self.set_allys_empty_if_null()
        other_agent.set_allys_empty_if_null()
        for allyunit in other_agent._allys.values():
            if self._allys.get(allyunit.name) is None:
                self.set_allyunit(allyunit=allyunit)
            else:
                self._allys.get(allyunit.name).meld(allyunit)

    def meld_brands(self, other_agent):
        self.set_brandunits_empty_if_null()
        other_agent.set_brandunits_empty_if_null()
        for brx in other_agent._brands.values():
            if self._brands.get(brx.name) is None:
                self.set_brandunit(brandunit=brx)
            else:
                self._brands.get(brx.name).meld(brx)

    def meld_acptfacts(self, other_agent):
        self._set_acptfacts_empty_if_null()
        other_agent._set_acptfacts_empty_if_null()
        for hx in other_agent._idearoot._acptfactunits.values():
            if self._idearoot._acptfactunits.get(hx.base) is None:
                self.set_acptfact(
                    base=hx.base, acptfact=hx.acptfact, open=hx.open, nigh=hx.nigh
                )
            else:
                self._idearoot._acptfactunits.get(hx.base).meld(hx)


# class Agentshop:
def get_from_json(lw_json: str) -> AgentUnit:
    return get_from_dict(lw_dict=json.loads(lw_json))


def get_from_dict(lw_dict: dict) -> AgentUnit:
    c_x = AgentUnit()
    c_x._idearoot._requiredunits = requireds_get_from_dict(
        requireds_dict=lw_dict["_requiredunits"]
    )
    c_x._idearoot._acptfactunits = acptfactunits_get_from_dict(
        x_dict=lw_dict["_acptfactunits"]
    )
    c_x._brands = brandunits_get_from_dict(x_dict=lw_dict["_brands"])
    c_x._idearoot._brandlinks = brandlinks_get_from_dict(x_dict=lw_dict["_brandlinks"])
    c_x._allys = allyunits_get_from_dict(x_dict=lw_dict["_allys"])
    c_x._desc = lw_dict["_desc"]
    c_x._idearoot._desc = lw_dict["_desc"]
    c_x._weight = lw_dict["_weight"]
    c_x._max_tree_traverse = lw_dict.get("_max_tree_traverse")
    if lw_dict.get("_max_tree_traverse") is None:
        c_x._max_tree_traverse = 20
    c_x._idearoot._weight = lw_dict["_weight"]
    c_x._idearoot._uid = lw_dict["_uid"]
    c_x._idearoot._begin = lw_dict["_begin"]
    c_x._idearoot._close = lw_dict["_close"]
    c_x._idearoot._numor = lw_dict["_numor"]
    c_x._idearoot._denom = lw_dict["_denom"]
    c_x._idearoot._reest = lw_dict["_reest"]
    c_x._idearoot._special_road = lw_dict["_special_road"]
    c_x._idearoot._numeric_road = lw_dict["_numeric_road"]
    c_x._idearoot._is_expanded = lw_dict["_is_expanded"]

    idea_dict_list = []
    for x_dict in lw_dict["_kids"].values():
        x_dict["temp_road"] = c_x._desc
        idea_dict_list.append(x_dict)

    while idea_dict_list != []:
        idea_dict = idea_dict_list.pop(0)
        for x_dict in idea_dict["_kids"].values():
            temp_road = idea_dict["temp_road"]
            temp_desc = idea_dict["_desc"]
            x_dict["temp_road"] = f"{temp_road},{temp_desc}"
            idea_dict_list.append(x_dict)

        idea_obj = IdeaKid(
            _desc=idea_dict["_desc"],
            _weight=idea_dict["_weight"],
            _uid=idea_dict["_uid"],
            _begin=idea_dict["_begin"],
            _close=idea_dict["_close"],
            _numor=idea_dict["_numor"],
            _denom=idea_dict["_denom"],
            _reest=idea_dict["_reest"],
            promise=idea_dict["promise"],
            _requiredunits=requireds_get_from_dict(
                requireds_dict=idea_dict["_requiredunits"]
            ),
            _brandlinks=brandlinks_get_from_dict(idea_dict["_brandlinks"]),
            _acptfactunits=acptfactunits_get_from_dict(idea_dict["_acptfactunits"]),
            _is_expanded=idea_dict["_is_expanded"],
            _special_road=idea_dict["_special_road"],
            _numeric_road=idea_dict["_numeric_road"],
        )
        c_x.add_idea(idea_kid=idea_obj, walk=idea_dict["temp_road"])

    c_x.set_agent_metrics()  # clean up tree traverse defined fields
    return c_x


def get_dict_of_agent_from_dict(x_dict: dict) -> dict[str:AgentUnit]:
    agentunits = {}
    for agentunit_dict in x_dict.values():
        x_agent = get_from_dict(lw_dict=agentunit_dict)
        agentunits[x_agent._desc] = x_agent
    return agentunits


def get_meld_of_agent_files(agentunit: AgentUnit, dir: str) -> AgentUnit:
    agentunit.set_agent_metrics()
    for bond_file_x in x_func_dir_files(dir_path=dir):
        bond_x = get_from_json(
            lw_json=x_func_open_file(dest_dir=dir, file_name=bond_file_x)
        )
        bond_x.make_meldable(starting_digest_agent=agentunit)
        agentunit.meld(other_agent=bond_x)

    agentunit.set_agent_metrics()
    return agentunit
