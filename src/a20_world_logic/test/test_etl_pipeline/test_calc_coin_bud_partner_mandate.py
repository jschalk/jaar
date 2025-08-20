from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import (
    count_dirs_files,
    open_json,
    save_file,
    save_json,
)
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a12_hub_toolbox.a12_path import (
    create_believerevent_path,
    create_coin_believers_dir_path,
    create_coin_json_path,
)
from src.a15_coin_logic.a15_path import (
    create_bud_partner_mandate_ledger_path as bud_mandate_path,
)
from src.a15_coin_logic.coin_main import (
    coinunit_shop,
    get_from_dict as coinunit_get_from_dict,
)
from src.a18_etl_toolbox.a18_path import create_coin_ote1_json_path
from src.a20_world_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as worlds_dir,
)
from src.a20_world_logic.test._util.example_worlds import (
    example_casa_clean_factunit,
    get_bob_mop_with_reason_believerunit_example,
)
from src.a20_world_logic.world import worldunit_shop


def test_WorldUnit_calc_coin_bud_partner_mandate_net_ledgers_Scenaro0_BudEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_world = worldunit_shop("Fay", worlds_dir())
    a23_str = "amy23"
    coin_mstr_dir = fay_world._coin_mstr_dir
    amy23_coin = coinunit_shop(a23_str, coin_mstr_dir)
    a23_json_path = create_coin_json_path(fay_world._coin_mstr_dir, a23_str)
    save_file(a23_json_path, None, amy23_coin.get_json())
    print(f"{a23_json_path=}")
    a23_believers_path = create_coin_believers_dir_path(
        fay_world._coin_mstr_dir, a23_str
    )
    assert count_dirs_files(a23_believers_path) == 0

    # WHEN
    fay_world.calc_coin_bud_partner_mandate_net_ledgers()

    # THEN
    assert count_dirs_files(a23_believers_path) == 0


def test_WorldUnit_calc_coin_bud_partner_mandate_net_ledgers_Scenaro1_SimpleBud(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_world = worldunit_shop("Fay", worlds_dir())
    mstr_dir = fay_world._coin_mstr_dir
    a23_str = "amy23"
    amy23_coin = coinunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    amy23_coin.add_budunit(bob_str, tp37, bud1_quota, celldepth=x_celldepth)
    a23_json_path = create_coin_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, amy23_coin.get_json())
    # Create empty ote1 file
    a23_ote1_json_path = create_coin_ote1_json_path(mstr_dir, a23_str)
    save_json(a23_ote1_json_path, None, {})
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    fay_world.calc_coin_bud_partner_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_partner_nets = {bob_str: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_partner_nets
    gen_a23_coinunit = coinunit_get_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_coinunit.get_budunit(bob_str, tp37)
    assert gen_bob37_budunit._bud_partner_nets == expected_bud_partner_nets


def test_WorldUnit_calc_coin_bud_partner_mandate_net_ledgers_Scenaro2_BudExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_world = worldunit_shop("Fay", worlds_dir())
    mstr_dir = fay_world._coin_mstr_dir
    a23_str = "amy23"

    # Create CoinUnit with bob bud at time 37
    amy23_coin = coinunit_shop(a23_str, mstr_dir)
    a23_str = "amy23"
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    amy23_coin.add_budunit(bob_str, tp37, bud1_quota, celldepth=x_celldepth)
    a23_json_path = create_coin_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, amy23_coin.get_json())

    # Create event time mapping believer_time_agg for time 37
    event33 = 33
    event44 = 44
    event55 = 55
    bob55_believerevent = get_bob_mop_with_reason_believerunit_example()
    bob55_believerevent.add_partnerunit(sue_str, 1)
    sue44_believerevent = believerunit_shop(sue_str, a23_str)
    sue44_believerevent.set_believer_name(sue_str)
    sue44_believerevent.add_partnerunit(yao_str, 1)
    yao44_believerevent = get_bob_mop_with_reason_believerunit_example()
    yao44_believerevent.set_believer_name(yao_str)
    yao44_believerevent.add_partnerunit(zia_str, 1)
    clean_fact = example_casa_clean_factunit()
    yao44_believerevent.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    zia33_believerevent = get_bob_mop_with_reason_believerunit_example()
    zia33_believerevent.set_believer_name(zia_str)
    bob55_path = create_believerevent_path(mstr_dir, a23_str, bob_str, event55)
    sue44_path = create_believerevent_path(mstr_dir, a23_str, sue_str, event44)
    yao44_path = create_believerevent_path(mstr_dir, a23_str, yao_str, event44)
    zia33_path = create_believerevent_path(mstr_dir, a23_str, zia_str, event33)
    save_json(bob55_path, None, bob55_believerevent.to_dict())
    save_json(sue44_path, None, sue44_believerevent.to_dict())
    save_json(yao44_path, None, yao44_believerevent.to_dict())
    save_json(zia33_path, None, zia33_believerevent.to_dict())

    # Create empty ote1 file
    a23_ote1_dict = {
        bob_str: {str(tp37): event55},
        sue_str: {str(tp37): event44},
        yao_str: {str(tp37): event44},
        zia_str: {str(tp37): event33},
    }
    a23_ote1_json_path = create_coin_ote1_json_path(mstr_dir, a23_str)
    save_json(a23_ote1_json_path, None, a23_ote1_dict)

    # create result bud_partner_mandate_ledger file
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    fay_world.calc_coin_bud_partner_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_partner_nets = {zia_str: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_partner_nets
    gen_a23_coinunit = coinunit_get_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_coinunit.get_budunit(bob_str, tp37)
    assert gen_bob37_budunit._bud_partner_nets == expected_bud_partner_nets
