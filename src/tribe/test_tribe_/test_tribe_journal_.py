from src._instrument.python_tool import get_dict_from_json, get_nested_value
from src._instrument.file import delete_dir, save_file, open_file
from src._instrument.db_tool import (
    get_db_tables,
    get_db_columns,
    check_connection,
    check_table_column_existence,
)
from src._road.jaar_config import get_tribe_id_if_None
from src.tribe.tribe import TribeUnit, tribeunit_shop
from src.tribe.examples.tribe_env import (
    get_test_tribes_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_TribeUnit_get_journal_db_path_ReturnsCorrectObj():
    # ESTABLISH
    music_str = "music"
    music_tribe = TribeUnit(tribe_id=music_str, tribes_dir=get_test_tribes_dir())

    # WHEN
    x_journal_db_path = music_tribe.get_journal_db_path()

    # THEN
    x_tribe_dir = f"{get_test_tribes_dir()}/{music_str}"
    journal_file_name = "journal.db"
    assert x_journal_db_path == f"{x_tribe_dir}/{journal_file_name}"


def test_TribeUnit_create_journal_db_CreatesDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_str = "music"
    music_tribe = tribeunit_shop(tribe_id=music_str, tribes_dir=get_test_tribes_dir())
    assert os_path_exists(music_tribe.get_journal_db_path())
    delete_dir(music_tribe.get_journal_db_path())
    assert os_path_exists(music_tribe.get_journal_db_path()) is False

    # WHEN
    music_tribe._create_journal_db()

    # THEN
    assert os_path_exists(music_tribe.get_journal_db_path())


def test_TribeUnit_create_journal_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_str = "music"
    music_tribe = tribeunit_shop(tribe_id=music_str, tribes_dir=get_test_tribes_dir())
    delete_dir(dir=music_tribe.get_journal_db_path())  # clear out any treasury.db file
    music_tribe._create_journal_db()
    assert os_path_exists(music_tribe.get_journal_db_path())

    # SETUP
    x_file_str = "Texas Dallas ElPaso"
    db_file = "journal.db"
    save_file(music_tribe._tribe_dir, db_file, file_str=x_file_str, replace=True)
    assert os_path_exists(music_tribe.get_journal_db_path())
    assert open_file(music_tribe._tribe_dir, file_name=db_file) == x_file_str

    # WHEN
    music_tribe._create_journal_db()
    # THEN
    assert open_file(music_tribe._tribe_dir, file_name=db_file) == x_file_str

    # # WHEN
    # music_tribe._create_journal_db(overwrite=True)
    # # THEN
    # assert open_file(music_tribe._tribe_dir, file_name=db_file) != x_file_str


def test_TribeUnit_create_journal_db_CanCreateInMemory(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_tribe = tribeunit_shop(
        tribe_id=music_str, tribes_dir=get_test_tribes_dir(), in_memory_journal=True
    )

    music_tribe._journal_db = None
    assert music_tribe._journal_db is None
    assert os_path_exists(music_tribe.get_journal_db_path()) is False

    # WHEN
    music_tribe._create_journal_db(in_memory=True)

    # THEN
    assert music_tribe._journal_db is not None
    assert os_path_exists(music_tribe.get_journal_db_path()) is False


def test_TribeUnit_get_journal_conn_CreatesTreasuryDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH create Tribe
    x_tribe = TribeUnit(get_tribe_id_if_None(), get_test_tribes_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_tribe.get_journal_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_tribe._set_tribe_dirs(in_memory_journal=True)

    # THEN
    assert check_connection(x_tribe.get_journal_conn())


def test_tribe_set_tribe_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # ESTABLISH create tribe
    x_tribe = tribeunit_shop(get_tribe_id_if_None(), get_test_tribes_dir())

    # WHEN
    x_tribe._set_tribe_dirs(in_memory_journal=True)

    # THEN
    # grab config.json
    config_str = open_file(dest_dir="src/tribe", file_name="journal_db_check.json")
    config_dict = get_dict_from_json(config_str)
    tables_dict = get_nested_value(config_dict, ["tables"])
    print(f"{tables_dict=}")

    with x_tribe.get_journal_conn() as journal_conn:
        assert check_table_column_existence(tables_dict, journal_conn)
