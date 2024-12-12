from src.f00_instrument.file import create_path, get_dir_file_strs, save_file, open_file
from src.f01_road.finance_tran import TimeLinePoint, FiscalID
from src.f01_road.road import FaceID
from src.f08_pidgin.pidgin import get_pidginunit_from_json, inherit_pidginunit
from src.f08_pidgin.pidgin_config import get_quick_pidgens_column_ref
from src.f09_brick.brick_config import (
    get_brick_numbers,
    get_brick_format_filename,
    get_brick_category_ref,
)
from src.f09_brick.brick import get_brickref_obj
from src.f09_brick.pandas_tool import (
    get_sorting_columns,
    upsert_sheet,
    split_excel_into_dirs,
    sheet_exists,
    _get_pidgen_brick_format_filenames,
    get_forge_staging_grouping_with_all_values_equal_df,
    translate_all_columns_dataframe,
)
from src.f09_brick.pidgin_toolbox import init_pidginunit_from_dir
from src.f10_etl.brick_collector import get_all_brick_dataframes, BrickFileRef
from src.f10_etl.pidgin_agg import (
    pidginheartbook_shop,
    PidginHeartRow,
    PidginHeartBook,
    pidginbodybook_shop,
    PidginBodyRow,
    PidginBodyBook,
)
from pandas import read_excel as pandas_read_excel, concat as pandas_concat, DataFrame
from os.path import exists as os_path_exists


class not_given_pidgin_category_Exception(Exception):
    pass


BRIDGES_CATEGORYS = {
    "bridge_acct_id": "AcctID",
    "bridge_group_id": "GroupID",
    "bridge_idea": "IdeaUnit",
    "bridge_road": "RoadUnit",
}

JAAR_TYPES = {
    "AcctID": {
        "stage": "acct_staging",
        "agg": "acct_agg",
        "csv_filename": "acct.csv",
        "otx_obj": "otx_acct_id",
        "inx_obj": "inx_acct_id",
    },
    "GroupID": {
        "stage": "group_staging",
        "agg": "group_agg",
        "csv_filename": "group.csv",
        "otx_obj": "otx_group_id",
        "inx_obj": "inx_group_id",
    },
    "IdeaUnit": {
        "stage": "idea_staging",
        "agg": "idea_agg",
        "csv_filename": "idea.csv",
        "otx_obj": "otx_idea",
        "inx_obj": "inx_idea",
    },
    "RoadUnit": {
        "stage": "road_staging",
        "agg": "road_agg",
        "csv_filename": "road.csv",
        "otx_obj": "otx_road",
        "inx_obj": "inx_road",
    },
}


def get_jaar_type(pidgin_category: str) -> str:
    if pidgin_category not in BRIDGES_CATEGORYS:
        raise not_given_pidgin_category_Exception("not given pidgin_category")
    return BRIDGES_CATEGORYS[pidgin_category]


def get_sheet_stage_name(jaar_type: str) -> str:
    return JAAR_TYPES[jaar_type]["stage"]


def get_sheet_agg_name(jaar_type: str) -> str:
    return JAAR_TYPES[jaar_type]["agg"]


def get_otx_obj(jaar_type, x_row) -> str:
    return x_row[JAAR_TYPES[jaar_type]["otx_obj"]]


def get_inx_obj(jaar_type, x_row) -> str:
    return x_row[JAAR_TYPES[jaar_type]["inx_obj"]]


def etl_mine_to_forge_staging(mine_dir: str, forge_dir: str):
    transformer = JungleToZooTransformer(mine_dir, forge_dir)
    transformer.transform()


class JungleToZooTransformer:
    def __init__(self, mine_dir: str, forge_dir: str):
        self.mine_dir = mine_dir
        self.forge_dir = forge_dir

    def transform(self):
        for brick_number, dfs in self._group_mine_data().items():
            self._save_to_forge_staging(brick_number, dfs)

    def _group_mine_data(self):
        grouped_data = {}
        for ref in get_all_brick_dataframes(self.mine_dir):
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

    def _save_to_forge_staging(self, brick_number: str, dfs: list):
        final_df = pandas_concat(dfs)
        forge_path = create_path(self.forge_dir, f"{brick_number}.xlsx")
        upsert_sheet(forge_path, "forge_staging", final_df)


