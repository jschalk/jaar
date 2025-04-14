from src.a00_data_toolboxs.file_toolbox import (
    create_path,
    get_dir_file_strs,
    save_file,
    open_file,
    save_json,
    open_json,
    get_level1_dirs,
)
from src.a00_data_toolboxs.csv_toolbox import open_csv_with_types
from src.a00_data_toolboxs.db_toolbox import (
    db_table_exists,
    get_row_count,
    save_to_split_csvs,
)
from src.a01_word_logic.road import FaceName, EventInt, OwnerName, FiscTitle
from src.a06_bud_logic.bud import budunit_shop, BudUnit
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a08_bud_atom_logic.atom_config import get_bud_dimens
from src.f04_pack.delta import get_minimal_buddelta
from src.f04_pack.pack import packunit_shop, get_packunit_from_json, PackUnit
from src.f06_listen.hub_path import (
    create_gut_path,
    create_fisc_ote1_csv_path,
    create_fisc_ote1_json_path,
    create_owner_event_dir_path,
    create_budevent_path,
)
from src.f06_listen.hub_tool import (
    collect_owner_event_dir_sets,
    get_owners_downhill_event_ints,
    open_bud_file,
    open_plan_file,
)
from src.f08_fisc.fisc import (
    get_from_default_path as fiscunit_get_from_default_path,
)
from src.f08_fisc.fisc_tool import (
    create_fisc_owners_cell_trees,
    set_cell_trees_found_facts,
    set_cell_trees_decrees,
    set_cell_tree_cell_mandates,
    create_deal_mandate_ledgers,
)
from src.f08_fisc.fisc_config import get_fisc_dimens
from src.f09_pidgin.pidgin import get_pidginunit_from_json, inherit_pidginunit
from src.f09_pidgin.pidgin_config import get_quick_pidgens_column_ref
from src.f10_idea.idea_config import (
    get_idea_numbers,
    get_idea_format_filename,
    get_idea_dimen_ref,
    get_idea_config_dict,
    get_idea_sqlite_types,
)
from src.f10_idea.idea import get_idearef_obj
from src.f10_idea.idea_db_tool import (
    get_default_sorted_list,
    upsert_sheet,
    split_excel_into_dirs,
    sheet_exists,
    _get_pidgen_idea_format_filenames,
    get_cart_staging_grouping_with_all_values_equal_df,
    translate_all_columns_dataframe,
    insert_idea_csv,
    save_table_to_csv,
    get_ordered_csv,
    get_idea_into_dimen_staging_query,
)
from src.f10_idea.pidgin_toolbox import init_pidginunit_from_dir
from src.f11_etl.tran_path import create_cart_events_path, create_cart_pidgin_path
from src.f11_etl.tran_sqlstrs import (
    get_bud_create_table_sqlstrs,
    create_fisc_tables,
    create_bud_tables,
    get_fisc_update_inconsist_error_message_sqlstrs,
    get_fisc_insert_agg_from_staging_sqlstrs,
    get_bud_put_update_inconsist_error_message_sqlstrs,
    get_bud_insert_put_agg_from_staging_sqlstrs,
    get_bud_insert_del_agg_from_staging_sqlstrs,
    IDEA_STAGEABLE_PUT_DIMENS,
    CREATE_FISC_EVENT_TIME_AGG_SQLSTR,
    INSERT_FISC_EVENT_TIME_AGG_SQLSTR,
    UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR,
    CREATE_FISC_OTE1_AGG_SQLSTR,
    INSERT_FISC_OTE1_AGG_SQLSTR,
)
from src.f11_etl.db_obj_tool import get_fisc_dict_from_db, insert_plan_obj
from src.f11_etl.idea_collector import get_all_idea_dataframes, IdeaFileRef
from src.f11_etl.pidgin_agg import (
    pidginheartbook_shop,
    PidginHeartRow,
    PidginHeartBook,
    pidginbodybook_shop,
    PidginBodyRow,
    PidginBodyBook,
)
from pandas import read_excel as pandas_read_excel, concat as pandas_concat, DataFrame
from os.path import exists as os_path_exists
from sqlite3 import Connection as sqlite3_Connection, Cursor as sqlite3_Cursor
from copy import deepcopy as copy_deepcopy


class not_given_pidgin_dimen_Exception(Exception):
    pass


MAPS_DIMENS = {
    "map_name": "NameUnit",
    "map_label": "LabelUnit",
    "map_title": "TitleUnit",
    "map_road": "RoadUnit",
}

