from src.a00_data_toolbox.file_toolbox import (
    open_json,
    save_json,
    count_dirs_files,
    save_file,
)
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hub_path import (
    create_budevent_path,
    create_deal_acct_mandate_ledger_path as deal_mandate_path,
    create_fisc_owners_dir_path,
    create_fisc_json_path,
    create_fisc_ote1_json_path,
)
from src.a15_fisc_logic.fisc import (
    fiscunit_shop,
    get_from_dict as fiscunit_get_from_dict,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._test_util.example_worlds import (
    get_bob_mop_with_reason_budunit_example,
    example_casa_clean_factunit,
)
from src.a19_world_logic._test_util.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_WorldUnit_calc_fisc_deal_acct_mandate_net_ledgers_Scenaro0_DealEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz", worlds_dir())
    a23_str = "accord23"
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    a23_json_path = create_fisc_json_path(fizz_world._fisc_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    print(f"{a23_json_path=}")
    a23_owners_path = create_fisc_owners_dir_path(fizz_world._fisc_mstr_dir, a23_str)
    assert count_dirs_files(a23_owners_path) == 0

    # WHEN
    fizz_world.calc_fisc_deal_acct_mandate_net_ledgers()

    # THEN
    assert count_dirs_files(a23_owners_path) == 0


def test_WorldUnit_calc_fisc_deal_acct_mandate_net_ledgers_Scenaro1_SimpleDeal(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz", worlds_dir())
    mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    tp37 = 37
    deal1_quota = 450
    x_celldepth = 2
    accord23_fisc.add_dealunit(bob_str, tp37, deal1_quota, celldepth=x_celldepth)
    a23_json_path = create_fisc_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    # Create empty ote1 file
    a23_ote1_json_path = create_fisc_ote1_json_path(mstr_dir, a23_str)
    save_json(a23_ote1_json_path, None, {})
    bob37_deal_mandate_path = deal_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_deal_mandate_path) is False

    # WHEN
    fizz_world.calc_fisc_deal_acct_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_deal_mandate_path)
    expected_deal_acct_nets = {bob_str: deal1_quota}
    assert open_json(bob37_deal_mandate_path) == expected_deal_acct_nets
    gen_a23_fiscunit = fiscunit_get_from_dict(open_json(a23_json_path))
    gen_bob37_dealunit = gen_a23_fiscunit.get_dealunit(bob_str, tp37)
    assert gen_bob37_dealunit._deal_acct_nets == expected_deal_acct_nets


def test_WorldUnit_calc_fisc_deal_acct_mandate_net_ledgers_Scenaro2_DealExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz", worlds_dir())
    mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
    a23_str = "accord23"
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37
    deal1_quota = 450
    x_celldepth = 2
    accord23_fisc.add_dealunit(bob_str, tp37, deal1_quota, celldepth=x_celldepth)
    a23_json_path = create_fisc_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())

    # Create event time mapping owner_time_agg for time 37
    event33 = 33
    event44 = 44
    event55 = 55
    bob55_budevent = get_bob_mop_with_reason_budunit_example()
    bob55_budevent.add_acctunit(sue_str, 1)
    sue44_budevent = budunit_shop(sue_str, a23_str)
    sue44_budevent.set_owner_name(sue_str)
    sue44_budevent.add_acctunit(yao_str, 1)
    yao44_budevent = get_bob_mop_with_reason_budunit_example()
    yao44_budevent.set_owner_name(yao_str)
    yao44_budevent.add_acctunit(zia_str, 1)
    clean_fact = example_casa_clean_factunit()
    yao44_budevent.add_fact(clean_fact.fcontext, clean_fact.fstate)
    zia33_budevent = get_bob_mop_with_reason_budunit_example()
    zia33_budevent.set_owner_name(zia_str)
    bob55_path = create_budevent_path(mstr_dir, a23_str, bob_str, event55)
    sue44_path = create_budevent_path(mstr_dir, a23_str, sue_str, event44)
    yao44_path = create_budevent_path(mstr_dir, a23_str, yao_str, event44)
    zia33_path = create_budevent_path(mstr_dir, a23_str, zia_str, event33)
    save_json(bob55_path, None, bob55_budevent.get_dict())
    save_json(sue44_path, None, sue44_budevent.get_dict())
    save_json(yao44_path, None, yao44_budevent.get_dict())
    save_json(zia33_path, None, zia33_budevent.get_dict())

    # Create empty ote1 file
    a23_ote1_dict = {
        bob_str: {str(tp37): event55},
        sue_str: {str(tp37): event44},
        yao_str: {str(tp37): event44},
        zia_str: {str(tp37): event33},
    }
    a23_ote1_json_path = create_fisc_ote1_json_path(mstr_dir, a23_str)
    save_json(a23_ote1_json_path, None, a23_ote1_dict)

    # create output deal_acct_mandate_ledger file
    bob37_deal_mandate_path = deal_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_deal_mandate_path) is False

    # WHEN
    fizz_world.calc_fisc_deal_acct_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_deal_mandate_path)
    expected_deal_acct_nets = {zia_str: deal1_quota}
    assert open_json(bob37_deal_mandate_path) == expected_deal_acct_nets
    gen_a23_fiscunit = fiscunit_get_from_dict(open_json(a23_json_path))
    gen_bob37_dealunit = gen_a23_fiscunit.get_dealunit(bob_str, tp37)
    assert gen_bob37_dealunit._deal_acct_nets == expected_deal_acct_nets