def get_existing_excel_brick_file_refs(x_dir: str) -> list[BrickFileRef]:
    existing_excel_brick_filepaths = []
    for brick_number in sorted(get_brick_numbers()):
        brick_filename = f"{brick_number}.xlsx"
        x_brick_path = create_path(x_dir, brick_filename)
        if os_path_exists(x_brick_path):
            x_fileref = BrickFileRef(
                file_dir=x_dir, file_name=brick_filename, brick_number=brick_number
            )
            existing_excel_brick_filepaths.append(x_fileref)
    return existing_excel_brick_filepaths


def etl_forge_staging_to_forge_agg(forge_dir):
    transformer = ZooStagingToZooAggTransformer(forge_dir)
    transformer.transform()


class ZooStagingToZooAggTransformer:
    def __init__(self, forge_dir: str):
        self.forge_dir = forge_dir

    def transform(self):
        for br_ref in get_existing_excel_brick_file_refs(self.forge_dir):
            forge_brick_path = create_path(br_ref.file_dir, br_ref.file_name)
            forge_staging_df = pandas_read_excel(forge_brick_path, "forge_staging")
            otx_df = self._group_by_brick_columns(forge_staging_df, br_ref.brick_number)
            upsert_sheet(forge_brick_path, "forge_agg", otx_df)

    def _group_by_brick_columns(
        self, forge_staging_df: DataFrame, brick_number: str
    ) -> DataFrame:
        brick_filename = get_brick_format_filename(brick_number)
        brickref = get_brickref_obj(brick_filename)
        required_columns = brickref.get_otx_keys_list()
        brick_columns_set = set(brickref._attributes.keys())
        brick_columns_list = get_sorting_columns(brick_columns_set)
        forge_staging_df = forge_staging_df[brick_columns_list]
        return get_forge_staging_grouping_with_all_values_equal_df(
            forge_staging_df, required_columns
        )


def etl_forge_agg_to_forge_valid(forge_dir: str, legitimate_events: set[TimeLinePoint]):
    transformer = ZooAggToZooValidTransformer(forge_dir, legitimate_events)
    transformer.transform()


class ZooAggToZooValidTransformer:
    def __init__(self, forge_dir: str, legitimate_events: set[TimeLinePoint]):
        self.forge_dir = forge_dir
        self.legitimate_events = legitimate_events

    def transform(self):
        for br_ref in get_existing_excel_brick_file_refs(self.forge_dir):
            forge_brick_path = create_path(br_ref.file_dir, br_ref.file_name)
            forge_agg = pandas_read_excel(forge_brick_path, "forge_agg")
            forge_valid_df = forge_agg[
                forge_agg["event_id"].isin(self.legitimate_events)
            ]
            upsert_sheet(forge_brick_path, "forge_valid", forge_valid_df)

    # def _group_by_brick_columns(
    #     self, forge_staging_df: DataFrame, brick_number: str
    # ) -> DataFrame:
    #     brick_filename = get_brick_format_filename(brick_number)
    #     brickref = get_brickref_obj(brick_filename)
    #     required_columns = brickref.get_otx_keys_list()
    #     brick_columns_set = set(brickref._attributes.keys())
    #     brick_columns_list = get_sorting_columns(brick_columns_set)
    #     forge_staging_df = forge_staging_df[brick_columns_list]
    #     return get_forge_staging_grouping_with_all_values_equal_df(
    #         forge_staging_df, required_columns
    #     )


def etl_forge_agg_to_forge_events(forge_dir):
    transformer = ZooAggToZooEventsTransformer(forge_dir)
    transformer.transform()


class ZooAggToZooEventsTransformer:
    def __init__(self, forge_dir: str):
        self.forge_dir = forge_dir

    def transform(self):
        for file_ref in get_existing_excel_brick_file_refs(self.forge_dir):
            forge_brick_path = create_path(self.forge_dir, file_ref.file_name)
            forge_agg_df = pandas_read_excel(forge_brick_path, "forge_agg")
            events_df = self.get_unique_events(forge_agg_df)
            upsert_sheet(forge_brick_path, "forge_events", events_df)

    def get_unique_events(self, forge_agg_df: DataFrame) -> DataFrame:
        events_df = forge_agg_df[["face_id", "event_id"]].drop_duplicates()
        events_df["note"] = (
            events_df["event_id"]
            .duplicated(keep=False)
            .apply(lambda x: "invalid because of conflicting event_id" if x else "")
        )
        return events_df.sort_values(["face_id", "event_id"])


