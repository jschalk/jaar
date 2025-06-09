from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import Connection, connect as sqlite3_connect
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_dict_from_json,
    get_empty_set_if_None,
    get_json_from_dict,
)
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    delete_dir,
    get_dir_file_strs,
    open_file,
    set_dir,
)
from src.a01_term_logic.term import (
    AcctName,
    EventInt,
    OwnerName,
    VowLabel,
    WayTerm,
    default_bridge_if_None,
)
from src.a02_finance_logic.deal import (
    BrokerUnit,
    DealUnit,
    TranBook,
    TranUnit,
    brokerunit_shop,
    get_brokerunit_from_dict,
    get_tranbook_from_dict,
    tranbook_shop,
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
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a07_calendar_logic.chrono import TimeLineUnit, timelineunit_shop
from src.a11_deal_cell_logic.cell import cellunit_shop
from src.a12_hub_tools.basis_plans import create_listen_basis, get_default_job
from src.a12_hub_tools.hub_path import create_cell_dir_path, create_vow_json_path
from src.a12_hub_tools.hub_tool import (
    cellunit_save_to_dir,
    gut_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from src.a13_plan_listen_logic.listen import (
    create_vision_file_from_duty_file,
    listen_to_agendas_create_init_job_from_guts,
    listen_to_debtors_roll_jobs_into_job,
    listen_to_speaker_agenda,
)
from src.a15_vow_logic.journal_sqlstr import get_create_table_if_not_exist_sqlstrs


def get_default_job_listen_count() -> int:
    return 3


class dealunit_Exception(Exception):
    pass


class set_paypurchase_Exception(Exception):
    pass


class set_offi_time_max_Exception(Exception):
    pass


@dataclass
class VowUnit:
    """Data pipelines:
    pipeline1: packs->gut
    pipeline2: gut->dutys
    pipeline3: duty->vision
    pipeline4: vision->job
    pipeline5: gut->job (direct)
    pipeline6: gut->vision->job (through visions)
    pipeline7: packs->job (could be 5 of 6)
    """

    vow_label: VowLabel = None
    vow_mstr_dir: str = None
    timeline: TimeLineUnit = None
    brokerunits: dict[OwnerName, BrokerUnit] = None
    paybook: TranBook = None
    offi_times: set[TimeLinePoint] = None
    bridge: str = None
    fund_iota: FundIota = None
    respect_bit: BitNum = None
    penny: PennyNum = None
    job_listen_rotations: int = None
    _offi_time_max: TimeLinePoint = None
    _vow_dir: str = None
    _owners_dir: str = None
    _journal_db: str = None
    _packs_dir: str = None
    _all_tranbook: TranBook = None

    # directory setup
    def _set_vow_dirs(self, in_memory_journal: bool = None):
        vows_dir = create_path(self.vow_mstr_dir, "vows")
        self._vow_dir = create_path(vows_dir, self.vow_label)
        self._owners_dir = create_path(self._vow_dir, "owners")
        self._packs_dir = create_path(self._vow_dir, "packs")
        set_dir(x_path=self._vow_dir)
        set_dir(x_path=self._owners_dir)
        set_dir(x_path=self._packs_dir)
        self._create_journal_db(in_memory=in_memory_journal)

    def _get_owner_dir(self, owner_name):
        return create_path(self._owners_dir, owner_name)

    def _get_owner_folder_names(self) -> set:
        owners = get_dir_file_strs(
            self._owners_dir, include_dirs=True, include_files=False
        )
        return sorted(list(owners.keys()))

    # database
    def get_journal_db_path(self) -> str:
        vows_dir = create_path(self.vow_mstr_dir, "vows")
        vow_dir = create_path(vows_dir, self.vow_label)
        return create_path(vow_dir, "journal.db")

    def _create_journal_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> None:
        journal_file_new = False
        if overwrite:
            journal_file_new = True
            self._delete_journal()

        if in_memory:
            if self._journal_db is None:
                journal_file_new = True
            self._journal_db = sqlite3_connect(":memory:")
        else:
            conn = sqlite3_connect(self.get_journal_db_path())
            conn.close()

        if journal_file_new:
            with self.get_journal_conn() as journal_conn:
                for sqlstr in get_create_table_if_not_exist_sqlstrs():
                    journal_conn.execute(sqlstr)

    def _delete_journal(self):
        self._journal_db = None
        delete_dir(dir=self.get_journal_db_path())

    def get_journal_conn(self) -> Connection:
        if self._journal_db is None:
            return sqlite3_connect(self.get_journal_db_path())
        else:
            return self._journal_db

    # owner management
    def _set_all_healer_dutys(self, owner_name: OwnerName):
        x_gut = open_gut_file(self.vow_mstr_dir, self.vow_label, owner_name)
        x_gut.settle_plan()
        for healer_name, healer_dict in x_gut._healers_dict.items():
            healer_hubunit = hubunit_shop(
                self.vow_mstr_dir,
                self.vow_label,
                healer_name,
                keep_way=None,
                # "duty_vision",
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            for keep_way in healer_dict.keys():
                self._set_owner_duty(healer_hubunit, keep_way, x_gut)

    def _set_owner_duty(
        self,
        healer_hubunit: HubUnit,
        keep_way: WayTerm,
        gut_plan: PlanUnit,
    ) -> None:
        healer_hubunit.keep_way = keep_way
        healer_hubunit.create_treasury_db_file()
        healer_hubunit.save_duty_plan(gut_plan)

    def generate_healers_authored_job(
        self, owner_name: OwnerName, x_gut: PlanUnit
    ) -> PlanUnit:
        x_job = get_default_job(x_gut)
        for healer_name, healer_dict in x_gut._healers_dict.items():
            healer_hubunit = hubunit_shop(
                vow_mstr_dir=self.vow_mstr_dir,
                vow_label=self.vow_label,
                owner_name=healer_name,
                keep_way=None,
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            healer_hubunit.create_gut_treasury_db_files()
            for keep_way in healer_dict.keys():
                keep_hubunit = hubunit_shop(
                    vow_mstr_dir=self.vow_mstr_dir,
                    vow_label=self.vow_label,
                    owner_name=healer_name,
                    keep_way=keep_way,
                    # "duty_vision",
                    bridge=self.bridge,
                    respect_bit=self.respect_bit,
                )
                keep_hubunit.save_duty_plan(x_gut)
                create_vision_file_from_duty_file(keep_hubunit, owner_name)
                x_vision = keep_hubunit.get_vision_plan(owner_name)
                x_job = listen_to_speaker_agenda(x_job, x_vision)
        return x_job

    # job plan management
    def create_empty_plan_from_vow(self, owner_name: OwnerName) -> PlanUnit:
        return planunit_shop(
            owner_name,
            self.vow_label,
            bridge=self.bridge,
            fund_iota=self.fund_iota,
            respect_bit=self.respect_bit,
            penny=self.penny,
        )

    def create_gut_file_if_none(self, owner_name: OwnerName) -> None:
        if not gut_file_exists(self.vow_mstr_dir, self.vow_label, owner_name):
            empty_plan = self.create_empty_plan_from_vow(owner_name)
            save_gut_file(self.vow_mstr_dir, empty_plan)

    def create_init_job_from_guts(self, owner_name: OwnerName) -> None:
        self.create_gut_file_if_none(owner_name)
        x_gut = open_gut_file(self.vow_mstr_dir, self.vow_label, owner_name)
        x_job = create_listen_basis(x_gut)
        listen_to_agendas_create_init_job_from_guts(self.vow_mstr_dir, x_job)
        save_job_file(self.vow_mstr_dir, x_job)

    def rotate_job(self, owner_name: OwnerName) -> PlanUnit:
        x_job = open_job_file(self.vow_mstr_dir, self.vow_label, owner_name)
        x_job.settle_plan()
        # # if planunit has healers create job from healers.
        # if len(x_gut._healers_dict) > 0:
        #     return self.generate_healers_authored_job(owner_name, x_gut)
        # create planunit from debtors roll
        return listen_to_debtors_roll_jobs_into_job(
            self.vow_mstr_dir, self.vow_label, owner_name
        )

    def generate_all_jobs(self) -> None:
        owner_names = self._get_owner_folder_names()
        for owner_name in owner_names:
            self.create_init_job_from_guts(owner_name)

        for _ in range(self.job_listen_rotations):
            for owner_name in owner_names:
                save_job_file(self.vow_mstr_dir, self.rotate_job(owner_name))

    def get_job_file_plan(self, owner_name: OwnerName) -> PlanUnit:
        return open_job_file(self.vow_mstr_dir, self.vow_label, owner_name)

    # brokerunits
    def set_brokerunit(self, x_brokerunit: BrokerUnit) -> None:
        self.brokerunits[x_brokerunit.owner_name] = x_brokerunit

    def brokerunit_exists(self, x_owner_name: OwnerName) -> bool:
        return self.brokerunits.get(x_owner_name) != None

    def get_brokerunit(self, x_owner_name: OwnerName) -> BrokerUnit:
        return self.brokerunits.get(x_owner_name)

    def del_brokerunit(self, x_owner_name: OwnerName) -> None:
        self.brokerunits.pop(x_owner_name)

    def add_dealunit(
        self,
        owner_name: OwnerName,
        deal_time: TimeLinePoint,
        quota: int,
        allow_prev_to_offi_time_max_entry: bool = False,
        celldepth: int = None,
    ):
        self._offi_time_max = get_0_if_None(self._offi_time_max)
        if deal_time < self._offi_time_max and not allow_prev_to_offi_time_max_entry:
            exception_str = f"Cannot set dealunit because deal_time {deal_time} is less than VowUnit._offi_time_max {self._offi_time_max}."
            raise dealunit_Exception(exception_str)
        if self.brokerunit_exists(owner_name) is False:
            self.set_brokerunit(brokerunit_shop(owner_name))
        x_brokerunit = self.get_brokerunit(owner_name)
        x_brokerunit.add_deal(deal_time, quota, celldepth)

    def get_dealunit(self, owner_name: OwnerName, deal_time: TimeLinePoint) -> DealUnit:
        if not self.get_brokerunit(owner_name):
            return None
        x_brokerunit = self.get_brokerunit(owner_name)
        return x_brokerunit.get_deal(deal_time)

    def get_dict(self, include_paybook: bool = True) -> dict:
        x_dict = {
            "vow_label": self.vow_label,
            "bridge": self.bridge,
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

    def _get_brokerunits_dict(self) -> dict[OwnerName, dict]:
        return {
            x_deal.owner_name: x_deal.get_dict() for x_deal in self.brokerunits.values()
        }

    def get_brokerunits_deal_times(self) -> set[TimeLinePoint]:
        all_dealunit_deal_times = set()
        for x_brokerunit in self.brokerunits.values():
            all_dealunit_deal_times.update(x_brokerunit.get_deal_times())
        return all_dealunit_deal_times

    def set_paypurchase(self, x_paypurchase: TranUnit):
        self.paybook.set_tranunit(
            tranunit=x_paypurchase,
            blocked_tran_times=self.get_brokerunits_deal_times(),
            _offi_time_max=self._offi_time_max,
        )

    def add_paypurchase(
        self,
        owner_name: OwnerName,
        acct_name: AcctName,
        tran_time: TimeLinePoint,
        amount: FundNum,
        blocked_tran_times: set[TimeLinePoint] = None,
        _offi_time_max: TimeLinePoint = None,
    ) -> None:
        self.paybook.add_tranunit(
            owner_name=owner_name,
            acct_name=acct_name,
            tran_time=tran_time,
            amount=amount,
            blocked_tran_times=blocked_tran_times,
            _offi_time_max=_offi_time_max,
        )

    def paypurchase_exists(
        self, src: AcctName, dst: AcctName, x_tran_time: TimeLinePoint
    ) -> bool:
        return self.paybook.tranunit_exists(src, dst, x_tran_time)

    def get_paypurchase(
        self, src: AcctName, dst: AcctName, x_tran_time: TimeLinePoint
    ) -> TranUnit:
        return self.paybook.get_tranunit(src, dst, x_tran_time)

    def del_paypurchase(
        self, src: AcctName, dst: AcctName, x_tran_time: TimeLinePoint
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
        x_tranbook = tranbook_shop(self.vow_label, x_tranunits)
        for owner_name, x_brokerunit in self.brokerunits.items():
            for x_deal_time, x_dealunit in x_brokerunit.deals.items():
                for acct_name, x_amount in x_dealunit._deal_acct_nets.items():
                    x_tranbook.add_tranunit(
                        owner_name, acct_name, x_deal_time, x_amount
                    )
        self._all_tranbook = x_tranbook

    def create_deals_root_cells(
        self,
        ote1_dict: dict[OwnerName, dict[TimeLinePoint, EventInt]],
    ) -> None:
        for owner_name, brokerunit in self.brokerunits.items():
            for deal_time in brokerunit.deals.keys():
                self._create_deal_root_cell(owner_name, ote1_dict, deal_time)

    def _create_deal_root_cell(
        self,
        owner_name: OwnerName,
        ote1_dict: dict[OwnerName, dict[TimeLinePoint, EventInt]],
        deal_time: TimeLinePoint,
    ) -> None:
        past_event_int = _get_ote1_max_past_event_int(owner_name, ote1_dict, deal_time)
        dealunit = self.get_dealunit(owner_name, deal_time)
        cellunit = cellunit_shop(
            deal_owner_name=owner_name,
            ancestors=[],
            event_int=past_event_int,
            celldepth=dealunit.celldepth,
            quota=dealunit.quota,
            penny=self.penny,
        )
        root_cell_dir = create_cell_dir_path(
            self.vow_mstr_dir, self.vow_label, owner_name, deal_time, []
        )
        cellunit_save_to_dir(root_cell_dir, cellunit)


def _get_ote1_max_past_event_int(
    owner_name: str, ote1_dict: dict[str, dict[str, int]], deal_time: int
) -> EventInt:
    """Using the vow_ote1_agg grab most recent event int before a given deal_time"""
    ote1_owner_dict = ote1_dict.get(owner_name)
    if not ote1_owner_dict:
        return None
    event_timepoints = set(ote1_owner_dict.keys())
    if past_timepoints := {tp for tp in event_timepoints if int(tp) <= deal_time}:
        max_past_timepoint = max(past_timepoints)
        return ote1_owner_dict.get(max_past_timepoint)


# TODO get rid of this function
def get_module_temp_dir():
    return "src/a15_vow_logic/_test_util/vow_mstr"


def vowunit_shop(
    vow_label: VowLabel,
    vow_mstr_dir: str = None,
    timeline: TimeLineUnit = None,
    offi_times: set[TimeLinePoint] = None,
    in_memory_journal: bool = None,
    bridge: str = None,
    fund_iota: float = None,
    respect_bit: float = None,
    penny: float = None,
    job_listen_rotations: int = None,
) -> VowUnit:
    if timeline is None:
        timeline = timelineunit_shop()
    if vow_mstr_dir is None:
        vow_mstr_dir = get_module_temp_dir()
    if not job_listen_rotations:
        job_listen_rotations = get_default_job_listen_count()
    x_vowunit = VowUnit(
        vow_label=vow_label,
        vow_mstr_dir=vow_mstr_dir,
        timeline=timeline,
        brokerunits={},
        paybook=tranbook_shop(vow_label),
        offi_times=get_empty_set_if_None(offi_times),
        bridge=default_bridge_if_None(bridge),
        fund_iota=default_fund_iota_if_None(fund_iota),
        respect_bit=default_RespectBit_if_None(respect_bit),
        penny=filter_penny(penny),
        _all_tranbook=tranbook_shop(vow_label),
        job_listen_rotations=job_listen_rotations,
    )
    x_vowunit._set_vow_dirs(in_memory_journal=in_memory_journal)
    return x_vowunit


def _get_brokerunits_from_dict(brokerunits_dict: dict) -> dict[OwnerName, BrokerUnit]:
    return {
        x_owner_name: get_brokerunit_from_dict(brokerunit_dict)
        for x_owner_name, brokerunit_dict in brokerunits_dict.items()
    }


def get_from_dict(vow_dict: dict) -> VowUnit:
    x_vow_label = vow_dict.get("vow_label")
    x_vow = vowunit_shop(
        vow_label=x_vow_label,
        vow_mstr_dir=None,
        offi_times=set(vow_dict.get("offi_times")),
        bridge=vow_dict.get("bridge"),
        fund_iota=vow_dict.get("fund_iota"),
        respect_bit=vow_dict.get("respect_bit"),
        penny=vow_dict.get("penny"),
    )
    vow_dict_timeline_value = vow_dict.get("timeline")
    if vow_dict_timeline_value:
        x_vow.timeline = timelineunit_shop(vow_dict_timeline_value)
    else:
        x_vow.timeline = timelineunit_shop(None)
    x_vow.brokerunits = _get_brokerunits_from_dict(vow_dict.get("brokerunits"))
    x_vow.paybook = get_tranbook_from_dict(vow_dict.get("paybook"))
    return x_vow


def get_from_json(x_vow_json: str) -> VowUnit:
    return get_from_dict(get_dict_from_json(x_vow_json))


def get_from_default_path(vow_mstr_dir: str, vow_label: VowLabel) -> VowUnit:
    vow_json_path = create_vow_json_path(vow_mstr_dir, vow_label)
    x_vowunit = get_from_json(open_file(vow_json_path))
    x_vowunit.vow_mstr_dir = vow_mstr_dir
    x_vowunit._set_vow_dirs()
    return x_vowunit
