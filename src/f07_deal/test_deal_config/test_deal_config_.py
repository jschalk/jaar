from src.f00_instrument.file import create_path
from src.f03_chrono.chrono import (
    c400_number_str,
    timeline_label_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
)
from src.f04_gift.atom_config import (
    deal_id_str,
    penny_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
    jkeys_str,
    jvalues_str,
    atom_update,
    atom_insert,
    atom_delete,
    normal_specs_str,
    jaar_type_str,
    type_AcctID_str,
    type_GroupID_str,
    type_IdeaUnit_str,
    type_RoadUnit_str,
    get_allowed_jaar_types,
)
from src.f07_deal.deal_config import (
    config_file_dir,
    get_deal_config_file_name,
    get_deal_config_dict,
    get_deal_args_category_mapping,
    current_time_str,
    amount_str,
    month_label_str,
    hour_label_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_label_str,
    weekday_order_str,
    dealunit_str,
    deal_purviewlog_str,
    deal_purview_episode_str,
    deal_cashbook_str,
    deal_timeline_hour_str,
    deal_timeline_month_str,
    deal_timeline_weekday_str,
    get_deal_categorys,
    get_deal_args_jaar_types,
)
from os import getcwd as os_getcwd


def test_str_functions_ReturnsObj():
    assert current_time_str() == "current_time"
    assert amount_str() == "amount"
    assert month_label_str() == "month_label"
    assert hour_label_str() == "hour_label"
    assert cumlative_minute_str() == "cumlative_minute"
    assert cumlative_day_str() == "cumlative_day"
    assert weekday_label_str() == "weekday_label"
    assert weekday_order_str() == "weekday_order"
    assert dealunit_str() == "dealunit"
    assert deal_purviewlog_str() == "deal_purviewlog"
    assert deal_purview_episode_str() == "deal_purview_episode"
    assert deal_cashbook_str() == "deal_cashbook"
    assert deal_timeline_hour_str() == "deal_timeline_hour"
    assert deal_timeline_month_str() == "deal_timeline_month"
    assert deal_timeline_weekday_str() == "deal_timeline_weekday"


def test_get_deal_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_deal_config_file_name() == "deal_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "f07_deal")


