from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class BudTable(Base):
    __tablename__ = "bud"
    uid = Column(Integer, primary_key=True)
    max_tree_traverse = Column(Integer)
    credor_respect = Column(Float)
    debtor_respect = Column(Float)
    fund_pool = Column(Float)
    fund_coin = Column(Float)
    respect_bit = Column(Float)
    penny = Column(Float)
    tally = Column(Integer)


class AcctUnitTable(Base):
    __tablename__ = "acctunit"
    uid = Column(Integer, primary_key=True)
    acct_name = Column(String)
    credit_belief = Column(Float)
    debtit_belief = Column(Float)


class MemberShipTable(Base):
    __tablename__ = "membership"
    uid = Column(Integer, primary_key=True)
    group_label = Column(String)
    acct_name = Column(String)
    credit_vote = Column(Float)
    debtit_vote = Column(Float)


class IdeaTable(Base):
    __tablename__ = "idea"
    uid = Column(Integer, primary_key=True)
    idea_way = Column(String)
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
    awardee_label = Column(String)
    idea_way = Column(String)
    give_force = Column(Float)
    take_force = Column(Float)


class ReasonTable(Base):
    __tablename__ = "reason"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    idea_way = Column(String)
    base_idea_active_requisite = Column(Integer)


class PremiseTable(Base):
    __tablename__ = "premise"
    uid = Column(Integer, primary_key=True)
    base = Column(String)
    need = Column(String)
    idea_way = Column(String)
    divisor = Column(Integer)
    nigh = Column(Float)
    open = Column(Float)


class TeamLinkTable(Base):
    __tablename__ = "teamlink"
    uid = Column(Integer, primary_key=True)
    team_label = Column(String)
    idea_way = Column(String)


class HealerLinkTable(Base):
    __tablename__ = "healerlink"
    uid = Column(Integer, primary_key=True)
    healer_name = Column(String)
    idea_way = Column(String)


class FactTable(Base):
    __tablename__ = "fact"
    uid = Column(Integer, primary_key=True)
    fbase = Column(String)
    idea_way = Column(String)
    fnigh = Column(Float)
    fopen = Column(Float)
    fneed = Column(String)
