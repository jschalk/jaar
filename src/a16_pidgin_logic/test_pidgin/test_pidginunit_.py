from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a01_way_logic.way import default_bridge_if_None
from src.a06_bud_logic._utils.str_a06 import (
    type_NameStr_str,
    type_LabelStr_str,
    type_TagStr_str,
    type_WayStr_str,
    acct_name_str,
    awardee_label_str,
    context_str,
    face_name_str,
    fcontext_str,
    fbranch_str,
    fopen_str,
    fund_coin_str,
    healer_name_str,
    group_label_str,
    idea_tag_str,
    rbranch_str,
    penny_str,
    respect_bit_str,
    idea_way_str,
    team_label_str,
)
from src.a07_calendar_logic._utils.str_a07 import timeline_tag_str
from src.a08_bud_atom_logic.atom_config import get_atom_args_class_types
from src.a15_fisc_logic._utils.str_a15 import (
    weekday_tag_str,
    month_tag_str,
    hour_tag_str,
)
from src.a15_fisc_logic.fisc_config import get_fisc_args_class_types
from src.a16_pidgin_logic.map import (
    labelmap_shop,
    namemap_shop,
    tagmap_shop,
    waymap_shop,
)
from src.a16_pidgin_logic.pidgin_config import (
    get_pidgin_args_class_types,
    default_unknown_word_if_None,
    pidginable_class_types,
    pidginable_atom_args,
)
from src.a16_pidgin_logic.pidgin import PidginUnit, pidginunit_shop
from src.a16_pidgin_logic._utils.example_pidgins import (
    get_invalid_namemap,
    get_invalid_labelmap,
    get_invalid_waymap,
    get_clean_waymap,
    get_clean_tagmap,
    get_swim_labelmap,
    get_suita_namemap,
)
from pytest import raises as pytest_raises


