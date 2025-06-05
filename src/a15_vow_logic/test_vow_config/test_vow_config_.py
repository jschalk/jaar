from os import getcwd as os_getcwd
from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._test_util.a02_str import (
    bridge_str,
    celldepth_str,
    deal_time_str,
    owner_name_str,
    quota_str,
    tran_time_str,
    vow_label_str,
)
from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    fund_iota_str,
    penny_str,
    respect_bit_str,
)
from src.a07_calendar_logic._test_util.a07_str import (
    c400_number_str,
    monthday_distortion_str,
    timeline_label_str,
    yr1_jan1_offset_str,
)
from src.a08_plan_atom_logic._test_util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    class_type_str,
    jkeys_str,
    jvalues_str,
    normal_specs_str,
)
from src.a08_plan_atom_logic.atom_config import get_allowed_class_types
from src.a15_vow_logic._test_util.a15_str import (
    amount_str,
    cumlative_day_str,
    cumlative_minute_str,
    hour_label_str,
    month_label_str,
    offi_time_str,
    vow_dealunit_str,
    vow_paybook_str,
    vow_timeline_hour_str,
    vow_timeline_month_str,
    vow_timeline_weekday_str,
    vow_timeoffi_str,
    vowunit_str,
    weekday_label_str,
    weekday_order_str,
)
from src.a15_vow_logic.vow_config import (
    config_file_dir,
    get_vow_args_class_types,
    get_vow_args_dimen_mapping,
    get_vow_args_set,
    get_vow_config_dict,
    get_vow_config_filename,
    get_vow_dimens,
)


def test_get_vow_config_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_vow_config_filename() == "vow_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "a15_vow_logic")


