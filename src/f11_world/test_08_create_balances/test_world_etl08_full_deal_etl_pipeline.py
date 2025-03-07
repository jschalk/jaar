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
from src.f07_fisc.fisc import fiscunit_shop, get_from_dict as fiscunit_get_from_dict
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.example_worlds import (
    get_bob_mop_with_reason_budunit_example,
)
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


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


# def test_WorldUnit_create_deals_root_cells_Scenaro1_DealExists(env_dir_setup_cleanup):
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


# # def test_WorldUnit_set_deal_tree_cell_mandates_SetsRootAttr_Scenario0_Depth0NoFacts(
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
# #     fizz_world.set_deal_tree_cell_mandates()

# #     # THEN
# #     assert os_path_exists(bob_root_mandate_path)
# #     assert os_path_exists(bob_bob_mandate_path)
# #     assert open_json(bob_root_mandate_path) == {bob_str: 1000}
# #     assert open_json(bob_bob_mandate_path) == {bob_str: 1000}


# # def test_WorldUnit_set_deal_tree_cell_mandates_SetsRootAttr_Scenario0_Depth0NoFacts(
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
# #     fizz_world.set_deal_tree_cell_mandates()

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
