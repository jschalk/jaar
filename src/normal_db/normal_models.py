from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class BudTable(Base):
    __tablename__ = "bud"
    uid = Column(Integer, primary_key=True)
    _max_tree_traverse = Column(Integer)
    _monetary_desc = Column(String)
    _credor_respect = Column(Integer)
    _debtor_respect = Column(Integer)
    _fund_pool = Column(Float)
    _fund_coin = Column(Float)
    _bit = Column(Float)
    _penny = Column(Float)
    _tally = Column(Integer)


class AcctUnitTable(Base):
    __tablename__ = "acctunit"

    uid = Column(Integer, primary_key=True)
    acct_id = Column(String)
    credit_score = Column(Integer)
    debtit_score = Column(Integer)


# class GroupTable(Base):
#     __tablename__ = "groupbox"

#     uid = Column(Integer, primary_key=True)
#     group_id = Column(String)


class MemberShipTable(Base):
    __tablename__ = "membership"
    uid = Column(Integer, primary_key=True)
    group_id = Column(String)
    acct_id = Column(String)
    credit_weight = Column(Integer)
    debtit_weight = Column(Integer)


class IdeaTable(Base):
    __tablename__ = "idea"
    uid = Column(Integer, primary_key=True)
    label = Column(String)
    parent_road = Column(String)
    _addin = Column(Float)
    _begin = Column(Float)
    _close = Column(Float)
    _denom = Column(Integer)
    _numeric_road = Column(String)
    _numor = Column(Integer)
    _problem_bool = Column(Integer)
    _range_source_road = Column(String)
    _reest = Column(Integer)
    _mass = Column(Integer)
    pledge = Column(Integer)


class AwardLinkTable(Base):
    __tablename__ = "awardlink"
    uid = Column(Integer, primary_key=True)
    group_id = Column(String)
    road = Column(String)
    give_force = Column(Float)
    take_force = Column(Float)


class ReasonTable(Base):
    __tablename__ = "reason"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    road = Column(String)
    base_idea_active_requisite = Column(Integer)


class PremiseTable(Base):
    __tablename__ = "premise"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    need = Column(String)
    road = Column(String)
    divisor = Column(Integer)
    nigh = Column(Float)
    open = Column(Float)


class groupholdTable(Base):
    __tablename__ = "grouphold"
    uid = Column(Integer, primary_key=True)
    group_id = Column(String)
    road = Column(String)


class HealerHoldTable(Base):
    __tablename__ = "healerhold"
    uid = Column(Integer, primary_key=True)
    group_id = Column(String)
    road = Column(String)


class FactTable(Base):
    __tablename__ = "fact"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    road = Column(String)
    nigh = Column(Float)
    open = Column(Float)
    pick = Column(String)
