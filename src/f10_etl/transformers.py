from src.f00_instrument.file import create_path, get_dir_file_strs, save_file, open_file
from src.f00_instrument.db_toolbox import (
    db_table_exists,
    get_table_columns,
    is_stageable,
)
from src.f01_road.road import FaceName, EventInt
from src.f04_gift.atom_config import get_bud_dimens
from src.f07_fiscal.fiscal_config import get_fiscal_dimens
from src.f08_pidgin.pidgin import get_pidginunit_from_json, inherit_pidginunit
from src.f08_pidgin.pidgin_config import get_quick_pidgens_column_ref
from src.f09_idea.idea_config import (
    get_idea_numbers,
    get_idea_format_filename,
    get_idea_dimen_ref,
    get_idea_config_dict,
)
from src.f09_idea.idea import get_idearef_obj
from src.f09_idea.idea_db_tool import (
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
    get_idea_into_dimen_staging_query,
)
from src.f09_idea.pidgin_toolbox import init_pidginunit_from_dir
from src.f10_etl.tran_sqlstrs import (
    create_fiscal_tables,
    create_bud_tables,
    get_fiscal_update_inconsist_error_message_sqlstrs,
    get_fiscal_insert_agg_from_staging_sqlstrs,
    get_bud_update_inconsist_error_message_sqlstrs,
    get_bud_insert_agg_from_staging_sqlstrs,
)
from src.f10_etl.idea_collector import get_all_idea_dataframes, IdeaFileRef
from src.f10_etl.fiscal_etl_tool import create_fiscalunit_jsons_from_prime_files
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


class not_given_pidgin_dimen_Exception(Exception):
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


def get_class_type(pidgin_dimen: str) -> str:
    if pidgin_dimen not in MAPS_CATEGORYS:
        raise not_given_pidgin_dimen_Exception("not given pidgin_dimen")
    return MAPS_CATEGORYS[pidgin_dimen]


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
        voice_df = pandas_concat(dfs)
        boat_path = create_path(self.boat_dir, f"{idea_number}.xlsx")
        upsert_sheet(boat_path, "boat_staging", voice_df)


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
    pidgin_dimen: str, legitimate_events: set[EventInt], boat_dir: str
):
    x_events = legitimate_events
    transformer = boatAggToStagingTransformer(boat_dir, pidgin_dimen, x_events)
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
        self, boat_dir: str, pidgin_dimen: str, legitmate_events: set[EventInt]
    ):
        self.boat_dir = boat_dir
        self.legitmate_events = legitmate_events
        self.pidgin_dimen = pidgin_dimen
        self.class_type = get_class_type(pidgin_dimen)

    def transform(self):
        dimen_ideas = get_idea_dimen_ref().get(self.pidgin_dimen)
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_dimen)
        pidgin_columns.update({"face_name", "event_int"})
        pidgin_columns = get_custom_sorted_list(pidgin_columns)
        pidgin_columns.insert(0, "src_idea")
        pidgin_df = DataFrame(columns=pidgin_columns)
        for idea_number in sorted(dimen_ideas):
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


def etl_pidgin_single_staging_to_agg(boat_dir: str, map_dimen: str):
    transformer = PidginStagingToAggTransformer(boat_dir, map_dimen)
    transformer.transform()


def etl_boat_pidgin_staging_to_agg(boat_dir):
    etl_pidgin_name_staging_to_name_agg(boat_dir)
    etl_pidgin_label_staging_to_label_agg(boat_dir)
    etl_pidgin_road_staging_to_road_agg(boat_dir)
    etl_pidgin_title_staging_to_title_agg(boat_dir)


class PidginStagingToAggTransformer:
    def __init__(self, boat_dir: str, pidgin_dimen: str):
        self.boat_dir = boat_dir
        self.pidgin_dimen = pidgin_dimen
        self.file_path = create_path(self.boat_dir, "pidgin.xlsx")
        self.class_type = get_class_type(self.pidgin_dimen)

    def transform(self):
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_dimen)
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


def etl_aft_face_ideas_to_csv_files(faces_aft_dir: str):
    for face_name in get_level1_dirs(faces_aft_dir):
        face_dir = create_path(faces_aft_dir, face_name)
        for face_br_ref in get_existing_excel_idea_file_refs(face_dir):
            face_idea_excel_path = create_path(face_dir, face_br_ref.file_name)
            idea_csv = get_ordered_csv(pandas_read_excel(face_idea_excel_path, "inx"))
            save_file(face_dir, face_br_ref.get_csv_filename(), idea_csv)


