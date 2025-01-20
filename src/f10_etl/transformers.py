from src.f00_instrument.file import create_path, get_dir_file_strs, save_file, open_file
from src.f00_instrument.db_toolbox import (
    create_table_from_columns,
    db_table_exists,
    get_table_columns,
)
from src.f01_road.road import FaceName, EventInt
from src.f08_pidgin.pidgin import get_pidginunit_from_json, inherit_pidginunit
from src.f08_pidgin.pidgin_config import get_quick_pidgens_column_ref
from src.f09_idea.idea_config import (
    get_idea_numbers,
    get_idea_format_filename,
    get_idea_category_ref,
    get_idea_sqlite_types,
)
from src.f09_idea.idea import get_idearef_obj
from src.f09_idea.pandas_tool import (
    get_custom_sorted_list,
    upsert_sheet,
    split_excel_into_dirs,
    sheet_exists,
    _get_pidgen_idea_format_filenames,
    get_boat_staging_grouping_with_all_values_equal_df,
    translate_all_columns_dataframe,
    insert_idea_csv,
    save_table_to_csv,
    open_csv,
    get_ordered_csv,
)
from src.f09_idea.pidgin_toolbox import init_pidginunit_from_dir
from src.f10_etl.idea_collector import get_all_idea_dataframes, IdeaFileRef
from src.f10_etl.fiscal_etl_tool import (
    create_fiscalunit_jsons_from_prime_files,
    get_fiscalunit_sorted_args,
    get_fiscaldeal_sorted_args,
    get_fiscalcash_sorted_args,
    get_fiscalhour_sorted_args,
    get_fiscalmont_sorted_args,
    get_fiscalweek_sorted_args,
)
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
from sqlite3 import Connection as sqlite3_Connection
from copy import copy as copy_copy
import os


class not_given_pidgin_category_Exception(Exception):
    pass


MAPS_CATEGORYS = {
    "map_name": "AcctName",
    "map_label": "GroupLabel",
    "map_title": "TitleUnit",
    "map_road": "RoadUnit",
}

class_typeS = {
    "AcctName": {
        "stage": "name_staging",
        "agg": "name_agg",
        "csv_filename": "name.csv",
        "otx_obj": "otx_name",
        "inx_obj": "inx_name",
    },
    "GroupLabel": {
        "stage": "label_staging",
        "agg": "label_agg",
        "csv_filename": "label.csv",
        "otx_obj": "otx_label",
        "inx_obj": "inx_label",
    },
    "TitleUnit": {
        "stage": "title_staging",
        "agg": "title_agg",
        "csv_filename": "title.csv",
        "otx_obj": "otx_title",
        "inx_obj": "inx_title",
    },
    "RoadUnit": {
        "stage": "road_staging",
        "agg": "road_agg",
        "csv_filename": "road.csv",
        "otx_obj": "otx_road",
        "inx_obj": "inx_road",
    },
}


def get_class_type(pidgin_category: str) -> str:
    if pidgin_category not in MAPS_CATEGORYS:
        raise not_given_pidgin_category_Exception("not given pidgin_category")
    return MAPS_CATEGORYS[pidgin_category]


def get_sheet_stage_name(class_type: str) -> str:
    return class_typeS[class_type]["stage"]


def get_sheet_agg_name(class_type: str) -> str:
    return class_typeS[class_type]["agg"]


def get_otx_obj(class_type, x_row) -> str:
    return x_row[class_typeS[class_type]["otx_obj"]]


def get_inx_obj(class_type, x_row) -> str:
    return x_row[class_typeS[class_type]["inx_obj"]]


def etl_ocean_to_boat_staging(ocean_dir: str, boat_dir: str):
    transformer = OceanToboatTransformer(ocean_dir, boat_dir)
    transformer.transform()


class OceanToboatTransformer:
    def __init__(self, ocean_dir: str, boat_dir: str):
        self.ocean_dir = ocean_dir
        self.boat_dir = boat_dir

    def transform(self):
        for idea_number, dfs in self._group_ocean_data().items():
            self._save_to_boat_staging(idea_number, dfs)

    def _group_ocean_data(self):
        grouped_data = {}
        for ref in get_all_idea_dataframes(self.ocean_dir):
            df = self._read_and_tag_dataframe(ref)
            grouped_data.setdefault(ref.idea_number, []).append(df)
        return grouped_data

    def _read_and_tag_dataframe(self, ref):
        x_file_path = create_path(ref.file_dir, ref.file_name)
        df = pandas_read_excel(x_file_path, ref.sheet_name)
        df["file_dir"] = ref.file_dir
        df["file_name"] = ref.file_name
        df["sheet_name"] = ref.sheet_name
        return df

    def _save_to_boat_staging(self, idea_number: str, dfs: list):
        final_df = pandas_concat(dfs)
        boat_path = create_path(self.boat_dir, f"{idea_number}.xlsx")
        upsert_sheet(boat_path, "boat_staging", final_df)


def get_existing_excel_idea_file_refs(x_dir: str) -> list[IdeaFileRef]:
    existing_excel_idea_filepaths = []
    for idea_number in sorted(get_idea_numbers()):
        idea_filename = f"{idea_number}.xlsx"
        x_idea_path = create_path(x_dir, idea_filename)
        if os_path_exists(x_idea_path):
            x_fileref = IdeaFileRef(
                file_dir=x_dir, file_name=idea_filename, idea_number=idea_number
            )
            existing_excel_idea_filepaths.append(x_fileref)
    return existing_excel_idea_filepaths


def etl_boat_staging_to_boat_agg(boat_dir):
    transformer = boatStagingToboatAggTransformer(boat_dir)
    transformer.transform()


class boatStagingToboatAggTransformer:
    def __init__(self, boat_dir: str):
        self.boat_dir = boat_dir

    def transform(self):
        for br_ref in get_existing_excel_idea_file_refs(self.boat_dir):
            boat_idea_path = create_path(br_ref.file_dir, br_ref.file_name)
            boat_staging_df = pandas_read_excel(boat_idea_path, "boat_staging")
            otx_df = self._group_by_idea_columns(boat_staging_df, br_ref.idea_number)
            upsert_sheet(boat_idea_path, "boat_agg", otx_df)

    def _group_by_idea_columns(
        self, boat_staging_df: DataFrame, idea_number: str
    ) -> DataFrame:
        idea_filename = get_idea_format_filename(idea_number)
        idearef = get_idearef_obj(idea_filename)
        required_columns = idearef.get_otx_keys_list()
        idea_columns_set = set(idearef._attributes.keys())
        idea_columns_list = get_custom_sorted_list(idea_columns_set)
        boat_staging_df = boat_staging_df[idea_columns_list]
        return get_boat_staging_grouping_with_all_values_equal_df(
            boat_staging_df, required_columns
        )


def etl_boat_agg_to_boat_valid(boat_dir: str, legitimate_events: set[EventInt]):
    transformer = boatAggToboatValidTransformer(boat_dir, legitimate_events)
    transformer.transform()


class boatAggToboatValidTransformer:
    def __init__(self, boat_dir: str, legitimate_events: set[EventInt]):
        self.boat_dir = boat_dir
        self.legitimate_events = legitimate_events

    def transform(self):
        for br_ref in get_existing_excel_idea_file_refs(self.boat_dir):
            boat_idea_path = create_path(br_ref.file_dir, br_ref.file_name)
            boat_agg = pandas_read_excel(boat_idea_path, "boat_agg")
            boat_valid_df = boat_agg[boat_agg["event_int"].isin(self.legitimate_events)]
            upsert_sheet(boat_idea_path, "boat_valid", boat_valid_df)

    # def _group_by_idea_columns(
    #     self, boat_staging_df: DataFrame, idea_number: str
    # ) -> DataFrame:
    #     idea_filename = get_idea_format_filename(idea_number)
    #     idearef = get_idearef_obj(idea_filename)
    #     required_columns = idearef.get_otx_keys_list()
    #     idea_columns_set = set(idearef._attributes.keys())
    #     idea_columns_list = get_custom_sorted_list(idea_columns_set)
    #     boat_staging_df = boat_staging_df[idea_columns_list]
    #     return get_boat_staging_grouping_with_all_values_equal_df(
    #         boat_staging_df, required_columns
    #     )


def etl_boat_agg_to_boat_events(boat_dir):
    transformer = boatAggToboatEventsTransformer(boat_dir)
    transformer.transform()


class boatAggToboatEventsTransformer:
    def __init__(self, boat_dir: str):
        self.boat_dir = boat_dir

    def transform(self):
        for file_ref in get_existing_excel_idea_file_refs(self.boat_dir):
            boat_idea_path = create_path(self.boat_dir, file_ref.file_name)
            boat_agg_df = pandas_read_excel(boat_idea_path, "boat_agg")
            events_df = self.get_unique_events(boat_agg_df)
            upsert_sheet(boat_idea_path, "boat_events", events_df)

    def get_unique_events(self, boat_agg_df: DataFrame) -> DataFrame:
        events_df = boat_agg_df[["face_name", "event_int"]].drop_duplicates()
        events_df["error_message"] = (
            events_df["event_int"]
            .duplicated(keep=False)
            .apply(lambda x: "invalid because of conflicting event_int" if x else "")
        )
        return events_df.sort_values(["face_name", "event_int"])


def etl_boat_events_to_events_log(boat_dir: str):
    transformer = boatEventsToEventsLogTransformer(boat_dir)
    transformer.transform()


class boatEventsToEventsLogTransformer:
    def __init__(self, boat_dir: str):
        self.boat_dir = boat_dir

    def transform(self):
        sheet_name = "boat_events"
        for br_ref in get_existing_excel_idea_file_refs(self.boat_dir):
            boat_idea_path = create_path(self.boat_dir, br_ref.file_name)
            otx_events_df = pandas_read_excel(boat_idea_path, sheet_name)
            events_log_df = self.get_event_log_df(
                otx_events_df, self.boat_dir, br_ref.file_name
            )
            self._save_events_log_file(events_log_df)

    def get_event_log_df(
        self, otx_events_df: DataFrame, x_dir: str, x_file_name: str
    ) -> DataFrame:
        otx_events_df[["file_dir"]] = x_dir
        otx_events_df[["file_name"]] = x_file_name
        otx_events_df[["sheet_name"]] = "boat_events"
        cols = [
            "file_dir",
            "file_name",
            "sheet_name",
            "face_name",
            "event_int",
            "error_message",
        ]
        otx_events_df = otx_events_df[cols]
        return otx_events_df

    def _save_events_log_file(self, events_df: DataFrame):
        events_file_path = create_path(self.boat_dir, "events.xlsx")
        events_log_str = "events_log"
        if os_path_exists(events_file_path):
            events_log_df = pandas_read_excel(events_file_path, events_log_str)
            events_df = pandas_concat([events_log_df, events_df])
        upsert_sheet(events_file_path, events_log_str, events_df, replace=True)


def _create_events_agg_df(events_log_df: DataFrame) -> DataFrame:
    events_agg_df = events_log_df[["face_name", "event_int"]].drop_duplicates()
    events_agg_df["error_message"] = (
        events_agg_df["event_int"]
        .duplicated(keep=False)
        .apply(lambda x: "invalid because of conflicting event_int" if x else "")
    )
    return events_agg_df.sort_values(["event_int", "face_name"])


def etl_boat_events_log_to_events_agg(boat_dir):
    transformer = EventsLogToEventsAggTransformer(boat_dir)
    transformer.transform()


class EventsLogToEventsAggTransformer:
    def __init__(self, boat_dir: str):
        self.boat_dir = boat_dir

    def transform(self):
        events_file_path = create_path(self.boat_dir, "events.xlsx")
        events_log_df = pandas_read_excel(events_file_path, "events_log")
        events_agg_df = _create_events_agg_df(events_log_df)
        upsert_sheet(events_file_path, "events_agg", events_agg_df)


def get_events_dict_from_events_agg_file(boat_dir) -> dict[int, str]:
    events_file_path = create_path(boat_dir, "events.xlsx")
    events_agg_df = pandas_read_excel(events_file_path, "events_agg")
    x_dict = {}
    for index, event_agg_row in events_agg_df.iterrows():
        x_note = event_agg_row["error_message"]
        if x_note != "invalid because of conflicting event_int":
            x_dict[event_agg_row["event_int"]] = event_agg_row["face_name"]
    return x_dict


def boat_agg_single_to_pidgin_staging(
    pidgin_category: str, legitimate_events: set[EventInt], boat_dir: str
):
    x_events = legitimate_events
    transformer = boatAggToStagingTransformer(boat_dir, pidgin_category, x_events)
    transformer.transform()


def etl_boat_agg_to_pidgin_name_staging(
    legitimate_events: set[EventInt], boat_dir: str
):
    boat_agg_single_to_pidgin_staging("map_name", legitimate_events, boat_dir)


def etl_boat_agg_to_pidgin_label_staging(
    legitimate_events: set[EventInt], boat_dir: str
):
    boat_agg_single_to_pidgin_staging("map_label", legitimate_events, boat_dir)


def etl_boat_agg_to_pidgin_title_staging(
    legitimate_events: set[EventInt], boat_dir: str
):
    boat_agg_single_to_pidgin_staging("map_title", legitimate_events, boat_dir)


def etl_boat_agg_to_pidgin_road_staging(
    legitimate_events: set[EventInt], boat_dir: str
):
    boat_agg_single_to_pidgin_staging("map_road", legitimate_events, boat_dir)


def etl_boat_agg_to_pidgin_staging(legitimate_events: set[EventInt], boat_dir: str):
    etl_boat_agg_to_pidgin_name_staging(legitimate_events, boat_dir)
    etl_boat_agg_to_pidgin_label_staging(legitimate_events, boat_dir)
    etl_boat_agg_to_pidgin_title_staging(legitimate_events, boat_dir)
    etl_boat_agg_to_pidgin_road_staging(legitimate_events, boat_dir)


class boatAggToStagingTransformer:
    def __init__(
        self, boat_dir: str, pidgin_category: str, legitmate_events: set[EventInt]
    ):
        self.boat_dir = boat_dir
        self.legitmate_events = legitmate_events
        self.pidgin_category = pidgin_category
        self.class_type = get_class_type(pidgin_category)

    def transform(self):
        category_ideas = get_idea_category_ref().get(self.pidgin_category)
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_category)
        pidgin_columns.update({"face_name", "event_int"})
        pidgin_columns = get_custom_sorted_list(pidgin_columns)
        pidgin_columns.insert(0, "src_idea")
        pidgin_df = DataFrame(columns=pidgin_columns)
        for idea_number in sorted(category_ideas):
            idea_file_name = f"{idea_number}.xlsx"
            boat_idea_path = create_path(self.boat_dir, idea_file_name)
            if os_path_exists(boat_idea_path):
                self.insert_staging_rows(
                    pidgin_df, idea_number, boat_idea_path, pidgin_columns
                )

        pidgin_file_path = create_path(self.boat_dir, "pidgin.xlsx")
        upsert_sheet(pidgin_file_path, get_sheet_stage_name(self.class_type), pidgin_df)

    def insert_staging_rows(
        self,
        stage_df: DataFrame,
        idea_number: str,
        boat_idea_path: str,
        df_columns: list[str],
    ):
        boat_agg_df = pandas_read_excel(boat_idea_path, sheet_name="boat_agg")
        df_missing_cols = set(df_columns).difference(boat_agg_df.columns)

        for index, x_row in boat_agg_df.iterrows():
            event_int = x_row["event_int"]
            if event_int in self.legitmate_events:
                face_name = x_row["face_name"]
                otx_bridge = None
                if "otx_bridge" not in df_missing_cols:
                    otx_bridge = x_row["otx_bridge"]
                inx_bridge = None
                if "inx_bridge" not in df_missing_cols:
                    inx_bridge = x_row["inx_bridge"]
                unknown_word = None
                if "unknown_word" not in df_missing_cols:
                    unknown_word = x_row["unknown_word"]
                df_len = len(stage_df.index)
                stage_df.loc[df_len] = [
                    idea_number,
                    face_name,
                    event_int,
                    get_otx_obj(self.class_type, x_row),
                    self.get_inx_obj(x_row, df_missing_cols),
                    otx_bridge,
                    inx_bridge,
                    unknown_word,
                ]

    def get_inx_obj(self, x_row, missing_col: set[str]) -> str:
        if self.class_type == "AcctName" and "inx_name" not in missing_col:
            return x_row["inx_name"]
        elif self.class_type == "GroupLabel" and "inx_label" not in missing_col:
            return x_row["inx_label"]
        elif self.class_type == "TitleUnit" and "inx_title" not in missing_col:
            return x_row["inx_title"]
        elif self.class_type == "RoadUnit" and "inx_road" not in missing_col:
            return x_row["inx_road"]
        return None


def etl_pidgin_name_staging_to_name_agg(boat_dir: str):
    etl_pidgin_single_staging_to_agg(boat_dir, "map_name")


def etl_pidgin_label_staging_to_label_agg(boat_dir: str):
    etl_pidgin_single_staging_to_agg(boat_dir, "map_label")


def etl_pidgin_road_staging_to_road_agg(boat_dir: str):
    etl_pidgin_single_staging_to_agg(boat_dir, "map_road")


def etl_pidgin_title_staging_to_title_agg(boat_dir: str):
    etl_pidgin_single_staging_to_agg(boat_dir, "map_title")


def etl_pidgin_single_staging_to_agg(boat_dir: str, map_category: str):
    transformer = PidginStagingToAggTransformer(boat_dir, map_category)
    transformer.transform()


def etl_boat_pidgin_staging_to_agg(boat_dir):
    etl_pidgin_name_staging_to_name_agg(boat_dir)
    etl_pidgin_label_staging_to_label_agg(boat_dir)
    etl_pidgin_road_staging_to_road_agg(boat_dir)
    etl_pidgin_title_staging_to_title_agg(boat_dir)


class PidginStagingToAggTransformer:
    def __init__(self, boat_dir: str, pidgin_category: str):
        self.boat_dir = boat_dir
        self.pidgin_category = pidgin_category
        self.file_path = create_path(self.boat_dir, "pidgin.xlsx")
        self.class_type = get_class_type(self.pidgin_category)

    def transform(self):
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_category)
        pidgin_columns.update({"face_name", "event_int"})
        pidgin_columns = get_custom_sorted_list(pidgin_columns)
        pidgin_agg_df = DataFrame(columns=pidgin_columns)
        self.insert_agg_rows(pidgin_agg_df)
        upsert_sheet(self.file_path, get_sheet_agg_name(self.class_type), pidgin_agg_df)

    def insert_agg_rows(self, pidgin_agg_df: DataFrame):
        pidgin_file_path = create_path(self.boat_dir, "pidgin.xlsx")
        stage_sheet_name = get_sheet_stage_name(self.class_type)
        staging_df = pandas_read_excel(pidgin_file_path, sheet_name=stage_sheet_name)
        x_pidginbodybook = self.get_validated_pidginbodybook(staging_df)
        for pidginbodylist in x_pidginbodybook.get_valid_pidginbodylists():
            pidgin_agg_df.loc[len(pidgin_agg_df)] = pidginbodylist

    def get_validated_pidginbodybook(self, staging_df: DataFrame) -> PidginBodyBook:
        x_pidginheartbook = self.get_validated_pidginheart(staging_df)
        x_pidginbodybook = pidginbodybook_shop(x_pidginheartbook)
        for index, x_row in staging_df.iterrows():
            x_pidginbodyrow = PidginBodyRow(
                event_int=x_row["event_int"],
                face_name=x_row["face_name"],
                otx_str=get_otx_obj(self.class_type, x_row),
                inx_str=get_inx_obj(self.class_type, x_row),
            )
            x_pidginbodybook.eval_pidginbodyrow(x_pidginbodyrow)
        return x_pidginbodybook

    def get_validated_pidginheart(self, staging_df: DataFrame) -> PidginHeartBook:
        x_pidginheartbook = pidginheartbook_shop()
        for index, x_row in staging_df.iterrows():
            x_pidginheartrow = PidginHeartRow(
                event_int=x_row["event_int"],
                face_name=x_row["face_name"],
                otx_bridge=x_row["otx_bridge"],
                inx_bridge=x_row["inx_bridge"],
                unknown_word=x_row["unknown_word"],
            )
            x_pidginheartbook.eval_pidginheartrow(x_pidginheartrow)
        return x_pidginheartbook


def etl_boat_pidgin_agg_to_bow_face_dirs(boat_dir: str, faces_dir: str):
    agg_pidgin = create_path(boat_dir, "pidgin.xlsx")
    for class_type in class_typeS.keys():
        agg_sheet_name = class_typeS[class_type]["agg"]
        if sheet_exists(agg_pidgin, agg_sheet_name):
            split_excel_into_dirs(
                input_file=agg_pidgin,
                output_dir=faces_dir,
                column_name="face_name",
                file_name="pidgin",
                sheet_name=agg_sheet_name,
            )


def etl_face_pidgin_to_event_pidgins(face_dir: str):
    face_pidgin_path = create_path(face_dir, "pidgin.xlsx")
    for class_type in class_typeS.keys():
        agg_sheet_name = class_typeS[class_type]["agg"]
        if sheet_exists(face_pidgin_path, agg_sheet_name):
            split_excel_into_events_dirs(face_pidgin_path, face_dir, agg_sheet_name)


def get_level1_dirs(x_dir: str) -> list[str]:
    try:
        level1_dirs = get_dir_file_strs(x_dir, include_dirs=True, include_files=False)
        return sorted(list(level1_dirs.keys()))
    except OSError as e:
        return []


def etl_bow_face_pidgins_to_bow_event_pidgins(faces_dir: str):
    for face_name_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name_dir)
        etl_face_pidgin_to_event_pidgins(face_dir)


def split_excel_into_events_dirs(pidgin_file: str, face_dir: str, sheet_name: str):
    split_excel_into_dirs(pidgin_file, face_dir, "event_int", "pidgin", sheet_name)


def event_pidgin_to_pidgin_csv_files(event_pidgin_dir: str):
    event_pidgin_path = create_path(event_pidgin_dir, "pidgin.xlsx")
    for class_type in class_typeS.keys():
        agg_sheet_name = class_typeS[class_type]["agg"]
        csv_filename = class_typeS[class_type]["csv_filename"]
        if sheet_exists(event_pidgin_path, agg_sheet_name):
            acct_csv_path = create_path(event_pidgin_dir, csv_filename)
            acct_df = pandas_read_excel(event_pidgin_path, agg_sheet_name)
            acct_df.to_csv(acct_csv_path, index=False)


def _get_all_faces_bow_dir_event_dirs(faces_dir) -> list[str]:
    full_event_dirs = []
    for face_name_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name_dir)
        event_dirs = get_dir_file_strs(face_dir, include_dirs=True, include_files=False)
        full_event_dirs.extend(
            create_path(face_dir, event_dir) for event_dir in event_dirs.keys()
        )
    return full_event_dirs


def etl_bow_event_pidgins_to_bow_pidgin_csv_files(faces_dir: str):
    for event_pidgin_dir in _get_all_faces_bow_dir_event_dirs(faces_dir):
        event_pidgin_to_pidgin_csv_files(event_pidgin_dir)


def etl_event_pidgin_csvs_to_pidgin_json(event_dir: str):
    pidginunit = init_pidginunit_from_dir(event_dir)
    save_file(event_dir, "pidgin.json", pidginunit.get_json(), replace=True)


def etl_bow_event_pidgins_csvs_to_bow_pidgin_jsons(faces_dir: str):
    for event_pidgin_dir in _get_all_faces_bow_dir_event_dirs(faces_dir):
        etl_event_pidgin_csvs_to_pidgin_json(event_pidgin_dir)


def etl_pidgin_jsons_inherit_younger_pidgins(
    faces_dir: str, pidgin_events: dict[FaceName, set[EventInt]]
):
    old_pidginunit = None
    for face_name, pidgin_event_ints in pidgin_events.items():
        for pidgin_event_int in pidgin_event_ints:
            new_pidgin_path = get_event_pidgin_path(
                faces_dir, face_name, pidgin_event_int
            )
            new_pidginunit = get_pidginunit_from_json(open_file(new_pidgin_path))
            if old_pidginunit != None:
                new_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)
                save_file(new_pidgin_path, None, new_pidginunit.get_json())
            old_pidginunit = new_pidginunit


def get_event_pidgin_path(
    faces_dir: str, face_name: FaceName, pidgin_event_int: EventInt
):
    face_dir = create_path(faces_dir, face_name)
    event_dir = create_path(face_dir, pidgin_event_int)
    return create_path(event_dir, "pidgin.json")


def etl_boat_ideas_to_bow_face_ideas(boat_dir: str, faces_dir: str):
    for boat_br_ref in get_existing_excel_idea_file_refs(boat_dir):
        boat_idea_path = create_path(boat_dir, boat_br_ref.file_name)
        if boat_br_ref.file_name not in _get_pidgen_idea_format_filenames():
            split_excel_into_dirs(
                input_file=boat_idea_path,
                output_dir=faces_dir,
                column_name="face_name",
                file_name=boat_br_ref.idea_number,
                sheet_name="boat_valid",
            )