def etl_forge_events_to_events_log(forge_dir: str):
    transformer = ZooEventsToEventsLogTransformer(forge_dir)
    transformer.transform()


class ZooEventsToEventsLogTransformer:
    def __init__(self, forge_dir: str):
        self.forge_dir = forge_dir

    def transform(self):
        sheet_name = "forge_events"
        for br_ref in get_existing_excel_brick_file_refs(self.forge_dir):
            forge_brick_path = create_path(self.forge_dir, br_ref.file_name)
            otx_events_df = pandas_read_excel(forge_brick_path, sheet_name)
            events_log_df = self.get_event_log_df(
                otx_events_df, self.forge_dir, br_ref.file_name
            )
            self._save_events_log_file(events_log_df)

    def get_event_log_df(
        self, otx_events_df: DataFrame, x_dir: str, x_file_name: str
    ) -> DataFrame:
        otx_events_df[["file_dir"]] = x_dir
        otx_events_df[["file_name"]] = x_file_name
        otx_events_df[["sheet_name"]] = "forge_events"
        cols = ["file_dir", "file_name", "sheet_name", "face_id", "event_id", "note"]
        otx_events_df = otx_events_df[cols]
        return otx_events_df

    def _save_events_log_file(self, events_df: DataFrame):
        events_file_path = create_path(self.forge_dir, "events.xlsx")
        events_log_str = "events_log"
        if os_path_exists(events_file_path):
            events_log_df = pandas_read_excel(events_file_path, events_log_str)
            events_df = pandas_concat([events_log_df, events_df])
        upsert_sheet(events_file_path, events_log_str, events_df)


def _create_events_agg_df(events_log_df: DataFrame) -> DataFrame:
    events_agg_df = events_log_df[["face_id", "event_id"]].drop_duplicates()
    events_agg_df["note"] = (
        events_agg_df["event_id"]
        .duplicated(keep=False)
        .apply(lambda x: "invalid because of conflicting event_id" if x else "")
    )
    return events_agg_df.sort_values(["event_id", "face_id"])


def etl_events_log_to_events_agg(forge_dir):
    transformer = EventsLogToEventsAggTransformer(forge_dir)
    transformer.transform()


class EventsLogToEventsAggTransformer:
    def __init__(self, forge_dir: str):
        self.forge_dir = forge_dir

    def transform(self):
        events_file_path = create_path(self.forge_dir, "events.xlsx")
        events_log_df = pandas_read_excel(events_file_path, "events_log")
        events_agg_df = _create_events_agg_df(events_log_df)
        upsert_sheet(events_file_path, "events_agg", events_agg_df)


def get_events_dict_from_events_agg_file(forge_dir) -> dict[int, str]:
    events_file_path = create_path(forge_dir, "events.xlsx")
    events_agg_df = pandas_read_excel(events_file_path, "events_agg")
    x_dict = {}
    for index, event_agg_row in events_agg_df.iterrows():
        x_note = event_agg_row["note"]
        if x_note != "invalid because of conflicting event_id":
            x_dict[event_agg_row["event_id"]] = event_agg_row["face_id"]
    return x_dict


def forge_agg_single_to_pidgin_staging(
    pidgin_category: str, legitimate_events: set[TimeLinePoint], forge_dir: str
):
    x_events = legitimate_events
    transformer = ZooAggToStagingTransformer(forge_dir, pidgin_category, x_events)
    transformer.transform()


def etl_forge_agg_to_pidgin_acct_staging(
    legitimate_events: set[TimeLinePoint], forge_dir: str
):
    forge_agg_single_to_pidgin_staging("bridge_acct_id", legitimate_events, forge_dir)


def etl_forge_agg_to_pidgin_group_staging(
    legitimate_events: set[TimeLinePoint], forge_dir: str
):
    forge_agg_single_to_pidgin_staging("bridge_group_id", legitimate_events, forge_dir)


def etl_forge_agg_to_pidgin_idea_staging(
    legitimate_events: set[TimeLinePoint], forge_dir: str
):
    forge_agg_single_to_pidgin_staging("bridge_idea", legitimate_events, forge_dir)


def etl_forge_agg_to_pidgin_road_staging(
    legitimate_events: set[TimeLinePoint], forge_dir: str
):
    forge_agg_single_to_pidgin_staging("bridge_road", legitimate_events, forge_dir)


