from pytest import raises as pytest_raises
from src.a01_term_logic.rope import default_knot_if_None
from src.a06_believer_logic.test._util.a06_str import (
    LabelTerm_str,
    NameTerm_str,
    RopeTerm_str,
    TitleTerm_str,
    awardee_title_str,
    belief_label_str,
    believer_name_str,
    f_context_str,
    f_lower_str,
    f_state_str,
    fund_iota_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    p_state_str,
    partner_name_str,
    penny_str,
    plan_label_str,
    plan_rope_str,
    r_context_str,
    respect_bit_str,
)
from src.a07_timeline_logic.test._util.a07_str import timeline_label_str
from src.a08_believer_atom_logic.atom_config import (
    get_all_believer_dimen_delete_keys,
    get_atom_args_class_types,
)
from src.a09_pack_logic.test._util.a09_str import face_name_str
from src.a15_belief_logic.belief_config import get_belief_args_class_types
from src.a15_belief_logic.test._util.a15_str import (
    hour_label_str,
    month_label_str,
    weekday_label_str,
)
from src.a16_pidgin_logic.map import (
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)
from src.a16_pidgin_logic.pidgin import PidginUnit, pidginunit_shop
from src.a16_pidgin_logic.pidgin_config import (
    default_unknown_str_if_None,
    find_set_otx_inx_args,
    get_pidgin_args_class_types,
    get_pidgin_LabelTerm_args,
    get_pidgin_NameTerm_args,
    get_pidgin_RopeTerm_args,
    get_pidgin_TitleTerm_args,
    get_pidginable_args,
    pidginable_class_types,
)
from src.a16_pidgin_logic.test._util.example_pidgins import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_invalid_namemap,
    get_invalid_ropemap,
    get_invalid_titlemap,
    get_suita_namemap,
    get_swim_titlemap,
)


