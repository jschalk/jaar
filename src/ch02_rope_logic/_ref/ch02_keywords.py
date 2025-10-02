from enum import Enum


class Ch02Keywords(str, Enum):
    FirstLabel = "FirstLabel"
    INSERT = "INSERT"
    KnotTerm = "KnotTerm"
    LabelTerm = "LabelTerm"
    NameTerm = "NameTerm"
    RopeTerm = "RopeTerm"
    TitleTerm = "TitleTerm"
    UPDATE = "UPDATE"
    knot = "knot"
    parent_rope = "parent_rope"
    sqlite_datatype = "sqlite_datatype"

    def __str__(self):
        return self.value
