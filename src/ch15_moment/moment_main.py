from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch01_py.dict_toolbox import get_0_if_None, get_empty_set_if_None
from src.ch01_py.file_toolbox import create_path, get_dir_file_strs, open_json, set_dir
from src.ch02_allot.allot import default_grain_num_if_None
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch09_belief_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_belief_lesson.lesson_filehandler import (
    gut_file_exists,
    open_gut_file,
    save_gut_file,
)
from src.ch11_belief_listen.basis_beliefs import create_listen_basis
from src.ch11_belief_listen.keep_tool import (
    create_treasury_db_file,
    open_job_file,
    save_duty_belief,
    save_job_file,
)
from src.ch11_belief_listen.listen_main import (
    listen_to_agendas_create_init_job_from_guts,
    listen_to_debtors_roll_jobs_into_job,
)
from src.ch12_bud._ref.ch12_path import create_cell_dir_path
from src.ch12_bud.bud_filehandler import cellunit_save_to_dir
from src.ch12_bud.bud_main import (
    BeliefBudHistory,
    BudUnit,
    TranBook,
    TranUnit,
    beliefbudhistory_shop,
    get_beliefbudhistory_from_dict,
    get_tranbook_from_dict,
    tranbook_shop,
)
from src.ch12_bud.cell import cellunit_shop
from src.ch14_epoch.epoch_main import (
    EpochTime,
    EpochUnit,
    add_epoch_planunit,
    epochunit_shop,
)
from src.ch15_moment._ref.ch15_semantic_types import (
    BeliefName,
    FundGrain,
    FundNum,
    KnotTerm,
    ManaGrain,
    MomentLabel,
    RespectGrain,
    SparkInt,
    VoiceName,
    default_knot_if_None,
)


def get_default_job_listen_count() -> int:
    return 3


class budunit_Exception(Exception):
    pass


class set_paypurchase_Exception(Exception):
    pass


class set_offi_time_max_Exception(Exception):
    pass