# The goal of the pidgin function is to allow a single command, pointing at a bunch of directories
# initialize fiscunits and output acct metrics such as calendars, financial status, healer status
def test_get_pidgin_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_args_class_types = get_pidgin_args_class_types()

    # THEN
    assert pidgin_args_class_types.get("acct_name") == type_NameStr_str()
    assert pidgin_args_class_types.get("addin") == "float"
    assert pidgin_args_class_types.get("amount") == "float"
    assert pidgin_args_class_types.get("awardee_label") == type_LabelStr_str()
    assert pidgin_args_class_types.get("context") == type_WayStr_str()
    assert pidgin_args_class_types.get("context_idea_active_requisite") == "bool"
    assert pidgin_args_class_types.get("begin") == "float"
    assert pidgin_args_class_types.get("c400_number") == "int"
    assert pidgin_args_class_types.get("close") == "float"
    assert pidgin_args_class_types.get("credit_belief") == "float"
    assert pidgin_args_class_types.get("credit_vote") == "float"
    assert pidgin_args_class_types.get("credor_respect") == "float"
    assert pidgin_args_class_types.get("cumlative_day") == "int"
    assert pidgin_args_class_types.get("cumlative_minute") == "int"
    assert pidgin_args_class_types.get("debtit_belief") == "float"
    assert pidgin_args_class_types.get("debtit_vote") == "float"
    assert pidgin_args_class_types.get("debtor_respect") == "float"
    assert pidgin_args_class_types.get("denom") == "int"
    assert pidgin_args_class_types.get("divisor") == "int"
    assert pidgin_args_class_types.get("face_name") == type_NameStr_str()
    assert pidgin_args_class_types.get("fcontext") == type_WayStr_str()
    assert pidgin_args_class_types.get("fisc_tag") == type_TagStr_str()
    assert pidgin_args_class_types.get("fnigh") == "float"
    assert pidgin_args_class_types.get("fopen") == "float"
    assert pidgin_args_class_types.get("fund_coin") == "float"
    assert pidgin_args_class_types.get("fund_pool") == "float"
    assert pidgin_args_class_types.get("give_force") == "float"
    assert pidgin_args_class_types.get("gogo_want") == "float"
    assert pidgin_args_class_types.get("group_label") == type_LabelStr_str()
    assert pidgin_args_class_types.get("healer_name") == type_NameStr_str()
    assert pidgin_args_class_types.get("hour_tag") == type_TagStr_str()
    assert pidgin_args_class_types.get("mass") == "int"
    assert pidgin_args_class_types.get("max_tree_traverse") == "int"
    assert pidgin_args_class_types.get("month_tag") == type_TagStr_str()
    assert pidgin_args_class_types.get("monthday_distortion") == "int"
    assert pidgin_args_class_types.get("morph") == "bool"
    assert pidgin_args_class_types.get("rbranch") == type_WayStr_str()
    assert pidgin_args_class_types.get("nigh") == "float"
    assert pidgin_args_class_types.get("numor") == "int"
    assert pidgin_args_class_types.get("offi_time") == "TimeLinePoint"
    assert pidgin_args_class_types.get("owner_name") == type_NameStr_str()
    assert pidgin_args_class_types.get("open") == "float"
    assert pidgin_args_class_types.get("penny") == "float"
    assert pidgin_args_class_types.get("fbranch") == type_WayStr_str()
    assert pidgin_args_class_types.get("pledge") == "bool"
    assert pidgin_args_class_types.get("problem_bool") == "bool"
    assert pidgin_args_class_types.get("quota") == "int"
    assert pidgin_args_class_types.get("respect_bit") == "float"
    assert pidgin_args_class_types.get("idea_way") == type_WayStr_str()
    assert pidgin_args_class_types.get("celldepth") == "int"
    assert pidgin_args_class_types.get("stop_want") == "float"
    assert pidgin_args_class_types.get("take_force") == "float"
    assert pidgin_args_class_types.get("tally") == "int"
    assert pidgin_args_class_types.get("team_label") == type_LabelStr_str()
    assert pidgin_args_class_types.get("deal_time") == "TimeLinePoint"
    assert pidgin_args_class_types.get("tran_time") == "TimeLinePoint"
    assert pidgin_args_class_types.get("timeline_tag") == type_TagStr_str()
    assert pidgin_args_class_types.get("weekday_tag") == type_TagStr_str()
    assert pidgin_args_class_types.get("weekday_order") == "int"
    assert pidgin_args_class_types.get("bridge") == "str"
    assert pidgin_args_class_types.get("yr1_jan1_offset") == "int"

    # make sure it pidgin_arg_class_types has all fisc and all atom args
    pidgin_args = set(pidgin_args_class_types.keys())
    atom_args = set(get_atom_args_class_types().keys())
    fisc_args = set(get_fisc_args_class_types().keys())
    assert atom_args.issubset(pidgin_args)
    assert fisc_args.issubset(pidgin_args)
    assert atom_args.intersection(fisc_args) == {
        acct_name_str(),
        fund_coin_str(),
        penny_str(),
        respect_bit_str(),
    }
    assert atom_args.union(fisc_args) != pidgin_args
    assert atom_args.union(fisc_args).union({"face_name"}) == pidgin_args
    assert check_class_types_are_correct()
    # assert pidgin_args_class_types.keys() == get_atom_args_dimen_mapping().keys()
    # assert all_atom_args_class_types_are_correct(x_class_types)


def check_class_types_are_correct() -> bool:
    pidgin_args_class_types = get_pidgin_args_class_types()
    atom_args_class_types = get_atom_args_class_types()
    fisc_args_class_types = get_fisc_args_class_types()
    for pidgin_arg, pidgin_type in pidgin_args_class_types.items():
        print(f"check {pidgin_arg=} {pidgin_type=}")
        if atom_args_class_types.get(pidgin_arg) not in [None, pidgin_type]:
            print(
                f"{pidgin_arg=} {pidgin_type=} {atom_args_class_types.get(pidgin_arg)=}"
            )
            return False
        if fisc_args_class_types.get(pidgin_arg) not in [None, pidgin_type]:
            print(
                f"{pidgin_arg=} {pidgin_type=} {fisc_args_class_types.get(pidgin_arg)=}"
            )
            return False
    return True


