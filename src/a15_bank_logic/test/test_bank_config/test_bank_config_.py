from os import getcwd as os_getcwd
from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic.test._util.a02_str import (
    bank_label_str,
    bud_time_str,
    celldepth_str,
    knot_str,
    owner_name_str,
    quota_str,
    tran_time_str,
)
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    fund_iota_str,
    penny_str,
    respect_bit_str,
)
from src.a07_timeline_logic.test._util.a07_str import (
    c400_number_str,
    monthday_distortion_str,
    timeline_label_str,
    yr1_jan1_offset_str,
)
from src.a08_plan_atom_logic.atom_config import get_allowed_class_types
from src.a08_plan_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    class_type_str,
    jkeys_str,
    jvalues_str,
    normal_specs_str,
)
from src.a15_bank_logic.bank_config import (
    config_file_dir,
    get_bank_args_class_types,
    get_bank_args_dimen_mapping,
    get_bank_args_set,
    get_bank_config_dict,
    get_bank_config_filename,
    get_bank_dimens,
)
from src.a15_bank_logic.test._util.a15_str import (
    amount_str,
    bank_budunit_str,
    bank_paybook_str,
    bank_timeline_hour_str,
    bank_timeline_month_str,
    bank_timeline_weekday_str,
    bank_timeoffi_str,
    bankunit_str,
    cumulative_day_str,
    cumulative_minute_str,
    hour_label_str,
    month_label_str,
    offi_time_str,
    weekday_label_str,
    weekday_order_str,
)


def test_get_bank_config_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_bank_config_filename() == "bank_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "a15_bank_logic")


