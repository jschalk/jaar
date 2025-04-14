from src.a00_data_toolboxs.file_toolbox import (
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
from src.a19_world_logic.examples.example_worlds import (
    get_bob_mop_with_reason_budunit_example,
    example_casa_clean_factunit,
)
from src.a19_world_logic.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_calc_fisc_deal_acct_mandate_net_ledgers_Scenaro0_DealEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    accord23_str = "accord23"
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    accord23_fisc = fiscunit_shop(accord23_str, fisc_mstr_dir)
    a23_json_path = create_fisc_json_path(fizz_world._fisc_mstr_dir, accord23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    print(f"{a23_json_path=}")
    a23_owners_path = create_fisc_owners_dir_path(
        fizz_world._fisc_mstr_dir, accord23_str
    )
    assert count_dirs_files(a23_owners_path) == 0

    # WHEN
    fizz_world.calc_fisc_deal_acct_mandate_net_ledgers()

    # THEN
    assert count_dirs_files(a23_owners_path) == 0


def test_WorldUnit_calc_fisc_deal_acct_mandate_net_ledgers_Scenaro1_SimpleDeal(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
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
    fizz_world = worldunit_shop("fizz")
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
    yao44_budevent.add_fact(clean_fact.base, clean_fact.pick)
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


# def test_WorldUnit_calc_fisc_deal_acct_mandate_net_ledgers_Scenaro2_DealExistsButNoBudExistsInEventsPast(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     fisc_mstr_dir = fizz_world._fisc_mstr_dir
#     a23_str = "accord23"

#     # Create FiscUnit with bob deal at time 37
#     accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
#     bob_str = "Bob"
#     tp37 = 37
#     deal1_quota = 450
#     accord23_fisc.add_dealunit(bob_str, tp37, deal1_quota)
#     a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
#     save_file(a23_json_path, None, accord23_fisc.get_json())
#     assert os_path_exists(a23_json_path)

#     # Create event time mapping owner_time_agg for time 37
#     event3 = 3
#     event7 = 7
#     timepoint40 = 40
#     timepoint66 = 66
#     a23_ote1_dict = {bob_str: {str(timepoint40): event3, str(timepoint66): event7}}
#     a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
#     print(f"{a23_ote1_json_path=}")
#     save_json(a23_ote1_json_path, None, a23_ote1_dict)
#     assert os_path_exists(a23_ote1_json_path)
#     tp37_cell_json_path = create_cell_json_path(
#         fisc_mstr_dir, a23_str, bob_str, tp37
#     )
#     assert os_path_exists(tp37_cell_json_path) is False

#     # WHEN
#     fizz_world.calc_fisc_deal_acct_mandate_net_ledgers()

#     # THEN
#     assert os_path_exists(tp37_cell_json_path)
#     cell_dict = open_json(tp37_cell_json_path)
#     print(f"{cell_dict=}")
#     assert cell_dict.get(ancestors_str()) == [bob_str]
#     assert not cell_dict.get(event_int_str())
#     assert cell_dict.get(celldepth_str()) == DEFAULT_CELLDEPTH
#     assert cell_dict.get(deal_owner_name_str()) == bob_str
#     assert cell_dict.get(quota_str()) == deal1_quota


# def test_WorldUnit_calc_fisc_deal_acct_mandate_net_ledgers_Scenaro3_DealExistsNotPerfectMatch_deal_time_event_int(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     fisc_mstr_dir = fizz_world._fisc_mstr_dir
#     a23_str = "accord23"
#     a23_penny = 2

#     # Create FiscUnit with bob deal at time 37
#     accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir, penny=a23_penny)
#     print(f"{accord23_fisc.penny=}")
#     bob_str = "Bob"
#     tp37 = 37
#     deal1_quota = 450
#     deal1_celldepth = 3
#     accord23_fisc.add_dealunit(
#         bob_str, tp37, deal1_quota, celldepth=deal1_celldepth
#     )
#     a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
#     save_file(a23_json_path, None, accord23_fisc.get_json())
#     assert os_path_exists(a23_json_path)

#     # Create event time mapping owner_time_agg for time 37
#     event3 = 3
#     event7 = 7
#     timepoint30 = 30
#     timepoint66 = 66
#     a23_ote1_dict = {bob_str: {str(timepoint30): event3, str(timepoint66): event7}}
#     a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
#     print(f"{a23_ote1_json_path=}")
#     save_json(a23_ote1_json_path, None, a23_ote1_dict)
#     assert os_path_exists(a23_ote1_json_path)

#     # destination of cell json
#     tp37_cell_json_path = create_cell_json_path(
#         fisc_mstr_dir, a23_str, bob_str, tp37
#     )
#     assert os_path_exists(tp37_cell_json_path) is False

#     # WHEN
#     fizz_world.calc_fisc_deal_acct_mandate_net_ledgers()

#     # THEN
#     assert os_path_exists(tp37_cell_json_path)
#     cell_dict = open_json(tp37_cell_json_path)
#     assert cell_dict.get(ancestors_str()) == [bob_str]
#     assert cell_dict.get(event_int_str()) == event3
#     assert cell_dict.get(celldepth_str()) == deal1_celldepth
#     assert cell_dict.get(deal_owner_name_str()) == bob_str
#     assert cell_dict.get(penny_str()) == a23_penny
#     assert cell_dict.get(quota_str()) == deal1_quota


# def test_WorldUnit_create_deal_mandate_ledgers_Scenaro0_DealEmpty(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     a23_str = "accord23"
#     mstr_dir = fizz_world._fisc_mstr_dir
#     accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
#     a23_json_path = create_fisc_json_path(fizz_world._fisc_mstr_dir, a23_str)
#     save_json(a23_json_path, None, accord23_fisc.get_dict())
#     bob_str = "Bob"
#     timepoint9 = 9
#     bob9_deal_mandate_path = deal_mandate_path(mstr_dir, a23_str, bob_str, timepoint9)
#     assert os_path_exists(bob9_deal_mandate_path) is False

#     # WHEN
#     fizz_world.create_deal_mandate_ledgers()

#     # THEN
#     assert os_path_exists(bob9_deal_mandate_path) is False


# def test_WorldUnit_calc_fisc_deal_acct_mandate_net_ledgers_Scenaro1_DealExists(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     mstr_dir = fizz_world._fisc_mstr_dir
#     a23_str = "accord23"

#     # Create FiscUnit with bob deal at time 37
#     accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
#     bob_str = "Bob"
#     tp37 = 37
#     deal1_quota = 450
#     accord23_fisc.add_dealunit(bob_str, tp37, deal1_quota)
#     a23_json_path = create_fisc_json_path(mstr_dir, a23_str)
#     save_json(a23_json_path, None, accord23_fisc.get_dict())
#     bob37_cell_mandate_path = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37)
#     bob_mandate = 777
#     assert deal1_quota != bob_mandate
#     save_json(bob37_cell_mandate_path, None, {bob_str: bob_mandate})
#     bob37_deal_mandate_path = deal_mandate_path(mstr_dir, a23_str, bob_str, tp37)
#     assert os_path_exists(bob37_deal_mandate_path) is False

#     # WHEN
#     fizz_world.create_deal_mandate_ledgers()

#     # THEN
#     assert os_path_exists(bob37_deal_mandate_path)
#     expected_deal_acct_nets = {bob_str: deal1_quota}
#     assert open_json(bob37_deal_mandate_path) == expected_deal_acct_nets
#     gen_a23_fiscunit = fiscunit_get_from_dict(open_json(a23_json_path))
#     gen_bob37_dealunit = gen_a23_fiscunit.get_dealunit(bob_str, tp37)
#     assert gen_bob37_dealunit._deal_acct_nets == expected_deal_acct_nets
#     assert gen_a23_fiscunit._all_tranbook == {bob_str: 888}


# # def test_WorldUnit_set_cell_tree_cell_mandates_SetsRootAttr_Scenario0_Depth0NoFacts(
# #     env_dir_setup_cleanup,
# # ):
# #     # ESTABLISH
# #     fizz_world = worldunit_shop("fizz")
# #     mstr_dir = fizz_world._fisc_mstr_dir
# #     a23_str = "accord"
# #     tp5 = 5
# #     bob_str = "Bob"
# #     das = []
# #     event7 = 7
# #     # create dealunit file
# #     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
# #     bob_bob_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [bob_str])
# #     cellunit_save_to_dir(bob_root_dir, bob_cell)
# #     cellunit_save_to_dir(bob_bob_dir, bob_cell)
# #     bob_root_mandate_path = mandate_path(mstr_dir, a23_str, bob_str, tp5, [])
# #     bob_bob_mandate_path = mandate_path(mstr_dir, a23_str, bob_str, tp5, [bob_str])
# #     assert os_path_exists(bob_root_mandate_path) is False
# #     assert os_path_exists(bob_bob_mandate_path) is False

# #     # WHEN
# #     fizz_world.set_cell_tree_cell_mandates()

# #     # THEN
# #     assert os_path_exists(bob_root_mandate_path)
# #     assert os_path_exists(bob_bob_mandate_path)
# #     assert open_json(bob_root_mandate_path) == {bob_str: 1000}
# #     assert open_json(bob_bob_mandate_path) == {bob_str: 1000}


# # def test_WorldUnit_set_cell_tree_cell_mandates_SetsRootAttr_Scenario0_Depth0NoFacts(
# #     env_dir_setup_cleanup,
# # ):
# #     # ESTABLISH
# #     fizz_world = worldunit_shop("fizz")
# #     mstr_dir = fizz_world._fisc_mstr_dir
# #     a23_str = "accord"
# #     tp5 = 5
# #     bob_str = "Bob"
# #     das = []
# #     event7 = 7
# #     # create cell file
# #     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
# #     bob_bob_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [bob_str])
# #     cellunit_save_to_dir(bob_root_dir, bob_cell)
# #     cellunit_save_to_dir(bob_bob_dir, bob_cell)
# #     bob_root_mandate_path = mandate_path(mstr_dir, a23_str, bob_str, tp5, [])
# #     bob_bob_mandate_path = mandate_path(mstr_dir, a23_str, bob_str, tp5, [bob_str])
# #     assert os_path_exists(bob_root_mandate_path) is False
# #     assert os_path_exists(bob_bob_mandate_path) is False

# #     # WHEN
# #     fizz_world.set_cell_tree_cell_mandates()

# #     # THEN
# #     assert os_path_exists(bob_root_mandate_path)
# #     assert os_path_exists(bob_bob_mandate_path)
# #     assert open_json(bob_root_mandate_path) == {bob_str: 1000}
# #     assert open_json(bob_bob_mandate_path) == {bob_str: 1000}

# #     # ESTABLISH
# #     bob_str = "Bob"
# #     sue_str = "Sue"
# #     root_ledger = {bob_str: 10, sue_str: 40}
# #     x_filename = "ledger.json"
# #     save_json(x_dir, CELL_MANDATE_FILENAME, root_ledger)
# #     x_scale = 200
# #     x_grain = 1

# #     # WHEN
# #     nested_allot_scale = allot_nested_scale(
# #         x_dir=x_dir,
# #         src_filename=x_filename,
# #         scale_number=x_scale,
# #         grain_unit=x_grain,
# #         depth=0,
# #     )

# #     # THEN
# #     assert nested_allot_scale == {bob_str: 40, sue_str: 160}


# # def test_allot_nested_scale_ReturnsObj_Scenari1_depth0_NestedFilesExist(
# #     env_dir_setup_cleanup,
# # ):
# #     # ESTABLISH
# #     x_dir = get_road_temp_env_dir()
# #     bob_str = "Bob"
# #     sue_str = "Sue"
# #     yao_str = "Yao"
# #     root_ledger = {bob_str: 10, sue_str: 40}
# #     bob_ledger = {sue_str: 1, yao_str: 1}
# #     sue_ledger = {sue_str: 1, yao_str: 3}
# #     x_filename = "ledger.json"
# #     bob_dir = create_path(x_dir, bob_str)
# #     sue_dir = create_path(x_dir, sue_str)
# #     save_json(x_dir, x_filename, root_ledger)
# #     save_json(bob_dir, x_filename, bob_ledger)
# #     save_json(sue_dir, x_filename, sue_ledger)
# #     x_scale = 200
# #     x_grain = 1

# #     # WHEN
# #     nested_allot_scale = allot_nested_scale(
# #         x_dir=x_dir,
# #         src_filename=x_filename,
# #         scale_number=x_scale,
# #         grain_unit=x_grain,
# #         depth=0,
# #     )

# #     # THEN
# #     assert nested_allot_scale == {bob_str: 40, sue_str: 160}


# # def test_allot_nested_scale_ReturnsObj_Scenari2_depth1_NestedFilesExist(
# #     env_dir_setup_cleanup,
# # ):
# #     # ESTABLISH
# #     x_dir = get_road_temp_env_dir()
# #     bob_str = "Bob"
# #     sue_str = "Sue"
# #     yao_str = "Yao"
# #     root_ledger = {bob_str: 10, sue_str: 40}
# #     bob_ledger = {sue_str: 1, yao_str: 1}
# #     sue_ledger = {sue_str: 1, yao_str: 3}
# #     x_filename = "ledger.json"
# #     bob_dir = create_path(x_dir, bob_str)
# #     sue_dir = create_path(x_dir, sue_str)
# #     save_json(x_dir, x_filename, root_ledger)
# #     save_json(bob_dir, x_filename, bob_ledger)
# #     save_json(sue_dir, x_filename, sue_ledger)
# #     x_scale = 200
# #     x_grain = 1

# #     # WHEN
# #     nested_allot_scale = allot_nested_scale(
# #         x_dir=x_dir,
# #         src_filename=x_filename,
# #         scale_number=x_scale,
# #         grain_unit=x_grain,
# #         depth=1,
# #     )

# #     # THEN
# #     assert set(nested_allot_scale.keys()) == {sue_str, yao_str}
# #     print(set(nested_allot_scale.keys()))
# #     assert nested_allot_scale == {sue_str: 60, yao_str: 140}


# # def test_allot_nested_scale_ReturnsObj_Scenari3_depth1_NoNestedFiles(
# #     env_dir_setup_cleanup,
# # ):
# #     # ESTABLISH
# #     x_dir = get_road_temp_env_dir()
# #     bob_str = "Bob"
# #     sue_str = "Sue"
# #     root_ledger = {bob_str: 10, sue_str: 40}
# #     x_filename = "ledger.json"
# #     save_json(x_dir, x_filename, root_ledger)
# #     x_scale = 200
# #     x_grain = 1

# #     # WHEN
# #     nested_allot_scale = allot_nested_scale(
# #         x_dir=x_dir,
# #         src_filename=x_filename,
# #         scale_number=x_scale,
# #         grain_unit=x_grain,
# #         depth=0,
# #     )

# #     # THEN
# #     assert nested_allot_scale == {bob_str: 40, sue_str: 160}


# # def test_allot_nested_scale_ReturnsObj_Scenari4_depth1_NestedFilesExist(
# #     env_dir_setup_cleanup,
# # ):
# #     # ESTABLISH
# #     x_dir = get_road_temp_env_dir()
# #     bob_str = "Bob"
# #     sue_str = "Sue"
# #     yao_str = "Yao"
# #     xio_str = "Xio"
# #     zia_str = "Zia"
# #     root_ledger = {bob_str: 10, sue_str: 40}
# #     bob_ledger = {sue_str: 1, yao_str: 1}
# #     sue_ledger = {sue_str: 1, yao_str: 3}
# #     sue_yao_ledger = {sue_str: 1, yao_str: 1, xio_str: 3}
# #     bob_yao_ledger = {sue_str: 1, yao_str: 1, zia_str: 3}
# #     x_filename = "ledger.json"
# #     bob_dir = create_path(x_dir, bob_str)
# #     sue_dir = create_path(x_dir, sue_str)
# #     bob_yao_dir = create_path(bob_dir, yao_str)
# #     sue_yao_dir = create_path(sue_dir, yao_str)
# #     save_json(x_dir, x_filename, root_ledger)
# #     save_json(bob_dir, x_filename, bob_ledger)
# #     save_json(sue_dir, x_filename, sue_ledger)
# #     save_json(bob_yao_dir, x_filename, bob_yao_ledger)
# #     save_json(sue_yao_dir, x_filename, sue_yao_ledger)
# #     x_scale = 200
# #     x_grain = 1

# #     # WHEN
# #     nested_allot_scale = allot_nested_scale(
# #         x_dir=x_dir,
# #         src_filename=x_filename,
# #         scale_number=x_scale,
# #         grain_unit=x_grain,
# #         depth=3,
# #     )

# #     # THEN
# #     assert set(nested_allot_scale.keys()) == {sue_str, yao_str, xio_str, zia_str}
# #     print(set(nested_allot_scale.keys()))
# #     assert nested_allot_scale == {sue_str: 88, yao_str: 28, xio_str: 72, zia_str: 12}


# # def test_allot_nested_scale_SetsFiles_Scenario0(env_dir_setup_cleanup):
# #     # ESTABLISH
# #     x_dir = get_road_temp_env_dir()
# #     bob_str = "Bob"
# #     sue_str = "Sue"
# #     yao_str = "Yao"
# #     xio_str = "Xio"
# #     zia_str = "Zia"
# #     root_ledger = {bob_str: 10, sue_str: 40}
# #     bob_ledger = {sue_str: 1, yao_str: 1}
# #     sue_ledger = {sue_str: 1, yao_str: 3}
# #     sue_yao_ledger = {sue_str: 1, yao_str: 1, xio_str: 3}
# #     bob_yao_ledger = {sue_str: 1, yao_str: 1, zia_str: 3}
# #     x_filename = "ledger.json"
# #     bob_dir = create_path(x_dir, bob_str)
# #     sue_dir = create_path(x_dir, sue_str)
# #     bob_yao_dir = create_path(bob_dir, yao_str)
# #     sue_yao_dir = create_path(sue_dir, yao_str)
# #     save_json(x_dir, x_filename, root_ledger)
# #     save_json(bob_dir, x_filename, bob_ledger)
# #     save_json(sue_dir, x_filename, sue_ledger)
# #     save_json(bob_yao_dir, x_filename, bob_yao_ledger)
# #     save_json(sue_yao_dir, x_filename, sue_yao_ledger)
# #     x_scale = 200
# #     x_grain = 1
# #     alloted_filename = "alloted.json"
# #     x_alloted_path = create_path(x_dir, alloted_filename)
# #     bob_alloted_path = create_path(bob_dir, alloted_filename)
# #     sue_alloted_path = create_path(sue_dir, alloted_filename)
# #     bob_yao_alloted_path = create_path(bob_yao_dir, alloted_filename)
# #     sue_yao_alloted_path = create_path(sue_yao_dir, alloted_filename)
# #     assert os_path_exists(x_alloted_path) is False
# #     assert os_path_exists(bob_alloted_path) is False
# #     assert os_path_exists(sue_alloted_path) is False
# #     assert os_path_exists(bob_yao_alloted_path) is False
# #     assert os_path_exists(sue_yao_alloted_path) is False

# #     # WHEN
# #     allot_nested_scale(
# #         x_dir=x_dir,
# #         src_filename=x_filename,
# #         scale_number=x_scale,
# #         grain_unit=x_grain,
# #         depth=3,
# #     )

# #     # THEN
# #     assert os_path_exists(x_alloted_path)
# #     assert os_path_exists(bob_alloted_path)
# #     assert os_path_exists(sue_alloted_path)
# #     assert os_path_exists(bob_yao_alloted_path)
# #     assert os_path_exists(sue_yao_alloted_path)
# #     x_alloted_dict = open_json(x_alloted_path)
# #     bob_alloted_dict = open_json(bob_alloted_path)
# #     sue_alloted_dict = open_json(sue_alloted_path)
# #     bob_yao_alloted_dict = open_json(bob_yao_alloted_path)
# #     sue_yao_alloted_dict = open_json(sue_yao_alloted_path)
# #     assert x_alloted_dict == {sue_str: 160, bob_str: 40}
# #     assert bob_alloted_dict == {sue_str: 20, yao_str: 20}
# #     assert sue_alloted_dict == {sue_str: 40, yao_str: 120}
# #     assert bob_yao_alloted_dict == {sue_str: 4, yao_str: 4, zia_str: 12}
# #     assert sue_yao_alloted_dict == {sue_str: 24, yao_str: 24, xio_str: 72}


# # def test_allot_nested_scale_SetsFiles_Scenario1_Custom_output_filename(
# #     env_dir_setup_cleanup,
# # ):
# #     # ESTABLISH
# #     x_dir = get_road_temp_env_dir()
# #     bob_str = "Bob"
# #     sue_str = "Sue"
# #     yao_str = "Yao"
# #     xio_str = "Xio"
# #     zia_str = "Zia"
# #     root_ledger = {bob_str: 10, sue_str: 40}
# #     bob_ledger = {sue_str: 1, yao_str: 1}
# #     sue_ledger = {sue_str: 1, yao_str: 3}
# #     sue_yao_ledger = {sue_str: 1, yao_str: 1, xio_str: 3}
# #     bob_yao_ledger = {sue_str: 1, yao_str: 1, zia_str: 3}
# #     x_filename = "ledger.json"
# #     bob_dir = create_path(x_dir, bob_str)
# #     sue_dir = create_path(x_dir, sue_str)
# #     bob_yao_dir = create_path(bob_dir, yao_str)
# #     sue_yao_dir = create_path(sue_dir, yao_str)
# #     save_json(x_dir, x_filename, root_ledger)
# #     save_json(bob_dir, x_filename, bob_ledger)
# #     save_json(sue_dir, x_filename, sue_ledger)
# #     save_json(bob_yao_dir, x_filename, bob_yao_ledger)
# #     save_json(sue_yao_dir, x_filename, sue_yao_ledger)
# #     x_scale = 200
# #     x_grain = 1
# #     output_filename = "outputed_alloted.json"
# #     x_output_path = create_path(x_dir, output_filename)
# #     bob_output_path = create_path(bob_dir, output_filename)
# #     sue_output_path = create_path(sue_dir, output_filename)
# #     bob_yao_output_path = create_path(bob_yao_dir, output_filename)
# #     sue_yao_output_path = create_path(sue_yao_dir, output_filename)
# #     assert os_path_exists(x_output_path) is False
# #     assert os_path_exists(bob_output_path) is False
# #     assert os_path_exists(sue_output_path) is False
# #     assert os_path_exists(bob_yao_output_path) is False
# #     assert os_path_exists(sue_yao_output_path) is False

# #     # WHEN
# #     allot_nested_scale(
# #         x_dir=x_dir,
# #         src_filename=x_filename,
# #         scale_number=x_scale,
# #         grain_unit=x_grain,
# #         depth=3,
# #         dst_filename=output_filename,
# #     )

# #     # THEN
# #     assert os_path_exists(x_output_path)
# #     assert os_path_exists(bob_output_path)
# #     assert os_path_exists(sue_output_path)
# #     assert os_path_exists(bob_yao_output_path)
# #     assert os_path_exists(sue_yao_output_path)
# #     assert open_json(x_output_path) == {sue_str: 160, bob_str: 40}
# #     assert open_json(bob_output_path) == {sue_str: 20, yao_str: 20}
# #     assert open_json(sue_output_path) == {sue_str: 40, yao_str: 120}
# #     assert open_json(bob_yao_output_path) == {sue_str: 4, yao_str: 4, zia_str: 12}
# #     assert open_json(sue_yao_output_path) == {sue_str: 24, yao_str: 24, xio_str: 72}
