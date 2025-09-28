from src.ch01_data_toolbox._ref.ch01_keywords import *


def KnotTerm_str() -> str:
    return "KnotTerm"


def LabelTerm_str() -> str:
    return "LabelTerm"


def MomentLabel_str() -> str:
    return "MomentLabel"


def NameTerm_str() -> str:
    return "NameTerm"


def NexusLabel_str() -> str:
    return "NexusLabel"


def RopeTerm_str() -> str:
    return "RopeTerm"


def TitleTerm_str() -> str:
    return "TitleTerm"


def knot_str() -> str:
    return "knot"


def parent_rope_str() -> str:
    return "parent_rope"


class Ch02Keywords(str, Enum):
    INSERT = "INSERT"
    KnotTerm = "KnotTerm"
    LabelTerm = "LabelTerm"
    MomentLabel = "MomentLabel"
    NameTerm = "NameTerm"
    NexusLabel = "NexusLabel"
    RopeTerm = "RopeTerm"
    TitleTerm = "TitleTerm"
    UPDATE = "UPDATE"
    knot = "knot"
    parent_rope = "parent_rope"
    sqlite_datatype = "sqlite_datatype"
