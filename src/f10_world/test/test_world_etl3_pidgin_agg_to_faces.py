from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    face_id_str,
    fiscal_id_str,
    acct_id_str,
    owner_id_str,
)
from src.f08_pidgin.pidgin_config import (
    event_id_str,
    inx_wall_str,
    otx_wall_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
)

# from src.f09_brick.pandas_tool import split_excel_into_dirs
# from src.f10_world.world import worldunit_shop, split_staging_to_faces

# from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


# def test_split_staging_to_faces_CreatesFiles_Scenario0_1source(
#     sample_excel_file, output_dir
# ):
#     """Test splitting an Excel file by a valid column."""
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     m_str = "music23"
#     event7 = 7
#     br00117_file_path = create_path(fizz_world._zoo_dir, "br00117.xlsx")
#     br00117_columns = [
#         face_id_str(),
#         event_id_str(),
#         fiscal_id_str(),
#         owner_id_str(),
#         acct_id_str(),
#         otx_road_str(),
#         inx_road_str(),
#     ]
#     sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
#     b117_rows = [sue0, sue1]
#     br00117_df = DataFrame(b117_rows, columns=br00117_columns)
#     upsert_sheet(br00117_file_path, "zoo_agg", br00117_df)
#     pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
#     fizz_world.zoo_agg_to_zoo_events()
#     fizz_world.zoo_events_to_events_log()
#     fizz_world.events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg_file()
#     fizz_world.zoo_agg_to_road_staging()
#     road_staging_str = "road_staging"
#     gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)
#     sue_face_path = create_path(fizz_world._pidgins_dir)
#     sue_otx2inx_file_path = create_path()

#     # WHEN
#     fizz_world.acct_staging_to_faces()

#     x_filename = "fizz"
#     a_file_path = create_path(output_dir, f"A/{x_filename}.xlsx")
#     b_file_path = create_path(output_dir, f"B/{x_filename}.xlsx")
#     c_file_path = create_path(output_dir, f"C/{x_filename}.xlsx")
#     assert os_path_exists(a_file_path) is False
#     assert os_path_exists(b_file_path) is False
#     assert os_path_exists(c_file_path) is False

#     # WHEN
#     split_staging_to_faces(
#         sample_excel_file, "Category", x_filename, "sheet5"
#     )

#     # Verify files are created for each unique value in "Category"
#     assert os_path_exists(a_file_path)
#     assert os_path_exists(b_file_path)
#     assert os_path_exists(c_file_path)

#     # Verify contents of one of the created files
#     a_df = pandas_read_excel(a_file_path)
#     expected_a = DataFrame({"ID": [1, 3], "Category": ["A", "A"], "Value": [100, 150]})
#     pandas_testing_assert_frame_equal(a_df, expected_a)

#     b_df = pandas_read_excel(b_file_path)
#     b_expected = DataFrame({"ID": [2, 5], "Category": ["B", "B"], "Value": [200, 250]})
#     pandas_testing_assert_frame_equal(b_df, b_expected)

#     c_df = pandas_read_excel(c_file_path)
#     c_expected = DataFrame({"ID": [4], "Category": ["C"], "Value": [300]})
#     pandas_testing_assert_frame_equal(c_df, c_expected)

# def test_WorldUnit_acct_staging_to_faces_CreatesFile_Scenario0_SingleBrick(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     m_str = "music23"
#     event7 = 7
#     br00113_file_path = create_path(fizz_world._zoo_dir, "br00113.xlsx")
#     br00113_columns = [
#         face_id_str(),
#         event_id_str(),
#         fiscal_id_str(),
#         owner_id_str(),
#         acct_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#     ]
#     sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
#     br00113_rows = [sue0, sue1]
#     br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
#     upsert_sheet(br00113_file_path, "zoo_agg", br00113_df)
#     pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
#     fizz_world.zoo_agg_to_zoo_events()
#     fizz_world.zoo_events_to_events_log()
#     fizz_world.events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg_file()
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.zoo_agg_to_acct_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     acct_staging_str = "acct_staging"
#     gen_acct_df = pandas_read_excel(pidgin_path, sheet_name=acct_staging_str)
#     acct_file_columns = [
#         "src_brick",
#         face_id_str(),
#         event_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_acct_df.columns) == acct_file_columns
#     assert len(gen_acct_df) == 2
#     bx = "br00113"
#     e1_acct0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
#     e1_acct1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
#     e1_acct_rows = [e1_acct0, e1_acct1]
#     e1_acct_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
#     assert len(gen_acct_df) == len(e1_acct_df)
#     print(f"{gen_acct_df.to_csv()=}")
#     print(f" {e1_acct_df.to_csv()=}")
#     assert gen_acct_df.to_csv(index=False) == e1_acct_df.to_csv(index=False)
#     assert get_sheet_names(pidgin_path) == [acct_staging_str]


