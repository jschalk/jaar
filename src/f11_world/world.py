from src.f00_instrument.file import set_dir, create_path
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
    etl_ocean_to_boat_staging,
    etl_boat_staging_to_boat_agg,
    etl_boat_agg_to_boat_valid,
    etl_boat_agg_to_boat_events,
    etl_boat_events_to_events_log,
    etl_boat_pidgin_staging_to_agg,
    etl_boat_agg_to_pidgin_staging,
    etl_boat_events_log_to_events_agg,
    get_events_dict_from_events_agg_file,
    etl_boat_pidgin_agg_to_bow_face_dirs,
    etl_bow_face_pidgins_to_bow_event_pidgins,
    etl_bow_event_pidgins_to_bow_pidgin_csv_files,
    etl_bow_event_pidgins_csvs_to_bow_pidgin_jsons,
    etl_pidgin_jsons_inherit_younger_pidgins,
    get_pidgin_events_by_dirs,
    etl_boat_ideas_to_bow_face_ideas,
    etl_bow_face_ideas_to_bow_event_otx_ideas,
    etl_bow_event_ideas_to_inx_events,
    etl_bow_inx_event_ideas_to_aft_faces,
    etl_aft_face_ideas_to_csv_files,
    etl_aft_face_csv_files2idea_staging_tables,
    etl_idea_staging_to_fiscal_tables,
    etl_fiscal_staging_tables_to_fiscal_csvs,
    etl_fiscal_agg_tables_to_fiscal_csvs,
    etl_fiscal_csvs_to_jsons,
    etl_idea_staging_to_bud_tables,
    etl_bud_tables_to_event_bud_csvs,
    etl_event_bud_csvs_to_gift_json,
    etl_event_gift_json_to_event_inherited_budunits,
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
    _faces_bow_dir: str = None
    _faces_aft_dir: str = None
    _world_dir: str = None
    _ocean_dir: str = None
    _boat_dir: str = None
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
        face_dir = create_path(self._faces_bow_dir, face_name)
        return create_path(face_dir, event_int)

    def _set_pidgin_events(self):
        self._pidgin_events = get_pidgin_events_by_dirs(self._faces_bow_dir)

    def set_ocean_dir(self, x_dir: str):
        self._ocean_dir = x_dir
        set_dir(self._ocean_dir)

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_id)
        self._faces_bow_dir = create_path(self._world_dir, "faces_bow")
        self._faces_aft_dir = create_path(self._world_dir, "faces_aft")
        self._boat_dir = create_path(self._world_dir, "boat")
        self._fiscal_mstr_dir = create_path(self._world_dir, "fiscal_mstr")
        set_dir(self._world_dir)
        set_dir(self._faces_bow_dir)
        set_dir(self._faces_aft_dir)
        set_dir(self._boat_dir)
        set_dir(self._fiscal_mstr_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineTitle, TimeConversion]:
        return self.timeconversions

    def ocean_to_boat_staging(self):
        etl_ocean_to_boat_staging(self._ocean_dir, self._boat_dir)

    def boat_staging_to_boat_agg(self):
        etl_boat_staging_to_boat_agg(self._boat_dir)

    def boat_agg_to_boat_valid(self):
        etl_boat_agg_to_boat_valid(self._boat_dir, self.legitimate_events())

    def boat_agg_to_boat_events(self):
        etl_boat_agg_to_boat_events(self._boat_dir)

    def boat_events_to_events_log(self):
        etl_boat_events_to_events_log(self._boat_dir)

    def boat_events_log_to_events_agg(self):
        etl_boat_events_log_to_events_agg(self._boat_dir)

    def set_events_from_events_agg_file(self):
        self.events = get_events_dict_from_events_agg_file(self._boat_dir)

    def boat_agg_to_pidgin_staging(self):
        etl_boat_agg_to_pidgin_staging(self.legitimate_events(), self._boat_dir)

    def boat_pidgin_staging_to_agg(self):
        etl_boat_pidgin_staging_to_agg(self._boat_dir)

    def boat_pidgin_agg_to_bow_face_dirs(self):
        etl_boat_pidgin_agg_to_bow_face_dirs(self._boat_dir, self._faces_bow_dir)

    def pidgin_jsons_inherit_younger_pidgins(self):
        etl_pidgin_jsons_inherit_younger_pidgins(
            self._faces_bow_dir, self._pidgin_events
        )

    def bow_face_pidgins_to_bow_event_pidgins(self):
        etl_bow_face_pidgins_to_bow_event_pidgins(self._faces_bow_dir)

    def bow_event_pidgins_to_bow_pidgin_csv_files(self):
        etl_bow_event_pidgins_to_bow_pidgin_csv_files(self._faces_bow_dir)

    def bow_event_pidgins_csvs_to_bow_pidgin_jsons(self):
        etl_bow_event_pidgins_csvs_to_bow_pidgin_jsons(self._faces_bow_dir)
        self._set_pidgin_events()

    def boat_ideas_to_bow_face_ideas(self):
        etl_boat_ideas_to_bow_face_ideas(self._boat_dir, self._faces_bow_dir)

    def bow_face_ideas_to_bow_event_otx_ideas(self):
        etl_bow_face_ideas_to_bow_event_otx_ideas(self._faces_bow_dir)

    def bow_event_ideas_to_inx_events(self):
        etl_bow_event_ideas_to_inx_events(self._faces_bow_dir, self._pidgin_events)

    def bow_inx_event_ideas_to_aft_faces(self):
        etl_bow_inx_event_ideas_to_aft_faces(self._faces_bow_dir, self._faces_aft_dir)

    def aft_face_ideas_to_csv_files(self):
        etl_aft_face_ideas_to_csv_files(self._faces_aft_dir)

    def etl_aft_face_csv_files2idea_staging_tables(
        self, conn_or_cursor: sqlite3_Connection
    ):
        etl_aft_face_csv_files2idea_staging_tables(conn_or_cursor, self._faces_aft_dir)

    def idea_staging_to_fiscal_tables(self, conn_or_cursor: sqlite3_Connection):
        etl_idea_staging_to_fiscal_tables(conn_or_cursor)

    def idea_staging_to_bud_tables(self, conn_or_cursor: sqlite3_Connection):
        etl_idea_staging_to_bud_tables(conn_or_cursor)

    def aft_faces_ideas_to_fiscal_mstr_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_fiscal_staging_tables_to_fiscal_csvs(conn_or_cursor, self._fiscal_mstr_dir)
        etl_fiscal_agg_tables_to_fiscal_csvs(conn_or_cursor, self._fiscal_mstr_dir)

    def fiscal_csvs_to_jsons(self):
        etl_fiscal_csvs_to_jsons(self._fiscal_mstr_dir)

    def bud_tables_to_event_bud_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_bud_tables_to_event_bud_csvs(conn_or_cursor, self._fiscal_mstr_dir)

    def event_bud_csvs_to_gift_json(self):
        etl_event_bud_csvs_to_gift_json(self._fiscal_mstr_dir)

    def event_gift_json_to_event_inherited_budunits(self):
        etl_event_gift_json_to_event_inherited_budunits(self._fiscal_mstr_dir)

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
    ocean_dir: str = None,
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
        _ocean_dir=ocean_dir,
        _pidgin_events={},
    )
    x_worldunit._set_world_dirs()
    if not x_worldunit._ocean_dir:
        x_worldunit.set_ocean_dir(create_path(x_worldunit._world_dir, "ocean"))
    return x_worldunit


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []
