from src.f00_instrument.file import open_json, save_json, count_dirs_files
from src.f01_road.allot import allot_nested_scale
from src.f05_listen.cell import cellunit_shop
from src.f05_listen.hub_path import (
    CELL_MANDATE_FILENAME,
    create_cell_dir_path as cell_dir,
    create_cell_acct_mandate_ledger_path as cell_mandate_path,
    create_deal_acct_mandate_ledger_path as deal_mandate_path,
    create_fisc_json_path,
)
from src.f05_listen.hub_tool import cellunit_save_to_dir
from src.f07_fisc.fisc import fiscunit_shop
from src.f07_fisc.fisc_tool import create_deal_mandate_ledgers
from src.f11_world.examples.example_worlds import (
    get_bob_mop_with_reason_budunit_example,
)
from src.f07_fisc.examples.fisc_env import env_dir_setup_cleanup, get_test_fisc_mstr_dir
from os.path import exists as os_path_exists


def test_WorldUnit_create_deal_mandate_ledgers_Scenaro0_DealEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    mstr_dir = get_test_fisc_mstr_dir()
    accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
    a23_json_path = create_fisc_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, accord23_fisc.get_dict())
    bob_str = "Bob"
    timepoint9 = 9
    bob9_deal_mandate_path = deal_mandate_path(mstr_dir, a23_str, bob_str, timepoint9)
    assert os_path_exists(bob9_deal_mandate_path) is False

    # WHEN
    create_deal_mandate_ledgers(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob9_deal_mandate_path) is False


def test_WorldUnit_create_deals_root_cells_Scenaro1_DealExists(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    mstr_dir = get_test_fisc_mstr_dir()
    accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    tp37 = 37
    deal1_quota = 450
    accord23_fisc.add_dealunit(bob_str, tp37, deal1_quota)
    a23_json_path = create_fisc_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, accord23_fisc.get_dict())
    bob37_cell_mandate_path = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    bob_mandate = 777
    assert deal1_quota != bob_mandate
    save_json(bob37_cell_mandate_path, None, {bob_str: bob_mandate})
    bob37_deal_mandate_path = deal_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_deal_mandate_path) is False

    # WHEN
    create_deal_mandate_ledgers(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob37_deal_mandate_path)
    assert open_json(bob37_deal_mandate_path) == {bob_str: deal1_quota}
