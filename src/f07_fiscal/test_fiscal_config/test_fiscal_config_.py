from src.f00_instrument.file import create_path
from src.f01_road.deal import (
    quota_str,
    time_int_str,
    bridge_str,
    ledger_depth_str,
)
from src.f03_chrono.chrono import (
    c400_number_str,
    timeline_title_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
)
from src.f04_gift.atom_config import (
    acct_name_str,
    owner_name_str,
    fiscal_title_str,
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
    class_type_str,
    get_allowed_class_types,
)
from src.f07_fiscal.fiscal_config import (
    config_file_dir,
    get_fiscal_config_file_name,
    get_fiscal_config_dict,
    get_fiscal_args_dimen_mapping,
    present_time_str,
    cumlative_minute_str,
    fiscalunit_str,
    fiscal_deal_episode_str,
    fiscal_cashbook_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
    get_fiscal_dimens,
    get_fiscal_args_class_types,
    get_fiscal_args_set,
    amount_str,
    cumlative_day_str,
    cumlative_minute_str,
    present_time_str,
    hour_title_str,
    month_title_str,
    weekday_title_str,
    weekday_order_str,
)
from os import getcwd as os_getcwd


def test_get_fiscal_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_fiscal_config_file_name() == "fiscal_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "f07_fiscal")


