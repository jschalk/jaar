from src.a00_data_toolbox.file_toolbox import set_dir, create_path, delete_dir
from src.a00_data_toolbox.dict_toolbox import (
    get_empty_dict_if_None,
    get_0_if_None,
    get_empty_set_if_None,
)
from src.a02_finance_logic.deal import TimeLinePoint, TimeConversion
from src.a01_word_logic.road import (
    FaceName,
    EventInt,
    FiscTag,
    WorldID,
    TimeLineTag,
)
from src.a15_fisc_logic.fisc import FiscUnit
from src.a18_etl_toolbox.stance_tool import create_stance0001_file
from src.a18_etl_toolbox.transformers import (
    etl_mud_df_to_yell_raw_db,
    etl_yell_raw_db_to_yell_agg_db,
    etl_yell_raw_db_to_yell_raw_df,
    etl_yell_agg_db_to_yell_agg_df,
    etl_yell_raw_db_to_yell_agg_events_db,
    etl_yell_agg_events_db_to_yell_valid_events_db,
    etl_yell_agg_events_db_to_event_dict,
    etl_yell_agg_non_pidgin_ideas_to_yell_valid,
    etl_yell_pidgin_raw_df_to_pidgin_agg_df,
    etl_yell_agg_df_to_yell_pidgin_raw_df,
    etl_yell_pidgin_agg_df_to_otz_face_pidgin_agg_df,
    etl_otz_face_pidgins_df_to_otz_event_pidgins_df,
    etl_otz_event_pidgins_to_otz_pidgin_csv_files,
    etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons,
    etl_pidgin_jsons_inherit_younger_pidgins,
    get_pidgin_events_by_dirs,
    etl_yell_ideas_to_otz_face_ideas,
    etl_otz_face_ideas_to_otz_event_otx_ideas,
    etl_otz_event_ideas_to_inz_events,
    etl_otz_inx_event_ideas_to_inz_faces,
    etl_inz_face_ideas_to_csv_files,
    etl_inz_face_csv_files2idea_raw_tables,
    etl_idea_raw_to_fisc_prime_tables,
    etl_fisc_raw_tables_to_fisc_csvs,
    etl_fisc_agg_tables_to_fisc_csvs,
    etl_fisc_agg_tables_to_fisc_jsons,
    etl_idea_raw_to_bud_prime_tables,
    etl_bud_tables_to_event_bud_csvs,
    etl_event_bud_csvs_to_pack_json,
    etl_event_pack_json_to_event_inherited_budunits,
    etl_event_inherited_budunits_to_fisc_gut,
    etl_fisc_gut_to_fisc_job,
    etl_fisc_agg_tables_to_fisc_ote1_agg,
    etl_fisc_table2fisc_ote1_agg_csvs,
    etl_fisc_ote1_agg_csvs2jsons,
    etl_create_deals_root_cells,
    etl_create_fisc_cell_trees,
    etl_set_cell_trees_found_facts,
    etl_set_cell_trees_decrees,
    etl_set_cell_tree_cell_mandates,
    etl_create_deal_mandate_ledgers,
)
from dataclasses import dataclass
from sqlite3 import (
    connect as sqlite3_connect,
    Connection as sqlite3_Connection,
    Cursor as sqlite3_Cursor,
)


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    world_time_nigh: TimeLinePoint = None
    timeconversions: dict[TimeLineTag, TimeConversion] = None
    _syntax_otz_dir: str = None
    _syntax_inz_dir: str = None
    _world_dir: str = None
    _mud_dir: str = None
    _yell_dir: str = None
    _fisc_mstr_dir: str = None
    _fiscunits: set[FiscTag] = None
    _events: dict[EventInt, FaceName] = None
    _pidgin_events: dict[FaceName, set[EventInt]] = None

    def set_event(self, event_int: EventInt, face_name: FaceName):
        self._events[event_int] = face_name

    def event_exists(self, event_int: EventInt) -> bool:
        return self._events.get(event_int) != None

    def get_event(self, event_int: EventInt) -> FaceName:
        return self._events.get(event_int)

    def _event_dir(self, face_name: FaceName, event_int: EventInt) -> str:
        face_dir = create_path(self._syntax_otz_dir, face_name)
        return create_path(face_dir, event_int)

    def _set_pidgin_events(self):
        self._pidgin_events = get_pidgin_events_by_dirs(self._syntax_otz_dir)

    def set_mud_dir(self, x_dir: str):
        self._mud_dir = x_dir
        set_dir(self._mud_dir)

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_id)
        self._syntax_otz_dir = create_path(self._world_dir, "syntax_otz")
        self._syntax_inz_dir = create_path(self._world_dir, "syntax_inz")
        self._yell_dir = create_path(self._world_dir, "yell")
        self._fisc_mstr_dir = create_path(self._world_dir, "fisc_mstr")
        set_dir(self._world_dir)
        set_dir(self._syntax_otz_dir)
        set_dir(self._syntax_inz_dir)
        set_dir(self._yell_dir)
        set_dir(self._fisc_mstr_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineTag, TimeConversion]:
        return self.timeconversions

    def mud_df_to_yell_raw_db(self, conn: sqlite3_Connection):
        etl_mud_df_to_yell_raw_db(conn, self._mud_dir)

    def yell_raw_db_to_yell_agg_df(
        self, conn: sqlite3_Connection, cursor: sqlite3_Cursor
    ):
        etl_yell_raw_db_to_yell_agg_db(cursor)
        etl_yell_agg_db_to_yell_agg_df(conn, self._yell_dir)

    def yell_agg_non_pidgin_ideas_to_yell_valid(self):
        etl_yell_agg_non_pidgin_ideas_to_yell_valid(
            self._yell_dir, set(self._events.keys())
        )

    def yell_agg_df_to_yell_pidgin_raw_df(self):
        etl_yell_agg_df_to_yell_pidgin_raw_df(set(self._events.keys()), self._yell_dir)

    def yell_pidgin_raw_df_to_pidgin_agg_df(self):
        etl_yell_pidgin_raw_df_to_pidgin_agg_df(self._yell_dir)

    def yell_pidgin_agg_df_to_otz_face_pidgin_agg_df(self):
        etl_yell_pidgin_agg_df_to_otz_face_pidgin_agg_df(
            self._yell_dir, self._syntax_otz_dir
        )

    def pidgin_jsons_inherit_younger_pidgins(self):
        etl_pidgin_jsons_inherit_younger_pidgins(
            self._syntax_otz_dir, self._pidgin_events
        )

    def otz_face_pidgins_df_to_otz_event_pidgins_df(self):
        etl_otz_face_pidgins_df_to_otz_event_pidgins_df(self._syntax_otz_dir)

    def otz_event_pidgins_to_otz_pidgin_csv_files(self):
        etl_otz_event_pidgins_to_otz_pidgin_csv_files(self._syntax_otz_dir)

    def otz_event_pidgins_csvs_to_otz_pidgin_jsons(self):
        etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons(self._syntax_otz_dir)
        self._set_pidgin_events()

    def yell_ideas_to_otz_face_ideas(self):
        etl_yell_ideas_to_otz_face_ideas(self._yell_dir, self._syntax_otz_dir)

    def otz_face_ideas_to_otz_event_otx_ideas(self):
        etl_otz_face_ideas_to_otz_event_otx_ideas(self._syntax_otz_dir)

    def otz_event_ideas_to_inz_events(self):
        etl_otz_event_ideas_to_inz_events(self._syntax_otz_dir, self._pidgin_events)

    def otz_inx_event_ideas_to_inz_faces(self):
        etl_otz_inx_event_ideas_to_inz_faces(self._syntax_otz_dir, self._syntax_inz_dir)

    def inz_face_ideas_to_csv_files(self):
        etl_inz_face_ideas_to_csv_files(self._syntax_inz_dir)

    def inz_face_csv_files2idea_raw_tables(self, conn_or_cursor: sqlite3_Connection):
        etl_inz_face_csv_files2idea_raw_tables(conn_or_cursor, self._syntax_inz_dir)

    def idea_raw_to_fisc_prime_tables(self, conn_or_cursor: sqlite3_Connection):
        etl_idea_raw_to_fisc_prime_tables(conn_or_cursor)

    def idea_raw_to_bud_prime_tables(self, conn_or_cursor: sqlite3_Connection):
        etl_idea_raw_to_bud_prime_tables(conn_or_cursor)

    def inz_faces_ideas_to_fisc_mstr_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_fisc_raw_tables_to_fisc_csvs(conn_or_cursor, self._fisc_mstr_dir)
        etl_fisc_agg_tables_to_fisc_csvs(conn_or_cursor, self._fisc_mstr_dir)

    def fisc_agg_tables_to_fisc_jsons(self, cursor: sqlite3_Connection):
        etl_fisc_agg_tables_to_fisc_jsons(cursor, self._fisc_mstr_dir)

    def fisc_agg_tables_to_fisc_ote1_agg(self, conn_or_cursor: sqlite3_Connection):
        etl_fisc_agg_tables_to_fisc_ote1_agg(conn_or_cursor)

    def fisc_table2fisc_ote1_agg_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_fisc_table2fisc_ote1_agg_csvs(conn_or_cursor, self._fisc_mstr_dir)

    def bud_tables_to_event_bud_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_bud_tables_to_event_bud_csvs(conn_or_cursor, self._fisc_mstr_dir)

    def event_bud_csvs_to_pack_json(self):
        etl_event_bud_csvs_to_pack_json(self._fisc_mstr_dir)

    def event_pack_json_to_event_inherited_budunits(self):
        etl_event_pack_json_to_event_inherited_budunits(self._fisc_mstr_dir)

    def event_inherited_budunits_to_fisc_gut(self):
        etl_event_inherited_budunits_to_fisc_gut(self._fisc_mstr_dir)

    def fisc_gut_to_fisc_job(self):
        etl_fisc_gut_to_fisc_job(self._fisc_mstr_dir)

    def fisc_ote1_agg_csvs2jsons(self):
        etl_fisc_ote1_agg_csvs2jsons(self._fisc_mstr_dir)

    def create_deals_root_cells(self):
        etl_create_deals_root_cells(self._fisc_mstr_dir)

    def create_fisc_cell_trees(self):
        etl_create_fisc_cell_trees(self._fisc_mstr_dir)

    def set_cell_trees_found_facts(self):
        etl_set_cell_trees_found_facts(self._fisc_mstr_dir)

    def set_cell_trees_decrees(self):
        etl_set_cell_trees_decrees(self._fisc_mstr_dir)

    def set_cell_tree_cell_mandates(self):
        etl_set_cell_tree_cell_mandates(self._fisc_mstr_dir)

    def create_deal_mandate_ledgers(self):
        etl_create_deal_mandate_ledgers(self._fisc_mstr_dir)

    def calc_fisc_deal_acct_mandate_net_ledgers(self):
        mstr_dir = self._fisc_mstr_dir
        etl_create_deals_root_cells(mstr_dir)
        etl_create_fisc_cell_trees(mstr_dir)
        etl_set_cell_trees_found_facts(mstr_dir)
        etl_set_cell_trees_decrees(mstr_dir)
        etl_set_cell_tree_cell_mandates(mstr_dir)
        etl_create_deal_mandate_ledgers(mstr_dir)

    def mud_to_standings(
        self, store_tracing_files: bool = False
    ):  # sourcery skip: extract-method
        fisc_mstr_dir = create_path(self._world_dir, "fisc_mstr")
        delete_dir(fisc_mstr_dir)
        set_dir(fisc_mstr_dir)

        with sqlite3_connect(":memory:") as db_conn:
            cursor = db_conn.cursor()

            # collect excel file data into central location
            # grab all excel sheets that fit idea format
            self.mud_df_to_yell_raw_db(db_conn)
            # per idea filter to only non-conflicting idea data
            self.yell_raw_db_to_yell_agg_df(db_conn, cursor)

            # identify all idea data that has conflicting face_name/event_int uniqueness
            etl_yell_raw_db_to_yell_agg_events_db(cursor)
            etl_yell_agg_events_db_to_yell_valid_events_db(cursor)
            self._events = etl_yell_agg_events_db_to_event_dict(cursor)

            # build pidgins
            # collect all pidgin data from all relevant valid ideas
            self.yell_agg_df_to_yell_pidgin_raw_df()  # self._events.keys()
            # per pidgin dimen filter to only non-conflicting pidgin data
            self.yell_pidgin_raw_df_to_pidgin_agg_df()
            self.yell_pidgin_agg_df_to_otz_face_pidgin_agg_df()
            self.otz_face_pidgins_df_to_otz_event_pidgins_df()
            # per event create isolated pidgin.json
            self.otz_event_pidgins_csvs_to_otz_pidgin_jsons()  # self._pidgin_events
            # per event create complete (inherited) pidgin.json
            self.pidgin_jsons_inherit_younger_pidgins()  # self._pidgin_events

            # pidgins translate all fisc&bud ideas
            self.yell_agg_non_pidgin_ideas_to_yell_valid()  # self._events.keys()
            self.yell_ideas_to_otz_face_ideas()
            self.otz_face_ideas_to_otz_event_otx_ideas()
            self.otz_event_ideas_to_inz_events()  # self._pidgin_events
            self.otz_inx_event_ideas_to_inz_faces()
            self.inz_face_ideas_to_csv_files()
            self.inz_face_csv_files2idea_raw_tables(cursor)

            # create fiscunits
            self.idea_raw_to_fisc_prime_tables(cursor)
            self.fisc_agg_tables_to_fisc_jsons(cursor)
            self.fisc_agg_tables_to_fisc_ote1_agg(cursor)
            self.fisc_table2fisc_ote1_agg_csvs(cursor)
            self.fisc_ote1_agg_csvs2jsons()

            # create budunits
            self.idea_raw_to_bud_prime_tables(cursor)
            self.bud_tables_to_event_bud_csvs(cursor)
            self.event_bud_csvs_to_pack_json()
            self.event_pack_json_to_event_inherited_budunits()
            self.event_inherited_budunits_to_fisc_gut()

            # create all fisc_job and mandate reports
            self.fisc_gut_to_fisc_job()
            self.calc_fisc_deal_acct_mandate_net_ledgers()

            if store_tracing_files:
                etl_yell_raw_db_to_yell_raw_df(db_conn, self._yell_dir)
                # etl_yell_agg_db_to_yell_agg_df(db_conn, self._yell_dir)
                self.inz_faces_ideas_to_fisc_mstr_csvs(cursor)

    def create_stances(self):
        create_stance0001_file(self._fisc_mstr_dir)

    def get_dict(self) -> dict:
        return {
            "world_id": self.world_id,
            "world_time_nigh": self.world_time_nigh,
            "timeconversions": self.get_timeconversions_dict(),
        }


def worldunit_shop(
    world_id: WorldID,
    worlds_dir: str,
    mud_dir: str = None,
    world_time_nigh: TimeLinePoint = None,
    timeconversions: dict[TimeLineTag, TimeConversion] = None,
    _fiscunits: set[FiscTag] = None,
) -> WorldUnit:
    x_worldunit = WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        world_time_nigh=get_0_if_None(world_time_nigh),
        timeconversions=get_empty_dict_if_None(timeconversions),
        _events={},
        _fiscunits=get_empty_set_if_None(_fiscunits),
        _mud_dir=mud_dir,
        _pidgin_events={},
    )
    x_worldunit._set_world_dirs()
    if not x_worldunit._mud_dir:
        x_worldunit.set_mud_dir(create_path(x_worldunit._world_dir, "mud"))
    return x_worldunit


def init_fiscunits_from_dirs(x_dirs: list[str]) -> list[FiscUnit]:
    return []
