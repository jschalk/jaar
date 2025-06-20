from dataclasses import dataclass
from sqlite3 import (
    Connection as sqlite3_Connection,
    Cursor as sqlite3_Cursor,
    connect as sqlite3_connect,
)
from src.a00_data_toolbox.dict_toolbox import get_0_if_None, get_empty_set_if_None
from src.a00_data_toolbox.file_toolbox import create_path, delete_dir, set_dir
from src.a01_term_logic.term import EventInt, FaceName, VowLabel
from src.a02_finance_logic.bud import TimeLinePoint
from src.a15_vow_logic.vow import VowUnit
from src.a18_etl_toolbox.stance_tool import create_stance0001_file
from src.a18_etl_toolbox.transformers import (
    etl_brick_agg_tables_to_brick_valid_tables,
    etl_brick_raw_tables_to_brick_agg_tables,
    etl_brick_raw_tables_to_events_brick_agg_table,
    etl_brick_valid_tables_to_sound_raw_tables,
    etl_create_bud_mandate_ledgers,
    etl_create_buds_root_cells,
    etl_create_vow_cell_trees,
    etl_event_inherited_planunits_to_vow_gut,
    etl_event_pack_json_to_event_inherited_planunits,
    etl_event_plan_csvs_to_pack_json,
    etl_events_brick_agg_table_to_events_brick_valid_table,
    etl_mud_dfs_to_brick_raw_tables,
    etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables,
    etl_set_cell_tree_cell_mandates,
    etl_set_cell_trees_decrees,
    etl_set_cell_trees_found_facts,
    etl_sound_agg_tables_to_sound_vld_tables,
    etl_sound_raw_tables_to_sound_agg_tables,
    etl_sound_vld_tables_to_voice_raw_tables,
    etl_voice_agg_tables_to_vow_jsons,
    etl_voice_agg_to_event_plan_csvs,
    etl_voice_raw_tables_to_voice_agg_tables,
    etl_voice_raw_tables_to_vow_ote1_agg,
    etl_vow_guts_to_vow_jobs,
    etl_vow_job_jsons_to_job_tables,
    etl_vow_json_acct_nets_to_vow_acct_nets_table,
    etl_vow_ote1_agg_csvs_to_jsons,
    etl_vow_ote1_agg_table_to_vow_ote1_agg_csvs,
    get_pidgin_events_by_dirs,
)
from src.a19_kpi_toolbox.kpi_mstr import create_kpi_csvs, populate_kpi_bundle


class WorldID(str):
    pass


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    output_dir: str = None
    world_time_pnigh: TimeLinePoint = None
    _syntax_otz_dir: str = None
    _world_dir: str = None
    _mud_dir: str = None
    _brick_dir: str = None
    _vow_mstr_dir: str = None
    _vowunits: set[VowLabel] = None
    _events: dict[EventInt, FaceName] = None
    _pidgin_events: dict[FaceName, set[EventInt]] = None

    def get_db_path(self) -> str:
        return create_path(self._world_dir, "world.db")

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
        self._vow_mstr_dir = create_path(self._world_dir, "vow_mstr")
        set_dir(self._world_dir)
        set_dir(self._syntax_otz_dir)
        set_dir(self._brick_dir)
        set_dir(self._vow_mstr_dir)

    def mud_dfs_to_brick_raw_tables(self, conn: sqlite3_Connection):
        etl_mud_dfs_to_brick_raw_tables(conn, self._mud_dir)

    def event_pack_json_to_event_inherited_planunits(self):
        etl_event_pack_json_to_event_inherited_planunits(self._vow_mstr_dir)

    def calc_vow_bud_acct_mandate_net_ledgers(self):
        mstr_dir = self._vow_mstr_dir
        etl_create_buds_root_cells(mstr_dir)
        etl_create_vow_cell_trees(mstr_dir)
        etl_set_cell_trees_found_facts(mstr_dir)
        etl_set_cell_trees_decrees(mstr_dir)
        etl_set_cell_tree_cell_mandates(mstr_dir)
        etl_create_bud_mandate_ledgers(mstr_dir)

    def mud_to_clarity_mstr(self, store_tracing_files: bool = False):
        with sqlite3_connect(self.get_db_path()) as db_conn:
            cursor = db_conn.cursor()
            self.mud_to_clarity_with_cursor(db_conn, cursor, store_tracing_files)
            db_conn.commit()

    def mud_to_clarity_with_cursor(
        self,
        db_conn: sqlite3_Connection,
        cursor: sqlite3_Cursor,
        store_tracing_files: bool = False,
    ):
        delete_dir(self._vow_mstr_dir)
        set_dir(self._vow_mstr_dir)
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
        # voice raw to vow/plan jsons
        etl_voice_raw_tables_to_voice_agg_tables(cursor)
        etl_voice_agg_tables_to_vow_jsons(cursor, self._vow_mstr_dir)
        etl_voice_agg_to_event_plan_csvs(cursor, self._vow_mstr_dir)
        etl_event_plan_csvs_to_pack_json(self._vow_mstr_dir)
        etl_event_pack_json_to_event_inherited_planunits(self._vow_mstr_dir)
        etl_event_inherited_planunits_to_vow_gut(self._vow_mstr_dir)
        etl_vow_guts_to_vow_jobs(self._vow_mstr_dir)
        etl_voice_raw_tables_to_vow_ote1_agg(cursor)
        etl_vow_ote1_agg_table_to_vow_ote1_agg_csvs(cursor, self._vow_mstr_dir)
        etl_vow_ote1_agg_csvs_to_jsons(self._vow_mstr_dir)
        self.calc_vow_bud_acct_mandate_net_ledgers()
        etl_vow_job_jsons_to_job_tables(cursor, self._vow_mstr_dir)
        etl_vow_json_acct_nets_to_vow_acct_nets_table(cursor, self._vow_mstr_dir)
        populate_kpi_bundle(cursor)

        # # create all vow_job and mandate reports
        # self.calc_vow_bud_acct_mandate_net_ledgers()

        # if store_tracing_files:

    def create_stances(self):
        create_stance0001_file(self._vow_mstr_dir)

    def create_kpi_csvs(self):
        create_kpi_csvs(self.get_db_path(), self.output_dir)

    def get_dict(self) -> dict:
        return {
            "world_id": self.world_id,
            "world_time_pnigh": self.world_time_pnigh,
        }


def worldunit_shop(
    world_id: WorldID,
    worlds_dir: str,
    output_dir: str = None,
    mud_dir: str = None,
    world_time_pnigh: TimeLinePoint = None,
    _vowunits: set[VowLabel] = None,
) -> WorldUnit:
    x_worldunit = WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        output_dir=output_dir,
        world_time_pnigh=get_0_if_None(world_time_pnigh),
        _events={},
        _vowunits=get_empty_set_if_None(_vowunits),
        _mud_dir=mud_dir,
        _pidgin_events={},
    )
    x_worldunit._set_world_dirs()
    if not x_worldunit._mud_dir:
        x_worldunit.set_mud_dir(create_path(x_worldunit._world_dir, "mud"))
    return x_worldunit


def init_vowunits_from_dirs(x_dirs: list[str]) -> list[VowUnit]:
    return []
