from dataclasses import dataclass
from src.ch01_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_positive_int,
    set_in_nested_dict,
)
from src.ch01_data_toolbox.file_toolbox import save_file
from src.ch03_finance_logic.allot import allot_scale
from src.ch11_bud_logic._ref.ch11_semantic_types import BeliefName, VoiceName
from src.ch12_hub_toolbox.hubunit import HubUnit
from src.ch14_keep_logic.rivercycle import (
    RiverGrade,
    create_init_rivercycle,
    create_next_rivercycle,
    rivergrade_shop,
)


@dataclass
class RiverRun:
    hubunit: HubUnit = None
    number: int = None
    keep_credorledgers: dict[BeliefName : dict[VoiceName, float]] = None
    tax_dues: dict[VoiceName, float] = None
    cycle_max: int = None
    # calculated fields
    _grants: dict[VoiceName, float] = None
    _tax_yields: dict[VoiceName, float] = None
    _tax_got_prev: float = None
    _tax_got_curr: float = None
    _cycle_count: int = None
    _cycle_chargeees_prev: set = None
    _cycle_chargeees_curr: set = None
    _debtor_count: int = None
    _credor_count: int = None
    _rivergrades: dict[VoiceName, RiverGrade] = None

    def set_cycle_max(self, x_cycle_max: int):
        self.cycle_max = get_positive_int(x_cycle_max)

    def set_keep_credorledger(
        self,
        belief_name: BeliefName,
        voice_name: VoiceName,
        credit_ledger: float,
    ):
        set_in_nested_dict(
            x_dict=self.keep_credorledgers,
            x_keylist=[belief_name, voice_name],
            x_obj=credit_ledger,
        )

    def delete_keep_credorledgers_belief(self, belief_name: BeliefName):
        self.keep_credorledgers.pop(belief_name)

    def get_all_keep_credorledger_voice_names(self):
        x_set = set()
        for belief_name, belief_dict in self.keep_credorledgers.items():
            if belief_name not in x_set:
                x_set.add(belief_name)
            for voice_name in belief_dict.keys():
                if voice_name not in x_set:
                    x_set.add(voice_name)
        return x_set

    def levy_tax_dues(self, cycleledger: tuple[dict[VoiceName, float], float]):
        delete_from_cycleledger = []
        tax_got_total = 0
        for chargeee, chargeee_amount in cycleledger.items():
            if self.voice_has_tax_due(chargeee):
                excess_chargeer_points, tax_got = self.levy_tax_due(
                    chargeee, chargeee_amount
                )
                tax_got_total += tax_got
                if excess_chargeer_points == 0:
                    delete_from_cycleledger.append(chargeee)
                else:
                    cycleledger[chargeee] = excess_chargeer_points

        for chargeee_to_delete in delete_from_cycleledger:
            cycleledger.pop(chargeee_to_delete)
        return cycleledger, tax_got_total

    def set_voice_tax_due(self, x_voice_name: VoiceName, tax_due: float):
        self.tax_dues[x_voice_name] = tax_due

    def tax_dues_unpaid(self) -> bool:
        return len(self.tax_dues) != 0

    def set_tax_dues(self, debtorledger: dict[VoiceName, float]):
        x_amount = self.hubunit.keep_point_magnitude
        self.tax_dues = allot_scale(debtorledger, x_amount, self.hubunit.money_grain)

    def voice_has_tax_due(self, x_voice_name: VoiceName) -> bool:
        return self.tax_dues.get(x_voice_name) is not None

    def get_voice_tax_due(self, x_voice_name: VoiceName) -> float:
        x_tax_due = self.tax_dues.get(x_voice_name)
        return 0 if x_tax_due is None else x_tax_due

    def delete_tax_due(self, x_voice_name: VoiceName):
        self.tax_dues.pop(x_voice_name)

    def levy_tax_due(self, x_voice_name: VoiceName, chargeer_points: float) -> float:
        if self.voice_has_tax_due(x_voice_name) is False:
            return chargeer_points, 0
        x_tax_due = self.get_voice_tax_due(x_voice_name)
        if x_tax_due > chargeer_points:
            left_over_charge = x_tax_due - chargeer_points
            self.set_voice_tax_due(x_voice_name, left_over_charge)
            self.add_voice_tax_yield(x_voice_name, chargeer_points)
            return 0, chargeer_points
        else:
            self.delete_tax_due(x_voice_name)
            self.add_voice_tax_yield(x_voice_name, x_tax_due)
            return chargeer_points - x_tax_due, x_tax_due

    def get_ledger_dict(self) -> dict[VoiceName, float]:
        return self.tax_dues

    def set_voice_tax_yield(self, x_voice_name: VoiceName, tax_yield: float):
        self._tax_yields[x_voice_name] = tax_yield

    def tax_yields_is_empty(self) -> bool:
        return len(self._tax_yields) == 0

    def reset_tax_yields(self):
        self._tax_yields = {}

    def voice_has_tax_yield(self, x_voice_name: VoiceName) -> bool:
        return self._tax_yields.get(x_voice_name) is not None

    def get_voice_tax_yield(self, x_voice_name: VoiceName) -> float:
        x_tax_yield = self._tax_yields.get(x_voice_name)
        return 0 if x_tax_yield is None else x_tax_yield

    def delete_tax_yield(self, x_voice_name: VoiceName):
        self._tax_yields.pop(x_voice_name)

    def add_voice_tax_yield(self, x_voice_name: VoiceName, x_tax_yield: float):
        if self.voice_has_tax_yield(x_voice_name):
            x_tax_yield = self.get_voice_tax_yield(x_voice_name) + x_tax_yield
        self.set_voice_tax_yield(x_voice_name, x_tax_yield)

    def get_rivergrade(self, voice_name: VoiceName) -> RiverGrade:
        return self._rivergrades.get(voice_name)

    def _rivergrades_is_empty(self) -> bool:
        return self._rivergrades == {}

    def rivergrade_exists(self, voice_name: VoiceName) -> bool:
        return self._rivergrades.get(voice_name) is not None

    def _get_voice_grant(self, voice_name: VoiceName) -> float:
        return get_0_if_None(self._grants.get(voice_name))

    def set_initial_rivergrade(self, voice_name: VoiceName):
        x_rivergrade = rivergrade_shop(self.hubunit, voice_name, self.number)
        x_rivergrade.debtor_count = self._debtor_count
        x_rivergrade.credor_count = self._credor_count
        x_rivergrade.grant_amount = self._get_voice_grant(voice_name)
        self._rivergrades[voice_name] = x_rivergrade

    def set_all_initial_rivergrades(self):
        self._rivergrades = {}
        all_voice_names = self.get_all_keep_credorledger_voice_names()
        for voice_name in all_voice_names:
            self.set_initial_rivergrade(voice_name)

    def _set_post_loop_rivergrade_attrs(self):
        for x_voice_name, voice_rivergrade in self._rivergrades.items():
            tax_due_leftover = self.get_voice_tax_due(x_voice_name)
            tax_due_paid = self.get_voice_tax_yield(x_voice_name)
            voice_rivergrade.set_tax_bill_amount(tax_due_paid + tax_due_leftover)
            voice_rivergrade.set_tax_paid_amount(tax_due_paid)

    def calc_metrics(self):
        self._set_debtor_count_credor_count()
        self._set_grants()
        self.set_all_initial_rivergrades()

        self._cycle_count = 0
        x_rivercyle = create_init_rivercycle(self.hubunit, self.keep_credorledgers)
        x_cyclelegder = x_rivercyle.create_cylceledger()
        self._cycle_chargeees_curr = set(x_cyclelegder.keys())
        x_cyclelegder, tax_got_curr = self.levy_tax_dues(x_cyclelegder)
        self._set_tax_got_attrs(tax_got_curr)

        while self.cycle_max > self._cycle_count and self.cycles_vary():
            x_rivercyle = create_next_rivercycle(x_rivercyle, x_cyclelegder)
            x_cyclelegder, tax_got_curr = self.levy_tax_dues(x_cyclelegder)

            self._set_tax_got_attrs(tax_got_curr)
            self._cycle_chargeees_prev = self._cycle_chargeees_curr
            self._cycle_chargeees_curr = set(x_cyclelegder.keys())
            self._cycle_count += 1

        self._set_post_loop_rivergrade_attrs()

    def _set_debtor_count_credor_count(self):
        tax_dues_voices = set(self.tax_dues.keys())
        tax_yields_voices = set(self._tax_yields.keys())
        self._debtor_count = len(tax_dues_voices.union(tax_yields_voices))
        self._credor_count = len(self.keep_credorledgers.get(self.hubunit.belief_name))

    def _set_grants(self):
        grant_credorledger = self.keep_credorledgers.get(self.hubunit.belief_name)
        self._grants = allot_scale(
            ledger=grant_credorledger,
            scale_number=self.hubunit.keep_point_magnitude,
            grain_unit=self.hubunit.money_grain,
        )

    def _save_rivergrade_file(self, voice_name: VoiceName):
        rivergrade = self.get_rivergrade(voice_name)
        grade_path = self.hubunit.grade_path(voice_name)
        save_file(grade_path, None, rivergrade.get_json())

    def save_rivergrade_files(self):
        for rivergrade_voice in self._rivergrades.keys():
            self._save_rivergrade_file(rivergrade_voice)

    def _cycle_chargeees_vary(self) -> bool:
        return self._cycle_chargeees_prev != self._cycle_chargeees_curr

    def _set_tax_got_attrs(self, x_tax_got_curr: float):
        self._tax_got_prev = self._tax_got_curr
        self._tax_got_curr = x_tax_got_curr

    def _tax_gotten(self) -> bool:
        return max(self._tax_got_prev, self._tax_got_curr) > 0

    def cycles_vary(self) -> bool:
        return self._tax_gotten() or self._cycle_chargeees_vary()


def riverrun_shop(
    hubunit: HubUnit,
    number: int = None,
    keep_credorledgers: dict[BeliefName : dict[VoiceName, float]] = None,
    tax_dues: dict[VoiceName, float] = None,
    cycle_max: int = None,
):
    x_riverun = RiverRun(
        hubunit=hubunit,
        number=get_0_if_None(number),
        keep_credorledgers=get_empty_dict_if_None(keep_credorledgers),
        tax_dues=get_empty_dict_if_None(tax_dues),
        _rivergrades={},
        _grants={},
        _tax_yields={},
    )
    x_riverun._cycle_count = 0
    x_riverun._cycle_chargeees_prev = set()
    x_riverun._cycle_chargeees_curr = set()
    x_riverun._tax_got_prev = 0
    x_riverun._tax_got_curr = 0
    if cycle_max is None:
        cycle_max = 10
    x_riverun.set_cycle_max(cycle_max)
    return x_riverun
