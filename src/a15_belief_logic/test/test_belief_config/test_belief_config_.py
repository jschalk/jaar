from os import getcwd as os_getcwd
from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic.test._util.a02_str import knot_str
from src.a06_believer_logic.test._util.a06_str import (
    acct_name_str,
    belief_label_str,
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
from src.a15_belief_logic.belief_config import (
    config_file_dir,
    get_belief_args_class_types,
    get_belief_args_dimen_mapping,
    get_belief_args_set,
    get_belief_config_dict,
    get_belief_config_filename,
    get_belief_dimens,
)
from src.a15_belief_logic.test._util.a15_str import (
    amount_str,
    belief_budunit_str,
    belief_paybook_str,
    belief_timeline_hour_str,
    belief_timeline_month_str,
    belief_timeline_weekday_str,
    belief_timeoffi_str,
    beliefunit_str,
    cumulative_day_str,
    cumulative_minute_str,
    hour_label_str,
    month_label_str,
    offi_time_str,
    weekday_label_str,
    weekday_order_str,
)


def test_get_belief_config_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_belief_config_filename() == "belief_config.json"


def test_config_file_dir_ReturnsObj_Belief() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "a15_belief_logic")


def test_get_belief_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    belief_config = get_belief_config_dict()

    # THEN
    assert belief_config
    belief_config_dimens = set(belief_config.keys())
    assert beliefunit_str() in belief_config_dimens
    assert belief_budunit_str() in belief_config_dimens
    assert belief_paybook_str() in belief_config_dimens
    assert belief_timeline_hour_str() in belief_config_dimens
    assert belief_timeline_month_str() in belief_config_dimens
    assert belief_timeline_weekday_str() in belief_config_dimens
    assert belief_timeoffi_str() in belief_config_dimens
    assert len(belief_config) == 7
    _validate_belief_config(belief_config)
    beliefunit_dict = belief_config.get(beliefunit_str())
    belief_budunit_dict = belief_config.get(belief_budunit_str())
    belief_paybook_dict = belief_config.get(belief_paybook_str())
    belief_timeline_hour_dict = belief_config.get(belief_timeline_hour_str())
    belief_timeline_month_dict = belief_config.get(belief_timeline_month_str())
    belief_timeline_weekday_dict = belief_config.get(belief_timeline_weekday_str())
    # belief_timeoffi_dict = belief_config.get(belief_timeoffi_str())
    assert len(beliefunit_dict.get(jkeys_str())) == 1
    assert len(belief_budunit_dict.get(jkeys_str())) == 3
    assert len(belief_paybook_dict.get(jkeys_str())) == 4
    assert len(belief_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(belief_timeline_month_dict.get(jkeys_str())) == 2
    assert len(belief_timeline_weekday_dict.get(jkeys_str())) == 2
    # assert len(belief_timeoffi_dict.get(jkeys_str())) == 2

    x_beliefunit_jvalues = {
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
    print(f"{beliefunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(beliefunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_beliefunit_jvalues
    assert len(beliefunit_dict.get(jvalues_str())) == 9
    assert len(belief_budunit_dict.get(jvalues_str())) == 2
    assert len(belief_paybook_dict.get(jvalues_str())) == 1
    assert len(belief_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(belief_timeline_month_dict.get(jvalues_str())) == 1
    assert len(belief_timeline_weekday_dict.get(jvalues_str())) == 1
    # assert len(belief_timeoffi_dict.get(jvalues_str())) == 1


def _validate_belief_config(belief_config: dict):
    accepted_class_typees = get_allowed_class_types()
    accepted_class_typees.add("str")

    # for every belief_format file there exists a unique belief_number with leading zeros to make 5 digits
    for belief_dimen, dimen_dict in belief_config.items():
        print(f"_validate_belief_config {belief_dimen=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        if belief_dimen == belief_timeoffi_str():
            assert dimen_dict.get("belief_static") == "False"
        else:
            assert dimen_dict.get("belief_static") == "True"
        assert dimen_dict.get(UPDATE_str()) is None
        assert dimen_dict.get(INSERT_str()) is None
        assert dimen_dict.get(DELETE_str()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        belief_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in belief_jkeys_keys:
            jkey_dict = dimen_dict.get(jkeys_str())
            print(f"_validate_belief_config {belief_dimen=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees
        belief_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in belief_jvalues_keys:
            jvalue_dict = dimen_dict.get(jvalues_str())
            print(f"_validate_belief_config {belief_dimen=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees


def test_get_belief_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    belief_config_dimens = get_belief_dimens()

    # THEN
    assert beliefunit_str() in belief_config_dimens
    assert belief_budunit_str() in belief_config_dimens
    assert belief_paybook_str() in belief_config_dimens
    assert belief_timeline_hour_str() in belief_config_dimens
    assert belief_timeline_month_str() in belief_config_dimens
    assert belief_timeline_weekday_str() in belief_config_dimens
    assert belief_timeoffi_str() in belief_config_dimens
    assert len(belief_config_dimens) == 7
    assert belief_config_dimens == set(get_belief_config_dict().keys())


def test_get_belief_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_belief_args_dimen_mapping = get_belief_args_dimen_mapping()

    # THEN
    assert x_belief_args_dimen_mapping
    x_hour = {belief_timeline_hour_str()}
    assert x_belief_args_dimen_mapping.get(cumulative_minute_str()) == x_hour
    assert x_belief_args_dimen_mapping.get(fund_iota_str())
    belief_label_dimens = x_belief_args_dimen_mapping.get(belief_label_str())
    assert belief_timeline_hour_str() in belief_label_dimens
    assert beliefunit_str() in belief_label_dimens
    assert len(belief_label_dimens) == 7
    assert len(x_belief_args_dimen_mapping) == 24


def get_class_type(x_dimen: str, x_arg: str) -> str:
    belief_config_dict = get_belief_config_dict()
    dimen_dict = belief_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(jvalues_str())
    required_dict = dimen_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(class_type_str())


def all_args_class_types_are_correct(x_class_types) -> bool:
    x_belief_args_dimen_mapping = get_belief_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_belief_arg in x_sorted_class_types:
        x_dimens = list(x_belief_args_dimen_mapping.get(x_belief_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_class_type(x_dimen, x_belief_arg)
        print(
            f"assert x_class_types.get({x_belief_arg}) == {x_class_type} {x_class_types.get(x_belief_arg)=}"
        )
        if x_class_types.get(x_belief_arg) != x_class_type:
            return False
    return True


def test_get_belief_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    belief_args_class_types = get_belief_args_class_types()

    # THEN
    belief_args_from_dimens = set(get_belief_args_dimen_mapping().keys())
    print(f"{belief_args_from_dimens=}")
    assert set(belief_args_class_types.keys()) == belief_args_from_dimens
    assert all_args_class_types_are_correct(belief_args_class_types)


def test_get_belief_args_set_ReturnsObj():
    # ESTABLISH / WHEN
    belief_args_set = get_belief_args_set()

    # THEN
    assert belief_args_set
    mapping_args_set = set(get_belief_args_dimen_mapping().keys())
    print(f"{mapping_args_set=}")
    assert belief_args_set == mapping_args_set
    assert len(belief_args_set) == 24
    expected_belief_args_set = {
        acct_name_str(),
        amount_str(),
        knot_str(),
        c400_number_str(),
        cumulative_day_str(),
        cumulative_minute_str(),
        hour_label_str(),
        belief_label_str(),
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
    assert belief_args_set == expected_belief_args_set
