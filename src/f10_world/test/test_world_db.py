from src.f00_instrument.file import save_file, delete_dir, create_file_path, open_file
from src.f00_instrument.db_toolbox import check_connection, check_table_column_existence
from src.f00_instrument.dict_toolbox import get_dict_from_json, get_from_nested_dict
from src.f08_filter.filter import filterunit_shop
from src.f10_world.world import WorldUnit, worldunit_shop
from src.f10_world.examples.world_env import (
    get_test_world_id,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists

# The goal of the world function is to allow a single command, pointing at a bunch of directories
# initialize worldunits and output acct metrics such as calendars, financial status, healer status


def test_WorldUnit_set_world_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_world = WorldUnit(world_id=music_str, worlds_dir=get_test_worlds_dir())
    x_world_dir = f"{get_test_worlds_dir()}/{music_str}"
    wrd_file_name = "wrd.db"
    wrd_file_path = f"{x_world_dir}/{wrd_file_name}"
    x_faces_dir = f"{x_world_dir}/faces"

    assert music_world._world_dir is None
    assert music_world._faces_dir is None
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_faces_dir) is False

    # WHEN
    music_world._set_world_dirs()

    # THEN
    assert music_world._world_dir == x_world_dir
    assert music_world._faces_dir == x_faces_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_faces_dir)


def test_WorldUnit_get_db_path_ReturnsCorrectObj():
    # ESTABLISH
    music_str = "music"
    music_world = WorldUnit(world_id=music_str, worlds_dir=get_test_worlds_dir())

    # WHEN
    x_db_path = music_world.get_db_path()

    # THEN
    x_world_dir = f"{get_test_worlds_dir()}/{music_str}"
    file_name = "wrd.db"
    assert x_db_path == f"{x_world_dir}/{file_name}"


# def test_WorldUnit_create_db_CreatesDBIfDoesNotExist(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     music_str = "music"
#     music_world = worldunit_shop(world_id=music_str, worlds_dir=get_test_worlds_dir())
#     assert os_path_exists(music_world.get_db_path())
#     delete_dir(music_world.get_db_path())
#     assert os_path_exists(music_world.get_db_path()) is False

#     # WHEN
#     music_world._create_db(in_memory=False)

#     # THEN
#     assert os_path_exists(music_world.get_db_path())


# def test_WorldUnit_create_db_DoesNotOverWriteDBIfExists(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     music_str = "music"
#     music_world = worldunit_shop(world_id=music_str, worlds_dir=get_test_worlds_dir())
#     delete_dir(dir=music_world.get_db_path())  # clear out any treasury.db file
#     music_world._create_db(in_memory=False)
#     assert os_path_exists(music_world.get_db_path())

#     # SETUP
#     x_file_str = "Texas Dallas ElPaso"
#     db_file = "wrd.db"
#     save_file(music_world._world_dir, db_file, file_str=x_file_str, replace=True)
#     assert os_path_exists(music_world.get_db_path())
#     assert open_file(music_world._world_dir, file_name=db_file) == x_file_str

#     # WHEN
#     music_world._create_db(in_memory=False)
#     # THEN
#     assert open_file(music_world._world_dir, file_name=db_file) == x_file_str

#     # # WHEN
#     # music_world._create_db(overwrite=True)
#     # # THEN
#     # assert open_file(music_world._world_dir, file_name=db_file) != x_file_str


# def test_WorldUnit_create_db_CanCreateInMemory(env_dir_setup_cleanup):
#     # ESTABLISH
#     music_str = "music"
#     music_world = worldunit_shop(music_str, get_test_worlds_dir(), in_memory_db=True)

#     music_world._db = None
#     assert music_world._db is None
#     assert os_path_exists(music_world.get_db_path()) is False

#     # WHEN
#     music_world._create_db(in_memory=True)

#     # THEN
#     assert music_world._db is not None
#     assert os_path_exists(music_world.get_db_path()) is False


# def test_WorldUnit_get_conn_CreatesWrdDBIfDoesNotExist(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = WorldUnit("fizz", worlds_dir=get_test_worlds_dir())
#     print(f"{fizz_world.get_db_path()=}")
#     assert os_path_exists(fizz_world.get_db_path()) is False

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         check_connection(fizz_world.get_conn())
#     assert str(excinfo.value) == "unable to open database file"

#     # WHEN
#     fizz_world._set_world_dirs(in_memory=True)

#     # THEN
#     assert check_connection(fizz_world.get_conn())


# def test_world_set_world_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
#     # ESTABLISH
#     # create db in memory, check each table has the columns it needs
#     x_world = worldunit_shop(get_test_world_id(), get_test_worlds_dir())
#     # grab config.json
#     tables_dict = {"fan": {}}

#     # WHEN
#     x_world._set_world_dirs(in_memory=True)

#     # THEN
#     with x_world.get_conn() as conn:
#         assert check_table_column_existence(tables_dict, conn)


# def test_WorldUnit_set_face_id_SetsAttr_Scenario0():
#     # ESTABLISH
#     x_world = worldunit_shop()
#     assert x_world.faces == {}

#     # WHEN
#     sue_str = "Sue"
#     sue_filterunit = filterunit_shop(sue_str)
#     x_world.set_face_id(sue_str, sue_filterunit)

#     # THEN
#     assert x_world.faces != {}
#     assert x_world.faces == {sue_str: sue_filterunit}