def test_get_fiscal_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    fiscal_config = get_fiscal_config_dict()

    # THEN
    assert fiscal_config
    fiscal_config_dimens = set(fiscal_config.keys())
    assert fiscalunit_str() in fiscal_config_dimens
    assert fiscal_deal_episode_str() in fiscal_config_dimens
    assert fiscal_cashbook_str() in fiscal_config_dimens
    assert fiscal_timeline_hour_str() in fiscal_config_dimens
    assert fiscal_timeline_month_str() in fiscal_config_dimens
    assert fiscal_timeline_weekday_str() in fiscal_config_dimens
    assert len(fiscal_config) == 6
    _validate_fiscal_config(fiscal_config)
    fiscalunit_dict = fiscal_config.get(fiscalunit_str())
    fiscal_deal_episode_dict = fiscal_config.get(fiscal_deal_episode_str())
    fiscal_cashbook_dict = fiscal_config.get(fiscal_cashbook_str())
    fiscal_timeline_hour_dict = fiscal_config.get(fiscal_timeline_hour_str())
    fiscal_timeline_month_dict = fiscal_config.get(fiscal_timeline_month_str())
    fiscal_timeline_weekday_dict = fiscal_config.get(fiscal_timeline_weekday_str())
    assert len(fiscalunit_dict.get(jkeys_str())) == 1
    assert len(fiscal_deal_episode_dict.get(jkeys_str())) == 3
    assert len(fiscal_cashbook_dict.get(jkeys_str())) == 4
    assert len(fiscal_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(fiscal_timeline_month_dict.get(jkeys_str())) == 2
    assert len(fiscal_timeline_weekday_dict.get(jkeys_str())) == 2

    x_fiscalunit_jvalues = {
        c400_number_str(),
        present_time_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        "bridge",
        timeline_title_str(),
        yr1_jan1_offset_str(),
    }
    print(f"{fiscalunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(fiscalunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_fiscalunit_jvalues
    assert len(fiscalunit_dict.get(jvalues_str())) == 9
    assert len(fiscal_deal_episode_dict.get(jvalues_str())) == 2
    assert len(fiscal_cashbook_dict.get(jvalues_str())) == 1
    assert len(fiscal_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(fiscal_timeline_month_dict.get(jvalues_str())) == 1
    assert len(fiscal_timeline_weekday_dict.get(jvalues_str())) == 1


def _validate_fiscal_config(fiscal_config: dict):
    accepted_class_typees = get_allowed_class_types()
    accepted_class_typees.add("str")

    # for every fiscal_format file there exists a unique fiscal_number always with leading zeros to make 5 digits
    for fiscal_dimens, dimen_dict in fiscal_config.items():
        print(f"_validate_fiscal_config {fiscal_dimens=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        assert dimen_dict.get(atom_update()) is None
        assert dimen_dict.get(atom_insert()) is None
        assert dimen_dict.get(atom_delete()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        fiscal_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in fiscal_jkeys_keys:
            jkey_dict = dimen_dict.get(jkeys_str())
            print(f"_validate_fiscal_config {fiscal_dimens=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees
        fiscal_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in fiscal_jvalues_keys:
            jvalue_dict = dimen_dict.get(jvalues_str())
            print(f"_validate_fiscal_config {fiscal_dimens=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees


def test_get_fiscal_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    fiscal_config_dimens = get_fiscal_dimens()

    # THEN
    assert fiscalunit_str() in fiscal_config_dimens
    assert fiscal_deal_episode_str() in fiscal_config_dimens
    assert fiscal_cashbook_str() in fiscal_config_dimens
    assert fiscal_timeline_hour_str() in fiscal_config_dimens
    assert fiscal_timeline_month_str() in fiscal_config_dimens
    assert fiscal_timeline_weekday_str() in fiscal_config_dimens
    assert len(fiscal_config_dimens) == 6
    return fiscal_config_dimens == set(get_fiscal_config_dict().keys())


def test_get_fiscal_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_fiscal_args_dimen_mapping = get_fiscal_args_dimen_mapping()

    # THEN
    assert x_fiscal_args_dimen_mapping
    assert x_fiscal_args_dimen_mapping.get(present_time_str())
    x_hour = {fiscal_timeline_hour_str()}
    assert x_fiscal_args_dimen_mapping.get(cumlative_minute_str()) == x_hour
    assert x_fiscal_args_dimen_mapping.get(fund_coin_str())
    fiscal_title_dimens = x_fiscal_args_dimen_mapping.get(fiscal_title_str())
    assert fiscal_timeline_hour_str() in fiscal_title_dimens
    assert fiscalunit_str() in fiscal_title_dimens
    assert len(fiscal_title_dimens) == 6
    assert len(x_fiscal_args_dimen_mapping) == 22


def get_class_type(x_dimen: str, x_arg: str) -> str:
    fiscal_config_dict = get_fiscal_config_dict()
    dimen_dict = fiscal_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(jvalues_str())
    required_dict = dimen_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(class_type_str())


def all_args_class_types_are_correct(x_class_types) -> bool:
    x_fiscal_args_dimen_mapping = get_fiscal_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_fiscal_arg in x_sorted_class_types:
        x_dimens = list(x_fiscal_args_dimen_mapping.get(x_fiscal_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_class_type(x_dimen, x_fiscal_arg)
        print(
            f"assert x_class_types.get({x_fiscal_arg}) == {x_class_type} {x_class_types.get(x_fiscal_arg)=}"
        )
        if x_class_types.get(x_fiscal_arg) != x_class_type:
            return False
    return True


def test_get_fiscal_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    fiscal_args_class_types = get_fiscal_args_class_types()

    # THEN
    fiscal_args_from_dimens = set(get_fiscal_args_dimen_mapping().keys())
    print(f"{fiscal_args_from_dimens=}")
    assert set(fiscal_args_class_types.keys()) == fiscal_args_from_dimens
    assert all_args_class_types_are_correct(fiscal_args_class_types)


def test_get_fiscal_args_set_ReturnsObj():
    # ESTABLISH / WHEN
    fiscal_args_set = get_fiscal_args_set()

    # THEN
    assert fiscal_args_set
    mapping_args_set = set(get_fiscal_args_dimen_mapping().keys())
    print(f"{mapping_args_set=}")
    assert fiscal_args_set == mapping_args_set
    assert len(fiscal_args_set) == 22
    expected_fiscal_args_set = {
        acct_name_str(),
        amount_str(),
        bridge_str(),
        c400_number_str(),
        cumlative_day_str(),
        cumlative_minute_str(),
        present_time_str(),
        hour_title_str(),
        fiscal_title_str(),
        fund_coin_str(),
        month_title_str(),
        monthday_distortion_str(),
        penny_str(),
        owner_name_str(),
        quota_str(),
        ledger_depth_str(),
        respect_bit_str(),
        time_int_str(),
        timeline_title_str(),
        weekday_title_str(),
        weekday_order_str(),
        yr1_jan1_offset_str(),
    }
    assert fiscal_args_set == expected_fiscal_args_set
