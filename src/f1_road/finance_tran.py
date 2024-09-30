from src.f0_instrument.python_tool import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_json_from_dict,
    get_dict_from_json,
)
from src.f1_road.finance import FundNum, TimeLinePoint, default_fund_pool
from src.f1_road.road import AcctID, OwnerID, FiscalID
from dataclasses import dataclass


class calc_magnitudeException(Exception):
    pass


@dataclass
class OutlayEvent:
    timestamp: TimeLinePoint = None
    purview: FundNum = None
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

    def calc_magnitude(self):
        net_outlays = self._net_outlays.values()
        x_cred_sum = sum(net_outlay for net_outlay in net_outlays if net_outlay > 0)
        x_debt_sum = sum(net_outlay for net_outlay in net_outlays if net_outlay < 0)
        if x_cred_sum + x_debt_sum != 0:
            exception_text = f"magnitude cannot be calculated: debt_outlay={x_debt_sum}, cred_outlay={x_cred_sum}"
            raise calc_magnitudeException(exception_text)
        self._magnitude = x_cred_sum

    def get_dict(self) -> dict[str,]:
        x_dict = {"timestamp": self.timestamp, "purview": self.purview}
        if self._net_outlays:
            x_dict["net_outlays"] = self._net_outlays
        if self._magnitude:
            x_dict["magnitude"] = self._magnitude
        return x_dict

    def get_json(self) -> dict[str,]:
        return get_json_from_dict(self.get_dict())


def outlayevent_shop(
    x_timestamp: TimeLinePoint,
    x_purview: FundNum = None,
    net_outlays: dict[AcctID, FundNum] = None,
    x_magnitude: FundNum = None,
) -> OutlayEvent:
    if x_purview is None:
        x_purview = default_fund_pool()

    return OutlayEvent(
        timestamp=x_timestamp,
        purview=x_purview,
        _net_outlays=get_empty_dict_if_none(net_outlays),
        _magnitude=get_0_if_None(x_magnitude),
    )


@dataclass
class OutlayLog:
    owner_id: OwnerID = None
    events: dict[TimeLinePoint, OutlayEvent] = None
    _sum_outlayevent_purview: FundNum = None
    _sum_acct_outlays: int = None
    _timestamp_min: TimeLinePoint = None
    _timestamp_max: TimeLinePoint = None

    def set_event(self, x_event: OutlayEvent):
        self.events[x_event.timestamp] = x_event

    def add_event(self, x_timestamp: TimeLinePoint, x_purview: FundNum):
        self.set_event(outlayevent_shop(x_timestamp, x_purview))

    def event_exists(self, x_timestamp: TimeLinePoint) -> bool:
        return self.events.get(x_timestamp) != None

    def get_event(self, x_timestamp: TimeLinePoint) -> OutlayEvent:
        return self.events.get(x_timestamp)

    def del_event(self, x_timestamp: TimeLinePoint):
        self.events.pop(x_timestamp)

    def get_2d_array(self) -> list[list]:
        return [
            [self.owner_id, x_event.timestamp, x_event.purview]
            for x_event in self.events.values()
        ]

    def get_headers(self) -> list:
        return ["owner_id", "timestamp", "purview"]

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
    x_purview = x_dict.get("purview")
    x_net_outlays = x_dict.get("net_outlays")
    x_magnitude = x_dict.get("magnitude")
    return outlayevent_shop(x_timestamp, x_purview, x_net_outlays, x_magnitude)


def get_outlayevent_from_json(x_json: str) -> OutlayEvent:
    return get_outlayevent_from_dict(get_dict_from_json(x_json))


def get_outlaylog_from_dict(x_dict: dict) -> OutlayLog:
    x_owner_id = x_dict.get("owner_id")
    x_outlaylog = outlaylog_shop(x_owner_id)
    x_outlaylog.events = get_events_from_dict(x_dict.get("events"))
    return x_outlaylog


def get_events_from_dict(events_dict: dict) -> dict[TimeLinePoint, OutlayEvent]:
    x_dict = {}
    for x_event_dict in events_dict.values():
        x_outlay_event = get_outlayevent_from_dict(x_event_dict)
        x_dict[x_outlay_event.timestamp] = x_outlay_event
    return x_dict


@dataclass
class TranBook:
    fiscal_id: FiscalID = None
    tranlogs: dict[OwnerID, dict[AcctID, dict[TimeLinePoint, FundNum]]] = None
    tender_desc: str = None
    _accts_net: dict[AcctID, FundNum] = None

    def get_dict(
        self,
    ) -> dict[FiscalID, dict[OwnerID, dict[AcctID, dict[TimeLinePoint, FundNum]]]]:
        return {"fiscal_id": self.fiscal_id}


def tranbook_shop(
    x_fiscal_id: FiscalID,
    x_tranlogs: dict[OwnerID, dict[AcctID, dict[TimeLinePoint, FundNum]]] = None,
    x_tender_desc: str = None,
):
    return TranBook(
        fiscal_id=x_fiscal_id,
        tranlogs=get_empty_dict_if_none(x_tranlogs),
        tender_desc=x_tender_desc,
        _accts_net={},
    )


def get_tranbook_from_dict():
    pass


def get_tranbook_from_json():
    pass
