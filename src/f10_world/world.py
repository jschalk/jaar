from src.f00_instrument.file import set_dir, create_path, get_dir_file_strs, delete_dir
from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_empty_set_if_none,
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
from src.f08_pidgin.pidgin import PidginUnit, pidginunit_shop
from src.f09_brick.pidgin_toolbox import (
    save_all_csvs_from_pidginunit,
    init_pidginunit_from_dir,
)
from src.f10_world.transformers import (
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
)
from pandas import read_excel as pandas_read_excel
from dataclasses import dataclass
from os.path import exists as os_path_exists


def get_default_worlds_dir() -> str:
    return "src/f10_world/examples/worlds"


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    current_time: TimeLinePoint = None
    events: dict[TimeLinePoint, AcctID] = None
    pidgins: dict[TimeLinePoint, PidginUnit] = None
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

    def set_pidginunit(self, x_pidginunit: PidginUnit):
        self.pidgins[x_pidginunit.event_id] = x_pidginunit

    def add_pidginunit(self, face_id: AcctID, event_id: TimeLinePoint):
        self.set_pidginunit(pidginunit_shop(face_id, event_id))

    def pidginunit_exists(self, event_id: TimeLinePoint) -> bool:
        return self.pidgins.get(event_id) != None

    def get_pidginunit(self, event_id: TimeLinePoint) -> PidginUnit:
        return self.pidgins.get(event_id)

    def del_pidginunit(self, event_id: TimeLinePoint):
        self.pidgins.pop(event_id)

    def del_all_pidginunits(self):
        self.pidgins = {}

    def pidgins_empty(self) -> bool:
        return self.pidgins == {}

    def _event_dir(self, face_id: AcctID, event_id: TimeLinePoint) -> str:
        face_dir = create_path(self._faces_dir, face_id)
        return create_path(face_dir, event_id)

    def save_pidginunit_files(self, face_id: AcctID, event_id: AcctID):
        x_pidginunit = self.get_pidginunit(event_id)
        save_all_csvs_from_pidginunit(self._event_dir(face_id, event_id), x_pidginunit)

    def pidgin_dir_exists(self, face_id: AcctID, event_id: TimeLinePoint) -> bool:
        return os_path_exists(self._event_dir(face_id, event_id))

    def _set_all_pidginunits_from_dirs(self):
        self.del_all_pidginunits()
        for face_dir in get_dir_file_strs(self._faces_dir, include_files=False).keys():
            for event_dir in get_dir_file_strs(face_dir, include_files=False).keys():
                self.add_pidginunit(face_dir, int(event_dir))

    def _delete_pidginunit_dir(self, face_id: AcctID, event_id: TimeLinePoint):
        face_dir = create_path(self._faces_dir, face_id)
        delete_dir(create_path(face_dir, event_id))

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_id)
        self._faces_dir = create_path(self._world_dir, "pidgins")
        self._jungle_dir = create_path(self._world_dir, "jungle")
        self._zoo_dir = create_path(self._world_dir, "zoo")
        set_dir(self._world_dir)
        set_dir(self._faces_dir)
        set_dir(self._jungle_dir)
        set_dir(self._zoo_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineLabel, TimeConversion]:
        return self.timeconversions

    def load_pidginunit_from_files(self, face_id: AcctID, event_id: TimeLinePoint):
        x_pidginunit = init_pidginunit_from_dir(self._event_dir(face_id, event_id))
        self.set_pidginunit(x_pidginunit)

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

    def get_dict(self) -> dict:
        return {
            "world_id": self.world_id,
            "current_time": self.current_time,
            "timeconversions": self.get_timeconversions_dict(),
            "events": self.events,
            "pidgins": self.pidgins,
        }


def worldunit_shop(
    world_id: WorldID = None,
    worlds_dir: str = None,
    current_time: TimeLinePoint = None,
    timeconversions: dict[TimeLineLabel, TimeConversion] = None,
    pidgins: dict[AcctID, PidginUnit] = None,
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
        timeconversions=get_empty_dict_if_none(timeconversions),
        events={},
        pidgins=get_empty_dict_if_none(pidgins),
        _fiscalunits=get_empty_set_if_none(_fiscalunits),
    )
    x_worldunit._set_world_dirs()
    return x_worldunit


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []
