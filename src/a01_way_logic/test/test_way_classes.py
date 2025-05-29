from src.a01_way_logic.way import (
    LabelStr,
    NameStr,
    TitleStr,
    HealerName,
    OwnerName,
    AcctName,
    WayStr,
    YawStr,
    GroupTitle,
    default_bridge_if_None,
    WorldID,
    TimeLineLabel,
    FaceName,
    get_default_face_name,
    EventInt,
)
from src.a01_way_logic._test_util.a01_str import bridge_str
from inspect import getdoc as inspect_getdoc


def test_NameStr_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_namestr = NameStr(bob_str)
    # THEN
    assert bob_namestr == bob_str
    doc_str = "All Name string classes should inherit from this class"
    assert inspect_getdoc(bob_namestr) == doc_str


def test_NameStr_is_name_ReturnsObj_Scenario0():
    # WHEN / THEN
    assert NameStr("").is_name() is False
    assert NameStr("A").is_name()

    # WHEN / THEN
    x_s = default_bridge_if_None()
    x_namestr = NameStr(f"casa{x_s}kitchen")
    assert x_namestr.is_name() is False


def test_NameStr_is_name_ReturnsObj_Scenario1():
    # ESTABLISH / WHEN / THEN
    slash_str = "/"
    x_namestr = NameStr(f"casa{slash_str}kitchen")
    assert x_namestr.is_name()
    assert x_namestr.is_name(slash_str) is False


def test_HealerName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_healer_name = HealerName(bob_str)
    # THEN
    assert bob_healer_name == bob_str
    doc_str = "A LabelStr used to identify a Problem's Healer"
    assert inspect_getdoc(bob_healer_name) == doc_str


def test_OwnerName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_owner_name = OwnerName(bob_str)
    # THEN
    assert bob_owner_name == bob_str
    doc_str = "A LabelStr used to identify a BudUnit's owner_name"
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


def test_TitleStr_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_namestr = TitleStr(bob_str)
    # THEN
    assert bob_namestr == bob_str
    doc_str = f"""If a TitleStr contains {bridge_str()}s it represents a group otherwise it's a single member group of an AcctName."""
    assert inspect_getdoc(bob_namestr) == doc_str


def test_GroupTitle_exists():
    bikers_group_title = GroupTitle(";bikers")
    assert bikers_group_title is not None
    assert str(type(bikers_group_title)).find("src.a01_way_logic.way.GroupTitle") > 0


def test_LabelStr_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_way = LabelStr(empty_str)
    # THEN
    assert x_way == empty_str
    doc_str = f"A string representation of a tree node. Nodes cannot contain WayStr {bridge_str()}"
    assert inspect_getdoc(x_way) == doc_str


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


def test_LabelStr_is_label_ReturnsObj_Scenario0():
    # WHEN / THEN
    assert LabelStr("").is_label() is False
    assert LabelStr("A").is_label()

    # WHEN / THEN
    x_s = default_bridge_if_None()
    x_labelstr = LabelStr(f"casa{x_s}kitchen")
    assert x_labelstr.is_label() is False


def test_LabelStr_is_label_ReturnsObj_Scenario1():
    # ESTABLISH / WHEN / THEN
    slash_str = "/"
    x_labelstr = LabelStr(f"casa{slash_str}kitchen")
    assert x_labelstr.is_label()
    assert x_labelstr.is_label(slash_str) is False


def test_WayStr_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_way = WayStr(empty_str)
    # THEN
    assert x_way == empty_str
    doc_str = f"A string representation of a tree path. LabelStrs are seperated by way {bridge_str()}"
    assert inspect_getdoc(x_way) == doc_str


def test_YawStr_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_way = YawStr(empty_str)
    # THEN
    assert x_way == empty_str
    doc_str = f"YawStr is a WayStr in reverse direction. A string representation of a tree path. LabelStrs are seperated by way {bridge_str()}."
    assert inspect_getdoc(x_way) == doc_str


def test_TimeLineLabel_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_timelinelabel = TimeLineLabel(empty_str)
    # THEN
    assert x_timelinelabel == empty_str
    doc_str = f"TimeLineLabel is required for every TimeLineUnit. It is a LabelStr that must not container the {bridge_str()}."
    assert inspect_getdoc(x_timelinelabel) == doc_str


def test_WorldID_Exists():
    # ESTABLISH / WHEN / THEN
    assert WorldID() == ""
    assert WorldID("cookie") == "cookie"


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
