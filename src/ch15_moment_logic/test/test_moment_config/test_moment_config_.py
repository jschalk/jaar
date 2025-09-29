from os import getcwd as os_getcwd
from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch09_belief_atom_logic.atom_config import get_allowed_class_types
from src.ch15_moment_logic._ref.ch15_keywords import (
    Ch09Keywords as wx,
    DELETE_str,
    INSERT_str,
    amount_str,
    belief_name_str,
    bud_time_str,
    c400_number_str,
    celldepth_str,
    class_type_str,
    cumulative_day_str,
    cumulative_minute_str,
    fund_iota_str,
    hour_label_str,
    jkeys_str,
    jvalues_str,
    knot_str,
    moment_budunit_str,
    moment_label_str,
    moment_paybook_str,
    moment_timeline_hour_str,
    moment_timeline_month_str,
    moment_timeline_weekday_str,
    moment_timeoffi_str,
    momentunit_str,
    month_label_str,
    monthday_distortion_str,
    normal_specs_str,
    offi_time_str,
    penny_str,
    quota_str,
    respect_bit_str,
    timeline_label_str,
    tran_time_str,
    voice_name_str,
    weekday_label_str,
    weekday_order_str,
    yr1_jan1_offset_str,
)
from src.ch15_moment_logic.moment_config import (
    get_moment_args_class_types,
    get_moment_args_dimen_mapping,
    get_moment_args_set,
    get_moment_config_dict,
    get_moment_dimens,
    moment_config_path,
)


def test_moment_config_path_ReturnsObj_Moment() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch15_moment_logic")
    assert moment_config_path() == create_path(chapter_dir, "moment_config.json")