class_typeS = {
    "NameUnit": {
        "stage": "name_staging",
        "agg": "name_agg",
        "csv_filename": "name.csv",
        "otx_obj": "otx_name",
        "inx_obj": "inx_name",
    },
    "LabelUnit": {
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
    if pidgin_dimen not in MAPS_DIMENS:
        raise not_given_pidgin_dimen_Exception("not given pidgin_dimen")
    return MAPS_DIMENS[pidgin_dimen]


def get_sheet_stage_name(class_type: str) -> str:
    return class_typeS[class_type]["stage"]


def get_sheet_agg_name(class_type: str) -> str:
    return class_typeS[class_type]["agg"]


def get_otx_obj(class_type, x_row) -> str:
    return x_row[class_typeS[class_type]["otx_obj"]]


def get_inx_obj(class_type, x_row) -> str:
    return x_row[class_typeS[class_type]["inx_obj"]]


def etl_mine_to_cart_staging(mine_dir: str, cart_dir: str):
    transformer = MineTocartTransformer(mine_dir, cart_dir)
    transformer.transform()


class MineTocartTransformer:
    def __init__(self, mine_dir: str, cart_dir: str):
        self.mine_dir = mine_dir
        self.cart_dir = cart_dir

    def transform(self):
        for idea_number, dfs in self._group_mine_data().items():
            self._save_to_cart_staging(idea_number, dfs)

    def _group_mine_data(self):
        grouped_data = {}
        for ref in get_all_idea_dataframes(self.mine_dir):
            df = self._read_and_tag_dataframe(ref)
            grouped_data.setdefault(ref.idea_number, []).append(df)
        return grouped_data

    def _read_and_tag_dataframe(self, ref):
        x_file_path = create_path(ref.file_dir, ref.filename)
        df = pandas_read_excel(x_file_path, ref.sheet_name)
        df["file_dir"] = ref.file_dir
        df["filename"] = ref.filename
        df["sheet_name"] = ref.sheet_name
        return df

    def _save_to_cart_staging(self, idea_number: str, dfs: list):
        plan_df = pandas_concat(dfs)
        cart_path = create_path(self.cart_dir, f"{idea_number}.xlsx")
        upsert_sheet(cart_path, "cart_staging", plan_df)


def get_existing_excel_idea_file_refs(x_dir: str) -> list[IdeaFileRef]:
    existing_excel_idea_filepaths = []
    for idea_number in sorted(get_idea_numbers()):
        idea_filename = f"{idea_number}.xlsx"
        x_idea_path = create_path(x_dir, idea_filename)
        if os_path_exists(x_idea_path):
            x_fileref = IdeaFileRef(
                file_dir=x_dir, filename=idea_filename, idea_number=idea_number
            )
            existing_excel_idea_filepaths.append(x_fileref)
    return existing_excel_idea_filepaths


def etl_cart_staging_to_cart_agg(cart_dir):
    transformer = CartStagingToCartAggTransformer(cart_dir)
    transformer.transform()


class CartStagingToCartAggTransformer:
    def __init__(self, cart_dir: str):
        self.cart_dir = cart_dir

    def transform(self):
        for br_ref in get_existing_excel_idea_file_refs(self.cart_dir):
            cart_idea_path = create_path(br_ref.file_dir, br_ref.filename)
            cart_staging_df = pandas_read_excel(cart_idea_path, "cart_staging")
            otx_df = self._groupby_idea_columns(cart_staging_df, br_ref.idea_number)
            upsert_sheet(cart_idea_path, "cart_agg", otx_df)

    def _groupby_idea_columns(
        self, cart_staging_df: DataFrame, idea_number: str
    ) -> DataFrame:
        idea_filename = get_idea_format_filename(idea_number)
        idearef = get_idearef_obj(idea_filename)
        required_columns = idearef.get_otx_keys_list()
        idea_columns_set = set(idearef._attributes.keys())
        idea_columns_list = get_default_sorted_list(idea_columns_set)
        cart_staging_df = cart_staging_df[idea_columns_list]
        return get_cart_staging_grouping_with_all_values_equal_df(
            cart_staging_df, required_columns
        )


def etl_cart_agg_to_cart_valid(cart_dir: str, legitimate_events: set[EventInt]):
    transformer = cartAggTocartValidTransformer(cart_dir, legitimate_events)
    transformer.transform()


class cartAggTocartValidTransformer:
    def __init__(self, cart_dir: str, legitimate_events: set[EventInt]):
        self.cart_dir = cart_dir
        self.legitimate_events = legitimate_events

    def transform(self):
        for br_ref in get_existing_excel_idea_file_refs(self.cart_dir):
            cart_idea_path = create_path(br_ref.file_dir, br_ref.filename)
            cart_agg = pandas_read_excel(cart_idea_path, "cart_agg")
            cart_valid_df = cart_agg[cart_agg["event_int"].isin(self.legitimate_events)]
            upsert_sheet(cart_idea_path, "cart_valid", cart_valid_df)

    # def _groupby_idea_columns(
    #     self, cart_staging_df: DataFrame, idea_number: str
    # ) -> DataFrame:
    #     idea_filename = get_idea_format_filename(idea_number)
    #     idearef = get_idearef_obj(idea_filename)
    #     required_columns = idearef.get_otx_keys_list()
    #     idea_columns_set = set(idearef._attributes.keys())
    #     idea_columns_list = get_default_sorted_list(idea_columns_set)
    #     cart_staging_df = cart_staging_df[idea_columns_list]
    #     return get_cart_staging_grouping_with_all_values_equal_df(
    #         cart_staging_df, required_columns
    #     )


def etl_cart_agg_to_cart_events(cart_dir):
    transformer = cartAggTocartEventsTransformer(cart_dir)
    transformer.transform()


class cartAggTocartEventsTransformer:
    def __init__(self, cart_dir: str):
        self.cart_dir = cart_dir

    def transform(self):
        for file_ref in get_existing_excel_idea_file_refs(self.cart_dir):
            cart_idea_path = create_path(self.cart_dir, file_ref.filename)
            cart_agg_df = pandas_read_excel(cart_idea_path, "cart_agg")
            events_df = self.get_unique_events(cart_agg_df)
            upsert_sheet(cart_idea_path, "cart_events", events_df)

    def get_unique_events(self, cart_agg_df: DataFrame) -> DataFrame:
        events_df = cart_agg_df[["face_name", "event_int"]].drop_duplicates()
        events_df["error_message"] = (
            events_df["event_int"]
            .duplicated(keep=False)
            .apply(lambda x: "invalid because of conflicting event_int" if x else "")
        )
        return events_df.sort_values(["face_name", "event_int"])


def etl_cart_events_to_events_log(cart_dir: str):
    transformer = cartEventsToEventsLogTransformer(cart_dir)
    transformer.transform()


class cartEventsToEventsLogTransformer:
    def __init__(self, cart_dir: str):
        self.cart_dir = cart_dir

    def transform(self):
        sheet_name = "cart_events"
        for br_ref in get_existing_excel_idea_file_refs(self.cart_dir):
            cart_idea_path = create_path(self.cart_dir, br_ref.filename)
            otx_events_df = pandas_read_excel(cart_idea_path, sheet_name)
            events_log_df = self.get_event_log_df(
                otx_events_df, self.cart_dir, br_ref.filename
            )
            self._save_events_log_file(events_log_df)

    def get_event_log_df(
        self, otx_events_df: DataFrame, x_dir: str, x_filename: str
    ) -> DataFrame:
        otx_events_df[["file_dir"]] = x_dir
        otx_events_df[["filename"]] = x_filename
        otx_events_df[["sheet_name"]] = "cart_events"
        cols = [
            "file_dir",
            "filename",
            "sheet_name",
            "face_name",
            "event_int",
            "error_message",
        ]
        otx_events_df = otx_events_df[cols]
        return otx_events_df

    def _save_events_log_file(self, events_df: DataFrame):
        events_file_path = create_cart_events_path(self.cart_dir)
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


def etl_cart_events_log_to_events_agg(cart_dir):
    transformer = EventsLogToEventsAggTransformer(cart_dir)
    transformer.transform()


class EventsLogToEventsAggTransformer:
    def __init__(self, cart_dir: str):
        self.cart_dir = cart_dir

    def transform(self):
        events_file_path = create_cart_events_path(self.cart_dir)
        if os_path_exists(events_file_path):
            events_log_df = pandas_read_excel(events_file_path, "events_log")
            events_agg_df = _create_events_agg_df(events_log_df)
            upsert_sheet(events_file_path, "events_agg", events_agg_df)


def get_events_dict_from_events_agg_file(cart_dir) -> dict[EventInt, FaceName]:
    events_file_path = create_cart_events_path(cart_dir)
    x_dict = {}
    if os_path_exists(events_file_path):
        events_agg_df = pandas_read_excel(events_file_path, "events_agg")
        for index, event_agg_row in events_agg_df.iterrows():
            x_note = event_agg_row["error_message"]
            if x_note != "invalid because of conflicting event_int":
                x_dict[event_agg_row["event_int"]] = event_agg_row["face_name"]
    return x_dict


def cart_agg_single_to_pidgin_staging(
    pidgin_dimen: str, legitimate_events: set[EventInt], cart_dir: str
):
    x_events = legitimate_events
    transformer = cartAggToStagingTransformer(cart_dir, pidgin_dimen, x_events)
    transformer.transform()


def etl_cart_agg_to_pidgin_name_staging(
    legitimate_events: set[EventInt], cart_dir: str
):
    cart_agg_single_to_pidgin_staging("map_name", legitimate_events, cart_dir)


def etl_cart_agg_to_pidgin_label_staging(
    legitimate_events: set[EventInt], cart_dir: str
):
    cart_agg_single_to_pidgin_staging("map_label", legitimate_events, cart_dir)


def etl_cart_agg_to_pidgin_title_staging(
    legitimate_events: set[EventInt], cart_dir: str
):
    cart_agg_single_to_pidgin_staging("map_title", legitimate_events, cart_dir)


def etl_cart_agg_to_pidgin_road_staging(
    legitimate_events: set[EventInt], cart_dir: str
):
    cart_agg_single_to_pidgin_staging("map_road", legitimate_events, cart_dir)


def etl_cart_agg_to_pidgin_staging(legitimate_events: set[EventInt], cart_dir: str):
    etl_cart_agg_to_pidgin_name_staging(legitimate_events, cart_dir)
    etl_cart_agg_to_pidgin_label_staging(legitimate_events, cart_dir)
    etl_cart_agg_to_pidgin_title_staging(legitimate_events, cart_dir)
    etl_cart_agg_to_pidgin_road_staging(legitimate_events, cart_dir)


class cartAggToStagingTransformer:
    def __init__(
        self, cart_dir: str, pidgin_dimen: str, legitmate_events: set[EventInt]
    ):
        self.cart_dir = cart_dir
        self.legitmate_events = legitmate_events
        self.pidgin_dimen = pidgin_dimen
        self.class_type = get_class_type(pidgin_dimen)

    def transform(self):
        dimen_ideas = get_idea_dimen_ref().get(self.pidgin_dimen)
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_dimen)
        pidgin_columns.update({"face_name", "event_int"})
        pidgin_columns = get_default_sorted_list(pidgin_columns)
        pidgin_columns.insert(0, "src_idea")
        pidgin_df = DataFrame(columns=pidgin_columns)
        for idea_number in sorted(dimen_ideas):
            idea_filename = f"{idea_number}.xlsx"
            cart_idea_path = create_path(self.cart_dir, idea_filename)
            if os_path_exists(cart_idea_path):
                self.insert_staging_rows(
                    pidgin_df, idea_number, cart_idea_path, pidgin_columns
                )

        pidgin_file_path = create_cart_pidgin_path(self.cart_dir)
        upsert_sheet(pidgin_file_path, get_sheet_stage_name(self.class_type), pidgin_df)

    def insert_staging_rows(
        self,
        stage_df: DataFrame,
        idea_number: str,
        cart_idea_path: str,
        df_columns: list[str],
    ):
        cart_agg_df = pandas_read_excel(cart_idea_path, sheet_name="cart_agg")
        df_missing_cols = set(df_columns).difference(cart_agg_df.columns)

        for index, x_row in cart_agg_df.iterrows():
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
        if self.class_type == "NameUnit" and "inx_name" not in missing_col:
            return x_row["inx_name"]
        elif self.class_type == "LabelUnit" and "inx_label" not in missing_col:
            return x_row["inx_label"]
        elif self.class_type == "TitleUnit" and "inx_title" not in missing_col:
            return x_row["inx_title"]
        elif self.class_type == "RoadUnit" and "inx_road" not in missing_col:
            return x_row["inx_road"]
        return None


def etl_pidgin_name_staging_to_name_agg(cart_dir: str):
    etl_pidgin_single_staging_to_agg(cart_dir, "map_name")


def etl_pidgin_label_staging_to_label_agg(cart_dir: str):
    etl_pidgin_single_staging_to_agg(cart_dir, "map_label")


def etl_pidgin_road_staging_to_road_agg(cart_dir: str):
    etl_pidgin_single_staging_to_agg(cart_dir, "map_road")


def etl_pidgin_title_staging_to_title_agg(cart_dir: str):
    etl_pidgin_single_staging_to_agg(cart_dir, "map_title")


def etl_pidgin_single_staging_to_agg(cart_dir: str, map_dimen: str):
    transformer = PidginStagingToAggTransformer(cart_dir, map_dimen)
    transformer.transform()


def etl_cart_pidgin_staging_to_agg(cart_dir):
    etl_pidgin_name_staging_to_name_agg(cart_dir)
    etl_pidgin_label_staging_to_label_agg(cart_dir)
    etl_pidgin_road_staging_to_road_agg(cart_dir)
    etl_pidgin_title_staging_to_title_agg(cart_dir)


class PidginStagingToAggTransformer:
    def __init__(self, cart_dir: str, pidgin_dimen: str):
        self.cart_dir = cart_dir
        self.pidgin_dimen = pidgin_dimen
        self.file_path = create_cart_pidgin_path(self.cart_dir)
        self.class_type = get_class_type(self.pidgin_dimen)

    def transform(self):
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_dimen)
        pidgin_columns.update({"face_name", "event_int"})
        pidgin_columns = get_default_sorted_list(pidgin_columns)
        pidgin_agg_df = DataFrame(columns=pidgin_columns)
        self.insert_agg_rows(pidgin_agg_df)
        upsert_sheet(self.file_path, get_sheet_agg_name(self.class_type), pidgin_agg_df)

    def insert_agg_rows(self, pidgin_agg_df: DataFrame):
        pidgin_file_path = create_cart_pidgin_path(self.cart_dir)
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


