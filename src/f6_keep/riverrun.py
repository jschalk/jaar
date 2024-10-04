from src.f0_instrument.file import save_file
from src.f0_instrument.dict_tool import (
    get_empty_dict_if_none,
    get_positive_int,
    get_0_if_None,
    set_in_nested_dict,
)
from src.f1_road.jaar_config import get_json_filename
from src.f1_road.finance import allot_scale
from src.f1_road.road import AcctID, OwnerID
from src.f6_keep.rivercycle import (
    RiverGrade,
    rivergrade_shop,
    create_init_rivercycle,
    create_next_rivercycle,
)
from src.f5_listen.hubunit import HubUnit
from dataclasses import dataclass


@dataclass
class RiverRun:
    hubunit: HubUnit = None
    number: int = None
    keep_credorledgers: dict[OwnerID : dict[AcctID, float]] = None
    tax_dues: dict[AcctID, float] = None
    cycle_max: int = None
    # calculated fields
    _grants: dict[AcctID, float] = None
    _tax_yields: dict[AcctID, float] = None
    _tax_got_prev: float = None
    _tax_got_curr: float = None
    _cycle_count: int = None
    _cycle_payees_prev: set = None
    _cycle_payees_curr: set = None
    _debtor_count: int = None
    _credor_count: int = None
    _rivergrades: dict[AcctID, RiverGrade] = None

    def set_cycle_max(self, x_cycle_max: int):
        self.cycle_max = get_positive_int(x_cycle_max)

    def set_keep_credorledger(
        self, owner_id: OwnerID, acct_id: AcctID, acct_credit_belief: float
    ):
        set_in_nested_dict(
            x_dict=self.keep_credorledgers,
            x_keylist=[owner_id, acct_id],
            x_obj=acct_credit_belief,
        )

    def delete_keep_credorledgers_owner(self, owner_id: OwnerID):
        self.keep_credorledgers.pop(owner_id)

    def get_all_keep_credorledger_acct_ids(self):
        x_set = set()
        for owner_id, owner_dict in self.keep_credorledgers.items():
            if owner_id not in x_set:
                x_set.add(owner_id)
            for acct_id in owner_dict.keys():
                if acct_id not in x_set:
                    x_set.add(acct_id)
        return x_set

    def levy_tax_dues(self, cycleledger: tuple[dict[AcctID, float], float]):
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

    def set_acct_tax_due(self, x_acct_id: AcctID, tax_due: float):
        self.tax_dues[x_acct_id] = tax_due

    def tax_dues_unpaid(self) -> bool:
        return len(self.tax_dues) != 0

    def set_tax_dues(self, debtorledger: dict[AcctID, float]):
        x_amount = self.hubunit.keep_point_magnitude
        self.tax_dues = allot_scale(debtorledger, x_amount, self.hubunit.penny)

    def acct_has_tax_due(self, x_acct_id: AcctID) -> bool:
        return self.tax_dues.get(x_acct_id) is not None

    def get_acct_tax_due(self, x_acct_id: AcctID) -> float:
        x_tax_due = self.tax_dues.get(x_acct_id)
        return 0 if x_tax_due is None else x_tax_due

    def delete_tax_due(self, x_acct_id: AcctID):
        self.tax_dues.pop(x_acct_id)

    def levy_tax_due(self, x_acct_id: AcctID, payer_points: float) -> float:
        if self.acct_has_tax_due(x_acct_id) is False:
            return payer_points, 0
        x_tax_due = self.get_acct_tax_due(x_acct_id)
        if x_tax_due > payer_points:
            left_over_pay = x_tax_due - payer_points
            self.set_acct_tax_due(x_acct_id, left_over_pay)
            self.add_acct_tax_yield(x_acct_id, payer_points)
            return 0, payer_points
        else:
            self.delete_tax_due(x_acct_id)
            self.add_acct_tax_yield(x_acct_id, x_tax_due)
            return payer_points - x_tax_due, x_tax_due

    def get_ledger_dict(self) -> dict[AcctID, float]:
        return self.tax_dues

    def set_acct_tax_yield(self, x_acct_id: AcctID, tax_yield: float):
        self._tax_yields[x_acct_id] = tax_yield

    def tax_yields_is_empty(self) -> bool:
        return len(self._tax_yields) == 0

    def reset_tax_yields(self):
        self._tax_yields = {}

    def acct_has_tax_yield(self, x_acct_id: AcctID) -> bool:
        return self._tax_yields.get(x_acct_id) is not None

    def get_acct_tax_yield(self, x_acct_id: AcctID) -> float:
        x_tax_yield = self._tax_yields.get(x_acct_id)
        return 0 if x_tax_yield is None else x_tax_yield

    def delete_tax_yield(self, x_acct_id: AcctID):
        self._tax_yields.pop(x_acct_id)

    def add_acct_tax_yield(self, x_acct_id: AcctID, x_tax_yield: float):
        if self.acct_has_tax_yield(x_acct_id):
            x_tax_yield = self.get_acct_tax_yield(x_acct_id) + x_tax_yield
        self.set_acct_tax_yield(x_acct_id, x_tax_yield)

    def get_rivergrade(self, acct_id: AcctID) -> RiverGrade:
        return self._rivergrades.get(acct_id)

    def _rivergrades_is_empty(self) -> bool:
        return self._rivergrades == {}

    def rivergrade_exists(self, acct_id: AcctID) -> bool:
        return self._rivergrades.get(acct_id) is not None

    def _get_acct_grant(self, acct_id: AcctID) -> float:
        return get_0_if_None(self._grants.get(acct_id))

    def set_initial_rivergrade(self, acct_id: AcctID):
        x_rivergrade = rivergrade_shop(self.hubunit, acct_id, self.number)
        x_rivergrade.debtor_count = self._debtor_count
        x_rivergrade.credor_count = self._credor_count
        x_rivergrade.grant_amount = self._get_acct_grant(acct_id)
        self._rivergrades[acct_id] = x_rivergrade

    def set_all_initial_rivergrades(self):
        self._rivergrades = {}
        all_acct_ids = self.get_all_keep_credorledger_acct_ids()
        for acct_id in all_acct_ids:
            self.set_initial_rivergrade(acct_id)

    def _set_post_loop_rivergrade_attrs(self):
        for x_acct_id, acct_rivergrade in self._rivergrades.items():
            tax_due_leftover = self.get_acct_tax_due(x_acct_id)
            tax_due_paid = self.get_acct_tax_yield(x_acct_id)
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
        self._credor_count = len(self.keep_credorledgers.get(self.hubunit.owner_id))

    def _set_grants(self):
        grant_credorledger = self.keep_credorledgers.get(self.hubunit.owner_id)
        self._grants = allot_scale(
            ledger=grant_credorledger,
            scale_number=self.hubunit.keep_point_magnitude,
            grain_unit=self.hubunit.penny,
        )

    def _save_rivergrade_file(self, acct_id: AcctID):
        rivergrade = self.get_rivergrade(acct_id)
        grade_path = self.hubunit.grade_path(acct_id)
        grade_filename = get_json_filename(acct_id)
        save_file(grade_path, grade_filename, rivergrade.get_json())

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
    keep_credorledgers: dict[OwnerID : dict[AcctID, float]] = None,
    tax_dues: dict[AcctID, float] = None,
    cycle_max: int = None,
):
    x_riverun = RiverRun(
        hubunit=hubunit,
        number=get_0_if_None(number),
        keep_credorledgers=get_empty_dict_if_none(keep_credorledgers),
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
