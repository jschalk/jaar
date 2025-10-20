from dataclasses import dataclass
from src.ch01_py.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_positive_int,
    set_in_nested_dict,
)
from src.ch01_py.file_toolbox import save_json
from src.ch02_allot.allot import (
    allot_scale,
    default_grain_num_if_None,
    validate_pool_num,
)
from src.ch13_belief_listen._ref.ch13_path import create_keep_grade_path
from src.ch14_keep._ref.ch14_semantic_types import (
    BeliefName,
    LabelTerm,
    ManaGrain,
    ManaNum,
    RopeTerm,
    VoiceName,
    default_knot_if_None,
)
from src.ch14_keep.rivercycle import (
    RiverGrade,
    create_init_rivercycle,
    create_next_rivercycle,
    rivergrade_shop,
)


@dataclass
class RiverRun:
    moment_mstr_dir: str = None
    moment_label: LabelTerm = None
    belief_name: BeliefName = None
    keep_rope: RopeTerm = None
    knot: str = None
    keep_point_magnitude: ManaNum = None
    mana_grain: ManaGrain = None
    number: int = None
    keep_patientledgers: dict[BeliefName : dict[VoiceName, float]] = None
    need_dues: dict[VoiceName, float] = None
    cycle_max: int = None
    # calculated fields
    _cares: dict[VoiceName, float] = None
    _need_yields: dict[VoiceName, float] = None
    _need_got_prev: float = None
    _need_got_curr: float = None
    _cycle_count: int = None
    _cycle_carees_prev: set = None
    _cycle_carees_curr: set = None
    _doctor_count: int = None
    _patient_count: int = None
    _rivergrades: dict[VoiceName, RiverGrade] = None

    def set_cycle_max(self, x_cycle_max: int):
        self.cycle_max = get_positive_int(x_cycle_max)

    def set_keep_patientledger(
        self,
        belief_name: BeliefName,
        voice_name: VoiceName,
        mana_ledger: float,
    ):
        set_in_nested_dict(
            x_dict=self.keep_patientledgers,
            x_keylist=[belief_name, voice_name],
            x_obj=mana_ledger,
        )

    def delete_keep_patientledgers_belief(self, belief_name: BeliefName):
        self.keep_patientledgers.pop(belief_name)

    def get_all_keep_patientledger_voice_names(self):
        x_set = set()
        for belief_name, belief_dict in self.keep_patientledgers.items():
            if belief_name not in x_set:
                x_set.add(belief_name)
            for voice_name in belief_dict.keys():
                if voice_name not in x_set:
                    x_set.add(voice_name)
        return x_set

    def levy_need_dues(self, cycleledger: tuple[dict[VoiceName, float], float]):
        delete_from_cycleledger = []
        need_got_total = 0
        for caree, caree_amount in cycleledger.items():
            if self.voice_has_need_due(caree):
                excess_carer_points, need_got = self.levy_need_due(caree, caree_amount)
                need_got_total += need_got
                if excess_carer_points == 0:
                    delete_from_cycleledger.append(caree)
                else:
                    cycleledger[caree] = excess_carer_points

        for caree_to_delete in delete_from_cycleledger:
            cycleledger.pop(caree_to_delete)
        return cycleledger, need_got_total

    def set_voice_need_due(self, x_voice_name: VoiceName, need_due: float):
        self.need_dues[x_voice_name] = need_due

    def need_dues_unpaid(self) -> bool:
        return len(self.need_dues) != 0

    def set_need_dues(self, doctorledger: dict[VoiceName, float]):
        x_amount = self.keep_point_magnitude
        self.need_dues = allot_scale(doctorledger, x_amount, self.mana_grain)

    def voice_has_need_due(self, x_voice_name: VoiceName) -> bool:
        return self.need_dues.get(x_voice_name) is not None

    def get_voice_need_due(self, x_voice_name: VoiceName) -> float:
        x_need_due = self.need_dues.get(x_voice_name)
        return 0 if x_need_due is None else x_need_due

    def delete_need_due(self, x_voice_name: VoiceName):
        self.need_dues.pop(x_voice_name)

    def levy_need_due(self, x_voice_name: VoiceName, carer_points: float) -> float:
        if self.voice_has_need_due(x_voice_name) is False:
            return carer_points, 0
        x_need_due = self.get_voice_need_due(x_voice_name)
        if x_need_due > carer_points:
            left_over_care = x_need_due - carer_points
            self.set_voice_need_due(x_voice_name, left_over_care)
            self.add_voice_need_yield(x_voice_name, carer_points)
            return 0, carer_points
        else:
            self.delete_need_due(x_voice_name)
            self.add_voice_need_yield(x_voice_name, x_need_due)
            return carer_points - x_need_due, x_need_due

    def get_ledger_dict(self) -> dict[VoiceName, float]:
        return self.need_dues

    def set_voice_need_yield(self, x_voice_name: VoiceName, need_yield: float):
        self._need_yields[x_voice_name] = need_yield

    def need_yields_is_empty(self) -> bool:
        return len(self._need_yields) == 0

    def reset_need_yields(self):
        self._need_yields = {}

    def voice_has_need_yield(self, x_voice_name: VoiceName) -> bool:
        return self._need_yields.get(x_voice_name) is not None

    def get_voice_need_yield(self, x_voice_name: VoiceName) -> float:
        x_need_yield = self._need_yields.get(x_voice_name)
        return 0 if x_need_yield is None else x_need_yield

    def delete_need_yield(self, x_voice_name: VoiceName):
        self._need_yields.pop(x_voice_name)

    def add_voice_need_yield(self, x_voice_name: VoiceName, x_need_yield: float):
        if self.voice_has_need_yield(x_voice_name):
            x_need_yield = self.get_voice_need_yield(x_voice_name) + x_need_yield
        self.set_voice_need_yield(x_voice_name, x_need_yield)

    def get_rivergrade(self, voice_name: VoiceName) -> RiverGrade:
        return self._rivergrades.get(voice_name)

    def _rivergrades_is_empty(self) -> bool:
        return self._rivergrades == {}

    def rivergrade_exists(self, voice_name: VoiceName) -> bool:
        return self._rivergrades.get(voice_name) is not None

    def _get_voice_care(self, voice_name: VoiceName) -> float:
        return get_0_if_None(self._cares.get(voice_name))

    def set_initial_rivergrade(self, voice_name: VoiceName):
        x_rivergrade = rivergrade_shop(
            self.moment_label,
            self.belief_name,
            self.keep_rope,
            voice_name,
            self.number,
        )
        x_rivergrade.doctor_count = self._doctor_count
        x_rivergrade.patient_count = self._patient_count
        x_rivergrade.care_amount = self._get_voice_care(voice_name)
        self._rivergrades[voice_name] = x_rivergrade

    def set_all_initial_rivergrades(self):
        self._rivergrades = {}
        all_voice_names = self.get_all_keep_patientledger_voice_names()
        for voice_name in all_voice_names:
            self.set_initial_rivergrade(voice_name)

    def _set_post_loop_rivergrade_attrs(self):
        for x_voice_name, voice_rivergrade in self._rivergrades.items():
            need_due_leftover = self.get_voice_need_due(x_voice_name)
            need_due_paid = self.get_voice_need_yield(x_voice_name)
            voice_rivergrade.set_need_bill_amount(need_due_paid + need_due_leftover)
            voice_rivergrade.set_need_paid_amount(need_due_paid)

    def calc_metrics(self):
        self._set_doctor_count_patient_count()
        self._set_cares()
        self.set_all_initial_rivergrades()

        self._cycle_count = 0
        x_rivercyle = create_init_rivercycle(self.belief_name, self.keep_patientledgers)
        x_cyclelegder = x_rivercyle.create_cylceledger()
        self._cycle_carees_curr = set(x_cyclelegder.keys())
        x_cyclelegder, need_got_curr = self.levy_need_dues(x_cyclelegder)
        self._set_need_got_attrs(need_got_curr)

        while self.cycle_max > self._cycle_count and self.cycles_vary():
            x_rivercyle = create_next_rivercycle(x_rivercyle, x_cyclelegder)
            x_cyclelegder, need_got_curr = self.levy_need_dues(x_cyclelegder)

            self._set_need_got_attrs(need_got_curr)
            self._cycle_carees_prev = self._cycle_carees_curr
            self._cycle_carees_curr = set(x_cyclelegder.keys())
            self._cycle_count += 1

        self._set_post_loop_rivergrade_attrs()

    def _set_doctor_count_patient_count(self):
        need_dues_voices = set(self.need_dues.keys())
        need_yields_voices = set(self._need_yields.keys())
        self._doctor_count = len(need_dues_voices.union(need_yields_voices))
        self._patient_count = len(self.keep_patientledgers.get(self.belief_name))

    def _set_cares(self):
        care_patientledger = self.keep_patientledgers.get(self.belief_name)
        self._cares = allot_scale(
            ledger=care_patientledger,
            scale_number=self.keep_point_magnitude,
            grain_unit=self.mana_grain,
        )

    def _save_rivergrade_file(self, voice_name: VoiceName):
        rivergrade = self.get_rivergrade(voice_name)
        grade_path = create_keep_grade_path(
            moment_mstr_dir=self.moment_mstr_dir,
            belief_name=self.belief_name,
            moment_label=self.moment_label,
            keep_rope=self.keep_rope,
            knot=self.knot,
            grade_belief_name=voice_name,
        )
        save_json(grade_path, None, rivergrade.to_dict())

    def save_rivergrade_files(self):
        for rivergrade_voice in self._rivergrades.keys():
            self._save_rivergrade_file(rivergrade_voice)

    def _cycle_carees_vary(self) -> bool:
        return self._cycle_carees_prev != self._cycle_carees_curr

    def _set_need_got_attrs(self, x_need_got_curr: float):
        self._need_got_prev = self._need_got_curr
        self._need_got_curr = x_need_got_curr

    def _need_gotten(self) -> bool:
        return max(self._need_got_prev, self._need_got_curr) > 0

    def cycles_vary(self) -> bool:
        return self._need_gotten() or self._cycle_carees_vary()