@dataclass
class MomentUnit:
    """Data pipelines:
    pipeline1: lessons->gut
    pipeline2: gut->dutys
    pipeline3: duty->vision
    pipeline4: vision->job
    pipeline5: gut->job (direct)
    pipeline6: gut->vision->job (through visions)
    pipeline7: lessons->job (could be 5 of 6)
    """

    # TODO extraction pipelines into standalone functions

    moment_label: MomentLabel = None
    moment_mstr_dir: str = None
    epoch: EpochUnit = None
    beliefbudhistorys: dict[BeliefName, BeliefBudHistory] = None
    paybook: TranBook = None
    offi_times: set[EpochTime] = None
    knot: KnotTerm = None
    fund_grain: FundGrain = None
    respect_grain: RespectGrain = None
    mana_grain: ManaGrain = None
    job_listen_rotations: int = None
    # calculated fields
    offi_time_max: EpochTime = None
    moment_dir: str = None
    beliefs_dir: str = None
    lessons_dir: str = None
    all_tranbook: TranBook = None

    # directory setup
    def _set_moment_dirs(self):
        moments_dir = create_path(self.moment_mstr_dir, "moments")
        self.moment_dir = create_path(moments_dir, self.moment_label)
        self.beliefs_dir = create_path(self.moment_dir, "beliefs")
        self.lessons_dir = create_path(self.moment_dir, "lessons")
        set_dir(x_path=self.moment_dir)
        set_dir(x_path=self.beliefs_dir)
        set_dir(x_path=self.lessons_dir)

    def _get_belief_dir(self, belief_name) -> str:
        return create_path(self.beliefs_dir, belief_name)

    def _get_belief_folder_names(self) -> set:
        beliefs = get_dir_file_strs(
            self.beliefs_dir, include_dirs=True, include_files=False
        )
        return sorted(list(beliefs.keys()))

    # belief administration
    def _set_all_healer_dutys(self, belief_name: BeliefName):
        x_gut = open_gut_file(self.moment_mstr_dir, self.moment_label, belief_name)
        x_gut.cashout()
        for healer_name, healer_dict in x_gut._healers_dict.items():
            for keep_rope in healer_dict.keys():
                create_treasury_db_file(
                    self.moment_mstr_dir,
                    belief_name=belief_name,
                    moment_label=self.moment_label,
                    keep_rope=keep_rope,
                    knot=self.knot,
                )
                save_duty_belief(
                    moment_mstr_dir=self.moment_mstr_dir,
                    belief_name=healer_name,
                    moment_label=self.moment_label,
                    keep_rope=keep_rope,
                    knot=None,
                    duty_belief=x_gut,
                )

    # job belief administration
    def create_empty_belief_from_moment(self, belief_name: BeliefName) -> BeliefUnit:
        return beliefunit_shop(
            belief_name,
            self.moment_label,
            knot=self.knot,
            fund_grain=self.fund_grain,
            respect_grain=self.respect_grain,
            mana_grain=self.mana_grain,
        )

    def create_gut_file_if_none(self, belief_name: BeliefName) -> None:
        if not gut_file_exists(self.moment_mstr_dir, self.moment_label, belief_name):
            empty_belief = self.create_empty_belief_from_moment(belief_name)
            save_gut_file(self.moment_mstr_dir, empty_belief)

    def create_init_job_from_guts(self, belief_name: BeliefName) -> None:
        self.create_gut_file_if_none(belief_name)
        x_gut = open_gut_file(self.moment_mstr_dir, self.moment_label, belief_name)
        x_job = create_listen_basis(x_gut)
        listen_to_agendas_create_init_job_from_guts(self.moment_mstr_dir, x_job)
        save_job_file(self.moment_mstr_dir, x_job)

    def rotate_job(self, belief_name: BeliefName) -> BeliefUnit:
        x_job = open_job_file(self.moment_mstr_dir, self.moment_label, belief_name)
        x_job.cashout()
        # # if beliefunit has healers create job from healers.
        # create beliefunit from debtors roll
        return listen_to_debtors_roll_jobs_into_job(
            self.moment_mstr_dir, self.moment_label, belief_name
        )

    def generate_all_jobs(self) -> None:
        belief_names = self._get_belief_folder_names()
        for belief_name in belief_names:
            self.create_init_job_from_guts(belief_name)

        for _ in range(self.job_listen_rotations):
            for belief_name in belief_names:
                save_job_file(self.moment_mstr_dir, self.rotate_job(belief_name))

    def get_job_file_belief(self, belief_name: BeliefName) -> BeliefUnit:
        return open_job_file(self.moment_mstr_dir, self.moment_label, belief_name)

    # beliefbudhistorys
    def set_beliefbudhistory(self, x_beliefbudhistory: BeliefBudHistory) -> None:
        self.beliefbudhistorys[x_beliefbudhistory.belief_name] = x_beliefbudhistory

    def beliefbudhistory_exists(self, x_belief_name: BeliefName) -> bool:
        return self.beliefbudhistorys.get(x_belief_name) != None

    def get_beliefbudhistory(self, x_belief_name: BeliefName) -> BeliefBudHistory:
        return self.beliefbudhistorys.get(x_belief_name)

    def del_beliefbudhistory(self, x_belief_name: BeliefName) -> None:
        self.beliefbudhistorys.pop(x_belief_name)

    def add_budunit(
        self,
        belief_name: BeliefName,
        bud_time: EpochTime,
        quota: int,
        allow_prev_to_offi_time_max_entry: bool = False,
        celldepth: int = None,
    ):
        self.offi_time_max = get_0_if_None(self.offi_time_max)
        if bud_time < self.offi_time_max and not allow_prev_to_offi_time_max_entry:
            exception_str = f"Cannot set budunit because bud_time {bud_time} is less than MomentUnit.offi_time_max {self.offi_time_max}."
            raise budunit_Exception(exception_str)
        if self.beliefbudhistory_exists(belief_name) is False:
            self.set_beliefbudhistory(beliefbudhistory_shop(belief_name))
        x_beliefbudhistory = self.get_beliefbudhistory(belief_name)
        x_beliefbudhistory.add_bud(bud_time, quota, celldepth)

    def get_budunit(self, belief_name: BeliefName, bud_time: EpochTime) -> BudUnit:
        if not self.get_beliefbudhistory(belief_name):
            return None
        x_beliefbudhistory = self.get_beliefbudhistory(belief_name)
        return x_beliefbudhistory.get_bud(bud_time)

    def to_dict(self, include_paybook: bool = True) -> dict:
        """Returns dict that is serializable to JSON."""

        x_dict = {
            "moment_label": self.moment_label,
            "moment_mstr_dir": self.moment_mstr_dir,
            "knot": self.knot,
            "fund_grain": self.fund_grain,
            "mana_grain": self.mana_grain,
            "beliefbudhistorys": self._get_beliefbudhistorys_dict(),
            "respect_grain": self.respect_grain,
            "epoch": self.epoch.to_dict(),
            "offi_times": list(self.offi_times),
        }
        if include_paybook:
            x_dict["paybook"] = self.paybook.to_dict()
        return x_dict

    def _get_beliefbudhistorys_dict(self) -> dict[BeliefName, dict]:
        return {
            x_bud.belief_name: x_bud.to_dict()
            for x_bud in self.beliefbudhistorys.values()
        }

    def get_beliefbudhistorys_bud_times(self) -> set[EpochTime]:
        all_budunit_bud_times = set()
        for x_beliefbudhistory in self.beliefbudhistorys.values():
            all_budunit_bud_times.update(x_beliefbudhistory.get_bud_times())
        return all_budunit_bud_times

    def set_paypurchase(self, x_paypurchase: TranUnit):
        self.paybook.set_tranunit(
            tranunit=x_paypurchase,
            blocked_tran_times=self.get_beliefbudhistorys_bud_times(),
            offi_time_max=self.offi_time_max,
        )

    def add_paypurchase(
        self,
        belief_name: BeliefName,
        voice_name: VoiceName,
        tran_time: EpochTime,
        amount: FundNum,
        blocked_tran_times: set[EpochTime] = None,
        offi_time_max: EpochTime = None,
    ) -> None:
        self.paybook.add_tranunit(
            belief_name=belief_name,
            voice_name=voice_name,
            tran_time=tran_time,
            amount=amount,
            blocked_tran_times=blocked_tran_times,
            offi_time_max=offi_time_max,
        )

    def paypurchase_exists(
        self, src: BeliefName, dst: VoiceName, x_tran_time: EpochTime
    ) -> bool:
        return self.paybook.tranunit_exists(src, dst, x_tran_time)

    def get_paypurchase(
        self, src: BeliefName, dst: VoiceName, x_tran_time: EpochTime
    ) -> TranUnit:
        return self.paybook.get_tranunit(src, dst, x_tran_time)

    def del_paypurchase(
        self, src: BeliefName, dst: VoiceName, x_tran_time: EpochTime
    ) -> TranUnit:
        return self.paybook.del_tranunit(src, dst, x_tran_time)

    # def set_offi_time(self, offi_time: EpochTime):
    #     self.offi_time = offi_time
    #     if self.offi_time_max < self.offi_time:
    #         self.offi_time_max = self.offi_time

    def set_offi_time_max(self, x_offi_time_max: EpochTime):
        x_tran_times = self.paybook.get_tran_times()
        if x_tran_times != set() and max(x_tran_times) >= x_offi_time_max:
            exception_str = f"Cannot set offi_time_max {x_offi_time_max}, paypurchase with greater tran_time exists"
            raise set_offi_time_max_Exception(exception_str)
        # if self.offi_time > x_offi_time_max:
        #     exception_str = f"Cannot set offi_time_max={x_offi_time_max} because it is less than offi_time={self.offi_time}"
        #     raise set_offi_time_max_Exception(exception_str)
        self.offi_time_max = x_offi_time_max

    # def set_offi_time(
    #     self, offi_time: EpochTime, offi_time_max: EpochTime
    # ):
    #     self.set_offi_time(offi_time)
    #     self.set_offi_time_max(_offi_time_max)

    def set_all_tranbook(self) -> None:
        x_tranunits = copy_deepcopy(self.paybook.tranunits)
        x_tranbook = tranbook_shop(self.moment_label, x_tranunits)
        for belief_name, x_beliefbudhistory in self.beliefbudhistorys.items():
            for x_bud_time, x_budunit in x_beliefbudhistory.buds.items():
                for voice_name, x_amount in x_budunit._bud_voice_nets.items():
                    x_tranbook.add_tranunit(
                        belief_name, voice_name, x_bud_time, x_amount
                    )
        self.all_tranbook = x_tranbook

    def create_buds_root_cells(
        self,
        ote1_dict: dict[BeliefName, dict[EpochTime, SparkInt]],
    ) -> None:
        for belief_name, beliefbudhistory in self.beliefbudhistorys.items():
            for bud_time in beliefbudhistory.buds.keys():
                self._create_bud_root_cell(belief_name, ote1_dict, bud_time)

    def _create_bud_root_cell(
        self,
        belief_name: BeliefName,
        ote1_dict: dict[BeliefName, dict[EpochTime, SparkInt]],
        bud_time: EpochTime,
    ) -> None:
        past_spark_num = _get_ote1_max_past_spark_num(belief_name, ote1_dict, bud_time)
        budunit = self.get_budunit(belief_name, bud_time)
        cellunit = cellunit_shop(
            bud_belief_name=belief_name,
            ancestors=[],
            spark_num=past_spark_num,
            celldepth=budunit.celldepth,
            quota=budunit.quota,
            mana_grain=self.mana_grain,
        )
        root_cell_dir = create_cell_dir_path(
            self.moment_mstr_dir, self.moment_label, belief_name, bud_time, []
        )
        cellunit_save_to_dir(root_cell_dir, cellunit)

    def get_epoch_config(self) -> dict:
        return self.epoch.to_dict()

    def add_epoch_to_gut(self, belief_name: BeliefName) -> None:
        """Adds the epoch to the gut file for the given belief."""
        x_gut = open_gut_file(self.moment_mstr_dir, self.moment_label, belief_name)
        add_epoch_planunit(x_gut, self.get_epoch_config())
        save_gut_file(self.moment_mstr_dir, x_gut)

    def add_epoch_to_guts(self) -> None:
        """Adds the epoch to all gut files."""
        belief_names = self._get_belief_folder_names()
        for belief_name in belief_names:
            self.add_epoch_to_gut(belief_name)


