from src.f01_road.road import default_wall_if_none
from src.f04_gift.atom_config import (
    get_atom_args_jaar_types,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
)
from src.f08_pidgin.bridge import (
    groupbridge_shop,
    acctbridge_shop,
    nodebridge_shop,
    roadbridge_shop,
)
from src.f08_pidgin.pidgin import (
    PidginUnit,
    pidginunit_shop,
    default_unknown_word,
    pidginable_jaar_types,
    pidginable_atom_args,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_invalid_acctbridge,
    get_invalid_groupbridge,
    get_invalid_nodebridge,
    get_clean_roadbridge,
    get_clean_nodebridge,
    get_swim_groupbridge,
    get_suita_acctbridge,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy

# from otx.f08_pidgin.examples.pidgin_env import get_test_pidgins_dir, env_dir_setup_cleanup

# The goal of the pidgin function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_pidginable_jaar_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginable_jaar_types = pidginable_jaar_types()

    # THEN
    assert len(x_pidginable_jaar_types) == 4
    assert x_pidginable_jaar_types == {
        type_AcctID_str(),
        type_GroupID_str(),
        type_RoadNode_str(),
        type_RoadUnit_str(),
    }
    print(f"{set(get_atom_args_jaar_types().values())=}")
    all_atom_jaar_types = set(get_atom_args_jaar_types().values())
    inter_x = set(all_atom_jaar_types).intersection(x_pidginable_jaar_types)
    assert inter_x == x_pidginable_jaar_types


def test_pidginable_atom_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert len(pidginable_atom_args()) == 11
    assert pidginable_atom_args() == {
        "acct_id",
        "awardee_id",
        "road",
        "parent_road",
        "label",
        "healer_id",
        "need",
        "base",
        "pick",
        "group_id",
        "team_id",
    }

    print(f"{pidginable_jaar_types()=}")
    all_jaar_types = set(get_atom_args_jaar_types().keys())
    assert pidginable_atom_args().issubset(all_jaar_types)
    static_pidginable_atom_args = {
        x_arg
        for x_arg, jaar_type in get_atom_args_jaar_types().items()
        if jaar_type in pidginable_jaar_types()
    }
    assert pidginable_atom_args() == static_pidginable_atom_args


def test_PidginUnit_Exists():
    # ESTABLISH
    x_pidginunit = PidginUnit()

    # WHEN / THEN
    assert not x_pidginunit.event_id
    assert not x_pidginunit.groupbridge
    assert not x_pidginunit.acctbridge
    assert not x_pidginunit.nodebridge
    assert not x_pidginunit.roadbridge
    assert not x_pidginunit.unknown_word
    assert not x_pidginunit.otx_wall
    assert not x_pidginunit.inx_wall
    assert not x_pidginunit.face_id


def test_pidginunit_shop_ReturnsObj_scenario0():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    sue_pidginunit = pidginunit_shop(sue_str)

    # THEN
    assert sue_pidginunit.face_id == sue_str
    assert sue_pidginunit.event_id == 0
    assert sue_pidginunit.unknown_word == default_unknown_word()
    assert sue_pidginunit.otx_wall == default_wall_if_none()
    assert sue_pidginunit.inx_wall == default_wall_if_none()
    assert sue_pidginunit.groupbridge == groupbridge_shop(x_face_id=sue_str)
    assert sue_pidginunit.acctbridge == acctbridge_shop(x_face_id=sue_str)
    assert sue_pidginunit.nodebridge == nodebridge_shop(x_face_id=sue_str)
    assert sue_pidginunit.roadbridge == roadbridge_shop(x_face_id=sue_str)
    assert sue_pidginunit.acctbridge.unknown_word == default_unknown_word()
    assert sue_pidginunit.acctbridge.otx_wall == default_wall_if_none()
    assert sue_pidginunit.acctbridge.inx_wall == default_wall_if_none()
    assert sue_pidginunit.groupbridge.unknown_word == default_unknown_word()
    assert sue_pidginunit.groupbridge.otx_wall == default_wall_if_none()
    assert sue_pidginunit.groupbridge.inx_wall == default_wall_if_none()
    assert sue_pidginunit.roadbridge.unknown_word == default_unknown_word()
    assert sue_pidginunit.roadbridge.otx_wall == default_wall_if_none()
    assert sue_pidginunit.roadbridge.inx_wall == default_wall_if_none()


def test_pidginunit_shop_ReturnsObj_scenario1():
    # ESTABLISH
    sue_str = "Sue"
    five_event_id = 5
    y_uk = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"

    # WHEN
    sue_pidginunit = pidginunit_shop(
        sue_str, five_event_id, slash_otx_wall, colon_inx_wall, y_uk
    )

    # THEN
    assert sue_pidginunit.event_id == five_event_id
    assert sue_pidginunit.unknown_word == y_uk
    assert sue_pidginunit.otx_wall == slash_otx_wall
    assert sue_pidginunit.inx_wall == colon_inx_wall

    x_groupbridge = groupbridge_shop(slash_otx_wall, colon_inx_wall, {}, y_uk, sue_str)
    x_acctbridge = acctbridge_shop(slash_otx_wall, colon_inx_wall, {}, y_uk, sue_str)
    x_roadbridge = roadbridge_shop(
        slash_otx_wall, colon_inx_wall, None, {}, y_uk, sue_str
    )
    assert sue_pidginunit.groupbridge == x_groupbridge
    assert sue_pidginunit.acctbridge == x_acctbridge
    assert sue_pidginunit.roadbridge == x_roadbridge

    assert sue_pidginunit.acctbridge.unknown_word == y_uk
    assert sue_pidginunit.acctbridge.otx_wall == slash_otx_wall
    assert sue_pidginunit.acctbridge.inx_wall == colon_inx_wall
    assert sue_pidginunit.acctbridge.face_id == sue_str
    assert sue_pidginunit.groupbridge.unknown_word == y_uk
    assert sue_pidginunit.groupbridge.otx_wall == slash_otx_wall
    assert sue_pidginunit.groupbridge.inx_wall == colon_inx_wall
    assert sue_pidginunit.groupbridge.face_id == sue_str
    assert sue_pidginunit.nodebridge.unknown_word == y_uk
    assert sue_pidginunit.nodebridge.otx_wall == slash_otx_wall
    assert sue_pidginunit.nodebridge.inx_wall == colon_inx_wall
    assert sue_pidginunit.nodebridge.face_id == sue_str
    assert sue_pidginunit.roadbridge.unknown_word == y_uk
    assert sue_pidginunit.roadbridge.otx_wall == slash_otx_wall
    assert sue_pidginunit.roadbridge.inx_wall == colon_inx_wall
    assert sue_pidginunit.roadbridge.face_id == sue_str


def test_PidginUnit_set_bridgeunit_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    acctbridge = acctbridge_shop(x_face_id=sue_str)
    acctbridge.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.acctbridge != acctbridge

    # WHEN
    sue_pidginunit.set_acctbridge(acctbridge)

    # THEN
    assert sue_pidginunit.acctbridge == acctbridge


def test_PidginUnit_set_bridgeunit_SetsAttr_SpecialCase_RoadUnit():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    roadbridge = roadbridge_shop(x_face_id=sue_str)
    roadbridge.set_otx2inx("Bob", "Bob of Portland")
    assert sue_pidginunit.roadbridge != roadbridge

    # WHEN
    sue_pidginunit.set_roadbridge(roadbridge)

    # THEN
    assert sue_pidginunit.roadbridge == roadbridge


def test_PidginUnit_set_bridgeunit_RaisesErrorIf_bridgeunit_otx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_wall = "/"
    acctbridge = acctbridge_shop(x_otx_wall=slash_otx_wall, x_face_id=sue_str)
    assert sue_pidginunit.otx_wall != acctbridge.otx_wall
    assert sue_pidginunit.acctbridge != acctbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctbridge(acctbridge)
    exception_str = f"set_bridgecore Error: PidginUnit otx_wall is '{sue_pidginunit.otx_wall}', BridgeCore is '{slash_otx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_bridgeunit_RaisesErrorIf_bridgeunit_inx_wall_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_wall = "/"
    acctbridge = acctbridge_shop(x_inx_wall=slash_inx_wall, x_face_id=sue_str)
    assert sue_pidginunit.inx_wall != acctbridge.inx_wall
    assert sue_pidginunit.acctbridge != acctbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctbridge(acctbridge)
    exception_str = f"set_bridgecore Error: PidginUnit inx_wall is '{sue_pidginunit.inx_wall}', BridgeCore is '{slash_inx_wall}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_bridgeunit_RaisesErrorIf_bridgeunit_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    acctbridge = acctbridge_shop(x_unknown_word=casa_unknown_word, x_face_id=sue_str)
    assert sue_pidginunit.unknown_word != acctbridge.unknown_word
    assert sue_pidginunit.acctbridge != acctbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctbridge(acctbridge)
    exception_str = f"set_bridgecore Error: PidginUnit unknown_word is '{sue_pidginunit.unknown_word}', BridgeCore is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_bridgeunit_RaisesErrorIf_bridgeunit_face_id_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    acctbridge = acctbridge_shop(x_face_id=yao_str)
    assert sue_pidginunit.face_id != acctbridge.face_id
    assert sue_pidginunit.acctbridge != acctbridge

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_acctbridge(acctbridge)
    exception_str = f"set_bridgecore Error: PidginUnit face_id is '{sue_pidginunit.face_id}', BridgeCore is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_bridgeunit_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pu = pidginunit_shop(sue_str)
    static_acctbridge = acctbridge_shop(x_face_id=sue_str)
    static_acctbridge.set_otx2inx("Bob", "Bob of Portland")
    sue_pu.set_acctbridge(static_acctbridge)

    # WHEN / THEN
    assert sue_pu.get_bridgeunit(type_AcctID_str()) == sue_pu.acctbridge
    assert sue_pu.get_bridgeunit(type_GroupID_str()) == sue_pu.groupbridge
    assert sue_pu.get_bridgeunit(type_RoadNode_str()) == sue_pu.nodebridge
    assert sue_pu.get_bridgeunit(type_RoadUnit_str()) == sue_pu.roadbridge

    assert sue_pu.get_bridgeunit(type_AcctID_str()) != sue_pu.roadbridge
    assert sue_pu.get_bridgeunit(type_GroupID_str()) != sue_pu.roadbridge
    assert sue_pu.get_bridgeunit(type_RoadNode_str()) != sue_pu.roadbridge


def test_PidginUnit_is_valid_ReturnsObj():
    # ESTABLISH
    invalid_acctbridge = get_invalid_acctbridge()
    invalid_groupbridge = get_invalid_groupbridge()
    invalid_nodebridge = get_invalid_nodebridge()
    valid_acctbridge = get_suita_acctbridge()
    valid_groupbridge = get_swim_groupbridge()
    valid_nodebridge = get_clean_roadbridge()
    assert valid_acctbridge.is_valid()
    assert valid_groupbridge.is_valid()
    assert valid_nodebridge.is_valid()
    assert invalid_nodebridge.is_valid() is False
    assert invalid_groupbridge.is_valid() is False
    assert invalid_acctbridge.is_valid() is False

    # WHEN / THEN
    sue_pidginunit = pidginunit_shop("Sue")
    assert sue_pidginunit.is_valid()
    sue_pidginunit.set_acctbridge(valid_acctbridge)
    sue_pidginunit.set_groupbridge(valid_groupbridge)
    sue_pidginunit.set_roadbridge(valid_nodebridge)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_acctbridge(invalid_acctbridge)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_acctbridge(valid_acctbridge)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_groupbridge(invalid_groupbridge)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_groupbridge(valid_groupbridge)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_roadbridge(invalid_nodebridge)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_roadbridge(valid_nodebridge)
    assert sue_pidginunit.is_valid()


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario0_type_AcctID_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acctbridge = zia_pidginunit.get_acctbridge()
    assert acctbridge.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_AcctID_str(), sue_otx, sue_inx)

    # THEN
    assert acctbridge.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario1_type_RoadUnit_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    roadbridge = zia_pidginunit.get_roadbridge()
    assert roadbridge.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_RoadUnit_str(), sue_otx, sue_inx)

    # THEN
    assert roadbridge.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx2inx_SetsAttr_Scenario2_type_RoadNode_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    roadbridge = zia_pidginunit.get_nodebridge()
    assert roadbridge.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_RoadNode_str(), sue_otx, sue_inx)

    # THEN
    assert roadbridge.otx2inx_exists(sue_otx, sue_inx)


