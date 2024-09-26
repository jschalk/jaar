from src.f0_instrument.python_tool import get_dict_from_json, get_nested_value
from src.f0_instrument.file import delete_dir, save_file, open_file
from src.f0_instrument.db_tool import (
    get_db_tables,
    get_db_columns,
    check_connection,
    check_table_column_existence,
)
from src.f1_road.jaar_config import get_fiscal_id_if_None
from src.f7_fiscal.fiscal import FiscalUnit, fiscalunit_shop
from src.f7_fiscal.examples.fiscal_env import (
    get_test_fiscals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_FiscalUnit_get_journal_db_path_ReturnsCorrectObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = FiscalUnit(fiscal_id=music_str, fiscals_dir=get_test_fiscals_dir())

    # WHEN
    x_journal_db_path = music_fiscal.get_journal_db_path()

    # THEN
    x_fiscal_dir = f"{get_test_fiscals_dir()}/{music_str}"
    journal_file_name = "journal.db"
    assert x_journal_db_path == f"{x_fiscal_dir}/{journal_file_name}"


def test_FiscalUnit_create_journal_db_CreatesDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(
        fiscal_id=music_str, fiscals_dir=get_test_fiscals_dir()
    )
    assert os_path_exists(music_fiscal.get_journal_db_path())
    delete_dir(music_fiscal.get_journal_db_path())
    assert os_path_exists(music_fiscal.get_journal_db_path()) is False

    # WHEN
    music_fiscal._create_journal_db()

    # THEN
    assert os_path_exists(music_fiscal.get_journal_db_path())


def test_FiscalUnit_create_journal_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(
        fiscal_id=music_str, fiscals_dir=get_test_fiscals_dir()
    )
    delete_dir(dir=music_fiscal.get_journal_db_path())  # clear out any treasury.db file
    music_fiscal._create_journal_db()
    assert os_path_exists(music_fiscal.get_journal_db_path())

    # SETUP
    x_file_str = "Texas Dallas ElPaso"
    db_file = "journal.db"
    save_file(music_fiscal._fiscal_dir, db_file, file_str=x_file_str, replace=True)
    assert os_path_exists(music_fiscal.get_journal_db_path())
    assert open_file(music_fiscal._fiscal_dir, file_name=db_file) == x_file_str

    # WHEN
    music_fiscal._create_journal_db()
    # THEN
    assert open_file(music_fiscal._fiscal_dir, file_name=db_file) == x_file_str

    # # WHEN
    # music_fiscal._create_journal_db(overwrite=True)
    # # THEN
    # assert open_file(music_fiscal._fiscal_dir, file_name=db_file) != x_file_str


def test_FiscalUnit_create_journal_db_CanCreateInMemory(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(
        fiscal_id=music_str, fiscals_dir=get_test_fiscals_dir(), in_memory_journal=True
    )

    music_fiscal._journal_db = None
    assert music_fiscal._journal_db is None
    assert os_path_exists(music_fiscal.get_journal_db_path()) is False

    # WHEN
    music_fiscal._create_journal_db(in_memory=True)

    # THEN
    assert music_fiscal._journal_db is not None
    assert os_path_exists(music_fiscal.get_journal_db_path()) is False


def test_FiscalUnit_get_journal_conn_CreatesTreasuryDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH create Fiscal
    x_fiscal = FiscalUnit(get_fiscal_id_if_None(), get_test_fiscals_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_fiscal.get_journal_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_fiscal._set_fiscal_dirs(in_memory_journal=True)

    # THEN
    assert check_connection(x_fiscal.get_journal_conn())


def test_fiscal_set_fiscal_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # ESTABLISH create fiscal
    x_fiscal = fiscalunit_shop(get_fiscal_id_if_None(), get_test_fiscals_dir())

    # WHEN
    x_fiscal._set_fiscal_dirs(in_memory_journal=True)

    # THEN
    # grab config.json
    config_str = open_file(dest_dir="src/f7_fiscal", file_name="journal_db_check.json")
    config_dict = get_dict_from_json(config_str)
    tables_dict = get_nested_value(config_dict, ["tables"])
    print(f"{tables_dict=}")

    with x_fiscal.get_journal_conn() as journal_conn:
        assert check_table_column_existence(tables_dict, journal_conn)