def test_get_vow_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    vow_config = get_vow_config_dict()

    # THEN
    assert vow_config
    vow_config_dimens = set(vow_config.keys())
    assert vowunit_str() in vow_config_dimens
    assert vow_dealunit_str() in vow_config_dimens
    assert vow_paybook_str() in vow_config_dimens
    assert vow_timeline_hour_str() in vow_config_dimens
    assert vow_timeline_month_str() in vow_config_dimens
    assert vow_timeline_weekday_str() in vow_config_dimens
    assert vow_timeoffi_str() in vow_config_dimens
    assert len(vow_config) == 7
    _validate_vow_config(vow_config)
    vowunit_dict = vow_config.get(vowunit_str())
    vow_dealunit_dict = vow_config.get(vow_dealunit_str())
    vow_paybook_dict = vow_config.get(vow_paybook_str())
    vow_timeline_hour_dict = vow_config.get(vow_timeline_hour_str())
    vow_timeline_month_dict = vow_config.get(vow_timeline_month_str())
    vow_timeline_weekday_dict = vow_config.get(vow_timeline_weekday_str())
    # vow_timeoffi_dict = vow_config.get(vow_timeoffi_str())
    assert len(vowunit_dict.get(jkeys_str())) == 1
    assert len(vow_dealunit_dict.get(jkeys_str())) == 3
    assert len(vow_paybook_dict.get(jkeys_str())) == 4
    assert len(vow_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(vow_timeline_month_dict.get(jkeys_str())) == 2
    assert len(vow_timeline_weekday_dict.get(jkeys_str())) == 2
    # assert len(vow_timeoffi_dict.get(jkeys_str())) == 2

    x_vowunit_jvalues = {
        c400_number_str(),
        fund_iota_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        timeline_label_str(),
        yr1_jan1_offset_str(),
        "job_listen_rotations",
    }
    print(f"{vowunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(vowunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_vowunit_jvalues
    assert len(vowunit_dict.get(jvalues_str())) == 9
    assert len(vow_dealunit_dict.get(jvalues_str())) == 2
    assert len(vow_paybook_dict.get(jvalues_str())) == 1
    assert len(vow_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(vow_timeline_month_dict.get(jvalues_str())) == 1
    assert len(vow_timeline_weekday_dict.get(jvalues_str())) == 1
    # assert len(vow_timeoffi_dict.get(jvalues_str())) == 1


def _validate_vow_config(vow_config: dict):
    accepted_class_typees = get_allowed_class_types()
    accepted_class_typees.add("str")

    # for every vow_format file there exists a unique vow_number with leading zeros to make 5 digits
    for vow_dimen, dimen_dict in vow_config.items():
        print(f"_validate_vow_config {vow_dimen=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        if vow_dimen == vow_timeoffi_str():
            assert dimen_dict.get("vow_static") == "False"
        else:
            assert dimen_dict.get("vow_static") == "True"
        assert dimen_dict.get(UPDATE_str()) is None
        assert dimen_dict.get(INSERT_str()) is None
        assert dimen_dict.get(DELETE_str()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        vow_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in vow_jkeys_keys:
            jkey_dict = dimen_dict.get(jkeys_str())
            print(f"_validate_vow_config {vow_dimen=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees
        vow_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in vow_jvalues_keys:
            jvalue_dict = dimen_dict.get(jvalues_str())
            print(f"_validate_vow_config {vow_dimen=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees


def test_get_vow_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    vow_config_dimens = get_vow_dimens()

    # THEN
    assert vowunit_str() in vow_config_dimens
    assert vow_dealunit_str() in vow_config_dimens
    assert vow_paybook_str() in vow_config_dimens
    assert vow_timeline_hour_str() in vow_config_dimens
    assert vow_timeline_month_str() in vow_config_dimens
    assert vow_timeline_weekday_str() in vow_config_dimens
    assert vow_timeoffi_str() in vow_config_dimens
    assert len(vow_config_dimens) == 7
    assert vow_config_dimens == set(get_vow_config_dict().keys())


def test_get_vow_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_vow_args_dimen_mapping = get_vow_args_dimen_mapping()

    # THEN
    assert x_vow_args_dimen_mapping
    x_hour = {vow_timeline_hour_str()}
    assert x_vow_args_dimen_mapping.get(cumlative_minute_str()) == x_hour
    assert x_vow_args_dimen_mapping.get(fund_iota_str())
    vow_label_dimens = x_vow_args_dimen_mapping.get(vow_label_str())
    assert vow_timeline_hour_str() in vow_label_dimens
    assert vowunit_str() in vow_label_dimens
    assert len(vow_label_dimens) == 7
    assert len(x_vow_args_dimen_mapping) == 24


def get_class_type(x_dimen: str, x_arg: str) -> str:
    vow_config_dict = get_vow_config_dict()
    dimen_dict = vow_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(jvalues_str())
    required_dict = dimen_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(class_type_str())


def all_args_class_types_are_correct(x_class_types) -> bool:
    x_vow_args_dimen_mapping = get_vow_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_vow_arg in x_sorted_class_types:
        x_dimens = list(x_vow_args_dimen_mapping.get(x_vow_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_class_type(x_dimen, x_vow_arg)
        print(
            f"assert x_class_types.get({x_vow_arg}) == {x_class_type} {x_class_types.get(x_vow_arg)=}"
        )
        if x_class_types.get(x_vow_arg) != x_class_type:
            return False
    return True


def test_get_vow_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    vow_args_class_types = get_vow_args_class_types()

    # THEN
    vow_args_from_dimens = set(get_vow_args_dimen_mapping().keys())
    print(f"{vow_args_from_dimens=}")
    assert set(vow_args_class_types.keys()) == vow_args_from_dimens
    assert all_args_class_types_are_correct(vow_args_class_types)


def test_get_vow_args_set_ReturnsObj():
    # ESTABLISH / WHEN
    vow_args_set = get_vow_args_set()

    # THEN
    assert vow_args_set
    mapping_args_set = set(get_vow_args_dimen_mapping().keys())
    print(f"{mapping_args_set=}")
    assert vow_args_set == mapping_args_set
    assert len(vow_args_set) == 24
    expected_vow_args_set = {
        acct_name_str(),
        amount_str(),
        bridge_str(),
        c400_number_str(),
        cumlative_day_str(),
        cumlative_minute_str(),
        hour_label_str(),
        vow_label_str(),
        fund_iota_str(),
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
    assert vow_args_set == expected_vow_args_set
