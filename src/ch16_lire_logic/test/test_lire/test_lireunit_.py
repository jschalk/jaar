from pytest import raises as pytest_raises
from src.ch02_rope_logic.rope import default_knot_if_None
from src.ch09_belief_atom_logic.atom_config import (
    get_all_belief_dimen_delete_keys,
    get_atom_args_class_types,
)
from src.ch15_moment_logic.moment_config import get_moment_args_class_types
from src.ch16_lire_logic._ref.ch16_keywords import (
    LabelTerm_str,
    NameTerm_str,
    RopeTerm_str,
    TitleTerm_str,
    awardee_title_str,
    belief_name_str,
    face_name_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fund_iota_str,
    group_title_str,
    healer_name_str,
    hour_label_str,
    moment_label_str,
    month_label_str,
    party_title_str,
    penny_str,
    plan_label_str,
    plan_rope_str,
    reason_context_str,
    reason_state_str,
    respect_bit_str,
    timeline_label_str,
    voice_name_str,
    weekday_label_str,
)
from src.ch16_lire_logic.lire_config import (
    default_unknown_str_if_None,
    find_set_otx_inx_args,
    get_lire_args_class_types,
    get_lire_LabelTerm_args,
    get_lire_NameTerm_args,
    get_lire_RopeTerm_args,
    get_lire_TitleTerm_args,
    get_lireable_args,
    lireable_class_types,
)
from src.ch16_lire_logic.lire_main import LireUnit, lireunit_shop
from src.ch16_lire_logic.map import (
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)
from src.ch16_lire_logic.test._util.example_lires import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_invalid_namemap,
    get_invalid_ropemap,
    get_invalid_titlemap,
    get_suita_namemap,
    get_swim_titlemap,
)


