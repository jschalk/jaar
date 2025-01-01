from src.f00_instrument.file import create_path
from src.f03_chrono.chrono import (
    c400_number_str,
    timeline_idea_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
)
from src.f04_gift.atom_config import (
    cmty_idea_str,
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
    get_allowed_jaar_types,
)
from src.f07_cmty.cmty_config import (
    config_file_dir,
    get_cmty_config_file_name,
    get_cmty_config_dict,
    get_cmty_args_category_mapping,
    current_time_str,
    cumlative_minute_str,
    cmtyunit_str,
    cmty_deallog_str,
    cmty_deal_episode_str,
    cmty_cashbook_str,
    cmty_timeline_hour_str,
    cmty_timeline_month_str,
    cmty_timeline_weekday_str,
    get_cmty_categorys,
    get_cmty_args_jaar_types,
)
from os import getcwd as os_getcwd


def test_get_cmty_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_cmty_config_file_name() == "cmty_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "f07_cmty")


def test_get_cmty_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    cmty_config = get_cmty_config_dict()

    # THEN
    assert cmty_config
    cmty_config_categorys = set(cmty_config.keys())
    assert cmtyunit_str() in cmty_config_categorys
    assert cmty_deallog_str() not in cmty_config_categorys
    assert cmty_deal_episode_str() in cmty_config_categorys
    assert cmty_cashbook_str() in cmty_config_categorys
    assert cmty_timeline_hour_str() in cmty_config_categorys
    assert cmty_timeline_month_str() in cmty_config_categorys
    assert cmty_timeline_weekday_str() in cmty_config_categorys
    assert len(cmty_config) == 6
    _validate_cmty_config(cmty_config)
    cmtyunit_dict = cmty_config.get(cmtyunit_str())
    cmty_deal_episode_dict = cmty_config.get(cmty_deal_episode_str())
    cmty_cashbook_dict = cmty_config.get(cmty_cashbook_str())
    cmty_timeline_hour_dict = cmty_config.get(cmty_timeline_hour_str())
    cmty_timeline_month_dict = cmty_config.get(cmty_timeline_month_str())
    cmty_timeline_weekday_dict = cmty_config.get(cmty_timeline_weekday_str())
    assert len(cmtyunit_dict.get(jkeys_str())) == 1
    assert len(cmty_deal_episode_dict.get(jkeys_str())) == 3
    assert len(cmty_cashbook_dict.get(jkeys_str())) == 4
    assert len(cmty_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(cmty_timeline_month_dict.get(jkeys_str())) == 2
    assert len(cmty_timeline_weekday_dict.get(jkeys_str())) == 2

    x_cmtyunit_jvalues = {
        c400_number_str(),
        current_time_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        "bridge",
        timeline_idea_str(),
        yr1_jan1_offset_str(),
    }
    print(f"{cmtyunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(cmtyunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_cmtyunit_jvalues
    assert len(cmtyunit_dict.get(jvalues_str())) == 9
    assert len(cmty_deal_episode_dict.get(jvalues_str())) == 1
    assert len(cmty_cashbook_dict.get(jvalues_str())) == 1
    assert len(cmty_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(cmty_timeline_month_dict.get(jvalues_str())) == 1
    assert len(cmty_timeline_weekday_dict.get(jvalues_str())) == 1


def _validate_cmty_config(cmty_config: dict):
    accepted_jaar_typees = get_allowed_jaar_types()
    accepted_jaar_typees.add("str")

    # for every cmty_format file there exists a unique cmty_number always with leading zeros to make 5 digits
    for cmty_categorys, cat_dict in cmty_config.items():
        print(f"_validate_cmty_config {cmty_categorys=}")
        assert cat_dict.get(jkeys_str()) is not None
        assert cat_dict.get(jvalues_str()) is not None
        assert cat_dict.get(atom_update()) is None
        assert cat_dict.get(atom_insert()) is None
        assert cat_dict.get(atom_delete()) is None
        assert cat_dict.get(normal_specs_str()) is None

        cmty_jkeys_keys = set(cat_dict.get(jkeys_str()).keys())
        for jkey_key in cmty_jkeys_keys:
            jkey_dict = cat_dict.get(jkeys_str())
            print(f"_validate_cmty_config {cmty_categorys=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(jaar_type_str()) in accepted_jaar_typees
        cmty_jvalues_keys = set(cat_dict.get(jvalues_str()).keys())
        for jvalue_key in cmty_jvalues_keys:
            jvalue_dict = cat_dict.get(jvalues_str())
            print(f"_validate_cmty_config {cmty_categorys=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(jaar_type_str()) in accepted_jaar_typees


def test_get_cmty_categorys_ReturnsObj():
    # ESTABLISH / WHEN
    cmty_config_categorys = get_cmty_categorys()

    # THEN
    assert cmtyunit_str() in cmty_config_categorys
    assert cmty_deallog_str() not in cmty_config_categorys
    assert cmty_deal_episode_str() in cmty_config_categorys
    assert cmty_cashbook_str() in cmty_config_categorys
    assert cmty_timeline_hour_str() in cmty_config_categorys
    assert cmty_timeline_month_str() in cmty_config_categorys
    assert cmty_timeline_weekday_str() in cmty_config_categorys


def test_get_cmty_args_category_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_cmty_args_category_mapping = get_cmty_args_category_mapping()

    # THEN
    assert x_cmty_args_category_mapping
    assert x_cmty_args_category_mapping.get(current_time_str())
    x_hour = {cmty_timeline_hour_str()}
    assert x_cmty_args_category_mapping.get(cumlative_minute_str()) == x_hour
    assert x_cmty_args_category_mapping.get(fund_coin_str())
    cmty_idea_categorys = x_cmty_args_category_mapping.get(cmty_idea_str())
    assert cmty_timeline_hour_str() in cmty_idea_categorys
    assert cmtyunit_str() in cmty_idea_categorys
    assert len(cmty_idea_categorys) == 6
    assert len(x_cmty_args_category_mapping) == 21


def get_jaar_type(x_category: str, x_arg: str) -> str:
    cmty_config_dict = get_cmty_config_dict()
    category_dict = cmty_config_dict.get(x_category)
    optional_dict = category_dict.get(jvalues_str())
    required_dict = category_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = category_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(jaar_type_str())


def all_args_jaar_types_are_correct(x_jaar_types) -> bool:
    x_cmty_args_category_mapping = get_cmty_args_category_mapping()
    x_sorted_jaar_types = sorted(list(x_jaar_types.keys()))
    for x_cmty_arg in x_sorted_jaar_types:
        x_categorys = list(x_cmty_args_category_mapping.get(x_cmty_arg))
        x_category = x_categorys[0]
        x_jaar_type = get_jaar_type(x_category, x_cmty_arg)
        print(
            f"assert x_jaar_types.get({x_cmty_arg}) == {x_jaar_type} {x_jaar_types.get(x_cmty_arg)=}"
        )
        if x_jaar_types.get(x_cmty_arg) != x_jaar_type:
            return False
    return True


def test_get_cmty_args_jaar_types_ReturnsObj():
    # ESTABLISH / WHEN
    cmty_args_jaar_types = get_cmty_args_jaar_types()

    # THEN
    cmty_args_from_categorys = set(get_cmty_args_category_mapping().keys())
    print(f"{cmty_args_from_categorys=}")
    assert set(cmty_args_jaar_types.keys()) == cmty_args_from_categorys
    assert all_args_jaar_types_are_correct(cmty_args_jaar_types)
