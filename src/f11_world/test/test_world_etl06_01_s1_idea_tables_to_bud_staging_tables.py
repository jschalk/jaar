from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.db_toolbox import db_table_exists, get_row_count
from src.f02_bud.bud_tool import budunit_str, bud_acct_membership_str
from src.f04_gift.atom_config import (
    face_name_str,
    acct_name_str,
    owner_name_str,
    get_bud_categorys,
    fiscal_title_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection


def get_existing_bud_x_tables(cursor: sqlite3_Connection, ending: str) -> set:
    return {
        bud_category
        for bud_category in get_bud_categorys()
        if db_table_exists(cursor, f"{bud_category}{ending}")
    }


def test_WorldUnit_idea_staging_to_fiscal_tables_CreatesFiscalStagingTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        assert len(get_existing_bud_x_tables(cursor, "_staging")) == 0
        assert len(get_existing_bud_x_tables(cursor, "_agg")) == 0

        # WHEN
        fizz_world.idea_staging_to_bud_tables(cursor)

        # THEN
        assert len(get_existing_bud_x_tables(cursor, "_staging")) != 0
        assert len(get_existing_bud_x_tables(cursor, "_agg")) != 0
        bud_count = len(get_bud_categorys())
        bud_staging_tables = get_existing_bud_x_tables(cursor, "_staging")
        bud_agg_tables = get_existing_bud_x_tables(cursor, "_staging")
        print(f"{get_bud_categorys()=}")
        print(f"{bud_staging_tables=}")
        print(f"{bud_agg_tables=}")
        assert len(get_existing_bud_x_tables(cursor, "_staging")) == bud_count
        assert len(get_existing_bud_x_tables(cursor, "_agg")) == bud_count


def test_WorldUnit_idea_staging_to_bud_tables_Bud_category_idea_PopulatesFiscalStagingTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    fizz_world = worldunit_shop("fizz")
    sue_aft_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        fizz_world.etl_aft_face_csv_files2idea_staging_tables(cursor)
        budunit_staging_tablename = f"{budunit_str()}_staging"
        assert not db_table_exists(cursor, budunit_staging_tablename)

        # WHEN
        fizz_world.idea_staging_to_bud_tables(cursor)

        # THEN
        assert db_table_exists(cursor, budunit_staging_tablename)
        assert get_row_count(cursor, budunit_staging_tablename) == 3
        cursor.execute(f"SELECT * FROM {budunit_staging_tablename}")
        budunit_db_rows = cursor.fetchall()
        expected_row1 = (
            br00011_str,
            sue_inx,
            event3,
            accord23_str,  # fiscal_title,
            bob_inx,  # owner_name,
            None,  # credor_respect,
            None,  # debtor_respect,
            None,  # fund_pool,
            None,  # max_tree_traverse,
            None,  # deal_time_int,
            None,  # tally,
            None,  # fund_coin,
            None,  # penny,
            None,  # respect_bit
            None,  # error_message
        )
        expected_row2 = (
            br00011_str,
            sue_inx,
            event3,
            accord23_str,  # fiscal_title,
            yao_inx,  # owner_name,
            None,  # credor_respect,
            None,  # debtor_respect,
            None,  # fund_pool,
            None,  # max_tree_traverse,
            None,  # deal_time_int,
            None,  # tally,
            None,  # fund_coin,
            None,  # penny,
            None,  # respect_bit
            None,  # error_message
        )
        expected_row3 = (
            br00011_str,
            sue_inx,
            event7,
            accord23_str,  # fiscal_title,
            yao_inx,  # owner_name,
            None,  # credor_respect,
            None,  # debtor_respect,
            None,  # fund_pool,
            None,  # max_tree_traverse,
            None,  # deal_time_int,
            None,  # tally,
            None,  # fund_coin,
            None,  # penny,
            None,  # respect_bit
            None,  # error_message
        )
        print(f"{budunit_db_rows[2]=}")
        print(f"     {expected_row3=}")
        assert budunit_db_rows == [expected_row1, expected_row2, expected_row3]