def _get_ote1_max_past_spark_num(
    belief_name: str, ote1_dict: dict[str, dict[str, int]], bud_time: int
) -> SparkInt:
    """Using the grab most recent ote1 spark int before a given bud_time"""
    ote1_belief_dict = ote1_dict.get(belief_name)
    if not ote1_belief_dict:
        return None
    spark_epochtimes = set(ote1_belief_dict.keys())
    if past_epochtimes := {tp for tp in spark_epochtimes if int(tp) <= bud_time}:
        max_past_epochtime = max(past_epochtimes)
        return ote1_belief_dict.get(max_past_epochtime)


def momentunit_shop(
    moment_label: MomentLabel,
    moment_mstr_dir: str,
    epoch: EpochUnit = None,
    offi_times: set[EpochTime] = None,
    knot: KnotTerm = None,
    fund_grain: float = None,
    respect_grain: float = None,
    mana_grain: float = None,
    job_listen_rotations: int = None,
) -> MomentUnit:
    if epoch is None:
        epoch = epochunit_shop()
    if not job_listen_rotations:
        job_listen_rotations = get_default_job_listen_count()
    x_momentunit = MomentUnit(
        moment_label=moment_label,
        moment_mstr_dir=moment_mstr_dir,
        epoch=epoch,
        beliefbudhistorys={},
        paybook=tranbook_shop(moment_label),
        offi_times=get_empty_set_if_None(offi_times),
        knot=default_knot_if_None(knot),
        fund_grain=default_grain_num_if_None(fund_grain),
        respect_grain=default_grain_num_if_None(respect_grain),
        mana_grain=default_grain_num_if_None(mana_grain),
        all_tranbook=tranbook_shop(moment_label),
        job_listen_rotations=job_listen_rotations,
    )
    if x_momentunit.moment_mstr_dir:
        x_momentunit._set_moment_dirs()
    return x_momentunit


