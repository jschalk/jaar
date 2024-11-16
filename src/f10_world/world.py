from src.f00_instrument.file import (
    set_dir,
    create_file_path,
    get_dir_file_strs,
    delete_dir,
)
from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_empty_set_if_none,
)
from src.f01_road.finance_tran import TimeLinePoint, TimeConversion
from src.f01_road.road import FiscalID, WorldID, TimeLineLabel, get_default_world_id
from src.f07_fiscal.fiscal import FiscalUnit
from src.f08_pidgin.pidgin import PidginUnit, pidginunit_shop
from src.f09_brick.brick_config import (
    get_brick_numbers,
    get_brick_format_filename,
    get_quick_bricks_column_ref,
)
from src.f09_brick.brick import get_brickref_obj
from src.f09_brick.pandas_tool import _get_pidgen_brick_format_filenames
from src.f09_brick.pidgin_toolbox import (
    save_all_csvs_from_pidginunit,
    init_pidginunit_from_dir,
)
from src.f09_brick.pandas_tool import (
    get_new_sorting_columns,
    get_grouping_with_all_values_equal_df,
)
from src.f10_world.world_tool import get_all_brick_dataframes
from pandas import (
    ExcelWriter,
    read_excel as pandas_read_excel,
    concat as pandas_concat,
    DataFrame,
)
from dataclasses import dataclass
from os.path import exists as os_path_exists


def get_default_worlds_dir() -> str:
    return "src/f10_world/examples/worlds"


class JungleToZooTransformer:
    def __init__(self, jungle_dir: str, zoo_dir: str):
        self.jungle_dir = jungle_dir
        self.zoo_dir = zoo_dir

    def transform(self):
        for brick_number, dfs in self._group_jungle_data().items():
            self._save_consolidated_brick(brick_number, dfs)

    def _group_jungle_data(self):
        grouped_data = {}
        for ref in get_all_brick_dataframes(self.jungle_dir):
            df = self._read_and_tag_dataframe(ref)
            grouped_data.setdefault(ref.brick_number, []).append(df)
        return grouped_data

    def _read_and_tag_dataframe(self, ref):
        x_file_path = create_file_path(ref.file_dir, ref.file_name)
        df = pandas_read_excel(x_file_path, ref.sheet_name)
        df["file_dir"] = ref.file_dir
        df["file_name"] = ref.file_name
        df["sheet_name"] = ref.sheet_name
        return df

    def _save_consolidated_brick(self, brick_number: str, dfs: list):
        final_df = pandas_concat(dfs)
        zoo_path = create_file_path(self.zoo_dir, f"{brick_number}.xlsx")
        with ExcelWriter(zoo_path) as writer:
            final_df.to_excel(writer, sheet_name="zoo", index=False)


class ZooToOtxTransformer:
    def __init__(self, zoo_dir: str):
        self.zoo_dir = zoo_dir

    def transform(self):
        for brick_number in get_brick_numbers():
            zoo_brick_path = create_file_path(self.zoo_dir, f"{brick_number}.xlsx")
            if os_path_exists(zoo_brick_path):
                zoo_df = pandas_read_excel(zoo_brick_path, "zoo")
                otx_df = self._group_by_brick_columns(zoo_df, brick_number)
                self._save_otx_brick(zoo_brick_path, otx_df)

    def _group_by_brick_columns(
        self, zoo_df: DataFrame, brick_number: str
    ) -> DataFrame:
        brick_filename = get_brick_format_filename(brick_number)
        brickref = get_brickref_obj(brick_filename)
        required_columns = brickref.get_otx_keys_list()
        brick_columns_set = set(brickref._attributes.keys())
        brick_columns_list = get_new_sorting_columns(brick_columns_set)
        zoo_df = zoo_df[brick_columns_list]
        return get_grouping_with_all_values_equal_df(zoo_df, required_columns)

    def _save_otx_brick(self, brick_path: str, zoo_df: DataFrame):
        with ExcelWriter(brick_path) as writer:
            zoo_df.to_excel(writer, sheet_name="otx", index=False)


class OtxToOtxEventsTransformer:
    def __init__(self, zoo_dir: str):
        self.zoo_dir = zoo_dir

    def transform(self):
        for brick_number in get_brick_numbers():
            zoo_brick_path = create_file_path(self.zoo_dir, f"{brick_number}.xlsx")
            if os_path_exists(zoo_brick_path):
                otx_df = pandas_read_excel(zoo_brick_path, "otx")
                events_df = self.get_unique_events(otx_df)
                self._save_otx_brick(zoo_brick_path, events_df)

    def get_unique_events(self, otx_df: DataFrame) -> DataFrame:
        events_df = otx_df[["face_id", "event_id"]].drop_duplicates()
        events_df["note"] = (
            events_df["event_id"]
            .duplicated(keep=False)
            .apply(lambda x: "invalid because of conflicting event_id" if x else "")
        )
        return events_df.sort_values(["face_id", "event_id"])

    def _save_otx_brick(self, brick_path: str, events_df: DataFrame):
        with ExcelWriter(brick_path) as writer:
            events_df.to_excel(writer, sheet_name="otx_events", index=False)


