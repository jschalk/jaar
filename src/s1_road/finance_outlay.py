from src.s0_instrument.python_tool import get_empty_dict_if_none
from src.s1_road.finance import FundNum, TimeLinePoint
from src.s1_road.road import AcctID
from src.s1_road.road import OwnerID
from dataclasses import dataclass


@dataclass
class OutlayEvent:
    timestamp: TimeLinePoint = None
    money_magnitude: int = None
    _net_outlays: dict[AcctID, FundNum] = None
    _tender_desc: str = None

    def get_array(self) -> list[int]:
        return [self.timestamp, self.money_magnitude]

    def get_dict(self) -> dict[str,]:
        return {"timestamp": self.timestamp, "money_magnitude": self.money_magnitude}


def outlayevent_shop(
    x_timestamp: TimeLinePoint,
    x_money_magnitude: int,
    net_outlays: dict[AcctID, FundNum] = None,
) -> OutlayEvent:
    return OutlayEvent(
        x_timestamp,
        money_magnitude=x_money_magnitude,
        _net_outlays=get_empty_dict_if_none(net_outlays),
    )


@dataclass
class OutlayLog:
    owner_id: OwnerID = None
    events: dict[TimeLinePoint:OutlayEvent] = None
    _sum_money_magnitude: int = None
    _sum_acct_outlays: int = None
    _timestamp_min: TimeLinePoint = None
    _timestamp_max: TimeLinePoint = None

    def set_event(self, x_event: OutlayEvent):
        self.events[x_event.timestamp] = x_event

    def add_event(self, x_timestamp: TimeLinePoint, x_money_magnitude: int):
        self.set_event(outlayevent_shop(x_timestamp, x_money_magnitude))

    def event_exists(self, x_timestamp: TimeLinePoint) -> bool:
        return self.events.get(x_timestamp) != None

    def get_event(self, x_timestamp: TimeLinePoint) -> OutlayEvent:
        return self.events.get(x_timestamp)

    def del_event(self, x_timestamp: TimeLinePoint):
        self.events.pop(x_timestamp)

    def get_2d_array(self) -> list[list]:
        return [
            [self.owner_id, x_event.timestamp, x_event.money_magnitude]
            for x_event in self.events.values()
        ]

    def get_headers(self) -> list:
        return ["owner_id", "timestamp", "money_magnitude"]

    def get_dict(self) -> dict:
        return {"owner_id": self.owner_id, "events": self._get_events_dict()}

    def _get_events_dict(self) -> dict:
        return {
            x_event.timestamp: x_event.get_dict() for x_event in self.events.values()
        }


def outlaylog_shop(owner_id: OwnerID) -> OutlayLog:
    return OutlayLog(owner_id=owner_id, events={}, _sum_acct_outlays={})


def get_outlayevent_from_dict(x_dict: dict) -> OutlayEvent:
    x_timestamp = x_dict.get("timestamp")
    x_money_magnitude = x_dict.get("money_magnitude")
    return outlayevent_shop(x_timestamp, x_money_magnitude)


def get_outlaylog_from_dict(x_dict: dict) -> OutlayLog:
    x_owner_id = x_dict.get("owner_id")
    x_outlaylog = outlaylog_shop(x_owner_id)
    x_outlaylog.events = get_events_from_dict(x_dict.get("events"))
    return x_outlaylog


def get_events_from_dict(events_dict: dict) -> dict[TimeLinePoint:OutlayEvent]:
    x_dict = {}
    for x_event in events_dict.values():
        x_timestamp = x_event.get("timestamp")
        x_money_magnitude = x_event.get("money_magnitude")
        x_dict[x_timestamp] = outlayevent_shop(x_timestamp, x_money_magnitude)
    return x_dict
