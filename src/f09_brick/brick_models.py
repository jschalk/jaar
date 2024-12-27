from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class br00000AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    c400_number = Column(Integer)
    current_time = Column(Integer)
    deal_id = Column(String)
    fund_coin = Column(Float)
    monthday_distortion = Column(Integer)
    penny = Column(Float)
    respect_bit = Column(Float)
    bridge = Column(String)
    timeline_idea = Column(String)
    yr1_jan1_offset = Column(Integer)


class br00001AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    deal_id = Column(String)
    owner_id = Column(String)
    quota = Column(Float)
    time_id = Column(Integer)


class br00002AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    amount = Column(Float)
    deal_id = Column(String)
    owner_id = Column(String)
    time_id = Column(Integer)


class br00003AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    cumlative_minute = Column(Integer)
    deal_id = Column(String)
    hour_idea = Column(String)


class br00004AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    cumlative_day = Column(Integer)
    deal_id = Column(String)
    month_idea = Column(String)


class br00005AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    weekday_order = Column(Integer)
    deal_id = Column(String)
    weekday_label = Column(String)


class br00011AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    deal_id = Column(String)
    owner_id = Column(String)


class br00012AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    group_id = Column(String)
    deal_id = Column(String)
    owner_id = Column(String)


class br00013AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    deal_id = Column(String)
    lx = Column(String)
    mass = Column(Float)
    owner_id = Column(String)
    parent_road = Column(String)
    pledge = Column(Integer)


class br00019AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    addin = Column(Float)
    begin = Column(Float)
    close = Column(Float)
    denom = Column(Float)
    deal_id = Column(String)
    gogo_want = Column(Float)
    lx = Column(String)
    morph = Column(Integer)
    numor = Column(Float)
    owner_id = Column(String)
    parent_road = Column(String)
    stop_want = Column(Float)


class br00020AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    credit_vote = Column(Float)
    debtit_vote = Column(Float)
    deal_id = Column(String)
    group_id = Column(String)
    owner_id = Column(String)


class br00021AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    credit_belief = Column(Float)
    debtit_belief = Column(Float)
    deal_id = Column(String)
    owner_id = Column(String)


class br00022AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    awardee_id = Column(String)
    deal_id = Column(String)
    give_force = Column(Float)
    owner_id = Column(String)
    road = Column(String)
    take_force = Column(Float)


class br00023AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    base = Column(String)
    deal_id = Column(String)
    fopen = Column(Float)
    fnigh = Column(Float)
    owner_id = Column(String)
    pick = Column(String)
    road = Column(String)


class br00024AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    deal_id = Column(String)
    owner_id = Column(String)
    road = Column(String)
    team_id = Column(String)


class br00025AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    deal_id = Column(String)
    owner_id = Column(String)
    road = Column(String)
    healer_id = Column(String)


class br00026AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    base = Column(String)
    divisor = Column(Float)
    deal_id = Column(String)
    need = Column(String)
    nigh = Column(Float)
    open = Column(Float)
    owner_id = Column(String)
    road = Column(String)


class br00027AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    base = Column(String)
    base_item_active_requisite = Column(String)
    deal_id = Column(String)
    owner_id = Column(String)
    road = Column(String)


class br00028AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    addin = Column(Float)
    begin = Column(Float)
    close = Column(Float)
    denom = Column(Float)
    deal_id = Column(String)
    gogo_want = Column(Float)
    lx = Column(String)
    mass = Column(Float)
    morph = Column(Integer)
    numor = Column(Float)
    owner_id = Column(String)
    parent_road = Column(String)
    pledge = Column(Integer)
    problem_bool = Column(Integer)
    stop_want = Column(Float)


class br00029AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    credor_respect = Column(Float)
    debtor_respect = Column(Float)
    deal_id = Column(String)
    fund_coin = Column(Float)
    fund_pool = Column(Float)
    max_tree_traverse = Column(Integer)
    owner_id = Column(String)
    penny = Column(Float)
    purview_time_id = Column(Integer)
    respect_bit = Column(Float)
    tally = Column(Float)


class br00036AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    deal_id = Column(String)
    healer_id = Column(String)
    lx = Column(String)
    owner_id = Column(String)
    parent_road = Column(String)
    problem_bool = Column(Integer)


class br00042AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    inx_group_id = Column(String)
    inx_bridge = Column(String)
    otx_group_id = Column(String)
    otx_bridge = Column(String)
    unknown_word = Column(String)


