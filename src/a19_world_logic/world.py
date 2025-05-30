from dataclasses import dataclass
from sqlite3 import Connection as sqlite3_Connection
from sqlite3 import Cursor as sqlite3_Cursor
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_empty_set_if_None,
)
from src.a00_data_toolbox.file_toolbox import create_path, delete_dir, set_dir
from src.a01_term_logic.way import EventInt, FaceName, FiscLabel, WorldID
from src.a02_finance_logic.deal import TimeConversion, TimeLinePoint
from src.a07_calendar_logic.chrono import TimeLineLabel
from src.a15_fisc_logic.fisc import FiscUnit
from src.a18_etl_toolbox.stance_tool import create_stance0001_file
from src.a18_etl_toolbox.transformers import (
    etl_brick_agg_tables_to_brick_valid_tables,
    etl_brick_raw_tables_to_brick_agg_tables,
    etl_brick_raw_tables_to_events_brick_agg_table,
    etl_brick_valid_tables_to_sound_raw_tables,
    etl_create_deal_mandate_ledgers,
    etl_create_deals_root_cells,
    etl_create_fisc_cell_trees,
    etl_event_bud_csvs_to_pack_json,
    etl_event_inherited_budunits_to_fisc_gut,
    etl_event_pack_json_to_event_inherited_budunits,
    etl_events_brick_agg_table_to_events_brick_valid_table,
    etl_fisc_guts_to_fisc_jobs,
    etl_fisc_job_jsons_to_job_tables,
    etl_fisc_ote1_agg_csvs_to_jsons,
    etl_fisc_ote1_agg_table_to_fisc_ote1_agg_csvs,
    etl_mud_dfs_to_brick_raw_tables,
    etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables,
    etl_set_cell_tree_cell_mandates,
    etl_set_cell_trees_decrees,
    etl_set_cell_trees_found_facts,
    etl_sound_agg_tables_to_sound_vld_tables,
    etl_sound_raw_tables_to_sound_agg_tables,
    etl_sound_vld_tables_to_voice_raw_tables,
    etl_voice_agg_tables_to_fisc_jsons,
    etl_voice_agg_to_event_bud_csvs,
    etl_voice_raw_tables_to_fisc_ote1_agg,
    etl_voice_raw_tables_to_voice_agg_tables,
    get_pidgin_events_by_dirs,
)


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    world_time_pnigh: TimeLinePoint = None
    timeconversions: dict[TimeLineLabel, TimeConversion] = None
    _syntax_otz_dir: str = None
    _world_dir: str = None
    _mud_dir: str = None
    _brick_dir: str = None
    _fisc_mstr_dir: str = None
    _fiscunits: set[FiscLabel] = None
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
        self._brick_dir = create_path(self._world_dir, "brick")
        self._fisc_mstr_dir = create_path(self._world_dir, "fisc_mstr")
        set_dir(self._world_dir)
        set_dir(self._syntax_otz_dir)
        set_dir(self._brick_dir)
        set_dir(self._fisc_mstr_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineLabel, TimeConversion]:
        return self.timeconversions

    def mud_dfs_to_brick_raw_tables(self, conn: sqlite3_Connection):
        etl_mud_dfs_to_brick_raw_tables(conn, self._mud_dir)

    def event_pack_json_to_event_inherited_budunits(self):
        etl_event_pack_json_to_event_inherited_budunits(self._fisc_mstr_dir)

    def calc_fisc_deal_acct_mandate_net_ledgers(self):
        mstr_dir = self._fisc_mstr_dir
        etl_create_deals_root_cells(mstr_dir)
        etl_create_fisc_cell_trees(mstr_dir)
        etl_set_cell_trees_found_facts(mstr_dir)
        etl_set_cell_trees_decrees(mstr_dir)
        etl_set_cell_tree_cell_mandates(mstr_dir)
        etl_create_deal_mandate_ledgers(mstr_dir)

    def mud_to_clarity(self, store_tracing_files: bool = False):
        with sqlite3_connect(":memory:") as db_conn:
            cursor = db_conn.cursor()
            self.mud_to_clarity_with_cursor(db_conn, cursor, store_tracing_files)

    def mud_to_clarity_with_cursor(
        self,
        db_conn: sqlite3_Connection,
        cursor: sqlite3_Cursor,
        store_tracing_files: bool = False,
    ):
        fisc_mstr_dir = create_path(self._world_dir, "fisc_mstr")
        delete_dir(fisc_mstr_dir)
        set_dir(fisc_mstr_dir)
        # collect excel file data into central location
        etl_mud_dfs_to_brick_raw_tables(db_conn, self._mud_dir)
        # brick raw to sound raw, check by event_ints
        etl_brick_raw_tables_to_brick_agg_tables(cursor)
        etl_brick_raw_tables_to_events_brick_agg_table(cursor)
        etl_events_brick_agg_table_to_events_brick_valid_table(cursor)
        etl_brick_agg_tables_to_brick_valid_tables(cursor)
        etl_brick_valid_tables_to_sound_raw_tables(cursor)
        # sound raw to voice raw, filter through pidgins
        etl_sound_raw_tables_to_sound_agg_tables(cursor)
        etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables(cursor)
        etl_sound_agg_tables_to_sound_vld_tables(cursor)
        etl_sound_vld_tables_to_voice_raw_tables(cursor)
        # voice raw to fisc/bud jsons
        etl_voice_raw_tables_to_voice_agg_tables(cursor)
        etl_voice_agg_tables_to_fisc_jsons(cursor, self._fisc_mstr_dir)
        etl_voice_agg_to_event_bud_csvs(cursor, self._fisc_mstr_dir)
        etl_event_bud_csvs_to_pack_json(self._fisc_mstr_dir)
        etl_event_pack_json_to_event_inherited_budunits(self._fisc_mstr_dir)
        etl_event_inherited_budunits_to_fisc_gut(self._fisc_mstr_dir)
        etl_fisc_guts_to_fisc_jobs(self._fisc_mstr_dir)
        etl_voice_raw_tables_to_fisc_ote1_agg(cursor)
        etl_fisc_ote1_agg_table_to_fisc_ote1_agg_csvs(cursor, self._fisc_mstr_dir)
        etl_fisc_ote1_agg_csvs_to_jsons(self._fisc_mstr_dir)
        self.calc_fisc_deal_acct_mandate_net_ledgers()
        etl_fisc_job_jsons_to_job_tables(cursor, self._fisc_mstr_dir)

        # # create all fisc_job and mandate reports
        # self.calc_fisc_deal_acct_mandate_net_ledgers()

        # if store_tracing_files:

    def create_stances(self):
        create_stance0001_file(self._fisc_mstr_dir)

    def get_dict(self) -> dict:
        return {
            "world_id": self.world_id,
            "world_time_pnigh": self.world_time_pnigh,
            "timeconversions": self.get_timeconversions_dict(),
        }


def worldunit_shop(
    world_id: WorldID,
    worlds_dir: str,
    mud_dir: str = None,
    world_time_pnigh: TimeLinePoint = None,
    timeconversions: dict[TimeLineLabel, TimeConversion] = None,
    _fiscunits: set[FiscLabel] = None,
) -> WorldUnit:
    x_worldunit = WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        world_time_pnigh=get_0_if_None(world_time_pnigh),
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
