from src.f00_instrument.file import (
    set_dir,
    create_path,
    get_dir_file_strs,
    delete_dir,
)
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
    JungleToZooTransformer,
    ZooStagingToZooAggTransformer,
    ZooAggToZooEventsTransformer,
    ZooEventsToEventsLogTransformer,
    ZooAggToNubStagingTransformer,
    ZooAggToStagingTransformer,
    etl_pidgin_staging_to_agg,
    zoo_agg_single_to_pidgin_staging,
    zoo_agg_to_pidgin_acct_staging,
    zoo_agg_to_pidgin_group_staging,
    zoo_agg_to_pidgin_node_staging,
    zoo_agg_to_pidgin_road_staging,
    EventsLogToEventsAggTransformer,
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
    pidgins: dict[AcctID, PidginUnit] = None
    timeconversions: dict[TimeLineLabel, TimeConversion] = None
    _events_dir: str = None
    _pidgins_dir: str = None
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
        self.pidgins[x_pidginunit.face_id] = x_pidginunit

    def add_pidginunit(self, face_id: AcctID):
        x_pidginunit = pidginunit_shop(face_id)
        self.set_pidginunit(x_pidginunit)

    def pidginunit_exists(self, face_id: AcctID) -> bool:
        return self.pidgins.get(face_id) != None

    def get_pidginunit(self, face_id: AcctID) -> PidginUnit:
        return self.pidgins.get(face_id)

    def del_pidginunit(self, face_id: TimeLinePoint):
        self.pidgins.pop(face_id)

    def del_all_pidginunits(self):
        self.pidgins = {}

    def pidgins_empty(self) -> bool:
        return self.pidgins == {}

    def _pidgin_dir(self, face_id: AcctID) -> str:
        return create_path(self._pidgins_dir, face_id)

    def save_pidginunit_files(self, face_id: AcctID):
        x_pidginunit = self.get_pidginunit(face_id)
        save_all_csvs_from_pidginunit(self._pidgin_dir(face_id), x_pidginunit)

    def pidgin_dir_exists(self, face_id: AcctID) -> bool:
        return os_path_exists(self._pidgin_dir(face_id))

    def _set_all_pidginunits_from_dirs(self):
        self.del_all_pidginunits()
        for dir_name in get_dir_file_strs(
            self._pidgins_dir, include_files=False
        ).keys():
            self.add_pidginunit(dir_name)

    def _delete_pidginunit_dir(self, event_id: TimeLinePoint):
        delete_dir(self._pidgin_dir(event_id))

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_id)
        self._events_dir = create_path(self._world_dir, "events")
        self._pidgins_dir = create_path(self._world_dir, "pidgins")
        self._jungle_dir = create_path(self._world_dir, "jungle")
        self._zoo_dir = create_path(self._world_dir, "zoo")
        set_dir(self._world_dir)
        set_dir(self._events_dir)
        set_dir(self._pidgins_dir)
        set_dir(self._jungle_dir)
        set_dir(self._zoo_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineLabel, TimeConversion]:
        return self.timeconversions

    def load_pidginunit_from_files(self, face_id: AcctID):
        x_pidginunit = init_pidginunit_from_dir(self._pidgin_dir(face_id))
        self.set_pidginunit(x_pidginunit)

    def jungle_to_zoo_staging(self):
        transformer = JungleToZooTransformer(self._jungle_dir, self._zoo_dir)
        transformer.transform()

    def zoo_staging_to_zoo_agg(self):
        transformer = ZooStagingToZooAggTransformer(self._zoo_dir)
        transformer.transform()

    def zoo_agg_to_zoo_events(self):
        transformer = ZooAggToZooEventsTransformer(self._zoo_dir)
        transformer.transform()

    def zoo_events_to_events_log(self):
        transformer = ZooEventsToEventsLogTransformer(self._zoo_dir)
        transformer.transform()

    def events_log_to_events_agg(self):
        transformer = EventsLogToEventsAggTransformer(self._zoo_dir)
        transformer.transform()

    def set_events_from_events_agg_file(self):
        self.events = {}
        events_file_path = create_path(self._zoo_dir, "events.xlsx")
        events_agg_df = pandas_read_excel(events_file_path, "events_agg")
        for index, event_agg_row in events_agg_df.iterrows():
            x_note = event_agg_row["note"]
            if x_note != "invalid because of conflicting event_id":
                self.set_event(event_agg_row["event_id"], event_agg_row["face_id"])

    def zoo_agg_to_acct_staging(self):
        legitimate_events = set(self.events.keys())
        zoo_agg_to_pidgin_acct_staging(legitimate_events, self._zoo_dir)

    def zoo_agg_to_group_staging(self):
        legitimate_events = set(self.events.keys())
        zoo_agg_to_pidgin_group_staging(legitimate_events, self._zoo_dir)

    def zoo_agg_to_node_staging(self):
        legitimate_events = set(self.events.keys())
        zoo_agg_to_pidgin_node_staging(legitimate_events, self._zoo_dir)

    def zoo_agg_to_road_staging(self):
        legitimate_events = set(self.events.keys())
        zoo_agg_to_pidgin_road_staging(legitimate_events, self._zoo_dir)

    def zoo_agg_to_nub_staging(self):
        legitimate_events = set(self.events.keys())
        transformer = ZooAggToNubStagingTransformer(self._zoo_dir, legitimate_events)
        transformer.transform()

    def pidgin_staging_to_agg(self):
        etl_pidgin_staging_to_agg(self._zoo_dir)

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