class br00043AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    inx_acct_id = Column(String)
    inx_bridge = Column(String)
    otx_acct_id = Column(String)
    otx_bridge = Column(String)
    unknown_word = Column(String)


class br00044AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    inx_idea = Column(String)
    inx_bridge = Column(String)
    otx_idea = Column(String)
    otx_bridge = Column(String)
    unknown_word = Column(String)


class br00045AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    inx_road = Column(String)
    inx_bridge = Column(String)
    otx_road = Column(String)
    otx_bridge = Column(String)
    unknown_word = Column(String)


class br00113AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    deal_id = Column(String)
    inx_acct_id = Column(String)
    otx_acct_id = Column(String)
    owner_id = Column(String)


class br00115AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    deal_id = Column(String)
    inx_group_id = Column(String)
    otx_group_id = Column(String)
    owner_id = Column(String)


class br00116AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    deal_id = Column(String)
    inx_idea = Column(String)
    otx_idea = Column(String)
    owner_id = Column(String)


class br00117AbstractTable(Base):
    __abstract__ = True
    face_id = Column(String, primary_key=True)
    event_id = Column(Integer, primary_key=True)
    acct_id = Column(String)
    deal_id = Column(String)
    inx_road = Column(String)
    otx_road = Column(String)
    owner_id = Column(String)


class br00000HoldTable(br00000AbstractTable):
    __tablename__ = "br00000_hold"


class br00001HoldTable(br00001AbstractTable):
    __tablename__ = "br00001_hold"


class br00002HoldTable(br00002AbstractTable):
    __tablename__ = "br00002_hold"


class br00003HoldTable(br00003AbstractTable):
    __tablename__ = "br00003_hold"


class br00004HoldTable(br00004AbstractTable):
    __tablename__ = "br00004_hold"


class br00005HoldTable(br00005AbstractTable):
    __tablename__ = "br00005_hold"


class br00011HoldTable(br00011AbstractTable):
    __tablename__ = "br00011_hold"


class br00012HoldTable(br00012AbstractTable):
    __tablename__ = "br00012_hold"


class br00013HoldTable(br00013AbstractTable):
    __tablename__ = "br00013_hold"


class br00019HoldTable(br00019AbstractTable):
    __tablename__ = "br00019_hold"


class br00020HoldTable(br00020AbstractTable):
    __tablename__ = "br00020_hold"


class br00021HoldTable(br00021AbstractTable):
    __tablename__ = "br00021_hold"


class br00022HoldTable(br00022AbstractTable):
    __tablename__ = "br00022_hold"


class br00023HoldTable(br00023AbstractTable):
    __tablename__ = "br00023_hold"


class br00024HoldTable(br00024AbstractTable):
    __tablename__ = "br00024_hold"


class br00025HoldTable(br00025AbstractTable):
    __tablename__ = "br00025_hold"


class br00026HoldTable(br00026AbstractTable):
    __tablename__ = "br00026_hold"


class br00027HoldTable(br00027AbstractTable):
    __tablename__ = "br00027_hold"


class br00028HoldTable(br00028AbstractTable):
    __tablename__ = "br00028_hold"


class br00029HoldTable(br00029AbstractTable):
    __tablename__ = "br00029_hold"


class br00036HoldTable(br00036AbstractTable):
    __tablename__ = "br00036_hold"


class br00042HoldTable(br00042AbstractTable):
    __tablename__ = "br00042_hold"


class br00043HoldTable(br00043AbstractTable):
    __tablename__ = "br00043_hold"


class br00044HoldTable(br00044AbstractTable):
    __tablename__ = "br00044_hold"


class br00045HoldTable(br00045AbstractTable):
    __tablename__ = "br00045_hold"


class br00113HoldTable(br00113AbstractTable):
    __tablename__ = "br00113_hold"


class br00115HoldTable(br00115AbstractTable):
    __tablename__ = "br00115_hold"


class br00116HoldTable(br00116AbstractTable):
    __tablename__ = "br00116_hold"


class br00117HoldTable(br00117AbstractTable):
    __tablename__ = "br00117_hold"