class OtxEventsToEventsLogTransformer:
    def __init__(self, zoo_dir: str):
        self.zoo_dir = zoo_dir

    def transform(self):
        for brick_number in get_brick_numbers():
            brick_file_name = f"{brick_number}.xlsx"
            zoo_brick_path = create_file_path(self.zoo_dir, brick_file_name)
            if os_path_exists(zoo_brick_path):
                sheet_name = "otx_events"
                otx_events_df = pandas_read_excel(zoo_brick_path, sheet_name)
                events_log_df = self.get_event_log_df(
                    otx_events_df, self.zoo_dir, brick_file_name
                )
                self._save_events_log_file(events_log_df)

    def get_event_log_df(
        self, otx_events_df: DataFrame, x_dir: str, x_file_name: str
    ) -> DataFrame:
        otx_events_df[["file_dir"]] = x_dir
        otx_events_df[["file_name"]] = x_file_name
        otx_events_df[["sheet_name"]] = "otx_events"
        otx_events_df = otx_events_df[
            ["file_dir", "file_name", "sheet_name", "face_id", "event_id", "note"]
        ]
        file_name_str = "file_name"
        print(f"{otx_events_df[file_name_str]=}")
        return otx_events_df

    def _save_events_log_file(self, events_df: DataFrame):
        events_file_path = create_file_path(self.zoo_dir, "events.xlsx")
        print(f"{events_file_path=}")
        with ExcelWriter(events_file_path) as writer:
            events_df.to_excel(writer, sheet_name="events_log", index=False)


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    current_time: TimeLinePoint = None
    events: dict[TimeLinePoint, PidginUnit] = None
    _events_dir: str = None
    timeconversions: dict[TimeLineLabel, TimeConversion] = None
    _fiscalunits: set[FiscalID] = None
    _world_dir: str = None
    _jungle_dir: str = None
    _zoo_dir: str = None

    def set_event_id(self, event_id: TimeLinePoint, x_pidginunit: PidginUnit = None):
        if x_pidginunit is None:
            x_pidginunit = pidginunit_shop(event_id)
        self.events[event_id] = x_pidginunit

    def event_id_exists(self, event_id: TimeLinePoint) -> bool:
        return self.events.get(event_id) != None

    def get_pidginunit(self, event_id: TimeLinePoint) -> PidginUnit:
        return self.events.get(event_id)

    def del_event_id(self, event_id: TimeLinePoint):
        self.events.pop(event_id)

    def del_all_event_id(self):
        self.events = {}

    def events_empty(self) -> bool:
        return self.events == {}

    def _event_dir(self, event_id: TimeLinePoint) -> str:
        return create_file_path(self._events_dir, event_id)

    def save_pidginunit_files(self, event_id: TimeLinePoint):
        x_pidginunit = self.get_pidginunit(event_id)
        save_all_csvs_from_pidginunit(self._event_dir(event_id), x_pidginunit)

    def event_dir_exists(self, event_id: TimeLinePoint) -> bool:
        return os_path_exists(self._event_dir(event_id))

    def _set_all_events_from_dirs(self):
        self.del_all_event_id()
        for dir_name in get_dir_file_strs(self._events_dir, include_files=False).keys():
            self.set_event_id(dir_name)

    def _delete_pidginunit_dir(self, event_id: TimeLinePoint):
        delete_dir(self._event_dir(event_id))

    # def get_db_path(self) -> str:
    #     return create_file_path(self._world_dir, "wrd.db")

    # def _create_wrd_db(self):
    #     engine = create_engine(f"sqlite:///{self.get_db_path()}", echo=False)
    #     brick_modelsBase.metadata.create_all(engine)
    #     engine.dispose()

    # def db_exists(self) -> bool:
    #     return os_path_exists(self.get_db_path())

    # def get_db_engine(self) -> Engine:
    #     if self.db_exists() is False:
    #         self._create_wrd_db()
    #     return create_engine(f"sqlite:///{self.get_db_path()}", echo=False)

    def _set_world_dirs(self):
        self._world_dir = create_file_path(self.worlds_dir, self.world_id)
        self._events_dir = create_file_path(self._world_dir, "events")
        self._jungle_dir = create_file_path(self._world_dir, "jungle")
        self._zoo_dir = create_file_path(self._world_dir, "zoo")
        if not os_path_exists(self._world_dir):
            set_dir(self._world_dir)
        if not os_path_exists(self._events_dir):
            set_dir(self._events_dir)
        if not os_path_exists(self._jungle_dir):
            set_dir(self._jungle_dir)
        if not os_path_exists(self._zoo_dir):
            set_dir(self._zoo_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineLabel, TimeConversion]:
        return self.timeconversions

    def load_pidginunit_from_files(self, event_id: TimeLinePoint):
        x_pidginunit = init_pidginunit_from_dir(self._event_dir(event_id))
        self.set_event_id(event_id, x_pidginunit)

    def jungle_to_zoo(self):
        transformer = JungleToZooTransformer(self._jungle_dir, self._zoo_dir)
        transformer.transform()

    def zoo_to_otx(self):
        transformer = ZooToOtxTransformer(self._zoo_dir)
        transformer.transform()

    def otx_to_faces_event(self):
        pidgen_brick_filenames = _get_pidgen_brick_format_filenames()
        # for pidgen_brick_filename in pidgen_brick_filenames:
        #     pidgen_brick_path = create_file_path(self._zoo_dir, pidgen_brick_filename)
        #     df = pandas_read_excel(pidgen_brick_path, "otx")

        #     print(f"{pidgen_brick_path=}")
        #     print(f"{df=}")

    def otx_to_otx_events(self):
        transformer = OtxToOtxEventsTransformer(self._zoo_dir)
        transformer.transform()

    def otx_events_to_events_log(self):
        transformer = OtxEventsToEventsLogTransformer(self._zoo_dir)
        transformer.transform()
        print("huh")

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
    current_time: TimeLinePoint = None,
    timeconversions: dict[TimeLineLabel, TimeConversion] = None,
    events: set[str] = None,
    _fiscalunits: set[FiscalID] = None,
    in_memory_db: bool = None,
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
        events=get_empty_dict_if_none(events),
        _events_dir=create_file_path(worlds_dir, "events"),
        _fiscalunits=get_empty_set_if_none(_fiscalunits),
    )
    x_worldunit._set_world_dirs()
    return x_worldunit


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []
