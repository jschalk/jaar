from pytest import raises as pytest_raises
from src.ch04_rope.rope import default_knot_if_None
from src.ch08_belief_atom.atom_config import (
    get_all_belief_dimen_delete_keys,
    get_atom_args_class_types,
)
from src.ch15_moment.moment_config import get_moment_args_class_types
from src.ch16_translate.map import (
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)
from src.ch16_translate.test._util.ch16_examples import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_invalid_namemap,
    get_invalid_ropemap,
    get_invalid_titlemap,
    get_suita_namemap,
    get_swim_titlemap,
)
from src.ch16_translate.translate_config import (
    default_unknown_str_if_None,
    find_set_otx_inx_args,
    get_translate_args_class_types,
    get_translate_LabelTerm_args,
    get_translate_NameTerm_args,
    get_translate_RopeTerm_args,
    get_translate_TitleTerm_args,
    get_translateable_args,
    translateable_class_types,
)
from src.ch16_translate.translate_main import TranslateUnit, translateunit_shop
from src.ref.keywords import Ch16Keywords as kw


def test_get_translate_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    translate_args_class_types = get_translate_args_class_types()

    # THEN
    assert translate_args_class_types.get(kw.voice_name) == kw.NameTerm
    assert translate_args_class_types.get(kw.addin) == "float"
    assert translate_args_class_types.get(kw.amount) == "float"
    assert translate_args_class_types.get(kw.awardee_title) == kw.TitleTerm
    assert translate_args_class_types.get(kw.reason_context) == kw.RopeTerm
    assert translate_args_class_types.get(kw.active_requisite) == "bool"
    assert translate_args_class_types.get(kw.begin) == "float"
    assert translate_args_class_types.get(kw.c400_number) == "int"
    assert translate_args_class_types.get(kw.close) == "float"
    assert translate_args_class_types.get(kw.voice_cred_lumen) == "float"
    assert translate_args_class_types.get(kw.group_cred_lumen) == "float"
    assert translate_args_class_types.get(kw.credor_respect) == "float"
    assert translate_args_class_types.get(kw.cumulative_day) == "int"
    assert translate_args_class_types.get(kw.cumulative_minute) == "int"
    assert translate_args_class_types.get(kw.voice_debt_lumen) == "float"
    assert translate_args_class_types.get(kw.group_debt_lumen) == "float"
    assert translate_args_class_types.get(kw.debtor_respect) == "float"
    assert translate_args_class_types.get(kw.denom) == "int"
    assert translate_args_class_types.get(kw.reason_divisor) == "int"
    assert translate_args_class_types.get(kw.face_name) == kw.NameTerm
    assert translate_args_class_types.get(kw.fact_context) == kw.RopeTerm
    assert translate_args_class_types.get(kw.moment_label) == kw.LabelTerm
    assert translate_args_class_types.get(kw.fact_upper) == "float"
    assert translate_args_class_types.get(kw.fact_lower) == "float"
    assert translate_args_class_types.get(kw.fund_grain) == "float"
    assert translate_args_class_types.get(kw.fund_pool) == "float"
    assert translate_args_class_types.get(kw.give_force) == "float"
    assert translate_args_class_types.get(kw.gogo_want) == "float"
    assert translate_args_class_types.get(kw.group_title) == kw.TitleTerm
    assert translate_args_class_types.get(kw.healer_name) == kw.NameTerm
    assert translate_args_class_types.get(kw.hour_label) == kw.LabelTerm
    assert translate_args_class_types.get(kw.star) == "int"
    assert translate_args_class_types.get(kw.max_tree_traverse) == "int"
    assert translate_args_class_types.get(kw.month_label) == kw.LabelTerm
    assert translate_args_class_types.get(kw.monthday_index) == "int"
    assert translate_args_class_types.get(kw.morph) == "bool"
    assert translate_args_class_types.get(kw.reason_state) == kw.RopeTerm
    assert translate_args_class_types.get(kw.reason_upper) == "float"
    assert translate_args_class_types.get(kw.numor) == "int"
    assert translate_args_class_types.get(kw.offi_time) == kw.EpochTime
    assert translate_args_class_types.get(kw.belief_name) == kw.NameTerm
    assert translate_args_class_types.get(kw.reason_lower) == "float"
    assert translate_args_class_types.get(kw.mana_grain) == "float"
    assert translate_args_class_types.get(kw.fact_state) == kw.RopeTerm
    assert translate_args_class_types.get(kw.pledge) == "bool"
    assert translate_args_class_types.get(kw.problem_bool) == "bool"
    assert translate_args_class_types.get(kw.quota) == "int"
    assert translate_args_class_types.get(kw.respect_grain) == "float"
    assert translate_args_class_types.get(kw.plan_rope) == kw.RopeTerm
    assert translate_args_class_types.get(kw.celldepth) == "int"
    assert translate_args_class_types.get(kw.stop_want) == "float"
    assert translate_args_class_types.get(kw.take_force) == "float"
    assert translate_args_class_types.get(kw.tally) == "int"
    assert translate_args_class_types.get(kw.party_title) == kw.TitleTerm
    assert translate_args_class_types.get(kw.bud_time) == kw.EpochTime
    assert translate_args_class_types.get(kw.tran_time) == kw.EpochTime
    assert translate_args_class_types.get(kw.epoch_label) == kw.LabelTerm
    assert translate_args_class_types.get(kw.weekday_label) == kw.LabelTerm
    assert translate_args_class_types.get(kw.weekday_order) == "int"
    assert translate_args_class_types.get(kw.knot) == "str"
    assert translate_args_class_types.get(kw.yr1_jan1_offset) == "int"
    assert translate_args_class_types.get(kw.solo) == "int"

    # make sure it translate_arg_class_types has all moment and all atom args
    translate_args = set(translate_args_class_types.keys())
    atom_args = set(get_atom_args_class_types().keys())
    moment_args = set(get_moment_args_class_types().keys())
    assert atom_args.issubset(translate_args)
    assert moment_args.issubset(translate_args)
    assert atom_args & (moment_args) == {
        kw.voice_name,
        kw.fund_grain,
        kw.mana_grain,
        kw.respect_grain,
    }
    assert atom_args.union(moment_args) != translate_args
    assert atom_args.union(moment_args).union({kw.face_name}) == translate_args
    assert check_class_types_are_correct()
    # assert translate_args_class_types.keys() == get_atom_args_dimen_mapping().keys()
    # assert all_atom_args_class_types_are_correct(x_class_types)