class br00000StageTable(br00000AbstractTable):
    __tablename__ = "br00000_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00001StageTable(br00001AbstractTable):
    __tablename__ = "br00001_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00002StageTable(br00002AbstractTable):
    __tablename__ = "br00002_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00003StageTable(br00003AbstractTable):
    __tablename__ = "br00003_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00004StageTable(br00004AbstractTable):
    __tablename__ = "br00004_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00005StageTable(br00005AbstractTable):
    __tablename__ = "br00005_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00011StageTable(br00011AbstractTable):
    __tablename__ = "br00011_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00012StageTable(br00012AbstractTable):
    __tablename__ = "br00012_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00013StageTable(br00013AbstractTable):
    __tablename__ = "br00013_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00019StageTable(br00019AbstractTable):
    __tablename__ = "br00019_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00020StageTable(br00020AbstractTable):
    __tablename__ = "br00020_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00021StageTable(br00021AbstractTable):
    __tablename__ = "br00021_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00022StageTable(br00022AbstractTable):
    __tablename__ = "br00022_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00023StageTable(br00023AbstractTable):
    __tablename__ = "br00023_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00024StageTable(br00024AbstractTable):
    __tablename__ = "br00024_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00025StageTable(br00025AbstractTable):
    __tablename__ = "br00025_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00026StageTable(br00026AbstractTable):
    __tablename__ = "br00026_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00027StageTable(br00027AbstractTable):
    __tablename__ = "br00027_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00028StageTable(br00028AbstractTable):
    __tablename__ = "br00028_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00029StageTable(br00029AbstractTable):
    __tablename__ = "br00029_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00036StageTable(br00036AbstractTable):
    __tablename__ = "br00036_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00042StageTable(br00042AbstractTable):
    __tablename__ = "br00042_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00043StageTable(br00043AbstractTable):
    __tablename__ = "br00043_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00044StageTable(br00044AbstractTable):
    __tablename__ = "br00044_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00045StageTable(br00045AbstractTable):
    __tablename__ = "br00045_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00113StageTable(br00113AbstractTable):
    __tablename__ = "br00113_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00115StageTable(br00115AbstractTable):
    __tablename__ = "br00115_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00116StageTable(br00116AbstractTable):
    __tablename__ = "br00116_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


class br00117StageTable(br00117AbstractTable):
    __tablename__ = "br00117_stage"
    src_type = Column(String)
    src_path = Column(String)
    src_sheet = Column(String)


def get_brick_holdtables() -> dict[str, DeclarativeBase]:
    return {
        "br00000": br00000HoldTable,
        "br00001": br00001HoldTable,
        "br00002": br00002HoldTable,
        "br00003": br00003HoldTable,
        "br00004": br00004HoldTable,
        "br00005": br00005HoldTable,
        "br00011": br00011HoldTable,
        "br00012": br00012HoldTable,
        "br00013": br00013HoldTable,
        "br00019": br00019HoldTable,
        "br00020": br00020HoldTable,
        "br00021": br00021HoldTable,
        "br00022": br00022HoldTable,
        "br00023": br00023HoldTable,
        "br00024": br00024HoldTable,
        "br00025": br00025HoldTable,
        "br00026": br00026HoldTable,
        "br00027": br00027HoldTable,
        "br00028": br00028HoldTable,
        "br00029": br00029HoldTable,
        "br00036": br00036HoldTable,
        "br00042": br00042HoldTable,
        "br00043": br00043HoldTable,
        "br00044": br00044HoldTable,
        "br00045": br00045HoldTable,
        "br00113": br00113HoldTable,
        "br00115": br00115HoldTable,
        "br00116": br00116HoldTable,
        "br00117": br00117HoldTable,
    }


def get_brick_stagetables() -> dict[str, DeclarativeBase]:
    return {
        "br00000": br00000StageTable,
        "br00001": br00001StageTable,
        "br00002": br00002StageTable,
        "br00003": br00003StageTable,
        "br00004": br00004StageTable,
        "br00005": br00005StageTable,
        "br00011": br00011StageTable,
        "br00012": br00012StageTable,
        "br00013": br00013StageTable,
        "br00019": br00019StageTable,
        "br00020": br00020StageTable,
        "br00021": br00021StageTable,
        "br00022": br00022StageTable,
        "br00023": br00023StageTable,
        "br00024": br00024StageTable,
        "br00025": br00025StageTable,
        "br00026": br00026StageTable,
        "br00027": br00027StageTable,
        "br00028": br00028StageTable,
        "br00029": br00029StageTable,
        "br00036": br00036StageTable,
        "br00042": br00042StageTable,
        "br00043": br00043StageTable,
        "br00044": br00044StageTable,
        "br00045": br00045StageTable,
        "br00113": br00113StageTable,
        "br00115": br00115StageTable,
        "br00116": br00116StageTable,
        "br00117": br00117StageTable,
    }
