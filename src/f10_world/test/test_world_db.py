# from src.f00_instrument.file import save_file, delete_dir, create_path, open_file
# from src.f00_instrument.db_toolbox import check_connection, check_table_column_existence
# from src.f00_instrument.dict_toolbox import get_dict_from_json, get_from_nested_dict
# from src.f08_pidgin.pidgin import pidginunit_shop
# from src.f09_brick.examples.brick_df_examples import get_ex1_br00001_df
from src.f10_world.world import WorldUnit, worldunit_shop
from src.f10_world.examples.world_env import (
    get_test_world_id,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import read_sql_table
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists

# The goal of the world function is to allow a single command, pointing at a bunch of directories
# initialize worldunits and output acct metrics such as calendars, financial status, healer status


def test_WorldUnit_set_world_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = WorldUnit(world_id=fizz_str, worlds_dir=get_test_worlds_dir())
    x_world_dir = f"{get_test_worlds_dir()}/{fizz_str}"
    x_events_dir = f"{x_world_dir}/events"
    x_pidgins_dir = f"{x_world_dir}/pidgins"
    x_jungle_dir = f"{x_world_dir}/jungle"
    x_zoo_dir = f"{x_world_dir}/zoo"

    assert fizz_world._world_dir is None
    assert fizz_world._events_dir is None
    assert fizz_world._pidgins_dir is None
    assert fizz_world._jungle_dir is None
    assert fizz_world._zoo_dir is None
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_events_dir) is False
    assert os_path_exists(x_pidgins_dir) is False
    assert os_path_exists(x_jungle_dir) is False
    assert os_path_exists(x_zoo_dir) is False

    # WHEN
    fizz_world._set_world_dirs()

    # THEN
    assert fizz_world._world_dir == x_world_dir
    assert fizz_world._events_dir == x_events_dir
    assert fizz_world._pidgins_dir == x_pidgins_dir
    assert fizz_world._jungle_dir == x_jungle_dir
    assert fizz_world._zoo_dir == x_zoo_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_events_dir)
    assert os_path_exists(x_pidgins_dir)
    assert os_path_exists(x_jungle_dir)
    assert os_path_exists(x_zoo_dir)


# def test_WorldUnit_get_db_path_ReturnsCorrectObj():
#     # ESTABLISH
#     fizz_str = "fizz"
#     fizz_world = WorldUnit(world_id=fizz_str, worlds_dir=get_test_worlds_dir())
#     fizz_world._world_dir = create_path(fizz_world.worlds_dir, fizz_str)

#     # WHEN
#     x_db_path = fizz_world.get_db_path()

#     # THEN
#     x_world_dir = f"{get_test_worlds_dir()}/{fizz_str}"
#     file_name = "wrd.db"
#     assert x_db_path == f"{x_world_dir}/{file_name}"


# def test_WorldUnit_create_wrd_db_CreatesDBFile(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_str = "fizz"
#     fizz_world = worldunit_shop(fizz_str, get_test_worlds_dir())
#     assert os_path_exists(fizz_world.get_db_path()) is False

#     # WHEN
#     fizz_world._create_wrd_db()
#     # THEN
#     assert os_path_exists(fizz_world.get_db_path())


# def test_WorldUnit_db_exists_ReturnsObj(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_str = "fizz"
#     fizz_world = worldunit_shop(fizz_str, get_test_worlds_dir())
#     assert os_path_exists(fizz_world.get_db_path()) is False
#     assert fizz_world.db_exists() is False

#     # WHEN
#     fizz_world._create_wrd_db()
#     # THEN
#     assert os_path_exists(fizz_world.get_db_path())
#     assert fizz_world.db_exists()


# def test_WorldUnit_get_engine_CreatesWrdDBIfDoesNotExist(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz", worlds_dir=get_test_worlds_dir())
#     assert fizz_world.db_exists() is False

#     # WHEN
#     fizz_world.get_db_engine()
#     # THEN
#     assert fizz_world.db_exists()

#     # WHEN
#     fizz_world.get_db_engine()
#     # THEN
#     assert fizz_world.db_exists()


# def test_WorldUnit_insert_brick_into_wrd_db_CorrectChangesDB():
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz", get_test_worlds_dir())
#     # get brick dataframe
#     x_df = get_ex1_br00001_df()
#     x_df["face_id"] = "Sue"
#     x_df["event_id"] = 2
#     engine = fizz_world.get_db_engine()

#     brick_number = "br00001"
#     x_table = "br00001_hold"

#     # WHEN
#     with engine.connect() as conn:
#         assert len(read_sql_table(x_table, conn)) == 0
#         x_df.to_sql(
#             name=x_table,
#             con=conn,
#             if_exists="append",
#             index=False,
#             schema=fizz_world.get_db_path(),
#         )
#         assert len(read_sql_table(x_table, conn)) == 1

#     with engine.connect() as conn:
#         assert len(read_sql_table(x_table, conn)) == 1

#     # THEN
#     assert 1 == 2