def etl_cart_pidgin_agg_to_otz_face_dirs(cart_dir: str, faces_dir: str):
    agg_pidgin = create_cart_pidgin_path(cart_dir)
    for class_type in class_typeS.keys():
        agg_sheet_name = class_typeS[class_type]["agg"]
        if sheet_exists(agg_pidgin, agg_sheet_name):
            split_excel_into_dirs(
                input_file=agg_pidgin,
                output_dir=faces_dir,
                column_name="face_name",
                filename="pidgin",
                sheet_name=agg_sheet_name,
            )


def etl_face_pidgin_to_event_pidgins(face_dir: str):
    face_pidgin_path = create_cart_pidgin_path(face_dir)
    for class_type in class_typeS.keys():
        agg_sheet_name = class_typeS[class_type]["agg"]
        if sheet_exists(face_pidgin_path, agg_sheet_name):
            split_excel_into_events_dirs(face_pidgin_path, face_dir, agg_sheet_name)


def etl_otz_face_pidgins_to_otz_event_pidgins(faces_dir: str):
    for face_name_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name_dir)
        etl_face_pidgin_to_event_pidgins(face_dir)


def split_excel_into_events_dirs(pidgin_file: str, face_dir: str, sheet_name: str):
    split_excel_into_dirs(pidgin_file, face_dir, "event_int", "pidgin", sheet_name)


