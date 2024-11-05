from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


# class br00000Table(Base):__tablename__="br00000"
# class br00001Table(Base):__tablename__="br00001"
# class br00002Table(Base):__tablename__="br00002"
# class br00003Table(Base):__tablename__="br00003"
# class br00004Table(Base):__tablename__="br00004"
# class br00005Table(Base):__tablename__="br00005"
# class br00011Table(Base):__tablename__="br00011"
# class br00012Table(Base):__tablename__="br00012"
# class br00013Table(Base):__tablename__="br00013"
# class br00019Table(Base):__tablename__="br00019"
# class br00020Table(Base):__tablename__="br00020"
# class br00021Table(Base):__tablename__="br00021"
# class br00022Table(Base):__tablename__="br00022"
# class br00023Table(Base):__tablename__="br00023"
# class br00024Table(Base):__tablename__="br00024"
# class br00025Table(Base):__tablename__="br00025"
# class br00026Table(Base):__tablename__="br00026"
# class br00027Table(Base):__tablename__="br00027"
# class br00028Table(Base):__tablename__="br00028"
# class br00029Table(Base):__tablename__="br00029"
# class br00036Table(Base):__tablename__="br00036"
# class br00040Table(Base):__tablename__="br00040"
# class br00041Table(Base):__tablename__="br00041"


class br00000Table(Base):
    __tablename__ = "br00000"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    c400_number = Column(Integer)
    current_time = Column(Integer)
    fiscal_id = Column(String)
    fund_coin = Column(Float)
    monthday_distortion = Column(Integer)
    penny = Column(Float)
    respect_bit = Column(Float)
    road_delimiter = Column(String)
    timeline_label = Column(String)
    yr1_jan1_offset = Column(Integer)


class br00001Table(Base):
    __tablename__ = "br00001"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    fiscal_id = Column(String)
    owner_id = Column(String)
    quota = Column(Float)
    time_id = Column(Integer)


class br00002Table(Base):
    __tablename__ = "br00002"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    amount = Column(Float)
    fiscal_id = Column(String)
    owner_id = Column(String)
    time_id = Column(Integer)


class br00003Table(Base):
    __tablename__ = "br00003"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    cumlative_minute = Column(Integer)
    fiscal_id = Column(String)
    hour_label = Column(String)


class br00004Table(Base):
    __tablename__ = "br00004"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    cumlative_day = Column(Integer)
    fiscal_id = Column(String)
    month_label = Column(String)


class br00005Table(Base):
    __tablename__ = "br00005"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    weekday_order = Column(Integer)
    fiscal_id = Column(String)
    weekday_label = Column(String)


class br00011Table(Base):
    __tablename__ = "br00011"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    fiscal_id = Column(String)
    owner_id = Column(String)


class br00012Table(Base):
    __tablename__ = "br00012"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    group_id = Column(String)
    fiscal_id = Column(String)
    owner_id = Column(String)


class br00013Table(Base):
    __tablename__ = "br00013"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    fiscal_id = Column(String)
    label = Column(String)
    mass = Column(Float)
    owner_id = Column(String)
    parent_road = Column(String)
    pledge = Column(Integer)


class br00019Table(Base):
    __tablename__ = "br00019"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    addin = Column(Float)
    begin = Column(Float)
    close = Column(Float)
    denom = Column(Float)
    fiscal_id = Column(String)
    gogo_want = Column(Float)
    label = Column(String)
    morph = Column(Integer)
    numor = Column(Float)
    owner_id = Column(String)
    parent_road = Column(String)
    stop_want = Column(Float)


class br00020Table(Base):
    __tablename__ = "br00020"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    credit_vote = Column(Float)
    debtit_vote = Column(Float)
    fiscal_id = Column(String)
    group_id = Column(String)
    owner_id = Column(String)


class br00021Table(Base):
    __tablename__ = "br00021"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    credit_belief = Column(Float)
    debtit_belief = Column(Float)
    fiscal_id = Column(String)
    owner_id = Column(String)


class br00022Table(Base):
    __tablename__ = "br00022"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    awardee_id = Column(String)
    fiscal_id = Column(String)
    give_force = Column(Float)
    owner_id = Column(String)
    road = Column(String)
    take_force = Column(Float)


class br00023Table(Base):
    __tablename__ = "br00023"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    base = Column(String)
    fiscal_id = Column(String)
    fopen = Column(Float)
    fnigh = Column(Float)
    owner_id = Column(String)
    pick = Column(String)
    road = Column(String)


class br00024Table(Base):
    __tablename__ = "br00024"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    fiscal_id = Column(String)
    owner_id = Column(String)
    road = Column(String)
    team_id = Column(String)


class br00025Table(Base):
    __tablename__ = "br00025"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    fiscal_id = Column(String)
    owner_id = Column(String)
    road = Column(String)
    healer_id = Column(String)


class br00026Table(Base):
    __tablename__ = "br00026"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    base = Column(String)
    divisor = Column(Float)
    fiscal_id = Column(String)
    need = Column(String)
    nigh = Column(Float)
    open = Column(Float)
    owner_id = Column(String)
    road = Column(String)


class br00027Table(Base):
    __tablename__ = "br00027"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    base = Column(String)
    base_item_active_requisite = Column(String)
    fiscal_id = Column(String)
    owner_id = Column(String)
    road = Column(String)


class br00028Table(Base):
    __tablename__ = "br00028"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    addin = Column(Float)
    begin = Column(Float)
    close = Column(Float)
    denom = Column(Float)
    fiscal_id = Column(String)
    gogo_want = Column(Float)
    label = Column(String)
    mass = Column(Float)
    morph = Column(Integer)
    numor = Column(Float)
    owner_id = Column(String)
    parent_road = Column(String)
    pledge = Column(Integer)
    problem_bool = Column(Integer)
    stop_want = Column(Float)


class br00029Table(Base):
    __tablename__ = "br00029"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    credor_respect = Column(Float)
    debtor_respect = Column(Float)
    fiscal_id = Column(String)
    fund_coin = Column(Float)
    fund_pool = Column(Float)
    max_tree_traverse = Column(Integer)
    owner_id = Column(String)
    penny = Column(Float)
    purview_time_id = Column(Integer)
    respect_bit = Column(Float)
    tally = Column(Float)


class br00036Table(Base):
    __tablename__ = "br00036"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    fiscal_id = Column(String)
    healer_id = Column(String)
    label = Column(String)
    owner_id = Column(String)
    parent_road = Column(String)
    problem_bool = Column(Integer)


class br00040Table(Base):
    __tablename__ = "br00040"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    inx_road_delimiter = Column(String)
    inx_word = Column(String)
    otx_road_delimiter = Column(String)
    otx_word = Column(String)
    unknown_word = Column(String)


class br00041Table(Base):
    __tablename__ = "br00041"
    face_id = Column(String, primary_key=True)
    eon_id = Column(Integer, primary_key=True)
    inx_label = Column(String)
    inx_road_delimiter = Column(String)
    otx_label = Column(String)
    otx_road_delimiter = Column(String)
    unknown_word = Column(String)