def test_get_moment_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    moment_config = get_moment_config_dict()

    # THEN
    assert moment_config
    moment_config_dimens = set(moment_config.keys())
    assert momentunit_str() in moment_config_dimens
    assert moment_budunit_str() in moment_config_dimens
    assert moment_paybook_str() in moment_config_dimens
    assert moment_timeline_hour_str() in moment_config_dimens
    assert moment_timeline_month_str() in moment_config_dimens
    assert moment_timeline_weekday_str() in moment_config_dimens
    assert moment_timeoffi_str() in moment_config_dimens
    assert len(moment_config) == 7
    _validate_moment_config(moment_config)
    momentunit_dict = moment_config.get(momentunit_str())
    moment_budunit_dict = moment_config.get(moment_budunit_str())
    moment_paybook_dict = moment_config.get(moment_paybook_str())
    moment_timeline_hour_dict = moment_config.get(moment_timeline_hour_str())
    moment_timeline_month_dict = moment_config.get(moment_timeline_month_str())
    moment_timeline_weekday_dict = moment_config.get(moment_timeline_weekday_str())
    # moment_timeoffi_dict = moment_config.get(moment_timeoffi_str())
    assert len(momentunit_dict.get(jkeys_str())) == 1
    assert len(moment_budunit_dict.get(jkeys_str())) == 3
    assert len(moment_paybook_dict.get(jkeys_str())) == 4
    assert len(moment_timeline_hour_dict.get(jkeys_str())) == 2
    assert len(moment_timeline_month_dict.get(jkeys_str())) == 2
    assert len(moment_timeline_weekday_dict.get(jkeys_str())) == 2
    # assert len(moment_timeoffi_dict.get(jkeys_str())) == 2

    x_momentunit_jvalues = {
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
    print(f"{momentunit_dict.get(jvalues_str()).keys()=}")
    gen_jvalues = set(momentunit_dict.get(jvalues_str()).keys())
    assert gen_jvalues == x_momentunit_jvalues
    assert len(momentunit_dict.get(jvalues_str())) == 9
    assert len(moment_budunit_dict.get(jvalues_str())) == 2
    assert len(moment_paybook_dict.get(jvalues_str())) == 1
    assert len(moment_timeline_hour_dict.get(jvalues_str())) == 1
    assert len(moment_timeline_month_dict.get(jvalues_str())) == 1
    assert len(moment_timeline_weekday_dict.get(jvalues_str())) == 1
    # assert len(moment_timeoffi_dict.get(jvalues_str())) == 1


def _validate_moment_config(moment_config: dict):
    accepted_class_typees = get_allowed_class_types()
    accepted_class_typees.add("str")

    # for every moment_format file there exists a unique moment_number with leading zeros to make 5 digits
    for moment_dimen, dimen_dict in moment_config.items():
        print(f"_validate_moment_config {moment_dimen=}")
        assert dimen_dict.get(jkeys_str()) is not None
        assert dimen_dict.get(jvalues_str()) is not None
        if moment_dimen == moment_timeoffi_str():
            assert dimen_dict.get("moment_static") == "False"
        else:
            assert dimen_dict.get("moment_static") == "True"
        assert dimen_dict.get(wx.UPDATE) is None
        assert dimen_dict.get(INSERT_str()) is None
        assert dimen_dict.get(DELETE_str()) is None
        assert dimen_dict.get(normal_specs_str()) is None

        moment_jkeys_keys = set(dimen_dict.get(jkeys_str()).keys())
        for jkey_key in moment_jkeys_keys:
            jkey_dict = dimen_dict.get(jkeys_str())
            print(f"_validate_moment_config {moment_dimen=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees
        moment_jvalues_keys = set(dimen_dict.get(jvalues_str()).keys())
        for jvalue_key in moment_jvalues_keys:
            jvalue_dict = dimen_dict.get(jvalues_str())
            print(f"_validate_moment_config {moment_dimen=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(class_type_str()) in accepted_class_typees


def test_get_moment_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    moment_config_dimens = get_moment_dimens()

    # THEN
    assert momentunit_str() in moment_config_dimens
    assert moment_budunit_str() in moment_config_dimens
    assert moment_paybook_str() in moment_config_dimens
    assert moment_timeline_hour_str() in moment_config_dimens
    assert moment_timeline_month_str() in moment_config_dimens
    assert moment_timeline_weekday_str() in moment_config_dimens
    assert moment_timeoffi_str() in moment_config_dimens
    assert len(moment_config_dimens) == 7
    assert moment_config_dimens == set(get_moment_config_dict().keys())


def test_get_moment_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_moment_args_dimen_mapping = get_moment_args_dimen_mapping()

    # THEN
    assert x_moment_args_dimen_mapping
    x_hour = {moment_timeline_hour_str()}
    assert x_moment_args_dimen_mapping.get(cumulative_minute_str()) == x_hour
    assert x_moment_args_dimen_mapping.get(fund_iota_str())
    moment_label_dimens = x_moment_args_dimen_mapping.get(moment_label_str())
    assert moment_timeline_hour_str() in moment_label_dimens
    assert momentunit_str() in moment_label_dimens
    assert len(moment_label_dimens) == 7
    assert len(x_moment_args_dimen_mapping) == 24


def get_moment_class_type(x_dimen: str, x_arg: str) -> str:
    moment_config_dict = get_moment_config_dict()
    dimen_dict = moment_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(jvalues_str())
    required_dict = dimen_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(class_type_str())


def all_args_class_types_are_correct(x_class_types) -> bool:
    x_moment_args_dimen_mapping = get_moment_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_moment_arg in x_sorted_class_types:
        x_dimens = list(x_moment_args_dimen_mapping.get(x_moment_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_moment_class_type(x_dimen, x_moment_arg)
        print(
            f"assert x_class_types.get({x_moment_arg}) == {x_class_type} {x_class_types.get(x_moment_arg)=}"
        )
        if x_class_types.get(x_moment_arg) != x_class_type:
            return False
    return True


def test_get_moment_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    moment_args_class_types = get_moment_args_class_types()

    # THEN
    moment_args_from_dimens = set(get_moment_args_dimen_mapping().keys())
    print(f"{moment_args_from_dimens=}")
    assert set(moment_args_class_types.keys()) == moment_args_from_dimens
    assert all_args_class_types_are_correct(moment_args_class_types)


def test_get_moment_args_set_ReturnsObj():
    # ESTABLISH / WHEN
    moment_args_set = get_moment_args_set()

    # THEN
    assert moment_args_set
    mapping_args_set = set(get_moment_args_dimen_mapping().keys())
    print(f"{mapping_args_set=}")
    assert moment_args_set == mapping_args_set
    assert len(moment_args_set) == 24
    expected_moment_args_set = {
        voice_name_str(),
        amount_str(),
        knot_str(),
        c400_number_str(),
        cumulative_day_str(),
        cumulative_minute_str(),
        hour_label_str(),
        moment_label_str(),
        fund_iota_str(),
        month_label_str(),
        monthday_distortion_str(),
        # job_listen_rotations_str(),
        "job_listen_rotations",
        penny_str(),
        belief_name_str(),
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
    assert moment_args_set == expected_moment_args_set