def check_class_types_are_correct() -> bool:
    translate_args_class_types = get_translate_args_class_types()
    atom_args_class_types = get_atom_args_class_types()
    moment_args_class_types = get_moment_args_class_types()
    for translate_arg, translate_type in translate_args_class_types.items():
        print(f"check {translate_arg=} {translate_type=}")
        if atom_args_class_types.get(translate_arg) not in [None, translate_type]:
            print(
                f"{translate_arg=} {translate_type=} {atom_args_class_types.get(translate_arg)=}"
            )
            return False
        if moment_args_class_types.get(translate_arg) not in [None, translate_type]:
            print(
                f"{translate_arg=} {translate_type=} {moment_args_class_types.get(translate_arg)=}"
            )
            return False
    return True


def test_translateable_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_translateable_class_types = translateable_class_types()

    # THEN
    assert len(x_translateable_class_types) == 4
    assert x_translateable_class_types == {
        kw.NameTerm,
        kw.TitleTerm,
        kw.LabelTerm,
        kw.RopeTerm,
    }
    print(f"{set(get_atom_args_class_types().values())=}")
    all_atom_class_types = set(get_atom_args_class_types().values())
    all_atom_class_types.add(kw.LabelTerm)
    x_cL_tyep = set(all_atom_class_types) & (x_translateable_class_types)
    assert x_cL_tyep == x_translateable_class_types


def test_get_translateable_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{translateable_class_types()=}")
    all_translate_args = set(get_translate_args_class_types().keys())
    print(f"{get_translateable_args().difference(all_translate_args)}")
    assert get_translateable_args().issubset(all_translate_args)
    static_get_translateable_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type in translateable_class_types()
    }
    assert get_translateable_args() == static_get_translateable_args

    assert len(get_translateable_args()) == 17
    assert get_translateable_args() == {
        kw.voice_name,
        kw.awardee_title,
        kw.reason_context,
        kw.face_name,
        kw.fact_context,
        kw.moment_label,
        kw.fact_state,
        kw.group_title,
        kw.healer_name,
        kw.hour_label,
        kw.month_label,
        kw.reason_state,
        kw.belief_name,
        kw.plan_rope,
        kw.party_title,
        kw.epoch_label,
        kw.weekday_label,
    }


