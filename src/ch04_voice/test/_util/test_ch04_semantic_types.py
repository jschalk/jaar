from inspect import getdoc as inspect_getdoc
from src.ch04_voice._ref.ch04_semantic_types import (
    FundGrain,
    FundNum,
    GroupTitle,
    HealerName,
    NameTerm,
    RespectGrain,
    RespectNum,
    TitleTerm,
    VoiceName,
)
from src.ref.keywords import Ch04Keywords as kw


def test_NameTerm_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_nameterm = NameTerm(bob_str)
    # THEN
    assert bob_nameterm == bob_str
    doc_str = "All Name string classes should inherit from this class"
    assert inspect_getdoc(bob_nameterm) == doc_str


def test_HealerName_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_healer_str = HealerName(bob_str)
    # THEN
    assert bob_healer_str == bob_str
    doc_str = "A LabelTerm used to identify a Problem's Healer"
    assert inspect_getdoc(bob_healer_str) == doc_str


def test_VoiceName_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_VoiceName = VoiceName(bob_str)
    # THEN
    assert bob_VoiceName == bob_str
    doc_str = "Every VoiceName object is NameTerm, must follow NameTerm format."
    assert inspect_getdoc(bob_VoiceName) == doc_str


def test_TitleTerm_Exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_nameterm = TitleTerm(bob_str)
    # THEN
    assert bob_nameterm == bob_str
    doc_str = f"""If a TitleTerm contains SepartorTerms(s) it represents a group otherwise its a single member group of an VoiceName."""
    assert inspect_getdoc(bob_nameterm) == doc_str


def test_GroupTitle_Exists():
    # ESTABLISH / WHEN
    bikers_GroupTitle = GroupTitle(";bikers")

    # THEN
    assert bikers_GroupTitle is not None


def test_FundNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_fund_num = FundNum(x_float)
    # THEN
    assert y_fund_num == x_float
    inspect_str = "FundNum inherits from float class"
    assert inspect_getdoc(y_fund_num) == inspect_str


def test_FundGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_fund_grainnum = FundGrain(x_float)
    # THEN
    assert y_fund_grainnum == x_float
    inspect_str = "Smallest Unit of fund_num"
    assert inspect_getdoc(y_fund_grainnum) == inspect_str


def test_RespectGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_RespectGrain = RespectGrain(x_float)
    # THEN
    assert y_RespectGrain == x_float
    inspect_str = (
        "Smallest Unit of score (RespectNum) ala 'the slightest bit of respect!'"
    )
    assert inspect_getdoc(y_RespectGrain) == inspect_str


def test_RespectNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_RespectNum = RespectNum(x_float)
    # THEN
    assert y_RespectNum == x_float
    assert inspect_getdoc(y_RespectNum) == "RespectNum inherits from float class"
