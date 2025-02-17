from src.f00_instrument.file import (
    set_dir,
    delete_dir,
    get_dir_file_strs,
    create_path,
    open_file,
    save_json,
)
from src.f00_instrument.dict_toolbox import (
    get_0_if_None,
    get_dict_from_json,
    get_json_from_dict,
)
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_fisc_title_if_None,
    get_test_fisc_mstr_dir,
)
from src.f01_road.finance import (
    default_respect_bit_if_None,
    filter_penny,
    PennyNum,
    default_fund_coin_if_None,
    FundCoin,
    BitNum,
    TimeLinePoint,
    FundNum,
)
from src.f01_road.deal import (
    BrokerUnit,
    brokerunit_shop,
    get_brokerunit_from_dict,
    TranUnit,
    TranBook,
    tranbook_shop,
    get_tranbook_from_dict,
)
from src.f01_road.road import (
    default_bridge_if_None,
    OwnerName,
    RoadUnit,
    FiscTitle,
    AcctName,
    EventInt,
)
from src.f02_bud.bud import BudUnit
from src.f03_chrono.chrono import TimeLineUnit, timelineunit_shop
from src.f05_listen.basis_buds import get_default_forecast_bud
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_episode_node_state_path,
)
from src.f05_listen.hubunit import hubunit_shop, HubUnit
from src.f05_listen.listen import (
    listen_to_speaker_agenda,
    listen_to_debtors_roll_voice_forecast,
    listen_to_debtors_roll_duty_job,
    create_job_file_from_duty_file,
)
from src.f07_fisc.journal_sqlstr import get_create_table_if_not_exist_sqlstrs
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from copy import deepcopy as copy_deepcopy


class dealepisode_Exception(Exception):
    pass


class set_cashpurchase_Exception(Exception):
    pass


class set_present_time_Exception(Exception):
    pass


