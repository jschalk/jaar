from src.f00_instrument.file import set_dir, create_path, get_dir_file_strs, delete_dir
from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_None,
    get_0_if_None,
    get_empty_set_if_None,
)
from src.f01_road.finance_tran import TimeLinePoint, TimeConversion
from src.f01_road.road import (
    AcctID,
    FiscalID,
    WorldID,
    TimeLineLabel,
    get_default_world_id,
)
from src.f07_fiscal.fiscal import FiscalUnit
from src.f10_etl.transformers import (
    etl_jungle_to_zoo_staging,
    etl_zoo_staging_to_zoo_agg,
    etl_zoo_agg_to_zoo_events,
    etl_zoo_events_to_events_log,
    etl_pidgin_staging_to_agg,
    etl_zoo_agg_to_pidgin_staging,
    etl_events_log_to_events_agg,
    get_events_dict_from_events_agg_file,
    etl_pidgin_agg_to_face_dirs,
    etl_face_pidgins_to_event_pidgins,
    etl_event_pidgins_to_pidgin_csv_files,
    etl_event_pidgins_csvs_to_pidgin_jsons,
    etl_zoo_bricks_to_face_bricks,
    etl_face_bricks_to_event_bricks,
)
from dataclasses import dataclass


def get_default_worlds_dir() -> str:
    return "src/f11_world/examples/worlds"


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    current_time: TimeLinePoint = None
    events: dict[TimeLinePoint, AcctID] = None
    timeconversions: dict[TimeLineLabel, TimeConversion] = None
    _faces_dir: str = None
    _fiscalunits: set[FiscalID] = None
    _world_dir: str = None
    _jungle_dir: str = None
    _zoo_dir: str = None

    def set_event(self, event_id: TimeLinePoint, face_id: AcctID):
        self.events[event_id] = face_id

    def event_exists(self, event_id: TimeLinePoint) -> bool:
        return self.events.get(event_id) != None

    def get_event(self, event_id: TimeLinePoint) -> bool:
        return self.events.get(event_id)

    def _event_dir(self, face_id: AcctID, event_id: TimeLinePoint) -> str:
        face_dir = create_path(self._faces_dir, face_id)
        return create_path(face_dir, event_id)

    def set_jungle_dir(self, x_dir: str):
        self._jungle_dir = x_dir
        set_dir(self._jungle_dir)

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_id)
        self._faces_dir = create_path(self._world_dir, "faces")
        self._zoo_dir = create_path(self._world_dir, "zoo")
        set_dir(self._world_dir)
        set_dir(self._faces_dir)
        set_dir(self._zoo_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineLabel, TimeConversion]:
        return self.timeconversions

    def jungle_to_zoo_staging(self):
        etl_jungle_to_zoo_staging(self._jungle_dir, self._zoo_dir)

    def zoo_staging_to_zoo_agg(self):
        etl_zoo_staging_to_zoo_agg(self._zoo_dir)

    def zoo_agg_to_zoo_events(self):
        etl_zoo_agg_to_zoo_events(self._zoo_dir)

    def zoo_events_to_events_log(self):
        etl_zoo_events_to_events_log(self._zoo_dir)

    def events_log_to_events_agg(self):
        etl_events_log_to_events_agg(self._zoo_dir)

    def set_events_from_events_agg_file(self):
        self.events = get_events_dict_from_events_agg_file(self._zoo_dir)

    def zoo_agg_to_pidgin_staging(self):
        legitimate_events = set(self.events.keys())
        etl_zoo_agg_to_pidgin_staging(legitimate_events, self._zoo_dir)

    def pidgin_staging_to_agg(self):
        etl_pidgin_staging_to_agg(self._zoo_dir)

    def pidgin_agg_to_face_dirs(self):
        etl_pidgin_agg_to_face_dirs(self._zoo_dir, self._faces_dir)

    def face_pidgins_to_event_pidgins(self):
        etl_face_pidgins_to_event_pidgins(self._faces_dir)

    def event_pidgins_to_pidgin_csv_files(self):
        etl_event_pidgins_to_pidgin_csv_files(self._faces_dir)

    def event_pidgins_csvs_to_pidgin_jsons(self):
        etl_event_pidgins_csvs_to_pidgin_jsons(self._faces_dir)

    def zoo_bricks_to_face_bricks(self):
        etl_zoo_bricks_to_face_bricks(self._zoo_dir, self._faces_dir)

    def face_bricks_to_event_bricks(self):
        etl_face_bricks_to_event_bricks(self._faces_dir)

    def get_dict(self) -> dict:
        return {
            "world_id": self.world_id,
            "current_time": self.current_time,
            "timeconversions": self.get_timeconversions_dict(),
            "events": self.events,
        }


def worldunit_shop(
    world_id: WorldID = None,
    worlds_dir: str = None,
    jungle_dir: str = None,
    current_time: TimeLinePoint = None,
    timeconversions: dict[TimeLineLabel, TimeConversion] = None,
    _fiscalunits: set[FiscalID] = None,
) -> WorldUnit:
    if world_id is None:
        world_id = get_default_world_id()
    if worlds_dir is None:
        worlds_dir = get_default_worlds_dir()
    x_worldunit = WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        current_time=get_0_if_None(current_time),
        timeconversions=get_empty_dict_if_None(timeconversions),
        events={},
        _fiscalunits=get_empty_set_if_None(_fiscalunits),
        _jungle_dir=jungle_dir,
    )
    x_worldunit._set_world_dirs()
    if not x_worldunit._jungle_dir:
        x_worldunit.set_jungle_dir(create_path(x_worldunit._world_dir, "jungle"))
    return x_worldunit


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []
