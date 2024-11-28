from src.f00_instrument.file import create_path
from src.f01_road.finance_tran import TimeLinePoint
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
from src.f10_world.world_tool import get_all_brick_dataframes
from src.f10_world.pidgin_agg import (
    pidginheartbook_shop,
    PidginHeartRow,
    PidginHeartBook,
    pidginbodybook_shop,
    PidginBodyRow,
    PidginBodyBook,
)
from pandas import read_excel as pandas_read_excel, concat as pandas_concat, DataFrame
from os.path import exists as os_path_exists


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
        upsert_sheet(self.file_path, "acct_agg", pidgin_agg_df)

    def insert_agg_rows(self, pidgin_agg_df: DataFrame):
        pidgin_file_path = create_path(self.zoo_dir, "pidgin.xlsx")
        staging_df = pandas_read_excel(pidgin_file_path, sheet_name="acct_staging")

        x_pidginheartbook = self.get_pidginheart_validations(staging_df)
        # pidginbodybook_shop()
        # for pidginheartrow in x_pidginheartbook.pidginheartcores.values():
        #     df_len = len(staging_df.index)
        #     pidgin_agg_df.loc[df_len] = [
        #         face_id,
        #         event_id,
        #         self.get_otx_obj(x_row),
        #         self.get_inx_obj(x_row, df_missing_cols),
        #         otx_wall,
        #         inx_wall,
        #         unknown_word,
        #     ]

        #         event_id=x_row["event_id"],
        #         face_id=x_row["face_id"],
        #         otx_wall=x_row["otx_wall"],
        #         inx_wall=x_row["inx_wall"],
        #         unknown_word=x_row["unknown_word"],

    def get_pidginheart_validations(self, staging_df: DataFrame) -> PidginHeartBook:
        x_pidginheartbook = pidginheartbook_shop()
        for index, x_row in staging_df.iterrows():
            x_pidginheartcore = PidginHeartRow(
                event_id=x_row["event_id"],
                face_id=x_row["face_id"],
                otx_wall=x_row["otx_wall"],
                inx_wall=x_row["inx_wall"],
                unknown_word=x_row["unknown_word"],
            )
            x_pidginheartbook.eval_pidginheartrow(x_pidginheartcore)
        return x_pidginheartbook

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

    def get_inx_obj(self, x_row) -> str:
        if self.jaar_type == "AcctID":
            return x_row["inx_acct_id"]
        elif self.jaar_type == "GroupID":
            return x_row["inx_group_id"]
        elif self.jaar_type == "RoadNode":
            return x_row["inx_node"]
        elif self.jaar_type == "RoadUnit":
            return x_row["inx_road"]
        return None

    def get_sheet_agg_name(self) -> str:
        if self.jaar_type == "AcctID":
            return "acct_agg"
        elif self.jaar_type == "GroupID":
            return "group_agg"
        elif self.jaar_type == "RoadNode":
            return "node_agg"
        elif self.jaar_type == "RoadUnit":
            return "road_agg"
