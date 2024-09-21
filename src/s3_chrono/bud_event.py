from src.s1_road.road import FiscalID, OwnerID
from src.s2_bud.bud import BudUnit
from src.s3_chrono.chrono import TimeLinePoint
from dataclasses import dataclass


@dataclass
class OwnerBudEvent:
    fiscal_id: FiscalID = None
    owner_id: OwnerID = None
    timestamp: TimeLinePoint = None
    _bud: BudUnit = None
    _money_magnitude: int = None
    _money_desc: str = None


def ownerbudevent_shop(fiscal_id: FiscalID, owner_id: OwnerID) -> OwnerBudEvent:
    return OwnerBudEvent(fiscal_id=fiscal_id, owner_id=owner_id)


@dataclass
class OwnerBudEvents:
    fiscal_id: FiscalID = None
    owner_id: OwnerID = None
    events: dict[TimeLinePoint:OwnerBudEvent] = None
    _sum_money_magnitude: int = None
    _sum_acct_outlays: int = None
    _timestamp_min: TimeLinePoint = None
    _timestamp_max: TimeLinePoint = None


def ownerbudevents_shop(fiscal_id: FiscalID, owner_id: OwnerID) -> OwnerBudEvents:
    return OwnerBudEvents(
        fiscal_id=fiscal_id, owner_id=owner_id, events={}, _sum_acct_outlays={}
    )
