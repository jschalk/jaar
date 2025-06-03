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
from src.a01_term_logic.way import (
    AcctName,
    EventInt,
    FiscLabel,
    OwnerName,
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
    FundCoin,
    FundNum,
    PennyNum,
    TimeLinePoint,
    default_fund_coin_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a06_bud_logic.bud import BudUnit, budunit_shop
from src.a07_calendar_logic.chrono import TimeLineUnit, timelineunit_shop
from src.a11_deal_cell_logic.cell import cellunit_shop
from src.a12_hub_tools.basis_buds import create_listen_basis, get_default_job
from src.a12_hub_tools.hub_path import create_cell_dir_path, create_fisc_json_path
from src.a12_hub_tools.hub_tool import (
    cellunit_save_to_dir,
    gut_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from src.a13_bud_listen_logic.listen import (
    create_plan_file_from_duty_file,
    listen_to_agendas_create_init_job_from_guts,
    listen_to_debtors_roll_jobs_into_job,
    listen_to_speaker_agenda,
)
from src.a15_fisc_logic.journal_sqlstr import get_create_table_if_not_exist_sqlstrs


def get_default_job_listen_count() -> int:
    return 3


class dealunit_Exception(Exception):
    pass


class set_cashpurchase_Exception(Exception):
    pass


class set_offi_time_max_Exception(Exception):
    pass


@dataclass
class FiscUnit:
    """Data pipelines:
    pipeline1: packs->gut
    pipeline2: gut->dutys
    pipeline3: duty->plan
    pipeline4: plan->job
    pipeline5: gut->job (direct)
    pipeline6: gut->plan->job (through plans)
    pipeline7: packs->job (could be 5 of 6)
    """

    fisc_label: FiscLabel = None
    fisc_mstr_dir: str = None
    timeline: TimeLineUnit = None
    brokerunits: dict[OwnerName, BrokerUnit] = None
    cashbook: TranBook = None
    offi_times: set[TimeLinePoint] = None
    bridge: str = None
    fund_coin: FundCoin = None
    respect_bit: BitNum = None
    penny: PennyNum = None
    job_listen_rotations: int = None
    _offi_time_max: TimeLinePoint = None
    _fisc_dir: str = None
    _owners_dir: str = None
    _journal_db: str = None
    _packs_dir: str = None
    _all_tranbook: TranBook = None

    # directory setup
    def _set_fisc_dirs(self, in_memory_journal: bool = None):
        fiscs_dir = create_path(self.fisc_mstr_dir, "fiscs")
        self._fisc_dir = create_path(fiscs_dir, self.fisc_label)
        self._owners_dir = create_path(self._fisc_dir, "owners")
        self._packs_dir = create_path(self._fisc_dir, "packs")
        set_dir(x_path=self._fisc_dir)
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

    def get_owner_hubunits(self) -> dict[OwnerName:HubUnit]:
        return {
            x_owner_name: hubunit_shop(
                fisc_mstr_dir=self.fisc_mstr_dir,
                fisc_label=self.fisc_label,
                owner_name=x_owner_name,
                keep_way=None,
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            for x_owner_name in self._get_owner_folder_names()
        }

    # database
    def get_journal_db_path(self) -> str:
        fiscs_dir = create_path(self.fisc_mstr_dir, "fiscs")
        fisc_dir = create_path(fiscs_dir, self.fisc_label)
        return create_path(fisc_dir, "journal.db")

    def _create_journal_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> Connection:
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
        x_gut = open_gut_file(self.fisc_mstr_dir, self.fisc_label, owner_name)
        x_gut.settle_bud()
        for healer_name, healer_dict in x_gut._healers_dict.items():
            healer_hubunit = hubunit_shop(
                self.fisc_mstr_dir,
                self.fisc_label,
                healer_name,
                keep_way=None,
                # "duty_plan",
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            for keep_way in healer_dict.keys():
                self._set_owner_duty(healer_hubunit, keep_way, x_gut)

    def _set_owner_duty(
        self,
        healer_hubunit: HubUnit,
        keep_way: WayTerm,
        gut_bud: BudUnit,
    ):
        healer_hubunit.keep_way = keep_way
        healer_hubunit.create_treasury_db_file()
        healer_hubunit.save_duty_bud(gut_bud)

    def generate_healers_authored_job(self, owner_name: OwnerName, x_gut: BudUnit):
        x_job = get_default_job(x_gut)
        for healer_name, healer_dict in x_gut._healers_dict.items():
            healer_hubunit = hubunit_shop(
                fisc_mstr_dir=self.fisc_mstr_dir,
                fisc_label=self.fisc_label,
                owner_name=healer_name,
                keep_way=None,
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            healer_hubunit.create_gut_treasury_db_files()
            for keep_way in healer_dict.keys():
                keep_hubunit = hubunit_shop(
                    fisc_mstr_dir=self.fisc_mstr_dir,
                    fisc_label=self.fisc_label,
                    owner_name=healer_name,
                    keep_way=keep_way,
                    # "duty_plan",
                    bridge=self.bridge,
                    respect_bit=self.respect_bit,
                )
                keep_hubunit.save_duty_bud(x_gut)
                create_plan_file_from_duty_file(keep_hubunit, owner_name)
                x_plan = keep_hubunit.get_plan_bud(owner_name)
                x_job = listen_to_speaker_agenda(x_job, x_plan)
        return x_job

    # job bud management
    def create_empty_bud_from_fisc(self, owner_name: OwnerName) -> BudUnit:
        return budunit_shop(
            owner_name,
            self.fisc_label,
            bridge=self.bridge,
            fund_coin=self.fund_coin,
            respect_bit=self.respect_bit,
            penny=self.penny,
        )

    def create_gut_file_if_none(self, owner_name: OwnerName):
        if not gut_file_exists(self.fisc_mstr_dir, self.fisc_label, owner_name):
            empty_bud = self.create_empty_bud_from_fisc(owner_name)
            save_gut_file(self.fisc_mstr_dir, empty_bud)

    def create_init_job_from_guts(self, owner_name: OwnerName):
        self.create_gut_file_if_none(owner_name)
        x_gut = open_gut_file(self.fisc_mstr_dir, self.fisc_label, owner_name)
        x_job = create_listen_basis(x_gut)
        listen_to_agendas_create_init_job_from_guts(self.fisc_mstr_dir, x_job)
        save_job_file(self.fisc_mstr_dir, x_job)

    def rotate_job(self, owner_name: OwnerName) -> BudUnit:
        x_job = open_job_file(self.fisc_mstr_dir, self.fisc_label, owner_name)
        x_job.settle_bud()
        # # if budunit has healers create job from healers.
        # if len(x_gut._healers_dict) > 0:
        #     return self.generate_healers_authored_job(owner_name, x_gut)
        # create budunit from debtors roll
        return listen_to_debtors_roll_jobs_into_job(
            self.fisc_mstr_dir, self.fisc_label, owner_name
        )

    def generate_all_jobs(self):
        owner_names = self._get_owner_folder_names()
        for owner_name in owner_names:
            self.create_init_job_from_guts(owner_name)

        for _ in range(self.job_listen_rotations):
            for owner_name in owner_names:
                save_job_file(self.fisc_mstr_dir, self.rotate_job(owner_name))

    def get_job_file_bud(self, owner_name: OwnerName) -> BudUnit:
        return open_job_file(self.fisc_mstr_dir, self.fisc_label, owner_name)

    # brokerunits
    def set_brokerunit(self, x_brokerunit: BrokerUnit):
        self.brokerunits[x_brokerunit.owner_name] = x_brokerunit

    def brokerunit_exists(self, x_owner_name: OwnerName) -> bool:
        return self.brokerunits.get(x_owner_name) != None

    def get_brokerunit(self, x_owner_name: OwnerName) -> BrokerUnit:
        return self.brokerunits.get(x_owner_name)

    def del_brokerunit(self, x_owner_name: OwnerName):
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
            exception_str = f"Cannot set dealunit because deal_time {deal_time} is less than FiscUnit._offi_time_max {self._offi_time_max}."
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

    def get_dict(self, include_cashbook: bool = True) -> dict:
        x_dict = {
            "fisc_label": self.fisc_label,
            "bridge": self.bridge,
            "fund_coin": self.fund_coin,
            "penny": self.penny,
            "brokerunits": self._get_brokerunits_dict(),
            "respect_bit": self.respect_bit,
            "timeline": self.timeline.get_dict(),
            "offi_times": list(self.offi_times),
        }
        if include_cashbook:
            x_dict["cashbook"] = self.cashbook.get_dict()
        return x_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())

    def _get_brokerunits_dict(self):
        return {
            x_deal.owner_name: x_deal.get_dict() for x_deal in self.brokerunits.values()
        }

    def get_brokerunits_deal_times(self) -> set[TimeLinePoint]:
        all_dealunit_deal_times = set()
        for x_brokerunit in self.brokerunits.values():
            all_dealunit_deal_times.update(x_brokerunit.get_deal_times())
        return all_dealunit_deal_times

    def set_cashpurchase(self, x_cashpurchase: TranUnit):
        self.cashbook.set_tranunit(
            tranunit=x_cashpurchase,
            blocked_tran_times=self.get_brokerunits_deal_times(),
            _offi_time_max=self._offi_time_max,
        )

    def add_cashpurchase(
        self,
        owner_name: OwnerName,
        acct_name: AcctName,
        tran_time: TimeLinePoint,
        amount: FundNum,
        blocked_tran_times: set[TimeLinePoint] = None,
        _offi_time_max: TimeLinePoint = None,
    ):
        self.cashbook.add_tranunit(
            owner_name=owner_name,
            acct_name=acct_name,
            tran_time=tran_time,
            amount=amount,
            blocked_tran_times=blocked_tran_times,
            _offi_time_max=_offi_time_max,
        )

    def cashpurchase_exists(
        self, src: AcctName, dst: AcctName, x_tran_time: TimeLinePoint
    ) -> bool:
        return self.cashbook.tranunit_exists(src, dst, x_tran_time)

    def get_cashpurchase(
        self, src: AcctName, dst: AcctName, x_tran_time: TimeLinePoint
    ) -> TranUnit:
        return self.cashbook.get_tranunit(src, dst, x_tran_time)

    def del_cashpurchase(
        self, src: AcctName, dst: AcctName, x_tran_time: TimeLinePoint
    ):
        return self.cashbook.del_tranunit(src, dst, x_tran_time)

    # def set_offi_time(self, offi_time: TimeLinePoint):
    #     self.offi_time = offi_time
    #     if self._offi_time_max < self.offi_time:
    #         self._offi_time_max = self.offi_time

    def set_offi_time_max(self, x_offi_time_max: TimeLinePoint):
        x_tran_times = self.cashbook.get_tran_times()
        if x_tran_times != set() and max(x_tran_times) >= x_offi_time_max:
            exception_str = f"Cannot set _offi_time_max {x_offi_time_max}, cashpurchase with greater tran_time exists"
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

    def set_all_tranbook(self):
        x_tranunits = copy_deepcopy(self.cashbook.tranunits)
        x_tranbook = tranbook_shop(self.fisc_label, x_tranunits)
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
    ):
        for owner_name, brokerunit in self.brokerunits.items():
            for deal_time in brokerunit.deals.keys():
                self._create_deal_root_cell(owner_name, ote1_dict, deal_time)

    def _create_deal_root_cell(
        self,
        owner_name: OwnerName,
        ote1_dict: dict[OwnerName, dict[TimeLinePoint, EventInt]],
        deal_time: TimeLinePoint,
    ):
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
            self.fisc_mstr_dir, self.fisc_label, owner_name, deal_time, []
        )
        cellunit_save_to_dir(root_cell_dir, cellunit)


def _get_ote1_max_past_event_int(
    owner_name: str, ote1_dict: dict[str, dict[str, int]], deal_time: int
) -> EventInt:
    """Using the fisc_ote1_agg grab most recent event int before a given deal_time"""
    ote1_owner_dict = ote1_dict.get(owner_name)
    if not ote1_owner_dict:
        return None
    event_timepoints = set(ote1_owner_dict.keys())
    if past_timepoints := {tp for tp in event_timepoints if int(tp) <= deal_time}:
        max_past_timepoint = max(past_timepoints)
        return ote1_owner_dict.get(max_past_timepoint)


def get_module_temp_dir():
    return "src/a15_fisc_logic/_test_util/fisc_mstr"


def fiscunit_shop(
    fisc_label: FiscLabel,
    fisc_mstr_dir: str = None,
    timeline: TimeLineUnit = None,
    offi_times: set[TimeLinePoint] = None,
    in_memory_journal: bool = None,
    bridge: str = None,
    fund_coin: float = None,
    respect_bit: float = None,
    penny: float = None,
    job_listen_rotations: int = None,
) -> FiscUnit:
    if timeline is None:
        timeline = timelineunit_shop()
    if fisc_mstr_dir is None:
        fisc_mstr_dir = get_module_temp_dir()
    if not job_listen_rotations:
        job_listen_rotations = get_default_job_listen_count()
    x_fiscunit = FiscUnit(
        fisc_label=fisc_label,
        fisc_mstr_dir=fisc_mstr_dir,
        timeline=timeline,
        brokerunits={},
        cashbook=tranbook_shop(fisc_label),
        offi_times=get_empty_set_if_None(offi_times),
        bridge=default_bridge_if_None(bridge),
        fund_coin=default_fund_coin_if_None(fund_coin),
        respect_bit=default_RespectBit_if_None(respect_bit),
        penny=filter_penny(penny),
        _all_tranbook=tranbook_shop(fisc_label),
        job_listen_rotations=job_listen_rotations,
    )
    x_fiscunit._set_fisc_dirs(in_memory_journal=in_memory_journal)
    return x_fiscunit


def _get_brokerunits_from_dict(brokerunits_dict: dict) -> dict[OwnerName, BrokerUnit]:
    return {
        x_owner_name: get_brokerunit_from_dict(brokerunit_dict)
        for x_owner_name, brokerunit_dict in brokerunits_dict.items()
    }


def get_from_dict(fisc_dict: dict) -> FiscUnit:
    x_fisc_label = fisc_dict.get("fisc_label")
    x_fisc = fiscunit_shop(
        fisc_label=x_fisc_label,
        fisc_mstr_dir=None,
        offi_times=set(fisc_dict.get("offi_times")),
        bridge=fisc_dict.get("bridge"),
        fund_coin=fisc_dict.get("fund_coin"),
        respect_bit=fisc_dict.get("respect_bit"),
        penny=fisc_dict.get("penny"),
    )
    fisc_dict_timeline_value = fisc_dict.get("timeline")
    if fisc_dict_timeline_value:
        x_fisc.timeline = timelineunit_shop(fisc_dict_timeline_value)
    else:
        x_fisc.timeline = timelineunit_shop(None)
    x_fisc.brokerunits = _get_brokerunits_from_dict(fisc_dict.get("brokerunits"))
    x_fisc.cashbook = get_tranbook_from_dict(fisc_dict.get("cashbook"))
    return x_fisc


def get_from_json(x_fisc_json: str) -> FiscUnit:
    return get_from_dict(get_dict_from_json(x_fisc_json))


def get_from_default_path(fisc_mstr_dir: str, fisc_label: FiscLabel) -> FiscUnit:
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, fisc_label)
    x_fiscunit = get_from_json(open_file(fisc_json_path))
    x_fiscunit.fisc_mstr_dir = fisc_mstr_dir
    x_fiscunit._set_fisc_dirs()
    return x_fiscunit
