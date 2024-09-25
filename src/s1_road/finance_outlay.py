from src.s0_instrument.python_tool import get_empty_dict_if_none
from src.s1_road.finance import FundNum, TimeLinePoint
from src.s1_road.road import AcctID
from src.s1_road.road import OwnerID
from dataclasses import dataclass


@dataclass
class OutlayEvent:
    timestamp: TimeLinePoint = None
    _magnitude: FundNum = None
    _net_outlays: dict[AcctID, FundNum] = None
    _tender_desc: str = None

    def set_net_outlay(self, x_acct_id: AcctID, net_outlay: FundNum):
        self._net_outlays[x_acct_id] = net_outlay

    def net_outlay_exists(self, x_acct_id: AcctID) -> bool:
        return self._net_outlays.get(x_acct_id) != None

    def get_net_outlay(self, x_acct_id: AcctID) -> FundNum:
        return self._net_outlays.get(x_acct_id)

    def del_net_outlay(self, x_acct_id: AcctID):
        self._net_outlays.pop(x_acct_id)

    def get_array(self) -> list[int]:
        return [self.timestamp, self._magnitude]

    def get_dict(self) -> dict[str,]:
        x_dict = {"timestamp": self.timestamp, "magnitude": self._magnitude}
        if self._net_outlays:
            x_dict["net_outlays"] = self._net_outlays
        return x_dict


def outlayevent_shop(
    x_timestamp: TimeLinePoint,
    x_magnitude: FundNum,
    net_outlays: dict[AcctID, FundNum] = None,
) -> OutlayEvent:
    return OutlayEvent(
        x_timestamp,
        _magnitude=x_magnitude,
        _net_outlays=get_empty_dict_if_none(net_outlays),
    )


@dataclass
class OutlayLog:
    owner_id: OwnerID = None
    events: dict[TimeLinePoint:OutlayEvent] = None
    _sum_outlayevent_magnitude: FundNum = None
    _sum_acct_outlays: int = None
    _timestamp_min: TimeLinePoint = None
    _timestamp_max: TimeLinePoint = None

    def set_event(self, x_event: OutlayEvent):
        self.events[x_event.timestamp] = x_event

    def add_event(self, x_timestamp: TimeLinePoint, x_magnitude: int):
        self.set_event(outlayevent_shop(x_timestamp, x_magnitude))

    def event_exists(self, x_timestamp: TimeLinePoint) -> bool:
        return self.events.get(x_timestamp) != None

    def get_event(self, x_timestamp: TimeLinePoint) -> OutlayEvent:
        return self.events.get(x_timestamp)

    def del_event(self, x_timestamp: TimeLinePoint):
        self.events.pop(x_timestamp)

    def get_2d_array(self) -> list[list]:
        return [
            [self.owner_id, x_event.timestamp, x_event._magnitude]
            for x_event in self.events.values()
        ]

    def get_headers(self) -> list:
        return ["owner_id", "timestamp", "magnitude"]

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
    x_magnitude = x_dict.get("magnitude")
    x_net_outlays = x_dict.get("net_outlays")
    return outlayevent_shop(x_timestamp, x_magnitude, x_net_outlays)


def get_outlaylog_from_dict(x_dict: dict) -> OutlayLog:
    x_owner_id = x_dict.get("owner_id")
    x_outlaylog = outlaylog_shop(x_owner_id)
    x_outlaylog.events = get_events_from_dict(x_dict.get("events"))
    return x_outlaylog


def get_events_from_dict(events_dict: dict) -> dict[TimeLinePoint:OutlayEvent]:
    x_dict = {}
    for x_event_dict in events_dict.values():
        x_outlay_event = get_outlayevent_from_dict(x_event_dict)
        x_dict[x_outlay_event.timestamp] = x_outlay_event
    return x_dict
