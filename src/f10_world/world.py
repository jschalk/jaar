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
from src.f08_pidgin.pidgin_config import get_quick_pidgens_column_ref
from src.f09_brick.brick_config import (
    get_brick_numbers,
    get_brick_format_filename,
    get_brick_category_ref,
)
from src.f09_brick.brick import get_brickref_obj
from src.f09_brick.pandas_tool import (
    get_zoo_staging_grouping_with_all_values_equal_df,
    get_new_sorting_columns,
    upsert_sheet,
)
from src.f09_brick.pidgin_toolbox import (
    save_all_csvs_from_pidginunit,
    init_pidginunit_from_dir,
)
from src.f10_world.world_tool import get_all_brick_dataframes, _create_events_agg_df
from src.f10_world.pidgin_staging_to_agg import pidginaggbook_shop, PidginCore
from pandas import read_excel as pandas_read_excel, concat as pandas_concat, DataFrame
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
            self._save_to_zoo_staging(brick_number, dfs)

    def _group_jungle_data(self):
        grouped_data = {}
        for ref in get_all_brick_dataframes(self.jungle_dir):
            df = self._read_and_tag_dataframe(ref)
            grouped_data.setdefault(ref.brick_number, []).append(df)
        return grouped_data

    def _read_and_tag_dataframe(self, ref):
        x_file_path = create_path(ref.file_dir, ref.file_name)
        df = pandas_read_excel(x_file_path, ref.sheet_name)
        df["file_dir"] = ref.file_dir
        df["file_name"] = ref.file_name
        df["sheet_name"] = ref.sheet_name
        return df

    def _save_to_zoo_staging(self, brick_number: str, dfs: list):
        final_df = pandas_concat(dfs)
        zoo_path = create_path(self.zoo_dir, f"{brick_number}.xlsx")
        upsert_sheet(zoo_path, "zoo_staging", final_df)


class ZooStagingToZooAggTransformer:
    def __init__(self, zoo_dir: str):
        self.zoo_dir = zoo_dir

    def transform(self):
        for brick_number in get_brick_numbers():
            zoo_brick_path = create_path(self.zoo_dir, f"{brick_number}.xlsx")
            if os_path_exists(zoo_brick_path):
                zoo_staging_df = pandas_read_excel(zoo_brick_path, "zoo_staging")
                otx_df = self._group_by_brick_columns(zoo_staging_df, brick_number)
                upsert_sheet(zoo_brick_path, "zoo_agg", otx_df)

    def _group_by_brick_columns(
        self, zoo_staging_df: DataFrame, brick_number: str
    ) -> DataFrame:
        brick_filename = get_brick_format_filename(brick_number)
        brickref = get_brickref_obj(brick_filename)
        required_columns = brickref.get_otx_keys_list()
        brick_columns_set = set(brickref._attributes.keys())
        brick_columns_list = get_new_sorting_columns(brick_columns_set)
        zoo_staging_df = zoo_staging_df[brick_columns_list]
        return get_zoo_staging_grouping_with_all_values_equal_df(
            zoo_staging_df, required_columns
        )


class ZooAggToZooEventsTransformer:
    def __init__(self, zoo_dir: str):
        self.zoo_dir = zoo_dir

    def transform(self):
        for brick_number in get_brick_numbers():
            zoo_brick_path = create_path(self.zoo_dir, f"{brick_number}.xlsx")
            if os_path_exists(zoo_brick_path):
                zoo_agg_df = pandas_read_excel(zoo_brick_path, "zoo_agg")
                events_df = self.get_unique_events(zoo_agg_df)
                upsert_sheet(zoo_brick_path, "zoo_events", events_df)
                # self._save_zoo_events(zoo_brick_path, events_df)

    def get_unique_events(self, zoo_agg_df: DataFrame) -> DataFrame:
        events_df = zoo_agg_df[["face_id", "event_id"]].drop_duplicates()
        events_df["note"] = (
            events_df["event_id"]
            .duplicated(keep=False)
            .apply(lambda x: "invalid because of conflicting event_id" if x else "")
        )
        return events_df.sort_values(["face_id", "event_id"])


class ZooEventsToEventsLogTransformer:
    def __init__(self, zoo_dir: str):
        self.zoo_dir = zoo_dir

    def transform(self):
        for brick_number in sorted(get_brick_numbers()):
            brick_file_name = f"{brick_number}.xlsx"
            zoo_brick_path = create_path(self.zoo_dir, brick_file_name)
            if os_path_exists(zoo_brick_path):
                sheet_name = "zoo_events"
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
        otx_events_df[["sheet_name"]] = "zoo_events"
        cols = ["file_dir", "file_name", "sheet_name", "face_id", "event_id", "note"]
        otx_events_df = otx_events_df[cols]
        return otx_events_df

    def _save_events_log_file(self, events_df: DataFrame):
        events_file_path = create_path(self.zoo_dir, "events.xlsx")
        events_log_str = "events_log"
        if os_path_exists(events_file_path):
            events_log_df = pandas_read_excel(events_file_path, events_log_str)
            events_df = pandas_concat([events_log_df, events_df])
        upsert_sheet(events_file_path, events_log_str, events_df)


class ZooAggToStagingTransformer:
    def __init__(
        self, zoo_dir: str, pidgin_category: str, legitmate_events: set[TimeLinePoint]
    ):
        self.zoo_dir = zoo_dir
        self.legitmate_events = legitmate_events
        self.pidgin_category = pidgin_category
        if self.pidgin_category == "bridge_acct_id":
            self.jaar_type = "AcctID"
        elif self.pidgin_category == "bridge_group_id":
            self.jaar_type = "GroupID"
        elif self.pidgin_category == "bridge_node":
            self.jaar_type = "RoadNode"
        elif self.pidgin_category == "bridge_road":
            self.jaar_type = "RoadUnit"
        else:
            raise Exception("not given pidgin_category")

    def transform(self):
        category_bricks = get_brick_category_ref().get(self.pidgin_category)
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_category)
        pidgin_columns.update({"face_id", "event_id"})
        pidgin_columns = get_new_sorting_columns(pidgin_columns)
        pidgin_columns.insert(0, "src_brick")
        pidgin_df = DataFrame(columns=pidgin_columns)
        for brick_number in sorted(category_bricks):
            brick_file_name = f"{brick_number}.xlsx"
            zoo_brick_path = create_path(self.zoo_dir, brick_file_name)
            if os_path_exists(zoo_brick_path):
                self.insert_staging_rows(
                    pidgin_df, brick_number, zoo_brick_path, pidgin_columns
                )

        pidgin_file_path = create_path(self.zoo_dir, "pidgin.xlsx")
        upsert_sheet(pidgin_file_path, self.get_sheet_staging_name(), pidgin_df)

    def insert_staging_rows(
        self,
        stage_df: DataFrame,
        brick_number: str,
        zoo_brick_path: str,
        df_columns: list[str],
    ):
        zoo_agg_df = pandas_read_excel(zoo_brick_path, sheet_name="zoo_agg")
        df_missing_cols = set(df_columns).difference(zoo_agg_df.columns)

        for index, x_row in zoo_agg_df.iterrows():
            event_id = x_row["event_id"]
            if event_id in self.legitmate_events:
                face_id = x_row["face_id"]
                otx_wall = None
                if "otx_wall" not in df_missing_cols:
                    otx_wall = x_row["otx_wall"]
                inx_wall = None
                if "inx_wall" not in df_missing_cols:
                    inx_wall = x_row["inx_wall"]
                unknown_word = None
                if "unknown_word" not in df_missing_cols:
                    unknown_word = x_row["unknown_word"]
                df_len = len(stage_df.index)
                stage_df.loc[df_len] = [
                    brick_number,
                    face_id,
                    event_id,
                    self.get_otx_obj(x_row),
                    self.get_inx_obj(x_row, df_missing_cols),
                    otx_wall,
                    inx_wall,
                    unknown_word,
                ]

    def get_sheet_staging_name(self) -> str:
        if self.jaar_type == "AcctID":
            return "acct_staging"
        elif self.jaar_type == "GroupID":
            return "group_staging"
        elif self.jaar_type == "RoadNode":
            return "node_staging"
        elif self.jaar_type == "RoadUnit":
            return "road_staging"

    def get_otx_obj(self, x_row) -> str:
        if self.jaar_type == "AcctID":
            return x_row["otx_acct_id"]
        elif self.jaar_type == "GroupID":
            return x_row["otx_group_id"]
        elif self.jaar_type == "RoadNode":
            return x_row["otx_node"]
        elif self.jaar_type == "RoadUnit":
            return x_row["otx_road"]
        return None

    def get_inx_obj(self, x_row, missing_col: set[str]) -> str:
        if self.jaar_type == "AcctID" and "inx_acct_id" not in missing_col:
            return x_row["inx_acct_id"]
        elif self.jaar_type == "GroupID" and "inx_group_id" not in missing_col:
            return x_row["inx_group_id"]
        elif self.jaar_type == "RoadNode" and "inx_node" not in missing_col:
            return x_row["inx_node"]
        elif self.jaar_type == "RoadUnit" and "inx_road" not in missing_col:
            return x_row["inx_road"]
        return None


class ZooAggToNubStagingTransformer:
    def __init__(self, zoo_dir: str, legitmate_events: set[TimeLinePoint]):
        self.zoo_dir = zoo_dir
        self.legitmate_events = legitmate_events

    def transform(self):
        nub_bricks = get_brick_category_ref().get("bridge_nub_label")
        nub_columns = get_quick_pidgens_column_ref().get("bridge_nub_label")
        nub_columns.update({"face_id", "event_id"})
        nub_columns = get_new_sorting_columns(nub_columns)
        nub_columns.insert(0, "src_brick")
        nub_df = DataFrame(columns=nub_columns)
        for brick_number in sorted(nub_bricks):
            brick_file_name = f"{brick_number}.xlsx"
            zoo_brick_path = create_path(self.zoo_dir, brick_file_name)
            if os_path_exists(zoo_brick_path):
                self.insert_legitmate_zoo_agg_nub_atts(
                    nub_df, brick_number, zoo_brick_path, nub_columns
                )

        pidgin_file_path = create_path(self.zoo_dir, "pidgin.xlsx")
        upsert_sheet(pidgin_file_path, "nub_staging", nub_df)

    def insert_legitmate_zoo_agg_nub_atts(
        self,
        nub_df: DataFrame,
        brick_number: str,
        zoo_brick_path: str,
        nub_columns: list[str],
    ):
        zoo_agg_df = pandas_read_excel(zoo_brick_path, sheet_name="zoo_agg")
        nub_missing_cols = set(nub_columns).difference(zoo_agg_df.columns)
        for index, x_row in zoo_agg_df.iterrows():
            event_id = x_row["event_id"]
            if event_id in self.legitmate_events:
                face_id = x_row["face_id"]
                otx_label = x_row["otx_label"]
                df_len = len(nub_df.index)
                otx_wall = None
                if "otx_wall" not in nub_missing_cols:
                    otx_wall = x_row["otx_wall"]
                inx_label = None
                if "inx_label" not in nub_missing_cols:
                    inx_label = x_row["inx_label"]
                inx_wall = None
                if "inx_wall" not in nub_missing_cols:
                    inx_wall = x_row["inx_wall"]
                unknown_word = None
                if "unknown_word" not in nub_missing_cols:
                    unknown_word = x_row["unknown_word"]
                nub_df.loc[df_len] = [
                    brick_number,
                    face_id,
                    event_id,
                    otx_label,
                    inx_label,
                    otx_wall,
                    inx_wall,
                    unknown_word,
                ]