def etl_bow_face_ideas_to_bow_event_otx_ideas(faces_dir: str):
    for face_name_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name_dir)
        for face_br_ref in get_existing_excel_idea_file_refs(face_dir):
            face_idea_path = create_path(face_dir, face_br_ref.file_name)
            split_excel_into_dirs(
                input_file=face_idea_path,
                output_dir=face_dir,
                column_name="event_int",
                file_name=face_br_ref.idea_number,
                sheet_name="boat_valid",
            )


def get_pidgin_events_by_dirs(faces_dir: str) -> dict[FaceName, set[EventInt]]:
    pidgin_events = {}
    for face_name in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name)
        for event_int in get_level1_dirs(face_dir):
            event_dir = create_path(face_dir, event_int)
            pidgin_path = create_path(event_dir, "pidgin.json")
            if os_path_exists(pidgin_path):
                if pidgin_events.get(face_name) is None:
                    pidgin_events[face_name] = {int(event_int)}
                else:
                    events_list = pidgin_events.get(face_name)
                    events_list.add(int(event_int))
    return pidgin_events


def get_most_recent_event_int(
    event_set: set[EventInt], max_event_int: EventInt
) -> EventInt:
    recent_event_ints = [e_id for e_id in event_set if e_id <= max_event_int]
    return max(recent_event_ints, default=None)


def etl_bow_event_ideas_to_inx_events(
    faces_bow_dir: str, event_pidgins: dict[FaceName, set[EventInt]]
):
    for face_name in get_level1_dirs(faces_bow_dir):
        face_pidgin_events = event_pidgins.get(face_name)
        if face_pidgin_events is None:
            face_pidgin_events = set()
        face_dir = create_path(faces_bow_dir, face_name)
        for event_int in get_level1_dirs(face_dir):
            event_int = int(event_int)
            event_dir = create_path(face_dir, event_int)
            pidgin_event_int = get_most_recent_event_int(face_pidgin_events, event_int)
            for event_br_ref in get_existing_excel_idea_file_refs(event_dir):
                event_idea_path = create_path(event_dir, event_br_ref.file_name)
                idea_df = pandas_read_excel(event_idea_path, "boat_valid")
                if pidgin_event_int != None:
                    pidgin_event_dir = create_path(face_dir, pidgin_event_int)
                    pidgin_path = create_path(pidgin_event_dir, "pidgin.json")
                    x_pidginunit = get_pidginunit_from_json(open_file(pidgin_path))
                    translate_all_columns_dataframe(idea_df, x_pidginunit)
                upsert_sheet(event_idea_path, "inx", idea_df)


def etl_bow_inx_event_ideas_to_aft_faces(faces_bow_dir: str, faces_aft_dir: str):
    for face_name in get_level1_dirs(faces_bow_dir):
        face_dir = create_path(faces_bow_dir, face_name)
        for event_int in get_level1_dirs(face_dir):
            event_int = int(event_int)
            event_dir = create_path(face_dir, event_int)
            for event_br_ref in get_existing_excel_idea_file_refs(event_dir):
                event_idea_path = create_path(event_dir, event_br_ref.file_name)
                split_excel_into_dirs(
                    input_file=event_idea_path,
                    output_dir=faces_aft_dir,
                    column_name="face_name",
                    file_name=event_br_ref.idea_number,
                    sheet_name="inx",
                )


def etl_aft_face_ideas_to_aft_event_ideas(faces_aft_dir: str):
    for face_name_dir in get_level1_dirs(faces_aft_dir):
        face_dir = create_path(faces_aft_dir, face_name_dir)
        for face_br_ref in get_existing_excel_idea_file_refs(face_dir):
            face_idea_path = create_path(face_dir, face_br_ref.file_name)
            split_excel_into_dirs(
                input_file=face_idea_path,
                output_dir=face_dir,
                column_name="event_int",
                file_name=face_br_ref.idea_number,
                sheet_name="inx",
            )


def etl_aft_event_ideas_to_fiscal_ideas(faces_aft_dir: str):
    for face_name in get_level1_dirs(faces_aft_dir):
        face_dir = create_path(faces_aft_dir, face_name)
        for event_int in get_level1_dirs(face_dir):
            event_int = int(event_int)
            event_dir = create_path(face_dir, event_int)
            for event_br_ref in get_existing_excel_idea_file_refs(event_dir):
                event_idea_path = create_path(event_dir, event_br_ref.file_name)
                split_excel_into_dirs(
                    input_file=event_idea_path,
                    output_dir=event_dir,
                    column_name="fiscal_title",
                    file_name=event_br_ref.idea_number,
                    sheet_name="inx",
                )


def etl_aft_face_ideas_to_csv_files(faces_aft_dir: str):
    for face_name in get_level1_dirs(faces_aft_dir):
        face_dir = create_path(faces_aft_dir, face_name)
        for face_br_ref in get_existing_excel_idea_file_refs(face_dir):
            face_idea_excel_path = create_path(face_dir, face_br_ref.file_name)
            idea_csv = get_ordered_csv(pandas_read_excel(face_idea_excel_path, "inx"))
            save_file(face_dir, face_br_ref.get_csv_filename(), idea_csv)


def etl_aft_face_csv_files_to_fiscal_db(conn: sqlite3_Connection, faces_aft_dir: str):
    for face_name in get_level1_dirs(faces_aft_dir):
        face_dir = create_path(faces_aft_dir, face_name)
        for idea_number in sorted(get_idea_numbers()):
            csv_filename = f"{idea_number}.csv"
            csv_path = create_path(face_dir, csv_filename)
            if os_path_exists(csv_path):
                insert_idea_csv(csv_path, conn, f"{idea_number}_staging")


def etl_idea_staging_to_fiscal_tables(conn):
    create_fiscal_tables(conn)
    idea_staging_tables2fiscal_staging_tables(conn)
    fiscal_staging_tables2fiscal_agg_tables(conn)


def create_fiscal_tables(conn: sqlite3_Connection):
    fiscalunit_agg_cols = [
        "fiscal_title",
        "fund_coin",
        "penny",
        "respect_bit",
        "present_time",
        "bridge",
        "c400_number",
        "yr1_jan1_offset",
        "monthday_distortion",
        "timeline_title",
    ]
    fiscaldeal_agg_cols = ["fiscal_title", "owner_name", "time_int", "quota"]
    fiscalcash_agg_cols = [
        "fiscal_title",
        "owner_name",
        "acct_name",
        "time_int",
        "amount",
    ]
    fiscalhour_agg_cols = ["fiscal_title", "hour_title", "cumlative_minute"]
    fiscalmont_agg_cols = ["fiscal_title", "month_title", "cumlative_day"]
    fiscalweek_agg_cols = ["fiscal_title", "weekday_title", "weekday_order"]
    fiscalunit_agg = "fiscalunit_agg"
    fiscaldeal_agg = "fiscal_deal_episode_agg"
    fiscalcash_agg = "fiscal_cashbook_agg"
    fiscalhour_agg = "fiscal_timeline_hour_agg"
    fiscalmont_agg = "fiscal_timeline_month_agg"
    fiscalweek_agg = "fiscal_timeline_weekday_agg"
    col_types = get_idea_sqlite_types()
    create_table_from_columns(conn, fiscalunit_agg, fiscalunit_agg_cols, col_types)
    create_table_from_columns(conn, fiscaldeal_agg, fiscaldeal_agg_cols, col_types)
    create_table_from_columns(conn, fiscalcash_agg, fiscalcash_agg_cols, col_types)
    create_table_from_columns(conn, fiscalhour_agg, fiscalhour_agg_cols, col_types)
    create_table_from_columns(conn, fiscalmont_agg, fiscalmont_agg_cols, col_types)
    create_table_from_columns(conn, fiscalweek_agg, fiscalweek_agg_cols, col_types)

    staging_columns = ["idea_number", "face_name", "event_int"]
    fiscalunit_stage_cols = copy_copy(staging_columns)
    fiscaldeal_stage_cols = copy_copy(staging_columns)
    fiscalcash_stage_cols = copy_copy(staging_columns)
    fiscalhour_stage_cols = copy_copy(staging_columns)
    fiscalmont_stage_cols = copy_copy(staging_columns)
    fiscalweek_stage_cols = copy_copy(staging_columns)
    fiscalunit_agg_cols.extend(["error_message"])
    fiscaldeal_agg_cols.extend(["error_message"])
    fiscalcash_agg_cols.extend(["error_message"])
    fiscalhour_agg_cols.extend(["error_message"])
    fiscalmont_agg_cols.extend(["error_message"])
    fiscalweek_agg_cols.extend(["error_message"])
    fiscalunit_stage_cols.extend(fiscalunit_agg_cols)
    fiscaldeal_stage_cols.extend(fiscaldeal_agg_cols)
    fiscalcash_stage_cols.extend(fiscalcash_agg_cols)
    fiscalhour_stage_cols.extend(fiscalhour_agg_cols)
    fiscalmont_stage_cols.extend(fiscalmont_agg_cols)
    fiscalweek_stage_cols.extend(fiscalweek_agg_cols)
    fiscalunit_stage = "fiscalunit_staging"
    fiscaldeal_stage = "fiscal_deal_episode_staging"
    fiscalcash_stage = "fiscal_cashbook_staging"
    fiscalhour_stage = "fiscal_timeline_hour_staging"
    fiscalmont_stage = "fiscal_timeline_month_staging"
    fiscalweek_stage = "fiscal_timeline_weekday_staging"
    create_table_from_columns(conn, fiscalunit_stage, fiscalunit_stage_cols, col_types)
    create_table_from_columns(conn, fiscaldeal_stage, fiscaldeal_stage_cols, col_types)
    create_table_from_columns(conn, fiscalcash_stage, fiscalcash_stage_cols, col_types)
    create_table_from_columns(conn, fiscalhour_stage, fiscalhour_stage_cols, col_types)
    create_table_from_columns(conn, fiscalmont_stage, fiscalmont_stage_cols, col_types)
    create_table_from_columns(conn, fiscalweek_stage, fiscalweek_stage_cols, col_types)


def idea_staging_tables2fiscal_staging_tables(fiscal_db_conn: sqlite3_Connection):
    unit_dst = "fiscalunit_staging"
    deal_dst = "fiscal_deal_episode_staging"
    cash_dst = "fiscal_cashbook_staging"
    hour_dst = "fiscal_timeline_hour_staging"
    mont_dst = "fiscal_timeline_month_staging"
    week_dst = "fiscal_timeline_weekday_staging"
    unit_marks = set(get_fiscalunit_sorted_args())
    deal_marks = set(get_fiscaldeal_sorted_args())
    cash_marks = set(get_fiscalcash_sorted_args())
    hour_marks = set(get_fiscalhour_sorted_args())
    mont_marks = set(get_fiscalmont_sorted_args())
    week_marks = set(get_fiscalweek_sorted_args())
    deal_marks.remove("fiscal_title")
    deal_marks.remove("owner_name")
    cash_marks.remove("fiscal_title")
    cash_marks.remove("owner_name")
    cash_marks.remove("acct_name")
    hour_marks.remove("fiscal_title")
    mont_marks.remove("fiscal_title")
    week_marks.remove("fiscal_title")
    for idea_number in get_idea_numbers():
        idea_staging = f"{idea_number}_staging"
        if db_table_exists(fiscal_db_conn, idea_staging):
            insert_fiscal_staging(fiscal_db_conn, idea_number, unit_dst, unit_marks)
            insert_fiscal_staging(fiscal_db_conn, idea_number, deal_dst, deal_marks)
            insert_fiscal_staging(fiscal_db_conn, idea_number, cash_dst, cash_marks)
            insert_fiscal_staging(fiscal_db_conn, idea_number, hour_dst, hour_marks)
            insert_fiscal_staging(fiscal_db_conn, idea_number, mont_dst, mont_marks)
            insert_fiscal_staging(fiscal_db_conn, idea_number, week_dst, week_marks)


def insert_fiscal_staging(
    fiscal_db_conn: sqlite3_Connection,
    idea_number: str,
    dst_table: str,
    mark_columns: set[str],
):
    src_table = f"{idea_number}_staging"
    src_columns = get_table_columns(fiscal_db_conn, src_table)
    if not mark_columns.isdisjoint(src_columns):
        dst_columns = get_table_columns(fiscal_db_conn, dst_table)
        common_columns_set = set(dst_columns).intersection(set(src_columns))
        common_columns_list = [col for col in dst_columns if col in common_columns_set]
        common_columns_header = ", ".join(common_columns_list)
        cursor = fiscal_db_conn.cursor()
        insert_idea_staging_agg_str = f"""
INSERT INTO {dst_table} (idea_number, {common_columns_header})
SELECT '{idea_number}' as idea_number, {common_columns_header}
FROM {src_table}
GROUP BY face_name, event_int, fiscal_title
;
"""
        cursor.execute(insert_idea_staging_agg_str)
        cursor.close()


