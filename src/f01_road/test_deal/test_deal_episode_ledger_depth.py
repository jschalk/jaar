from src.f00_instrument.file import save_file, open_file
from src.f00_instrument.dict_toolbox import get_json_from_dict
from src.f01_road.finance import default_fund_pool
from src.f01_road.deal import (
    quota_str,
    time_int_str,
    bridge_str,
    ledger_depth_str,
    DealEpisode,
    dealepisode_shop,
    get_dealepisode_from_dict,
    get_dealepisode_from_json,
)
from pytest import raises as pytest_raises


# def test_set_deal_episode_net_deals_SetsAttrScenario0_ledger_depth_0():
#     # ESTABLISH
#     x_episode = dealepisode_shop(time_int=7, quota=45)


#     # WHEN


#     # THEN
#     assert x_episode._net_deals != None
#     assert x_episode._net_deals == {yao_str: 45, bob_str: -45}
