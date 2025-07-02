from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_empty_list_if_None,
    get_json_from_dict,
)
from src.a01_term_logic.term import EventInt, OwnerName, RopeTerm
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import FundNum, PennyNum
from src.a04_reason_logic.reason_plan import (
    FactUnit,
    factunits_get_from_dict,
    get_dict_from_factunits,
)
from src.a06_owner_logic.owner import (
    OwnerUnit,
    get_from_dict as ownerunit_get_from_dict,
    ownerunit_shop,
)
from src.a06_owner_logic.owner_tool import (
    clear_factunits_from_owner,
    get_acct_mandate_ledger,
    get_credit_ledger,
    get_owner_root_facts_dict as get_facts_dict,
)

CELLNODE_QUOTA_DEFAULT = 1000


@dataclass
class CellUnit:
    ancestors: list[OwnerName] = None
    event_int: EventInt = None
    celldepth: int = None
    bud_owner_name: OwnerName = None
    penny: PennyNum = None
    quota: float = None
    mandate: float = None
    owneradjust: OwnerUnit = None
    ownerevent_facts: dict[RopeTerm, FactUnit] = None
    found_facts: dict[RopeTerm, FactUnit] = None
    boss_facts: dict[RopeTerm, FactUnit] = None
    _reason_rcontexts: set[RopeTerm] = None
    _acct_mandate_ledger: dict[OwnerName, FundNum] = None

    def get_cell_owner_name(self) -> OwnerName:
        return self.bud_owner_name if self.ancestors == [] else self.ancestors[-1]

    def eval_ownerevent(self, x_owner: OwnerUnit):
        if not x_owner:
            self.owneradjust = None
            self.ownerevent_facts = {}
            self._reason_rcontexts = set()
        else:
            self._load_existing_ownerevent(x_owner)

    def _load_existing_ownerevent(self, x_owner: OwnerUnit):
        self._reason_rcontexts = x_owner.get_reason_rcontexts()
        self.ownerevent_facts = factunits_get_from_dict(get_facts_dict(x_owner))
        y_owner = copy_deepcopy(x_owner)
        clear_factunits_from_owner(y_owner)
        y_owner.settle_owner()
        self.owneradjust = y_owner

    def get_ownerevents_credit_ledger(self) -> dict[OwnerName, float]:
        return {} if self.owneradjust is None else get_credit_ledger(self.owneradjust)

    def get_ownerevents_quota_ledger(self) -> dict[OwnerName, float]:
        if not self.owneradjust:
            return None
        credit_ledger = self.get_ownerevents_credit_ledger()
        return allot_scale(credit_ledger, self.quota, self.penny)

    def set_ownerevent_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.ownerevent_facts = factunits_get_from_dict(fact_dict)

    def set_found_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.found_facts = factunits_get_from_dict(fact_dict)

    def set_boss_facts_from_other_facts(self):
        self.boss_facts = copy_deepcopy(self.ownerevent_facts)
        for x_fact in self.found_facts.values():
            self.boss_facts[x_fact.fcontext] = copy_deepcopy(x_fact)

    def add_other_facts_to_boss_facts(self):
        for x_fact in self.found_facts.values():
            if not self.boss_facts.get(x_fact.fcontext):
                self.boss_facts[x_fact.fcontext] = copy_deepcopy(x_fact)
        for x_fact in self.ownerevent_facts.values():
            if not self.boss_facts.get(x_fact.fcontext):
                self.boss_facts[x_fact.fcontext] = copy_deepcopy(x_fact)

    def filter_facts_by_reason_rcontexts(self):
        to_delete_ownerevent_fact_keys = set(self.ownerevent_facts.keys())
        to_delete_found_fact_keys = set(self.found_facts.keys())
        to_delete_boss_fact_keys = set(self.boss_facts.keys())
        to_delete_ownerevent_fact_keys.difference_update(self._reason_rcontexts)
        to_delete_found_fact_keys.difference_update(self._reason_rcontexts)
        to_delete_boss_fact_keys.difference_update(self._reason_rcontexts)
        for ownerevent_fact_key in to_delete_ownerevent_fact_keys:
            self.ownerevent_facts.pop(ownerevent_fact_key)
        for found_fact_key in to_delete_found_fact_keys:
            self.found_facts.pop(found_fact_key)
        for boss_fact_key in to_delete_boss_fact_keys:
            self.boss_facts.pop(boss_fact_key)

    def set_owneradjust_facts(self):
        for fact in self.ownerevent_facts.values():
            self.owneradjust.add_fact(
                fact.fcontext, fact.fstate, fact.fopen, fact.fnigh, True
            )
        for fact in self.found_facts.values():
            self.owneradjust.add_fact(
                fact.fcontext, fact.fstate, fact.fopen, fact.fnigh, True
            )
        for fact in self.boss_facts.values():
            self.owneradjust.add_fact(
                fact.fcontext, fact.fstate, fact.fopen, fact.fnigh, True
            )

    def _set_acct_mandate_ledger(self):
        self.owneradjust.set_fund_pool(self.mandate)
        self._acct_mandate_ledger = get_acct_mandate_ledger(self.owneradjust, True)

    def calc_acct_mandate_ledger(self):
        self._reason_rcontexts = self.owneradjust.get_reason_rcontexts()
        self.filter_facts_by_reason_rcontexts()
        self.set_owneradjust_facts()
        self._set_acct_mandate_ledger()

    def get_dict(self) -> dict[str, str | dict]:
        if not self.owneradjust:
            self.owneradjust = ownerunit_shop(self.get_cell_owner_name())
        return {
            "ancestors": self.ancestors,
            "event_int": self.event_int,
            "celldepth": self.celldepth,
            "bud_owner_name": self.bud_owner_name,
            "penny": self.penny,
            "quota": self.quota,
            "mandate": self.mandate,
            "owneradjust": self.owneradjust.get_dict(),
            "ownerevent_facts": get_dict_from_factunits(self.ownerevent_facts),
            "found_facts": get_dict_from_factunits(self.found_facts),
            "boss_facts": get_dict_from_factunits(self.boss_facts),
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def cellunit_shop(
    bud_owner_name: OwnerName,
    ancestors: list[OwnerName] = None,
    event_int: EventInt = None,
    celldepth: int = None,
    penny: PennyNum = None,
    quota: float = None,
    owneradjust: OwnerUnit = None,
    ownerevent_facts: dict[RopeTerm, FactUnit] = None,
    found_facts: dict[RopeTerm, FactUnit] = None,
    boss_facts: dict[RopeTerm, FactUnit] = None,
    mandate: float = None,
) -> CellUnit:
    if quota is None:
        quota = CELLNODE_QUOTA_DEFAULT
    if mandate is None:
        mandate = CELLNODE_QUOTA_DEFAULT
    if owneradjust is None:
        owneradjust = ownerunit_shop(bud_owner_name)
    reason_rcontexts = owneradjust.get_reason_rcontexts() if owneradjust else set()
    if owneradjust:
        owneradjust = copy_deepcopy(owneradjust)
        clear_factunits_from_owner(owneradjust)

    return CellUnit(
        ancestors=get_empty_list_if_None(ancestors),
        event_int=event_int,
        celldepth=get_0_if_None(celldepth),
        bud_owner_name=bud_owner_name,
        penny=get_1_if_None(penny),
        quota=quota,
        mandate=mandate,
        owneradjust=owneradjust,
        ownerevent_facts=get_empty_dict_if_None(ownerevent_facts),
        found_facts=get_empty_dict_if_None(found_facts),
        boss_facts=get_empty_dict_if_None(boss_facts),
        _reason_rcontexts=reason_rcontexts,
        _acct_mandate_ledger={},
    )


def cellunit_get_from_dict(x_dict: dict) -> CellUnit:
    bud_owner_name = x_dict.get("bud_owner_name")
    ancestors = x_dict.get("ancestors")
    event_int = x_dict.get("event_int")
    celldepth = x_dict.get("celldepth")
    penny = x_dict.get("penny")
    quota = x_dict.get("quota")
    mandate = x_dict.get("mandate")
    owneradjust_dict = x_dict.get("owneradjust")
    if owneradjust_dict:
        owneradjust_obj = ownerunit_get_from_dict(owneradjust_dict)
    else:
        owneradjust_obj = None
    ownerevent_fact_dict = get_empty_dict_if_None(x_dict.get("ownerevent_facts"))
    found_fact_dict = get_empty_dict_if_None(x_dict.get("found_facts"))
    boss_fact_dict = get_empty_dict_if_None(x_dict.get("boss_facts"))
    ownerevent_facts = factunits_get_from_dict(ownerevent_fact_dict)
    found_facts = factunits_get_from_dict(found_fact_dict)
    boss_facts = factunits_get_from_dict(boss_fact_dict)
    return cellunit_shop(
        bud_owner_name=bud_owner_name,
        ancestors=ancestors,
        event_int=event_int,
        celldepth=celldepth,
        penny=penny,
        quota=quota,
        owneradjust=owneradjust_obj,
        ownerevent_facts=ownerevent_facts,
        found_facts=found_facts,
        boss_facts=boss_facts,
        mandate=mandate,
    )


def create_child_cellunits(parent_cell: CellUnit) -> list[CellUnit]:
    parent_cell.calc_acct_mandate_ledger()
    x_list = []
    for child_owner_name in sorted(parent_cell._acct_mandate_ledger):
        child_mandate = parent_cell._acct_mandate_ledger.get(child_owner_name)
        if child_mandate > 0 and parent_cell.celldepth > 0:
            child_ancestors = copy_deepcopy(parent_cell.ancestors)
            child_ancestors.append(child_owner_name)
            boss_facts = factunits_get_from_dict(
                get_facts_dict(parent_cell.owneradjust)
            )
            child_cell = cellunit_shop(
                bud_owner_name=parent_cell.bud_owner_name,
                ancestors=child_ancestors,
                event_int=parent_cell.event_int,
                celldepth=parent_cell.celldepth - 1,
                penny=parent_cell.penny,
                mandate=child_mandate,
                boss_facts=boss_facts,
            )
            x_list.append(child_cell)
    return x_list