def test_pidginable_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginable_class_types = pidginable_class_types()

    # THEN
    assert len(x_pidginable_class_types) == 4
    assert x_pidginable_class_types == {
        type_NameStr_str(),
        type_LabelStr_str(),
        type_TagStr_str(),
        type_WayStr_str(),
    }
    print(f"{set(get_atom_args_class_types().values())=}")
    all_atom_class_types = set(get_atom_args_class_types().values())
    all_atom_class_types.add(type_TagStr_str())
    inter_x = set(all_atom_class_types).intersection(x_pidginable_class_types)
    assert inter_x == x_pidginable_class_types


def test_pidginable_atom_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{pidginable_class_types()=}")
    all_pidgin_args = set(get_pidgin_args_class_types().keys())
    print(f"{pidginable_atom_args().difference(all_pidgin_args)}")
    assert pidginable_atom_args().issubset(all_pidgin_args)
    static_pidginable_atom_args = {
        x_arg
        for x_arg, class_type in get_pidgin_args_class_types().items()
        if class_type in pidginable_class_types()
    }
    assert pidginable_atom_args() == static_pidginable_atom_args

    assert len(pidginable_atom_args()) == 17
    assert pidginable_atom_args() == {
        acct_name_str(),
        awardee_label_str(),
        context_str(),
        face_name_str(),
        fcontext_str(),
        fisc_tag_str(),
        fbranch_str(),
        group_label_str(),
        healer_name_str(),
        hour_tag_str(),
        month_tag_str(),
        rbranch_str(),
        owner_name_str(),
        idea_way_str(),
        team_label_str(),
        timeline_tag_str(),
        weekday_tag_str(),
    }


def test_PidginUnit_Exists():
    # ESTABLISH
    x_pidginunit = PidginUnit()

    # WHEN / THEN
    assert not x_pidginunit.event_int
    assert not x_pidginunit.labelmap
    assert not x_pidginunit.namemap
    assert not x_pidginunit.tagmap
    assert not x_pidginunit.waymap
    assert not x_pidginunit.unknown_word
    assert not x_pidginunit.otx_bridge
    assert not x_pidginunit.inx_bridge
    assert not x_pidginunit.face_name


def test_pidginunit_shop_ReturnsObj_scenario0():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    sue_pidginunit = pidginunit_shop(sue_str)

    # THEN
    assert sue_pidginunit.face_name == sue_str
    assert sue_pidginunit.event_int == 0
    assert sue_pidginunit.unknown_word == default_unknown_word_if_None()
    assert sue_pidginunit.otx_bridge == default_bridge_if_None()
    assert sue_pidginunit.inx_bridge == default_bridge_if_None()
    assert sue_pidginunit.labelmap == labelmap_shop(face_name=sue_str)
    assert sue_pidginunit.namemap == namemap_shop(face_name=sue_str)
    assert sue_pidginunit.tagmap == tagmap_shop(face_name=sue_str)
    assert sue_pidginunit.waymap == waymap_shop(face_name=sue_str)
    assert sue_pidginunit.namemap.event_int == 0
    assert sue_pidginunit.namemap.unknown_word == default_unknown_word_if_None()
    assert sue_pidginunit.namemap.otx_bridge == default_bridge_if_None()
    assert sue_pidginunit.namemap.inx_bridge == default_bridge_if_None()
    assert sue_pidginunit.labelmap.event_int == 0
    assert sue_pidginunit.labelmap.unknown_word == default_unknown_word_if_None()
    assert sue_pidginunit.labelmap.otx_bridge == default_bridge_if_None()
    assert sue_pidginunit.labelmap.inx_bridge == default_bridge_if_None()
    assert sue_pidginunit.tagmap.event_int == 0
    assert sue_pidginunit.tagmap.unknown_word == default_unknown_word_if_None()
    assert sue_pidginunit.tagmap.otx_bridge == default_bridge_if_None()
    assert sue_pidginunit.tagmap.inx_bridge == default_bridge_if_None()
    assert sue_pidginunit.waymap.event_int == 0
    assert sue_pidginunit.waymap.unknown_word == default_unknown_word_if_None()
    assert sue_pidginunit.waymap.otx_bridge == default_bridge_if_None()
    assert sue_pidginunit.waymap.inx_bridge == default_bridge_if_None()


def test_pidginunit_shop_ReturnsObj_scenario1():
    # ESTABLISH
    sue_str = "Sue"
    five_event_int = 5
    y_uk = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"

    # WHEN
    sue_pidginunit = pidginunit_shop(
        sue_str, five_event_int, slash_otx_bridge, colon_inx_bridge, y_uk
    )

    # THEN
    assert sue_pidginunit.event_int == five_event_int
    assert sue_pidginunit.unknown_word == y_uk
    assert sue_pidginunit.otx_bridge == slash_otx_bridge
    assert sue_pidginunit.inx_bridge == colon_inx_bridge

    # x_labelmap = labelmap_shop(
    #     slash_otx_bridge, colon_inx_bridge, {}, y_uk, sue_str, five_event_int
    # )
    # x_namemap = namemap_shop(
    #     slash_otx_bridge, colon_inx_bridge, {}, y_uk, sue_str, five_event_int
    # )
    # x_waymap = waymap_shop(
    #     slash_otx_bridge, colon_inx_bridge, None, {}, y_uk, sue_str, five_event_int
    # )
    # assert sue_pidginunit.labelmap == x_labelmap
    # assert sue_pidginunit.namemap == x_namemap
    # assert sue_pidginunit.waymap == x_waymap

    assert sue_pidginunit.namemap.face_name == sue_str
    assert sue_pidginunit.namemap.event_int == five_event_int
    assert sue_pidginunit.namemap.unknown_word == y_uk
    assert sue_pidginunit.namemap.otx_bridge == slash_otx_bridge
    assert sue_pidginunit.namemap.inx_bridge == colon_inx_bridge
    assert sue_pidginunit.labelmap.face_name == sue_str
    assert sue_pidginunit.labelmap.event_int == five_event_int
    assert sue_pidginunit.labelmap.unknown_word == y_uk
    assert sue_pidginunit.labelmap.otx_bridge == slash_otx_bridge
    assert sue_pidginunit.labelmap.inx_bridge == colon_inx_bridge
    assert sue_pidginunit.tagmap.face_name == sue_str
    assert sue_pidginunit.tagmap.event_int == five_event_int
    assert sue_pidginunit.tagmap.unknown_word == y_uk
    assert sue_pidginunit.tagmap.otx_bridge == slash_otx_bridge
    assert sue_pidginunit.tagmap.inx_bridge == colon_inx_bridge
    assert sue_pidginunit.waymap.face_name == sue_str
    assert sue_pidginunit.waymap.event_int == five_event_int
    assert sue_pidginunit.waymap.unknown_word == y_uk
    assert sue_pidginunit.waymap.otx_bridge == slash_otx_bridge
    assert sue_pidginunit.waymap.inx_bridge == colon_inx_bridge


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
        unknown_word=x_nan,
        otx_bridge=x_nan,
        inx_bridge=x_nan,
    )

    # THEN
    assert x_pidginunit.face_name == bob_str
    assert x_pidginunit.event_int == event7
    assert x_pidginunit.unknown_word == default_unknown_word_if_None()
    assert x_pidginunit.otx_bridge == default_bridge_if_None()
    assert x_pidginunit.inx_bridge == default_bridge_if_None()


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


def test_PidginUnit_set_mapunit_SetsAttr_SpecialCase_WayStr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    waymap = waymap_shop(face_name=sue_str)
    waymap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.waymap != waymap

    # WHEN
    sue_pidginunit.set_waymap(waymap)

    # THEN
    assert sue_pidginunit.waymap == waymap


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    namemap = namemap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != namemap.otx_bridge
    assert sue_pidginunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    namemap = namemap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != namemap.inx_bridge
    assert sue_pidginunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    namemap = namemap_shop(unknown_word=casa_unknown_word, face_name=sue_str)
    assert sue_pidginunit.unknown_word != namemap.unknown_word
    assert sue_pidginunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', MapCore is '{casa_unknown_word}'."
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
    assert sue_pu.get_mapunit(type_NameStr_str()) == sue_pu.namemap
    assert sue_pu.get_mapunit(type_LabelStr_str()) == sue_pu.labelmap
    assert sue_pu.get_mapunit(type_TagStr_str()) == sue_pu.tagmap
    assert sue_pu.get_mapunit(type_WayStr_str()) == sue_pu.waymap

    assert sue_pu.get_mapunit(type_NameStr_str()) != sue_pu.waymap
    assert sue_pu.get_mapunit(type_LabelStr_str()) != sue_pu.waymap
    assert sue_pu.get_mapunit(type_TagStr_str()) != sue_pu.waymap