def test_find_set_otx_inx_args_ReturnsObj_Scenario0_All_translateable_args():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    translateable_args = get_translateable_args()

    # WHEN
    otx_inx_args = find_set_otx_inx_args(translateable_args)

    # THEN
    expected_otx_inx_args = set()
    for translateable_arg in translateable_args:
        expected_otx_inx_args.add(f"{translateable_arg}_otx")
        expected_otx_inx_args.add(f"{translateable_arg}_inx")
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
    for translateable_arg in belief_dimen_delete_keys:
        expected_otx_inx_args.add(f"{translateable_arg}_otx")
        expected_otx_inx_args.add(f"{translateable_arg}_inx")
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
    for translateable_arg in get_all_belief_dimen_delete_keys():
        expected_otx_inx_args.add(f"{translateable_arg}_otx")
        expected_otx_inx_args.add(f"{translateable_arg}_inx")
    expected_otx_inx_args.add(run_str)
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario3_PartialSets():
    # ESTABLISH
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    run_str = "run"
    given_belief_dimen_delete_keys = {run_str, healer_name_ERASE_str}

    # WHEN
    otx_inx_args = find_set_otx_inx_args(given_belief_dimen_delete_keys)

    # THEN
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    expected_otx_inx_args = {
        f"{healer_name_ERASE_str}_otx",
        f"{healer_name_ERASE_str}_inx",
        run_str,
    }
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_get_translate_NameTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    translate_NameTerm_args = get_translate_NameTerm_args()

    # THEN
    assert translate_NameTerm_args == {
        kw.voice_name,
        kw.face_name,
        kw.healer_name,
        kw.belief_name,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type == kw.NameTerm
    }
    assert translate_NameTerm_args == expected_args


def test_get_translate_TitleTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    translate_TitleTerm_args = get_translate_TitleTerm_args()

    # THEN
    assert translate_TitleTerm_args == {
        kw.awardee_title,
        kw.group_title,
        kw.party_title,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type == kw.TitleTerm
    }
    assert translate_TitleTerm_args == expected_args


def test_get_translate_LabelTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    translate_LabelTerm_args = get_translate_LabelTerm_args()

    # THEN
    assert translate_LabelTerm_args == {
        kw.moment_label,
        kw.hour_label,
        kw.month_label,
        kw.epoch_label,
        kw.weekday_label,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type == kw.LabelTerm
    }
    assert translate_LabelTerm_args == expected_args


def test_get_translate_RopeTerm_args_ReturnsObj():
    # ESTABLISH / WHEN
    translate_RopeTerm_args = get_translate_RopeTerm_args()

    # THEN
    assert translate_RopeTerm_args == {
        kw.fact_state,
        kw.fact_context,
        kw.plan_rope,
        kw.reason_context,
        kw.reason_state,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type == kw.RopeTerm
    }
    assert translate_RopeTerm_args == expected_args


def test_TranslateUnit_Exists():
    # ESTABLISH
    x_translateunit = TranslateUnit()

    # WHEN / THEN
    assert not x_translateunit.spark_num
    assert not x_translateunit.titlemap
    assert not x_translateunit.namemap
    assert not x_translateunit.labelmap
    assert not x_translateunit.ropemap
    assert not x_translateunit.unknown_str
    assert not x_translateunit.otx_knot
    assert not x_translateunit.inx_knot
    assert not x_translateunit.face_name


def test_translateunit_shop_ReturnsObj_scenario0():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    sue_translateunit = translateunit_shop(sue_str)

    # THEN
    assert sue_translateunit.face_name == sue_str
    assert sue_translateunit.spark_num == 0
    assert sue_translateunit.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.otx_knot == default_knot_if_None()
    assert sue_translateunit.inx_knot == default_knot_if_None()
    assert sue_translateunit.titlemap == titlemap_shop(face_name=sue_str)
    assert sue_translateunit.namemap == namemap_shop(face_name=sue_str)
    assert sue_translateunit.labelmap == labelmap_shop(face_name=sue_str)
    assert sue_translateunit.ropemap == ropemap_shop(face_name=sue_str)
    assert sue_translateunit.namemap.spark_num == 0
    assert sue_translateunit.namemap.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.namemap.otx_knot == default_knot_if_None()
    assert sue_translateunit.namemap.inx_knot == default_knot_if_None()
    assert sue_translateunit.titlemap.spark_num == 0
    assert sue_translateunit.titlemap.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.titlemap.otx_knot == default_knot_if_None()
    assert sue_translateunit.titlemap.inx_knot == default_knot_if_None()
    assert sue_translateunit.labelmap.spark_num == 0
    assert sue_translateunit.labelmap.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.labelmap.otx_knot == default_knot_if_None()
    assert sue_translateunit.labelmap.inx_knot == default_knot_if_None()
    assert sue_translateunit.ropemap.spark_num == 0
    assert sue_translateunit.ropemap.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.ropemap.otx_knot == default_knot_if_None()
    assert sue_translateunit.ropemap.inx_knot == default_knot_if_None()


