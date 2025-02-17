from src.f00_instrument.file import save_file, open_file
from src.f00_instrument.dict_toolbox import get_json_from_dict
from src.f01_road.finance import default_fund_pool
from src.f01_road.deal import (
    quota_str,
    time_int_str,
    bridge_str,
    dealdepth_str,
    DealUnit,
    dealunit_shop,
    get_dealunit_from_dict,
    get_dealunit_from_json,
)
from pytest import raises as pytest_raises


# def test_set_dealunit_deal_nets_SetsAttrScenario0_dealdepth_0():
#     # ESTABLISH
#     x_deal = dealunit_shop(time_int=7, quota=45)


#     # WHEN


#     # THEN
#     assert x_deal._deal_nets != None
#     assert x_deal._deal_nets == {yao_str: 45, bob_str: -45}
