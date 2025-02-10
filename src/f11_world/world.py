from src.f00_instrument.file import set_dir, create_path, count_dirs_files, delete_dir
from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_None,
    get_0_if_None,
    get_empty_set_if_None,
)
from src.f01_road.deal import TimeLinePoint, TimeConversion
from src.f01_road.road import (
    FaceName,
    EventInt,
    FiscalTitle,
    WorldID,
    TimeLineTitle,
    get_default_world_id,
)
from src.f07_fiscal.fiscal import FiscalUnit
from src.f10_etl.transformers import (
    etl_mine_to_train_staging,
    etl_train_staging_to_train_agg,
    etl_train_agg_to_train_valid,
    etl_train_agg_to_train_events,
    etl_train_events_to_events_log,
    etl_train_pidgin_staging_to_agg,
    etl_train_agg_to_pidgin_staging,
    etl_train_events_log_to_events_agg,
    get_events_dict_from_events_agg_file,
    etl_train_pidgin_agg_to_otz_face_dirs,
    etl_otz_face_pidgins_to_otz_event_pidgins,
    etl_otz_event_pidgins_to_otz_pidgin_csv_files,
    etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons,
    etl_pidgin_jsons_inherit_younger_pidgins,
    get_pidgin_events_by_dirs,
    etl_train_ideas_to_otz_face_ideas,
    etl_otz_face_ideas_to_otz_event_otx_ideas,
    etl_otz_event_ideas_to_inx_events,
    etl_otz_inx_event_ideas_to_inz_faces,
    etl_inz_face_ideas_to_csv_files,
    etl_inz_face_csv_files2idea_staging_tables,
    etl_idea_staging_to_fiscal_tables,
    etl_fiscal_staging_tables_to_fiscal_csvs,
    etl_fiscal_agg_tables_to_fiscal_csvs,
    etl_fiscal_csvs_to_fiscal_jsons,
    etl_idea_staging_to_bud_tables,
    etl_bud_tables_to_event_bud_csvs,
    etl_event_bud_csvs_to_gift_json,
    etl_event_gift_json_to_event_inherited_budunits,
    etl_event_inherited_budunits_to_fiscal_voice,
    etl_fiscal_voice_to_fiscal_forecast,
    etl_fiscal_agg_tables2fiscal_owner_time_agg,
)
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection


def get_default_worlds_dir() -> str:
    return "src/f11_world/examples/worlds"