def test_PidginUnit_is_valid_ReturnsObj():
    # ESTABLISH
    invalid_namemap = get_invalid_namemap()
    invalid_labelmap = get_invalid_labelmap()
    invalid_tagmap = get_invalid_waymap()
    valid_namemap = get_suita_namemap()
    valid_labelmap = get_swim_labelmap()
    valid_tagmap = get_clean_waymap()
    assert valid_namemap.is_valid()
    assert valid_labelmap.is_valid()
    assert valid_tagmap.is_valid()
    assert invalid_tagmap.is_valid() is False
    assert invalid_labelmap.is_valid() is False
    assert invalid_namemap.is_valid() is False

    # WHEN / THEN
    sue_pidginunit = pidginunit_shop("Sue")
    assert sue_pidginunit.is_valid()
    sue_pidginunit.set_namemap(valid_namemap)
    sue_pidginunit.set_labelmap(valid_labelmap)
    sue_pidginunit.set_waymap(valid_tagmap)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_namemap(invalid_namemap)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_namemap(valid_namemap)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_labelmap(invalid_labelmap)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_labelmap(valid_labelmap)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_waymap(invalid_tagmap)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_waymap(valid_tagmap)
    assert sue_pidginunit.is_valid()


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario0_type_NameStr_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    namemap = zia_pidginunit.get_namemap()
    assert namemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_NameStr_str(), sue_otx, sue_inx)

    # THEN
    assert namemap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario1_type_WayStr_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    waymap = zia_pidginunit.get_waymap()
    assert waymap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_WayStr_str(), sue_otx, sue_inx)

    # THEN
    assert waymap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario2_type_TagStr_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    waymap = zia_pidginunit.get_tagmap()
    assert waymap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_TagStr_str(), sue_otx, sue_inx)

    # THEN
    assert waymap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    way_type = type_TagStr_str()
    assert zia_pidginunit.otx2inx_exists(way_type, sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_TagStr_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.otx2inx_exists(way_type, sue_otx, sue_inx)


def test_PidginUnit_get_inx_value_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_value(type_NameStr_str(), sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_otx2inx(type_NameStr_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_value(type_NameStr_str(), sue_otx) == sue_inx


def test_PidginUnit_del_otx2inx_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    way_type = type_TagStr_str()
    zia_pidginunit.set_otx2inx(type_TagStr_str(), sue_otx, sue_inx)
    zia_pidginunit.set_otx2inx(type_TagStr_str(), zia_str, zia_str)
    assert zia_pidginunit.otx2inx_exists(way_type, sue_otx, sue_inx)
    assert zia_pidginunit.otx2inx_exists(way_type, zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_otx2inx(way_type, sue_otx)

    # THEN
    assert zia_pidginunit.otx2inx_exists(way_type, sue_otx, sue_inx) is False
    assert zia_pidginunit.otx2inx_exists(way_type, zia_str, zia_str)


def test_PidginUnit_set_tag_SetsAttr_Scenario1_type_WayStr_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    waymap = zia_pidginunit.get_waymap()
    assert waymap.tag_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_tag(sue_otx, sue_inx)

    # THEN
    assert waymap.tag_exists(sue_otx, sue_inx)


def test_PidginUnit_tag_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    sue_exists = zia_pidginunit.tag_exists(sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_pidginunit.set_tag(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.tag_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_tag_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_tag(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_tag(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_tag(sue_otx) == sue_inx


def test_PidginUnit_del_tag_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    zia_pidginunit.set_tag(sue_otx, sue_inx)
    zia_pidginunit.set_tag(zia_str, zia_str)
    assert zia_pidginunit.tag_exists(sue_otx, sue_inx)
    assert zia_pidginunit.tag_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_tag(sue_otx)

    # THEN
    sue_exists = zia_pidginunit.tag_exists(sue_otx, sue_inx)
    assert sue_exists is False
    assert zia_pidginunit.tag_exists(zia_str, zia_str)