@dataclass
class FiscUnit:
    """Data pipelines:
    pipeline1: gifts->voice
    pipeline2: voice->dutys
    pipeline3: duty->job
    pipeline4: job->forecast
    pipeline5: voice->forecast (direct)
    pipeline6: voice->job->forecast (through jobs)
    pipeline7: gifts->forecast (could be 5 of 6)
    """

    fisc_title: FiscTitle = None
    fisc_mstr_dir: str = None
    timeline: TimeLineUnit = None
    present_time: int = None
    brokerunits: dict[OwnerName, BrokerUnit] = None
    cashbook: TranBook = None
    bridge: str = None
    fund_coin: FundCoin = None
    respect_bit: BitNum = None
    penny: PennyNum = None
    _fisc_dir: str = None
    _owners_dir: str = None
    _journal_db: str = None
    _gifts_dir: str = None
    _all_tranbook: TranBook = None

    # directory setup
    def _set_fisc_dirs(self, in_memory_journal: bool = None):
        fiscs_dir = create_path(self.fisc_mstr_dir, "fiscs")
        self._fisc_dir = create_path(fiscs_dir, self.fisc_title)
        self._owners_dir = create_path(self._fisc_dir, "owners")
        self._gifts_dir = create_path(self._fisc_dir, get_gifts_folder())
        set_dir(x_path=self._fisc_dir)
        set_dir(x_path=self._owners_dir)
        set_dir(x_path=self._gifts_dir)
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
                fisc_title=self.fisc_title,
                owner_name=x_owner_name,
                keep_road=None,
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            for x_owner_name in self._get_owner_folder_names()
        }

    # database
    def get_journal_db_path(self) -> str:
        fiscs_dir = create_path(self.fisc_mstr_dir, "fiscs")
        fisc_dir = create_path(fiscs_dir, self.fisc_title)
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
            sqlite3_connect(self.get_journal_db_path())

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
    def _get_hubunit(self, owner_name: OwnerName) -> HubUnit:
        return hubunit_shop(
            owner_name=owner_name,
            fisc_title=self.fisc_title,
            fisc_mstr_dir=self.fisc_mstr_dir,
            keep_road=None,
            bridge=self.bridge,
            respect_bit=self.respect_bit,
        )

    def init_owner_keeps(self, owner_name: OwnerName):
        x_hubunit = self._get_hubunit(owner_name)
        x_hubunit.initialize_gift_voice_files()
        x_hubunit.initialize_forecast_file(self.get_owner_voice_from_file(owner_name))

    def get_owner_voice_from_file(self, owner_name: OwnerName) -> BudUnit:
        return self._get_hubunit(owner_name).get_voice_bud()

    def _set_all_healer_dutys(self, owner_name: OwnerName):
        x_voice = self.get_owner_voice_from_file(owner_name)
        x_voice.settle_bud()
        for healer_name, healer_dict in x_voice._healers_dict.items():
            healer_hubunit = hubunit_shop(
                self.fisc_mstr_dir,
                self.fisc_title,
                healer_name,
                keep_road=None,
                # "duty_job",
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            for keep_road in healer_dict.keys():
                self._set_owner_duty(healer_hubunit, keep_road, x_voice)

    def _set_owner_duty(
        self,
        healer_hubunit: HubUnit,
        keep_road: RoadUnit,
        voice_bud: BudUnit,
    ):
        healer_hubunit.keep_road = keep_road
        healer_hubunit.create_treasury_db_file()
        healer_hubunit.save_duty_bud(voice_bud)

    # forecast bud management
    def generate_forecast_bud(self, owner_name: OwnerName) -> BudUnit:
        listener_hubunit = self._get_hubunit(owner_name)
        x_voice = listener_hubunit.get_voice_bud()
        x_voice.settle_bud()
        x_forecast = get_default_forecast_bud(x_voice)
        for healer_name, healer_dict in x_voice._healers_dict.items():
            healer_hubunit = hubunit_shop(
                fisc_mstr_dir=self.fisc_mstr_dir,
                fisc_title=self.fisc_title,
                owner_name=healer_name,
                keep_road=None,
                # "duty_job",
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            healer_hubunit.create_voice_treasury_db_files()
            for keep_road in healer_dict.keys():
                keep_hubunit = hubunit_shop(
                    fisc_mstr_dir=self.fisc_mstr_dir,
                    fisc_title=self.fisc_title,
                    owner_name=healer_name,
                    keep_road=keep_road,
                    # "duty_job",
                    bridge=self.bridge,
                    respect_bit=self.respect_bit,
                )
                keep_hubunit.save_duty_bud(x_voice)
                create_job_file_from_duty_file(keep_hubunit, owner_name)
                x_job = keep_hubunit.get_job_bud(owner_name)
                listen_to_speaker_agenda(x_forecast, x_job)

        # if no budunit has come from voice->duty->job->forecast pipeline use voice->forecast pipeline
        x_forecast.settle_bud()
        if len(x_forecast._item_dict) == 1:
            x_forecast = listen_to_debtors_roll_voice_forecast(listener_hubunit)
        if len(x_forecast._item_dict) == 1:
            x_forecast = x_voice
        listener_hubunit.save_forecast_bud(x_forecast)

        return self.get_forecast_file_bud(owner_name)

    def generate_all_forecast_buds(self):
        for x_owner_name in self._get_owner_folder_names():
            self.init_owner_keeps(x_owner_name)
            self.generate_forecast_bud(x_owner_name)

    def get_forecast_file_bud(self, owner_name: OwnerName) -> BudUnit:
        return self._get_hubunit(owner_name).get_forecast_bud()

    # brokerunits
    def set_brokerunit(self, x_brokerunit: BrokerUnit):
        self.brokerunits[x_brokerunit.owner_name] = x_brokerunit

    def brokerunit_exists(self, x_owner_name: OwnerName) -> bool:
        return self.brokerunits.get(x_owner_name) != None

    def get_brokerunit(self, x_owner_name: OwnerName) -> BrokerUnit:
        return self.brokerunits.get(x_owner_name)

    def del_brokerunit(self, x_owner_name: OwnerName):
        self.brokerunits.pop(x_owner_name)

    def add_dealepisode(
        self,
        owner_name: OwnerName,
        time_int: TimeLinePoint,
        quota: int,
        allow_prev_to_present_time_entry: bool = False,
        ledger_depth: int = None,
    ):
        if time_int < self.present_time and not allow_prev_to_present_time_entry:
            exception_str = f"Cannot set dealepisode because time_int {time_int} is less than FiscUnit.present_time {self.present_time}."
            raise dealepisode_Exception(exception_str)
        if self.brokerunit_exists(owner_name) is False:
            self.set_brokerunit(brokerunit_shop(owner_name))
        x_brokerunit = self.get_brokerunit(owner_name)
        x_brokerunit.add_episode(time_int, quota, ledger_depth)

    def get_dict(self, include_cashbook: bool = True) -> dict:
        x_dict = {
            "fisc_title": self.fisc_title,
            "bridge": self.bridge,
            "present_time": self.present_time,
            "fund_coin": self.fund_coin,
            "penny": self.penny,
            "brokerunits": self._get_brokerunits_dict(),
            "respect_bit": self.respect_bit,
            "timeline": self.timeline.get_dict(),
        }
        if include_cashbook:
            x_dict["cashbook"] = self.cashbook.get_dict()
        return x_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())

    def _get_brokerunits_dict(self):
        return {
            x_episode.owner_name: x_episode.get_dict()
            for x_episode in self.brokerunits.values()
        }

    def get_brokerunits_time_ints(self) -> set[TimeLinePoint]:
        all_dealepisode_time_ints = set()
        for x_brokerunit in self.brokerunits.values():
            all_dealepisode_time_ints.update(x_brokerunit.get_time_ints())
        return all_dealepisode_time_ints

    def set_cashpurchase(self, x_cashpurchase: TranUnit):
        self.cashbook.set_tranunit(
            tranunit=x_cashpurchase,
            blocked_time_ints=self.get_brokerunits_time_ints(),
            present_time=self.present_time,
        )

    def add_cashpurchase(
        self,
        owner_name: OwnerName,
        acct_name: AcctName,
        time_int: TimeLinePoint,
        amount: FundNum,
        blocked_time_ints: set[TimeLinePoint] = None,
        present_time: TimeLinePoint = None,
    ):
        self.cashbook.add_tranunit(
            owner_name=owner_name,
            acct_name=acct_name,
            time_int=time_int,
            amount=amount,
            blocked_time_ints=blocked_time_ints,
            present_time=present_time,
        )

    def cashpurchase_exists(
        self, src: AcctName, dst: AcctName, x_time_int: TimeLinePoint
    ) -> bool:
        return self.cashbook.tranunit_exists(src, dst, x_time_int)

    def get_cashpurchase(
        self, src: AcctName, dst: AcctName, x_time_int: TimeLinePoint
    ) -> TranUnit:
        return self.cashbook.get_tranunit(src, dst, x_time_int)

    def del_cashpurchase(self, src: AcctName, dst: AcctName, x_time_int: TimeLinePoint):
        return self.cashbook.del_tranunit(src, dst, x_time_int)

    def set_present_time(self, x_present_time: TimeLinePoint):
        x_time_ints = self.cashbook.get_time_ints()
        if x_time_ints != set() and max(x_time_ints) >= x_present_time:
            exception_str = f"Cannot set present_time {x_present_time}, cashpurchase with greater time_int exists"
            raise set_present_time_Exception(exception_str)
        self.present_time = x_present_time

    def set_all_tranbook(self):
        x_tranunits = copy_deepcopy(self.cashbook.tranunits)
        x_tranbook = tranbook_shop(self.fisc_title, x_tranunits)
        for owner_name, x_brokerunit in self.brokerunits.items():
            for x_time_int, x_dealepisode in x_brokerunit.episodes.items():
                for acct_name, x_amount in x_dealepisode._episode_net.items():
                    x_tranbook.add_tranunit(owner_name, acct_name, x_time_int, x_amount)
        self._all_tranbook = x_tranbook

    def create_root_episode_nodes(self, ote1_dict):
        for owner_name, brokerunit in self.brokerunits.items():
            for time_int in brokerunit.episodes.keys():
                self.create_and_save_root_episode_node(owner_name, ote1_dict, time_int)

    def create_and_save_root_episode_node(
        self,
        owner_name: OwnerName,
        ote1_dict: dict[OwnerName, dict[TimeLinePoint, EventInt]],
        time_int: TimeLinePoint,
    ):
        max_past_event_int = _get_ote1_max_past_event_int(
            owner_name, ote1_dict, time_int
        )
        owner_brokerunit = self.get_brokerunit(owner_name)
        deal_episode = owner_brokerunit.get_episode(time_int)
        episode_node = {
            "owner_name": owner_name,
            "event_int": max_past_event_int,
            "ledger_depth": deal_episode.ledger_depth,
            "quota": deal_episode.quota,
            "penny": self.penny,
            "ancestors": [],
        }
        episode_node_json_path = create_episode_node_state_path(
            self.fisc_mstr_dir, self.fisc_title, owner_name, time_int
        )
        save_json(episode_node_json_path, None, episode_node)

    # TODO evaluate if this should be used
    # def set_all_tranbook(self):
    #     if not hasattr(self, "_combined_tranbook"):
    #         self._combined_tranbook = tranbook_shop(self.fisc_title, [])
    #     new_tranunits = self.cashbook.get_new_tranunits()
    #     self._combined_tranbook.add_tranunits(new_tranunits)
    #     return self._combined_tranbook


def _get_ote1_max_past_event_int(
    owner_name: str, ote1_dict: dict[str, dict[str, int]], time_int: int
):
    """Using the fisc_ote1_agg grab most recent event int before a given time_int"""
    ote1_owner_dict = ote1_dict.get(owner_name)
    event_timepoints = set(ote1_owner_dict.keys())
    if past_timepoints := {tp for tp in event_timepoints if int(tp) <= time_int}:
        max_past_timepoint = max(past_timepoints)
        return ote1_owner_dict.get(max_past_timepoint)


def fiscunit_shop(
    fisc_title: FiscTitle = None,
    fisc_mstr_dir: str = None,
    timeline: TimeLineUnit = None,
    present_time: int = None,
    in_memory_journal: bool = None,
    bridge: str = None,
    fund_coin: float = None,
    respect_bit: float = None,
    penny: float = None,
) -> FiscUnit:
    if timeline is None:
        timeline = timelineunit_shop()
    fisc_title = get_fisc_title_if_None(fisc_title)
    if fisc_mstr_dir is None:
        fisc_mstr_dir = get_test_fisc_mstr_dir()
    x_fiscunit = FiscUnit(
        fisc_title=fisc_title,
        fisc_mstr_dir=fisc_mstr_dir,
        timeline=timeline,
        present_time=get_0_if_None(present_time),
        brokerunits={},
        cashbook=tranbook_shop(fisc_title),
        bridge=default_bridge_if_None(bridge),
        fund_coin=default_fund_coin_if_None(fund_coin),
        respect_bit=default_respect_bit_if_None(respect_bit),
        penny=filter_penny(penny),
        _all_tranbook=tranbook_shop(fisc_title),
    )
    x_fiscunit._set_fisc_dirs(in_memory_journal=in_memory_journal)
    return x_fiscunit


def _get_brokerunits_from_dict(brokerunits_dict: dict) -> dict[OwnerName, BrokerUnit]:
    return {
        x_owner_name: get_brokerunit_from_dict(brokerunit_dict)
        for x_owner_name, brokerunit_dict in brokerunits_dict.items()
    }


def get_from_dict(fisc_dict: dict) -> FiscUnit:
    x_fisc_title = fisc_dict.get("fisc_title")
    x_fisc = fiscunit_shop(x_fisc_title, None)
    x_fisc.timeline = timelineunit_shop(fisc_dict.get("timeline"))
    x_fisc.present_time = fisc_dict.get("present_time")
    x_fisc.bridge = fisc_dict.get("bridge")
    x_fisc.fund_coin = fisc_dict.get("fund_coin")
    x_fisc.respect_bit = fisc_dict.get("respect_bit")
    x_fisc.penny = fisc_dict.get("penny")
    x_fisc.brokerunits = _get_brokerunits_from_dict(fisc_dict.get("brokerunits"))
    x_fisc.cashbook = get_tranbook_from_dict(fisc_dict.get("cashbook"))
    return x_fisc


def get_from_json(x_fisc_json: str) -> FiscUnit:
    return get_from_dict(get_dict_from_json(x_fisc_json))


def get_from_standard(fisc_mstr_dir: str, fisc_title: FiscTitle) -> FiscUnit:
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, fisc_title)
    x_fiscunit = get_from_json(open_file(fisc_json_path))
    x_fiscunit.fisc_mstr_dir = fisc_mstr_dir
    x_fiscunit._set_fisc_dirs()
    return x_fiscunit