def event_pidgin_to_pidgin_csv_files(event_pidgin_dir: str):
    event_pidgin_path = create_cart_pidgin_path(event_pidgin_dir)
    for class_type in class_typeS.keys():
        agg_sheet_name = class_typeS[class_type]["agg"]
        csv_filename = class_typeS[class_type]["csv_filename"]
        if sheet_exists(event_pidgin_path, agg_sheet_name):
            name_csv_path = create_path(event_pidgin_dir, csv_filename)
            name_df = pandas_read_excel(event_pidgin_path, agg_sheet_name)
            name_df.to_csv(name_csv_path, index=False)


def _get_all_faces_otz_dir_event_dirs(faces_dir) -> list[str]:
    full_event_dirs = []
    for face_name_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name_dir)
        event_dirs = get_dir_file_strs(face_dir, include_dirs=True, include_files=False)
        full_event_dirs.extend(
            create_path(face_dir, event_dir) for event_dir in event_dirs.keys()
        )
    return full_event_dirs


def etl_otz_event_pidgins_to_otz_pidgin_csv_files(faces_dir: str):
    for event_pidgin_dir in _get_all_faces_otz_dir_event_dirs(faces_dir):
        event_pidgin_to_pidgin_csv_files(event_pidgin_dir)


def etl_event_pidgin_csvs_to_pidgin_json(event_dir: str):
    pidginunit = init_pidginunit_from_dir(event_dir)
    save_file(event_dir, "pidgin.json", pidginunit.get_json(), replace=True)


def etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons(faces_dir: str):
    for event_pidgin_dir in _get_all_faces_otz_dir_event_dirs(faces_dir):
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


def etl_cart_ideas_to_otz_face_ideas(cart_dir: str, faces_dir: str):
    for cart_br_ref in get_existing_excel_idea_file_refs(cart_dir):
        cart_idea_path = create_path(cart_dir, cart_br_ref.filename)
        if cart_br_ref.filename not in _get_pidgen_idea_format_filenames():
            split_excel_into_dirs(
                input_file=cart_idea_path,
                output_dir=faces_dir,
                column_name="face_name",
                filename=cart_br_ref.idea_number,
                sheet_name="cart_valid",
            )


def etl_otz_face_ideas_to_otz_event_otx_ideas(faces_dir: str):
    for face_name_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name_dir)
        for face_br_ref in get_existing_excel_idea_file_refs(face_dir):
            face_idea_path = create_path(face_dir, face_br_ref.filename)
            split_excel_into_dirs(
                input_file=face_idea_path,
                output_dir=face_dir,
                column_name="event_int",
                filename=face_br_ref.idea_number,
                sheet_name="cart_valid",
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


def etl_otz_event_ideas_to_inx_events(
    faces_otz_dir: str, event_pidgins: dict[FaceName, set[EventInt]]
):
    for face_name in get_level1_dirs(faces_otz_dir):
        face_pidgin_events = event_pidgins.get(face_name)
        if face_pidgin_events is None:
            face_pidgin_events = set()
        face_dir = create_path(faces_otz_dir, face_name)
        for event_int in get_level1_dirs(face_dir):
            event_dir = create_path(face_dir, event_int)
            event_int = int(event_int)
            pidgin_event_int = get_most_recent_event_int(face_pidgin_events, event_int)
            for event_br_ref in get_existing_excel_idea_file_refs(event_dir):
                event_idea_path = create_path(event_dir, event_br_ref.filename)
                idea_df = pandas_read_excel(event_idea_path, "cart_valid")
                if pidgin_event_int != None:
                    pidgin_event_dir = create_path(face_dir, pidgin_event_int)
                    pidgin_path = create_path(pidgin_event_dir, "pidgin.json")
                    x_pidginunit = get_pidginunit_from_json(open_file(pidgin_path))
                    translate_all_columns_dataframe(idea_df, x_pidginunit)
                upsert_sheet(event_idea_path, "inx", idea_df)


def etl_otz_inx_event_ideas_to_inz_faces(faces_otz_dir: str, faces_inz_dir: str):
    for face_name in get_level1_dirs(faces_otz_dir):
        face_dir = create_path(faces_otz_dir, face_name)
        for event_int in get_level1_dirs(face_dir):
            event_int = int(event_int)
            event_dir = create_path(face_dir, event_int)
            for event_br_ref in get_existing_excel_idea_file_refs(event_dir):
                event_idea_path = create_path(event_dir, event_br_ref.filename)
                split_excel_into_dirs(
                    input_file=event_idea_path,
                    output_dir=faces_inz_dir,
                    column_name="face_name",
                    filename=event_br_ref.idea_number,
                    sheet_name="inx",
                )


def etl_inz_face_ideas_to_csv_files(faces_inz_dir: str):
    for face_name in get_level1_dirs(faces_inz_dir):
        face_dir = create_path(faces_inz_dir, face_name)
        for face_br_ref in get_existing_excel_idea_file_refs(face_dir):
            face_idea_excel_path = create_path(face_dir, face_br_ref.filename)
            idea_csv = get_ordered_csv(pandas_read_excel(face_idea_excel_path, "inx"))
            save_file(face_dir, face_br_ref.get_csv_filename(), idea_csv)


def etl_inz_face_csv_files2idea_staging_tables(
    conn_or_cursor: sqlite3_Connection, faces_inz_dir: str
):
    for face_name in get_level1_dirs(faces_inz_dir):
        face_dir = create_path(faces_inz_dir, face_name)
        for idea_number in sorted(get_idea_numbers()):
            csv_filename = f"{idea_number}.csv"
            csv_path = create_path(face_dir, csv_filename)
            if os_path_exists(csv_path):
                insert_idea_csv(csv_path, conn_or_cursor, f"{idea_number}_staging")


def etl_idea_staging_to_fisc_tables(conn_or_cursor):
    create_fisc_tables(conn_or_cursor)
    idea_staging_tables2fisc_staging_tables(conn_or_cursor)
    set_fisc_staging_error_message(conn_or_cursor)
    fisc_staging_tables2fisc_agg_tables(conn_or_cursor)
    fisc_agg_tables2fisc_event_time_agg(conn_or_cursor)


def etl_idea_staging_to_bud_tables(conn_or_cursor):
    create_bud_tables(conn_or_cursor)
    idea_staging_tables2bud_staging_tables(conn_or_cursor)
    set_bud_staging_error_message(conn_or_cursor)
    bud_staging_tables2bud_agg_tables(conn_or_cursor)


def idea_staging_tables2fisc_staging_tables(conn_or_cursor: sqlite3_Connection):
    idea_config_dict = get_idea_config_dict()
    for idea_number in get_idea_numbers():
        idea_staging = f"{idea_number}_staging"
        if db_table_exists(conn_or_cursor, idea_staging):
            # only inserts from pre-identified idea categorys
            stageable_dimens = IDEA_STAGEABLE_PUT_DIMENS.get(idea_number)
            for x_dimen in stageable_dimens:
                dimen_config = idea_config_dict.get(x_dimen)
                if dimen_config.get("idea_category") == "fisc":
                    dimen_jkeys = set(dimen_config.get("jkeys").keys())
                    gen_sqlstr = get_idea_into_dimen_staging_query(
                        conn_or_cursor, idea_number, x_dimen, dimen_jkeys
                    )
                    conn_or_cursor.execute(gen_sqlstr)

            # for x_dimen in fisc_dimens:
            #     dimen_config = idea_config_dict.get(x_dimen)
            #     dimen_jkeys = set(dimen_config.get("jkeys").keys())
            #     if is_stageable(conn_or_cursor, idea_staging, dimen_jkeys):
            #         gen_sqlstr = get_idea_into_dimen_staging_query(
            #             conn_or_cursor, idea_number, x_dimen, dimen_jkeys
            #         )
            #         conn_or_cursor.execute(gen_sqlstr)


def idea_staging_tables2bud_staging_tables(conn_or_cursor: sqlite3_Connection):
    idea_config_dict = get_idea_config_dict()

    for idea_number in get_idea_numbers():
        idea_staging = f"{idea_number}_staging"
        if db_table_exists(conn_or_cursor, idea_staging):
            # only inserts from pre-identified idea categorys
            stageable_dimens = IDEA_STAGEABLE_PUT_DIMENS.get(idea_number)
            for x_dimen in stageable_dimens:
                dimen_config = idea_config_dict.get(x_dimen)
                if dimen_config.get("idea_category") == "bud":
                    dimen_jkeys = set(dimen_config.get("jkeys").keys())
                    insert_sqlstr = get_idea_into_dimen_staging_query(
                        conn_or_cursor, idea_number, x_dimen, dimen_jkeys, "put"
                    )
                    conn_or_cursor.execute(insert_sqlstr)

            # manually checks each idea categorys
            # for x_dimen in bud_dimens:
            #     dimen_config = idea_config_dict.get(x_dimen)
            #     dimen_jkeys = set(dimen_config.get("jkeys").keys())
            #     if is_stageable(conn_or_cursor, idea_staging, dimen_jkeys):
            #         insert_sqlstr = get_idea_into_dimen_staging_query(
            #             conn_or_cursor, idea_number, x_dimen, dimen_jkeys
            #         )
            #         conn_or_cursor.execute(insert_sqlstr)


def set_fisc_staging_error_message(conn_or_cursor: sqlite3_Connection):
    for set_error_sqlstr in get_fisc_update_inconsist_error_message_sqlstrs().values():
        conn_or_cursor.execute(set_error_sqlstr)


def set_bud_staging_error_message(conn_or_cursor: sqlite3_Connection):
    for (
        set_error_sqlstr
    ) in get_bud_put_update_inconsist_error_message_sqlstrs().values():
        conn_or_cursor.execute(set_error_sqlstr)


def fisc_agg_tables2fisc_event_time_agg(conn_or_cursor: sqlite3_Connection):
    conn_or_cursor.execute(CREATE_FISC_EVENT_TIME_AGG_SQLSTR)
    conn_or_cursor.execute(INSERT_FISC_EVENT_TIME_AGG_SQLSTR)
    conn_or_cursor.execute(UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR)


def etl_fisc_agg_tables2fisc_ote1_agg(conn_or_cursor: sqlite3_Connection):
    conn_or_cursor.execute(CREATE_FISC_OTE1_AGG_SQLSTR)
    conn_or_cursor.execute(INSERT_FISC_OTE1_AGG_SQLSTR)


def etl_fisc_table2fisc_ote1_agg_csvs(
    conn_or_cursor: sqlite3_Connection, fisc_mstr_dir: str
):
    empty_ote1_csv_str = """fisc_title,owner_name,event_int,deal_time,error_message
"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        ote1_csv_path = create_fisc_ote1_csv_path(fisc_mstr_dir, fisc_title)
        save_file(ote1_csv_path, None, empty_ote1_csv_str)

    save_to_split_csvs(conn_or_cursor, "fisc_ote1_agg", ["fisc_title"], fiscs_dir)


def etl_fisc_ote1_agg_csvs2jsons(fisc_mstr_dir: str):
    idea_types = get_idea_sqlite_types()
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        csv_path = create_fisc_ote1_csv_path(fisc_mstr_dir, fisc_title)
        csv_arrays = open_csv_with_types(csv_path, idea_types)
        x_dict = {}
        header_row = csv_arrays.pop(0)
        for row in csv_arrays:
            owner_name = row[1]
            event_int = row[2]
            deal_time = row[3]
            if x_dict.get(owner_name) is None:
                x_dict[owner_name] = {}
            owner_dict = x_dict.get(owner_name)
            owner_dict[int(deal_time)] = event_int
        json_path = create_fisc_ote1_json_path(fisc_mstr_dir, fisc_title)
        save_json(json_path, None, x_dict)


def etl_create_deals_root_cells(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        fisc_dir = create_path(fiscs_dir, fisc_title)
        ote1_json_path = create_path(fisc_dir, "fisc_ote1_agg.json")
        if os_path_exists(ote1_json_path):
            ote1_dict = open_json(ote1_json_path)
            x_fiscunit = fiscunit_get_from_default_path(fisc_mstr_dir, fisc_title)
            x_fiscunit.create_deals_root_cells(ote1_dict)


def etl_create_fisc_cell_trees(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        create_fisc_owners_cell_trees(fisc_mstr_dir, fisc_title)


def etl_set_cell_trees_found_facts(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        set_cell_trees_found_facts(fisc_mstr_dir, fisc_title)


def etl_set_cell_trees_decrees(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        set_cell_trees_decrees(fisc_mstr_dir, fisc_title)


def etl_set_cell_tree_cell_mandates(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        set_cell_tree_cell_mandates(fisc_mstr_dir, fisc_title)


def etl_create_deal_mandate_ledgers(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        create_deal_mandate_ledgers(fisc_mstr_dir, fisc_title)


def fisc_staging_tables2fisc_agg_tables(conn_or_cursor: sqlite3_Connection):
    for x_sqlstr in get_fisc_insert_agg_from_staging_sqlstrs().values():
        conn_or_cursor.execute(x_sqlstr)


def bud_staging_tables2bud_agg_tables(conn_or_cursor: sqlite3_Connection):
    for x_sqlstr in get_bud_insert_put_agg_from_staging_sqlstrs().values():
        conn_or_cursor.execute(x_sqlstr)
    for x_sqlstr in get_bud_insert_del_agg_from_staging_sqlstrs().values():
        conn_or_cursor.execute(x_sqlstr)


def etl_bud_tables_to_event_bud_csvs(
    conn_or_cursor: sqlite3_Connection, fisc_mstr_dir: str
):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for bud_table in get_bud_create_table_sqlstrs():
        if get_row_count(conn_or_cursor, bud_table) > 0:
            save_to_split_csvs(
                conn_or_cursor=conn_or_cursor,
                tablename=bud_table,
                key_columns=["fisc_title", "owner_name", "event_int"],
                output_dir=fiscs_dir,
                col1_prefix="owners",
                col2_prefix="events",
            )


def etl_fisc_staging_tables_to_fisc_csvs(
    conn_or_cursor: sqlite3_Connection, fisc_mstr_dir: str
):
    for fisc_dimen in get_fisc_dimens():
        staging_tablename = f"{fisc_dimen}_staging"
        save_table_to_csv(conn_or_cursor, fisc_mstr_dir, staging_tablename)


def etl_fisc_agg_tables_to_fisc_csvs(
    conn_or_cursor: sqlite3_Connection, fisc_mstr_dir: str
):
    for fisc_dimen in get_fisc_dimens():
        save_table_to_csv(conn_or_cursor, fisc_mstr_dir, f"{fisc_dimen}_agg")


def etl_fisc_agg_tables_to_fisc_jsons(cursor: sqlite3_Cursor, fisc_mstr_dir: str):
    fisc_filename = "fisc.json"
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    insert_staging_sqlstr = """SELECT fisc_title FROM fiscunit_agg;"""
    cursor.execute(insert_staging_sqlstr)
    for fisc_title_set in cursor.fetchall():
        fisc_title = fisc_title_set[0]
        fisc_dict = get_fisc_dict_from_db(cursor, fisc_title)
        fiscunit_dir = create_path(fiscs_dir, fisc_title)
        save_json(fiscunit_dir, fisc_filename, fisc_dict)


def etl_event_bud_csvs_to_pack_json(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        fisc_path = create_path(fiscs_dir, fisc_title)
        owners_path = create_path(fisc_path, "owners")
        for owner_name in get_level1_dirs(owners_path):
            owner_path = create_path(owners_path, owner_name)
            events_path = create_path(owner_path, "events")
            for event_int in get_level1_dirs(events_path):
                event_path = create_path(events_path, event_int)
                event_pack = packunit_shop(
                    owner_name=owner_name,
                    face_name=None,
                    fisc_title=fisc_title,
                    event_int=event_int,
                )
                add_budatoms_from_csv(event_pack, event_path)
                save_file(event_path, "all_pack.json", event_pack.get_json())


def add_budatoms_from_csv(owner_pack: PackUnit, owner_path: str):
    idea_sqlite_types = get_idea_sqlite_types()
    bud_dimens = get_bud_dimens()
    bud_dimens.remove("budunit")
    for bud_dimen in bud_dimens:
        bud_dimen_put_csv = f"{bud_dimen}_put_agg.csv"
        bud_dimen_del_csv = f"{bud_dimen}_del_agg.csv"
        put_path = create_path(owner_path, bud_dimen_put_csv)
        del_path = create_path(owner_path, bud_dimen_del_csv)
        if os_path_exists(put_path):
            put_rows = open_csv_with_types(put_path, idea_sqlite_types)
            headers = put_rows.pop(0)
            for put_row in put_rows:
                x_atom = budatom_shop(bud_dimen, "INSERT")
                for col_name, row_value in zip(headers, put_row):
                    if col_name not in {
                        "face_name",
                        "event_int",
                        "fisc_title",
                        "owner_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                owner_pack._buddelta.set_budatom(x_atom)

        if os_path_exists(del_path):
            del_rows = open_csv_with_types(del_path, idea_sqlite_types)
            headers = del_rows.pop(0)
            for del_row in del_rows:
                x_atom = budatom_shop(bud_dimen, "DELETE")
                for col_name, row_value in zip(headers, del_row):
                    if col_name not in {
                        "face_name",
                        "event_int",
                        "fisc_title",
                        "owner_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                owner_pack._buddelta.set_budatom(x_atom)


def etl_event_pack_json_to_event_inherited_budunits(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        fisc_path = create_path(fiscs_dir, fisc_title)
        owners_dir = create_path(fisc_path, "owners")
        for owner_name in get_level1_dirs(owners_dir):
            owner_dir = create_path(owners_dir, owner_name)
            events_dir = create_path(owner_dir, "events")
            prev_event_int = None
            for event_int in get_level1_dirs(events_dir):
                prev_bud = _get_prev_event_int_budunit(
                    fisc_mstr_dir, fisc_title, owner_name, prev_event_int
                )
                budevent_path = create_budevent_path(
                    fisc_mstr_dir, fisc_title, owner_name, event_int
                )
                event_dir = create_owner_event_dir_path(
                    fisc_mstr_dir, fisc_title, owner_name, event_int
                )
                pack_path = create_path(event_dir, "all_pack.json")
                event_pack = get_packunit_from_json(open_file(pack_path))
                sift_delta = get_minimal_buddelta(event_pack._buddelta, prev_bud)
                curr_bud = event_pack.get_edited_bud(prev_bud)
                save_file(budevent_path, None, curr_bud.get_json())
                expressed_pack = copy_deepcopy(event_pack)
                expressed_pack.set_buddelta(sift_delta)
                save_file(event_dir, "expressed_pack.json", expressed_pack.get_json())
                prev_event_int = event_int


def _get_prev_event_int_budunit(
    fisc_mstr_dir, fisc_title, owner_name, prev_event_int
) -> BudUnit:
    if prev_event_int is None:
        return budunit_shop(owner_name, fisc_title)
    prev_budevent_path = create_budevent_path(
        fisc_mstr_dir, fisc_title, owner_name, prev_event_int
    )
    return open_bud_file(prev_budevent_path)


def etl_event_inherited_budunits_to_fisc_gut(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        owner_events = collect_owner_event_dir_sets(fisc_mstr_dir, fisc_title)
        owners_max_event_int_dict = get_owners_downhill_event_ints(owner_events)
        for owner_name, max_event_int in owners_max_event_int_dict.items():
            max_budevent_path = create_budevent_path(
                fisc_mstr_dir, fisc_title, owner_name, max_event_int
            )
            max_event_bud_json = open_file(max_budevent_path)
            gut_path = create_gut_path(fisc_mstr_dir, fisc_title, owner_name)
            save_file(gut_path, None, max_event_bud_json)


def etl_fisc_gut_to_fisc_plan(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        x_fiscunit = fiscunit_get_from_default_path(fisc_mstr_dir, fisc_title)
        x_fiscunit.generate_all_plans()


def etl_fisc_plan_jsons_to_fisc_db(
    conn_or_cursor: sqlite3_Connection, world_id: str, fisc_mstr_dir: str
):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        fisc_path = create_path(fiscs_dir, fisc_title)
        owners_dir = create_path(fisc_path, "owners")
        for owner_name in get_level1_dirs(owners_dir):
            plan_obj = open_plan_file(fisc_mstr_dir, fisc_title, owner_name)
            insert_plan_obj(conn_or_cursor, world_id, plan_obj)
