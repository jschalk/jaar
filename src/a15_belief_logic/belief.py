from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_dict_from_json,
    get_empty_set_if_None,
    get_json_from_dict,
)
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_dir_file_strs,
    open_file,
    set_dir,
)
from src.a01_term_logic.term import (
    BeliefLabel,
    BelieverName,
    EventInt,
    PersonName,
    RopeTerm,
    default_knot_if_None,
)
from src.a02_finance_logic.finance_config import (
    BitNum,
    FundIota,
    FundNum,
    PennyNum,
    TimeLinePoint,
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a06_believer_logic.believer import BelieverUnit, believerunit_shop
from src.a07_timeline_logic.timeline import (
    TimeLineUnit,
    add_newtimeline_planunit,
    timelineunit_shop,
)
from src.a11_bud_logic.bud import (
    BrokerUnit,
    BudUnit,
    TranBook,
    TranUnit,
    brokerunit_shop,
    get_brokerunit_from_dict,
    get_tranbook_from_dict,
    tranbook_shop,
)
from src.a11_bud_logic.cell import cellunit_shop
from src.a12_hub_toolbox.a12_path import create_belief_json_path, create_cell_dir_path
from src.a12_hub_toolbox.basis_believers import create_listen_basis, get_default_job
from src.a12_hub_toolbox.hub_tool import (
    cellunit_save_to_dir,
    gut_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a13_believer_listen_logic.listen import (
    create_vision_file_from_duty_file,
    listen_to_agendas_create_init_job_from_guts,
    listen_to_debtors_roll_jobs_into_job,
    listen_to_speaker_agenda,
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
class BeliefUnit:
    """Data pipelines:
    pipeline1: packs->gut
    pipeline2: gut->dutys
    pipeline3: duty->vision
    pipeline4: vision->job
    pipeline5: gut->job (direct)
    pipeline6: gut->vision->job (through visions)
    pipeline7: packs->job (could be 5 of 6)
    """

    belief_label: BeliefLabel = None
    belief_mstr_dir: str = None
    timeline: TimeLineUnit = None
    brokerunits: dict[BelieverName, BrokerUnit] = None
    paybook: TranBook = None
    offi_times: set[TimeLinePoint] = None
    knot: str = None
    fund_iota: FundIota = None
    respect_bit: BitNum = None
    penny: PennyNum = None
    job_listen_rotations: int = None
    _offi_time_max: TimeLinePoint = None
    _belief_dir: str = None
    _believers_dir: str = None
    _packs_dir: str = None
    _all_tranbook: TranBook = None

    # directory setup
    def _set_belief_dirs(self):
        beliefs_dir = create_path(self.belief_mstr_dir, "beliefs")
        self._belief_dir = create_path(beliefs_dir, self.belief_label)
        self._believers_dir = create_path(self._belief_dir, "believers")
        self._packs_dir = create_path(self._belief_dir, "packs")
        set_dir(x_path=self._belief_dir)
        set_dir(x_path=self._believers_dir)
        set_dir(x_path=self._packs_dir)

    def _get_believer_dir(self, believer_name):
        return create_path(self._believers_dir, believer_name)

    def _get_believer_folder_names(self) -> set:
        believers = get_dir_file_strs(
            self._believers_dir, include_dirs=True, include_files=False
        )
        return sorted(list(believers.keys()))

    # believer management
    def _set_all_healer_dutys(self, believer_name: BelieverName):
        x_gut = open_gut_file(self.belief_mstr_dir, self.belief_label, believer_name)
        x_gut.settle_believer()
        for healer_name, healer_dict in x_gut._healers_dict.items():
            healer_hubunit = hubunit_shop(
                self.belief_mstr_dir,
                self.belief_label,
                healer_name,
                keep_rope=None,
                # "duty_vision",
                knot=self.knot,
                respect_bit=self.respect_bit,
            )
            for keep_rope in healer_dict.keys():
                self._set_believer_duty(healer_hubunit, keep_rope, x_gut)

    def _set_believer_duty(
        self,
        healer_hubunit: HubUnit,
        keep_rope: RopeTerm,
        gut_believer: BelieverUnit,
    ) -> None:
        healer_hubunit.keep_rope = keep_rope
        healer_hubunit.create_treasury_db_file()
        healer_hubunit.save_duty_believer(gut_believer)

    def generate_healers_authored_job(
        self, believer_name: BelieverName, x_gut: BelieverUnit
    ) -> BelieverUnit:
        x_job = get_default_job(x_gut)
        for healer_name, healer_dict in x_gut._healers_dict.items():
            healer_hubunit = hubunit_shop(
                belief_mstr_dir=self.belief_mstr_dir,
                belief_label=self.belief_label,
                believer_name=healer_name,
                keep_rope=None,
                knot=self.knot,
                respect_bit=self.respect_bit,
            )
            healer_hubunit.create_gut_treasury_db_files()
            for keep_rope in healer_dict.keys():
                keep_hubunit = hubunit_shop(
                    belief_mstr_dir=self.belief_mstr_dir,
                    belief_label=self.belief_label,
                    believer_name=healer_name,
                    keep_rope=keep_rope,
                    # "duty_vision",
                    knot=self.knot,
                    respect_bit=self.respect_bit,
                )
                keep_hubunit.save_duty_believer(x_gut)
                create_vision_file_from_duty_file(keep_hubunit, believer_name)
                x_vision = keep_hubunit.get_vision_believer(believer_name)
                x_job = listen_to_speaker_agenda(x_job, x_vision)
        return x_job

    # job believer management
    def create_empty_believer_from_belief(
        self, believer_name: BelieverName
    ) -> BelieverUnit:
        return believerunit_shop(
            believer_name,
            self.belief_label,
            knot=self.knot,
            fund_iota=self.fund_iota,
            respect_bit=self.respect_bit,
            penny=self.penny,
        )

    def create_gut_file_if_none(self, believer_name: BelieverName) -> None:
        if not gut_file_exists(self.belief_mstr_dir, self.belief_label, believer_name):
            empty_believer = self.create_empty_believer_from_belief(believer_name)
            save_gut_file(self.belief_mstr_dir, empty_believer)

    def create_init_job_from_guts(self, believer_name: BelieverName) -> None:
        self.create_gut_file_if_none(believer_name)
        x_gut = open_gut_file(self.belief_mstr_dir, self.belief_label, believer_name)
        x_job = create_listen_basis(x_gut)
        listen_to_agendas_create_init_job_from_guts(self.belief_mstr_dir, x_job)
        save_job_file(self.belief_mstr_dir, x_job)

    def rotate_job(self, believer_name: BelieverName) -> BelieverUnit:
        x_job = open_job_file(self.belief_mstr_dir, self.belief_label, believer_name)
        x_job.settle_believer()
        # # if believerunit has healers create job from healers.
        # if len(x_gut._healers_dict) > 0:
        #     return self.generate_healers_authored_job(believer_name, x_gut)
        # create believerunit from debtors roll
        return listen_to_debtors_roll_jobs_into_job(
            self.belief_mstr_dir, self.belief_label, believer_name
        )

    def generate_all_jobs(self) -> None:
        believer_names = self._get_believer_folder_names()
        for believer_name in believer_names:
            self.create_init_job_from_guts(believer_name)

        for _ in range(self.job_listen_rotations):
            for believer_name in believer_names:
                save_job_file(self.belief_mstr_dir, self.rotate_job(believer_name))

    def get_job_file_believer(self, believer_name: BelieverName) -> BelieverUnit:
        return open_job_file(self.belief_mstr_dir, self.belief_label, believer_name)

    # brokerunits
    def set_brokerunit(self, x_brokerunit: BrokerUnit) -> None:
        self.brokerunits[x_brokerunit.believer_name] = x_brokerunit

    def brokerunit_exists(self, x_believer_name: BelieverName) -> bool:
        return self.brokerunits.get(x_believer_name) != None

    def get_brokerunit(self, x_believer_name: BelieverName) -> BrokerUnit:
        return self.brokerunits.get(x_believer_name)

    def del_brokerunit(self, x_believer_name: BelieverName) -> None:
        self.brokerunits.pop(x_believer_name)

    def add_budunit(
        self,
        believer_name: BelieverName,
        bud_time: TimeLinePoint,
        quota: int,
        allow_prev_to_offi_time_max_entry: bool = False,
        celldepth: int = None,
    ):
        self._offi_time_max = get_0_if_None(self._offi_time_max)
        if bud_time < self._offi_time_max and not allow_prev_to_offi_time_max_entry:
            exception_str = f"Cannot set budunit because bud_time {bud_time} is less than BeliefUnit._offi_time_max {self._offi_time_max}."
            raise budunit_Exception(exception_str)
        if self.brokerunit_exists(believer_name) is False:
            self.set_brokerunit(brokerunit_shop(believer_name))
        x_brokerunit = self.get_brokerunit(believer_name)
        x_brokerunit.add_bud(bud_time, quota, celldepth)

    def get_budunit(
        self, believer_name: BelieverName, bud_time: TimeLinePoint
    ) -> BudUnit:
        if not self.get_brokerunit(believer_name):
            return None
        x_brokerunit = self.get_brokerunit(believer_name)
        return x_brokerunit.get_bud(bud_time)

    def get_dict(self, include_paybook: bool = True) -> dict:
        x_dict = {
            "belief_label": self.belief_label,
            "belief_mstr_dir": self.belief_mstr_dir,
            "knot": self.knot,
            "fund_iota": self.fund_iota,
            "penny": self.penny,
            "brokerunits": self._get_brokerunits_dict(),
            "respect_bit": self.respect_bit,
            "timeline": self.timeline.get_dict(),
            "offi_times": list(self.offi_times),
        }
        if include_paybook:
            x_dict["paybook"] = self.paybook.get_dict()
        return x_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())

    def _get_brokerunits_dict(self) -> dict[BelieverName, dict]:
        return {
            x_bud.believer_name: x_bud.get_dict() for x_bud in self.brokerunits.values()
        }

    def get_brokerunits_bud_times(self) -> set[TimeLinePoint]:
        all_budunit_bud_times = set()
        for x_brokerunit in self.brokerunits.values():
            all_budunit_bud_times.update(x_brokerunit.get_bud_times())
        return all_budunit_bud_times

    def set_paypurchase(self, x_paypurchase: TranUnit):
        self.paybook.set_tranunit(
            tranunit=x_paypurchase,
            blocked_tran_times=self.get_brokerunits_bud_times(),
            _offi_time_max=self._offi_time_max,
        )

    def add_paypurchase(
        self,
        believer_name: BelieverName,
        person_name: PersonName,
        tran_time: TimeLinePoint,
        amount: FundNum,
        blocked_tran_times: set[TimeLinePoint] = None,
        _offi_time_max: TimeLinePoint = None,
    ) -> None:
        self.paybook.add_tranunit(
            believer_name=believer_name,
            person_name=person_name,
            tran_time=tran_time,
            amount=amount,
            blocked_tran_times=blocked_tran_times,
            _offi_time_max=_offi_time_max,
        )

    def paypurchase_exists(
        self, src: BelieverName, dst: PersonName, x_tran_time: TimeLinePoint
    ) -> bool:
        return self.paybook.tranunit_exists(src, dst, x_tran_time)

    def get_paypurchase(
        self, src: BelieverName, dst: PersonName, x_tran_time: TimeLinePoint
    ) -> TranUnit:
        return self.paybook.get_tranunit(src, dst, x_tran_time)

    def del_paypurchase(
        self, src: BelieverName, dst: PersonName, x_tran_time: TimeLinePoint
    ) -> TranUnit:
        return self.paybook.del_tranunit(src, dst, x_tran_time)

    # def set_offi_time(self, offi_time: TimeLinePoint):
    #     self.offi_time = offi_time
    #     if self._offi_time_max < self.offi_time:
    #         self._offi_time_max = self.offi_time

    def set_offi_time_max(self, x_offi_time_max: TimeLinePoint):
        x_tran_times = self.paybook.get_tran_times()
        if x_tran_times != set() and max(x_tran_times) >= x_offi_time_max:
            exception_str = f"Cannot set _offi_time_max {x_offi_time_max}, paypurchase with greater tran_time exists"
            raise set_offi_time_max_Exception(exception_str)
        # if self.offi_time > x_offi_time_max:
        #     exception_str = f"Cannot set _offi_time_max={x_offi_time_max} because it is less than offi_time={self.offi_time}"
        #     raise set_offi_time_max_Exception(exception_str)
        self._offi_time_max = x_offi_time_max

    # def set_offi_time(
    #     self, offi_time: TimeLinePoint, _offi_time_max: TimeLinePoint
    # ):
    #     self.set_offi_time(offi_time)
    #     self.set_offi_time_max(_offi_time_max)

    def set_all_tranbook(self) -> None:
        x_tranunits = copy_deepcopy(self.paybook.tranunits)
        x_tranbook = tranbook_shop(self.belief_label, x_tranunits)
        for believer_name, x_brokerunit in self.brokerunits.items():
            for x_bud_time, x_budunit in x_brokerunit.buds.items():
                for person_name, x_amount in x_budunit._bud_person_nets.items():
                    x_tranbook.add_tranunit(
                        believer_name, person_name, x_bud_time, x_amount
                    )
        self._all_tranbook = x_tranbook

    def create_buds_root_cells(
        self,
        ote1_dict: dict[BelieverName, dict[TimeLinePoint, EventInt]],
    ) -> None:
        for believer_name, brokerunit in self.brokerunits.items():
            for bud_time in brokerunit.buds.keys():
                self._create_bud_root_cell(believer_name, ote1_dict, bud_time)

    def _create_bud_root_cell(
        self,
        believer_name: BelieverName,
        ote1_dict: dict[BelieverName, dict[TimeLinePoint, EventInt]],
        bud_time: TimeLinePoint,
    ) -> None:
        past_event_int = _get_ote1_max_past_event_int(
            believer_name, ote1_dict, bud_time
        )
        budunit = self.get_budunit(believer_name, bud_time)
        cellunit = cellunit_shop(
            bud_believer_name=believer_name,
            ancestors=[],
            event_int=past_event_int,
            celldepth=budunit.celldepth,
            quota=budunit.quota,
            penny=self.penny,
        )
        root_cell_dir = create_cell_dir_path(
            self.belief_mstr_dir, self.belief_label, believer_name, bud_time, []
        )
        cellunit_save_to_dir(root_cell_dir, cellunit)

    def get_timeline_config(self) -> dict:
        return self.timeline.get_dict()

    def add_timeline_to_gut(self, believer_name: BelieverName) -> None:
        """Adds the timeline to the gut file for the given believer."""
        x_gut = open_gut_file(self.belief_mstr_dir, self.belief_label, believer_name)
        add_newtimeline_planunit(x_gut, self.get_timeline_config())
        save_gut_file(self.belief_mstr_dir, x_gut)

    def add_timeline_to_guts(self) -> None:
        """Adds the timeline to all gut files."""
        believer_names = self._get_believer_folder_names()
        for believer_name in believer_names:
            self.add_timeline_to_gut(believer_name)


def _get_ote1_max_past_event_int(
    believer_name: str, ote1_dict: dict[str, dict[str, int]], bud_time: int
) -> EventInt:
    """Using the grab most recent ote1 event int before a given bud_time"""
    ote1_believer_dict = ote1_dict.get(believer_name)
    if not ote1_believer_dict:
        return None
    event_timepoints = set(ote1_believer_dict.keys())
    if past_timepoints := {tp for tp in event_timepoints if int(tp) <= bud_time}:
        max_past_timepoint = max(past_timepoints)
        return ote1_believer_dict.get(max_past_timepoint)


def beliefunit_shop(
    belief_label: BeliefLabel,
    belief_mstr_dir: str,
    timeline: TimeLineUnit = None,
    offi_times: set[TimeLinePoint] = None,
    knot: str = None,
    fund_iota: float = None,
    respect_bit: float = None,
    penny: float = None,
    job_listen_rotations: int = None,
) -> BeliefUnit:
    if timeline is None:
        timeline = timelineunit_shop()
    if not job_listen_rotations:
        job_listen_rotations = get_default_job_listen_count()
    x_beliefunit = BeliefUnit(
        belief_label=belief_label,
        belief_mstr_dir=belief_mstr_dir,
        timeline=timeline,
        brokerunits={},
        paybook=tranbook_shop(belief_label),
        offi_times=get_empty_set_if_None(offi_times),
        knot=default_knot_if_None(knot),
        fund_iota=default_fund_iota_if_None(fund_iota),
        respect_bit=default_RespectBit_if_None(respect_bit),
        penny=filter_penny(penny),
        _all_tranbook=tranbook_shop(belief_label),
        job_listen_rotations=job_listen_rotations,
    )
    if x_beliefunit.belief_mstr_dir:
        x_beliefunit._set_belief_dirs()
    return x_beliefunit


def _get_brokerunits_from_dict(
    brokerunits_dict: dict,
) -> dict[BelieverName, BrokerUnit]:
    return {
        x_believer_name: get_brokerunit_from_dict(brokerunit_dict)
        for x_believer_name, brokerunit_dict in brokerunits_dict.items()
    }


def get_from_dict(belief_dict: dict) -> BeliefUnit:
    x_belief_label = belief_dict.get("belief_label")
    x_belief = beliefunit_shop(
        belief_label=x_belief_label,
        belief_mstr_dir=belief_dict.get("belief_mstr_dir"),
        offi_times=set(belief_dict.get("offi_times")),
        knot=belief_dict.get("knot"),
        fund_iota=belief_dict.get("fund_iota"),
        respect_bit=belief_dict.get("respect_bit"),
        penny=belief_dict.get("penny"),
    )
    belief_dict_timeline_value = belief_dict.get("timeline")
    if belief_dict_timeline_value:
        x_belief.timeline = timelineunit_shop(belief_dict_timeline_value)
    else:
        x_belief.timeline = timelineunit_shop(None)
    x_belief.brokerunits = _get_brokerunits_from_dict(belief_dict.get("brokerunits"))
    x_belief.paybook = get_tranbook_from_dict(belief_dict.get("paybook"))
    return x_belief


def get_from_json(x_belief_json: str) -> BeliefUnit:
    return get_from_dict(get_dict_from_json(x_belief_json))


def get_default_path_beliefunit(
    belief_mstr_dir: str, belief_label: BeliefLabel
) -> BeliefUnit:
    belief_json_path = create_belief_json_path(belief_mstr_dir, belief_label)
    x_beliefunit = get_from_json(open_file(belief_json_path))
    x_beliefunit.belief_mstr_dir = belief_mstr_dir
    x_beliefunit._set_belief_dirs()
    return x_beliefunit
