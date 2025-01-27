from src.f01_road.road import (
    TitleUnit,
    NameUnit,
    HealerName,
    OwnerName,
    AcctName,
    RoadUnit,
    DoarUnit,
    GroupLabel,
    default_bridge_if_None,
    WorldID,
    get_default_world_id,
    TimeLineTitle,
    FaceName,
    get_default_face_name,
    EventInt,
)
from inspect import getdoc as inspect_getdoc


def test_NameUnit_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_nameunit = NameUnit(bob_str)
    # THEN
    assert bob_nameunit == bob_str
    doc_str = "All Name string classes should inherit from this class"
    assert inspect_getdoc(bob_nameunit) == doc_str


def test_NameUnit_is_name_ReturnsObj_Scenario0():
    # WHEN / THEN
    assert NameUnit("").is_name() is False
    assert NameUnit("A").is_name()

    # WHEN / THEN
    x_s = default_bridge_if_None()
    x_nameunit = NameUnit(f"casa{x_s}kitchen")
    assert x_nameunit.is_name() is False


def test_NameUnit_is_name_ReturnsObj_Scenario1():
    # ESTABLISH / WHEN / THEN
    slash_str = "/"
    x_nameunit = NameUnit(f"casa{slash_str}kitchen")
    assert x_nameunit.is_name()
    assert x_nameunit.is_name(slash_str) is False


def test_HealerName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_healer_name = HealerName(bob_str)
    # THEN
    assert bob_healer_name == bob_str
    doc_str = "A TitleUnit used to identify a Problem's Healer"
    assert inspect_getdoc(bob_healer_name) == doc_str


def test_OwnerName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_owner_name = OwnerName(bob_str)
    # THEN
    assert bob_owner_name == bob_str
    doc_str = "A TitleUnit used to identify a BudUnit's owner_name"
    assert inspect_getdoc(bob_owner_name) == doc_str


def test_AcctName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_acct_name = AcctName(bob_str)
    # THEN
    assert bob_acct_name == bob_str
    doc_str = "Every AcctName object is OwnerName, must follow OwnerName format."
    assert inspect_getdoc(bob_acct_name) == doc_str


def test_GroupLabel_exists():
    bikers_group_label = GroupLabel("bikers")
    assert bikers_group_label is not None
    assert str(type(bikers_group_label)).find("src.f01_road.road.GroupLabel") > 0


def test_TitleUnit_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_road = TitleUnit(empty_str)
    # THEN
    assert x_road == empty_str
    doc_str = (
        "A string presentation of a tree node. Nodes cannot contain RoadUnit bridge"
    )
    assert inspect_getdoc(x_road) == doc_str


def test_default_bridge_if_None_ReturnsObj():
    # ESTABLISH
    semicolon_str = ";"
    slash_str = "/"
    colon_str = ":"
    buzz_str = "buzz"

    # WHEN / THEN
    assert default_bridge_if_None() == semicolon_str
    assert default_bridge_if_None(None) == semicolon_str
    x_nan = float("nan")
    assert default_bridge_if_None(x_nan) == semicolon_str
    assert default_bridge_if_None(slash_str) == slash_str
    assert default_bridge_if_None(colon_str) == colon_str
    assert default_bridge_if_None(buzz_str) == buzz_str


def test_TitleUnit_is_title_ReturnsObj_Scenario0():
    # WHEN / THEN
    assert TitleUnit("").is_title() is False
    assert TitleUnit("A").is_title()

    # WHEN / THEN
    x_s = default_bridge_if_None()
    x_titleunit = TitleUnit(f"casa{x_s}kitchen")
    assert x_titleunit.is_title() is False


def test_TitleUnit_is_title_ReturnsObj_Scenario1():
    # ESTABLISH / WHEN / THEN
    slash_str = "/"
    x_titleunit = TitleUnit(f"casa{slash_str}kitchen")
    assert x_titleunit.is_title()
    assert x_titleunit.is_title(slash_str) is False


def test_RoadUnit_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_road = RoadUnit(empty_str)
    # THEN
    assert x_road == empty_str
    doc_str = (
        "A string presentation of a tree path. TitleUnits are seperated by road bridge"
    )
    assert inspect_getdoc(x_road) == doc_str


def test_DoarUnit_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_road = DoarUnit(empty_str)
    # THEN
    assert x_road == empty_str
    doc_str = "DoarUnit is a RoadUnit in reverse direction. A string presentation of a tree path. TitleUnits are seperated by road bridge."
    assert inspect_getdoc(x_road) == doc_str


def test_TimeLineTitle_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_timelinetitle = TimeLineTitle(empty_str)
    # THEN
    assert x_timelinetitle == empty_str
    doc_str = "TimeLineTitle is required for every TimeLineUnit. It is a TitleUnit that must not container the bridge."
    assert inspect_getdoc(x_timelinetitle) == doc_str


def test_WorldID_Exists():
    # ESTABLISH / WHEN / THEN
    assert WorldID() == ""
    assert WorldID("cookie") == "cookie"


def test_get_default_world_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_world_id() == "TestingWorld3"


def test_FaceName_Exists():
    # ESTABLISH / WHEN / THEN
    assert FaceName() == ""
    assert FaceName("cookie") == "cookie"


def test_get_default_face_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_face_name() == "Face1234"


def test_EventInt_Exists():
    # ESTABLISH / WHEN / THEN
    assert EventInt() == 0
    assert EventInt(12) == 12
    assert EventInt(12.4) == 12
