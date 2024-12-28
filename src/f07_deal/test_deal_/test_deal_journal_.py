from src.f00_instrument.dict_toolbox import get_dict_from_json, get_from_nested_dict
from src.f00_instrument.file import delete_dir, save_file, open_file, create_path
from src.f00_instrument.db_toolbox import (
    get_db_tables,
    get_db_columns,
    check_connection,
    check_table_column_existence,
)
from src.f01_road.jaar_config import get_deal_idea_if_None
from src.f07_deal.deal import DealUnit, dealunit_shop
from src.f07_deal.examples.deal_env import (
    get_test_deals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_DealUnit_get_journal_db_path_ReturnsCorrectObj():
    # ESTABLISH
    accord_str = "accord"
    accord_deal = DealUnit(deal_idea=accord_str, deals_dir=get_test_deals_dir())

    # WHEN
    x_journal_db_path = accord_deal.get_journal_db_path()

    # THEN
    x_deal_dir = create_path(get_test_deals_dir(), accord_str)
    journal_file_name = "journal.db"
    assert x_journal_db_path == create_path(x_deal_dir, journal_file_name)


def test_DealUnit_create_journal_db_CreatesDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord_str = "accord"
    accord_deal = dealunit_shop(deal_idea=accord_str, deals_dir=get_test_deals_dir())
    assert os_path_exists(accord_deal.get_journal_db_path())
    delete_dir(accord_deal.get_journal_db_path())
    assert os_path_exists(accord_deal.get_journal_db_path()) is False

    # WHEN
    accord_deal._create_journal_db()

    # THEN
    assert os_path_exists(accord_deal.get_journal_db_path())


def test_DealUnit_create_journal_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord_str = "accord"
    accord_deal = dealunit_shop(deal_idea=accord_str, deals_dir=get_test_deals_dir())
    delete_dir(dir=accord_deal.get_journal_db_path())  # clear out any treasury.db file
    accord_deal._create_journal_db()
    assert os_path_exists(accord_deal.get_journal_db_path())

    # SETUP
    x_file_str = "Texas Dallas ElPaso"
    db_file = "journal.db"
    save_file(accord_deal._deal_dir, db_file, file_str=x_file_str, replace=True)
    assert os_path_exists(accord_deal.get_journal_db_path())
    assert open_file(accord_deal._deal_dir, file_name=db_file) == x_file_str

    # WHEN
    accord_deal._create_journal_db()
    # THEN
    assert open_file(accord_deal._deal_dir, file_name=db_file) == x_file_str

    # # WHEN
    # accord_deal._create_journal_db(overwrite=True)
    # # THEN
    # assert open_file(accord_deal._deal_dir, file_name=db_file) != x_file_str


def test_DealUnit_create_journal_db_CanCreateInMemory(env_dir_setup_cleanup):
    # ESTABLISH
    accord_str = "accord"
    accord_deal = dealunit_shop(
        deal_idea=accord_str, deals_dir=get_test_deals_dir(), in_memory_journal=True
    )

    accord_deal._journal_db = None
    assert accord_deal._journal_db is None
    assert os_path_exists(accord_deal.get_journal_db_path()) is False

    # WHEN
    accord_deal._create_journal_db(in_memory=True)

    # THEN
    assert accord_deal._journal_db is not None
    assert os_path_exists(accord_deal.get_journal_db_path()) is False


def test_DealUnit_get_journal_conn_CreatesTreasuryDBIfDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH create deal
    x_deal = DealUnit(get_deal_idea_if_None(), get_test_deals_dir())
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_deal.get_journal_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_deal._set_deal_dirs(in_memory_journal=True)

    # THEN
    assert check_connection(x_deal.get_journal_conn())


def test_deal_set_deal_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # ESTABLISH create deal
    x_deal = dealunit_shop(get_deal_idea_if_None(), get_test_deals_dir())

    # WHEN
    x_deal._set_deal_dirs(in_memory_journal=True)

    # THEN
    # grab config.json
    config_str = open_file(dest_dir="src/f07_deal", file_name="journal_db_check.json")
    config_dict = get_dict_from_json(config_str)
    tables_dict = get_from_nested_dict(config_dict, ["tables"])
    print(f"{tables_dict=}")

    with x_deal.get_journal_conn() as journal_conn:
        assert check_table_column_existence(tables_dict, journal_conn)
