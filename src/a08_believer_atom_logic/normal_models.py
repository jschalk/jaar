from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class BelieverTable(Base):
    __tablename__ = "believer"
    uid = Column(Integer, primary_key=True)
    max_tree_traverse = Column(Integer)
    credor_respect = Column(Float)
    debtor_respect = Column(Float)
    fund_pool = Column(Float)
    fund_iota = Column(Float)
    respect_bit = Column(Float)
    penny = Column(Float)
    tally = Column(Integer)


class PartnerUnitTable(Base):
    __tablename__ = "partnerunit"
    uid = Column(Integer, primary_key=True)
    partner_name = Column(String)
    partner_cred_points = Column(Float)
    partner_debt_points = Column(Float)


class MemberShipTable(Base):
    __tablename__ = "membership"
    uid = Column(Integer, primary_key=True)
    group_title = Column(String)
    partner_name = Column(String)
    group_cred_points = Column(Float)
    group_debt_points = Column(Float)


class PlanTable(Base):
    __tablename__ = "plan"
    uid = Column(Integer, primary_key=True)
    plan_rope = Column(String)
    addin = Column(Float)
    begin = Column(Float)
    close = Column(Float)
    denom = Column(Integer)
    gogo_want = Column(Float)
    numor = Column(Integer)
    problem_bool = Column(Integer)
    morph = Column(Integer)
    star = Column(Integer)
    task = Column(Integer)
    stop_want = Column(Float)


class AwardLinkTable(Base):
    __tablename__ = "awardlink"
    uid = Column(Integer, primary_key=True)
    awardee_title = Column(String)
    plan_rope = Column(String)
    give_force = Column(Float)
    take_force = Column(Float)


class ReasonTable(Base):
    __tablename__ = "reason"
    uid = Column(Integer, primary_key=True)
    reason_context = Column(String)
    plan_rope = Column(String)
    reason_active_requisite = Column(Integer)


class CaseTable(Base):
    __tablename__ = "case"
    uid = Column(Integer, primary_key=True)
    reason_context = Column(String)
    reason_state = Column(String)
    plan_rope = Column(String)
    reason_divisor = Column(Integer)
    reason_upper = Column(Float)
    reason_lower = Column(Float)


class LaborLinkTable(Base):
    __tablename__ = "partyunit"
    uid = Column(Integer, primary_key=True)
    party_title = Column(String)
    plan_rope = Column(String)


class HealerLinkTable(Base):
    __tablename__ = "healerlink"
    uid = Column(Integer, primary_key=True)
    healer_name = Column(String)
    plan_rope = Column(String)


class FactTable(Base):
    __tablename__ = "fact"
    uid = Column(Integer, primary_key=True)
    fact_context = Column(String)
    plan_rope = Column(String)
    fact_upper = Column(Float)
    fact_lower = Column(Float)
    fact_state = Column(String)