class PidginStagingToAggTransformer:
    def __init__(self, zoo_dir: str, pidgin_category: str):
        self.zoo_dir = zoo_dir
        self.pidgin_category = pidgin_category
        self.file_path = create_path(self.zoo_dir, "pidgin.xlsx")
        if self.pidgin_category == "bridge_acct_id":
            self.jaar_type = "AcctID"
        elif self.pidgin_category == "bridge_group_id":
            self.jaar_type = "GroupID"
        elif self.pidgin_category == "bridge_node":
            self.jaar_type = "RoadNode"
        elif self.pidgin_category == "bridge_road":
            self.jaar_type = "RoadUnit"
        else:
            raise Exception("not given pidgin_category")

    def transform(self):
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_category)
        pidgin_columns.update({"face_id", "event_id"})
        pidgin_columns = get_new_sorting_columns(pidgin_columns)
        pidgin_agg_df = DataFrame(columns=pidgin_columns)
        self.insert_agg_rows(pidgin_agg_df)
        upsert_sheet(self.file_path, self.get_sheet_agg_name(), pidgin_agg_df)

    def insert_agg_rows(self, stage_df: DataFrame):
        pidgin_file_path = create_path(self.zoo_dir, "pidgin.xlsx")
        # def get_sheet_staging_name(self) -> str:
        #     if self.jaar_type == "AcctID":
        #         return "acct_staging"
        #     elif self.jaar_type == "GroupID":
        #         return "group_staging"
        #     elif self.jaar_type == "RoadNode":
        #         return "node_staging"
        #     elif self.jaar_type == "RoadUnit":
        #         return "road_staging"

        staging_df = pandas_read_excel(pidgin_file_path, sheet_name="acct_staging")

        eventaggs = pidginaggbook_shop()

        for index, x_row in staging_df.iterrows():
            x_pidgincore = PidginCore(
                event_id=x_row["event_id"],
                face_id=x_row["face_id"],
                otx_wall=x_row["otx_wall"],
                inx_wall=x_row["inx_wall"],
                unknown_word=x_row["unknown_word"],
                otx_obj=self.get_otx_obj(x_row),
                inx_obj=self.get_inx_obj(x_row),
            )
            eventaggs.eval_pidgincore(x_pidgincore)

    def get_otx_obj(self, x_row) -> str:
        if self.jaar_type == "AcctID":
            return x_row["otx_acct_id"]
        elif self.jaar_type == "GroupID":
            return x_row["otx_group_id"]
        elif self.jaar_type == "RoadNode":
            return x_row["otx_node"]
        elif self.jaar_type == "RoadUnit":
            return x_row["otx_road"]
        return None

    def get_inx_obj(self, x_row, missing_col: set[str]) -> str:
        if self.jaar_type == "AcctID" and "inx_acct_id" not in missing_col:
            return x_row["inx_acct_id"]
        elif self.jaar_type == "GroupID" and "inx_group_id" not in missing_col:
            return x_row["inx_group_id"]
        elif self.jaar_type == "RoadNode" and "inx_node" not in missing_col:
            return x_row["inx_node"]
        elif self.jaar_type == "RoadUnit" and "inx_road" not in missing_col:
            return x_row["inx_road"]
        return None


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

    # def get_db_path(self) -> str:
    #     return create_path(self._world_dir, "wrd.db")

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
        events_file_path = create_path(self._zoo_dir, "events.xlsx")
        events_log_df = pandas_read_excel(events_file_path, "events_log")
        events_agg_df = _create_events_agg_df(events_log_df)
        upsert_sheet(events_file_path, "events_agg", events_agg_df)

    def set_events_from_events_agg(self):
        self.events = {}
        events_file_path = create_path(self._zoo_dir, "events.xlsx")
        events_agg_df = pandas_read_excel(events_file_path, "events_agg")
        for index, event_agg_row in events_agg_df.iterrows():
            x_note = event_agg_row["note"]
            if x_note != "invalid because of conflicting event_id":
                self.set_event(event_agg_row["event_id"], event_agg_row["face_id"])

    def zoo_agg_to_acct_staging(self):
        pidgin_cat = "bridge_acct_id"
        legitmate_events = set(self.events.keys())
        transformer = ZooAggToStagingTransformer(
            self._zoo_dir, pidgin_cat, legitmate_events
        )
        transformer.transform()

    def zoo_agg_to_group_staging(self):
        pidgin_cat = "bridge_group_id"
        legitmate_events = set(self.events.keys())
        transformer = ZooAggToStagingTransformer(
            self._zoo_dir, pidgin_cat, legitmate_events
        )
        transformer.transform()

    def zoo_agg_to_node_staging(self):
        pidgin_cat = "bridge_node"
        legitmate_events = set(self.events.keys())
        transformer = ZooAggToStagingTransformer(
            self._zoo_dir, pidgin_cat, legitmate_events
        )
        transformer.transform()

    def zoo_agg_to_road_staging(self):
        pidgin_cat = "bridge_road"
        legitmate_events = set(self.events.keys())
        transformer = ZooAggToStagingTransformer(
            self._zoo_dir, pidgin_cat, legitmate_events
        )
        transformer.transform()

    def zoo_agg_to_nub_staging(self):
        legitmate_events = set(self.events.keys())
        transformer = ZooAggToNubStagingTransformer(self._zoo_dir, legitmate_events)
        transformer.transform()

    def acct_staging_to_acct_agg(self):
        pidgin_cat = "bridge_acct_id"
        transformer = PidginStagingToAggTransformer(self._zoo_dir, pidgin_cat)
        transformer.transform()

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
