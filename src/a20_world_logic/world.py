from dataclasses import dataclass
from os.path import exists as os_path_exists
from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.a00_data_toolbox.dict_toolbox import get_0_if_None, get_empty_set_if_None
from src.a00_data_toolbox.file_toolbox import create_path, delete_dir, set_dir
from src.a01_term_logic.term import CoinLabel, EventInt, FaceName
from src.a11_bud_logic.bud import TimeLinePoint
from src.a15_coin_logic.coin_main import CoinUnit
from src.a17_idea_logic.idea_db_tool import update_event_int_in_excel_files
from src.a18_etl_toolbox.a18_path import create_coin_mstr_path, create_world_db_path
from src.a18_etl_toolbox.stance_tool import create_stance0001_file
from src.a18_etl_toolbox.transformers import (
    add_coin_timeline_to_guts,
    create_last_run_metrics_json,
    etl_brick_agg_tables_to_brick_valid_tables,
    etl_brick_agg_tables_to_events_brick_agg_table,
    etl_brick_raw_tables_to_brick_agg_tables,
    etl_brick_valid_tables_to_sound_raw_tables,
    etl_coin_guts_to_coin_jobs,
    etl_coin_job_jsons_to_job_tables,
    etl_coin_json_partner_nets_to_coin_partner_nets_table,
    etl_coin_ote1_agg_csvs_to_jsons,
    etl_coin_ote1_agg_table_to_coin_ote1_agg_csvs,
    etl_create_bud_mandate_ledgers,
    etl_create_buds_root_cells,
    etl_create_coin_cell_trees,
    etl_event_believer_csvs_to_pack_json,
    etl_event_inherited_believerunits_to_coin_gut,
    etl_event_pack_json_to_event_inherited_believerunits,
    etl_events_brick_agg_table_to_events_brick_valid_table,
    etl_input_dfs_to_brick_raw_tables,
    etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables,
    etl_set_cell_tree_cell_mandates,
    etl_set_cell_trees_decrees,
    etl_set_cell_trees_found_facts,
    etl_sound_agg_tables_to_sound_vld_tables,
    etl_sound_raw_tables_to_sound_agg_tables,
    etl_sound_vld_tables_to_voice_raw_tables,
    etl_voice_agg_tables_to_coin_jsons,
    etl_voice_agg_to_event_believer_csvs,
    etl_voice_raw_tables_to_coin_ote1_agg,
    etl_voice_raw_tables_to_voice_agg_tables,
    get_max_brick_agg_event_int,
)
from src.a19_kpi_toolbox.kpi_mstr import (
    create_calendar_markdown_files,
    create_kpi_csvs,
    populate_kpi_bundle,
)


class WorldName(str):
    pass


