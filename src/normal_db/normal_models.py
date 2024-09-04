from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class BudTable(Base):
    __tablename__ = "bud"
    uid = Column(Integer, primary_key=True)
    max_tree_traverse = Column(Integer)
    monetary_desc = Column(String)
    credor_respect = Column(Integer)
    debtor_respect = Column(Integer)
    fund_pool = Column(Float)
    fund_coin = Column(Float)
    bit = Column(Float)
    penny = Column(Float)
    tally = Column(Integer)


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
    credit_vote = Column(Integer)
    debtit_vote = Column(Integer)


class IdeaTable(Base):
    __tablename__ = "idea"
    uid = Column(Integer, primary_key=True)
    label = Column(String)
    parent_road = Column(String)
    addin = Column(Float)
    begin = Column(Float)
    close = Column(Float)
    denom = Column(Integer)
    gogo_want = Column(Float)
    numor = Column(Integer)
    problem_bool = Column(Integer)
    morph = Column(Integer)
    mass = Column(Integer)
    pledge = Column(Integer)
    stop_want = Column(Float)


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


class TeamlinkTable(Base):
    __tablename__ = "teamlink"
    uid = Column(Integer, primary_key=True)
    group_id = Column(String)
    road = Column(String)


class HealerHoldTable(Base):
    __tablename__ = "healerhold"
    uid = Column(Integer, primary_key=True)
    healer_id = Column(String)
    road = Column(String)


class FactTable(Base):
    __tablename__ = "fact"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    road = Column(String)
    fnigh = Column(Float)
    fopen = Column(Float)
    pick = Column(String)
