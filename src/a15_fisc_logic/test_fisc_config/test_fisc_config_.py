from os import getcwd as os_getcwd
from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._test_util.a02_str import (
    bridge_str,
    celldepth_str,
    deal_time_str,
    fisc_label_str,
    owner_name_str,
    quota_str,
    tran_time_str,
)
from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.a07_calendar_logic._test_util.a07_str import (
    c400_number_str,
    monthday_distortion_str,
    timeline_label_str,
    yr1_jan1_offset_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    class_type_str,
    jkeys_str,
    jvalues_str,
    normal_specs_str,
)
from src.a08_bud_atom_logic.atom_config import get_allowed_class_types
from src.a15_fisc_logic._test_util.a15_str import (
    amount_str,
    cumlative_day_str,
    cumlative_minute_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
    fiscunit_str,
    hour_label_str,
    month_label_str,
    offi_time_str,
    weekday_label_str,
    weekday_order_str,
)
from src.a15_fisc_logic.fisc_config import (
    config_file_dir,
    get_fisc_args_class_types,
    get_fisc_args_dimen_mapping,
    get_fisc_args_set,
    get_fisc_config_dict,
    get_fisc_config_filename,
    get_fisc_dimens,
)


def test_get_fisc_config_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_fisc_config_filename() == "fisc_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "a15_fisc_logic")


