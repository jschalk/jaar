from src.f00_instrument.file import set_dir, delete_dir, get_dir_file_strs, create_path
from src.f00_instrument.dict_toolbox import (
    get_0_if_None,
    get_dict_from_json,
    get_json_from_dict,
)
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_fiscal_title_if_None,
    get_test_fiscals_dir,
)
from src.f01_road.finance import (
    default_respect_bit_if_None,
    default_penny_if_None,
    PennyNum,
    default_fund_coin_if_None,
    FundCoin,
    BitNum,
    TimeLinePoint,
    FundNum,
)
from src.f01_road.finance_tran import get_tranbook_from_dict
from src.f01_road.road import (
    default_bridge_if_None,
    OwnerName,
    RoadUnit,
    FiscalTitle,
    AcctName,
)
from src.f02_bud.bud import BudUnit
from src.f03_chrono.chrono import TimeLineUnit, timelineunit_shop
from src.f01_road.finance_tran import (
    DealLog,
    deallog_shop,
    get_deallog_from_dict,
    TranUnit,
    TranBook,
    tranbook_shop,
)
from src.f05_listen.basis_buds import get_default_final_bud
from src.f05_listen.hubunit import hubunit_shop, HubUnit
from src.f05_listen.listen import (
    listen_to_speaker_agenda,
    listen_to_debtors_roll_voice_final,
    listen_to_debtors_roll_duty_job,
    create_job_file_from_duty_file,
)
from src.f07_fiscal.journal_sqlstr import get_create_table_if_not_exist_sqlstrs
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
class FiscalUnit:
    """Data pipelines:
    pipeline1: gifts->voice
    pipeline2: voice->dutys
    pipeline3: duty->job
    pipeline4: job->final
    pipeline5: voice->final (direct)
    pipeline6: voice->job->final (through jobs)
    pipeline7: gifts->final (could be 5 of 6)
    """

    fiscal_title: FiscalTitle = None
    fiscals_dir: str = None
    timeline: TimeLineUnit = None
    present_time: int = None
    deallogs: dict[OwnerName, DealLog] = None
    cashbook: TranBook = None
    bridge: str = None
    fund_coin: FundCoin = None
    respect_bit: BitNum = None
    penny: PennyNum = None
    _fiscal_dir: str = None
    _owners_dir: str = None
    _journal_db: str = None
    _gifts_dir: str = None
    _all_tranbook: TranBook = None

    # directory setup
    def _set_fiscal_dirs(self, in_memory_journal: bool = None):
        self._fiscal_dir = create_path(self.fiscals_dir, self.fiscal_title)
        self._owners_dir = create_path(self._fiscal_dir, "owners")
        self._gifts_dir = create_path(self._fiscal_dir, get_gifts_folder())
        set_dir(x_path=self._fiscal_dir)
        set_dir(x_path=self._owners_dir)
        set_dir(x_path=self._gifts_dir)
        self._create_journal_db(in_memory=in_memory_journal)

    def _get_owner_dir(self, owner_name):
        return create_path(self._owners_dir, owner_name)

    def _get_owner_folder_names(self) -> set:
        owners = get_dir_file_strs(
            self._owners_dir, include_dirs=True, include_files=False
        )
        return set(owners.keys())

    def get_owner_hubunits(self) -> dict[OwnerName:HubUnit]:
        x_owner_names = self._get_owner_folder_names()
        return {
            x_owner_name: hubunit_shop(
                fiscals_dir=self.fiscals_dir,
                fiscal_title=self.fiscal_title,
                owner_name=x_owner_name,
                keep_road=None,
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            for x_owner_name in x_owner_names
        }

    # database
    def get_journal_db_path(self) -> str:
        fiscal_dir = create_path(self.fiscals_dir, f"{self.fiscal_title}")
        return create_path(fiscal_dir, "journal.db")

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
            fiscal_title=self.fiscal_title,
            fiscals_dir=self.fiscals_dir,
            keep_road=None,
            bridge=self.bridge,
            respect_bit=self.respect_bit,
        )

    def init_owner_keeps(self, owner_name: OwnerName):
        x_hubunit = self._get_hubunit(owner_name)
        x_hubunit.initialize_gift_voice_files()
        x_hubunit.initialize_final_file(self.get_owner_voice_from_file(owner_name))

    def get_owner_voice_from_file(self, owner_name: OwnerName) -> BudUnit:
        return self._get_hubunit(owner_name).get_voice_bud()

    def _set_all_healer_dutys(self, owner_name: OwnerName):
        x_voice = self.get_owner_voice_from_file(owner_name)
        x_voice.settle_bud()
        for healer_name, healer_dict in x_voice._healers_dict.items():
            healer_hubunit = hubunit_shop(
                self.fiscals_dir,
                self.fiscal_title,
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

    # final bud management
    def generate_final_bud(self, owner_name: OwnerName) -> BudUnit:
        listener_hubunit = self._get_hubunit(owner_name)
        x_voice = listener_hubunit.get_voice_bud()
        x_voice.settle_bud()
        x_final = get_default_final_bud(x_voice)
        for healer_name, healer_dict in x_voice._healers_dict.items():
            healer_hubunit = hubunit_shop(
                fiscals_dir=self.fiscals_dir,
                fiscal_title=self.fiscal_title,
                owner_name=healer_name,
                keep_road=None,
                # "duty_job",
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            healer_hubunit.create_voice_treasury_db_files()
            for keep_road in healer_dict.keys():
                keep_hubunit = hubunit_shop(
                    fiscals_dir=self.fiscals_dir,
                    fiscal_title=self.fiscal_title,
                    owner_name=healer_name,
                    keep_road=keep_road,
                    # "duty_job",
                    bridge=self.bridge,
                    respect_bit=self.respect_bit,
                )
                keep_hubunit.save_duty_bud(x_voice)
                create_job_file_from_duty_file(keep_hubunit, owner_name)
                x_job = keep_hubunit.get_job_bud(owner_name)
                listen_to_speaker_agenda(x_final, x_job)

        # if no budunit has come from voice->duty->job->final pipeline use voice->final pipeline
        x_final.settle_bud()
        if len(x_final._item_dict) == 1:
            # pipeline_voice_final_str()
            listen_to_debtors_roll_voice_final(listener_hubunit)
            listener_hubunit.open_file_final()
            x_final.settle_bud()
        if len(x_final._item_dict) == 1:
            x_final = x_voice
        listener_hubunit.save_final_bud(x_final)

        return self.get_final_file_bud(owner_name)

    def generate_all_final_buds(self):
        for x_owner_name in self._get_owner_folder_names():
            self.generate_final_bud(x_owner_name)

    def get_final_file_bud(self, owner_name: OwnerName) -> BudUnit:
        return self._get_hubunit(owner_name).get_final_bud()

    # deallogs
    def set_deallog(self, x_deallog: DealLog):
        self.deallogs[x_deallog.owner_name] = x_deallog

    def deallog_exists(self, x_owner_name: OwnerName) -> bool:
        return self.deallogs.get(x_owner_name) != None

    def get_deallog(self, x_owner_name: OwnerName) -> DealLog:
        return self.deallogs.get(x_owner_name)

    def del_deallog(self, x_owner_name: OwnerName):
        self.deallogs.pop(x_owner_name)

    def add_dealepisode(
        self,
        x_owner_name: OwnerName,
        x_time_int: TimeLinePoint,
        x_money_magnitude: int,
        allow_prev_to_present_time_entry: bool = False,
    ):
        if x_time_int < self.present_time and not allow_prev_to_present_time_entry:
            exception_str = f"Cannot set dealepisode because time_int {x_time_int} is less than FiscalUnit.present_time {self.present_time}."
            raise dealepisode_Exception(exception_str)
        if self.deallog_exists(x_owner_name) is False:
            self.set_deallog(deallog_shop(x_owner_name))
        x_deallog = self.get_deallog(x_owner_name)
        x_deallog.add_episode(x_time_int, x_money_magnitude)

    def get_dict(self, include_cashbook: bool = True) -> dict:
        x_dict = {
            "fiscal_title": self.fiscal_title,
            "bridge": self.bridge,
            "present_time": self.present_time,
            "fund_coin": self.fund_coin,
            "penny": self.penny,
            "deallogs": self._get_deallogs_dict(),
            "respect_bit": self.respect_bit,
            "timeline": self.timeline.get_dict(),
        }
        if include_cashbook:
            x_dict["cashbook"] = self.cashbook.get_dict()
        return x_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())

    def _get_deallogs_dict(self):
        return {
            x_episode.owner_name: x_episode.get_dict()
            for x_episode in self.deallogs.values()
        }

    def get_deallogs_time_ints(self) -> set[TimeLinePoint]:
        all_dealepisode_time_ints = set()
        for x_deallog in self.deallogs.values():
            all_dealepisode_time_ints.update(x_deallog.get_time_ints())
        return all_dealepisode_time_ints

    def set_cashpurchase(self, x_cashpurchase: TranUnit):
        self.cashbook.set_tranunit(
            x_tranunit=x_cashpurchase,
            x_blocked_time_ints=self.get_deallogs_time_ints(),
            x_present_time=self.present_time,
        )

    def add_cashpurchase(
        self,
        x_owner_name: OwnerName,
        x_acct_name: AcctName,
        x_time_int: TimeLinePoint,
        x_amount: FundNum,
        x_blocked_time_ints: set[TimeLinePoint] = None,
        x_present_time: TimeLinePoint = None,
    ):
        self.cashbook.add_tranunit(
            x_owner_name=x_owner_name,
            x_acct_name=x_acct_name,
            x_time_int=x_time_int,
            x_amount=x_amount,
            x_blocked_time_ints=x_blocked_time_ints,
            x_present_time=x_present_time,
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
        x_tranbook = tranbook_shop(self.fiscal_title, x_tranunits)
        for owner_name, x_deallog in self.deallogs.items():
            for x_time_int, x_dealepisode in x_deallog.episodes.items():
                for acct_name, x_amount in x_dealepisode._net_deals.items():
                    x_tranbook.add_tranunit(owner_name, acct_name, x_time_int, x_amount)
        self._all_tranbook = x_tranbook

    # TODO evaluate if this should be used
    # def set_all_tranbook(self):
    #     if not hasattr(self, "_combined_tranbook"):
    #         self._combined_tranbook = tranbook_shop(self.fiscal_title, [])
    #     new_tranunits = self.cashbook.get_new_tranunits()
    #     self._combined_tranbook.add_tranunits(new_tranunits)
    #     return self._combined_tranbook


def fiscalunit_shop(
    fiscal_title: FiscalTitle = None,
    fiscals_dir: str = None,
    timeline: TimeLineUnit = None,
    present_time: int = None,
    in_memory_journal: bool = None,
    bridge: str = None,
    fund_coin: float = None,
    respect_bit: float = None,
    penny: float = None,
) -> FiscalUnit:
    if timeline is None:
        timeline = timelineunit_shop()
    fiscal_title = get_fiscal_title_if_None(fiscal_title)
    if fiscals_dir is None:
        fiscals_dir = get_test_fiscals_dir()
    fiscal_x = FiscalUnit(
        fiscal_title=fiscal_title,
        fiscals_dir=fiscals_dir,
        timeline=timeline,
        present_time=get_0_if_None(present_time),
        deallogs={},
        cashbook=tranbook_shop(fiscal_title),
        bridge=default_bridge_if_None(bridge),
        fund_coin=default_fund_coin_if_None(fund_coin),
        respect_bit=default_respect_bit_if_None(respect_bit),
        penny=default_penny_if_None(penny),
        _all_tranbook=tranbook_shop(fiscal_title),
    )
    fiscal_x._set_fiscal_dirs(in_memory_journal=in_memory_journal)
    return fiscal_x


def get_from_json(x_fiscal_json: str) -> FiscalUnit:
    return get_from_dict(get_dict_from_json(x_fiscal_json))


def get_from_dict(fiscal_dict: dict) -> FiscalUnit:
    x_fiscal_title = fiscal_dict.get("fiscal_title")
    x_fiscal = fiscalunit_shop(x_fiscal_title, None)
    x_fiscal.timeline = timelineunit_shop(fiscal_dict.get("timeline"))
    x_fiscal.present_time = fiscal_dict.get("present_time")
    x_fiscal.bridge = fiscal_dict.get("bridge")
    x_fiscal.fund_coin = fiscal_dict.get("fund_coin")
    x_fiscal.respect_bit = fiscal_dict.get("respect_bit")
    x_fiscal.penny = fiscal_dict.get("penny")
    x_fiscal.deallogs = _get_deallogs_from_dict(fiscal_dict.get("deallogs"))
    x_fiscal.cashbook = get_tranbook_from_dict(fiscal_dict.get("cashbook"))
    return x_fiscal


def _get_deallogs_from_dict(deallogs_dict: dict) -> dict[OwnerName, DealLog]:
    return {
        x_owner_name: get_deallog_from_dict(deallog_dict)
        for x_owner_name, deallog_dict in deallogs_dict.items()
    }
