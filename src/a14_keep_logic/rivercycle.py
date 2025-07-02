from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_json_from_dict,
)
from src.a01_term_logic.term import BelieverName, PersonName
from src.a02_finance_logic.allot import allot_scale
from src.a06_believer_logic.believer import BelieverUnit
from src.a12_hub_toolbox.hubunit import HubUnit


def get_credorledger(x_believer: BelieverUnit) -> dict[PersonName, float]:
    return {
        personunit.person_name: personunit.person_cred_points
        for personunit in x_believer.persons.values()
        if personunit.person_cred_points > 0
    }


def get_debtorledger(x_believer: BelieverUnit) -> dict[PersonName, float]:
    return {
        personunit.person_name: personunit.person_debt_points
        for personunit in x_believer.persons.values()
        if personunit.person_debt_points > 0
    }


@dataclass
class RiverBook:
    hubunit: HubUnit = None
    believer_name: BelieverName = None
    _rivergrants: dict[PersonName, float] = None


def riverbook_shop(hubunit: HubUnit, believer_name: BelieverName):
    x_riverbook = RiverBook(hubunit, believer_name)
    x_riverbook._rivergrants = {}
    return x_riverbook


def create_riverbook(
    hubunit: HubUnit,
    believer_name: BelieverName,
    keep_credorledger: dict,
    book_point_amount: int,
) -> RiverBook:
    x_riverbook = riverbook_shop(hubunit, believer_name)
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
    keep_credorledgers: dict[BelieverName : dict[PersonName, float]] = None
    riverbooks: dict[PersonName, RiverBook] = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.believer_name] = x_riverbook

    def set_riverbook(self, book_person_name: PersonName, book_point_amount: float):
        believer_credorledger = self.keep_credorledgers.get(book_person_name)
        if believer_credorledger is not None:
            x_riverbook = create_riverbook(
                hubunit=self.hubunit,
                believer_name=book_person_name,
                keep_credorledger=believer_credorledger,
                book_point_amount=book_point_amount,
            )
            self._set_complete_riverbook(x_riverbook)

    def create_cylceledger(self) -> dict[PersonName, float]:
        x_dict = {}
        for x_riverbook in self.riverbooks.values():
            for chargeee, charge_amount in x_riverbook._rivergrants.items():
                if x_dict.get(chargeee) is None:
                    x_dict[chargeee] = charge_amount
                else:
                    x_dict[chargeee] = x_dict[chargeee] + charge_amount
        return x_dict


def rivercycle_shop(
    hubunit: HubUnit,
    number: int,
    keep_credorledgers: dict[BelieverName : dict[PersonName, float]] = None,
):
    return RiverCycle(
        hubunit=hubunit,
        number=number,
        keep_credorledgers=get_empty_dict_if_None(keep_credorledgers),
        riverbooks=get_empty_dict_if_None(),
    )


def create_init_rivercycle(
    healer_hubunit: HubUnit,
    keep_credorledgers: dict[BelieverName : dict[PersonName, float]],
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(healer_hubunit, 0, keep_credorledgers)
    init_amount = healer_hubunit.keep_point_magnitude
    x_rivercycle.set_riverbook(healer_hubunit.believer_name, init_amount)
    return x_rivercycle


def create_next_rivercycle(
    prev_rivercycle: RiverCycle,
    prev_cycle_cycleledger_post_tax: dict[PersonName, float],
) -> RiverCycle:
    next_rivercycle = rivercycle_shop(
        hubunit=prev_rivercycle.hubunit,
        number=prev_rivercycle.number + 1,
        keep_credorledgers=prev_rivercycle.keep_credorledgers,
    )
    for chargeer_id, chargeing_amount in prev_cycle_cycleledger_post_tax.items():
        next_rivercycle.set_riverbook(chargeer_id, chargeing_amount)
    return next_rivercycle


@dataclass
class RiverGrade:
    hubunit: HubUnit = None
    person_name: PersonName = None
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
            "belief_label": self.hubunit.belief_label,
            "healer_name": self.hubunit.believer_name,
            "keep_rope": self.hubunit.keep_rope,
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
    person_name: PersonName,
    number: float = None,
    debtor_count: int = None,
    credor_count: int = None,
):
    return RiverGrade(
        hubunit=hubunit,
        person_name=person_name,
        number=get_0_if_None(number),
        debtor_count=debtor_count,
        credor_count=credor_count,
    )
