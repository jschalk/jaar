from src.f00_instrument.file import create_path, save_file, open_file
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f06_listen.hub_path import (
    create_fisc_json_path,
    create_voice_path,
    create_forecast_path,
)
from src.f06_listen.special_func import create_pledge
from src.f08_fisc.fisc import fiscunit_shop
from src.f12_world.world import worldunit_shop
from src.f12_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_fisc_voice_to_fisc_forecast_SetsFiles_Scenario0(
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
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    bob_voice = budunit_shop(bob_inx, a23_str)
    bob_voice.add_acctunit(bob_inx, credit77)
    bob_voice.add_acctunit(yao_inx, credit44)
    bob_voice.add_acctunit(bob_inx, credit77)
    bob_voice.add_acctunit(sue_inx, credit88)
    bob_voice.add_acctunit(yao_inx, credit44)
    a23_bob_voice_path = create_voice_path(fisc_mstr_dir, a23_str, bob_inx)
    save_file(a23_bob_voice_path, None, bob_voice.get_json())
    a23_bob_forecast_path = create_forecast_path(fisc_mstr_dir, a23_str, bob_inx)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, fiscunit_shop(a23_str, fisc_mstr_dir).get_json())
    assert os_path_exists(a23_bob_voice_path)
    assert os_path_exists(a23_bob_forecast_path) is False

    # WHEN
    fizz_world.fisc_voice_to_fisc_forecast()

    # THEN
    assert os_path_exists(a23_bob_forecast_path)
    generated_forecast = budunit_get_from_json(open_file(a23_bob_forecast_path))
    expected_forecast = budunit_shop(bob_inx, a23_str)
    expected_forecast.add_acctunit(bob_inx, credit77)
    expected_forecast.add_acctunit(yao_inx, credit44)
    expected_forecast.add_acctunit(bob_inx, credit77)
    expected_forecast.add_acctunit(sue_inx, credit88)
    expected_forecast.add_acctunit(yao_inx, credit44)
    expected_forecast.settle_bud()
    assert generated_forecast.accts.keys() == expected_forecast.accts.keys()
    # assert generated_forecast.get_dict() == expected_forecast.get_dict()
    # assert generated_forecast == expected_forecast


def test_WorldUnit_fisc_voice_to_fisc_forecast_SetsFiles_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yao"
    a23_str = "accord23"
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    bob_voice = budunit_shop(bob_inx, a23_str)
    bob_voice.add_acctunit(bob_inx)
    bob_voice.add_acctunit(yao_inx)
    bob_voice.add_acctunit(bob_inx)
    bob_voice.add_acctunit(sue_inx)
    bob_voice.add_acctunit(yao_inx)
    clean_road = bob_voice.make_l1_road("clean")
    bob_voice.add_item(clean_road, pledge=True)

    yao_voice = budunit_shop(yao_inx, a23_str)
    yao_voice.add_acctunit(bob_inx)
    yao_voice.add_acctunit(yao_inx)
    run_road = bob_voice.make_l1_road("run")
    fly_road = bob_voice.make_l1_road("fly")
    yao_voice.add_item(run_road, pledge=True)
    yao_voice.add_item(fly_road, pledge=True)
    assert bob_voice.item_exists(clean_road)
    assert yao_voice.item_exists(clean_road) is False

    a23_bob_voice_path = create_voice_path(fisc_mstr_dir, a23_str, bob_inx)
    a23_yao_voice_path = create_voice_path(fisc_mstr_dir, a23_str, yao_inx)
    save_file(a23_bob_voice_path, None, bob_voice.get_json())
    save_file(a23_yao_voice_path, None, yao_voice.get_json())
    a23_bob_forecast_path = create_forecast_path(fisc_mstr_dir, a23_str, bob_inx)
    a23_yao_forecast_path = create_forecast_path(fisc_mstr_dir, a23_str, yao_inx)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, fiscunit_shop(a23_str, fisc_mstr_dir).get_json())
    assert os_path_exists(a23_bob_voice_path)
    assert os_path_exists(a23_yao_voice_path)
    assert os_path_exists(a23_bob_forecast_path) is False
    assert os_path_exists(a23_yao_forecast_path) is False

    # WHEN
    fizz_world.fisc_voice_to_fisc_forecast()
    fizz_world.fisc_voice_to_fisc_forecast()

    # THEN
    assert os_path_exists(a23_bob_forecast_path)
    assert os_path_exists(a23_yao_forecast_path)
    gen_bob_forecast = budunit_get_from_json(open_file(a23_bob_forecast_path))
    gen_yao_forecast = budunit_get_from_json(open_file(a23_yao_forecast_path))
    expected_bob_forecast = budunit_shop(bob_inx, a23_str)
    expected_yao_forecast = budunit_shop(yao_inx, a23_str)
    expected_bob_forecast.add_acctunit(bob_inx)
    expected_bob_forecast.add_acctunit(yao_inx)
    expected_bob_forecast.add_acctunit(bob_inx)
    expected_bob_forecast.add_acctunit(sue_inx)
    expected_bob_forecast.add_acctunit(yao_inx)
    expected_yao_forecast.add_acctunit(bob_inx)
    expected_yao_forecast.add_acctunit(yao_inx)
    expected_bob_forecast.add_item(clean_road, pledge=True)
    expected_bob_forecast.add_item(run_road, pledge=True)
    expected_bob_forecast.add_item(fly_road, pledge=True)
    expected_yao_forecast.add_item(clean_road, pledge=True)
    expected_yao_forecast.add_item(run_road, pledge=True)
    expected_yao_forecast.add_item(fly_road, pledge=True)

    assert gen_yao_forecast.accts.keys() == expected_yao_forecast.accts.keys()
    print(f"{gen_yao_forecast.get_item_dict().keys()=}")
    assert gen_yao_forecast.item_exists(clean_road)
    assert gen_yao_forecast.get_dict() == expected_yao_forecast.get_dict()

    assert gen_bob_forecast.accts.keys() == expected_bob_forecast.accts.keys()
    expected_bob_items = expected_bob_forecast.get_item_dict().keys()
    generate_bob_items = gen_bob_forecast.get_item_dict().keys()
    print(f"{expected_bob_items=}")
    print(f"{generate_bob_items=}")
    assert generate_bob_items == expected_bob_items
    expected_clean_item = expected_bob_forecast.get_item_obj(clean_road)
    gen_clean_item = gen_bob_forecast.get_item_obj(clean_road)
    assert gen_clean_item._bud_fisc_title == expected_clean_item._bud_fisc_title
    assert gen_clean_item == expected_clean_item
    assert gen_bob_forecast.get_item_obj(clean_road) == expected_clean_item
