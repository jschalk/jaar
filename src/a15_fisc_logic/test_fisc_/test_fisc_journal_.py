from src.a00_data_toolboxs.dict_toolbox import get_from_nested_dict
from src.a00_data_toolboxs.file_toolbox import (
    delete_dir,
    save_file,
    open_file,
    open_json,
    create_path,
)
from src.a00_data_toolboxs.db_toolbox import (
    get_db_tables,
    get_db_columns,
    check_connection,
    check_table_column_existence,
)
from src.a15_fisc_logic.fisc import FiscUnit, fiscunit_shop
from src.a15_fisc_logic.examples.fisc_env import (
    get_test_fisc_mstr_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_FiscUnit_get_journal_db_path_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = FiscUnit(
        fisc_tag=accord45_str, fisc_mstr_dir=get_test_fisc_mstr_dir()
    )

    # WHEN
    x_journal_db_path = accord_fisc.get_journal_db_path()

    # THEN
    fiscs_dir = create_path(get_test_fisc_mstr_dir(), "fiscs")
    x_fisc_dir = create_path(fiscs_dir, accord45_str)
    journal_filename = "journal.db"
    assert x_journal_db_path == create_path(x_fisc_dir, journal_filename)


def test_FiscUnit_create_journal_db_CreatesDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(
        fisc_tag=accord45_str, fisc_mstr_dir=get_test_fisc_mstr_dir()
    )
    assert os_path_exists(accord_fisc.get_journal_db_path())
    delete_dir(accord_fisc.get_journal_db_path())
    assert os_path_exists(accord_fisc.get_journal_db_path()) is False

    # WHEN
    accord_fisc._create_journal_db()

    # THEN
    assert os_path_exists(accord_fisc.get_journal_db_path())


def test_FiscUnit_create_journal_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(
        fisc_tag=accord45_str, fisc_mstr_dir=get_test_fisc_mstr_dir()
    )
    delete_dir(dir=accord_fisc.get_journal_db_path())  # clear out any treasury.db file
    accord_fisc._create_journal_db()
    assert os_path_exists(accord_fisc.get_journal_db_path())

    # SETUP
    x_file_str = "Texas Dallas ElPaso"
    db_file = "journal.db"
    save_file(accord_fisc._fisc_dir, db_file, file_str=x_file_str, replace=True)
    assert os_path_exists(accord_fisc.get_journal_db_path())
    assert open_file(accord_fisc._fisc_dir, filename=db_file) == x_file_str

    # WHEN
    accord_fisc._create_journal_db()
    # THEN
    assert open_file(accord_fisc._fisc_dir, filename=db_file) == x_file_str

    # # WHEN
    # accord_fisc._create_journal_db(overwrite=True)
    # # THEN
    # assert open_file(accord_fisc._fisc_dir, filename=db_file) != x_file_str


def test_FiscUnit_create_journal_db_CanCreateInMemory(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(
        fisc_tag=accord45_str,
        fisc_mstr_dir=get_test_fisc_mstr_dir(),
        in_memory_journal=True,
    )

    accord_fisc._journal_db = None
    assert not accord_fisc._journal_db
    assert os_path_exists(accord_fisc.get_journal_db_path()) is False

    # WHEN
    accord_fisc._create_journal_db(in_memory=True)

    # THEN
    assert accord_fisc._journal_db is not None
    assert os_path_exists(accord_fisc.get_journal_db_path()) is False


def test_FiscUnit_get_journal_conn_CreatesTreasuryDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH create fisc
    x_fisc = FiscUnit("accord23", get_test_fisc_mstr_dir())
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_fisc.get_journal_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_fisc._set_fisc_dirs(in_memory_journal=True)

    # THEN
    assert check_connection(x_fisc.get_journal_conn())


def test_fisc_set_fisc_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # ESTABLISH create fisc
    x_fisc = fiscunit_shop("accord23", get_test_fisc_mstr_dir())

    # WHEN
    x_fisc._set_fisc_dirs(in_memory_journal=True)

    # THEN
    # grab config.json
    config_dict = open_json(
        dest_dir="src/a15_fisc_logic", filename="journal_db_check.json"
    )
    tables_dict = get_from_nested_dict(config_dict, ["tables"])
    print(f"{tables_dict=}")

    with x_fisc.get_journal_conn() as journal_conn:
        assert check_table_column_existence(tables_dict, journal_conn)
