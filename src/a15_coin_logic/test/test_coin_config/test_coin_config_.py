from os import getcwd as os_getcwd
from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic.test._util.a02_str import knot_str
from src.a06_believer_logic.test._util.a06_str import (
    coin_label_str,
    fund_iota_str,
    partner_name_str,
    penny_str,
    respect_bit_str,
)
from src.a07_timeline_logic.test._util.a07_str import (
    c400_number_str,
    monthday_distortion_str,
    timeline_label_str,
    yr1_jan1_offset_str,
)
from src.a08_believer_atom_logic.atom_config import get_allowed_class_types
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    class_type_str,
    jkeys_str,
    jvalues_str,
    normal_specs_str,
)
from src.a11_bud_logic.test._util.a11_str import (
    believer_name_str,
    bud_time_str,
    celldepth_str,
    quota_str,
    tran_time_str,
)
from src.a15_coin_logic.coin_config import (
    coin_config_path,
    get_coin_args_class_types,
    get_coin_args_dimen_mapping,
    get_coin_args_set,
    get_coin_config_dict,
    get_coin_dimens,
)
from src.a15_coin_logic.test._util.a15_str import (
    amount_str,
    coin_budunit_str,
    coin_paybook_str,
    coin_timeline_hour_str,
    coin_timeline_month_str,
    coin_timeline_weekday_str,
    coin_timeoffi_str,
    coinunit_str,
    cumulative_day_str,
    cumulative_minute_str,
    hour_label_str,
    month_label_str,
    offi_time_str,
    weekday_label_str,
    weekday_order_str,
)


def test_coin_config_path_ReturnsObj_Coin() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    module_dir = create_path(src_dir, "a15_coin_logic")
    assert coin_config_path() == create_path(module_dir, "coin_config.json")


