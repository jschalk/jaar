from src.f00_instrument.dict_toolbox import get_dict_from_json, get_from_nested_dict
from src.f00_instrument.file import delete_dir, save_file, open_file, create_path
from src.f00_instrument.db_toolbox import (
    get_db_tables,
    get_db_columns,
    check_connection,
    check_table_column_existence,
)
from src.f01_road.jaar_config import get_fiscal_title_if_None
from src.f07_fiscal.fiscal import FiscalUnit, fiscalunit_shop
from src.f07_fiscal.examples.fiscal_env import (
    get_test_fiscals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_FiscalUnit_get_journal_db_path_ReturnsCorrectObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fiscal = FiscalUnit(
        fiscal_title=accord45_str, fiscals_dir=get_test_fiscals_dir()
    )

    # WHEN
    x_journal_db_path = accord_fiscal.get_journal_db_path()

    # THEN
    x_fiscal_dir = create_path(get_test_fiscals_dir(), accord45_str)
    journal_file_name = "journal.db"
    assert x_journal_db_path == create_path(x_fiscal_dir, journal_file_name)


def test_FiscalUnit_create_journal_db_CreatesDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord45_str = "accord45"
    accord_fiscal = fiscalunit_shop(
        fiscal_title=accord45_str, fiscals_dir=get_test_fiscals_dir()
    )
    assert os_path_exists(accord_fiscal.get_journal_db_path())
    delete_dir(accord_fiscal.get_journal_db_path())
    assert os_path_exists(accord_fiscal.get_journal_db_path()) is False

    # WHEN
    accord_fiscal._create_journal_db()

    # THEN
    assert os_path_exists(accord_fiscal.get_journal_db_path())


def test_FiscalUnit_create_journal_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord45_str = "accord45"
    accord_fiscal = fiscalunit_shop(
        fiscal_title=accord45_str, fiscals_dir=get_test_fiscals_dir()
    )
    delete_dir(
        dir=accord_fiscal.get_journal_db_path()
    )  # clear out any treasury.db file
    accord_fiscal._create_journal_db()
    assert os_path_exists(accord_fiscal.get_journal_db_path())

    # SETUP
    x_file_str = "Texas Dallas ElPaso"
    db_file = "journal.db"
    save_file(accord_fiscal._fiscal_dir, db_file, file_str=x_file_str, replace=True)
    assert os_path_exists(accord_fiscal.get_journal_db_path())
    assert open_file(accord_fiscal._fiscal_dir, file_name=db_file) == x_file_str

    # WHEN
    accord_fiscal._create_journal_db()
    # THEN
    assert open_file(accord_fiscal._fiscal_dir, file_name=db_file) == x_file_str

    # # WHEN
    # accord_fiscal._create_journal_db(overwrite=True)
    # # THEN
    # assert open_file(accord_fiscal._fiscal_dir, file_name=db_file) != x_file_str


def test_FiscalUnit_create_journal_db_CanCreateInMemory(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    accord_fiscal = fiscalunit_shop(
        fiscal_title=accord45_str,
        fiscals_dir=get_test_fiscals_dir(),
        in_memory_journal=True,
    )

    accord_fiscal._journal_db = None
    assert accord_fiscal._journal_db is None
    assert os_path_exists(accord_fiscal.get_journal_db_path()) is False

    # WHEN
    accord_fiscal._create_journal_db(in_memory=True)

    # THEN
    assert accord_fiscal._journal_db is not None
    assert os_path_exists(accord_fiscal.get_journal_db_path()) is False


def test_FiscalUnit_get_journal_conn_CreatesTreasuryDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH create fiscal
    x_fiscal = FiscalUnit(get_fiscal_title_if_None(), get_test_fiscals_dir())
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_fiscal.get_journal_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_fiscal._set_fiscal_dirs(in_memory_journal=True)

    # THEN
    assert check_connection(x_fiscal.get_journal_conn())


def test_fiscal_set_fiscal_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # ESTABLISH create fiscal
    x_fiscal = fiscalunit_shop(get_fiscal_title_if_None(), get_test_fiscals_dir())

    # WHEN
    x_fiscal._set_fiscal_dirs(in_memory_journal=True)

    # THEN
    # grab config.json
    config_str = open_file(dest_dir="src/f07_fiscal", file_name="journal_db_check.json")
    config_dict = get_dict_from_json(config_str)
    tables_dict = get_from_nested_dict(config_dict, ["tables"])
    print(f"{tables_dict=}")

    with x_fiscal.get_journal_conn() as journal_conn:
        assert check_table_column_existence(tables_dict, journal_conn)