FISCALUNIT_INCONSISTENCY_SQLSTR = """SELECT fiscal_title
FROM fiscalunit_staging
GROUP BY fiscal_title
HAVING MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
    OR MIN(present_time) != MAX(present_time)
    OR MIN(bridge) != MAX(bridge)
    OR MIN(c400_number) != MAX(c400_number)
    OR MIN(yr1_jan1_offset) != MAX(yr1_jan1_offset)
    OR MIN(monthday_distortion) != MAX(monthday_distortion)
    OR MIN(timeline_title) != MAX(timeline_title)
"""
FISCALDEAL_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, owner_name, time_int
FROM fiscal_deal_episode_staging
GROUP BY fiscal_title, owner_name, time_int
HAVING MIN(quota) != MAX(quota)
"""
FISCALCASH_INCONSISTENCY_SQLSTR = """SELECT acct_name, fiscal_title, owner_name, time_int
FROM fiscal_cashbook_staging
GROUP BY acct_name, fiscal_title, owner_name, time_int
HAVING MIN(amount) != MAX(amount)
"""
FISCALHOUR_INCONSISTENCY_SQLSTR = """SELECT fiscal_title
FROM fiscal_timeline_hour_staging
GROUP BY fiscal_title, hour_title
HAVING MIN(hour_title) != MAX(hour_title)
    OR MIN(cumlative_minute) != MAX(cumlative_minute)
"""
FISCALMONT_INCONSISTENCY_SQLSTR = """SELECT fiscal_title
FROM fiscal_timeline_month_staging
GROUP BY fiscal_title, month_title
HAVING MIN(cumlative_day) != MAX(cumlative_day)
"""
FISCALWEEK_INCONSISTENCY_SQLSTR = """SELECT fiscal_title
FROM fiscal_timeline_weekday_staging
GROUP BY fiscal_title, weekday_title
HAVING MIN(weekday_order) != MAX(weekday_order)
"""

FISCALUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALUNIT_INCONSISTENCY_SQLSTR}
)
UPDATE fiscalunit_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscalunit_staging.fiscal_title
;
"""
FISCALDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALDEAL_INCONSISTENCY_SQLSTR}
)
UPDATE fiscal_deal_episode_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_deal_episode_staging.fiscal_title
    AND inconsistency_rows.owner_name = fiscal_deal_episode_staging.owner_name
    AND inconsistency_rows.time_int = fiscal_deal_episode_staging.time_int
;
"""
FISCALCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALCASH_INCONSISTENCY_SQLSTR}
)
UPDATE fiscal_cashbook_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_cashbook_staging.fiscal_title
    AND inconsistency_rows.owner_name = fiscal_cashbook_staging.owner_name
    AND inconsistency_rows.acct_name = fiscal_cashbook_staging.acct_name
    AND inconsistency_rows.time_int = fiscal_cashbook_staging.time_int
;
"""
FISCALHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALHOUR_INCONSISTENCY_SQLSTR}
)
UPDATE fiscal_timeline_hour_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_timeline_hour_staging.fiscal_title
    AND inconsistency_rows.hour_title = fiscal_timeline_hour_staging.hour_title
;
"""
FISCALMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALMONT_INCONSISTENCY_SQLSTR}
)
UPDATE fiscal_timeline_month_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_timeline_month_staging.fiscal_title
;
"""
FISCALWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALWEEK_INCONSISTENCY_SQLSTR}
)
UPDATE fiscal_timeline_weekday_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_timeline_weekday_staging.fiscal_title
;
"""


def set_fiscal_staging_error_message(fiscal_db_conn: sqlite3_Connection):
    cursor = fiscal_db_conn.cursor()
    cursor.execute(FISCALUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR)
    cursor.execute(FISCALDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR)
    cursor.execute(FISCALCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR)
    cursor.execute(FISCALHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR)
    cursor.execute(FISCALMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR)
    cursor.execute(FISCALWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR)
    cursor.close()


FISCALUNIT_AGG_INSERT_SQLSTR = """INSERT INTO fiscalunit_agg (fiscal_title, fund_coin, penny, respect_bit, present_time, bridge, c400_number, yr1_jan1_offset, monthday_distortion, timeline_title)
SELECT fiscal_title, fund_coin, penny, respect_bit, present_time, bridge, c400_number, yr1_jan1_offset, monthday_distortion, timeline_title
FROM fiscalunit_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, fund_coin, penny, respect_bit, present_time, bridge, c400_number, yr1_jan1_offset, monthday_distortion, timeline_title
;
"""
FISCALDEAL_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_deal_episode_agg (fiscal_title, owner_name, time_int, quota)
SELECT fiscal_title, owner_name, time_int, quota
FROM fiscal_deal_episode_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, owner_name, time_int, quota
;
"""
FISCALCASH_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_cashbook_agg (fiscal_title, owner_name, acct_name, time_int, amount)
SELECT fiscal_title, owner_name, acct_name, time_int, amount
FROM fiscal_cashbook_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, owner_name, acct_name, time_int, amount
;
"""
FISCALHOUR_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_timeline_hour_agg (fiscal_title, hour_title, cumlative_minute)
SELECT fiscal_title, hour_title, cumlative_minute
FROM fiscal_timeline_hour_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, hour_title, cumlative_minute
;
"""
FISCALMONT_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_timeline_month_agg (fiscal_title, month_title, cumlative_day)
SELECT fiscal_title, month_title, cumlative_day
FROM fiscal_timeline_month_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, month_title, cumlative_day
;
"""
FISCALWEEK_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_timeline_weekday_agg (fiscal_title, weekday_title, weekday_order)
SELECT fiscal_title, weekday_title, weekday_order
FROM fiscal_timeline_weekday_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, weekday_title, weekday_order
;
"""


def fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn: sqlite3_Connection):
    cursor = fiscal_db_conn.cursor()
    cursor.execute(FISCALUNIT_AGG_INSERT_SQLSTR)
    # cursor.execute(FISCALDEAL_AGG_INSERT_SQLSTR)
    # cursor.execute(FISCALCASH_AGG_INSERT_SQLSTR)
    cursor.execute(FISCALHOUR_AGG_INSERT_SQLSTR)
    cursor.execute(FISCALMONT_AGG_INSERT_SQLSTR)
    cursor.execute(FISCALWEEK_AGG_INSERT_SQLSTR)
    cursor.close()


