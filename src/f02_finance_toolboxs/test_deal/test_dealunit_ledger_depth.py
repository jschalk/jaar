from src.a00_data_toolboxs.file_toolbox import save_file, open_file
from src.a00_data_toolboxs.dict_toolbox import get_json_from_dict
from src.f02_finance_toolboxs.finance_config import default_fund_pool
from src.f02_finance_toolboxs.deal import (
    quota_str,
    deal_time_str,
    bridge_str,
    celldepth_str,
    DealUnit,
    dealunit_shop,
    get_dealunit_from_dict,
    get_dealunit_from_json,
)
from pytest import raises as pytest_raises


# def test_set_dealunit_deal_nets_SetsAttrScenario0_celldepth_0():
#     # ESTABLISH
#     x_deal = dealunit_shop(deal_time=7, quota=45)


#     # WHEN


#     # THEN
#     assert x_deal._deal_nets != None
#     assert x_deal._deal_nets == {yao_str: 45, bob_str: -45}
