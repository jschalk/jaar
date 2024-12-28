from src.f00_instrument.file import set_dir, delete_dir, get_dir_file_strs, create_path
from src.f00_instrument.dict_toolbox import (
    get_0_if_None,
    get_dict_from_json,
    get_json_from_dict,
)
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_deal_id_if_None,
    get_test_deals_dir,
)
from src.f01_road.finance import (
    default_respect_bit_if_None,
    default_penny_if_None,
    PennyNum,
    FundCoin,
    BitNum,
    TimeLinePoint,
    FundNum,
)
from src.f01_road.road import (
    default_bridge_if_None,
    OwnerID,
    RoadUnit,
    DealID,
    AcctID,
)
from src.f02_bud.bud import BudUnit
from src.f03_chrono.chrono import TimeLineUnit, timelineunit_shop
from src.f01_road.finance_tran import (
    PurviewLog,
    purviewlog_shop,
    get_purviewlog_from_dict,
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
from src.f07_deal.journal_sqlstr import get_create_table_if_not_exist_sqlstrs
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from copy import deepcopy as copy_deepcopy


class purviewepisode_Exception(Exception):
    pass


class set_cashpurchase_Exception(Exception):
    pass


class set_current_time_Exception(Exception):
    pass


@dataclass
class DealUnit:
    """Data pipelines:
    pipeline1: gifts->voice
    pipeline2: voice->dutys
    pipeline3: duty->job
    pipeline4: job->final
    pipeline5: voice->final (direct)
    pipeline6: voice->job->final (through jobs)
    pipeline7: gifts->final (could be 5 of 6)
    """

    deal_id: DealID = None
    deals_dir: str = None
    timeline: TimeLineUnit = None
    current_time: int = None
    purviewlogs: dict[OwnerID, PurviewLog] = None
    cashbook: TranBook = None
    bridge: str = None
    fund_coin: FundCoin = None
    respect_bit: BitNum = None
    penny: PennyNum = None
    _deal_dir: str = None
    _owners_dir: str = None
    _journal_db: str = None
    _gifts_dir: str = None
    _all_tranbook: TranBook = None

    # directory setup
    def _set_deal_dirs(self, in_memory_journal: bool = None):
        self._deal_dir = create_path(self.deals_dir, self.deal_id)
        self._owners_dir = create_path(self._deal_dir, "owners")
        self._gifts_dir = create_path(self._deal_dir, get_gifts_folder())
        set_dir(x_path=self._deal_dir)
        set_dir(x_path=self._owners_dir)
        set_dir(x_path=self._gifts_dir)
        self._create_journal_db(in_memory=in_memory_journal)

    def _get_owner_dir(self, owner_id):
        return create_path(self._owners_dir, owner_id)

    def _get_owner_folder_names(self) -> set:
        owners = get_dir_file_strs(
            self._owners_dir, include_dirs=True, include_files=False
        )
        return set(owners.keys())

    def get_owner_hubunits(self) -> dict[OwnerID:HubUnit]:
        x_owner_ids = self._get_owner_folder_names()
        return {
            x_owner_id: hubunit_shop(
                deals_dir=self.deals_dir,
                deal_id=self.deal_id,
                owner_id=x_owner_id,
                keep_road=None,
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            for x_owner_id in x_owner_ids
        }

    # database
    def get_journal_db_path(self) -> str:
        deal_dir = create_path(self.deals_dir, f"{self.deal_id}")
        return create_path(deal_dir, "journal.db")

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
    def _get_hubunit(self, owner_id: OwnerID) -> HubUnit:
        return hubunit_shop(
            owner_id=owner_id,
            deal_id=self.deal_id,
            deals_dir=self.deals_dir,
            keep_road=None,
            bridge=self.bridge,
            respect_bit=self.respect_bit,
        )

    def init_owner_keeps(self, owner_id: OwnerID):
        x_hubunit = self._get_hubunit(owner_id)
        x_hubunit.initialize_gift_voice_files()
        x_hubunit.initialize_final_file(self.get_owner_voice_from_file(owner_id))

    def get_owner_voice_from_file(self, owner_id: OwnerID) -> BudUnit:
        return self._get_hubunit(owner_id).get_voice_bud()

    def _set_all_healer_dutys(self, owner_id: OwnerID):
        x_voice = self.get_owner_voice_from_file(owner_id)
        x_voice.settle_bud()
        for healer_id, healer_dict in x_voice._healers_dict.items():
            healer_hubunit = hubunit_shop(
                self.deals_dir,
                self.deal_id,
                healer_id,
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
    def generate_final_bud(self, owner_id: OwnerID) -> BudUnit:
        listener_hubunit = self._get_hubunit(owner_id)
        x_voice = listener_hubunit.get_voice_bud()
        x_voice.settle_bud()
        x_final = get_default_final_bud(x_voice)
        for healer_id, healer_dict in x_voice._healers_dict.items():
            healer_hubunit = hubunit_shop(
                deals_dir=self.deals_dir,
                deal_id=self.deal_id,
                owner_id=healer_id,
                keep_road=None,
                # "duty_job",
                bridge=self.bridge,
                respect_bit=self.respect_bit,
            )
            healer_hubunit.create_voice_treasury_db_files()
            for keep_road in healer_dict.keys():
                keep_hubunit = hubunit_shop(
                    deals_dir=self.deals_dir,
                    deal_id=self.deal_id,
                    owner_id=healer_id,
                    keep_road=keep_road,
                    # "duty_job",
                    bridge=self.bridge,
                    respect_bit=self.respect_bit,
                )
                keep_hubunit.save_duty_bud(x_voice)
                create_job_file_from_duty_file(keep_hubunit, owner_id)
                x_job = keep_hubunit.get_job_bud(owner_id)
                listen_to_speaker_agenda(x_final, x_job)

        # if nothing has come from voice->duty->job->final pipeline use voice->final pipeline
        x_final.settle_bud()
        if len(x_final._item_dict) == 1:
            # pipeline_voice_final_str()
            listen_to_debtors_roll_voice_final(listener_hubunit)
            listener_hubunit.open_file_final()
            x_final.settle_bud()
        if len(x_final._item_dict) == 1:
            x_final = x_voice
        listener_hubunit.save_final_bud(x_final)

        return self.get_final_file_bud(owner_id)

    def generate_all_final_buds(self):
        for x_owner_id in self._get_owner_folder_names():
            self.generate_final_bud(x_owner_id)

    def get_final_file_bud(self, owner_id: OwnerID) -> BudUnit:
        return self._get_hubunit(owner_id).get_final_bud()

    # purviewlogs
    def set_purviewlog(self, x_purviewlog: PurviewLog):
        self.purviewlogs[x_purviewlog.owner_id] = x_purviewlog

    def purviewlog_exists(self, x_owner_id: OwnerID) -> bool:
        return self.purviewlogs.get(x_owner_id) != None

    def get_purviewlog(self, x_owner_id: OwnerID) -> PurviewLog:
        return self.purviewlogs.get(x_owner_id)

    def del_purviewlog(self, x_owner_id: OwnerID):
        self.purviewlogs.pop(x_owner_id)

    def add_purviewepisode(
        self,
        x_owner_id: OwnerID,
        x_time_int: TimeLinePoint,
        x_money_magnitude: int,
        allow_prev_to_current_time_entry: bool = False,
    ):
        if x_time_int < self.current_time and allow_prev_to_current_time_entry is False:
            exception_str = f"Cannot set purviewepisode because time_int {x_time_int} is less than DealUnit.current_time {self.current_time}."
            raise purviewepisode_Exception(exception_str)
        if self.purviewlog_exists(x_owner_id) is False:
            self.set_purviewlog(purviewlog_shop(x_owner_id))
        x_purviewlog = self.get_purviewlog(x_owner_id)
        x_purviewlog.add_episode(x_time_int, x_money_magnitude)

    def get_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "timeline": self.timeline.get_dict(),
            "current_time": self.current_time,
            "purviewlogs": self._get_purviewlogs_dict(),
            "bridge": self.bridge,
            "fund_coin": self.fund_coin,
            "respect_bit": self.respect_bit,
            "penny": self.penny,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())

    def _get_purviewlogs_dict(self):
        return {
            x_episode.owner_id: x_episode.get_dict()
            for x_episode in self.purviewlogs.values()
        }

    def get_purviewlogs_time_ints(self) -> set[TimeLinePoint]:
        all_purviewepisode_time_ints = set()
        for x_purviewlog in self.purviewlogs.values():
            all_purviewepisode_time_ints.update(x_purviewlog.get_time_ints())
        return all_purviewepisode_time_ints

    def set_cashpurchase(self, x_cashpurchase: TranUnit):
        self.cashbook.set_tranunit(
            x_tranunit=x_cashpurchase,
            x_blocked_time_ints=self.get_purviewlogs_time_ints(),
            x_current_time=self.current_time,
        )

    def add_cashpurchase(
        self,
        x_owner_id: OwnerID,
        x_acct_id: AcctID,
        x_time_int: TimeLinePoint,
        x_amount: FundNum,
        x_blocked_time_ints: set[TimeLinePoint] = None,
        x_current_time: TimeLinePoint = None,
    ):
        self.cashbook.add_tranunit(
            x_owner_id=x_owner_id,
            x_acct_id=x_acct_id,
            x_time_int=x_time_int,
            x_amount=x_amount,
            x_blocked_time_ints=x_blocked_time_ints,
            x_current_time=x_current_time,
        )

    def cashpurchase_exists(
        self, src: AcctID, dst: AcctID, x_time_int: TimeLinePoint
    ) -> bool:
        return self.cashbook.tranunit_exists(src, dst, x_time_int)

    def get_cashpurchase(
        self, src: AcctID, dst: AcctID, x_time_int: TimeLinePoint
    ) -> TranUnit:
        return self.cashbook.get_tranunit(src, dst, x_time_int)

    def del_cashpurchase(self, src: AcctID, dst: AcctID, x_time_int: TimeLinePoint):
        return self.cashbook.del_tranunit(src, dst, x_time_int)

    def set_current_time(self, x_current_time: TimeLinePoint):
        x_time_ints = self.cashbook.get_time_ints()
        if x_time_ints != set() and max(x_time_ints) >= x_current_time:
            exception_str = f"Cannot set current_time {x_current_time}, cashpurchase with greater time_int exists"
            raise set_current_time_Exception(exception_str)
        self.current_time = x_current_time

    def set_all_tranbook(self):
        x_tranunits = copy_deepcopy(self.cashbook.tranunits)
        x_tranbook = tranbook_shop(self.deal_id, x_tranunits)
        for owner_id, x_purviewlog in self.purviewlogs.items():
            for x_time_int, x_purviewepisode in x_purviewlog.episodes.items():
                for acct_id, x_amount in x_purviewepisode._net_purviews.items():
                    x_tranbook.add_tranunit(owner_id, acct_id, x_time_int, x_amount)
        self._all_tranbook = x_tranbook

    # TODO evaluate if this should be used
    # def set_all_tranbook(self):
    #     if not hasattr(self, "_combined_tranbook"):
    #         self._combined_tranbook = tranbook_shop(self.deal_id, [])
    #     new_tranunits = self.cashbook.get_new_tranunits()
    #     self._combined_tranbook.add_tranunits(new_tranunits)
    #     return self._combined_tranbook


def dealunit_shop(
    deal_id: DealID = None,
    deals_dir: str = None,
    timeline: TimeLineUnit = None,
    current_time: int = None,
    in_memory_journal: bool = None,
    bridge: str = None,
    fund_coin: float = None,
    respect_bit: float = None,
    penny: float = None,
) -> DealUnit:
    if timeline is None:
        timeline = timelineunit_shop()
    deal_id = get_deal_id_if_None(deal_id)
    if deals_dir is None:
        deals_dir = get_test_deals_dir()
    deal_x = DealUnit(
        deal_id=deal_id,
        deals_dir=deals_dir,
        timeline=timeline,
        current_time=get_0_if_None(current_time),
        purviewlogs={},
        cashbook=tranbook_shop(deal_id),
        bridge=default_bridge_if_None(bridge),
        fund_coin=default_respect_bit_if_None(fund_coin),
        respect_bit=default_respect_bit_if_None(respect_bit),
        penny=default_penny_if_None(penny),
        _all_tranbook=tranbook_shop(deal_id),
    )
    deal_x._set_deal_dirs(in_memory_journal=in_memory_journal)
    return deal_x


def get_from_json(x_deal_json: str) -> DealUnit:
    return get_from_dict(get_dict_from_json(x_deal_json))


def get_from_dict(deal_dict: dict) -> DealUnit:
    x_deal_id = deal_dict.get("deal_id")
    x_deal = dealunit_shop(x_deal_id, None)
    x_deal.timeline = timelineunit_shop(deal_dict.get("timeline"))
    x_deal.current_time = deal_dict.get("current_time")
    x_deal.bridge = deal_dict.get("bridge")
    x_deal.fund_coin = deal_dict.get("fund_coin")
    x_deal.respect_bit = deal_dict.get("respect_bit")
    x_deal.penny = deal_dict.get("penny")
    x_deal.purviewlogs = _get_purviewlogs_from_dict(deal_dict.get("purviewlogs"))
    return x_deal


def _get_purviewlogs_from_dict(purviewlogs_dict: dict) -> dict[OwnerID, PurviewLog]:
    return {
        x_owner_id: get_purviewlog_from_dict(purviewlog_dict)
        for x_owner_id, purviewlog_dict in purviewlogs_dict.items()
    }