def etl_fiscal_staging_tables_to_fiscal_csvs(
    fiscal_db_conn: sqlite3_Connection, fiscal_mstr_dir: str
):
    fiscalunit_str = "fiscalunit"
    fiscaldeal_str = "fiscal_deal_episode"
    fiscalcash_str = "fiscal_cashbook"
    fiscalhour_str = "fiscal_timeline_hour"
    fiscalmont_str = "fiscal_timeline_month"
    fiscalweek_str = "fiscal_timeline_weekday"
    fiscalunit_staging_tablename = f"{fiscalunit_str}_staging"
    fiscaldeal_staging_tablename = f"{fiscaldeal_str}_staging"
    fiscalcash_staging_tablename = f"{fiscalcash_str}_staging"
    fiscalhour_staging_tablename = f"{fiscalhour_str}_staging"
    fiscalmont_staging_tablename = f"{fiscalmont_str}_staging"
    fiscalweek_staging_tablename = f"{fiscalweek_str}_staging"
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalunit_staging_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscaldeal_staging_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalcash_staging_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalhour_staging_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalmont_staging_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalweek_staging_tablename)


def etl_fiscal_agg_tables_to_fiscal_csvs(
    fiscal_db_conn: sqlite3_Connection, fiscal_mstr_dir: str
):
    fiscalunit_str = "fiscalunit"
    fiscaldeal_str = "fiscal_deal_episode"
    fiscalcash_str = "fiscal_cashbook"
    fiscalhour_str = "fiscal_timeline_hour"
    fiscalmont_str = "fiscal_timeline_month"
    fiscalweek_str = "fiscal_timeline_weekday"
    fiscalunit_agg_tablename = f"{fiscalunit_str}_agg"
    fiscaldeal_agg_tablename = f"{fiscaldeal_str}_agg"
    fiscalcash_agg_tablename = f"{fiscalcash_str}_agg"
    fiscalhour_agg_tablename = f"{fiscalhour_str}_agg"
    fiscalmont_agg_tablename = f"{fiscalmont_str}_agg"
    fiscalweek_agg_tablename = f"{fiscalweek_str}_agg"
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalunit_agg_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscaldeal_agg_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalcash_agg_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalhour_agg_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalmont_agg_tablename)
    save_table_to_csv(fiscal_db_conn, fiscal_mstr_dir, fiscalweek_agg_tablename)


def etl_fiscal_csvs_to_jsons(fiscal_mstr_dir: str):
    fiscalunit_str = "fiscalunit"
    fiscaldeal_str = "fiscal_deal_episode"
    fiscalcash_str = "fiscal_cashbook"
    fiscalhour_str = "fiscal_timeline_hour"
    fiscalmont_str = "fiscal_timeline_month"
    fiscalweek_str = "fiscal_timeline_weekday"
    fiscalunit_excel_path = create_path(fiscal_mstr_dir, f"{fiscalunit_str}.xlsx")
    fiscaldeal_excel_path = create_path(fiscal_mstr_dir, f"{fiscaldeal_str}.xlsx")
    fiscalcash_excel_path = create_path(fiscal_mstr_dir, f"{fiscalcash_str}.xlsx")
    fiscalhour_excel_path = create_path(fiscal_mstr_dir, f"{fiscalhour_str}.xlsx")
    fiscalmont_excel_path = create_path(fiscal_mstr_dir, f"{fiscalmont_str}.xlsx")
    fiscalweek_excel_path = create_path(fiscal_mstr_dir, f"{fiscalweek_str}.xlsx")
    fiscalunit_df = open_csv(fiscal_mstr_dir, f"{fiscalunit_str}_agg.csv")
    fiscaldeal_df = open_csv(fiscal_mstr_dir, f"{fiscaldeal_str}_agg.csv")
    fiscalcash_df = open_csv(fiscal_mstr_dir, f"{fiscalcash_str}_agg.csv")
    fiscalhour_df = open_csv(fiscal_mstr_dir, f"{fiscalhour_str}_agg.csv")
    fiscalmont_df = open_csv(fiscal_mstr_dir, f"{fiscalmont_str}_agg.csv")
    fiscalweek_df = open_csv(fiscal_mstr_dir, f"{fiscalweek_str}_agg.csv")
    upsert_sheet(fiscalunit_excel_path, "agg", fiscalunit_df)
    upsert_sheet(fiscaldeal_excel_path, "agg", fiscaldeal_df)
    upsert_sheet(fiscalcash_excel_path, "agg", fiscalcash_df)
    upsert_sheet(fiscalhour_excel_path, "agg", fiscalhour_df)
    upsert_sheet(fiscalmont_excel_path, "agg", fiscalmont_df)
    upsert_sheet(fiscalweek_excel_path, "agg", fiscalweek_df)

    # TODO replace empty sheet upsert with csv file upsert
    # xp = FiscalPrimeObjsRef(fiscal_mstr_dir)
    # xc = FiscalPrimeColumnsRef()
    # agg_fiscal_deal_df = DataFrame([], columns=xc.fiscal_deal_agg_columns)
    # agg_fiscal_cashbook_df = DataFrame([], columns=xc.fiscal_cashbook_agg_columns)
    # agg_fiscal_hour_df = DataFrame([], columns=xc.fiscal_hour_agg_columns)
    # agg_fiscal_month_df = DataFrame([], columns=xc.fiscal_month_agg_columns)
    # agg_fiscal_weekday_df = DataFrame([], columns=xc.fiscal_weekday_agg_columns)
    # upsert_sheet(xp.deal_excel_path, "agg", agg_fiscal_deal_df)
    # upsert_sheet(xp.cash_excel_path, "agg", agg_fiscal_cashbook_df)
    # upsert_sheet(xp.hour_excel_path, "agg", agg_fiscal_hour_df)
    # upsert_sheet(xp.mont_excel_path, "agg", agg_fiscal_month_df)
    # upsert_sheet(xp.week_excel_path, "agg", agg_fiscal_weekday_df)

    # if fiscaldeal_df:
    #     upsert_sheet(fiscal_excel_path, fiscaldeal_str, fiscaldeal_df)
    # if fiscalcash_df:
    #     upsert_sheet(fiscal_excel_path, fiscalcash_str, fiscalcash_df)
    # if fiscalhour_df:
    #     upsert_sheet(fiscal_excel_path, fiscalhour_str, fiscalhour_df)
    # if fiscalmont_df:
    #     upsert_sheet(fiscal_excel_path, fiscalmont_str, fiscalmont_df)
    # if fiscalweek_df:
    #     upsert_sheet(fiscal_excel_path, fiscalweek_str, fiscalweek_df)
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)
