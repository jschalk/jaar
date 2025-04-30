from src.a00_data_toolbox.file_toolbox import create_path, save_file
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    face_name_str,
    acct_name_str,
    event_int_str,
    credit_belief_str,
    debtit_belief_str,
)
from src.a08_bud_atom_logic.atom_config import get_bud_dimens
from src.a17_idea_logic._utils.str_a17 import idea_number_str
from src.a18_etl_toolbox.tran_sqlstrs import create_bud_prime_tables
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection


def get_existing_bud_x_tables(cursor: sqlite3_Connection, ending: str) -> set:
    return {
        bud_dimen
        for bud_dimen in get_bud_dimens()
        if db_table_exists(cursor, f"{bud_dimen}{ending}")
    }


def test_WorldUnit_idea_raw_to_bud_prime_tables_CreatesBudRawTables(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-method
    # ESTABLISH
    raw_str = "_put_raw"
    agg_str = "_put_agg"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        assert len(get_existing_bud_x_tables(cursor, raw_str)) == 0
        assert len(get_existing_bud_x_tables(cursor, agg_str)) == 0

        # WHEN
        fizz_world.idea_raw_to_bud_prime_tables(cursor)

        # THEN
        assert len(get_existing_bud_x_tables(cursor, raw_str)) != 0
        assert len(get_existing_bud_x_tables(cursor, agg_str)) != 0
        bud_count = len(get_bud_dimens())
        bud_raw_tables = get_existing_bud_x_tables(cursor, raw_str)
        bud_agg_tables = get_existing_bud_x_tables(cursor, agg_str)
        print(f"{get_bud_dimens()=}")
        print(f"{bud_raw_tables=}")
        print(f"{bud_agg_tables=}")
        assert len(get_existing_bud_x_tables(cursor, raw_str)) == bud_count
        assert len(get_existing_bud_x_tables(cursor, agg_str)) == bud_count


def test_WorldUnit_idea_raw_to_bud_prime_tables_Bud_dimen_idea_PopulatesFiscRawTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    sue_inz_dir = create_path(fizz_world._syntax_inz_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fisc_tag_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz", worlds_dir())
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        fizz_world.inz_face_csv_files2idea_raw_tables(cursor)
        budunit_raw_tablename = f"{budunit_str()}_put_raw"
        assert not db_table_exists(cursor, budunit_raw_tablename)

        # WHEN
        fizz_world.idea_raw_to_bud_prime_tables(cursor)

        # THEN
        assert db_table_exists(cursor, budunit_raw_tablename)
        assert get_row_count(cursor, budunit_raw_tablename) == 3
        cursor.execute(f"SELECT * FROM {budunit_raw_tablename}")
        budunit_db_rows = cursor.fetchall()
        expected_row1 = (
            br00011_str,
            sue_inx,
            event3,
            accord23_str,  # fisc_tag,
            bob_inx,  # owner_name,
            None,  # credor_respect,
            None,  # debtor_respect,
            None,  # fund_pool,
            None,  # max_tree_traverse,
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
            accord23_str,  # fisc_tag,
            yao_inx,  # owner_name,
            None,  # credor_respect,
            None,  # debtor_respect,
            None,  # fund_pool,
            None,  # max_tree_traverse,
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
            accord23_str,  # fisc_tag,
            yao_inx,  # owner_name,
            None,  # credor_respect,
            None,  # debtor_respect,
            None,  # fund_pool,
            None,  # max_tree_traverse,
            None,  # tally,
            None,  # fund_coin,
            None,  # penny,
            None,  # respect_bit
            None,  # error_message
        )
        print(f"{budunit_db_rows[2]=}")
        print(f"     {expected_row3=}")
        assert budunit_db_rows == [expected_row1, expected_row2, expected_row3]


def test_WorldUnit_idea_raw_to_bud_prime_tables_Sets_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    yao_credit_belief5 = 5
    yao_credit_belief7 = 7
    fizz_world = worldunit_shop("fizz", worlds_dir())
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_bud_prime_tables(cursor)
        x_tablename = f"{bud_acctunit_str()}_put_raw"
        assert db_table_exists(cursor, x_tablename)
        insert_raw_sqlstr = f"""
INSERT INTO {x_tablename} ({idea_number_str()},{face_name_str()},{event_int_str()},{fisc_tag_str()},{owner_name_str()},{acct_name_str()},{credit_belief_str()},{debtit_belief_str()})
VALUES
  ('br00021','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5},NULL)
, ('br00021','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',NULL,NULL)
, ('br00021','{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5},NULL)
, ('br00021','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5},NULL)
, ('br00021','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}',{yao_credit_belief7},NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_tag_str()}, {credit_belief_str()}, error_message FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (event3, accord23_str, yao_credit_belief5, None),
            (event3, accord23_str, None, None),
            (event7, accord23_str, yao_credit_belief5, None),
            (event7, accord45_str, yao_credit_belief5, None),
            (event7, accord45_str, yao_credit_belief7, None),
        ]

        # WHEN
        fizz_world.idea_raw_to_bud_prime_tables(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        x_error_message = "Inconsistent data"
        assert rows == [
            (event3, accord23_str, yao_credit_belief5, None),
            (event3, accord23_str, None, None),
            (event7, accord23_str, yao_credit_belief5, None),
            (event7, accord45_str, yao_credit_belief5, x_error_message),
            (event7, accord45_str, yao_credit_belief7, x_error_message),
        ]
