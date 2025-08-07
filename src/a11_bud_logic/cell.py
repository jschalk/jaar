from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_empty_list_if_None,
    get_json_from_dict,
)
from src.a01_term_logic.term import BelieverName, EventInt, RopeTerm
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import FundNum, PennyNum
from src.a04_reason_logic.reason_plan import (
    FactUnit,
    factunits_get_from_dict,
    get_dict_from_factunits,
)
from src.a06_believer_logic.believer_main import (
    BelieverUnit,
    believerunit_shop,
    get_from_dict as believerunit_get_from_dict,
)
from src.a06_believer_logic.believer_tool import (
    clear_factunits_from_believer,
    get_believer_root_facts_dict as get_facts_dict,
    get_credit_ledger,
    get_partner_mandate_ledger,
)

CELLNODE_QUOTA_DEFAULT = 1000


@dataclass
class CellUnit:
    ancestors: list[BelieverName] = None
    event_int: EventInt = None
    celldepth: int = None
    bud_believer_name: BelieverName = None
    penny: PennyNum = None
    quota: float = None
    mandate: float = None
    believeradjust: BelieverUnit = None
    believerevent_facts: dict[RopeTerm, FactUnit] = None
    found_facts: dict[RopeTerm, FactUnit] = None
    boss_facts: dict[RopeTerm, FactUnit] = None
    _reason_contexts: set[RopeTerm] = None
    _partner_mandate_ledger: dict[BelieverName, FundNum] = None

    def get_cell_believer_name(self) -> BelieverName:
        return self.bud_believer_name if self.ancestors == [] else self.ancestors[-1]

    def eval_believerevent(self, x_believer: BelieverUnit):
        if not x_believer:
            self.believeradjust = None
            self.believerevent_facts = {}
            self._reason_contexts = set()
        else:
            self._load_existing_believerevent(x_believer)

    def _load_existing_believerevent(self, x_believer: BelieverUnit):
        self._reason_contexts = x_believer.get_reason_contexts()
        self.believerevent_facts = factunits_get_from_dict(get_facts_dict(x_believer))
        y_believer = copy_deepcopy(x_believer)
        clear_factunits_from_believer(y_believer)
        y_believer.settle_believer()
        self.believeradjust = y_believer

    def get_believerevents_credit_ledger(self) -> dict[BelieverName, float]:
        return (
            {}
            if self.believeradjust is None
            else get_credit_ledger(self.believeradjust)
        )

    def get_believerevents_quota_ledger(self) -> dict[BelieverName, float]:
        if not self.believeradjust:
            return None
        credit_ledger = self.get_believerevents_credit_ledger()
        return allot_scale(credit_ledger, self.quota, self.penny)

    def set_believerevent_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.believerevent_facts = factunits_get_from_dict(fact_dict)

    def set_found_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.found_facts = factunits_get_from_dict(fact_dict)

    def set_boss_facts_from_other_facts(self):
        self.boss_facts = copy_deepcopy(self.believerevent_facts)
        for x_fact in self.found_facts.values():
            self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def add_other_facts_to_boss_facts(self):
        for x_fact in self.found_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)
        for x_fact in self.believerevent_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def filter_facts_by_reason_contexts(self):
        to_delete_believerevent_fact_keys = set(self.believerevent_facts.keys())
        to_delete_found_fact_keys = set(self.found_facts.keys())
        to_delete_boss_fact_keys = set(self.boss_facts.keys())
        to_delete_believerevent_fact_keys.difference_update(self._reason_contexts)
        to_delete_found_fact_keys.difference_update(self._reason_contexts)
        to_delete_boss_fact_keys.difference_update(self._reason_contexts)
        for believerevent_fact_key in to_delete_believerevent_fact_keys:
            self.believerevent_facts.pop(believerevent_fact_key)
        for found_fact_key in to_delete_found_fact_keys:
            self.found_facts.pop(found_fact_key)
        for boss_fact_key in to_delete_boss_fact_keys:
            self.boss_facts.pop(boss_fact_key)

    def set_believeradjust_facts(self):
        for fact in self.believerevent_facts.values():
            self.believeradjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )
        for fact in self.found_facts.values():
            self.believeradjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )
        for fact in self.boss_facts.values():
            self.believeradjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )

    def _set_partner_mandate_ledger(self):
        self.believeradjust.set_fund_pool(self.mandate)
        self._partner_mandate_ledger = get_partner_mandate_ledger(
            self.believeradjust, True
        )

    def calc_partner_mandate_ledger(self):
        self._reason_contexts = self.believeradjust.get_reason_contexts()
        self.filter_facts_by_reason_contexts()
        self.set_believeradjust_facts()
        self._set_partner_mandate_ledger()

    def to_dict(self) -> dict[str, str | dict]:
        if not self.believeradjust:
            self.believeradjust = believerunit_shop(self.get_cell_believer_name())
        return {
            "ancestors": self.ancestors,
            "event_int": self.event_int,
            "celldepth": self.celldepth,
            "bud_believer_name": self.bud_believer_name,
            "penny": self.penny,
            "quota": self.quota,
            "mandate": self.mandate,
            "believeradjust": self.believeradjust.to_dict(),
            "believerevent_facts": get_dict_from_factunits(self.believerevent_facts),
            "found_facts": get_dict_from_factunits(self.found_facts),
            "boss_facts": get_dict_from_factunits(self.boss_facts),
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.to_dict())


def cellunit_shop(
    bud_believer_name: BelieverName,
    ancestors: list[BelieverName] = None,
    event_int: EventInt = None,
    celldepth: int = None,
    penny: PennyNum = None,
    quota: float = None,
    believeradjust: BelieverUnit = None,
    believerevent_facts: dict[RopeTerm, FactUnit] = None,
    found_facts: dict[RopeTerm, FactUnit] = None,
    boss_facts: dict[RopeTerm, FactUnit] = None,
    mandate: float = None,
) -> CellUnit:
    if quota is None:
        quota = CELLNODE_QUOTA_DEFAULT
    if mandate is None:
        mandate = CELLNODE_QUOTA_DEFAULT
    if believeradjust is None:
        believeradjust = believerunit_shop(bud_believer_name)
    reason_contexts = believeradjust.get_reason_contexts() if believeradjust else set()
    if believeradjust:
        believeradjust = copy_deepcopy(believeradjust)
        clear_factunits_from_believer(believeradjust)

    return CellUnit(
        ancestors=get_empty_list_if_None(ancestors),
        event_int=event_int,
        celldepth=get_0_if_None(celldepth),
        bud_believer_name=bud_believer_name,
        penny=get_1_if_None(penny),
        quota=quota,
        mandate=mandate,
        believeradjust=believeradjust,
        believerevent_facts=get_empty_dict_if_None(believerevent_facts),
        found_facts=get_empty_dict_if_None(found_facts),
        boss_facts=get_empty_dict_if_None(boss_facts),
        _reason_contexts=reason_contexts,
        _partner_mandate_ledger={},
    )


def cellunit_get_from_dict(x_dict: dict) -> CellUnit:
    bud_believer_name = x_dict.get("bud_believer_name")
    ancestors = x_dict.get("ancestors")
    event_int = x_dict.get("event_int")
    celldepth = x_dict.get("celldepth")
    penny = x_dict.get("penny")
    quota = x_dict.get("quota")
    mandate = x_dict.get("mandate")
    believeradjust_dict = x_dict.get("believeradjust")
    if believeradjust_dict:
        believeradjust_obj = believerunit_get_from_dict(believeradjust_dict)
    else:
        believeradjust_obj = None
    believerevent_fact_dict = get_empty_dict_if_None(x_dict.get("believerevent_facts"))
    found_fact_dict = get_empty_dict_if_None(x_dict.get("found_facts"))
    boss_fact_dict = get_empty_dict_if_None(x_dict.get("boss_facts"))
    believerevent_facts = factunits_get_from_dict(believerevent_fact_dict)
    found_facts = factunits_get_from_dict(found_fact_dict)
    boss_facts = factunits_get_from_dict(boss_fact_dict)
    return cellunit_shop(
        bud_believer_name=bud_believer_name,
        ancestors=ancestors,
        event_int=event_int,
        celldepth=celldepth,
        penny=penny,
        quota=quota,
        believeradjust=believeradjust_obj,
        believerevent_facts=believerevent_facts,
        found_facts=found_facts,
        boss_facts=boss_facts,
        mandate=mandate,
    )


def create_child_cellunits(parent_cell: CellUnit) -> list[CellUnit]:
    parent_cell.calc_partner_mandate_ledger()
    x_list = []
    for child_believer_name in sorted(parent_cell._partner_mandate_ledger):
        child_mandate = parent_cell._partner_mandate_ledger.get(child_believer_name)
        if child_mandate > 0 and parent_cell.celldepth > 0:
            child_ancestors = copy_deepcopy(parent_cell.ancestors)
            child_ancestors.append(child_believer_name)
            boss_facts = factunits_get_from_dict(
                get_facts_dict(parent_cell.believeradjust)
            )
            child_cell = cellunit_shop(
                bud_believer_name=parent_cell.bud_believer_name,
                ancestors=child_ancestors,
                event_int=parent_cell.event_int,
                celldepth=parent_cell.celldepth - 1,
                penny=parent_cell.penny,
                mandate=child_mandate,
                boss_facts=boss_facts,
            )
            x_list.append(child_cell)
    return x_list
