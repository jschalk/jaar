from src.f00_instrument.dict_toolbox import (
    get_empty_list_if_None,
    get_empty_dict_if_None,
    get_0_if_None,
    get_1_if_None,
    get_json_from_dict,
)
from src.f01_road.allot import allot_scale
from src.f01_road.finance import PennyNum, FundNum
from src.f01_road.road import OwnerName, EventInt, RoadUnit
from src.f02_bud.reason_item import (
    FactUnit,
    factunits_get_from_dict,
    get_dict_from_factunits,
)
from src.f02_bud.bud import (
    BudUnit,
    budunit_shop,
    get_from_dict as budunit_get_from_dict,
)
from src.f02_bud.bud_tool import (
    get_bud_root_facts_dict as get_facts_dict,
    clear_factunits_from_bud,
    get_acct_mandate_ledger,
    get_credit_ledger,
)
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy

CELLNODE_QUOTA_DEFAULT = 1000


@dataclass
class CellUnit:
    ancestors: list[OwnerName] = None
    event_int: EventInt = None
    celldepth: int = None
    deal_owner_name: OwnerName = None
    penny: PennyNum = None
    quota: float = None
    mandate: float = None
    budadjust: BudUnit = None
    budevent_facts: dict[RoadUnit, FactUnit] = None
    found_facts: dict[RoadUnit, FactUnit] = None
    boss_facts: dict[RoadUnit, FactUnit] = None
    _reason_bases: set[RoadUnit] = None
    _acct_mandate_ledger: dict[OwnerName, FundNum] = None

    def get_cell_owner_name(self) -> OwnerName:
        return self.deal_owner_name if self.ancestors == [] else self.ancestors[-1]

    def load_budevent(self, x_bud: BudUnit):
        if not x_bud:
            self.budadjust = None
            self.budevent_facts = {}
            self._reason_bases = set()
        else:
            self._load_existing_budevent(x_bud)

    def _load_existing_budevent(self, x_bud: BudUnit):
        self._reason_bases = x_bud.get_reason_bases()
        self.budevent_facts = factunits_get_from_dict(get_facts_dict(x_bud))
        y_bud = copy_deepcopy(x_bud)
        clear_factunits_from_bud(y_bud)
        y_bud.settle_bud()
        self.budadjust = y_bud

    def get_budevents_credit_ledger(self) -> dict[OwnerName, float]:
        return {} if self.budadjust is None else get_credit_ledger(self.budadjust)

    def get_budevents_quota_ledger(self) -> dict[OwnerName, float]:
        if not self.budadjust:
            return None
        credit_ledger = self.get_budevents_credit_ledger()
        return allot_scale(credit_ledger, self.quota, self.penny)

    def set_budevent_facts_from_dict(self, fact_dict: dict[RoadUnit, dict]):
        self.budevent_facts = factunits_get_from_dict(fact_dict)

    def set_found_facts_from_dict(self, fact_dict: dict[RoadUnit, dict]):
        self.found_facts = factunits_get_from_dict(fact_dict)

    def set_boss_facts_from_other_facts(self):
        self.boss_facts = copy_deepcopy(self.budevent_facts)
        for x_fact in self.found_facts.values():
            self.boss_facts[x_fact.base] = copy_deepcopy(x_fact)

    def filter_facts_by_reason_bases(self):
        to_delete_budevent_fact_keys = set(self.budevent_facts.keys())
        to_delete_found_fact_keys = set(self.found_facts.keys())
        to_delete_boss_fact_keys = set(self.boss_facts.keys())
        to_delete_budevent_fact_keys.difference_update(self._reason_bases)
        to_delete_found_fact_keys.difference_update(self._reason_bases)
        to_delete_boss_fact_keys.difference_update(self._reason_bases)
        for budevent_fact_key in to_delete_budevent_fact_keys:
            self.budevent_facts.pop(budevent_fact_key)
        for found_fact_key in to_delete_found_fact_keys:
            self.found_facts.pop(found_fact_key)
        for boss_fact_key in to_delete_boss_fact_keys:
            self.boss_facts.pop(boss_fact_key)

    def set_budadjust_facts(self):
        for fact in self.budevent_facts.values():
            self.budadjust.add_fact(fact.base, fact.pick, fact.fopen, fact.fnigh, True)
        for fact in self.found_facts.values():
            self.budadjust.add_fact(fact.base, fact.pick, fact.fopen, fact.fnigh, True)
        for fact in self.boss_facts.values():
            self.budadjust.add_fact(fact.base, fact.pick, fact.fopen, fact.fnigh, True)

    def _set_acct_mandate_ledger(self):
        self.budadjust.set_fund_pool(self.mandate)
        acct_agenda_give_ledger = get_acct_mandate_ledger(self.budadjust, True)
        self._acct_mandate_ledger = acct_agenda_give_ledger

    def calc_acct_mandate_ledger(self):
        self._reason_bases = self.budadjust.get_reason_bases()
        self.filter_facts_by_reason_bases()
        self.set_budadjust_facts()
        self._set_acct_mandate_ledger()

    def get_dict(self) -> dict[str, str | dict]:
        return {
            "ancestors": self.ancestors,
            "event_int": self.event_int,
            "celldepth": self.celldepth,
            "deal_owner_name": self.deal_owner_name,
            "penny": self.penny,
            "quota": self.quota,
            "budadjust": self.budadjust.get_dict(),
            "budevent_facts": get_dict_from_factunits(self.budevent_facts),
            "found_facts": get_dict_from_factunits(self.found_facts),
            "boss_facts": get_dict_from_factunits(self.boss_facts),
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def cellunit_shop(
    deal_owner_name: OwnerName,
    ancestors: list[OwnerName] = None,
    event_int: EventInt = None,
    celldepth: int = None,
    penny: PennyNum = None,
    quota: float = None,
    budadjust: BudUnit = None,
    budevent_facts: dict[RoadUnit, FactUnit] = None,
    found_facts: dict[RoadUnit, FactUnit] = None,
    boss_facts: dict[RoadUnit, FactUnit] = None,
    mandate: float = None,
) -> CellUnit:
    if quota is None:
        quota = CELLNODE_QUOTA_DEFAULT
    if mandate is None:
        mandate = CELLNODE_QUOTA_DEFAULT
    if budadjust is None:
        budadjust = budunit_shop(deal_owner_name)
    reason_bases = budadjust.get_reason_bases() if budadjust else set()
    if budadjust:
        budadjust = copy_deepcopy(budadjust)
        clear_factunits_from_bud(budadjust)

    return CellUnit(
        ancestors=get_empty_list_if_None(ancestors),
        event_int=event_int,
        celldepth=get_0_if_None(celldepth),
        deal_owner_name=deal_owner_name,
        penny=get_1_if_None(penny),
        quota=quota,
        mandate=mandate,
        budadjust=budadjust,
        budevent_facts=get_empty_dict_if_None(budevent_facts),
        found_facts=get_empty_dict_if_None(found_facts),
        boss_facts=get_empty_dict_if_None(boss_facts),
        _reason_bases=reason_bases,
        _acct_mandate_ledger={},
    )


def cellunit_get_from_dict(x_dict: dict) -> CellUnit:
    deal_owner_name = x_dict.get("deal_owner_name")
    ancestors = x_dict.get("ancestors")
    event_int = x_dict.get("event_int")
    celldepth = x_dict.get("celldepth")
    penny = x_dict.get("penny")
    quota = x_dict.get("quota")
    budadjust_dict = x_dict.get("budadjust")
    if budadjust_dict:
        budadjust_obj = budunit_get_from_dict(budadjust_dict)
    else:
        budadjust_obj = None
    budevent_fact_dict = get_empty_dict_if_None(x_dict.get("budevent_facts"))
    found_fact_dict = get_empty_dict_if_None(x_dict.get("found_facts"))
    boss_fact_dict = get_empty_dict_if_None(x_dict.get("boss_facts"))
    budevent_facts = factunits_get_from_dict(budevent_fact_dict)
    found_facts = factunits_get_from_dict(found_fact_dict)
    boss_facts = factunits_get_from_dict(boss_fact_dict)
    return cellunit_shop(
        deal_owner_name=deal_owner_name,
        ancestors=ancestors,
        event_int=event_int,
        celldepth=celldepth,
        penny=penny,
        quota=quota,
        budadjust=budadjust_obj,
        budevent_facts=budevent_facts,
        found_facts=found_facts,
        boss_facts=boss_facts,
    )


def create_child_cellunits(parent_cell: CellUnit) -> list[CellUnit]:
    parent_cell.calc_acct_mandate_ledger()
    x_list = []
    for child_owner_name in sorted(parent_cell._acct_mandate_ledger):
        child_mandate = parent_cell._acct_mandate_ledger.get(child_owner_name)
        if child_mandate > 0 and parent_cell.celldepth > 0:
            child_ancestors = copy_deepcopy(parent_cell.ancestors)
            child_ancestors.append(child_owner_name)
            boss_facts = factunits_get_from_dict(get_facts_dict(parent_cell.budadjust))
            child_cell = cellunit_shop(
                deal_owner_name=parent_cell.deal_owner_name,
                ancestors=child_ancestors,
                event_int=parent_cell.event_int,
                celldepth=parent_cell.celldepth - 1,
                penny=parent_cell.penny,
                mandate=child_mandate,
                boss_facts=boss_facts,
            )
            x_list.append(child_cell)
    return x_list


# TODO create tool that takes current cell, compares it to parent's generated child cell and takes only boss facts
