from src.a00_data_toolboxs.file_toolbox import open_json, save_json
from src.a12_hub_tools.hub_path import (
    create_cell_acct_mandate_ledger_path as cell_mandate_path,
    create_deal_acct_mandate_ledger_path as deal_mandate_path,
    create_fisc_json_path,
)
from src.a15_fisc_logic.fisc import (
    fiscunit_shop,
    get_from_dict as fiscunit_get_from_dict,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_create_deal_mandate_ledgers_Scenaro0_DealEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    a23_str = "accord23"
    mstr_dir = fizz_world._fisc_mstr_dir
    accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
    a23_json_path = create_fisc_json_path(fizz_world._fisc_mstr_dir, a23_str)
    save_json(a23_json_path, None, accord23_fisc.get_dict())
    bob_str = "Bob"
    timepoint9 = 9
    bob9_deal_mandate_path = deal_mandate_path(mstr_dir, a23_str, bob_str, timepoint9)
    assert os_path_exists(bob9_deal_mandate_path) is False

    # WHEN
    fizz_world.create_deal_mandate_ledgers()

    # THEN
    assert os_path_exists(bob9_deal_mandate_path) is False


def test_WorldUnit_create_deals_root_cells_Scenaro1_DealExists(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"

    # Create FiscUnit with bob deal at time 37
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
    fizz_world.create_deal_mandate_ledgers()

    # THEN
    assert os_path_exists(bob37_deal_mandate_path)
    expected_deal_acct_nets = {bob_str: deal1_quota}
    assert open_json(bob37_deal_mandate_path) == expected_deal_acct_nets
    gen_a23_fiscunit = fiscunit_get_from_dict(open_json(a23_json_path))
    gen_bob37_dealunit = gen_a23_fiscunit.get_dealunit(bob_str, tp37)
    assert gen_bob37_dealunit._deal_acct_nets == expected_deal_acct_nets
