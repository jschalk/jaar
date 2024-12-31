from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_bridge_if_None
from src.f03_chrono.chrono import timeline_idea_str
from src.f04_gift.atom_config import (
    get_atom_args_jaar_types,
    type_AcctName_str,
    type_GroupLabel_str,
    type_IdeaUnit_str,
    type_RoadUnit_str,
    acct_name_str,
    awardee_label_str,
    base_str,
    face_name_str,
    deal_idea_str,
    fund_coin_str,
    healer_name_str,
    group_label_str,
    idee_str,
    parent_road_str,
    penny_str,
    owner_name_str,
    respect_bit_str,
    road_str,
    team_label_str,
)
from src.f07_deal.deal_config import (
    get_deal_args_jaar_types,
    weekday_idea_str,
    month_idea_str,
    hour_idea_str,
)
from src.f08_pidgin.map import (
    groupmap_shop,
    acctmap_shop,
    ideamap_shop,
    roadmap_shop,
)
from src.f08_pidgin.pidgin_config import get_pidgin_args_jaar_types
from src.f08_pidgin.pidgin import (
    PidginUnit,
    pidginunit_shop,
    pidginable_jaar_types,
    pidginable_atom_args,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_invalid_acctmap,
    get_invalid_groupmap,
    get_invalid_ideamap,
    get_clean_roadmap,
    get_clean_ideamap,
    get_swim_groupmap,
    get_suita_acctmap,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


# The goal of the pidgin function is to allow a single command, pointing at a bunch of directories
# initialize dealunits and output acct metrics such as calendars, financial status, healer status
def test_get_pidgin_args_jaar_types_ReturnsObj():
    # ESTABLISH / WHEN
    pidgin_args_jaar_types = get_pidgin_args_jaar_types()

    # THEN
    assert pidgin_args_jaar_types.get("acct_name") == type_AcctName_str()
    assert pidgin_args_jaar_types.get("addin") == "float"
    assert pidgin_args_jaar_types.get("amount") == "float"
    assert pidgin_args_jaar_types.get("awardee_label") == type_GroupLabel_str()
    assert pidgin_args_jaar_types.get("base") == type_RoadUnit_str()
    assert pidgin_args_jaar_types.get("base_item_active_requisite") == "bool"
    assert pidgin_args_jaar_types.get("begin") == "float"
    assert pidgin_args_jaar_types.get("c400_number") == "int"
    assert pidgin_args_jaar_types.get("close") == "float"
    assert pidgin_args_jaar_types.get("credit_belief") == "int"
    assert pidgin_args_jaar_types.get("credit_vote") == "int"
    assert pidgin_args_jaar_types.get("credor_respect") == "int"
    assert pidgin_args_jaar_types.get("cumlative_day") == "int"
    assert pidgin_args_jaar_types.get("cumlative_minute") == "int"
    assert pidgin_args_jaar_types.get("current_time") == "int"
    assert pidgin_args_jaar_types.get("debtit_belief") == "int"
    assert pidgin_args_jaar_types.get("debtit_vote") == "int"
    assert pidgin_args_jaar_types.get("debtor_respect") == "int"
    assert pidgin_args_jaar_types.get("denom") == "int"
    assert pidgin_args_jaar_types.get("divisor") == "int"
    assert pidgin_args_jaar_types.get("face_name") == type_AcctName_str()
    assert pidgin_args_jaar_types.get("deal_idea") == type_IdeaUnit_str()
    assert pidgin_args_jaar_types.get("fnigh") == "float"
    assert pidgin_args_jaar_types.get("fopen") == "float"
    assert pidgin_args_jaar_types.get("fund_coin") == "float"
    assert pidgin_args_jaar_types.get("fund_pool") == "float"
    assert pidgin_args_jaar_types.get("give_force") == "float"
    assert pidgin_args_jaar_types.get("gogo_want") == "float"
    assert pidgin_args_jaar_types.get("group_label") == type_GroupLabel_str()
    assert pidgin_args_jaar_types.get("healer_name") == type_AcctName_str()
    assert pidgin_args_jaar_types.get("hour_idea") == type_IdeaUnit_str()
    assert pidgin_args_jaar_types.get("idee") == type_IdeaUnit_str()
    assert pidgin_args_jaar_types.get("mass") == "int"
    assert pidgin_args_jaar_types.get("max_tree_traverse") == "int"
    assert pidgin_args_jaar_types.get("month_idea") == type_IdeaUnit_str()
    assert pidgin_args_jaar_types.get("monthday_distortion") == "int"
    assert pidgin_args_jaar_types.get("morph") == "bool"
    assert pidgin_args_jaar_types.get("need") == type_RoadUnit_str()
    assert pidgin_args_jaar_types.get("nigh") == "float"
    assert pidgin_args_jaar_types.get("numor") == "int"
    assert pidgin_args_jaar_types.get("owner_name") == type_AcctName_str()
    assert pidgin_args_jaar_types.get("open") == "float"
    assert pidgin_args_jaar_types.get("parent_road") == type_RoadUnit_str()
    assert pidgin_args_jaar_types.get("penny") == "float"
    assert pidgin_args_jaar_types.get("pick") == type_RoadUnit_str()
    assert pidgin_args_jaar_types.get("pledge") == "bool"
    assert pidgin_args_jaar_types.get("problem_bool") == "bool"
    assert pidgin_args_jaar_types.get("pact_time_int") == "TimeLinePoint"
    assert pidgin_args_jaar_types.get("quota") == "int"
    assert pidgin_args_jaar_types.get("respect_bit") == "float"
    assert pidgin_args_jaar_types.get("road") == type_RoadUnit_str()
    assert pidgin_args_jaar_types.get("stop_want") == "float"
    assert pidgin_args_jaar_types.get("take_force") == "float"
    assert pidgin_args_jaar_types.get("tally") == "int"
    assert pidgin_args_jaar_types.get("team_label") == type_GroupLabel_str()
    assert pidgin_args_jaar_types.get("time_int") == "TimeLinePoint"
    assert pidgin_args_jaar_types.get("timeline_idea") == type_IdeaUnit_str()
    assert pidgin_args_jaar_types.get("weekday_idea") == type_IdeaUnit_str()
    assert pidgin_args_jaar_types.get("weekday_order") == "int"
    assert pidgin_args_jaar_types.get("bridge") == "str"
    assert pidgin_args_jaar_types.get("yr1_jan1_offset") == "int"

    # make sure it pidgin_arg_jaar_types has all deal and all atom args
    pidgin_args = set(pidgin_args_jaar_types.keys())
    atom_args = set(get_atom_args_jaar_types().keys())
    deal_args = set(get_deal_args_jaar_types().keys())
    assert atom_args.issubset(pidgin_args)
    assert deal_args.issubset(pidgin_args)
    assert atom_args.intersection(deal_args) == {
        acct_name_str(),
        fund_coin_str(),
        penny_str(),
        respect_bit_str(),
    }
    assert atom_args.union(deal_args) != pidgin_args
    assert atom_args.union(deal_args).union({"face_name"}) == pidgin_args
    assert check_jaar_types_are_correct()
    # assert pidgin_args_jaar_types.keys() == get_atom_args_category_mapping().keys()
    # assert all_atom_args_jaar_types_are_correct(x_jaar_types)


def check_jaar_types_are_correct() -> bool:
    pidgin_args_jaar_types = get_pidgin_args_jaar_types()
    atom_args_jaar_types = get_atom_args_jaar_types()
    deal_args_jaar_types = get_deal_args_jaar_types()
    for pidgin_arg, pidgin_type in pidgin_args_jaar_types.items():
        print(f"check {pidgin_arg=} {pidgin_type=}")
        if atom_args_jaar_types.get(pidgin_arg) not in [None, pidgin_type]:
            print(
                f"{pidgin_arg=} {pidgin_type=} {atom_args_jaar_types.get(pidgin_arg)=}"
            )
            return False
        if deal_args_jaar_types.get(pidgin_arg) not in [None, pidgin_type]:
            print(
                f"{pidgin_arg=} {pidgin_type=} {deal_args_jaar_types.get(pidgin_arg)=}"
            )
            return False
    return True


def test_pidginable_jaar_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginable_jaar_types = pidginable_jaar_types()

    # THEN
    assert len(x_pidginable_jaar_types) == 4
    assert x_pidginable_jaar_types == {
        type_AcctName_str(),
        type_GroupLabel_str(),
        type_IdeaUnit_str(),
        type_RoadUnit_str(),
    }
    print(f"{set(get_atom_args_jaar_types().values())=}")
    all_atom_jaar_types = set(get_atom_args_jaar_types().values())
    inter_x = set(all_atom_jaar_types).intersection(x_pidginable_jaar_types)
    assert inter_x == x_pidginable_jaar_types


def test_pidginable_atom_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert len(pidginable_atom_args()) == 18
    assert pidginable_atom_args() == {
        acct_name_str(),
        awardee_label_str(),
        base_str(),
        face_name_str(),
        deal_idea_str(),
        group_label_str(),
        healer_name_str(),
        hour_idea_str(),
        idee_str(),
        month_idea_str(),
        parent_road_str(),
        "pick",
        "need",
        owner_name_str(),
        road_str(),
        team_label_str(),
        timeline_idea_str(),
        weekday_idea_str(),
    }

    print(f"{pidginable_jaar_types()=}")
    all_pidgin_args = set(get_pidgin_args_jaar_types().keys())
    print(f"{pidginable_atom_args().difference(all_pidgin_args)}")
    assert pidginable_atom_args().issubset(all_pidgin_args)
    static_pidginable_atom_args = {
        x_arg
        for x_arg, jaar_type in get_pidgin_args_jaar_types().items()
        if jaar_type in pidginable_jaar_types()
    }
    assert pidginable_atom_args() == static_pidginable_atom_args


def test_PidginUnit_Exists():
    # ESTABLISH
    x_pidginunit = PidginUnit()

    # WHEN / THEN
    assert not x_pidginunit.event_int
    assert not x_pidginunit.groupmap
    assert not x_pidginunit.acctmap
    assert not x_pidginunit.ideamap
    assert not x_pidginunit.roadmap
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
    assert sue_pidginunit.groupmap == groupmap_shop(face_name=sue_str)
    assert sue_pidginunit.acctmap == acctmap_shop(face_name=sue_str)
    assert sue_pidginunit.ideamap == ideamap_shop(face_name=sue_str)
    assert sue_pidginunit.roadmap == roadmap_shop(face_name=sue_str)
    assert sue_pidginunit.acctmap.event_int == 0
    assert sue_pidginunit.acctmap.unknown_word == default_unknown_word_if_None()
    assert sue_pidginunit.acctmap.otx_bridge == default_bridge_if_None()
    assert sue_pidginunit.acctmap.inx_bridge == default_bridge_if_None()
    assert sue_pidginunit.groupmap.event_int == 0
    assert sue_pidginunit.groupmap.unknown_word == default_unknown_word_if_None()
    assert sue_pidginunit.groupmap.otx_bridge == default_bridge_if_None()
    assert sue_pidginunit.groupmap.inx_bridge == default_bridge_if_None()
    assert sue_pidginunit.ideamap.event_int == 0
    assert sue_pidginunit.ideamap.unknown_word == default_unknown_word_if_None()
    assert sue_pidginunit.ideamap.otx_bridge == default_bridge_if_None()
    assert sue_pidginunit.ideamap.inx_bridge == default_bridge_if_None()
    assert sue_pidginunit.roadmap.event_int == 0
    assert sue_pidginunit.roadmap.unknown_word == default_unknown_word_if_None()
    assert sue_pidginunit.roadmap.otx_bridge == default_bridge_if_None()
    assert sue_pidginunit.roadmap.inx_bridge == default_bridge_if_None()


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

    # x_groupmap = groupmap_shop(
    #     slash_otx_bridge, colon_inx_bridge, {}, y_uk, sue_str, five_event_int
    # )
    # x_acctmap = acctmap_shop(
    #     slash_otx_bridge, colon_inx_bridge, {}, y_uk, sue_str, five_event_int
    # )
    # x_roadmap = roadmap_shop(
    #     slash_otx_bridge, colon_inx_bridge, None, {}, y_uk, sue_str, five_event_int
    # )
    # assert sue_pidginunit.groupmap == x_groupmap
    # assert sue_pidginunit.acctmap == x_acctmap
    # assert sue_pidginunit.roadmap == x_roadmap

    assert sue_pidginunit.acctmap.face_name == sue_str
    assert sue_pidginunit.acctmap.event_int == five_event_int
    assert sue_pidginunit.acctmap.unknown_word == y_uk
    assert sue_pidginunit.acctmap.otx_bridge == slash_otx_bridge
    assert sue_pidginunit.acctmap.inx_bridge == colon_inx_bridge
    assert sue_pidginunit.groupmap.face_name == sue_str
    assert sue_pidginunit.groupmap.event_int == five_event_int
    assert sue_pidginunit.groupmap.unknown_word == y_uk
    assert sue_pidginunit.groupmap.otx_bridge == slash_otx_bridge
    assert sue_pidginunit.groupmap.inx_bridge == colon_inx_bridge
    assert sue_pidginunit.ideamap.face_name == sue_str
    assert sue_pidginunit.ideamap.event_int == five_event_int
    assert sue_pidginunit.ideamap.unknown_word == y_uk
    assert sue_pidginunit.ideamap.otx_bridge == slash_otx_bridge
    assert sue_pidginunit.ideamap.inx_bridge == colon_inx_bridge
    assert sue_pidginunit.roadmap.face_name == sue_str
    assert sue_pidginunit.roadmap.event_int == five_event_int
    assert sue_pidginunit.roadmap.unknown_word == y_uk
    assert sue_pidginunit.roadmap.otx_bridge == slash_otx_bridge
    assert sue_pidginunit.roadmap.inx_bridge == colon_inx_bridge


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
    acctmap = acctmap_shop(face_name=sue_str)
    acctmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.acctmap != acctmap

    # WHEN
    sue_pidginunit.set_acctmap(acctmap)

    # THEN
    assert sue_pidginunit.acctmap == acctmap


def test_PidginUnit_set_mapunit_SetsAttr_SpecialCase_RoadUnit():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    roadmap = roadmap_shop(face_name=sue_str)
    roadmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.roadmap != roadmap

    # WHEN
    sue_pidginunit.set_roadmap(roadmap)

    # THEN
    assert sue_pidginunit.roadmap == roadmap


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_otx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_bridge = "/"
    acctmap = acctmap_shop(otx_bridge=slash_otx_bridge, face_name=sue_str)
    assert sue_pidginunit.otx_bridge != acctmap.otx_bridge
    assert sue_pidginunit.acctmap != acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(acctmap)
    exception_str = f"set_mapcore Error: PidginUnit otx_bridge is '{sue_pidginunit.otx_bridge}', MapCore is '{slash_otx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_inx_bridge_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_bridge = "/"
    acctmap = acctmap_shop(inx_bridge=slash_inx_bridge, face_name=sue_str)
    assert sue_pidginunit.inx_bridge != acctmap.inx_bridge
    assert sue_pidginunit.acctmap != acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(acctmap)
    exception_str = f"set_mapcore Error: PidginUnit inx_bridge is '{sue_pidginunit.inx_bridge}', MapCore is '{slash_inx_bridge}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    acctmap = acctmap_shop(unknown_word=casa_unknown_word, face_name=sue_str)
    assert sue_pidginunit.unknown_word != acctmap.unknown_word
    assert sue_pidginunit.acctmap != acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(acctmap)
    exception_str = f"set_mapcore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', MapCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_mapunit_RaisesErrorIf_mapunit_face_name_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    acctmap = acctmap_shop(face_name=yao_str)
    assert sue_pidginunit.face_name != acctmap.face_name
    assert sue_pidginunit.acctmap != acctmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctmap(acctmap)
    exception_str = f"set_mapcore Error: PidginUnit face_name is '{sue_pidginunit.face_name}', MapCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_mapunit_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pu = pidginunit_shop(sue_str)
    static_acctmap = acctmap_shop(face_name=sue_str)
    static_acctmap.set_otx2inx("Bob", "Bob of Portland")
    sue_pu.set_acctmap(static_acctmap)

    # WHEN / THEN
    assert sue_pu.get_mapunit(type_AcctName_str()) == sue_pu.acctmap
    assert sue_pu.get_mapunit(type_GroupLabel_str()) == sue_pu.groupmap
    assert sue_pu.get_mapunit(type_IdeaUnit_str()) == sue_pu.ideamap
    assert sue_pu.get_mapunit(type_RoadUnit_str()) == sue_pu.roadmap

    assert sue_pu.get_mapunit(type_AcctName_str()) != sue_pu.roadmap
    assert sue_pu.get_mapunit(type_GroupLabel_str()) != sue_pu.roadmap
    assert sue_pu.get_mapunit(type_IdeaUnit_str()) != sue_pu.roadmap


def test_PidginUnit_is_valid_ReturnsObj():
    # ESTABLISH
    invalid_acctmap = get_invalid_acctmap()
    invalid_groupmap = get_invalid_groupmap()
    invalid_ideamap = get_invalid_ideamap()
    valid_acctmap = get_suita_acctmap()
    valid_groupmap = get_swim_groupmap()
    valid_ideamap = get_clean_roadmap()
    assert valid_acctmap.is_valid()
    assert valid_groupmap.is_valid()
    assert valid_ideamap.is_valid()
    assert invalid_ideamap.is_valid() is False
    assert invalid_groupmap.is_valid() is False
    assert invalid_acctmap.is_valid() is False

    # WHEN / THEN
    sue_pidginunit = pidginunit_shop("Sue")
    assert sue_pidginunit.is_valid()
    sue_pidginunit.set_acctmap(valid_acctmap)
    sue_pidginunit.set_groupmap(valid_groupmap)
    sue_pidginunit.set_roadmap(valid_ideamap)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_acctmap(invalid_acctmap)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_acctmap(valid_acctmap)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_groupmap(invalid_groupmap)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_groupmap(valid_groupmap)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_roadmap(invalid_ideamap)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_roadmap(valid_ideamap)
    assert sue_pidginunit.is_valid()


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario0_type_AcctName_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acctmap = zia_pidginunit.get_acctmap()
    assert acctmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_AcctName_str(), sue_otx, sue_inx)

    # THEN
    assert acctmap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario1_type_RoadUnit_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    roadmap = zia_pidginunit.get_roadmap()
    assert roadmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_RoadUnit_str(), sue_otx, sue_inx)

    # THEN
    assert roadmap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario2_type_IdeaUnit_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    roadmap = zia_pidginunit.get_ideamap()
    assert roadmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_IdeaUnit_str(), sue_otx, sue_inx)

    # THEN
    assert roadmap.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_type = type_IdeaUnit_str()
    assert zia_pidginunit.otx2inx_exists(road_type, sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_IdeaUnit_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.otx2inx_exists(road_type, sue_otx, sue_inx)


def test_PidginUnit_get_inx_value_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_value(type_AcctName_str(), sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_otx2inx(type_AcctName_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_value(type_AcctName_str(), sue_otx) == sue_inx


def test_PidginUnit_del_otx2inx_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_type = type_IdeaUnit_str()
    zia_pidginunit.set_otx2inx(type_IdeaUnit_str(), sue_otx, sue_inx)
    zia_pidginunit.set_otx2inx(type_IdeaUnit_str(), zia_str, zia_str)
    assert zia_pidginunit.otx2inx_exists(road_type, sue_otx, sue_inx)
    assert zia_pidginunit.otx2inx_exists(road_type, zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_otx2inx(road_type, sue_otx)

    # THEN
    assert zia_pidginunit.otx2inx_exists(road_type, sue_otx, sue_inx) is False
    assert zia_pidginunit.otx2inx_exists(road_type, zia_str, zia_str)


def test_PidginUnit_set_idea_SetsAttr_Scenario1_type_RoadUnit_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    roadmap = zia_pidginunit.get_roadmap()
    assert roadmap.idea_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_idea(sue_otx, sue_inx)

    # THEN
    assert roadmap.idea_exists(sue_otx, sue_inx)


def test_PidginUnit_idea_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    sue_exists = zia_pidginunit.idea_exists(sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_pidginunit.set_idea(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.idea_exists(sue_otx, sue_inx)


def test_PidginUnit_get_inx_idea_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_idea(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_idea(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_idea(sue_otx) == sue_inx


def test_PidginUnit_del_idea_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    zia_pidginunit.set_idea(sue_otx, sue_inx)
    zia_pidginunit.set_idea(zia_str, zia_str)
    assert zia_pidginunit.idea_exists(sue_otx, sue_inx)
    assert zia_pidginunit.idea_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_idea(sue_otx)

    # THEN
    sue_exists = zia_pidginunit.idea_exists(sue_otx, sue_inx)
    assert sue_exists is False
    assert zia_pidginunit.idea_exists(zia_str, zia_str)
