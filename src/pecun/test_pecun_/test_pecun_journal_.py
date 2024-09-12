from src._instrument.python_tool import get_dict_from_json, get_nested_value
from src._instrument.file import delete_dir, save_file, open_file
from src._instrument.db_tool import (
    get_db_tables,
    get_db_columns,
    check_connection,
    check_table_column_existence,
)
from src._road.jaar_config import get_pecun_id_if_None
from src.pecun.pecun import PecunUnit, pecununit_shop
from src.pecun.examples.pecun_env import (
    get_test_pecuns_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_PecunUnit_get_journal_db_path_ReturnsCorrectObj():
    # ESTABLISH
    music_str = "music"
    music_pecun = PecunUnit(pecun_id=music_str, pecuns_dir=get_test_pecuns_dir())

    # WHEN
    x_journal_db_path = music_pecun.get_journal_db_path()

    # THEN
    x_pecun_dir = f"{get_test_pecuns_dir()}/{music_str}"
    journal_file_name = "journal.db"
    assert x_journal_db_path == f"{x_pecun_dir}/{journal_file_name}"


def test_PecunUnit_create_journal_db_CreatesDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_str = "music"
    music_pecun = pecununit_shop(pecun_id=music_str, pecuns_dir=get_test_pecuns_dir())
    assert os_path_exists(music_pecun.get_journal_db_path())
    delete_dir(music_pecun.get_journal_db_path())
    assert os_path_exists(music_pecun.get_journal_db_path()) is False

    # WHEN
    music_pecun._create_journal_db()

    # THEN
    assert os_path_exists(music_pecun.get_journal_db_path())


def test_PecunUnit_create_journal_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_str = "music"
    music_pecun = pecununit_shop(pecun_id=music_str, pecuns_dir=get_test_pecuns_dir())
    delete_dir(dir=music_pecun.get_journal_db_path())  # clear out any treasury.db file
    music_pecun._create_journal_db()
    assert os_path_exists(music_pecun.get_journal_db_path())

    # SETUP
    x_file_str = "Texas Dallas ElPaso"
    db_file = "journal.db"
    save_file(music_pecun._pecun_dir, db_file, file_str=x_file_str, replace=True)
    assert os_path_exists(music_pecun.get_journal_db_path())
    assert open_file(music_pecun._pecun_dir, file_name=db_file) == x_file_str

    # WHEN
    music_pecun._create_journal_db()
    # THEN
    assert open_file(music_pecun._pecun_dir, file_name=db_file) == x_file_str

    # # WHEN
    # music_pecun._create_journal_db(overwrite=True)
    # # THEN
    # assert open_file(music_pecun._pecun_dir, file_name=db_file) != x_file_str


def test_PecunUnit_create_journal_db_CanCreateInMemory(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_pecun = pecununit_shop(
        pecun_id=music_str, pecuns_dir=get_test_pecuns_dir(), in_memory_journal=True
    )

    music_pecun._journal_db = None
    assert music_pecun._journal_db is None
    assert os_path_exists(music_pecun.get_journal_db_path()) is False

    # WHEN
    music_pecun._create_journal_db(in_memory=True)

    # THEN
    assert music_pecun._journal_db is not None
    assert os_path_exists(music_pecun.get_journal_db_path()) is False


def test_PecunUnit_get_journal_conn_CreatesTreasuryDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH create Pecun
    x_pecun = PecunUnit(get_pecun_id_if_None(), get_test_pecuns_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_pecun.get_journal_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_pecun._set_pecun_dirs(in_memory_journal=True)

    # THEN
    assert check_connection(x_pecun.get_journal_conn())


def test_pecun_set_pecun_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # ESTABLISH create pecun
    x_pecun = pecununit_shop(get_pecun_id_if_None(), get_test_pecuns_dir())

    # WHEN
    x_pecun._set_pecun_dirs(in_memory_journal=True)

    # THEN
    # grab config.json
    config_str = open_file(dest_dir="src/pecun", file_name="journal_db_check.json")
    config_dict = get_dict_from_json(config_str)
    tables_dict = get_nested_value(config_dict, ["tables"])
    print(f"{tables_dict=}")

    with x_pecun.get_journal_conn() as journal_conn:
        assert check_table_column_existence(tables_dict, journal_conn)
