from os import getcwd as os_getcwd
from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch09_belief_atom_logic.atom_config import get_allowed_class_types
from src.ch15_moment_logic.moment_config import (
    get_moment_args_class_types,
    get_moment_args_dimen_mapping,
    get_moment_args_set,
    get_moment_config_dict,
    get_moment_dimens,
    moment_config_path,
)
from src.ref.ch15_keywords import Ch15Keywords as wx


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
    assert wx.momentunit in moment_config_dimens
    assert wx.moment_budunit in moment_config_dimens
    assert wx.moment_paybook in moment_config_dimens
    assert wx.moment_epoch_hour in moment_config_dimens
    assert wx.moment_epoch_month in moment_config_dimens
    assert wx.moment_epoch_weekday in moment_config_dimens
    assert wx.moment_timeoffi in moment_config_dimens
    assert len(moment_config) == 7
    _validate_moment_config(moment_config)
    momentunit_dict = moment_config.get(wx.momentunit)
    moment_budunit_dict = moment_config.get(wx.moment_budunit)
    moment_paybook_dict = moment_config.get(wx.moment_paybook)
    moment_epoch_hour_dict = moment_config.get(wx.moment_epoch_hour)
    moment_epoch_month_dict = moment_config.get(wx.moment_epoch_month)
    moment_epoch_weekday_dict = moment_config.get(wx.moment_epoch_weekday)
    # moment_timeoffi_dict = moment_config.get(wx.moment_timeoffi)
    assert len(momentunit_dict.get(wx.jkeys)) == 1
    assert len(moment_budunit_dict.get(wx.jkeys)) == 3
    assert len(moment_paybook_dict.get(wx.jkeys)) == 4
    assert len(moment_epoch_hour_dict.get(wx.jkeys)) == 2
    assert len(moment_epoch_month_dict.get(wx.jkeys)) == 2
    assert len(moment_epoch_weekday_dict.get(wx.jkeys)) == 2
    # assert len(moment_timeoffi_dict.get(wx.jkeys)) == 2

    x_momentunit_jvalues = {
        wx.c400_number,
        wx.fund_grain,
        wx.monthday_index,
        wx.money_grain,
        wx.respect_grain,
        wx.knot,
        wx.epoch_label,
        wx.yr1_jan1_offset,
        "job_listen_rotations",
        # wx.job_listen_rotations,
    }
    print(f"{momentunit_dict.get(wx.jvalues).keys()=}")
    gen_jvalues = set(momentunit_dict.get(wx.jvalues).keys())
    assert gen_jvalues == x_momentunit_jvalues
    assert len(momentunit_dict.get(wx.jvalues)) == 9
    assert len(moment_budunit_dict.get(wx.jvalues)) == 2
    assert len(moment_paybook_dict.get(wx.jvalues)) == 1
    assert len(moment_epoch_hour_dict.get(wx.jvalues)) == 1
    assert len(moment_epoch_month_dict.get(wx.jvalues)) == 1
    assert len(moment_epoch_weekday_dict.get(wx.jvalues)) == 1
    # assert len(moment_timeoffi_dict.get(wx.jvalues)) == 1


def _validate_moment_config(moment_config: dict):
    accepted_class_typees = get_allowed_class_types()
    accepted_class_typees.add("str")

    # for every moment_format file there exists a unique moment_number with leading zeros to make 5 digits
    for moment_dimen, dimen_dict in moment_config.items():
        print(f"_validate_moment_config {moment_dimen=}")
        assert dimen_dict.get(wx.jkeys) is not None
        assert dimen_dict.get(wx.jvalues) is not None
        if moment_dimen == wx.moment_timeoffi:
            assert dimen_dict.get("moment_static") == "False"
        else:
            assert dimen_dict.get("moment_static") == "True"
        assert dimen_dict.get(wx.UPDATE) is None
        assert dimen_dict.get(wx.INSERT) is None
        assert dimen_dict.get(wx.DELETE) is None
        assert dimen_dict.get(wx.normal_specs) is None

        moment_jkeys_keys = set(dimen_dict.get(wx.jkeys).keys())
        for jkey_key in moment_jkeys_keys:
            jkey_dict = dimen_dict.get(wx.jkeys)
            print(f"_validate_moment_config {moment_dimen=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(wx.class_type) in accepted_class_typees
        moment_jvalues_keys = set(dimen_dict.get(wx.jvalues).keys())
        for jvalue_key in moment_jvalues_keys:
            jvalue_dict = dimen_dict.get(wx.jvalues)
            print(f"_validate_moment_config {moment_dimen=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(wx.class_type) in accepted_class_typees


def test_get_moment_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    moment_config_dimens = get_moment_dimens()

    # THEN
    assert wx.momentunit in moment_config_dimens
    assert wx.moment_budunit in moment_config_dimens
    assert wx.moment_paybook in moment_config_dimens
    assert wx.moment_epoch_hour in moment_config_dimens
    assert wx.moment_epoch_month in moment_config_dimens
    assert wx.moment_epoch_weekday in moment_config_dimens
    assert wx.moment_timeoffi in moment_config_dimens
    assert len(moment_config_dimens) == 7
    assert moment_config_dimens == set(get_moment_config_dict().keys())


def test_get_moment_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_moment_args_dimen_mapping = get_moment_args_dimen_mapping()

    # THEN
    assert x_moment_args_dimen_mapping
    x_hour = {wx.moment_epoch_hour}
    assert x_moment_args_dimen_mapping.get(wx.cumulative_minute) == x_hour
    assert x_moment_args_dimen_mapping.get(wx.fund_grain)
    moment_label_dimens = x_moment_args_dimen_mapping.get(wx.moment_label)
    assert wx.moment_epoch_hour in moment_label_dimens
    assert wx.momentunit in moment_label_dimens
    assert len(moment_label_dimens) == 7
    assert len(x_moment_args_dimen_mapping) == 24


def get_moment_class_type(x_dimen: str, x_arg: str) -> str:
    moment_config_dict = get_moment_config_dict()
    dimen_dict = moment_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(wx.jvalues)
    required_dict = dimen_dict.get(wx.jkeys)
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(wx.jvalues).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(wx.class_type)


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
        wx.voice_name,
        wx.amount,
        wx.knot,
        wx.c400_number,
        wx.cumulative_day,
        wx.cumulative_minute,
        wx.hour_label,
        wx.moment_label,
        wx.fund_grain,
        wx.month_label,
        wx.monthday_index,
        # wx.job_listen_rotations,
        "job_listen_rotations",
        wx.money_grain,
        wx.belief_name,
        wx.quota,
        wx.celldepth,
        wx.respect_grain,
        wx.bud_time,
        wx.tran_time,
        wx.offi_time,
        wx.epoch_label,
        wx.weekday_label,
        wx.weekday_order,
        wx.yr1_jan1_offset,
    }
    assert moment_args_set == expected_moment_args_set
