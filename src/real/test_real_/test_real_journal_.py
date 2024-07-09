from src._instrument.python import get_dict_from_json, get_nested_value
from src._instrument.file import delete_dir, save_file, open_file
from src._instrument.db_tool import (
    get_db_tables,
    get_db_columns,
    check_connection,
    check_table_column_existence,
)
from src._road.jaar_config import get_test_real_id
from src.real.real import RealUnit, realunit_shop
from src.real.examples.real_env import (
    get_test_reals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_RealUnit_get_journal_db_path_ReturnsCorrectObj():
    # GIVEN
    music_text = "music"
    music_real = RealUnit(real_id=music_text, reals_dir=get_test_reals_dir())

    # WHEN
    x_journal_db_path = music_real.get_journal_db_path()

    # THEN
    x_real_dir = f"{get_test_reals_dir()}/{music_text}"
    journal_file_name = "journal.db"
    assert x_journal_db_path == f"{x_real_dir}/{journal_file_name}"


def test_RealUnit_create_journal_db_CreatesDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(real_id=music_text, reals_dir=get_test_reals_dir())
    assert os_path_exists(music_real.get_journal_db_path())
    delete_dir(music_real.get_journal_db_path())
    assert os_path_exists(music_real.get_journal_db_path()) is False

    # WHEN
    music_real._create_journal_db()

    # THEN
    assert os_path_exists(music_real.get_journal_db_path())


def test_RealUnit_create_journal_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(real_id=music_text, reals_dir=get_test_reals_dir())
    delete_dir(dir=music_real.get_journal_db_path())  # clear out any treasury.db file
    music_real._create_journal_db()
    assert os_path_exists(music_real.get_journal_db_path())

    # SETUP
    x_file_text = "Texas Dallas ElPaso"
    db_file = "journal.db"
    save_file(music_real._real_dir, db_file, file_text=x_file_text, replace=True)
    assert os_path_exists(music_real.get_journal_db_path())
    assert open_file(music_real._real_dir, file_name=db_file) == x_file_text

    # WHEN
    music_real._create_journal_db()
    # THEN
    assert open_file(music_real._real_dir, file_name=db_file) == x_file_text

    # # WHEN
    # music_real._create_journal_db(overwrite=True)
    # # THEN
    # assert open_file(music_real._real_dir, file_name=db_file) != x_file_text


def test_RealUnit_create_journal_db_CanCreateInMemory(env_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(
        real_id=music_text, reals_dir=get_test_reals_dir(), in_memory_journal=True
    )

    music_real._journal_db = None
    assert music_real._journal_db is None
    assert os_path_exists(music_real.get_journal_db_path()) is False

    # WHEN
    music_real._create_journal_db(in_memory=True)

    # THEN
    assert music_real._journal_db != None
    assert os_path_exists(music_real.get_journal_db_path()) is False


def test_RealUnit_get_journal_conn_CreatesTreasuryDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create Real
    x_real = RealUnit(get_test_real_id(), get_test_reals_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_real.get_journal_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_real._set_real_dirs(in_memory_journal=True)

    # THEN
    assert check_connection(x_real.get_journal_conn())


def test_real_set_real_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create real
    x_real = realunit_shop(get_test_real_id(), get_test_reals_dir())

    # WHEN
    x_real._set_real_dirs(in_memory_journal=True)

    # THEN
    # grab config.json
    config_text = open_file(dest_dir="src/real", file_name="journal_db_check.json")
    config_dict = get_dict_from_json(config_text)
    tables_dict = get_nested_value(config_dict, ["tables"])
    print(f"{tables_dict=}")

    with x_real.get_journal_conn() as journal_conn:
        assert check_table_column_existence(tables_dict, journal_conn)