# def test_WorldUnit_zoo_agg_to_acct_staging_CreatesFile_Scenario1_MultipleBricksFiles(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     ukx = "Unknown"
#     m_str = "music23"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     br00113_file_path = create_path(fizz_world._zoo_dir, "br00113.xlsx")
#     br00113_columns = [
#         face_id_str(),
#         event_id_str(),
#         fiscal_id_str(),
#         owner_id_str(),
#         acct_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#     ]
#     br00043_file_path = create_path(fizz_world._zoo_dir, "br00043.xlsx")
#     br00043_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
#     br00113_rows = [sue0, sue1]
#     br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
#     upsert_sheet(br00113_file_path, "zoo_agg", br00113_df)
#     br00043_df = [sue2, sue3, yao1]
#     br00043_df = DataFrame(br00043_df, columns=br00043_columns)
#     upsert_sheet(br00043_file_path, "zoo_agg", br00043_df)
#     pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
#     fizz_world.zoo_agg_to_zoo_events()
#     fizz_world.zoo_events_to_events_log()
#     fizz_world.events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg_file()
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.zoo_agg_to_acct_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     acct_staging_str = "acct_staging"
#     gen_acct_df = pandas_read_excel(pidgin_path, sheet_name=acct_staging_str)
#     acct_file_columns = [
#         "src_brick",
#         face_id_str(),
#         event_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_acct_df.columns) == acct_file_columns
#     assert len(gen_acct_df) == 5
#     b3 = "br00113"
#     b4 = "br00043"
#     e1_acct3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_acct4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_acct5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
#     e1_acct0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
#     e1_acct1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

#     e1_acct_rows = [e1_acct3, e1_acct4, e1_acct5, e1_acct0, e1_acct1]
#     e1_acct_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
#     assert len(gen_acct_df) == len(e1_acct_df)
#     print(f"{gen_acct_df.to_csv()=}")
#     print(f" {e1_acct_df.to_csv()=}")
#     assert gen_acct_df.to_csv(index=False) == e1_acct_df.to_csv(index=False)
#     assert get_sheet_names(pidgin_path) == [acct_staging_str]


# def test_WorldUnit_zoo_agg_to_acct_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     ukx = "Unknown"
#     m_str = "music23"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     br00113_file_path = create_path(fizz_world._zoo_dir, "br00113.xlsx")
#     br00113_columns = [
#         face_id_str(),
#         event_id_str(),
#         fiscal_id_str(),
#         owner_id_str(),
#         acct_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#     ]
#     br00043_file_path = create_path(fizz_world._zoo_dir, "br00043.xlsx")
#     br00043_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00113_rows = [sue0, sue1]
#     br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
#     upsert_sheet(br00113_file_path, "zoo_agg", br00113_df)
#     br00043_df = [sue2, sue3, yao1]
#     br00043_df = DataFrame(br00043_df, columns=br00043_columns)
#     upsert_sheet(br00043_file_path, "zoo_agg", br00043_df)
#     pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
#     assert fizz_world.events == {}
#     fizz_world.zoo_agg_to_zoo_events()
#     fizz_world.zoo_events_to_events_log()
#     fizz_world.events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg_file()
#     assert fizz_world.events == {event2: sue_str, event5: sue_str}
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.zoo_agg_to_acct_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     acct_staging_str = "acct_staging"
#     gen_acct_df = pandas_read_excel(pidgin_path, sheet_name=acct_staging_str)
#     acct_file_columns = [
#         "src_brick",
#         face_id_str(),
#         event_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_acct_df.columns) == acct_file_columns
#     assert len(gen_acct_df) == 2
#     b3 = "br00113"
#     b4 = "br00043"
#     e1_acct3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_acct4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_acct_rows = [e1_acct3, e1_acct4]
#     e1_acct_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
#     assert len(gen_acct_df) == len(e1_acct_df)
#     print(f"{gen_acct_df.to_csv()=}")
#     print(f" {e1_acct_df.to_csv()=}")
#     assert gen_acct_df.to_csv(index=False) == e1_acct_df.to_csv(index=False)
#     assert get_sheet_names(pidgin_path) == [acct_staging_str]
