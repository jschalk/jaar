from src.s0_instrument.file import set_dir, delete_dir, dir_files
from src.s0_instrument.python_tool import get_0_if_None
from src.s1_road.jaar_config import get_gifts_folder
from src.s1_road.finance import (
    default_respect_bit_if_none,
    default_penny_if_none,
    PennyNum,
    FundCoin,
    BitNum,
)
from src.s1_road.road import default_road_delimiter_if_none, OwnerID, RoadUnit, FiscalID
from src.s2_bud.bud import BudUnit
from src.s3_chrono.chrono import TimeLineUnit, timelineunit_shop
from src.s3_chrono.bud_event import OwnerBudEvent, OwnerBudEvents
from src.s5_listen.basis_buds import get_default_final_bud
from src.s5_listen.hubunit import hubunit_shop, HubUnit
from src.s5_listen.listen import (
    listen_to_speaker_agenda,
    listen_to_debtors_roll_voice_final,
    listen_to_debtors_roll_duty_job,
    create_job_file_from_duty_file,
)
from src.s7_fiscal.journal_sqlstr import get_create_table_if_not_exist_sqlstrs
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


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

    fiscal_id: FiscalID
    fiscals_dir: str
    timeline: TimeLineUnit = None
    current_time: int = None
    bud_history: dict[OwnerID, OwnerBudEvents] = None
    _fiscal_dir: str = None
    _owners_dir: str = None
    _journal_db: str = None
    _gifts_dir: str = None
    _road_delimiter: str = None
    _fund_coin: FundCoin = None
    _respect_bit: BitNum = None
    _penny: PennyNum = None

    # directory setup
    def _set_fiscal_dirs(self, in_memory_journal: bool = None):
        self._fiscal_dir = f"{self.fiscals_dir}/{self.fiscal_id}"
        self._owners_dir = f"{self._fiscal_dir}/owners"
        self._gifts_dir = f"{self._fiscal_dir}/{get_gifts_folder()}"
        set_dir(x_path=self._fiscal_dir)
        set_dir(x_path=self._owners_dir)
        set_dir(x_path=self._gifts_dir)
        self._create_journal_db(in_memory=in_memory_journal)

    def _get_owner_dir(self, owner_id):
        return f"{self._owners_dir}/{owner_id}"

    def _get_owner_folder_names(self) -> set:
        owners = dir_files(self._owners_dir, include_dirs=True, include_files=False)
        return set(owners.keys())

    def get_owner_hubunits(self) -> dict[OwnerID:HubUnit]:
        x_owner_ids = self._get_owner_folder_names()
        return {
            x_owner_id: hubunit_shop(
                fiscals_dir=self.fiscals_dir,
                fiscal_id=self.fiscal_id,
                owner_id=x_owner_id,
                keep_road=None,
                road_delimiter=self._road_delimiter,
                respect_bit=self._respect_bit,
            )
            for x_owner_id in x_owner_ids
        }

    # database
    def get_journal_db_path(self) -> str:
        return f"{self.fiscals_dir}/{self.fiscal_id}/journal.db"

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
            fiscal_id=self.fiscal_id,
            fiscals_dir=self.fiscals_dir,
            keep_road=None,
            road_delimiter=self._road_delimiter,
            respect_bit=self._respect_bit,
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
                self.fiscals_dir,
                self.fiscal_id,
                healer_id,
                keep_road=None,
                # "duty_job",
                road_delimiter=self._road_delimiter,
                respect_bit=self._respect_bit,
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
                fiscals_dir=self.fiscals_dir,
                fiscal_id=self.fiscal_id,
                owner_id=healer_id,
                keep_road=None,
                # "duty_job",
                road_delimiter=self._road_delimiter,
                respect_bit=self._respect_bit,
            )
            healer_hubunit.create_voice_treasury_db_files()
            for keep_road in healer_dict.keys():
                keep_hubunit = hubunit_shop(
                    fiscals_dir=self.fiscals_dir,
                    fiscal_id=self.fiscal_id,
                    owner_id=healer_id,
                    keep_road=keep_road,
                    # "duty_job",
                    road_delimiter=self._road_delimiter,
                    respect_bit=self._respect_bit,
                )
                keep_hubunit.save_duty_bud(x_voice)
                create_job_file_from_duty_file(keep_hubunit, owner_id)
                x_job = keep_hubunit.get_job_bud(owner_id)
                listen_to_speaker_agenda(x_final, x_job)

        # if nothing has come from voice->duty->job->final pipeline use voice->final pipeline
        x_final.settle_bud()
        if len(x_final._idea_dict) == 1:
            # pipeline_voice_final_str()
            listen_to_debtors_roll_voice_final(listener_hubunit)
            listener_hubunit.open_file_final()
            x_final.settle_bud()
        if len(x_final._idea_dict) == 1:
            x_final = x_voice
        listener_hubunit.save_final_bud(x_final)

        return self.get_final_file_bud(owner_id)

    def generate_all_final_buds(self):
        for x_owner_id in self._get_owner_folder_names():
            self.generate_final_bud(x_owner_id)

    def get_final_file_bud(self, owner_id: OwnerID) -> BudUnit:
        return self._get_hubunit(owner_id).get_final_bud()

    # bud_history
    def set_ownerbudevent(self, x_ownerbudevents: OwnerBudEvents):
        self.bud_history[x_ownerbudevents.owner_id] = x_ownerbudevents

    def ownerbudevents_exists(self, x_owner_id: OwnerID) -> bool:
        return self.bud_history.get(x_owner_id) != None

    def get_ownerbudevents(self, x_owner_id: OwnerID) -> OwnerBudEvents:
        return self.bud_history.get(x_owner_id)

    def del_ownerbudevents(self, x_owner_id: OwnerID):
        self.bud_history.pop(x_owner_id)


def fiscalunit_shop(
    fiscal_id: FiscalID,
    fiscals_dir: str,
    timeline: TimeLineUnit = None,
    current_time: int = None,
    in_memory_journal: bool = None,
    _road_delimiter: str = None,
    _fund_coin: float = None,
    _respect_bit: float = None,
    _penny: float = None,
) -> FiscalUnit:
    if timeline is None:
        timeline = timelineunit_shop()
    fiscal_x = FiscalUnit(
        fiscal_id=fiscal_id,
        fiscals_dir=fiscals_dir,
        timeline=timeline,
        current_time=get_0_if_None(current_time),
        bud_history={},
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _fund_coin=default_respect_bit_if_none(_fund_coin),
        _respect_bit=default_respect_bit_if_none(_respect_bit),
        _penny=default_penny_if_none(_penny),
    )
    fiscal_x._set_fiscal_dirs(in_memory_journal=in_memory_journal)
    return fiscal_x
