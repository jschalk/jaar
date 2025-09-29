from src.ch01_data_toolbox._ref.ch01_keywords import *


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

    def __str__(self):
        return self.value
