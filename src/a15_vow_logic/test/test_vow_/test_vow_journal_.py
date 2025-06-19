from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.a00_data_toolbox.db_toolbox import (
    check_connection,
    check_table_column_existence,
    get_db_columns,
    get_db_tables,
)
from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    delete_dir,
    open_file,
    open_json,
    save_file,
)
from src.a15_vow_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_vow_logic.vow import VowUnit, vowunit_shop


def test_VowUnit_get_journal_db_path_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = VowUnit(vow_label=accord45_str, vow_mstr_dir=get_module_temp_dir())

    # WHEN
    x_journal_db_path = accord_vow.get_journal_db_path()

    # THEN
    vows_dir = create_path(get_module_temp_dir(), "vows")
    x_vow_dir = create_path(vows_dir, accord45_str)
    journal_filename = "journal.db"
    assert x_journal_db_path == create_path(x_vow_dir, journal_filename)


def test_VowUnit_create_journal_db_CreatesDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(
        vow_label=accord45_str, vow_mstr_dir=get_module_temp_dir()
    )
    assert os_path_exists(accord_vow.get_journal_db_path())
    delete_dir(accord_vow.get_journal_db_path())
    assert os_path_exists(accord_vow.get_journal_db_path()) is False

    # WHEN
    accord_vow._create_journal_db()

    # THEN
    assert os_path_exists(accord_vow.get_journal_db_path())


def test_VowUnit_create_journal_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(
        vow_label=accord45_str, vow_mstr_dir=get_module_temp_dir()
    )
    delete_dir(dir=accord_vow.get_journal_db_path())  # clear out any treasury.db file
    accord_vow._create_journal_db()
    assert os_path_exists(accord_vow.get_journal_db_path())

    # SETUP
    x_file_str = "Texas Dallas ElPaso"
    db_file = "journal.db"
    save_file(accord_vow._vow_dir, db_file, file_str=x_file_str, replace=True)
    assert os_path_exists(accord_vow.get_journal_db_path())
    assert open_file(accord_vow._vow_dir, filename=db_file) == x_file_str

    # WHEN
    accord_vow._create_journal_db()
    # THEN
    assert open_file(accord_vow._vow_dir, filename=db_file) == x_file_str

    # # WHEN
    # accord_vow._create_journal_db(overwrite=True)
    # # THEN
    # assert open_file(accord_vow._vow_dir, filename=db_file) != x_file_str


def test_VowUnit_create_journal_db_CanCreateInMemory(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(
        vow_label=accord45_str,
        vow_mstr_dir=get_module_temp_dir(),
        in_memory_journal=True,
    )

    accord_vow._journal_db = None
    assert not accord_vow._journal_db
    assert os_path_exists(accord_vow.get_journal_db_path()) is False

    # WHEN
    accord_vow._create_journal_db(in_memory=True)

    # THEN
    assert accord_vow._journal_db is not None
    assert os_path_exists(accord_vow.get_journal_db_path()) is False


def test_VowUnit_get_journal_conn_CreatesTreasuryDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH create vow
    x_vow = VowUnit("accord23", get_module_temp_dir())
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_vow.get_journal_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_vow._set_vow_dirs(in_memory_journal=True)

    # THEN
    assert check_connection(x_vow.get_journal_conn())


def test_vow_set_vow_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # ESTABLISH create vow
    x_vow = vowunit_shop("accord23", get_module_temp_dir())

    # WHEN
    x_vow._set_vow_dirs(in_memory_journal=True)

    # THEN
    # grab config.json
    config_dict = open_json(
        dest_dir="src/a15_vow_logic", filename="journal_db_check.json"
    )
    tables_dict = get_from_nested_dict(config_dict, ["tables"])
    print(f"{tables_dict=}")

    with x_vow.get_journal_conn() as journal_conn:
        assert check_table_column_existence(tables_dict, journal_conn)