def riverrun_shop(
    moment_mstr_dir: str,
    moment_label: LabelTerm,
    belief_name: BeliefName,
    keep_rope: RopeTerm = None,
    knot: str = None,
    keep_point_magnitude: ManaNum = None,
    mana_grain: ManaGrain = None,
    number: int = None,
    keep_patientledgers: dict[BeliefName : dict[VoiceName, float]] = None,
    need_dues: dict[VoiceName, float] = None,
    cycle_max: int = None,
):
    x_riverun = RiverRun(
        moment_mstr_dir=moment_mstr_dir,
        moment_label=moment_label,
        belief_name=belief_name,
        keep_rope=keep_rope,
        knot=default_knot_if_None(knot),
        keep_point_magnitude=validate_pool_num(keep_point_magnitude),
        mana_grain=default_grain_num_if_None(mana_grain),
        number=get_0_if_None(number),
        keep_patientledgers=get_empty_dict_if_None(keep_patientledgers),
        need_dues=get_empty_dict_if_None(need_dues),
        _rivergrades={},
        _cares={},
        _need_yields={},
    )
    x_riverun._cycle_count = 0
    x_riverun._cycle_carees_prev = set()
    x_riverun._cycle_carees_curr = set()
    x_riverun._need_got_prev = 0
    x_riverun._need_got_curr = 0
    if cycle_max is None:
        cycle_max = 10
    x_riverun.set_cycle_max(cycle_max)
    return x_riverun
