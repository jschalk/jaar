from enum import Enum


class Ch03Keywords(str, Enum):
    FirstLabel = "FirstLabel"
    FundGrain = "FundGrain"
    FundNum = "FundNum"
    GrainFloat = "GrainFloat"
    INSERT = "INSERT"
    KnotTerm = "KnotTerm"
    LabelTerm = "LabelTerm"
    MoneyUnit = "MoneyUnit"
    PennyNum = "PennyNum"
    RespectGrain = "RespectGrain"
    RespectNum = "RespectNum"
    RopeTerm = "RopeTerm"
    UPDATE = "UPDATE"
    fund_grain = "fund_grain"
    fund_pool = "fund_pool"
    knot = "knot"
    parent_rope = "parent_rope"
    penny = "penny"
    respect_grain = "respect_grain"
    sqlite_datatype = "sqlite_datatype"

    def __str__(self):
        return self.value
