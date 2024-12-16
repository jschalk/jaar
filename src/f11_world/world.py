from src.f00_instrument.file import set_dir, create_path
from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_None,
    get_0_if_None,
    get_empty_set_if_None,
)
from src.f01_road.finance_tran import TimeLinePoint, TimeConversion
from src.f01_road.road import (
    FaceID,
    EventID,
    FiscalID,
    WorldID,
    TimeLineLabel,
    get_default_world_id,
)
from src.f07_fiscal.fiscal import FiscalUnit
from src.f10_etl.transformers import (
    etl_ocean_to_zoo_staging,
    etl_zoo_staging_to_zoo_agg,
    etl_zoo_agg_to_zoo_valid,
    etl_zoo_agg_to_zoo_events,
    etl_zoo_events_to_events_log,
    etl_zoo_pidgin_staging_to_agg,
    etl_zoo_agg_to_pidgin_staging,
    etl_zoo_events_log_to_events_agg,
    get_events_dict_from_events_agg_file,
    etl_zoo_pidgin_agg_to_bow_face_dirs,
    etl_bow_face_pidgins_to_bow_event_pidgins,
    etl_bow_event_pidgins_to_bow_pidgin_csv_files,
    etl_bow_event_pidgins_csvs_to_bow_pidgin_jsons,
    etl_pidgin_jsons_inherit_younger_pidgins,
    etl_zoo_bricks_to_bow_face_bricks,
    etl_bow_face_bricks_to_bow_event_otx_bricks,
    get_fiscal_events_by_dirs,
    get_pidgin_events_by_dirs,
)
from dataclasses import dataclass


def get_default_worlds_dir() -> str:
    return "src/f11_world/examples/worlds"


class _set_fiscal_pidgin_Exception(Exception):
    pass


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    current_time: TimeLinePoint = None
    events: dict[EventID, FaceID] = None
    timeconversions: dict[TimeLineLabel, TimeConversion] = None
    _faces_otx_dir: str = None
    _faces_inx_dir: str = None
    _world_dir: str = None
    _ocean_dir: str = None
    _zoo_dir: str = None
    _fiscalunits: set[FiscalID] = None
    _fiscal_events: dict[FiscalID, set[EventID]] = None
    _pidgin_events: dict[FaceID, set[EventID]] = None

    def set_event(self, event_id: EventID, face_id: FaceID):
        self.events[event_id] = face_id

    def event_exists(self, event_id: EventID) -> bool:
        return self.events.get(event_id) != None

    def get_event(self, event_id: EventID) -> FaceID:
        return self.events.get(event_id)

    def legitimate_events(self) -> set[EventID]:
        return set(self.events.keys())

    def _event_dir(self, face_id: FaceID, event_id: EventID) -> str:
        face_dir = create_path(self._faces_otx_dir, face_id)
        return create_path(face_dir, event_id)

    def _set_fiscal_events(self):
        self._fiscal_events = get_fiscal_events_by_dirs(self._faces_otx_dir)

    def _set_pidgin_events(self):
        self._pidgin_events = get_pidgin_events_by_dirs(self._faces_otx_dir)

    def set_ocean_dir(self, x_dir: str):
        self._ocean_dir = x_dir
        set_dir(self._ocean_dir)

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_id)
        self._faces_otx_dir = create_path(self._world_dir, "faces_otx")
        self._faces_inx_dir = create_path(self._world_dir, "faces_inx")
        self._zoo_dir = create_path(self._world_dir, "zoo")
        set_dir(self._world_dir)
        set_dir(self._faces_otx_dir)
        set_dir(self._faces_inx_dir)
        set_dir(self._zoo_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineLabel, TimeConversion]:
        return self.timeconversions

    def ocean_to_zoo_staging(self):
        etl_ocean_to_zoo_staging(self._ocean_dir, self._zoo_dir)

    def zoo_staging_to_zoo_agg(self):
        etl_zoo_staging_to_zoo_agg(self._zoo_dir)

    def zoo_agg_to_zoo_valid(self):
        etl_zoo_agg_to_zoo_valid(self._zoo_dir, self.legitimate_events())

    def zoo_agg_to_zoo_events(self):
        etl_zoo_agg_to_zoo_events(self._zoo_dir)

    def zoo_events_to_events_log(self):
        etl_zoo_events_to_events_log(self._zoo_dir)

    def zoo_events_log_to_events_agg(self):
        etl_zoo_events_log_to_events_agg(self._zoo_dir)

    def set_events_from_events_agg_file(self):
        self.events = get_events_dict_from_events_agg_file(self._zoo_dir)

    def zoo_agg_to_pidgin_staging(self):
        etl_zoo_agg_to_pidgin_staging(self.legitimate_events(), self._zoo_dir)

    def zoo_pidgin_staging_to_agg(self):
        etl_zoo_pidgin_staging_to_agg(self._zoo_dir)

    def zoo_pidgin_agg_to_bow_face_dirs(self):
        etl_zoo_pidgin_agg_to_bow_face_dirs(self._zoo_dir, self._faces_otx_dir)

    def pidgin_jsons_inherit_younger_pidgins(self):
        etl_pidgin_jsons_inherit_younger_pidgins(
            self._faces_otx_dir, self._pidgin_events
        )

    def bow_face_pidgins_to_bow_event_pidgins(self):
        etl_bow_face_pidgins_to_bow_event_pidgins(self._faces_otx_dir)

    def bow_event_pidgins_to_bow_pidgin_csv_files(self):
        etl_bow_event_pidgins_to_bow_pidgin_csv_files(self._faces_otx_dir)

    def bow_event_pidgins_csvs_to_bow_pidgin_jsons(self):
        etl_bow_event_pidgins_csvs_to_bow_pidgin_jsons(self._faces_otx_dir)
        self._set_pidgin_events()

    def zoo_bricks_to_bow_face_bricks(self):
        etl_zoo_bricks_to_bow_face_bricks(self._zoo_dir, self._faces_otx_dir)

    def bow_face_bricks_to_bow_event_otx_bricks(self):
        etl_bow_face_bricks_to_bow_event_otx_bricks(self._faces_otx_dir)

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
    ocean_dir: str = None,
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
        _ocean_dir=ocean_dir,
        _fiscal_events={},
        _pidgin_events={},
    )
    x_worldunit._set_world_dirs()
    if not x_worldunit._ocean_dir:
        x_worldunit.set_ocean_dir(create_path(x_worldunit._world_dir, "ocean"))
    return x_worldunit


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []
