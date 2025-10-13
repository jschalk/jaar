from dataclasses import dataclass
from src.ch01_py.dict_toolbox import get_0_if_None, get_empty_dict_if_None
from src.ch03_allot.allot import (
    allot_scale,
    default_grain_num_if_None,
    validate_pool_num,
)
from src.ch07_belief_logic.belief_main import BeliefUnit
from src.ch14_keep._ref.ch14_semantic_types import (
    BeliefName,
    MomentLabel,
    MoneyGrain,
    MoneyNum,
    RopeTerm,
    VoiceName,
)


def get_credorledger(x_belief: BeliefUnit) -> dict[VoiceName, float]:
    return {
        voiceunit.voice_name: voiceunit.voice_cred_lumen
        for voiceunit in x_belief.voices.values()
        if voiceunit.voice_cred_lumen > 0
    }


def get_debtorledger(x_belief: BeliefUnit) -> dict[VoiceName, float]:
    return {
        voiceunit.voice_name: voiceunit.voice_debt_lumen
        for voiceunit in x_belief.voices.values()
        if voiceunit.voice_debt_lumen > 0
    }


@dataclass
class RiverBook:
    belief_name: BeliefName = None
    _rivergrants: dict[VoiceName, float] = None
    money_grain: MoneyGrain = None


def riverbook_shop(belief_name: BeliefName, money_grain: MoneyGrain = None):
    x_riverbook = RiverBook(belief_name)
    x_riverbook._rivergrants = {}
    x_riverbook.money_grain = default_grain_num_if_None(money_grain)
    return x_riverbook


def create_riverbook(
    belief_name: BeliefName,
    keep_credorledger: dict,
    book_point_amount: int,
    money_grain: MoneyGrain = None,
) -> RiverBook:
    x_riverbook = riverbook_shop(belief_name, money_grain)
    x_riverbook._rivergrants = allot_scale(
        ledger=keep_credorledger,
        scale_number=book_point_amount,
        grain_unit=x_riverbook.money_grain,
    )
    return x_riverbook


@dataclass
class RiverCycle:
    healer_name: BeliefName = None
    number: int = None
    keep_credorledgers: dict[BeliefName : dict[VoiceName, float]] = None
    riverbooks: dict[VoiceName, RiverBook] = None
    money_grain: MoneyGrain = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.belief_name] = x_riverbook

    def set_riverbook(
        self,
        book_voice_name: VoiceName,
        book_point_amount: float,
    ):
        belief_credorledger = self.keep_credorledgers.get(book_voice_name)
        if belief_credorledger is not None:
            x_riverbook = create_riverbook(
                belief_name=book_voice_name,
                keep_credorledger=belief_credorledger,
                book_point_amount=book_point_amount,
                money_grain=default_grain_num_if_None(self.money_grain),
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
    healer_name: BeliefName,
    number: int,
    keep_credorledgers: dict[BeliefName : dict[VoiceName, float]] = None,
    money_grain: MoneyGrain = None,
):
    return RiverCycle(
        healer_name=healer_name,
        number=number,
        keep_credorledgers=get_empty_dict_if_None(keep_credorledgers),
        riverbooks=get_empty_dict_if_None(),
        money_grain=default_grain_num_if_None(money_grain),
    )


def create_init_rivercycle(
    healer_name: BeliefName,
    keep_credorledgers: dict[BeliefName : dict[VoiceName, float]],
    keep_point_magnitude: MoneyNum = None,
    money_grain: MoneyGrain = None,
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(
        healer_name, 0, keep_credorledgers, money_grain=money_grain
    )
    x_rivercycle.set_riverbook(healer_name, validate_pool_num(keep_point_magnitude))
    return x_rivercycle


def create_next_rivercycle(
    prev_rivercycle: RiverCycle,
    prev_cycle_cycleledger_post_tax: dict[VoiceName, float],
) -> RiverCycle:
    next_rivercycle = rivercycle_shop(
        healer_name=prev_rivercycle.healer_name,
        number=prev_rivercycle.number + 1,
        keep_credorledgers=prev_rivercycle.keep_credorledgers,
        money_grain=prev_rivercycle.money_grain,
    )
    for chargeer_id, chargeing_amount in prev_cycle_cycleledger_post_tax.items():
        next_rivercycle.set_riverbook(chargeer_id, chargeing_amount)
    return next_rivercycle


@dataclass
class RiverGrade:
    moment_label: MomentLabel = None
    belief_name: BeliefName = None
    keep_rope: RopeTerm = None
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
        """Returns dict that is serializable to JSON."""

        return {
            "moment_label": self.moment_label,
            "healer_name": self.belief_name,
            "keep_rope": self.keep_rope,
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


def rivergrade_shop(
    moment_label: MomentLabel,
    belief_name: BeliefName,
    keep_rope: RopeTerm,
    voice_name: VoiceName,
    number: float = None,
    debtor_count: int = None,
    credor_count: int = None,
):
    return RiverGrade(
        moment_label=moment_label,
        belief_name=belief_name,
        keep_rope=keep_rope,
        voice_name=voice_name,
        number=get_0_if_None(number),
        debtor_count=debtor_count,
        credor_count=credor_count,
    )
