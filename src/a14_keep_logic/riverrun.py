from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_positive_int,
    set_in_nested_dict,
)
from src.a00_data_toolbox.file_toolbox import save_file
from src.a01_term_logic.term import AcctName, OwnerName
from src.a02_finance_logic.allot import allot_scale
from src.a12_hub_tools.hubunit import HubUnit
from src.a14_keep_logic.rivercycle import (
    RiverGrade,
    create_init_rivercycle,
    create_next_rivercycle,
    rivergrade_shop,
)


@dataclass
class RiverRun:
    hubunit: HubUnit = None
    number: int = None
    keep_credorledgers: dict[OwnerName : dict[AcctName, float]] = None
    tax_dues: dict[AcctName, float] = None
    cycle_max: int = None
    # calculated fields
    _grants: dict[AcctName, float] = None
    _tax_yields: dict[AcctName, float] = None
    _tax_got_prev: float = None
    _tax_got_curr: float = None
    _cycle_count: int = None
    _cycle_payees_prev: set = None
    _cycle_payees_curr: set = None
    _debtor_count: int = None
    _credor_count: int = None
    _rivergrades: dict[AcctName, RiverGrade] = None

    def set_cycle_max(self, x_cycle_max: int):
        self.cycle_max = get_positive_int(x_cycle_max)

    def set_keep_credorledger(
        self, owner_name: OwnerName, acct_name: AcctName, acct_credit_belief: float
    ):
        set_in_nested_dict(
            x_dict=self.keep_credorledgers,
            x_keylist=[owner_name, acct_name],
            x_obj=acct_credit_belief,
        )

    def delete_keep_credorledgers_owner(self, owner_name: OwnerName):
        self.keep_credorledgers.pop(owner_name)

    def get_all_keep_credorledger_acct_names(self):
        x_set = set()
        for owner_name, owner_dict in self.keep_credorledgers.items():
            if owner_name not in x_set:
                x_set.add(owner_name)
            for acct_name in owner_dict.keys():
                if acct_name not in x_set:
                    x_set.add(acct_name)
        return x_set

    def levy_tax_dues(self, cycleledger: tuple[dict[AcctName, float], float]):
        delete_from_cycleledger = []
        tax_got_total = 0
        for payee, payee_amount in cycleledger.items():
            if self.acct_has_tax_due(payee):
                excess_payer_points, tax_got = self.levy_tax_due(payee, payee_amount)
                tax_got_total += tax_got
                if excess_payer_points == 0:
                    delete_from_cycleledger.append(payee)
                else:
                    cycleledger[payee] = excess_payer_points

        for payee_to_delete in delete_from_cycleledger:
            cycleledger.pop(payee_to_delete)
        return cycleledger, tax_got_total

    def set_acct_tax_due(self, x_acct_name: AcctName, tax_due: float):
        self.tax_dues[x_acct_name] = tax_due

    def tax_dues_unpaid(self) -> bool:
        return len(self.tax_dues) != 0

    def set_tax_dues(self, debtorledger: dict[AcctName, float]):
        x_amount = self.hubunit.keep_point_magnitude
        self.tax_dues = allot_scale(debtorledger, x_amount, self.hubunit.penny)

    def acct_has_tax_due(self, x_acct_name: AcctName) -> bool:
        return self.tax_dues.get(x_acct_name) is not None

    def get_acct_tax_due(self, x_acct_name: AcctName) -> float:
        x_tax_due = self.tax_dues.get(x_acct_name)
        return 0 if x_tax_due is None else x_tax_due

    def delete_tax_due(self, x_acct_name: AcctName):
        self.tax_dues.pop(x_acct_name)

    def levy_tax_due(self, x_acct_name: AcctName, payer_points: float) -> float:
        if self.acct_has_tax_due(x_acct_name) is False:
            return payer_points, 0
        x_tax_due = self.get_acct_tax_due(x_acct_name)
        if x_tax_due > payer_points:
            left_over_pay = x_tax_due - payer_points
            self.set_acct_tax_due(x_acct_name, left_over_pay)
            self.add_acct_tax_yield(x_acct_name, payer_points)
            return 0, payer_points
        else:
            self.delete_tax_due(x_acct_name)
            self.add_acct_tax_yield(x_acct_name, x_tax_due)
            return payer_points - x_tax_due, x_tax_due

    def get_ledger_dict(self) -> dict[AcctName, float]:
        return self.tax_dues

    def set_acct_tax_yield(self, x_acct_name: AcctName, tax_yield: float):
        self._tax_yields[x_acct_name] = tax_yield

    def tax_yields_is_empty(self) -> bool:
        return len(self._tax_yields) == 0

    def reset_tax_yields(self):
        self._tax_yields = {}

    def acct_has_tax_yield(self, x_acct_name: AcctName) -> bool:
        return self._tax_yields.get(x_acct_name) is not None

    def get_acct_tax_yield(self, x_acct_name: AcctName) -> float:
        x_tax_yield = self._tax_yields.get(x_acct_name)
        return 0 if x_tax_yield is None else x_tax_yield

    def delete_tax_yield(self, x_acct_name: AcctName):
        self._tax_yields.pop(x_acct_name)

    def add_acct_tax_yield(self, x_acct_name: AcctName, x_tax_yield: float):
        if self.acct_has_tax_yield(x_acct_name):
            x_tax_yield = self.get_acct_tax_yield(x_acct_name) + x_tax_yield
        self.set_acct_tax_yield(x_acct_name, x_tax_yield)

    def get_rivergrade(self, acct_name: AcctName) -> RiverGrade:
        return self._rivergrades.get(acct_name)

    def _rivergrades_is_empty(self) -> bool:
        return self._rivergrades == {}

    def rivergrade_exists(self, acct_name: AcctName) -> bool:
        return self._rivergrades.get(acct_name) is not None

    def _get_acct_grant(self, acct_name: AcctName) -> float:
        return get_0_if_None(self._grants.get(acct_name))

    def set_initial_rivergrade(self, acct_name: AcctName):
        x_rivergrade = rivergrade_shop(self.hubunit, acct_name, self.number)
        x_rivergrade.debtor_count = self._debtor_count
        x_rivergrade.credor_count = self._credor_count
        x_rivergrade.grant_amount = self._get_acct_grant(acct_name)
        self._rivergrades[acct_name] = x_rivergrade

    def set_all_initial_rivergrades(self):
        self._rivergrades = {}
        all_acct_names = self.get_all_keep_credorledger_acct_names()
        for acct_name in all_acct_names:
            self.set_initial_rivergrade(acct_name)

    def _set_post_loop_rivergrade_attrs(self):
        for x_acct_name, acct_rivergrade in self._rivergrades.items():
            tax_due_leftover = self.get_acct_tax_due(x_acct_name)
            tax_due_paid = self.get_acct_tax_yield(x_acct_name)
            acct_rivergrade.set_tax_bill_amount(tax_due_paid + tax_due_leftover)
            acct_rivergrade.set_tax_paid_amount(tax_due_paid)

    def calc_metrics(self):
        self._set_debtor_count_credor_count()
        self._set_grants()
        self.set_all_initial_rivergrades()

        self._cycle_count = 0
        x_rivercyle = create_init_rivercycle(self.hubunit, self.keep_credorledgers)
        x_cyclelegder = x_rivercyle.create_cylceledger()
        self._cycle_payees_curr = set(x_cyclelegder.keys())
        x_cyclelegder, tax_got_curr = self.levy_tax_dues(x_cyclelegder)
        self._set_tax_got_attrs(tax_got_curr)

        while self.cycle_max > self._cycle_count and self.cycles_vary():
            x_rivercyle = create_next_rivercycle(x_rivercyle, x_cyclelegder)
            x_cyclelegder, tax_got_curr = self.levy_tax_dues(x_cyclelegder)

            self._set_tax_got_attrs(tax_got_curr)
            self._cycle_payees_prev = self._cycle_payees_curr
            self._cycle_payees_curr = set(x_cyclelegder.keys())
            self._cycle_count += 1

        self._set_post_loop_rivergrade_attrs()

    def _set_debtor_count_credor_count(self):
        tax_dues_accts = set(self.tax_dues.keys())
        tax_yields_accts = set(self._tax_yields.keys())
        self._debtor_count = len(tax_dues_accts.union(tax_yields_accts))
        self._credor_count = len(self.keep_credorledgers.get(self.hubunit.owner_name))

    def _set_grants(self):
        grant_credorledger = self.keep_credorledgers.get(self.hubunit.owner_name)
        self._grants = allot_scale(
            ledger=grant_credorledger,
            scale_number=self.hubunit.keep_point_magnitude,
            grain_unit=self.hubunit.penny,
        )

    def _save_rivergrade_file(self, acct_name: AcctName):
        rivergrade = self.get_rivergrade(acct_name)
        grade_path = self.hubunit.grade_path(acct_name)
        save_file(grade_path, None, rivergrade.get_json())

    def save_rivergrade_files(self):
        for rivergrade_acct in self._rivergrades.keys():
            self._save_rivergrade_file(rivergrade_acct)

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
    keep_credorledgers: dict[OwnerName : dict[AcctName, float]] = None,
    tax_dues: dict[AcctName, float] = None,
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
    x_riverun._cycle_payees_prev = set()
    x_riverun._cycle_payees_curr = set()
    x_riverun._tax_got_prev = 0
    x_riverun._tax_got_curr = 0
    if cycle_max is None:
        cycle_max = 10
    x_riverun.set_cycle_max(cycle_max)
    return x_riverun