def test_translateunit_shop_ReturnsObj_scenario1():
    # ESTABLISH
    sue_str = "Sue"
    five_spark_num = 5
    y_uk = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"

    # WHEN
    sue_translateunit = translateunit_shop(
        sue_str, five_spark_num, slash_otx_knot, colon_inx_knot, y_uk
    )

    # THEN
    assert sue_translateunit.spark_num == five_spark_num
    assert sue_translateunit.unknown_str == y_uk
    assert sue_translateunit.otx_knot == slash_otx_knot
    assert sue_translateunit.inx_knot == colon_inx_knot

    # x_titlemap = titlemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, sue_str, five_spark_num
    # )
    # x_namemap = namemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, sue_str, five_spark_num
    # )
    # x_ropemap = ropemap_shop(
    #     slash_otx_knot, colon_inx_knot, None, {}, y_uk, sue_str, five_spark_num
    # )
    # assert sue_translateunit.titlemap == x_titlemap
    # assert sue_translateunit.namemap == x_namemap
    # assert sue_translateunit.ropemap == x_ropemap

    assert sue_translateunit.namemap.face_name == sue_str
    assert sue_translateunit.namemap.spark_num == five_spark_num
    assert sue_translateunit.namemap.unknown_str == y_uk
    assert sue_translateunit.namemap.otx_knot == slash_otx_knot
    assert sue_translateunit.namemap.inx_knot == colon_inx_knot
    assert sue_translateunit.titlemap.face_name == sue_str
    assert sue_translateunit.titlemap.spark_num == five_spark_num
    assert sue_translateunit.titlemap.unknown_str == y_uk
    assert sue_translateunit.titlemap.otx_knot == slash_otx_knot
    assert sue_translateunit.titlemap.inx_knot == colon_inx_knot
    assert sue_translateunit.labelmap.face_name == sue_str
    assert sue_translateunit.labelmap.spark_num == five_spark_num
    assert sue_translateunit.labelmap.unknown_str == y_uk
    assert sue_translateunit.labelmap.otx_knot == slash_otx_knot
    assert sue_translateunit.labelmap.inx_knot == colon_inx_knot
    assert sue_translateunit.ropemap.face_name == sue_str
    assert sue_translateunit.ropemap.spark_num == five_spark_num
    assert sue_translateunit.ropemap.unknown_str == y_uk
    assert sue_translateunit.ropemap.otx_knot == slash_otx_knot
    assert sue_translateunit.ropemap.inx_knot == colon_inx_knot


def test_translateunit_shop_ReturnsObj_scenario2_TranslateCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    spark7 = 7
    otx2inx = {xio_str: sue_str}
    x_nan = float("nan")

    # WHEN
    x_translateunit = translateunit_shop(
        face_name=bob_str,
        spark_num=spark7,
        unknown_str=x_nan,
        otx_knot=x_nan,
        inx_knot=x_nan,
    )

    # THEN
    assert x_translateunit.face_name == bob_str
    assert x_translateunit.spark_num == spark7
    assert x_translateunit.unknown_str == default_unknown_str_if_None()
    assert x_translateunit.otx_knot == default_knot_if_None()
    assert x_translateunit.inx_knot == default_knot_if_None()


def test_TranslateUnit_set_mapunit_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    namemap = namemap_shop(face_name=sue_str)
    namemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.namemap != namemap

    # WHEN
    sue_translateunit.set_namemap(namemap)

    # THEN
    assert sue_translateunit.namemap == namemap


def test_TranslateUnit_set_mapunit_SetsAttr_SpecialSituation_RopeTerm():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    ropemap = ropemap_shop(face_name=sue_str)
    ropemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.ropemap != ropemap

    # WHEN
    sue_translateunit.set_ropemap(ropemap)

    # THEN
    assert sue_translateunit.ropemap == ropemap


