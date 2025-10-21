from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch01_py.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_empty_list_if_None,
)
from src.ch02_allot.allot import allot_scale
from src.ch05_reason.reason import (
    FactUnit,
    get_dict_from_factunits,
    get_factunits_from_dict,
)
from src.ch07_belief_logic.belief_main import (
    BeliefUnit,
    beliefunit_shop,
    get_beliefunit_from_dict,
)
from src.ch07_belief_logic.belief_tool import (
    clear_factunits_from_belief,
    get_belief_root_facts_dict as get_facts_dict,
    get_credit_ledger,
    get_voice_mandate_ledger,
)
from src.ch11_bud._ref.ch11_semantic_types import (
    BeliefName,
    FundNum,
    ManaGrain,
    RopeTerm,
    SparkInt,
)

CELLNODE_QUOTA_DEFAULT = 1000


@dataclass
class CellUnit:
    ancestors: list[BeliefName] = None
    spark_num: SparkInt = None
    celldepth: int = None
    bud_belief_name: BeliefName = None
    mana_grain: ManaGrain = None
    quota: float = None
    mandate: float = None
    beliefadjust: BeliefUnit = None
    beliefspark_facts: dict[RopeTerm, FactUnit] = None
    found_facts: dict[RopeTerm, FactUnit] = None
    boss_facts: dict[RopeTerm, FactUnit] = None
    reason_contexts: set[RopeTerm] = None
    _voice_mandate_ledger: dict[BeliefName, FundNum] = None

    def get_cell_belief_name(self) -> BeliefName:
        return self.bud_belief_name if self.ancestors == [] else self.ancestors[-1]

    def eval_beliefspark(self, x_belief: BeliefUnit):
        if not x_belief:
            self.beliefadjust = None
            self.beliefspark_facts = {}
            self.reason_contexts = set()
        else:
            self._load_existing_beliefspark(x_belief)

    def _load_existing_beliefspark(self, x_belief: BeliefUnit):
        self.reason_contexts = x_belief.get_reason_contexts()
        self.beliefspark_facts = get_factunits_from_dict(get_facts_dict(x_belief))
        y_belief = copy_deepcopy(x_belief)
        clear_factunits_from_belief(y_belief)
        y_belief.cashout()
        self.beliefadjust = y_belief

    def get_beliefsparks_credit_ledger(self) -> dict[BeliefName, float]:
        return {} if self.beliefadjust is None else get_credit_ledger(self.beliefadjust)

    def get_beliefsparks_quota_ledger(self) -> dict[BeliefName, float]:
        if not self.beliefadjust:
            return None
        credit_ledger = self.get_beliefsparks_credit_ledger()
        return allot_scale(credit_ledger, self.quota, self.mana_grain)

    def set_beliefspark_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.beliefspark_facts = get_factunits_from_dict(fact_dict)

    def set_found_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.found_facts = get_factunits_from_dict(fact_dict)

    def set_boss_facts_from_other_facts(self):
        self.boss_facts = copy_deepcopy(self.beliefspark_facts)
        for x_fact in self.found_facts.values():
            self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def add_other_facts_to_boss_facts(self):
        for x_fact in self.found_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)
        for x_fact in self.beliefspark_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def filter_facts_by_reason_contexts(self):
        to_delete_beliefspark_fact_keys = set(self.beliefspark_facts.keys())
        to_delete_found_fact_keys = set(self.found_facts.keys())
        to_delete_boss_fact_keys = set(self.boss_facts.keys())
        to_delete_beliefspark_fact_keys.difference_update(self.reason_contexts)
        to_delete_found_fact_keys.difference_update(self.reason_contexts)
        to_delete_boss_fact_keys.difference_update(self.reason_contexts)
        for beliefspark_fact_key in to_delete_beliefspark_fact_keys:
            self.beliefspark_facts.pop(beliefspark_fact_key)
        for found_fact_key in to_delete_found_fact_keys:
            self.found_facts.pop(found_fact_key)
        for boss_fact_key in to_delete_boss_fact_keys:
            self.boss_facts.pop(boss_fact_key)

    def set_beliefadjust_facts(self):
        for fact in self.beliefspark_facts.values():
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
        """Returns dict that is serializable to JSON."""

        if not self.beliefadjust:
            self.beliefadjust = beliefunit_shop(self.get_cell_belief_name())
        return {
            "ancestors": self.ancestors,
            "spark_num": self.spark_num,
            "celldepth": self.celldepth,
            "bud_belief_name": self.bud_belief_name,
            "mana_grain": self.mana_grain,
            "quota": self.quota,
            "mandate": self.mandate,
            "beliefadjust": self.beliefadjust.to_dict(),
            "beliefspark_facts": get_dict_from_factunits(self.beliefspark_facts),
            "found_facts": get_dict_from_factunits(self.found_facts),
            "boss_facts": get_dict_from_factunits(self.boss_facts),
        }


