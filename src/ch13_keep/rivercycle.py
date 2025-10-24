from dataclasses import dataclass
from src.ch01_py.dict_toolbox import get_0_if_None, get_empty_dict_if_None
from src.ch02_allot.allot import (
    allot_scale,
    default_grain_num_if_None,
    validate_pool_num,
)
from src.ch07_belief_logic.belief_main import BeliefUnit
from src.ch13_keep._ref.ch13_semantic_types import (
    BeliefName,
    ManaGrain,
    ManaNum,
    MomentLabel,
    RespectNum,
    RopeTerm,
    VoiceName,
)


def get_patientledger(x_belief: BeliefUnit) -> dict[VoiceName, RespectNum]:
    return {
        voiceunit.voice_name: voiceunit.voice_cred_lumen
        for voiceunit in x_belief.voices.values()
        if voiceunit.voice_cred_lumen > 0
    }


def get_doctorledger(x_belief: BeliefUnit) -> dict[VoiceName, RespectNum]:
    return {
        voiceunit.voice_name: voiceunit.voice_debt_lumen
        for voiceunit in x_belief.voices.values()
        if voiceunit.voice_debt_lumen > 0
    }


@dataclass
class RiverBook:
    belief_name: BeliefName = None
    rivercares: dict[VoiceName, float] = None
    mana_grain: ManaGrain = None


def riverbook_shop(belief_name: BeliefName, mana_grain: ManaGrain = None):
    x_riverbook = RiverBook(belief_name)
    x_riverbook.rivercares = {}
    x_riverbook.mana_grain = default_grain_num_if_None(mana_grain)
    return x_riverbook


def create_riverbook(
    belief_name: BeliefName,
    keep_patientledger: dict,
    book_point_amount: int,
    mana_grain: ManaGrain = None,
) -> RiverBook:
    x_riverbook = riverbook_shop(belief_name, mana_grain)
    x_riverbook.rivercares = allot_scale(
        ledger=keep_patientledger,
        scale_number=book_point_amount,
        grain_unit=x_riverbook.mana_grain,
    )
    return x_riverbook


@dataclass
class RiverCycle:
    healer_name: BeliefName = None
    number: int = None
    keep_patientledgers: dict[BeliefName : dict[VoiceName, float]] = None
    riverbooks: dict[VoiceName, RiverBook] = None
    mana_grain: ManaGrain = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.belief_name] = x_riverbook

    def set_riverbook(
        self,
        book_voice_name: VoiceName,
        book_point_amount: float,
    ):
        belief_patientledger = self.keep_patientledgers.get(book_voice_name)
        if belief_patientledger is not None:
            x_riverbook = create_riverbook(
                belief_name=book_voice_name,
                keep_patientledger=belief_patientledger,
                book_point_amount=book_point_amount,
                mana_grain=default_grain_num_if_None(self.mana_grain),
            )
            self._set_complete_riverbook(x_riverbook)

    def create_cylceledger(self) -> dict[VoiceName, float]:
        x_dict = {}
        for x_riverbook in self.riverbooks.values():
            for caree, charge_amount in x_riverbook.rivercares.items():
                if x_dict.get(caree) is None:
                    x_dict[caree] = charge_amount
                else:
                    x_dict[caree] = x_dict[caree] + charge_amount
        return x_dict


def rivercycle_shop(
    healer_name: BeliefName,
    number: int,
    keep_patientledgers: dict[BeliefName : dict[VoiceName, float]] = None,
    mana_grain: ManaGrain = None,
):
    return RiverCycle(
        healer_name=healer_name,
        number=number,
        keep_patientledgers=get_empty_dict_if_None(keep_patientledgers),
        riverbooks=get_empty_dict_if_None(),
        mana_grain=default_grain_num_if_None(mana_grain),
    )


def create_init_rivercycle(
    healer_name: BeliefName,
    keep_patientledgers: dict[BeliefName : dict[VoiceName, float]],
    keep_point_magnitude: ManaNum = None,
    mana_grain: ManaGrain = None,
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(
        healer_name, 0, keep_patientledgers, mana_grain=mana_grain
    )
    x_rivercycle.set_riverbook(healer_name, validate_pool_num(keep_point_magnitude))
    return x_rivercycle


def create_next_rivercycle(
    prev_rivercycle: RiverCycle,
    prev_cycle_cycleledger_post_need: dict[VoiceName, float],
) -> RiverCycle:
    next_rivercycle = rivercycle_shop(
        healer_name=prev_rivercycle.healer_name,
        number=prev_rivercycle.number + 1,
        keep_patientledgers=prev_rivercycle.keep_patientledgers,
        mana_grain=prev_rivercycle.mana_grain,
    )
    for carer_id, chargeing_amount in prev_cycle_cycleledger_post_need.items():
        next_rivercycle.set_riverbook(carer_id, chargeing_amount)
    return next_rivercycle


@dataclass
class RiverGrade:
    moment_label: MomentLabel = None
    belief_name: BeliefName = None
    keep_rope: RopeTerm = None
    voice_name: VoiceName = None
    number: int = None
    need_bill_amount: float = None
    care_amount: float = None
    doctor_rank_num: float = None
    patient_rank_num: float = None
    need_paid_amount: float = None
    need_paid_bool: float = None
    need_paid_rank_num: float = None
    need_paid_rank_percent: float = None
    doctor_count: float = None
    patient_count: float = None
    doctor_rank_percent: float = None
    patient_rank_percent: float = None
    rewards_count: float = None
    rewards_magnitude: float = None

    def set_need_bill_amount(self, x_need_bill_amount: float):
        self.need_bill_amount = x_need_bill_amount
        self.set_need_paid_bool()

    def set_need_paid_amount(self, x_need_paid_amount: float):
        self.need_paid_amount = x_need_paid_amount
        self.set_need_paid_bool()

    def set_need_paid_bool(self):
        self.need_paid_bool = (
            self.need_bill_amount is not None
            and self.need_bill_amount == self.need_paid_amount
        )

    def to_dict(self) -> dict:
        """Returns dict that is serializable to JSON."""

        return {
            "moment_label": self.moment_label,
            "healer_name": self.belief_name,
            "keep_rope": self.keep_rope,
            "need_bill_amount": self.need_bill_amount,
            "care_amount": self.care_amount,
            "doctor_rank_num": self.doctor_rank_num,
            "patient_rank_num": self.patient_rank_num,
            "need_paid_amount": self.need_paid_amount,
            "need_paid_bool": self.need_paid_bool,
            "need_paid_rank_num": self.need_paid_rank_num,
            "need_paid_rank_percent": self.need_paid_rank_percent,
            "doctor_count": self.doctor_count,
            "patient_count": self.patient_count,
            "doctor_rank_percent": self.doctor_rank_percent,
            "patient_rank_percent": self.patient_rank_percent,
            "rewards_count": self.rewards_count,
            "rewards_magnitude": self.rewards_magnitude,
        }


def rivergrade_shop(
    moment_label: MomentLabel,
    belief_name: BeliefName,
    keep_rope: RopeTerm,
    voice_name: VoiceName,
    number: float = None,
    doctor_count: int = None,
    patient_count: int = None,
):
    return RiverGrade(
        moment_label=moment_label,
        belief_name=belief_name,
        keep_rope=keep_rope,
        voice_name=voice_name,
        number=get_0_if_None(number),
        doctor_count=doctor_count,
        patient_count=patient_count,
    )
