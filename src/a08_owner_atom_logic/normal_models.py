from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class OwnerTable(Base):
    __tablename__ = "owner"
    uid = Column(Integer, primary_key=True)
    max_tree_traverse = Column(Integer)
    credor_respect = Column(Float)
    debtor_respect = Column(Float)
    fund_pool = Column(Float)
    fund_iota = Column(Float)
    respect_bit = Column(Float)
    penny = Column(Float)
    tally = Column(Integer)


class AcctUnitTable(Base):
    __tablename__ = "acctunit"
    uid = Column(Integer, primary_key=True)
    acct_name = Column(String)
    acct_cred_points = Column(Float)
    acct_debt_points = Column(Float)


class MemberShipTable(Base):
    __tablename__ = "membership"
    uid = Column(Integer, primary_key=True)
    group_title = Column(String)
    acct_name = Column(String)
    group_cred_points = Column(Float)
    group_debt_points = Column(Float)


class ConceptTable(Base):
    __tablename__ = "concept"
    uid = Column(Integer, primary_key=True)
    concept_rope = Column(String)
    addin = Column(Float)
    begin = Column(Float)
    close = Column(Float)
    denom = Column(Integer)
    gogo_want = Column(Float)
    numor = Column(Integer)
    problem_bool = Column(Integer)
    morph = Column(Integer)
    mass = Column(Integer)
    task = Column(Integer)
    stop_want = Column(Float)


class AwardLinkTable(Base):
    __tablename__ = "awardlink"
    uid = Column(Integer, primary_key=True)
    awardee_title = Column(String)
    concept_rope = Column(String)
    give_force = Column(Float)
    take_force = Column(Float)


class ReasonTable(Base):
    __tablename__ = "reason"
    uid = Column(Integer, primary_key=True)
    rcontext = Column(String)
    concept_rope = Column(String)
    rconcept_active_requisite = Column(Integer)


class PremiseTable(Base):
    __tablename__ = "premise"
    uid = Column(Integer, primary_key=True)
    rcontext = Column(String)
    pstate = Column(String)
    concept_rope = Column(String)
    pdivisor = Column(Integer)
    pnigh = Column(Float)
    popen = Column(Float)


class LaborLinkTable(Base):
    __tablename__ = "laborlink"
    uid = Column(Integer, primary_key=True)
    labor_title = Column(String)
    concept_rope = Column(String)


class HealerLinkTable(Base):
    __tablename__ = "healerlink"
    uid = Column(Integer, primary_key=True)
    healer_name = Column(String)
    concept_rope = Column(String)


class FactTable(Base):
    __tablename__ = "fact"
    uid = Column(Integer, primary_key=True)
    fcontext = Column(String)
    concept_rope = Column(String)
    fnigh = Column(Float)
    fopen = Column(Float)
    fstate = Column(String)
