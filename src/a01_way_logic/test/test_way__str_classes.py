from src.a01_way_logic.way import (
    WordStr,
    NameStr,
    LabelStr,
    HealerName,
    OwnerName,
    AcctName,
    WayStr,
    YawStr,
    GroupLabel,
    default_bridge_if_None,
    WorldID,
    TimeLineWord,
    FaceName,
    get_default_face_name,
    EventInt,
)
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
    doc_str = "A WordStr used to identify a Problem's Healer"
    assert inspect_getdoc(bob_healer_name) == doc_str


def test_OwnerName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_owner_name = OwnerName(bob_str)
    # THEN
    assert bob_owner_name == bob_str
    doc_str = "A WordStr used to identify a BudUnit's owner_name"
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


def test_LabelStr_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_namestr = LabelStr(bob_str)
    # THEN
    assert bob_namestr == bob_str
    doc_str = """If a LabelStr contains bridges it represents a group otherwise it's a single member group of an AcctName."""
    assert inspect_getdoc(bob_namestr) == doc_str


def test_GroupLabel_exists():
    bikers_group_label = GroupLabel(";bikers")
    assert bikers_group_label is not None
    assert str(type(bikers_group_label)).find("src.a01_way_logic.way.GroupLabel") > 0


def test_WordStr_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_way = WordStr(empty_str)
    # THEN
    assert x_way == empty_str
    doc_str = (
        "A string representation of a tree node. Nodes cannot contain WayStr bridge"
    )
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


def test_WordStr_is_word_ReturnsObj_Scenario0():
    # WHEN / THEN
    assert WordStr("").is_word() is False
    assert WordStr("A").is_word()

    # WHEN / THEN
    x_s = default_bridge_if_None()
    x_wordstr = WordStr(f"casa{x_s}kitchen")
    assert x_wordstr.is_word() is False


def test_WordStr_is_word_ReturnsObj_Scenario1():
    # ESTABLISH / WHEN / THEN
    slash_str = "/"
    x_wordstr = WordStr(f"casa{slash_str}kitchen")
    assert x_wordstr.is_word()
    assert x_wordstr.is_word(slash_str) is False


def test_WayStr_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_way = WayStr(empty_str)
    # THEN
    assert x_way == empty_str
    doc_str = (
        "A string representation of a tree path. WordStrs are seperated by way bridge"
    )
    assert inspect_getdoc(x_way) == doc_str


def test_YawStr_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_way = YawStr(empty_str)
    # THEN
    assert x_way == empty_str
    doc_str = "YawStr is a WayStr in reverse direction. A string representation of a tree path. WordStrs are seperated by way bridge."
    assert inspect_getdoc(x_way) == doc_str


def test_TimeLineWord_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_timelineword = TimeLineWord(empty_str)
    # THEN
    assert x_timelineword == empty_str
    doc_str = "TimeLineWord is required for every TimeLineUnit. It is a WordStr that must not container the bridge."
    assert inspect_getdoc(x_timelineword) == doc_str


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