def etl_forge_agg_to_pidgin_staging(
    legitimate_events: set[TimeLinePoint], forge_dir: str
):
    etl_forge_agg_to_pidgin_acct_staging(legitimate_events, forge_dir)
    etl_forge_agg_to_pidgin_group_staging(legitimate_events, forge_dir)
    etl_forge_agg_to_pidgin_idea_staging(legitimate_events, forge_dir)
    etl_forge_agg_to_pidgin_road_staging(legitimate_events, forge_dir)


class ZooAggToStagingTransformer:
    def __init__(
        self, forge_dir: str, pidgin_category: str, legitmate_events: set[TimeLinePoint]
    ):
        self.forge_dir = forge_dir
        self.legitmate_events = legitmate_events
        self.pidgin_category = pidgin_category
        self.jaar_type = get_jaar_type(pidgin_category)

    def transform(self):
        category_bricks = get_brick_category_ref().get(self.pidgin_category)
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_category)
        pidgin_columns.update({"face_id", "event_id"})
        pidgin_columns = get_sorting_columns(pidgin_columns)
        pidgin_columns.insert(0, "src_brick")
        pidgin_df = DataFrame(columns=pidgin_columns)
        for brick_number in sorted(category_bricks):
            brick_file_name = f"{brick_number}.xlsx"
            forge_brick_path = create_path(self.forge_dir, brick_file_name)
            if os_path_exists(forge_brick_path):
                self.insert_staging_rows(
                    pidgin_df, brick_number, forge_brick_path, pidgin_columns
                )

        pidgin_file_path = create_path(self.forge_dir, "pidgin.xlsx")
        upsert_sheet(pidgin_file_path, get_sheet_stage_name(self.jaar_type), pidgin_df)

    def insert_staging_rows(
        self,
        stage_df: DataFrame,
        brick_number: str,
        forge_brick_path: str,
        df_columns: list[str],
    ):
        forge_agg_df = pandas_read_excel(forge_brick_path, sheet_name="forge_agg")
        df_missing_cols = set(df_columns).difference(forge_agg_df.columns)

        for index, x_row in forge_agg_df.iterrows():
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
                    get_otx_obj(self.jaar_type, x_row),
                    self.get_inx_obj(x_row, df_missing_cols),
                    otx_wall,
                    inx_wall,
                    unknown_word,
                ]

    def get_inx_obj(self, x_row, missing_col: set[str]) -> str:
        if self.jaar_type == "AcctID" and "inx_acct_id" not in missing_col:
            return x_row["inx_acct_id"]
        elif self.jaar_type == "GroupID" and "inx_group_id" not in missing_col:
            return x_row["inx_group_id"]
        elif self.jaar_type == "IdeaUnit" and "inx_idea" not in missing_col:
            return x_row["inx_idea"]
        elif self.jaar_type == "RoadUnit" and "inx_road" not in missing_col:
            return x_row["inx_road"]
        return None


def etl_pidgin_acct_staging_to_acct_agg(forge_dir: str):
    etl_pidgin_single_staging_to_agg(forge_dir, "bridge_acct_id")


def etl_pidgin_group_staging_to_group_agg(forge_dir: str):
    etl_pidgin_single_staging_to_agg(forge_dir, "bridge_group_id")


def etl_pidgin_road_staging_to_road_agg(forge_dir: str):
    etl_pidgin_single_staging_to_agg(forge_dir, "bridge_road")


def etl_pidgin_idea_staging_to_idea_agg(forge_dir: str):
    etl_pidgin_single_staging_to_agg(forge_dir, "bridge_idea")


def etl_pidgin_single_staging_to_agg(forge_dir: str, bridge_category: str):
    transformer = PidginStagingToAggTransformer(forge_dir, bridge_category)
    transformer.transform()


def etl_pidgin_staging_to_agg(forge_dir):
    etl_pidgin_acct_staging_to_acct_agg(forge_dir)
    etl_pidgin_group_staging_to_group_agg(forge_dir)
    etl_pidgin_road_staging_to_road_agg(forge_dir)
    etl_pidgin_idea_staging_to_idea_agg(forge_dir)


