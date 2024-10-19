from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class BudTable(Base):
    __tablename__ = "bud"
    uid = Column(Integer, primary_key=True)
    max_tree_traverse = Column(Integer)
    credor_respect = Column(Integer)
    debtor_respect = Column(Integer)
    fund_pool = Column(Float)
    fund_coin = Column(Float)
    respect_bit = Column(Float)
    penny = Column(Float)
    purview_timestamp = Column(Integer)
    tally = Column(Integer)


class AcctUnitTable(Base):
    __tablename__ = "acctunit"

    uid = Column(Integer, primary_key=True)
    acct_id = Column(String)
    credit_belief = Column(Integer)
    debtit_belief = Column(Integer)


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


class ItemTable(Base):
    __tablename__ = "item"
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
    awardee_id = Column(String)
    road = Column(String)
    give_force = Column(Float)
    take_force = Column(Float)


class ReasonTable(Base):
    __tablename__ = "reason"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    road = Column(String)
    base_item_active_requisite = Column(Integer)


class PremiseTable(Base):
    __tablename__ = "premise"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    need = Column(String)
    road = Column(String)
    divisor = Column(Integer)
    nigh = Column(Float)
    open = Column(Float)


class TeamLinkTable(Base):
    __tablename__ = "teamlink"
    uid = Column(Integer, primary_key=True)
    team_id = Column(String)
    road = Column(String)


class HealerLinkTable(Base):
    __tablename__ = "healerlink"
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