def test_get_lire_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    lire_args_class_types = get_lire_args_class_types()

    # THEN
    assert lire_args_class_types.get("voice_name") == NameTerm_str()
    assert lire_args_class_types.get("addin") == "float"
    assert lire_args_class_types.get("amount") == "float"
    assert lire_args_class_types.get("awardee_title") == TitleTerm_str()
    assert lire_args_class_types.get("reason_context") == RopeTerm_str()
    assert lire_args_class_types.get("reason_active_requisite") == "bool"
    assert lire_args_class_types.get("begin") == "float"
    assert lire_args_class_types.get("c400_number") == "int"
    assert lire_args_class_types.get("close") == "float"
    assert lire_args_class_types.get("voice_cred_points") == "float"
    assert lire_args_class_types.get("group_cred_points") == "float"
    assert lire_args_class_types.get("credor_respect") == "float"
    assert lire_args_class_types.get("cumulative_day") == "int"
    assert lire_args_class_types.get("cumulative_minute") == "int"
    assert lire_args_class_types.get("voice_debt_points") == "float"
    assert lire_args_class_types.get("group_debt_points") == "float"
    assert lire_args_class_types.get("debtor_respect") == "float"
    assert lire_args_class_types.get("denom") == "int"
    assert lire_args_class_types.get("reason_divisor") == "int"
    assert lire_args_class_types.get("face_name") == NameTerm_str()
    assert lire_args_class_types.get("fact_context") == RopeTerm_str()
    assert lire_args_class_types.get("moment_label") == LabelTerm_str()
    assert lire_args_class_types.get("fact_upper") == "float"
    assert lire_args_class_types.get("fact_lower") == "float"
    assert lire_args_class_types.get("fund_iota") == "float"
    assert lire_args_class_types.get("fund_pool") == "float"
    assert lire_args_class_types.get("give_force") == "float"
    assert lire_args_class_types.get("gogo_want") == "float"
    assert lire_args_class_types.get("group_title") == TitleTerm_str()
    assert lire_args_class_types.get("healer_name") == NameTerm_str()
    assert lire_args_class_types.get("hour_label") == LabelTerm_str()
    assert lire_args_class_types.get("star") == "int"
    assert lire_args_class_types.get("max_tree_traverse") == "int"
    assert lire_args_class_types.get("month_label") == LabelTerm_str()
    assert lire_args_class_types.get("monthday_distortion") == "int"
    assert lire_args_class_types.get("morph") == "bool"
    assert lire_args_class_types.get("reason_state") == RopeTerm_str()
    assert lire_args_class_types.get("reason_upper") == "float"
    assert lire_args_class_types.get("numor") == "int"
    assert lire_args_class_types.get("offi_time") == "TimeLinePoint"
    assert lire_args_class_types.get("belief_name") == NameTerm_str()
    assert lire_args_class_types.get("reason_lower") == "float"
    assert lire_args_class_types.get("penny") == "float"
    assert lire_args_class_types.get("fact_state") == RopeTerm_str()
    assert lire_args_class_types.get("task") == "bool"
    assert lire_args_class_types.get("problem_bool") == "bool"
    assert lire_args_class_types.get("quota") == "int"
    assert lire_args_class_types.get("respect_bit") == "float"
    assert lire_args_class_types.get("plan_rope") == RopeTerm_str()
    assert lire_args_class_types.get("celldepth") == "int"
    assert lire_args_class_types.get("stop_want") == "float"
    assert lire_args_class_types.get("take_force") == "float"
    assert lire_args_class_types.get("tally") == "int"
    assert lire_args_class_types.get("party_title") == TitleTerm_str()
    assert lire_args_class_types.get("bud_time") == "TimeLinePoint"
    assert lire_args_class_types.get("tran_time") == "TimeLinePoint"
    assert lire_args_class_types.get("timeline_label") == LabelTerm_str()
    assert lire_args_class_types.get("weekday_label") == LabelTerm_str()
    assert lire_args_class_types.get("weekday_order") == "int"
    assert lire_args_class_types.get("knot") == "str"
    assert lire_args_class_types.get("yr1_jan1_offset") == "int"
    assert lire_args_class_types.get("solo") == "int"

    # make sure it lire_arg_class_types has all moment and all atom args
    lire_args = set(lire_args_class_types.keys())
    atom_args = set(get_atom_args_class_types().keys())
    moment_args = set(get_moment_args_class_types().keys())
    assert atom_args.issubset(lire_args)
    assert moment_args.issubset(lire_args)
    assert atom_args & (moment_args) == {
        voice_name_str(),
        fund_iota_str(),
        penny_str(),
        respect_bit_str(),
    }
    assert atom_args.union(moment_args) != lire_args
    assert atom_args.union(moment_args).union({"face_name"}) == lire_args
    assert check_class_types_are_correct()
    # assert lire_args_class_types.keys() == get_atom_args_dimen_mapping().keys()
    # assert all_atom_args_class_types_are_correct(x_class_types)


def check_class_types_are_correct() -> bool:
    lire_args_class_types = get_lire_args_class_types()
    atom_args_class_types = get_atom_args_class_types()
    moment_args_class_types = get_moment_args_class_types()
    for lire_arg, lire_type in lire_args_class_types.items():
        print(f"check {lire_arg=} {lire_type=}")
        if atom_args_class_types.get(lire_arg) not in [None, lire_type]:
            print(f"{lire_arg=} {lire_type=} {atom_args_class_types.get(lire_arg)=}")
            return False
        if moment_args_class_types.get(lire_arg) not in [None, lire_type]:
            print(f"{lire_arg=} {lire_type=} {moment_args_class_types.get(lire_arg)=}")
            return False
    return True


def test_lireable_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_lireable_class_types = lireable_class_types()

    # THEN
    assert len(x_lireable_class_types) == 4
    assert x_lireable_class_types == {
        NameTerm_str(),
        TitleTerm_str(),
        LabelTerm_str(),
        RopeTerm_str(),
    }
    print(f"{set(get_atom_args_class_types().values())=}")
    all_atom_class_types = set(get_atom_args_class_types().values())
    all_atom_class_types.add(LabelTerm_str())
    x_cL_tyep = set(all_atom_class_types) & (x_lireable_class_types)
    assert x_cL_tyep == x_lireable_class_types