class PidginStagingToAggTransformer:
    def __init__(self, forge_dir: str, pidgin_category: str):
        self.forge_dir = forge_dir
        self.pidgin_category = pidgin_category
        self.file_path = create_path(self.forge_dir, "pidgin.xlsx")
        self.jaar_type = get_jaar_type(self.pidgin_category)

    def transform(self):
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_category)
        pidgin_columns.update({"face_id", "event_id"})
        pidgin_columns = get_sorting_columns(pidgin_columns)
        pidgin_agg_df = DataFrame(columns=pidgin_columns)
        self.insert_agg_rows(pidgin_agg_df)
        upsert_sheet(self.file_path, get_sheet_agg_name(self.jaar_type), pidgin_agg_df)

    def insert_agg_rows(self, pidgin_agg_df: DataFrame):
        pidgin_file_path = create_path(self.forge_dir, "pidgin.xlsx")
        stage_sheet_name = get_sheet_stage_name(self.jaar_type)
        staging_df = pandas_read_excel(pidgin_file_path, sheet_name=stage_sheet_name)
        x_pidginbodybook = self.get_validated_pidginbodybook(staging_df)
        for pidginbodylist in x_pidginbodybook.get_valid_pidginbodylists():
            pidgin_agg_df.loc[len(pidgin_agg_df)] = pidginbodylist

    def get_validated_pidginbodybook(self, staging_df: DataFrame) -> PidginBodyBook:
        x_pidginheartbook = self.get_validated_pidginheart(staging_df)
        x_pidginbodybook = pidginbodybook_shop(x_pidginheartbook)
        for index, x_row in staging_df.iterrows():
            x_pidginbodyrow = PidginBodyRow(
                event_id=x_row["event_id"],
                face_id=x_row["face_id"],
                otx_str=get_otx_obj(self.jaar_type, x_row),
                inx_str=get_inx_obj(self.jaar_type, x_row),
            )
            x_pidginbodybook.eval_pidginbodyrow(x_pidginbodyrow)
        return x_pidginbodybook

    def get_validated_pidginheart(self, staging_df: DataFrame) -> PidginHeartBook:
        x_pidginheartbook = pidginheartbook_shop()
        for index, x_row in staging_df.iterrows():
            x_pidginheartrow = PidginHeartRow(
                event_id=x_row["event_id"],
                face_id=x_row["face_id"],
                otx_wall=x_row["otx_wall"],
                inx_wall=x_row["inx_wall"],
                unknown_word=x_row["unknown_word"],
            )
            x_pidginheartbook.eval_pidginheartrow(x_pidginheartrow)
        return x_pidginheartbook


def etl_pidgin_agg_to_face_dirs(forge_dir: str, faces_dir: str):
    agg_pidgin = create_path(forge_dir, "pidgin.xlsx")
    for jaar_type in JAAR_TYPES.keys():
        agg_sheet_name = JAAR_TYPES[jaar_type]["agg"]
        if sheet_exists(agg_pidgin, agg_sheet_name):
            split_excel_into_dirs(
                input_file=agg_pidgin,
                output_dir=faces_dir,
                column_name="face_id",
                file_name="pidgin",
                sheet_name=agg_sheet_name,
            )


def etl_face_pidgin_to_event_pidgins(face_dir: str):
    face_pidgin_path = create_path(face_dir, "pidgin.xlsx")
    for jaar_type in JAAR_TYPES.keys():
        agg_sheet_name = JAAR_TYPES[jaar_type]["agg"]
        if sheet_exists(face_pidgin_path, agg_sheet_name):
            split_excel_into_events_dirs(face_pidgin_path, face_dir, agg_sheet_name)


def get_level1_dirs(x_dir: str) -> list[str]:
    level1_dirs = get_dir_file_strs(x_dir, include_dirs=True, include_files=False)
    return list(level1_dirs.keys())


def etl_face_pidgins_to_event_pidgins(faces_dir: str):
    for face_id_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_id_dir)
        etl_face_pidgin_to_event_pidgins(face_dir)


def split_excel_into_events_dirs(pidgin_file: str, face_dir: str, sheet_name: str):
    split_excel_into_dirs(pidgin_file, face_dir, "event_id", "pidgin", sheet_name)


def event_pidgin_to_pidgin_csv_files(event_pidgin_dir: str):
    event_pidgin_path = create_path(event_pidgin_dir, "pidgin.xlsx")
    for jaar_type in JAAR_TYPES.keys():
        agg_sheet_name = JAAR_TYPES[jaar_type]["agg"]
        csv_filename = JAAR_TYPES[jaar_type]["csv_filename"]
        if sheet_exists(event_pidgin_path, agg_sheet_name):
            acct_csv_path = create_path(event_pidgin_dir, csv_filename)
            acct_df = pandas_read_excel(event_pidgin_path, agg_sheet_name)
            acct_df.to_csv(acct_csv_path, index=False)


def _get_all_faces_dir_event_dirs(faces_dir) -> list[str]:
    full_event_dirs = []
    for face_id_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_id_dir)
        event_dirs = get_dir_file_strs(face_dir, include_dirs=True, include_files=False)
        full_event_dirs.extend(
            create_path(face_dir, event_dir) for event_dir in event_dirs.keys()
        )
    return full_event_dirs


def etl_event_pidgins_to_pidgin_csv_files(faces_dir: str):
    for event_pidgin_dir in _get_all_faces_dir_event_dirs(faces_dir):
        event_pidgin_to_pidgin_csv_files(event_pidgin_dir)


def etl_event_pidgin_csvs_to_pidgin_json(event_dir: str):
    pidginunit = init_pidginunit_from_dir(event_dir)
    save_file(event_dir, "pidgin.json", pidginunit.get_json(), replace=True)


def etl_event_pidgins_csvs_to_pidgin_jsons(faces_dir: str):
    for event_pidgin_dir in _get_all_faces_dir_event_dirs(faces_dir):
        etl_event_pidgin_csvs_to_pidgin_json(event_pidgin_dir)


def etl_pidgin_jsons_inherit_younger_pidgins(
    faces_dir: str, pidgin_events: dict[FaceID, set[TimeLinePoint]]
):
    old_pidginunit = None
    for face_id, pidgin_event_ids in pidgin_events.items():
        for pidgin_event_id in pidgin_event_ids:
            new_pidgin_path = get_event_pidgin_path(faces_dir, face_id, pidgin_event_id)
            new_pidginunit = get_pidginunit_from_json(open_file(new_pidgin_path))
            if old_pidginunit != None:
                new_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)
                save_file(new_pidgin_path, None, new_pidginunit.get_json())
            old_pidginunit = new_pidginunit


def get_event_pidgin_path(
    faces_dir: str, face_id: FaceID, pidgin_event_id: TimeLinePoint
):
    face_dir = create_path(faces_dir, face_id)
    event_dir = create_path(face_dir, pidgin_event_id)
    return create_path(event_dir, "pidgin.json")


def etl_forge_bricks_to_face_bricks(forge_dir: str, faces_dir: str):
    for forge_br_ref in get_existing_excel_brick_file_refs(forge_dir):
        forge_brick_path = create_path(forge_dir, forge_br_ref.file_name)
        if forge_br_ref.file_name not in _get_pidgen_brick_format_filenames():
            split_excel_into_dirs(
                input_file=forge_brick_path,
                output_dir=faces_dir,
                column_name="face_id",
                file_name=forge_br_ref.brick_number,
                sheet_name="forge_valid",
            )


def etl_face_bricks_to_event_bricks(faces_dir: str):
    for face_id_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_id_dir)
        for face_br_ref in get_existing_excel_brick_file_refs(face_dir):
            face_brick_path = create_path(face_dir, face_br_ref.file_name)
            split_excel_into_dirs(
                input_file=face_brick_path,
                output_dir=face_dir,
                column_name="event_id",
                file_name=face_br_ref.brick_number,
                sheet_name="forge_valid",
            )


def etl_event_bricks_to_fiscal_bricks(faces_dir: str):
    for event_brick_dir in _get_all_faces_dir_event_dirs(faces_dir):
        for event_br_ref in get_existing_excel_brick_file_refs(event_brick_dir):
            event_brick_path = create_path(event_brick_dir, event_br_ref.file_name)
            split_excel_into_dirs(
                input_file=event_brick_path,
                output_dir=event_brick_dir,
                column_name="fiscal_id",
                file_name=event_br_ref.brick_number,
                sheet_name="forge_valid",
            )


