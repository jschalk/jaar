from src.f00_instrument.file import create_path, save_file, open_file
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f05_listen.hub_paths import (
    create_fisc_json_path,
    create_voice_path,
    create_forecast_path,
)
from src.f07_fisc.fisc import fiscunit_shop
from src.f10_etl.transformers import etl_fisc_voice_to_fisc_forecast
from src.f10_etl.examples.etl_env import env_dir_setup_cleanup, get_test_etl_dir
from os.path import exists as os_path_exists


def test_etl_fisc_voice_to_fisc_forecast_SetsFiles_Scenario0(
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
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    bob_voice = budunit_shop(bob_inx, a23_str)
    bob_voice.add_acctunit(bob_inx, credit77)
    bob_voice.add_acctunit(yao_inx, credit44)
    bob_voice.add_acctunit(bob_inx, credit77)
    bob_voice.add_acctunit(sue_inx, credit88)
    bob_voice.add_acctunit(yao_inx, credit44)
    a23_bob_voice_path = create_voice_path(fiscs_dir, a23_str, bob_inx)
    save_file(a23_bob_voice_path, None, bob_voice.get_json())
    a23_bob_forecast_path = create_forecast_path(fiscs_dir, a23_str, bob_inx)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, fiscunit_shop(a23_str, fisc_mstr_dir).get_json())
    assert os_path_exists(fisc_json_path)
    assert os_path_exists(a23_bob_voice_path)
    print(f"{a23_bob_voice_path=}")
    assert os_path_exists(a23_bob_forecast_path) is False

    # WHEN
    etl_fisc_voice_to_fisc_forecast(fisc_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_forecast_path)
    generated_forecast = budunit_get_from_json(open_file(a23_bob_forecast_path))
    expected_forecast = budunit_shop(bob_inx, a23_str)
    expected_forecast.add_acctunit(bob_inx, credit77)
    expected_forecast.add_acctunit(yao_inx, credit44)
    expected_forecast.add_acctunit(bob_inx, credit77)
    expected_forecast.add_acctunit(sue_inx, credit88)
    expected_forecast.add_acctunit(yao_inx, credit44)
    # assert generated_forecast.get_acct(sue_inx) == expected_forecast.get_acct(sue_inx)
    # assert generated_forecast.get_acct(bob_inx) == expected_forecast.get_acct(bob_inx)
    # assert generated_forecast.get_acct(yao_inx) == expected_forecast.get_acct(yao_inx)
    assert generated_forecast.accts.keys() == expected_forecast.accts.keys()
    # assert generated_forecast.accts == expected_forecast.accts
    # assert generated_forecast.get_item_dict() == expected_forecast.get_dict()
    # assert generated_forecast.get_dict() == expected_forecast.get_dict()
    # assert generated_forecast == expected_forecast