class _set_fiscal_pidgin_Exception(Exception):
    pass


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    present_time: TimeLinePoint = None
    events: dict[EventInt, FaceName] = None
    timeconversions: dict[TimeLineTitle, TimeConversion] = None
    _faces_otz_dir: str = None
    _faces_inz_dir: str = None
    _world_dir: str = None
    _mine_dir: str = None
    _train_dir: str = None
    _fiscal_mstr_dir: str = None
    _fiscalunits: set[FiscalTitle] = None
    _pidgin_events: dict[FaceName, set[EventInt]] = None

    def set_event(self, event_int: EventInt, face_name: FaceName):
        self.events[event_int] = face_name

    def event_exists(self, event_int: EventInt) -> bool:
        return self.events.get(event_int) != None

    def get_event(self, event_int: EventInt) -> FaceName:
        return self.events.get(event_int)

    def legitimate_events(self) -> set[EventInt]:
        return set(self.events.keys())

    def _event_dir(self, face_name: FaceName, event_int: EventInt) -> str:
        face_dir = create_path(self._faces_otz_dir, face_name)
        return create_path(face_dir, event_int)

    def _set_pidgin_events(self):
        self._pidgin_events = get_pidgin_events_by_dirs(self._faces_otz_dir)

    def set_mine_dir(self, x_dir: str):
        self._mine_dir = x_dir
        set_dir(self._mine_dir)

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_id)
        self._faces_otz_dir = create_path(self._world_dir, "faces_otz")
        self._faces_inz_dir = create_path(self._world_dir, "faces_inz")
        self._train_dir = create_path(self._world_dir, "train")
        self._fiscal_mstr_dir = create_path(self._world_dir, "fiscal_mstr")
        set_dir(self._world_dir)
        set_dir(self._faces_otz_dir)
        set_dir(self._faces_inz_dir)
        set_dir(self._train_dir)
        set_dir(self._fiscal_mstr_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineTitle, TimeConversion]:
        return self.timeconversions

    def mine_to_train_staging(self):
        etl_mine_to_train_staging(self._mine_dir, self._train_dir)

    def train_staging_to_train_agg(self):
        etl_train_staging_to_train_agg(self._train_dir)

    def train_agg_to_train_valid(self):
        etl_train_agg_to_train_valid(self._train_dir, self.legitimate_events())

    def train_agg_to_train_events(self):
        etl_train_agg_to_train_events(self._train_dir)

    def train_events_to_events_log(self):
        etl_train_events_to_events_log(self._train_dir)

    def train_events_log_to_events_agg(self):
        etl_train_events_log_to_events_agg(self._train_dir)

    def set_events_from_events_agg_file(self):
        self.events = get_events_dict_from_events_agg_file(self._train_dir)

    def train_agg_to_pidgin_staging(self):
        etl_train_agg_to_pidgin_staging(self.legitimate_events(), self._train_dir)

    def train_pidgin_staging_to_agg(self):
        etl_train_pidgin_staging_to_agg(self._train_dir)

    def train_pidgin_agg_to_otz_face_dirs(self):
        etl_train_pidgin_agg_to_otz_face_dirs(self._train_dir, self._faces_otz_dir)

    def pidgin_jsons_inherit_younger_pidgins(self):
        etl_pidgin_jsons_inherit_younger_pidgins(
            self._faces_otz_dir, self._pidgin_events
        )

    def otz_face_pidgins_to_otz_event_pidgins(self):
        etl_otz_face_pidgins_to_otz_event_pidgins(self._faces_otz_dir)

    def otz_event_pidgins_to_otz_pidgin_csv_files(self):
        etl_otz_event_pidgins_to_otz_pidgin_csv_files(self._faces_otz_dir)

    def otz_event_pidgins_csvs_to_otz_pidgin_jsons(self):
        etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons(self._faces_otz_dir)
        self._set_pidgin_events()

    def train_ideas_to_otz_face_ideas(self):
        etl_train_ideas_to_otz_face_ideas(self._train_dir, self._faces_otz_dir)

    def otz_face_ideas_to_otz_event_otx_ideas(self):
        etl_otz_face_ideas_to_otz_event_otx_ideas(self._faces_otz_dir)

    def otz_event_ideas_to_inx_events(self):
        etl_otz_event_ideas_to_inx_events(self._faces_otz_dir, self._pidgin_events)

    def otz_inx_event_ideas_to_inz_faces(self):
        etl_otz_inx_event_ideas_to_inz_faces(self._faces_otz_dir, self._faces_inz_dir)

    def inz_face_ideas_to_csv_files(self):
        etl_inz_face_ideas_to_csv_files(self._faces_inz_dir)

    def etl_inz_face_csv_files2idea_staging_tables(
        self, conn_or_cursor: sqlite3_Connection
    ):
        etl_inz_face_csv_files2idea_staging_tables(conn_or_cursor, self._faces_inz_dir)

    def idea_staging_to_fiscal_tables(self, conn_or_cursor: sqlite3_Connection):
        etl_idea_staging_to_fiscal_tables(conn_or_cursor)

    def idea_staging_to_bud_tables(self, conn_or_cursor: sqlite3_Connection):
        etl_idea_staging_to_bud_tables(conn_or_cursor)

    def inz_faces_ideas_to_fiscal_mstr_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_fiscal_staging_tables_to_fiscal_csvs(conn_or_cursor, self._fiscal_mstr_dir)
        etl_fiscal_agg_tables_to_fiscal_csvs(conn_or_cursor, self._fiscal_mstr_dir)

    def fiscal_csvs_to_jsons(self):
        etl_fiscal_csvs_to_fiscal_jsons(self._fiscal_mstr_dir)

    def fiscal_agg_tables2fiscal_owner_time_agg(
        self, conn_or_cursor: sqlite3_Connection
    ):
        etl_fiscal_agg_tables2fiscal_owner_time_agg(conn_or_cursor)

    def bud_tables_to_event_bud_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_bud_tables_to_event_bud_csvs(conn_or_cursor, self._fiscal_mstr_dir)

    def event_bud_csvs_to_gift_json(self):
        etl_event_bud_csvs_to_gift_json(self._fiscal_mstr_dir)

    def event_gift_json_to_event_inherited_budunits(self):
        etl_event_gift_json_to_event_inherited_budunits(self._fiscal_mstr_dir)

    def event_inherited_budunits_to_fiscal_voice(self):
        etl_event_inherited_budunits_to_fiscal_voice(self._fiscal_mstr_dir)

    def fiscal_voice_to_fiscal_forecast(self):
        etl_fiscal_voice_to_fiscal_forecast(self._fiscal_mstr_dir)

    def mine_to_forecasts(self):  # sourcery skip: extract-method
        fiscal_mstr_dir = create_path(self._world_dir, "fiscal_mstr")
        delete_dir(fiscal_mstr_dir)
        print(f"{fiscal_mstr_dir=}")
        set_dir(fiscal_mstr_dir)
        print(f"      {self.worlds_dir=}")
        print(f"step 00 {count_dirs_files(self.worlds_dir)}")
        self.mine_to_train_staging()
        print(f"step 01 {count_dirs_files(self.worlds_dir)}")
        self.train_staging_to_train_agg()
        print(f"step 02 {count_dirs_files(self.worlds_dir)}")
        self.train_agg_to_train_events()
        self.train_events_to_events_log()
        self.train_events_log_to_events_agg()
        self.set_events_from_events_agg_file()
        print(f"step 03 {count_dirs_files(self.worlds_dir)}")
        self.train_agg_to_pidgin_staging()
        self.train_pidgin_staging_to_agg()
        self.train_pidgin_agg_to_otz_face_dirs()
        self.otz_face_pidgins_to_otz_event_pidgins()
        self.otz_event_pidgins_csvs_to_otz_pidgin_jsons()
        self.pidgin_jsons_inherit_younger_pidgins()
        print(f"step 04 {count_dirs_files(self.worlds_dir)}")
        self.train_agg_to_train_valid()
        self.train_ideas_to_otz_face_ideas()
        self.otz_face_ideas_to_otz_event_otx_ideas()
        self.otz_event_ideas_to_inx_events()
        self.otz_inx_event_ideas_to_inz_faces()
        self.inz_face_ideas_to_csv_files()
        print(f"step 05 {count_dirs_files(self.worlds_dir)}")
        with sqlite3_connect(":memory:") as fiscal_db_conn:
            cursor = fiscal_db_conn.cursor()
            self.etl_inz_face_csv_files2idea_staging_tables(cursor)
            self.idea_staging_to_fiscal_tables(cursor)
            print(f"step 05.1 {count_dirs_files(self.worlds_dir)}")
            self.idea_staging_to_fiscal_tables(cursor)
            self.inz_faces_ideas_to_fiscal_mstr_csvs(cursor)
            print(f"step 05.2 {count_dirs_files(self.worlds_dir)}")
            self.fiscal_csvs_to_jsons()
            print(f"step 06 {count_dirs_files(self.worlds_dir)}")
            self.idea_staging_to_bud_tables(cursor)
            self.bud_tables_to_event_bud_csvs(cursor)
        print(f"step 06.5 {count_dirs_files(self.worlds_dir)}")
        self.event_bud_csvs_to_gift_json()
        self.event_gift_json_to_event_inherited_budunits()
        # print(f"step 07 {count_dirs_files(self.worlds_dir)}")
        self.event_inherited_budunits_to_fiscal_voice()
        self.fiscal_voice_to_fiscal_forecast()
        # print(f"step 08 {count_dirs_files(self.worlds_dir)}")

    def get_dict(self) -> dict:
        return {
            "world_id": self.world_id,
            "present_time": self.present_time,
            "timeconversions": self.get_timeconversions_dict(),
            "events": self.events,
        }


def worldunit_shop(
    world_id: WorldID = None,
    worlds_dir: str = None,
    mine_dir: str = None,
    present_time: TimeLinePoint = None,
    timeconversions: dict[TimeLineTitle, TimeConversion] = None,
    _fiscalunits: set[FiscalTitle] = None,
) -> WorldUnit:
    if world_id is None:
        world_id = get_default_world_id()
    if worlds_dir is None:
        worlds_dir = get_default_worlds_dir()
    x_worldunit = WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        present_time=get_0_if_None(present_time),
        timeconversions=get_empty_dict_if_None(timeconversions),
        events={},
        _fiscalunits=get_empty_set_if_None(_fiscalunits),
        _mine_dir=mine_dir,
        _pidgin_events={},
    )
    x_worldunit._set_world_dirs()
    if not x_worldunit._mine_dir:
        x_worldunit.set_mine_dir(create_path(x_worldunit._world_dir, "mine"))
    return x_worldunit


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []
