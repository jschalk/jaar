from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import (
    count_dirs_files,
    open_json,
    save_file,
    save_json,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_toolbox.hub_path import (
    create_bank_json_path,
    create_bank_ote1_json_path,
    create_bank_owners_dir_path,
    create_bud_acct_mandate_ledger_path as bud_mandate_path,
    create_planevent_path,
)
from src.a15_bank_logic.bank import (
    bankunit_shop,
    get_from_dict as bankunit_get_from_dict,
)
from src.a20_fis_logic.fis import fisunit_shop
from src.a20_fis_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as fiss_dir,
)
from src.a20_fis_logic.test._util.example_fiss import (
    example_casa_clean_factunit,
    get_bob_mop_with_reason_planunit_example,
)


def test_FisUnit_calc_bank_bud_acct_mandate_net_ledgers_Scenaro0_BudEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_fis = fisunit_shop("fizz", fiss_dir())
    a23_str = "accord23"
    bank_mstr_dir = fizz_fis._bank_mstr_dir
    accord23_bank = bankunit_shop(a23_str, bank_mstr_dir)
    a23_json_path = create_bank_json_path(fizz_fis._bank_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_bank.get_json())
    print(f"{a23_json_path=}")
    a23_owners_path = create_bank_owners_dir_path(fizz_fis._bank_mstr_dir, a23_str)
    assert count_dirs_files(a23_owners_path) == 0

    # WHEN
    fizz_fis.calc_bank_bud_acct_mandate_net_ledgers()

    # THEN
    assert count_dirs_files(a23_owners_path) == 0


def test_FisUnit_calc_bank_bud_acct_mandate_net_ledgers_Scenaro1_SimpleBud(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_fis = fisunit_shop("fizz", fiss_dir())
    mstr_dir = fizz_fis._bank_mstr_dir
    a23_str = "accord23"
    accord23_bank = bankunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    accord23_bank.add_budunit(bob_str, tp37, bud1_quota, celldepth=x_celldepth)
    a23_json_path = create_bank_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_bank.get_json())
    # Create empty ote1 file
    a23_ote1_json_path = create_bank_ote1_json_path(mstr_dir, a23_str)
    save_json(a23_ote1_json_path, None, {})
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    fizz_fis.calc_bank_bud_acct_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_acct_nets = {bob_str: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_acct_nets
    gen_a23_bankunit = bankunit_get_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_bankunit.get_budunit(bob_str, tp37)
    assert gen_bob37_budunit._bud_acct_nets == expected_bud_acct_nets


def test_FisUnit_calc_bank_bud_acct_mandate_net_ledgers_Scenaro2_BudExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_fis = fisunit_shop("fizz", fiss_dir())
    mstr_dir = fizz_fis._bank_mstr_dir
    a23_str = "accord23"

    # Create BankUnit with bob bud at time 37
    accord23_bank = bankunit_shop(a23_str, mstr_dir)
    a23_str = "accord23"
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    accord23_bank.add_budunit(bob_str, tp37, bud1_quota, celldepth=x_celldepth)
    a23_json_path = create_bank_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_bank.get_json())

    # Create event time mapping owner_time_agg for time 37
    event33 = 33
    event44 = 44
    event55 = 55
    bob55_planevent = get_bob_mop_with_reason_planunit_example()
    bob55_planevent.add_acctunit(sue_str, 1)
    sue44_planevent = planunit_shop(sue_str, a23_str)
    sue44_planevent.set_owner_name(sue_str)
    sue44_planevent.add_acctunit(yao_str, 1)
    yao44_planevent = get_bob_mop_with_reason_planunit_example()
    yao44_planevent.set_owner_name(yao_str)
    yao44_planevent.add_acctunit(zia_str, 1)
    clean_fact = example_casa_clean_factunit()
    yao44_planevent.add_fact(clean_fact.fcontext, clean_fact.fstate)
    zia33_planevent = get_bob_mop_with_reason_planunit_example()
    zia33_planevent.set_owner_name(zia_str)
    bob55_path = create_planevent_path(mstr_dir, a23_str, bob_str, event55)
    sue44_path = create_planevent_path(mstr_dir, a23_str, sue_str, event44)
    yao44_path = create_planevent_path(mstr_dir, a23_str, yao_str, event44)
    zia33_path = create_planevent_path(mstr_dir, a23_str, zia_str, event33)
    save_json(bob55_path, None, bob55_planevent.get_dict())
    save_json(sue44_path, None, sue44_planevent.get_dict())
    save_json(yao44_path, None, yao44_planevent.get_dict())
    save_json(zia33_path, None, zia33_planevent.get_dict())

    # Create empty ote1 file
    a23_ote1_dict = {
        bob_str: {str(tp37): event55},
        sue_str: {str(tp37): event44},
        yao_str: {str(tp37): event44},
        zia_str: {str(tp37): event33},
    }
    a23_ote1_json_path = create_bank_ote1_json_path(mstr_dir, a23_str)
    save_json(a23_ote1_json_path, None, a23_ote1_dict)

    # create result bud_acct_mandate_ledger file
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    fizz_fis.calc_bank_bud_acct_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_acct_nets = {zia_str: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_acct_nets
    gen_a23_bankunit = bankunit_get_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_bankunit.get_budunit(bob_str, tp37)
    assert gen_bob37_budunit._bud_acct_nets == expected_bud_acct_nets
