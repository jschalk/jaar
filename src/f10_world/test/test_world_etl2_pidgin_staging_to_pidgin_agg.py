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
    inx_acct_id_str,
    otx_acct_id_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import upsert_sheet, sheet_exists
from src.f10_world.world import worldunit_shop
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_acct_staging_to_faces_Scenario0_CreatesEmptyFileBecauseOfConflict(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    event7 = 7
    acct_staging_str = "acct_staging"
    acct_agg_str = "acct_agg"
    colon_str = ":"
    slash_str = "/"
    acct_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    bx = "br00113"
    e1_acct0 = [bx, sue_str, event7, yao_str, yao_inx, None, colon_str, None]
    e1_acct1 = [bx, sue_str, event7, bob_str, bob_inx, None, slash_str, None]
    e1_acct_rows = [e1_acct0, e1_acct1]
    staging_acct_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
    pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
    upsert_sheet(pidgin_path, acct_staging_str, staging_acct_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, acct_staging_str)
    assert sheet_exists(pidgin_path, "acct_agg") is False

    # WHEN
    fizz_world.acct_staging_to_acct_agg()

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, acct_agg_str)
    gen_acct_agg_df = pandas_read_excel(pidgin_path, sheet_name=acct_agg_str)
    acct_file_columns = [
        face_id_str(),
        event_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_acct_agg_df.columns) == acct_file_columns
    assert len(gen_acct_agg_df) == 0
    e1_acct_agg_df = DataFrame([], columns=acct_file_columns)
    pandas_testing_assert_frame_equal(gen_acct_agg_df, e1_acct_agg_df)


# def test_WorldUnit_acct_staging_to_faces_CreatesFile_Scenario1_SingleBrick(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     event7 = 7
#     acct_staging_str = "acct_staging"
#     acct_agg_str = "acct_agg"
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
#     bx = "br00113"
#     e1_acct0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
#     e1_acct1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
#     e1_acct_rows = [e1_acct0, e1_acct1]
#     staging_acct_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
#     pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
#     upsert_sheet(pidgin_path, acct_staging_str, staging_acct_df)
#     assert os_path_exists(pidgin_path)
#     assert sheet_exists(pidgin_path, acct_staging_str)
#     assert sheet_exists(pidgin_path, "acct_agg") is False

#     # WHEN
#     fizz_world.acct_staging_to_acct_agg()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     assert sheet_exists(pidgin_path, acct_agg_str)
#     gen_acct_agg_df = pandas_read_excel(pidgin_path, sheet_name=acct_agg_str)
#     acct_file_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_acct_agg_df.columns) == acct_file_columns
#     assert len(gen_acct_agg_df) == 2
#     e1_acct0 = [sue_str, event7, yao_str, yao_inx, None, None, None]
#     e1_acct1 = [sue_str, event7, bob_str, bob_inx, None, None, None]
#     e1_acct_rows = [e1_acct0, e1_acct1]
#     e1_acct_agg_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
#     pandas_testing_assert_frame_equal(gen_acct_agg_df, e1_acct_agg_df)


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