def test_PidginUnit_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_type = type_RoadNode_str()
    assert zia_pidginunit.otx2inx_exists(road_type, sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx2inx(type_RoadNode_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.otx2inx_exists(road_type, sue_otx, sue_inx)


def test_PidginUnit_get_inx_value_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_value(type_AcctID_str(), sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_otx2inx(type_AcctID_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_value(type_AcctID_str(), sue_otx) == sue_inx


def test_PidginUnit_del_otx2inx_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_type = type_RoadNode_str()
    zia_pidginunit.set_otx2inx(type_RoadNode_str(), sue_otx, sue_inx)
    zia_pidginunit.set_otx2inx(type_RoadNode_str(), zia_str, zia_str)
    assert zia_pidginunit.otx2inx_exists(road_type, sue_otx, sue_inx)
    assert zia_pidginunit.otx2inx_exists(road_type, zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_otx2inx(road_type, sue_otx)

    # THEN
    assert zia_pidginunit.otx2inx_exists(road_type, sue_otx, sue_inx) is False
    assert zia_pidginunit.otx2inx_exists(road_type, zia_str, zia_str)


def test_PidginUnit_set_nub_label_SetsAttr_Scenario1_type_RoadUnit_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    roadbridge = zia_pidginunit.get_roadbridge()
    assert roadbridge.nub_label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_nub_label(sue_otx, sue_inx)

    # THEN
    assert roadbridge.nub_label_exists(sue_otx, sue_inx)


def test_PidginUnit_nub_label_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    sue_exists = zia_pidginunit.nub_label_exists(sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_pidginunit.set_nub_label(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.nub_label_exists(sue_otx, sue_inx)


def test_PidginUnit_get_nub_inx_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_nub_inx_label(sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_nub_label(sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_nub_inx_label(sue_otx) == sue_inx


def test_PidginUnit_del_nub_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    zia_pidginunit.set_nub_label(sue_otx, sue_inx)
    zia_pidginunit.set_nub_label(zia_str, zia_str)
    assert zia_pidginunit.nub_label_exists(sue_otx, sue_inx)
    assert zia_pidginunit.nub_label_exists(zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_nub_label(sue_otx)

    # THEN
    sue_exists = zia_pidginunit.nub_label_exists(sue_otx, sue_inx)
    assert sue_exists is False
    assert zia_pidginunit.nub_label_exists(zia_str, zia_str)
