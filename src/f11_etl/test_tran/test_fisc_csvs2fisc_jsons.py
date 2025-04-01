from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import get_row_count, db_table_exists
from src.f01_road.deal import bridge_str, owner_name_str, fisc_title_str
from src.f03_chrono.chrono import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_title_str,
    timeline_config_shop,
    timelineunit_shop,
)
from src.f04_vow.atom_config import (
    acct_name_str,
    face_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f06_listen.hub_path import create_fisc_json_path
from src.f08_fisc.fisc import get_from_json as fiscunit_get_from_json
from src.f08_fisc.fisc_config import fiscunit_str
from src.f11_etl.transformers import (
    create_fisc_tables,
    etl_fisc_agg_tables_to_fisc_jsons,
)
from src.f11_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_etl_fisc_agg_tables_to_fisc_jsons_Scenario0_CreateFilesWithOnlyFiscTitle(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    fisc_mstr_dir = get_test_etl_dir()
    fiscunit_agg_tablename = f"{fiscunit_str()}_agg"

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)

        insert_staging_sqlstr = f"""
INSERT INTO {fiscunit_agg_tablename} ({fisc_title_str()})
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, fiscunit_agg_tablename) == 2
        fisc_event_time_agg_str = "fisc_event_time_agg"
        assert db_table_exists(cursor, fisc_event_time_agg_str) is False

        accord23_json_path = create_fisc_json_path(fisc_mstr_dir, accord23_str)
        accord45_json_path = create_fisc_json_path(fisc_mstr_dir, accord45_str)
        assert os_path_exists(accord23_json_path) is False
        assert os_path_exists(accord45_json_path) is False

        # WHEN
        etl_fisc_agg_tables_to_fisc_jsons(cursor, fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord23_json_path)
    assert os_path_exists(accord45_json_path)
    accord23_fisc = fiscunit_get_from_json(open_file(accord23_json_path))
    accord45_fisc = fiscunit_get_from_json(open_file(accord45_json_path))
    assert accord23_fisc.fisc_title == accord23_str
    assert accord45_fisc.fisc_title == accord45_str


# def test_etl_fisc_agg_tables_to_fisc_jsons_Scenario1_CreateFilesWithFiscUnitAttrs(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     fisc_mstr_dir = get_test_etl_dir()
#     x_fisc = FiscPrimeObjsRef(fisc_mstr_dir)
#     x_cols = FiscPrimeColumnsRef()
#     a45_fund_coin = 3
#     a45_penny = 5
#     a45_respect_bit = 7
#     a45_bridge = "/"
#     a45_c400_number = 88
#     a45_yr1_jan1_offset = 501
#     a45_monthday_distortion = 17
#     a45_timeline_title = "a45_timeline"
#     print(f"{x_cols.unit_agg_csv_header=}")
#     fiscunit_agg_csv_str = f"""{x_cols.unit_agg_csv_header}
# {accord23_str},,,,,,,,
# {accord45_str},{a45_timeline_title},{a45_c400_number},{a45_yr1_jan1_offset},{a45_monthday_distortion},{a45_fund_coin},{a45_penny},{a45_respect_bit},{a45_bridge}
# """
#     save_file(fisc_mstr_dir, x_fisc.unit_agg_csv_filename, fiscunit_agg_csv_str)
#     save_file(fisc_mstr_dir, x_fisc.deal_agg_csv_filename, x_cols.deal_agg_empty_csv)
#     save_file(fisc_mstr_dir, x_fisc.cash_agg_csv_filename, x_cols.cash_agg_empty_csv)
#     save_file(fisc_mstr_dir, x_fisc.hour_agg_csv_filename, x_cols.hour_agg_empty_csv)
#     save_file(fisc_mstr_dir, x_fisc.mont_agg_csv_filename, x_cols.mont_agg_empty_csv)
#     save_file(fisc_mstr_dir, x_fisc.week_agg_csv_filename, x_cols.week_agg_empty_csv)
#     save_file(fisc_mstr_dir, x_fisc.offi_agg_csv_filename, x_cols.offi_agg_empty_csv)

#     accord23_json_path = create_fisc_json_path(fisc_mstr_dir, accord23_str)
#     accord45_json_path = create_fisc_json_path(fisc_mstr_dir, accord45_str)
#     assert os_path_exists(accord23_json_path) is False
#     assert os_path_exists(accord45_json_path) is False

#     # WHEN
#     etl_fisc_agg_tables_to_fisc_jsons(fisc_mstr_dir)

#     # THEN
#     assert os_path_exists(accord23_json_path)
#     assert os_path_exists(accord45_json_path)
#     accord23_fisc = fiscunit_get_from_json(open_file(accord23_json_path))
#     accord45_fisc = fiscunit_get_from_json(open_file(accord45_json_path))
#     assert accord23_fisc == fiscunit_shop(accord23_str)
#     expected_45_tl = timelineunit_shop(
#         timeline_config_shop(
#             timeline_title=a45_timeline_title,
#             c400_number=a45_c400_number,
#             yr1_jan1_offset=a45_yr1_jan1_offset,
#             monthday_distortion=a45_monthday_distortion,
#         )
#     )
#     accord_45_timeline = accord45_fisc.timeline
#     assert accord_45_timeline.c400_number == expected_45_tl.c400_number
#     assert accord_45_timeline.monthday_distortion == expected_45_tl.monthday_distortion
#     assert accord_45_timeline.timeline_title == expected_45_tl.timeline_title
#     assert accord_45_timeline.yr1_jan1_offset == expected_45_tl.yr1_jan1_offset
#     assert accord_45_timeline == expected_45_tl
#     assert accord45_fisc == fiscunit_shop(
#         fisc_title=accord45_str,
#         fund_coin=a45_fund_coin,
#         penny=a45_penny,
#         respect_bit=a45_respect_bit,
#         bridge=a45_bridge,
#         timeline=expected_45_tl,
#     )
#     assert 1 == 2
