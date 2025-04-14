from src.f00_data_toolboxs.file_toolbox import create_path, save_file, open_file
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f06_listen.hub_path import (
    create_fisc_json_path,
    create_gut_path,
    create_plan_path,
)
from src.f08_fisc.fisc import fiscunit_shop
from src.f11_etl.transformers import etl_fisc_gut_to_fisc_plan
from src.f11_etl.examples.etl_env import env_dir_setup_cleanup, get_test_etl_dir
from os.path import exists as os_path_exists


def test_etl_fisc_gut_to_fisc_plan_SetsFiles_Scenario0(
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
    fisc_mstr_dir = get_test_etl_dir()
    bob_gut = budunit_shop(bob_inx, a23_str)
    bob_gut.add_acctunit(bob_inx, credit77)
    bob_gut.add_acctunit(yao_inx, credit44)
    bob_gut.add_acctunit(bob_inx, credit77)
    bob_gut.add_acctunit(sue_inx, credit88)
    bob_gut.add_acctunit(yao_inx, credit44)
    a23_bob_gut_path = create_gut_path(fisc_mstr_dir, a23_str, bob_inx)
    save_file(a23_bob_gut_path, None, bob_gut.get_json())
    a23_bob_plan_path = create_plan_path(fisc_mstr_dir, a23_str, bob_inx)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, fiscunit_shop(a23_str, fisc_mstr_dir).get_json())
    assert os_path_exists(fisc_json_path)
    assert os_path_exists(a23_bob_gut_path)
    print(f"{a23_bob_gut_path=}")
    assert os_path_exists(a23_bob_plan_path) is False

    # WHEN
    etl_fisc_gut_to_fisc_plan(fisc_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_plan_path)
    generated_plan = budunit_get_from_json(open_file(a23_bob_plan_path))
    expected_plan = budunit_shop(bob_inx, a23_str)
    expected_plan.add_acctunit(bob_inx, credit77)
    expected_plan.add_acctunit(yao_inx, credit44)
    expected_plan.add_acctunit(bob_inx, credit77)
    expected_plan.add_acctunit(sue_inx, credit88)
    expected_plan.add_acctunit(yao_inx, credit44)
    # assert generated_plan.get_acct(sue_inx) == expected_plan.get_acct(sue_inx)
    # assert generated_plan.get_acct(bob_inx) == expected_plan.get_acct(bob_inx)
    # assert generated_plan.get_acct(yao_inx) == expected_plan.get_acct(yao_inx)
    assert generated_plan.accts.keys() == expected_plan.accts.keys()
    # assert generated_plan.accts == expected_plan.accts
    # assert generated_plan.get_item_dict() == expected_plan.get_dict()
    # assert generated_plan.get_dict() == expected_plan.get_dict()
    # assert generated_plan == expected_plan
