from src.s1_road.road import OwnerID
from src.s2_bud.bud import BudUnit
from src.s3_chrono.chrono import TimeLinePoint
from dataclasses import dataclass


@dataclass
class OwnerBudEvent:
    timestamp: TimeLinePoint = None
    money_magnitude: int = None
    _bud: BudUnit = None
    _money_desc: str = None

    def get_array(self) -> list[int]:
        return [self.timestamp, self.money_magnitude]

    def get_dict(self) -> dict[str,]:
        return {"timestamp": self.timestamp, "money_magnitude": self.money_magnitude}


def ownerbudevent_shop(
    x_timestamp: TimeLinePoint, x_money_magnitude: int
) -> OwnerBudEvent:
    return OwnerBudEvent(x_timestamp, money_magnitude=x_money_magnitude)


@dataclass
class OwnerBudEvents:
    owner_id: OwnerID = None
    events: dict[TimeLinePoint:OwnerBudEvent] = None
    _sum_money_magnitude: int = None
    _sum_acct_outlays: int = None
    _timestamp_min: TimeLinePoint = None
    _timestamp_max: TimeLinePoint = None

    def set_event(self, x_event: OwnerBudEvent):
        self.events[x_event.timestamp] = x_event

    def add_event(self, x_timestamp: TimeLinePoint, x_money_magnitude: int):
        self.set_event(ownerbudevent_shop(x_timestamp, x_money_magnitude))

    def event_exists(self, x_timestamp: TimeLinePoint) -> bool:
        return self.events.get(x_timestamp) != None

    def get_event(self, x_timestamp: TimeLinePoint) -> OwnerBudEvent:
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


def ownerbudevents_shop(owner_id: OwnerID) -> OwnerBudEvents:
    return OwnerBudEvents(owner_id=owner_id, events={}, _sum_acct_outlays={})


def get_ownerbudevent_from_dict(x_dict: dict) -> OwnerBudEvent:
    x_timestamp = x_dict.get("timestamp")
    x_money_magnitude = x_dict.get("money_magnitude")
    return ownerbudevent_shop(x_timestamp, x_money_magnitude)


def get_ownerbudevents_from_dict(x_dict: dict) -> OwnerBudEvents:
    x_owner_id = x_dict.get("owner_id")
    x_ownerbudevents = ownerbudevents_shop(x_owner_id)
    x_ownerbudevents.events = get_events_from_dict(x_dict.get("events"))
    return x_ownerbudevents


def get_events_from_dict(events_dict: dict) -> dict[TimeLinePoint:OwnerBudEvent]:
    x_dict = {}
    for x_event in events_dict.values():
        x_timestamp = x_event.get("timestamp")
        x_money_magnitude = x_event.get("money_magnitude")
        x_dict[x_timestamp] = ownerbudevent_shop(x_timestamp, x_money_magnitude)
    return x_dict