def test_get_lireable_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{lireable_class_types()=}")
    all_lire_args = set(get_lire_args_class_types().keys())
    print(f"{get_lireable_args().difference(all_lire_args)}")
    assert get_lireable_args().issubset(all_lire_args)
    static_get_lireable_args = {
        x_arg
        for x_arg, class_type in get_lire_args_class_types().items()
        if class_type in lireable_class_types()
    }
    assert get_lireable_args() == static_get_lireable_args

    assert len(get_lireable_args()) == 17
    assert get_lireable_args() == {
        voice_name_str(),
        awardee_title_str(),
        reason_context_str(),
        face_name_str(),
        fact_context_str(),
        moment_label_str(),
        fact_state_str(),
        group_title_str(),
        healer_name_str(),
        hour_label_str(),
        month_label_str(),
        reason_state_str(),
        belief_name_str(),
        plan_rope_str(),
        party_title_str(),
        timeline_label_str(),
        weekday_label_str(),
    }


def test_find_set_otx_inx_args_ReturnsObj_Scenario0_All_lireable_args():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    lireable_args = get_lireable_args()

    # WHEN
    otx_inx_args = find_set_otx_inx_args(lireable_args)

    # THEN
    expected_otx_inx_args = set()
    for lireable_arg in lireable_args:
        expected_otx_inx_args.add(f"{lireable_arg}_otx")
        expected_otx_inx_args.add(f"{lireable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario1_belief_dimen_delete_keys():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    belief_dimen_delete_keys = get_all_belief_dimen_delete_keys()

    # WHEN
    otx_inx_args = find_set_otx_inx_args(belief_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for lireable_arg in belief_dimen_delete_keys:
        expected_otx_inx_args.add(f"{lireable_arg}_otx")
        expected_otx_inx_args.add(f"{lireable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario2_OtherArgsAreUntouched():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    run_str = "run"
    given_belief_dimen_delete_keys = get_all_belief_dimen_delete_keys()
    given_belief_dimen_delete_keys.add(run_str)

    # WHEN
    otx_inx_args = find_set_otx_inx_args(given_belief_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for lireable_arg in get_all_belief_dimen_delete_keys():
        expected_otx_inx_args.add(f"{lireable_arg}_otx")
        expected_otx_inx_args.add(f"{lireable_arg}_inx")
    expected_otx_inx_args.add(run_str)
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario3_PartialSets():
    # ESTABLISH
    healer_name_ERASE_str = f"{healer_name_str()}_ERASE"
    run_str = "run"
    given_belief_dimen_delete_keys = {run_str, healer_name_ERASE_str}

    # WHEN
    otx_inx_args = find_set_otx_inx_args(given_belief_dimen_delete_keys)

    # THEN
    healer_name_ERASE_str = f"{healer_name_str()}_ERASE"
    expected_otx_inx_args = {
        f"{healer_name_ERASE_str}_otx",
        f"{healer_name_ERASE_str}_inx",
        run_str,
    }
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_get_lire_NameTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    lire_NameTerm_args = get_lire_NameTerm_args()

    # THEN
    assert lire_NameTerm_args == {
        voice_name_str(),
        face_name_str(),
        healer_name_str(),
        belief_name_str(),
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_lire_args_class_types().items()
        if class_type == NameTerm_str()
    }
    assert lire_NameTerm_args == expected_args


def test_get_lire_TitleTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    lire_TitleTerm_args = get_lire_TitleTerm_args()

    # THEN
    assert lire_TitleTerm_args == {
        awardee_title_str(),
        group_title_str(),
        party_title_str(),
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_lire_args_class_types().items()
        if class_type == TitleTerm_str()
    }
    assert lire_TitleTerm_args == expected_args


def test_get_lire_LabelTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    lire_LabelTerm_args = get_lire_LabelTerm_args()

    # THEN
    assert lire_LabelTerm_args == {
        moment_label_str(),
        hour_label_str(),
        month_label_str(),
        timeline_label_str(),
        weekday_label_str(),
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_lire_args_class_types().items()
        if class_type == LabelTerm_str()
    }
    assert lire_LabelTerm_args == expected_args


def test_get_lire_RopeTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    lire_RopeTerm_args = get_lire_RopeTerm_args()

    # THEN
    assert lire_RopeTerm_args == {
        fact_state_str(),
        fact_context_str(),
        plan_rope_str(),
        reason_context_str(),
        reason_state_str(),
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_lire_args_class_types().items()
        if class_type == RopeTerm_str()
    }
    assert lire_RopeTerm_args == expected_args


def test_LireUnit_Exists():
    # ESTABLISH
    x_lireunit = LireUnit()

    # WHEN / THEN
    assert not x_lireunit.event_int
    assert not x_lireunit.titlemap
    assert not x_lireunit.namemap
    assert not x_lireunit.labelmap
    assert not x_lireunit.ropemap
    assert not x_lireunit.unknown_str
    assert not x_lireunit.otx_knot
    assert not x_lireunit.inx_knot
    assert not x_lireunit.face_name


def test_lireunit_shop_ReturnsObj_scenario0():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    sue_lireunit = lireunit_shop(sue_str)

    # THEN
    assert sue_lireunit.face_name == sue_str
    assert sue_lireunit.event_int == 0
    assert sue_lireunit.unknown_str == default_unknown_str_if_None()
    assert sue_lireunit.otx_knot == default_knot_if_None()
    assert sue_lireunit.inx_knot == default_knot_if_None()
    assert sue_lireunit.titlemap == titlemap_shop(face_name=sue_str)
    assert sue_lireunit.namemap == namemap_shop(face_name=sue_str)
    assert sue_lireunit.labelmap == labelmap_shop(face_name=sue_str)
    assert sue_lireunit.ropemap == ropemap_shop(face_name=sue_str)
    assert sue_lireunit.namemap.event_int == 0
    assert sue_lireunit.namemap.unknown_str == default_unknown_str_if_None()
    assert sue_lireunit.namemap.otx_knot == default_knot_if_None()
    assert sue_lireunit.namemap.inx_knot == default_knot_if_None()
    assert sue_lireunit.titlemap.event_int == 0
    assert sue_lireunit.titlemap.unknown_str == default_unknown_str_if_None()
    assert sue_lireunit.titlemap.otx_knot == default_knot_if_None()
    assert sue_lireunit.titlemap.inx_knot == default_knot_if_None()
    assert sue_lireunit.labelmap.event_int == 0
    assert sue_lireunit.labelmap.unknown_str == default_unknown_str_if_None()
    assert sue_lireunit.labelmap.otx_knot == default_knot_if_None()
    assert sue_lireunit.labelmap.inx_knot == default_knot_if_None()
    assert sue_lireunit.ropemap.event_int == 0
    assert sue_lireunit.ropemap.unknown_str == default_unknown_str_if_None()
    assert sue_lireunit.ropemap.otx_knot == default_knot_if_None()
    assert sue_lireunit.ropemap.inx_knot == default_knot_if_None()


def test_lireunit_shop_ReturnsObj_scenario1():
    # ESTABLISH
    sue_str = "Sue"
    five_event_int = 5
    y_uk = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"

    # WHEN
    sue_lireunit = lireunit_shop(
        sue_str, five_event_int, slash_otx_knot, colon_inx_knot, y_uk
    )

    # THEN
    assert sue_lireunit.event_int == five_event_int
    assert sue_lireunit.unknown_str == y_uk
    assert sue_lireunit.otx_knot == slash_otx_knot
    assert sue_lireunit.inx_knot == colon_inx_knot

    # x_titlemap = titlemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, sue_str, five_event_int
    # )
    # x_namemap = namemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, sue_str, five_event_int
    # )
    # x_ropemap = ropemap_shop(
    #     slash_otx_knot, colon_inx_knot, None, {}, y_uk, sue_str, five_event_int
    # )
    # assert sue_lireunit.titlemap == x_titlemap
    # assert sue_lireunit.namemap == x_namemap
    # assert sue_lireunit.ropemap == x_ropemap

    assert sue_lireunit.namemap.face_name == sue_str
    assert sue_lireunit.namemap.event_int == five_event_int
    assert sue_lireunit.namemap.unknown_str == y_uk
    assert sue_lireunit.namemap.otx_knot == slash_otx_knot
    assert sue_lireunit.namemap.inx_knot == colon_inx_knot
    assert sue_lireunit.titlemap.face_name == sue_str
    assert sue_lireunit.titlemap.event_int == five_event_int
    assert sue_lireunit.titlemap.unknown_str == y_uk
    assert sue_lireunit.titlemap.otx_knot == slash_otx_knot
    assert sue_lireunit.titlemap.inx_knot == colon_inx_knot
    assert sue_lireunit.labelmap.face_name == sue_str
    assert sue_lireunit.labelmap.event_int == five_event_int
    assert sue_lireunit.labelmap.unknown_str == y_uk
    assert sue_lireunit.labelmap.otx_knot == slash_otx_knot
    assert sue_lireunit.labelmap.inx_knot == colon_inx_knot
    assert sue_lireunit.ropemap.face_name == sue_str
    assert sue_lireunit.ropemap.event_int == five_event_int
    assert sue_lireunit.ropemap.unknown_str == y_uk
    assert sue_lireunit.ropemap.otx_knot == slash_otx_knot
    assert sue_lireunit.ropemap.inx_knot == colon_inx_knot


def test_lireunit_shop_ReturnsObj_scenario2_LireCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    event7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_lireunit = lireunit_shop(
        face_name=bob_str,
        event_int=event7,
        unknown_str=x_nan,
        otx_knot=x_nan,
        inx_knot=x_nan,
    )

    # THEN
    assert x_lireunit.face_name == bob_str
    assert x_lireunit.event_int == event7
    assert x_lireunit.unknown_str == default_unknown_str_if_None()
    assert x_lireunit.otx_knot == default_knot_if_None()
    assert x_lireunit.inx_knot == default_knot_if_None()


def test_LireUnit_set_mapunit_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    namemap = namemap_shop(face_name=sue_str)
    namemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_lireunit.namemap != namemap

    # WHEN
    sue_lireunit.set_namemap(namemap)

    # THEN
    assert sue_lireunit.namemap == namemap


def test_LireUnit_set_mapunit_SetsAttr_SpecialSituation_RopeTerm():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    ropemap = ropemap_shop(face_name=sue_str)
    ropemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_lireunit.ropemap != ropemap

    # WHEN
    sue_lireunit.set_ropemap(ropemap)

    # THEN
    assert sue_lireunit.ropemap == ropemap


def test_LireUnit_set_mapunit_RaisesErrorIf_mapunit_otx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    slash_otx_knot = "/"
    namemap = namemap_shop(otx_knot=slash_otx_knot, face_name=sue_str)
    assert sue_lireunit.otx_knot != namemap.otx_knot
    assert sue_lireunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lireunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: LireUnit otx_knot is '{sue_lireunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_LireUnit_set_mapunit_RaisesErrorIf_mapunit_inx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    slash_inx_knot = "/"
    namemap = namemap_shop(inx_knot=slash_inx_knot, face_name=sue_str)
    assert sue_lireunit.inx_knot != namemap.inx_knot
    assert sue_lireunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lireunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: LireUnit inx_knot is '{sue_lireunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_LireUnit_set_mapunit_RaisesErrorIf_mapunit_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    namemap = namemap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_lireunit.unknown_str != namemap.unknown_str
    assert sue_lireunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lireunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: LireUnit unknown_str is '{sue_lireunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_LireUnit_set_mapunit_RaisesErrorIf_mapunit_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_lireunit = lireunit_shop(sue_str)
    namemap = namemap_shop(face_name=yao_str)
    assert sue_lireunit.face_name != namemap.face_name
    assert sue_lireunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lireunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: LireUnit face_name is '{sue_lireunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_LireUnit_get_mapunit_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pu = lireunit_shop(sue_str)
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


def test_LireUnit_is_valid_ReturnsObj():
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
    sue_lireunit = lireunit_shop("Sue")
    assert sue_lireunit.is_valid()
    sue_lireunit.set_namemap(valid_namemap)
    sue_lireunit.set_titlemap(valid_titlemap)
    sue_lireunit.set_ropemap(valid_labelmap)
    assert sue_lireunit.is_valid()

    # WHEN / THEN
    sue_lireunit.set_namemap(invalid_namemap)
    assert sue_lireunit.is_valid() is False
    sue_lireunit.set_namemap(valid_namemap)
    assert sue_lireunit.is_valid()

    # WHEN / THEN
    sue_lireunit.set_titlemap(invalid_titlemap)
    assert sue_lireunit.is_valid() is False
    sue_lireunit.set_titlemap(valid_titlemap)
    assert sue_lireunit.is_valid()

    # WHEN / THEN
    sue_lireunit.set_ropemap(invalid_labelmap)
    assert sue_lireunit.is_valid() is False
    sue_lireunit.set_ropemap(valid_labelmap)
    assert sue_lireunit.is_valid()


def test_LireUnit_set_otx2inx_SetsAttr_Scenario0_NameTerm_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    namemap = zia_lireunit.get_namemap()
    assert namemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_lireunit.set_otx2inx(NameTerm_str(), sue_otx, sue_inx)

    # THEN
    assert namemap.otx2inx_exists(sue_otx, sue_inx)


def test_LireUnit_set_otx2inx_SetsAttr_Scenario1_RopeTerm_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    ropemap = zia_lireunit.get_ropemap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_lireunit.set_otx2inx(RopeTerm_str(), sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_LireUnit_set_otx2inx_SetsAttr_Scenario2_LabelTerm_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    ropemap = zia_lireunit.get_labelmap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_lireunit.set_otx2inx(LabelTerm_str(), sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_LireUnit_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    rope_type = LabelTerm_str()
    assert zia_lireunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False

    # WHEN
    zia_lireunit.set_otx2inx(LabelTerm_str(), sue_otx, sue_inx)

    # THEN
    assert zia_lireunit.otx2inx_exists(rope_type, sue_otx, sue_inx)


def test_LireUnit_get_inx_value_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    assert zia_lireunit._get_inx_value(NameTerm_str(), sue_otx) != sue_inx

    # WHEN
    zia_lireunit.set_otx2inx(NameTerm_str(), sue_otx, sue_inx)

    # THEN
    assert zia_lireunit._get_inx_value(NameTerm_str(), sue_otx) == sue_inx


def test_LireUnit_del_otx2inx_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    rope_type = LabelTerm_str()
    zia_lireunit.set_otx2inx(LabelTerm_str(), sue_otx, sue_inx)
    zia_lireunit.set_otx2inx(LabelTerm_str(), zia_str, zia_str)
    assert zia_lireunit.otx2inx_exists(rope_type, sue_otx, sue_inx)
    assert zia_lireunit.otx2inx_exists(rope_type, zia_str, zia_str)

    # WHEN
    zia_lireunit.del_otx2inx(rope_type, sue_otx)

    # THEN
    assert zia_lireunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False
    assert zia_lireunit.otx2inx_exists(rope_type, zia_str, zia_str)


def test_LireUnit_set_label_SetsAttr_Scenario1_RopeTerm_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    ropemap = zia_lireunit.get_ropemap()
    assert ropemap.label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_lireunit.set_label(sue_otx, sue_inx)

    # THEN
    assert ropemap.label_exists(sue_otx, sue_inx)


def test_LireUnit_label_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_lireunit = lireunit_shop(zia_str)
    sue_exists = zia_lireunit.label_exists(sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_lireunit.set_label(sue_otx, sue_inx)

    # THEN
    assert zia_lireunit.label_exists(sue_otx, sue_inx)