def etl_aft_face_csv_files2idea_staging_tables(
    conn_or_cursor: sqlite3_Connection, faces_aft_dir: str
):
    for face_name in get_level1_dirs(faces_aft_dir):
        face_dir = create_path(faces_aft_dir, face_name)
        for idea_number in sorted(get_idea_numbers()):
            csv_filename = f"{idea_number}.csv"
            csv_path = create_path(face_dir, csv_filename)
            if os_path_exists(csv_path):
                insert_idea_csv(csv_path, conn_or_cursor, f"{idea_number}_staging")


def etl_idea_staging_to_fiscal_tables(conn_or_cursor):
    create_fiscal_tables(conn_or_cursor)
    idea_staging_tables2fiscal_staging_tables(conn_or_cursor)
    set_fiscal_staging_error_message(conn_or_cursor)
    fiscal_staging_tables2fiscal_agg_tables(conn_or_cursor)


def etl_idea_staging_to_bud_tables(conn_or_cursor):
    create_bud_tables(conn_or_cursor)
    idea_staging_tables2bud_staging_tables(conn_or_cursor)
    set_bud_staging_error_message(conn_or_cursor)
    bud_staging_tables2bud_agg_tables(conn_or_cursor)


def idea_staging_tables2fiscal_staging_tables(conn_or_cursor: sqlite3_Connection):
    fiscal_cats = get_fiscal_dimens()
    idea_config_dict = get_idea_config_dict()

    for idea_number in get_idea_numbers():
        idea_staging = f"{idea_number}_staging"
        if db_table_exists(conn_or_cursor, idea_staging):
            for x_cat in fiscal_cats:
                cat_config = idea_config_dict.get(x_cat)
                cat_jkeys = set(cat_config.get("jkeys").keys())
                if is_stageable(conn_or_cursor, idea_staging, cat_jkeys):
                    gen_sqlstr = get_idea_into_dimen_staging_query(
                        conn_or_cursor, idea_number, x_cat, cat_jkeys
                    )
                    conn_or_cursor.execute(gen_sqlstr)


def idea_staging_tables2bud_staging_tables(conn_or_cursor: sqlite3_Connection):
    bud_cats = get_bud_dimens()
    idea_config_dict = get_idea_config_dict()

    for idea_number in get_idea_numbers():
        idea_staging = f"{idea_number}_staging"
        if db_table_exists(conn_or_cursor, idea_staging):
            for x_cat in bud_cats:
                cat_config = idea_config_dict.get(x_cat)
                cat_jkeys = set(cat_config.get("jkeys").keys())
                if is_stageable(conn_or_cursor, idea_staging, cat_jkeys):
                    gen_sqlstr = get_idea_into_dimen_staging_query(
                        conn_or_cursor, idea_number, x_cat, cat_jkeys
                    )
                    conn_or_cursor.execute(gen_sqlstr)


def set_fiscal_staging_error_message(conn_or_cursor: sqlite3_Connection):
    for (
        set_error_sqlstr
    ) in get_fiscal_update_inconsist_error_message_sqlstrs().values():
        conn_or_cursor.execute(set_error_sqlstr)


def set_bud_staging_error_message(conn_or_cursor: sqlite3_Connection):
    for set_error_sqlstr in get_bud_update_inconsist_error_message_sqlstrs().values():
        conn_or_cursor.execute(set_error_sqlstr)


def fiscal_staging_tables2fiscal_agg_tables(conn_or_cursor: sqlite3_Connection):
    for x_sqlstr in get_fiscal_insert_agg_from_staging_sqlstrs().values():
        conn_or_cursor.execute(x_sqlstr)


def bud_staging_tables2bud_agg_tables(conn_or_cursor: sqlite3_Connection):
    for x_sqlstr in get_bud_insert_agg_from_staging_sqlstrs().values():
        conn_or_cursor.execute(x_sqlstr)


def etl_fiscal_staging_tables_to_fiscal_csvs(
    conn_or_cursor: sqlite3_Connection, fiscal_mstr_dir: str
):
    for ficsal_dimen in get_fiscal_dimens():
        staging_tablename = f"{ficsal_dimen}_staging"
        save_table_to_csv(conn_or_cursor, fiscal_mstr_dir, staging_tablename)


def etl_fiscal_agg_tables_to_fiscal_csvs(
    conn_or_cursor: sqlite3_Connection, fiscal_mstr_dir: str
):
    for ficsal_dimen in get_fiscal_dimens():
        save_table_to_csv(conn_or_cursor, fiscal_mstr_dir, f"{ficsal_dimen}_agg")


def etl_fiscal_csvs_to_jsons(fiscal_mstr_dir: str):
    for ficsal_dimen in get_fiscal_dimens():
        x_excel_path = create_path(fiscal_mstr_dir, f"{ficsal_dimen}.xlsx")
        cat_df = open_csv(fiscal_mstr_dir, f"{ficsal_dimen}_agg.csv")
        upsert_sheet(x_excel_path, "agg", cat_df)
    create_fiscalunit_jsons_from_prime_files(fiscal_mstr_dir)