def test_get_bank_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    bank_config = get_bank_config_dict()

    # THEN
    assert bank_config
    bank_config_dimens = set(bank_config.keys())
    assert bankunit_str() in bank_config_dimens
    assert bank_budunit_str() in bank_config_dimens
    assert bank_paybook_str() in bank_config_dimens
    assert bank_timeline_hour_str() in bank_config_dimens
    assert bank_timeline_month_str() in bank_config_dimens
    assert bank_timeline_weekday_str() in bank_config_dimens
    assert bank_timeoffi_str() in bank_config_dimens
    assert len(bank_config) == 7
    _validate_bank_config(bank_config)
    bankunit_dict = bank_config.get(bankunit_str())
    bank_budunit_dict = bank_config.get(bank_budunit_str())
    bank_paybook_dict = bank_config.get(bank_paybook_str())
    bank_timeline_hour_dict = bank_config.get(bank_timeline_hour_str())
    bank_timeline_month_dict = bank_config.get(bank_timeline_month_str())
    bank_timeline_weekday_dict = bank_config.get(bank_timeline_weekday_str())
    # bank_timeoffi_dict = bank_config.get(bank_timeoffi_str())
    assert len(bankunit_dict.get(jkeys_str())) == 1
    assert len(bank_budunit_dict.get(jkeys_str())) == 3
    assert len(bank_paybook_dict.get(jkeys_str())) == 4
    assert len(bank_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(bank_timeline_month_dict.get(jkeys_str())) == 2
    assert len(bank_timeline_weekday_dict.get(jkeys_str())) == 2
    # assert len(bank_timeoffi_dict.get(jkeys_str())) == 2

    x_bankunit_jvalues = {
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
    print(f"{bankunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(bankunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_bankunit_jvalues
    assert len(bankunit_dict.get(jvalues_str())) == 9
    assert len(bank_budunit_dict.get(jvalues_str())) == 2
    assert len(bank_paybook_dict.get(jvalues_str())) == 1
    assert len(bank_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(bank_timeline_month_dict.get(jvalues_str())) == 1
    assert len(bank_timeline_weekday_dict.get(jvalues_str())) == 1
    # assert len(bank_timeoffi_dict.get(jvalues_str())) == 1


def _validate_bank_config(bank_config: dict):
    accepted_class_typees = get_allowed_class_types()
    accepted_class_typees.add("str")

    # for every bank_format file there exists a unique bank_number with leading zeros to make 5 digits
    for bank_dimen, dimen_dict in bank_config.items():
        print(f"_validate_bank_config {bank_dimen=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        if bank_dimen == bank_timeoffi_str():
            assert dimen_dict.get("bank_static") == "False"
        else:
            assert dimen_dict.get("bank_static") == "True"
        assert dimen_dict.get(UPDATE_str()) is None
        assert dimen_dict.get(INSERT_str()) is None
        assert dimen_dict.get(DELETE_str()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        bank_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in bank_jkeys_keys:
            jkey_dict = dimen_dict.get(jkeys_str())
            print(f"_validate_bank_config {bank_dimen=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees
        bank_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in bank_jvalues_keys:
            jvalue_dict = dimen_dict.get(jvalues_str())
            print(f"_validate_bank_config {bank_dimen=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees


def test_get_bank_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    bank_config_dimens = get_bank_dimens()

    # THEN
    assert bankunit_str() in bank_config_dimens
    assert bank_budunit_str() in bank_config_dimens
    assert bank_paybook_str() in bank_config_dimens
    assert bank_timeline_hour_str() in bank_config_dimens
    assert bank_timeline_month_str() in bank_config_dimens
    assert bank_timeline_weekday_str() in bank_config_dimens
    assert bank_timeoffi_str() in bank_config_dimens
    assert len(bank_config_dimens) == 7
    assert bank_config_dimens == set(get_bank_config_dict().keys())


def test_get_bank_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_bank_args_dimen_mapping = get_bank_args_dimen_mapping()

    # THEN
    assert x_bank_args_dimen_mapping
    x_hour = {bank_timeline_hour_str()}
    assert x_bank_args_dimen_mapping.get(cumulative_minute_str()) == x_hour
    assert x_bank_args_dimen_mapping.get(fund_iota_str())
    bank_label_dimens = x_bank_args_dimen_mapping.get(bank_label_str())
    assert bank_timeline_hour_str() in bank_label_dimens
    assert bankunit_str() in bank_label_dimens
    assert len(bank_label_dimens) == 7
    assert len(x_bank_args_dimen_mapping) == 24


def get_class_type(x_dimen: str, x_arg: str) -> str:
    bank_config_dict = get_bank_config_dict()
    dimen_dict = bank_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(jvalues_str())
    required_dict = dimen_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(class_type_str())


def all_args_class_types_are_correct(x_class_types) -> bool:
    x_bank_args_dimen_mapping = get_bank_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_bank_arg in x_sorted_class_types:
        x_dimens = list(x_bank_args_dimen_mapping.get(x_bank_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_class_type(x_dimen, x_bank_arg)
        print(
            f"assert x_class_types.get({x_bank_arg}) == {x_class_type} {x_class_types.get(x_bank_arg)=}"
        )
        if x_class_types.get(x_bank_arg) != x_class_type:
            return False
    return True


def test_get_bank_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    bank_args_class_types = get_bank_args_class_types()

    # THEN
    bank_args_from_dimens = set(get_bank_args_dimen_mapping().keys())
    print(f"{bank_args_from_dimens=}")
    assert set(bank_args_class_types.keys()) == bank_args_from_dimens
    assert all_args_class_types_are_correct(bank_args_class_types)


def test_get_bank_args_set_ReturnsObj():
    # ESTABLISH / WHEN
    bank_args_set = get_bank_args_set()

    # THEN
    assert bank_args_set
    mapping_args_set = set(get_bank_args_dimen_mapping().keys())
    print(f"{mapping_args_set=}")
    assert bank_args_set == mapping_args_set
    assert len(bank_args_set) == 24
    expected_bank_args_set = {
        acct_name_str(),
        amount_str(),
        knot_str(),
        c400_number_str(),
        cumulative_day_str(),
        cumulative_minute_str(),
        hour_label_str(),
        bank_label_str(),
        fund_iota_str(),
        month_label_str(),
        monthday_distortion_str(),
        # job_listen_rotations_str(),
        "job_listen_rotations",
        penny_str(),
        owner_name_str(),
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
    assert bank_args_set == expected_bank_args_set
