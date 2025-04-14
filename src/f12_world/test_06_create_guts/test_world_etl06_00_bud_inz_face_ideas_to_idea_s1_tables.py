from src.f00_instrument.file_toolbox import create_path, save_file
from src.f01_road.deal import fisc_title_str
from src.f04_kick.atom_config import face_name_str, event_int_str, acct_name_str
from src.f12_world.world import worldunit_shop
from src.f12_world.examples.world_env import env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect


# def test_WorldUnit_inz_face_csv_files2idea_staging_tables_HasIdeaDataFromCSV(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_inx = "Suzy"
#     bob_inx = "Bob"
#     yao_inx = "Yao"
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     fizz_world = worldunit_shop("fizz")
#     sue_inz_dir = create_path(fizz_world._faces_inz_dir, sue_inx)
#     br00011_str = "br00011"
#     br00011_csv_filename = f"{br00011_str}.csv"
#     br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()}
# {sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
# {sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
# {sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
# {sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
# """
#     save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)
#     print(f"{sue_inz_dir=}")
#     fizz_world = worldunit_shop("fizz")

#     # WHEN / THEN
#     br00011_staging_tablename = f"{br00011_str}_staging"
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         fizz_world.inz_face_csv_files2idea_staging_tables(fisc_db_conn)
#         assert fisc_db_conn != None
#         cursor = fisc_db_conn.cursor()
#         cursor.execute(f"PRAGMA table_info({br00011_staging_tablename})")
#         br00011_db_columns = cursor.fetchall()
#         br00011_expected_columns = [
#             (0, face_name_str(), "TEXT", 0, None, 0),
#             (1, event_int_str(), "INTEGER", 0, None, 0),
#             (2, fisc_title_str(), "TEXT", 0, None, 0),
#             (3, owner_name_str(), "TEXT", 0, None, 0),
#             (4, acct_name_str(), "TEXT", 0, None, 0),
#         ]
#         print(f"{type(fisc_db_conn)=}")
#         print(f"      {br00011_db_columns=}")
#         print(f"{br00011_expected_columns=}")
#         assert br00011_db_columns == br00011_expected_columns
#         cursor.execute(f"SELECT * FROM {br00011_staging_tablename}")
#         br00011_db_rows = cursor.fetchall()
#         expected_data = [
#             (sue_inx, event3, accord23_str, bob_inx, bob_inx),
#             (sue_inx, event3, accord23_str, yao_inx, bob_inx),
#             (sue_inx, event3, accord23_str, yao_inx, yao_inx),
#             (sue_inx, event7, accord23_str, yao_inx, yao_inx),
#         ]
#         assert br00011_db_rows == expected_data

# already tested in test_world_etl05_00_inz_face_ideas_to_idea_staging_tables
