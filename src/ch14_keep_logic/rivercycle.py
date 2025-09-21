from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_json_from_dict,
)
from src.a01_rope_logic.term import BeliefName, VoiceName
from src.a02_finance_logic.allot import allot_scale
from src.a06_belief_logic.belief_main import BeliefUnit
from src.ch12_hub_toolbox.hubunit import HubUnit


def get_credorledger(x_belief: BeliefUnit) -> dict[VoiceName, float]:
    return {
        voiceunit.voice_name: voiceunit.voice_cred_points
        for voiceunit in x_belief.voices.values()
        if voiceunit.voice_cred_points > 0
    }


def get_debtorledger(x_belief: BeliefUnit) -> dict[VoiceName, float]:
    return {
        voiceunit.voice_name: voiceunit.voice_debt_points
        for voiceunit in x_belief.voices.values()
        if voiceunit.voice_debt_points > 0
    }


@dataclass
class RiverBook:
    hubunit: HubUnit = None
    belief_name: BeliefName = None
    _rivergrants: dict[VoiceName, float] = None


def riverbook_shop(hubunit: HubUnit, belief_name: BeliefName):
    x_riverbook = RiverBook(hubunit, belief_name)
    x_riverbook._rivergrants = {}
    return x_riverbook


def create_riverbook(
    hubunit: HubUnit,
    belief_name: BeliefName,
    keep_credorledger: dict,
    book_point_amount: int,
) -> RiverBook:
    x_riverbook = riverbook_shop(hubunit, belief_name)
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
    keep_credorledgers: dict[BeliefName : dict[VoiceName, float]] = None
    riverbooks: dict[VoiceName, RiverBook] = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.belief_name] = x_riverbook

    def set_riverbook(self, book_voice_name: VoiceName, book_point_amount: float):
        belief_credorledger = self.keep_credorledgers.get(book_voice_name)
        if belief_credorledger is not None:
            x_riverbook = create_riverbook(
                hubunit=self.hubunit,
                belief_name=book_voice_name,
                keep_credorledger=belief_credorledger,
                book_point_amount=book_point_amount,
            )
            self._set_complete_riverbook(x_riverbook)

    def create_cylceledger(self) -> dict[VoiceName, float]:
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
    keep_credorledgers: dict[BeliefName : dict[VoiceName, float]] = None,
):
    return RiverCycle(
        hubunit=hubunit,
        number=number,
        keep_credorledgers=get_empty_dict_if_None(keep_credorledgers),
        riverbooks=get_empty_dict_if_None(),
    )


def create_init_rivercycle(
    healer_hubunit: HubUnit,
    keep_credorledgers: dict[BeliefName : dict[VoiceName, float]],
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(healer_hubunit, 0, keep_credorledgers)
    init_amount = healer_hubunit.keep_point_magnitude
    x_rivercycle.set_riverbook(healer_hubunit.belief_name, init_amount)
    return x_rivercycle


def create_next_rivercycle(
    prev_rivercycle: RiverCycle,
    prev_cycle_cycleledger_post_tax: dict[VoiceName, float],
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
    voice_name: VoiceName = None
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

    def to_dict(self) -> dict:
        return {
            "moment_label": self.hubunit.moment_label,
            "healer_name": self.hubunit.belief_name,
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
        return get_json_from_dict(self.to_dict())


def rivergrade_shop(
    hubunit: HubUnit,
    voice_name: VoiceName,
    number: float = None,
    debtor_count: int = None,
    credor_count: int = None,
):
    return RiverGrade(
        hubunit=hubunit,
        voice_name=voice_name,
        number=get_0_if_None(number),
        debtor_count=debtor_count,
        credor_count=credor_count,
    )
