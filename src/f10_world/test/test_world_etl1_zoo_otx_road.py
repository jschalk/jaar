from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    face_id_str,
    fiscal_id_str,
    road_str,
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
from src.f09_brick.pandas_tool import get_sheet_names
from src.f10_world.world import worldunit_shop
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, ExcelWriter, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


# def test_WorldUnit_zoo_agg_to_road_staging_CreatesFile_Scenario0_SingleBrick(
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
#         road_str(),
#         otx_road_str(),
#         inx_road_str(),
#     ]
#     sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
#     b113_rows = [sue0, sue1]
#     br00113_df = DataFrame(b113_rows, columns=br00113_columns)
#     with ExcelWriter(br00113_file_path) as writer:
#         br00113_df.to_excel(writer, sheet_name="zoo_agg", index=False)
#     pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
#     fizz_world.zoo_agg_to_zoo_events()
#     fizz_world.zoo_events_to_events_log()
#     fizz_world.events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg()
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.zoo_agg_to_road_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     road_staging_str = "road_staging"
#     gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)
#     road_file_columns = [
#         "src_brick",
#         face_id_str(),
#         event_id_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_road_df.columns) == road_file_columns
#     assert len(gen_road_df) == 2
#     bx = "br00113"
#     e1_road0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
#     e1_road1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
#     e1_road_rows = [e1_road0, e1_road1]
#     e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
#     assert len(gen_road_df) == len(e1_road_df)
#     print(f"{gen_road_df.to_csv()=}")
#     print(f" {e1_road_df.to_csv()=}")
#     assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
#     assert get_sheet_names(pidgin_path) == [road_staging_str]


# def test_WorldUnit_zoo_agg_to_road_staging_CreatesFile_Scenario1_MultipleBricksFiles(
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
#         road_str(),
#         otx_road_str(),
#         inx_road_str(),
#     ]
#     br00043_file_path = create_path(fizz_world._zoo_dir, "br00043.xlsx")
#     br00043_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
#     b113_rows = [sue0, sue1]
#     br00113_df = DataFrame(b113_rows, columns=br00113_columns)
#     with ExcelWriter(br00113_file_path) as writer:
#         br00113_df.to_excel(writer, sheet_name="zoo_agg", index=False)
#     b40_rows = [sue2, sue3, yao1]
#     br00043_df = DataFrame(b40_rows, columns=br00043_columns)
#     with ExcelWriter(br00043_file_path) as writer:
#         br00043_df.to_excel(writer, sheet_name="zoo_agg", index=False)
#     pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
#     fizz_world.zoo_agg_to_zoo_events()
#     fizz_world.zoo_events_to_events_log()
#     fizz_world.events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg()
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.zoo_agg_to_road_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     road_staging_str = "road_staging"
#     gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)
#     road_file_columns = [
#         "src_brick",
#         face_id_str(),
#         event_id_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_road_df.columns) == road_file_columns
#     assert len(gen_road_df) == 5
#     b3 = "br00113"
#     b4 = "br00043"
#     e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_road5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
#     e1_road0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
#     e1_road1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

#     e1_road_rows = [e1_road3, e1_road4, e1_road5, e1_road0, e1_road1]
#     e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
#     assert len(gen_road_df) == len(e1_road_df)
#     print(f"{gen_road_df.to_csv()=}")
#     print(f" {e1_road_df.to_csv()=}")
#     assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
#     assert get_sheet_names(pidgin_path) == [road_staging_str]


# def test_WorldUnit_zoo_agg_to_road_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
#         road_str(),
#         otx_road_str(),
#         inx_road_str(),
#     ]
#     br00043_file_path = create_path(fizz_world._zoo_dir, "br00043.xlsx")
#     br00043_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     b113_rows = [sue0, sue1]
#     br00113_df = DataFrame(b113_rows, columns=br00113_columns)
#     with ExcelWriter(br00113_file_path) as writer:
#         br00113_df.to_excel(writer, sheet_name="zoo_agg", index=False)
#     b40_rows = [sue2, sue3, yao1]
#     br00043_df = DataFrame(b40_rows, columns=br00043_columns)
#     with ExcelWriter(br00043_file_path) as writer:
#         br00043_df.to_excel(writer, sheet_name="zoo_agg", index=False)
#     pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
#     assert fizz_world.events == {}
#     fizz_world.zoo_agg_to_zoo_events()
#     fizz_world.zoo_events_to_events_log()
#     fizz_world.events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg()
#     assert fizz_world.events == {event2: sue_str, event5: sue_str}
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.zoo_agg_to_road_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     road_staging_str = "road_staging"
#     gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)
#     road_file_columns = [
#         "src_brick",
#         face_id_str(),
#         event_id_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_road_df.columns) == road_file_columns
#     assert len(gen_road_df) == 2
#     b3 = "br00113"
#     b4 = "br00043"
#     e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_road_rows = [e1_road3, e1_road4]
#     e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
#     assert len(gen_road_df) == len(e1_road_df)
#     print(f"{gen_road_df.to_csv()=}")
#     print(f" {e1_road_df.to_csv()=}")
#     assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
#     assert get_sheet_names(pidgin_path) == [road_staging_str]
