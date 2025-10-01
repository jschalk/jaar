from enum import Enum


class Ch03Keywords(str, Enum):
    BitNum = "BitNum"
    FundIota = "FundIota"
    FundNum = "FundNum"
    GrainFloat = "GrainFloat"
    INSERT = "INSERT"
    KnotTerm = "KnotTerm"
    LabelTerm = "LabelTerm"
    MoneyUnit = "MoneyUnit"
    NameTerm = "NameTerm"
    NexusLabel = "NexusLabel"
    PennyNum = "PennyNum"
    RespectNum = "RespectNum"
    RopeTerm = "RopeTerm"
    TitleTerm = "TitleTerm"
    UPDATE = "UPDATE"
    fund_iota = "fund_iota"
    fund_pool = "fund_pool"
    knot = "knot"
    magnitude = "magnitude"
    parent_rope = "parent_rope"
    penny = "penny"
    sqlite_datatype = "sqlite_datatype"

    def __str__(self):
        return self.value
