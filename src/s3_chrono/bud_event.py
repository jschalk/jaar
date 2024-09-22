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
        x_list = []
        for x_event in self.events.values():
            x_list.append([self.owner_id, x_event.timestamp, x_event.money_magnitude])
        return x_list

    def get_headers(self) -> list:
        return ["owner_id", "timestamp", "money_magnitude"]

    def get_dict(self) -> dict:
        return {"owner_id": self.owner_id, "events": self._get_events_dict()}

    def _get_events_dict(self) -> dict:
        x_dict = {}
        for x_event in self.events.values():
            x_dict[x_event.timestamp] = {"money_magnitude": x_event.money_magnitude}
        return x_dict


def ownerbudevents_shop(owner_id: OwnerID) -> OwnerBudEvents:
    return OwnerBudEvents(owner_id=owner_id, events={}, _sum_acct_outlays={})
