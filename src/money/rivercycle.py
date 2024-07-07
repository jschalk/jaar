from src._instrument.python import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_json_from_dict,
)
from src._road.finance import allot_scale
from src._road.road import CharID, OwnerID
from src._world.world import WorldUnit
from src.listen.hubunit import HubUnit
from dataclasses import dataclass


def get_credorledger(x_world: WorldUnit) -> dict[CharID, float]:
    return {
        charunit.char_id: charunit.credor_weight
        for charunit in x_world._chars.values()
        if charunit.credor_weight > 0
    }


def get_debtorledger(x_world: WorldUnit) -> dict[CharID, float]:
    return {
        charunit.char_id: charunit.debtor_weight
        for charunit in x_world._chars.values()
        if charunit.debtor_weight > 0
    }


@dataclass
class RiverBook:
    hubunit: HubUnit = None
    owner_id: OwnerID = None
    _rivergrants: dict[CharID, float] = None


def riverbook_shop(hubunit: HubUnit, owner_id: OwnerID):
    x_riverbook = RiverBook(hubunit, owner_id)
    x_riverbook._rivergrants = {}
    return x_riverbook


def create_riverbook(
    hubunit: HubUnit,
    owner_id: OwnerID,
    econ_credorledger: dict,
    book_money_amount: int,
) -> RiverBook:
    x_riverbook = riverbook_shop(hubunit, owner_id)
    x_riverbook._rivergrants = allot_scale(
        ledger=econ_credorledger,
        scale_number=book_money_amount,
        grain_unit=x_riverbook.hubunit.penny,
    )
    return x_riverbook


@dataclass
class RiverCycle:
    hubunit: HubUnit = None
    number: int = None
    econ_credorledgers: dict[OwnerID : dict[CharID, float]] = None
    riverbooks: dict[CharID, RiverBook] = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.owner_id] = x_riverbook

    def set_riverbook(self, book_char_id: CharID, book_money_amount: float):
        owner_credorledger = self.econ_credorledgers.get(book_char_id)
        if owner_credorledger != None:
            x_riverbook = create_riverbook(
                hubunit=self.hubunit,
                owner_id=book_char_id,
                econ_credorledger=owner_credorledger,
                book_money_amount=book_money_amount,
            )
            self._set_complete_riverbook(x_riverbook)

    def create_cylceledger(self) -> dict[CharID, float]:
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
    econ_credorledgers: dict[OwnerID : dict[CharID, float]] = None,
):
    return RiverCycle(
        hubunit=hubunit,
        number=number,
        econ_credorledgers=get_empty_dict_if_none(econ_credorledgers),
        riverbooks=get_empty_dict_if_none(None),
    )


def create_init_rivercycle(
    healer_hubunit: HubUnit,
    econ_credorledgers: dict[OwnerID : dict[CharID, float]],
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(healer_hubunit, 0, econ_credorledgers)
    init_amount = healer_hubunit.econ_money_magnitude
    x_rivercycle.set_riverbook(healer_hubunit.owner_id, init_amount)
    return x_rivercycle


def create_next_rivercycle(
    prev_rivercycle: RiverCycle, prev_cycle_cycleledger_post_tax: dict[CharID, float]
) -> RiverCycle:
    next_rivercycle = rivercycle_shop(
        hubunit=prev_rivercycle.hubunit,
        number=prev_rivercycle.number + 1,
        econ_credorledgers=prev_rivercycle.econ_credorledgers,
    )
    for payer_id, paying_amount in prev_cycle_cycleledger_post_tax.items():
        next_rivercycle.set_riverbook(payer_id, paying_amount)
    return next_rivercycle


@dataclass
class RiverGrade:
    hubunit: HubUnit = None
    char_id: CharID = None
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
            self.tax_bill_amount != None
            and self.tax_bill_amount == self.tax_paid_amount
        )

    def get_dict(self) -> dict:
        return {
            "real_id": self.hubunit.real_id,
            "healer_id": self.hubunit.owner_id,
            "econ_road": self.hubunit.econ_road,
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
    char_id: CharID,
    number: float = None,
    debtor_count: int = None,
    credor_count: int = None,
):
    return RiverGrade(
        hubunit=hubunit,
        char_id=char_id,
        number=get_0_if_None(number),
        debtor_count=debtor_count,
        credor_count=credor_count,
    )