def test_get_fisc_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    fisc_config = get_fisc_config_dict()

    # THEN
    assert fisc_config
    fisc_config_dimens = set(fisc_config.keys())
    assert fiscunit_str() in fisc_config_dimens
    assert fisc_dealunit_str() in fisc_config_dimens
    assert fisc_cashbook_str() in fisc_config_dimens
    assert fisc_timeline_hour_str() in fisc_config_dimens
    assert fisc_timeline_month_str() in fisc_config_dimens
    assert fisc_timeline_weekday_str() in fisc_config_dimens
    assert fisc_timeoffi_str() in fisc_config_dimens
    assert len(fisc_config) == 7
    _validate_fisc_config(fisc_config)
    fiscunit_dict = fisc_config.get(fiscunit_str())
    fisc_dealunit_dict = fisc_config.get(fisc_dealunit_str())
    fisc_cashbook_dict = fisc_config.get(fisc_cashbook_str())
    fisc_timeline_hour_dict = fisc_config.get(fisc_timeline_hour_str())
    fisc_timeline_month_dict = fisc_config.get(fisc_timeline_month_str())
    fisc_timeline_weekday_dict = fisc_config.get(fisc_timeline_weekday_str())
    # fisc_timeoffi_dict = fisc_config.get(fisc_timeoffi_str())
    assert len(fiscunit_dict.get(jkeys_str())) == 1
    assert len(fisc_dealunit_dict.get(jkeys_str())) == 3
    assert len(fisc_cashbook_dict.get(jkeys_str())) == 4
    assert len(fisc_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(fisc_timeline_month_dict.get(jkeys_str())) == 2
    assert len(fisc_timeline_weekday_dict.get(jkeys_str())) == 2
    # assert len(fisc_timeoffi_dict.get(jkeys_str())) == 2

    x_fiscunit_jvalues = {
        c400_number_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        timeline_label_str(),
        yr1_jan1_offset_str(),
        "job_listen_rotations",
    }
    print(f"{fiscunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(fiscunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_fiscunit_jvalues
    assert len(fiscunit_dict.get(jvalues_str())) == 9
    assert len(fisc_dealunit_dict.get(jvalues_str())) == 2
    assert len(fisc_cashbook_dict.get(jvalues_str())) == 1
    assert len(fisc_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(fisc_timeline_month_dict.get(jvalues_str())) == 1
    assert len(fisc_timeline_weekday_dict.get(jvalues_str())) == 1
    # assert len(fisc_timeoffi_dict.get(jvalues_str())) == 1


def _validate_fisc_config(fisc_config: dict):
    accepted_class_typees = get_allowed_class_types()
    accepted_class_typees.add("str")

    # for every fisc_format file there exists a unique fisc_number with leading zeros to make 5 digits
    for fisc_dimen, dimen_dict in fisc_config.items():
        print(f"_validate_fisc_config {fisc_dimen=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        if fisc_dimen == fisc_timeoffi_str():
            assert dimen_dict.get("fisc_static") == "False"
        else:
            assert dimen_dict.get("fisc_static") == "True"
        assert dimen_dict.get(UPDATE_str()) is None
        assert dimen_dict.get(INSERT_str()) is None
        assert dimen_dict.get(DELETE_str()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        fisc_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in fisc_jkeys_keys:
            jkey_dict = dimen_dict.get(jkeys_str())
            print(f"_validate_fisc_config {fisc_dimen=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees
        fisc_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in fisc_jvalues_keys:
            jvalue_dict = dimen_dict.get(jvalues_str())
            print(f"_validate_fisc_config {fisc_dimen=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees


def test_get_fisc_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    fisc_config_dimens = get_fisc_dimens()

    # THEN
    assert fiscunit_str() in fisc_config_dimens
    assert fisc_dealunit_str() in fisc_config_dimens
    assert fisc_cashbook_str() in fisc_config_dimens
    assert fisc_timeline_hour_str() in fisc_config_dimens
    assert fisc_timeline_month_str() in fisc_config_dimens
    assert fisc_timeline_weekday_str() in fisc_config_dimens
    assert fisc_timeoffi_str() in fisc_config_dimens
    assert len(fisc_config_dimens) == 7
    assert fisc_config_dimens == set(get_fisc_config_dict().keys())


def test_get_fisc_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_fisc_args_dimen_mapping = get_fisc_args_dimen_mapping()

    # THEN
    assert x_fisc_args_dimen_mapping
    x_hour = {fisc_timeline_hour_str()}
    assert x_fisc_args_dimen_mapping.get(cumlative_minute_str()) == x_hour
    assert x_fisc_args_dimen_mapping.get(fund_coin_str())
    fisc_label_dimens = x_fisc_args_dimen_mapping.get(fisc_label_str())
    assert fisc_timeline_hour_str() in fisc_label_dimens
    assert fiscunit_str() in fisc_label_dimens
    assert len(fisc_label_dimens) == 7
    assert len(x_fisc_args_dimen_mapping) == 24


def get_class_type(x_dimen: str, x_arg: str) -> str:
    fisc_config_dict = get_fisc_config_dict()
    dimen_dict = fisc_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(jvalues_str())
    required_dict = dimen_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(class_type_str())


def all_args_class_types_are_correct(x_class_types) -> bool:
    x_fisc_args_dimen_mapping = get_fisc_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_fisc_arg in x_sorted_class_types:
        x_dimens = list(x_fisc_args_dimen_mapping.get(x_fisc_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_class_type(x_dimen, x_fisc_arg)
        print(
            f"assert x_class_types.get({x_fisc_arg}) == {x_class_type} {x_class_types.get(x_fisc_arg)=}"
        )
        if x_class_types.get(x_fisc_arg) != x_class_type:
            return False
    return True


def test_get_fisc_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    fisc_args_class_types = get_fisc_args_class_types()

    # THEN
    fisc_args_from_dimens = set(get_fisc_args_dimen_mapping().keys())
    print(f"{fisc_args_from_dimens=}")
    assert set(fisc_args_class_types.keys()) == fisc_args_from_dimens
    assert all_args_class_types_are_correct(fisc_args_class_types)


def test_get_fisc_args_set_ReturnsObj():
    # ESTABLISH / WHEN
    fisc_args_set = get_fisc_args_set()

    # THEN
    assert fisc_args_set
    mapping_args_set = set(get_fisc_args_dimen_mapping().keys())
    print(f"{mapping_args_set=}")
    assert fisc_args_set == mapping_args_set
    assert len(fisc_args_set) == 24
    expected_fisc_args_set = {
        acct_name_str(),
        amount_str(),
        bridge_str(),
        c400_number_str(),
        cumlative_day_str(),
        cumlative_minute_str(),
        hour_label_str(),
        fisc_label_str(),
        fund_coin_str(),
        month_label_str(),
        monthday_distortion_str(),
        "job_listen_rotations",
        penny_str(),
        owner_name_str(),
        quota_str(),
        celldepth_str(),
        respect_bit_str(),
        deal_time_str(),
        tran_time_str(),
        offi_time_str(),
        timeline_label_str(),
        weekday_label_str(),
        weekday_order_str(),
        yr1_jan1_offset_str(),
    }
    assert fisc_args_set == expected_fisc_args_set