def test_get_pidgin_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_args_class_types = get_pidgin_args_class_types()

    # THEN
    assert pidgin_args_class_types.get("partner_name") == NameTerm_str()
    assert pidgin_args_class_types.get("addin") == "float"
    assert pidgin_args_class_types.get("amount") == "float"
    assert pidgin_args_class_types.get("awardee_title") == TitleTerm_str()
    assert pidgin_args_class_types.get("r_context") == RopeTerm_str()
    assert pidgin_args_class_types.get("r_plan_active_requisite") == "bool"
    assert pidgin_args_class_types.get("begin") == "float"
    assert pidgin_args_class_types.get("c400_number") == "int"
    assert pidgin_args_class_types.get("close") == "float"
    assert pidgin_args_class_types.get("partner_cred_points") == "float"
    assert pidgin_args_class_types.get("group_cred_points") == "float"
    assert pidgin_args_class_types.get("credor_respect") == "float"
    assert pidgin_args_class_types.get("cumulative_day") == "int"
    assert pidgin_args_class_types.get("cumulative_minute") == "int"
    assert pidgin_args_class_types.get("partner_debt_points") == "float"
    assert pidgin_args_class_types.get("group_debt_points") == "float"
    assert pidgin_args_class_types.get("debtor_respect") == "float"
    assert pidgin_args_class_types.get("denom") == "int"
    assert pidgin_args_class_types.get("p_divisor") == "int"
    assert pidgin_args_class_types.get("face_name") == NameTerm_str()
    assert pidgin_args_class_types.get("f_context") == RopeTerm_str()
    assert pidgin_args_class_types.get("belief_label") == LabelTerm_str()
    assert pidgin_args_class_types.get("f_upper") == "float"
    assert pidgin_args_class_types.get("f_lower") == "float"
    assert pidgin_args_class_types.get("fund_iota") == "float"
    assert pidgin_args_class_types.get("fund_pool") == "float"
    assert pidgin_args_class_types.get("give_force") == "float"
    assert pidgin_args_class_types.get("gogo_want") == "float"
    assert pidgin_args_class_types.get("group_title") == TitleTerm_str()
    assert pidgin_args_class_types.get("healer_name") == NameTerm_str()
    assert pidgin_args_class_types.get("hour_label") == LabelTerm_str()
    assert pidgin_args_class_types.get("mass") == "int"
    assert pidgin_args_class_types.get("max_tree_traverse") == "int"
    assert pidgin_args_class_types.get("month_label") == LabelTerm_str()
    assert pidgin_args_class_types.get("monthday_distortion") == "int"
    assert pidgin_args_class_types.get("morph") == "bool"
    assert pidgin_args_class_types.get("p_state") == RopeTerm_str()
    assert pidgin_args_class_types.get("p_upper") == "float"
    assert pidgin_args_class_types.get("numor") == "int"
    assert pidgin_args_class_types.get("offi_time") == "TimeLinePoint"
    assert pidgin_args_class_types.get("believer_name") == NameTerm_str()
    assert pidgin_args_class_types.get("p_lower") == "float"
    assert pidgin_args_class_types.get("penny") == "float"
    assert pidgin_args_class_types.get("f_state") == RopeTerm_str()
    assert pidgin_args_class_types.get("task") == "bool"
    assert pidgin_args_class_types.get("problem_bool") == "bool"
    assert pidgin_args_class_types.get("quota") == "int"
    assert pidgin_args_class_types.get("respect_bit") == "float"
    assert pidgin_args_class_types.get("plan_rope") == RopeTerm_str()
    assert pidgin_args_class_types.get("celldepth") == "int"
    assert pidgin_args_class_types.get("stop_want") == "float"
    assert pidgin_args_class_types.get("take_force") == "float"
    assert pidgin_args_class_types.get("tally") == "int"
    assert pidgin_args_class_types.get("labor_title") == TitleTerm_str()
    assert pidgin_args_class_types.get("bud_time") == "TimeLinePoint"
    assert pidgin_args_class_types.get("tran_time") == "TimeLinePoint"
    assert pidgin_args_class_types.get("timeline_label") == LabelTerm_str()
    assert pidgin_args_class_types.get("weekday_label") == LabelTerm_str()
    assert pidgin_args_class_types.get("weekday_order") == "int"
    assert pidgin_args_class_types.get("knot") == "str"
    assert pidgin_args_class_types.get("yr1_jan1_offset") == "int"

    # make sure it pidgin_arg_class_types has all belief and all atom args
    pidgin_args = set(pidgin_args_class_types.keys())
    atom_args = set(get_atom_args_class_types().keys())
    belief_args = set(get_belief_args_class_types().keys())
    assert atom_args.issubset(pidgin_args)
    assert belief_args.issubset(pidgin_args)
    assert atom_args.intersection(belief_args) == {
        partner_name_str(),
        fund_iota_str(),
        penny_str(),
        respect_bit_str(),
    }
    assert atom_args.union(belief_args) != pidgin_args
    assert atom_args.union(belief_args).union({"face_name"}) == pidgin_args
    assert check_class_types_are_correct()
    # assert pidgin_args_class_types.keys() == get_atom_args_dimen_mapping().keys()
    # assert all_atom_args_class_types_are_correct(x_class_types)


def check_class_types_are_correct() -> bool:
    pidgin_args_class_types = get_pidgin_args_class_types()
    atom_args_class_types = get_atom_args_class_types()
    belief_args_class_types = get_belief_args_class_types()
    for pidgin_arg, pidgin_type in pidgin_args_class_types.items():
        print(f"check {pidgin_arg=} {pidgin_type=}")
        if atom_args_class_types.get(pidgin_arg) not in [None, pidgin_type]:
            print(
                f"{pidgin_arg=} {pidgin_type=} {atom_args_class_types.get(pidgin_arg)=}"
            )
            return False
        if belief_args_class_types.get(pidgin_arg) not in [None, pidgin_type]:
            print(
                f"{pidgin_arg=} {pidgin_type=} {belief_args_class_types.get(pidgin_arg)=}"
            )
            return False
    return True


