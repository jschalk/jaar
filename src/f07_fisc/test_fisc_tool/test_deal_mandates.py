from src.f00_instrument.file import open_json, save_json
from src.f01_road.deal import tranbook_shop
from src.f05_listen.hub_path import (
    create_cell_acct_mandate_ledger_path as cell_mandate_path,
    create_deal_acct_mandate_ledger_path as deal_mandate_path,
    create_fisc_json_path,
)
from src.f07_fisc.fisc import fiscunit_shop, get_from_dict as fiscunit_get_from_dict
from src.f07_fisc.fisc_tool import create_deal_mandate_ledgers
from src.f07_fisc.examples.fisc_env import env_dir_setup_cleanup, get_test_fisc_mstr_dir
from os.path import exists as os_path_exists


def test_create_deal_mandate_ledgers_Scenaro0_DealEmpty(env_dir_setup_cleanup):
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


def test_create_deal_mandate_ledgers_Scenaro1_DealExists(env_dir_setup_cleanup):
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
    bob37_dealunit = accord23_fisc.get_dealunit(bob_str, tp37)
    assert bob37_dealunit._deal_acct_nets == {}

    # WHEN
    create_deal_mandate_ledgers(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob37_deal_mandate_path)
    expected_deal_acct_nets = {bob_str: deal1_quota}
    assert open_json(bob37_deal_mandate_path) == expected_deal_acct_nets
    gen_a23_fiscunit = fiscunit_get_from_dict(open_json(a23_json_path))
    gen_a23_fiscunit.set_all_tranbook()
    gen_bob37_dealunit = gen_a23_fiscunit.get_dealunit(bob_str, tp37)
    assert gen_bob37_dealunit._deal_acct_nets == expected_deal_acct_nets
    expected_a23_all_tranbook = tranbook_shop(a23_str)
    expected_a23_all_tranbook.add_tranunit(bob_str, bob_str, tp37, 450)
    assert gen_a23_fiscunit._all_tranbook == expected_a23_all_tranbook


def test_create_deal_mandate_ledgers_Scenaro2_Mutliple_cell_acct_mandate_ledgers(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    mstr_dir = get_test_fisc_mstr_dir()
    accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_str = "Sue"
    xio_str = "Xio"
    tp37 = 37
    deal1_quota = 450
    accord23_fisc.add_dealunit(bob_str, tp37, deal1_quota)
    a23_json_path = create_fisc_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, accord23_fisc.get_dict())
    b37_cell_mandate = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    b37_sue_cell_path = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37, [sue_str])
    b37_yao_cell_path = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37, [yao_str])
    yz_anc = [yao_str, zia_str]
    b37_yao_zia_cell_path = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37, yz_anc)
    save_json(b37_cell_mandate, None, {sue_str: 1, yao_str: 3})
    save_json(b37_sue_cell_path, None, {zia_str: 1, sue_str: 3})
    save_json(b37_yao_cell_path, None, {zia_str: 1, yao_str: 3})
    save_json(b37_yao_zia_cell_path, None, {xio_str: 1})
    bob37_deal_mandate_path = deal_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_deal_mandate_path) is False
    bob37_dealunit = accord23_fisc.get_dealunit(bob_str, tp37)
    assert bob37_dealunit._deal_acct_nets == {}

    # WHEN
    create_deal_mandate_ledgers(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob37_deal_mandate_path)
    expected_deal_acct_nets = {
        yao_str: 254,
        xio_str: 84,
        sue_str: 84,
        zia_str: 28,
    }
    print(f"{open_json(bob37_deal_mandate_path)=}")
    assert open_json(bob37_deal_mandate_path) == expected_deal_acct_nets
    gen_a23_fiscunit = fiscunit_get_from_dict(open_json(a23_json_path))
    gen_bob37_dealunit = gen_a23_fiscunit.get_dealunit(bob_str, tp37)
    assert gen_bob37_dealunit._deal_acct_nets == expected_deal_acct_nets
    expected_a23_all_tranbook = tranbook_shop(a23_str)
    expected_a23_all_tranbook.add_tranunit(bob_str, sue_str, tp37, 84)
    expected_a23_all_tranbook.add_tranunit(bob_str, xio_str, tp37, 84)
    expected_a23_all_tranbook.add_tranunit(bob_str, zia_str, tp37, 28)
    expected_a23_all_tranbook.add_tranunit(bob_str, yao_str, tp37, 254)
    gen_a23_fiscunit.set_all_tranbook()
    gen_all_tranbook = gen_a23_fiscunit._all_tranbook
    assert gen_all_tranbook.tranunits == expected_a23_all_tranbook.tranunits