def get_fiscal_events_by_dirs(faces_dir: str) -> dict[FiscalID, set[TimeLinePoint]]:
    fiscal_events = {}
    for face_id in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_id)
        for event_id in get_level1_dirs(face_dir):
            event_dir = create_path(face_dir, event_id)
            for fiscal_id in get_level1_dirs(event_dir):
                if fiscal_events.get(fiscal_id) is None:
                    fiscal_events[fiscal_id] = {int(event_id)}
                else:
                    events_list = fiscal_events.get(fiscal_id)
                    events_list.add(int(event_id))
    return fiscal_events


def get_pidgin_events_by_dirs(faces_dir: str) -> dict[FaceID, set[TimeLinePoint]]:
    pidgin_events = {}
    for face_id in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_id)
        for event_id in get_level1_dirs(face_dir):
            event_dir = create_path(face_dir, event_id)
            pidgin_path = create_path(event_dir, "pidgin.json")
            if os_path_exists(pidgin_path):
                if pidgin_events.get(face_id) is None:
                    pidgin_events[face_id] = {int(event_id)}
                else:
                    events_list = pidgin_events.get(face_id)
                    events_list.add(int(event_id))
    return pidgin_events


def etl_fiscal_bricks_to_fiscal_inx(
    faces_dir: str,
    events: dict[TimeLinePoint, FaceID],
    fiscal_pidgins: dict[FiscalID, dict[TimeLinePoint, TimeLinePoint]],
):
    for fiscal_id, events_pidgins in fiscal_pidgins.items():
        for fiscal_event_id, pidgin_event_id in events_pidgins.items():
            fiscal_face_id = events.get(fiscal_event_id)
            pidgin_face_id = events.get(pidgin_event_id)
            if fiscal_face_id != pidgin_face_id:
                raise Exception("etl_fiscal_bricks_to_fiscal_inx error")
            face_dir = create_path(faces_dir, pidgin_face_id)
            pidgin_event_dir = create_path(face_dir, pidgin_event_id)
            fiscal_event_dir = create_path(face_dir, fiscal_event_id)
            fiscal_dir = create_path(fiscal_event_dir, fiscal_id)
            pidgin_path = create_path(pidgin_event_dir, "pidgin.json")
            x_pidginunit = get_pidginunit_from_json(open_file(pidgin_path))
            for fiscal_br_ref in get_existing_excel_brick_file_refs(fiscal_dir):
                br_path = create_path(fiscal_br_ref.file_dir, fiscal_br_ref.file_name)
                br_df = pandas_read_excel(br_path, "forge_valid")
                print(f"{br_path=}")
                print(f"before {br_df=}")
                translate_all_columns_dataframe(br_df, x_pidginunit)
                print(f"After  {br_df=}")
                upsert_sheet(br_path, "forge_inx", br_df)

    # for face_id in get_level1_dirs(faces_dir):
    #     face_dir = create_path(faces_dir, face_id)
    #     for event_id in get_level1_dirs(face_dir):
    #         event_dir = create_path(face_dir, event_id)
    #         for fiscal_id in get_level1_dirs(event_dir):
    #             fiscal_dir = create_path(event_dir, fiscal_id)
    #             for fiscal_br_ref in get_existing_excel_brick_file_refs(fiscal_dir):
    #                 print(f"{fiscal_br_ref=}")

    #             print(f"{fiscal_dir=}")

    # for event_brick_dir in _get_all_faces_dir_event_dirs(faces_dir):
    #     for event_br_ref in get_existing_excel_brick_file_refs(event_brick_dir):
    #         event_brick_path = create_path(event_brick_dir, event_br_ref.file_name)
    # split_excel_into_dirs(
    #     input_file=event_brick_path,
    #     output_dir=event_brick_dir,
    #     column_name="fiscal_id",
    #     file_name=event_br_ref.brick_number,
    #     sheet_name="forge_valid",
    # )

    # for face_id, pidgin_event_ids in pidgin_events.items():
    #     for pidgin_event_id in pidgin_event_ids:
    #         new_pidgin_path = get_event_pidgin_path(faces_dir, face_id, pidgin_event_id)
    #         new_pidginunit = get_pidginunit_from_json(open_file(new_pidgin_path))
    #         if old_pidginunit != None:
    #             new_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)
    #             save_file(new_pidgin_path, None, new_pidginunit.get_json())
    #             print(f"{face_id=} {new_pidgin_path=}")
    #             print(f"{new_pidginunit.acctbridge=}")
    #             print(f"{new_pidginunit.get_json()=}")
    #         old_pidginunit = new_pidginunit