def _get_beliefbudhistorys_from_dict(
    beliefbudhistorys_dict: dict,
) -> dict[BeliefName, BeliefBudHistory]:
    return {
        x_belief_name: get_beliefbudhistory_from_dict(beliefbudhistory_dict)
        for x_belief_name, beliefbudhistory_dict in beliefbudhistorys_dict.items()
    }


def get_momentunit_from_dict(moment_dict: dict) -> MomentUnit:
    x_moment_label = moment_dict.get("moment_label")
    x_moment = momentunit_shop(
        moment_label=x_moment_label,
        moment_mstr_dir=moment_dict.get("moment_mstr_dir"),
        offi_times=set(moment_dict.get("offi_times")),
        knot=moment_dict.get("knot"),
        fund_grain=moment_dict.get("fund_grain"),
        respect_grain=moment_dict.get("respect_grain"),
        mana_grain=moment_dict.get("mana_grain"),
    )
    moment_dict_epoch_value = moment_dict.get("epoch")
    if moment_dict_epoch_value:
        x_moment.epoch = epochunit_shop(moment_dict_epoch_value)
    else:
        x_moment.epoch = epochunit_shop(None)
    x_moment.beliefbudhistorys = _get_beliefbudhistorys_from_dict(
        moment_dict.get("beliefbudhistorys")
    )
    x_moment.paybook = get_tranbook_from_dict(moment_dict.get("paybook"))
    return x_moment


def get_default_path_momentunit(
    moment_mstr_dir: str, moment_label: MomentLabel
) -> MomentUnit:
    moment_json_path = create_moment_json_path(moment_mstr_dir, moment_label)
    x_momentunit = get_momentunit_from_dict(open_json(moment_json_path))
    x_momentunit.moment_mstr_dir = moment_mstr_dir
    x_momentunit._set_moment_dirs()
    return x_momentunit
