from src.a00_data_toolboxs.file_toolbox import save_file, open_file
from src.a06_bud_logic.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.a12_hub_tools.hub_path import (
    create_fisc_json_path,
    create_gut_path,
    create_job_path,
)
from src.a15_fisc_logic.fisc import fiscunit_shop
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic.examples.world_env import (
    get_test_worlds_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_WorldUnit_fisc_gut_to_fisc_job_SetsFiles_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "accord23"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    bob_gut = budunit_shop(bob_inx, a23_str)
    bob_gut.add_acctunit(bob_inx, credit77)
    bob_gut.add_acctunit(yao_inx, credit44)
    bob_gut.add_acctunit(bob_inx, credit77)
    bob_gut.add_acctunit(sue_inx, credit88)
    bob_gut.add_acctunit(yao_inx, credit44)
    a23_bob_gut_path = create_gut_path(fisc_mstr_dir, a23_str, bob_inx)
    save_file(a23_bob_gut_path, None, bob_gut.get_json())
    a23_bob_job_path = create_job_path(fisc_mstr_dir, a23_str, bob_inx)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, fiscunit_shop(a23_str, fisc_mstr_dir).get_json())
    assert os_path_exists(a23_bob_gut_path)
    assert os_path_exists(a23_bob_job_path) is False

    # WHEN
    fizz_world.fisc_gut_to_fisc_job()

    # THEN
    assert os_path_exists(a23_bob_job_path)
    generated_job = budunit_get_from_json(open_file(a23_bob_job_path))
    expected_job = budunit_shop(bob_inx, a23_str)
    expected_job.add_acctunit(bob_inx, credit77)
    expected_job.add_acctunit(yao_inx, credit44)
    expected_job.add_acctunit(bob_inx, credit77)
    expected_job.add_acctunit(sue_inx, credit88)
    expected_job.add_acctunit(yao_inx, credit44)
    expected_job.settle_bud()
    assert generated_job.accts.keys() == expected_job.accts.keys()
    # assert generated_job.get_dict() == expected_job.get_dict()
    # assert generated_job == expected_job


# def test_WorldUnit_fisc_gut_to_fisc_job_SetsFiles_Scenario1(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_inx = "Suzy"
#     bob_inx = "Bobby"
#     yao_inx = "Yao"
#     a23_str = "accord23"
#     fizz_world = worldunit_shop("fizz", worlds_dir())
#     fisc_mstr_dir = fizz_world._fisc_mstr_dir
#     bob_gut = budunit_shop(bob_inx, a23_str)
#     bob_gut.add_acctunit(bob_inx)
#     bob_gut.add_acctunit(yao_inx)
#     bob_gut.add_acctunit(bob_inx)
#     bob_gut.add_acctunit(sue_inx)
#     bob_gut.add_acctunit(yao_inx)
#     clean_road = bob_gut.make_l1_road("clean")
#     bob_gut.add_item(clean_road, pledge=True)

#     yao_gut = budunit_shop(yao_inx, a23_str)
#     yao_gut.add_acctunit(bob_inx)
#     yao_gut.add_acctunit(yao_inx)
#     run_road = bob_gut.make_l1_road("run")
#     fly_road = bob_gut.make_l1_road("fly")
#     yao_gut.add_item(run_road, pledge=True)
#     yao_gut.add_item(fly_road, pledge=True)
#     assert bob_gut.item_exists(clean_road)
#     assert yao_gut.item_exists(clean_road) is False

#     a23_bob_gut_path = create_gut_path(fisc_mstr_dir, a23_str, bob_inx)
#     a23_yao_gut_path = create_gut_path(fisc_mstr_dir, a23_str, yao_inx)
#     save_file(a23_bob_gut_path, None, bob_gut.get_json())
#     save_file(a23_yao_gut_path, None, yao_gut.get_json())
#     a23_bob_job_path = create_job_path(fisc_mstr_dir, a23_str, bob_inx)
#     a23_yao_job_path = create_job_path(fisc_mstr_dir, a23_str, yao_inx)
#     fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
#     save_file(fisc_json_path, None, fiscunit_shop(a23_str, fisc_mstr_dir).get_json())
#     assert os_path_exists(a23_bob_gut_path)
#     assert os_path_exists(a23_yao_gut_path)
#     assert os_path_exists(a23_bob_job_path) is False
#     assert os_path_exists(a23_yao_job_path) is False

#     # WHEN
#     fizz_world.fisc_gut_to_fisc_job()
#     fizz_world.fisc_gut_to_fisc_job()

#     # THEN
#     assert os_path_exists(a23_bob_job_path)
#     assert os_path_exists(a23_yao_job_path)
#     gen_bob_job = budunit_get_from_json(open_file(a23_bob_job_path))
#     gen_yao_job = budunit_get_from_json(open_file(a23_yao_job_path))
#     expected_bob_job = budunit_shop(bob_inx, a23_str)
#     expected_yao_job = budunit_shop(yao_inx, a23_str)
#     expected_bob_job.add_acctunit(bob_inx)
#     expected_bob_job.add_acctunit(yao_inx)
#     expected_bob_job.add_acctunit(bob_inx)
#     expected_bob_job.add_acctunit(sue_inx)
#     expected_bob_job.add_acctunit(yao_inx)
#     expected_yao_job.add_acctunit(bob_inx)
#     expected_yao_job.add_acctunit(yao_inx)
#     expected_bob_job.add_item(clean_road, pledge=True)
#     expected_bob_job.add_item(run_road, pledge=True)
#     expected_bob_job.add_item(fly_road, pledge=True)
#     expected_yao_job.add_item(clean_road, pledge=True)
#     expected_yao_job.add_item(run_road, pledge=True)
#     expected_yao_job.add_item(fly_road, pledge=True)

#     assert gen_yao_job.accts.keys() == expected_yao_job.accts.keys()
#     print(f"{gen_yao_job.get_item_dict().keys()=}")
#     assert gen_yao_job.item_exists(clean_road)
#     assert gen_yao_job.get_dict() == expected_yao_job.get_dict()

#     assert gen_bob_job.accts.keys() == expected_bob_job.accts.keys()
#     expected_bob_items = expected_bob_job.get_item_dict().keys()
#     generate_bob_items = gen_bob_job.get_item_dict().keys()
#     print(f"{expected_bob_items=}")
#     print(f"{generate_bob_items=}")
#     assert generate_bob_items == expected_bob_items
#     expected_clean_item = expected_bob_job.get_item_obj(clean_road)
#     gen_clean_item = gen_bob_job.get_item_obj(clean_road)
#     assert gen_clean_item.fisc_tag == expected_clean_item.fisc_tag
#     assert gen_clean_item == expected_clean_item
#     assert gen_bob_job.get_item_obj(clean_road) == expected_clean_item