def test_pidginable_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginable_class_types = pidginable_class_types()

    # THEN
    assert len(x_pidginable_class_types) == 4
    assert x_pidginable_class_types == {
        NameTerm_str(),
        TitleTerm_str(),
        LabelTerm_str(),
        RopeTerm_str(),
    }
    print(f"{set(get_atom_args_class_types().values())=}")
    all_atom_class_types = set(get_atom_args_class_types().values())
    all_atom_class_types.add(LabelTerm_str())
    inter_x = set(all_atom_class_types).intersection(x_pidginable_class_types)
    assert inter_x == x_pidginable_class_types


def test_get_pidginable_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{pidginable_class_types()=}")
    all_pidgin_args = set(get_pidgin_args_class_types().keys())
    print(f"{get_pidginable_args().difference(all_pidgin_args)}")
    assert get_pidginable_args().issubset(all_pidgin_args)
    static_get_pidginable_args = {
        x_arg
        for x_arg, class_type in get_pidgin_args_class_types().items()
        if class_type in pidginable_class_types()
    }
    assert get_pidginable_args() == static_get_pidginable_args

    assert len(get_pidginable_args()) == 17
    assert get_pidginable_args() == {
        partner_name_str(),
        awardee_title_str(),
        r_context_str(),
        face_name_str(),
        f_context_str(),
        belief_label_str(),
        f_state_str(),
        group_title_str(),
        healer_name_str(),
        hour_label_str(),
        month_label_str(),
        p_state_str(),
        believer_name_str(),
        plan_rope_str(),
        labor_title_str(),
        timeline_label_str(),
        weekday_label_str(),
    }


