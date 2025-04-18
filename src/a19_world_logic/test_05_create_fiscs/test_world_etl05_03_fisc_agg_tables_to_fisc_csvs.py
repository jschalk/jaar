from src.a00_data_toolboxs.file_toolbox import create_path, save_file, open_file
from src.a00_data_toolboxs.db_toolbox import db_table_exists, get_row_count
from src.a02_finance_toolboxs.deal import owner_name_str, fisc_title_str
from src.a08_bud_atom_logic.atom_config import (
    face_name_str,
    acct_name_str,
    event_int_str,
)
from src.a17_idea_logic.idea_db_tool import get_pragma_table_fetchall
from src.a18_etl_toolbox.fisc_etl_tool import (
    FiscPrimeColumnsRef,
    FiscPrimeObjsRef,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic.examples.world_env import (
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_inz_faces_ideas_to_fisc_mstr_csvs_CreateStagingFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    fizz_world = worldunit_shop("fizz")
    sue_inz_dir = create_path(fizz_world._faces_inz_dir, sue_inx)
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord45_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")
    fisc_objs = FiscPrimeObjsRef(fizz_world._fisc_mstr_dir)
    fizz_world.inz_face_ideas_to_csv_files()
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.inz_face_csv_files2idea_staging_tables(cursor)
        fizz_world.idea_staging_to_fisc_tables(cursor)
        assert os_path_exists(fisc_objs.unit_stage_csv_path) is False

        # WHEN
        fizz_world.inz_faces_ideas_to_fisc_mstr_csvs(cursor)

        # THEN
        print(f"{fisc_objs.unit_stage_csv_path=}")
        assert os_path_exists(fisc_objs.unit_stage_csv_path)
        generated_fiscunit_csv = open_file(fisc_objs.unit_stage_csv_path)
        fisc_cols = FiscPrimeColumnsRef()
        expected_fiscunit_csv_str = f"""{fisc_cols.unit_staging_csv_header}
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,,
{br00011_str},{sue_inx},{event7},{accord45_str},,,,,,,,,,
"""
        print(f"   {expected_fiscunit_csv_str=}")
        assert generated_fiscunit_csv == expected_fiscunit_csv_str


def test_WorldUnit_inz_faces_ideas_to_fisc_mstr_csvs_CreateAggFiles(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-method

    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    fizz_world = worldunit_shop("fizz")
    sue_inz_dir = create_path(fizz_world._faces_inz_dir, sue_inx)
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord45_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")
    fizz_world.inz_face_ideas_to_csv_files()
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.inz_face_csv_files2idea_staging_tables(cursor)
        fizz_world.idea_staging_to_fisc_tables(cursor)
        fiz_objs = FiscPrimeObjsRef(fizz_world._fisc_mstr_dir)
        assert os_path_exists(fiz_objs.unit_agg_csv_path) is False

        # WHEN
        fizz_world.inz_faces_ideas_to_fisc_mstr_csvs(cursor)

        # THEN
        # print(f"{fiscunit_csv_path=}")
        assert os_path_exists(fiz_objs.unit_agg_csv_path)
        generated_fiscunit_csv = open_file(fiz_objs.unit_agg_csv_path)
        fisc_cols = FiscPrimeColumnsRef()
        expected_fiscunit_csv_str = f"""{fisc_cols.unit_agg_csv_header}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
        print(f"{expected_fiscunit_csv_str=}")
        print(f"   {generated_fiscunit_csv=}")
        assert generated_fiscunit_csv == expected_fiscunit_csv_str


# def test_WorldUnit_inz_faces_ideas_to_fisc_staging_CreatesCorrectTables(
#     env_dir_setup_cleanup,
# ):

#     # THEN
#     staging_str = "staging"
#     br00000_path = create_path(fizz_world._faces_inz_dir, "br00000.xlsx")
#     br00001_path = create_path(fizz_world._faces_inz_dir, "br00001.xlsx")
#     br00002_path = create_path(fizz_world._faces_inz_dir, "br00002.xlsx")
#     br00003_path = create_path(fizz_world._faces_inz_dir, "br00003.xlsx")
#     br00004_path = create_path(fizz_world._faces_inz_dir, "br00004.xlsx")
#     br00005_path = create_path(fizz_world._faces_inz_dir, "br00005.xlsx")

#     br00000_df = pandas_read_excel(br00000_path, sheet_name=staging_str)
#     br00001_df = pandas_read_excel(br00001_path, sheet_name=staging_str)
#     br00002_df = pandas_read_excel(br00002_path, sheet_name=staging_str)
#     br00003_df = pandas_read_excel(br00003_path, sheet_name=staging_str)
#     br00004_df = pandas_read_excel(br00004_path, sheet_name=staging_str)
#     br00005_df = pandas_read_excel(br00005_path, sheet_name=staging_str)

#     common_cols = [face_name_str(), event_int_str(), fisc_title_str()]
#     expected_br0_columns = copy_copy(common_cols)
#     expected_br1_columns = copy_copy(common_cols)
#     expected_br2_columns = copy_copy(common_cols)
#     expected_br3_columns = copy_copy(common_cols)
#     expected_br4_columns = copy_copy(common_cols)
#     expected_br5_columns = copy_copy(common_cols)
#     expected_br0_columns.extend(
#         [
#             c400_number_str(),
#             fund_coin_str(),
#             monthday_distortion_str(),
#             penny_str(),
#             respect_bit_str(),
#             bridge_str(),
#             timeline_title_str(),
#             yr1_jan1_offset_str(),
#         ]
#     )
#     expected_br1_columns.extend(
#         [owner_name_str(), acct_name_str(), deal_time_str(), quota_str()]
#     )
#     expected_br2_columns.extend(
#         [owner_name_str(), acct_name_str(), tran_time_str(), amount_str()]
#     )
#     expected_br3_columns.extend([hour_title_str(), cumlative_minute_str()])
#     expected_br4_columns.extend([month_title_str(), cumlative_day_str()])
#     expected_br5_columns.extend([weekday_title_str(), weekday_order_str()])

#     print(f"{list(br00000_df.columns)=}")
#     assert list(br00000_df.columns) == expected_br0_columns
#     assert list(br00001_df.columns) == expected_br1_columns
#     assert list(br00002_df.columns) == expected_br2_columns
#     assert list(br00003_df.columns) == expected_br3_columns
#     assert list(br00004_df.columns) == expected_br4_columns
#     assert list(br00005_df.columns) == expected_br5_columns


# def test_WorldUnit_cart_agg_to_pidgin_staging_CreatesFile(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     ukx = "Unknown"
#     m_str = "accord23"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     br00113_file_path = create_path(fizz_world._cart_dir, "br00113.xlsx")
#     br00113_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_name_str(),
#         inx_name_str(),
#     ]
#     br00043_file_path = create_path(fizz_world._cart_dir, "br00043.xlsx")
#     br00043_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_name_str(),
#         inx_name_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00113_rows = [sue0, sue1]
#     br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
#     upsert_sheet(br00113_file_path, cart_agg_str(), br00113_df)
#     br00043_df = [sue2, sue3, yao1]
#     br00043_df = DataFrame(br00043_df, columns=br00043_columns)
#     upsert_sheet(br00043_file_path, cart_agg_str(), br00043_df)
#     pidgin_path = create_cart_pidgin_path(fizz_world._cart_dir)

#     br00115_file_path = create_path(fizz_world._cart_dir, "br00115.xlsx")
#     br00115_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_label_str(),
#         inx_label_str(),
#     ]
#     br00042_file_path = create_path(fizz_world._cart_dir, "br00042.xlsx")
#     br00042_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_label_str(),
#         inx_label_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00115_rows = [sue0, sue1]
#     br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
#     upsert_sheet(br00115_file_path, cart_agg_str(), br00115_df)
#     b40_rows = [sue2, sue3, yao1]
#     br00042_df = DataFrame(b40_rows, columns=br00042_columns)
#     upsert_sheet(br00042_file_path, cart_agg_str(), br00042_df)

#     br00116_file_path = create_path(fizz_world._cart_dir, "br00116.xlsx")
#     br00116_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_title_str(),
#         inx_title_str(),
#     ]
#     br00044_file_path = create_path(fizz_world._cart_dir, "br00044.xlsx")
#     br00044_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_title_str(),
#         inx_title_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00116_rows = [sue0, sue1]
#     br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
#     upsert_sheet(br00116_file_path, cart_agg_str(), br00116_df)
#     br00044_rows = [sue2, sue3, yao1]
#     br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
#     upsert_sheet(br00044_file_path, cart_agg_str(), br00044_df)

#     br00117_file_path = create_path(fizz_world._cart_dir, "br00117.xlsx")
#     br00117_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_road_str(),
#         inx_road_str(),
#     ]
#     br00045_file_path = create_path(fizz_world._cart_dir, "br00045.xlsx")
#     br00045_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     b117_rows = [sue0, sue1]
#     br00117_df = DataFrame(b117_rows, columns=br00117_columns)
#     upsert_sheet(br00117_file_path, cart_agg_str(), br00117_df)
#     br00045_rows = [sue2, sue3, yao1]
#     br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
#     upsert_sheet(br00045_file_path, cart_agg_str(), br00045_df)

#     assert fizz_world.events == {}
#     fizz_world.cart_agg_to_cart_events()
#     fizz_world.cart_events_to_events_log()
#     fizz_world.cart_events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg_file()
#     assert fizz_world.events == {event2: sue_str, event5: sue_str}
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.cart_agg_to_pidgin_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     label_staging_str = "label_staging"
#     name_staging_str = "name_staging"
#     title_staging_str = "title_staging"
#     road_staging_str = "road_staging"
#     assert sheet_exists(pidgin_path, name_staging_str)
#     assert sheet_exists(pidgin_path, label_staging_str)
#     assert sheet_exists(pidgin_path, title_staging_str)
#     assert sheet_exists(pidgin_path, road_staging_str)

#     gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_staging_str)
#     gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_staging_str)
#     gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_staging_str)
#     gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)

#     label_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_label_str(),
#         inx_label_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_label_df.columns) == label_file_columns
#     assert len(gen_label_df) == 2
#     b3 = "br00115"
#     b4 = "br00042"
#     e1_label3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_label4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_label_rows = [e1_label3, e1_label4]
#     e1_label_df = DataFrame(e1_label_rows, columns=label_file_columns)
#     assert len(gen_label_df) == len(e1_label_df)
#     print(f"{gen_label_df.to_csv()=}")
#     print(f" {e1_label_df.to_csv()=}")
#     assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)

#     name_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_name_str(),
#         inx_name_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_name_df.columns) == name_file_columns
#     assert len(gen_name_df) == 2
#     b3 = "br00113"
#     b4 = "br00043"
#     e1_name3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_name4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_name_rows = [e1_name3, e1_name4]
#     e1_name_df = DataFrame(e1_name_rows, columns=name_file_columns)
#     assert len(gen_name_df) == len(e1_name_df)
#     print(f"{gen_name_df.to_csv()=}")
#     print(f" {e1_name_df.to_csv()=}")
#     assert gen_name_df.to_csv(index=False) == e1_name_df.to_csv(index=False)

#     title_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_title_str(),
#         inx_title_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_title_df.columns) == title_file_columns
#     assert len(gen_title_df) == 2
#     b3 = "br00116"
#     b4 = "br00044"
#     e1_title3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_title4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_title_rows = [e1_title3, e1_title4]
#     e1_title_df = DataFrame(e1_title_rows, columns=title_file_columns)
#     assert len(gen_title_df) == len(e1_title_df)
#     print(f"{gen_title_df.to_csv()=}")
#     print(f" {e1_title_df.to_csv()=}")
#     assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)

#     road_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_road_df.columns) == road_file_columns
#     assert len(gen_road_df) == 2
#     b3 = "br00117"
#     b4 = "br00045"
#     e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_road_rows = [e1_road3, e1_road4]
#     e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
#     assert len(gen_road_df) == len(e1_road_df)
#     print(f"{gen_road_df.to_csv()=}")
#     print(f" {e1_road_df.to_csv()=}")
#     assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)


# def test_WorldUnit_inz_face_ideas_to_inz_event_ideas_CreatesFaceIdeaSheets_Scenario0_MultpleFaceNames(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_str = "Sue"
#     zia_str = "Zia"
#     event3 = 3
#     event7 = 7
#     event9 = 9
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     idea_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_title_str(),
#         hour_title_str(),
#         cumlative_minute_str(),
#     ]
#     accord23_str = "accord23"
#     sue0 = [sue_str, event3, accord23_str, hour6am, minute_360]
#     sue1 = [sue_str, event3, accord23_str, hour7am, minute_420]
#     zia0 = [zia_str, event7, accord23_str, hour7am, minute_420]
#     zia1 = [zia_str, event9, accord23_str, hour6am, minute_360]
#     zia2 = [zia_str, event9, accord23_str, hour7am, minute_420]
#     example_sue_df = DataFrame([sue0, sue1], columns=idea_columns)
#     example_zia_df = DataFrame([zia0, zia1, zia2], columns=idea_columns)
#     fizz_world = worldunit_shop("fizz")
#     br00003_filename = "br00003.xlsx"
#     sue_dir = create_path(fizz_world._faces_inz_dir, sue_str)
#     zia_dir = create_path(fizz_world._faces_inz_dir, zia_str)
#     sue_br00003_filepath = create_path(sue_dir, br00003_filename)
#     zia_br00003_filepath = create_path(zia_dir, br00003_filename)
#     upsert_sheet(sue_br00003_filepath, "inx", example_sue_df)
#     upsert_sheet(zia_br00003_filepath, "inx", example_zia_df)

#     event3_dir = create_path(sue_dir, event3)
#     event7_dir = create_path(zia_dir, event7)
#     event9_dir = create_path(zia_dir, event9)
#     event3_br00003_filepath = create_path(event3_dir, br00003_filename)
#     event7_br00003_filepath = create_path(event7_dir, br00003_filename)
#     event9_br00003_filepath = create_path(event9_dir, br00003_filename)
#     assert sheet_exists(event3_br00003_filepath, "inx") is False
#     assert sheet_exists(event7_br00003_filepath, "inx") is False
#     assert sheet_exists(event9_br00003_filepath, "inx") is False

#     # WHEN
#     fizz_world.inz_face_ideas_to_inz_event_ideas()

#     # THEN
#     assert sheet_exists(event3_br00003_filepath, "inx")
#     assert sheet_exists(event7_br00003_filepath, "inx")
#     assert sheet_exists(event9_br00003_filepath, "inx")
#     gen_event3_df = pandas_read_excel(event3_br00003_filepath, "inx")
#     gen_event7_df = pandas_read_excel(event7_br00003_filepath, "inx")
#     gen_event9_df = pandas_read_excel(event9_br00003_filepath, "inx")
#     example_event3_df = DataFrame([sue0, sue1], columns=idea_columns)
#     example_event7_df = DataFrame([zia0], columns=idea_columns)
#     example_event9_df = DataFrame([zia1, zia2], columns=idea_columns)
#     pandas_assert_frame_equal(gen_event3_df, example_event3_df)
#     pandas_assert_frame_equal(gen_event7_df, example_event7_df)
#     pandas_assert_frame_equal(gen_event9_df, example_event9_df)