def cellunit_shop(
    bud_belief_name: BeliefName,
    ancestors: list[BeliefName] = None,
    spark_num: SparkInt = None,
    celldepth: int = None,
    mana_grain: ManaGrain = None,
    quota: float = None,
    beliefadjust: BeliefUnit = None,
    beliefspark_facts: dict[RopeTerm, FactUnit] = None,
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
        spark_num=spark_num,
        celldepth=get_0_if_None(celldepth),
        bud_belief_name=bud_belief_name,
        mana_grain=get_1_if_None(mana_grain),
        quota=quota,
        mandate=mandate,
        beliefadjust=beliefadjust,
        beliefspark_facts=get_empty_dict_if_None(beliefspark_facts),
        found_facts=get_empty_dict_if_None(found_facts),
        boss_facts=get_empty_dict_if_None(boss_facts),
        reason_contexts=reason_contexts,
        _voice_mandate_ledger={},
    )


def cellunit_get_from_dict(x_dict: dict) -> CellUnit:
    bud_belief_name = x_dict.get("bud_belief_name")
    ancestors = x_dict.get("ancestors")
    spark_num = x_dict.get("spark_num")
    celldepth = x_dict.get("celldepth")
    mana_grain = x_dict.get("mana_grain")
    quota = x_dict.get("quota")
    mandate = x_dict.get("mandate")
    beliefadjust_dict = x_dict.get("beliefadjust")
    if beliefadjust_dict:
        beliefadjust_obj = get_beliefunit_from_dict(beliefadjust_dict)
    else:
        beliefadjust_obj = None
    beliefspark_fact_dict = get_empty_dict_if_None(x_dict.get("beliefspark_facts"))
    found_fact_dict = get_empty_dict_if_None(x_dict.get("found_facts"))
    boss_fact_dict = get_empty_dict_if_None(x_dict.get("boss_facts"))
    beliefspark_facts = get_factunits_from_dict(beliefspark_fact_dict)
    found_facts = get_factunits_from_dict(found_fact_dict)
    boss_facts = get_factunits_from_dict(boss_fact_dict)
    return cellunit_shop(
        bud_belief_name=bud_belief_name,
        ancestors=ancestors,
        spark_num=spark_num,
        celldepth=celldepth,
        mana_grain=mana_grain,
        quota=quota,
        beliefadjust=beliefadjust_obj,
        beliefspark_facts=beliefspark_facts,
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
            boss_facts = get_factunits_from_dict(
                get_facts_dict(parent_cell.beliefadjust)
            )
            child_cell = cellunit_shop(
                bud_belief_name=parent_cell.bud_belief_name,
                ancestors=child_ancestors,
                spark_num=parent_cell.spark_num,
                celldepth=parent_cell.celldepth - 1,
                mana_grain=parent_cell.mana_grain,
                mandate=child_mandate,
                boss_facts=boss_facts,
            )
            x_list.append(child_cell)
    return x_list