def test_find_set_otx_inx_args_ReturnsObj_Scenario0_All_pidginable_args():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    pidginable_args = get_pidginable_args()

    # WHEN
    otx_inx_args = find_set_otx_inx_args(pidginable_args)

    # THEN
    expected_otx_inx_args = set()
    for pidginable_arg in pidginable_args:
        expected_otx_inx_args.add(f"{pidginable_arg}_otx")
        expected_otx_inx_args.add(f"{pidginable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario1_believer_dimen_delete_keys():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    believer_dimen_delete_keys = get_all_believer_dimen_delete_keys()

    # WHEN
    otx_inx_args = find_set_otx_inx_args(believer_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for pidginable_arg in believer_dimen_delete_keys:
        expected_otx_inx_args.add(f"{pidginable_arg}_otx")
        expected_otx_inx_args.add(f"{pidginable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario2_OtherArgsAreUntouched():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    run_str = "run"
    given_believer_dimen_delete_keys = get_all_believer_dimen_delete_keys()
    given_believer_dimen_delete_keys.add(run_str)

    # WHEN
    otx_inx_args = find_set_otx_inx_args(given_believer_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for pidginable_arg in get_all_believer_dimen_delete_keys():
        expected_otx_inx_args.add(f"{pidginable_arg}_otx")
        expected_otx_inx_args.add(f"{pidginable_arg}_inx")
    expected_otx_inx_args.add(run_str)
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario3_PartialSets():
    # ESTABLISH
    healer_name_ERASE_str = f"{healer_name_str()}_ERASE"
    run_str = "run"
    given_believer_dimen_delete_keys = {run_str, healer_name_ERASE_str}

    # WHEN
    otx_inx_args = find_set_otx_inx_args(given_believer_dimen_delete_keys)

    # THEN
    healer_name_ERASE_str = f"{healer_name_str()}_ERASE"
    expected_otx_inx_args = {
        f"{healer_name_ERASE_str}_otx",
        f"{healer_name_ERASE_str}_inx",
        run_str,
    }
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_get_pidgin_NameTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_NameTerm_args = get_pidgin_NameTerm_args()

    # THEN
    assert pidgin_NameTerm_args == {
        partner_name_str(),
        face_name_str(),
        healer_name_str(),
        believer_name_str(),
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_pidgin_args_class_types().items()
        if class_type == NameTerm_str()
    }
    assert pidgin_NameTerm_args == expected_args


def test_get_pidgin_TitleTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_TitleTerm_args = get_pidgin_TitleTerm_args()

    # THEN
    assert pidgin_TitleTerm_args == {
        awardee_title_str(),
        group_title_str(),
        labor_title_str(),
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_pidgin_args_class_types().items()
        if class_type == TitleTerm_str()
    }
    assert pidgin_TitleTerm_args == expected_args


def test_get_pidgin_LabelTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_LabelTerm_args = get_pidgin_LabelTerm_args()

    # THEN
    assert pidgin_LabelTerm_args == {
        belief_label_str(),
        hour_label_str(),
        month_label_str(),
        timeline_label_str(),
        weekday_label_str(),
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_pidgin_args_class_types().items()
        if class_type == LabelTerm_str()
    }
    assert pidgin_LabelTerm_args == expected_args


def test_get_pidgin_RopeTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_RopeTerm_args = get_pidgin_RopeTerm_args()

    # THEN
    assert pidgin_RopeTerm_args == {
        f_state_str(),
        f_context_str(),
        plan_rope_str(),
        r_context_str(),
        p_state_str(),
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_pidgin_args_class_types().items()
        if class_type == RopeTerm_str()
    }
    assert pidgin_RopeTerm_args == expected_args


def test_PidginUnit_Exists():
    # ESTABLISH
    x_pidginunit = PidginUnit()

    # WHEN / THEN
    assert not x_pidginunit.event_int
    assert not x_pidginunit.titlemap
    assert not x_pidginunit.namemap
    assert not x_pidginunit.labelmap
    assert not x_pidginunit.ropemap
    assert not x_pidginunit.unknown_str
    assert not x_pidginunit.otx_knot
    assert not x_pidginunit.inx_knot
    assert not x_pidginunit.face_name


def test_pidginunit_shop_ReturnsObj_scenario0():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    sue_pidginunit = pidginunit_shop(sue_str)

    # THEN
    assert sue_pidginunit.face_name == sue_str
    assert sue_pidginunit.event_int == 0
    assert sue_pidginunit.unknown_str == default_unknown_str_if_None()
    assert sue_pidginunit.otx_knot == default_knot_if_None()
    assert sue_pidginunit.inx_knot == default_knot_if_None()
    assert sue_pidginunit.titlemap == titlemap_shop(face_name=sue_str)
    assert sue_pidginunit.namemap == namemap_shop(face_name=sue_str)
    assert sue_pidginunit.labelmap == labelmap_shop(face_name=sue_str)
    assert sue_pidginunit.ropemap == ropemap_shop(face_name=sue_str)
    assert sue_pidginunit.namemap.event_int == 0
    assert sue_pidginunit.namemap.unknown_str == default_unknown_str_if_None()
    assert sue_pidginunit.namemap.otx_knot == default_knot_if_None()
    assert sue_pidginunit.namemap.inx_knot == default_knot_if_None()
    assert sue_pidginunit.titlemap.event_int == 0
    assert sue_pidginunit.titlemap.unknown_str == default_unknown_str_if_None()
    assert sue_pidginunit.titlemap.otx_knot == default_knot_if_None()
    assert sue_pidginunit.titlemap.inx_knot == default_knot_if_None()
    assert sue_pidginunit.labelmap.event_int == 0
    assert sue_pidginunit.labelmap.unknown_str == default_unknown_str_if_None()
    assert sue_pidginunit.labelmap.otx_knot == default_knot_if_None()
    assert sue_pidginunit.labelmap.inx_knot == default_knot_if_None()
    assert sue_pidginunit.ropemap.event_int == 0
    assert sue_pidginunit.ropemap.unknown_str == default_unknown_str_if_None()
    assert sue_pidginunit.ropemap.otx_knot == default_knot_if_None()
    assert sue_pidginunit.ropemap.inx_knot == default_knot_if_None()


def test_pidginunit_shop_ReturnsObj_scenario1():
    # ESTABLISH
    sue_str = "Sue"
    five_event_int = 5
    y_uk = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"

    # WHEN
    sue_pidginunit = pidginunit_shop(
        sue_str, five_event_int, slash_otx_knot, colon_inx_knot, y_uk
    )

    # THEN
    assert sue_pidginunit.event_int == five_event_int
    assert sue_pidginunit.unknown_str == y_uk
    assert sue_pidginunit.otx_knot == slash_otx_knot
    assert sue_pidginunit.inx_knot == colon_inx_knot

    # x_titlemap = titlemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, sue_str, five_event_int
    # )
    # x_namemap = namemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, sue_str, five_event_int
    # )
    # x_ropemap = ropemap_shop(
    #     slash_otx_knot, colon_inx_knot, None, {}, y_uk, sue_str, five_event_int
    # )
    # assert sue_pidginunit.titlemap == x_titlemap
    # assert sue_pidginunit.namemap == x_namemap
    # assert sue_pidginunit.ropemap == x_ropemap

    assert sue_pidginunit.namemap.face_name == sue_str
    assert sue_pidginunit.namemap.event_int == five_event_int
    assert sue_pidginunit.namemap.unknown_str == y_uk
    assert sue_pidginunit.namemap.otx_knot == slash_otx_knot
    assert sue_pidginunit.namemap.inx_knot == colon_inx_knot
    assert sue_pidginunit.titlemap.face_name == sue_str
    assert sue_pidginunit.titlemap.event_int == five_event_int
    assert sue_pidginunit.titlemap.unknown_str == y_uk
    assert sue_pidginunit.titlemap.otx_knot == slash_otx_knot
    assert sue_pidginunit.titlemap.inx_knot == colon_inx_knot
    assert sue_pidginunit.labelmap.face_name == sue_str
    assert sue_pidginunit.labelmap.event_int == five_event_int
    assert sue_pidginunit.labelmap.unknown_str == y_uk
    assert sue_pidginunit.labelmap.otx_knot == slash_otx_knot
    assert sue_pidginunit.labelmap.inx_knot == colon_inx_knot
    assert sue_pidginunit.ropemap.face_name == sue_str
    assert sue_pidginunit.ropemap.event_int == five_event_int
    assert sue_pidginunit.ropemap.unknown_str == y_uk
    assert sue_pidginunit.ropemap.otx_knot == slash_otx_knot
    assert sue_pidginunit.ropemap.inx_knot == colon_inx_knot


def test_pidginunit_shop_ReturnsObj_scenario2_PidginCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_pidginunit = pidginunit_shop(
        face_name=bob_str,
        event_int=event7,
        unknown_str=x_nan,
        otx_knot=x_nan,
        inx_knot=x_nan,
    )

    # THEN
    assert x_pidginunit.face_name == bob_str
    assert x_pidginunit.event_int == event7
    assert x_pidginunit.unknown_str == default_unknown_str_if_None()
    assert x_pidginunit.otx_knot == default_knot_if_None()
    assert x_pidginunit.inx_knot == default_knot_if_None()


def test_PidginUnit_set_mapunit_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    namemap = namemap_shop(face_name=sue_str)
    namemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.namemap != namemap

    # WHEN
    sue_pidginunit.set_namemap(namemap)

    # THEN
    assert sue_pidginunit.namemap == namemap


def test_PidginUnit_set_mapunit_SetsAttr_SpecialCase_RopeTerm():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    ropemap = ropemap_shop(face_name=sue_str)
    ropemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.ropemap != ropemap

    # WHEN
    sue_pidginunit.set_ropemap(ropemap)

    # THEN
    assert sue_pidginunit.ropemap == ropemap


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_otx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_knot = "/"
    namemap = namemap_shop(otx_knot=slash_otx_knot, face_name=sue_str)
    assert sue_pidginunit.otx_knot != namemap.otx_knot
    assert sue_pidginunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: PidginUnit otx_knot is '{sue_pidginunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_inx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_knot = "/"
    namemap = namemap_shop(inx_knot=slash_inx_knot, face_name=sue_str)
    assert sue_pidginunit.inx_knot != namemap.inx_knot
    assert sue_pidginunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: PidginUnit inx_knot is '{sue_pidginunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    namemap = namemap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_pidginunit.unknown_str != namemap.unknown_str
    assert sue_pidginunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_str is '{sue_pidginunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    namemap = namemap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != namemap.face_name
    assert sue_pidginunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_mapunit_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pu = pidginunit_shop(sue_str)
    static_namemap = namemap_shop(face_name=sue_str)
    static_namemap.set_otx2inx("Bob", "Bob of Portland")
    sue_pu.set_namemap(static_namemap)

    # WHEN / THEN
    assert sue_pu.get_mapunit(NameTerm_str()) == sue_pu.namemap
    assert sue_pu.get_mapunit(TitleTerm_str()) == sue_pu.titlemap
    assert sue_pu.get_mapunit(LabelTerm_str()) == sue_pu.labelmap
    assert sue_pu.get_mapunit(RopeTerm_str()) == sue_pu.ropemap

    assert sue_pu.get_mapunit(NameTerm_str()) != sue_pu.ropemap
    assert sue_pu.get_mapunit(TitleTerm_str()) != sue_pu.ropemap
    assert sue_pu.get_mapunit(LabelTerm_str()) != sue_pu.ropemap


def test_PidginUnit_is_valid_ReturnsObj():
    # ESTABLISH
    invalid_namemap = get_invalid_namemap()
    invalid_titlemap = get_invalid_titlemap()
    invalid_labelmap = get_invalid_ropemap()
    valid_namemap = get_suita_namemap()
    valid_titlemap = get_swim_titlemap()
    valid_labelmap = get_clean_ropemap()
    assert valid_namemap.is_valid()
    assert valid_titlemap.is_valid()
    assert valid_labelmap.is_valid()
    assert invalid_labelmap.is_valid() is False
    assert invalid_titlemap.is_valid() is False
    assert invalid_namemap.is_valid() is False

    # WHEN / THEN
    sue_pidginunit = pidginunit_shop("Sue")
    assert sue_pidginunit.is_valid()
    sue_pidginunit.set_namemap(valid_namemap)
    sue_pidginunit.set_titlemap(valid_titlemap)
    sue_pidginunit.set_ropemap(valid_labelmap)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_namemap(invalid_namemap)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_namemap(valid_namemap)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_titlemap(invalid_titlemap)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_titlemap(valid_titlemap)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_ropemap(invalid_labelmap)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_ropemap(valid_labelmap)
    assert sue_pidginunit.is_valid()


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario0_NameTerm_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    namemap = zia_pidginunit.get_namemap()
    assert namemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(NameTerm_str(), sue_otx, sue_inx)

    # THEN
    assert namemap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario1_RopeTerm_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    ropemap = zia_pidginunit.get_ropemap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(RopeTerm_str(), sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario2_LabelTerm_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    ropemap = zia_pidginunit.get_labelmap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(LabelTerm_str(), sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    rope_type = LabelTerm_str()
    assert zia_pidginunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(LabelTerm_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.otx2inx_exists(rope_type, sue_otx, sue_inx)


def test_PidginUnit_get_inx_value_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_value(NameTerm_str(), sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_otx2inx(NameTerm_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_value(NameTerm_str(), sue_otx) == sue_inx


def test_PidginUnit_del_otx2inx_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    rope_type = LabelTerm_str()
    zia_pidginunit.set_otx2inx(LabelTerm_str(), sue_otx, sue_inx)
    zia_pidginunit.set_otx2inx(LabelTerm_str(), zia_str, zia_str)
    assert zia_pidginunit.otx2inx_exists(rope_type, sue_otx, sue_inx)
    assert zia_pidginunit.otx2inx_exists(rope_type, zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_otx2inx(rope_type, sue_otx)

    # THEN
    assert zia_pidginunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False
    assert zia_pidginunit.otx2inx_exists(rope_type, zia_str, zia_str)


def test_PidginUnit_set_label_SetsAttr_Scenario1_RopeTerm_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    ropemap = zia_pidginunit.get_ropemap()
    assert ropemap.label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_label(sue_otx, sue_inx)

    # THEN
    assert ropemap.label_exists(sue_otx, sue_inx)


def test_PidginUnit_label_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    sue_exists = zia_pidginunit.label_exists(sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_pidginunit.set_label(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.label_exists(sue_otx, sue_inx)
