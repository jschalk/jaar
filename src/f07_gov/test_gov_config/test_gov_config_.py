from src.f00_instrument.file import create_path
from src.f03_chrono.chrono import (
    c400_number_str,
    timeline_idea_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
)
from src.f04_gift.atom_config import (
    gov_idea_str,
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
from src.f07_gov.gov_config import (
    config_file_dir,
    get_gov_config_file_name,
    get_gov_config_dict,
    get_gov_args_category_mapping,
    current_time_str,
    cumlative_minute_str,
    govunit_str,
    gov_pactlog_str,
    gov_pact_episode_str,
    gov_cashbook_str,
    gov_timeline_hour_str,
    gov_timeline_month_str,
    gov_timeline_weekday_str,
    get_gov_categorys,
    get_gov_args_jaar_types,
)
from os import getcwd as os_getcwd


def test_get_gov_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_gov_config_file_name() == "gov_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "f07_gov")


def test_get_gov_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    gov_config = get_gov_config_dict()

    # THEN
    assert gov_config
    gov_config_categorys = set(gov_config.keys())
    assert govunit_str() in gov_config_categorys
    assert gov_pactlog_str() not in gov_config_categorys
    assert gov_pact_episode_str() in gov_config_categorys
    assert gov_cashbook_str() in gov_config_categorys
    assert gov_timeline_hour_str() in gov_config_categorys
    assert gov_timeline_month_str() in gov_config_categorys
    assert gov_timeline_weekday_str() in gov_config_categorys
    assert len(gov_config) == 6
    _validate_gov_config(gov_config)
    govunit_dict = gov_config.get(govunit_str())
    gov_pact_episode_dict = gov_config.get(gov_pact_episode_str())
    gov_cashbook_dict = gov_config.get(gov_cashbook_str())
    gov_timeline_hour_dict = gov_config.get(gov_timeline_hour_str())
    gov_timeline_month_dict = gov_config.get(gov_timeline_month_str())
    gov_timeline_weekday_dict = gov_config.get(gov_timeline_weekday_str())
    assert len(govunit_dict.get(jkeys_str())) == 1
    assert len(gov_pact_episode_dict.get(jkeys_str())) == 3
    assert len(gov_cashbook_dict.get(jkeys_str())) == 4
    assert len(gov_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(gov_timeline_month_dict.get(jkeys_str())) == 2
    assert len(gov_timeline_weekday_dict.get(jkeys_str())) == 2

    x_govunit_jvalues = {
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
    print(f"{govunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(govunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_govunit_jvalues
    assert len(govunit_dict.get(jvalues_str())) == 9
    assert len(gov_pact_episode_dict.get(jvalues_str())) == 1
    assert len(gov_cashbook_dict.get(jvalues_str())) == 1
    assert len(gov_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(gov_timeline_month_dict.get(jvalues_str())) == 1
    assert len(gov_timeline_weekday_dict.get(jvalues_str())) == 1


def _validate_gov_config(gov_config: dict):
    accepted_jaar_typees = get_allowed_jaar_types()
    accepted_jaar_typees.add("str")

    # for every gov_format file there exists a unique gov_number always with leading zeros to make 5 digits
    for gov_categorys, cat_dict in gov_config.items():
        print(f"_validate_gov_config {gov_categorys=}")
        assert cat_dict.get(jkeys_str()) is not None
        assert cat_dict.get(jvalues_str()) is not None
        assert cat_dict.get(atom_update()) is None
        assert cat_dict.get(atom_insert()) is None
        assert cat_dict.get(atom_delete()) is None
        assert cat_dict.get(normal_specs_str()) is None

        gov_jkeys_keys = set(cat_dict.get(jkeys_str()).keys())
        for jkey_key in gov_jkeys_keys:
            jkey_dict = cat_dict.get(jkeys_str())
            print(f"_validate_gov_config {gov_categorys=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(jaar_type_str()) in accepted_jaar_typees
        gov_jvalues_keys = set(cat_dict.get(jvalues_str()).keys())
        for jvalue_key in gov_jvalues_keys:
            jvalue_dict = cat_dict.get(jvalues_str())
            print(f"_validate_gov_config {gov_categorys=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(jaar_type_str()) in accepted_jaar_typees


def test_get_gov_categorys_ReturnsObj():
    # ESTABLISH / WHEN
    gov_config_categorys = get_gov_categorys()

    # THEN
    assert govunit_str() in gov_config_categorys
    assert gov_pactlog_str() not in gov_config_categorys
    assert gov_pact_episode_str() in gov_config_categorys
    assert gov_cashbook_str() in gov_config_categorys
    assert gov_timeline_hour_str() in gov_config_categorys
    assert gov_timeline_month_str() in gov_config_categorys
    assert gov_timeline_weekday_str() in gov_config_categorys


def test_get_gov_args_category_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_gov_args_category_mapping = get_gov_args_category_mapping()

    # THEN
    assert x_gov_args_category_mapping
    assert x_gov_args_category_mapping.get(current_time_str())
    x_hour = {gov_timeline_hour_str()}
    assert x_gov_args_category_mapping.get(cumlative_minute_str()) == x_hour
    assert x_gov_args_category_mapping.get(fund_coin_str())
    gov_idea_categorys = x_gov_args_category_mapping.get(gov_idea_str())
    assert gov_timeline_hour_str() in gov_idea_categorys
    assert govunit_str() in gov_idea_categorys
    assert len(gov_idea_categorys) == 6
    assert len(x_gov_args_category_mapping) == 21


def get_jaar_type(x_category: str, x_arg: str) -> str:
    gov_config_dict = get_gov_config_dict()
    category_dict = gov_config_dict.get(x_category)
    optional_dict = category_dict.get(jvalues_str())
    required_dict = category_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = category_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(jaar_type_str())


def all_args_jaar_types_are_correct(x_jaar_types) -> bool:
    x_gov_args_category_mapping = get_gov_args_category_mapping()
    x_sorted_jaar_types = sorted(list(x_jaar_types.keys()))
    for x_gov_arg in x_sorted_jaar_types:
        x_categorys = list(x_gov_args_category_mapping.get(x_gov_arg))
        x_category = x_categorys[0]
        x_jaar_type = get_jaar_type(x_category, x_gov_arg)
        print(
            f"assert x_jaar_types.get({x_gov_arg}) == {x_jaar_type} {x_jaar_types.get(x_gov_arg)=}"
        )
        if x_jaar_types.get(x_gov_arg) != x_jaar_type:
            return False
    return True


def test_get_gov_args_jaar_types_ReturnsObj():
    # ESTABLISH / WHEN
    gov_args_jaar_types = get_gov_args_jaar_types()

    # THEN
    gov_args_from_categorys = set(get_gov_args_category_mapping().keys())
    print(f"{gov_args_from_categorys=}")
    assert set(gov_args_jaar_types.keys()) == gov_args_from_categorys
    assert all_args_jaar_types_are_correct(gov_args_jaar_types)
