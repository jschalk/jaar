from src.f00_instrument.file import set_dir, create_path, count_dirs_files, delete_dir
from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_None,
    get_0_if_None,
    get_empty_set_if_None,
)
from src.f01_road.deal import TimeLinePoint, TimeConversion
from src.f01_road.road import (
    FaceName,
    EventInt,
    FiscTitle,
    WorldID,
    TimeLineTitle,
    get_default_world_id,
)
from src.f08_fisc.fisc import FiscUnit
from src.f11_etl.stance_tool import create_stance0001_file
from src.f11_etl.transformers import (
    etl_mine_to_cart_staging,
    etl_cart_staging_to_cart_agg,
    etl_cart_agg_to_cart_valid,
    etl_cart_agg_to_cart_events,
    etl_cart_events_to_events_log,
    etl_cart_pidgin_staging_to_agg,
    etl_cart_agg_to_pidgin_staging,
    etl_cart_events_log_to_events_agg,
    get_events_dict_from_events_agg_file,
    etl_cart_pidgin_agg_to_otz_face_dirs,
    etl_otz_face_pidgins_to_otz_event_pidgins,
    etl_otz_event_pidgins_to_otz_pidgin_csv_files,
    etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons,
    etl_pidgin_jsons_inherit_younger_pidgins,
    get_pidgin_events_by_dirs,
    etl_cart_ideas_to_otz_face_ideas,
    etl_otz_face_ideas_to_otz_event_otx_ideas,
    etl_otz_event_ideas_to_inx_events,
    etl_otz_inx_event_ideas_to_inz_faces,
    etl_inz_face_ideas_to_csv_files,
    etl_inz_face_csv_files2idea_staging_tables,
    etl_idea_staging_to_fisc_tables,
    etl_fisc_staging_tables_to_fisc_csvs,
    etl_fisc_agg_tables_to_fisc_csvs,
    etl_fisc_agg_tables_to_fisc_jsons,
    etl_idea_staging_to_bud_tables,
    etl_bud_tables_to_event_bud_csvs,
    etl_event_bud_csvs_to_kick_json,
    etl_event_kick_json_to_event_inherited_budunits,
    etl_event_inherited_budunits_to_fisc_voice,
    etl_fisc_voice_to_fisc_plan,
    etl_fisc_agg_tables2fisc_ote1_agg,
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
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection


def get_default_worlds_dir() -> str:
    return "src/f12_world/examples/worlds"


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    world_time_nigh: TimeLinePoint = None
    events: dict[EventInt, FaceName] = None
    timeconversions: dict[TimeLineTitle, TimeConversion] = None
    _faces_otz_dir: str = None
    _faces_inz_dir: str = None
    _world_dir: str = None
    _mine_dir: str = None
    _cart_dir: str = None
    _fisc_mstr_dir: str = None
    _fiscunits: set[FiscTitle] = None
    _pidgin_events: dict[FaceName, set[EventInt]] = None

    def set_event(self, event_int: EventInt, face_name: FaceName):
        self.events[event_int] = face_name

    def event_exists(self, event_int: EventInt) -> bool:
        return self.events.get(event_int) != None

    def get_event(self, event_int: EventInt) -> FaceName:
        return self.events.get(event_int)

    def legitimate_events(self) -> set[EventInt]:
        return set(self.events.keys())

    def _event_dir(self, face_name: FaceName, event_int: EventInt) -> str:
        face_dir = create_path(self._faces_otz_dir, face_name)
        return create_path(face_dir, event_int)

    def _set_pidgin_events(self):
        self._pidgin_events = get_pidgin_events_by_dirs(self._faces_otz_dir)

    def set_mine_dir(self, x_dir: str):
        self._mine_dir = x_dir
        set_dir(self._mine_dir)

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_id)
        self._faces_otz_dir = create_path(self._world_dir, "faces_otz")
        self._faces_inz_dir = create_path(self._world_dir, "faces_inz")
        self._cart_dir = create_path(self._world_dir, "cart")
        self._fisc_mstr_dir = create_path(self._world_dir, "fisc_mstr")
        set_dir(self._world_dir)
        set_dir(self._faces_otz_dir)
        set_dir(self._faces_inz_dir)
        set_dir(self._cart_dir)
        set_dir(self._fisc_mstr_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineTitle, TimeConversion]:
        return self.timeconversions

    def mine_to_cart_staging(self):
        etl_mine_to_cart_staging(self._mine_dir, self._cart_dir)

    def cart_staging_to_cart_agg(self):
        etl_cart_staging_to_cart_agg(self._cart_dir)

    def cart_agg_to_cart_valid(self):
        etl_cart_agg_to_cart_valid(self._cart_dir, self.legitimate_events())

    def cart_agg_to_cart_events(self):
        etl_cart_agg_to_cart_events(self._cart_dir)

    def cart_events_to_events_log(self):
        etl_cart_events_to_events_log(self._cart_dir)

    def cart_events_log_to_events_agg(self):
        etl_cart_events_log_to_events_agg(self._cart_dir)

    def set_events_from_events_agg_file(self):
        self.events = get_events_dict_from_events_agg_file(self._cart_dir)

    def cart_agg_to_pidgin_staging(self):
        etl_cart_agg_to_pidgin_staging(self.legitimate_events(), self._cart_dir)

    def cart_pidgin_staging_to_agg(self):
        etl_cart_pidgin_staging_to_agg(self._cart_dir)

    def cart_pidgin_agg_to_otz_face_dirs(self):
        etl_cart_pidgin_agg_to_otz_face_dirs(self._cart_dir, self._faces_otz_dir)

    def pidgin_jsons_inherit_younger_pidgins(self):
        etl_pidgin_jsons_inherit_younger_pidgins(
            self._faces_otz_dir, self._pidgin_events
        )

    def otz_face_pidgins_to_otz_event_pidgins(self):
        etl_otz_face_pidgins_to_otz_event_pidgins(self._faces_otz_dir)

    def otz_event_pidgins_to_otz_pidgin_csv_files(self):
        etl_otz_event_pidgins_to_otz_pidgin_csv_files(self._faces_otz_dir)

    def otz_event_pidgins_csvs_to_otz_pidgin_jsons(self):
        etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons(self._faces_otz_dir)
        self._set_pidgin_events()

    def cart_ideas_to_otz_face_ideas(self):
        etl_cart_ideas_to_otz_face_ideas(self._cart_dir, self._faces_otz_dir)

    def otz_face_ideas_to_otz_event_otx_ideas(self):
        etl_otz_face_ideas_to_otz_event_otx_ideas(self._faces_otz_dir)

    def otz_event_ideas_to_inx_events(self):
        etl_otz_event_ideas_to_inx_events(self._faces_otz_dir, self._pidgin_events)

    def otz_inx_event_ideas_to_inz_faces(self):
        etl_otz_inx_event_ideas_to_inz_faces(self._faces_otz_dir, self._faces_inz_dir)

    def inz_face_ideas_to_csv_files(self):
        etl_inz_face_ideas_to_csv_files(self._faces_inz_dir)

    def inz_face_csv_files2idea_staging_tables(
        self, conn_or_cursor: sqlite3_Connection
    ):
        etl_inz_face_csv_files2idea_staging_tables(conn_or_cursor, self._faces_inz_dir)

    def idea_staging_to_fisc_tables(self, conn_or_cursor: sqlite3_Connection):
        etl_idea_staging_to_fisc_tables(conn_or_cursor)

    def idea_staging_to_bud_tables(self, conn_or_cursor: sqlite3_Connection):
        etl_idea_staging_to_bud_tables(conn_or_cursor)

    def inz_faces_ideas_to_fisc_mstr_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_fisc_staging_tables_to_fisc_csvs(conn_or_cursor, self._fisc_mstr_dir)
        etl_fisc_agg_tables_to_fisc_csvs(conn_or_cursor, self._fisc_mstr_dir)

    def fisc_agg_tables_to_fisc_jsons(self, cursor: sqlite3_Connection):
        etl_fisc_agg_tables_to_fisc_jsons(cursor, self._fisc_mstr_dir)

    def fisc_agg_tables2fisc_ote1_agg(self, conn_or_cursor: sqlite3_Connection):
        etl_fisc_agg_tables2fisc_ote1_agg(conn_or_cursor)

    def fisc_table2fisc_ote1_agg_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_fisc_table2fisc_ote1_agg_csvs(conn_or_cursor, self._fisc_mstr_dir)

    def bud_tables_to_event_bud_csvs(self, conn_or_cursor: sqlite3_Connection):
        etl_bud_tables_to_event_bud_csvs(conn_or_cursor, self._fisc_mstr_dir)

    def event_bud_csvs_to_kick_json(self):
        etl_event_bud_csvs_to_kick_json(self._fisc_mstr_dir)

    def event_kick_json_to_event_inherited_budunits(self):
        etl_event_kick_json_to_event_inherited_budunits(self._fisc_mstr_dir)

    def event_inherited_budunits_to_fisc_voice(self):
        etl_event_inherited_budunits_to_fisc_voice(self._fisc_mstr_dir)

    def fisc_voice_to_fisc_plan(self):
        etl_fisc_voice_to_fisc_plan(self._fisc_mstr_dir)

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
        print(f"Starting files {count_dirs_files(mstr_dir)}")
        etl_create_deals_root_cells(mstr_dir)
        print(f"{count_dirs_files(mstr_dir)} etl_create_deals_root_cells")
        etl_create_fisc_cell_trees(mstr_dir)
        print(f"{count_dirs_files(mstr_dir)} etl_create_fisc_cell_trees")
        etl_set_cell_trees_found_facts(mstr_dir)
        print(f"{count_dirs_files(mstr_dir)} etl_set_cell_trees_found_facts")
        etl_set_cell_trees_decrees(mstr_dir)
        print(f"{count_dirs_files(mstr_dir)} etl_set_cell_trees_decrees")
        etl_set_cell_tree_cell_mandates(mstr_dir)
        print(f"{count_dirs_files(mstr_dir)} etl_set_cell_tree_cell_mandates")
        etl_create_deal_mandate_ledgers(mstr_dir)
        print(f"{count_dirs_files(mstr_dir)} etl_create_deal_mandate_ledgers")

    def mine_to_burdens(
        self, store_tracing_files: bool = False
    ):  # sourcery skip: extract-method
        fisc_mstr_dir = create_path(self._world_dir, "fisc_mstr")
        delete_dir(fisc_mstr_dir)
        print(f"{fisc_mstr_dir=}")
        set_dir(fisc_mstr_dir)

        # "mine_to_cart_staging step 00"),
        # "cart_staging_to_cart_agg step 01"),
        # "cart_agg_to_cart_events step 02"),
        # "cart_events_to_events_log step 02.1"),
        # "cart_events_log_to_events_agg step 02.2"),
        # "set_events_from_events_agg_file step 03"),
        # "cart_agg_to_pidgin_staging step 03.1"),
        # "cart_pidgin_staging_to_agg step 03.2"),
        # "cart_pidgin_agg_to_otz_face_dirs step 03.3"),
        # "otz_face_pidgins_to_otz_event_pidgins step 03.4"),
        # "otz_event_pidgins_csvs_to_otz_pidgin_jsons step 03.5"),
        # "pidgin_jsons_inherit_younger_pidgins step 04"),
        # "cart_agg_to_cart_valid step 04.1"),
        # "cart_ideas_to_otz_face_ideas step 04.2"),
        # "otz_face_ideas_to_otz_event_otx_ideas step 04.3"),
        # "otz_event_ideas_to_inx_events 04.4"),
        # "otz_inx_event_ideas_to_inz_faces 04.5"),
        # "inz_face_ideas_to_csv_files step 05"),

        mine_to_burdens_steps = [
            (self.mine_to_cart_staging, "step 00.0"),
            (self.cart_staging_to_cart_agg, "step 01.0"),
            (self.cart_agg_to_cart_events, "step 02.0"),
            (self.cart_events_to_events_log, "step 02.1"),
            (self.cart_events_log_to_events_agg, "step 02.2"),
            (self.set_events_from_events_agg_file, "step 03.0"),
            (self.cart_agg_to_pidgin_staging, "step 03.1"),
            (self.cart_pidgin_staging_to_agg, "step 03.2"),
            (self.cart_pidgin_agg_to_otz_face_dirs, "step 03.3"),
            (self.otz_face_pidgins_to_otz_event_pidgins, "step 03.4"),
            (self.otz_event_pidgins_csvs_to_otz_pidgin_jsons, "step 03.5"),
            (self.pidgin_jsons_inherit_younger_pidgins, "step 04.0"),
            (self.cart_agg_to_cart_valid, "step 04.1"),
            (self.cart_ideas_to_otz_face_ideas, "step 04.2"),
            (self.otz_face_ideas_to_otz_event_otx_ideas, "step 04.3"),
            (self.otz_event_ideas_to_inx_events, "step 04.4"),
            (self.otz_inx_event_ideas_to_inz_faces, "step 04.5"),
            (self.inz_face_ideas_to_csv_files, "step 05.0"),
        ]

        for etl_func, step_msg in mine_to_burdens_steps:
            # if step_msg:
            #     print(f"{step_msg} {count_dirs_files(self.worlds_dir)}")
            etl_func()

        with sqlite3_connect(":memory:") as fisc_db_conn:
            cursor = fisc_db_conn.cursor()
            self.inz_face_csv_files2idea_staging_tables(cursor)
            self.idea_staging_to_fisc_tables(cursor)
            print(f"step 05.1 {count_dirs_files(self.worlds_dir)}")
            # Save for reference, change be skipped
            if store_tracing_files:
                self.inz_faces_ideas_to_fisc_mstr_csvs(cursor)
            print(f"step 05.2 {count_dirs_files(self.worlds_dir)}")
            self.fisc_agg_tables_to_fisc_jsons(cursor)
            self.fisc_agg_tables2fisc_ote1_agg(cursor)
            self.fisc_table2fisc_ote1_agg_csvs(cursor)
            self.fisc_ote1_agg_csvs2jsons()
            print(f"step 06.0 {count_dirs_files(self.worlds_dir)}")
            self.idea_staging_to_bud_tables(cursor)
            self.bud_tables_to_event_bud_csvs(cursor)
        print(f"step 06.5 {count_dirs_files(self.worlds_dir)}")
        self.event_bud_csvs_to_kick_json()
        self.event_kick_json_to_event_inherited_budunits()
        print(f"step 07 {count_dirs_files(self.worlds_dir)}")
        self.event_inherited_budunits_to_fisc_voice()
        self.fisc_voice_to_fisc_plan()
        print(f"step 08 {count_dirs_files(self.worlds_dir)}")
        self.calc_fisc_deal_acct_mandate_net_ledgers()

    def create_stances(self):
        create_stance0001_file(self._fisc_mstr_dir)

    def get_dict(self) -> dict:
        return {
            "world_id": self.world_id,
            "world_time_nigh": self.world_time_nigh,
            "timeconversions": self.get_timeconversions_dict(),
            "events": self.events,
        }


def worldunit_shop(
    world_id: WorldID = None,
    worlds_dir: str = None,
    mine_dir: str = None,
    world_time_nigh: TimeLinePoint = None,
    timeconversions: dict[TimeLineTitle, TimeConversion] = None,
    _fiscunits: set[FiscTitle] = None,
) -> WorldUnit:
    if world_id is None:
        world_id = get_default_world_id()
    if worlds_dir is None:
        worlds_dir = get_default_worlds_dir()
    x_worldunit = WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        world_time_nigh=get_0_if_None(world_time_nigh),
        timeconversions=get_empty_dict_if_None(timeconversions),
        events={},
        _fiscunits=get_empty_set_if_None(_fiscunits),
        _mine_dir=mine_dir,
        _pidgin_events={},
    )
    x_worldunit._set_world_dirs()
    if not x_worldunit._mine_dir:
        x_worldunit.set_mine_dir(create_path(x_worldunit._world_dir, "mine"))
    return x_worldunit


def init_fiscunits_from_dirs(x_dirs: list[str]) -> list[FiscUnit]:
    return []
