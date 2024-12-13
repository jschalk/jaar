from src.f00_instrument.file import set_dir, create_path
from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_None,
    get_0_if_None,
    get_empty_set_if_None,
)
from src.f01_road.finance_tran import TimeLinePoint, TimeConversion
from src.f01_road.road import (
    FaceID,
    FiscalID,
    WorldID,
    TimeLineLabel,
    get_default_world_id,
)
from src.f07_fiscal.fiscal import FiscalUnit
from src.f10_etl.transformers import (
    etl_mine_to_forge_staging,
    etl_forge_staging_to_forge_agg,
    etl_forge_agg_to_forge_valid,
    etl_forge_agg_to_forge_events,
    etl_forge_events_to_events_log,
    etl_pidgin_staging_to_agg,
    etl_forge_agg_to_pidgin_staging,
    etl_events_log_to_events_agg,
    get_events_dict_from_events_agg_file,
    etl_pidgin_agg_to_face_dirs,
    etl_face_pidgins_to_event_pidgins,
    etl_event_pidgins_to_pidgin_csv_files,
    etl_event_pidgins_csvs_to_pidgin_jsons,
    etl_pidgin_jsons_inherit_younger_pidgins,
    etl_forge_bricks_to_otx_face_bricks,
    etl_face_bricks_to_event_bricks,
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
    events: dict[TimeLinePoint, FaceID] = None
    timeconversions: dict[TimeLineLabel, TimeConversion] = None
    _faces_otx_dir: str = None
    _faces_inx_dir: str = None
    _world_dir: str = None
    _mine_dir: str = None
    _forge_dir: str = None
    _fiscalunits: set[FiscalID] = None
    _fiscal_events: dict[FiscalID, set[TimeLinePoint]] = None
    _pidgin_events: dict[FaceID, set[TimeLinePoint]] = None

    def set_event(self, event_id: TimeLinePoint, face_id: FaceID):
        self.events[event_id] = face_id

    def event_exists(self, event_id: TimeLinePoint) -> bool:
        return self.events.get(event_id) != None

    def get_event(self, event_id: TimeLinePoint) -> FaceID:
        return self.events.get(event_id)

    def legitimate_events(self) -> set[TimeLinePoint]:
        return set(self.events.keys())

    def _event_dir(self, face_id: FaceID, event_id: TimeLinePoint) -> str:
        face_dir = create_path(self._faces_otx_dir, face_id)
        return create_path(face_dir, event_id)

    def _set_fiscal_events(self):
        self._fiscal_events = get_fiscal_events_by_dirs(self._faces_otx_dir)

    def _set_pidgin_events(self):
        self._pidgin_events = get_pidgin_events_by_dirs(self._faces_otx_dir)

    def set_mine_dir(self, x_dir: str):
        self._mine_dir = x_dir
        set_dir(self._mine_dir)

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_id)
        self._faces_otx_dir = create_path(self._world_dir, "faces_otx")
        self._faces_inx_dir = create_path(self._world_dir, "faces_inx")
        self._forge_dir = create_path(self._world_dir, "forge")
        set_dir(self._world_dir)
        set_dir(self._faces_otx_dir)
        set_dir(self._faces_inx_dir)
        set_dir(self._forge_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineLabel, TimeConversion]:
        return self.timeconversions

    def mine_to_forge_staging(self):
        etl_mine_to_forge_staging(self._mine_dir, self._forge_dir)

    def forge_staging_to_forge_agg(self):
        etl_forge_staging_to_forge_agg(self._forge_dir)

    def forge_agg_to_forge_valid(self):
        etl_forge_agg_to_forge_valid(self._forge_dir, self.legitimate_events())

    def forge_agg_to_forge_events(self):
        etl_forge_agg_to_forge_events(self._forge_dir)

    def forge_events_to_events_log(self):
        etl_forge_events_to_events_log(self._forge_dir)

    def events_log_to_events_agg(self):
        etl_events_log_to_events_agg(self._forge_dir)

    def set_events_from_events_agg_file(self):
        self.events = get_events_dict_from_events_agg_file(self._forge_dir)

    def forge_agg_to_pidgin_staging(self):
        etl_forge_agg_to_pidgin_staging(self.legitimate_events(), self._forge_dir)

    def pidgin_staging_to_agg(self):
        etl_pidgin_staging_to_agg(self._forge_dir)

    def pidgin_agg_to_face_dirs(self):
        etl_pidgin_agg_to_face_dirs(self._forge_dir, self._faces_otx_dir)

    def pidgin_jsons_inherit_younger_pidgins(self):
        etl_pidgin_jsons_inherit_younger_pidgins(
            self._faces_otx_dir, self._pidgin_events
        )

    def face_pidgins_to_event_pidgins(self):
        etl_face_pidgins_to_event_pidgins(self._faces_otx_dir)

    def event_pidgins_to_pidgin_csv_files(self):
        etl_event_pidgins_to_pidgin_csv_files(self._faces_otx_dir)

    def event_pidgins_csvs_to_pidgin_jsons(self):
        etl_event_pidgins_csvs_to_pidgin_jsons(self._faces_otx_dir)
        self._set_pidgin_events()

    def forge_bricks_to_otx_face_bricks(self):
        etl_forge_bricks_to_otx_face_bricks(self._forge_dir, self._faces_otx_dir)

    def face_bricks_to_event_bricks(self):
        etl_face_bricks_to_event_bricks(self._faces_otx_dir)

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
    mine_dir: str = None,
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
        _mine_dir=mine_dir,
        _fiscal_events={},
        _pidgin_events={},
    )
    x_worldunit._set_world_dirs()
    if not x_worldunit._mine_dir:
        x_worldunit.set_mine_dir(create_path(x_worldunit._world_dir, "mine"))
    return x_worldunit


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []
