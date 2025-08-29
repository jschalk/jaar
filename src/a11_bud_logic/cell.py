from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_empty_list_if_None,
    get_json_from_dict,
)
from src.a01_term_logic.term import BeliefName, EventInt, RopeTerm
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import FundNum, PennyNum
from src.a04_reason_logic.reason import (
    FactUnit,
    factunits_get_from_dict,
    get_dict_from_factunits,
)
from src.a06_belief_logic.belief_main import (
    BeliefUnit,
    beliefunit_shop,
    get_from_dict as beliefunit_get_from_dict,
)
from src.a06_belief_logic.belief_tool import (
    clear_factunits_from_belief,
    get_belief_root_facts_dict as get_facts_dict,
    get_credit_ledger,
    get_voice_mandate_ledger,
)

CELLNODE_QUOTA_DEFAULT = 1000


@dataclass
class CellUnit:
    ancestors: list[BeliefName] = None
    event_int: EventInt = None
    celldepth: int = None
    bud_belief_name: BeliefName = None
    penny: PennyNum = None
    quota: float = None
    mandate: float = None
    beliefadjust: BeliefUnit = None
    beliefevent_facts: dict[RopeTerm, FactUnit] = None
    found_facts: dict[RopeTerm, FactUnit] = None
    boss_facts: dict[RopeTerm, FactUnit] = None
    reason_contexts: set[RopeTerm] = None
    _voice_mandate_ledger: dict[BeliefName, FundNum] = None

    def get_cell_belief_name(self) -> BeliefName:
        return self.bud_belief_name if self.ancestors == [] else self.ancestors[-1]

    def eval_beliefevent(self, x_belief: BeliefUnit):
        if not x_belief:
            self.beliefadjust = None
            self.beliefevent_facts = {}
            self.reason_contexts = set()
        else:
            self._load_existing_beliefevent(x_belief)

    def _load_existing_beliefevent(self, x_belief: BeliefUnit):
        self.reason_contexts = x_belief.get_reason_contexts()
        self.beliefevent_facts = factunits_get_from_dict(get_facts_dict(x_belief))
        y_belief = copy_deepcopy(x_belief)
        clear_factunits_from_belief(y_belief)
        y_belief.cash_out()
        self.beliefadjust = y_belief

    def get_beliefevents_credit_ledger(self) -> dict[BeliefName, float]:
        return {} if self.beliefadjust is None else get_credit_ledger(self.beliefadjust)

    def get_beliefevents_quota_ledger(self) -> dict[BeliefName, float]:
        if not self.beliefadjust:
            return None
        credit_ledger = self.get_beliefevents_credit_ledger()
        return allot_scale(credit_ledger, self.quota, self.penny)

    def set_beliefevent_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.beliefevent_facts = factunits_get_from_dict(fact_dict)

    def set_found_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.found_facts = factunits_get_from_dict(fact_dict)

    def set_boss_facts_from_other_facts(self):
        self.boss_facts = copy_deepcopy(self.beliefevent_facts)
        for x_fact in self.found_facts.values():
            self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def add_other_facts_to_boss_facts(self):
        for x_fact in self.found_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)
        for x_fact in self.beliefevent_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def filter_facts_by_reason_contexts(self):
        to_delete_beliefevent_fact_keys = set(self.beliefevent_facts.keys())
        to_delete_found_fact_keys = set(self.found_facts.keys())
        to_delete_boss_fact_keys = set(self.boss_facts.keys())
        to_delete_beliefevent_fact_keys.difference_update(self.reason_contexts)
        to_delete_found_fact_keys.difference_update(self.reason_contexts)
        to_delete_boss_fact_keys.difference_update(self.reason_contexts)
        for beliefevent_fact_key in to_delete_beliefevent_fact_keys:
            self.beliefevent_facts.pop(beliefevent_fact_key)
        for found_fact_key in to_delete_found_fact_keys:
            self.found_facts.pop(found_fact_key)
        for boss_fact_key in to_delete_boss_fact_keys:
            self.boss_facts.pop(boss_fact_key)

    def set_beliefadjust_facts(self):
        for fact in self.beliefevent_facts.values():
            self.beliefadjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )
        for fact in self.found_facts.values():
            self.beliefadjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )
        for fact in self.boss_facts.values():
            self.beliefadjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )

    def _set_voice_mandate_ledger(self):
        self.beliefadjust.set_fund_pool(self.mandate)
        self._voice_mandate_ledger = get_voice_mandate_ledger(self.beliefadjust, True)

    def calc_voice_mandate_ledger(self):
        self.reason_contexts = self.beliefadjust.get_reason_contexts()
        self.filter_facts_by_reason_contexts()
        self.set_beliefadjust_facts()
        self._set_voice_mandate_ledger()

    def to_dict(self) -> dict[str, str | dict]:
        if not self.beliefadjust:
            self.beliefadjust = beliefunit_shop(self.get_cell_belief_name())
        return {
            "ancestors": self.ancestors,
            "event_int": self.event_int,
            "celldepth": self.celldepth,
            "bud_belief_name": self.bud_belief_name,
            "penny": self.penny,
            "quota": self.quota,
            "mandate": self.mandate,
            "beliefadjust": self.beliefadjust.to_dict(),
            "beliefevent_facts": get_dict_from_factunits(self.beliefevent_facts),
            "found_facts": get_dict_from_factunits(self.found_facts),
            "boss_facts": get_dict_from_factunits(self.boss_facts),
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.to_dict())


def cellunit_shop(
    bud_belief_name: BeliefName,
    ancestors: list[BeliefName] = None,
    event_int: EventInt = None,
    celldepth: int = None,
    penny: PennyNum = None,
    quota: float = None,
    beliefadjust: BeliefUnit = None,
    beliefevent_facts: dict[RopeTerm, FactUnit] = None,
    found_facts: dict[RopeTerm, FactUnit] = None,
    boss_facts: dict[RopeTerm, FactUnit] = None,
    mandate: float = None,
) -> CellUnit:
    if quota is None:
        quota = CELLNODE_QUOTA_DEFAULT
    if mandate is None:
        mandate = CELLNODE_QUOTA_DEFAULT
    if beliefadjust is None:
        beliefadjust = beliefunit_shop(bud_belief_name)
    reason_contexts = beliefadjust.get_reason_contexts() if beliefadjust else set()
    if beliefadjust:
        beliefadjust = copy_deepcopy(beliefadjust)
        clear_factunits_from_belief(beliefadjust)

    return CellUnit(
        ancestors=get_empty_list_if_None(ancestors),
        event_int=event_int,
        celldepth=get_0_if_None(celldepth),
        bud_belief_name=bud_belief_name,
        penny=get_1_if_None(penny),
        quota=quota,
        mandate=mandate,
        beliefadjust=beliefadjust,
        beliefevent_facts=get_empty_dict_if_None(beliefevent_facts),
        found_facts=get_empty_dict_if_None(found_facts),
        boss_facts=get_empty_dict_if_None(boss_facts),
        reason_contexts=reason_contexts,
        _voice_mandate_ledger={},
    )


def cellunit_get_from_dict(x_dict: dict) -> CellUnit:
    bud_belief_name = x_dict.get("bud_belief_name")
    ancestors = x_dict.get("ancestors")
    event_int = x_dict.get("event_int")
    celldepth = x_dict.get("celldepth")
    penny = x_dict.get("penny")
    quota = x_dict.get("quota")
    mandate = x_dict.get("mandate")
    beliefadjust_dict = x_dict.get("beliefadjust")
    if beliefadjust_dict:
        beliefadjust_obj = beliefunit_get_from_dict(beliefadjust_dict)
    else:
        beliefadjust_obj = None
    beliefevent_fact_dict = get_empty_dict_if_None(x_dict.get("beliefevent_facts"))
    found_fact_dict = get_empty_dict_if_None(x_dict.get("found_facts"))
    boss_fact_dict = get_empty_dict_if_None(x_dict.get("boss_facts"))
    beliefevent_facts = factunits_get_from_dict(beliefevent_fact_dict)
    found_facts = factunits_get_from_dict(found_fact_dict)
    boss_facts = factunits_get_from_dict(boss_fact_dict)
    return cellunit_shop(
        bud_belief_name=bud_belief_name,
        ancestors=ancestors,
        event_int=event_int,
        celldepth=celldepth,
        penny=penny,
        quota=quota,
        beliefadjust=beliefadjust_obj,
        beliefevent_facts=beliefevent_facts,
        found_facts=found_facts,
        boss_facts=boss_facts,
        mandate=mandate,
    )


def create_child_cellunits(parent_cell: CellUnit) -> list[CellUnit]:
    parent_cell.calc_voice_mandate_ledger()
    x_list = []
    for child_belief_name in sorted(parent_cell._voice_mandate_ledger):
        child_mandate = parent_cell._voice_mandate_ledger.get(child_belief_name)
        if child_mandate > 0 and parent_cell.celldepth > 0:
            child_ancestors = copy_deepcopy(parent_cell.ancestors)
            child_ancestors.append(child_belief_name)
            boss_facts = factunits_get_from_dict(
                get_facts_dict(parent_cell.beliefadjust)
            )
            child_cell = cellunit_shop(
                bud_belief_name=parent_cell.bud_belief_name,
                ancestors=child_ancestors,
                event_int=parent_cell.event_int,
                celldepth=parent_cell.celldepth - 1,
                penny=parent_cell.penny,
                mandate=child_mandate,
                boss_facts=boss_facts,
            )
            x_list.append(child_cell)
    return x_list