@dataclass
class WorldUnit:
    world_name: WorldName = None
    worlds_dir: str = None
    output_dir: str = None
    world_time_reason_upper: TimeLinePoint = None
    _world_dir: str = None
    _input_dir: str = None
    _brick_dir: str = None
    _coin_mstr_dir: str = None
    _coinunits: set[CoinLabel] = None
    _events: dict[EventInt, FaceName] = None
    _pidgin_events: dict[FaceName, set[EventInt]] = None

    def get_world_db_path(self) -> str:
        "Returns path: world_dir/world.db"
        return create_world_db_path(self._world_dir)

    def delete_world_db(self):
        delete_dir(self.get_world_db_path())

    def set_event(self, event_int: EventInt, face_name: FaceName):
        self._events[event_int] = face_name

    def event_exists(self, event_int: EventInt) -> bool:
        return self._events.get(event_int) != None

    def get_event(self, event_int: EventInt) -> FaceName:
        return self._events.get(event_int)

    def set_input_dir(self, x_dir: str):
        self._input_dir = x_dir
        set_dir(self._input_dir)

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_name)
        self._brick_dir = create_path(self._world_dir, "brick")
        self._coin_mstr_dir = create_coin_mstr_path(self._world_dir)
        set_dir(self._world_dir)
        set_dir(self._brick_dir)
        set_dir(self._coin_mstr_dir)

    def calc_coin_bud_partner_mandate_net_ledgers(self):
        mstr_dir = self._coin_mstr_dir
        etl_create_buds_root_cells(mstr_dir)
        etl_create_coin_cell_trees(mstr_dir)
        etl_set_cell_trees_found_facts(mstr_dir)
        etl_set_cell_trees_decrees(mstr_dir)
        etl_set_cell_tree_cell_mandates(mstr_dir)
        etl_create_bud_mandate_ledgers(mstr_dir)

    def sheets_input_to_clarity_mstr(self):
        with sqlite3_connect(self.get_world_db_path()) as db_conn:
            cursor = db_conn.cursor()
            self.sheets_input_to_clarity_with_cursor(cursor)
            db_conn.commit()
        db_conn.close()

    def stance_sheets_to_clarity_mstr(self):
        max_brick_agg_event_int = 0
        if os_path_exists(self.get_world_db_path()):
            with sqlite3_connect(self.get_world_db_path()) as db_conn0:
                cursor0 = db_conn0.cursor()
                max_brick_agg_event_int = get_max_brick_agg_event_int(cursor0)
            db_conn0.close()
        next_event_int = max_brick_agg_event_int + 1
        update_event_int_in_excel_files(self._input_dir, next_event_int)
        self.sheets_input_to_clarity_mstr()
        delete_dir(self._input_dir)

    def sheets_input_to_clarity_with_cursor(self, cursor: sqlite3_Cursor):
        delete_dir(self._coin_mstr_dir)
        set_dir(self._coin_mstr_dir)
        # collect excel file data into central location
        etl_input_dfs_to_brick_raw_tables(cursor, self._input_dir)
        # brick raw to sound raw, check by event_ints
        etl_brick_raw_tables_to_brick_agg_tables(cursor)
        etl_brick_agg_tables_to_events_brick_agg_table(cursor)
        etl_events_brick_agg_table_to_events_brick_valid_table(cursor)
        etl_brick_agg_tables_to_brick_valid_tables(cursor)
        etl_brick_valid_tables_to_sound_raw_tables(cursor)
        # sound raw to voice raw, filter through pidgins
        etl_sound_raw_tables_to_sound_agg_tables(cursor)
        etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables(cursor)
        etl_sound_agg_tables_to_sound_vld_tables(cursor)
        etl_sound_vld_tables_to_voice_raw_tables(cursor)
        # voice raw to coin/believer jsons
        etl_voice_raw_tables_to_voice_agg_tables(cursor)
        etl_voice_agg_tables_to_coin_jsons(cursor, self._coin_mstr_dir)
        etl_voice_agg_to_event_believer_csvs(cursor, self._coin_mstr_dir)
        etl_event_believer_csvs_to_pack_json(self._coin_mstr_dir)
        etl_event_pack_json_to_event_inherited_believerunits(self._coin_mstr_dir)
        etl_event_inherited_believerunits_to_coin_gut(self._coin_mstr_dir)
        add_coin_timeline_to_guts(self._coin_mstr_dir)
        etl_coin_guts_to_coin_jobs(self._coin_mstr_dir)
        etl_voice_raw_tables_to_coin_ote1_agg(cursor)
        etl_coin_ote1_agg_table_to_coin_ote1_agg_csvs(cursor, self._coin_mstr_dir)
        etl_coin_ote1_agg_csvs_to_jsons(self._coin_mstr_dir)
        self.calc_coin_bud_partner_mandate_net_ledgers()
        etl_coin_job_jsons_to_job_tables(cursor, self._coin_mstr_dir)
        etl_coin_json_partner_nets_to_coin_partner_nets_table(
            cursor, self._coin_mstr_dir
        )
        populate_kpi_bundle(cursor)
        create_last_run_metrics_json(cursor, self._coin_mstr_dir)

        # # create all coin_job and mandate reports
        # self.calc_coin_bud_partner_mandate_net_ledgers()

        # if store_tracing_files:

    def create_stances(self, prettify_excel_bool=True):
        # TODO why is create_stance0001_file not drawing from world db instead of files?
        # it should be the database because that's the end of the core pipeline so it should
        # be the source of truth.
        create_stance0001_file(
            self._world_dir, self.output_dir, self.world_name, prettify_excel_bool
        )
        create_calendar_markdown_files(self._coin_mstr_dir, self.output_dir)

    def create_kpi_csvs(self):
        create_kpi_csvs(self.get_world_db_path(), self.output_dir)

    def to_dict(self) -> dict:
        return {
            "world_name": self.world_name,
            "world_time_reason_upper": self.world_time_reason_upper,
        }


def worldunit_shop(
    world_name: WorldName,
    worlds_dir: str,
    output_dir: str = None,
    input_dir: str = None,
    world_time_reason_upper: TimeLinePoint = None,
    _coinunits: set[CoinLabel] = None,
) -> WorldUnit:
    x_worldunit = WorldUnit(
        world_name=world_name,
        worlds_dir=worlds_dir,
        output_dir=output_dir,
        world_time_reason_upper=get_0_if_None(world_time_reason_upper),
        _events={},
        _coinunits=get_empty_set_if_None(_coinunits),
        _input_dir=input_dir,
        _pidgin_events={},
    )
    x_worldunit._set_world_dirs()
    if not x_worldunit._input_dir:
        x_worldunit.set_input_dir(create_path(x_worldunit._world_dir, "input"))
    return x_worldunit


def init_coinunits_from_dirs(x_dirs: list[str]) -> list[CoinUnit]:
    return []
