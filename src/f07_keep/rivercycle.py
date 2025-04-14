from src.a00_data_toolboxs.dict_toolbox import (
    get_empty_dict_if_None,
    get_0_if_None,
    get_json_from_dict,
)
from src.a02_finance_toolboxs.allot import allot_scale
from src.a01_word_logic.road import AcctName, OwnerName
from src.a06_bud_logic.bud import BudUnit
from src.f06_listen.hubunit import HubUnit
from dataclasses import dataclass


def get_credorledger(x_bud: BudUnit) -> dict[AcctName, float]:
    return {
        acctunit.acct_name: acctunit.credit_belief
        for acctunit in x_bud.accts.values()
        if acctunit.credit_belief > 0
    }


def get_debtorledger(x_bud: BudUnit) -> dict[AcctName, float]:
    return {
        acctunit.acct_name: acctunit.debtit_belief
        for acctunit in x_bud.accts.values()
        if acctunit.debtit_belief > 0
    }


@dataclass
class RiverBook:
    hubunit: HubUnit = None
    owner_name: OwnerName = None
    _rivergrants: dict[AcctName, float] = None


def riverbook_shop(hubunit: HubUnit, owner_name: OwnerName):
    x_riverbook = RiverBook(hubunit, owner_name)
    x_riverbook._rivergrants = {}
    return x_riverbook


def create_riverbook(
    hubunit: HubUnit,
    owner_name: OwnerName,
    keep_credorledger: dict,
    book_point_amount: int,
) -> RiverBook:
    x_riverbook = riverbook_shop(hubunit, owner_name)
    x_riverbook._rivergrants = allot_scale(
        ledger=keep_credorledger,
        scale_number=book_point_amount,
        grain_unit=x_riverbook.hubunit.penny,
    )
    return x_riverbook


@dataclass
class RiverCycle:
    hubunit: HubUnit = None
    number: int = None
    keep_credorledgers: dict[OwnerName : dict[AcctName, float]] = None
    riverbooks: dict[AcctName, RiverBook] = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.owner_name] = x_riverbook

    def set_riverbook(self, book_acct_name: AcctName, book_point_amount: float):
        owner_credorledger = self.keep_credorledgers.get(book_acct_name)
        if owner_credorledger is not None:
            x_riverbook = create_riverbook(
                hubunit=self.hubunit,
                owner_name=book_acct_name,
                keep_credorledger=owner_credorledger,
                book_point_amount=book_point_amount,
            )
            self._set_complete_riverbook(x_riverbook)

    def create_cylceledger(self) -> dict[AcctName, float]:
        x_dict = {}
        for x_riverbook in self.riverbooks.values():
            for payee, pay_amount in x_riverbook._rivergrants.items():
                if x_dict.get(payee) is None:
                    x_dict[payee] = pay_amount
                else:
                    x_dict[payee] = x_dict[payee] + pay_amount
        return x_dict


def rivercycle_shop(
    hubunit: HubUnit,
    number: int,
    keep_credorledgers: dict[OwnerName : dict[AcctName, float]] = None,
):
    return RiverCycle(
        hubunit=hubunit,
        number=number,
        keep_credorledgers=get_empty_dict_if_None(keep_credorledgers),
        riverbooks=get_empty_dict_if_None(None),
    )


def create_init_rivercycle(
    healer_hubunit: HubUnit,
    keep_credorledgers: dict[OwnerName : dict[AcctName, float]],
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(healer_hubunit, 0, keep_credorledgers)
    init_amount = healer_hubunit.keep_point_magnitude
    x_rivercycle.set_riverbook(healer_hubunit.owner_name, init_amount)
    return x_rivercycle


def create_next_rivercycle(
    prev_rivercycle: RiverCycle, prev_cycle_cycleledger_post_tax: dict[AcctName, float]
) -> RiverCycle:
    next_rivercycle = rivercycle_shop(
        hubunit=prev_rivercycle.hubunit,
        number=prev_rivercycle.number + 1,
        keep_credorledgers=prev_rivercycle.keep_credorledgers,
    )
    for payer_id, paying_amount in prev_cycle_cycleledger_post_tax.items():
        next_rivercycle.set_riverbook(payer_id, paying_amount)
    return next_rivercycle


@dataclass
class RiverGrade:
    hubunit: HubUnit = None
    acct_name: AcctName = None
    number: int = None
    tax_bill_amount: float = None
    grant_amount: float = None
    debtor_rank_num: float = None
    credor_rank_num: float = None
    tax_paid_amount: float = None
    tax_paid_bool: float = None
    tax_paid_rank_num: float = None
    tax_paid_rank_percent: float = None
    debtor_count: float = None
    credor_count: float = None
    debtor_rank_percent: float = None
    credor_rank_percent: float = None
    rewards_count: float = None
    rewards_magnitude: float = None

    def set_tax_bill_amount(self, x_tax_bill_amount: float):
        self.tax_bill_amount = x_tax_bill_amount
        self.set_tax_paid_bool()

    def set_tax_paid_amount(self, x_tax_paid_amount: float):
        self.tax_paid_amount = x_tax_paid_amount
        self.set_tax_paid_bool()

    def set_tax_paid_bool(self):
        self.tax_paid_bool = (
            self.tax_bill_amount is not None
            and self.tax_bill_amount == self.tax_paid_amount
        )

    def get_dict(self) -> dict:
        return {
            "fisc_title": self.hubunit.fisc_title,
            "healer_name": self.hubunit.owner_name,
            "keep_road": self.hubunit.keep_road,
            "tax_bill_amount": self.tax_bill_amount,
            "grant_amount": self.grant_amount,
            "debtor_rank_num": self.debtor_rank_num,
            "credor_rank_num": self.credor_rank_num,
            "tax_paid_amount": self.tax_paid_amount,
            "tax_paid_bool": self.tax_paid_bool,
            "tax_paid_rank_num": self.tax_paid_rank_num,
            "tax_paid_rank_percent": self.tax_paid_rank_percent,
            "debtor_count": self.debtor_count,
            "credor_count": self.credor_count,
            "debtor_rank_percent": self.debtor_rank_percent,
            "credor_rank_percent": self.credor_rank_percent,
            "rewards_count": self.rewards_count,
            "rewards_magnitude": self.rewards_magnitude,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def rivergrade_shop(
    hubunit: HubUnit,
    acct_name: AcctName,
    number: float = None,
    debtor_count: int = None,
    credor_count: int = None,
):
    return RiverGrade(
        hubunit=hubunit,
        acct_name=acct_name,
        number=get_0_if_None(number),
        debtor_count=debtor_count,
        credor_count=credor_count,
    )