def test_get_coin_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    coin_config = get_coin_config_dict()

    # THEN
    assert coin_config
    coin_config_dimens = set(coin_config.keys())
    assert coinunit_str() in coin_config_dimens
    assert coin_budunit_str() in coin_config_dimens
    assert coin_paybook_str() in coin_config_dimens
    assert coin_timeline_hour_str() in coin_config_dimens
    assert coin_timeline_month_str() in coin_config_dimens
    assert coin_timeline_weekday_str() in coin_config_dimens
    assert coin_timeoffi_str() in coin_config_dimens
    assert len(coin_config) == 7
    _validate_coin_config(coin_config)
    coinunit_dict = coin_config.get(coinunit_str())
    coin_budunit_dict = coin_config.get(coin_budunit_str())
    coin_paybook_dict = coin_config.get(coin_paybook_str())
    coin_timeline_hour_dict = coin_config.get(coin_timeline_hour_str())
    coin_timeline_month_dict = coin_config.get(coin_timeline_month_str())
    coin_timeline_weekday_dict = coin_config.get(coin_timeline_weekday_str())
    # coin_timeoffi_dict = coin_config.get(coin_timeoffi_str())
    assert len(coinunit_dict.get(jkeys_str())) == 1
    assert len(coin_budunit_dict.get(jkeys_str())) == 3
    assert len(coin_paybook_dict.get(jkeys_str())) == 4
    assert len(coin_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(coin_timeline_month_dict.get(jkeys_str())) == 2
    assert len(coin_timeline_weekday_dict.get(jkeys_str())) == 2
    # assert len(coin_timeoffi_dict.get(jkeys_str())) == 2

    x_coinunit_jvalues = {
        c400_number_str(),
        fund_iota_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        knot_str(),
        timeline_label_str(),
        yr1_jan1_offset_str(),
        "job_listen_rotations",
        # job_listen_rotations_str(),
    }
    print(f"{coinunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(coinunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_coinunit_jvalues
    assert len(coinunit_dict.get(jvalues_str())) == 9
    assert len(coin_budunit_dict.get(jvalues_str())) == 2
    assert len(coin_paybook_dict.get(jvalues_str())) == 1
    assert len(coin_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(coin_timeline_month_dict.get(jvalues_str())) == 1
    assert len(coin_timeline_weekday_dict.get(jvalues_str())) == 1
    # assert len(coin_timeoffi_dict.get(jvalues_str())) == 1


def _validate_coin_config(coin_config: dict):
    accepted_class_typees = get_allowed_class_types()
    accepted_class_typees.add("str")

    # for every coin_format file there exists a unique coin_number with leading zeros to make 5 digits
    for coin_dimen, dimen_dict in coin_config.items():
        print(f"_validate_coin_config {coin_dimen=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        if coin_dimen == coin_timeoffi_str():
            assert dimen_dict.get("coin_static") == "False"
        else:
            assert dimen_dict.get("coin_static") == "True"
        assert dimen_dict.get(UPDATE_str()) is None
        assert dimen_dict.get(INSERT_str()) is None
        assert dimen_dict.get(DELETE_str()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        coin_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in coin_jkeys_keys:
            jkey_dict = dimen_dict.get(jkeys_str())
            print(f"_validate_coin_config {coin_dimen=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees
        coin_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in coin_jvalues_keys:
            jvalue_dict = dimen_dict.get(jvalues_str())
            print(f"_validate_coin_config {coin_dimen=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees


def test_get_coin_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    coin_config_dimens = get_coin_dimens()

    # THEN
    assert coinunit_str() in coin_config_dimens
    assert coin_budunit_str() in coin_config_dimens
    assert coin_paybook_str() in coin_config_dimens
    assert coin_timeline_hour_str() in coin_config_dimens
    assert coin_timeline_month_str() in coin_config_dimens
    assert coin_timeline_weekday_str() in coin_config_dimens
    assert coin_timeoffi_str() in coin_config_dimens
    assert len(coin_config_dimens) == 7
    assert coin_config_dimens == set(get_coin_config_dict().keys())


def test_get_coin_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_coin_args_dimen_mapping = get_coin_args_dimen_mapping()

    # THEN
    assert x_coin_args_dimen_mapping
    x_hour = {coin_timeline_hour_str()}
    assert x_coin_args_dimen_mapping.get(cumulative_minute_str()) == x_hour
    assert x_coin_args_dimen_mapping.get(fund_iota_str())
    coin_label_dimens = x_coin_args_dimen_mapping.get(coin_label_str())
    assert coin_timeline_hour_str() in coin_label_dimens
    assert coinunit_str() in coin_label_dimens
    assert len(coin_label_dimens) == 7
    assert len(x_coin_args_dimen_mapping) == 24


def get_class_type(x_dimen: str, x_arg: str) -> str:
    coin_config_dict = get_coin_config_dict()
    dimen_dict = coin_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(jvalues_str())
    required_dict = dimen_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(class_type_str())


def all_args_class_types_are_correct(x_class_types) -> bool:
    x_coin_args_dimen_mapping = get_coin_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_coin_arg in x_sorted_class_types:
        x_dimens = list(x_coin_args_dimen_mapping.get(x_coin_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_class_type(x_dimen, x_coin_arg)
        print(
            f"assert x_class_types.get({x_coin_arg}) == {x_class_type} {x_class_types.get(x_coin_arg)=}"
        )
        if x_class_types.get(x_coin_arg) != x_class_type:
            return False
    return True


def test_get_coin_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    coin_args_class_types = get_coin_args_class_types()

    # THEN
    coin_args_from_dimens = set(get_coin_args_dimen_mapping().keys())
    print(f"{coin_args_from_dimens=}")
    assert set(coin_args_class_types.keys()) == coin_args_from_dimens
    assert all_args_class_types_are_correct(coin_args_class_types)


def test_get_coin_args_set_ReturnsObj():
    # ESTABLISH / WHEN
    coin_args_set = get_coin_args_set()

    # THEN
    assert coin_args_set
    mapping_args_set = set(get_coin_args_dimen_mapping().keys())
    print(f"{mapping_args_set=}")
    assert coin_args_set == mapping_args_set
    assert len(coin_args_set) == 24
    expected_coin_args_set = {
        partner_name_str(),
        amount_str(),
        knot_str(),
        c400_number_str(),
        cumulative_day_str(),
        cumulative_minute_str(),
        hour_label_str(),
        coin_label_str(),
        fund_iota_str(),
        month_label_str(),
        monthday_distortion_str(),
        # job_listen_rotations_str(),
        "job_listen_rotations",
        penny_str(),
        believer_name_str(),
        quota_str(),
        celldepth_str(),
        respect_bit_str(),
        bud_time_str(),
        tran_time_str(),
        offi_time_str(),
        timeline_label_str(),
        weekday_label_str(),
        weekday_order_str(),
        yr1_jan1_offset_str(),
    }
    assert coin_args_set == expected_coin_args_set