def test_get_deal_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    deal_config = get_deal_config_dict()

    # THEN
    assert deal_config
    deal_config_categorys = set(deal_config.keys())
    assert dealunit_str() in deal_config_categorys
    assert deal_purviewlog_str() not in deal_config_categorys
    assert deal_purview_episode_str() in deal_config_categorys
    assert deal_cashbook_str() in deal_config_categorys
    assert deal_timeline_hour_str() in deal_config_categorys
    assert deal_timeline_month_str() in deal_config_categorys
    assert deal_timeline_weekday_str() in deal_config_categorys
    assert len(deal_config) == 6
    _validate_deal_config(deal_config)
    dealunit_dict = deal_config.get(dealunit_str())
    deal_purview_episode_dict = deal_config.get(deal_purview_episode_str())
    deal_cashbook_dict = deal_config.get(deal_cashbook_str())
    deal_timeline_hour_dict = deal_config.get(deal_timeline_hour_str())
    deal_timeline_month_dict = deal_config.get(deal_timeline_month_str())
    deal_timeline_weekday_dict = deal_config.get(deal_timeline_weekday_str())
    assert len(dealunit_dict.get(jkeys_str())) == 0
    assert len(deal_purview_episode_dict.get(jkeys_str())) == 4
    assert len(deal_cashbook_dict.get(jkeys_str())) == 4
    assert len(deal_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(deal_timeline_month_dict.get(jkeys_str())) == 2
    assert len(deal_timeline_weekday_dict.get(jkeys_str())) == 2

    x_dealunit_jvalues = {
        c400_number_str(),
        current_time_str(),
        deal_id_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        "wall",
        timeline_label_str(),
        yr1_jan1_offset_str(),
    }
    print(f"{dealunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(dealunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_dealunit_jvalues
    assert len(dealunit_dict.get(jvalues_str())) == 10
    assert len(deal_purview_episode_dict.get(jvalues_str())) == 1
    assert len(deal_cashbook_dict.get(jvalues_str())) == 1
    assert len(deal_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(deal_timeline_month_dict.get(jvalues_str())) == 1
    assert len(deal_timeline_weekday_dict.get(jvalues_str())) == 1


def _validate_deal_config(deal_config: dict):
    accepted_jaar_typees = get_allowed_jaar_types()
    accepted_jaar_typees.add("str")

    # for every deal_format file there exists a unique deal_number always with leading zeros to make 5 digits
    for deal_categorys, cat_dict in deal_config.items():
        print(f"_validate_deal_config {deal_categorys=}")
        assert cat_dict.get(jkeys_str()) is not None
        assert cat_dict.get(jvalues_str()) is not None
        assert cat_dict.get(atom_update()) is None
        assert cat_dict.get(atom_insert()) is None
        assert cat_dict.get(atom_delete()) is None
        assert cat_dict.get(normal_specs_str()) is None

        deal_jkeys_keys = set(cat_dict.get(jkeys_str()).keys())
        for jkey_key in deal_jkeys_keys:
            jkey_dict = cat_dict.get(jkeys_str())
            print(f"_validate_deal_config {deal_categorys=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(jaar_type_str()) in accepted_jaar_typees
        deal_jvalues_keys = set(cat_dict.get(jvalues_str()).keys())
        for jvalue_key in deal_jvalues_keys:
            jvalue_dict = cat_dict.get(jvalues_str())
            print(f"_validate_deal_config {deal_categorys=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(jaar_type_str()) in accepted_jaar_typees


def test_get_deal_categorys_ReturnsObj():
    # ESTABLISH / WHEN
    deal_config_categorys = get_deal_categorys()

    # THEN
    assert dealunit_str() in deal_config_categorys
    assert deal_purviewlog_str() not in deal_config_categorys
    assert deal_purview_episode_str() in deal_config_categorys
    assert deal_cashbook_str() in deal_config_categorys
    assert deal_timeline_hour_str() in deal_config_categorys
    assert deal_timeline_month_str() in deal_config_categorys
    assert deal_timeline_weekday_str() in deal_config_categorys


def test_get_deal_args_category_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_deal_args_category_mapping = get_deal_args_category_mapping()

    # THEN
    assert x_deal_args_category_mapping
    assert x_deal_args_category_mapping.get(current_time_str())
    x_hour = {deal_timeline_hour_str()}
    assert x_deal_args_category_mapping.get(cumlative_minute_str()) == x_hour
    assert x_deal_args_category_mapping.get(fund_coin_str())
    deal_id_categorys = x_deal_args_category_mapping.get(deal_id_str())
    assert deal_timeline_hour_str() in deal_id_categorys
    assert dealunit_str() in deal_id_categorys
    assert len(deal_id_categorys) == 6
    assert len(x_deal_args_category_mapping) == 21


def get_jaar_type(x_category: str, x_arg: str) -> str:
    deal_config_dict = get_deal_config_dict()
    category_dict = deal_config_dict.get(x_category)
    optional_dict = category_dict.get(jvalues_str())
    required_dict = category_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = category_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(jaar_type_str())


def all_args_jaar_types_are_correct(x_jaar_types) -> bool:
    x_deal_args_category_mapping = get_deal_args_category_mapping()
    x_sorted_jaar_types = sorted(list(x_jaar_types.keys()))
    for x_deal_arg in x_sorted_jaar_types:
        x_categorys = list(x_deal_args_category_mapping.get(x_deal_arg))
        x_category = x_categorys[0]
        x_jaar_type = get_jaar_type(x_category, x_deal_arg)
        print(
            f"assert x_jaar_types.get({x_deal_arg}) == {x_jaar_type} {x_jaar_types.get(x_deal_arg)=}"
        )
        if x_jaar_types.get(x_deal_arg) != x_jaar_type:
            return False
    return True


def test_get_deal_args_jaar_types_ReturnsObj():
    # ESTABLISH / WHEN
    deal_args_jaar_types = get_deal_args_jaar_types()

    # THEN
    deal_args_from_categorys = set(get_deal_args_category_mapping().keys())
    print(f"{deal_args_from_categorys=}")
    assert set(deal_args_jaar_types.keys()) == deal_args_from_categorys
    assert all_args_jaar_types_are_correct(deal_args_jaar_types)
