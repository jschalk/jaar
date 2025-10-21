from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class BeliefTable(Base):
    __tablename__ = "belief"
    uid = Column(Integer, primary_key=True)
    max_tree_traverse = Column(Integer)
    credor_respect = Column(Float)
    debtor_respect = Column(Float)
    fund_pool = Column(Float)
    fund_grain = Column(Float)
    respect_grain = Column(Float)
    mana_grain = Column(Float)
    tally = Column(Integer)


class VoiceUnitTable(Base):
    __tablename__ = "voiceunit"
    uid = Column(Integer, primary_key=True)
    voice_name = Column(String)
    voice_cred_lumen = Column(Float)
    voice_debt_lumen = Column(Float)


class MemberShipTable(Base):
    __tablename__ = "membership"
    uid = Column(Integer, primary_key=True)
    group_title = Column(String)
    voice_name = Column(String)
    group_cred_lumen = Column(Float)
    group_debt_lumen = Column(Float)


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
    pledge = Column(Integer)
    stop_want = Column(Float)


class AwardUnitTable(Base):
    __tablename__ = "awardunit"
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
    active_requisite = Column(Integer)


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
    solo = Column(Integer)


class HealerUnitTable(Base):
    __tablename__ = "healerunit"
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