def test_TranslateUnit_set_mapunit_RaisesErrorIf_mapunit_otx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    slash_otx_knot = "/"
    namemap = namemap_shop(otx_knot=slash_otx_knot, face_name=sue_str)
    assert sue_translateunit.otx_knot != namemap.otx_knot
    assert sue_translateunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: TranslateUnit otx_knot is '{sue_translateunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_mapunit_RaisesErrorIf_mapunit_inx_knot_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    slash_inx_knot = "/"
    namemap = namemap_shop(inx_knot=slash_inx_knot, face_name=sue_str)
    assert sue_translateunit.inx_knot != namemap.inx_knot
    assert sue_translateunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: TranslateUnit inx_knot is '{sue_translateunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_mapunit_RaisesErrorIf_mapunit_unknown_str_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    casa_unknown_str = "Unknown_casa"
    namemap = namemap_shop(unknown_str=casa_unknown_str, face_name=sue_str)
    assert sue_translateunit.unknown_str != namemap.unknown_str
    assert sue_translateunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: TranslateUnit unknown_str is '{sue_translateunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_mapunit_RaisesErrorIf_mapunit_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_translateunit = translateunit_shop(sue_str)
    namemap = namemap_shop(face_name=yao_str)
    assert sue_translateunit.face_name != namemap.face_name
    assert sue_translateunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: TranslateUnit face_name is '{sue_translateunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_get_mapunit_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pu = translateunit_shop(sue_str)
    static_namemap = namemap_shop(face_name=sue_str)
    static_namemap.set_otx2inx("Bob", "Bob of Portland")
    sue_pu.set_namemap(static_namemap)

    # WHEN / THEN
    assert sue_pu.get_mapunit(kw.NameTerm) == sue_pu.namemap
    assert sue_pu.get_mapunit(kw.TitleTerm) == sue_pu.titlemap
    assert sue_pu.get_mapunit(kw.LabelTerm) == sue_pu.labelmap
    assert sue_pu.get_mapunit(kw.RopeTerm) == sue_pu.ropemap

    assert sue_pu.get_mapunit(kw.NameTerm) != sue_pu.ropemap
    assert sue_pu.get_mapunit(kw.TitleTerm) != sue_pu.ropemap
    assert sue_pu.get_mapunit(kw.LabelTerm) != sue_pu.ropemap


def test_TranslateUnit_is_valid_ReturnsObj():
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
    sue_translateunit = translateunit_shop("Sue")
    assert sue_translateunit.is_valid()
    sue_translateunit.set_namemap(valid_namemap)
    sue_translateunit.set_titlemap(valid_titlemap)
    sue_translateunit.set_ropemap(valid_labelmap)
    assert sue_translateunit.is_valid()

    # WHEN / THEN
    sue_translateunit.set_namemap(invalid_namemap)
    assert sue_translateunit.is_valid() is False
    sue_translateunit.set_namemap(valid_namemap)
    assert sue_translateunit.is_valid()

    # WHEN / THEN
    sue_translateunit.set_titlemap(invalid_titlemap)
    assert sue_translateunit.is_valid() is False
    sue_translateunit.set_titlemap(valid_titlemap)
    assert sue_translateunit.is_valid()

    # WHEN / THEN
    sue_translateunit.set_ropemap(invalid_labelmap)
    assert sue_translateunit.is_valid() is False
    sue_translateunit.set_ropemap(valid_labelmap)
    assert sue_translateunit.is_valid()


def test_TranslateUnit_set_otx2inx_SetsAttr_Scenario0_NameTerm():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    namemap = zia_translateunit.get_namemap()
    assert namemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

    # THEN
    assert namemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_set_otx2inx_SetsAttr_Scenario1_RopeTerm():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    ropemap = zia_translateunit.get_ropemap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_otx2inx(kw.RopeTerm, sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_set_otx2inx_SetsAttr_Scenario2_LabelTerm():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    ropemap = zia_translateunit.get_labelmap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    rope_type = kw.LabelTerm
    assert zia_translateunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

    # THEN
    assert zia_translateunit.otx2inx_exists(rope_type, sue_otx, sue_inx)


def test_TranslateUnit_get_inx_value_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    assert zia_translateunit._get_inx_value(kw.NameTerm, sue_otx) != sue_inx

    # WHEN
    zia_translateunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

    # THEN
    assert zia_translateunit._get_inx_value(kw.NameTerm, sue_otx) == sue_inx


def test_TranslateUnit_del_otx2inx_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    rope_type = kw.LabelTerm
    zia_translateunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)
    zia_translateunit.set_otx2inx(kw.LabelTerm, zia_str, zia_str)
    assert zia_translateunit.otx2inx_exists(rope_type, sue_otx, sue_inx)
    assert zia_translateunit.otx2inx_exists(rope_type, zia_str, zia_str)

    # WHEN
    zia_translateunit.del_otx2inx(rope_type, sue_otx)

    # THEN
    assert zia_translateunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False
    assert zia_translateunit.otx2inx_exists(rope_type, zia_str, zia_str)


def test_TranslateUnit_set_label_SetsAttr_Scenario1_RopeTerm():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    ropemap = zia_translateunit.get_ropemap()
    assert ropemap.label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_label(sue_otx, sue_inx)

    # THEN
    assert ropemap.label_exists(sue_otx, sue_inx)


def test_TranslateUnit_label_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(zia_str)
    sue_exists = zia_translateunit.label_exists(sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_translateunit.set_label(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit.label_exists(sue_otx, sue_inx)
