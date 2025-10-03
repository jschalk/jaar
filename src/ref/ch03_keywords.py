from enum import Enum


class Ch03Keywords(str, Enum):
    FirstLabel = "FirstLabel"
    GrainNum = "GrainNum"
    INSERT = "INSERT"
    KnotTerm = "KnotTerm"
    LabelTerm = "LabelTerm"
    MoneyGrain = "MoneyGrain"
    MoneyNum = "MoneyNum"
    PoolNum = "PoolNum"
    RespectGrain = "RespectGrain"
    RespectNum = "RespectNum"
    RopeTerm = "RopeTerm"
    UPDATE = "UPDATE"
    knot = "knot"
    money_grain = "money_grain"
    parent_rope = "parent_rope"
    respect_grain = "respect_grain"
    sqlite_datatype = "sqlite_datatype"

    def __str__(self):
        return self.value
