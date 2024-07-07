from src._instrument.file import save_file
from src._instrument.python import (
    get_empty_dict_if_none,
    get_positive_int,
    get_0_if_None,
    place_obj_in_dict,
)
from src._road.jaar_config import get_json_filename
from src._road.finance import allot_scale
from src._road.road import CharID, OwnerID
from src.money.rivercycle import (
    RiverGrade,
    rivergrade_shop,
    create_init_rivercycle,
    create_next_rivercycle,
)
from src.listen.hubunit import HubUnit
from dataclasses import dataclass


@dataclass
class RiverRun:
    hubunit: HubUnit = None
    number: int = None
    econ_credorledgers: dict[OwnerID : dict[CharID, float]] = None
    tax_dues: dict[CharID, float] = None
    cycle_max: int = None
    # calculated fields
    _grants: dict[CharID, float] = None
    _tax_yields: dict[CharID, float] = None
    _tax_got_prev: float = None
    _tax_got_curr: float = None
    _cycle_count: int = None
    _cycle_payees_prev: set = None
    _cycle_payees_curr: set = None
    _debtor_count: int = None
    _credor_count: int = None
    _rivergrades: dict[CharID, RiverGrade] = None

    def set_cycle_max(self, x_cycle_max: int):
        self.cycle_max = get_positive_int(x_cycle_max)

    def set_econ_credorledger(
        self, owner_id: OwnerID, char_id: CharID, char_credor_weight: float
    ):
        place_obj_in_dict(
            x_dict=self.econ_credorledgers,
            x_keylist=[owner_id, char_id],
            x_obj=char_credor_weight,
        )

    def delete_econ_credorledgers_owner(self, owner_id: OwnerID):
        self.econ_credorledgers.pop(owner_id)

    def get_all_econ_credorledger_char_ids(self):
        x_set = set()
        for owner_id, owner_dict in self.econ_credorledgers.items():
            if owner_id not in x_set:
                x_set.add(owner_id)
            for char_id in owner_dict.keys():
                if char_id not in x_set:
                    x_set.add(char_id)
        return x_set

    def levy_tax_dues(self, cycleledger: tuple[dict[CharID, float], float]):
        delete_from_cycleledger = []
        tax_got_total = 0
        for payee, payee_amount in cycleledger.items():
            if self.char_has_tax_due(payee):
                excess_payer_money, tax_got = self.levy_tax_due(payee, payee_amount)
                tax_got_total += tax_got
                if excess_payer_money == 0:
                    delete_from_cycleledger.append(payee)
                else:
                    cycleledger[payee] = excess_payer_money

        for payee_to_delete in delete_from_cycleledger:
            cycleledger.pop(payee_to_delete)
        return cycleledger, tax_got_total

    def set_char_tax_due(self, x_char_id: CharID, tax_due: float):
        self.tax_dues[x_char_id] = tax_due

    def tax_dues_unpaid(self) -> bool:
        return len(self.tax_dues) != 0

    def set_tax_dues(self, debtorledger: dict[CharID, float]):
        x_amount = self.hubunit.econ_money_magnitude
        self.tax_dues = allot_scale(debtorledger, x_amount, self.hubunit.penny)

    def char_has_tax_due(self, x_char_id: CharID) -> bool:
        return self.tax_dues.get(x_char_id) != None

    def get_char_tax_due(self, x_char_id: CharID) -> float:
        x_tax_due = self.tax_dues.get(x_char_id)
        return 0 if x_tax_due is None else x_tax_due

    def delete_tax_due(self, x_char_id: CharID):
        self.tax_dues.pop(x_char_id)

    def levy_tax_due(self, x_char_id: CharID, payer_money: float) -> float:
        if self.char_has_tax_due(x_char_id) == False:
            return payer_money, 0
        x_tax_due = self.get_char_tax_due(x_char_id)
        if x_tax_due > payer_money:
            left_over_pay = x_tax_due - payer_money
            self.set_char_tax_due(x_char_id, left_over_pay)
            self.add_char_tax_yield(x_char_id, payer_money)
            return 0, payer_money
        else:
            self.delete_tax_due(x_char_id)
            self.add_char_tax_yield(x_char_id, x_tax_due)
            return payer_money - x_tax_due, x_tax_due

    def get_ledger_dict(self) -> dict[CharID, float]:
        return self.tax_dues

    def set_char_tax_yield(self, x_char_id: CharID, tax_yield: float):
        self._tax_yields[x_char_id] = tax_yield

    def tax_yields_is_empty(self) -> bool:
        return len(self._tax_yields) == 0

    def reset_tax_yields(self):
        self._tax_yields = {}

    def char_has_tax_yield(self, x_char_id: CharID) -> bool:
        return self._tax_yields.get(x_char_id) != None

    def get_char_tax_yield(self, x_char_id: CharID) -> float:
        x_tax_yield = self._tax_yields.get(x_char_id)
        return 0 if x_tax_yield is None else x_tax_yield

    def delete_tax_yield(self, x_char_id: CharID):
        self._tax_yields.pop(x_char_id)

    def add_char_tax_yield(self, x_char_id: CharID, x_tax_yield: float):
        if self.char_has_tax_yield(x_char_id):
            x_tax_yield = self.get_char_tax_yield(x_char_id) + x_tax_yield
        self.set_char_tax_yield(x_char_id, x_tax_yield)

    def get_rivergrade(self, char_id: CharID) -> RiverGrade:
        return self._rivergrades.get(char_id)

    def _rivergrades_is_empty(self) -> bool:
        return self._rivergrades == {}

    def rivergrade_exists(self, char_id: CharID) -> bool:
        return self._rivergrades.get(char_id) != None

    def _get_char_grant(self, char_id: CharID) -> float:
        return get_0_if_None(self._grants.get(char_id))

    def set_initial_rivergrade(self, char_id: CharID):
        x_rivergrade = rivergrade_shop(self.hubunit, char_id, self.number)
        x_rivergrade.debtor_count = self._debtor_count
        x_rivergrade.credor_count = self._credor_count
        x_rivergrade.grant_amount = self._get_char_grant(char_id)
        self._rivergrades[char_id] = x_rivergrade

    def set_all_initial_rivergrades(self):
        self._rivergrades = {}
        all_char_ids = self.get_all_econ_credorledger_char_ids()
        for char_id in all_char_ids:
            self.set_initial_rivergrade(char_id)

    def _set_post_loop_rivergrade_attrs(self):
        for x_char_id, char_rivergrade in self._rivergrades.items():
            tax_due_remaining = self.get_char_tax_due(x_char_id)
            tax_due_paid = self.get_char_tax_yield(x_char_id)
            char_rivergrade.set_tax_bill_amount(tax_due_paid + tax_due_remaining)
            char_rivergrade.set_tax_paid_amount(tax_due_paid)

    def calc_metrics(self):
        self._set_debtor_count_credor_count()
        self._set_grants()
        self.set_all_initial_rivergrades()

        self._cycle_count = 0
        x_rivercyle = create_init_rivercycle(self.hubunit, self.econ_credorledgers)
        x_cyclelegder = x_rivercyle.create_cylceledger()
        self._cycle_payees_curr = set(x_cyclelegder.keys())
        x_cyclelegder, tax_got_curr = self.levy_tax_dues(x_cyclelegder)
        self._set_tax_got_attrs(tax_got_curr)

        while self.cycle_max > self._cycle_count and self.cycles_vary():
            x_rivercyle = create_next_rivercycle(x_rivercyle, x_cyclelegder)
            x_cyclelegder, tax_got_curr = self.levy_tax_dues(x_cyclelegder)

            self._set_tax_got_attrs(tax_got_curr)
            print(f"{self._tax_got_curr=} {self._tax_got_prev=}")
            self._cycle_payees_prev = self._cycle_payees_curr
            self._cycle_payees_curr = set(x_cyclelegder.keys())
            self._cycle_count += 1

        self._set_post_loop_rivergrade_attrs()

    def _set_debtor_count_credor_count(self):
        tax_dues_chars = set(self.tax_dues.keys())
        tax_yields_chars = set(self._tax_yields.keys())
        self._debtor_count = len(tax_dues_chars.union(tax_yields_chars))
        self._credor_count = len(self.econ_credorledgers.get(self.hubunit.owner_id))

    def _set_grants(self):
        grant_credorledger = self.econ_credorledgers.get(self.hubunit.owner_id)
        self._grants = allot_scale(
            ledger=grant_credorledger,
            scale_number=self.hubunit.econ_money_magnitude,
            grain_unit=self.hubunit.penny,
        )

    def _save_rivergrade_file(self, char_id: CharID):
        rivergrade = self.get_rivergrade(char_id)
        grade_path = self.hubunit.grade_path(char_id)
        grade_filename = get_json_filename(char_id)
        save_file(grade_path, grade_filename, rivergrade.get_json())

    def save_rivergrade_files(self):
        for rivergrade_char in self._rivergrades.keys():
            self._save_rivergrade_file(rivergrade_char)

    def _cycle_payees_vary(self) -> bool:
        return self._cycle_payees_prev != self._cycle_payees_curr

    def _set_tax_got_attrs(self, x_tax_got_curr: float):
        self._tax_got_prev = self._tax_got_curr
        self._tax_got_curr = x_tax_got_curr

    def _tax_gotten(self) -> bool:
        return max(self._tax_got_prev, self._tax_got_curr) > 0

    def cycles_vary(self) -> bool:
        return self._tax_gotten() or self._cycle_payees_vary()


def riverrun_shop(
    hubunit: HubUnit,
    number: int = None,
    econ_credorledgers: dict[OwnerID : dict[CharID, float]] = None,
    tax_dues: dict[CharID, float] = None,
    cycle_max: int = None,
):
    x_riverun = RiverRun(
        hubunit=hubunit,
        number=get_0_if_None(number),
        econ_credorledgers=get_empty_dict_if_none(econ_credorledgers),
        tax_dues=get_empty_dict_if_none(tax_dues),
        _rivergrades={},
        _grants={},
        _tax_yields={},
    )
    x_riverun._cycle_count = 0
    x_riverun._cycle_payees_prev = set()
    x_riverun._cycle_payees_curr = set()
    x_riverun._tax_got_prev = 0
    x_riverun._tax_got_curr = 0
    if cycle_max is None:
        cycle_max = 10
    x_riverun.set_cycle_max(cycle_max)
    return x_riverun
