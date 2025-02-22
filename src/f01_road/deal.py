from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_None,
    get_empty_set_if_None,
    get_0_if_None,
    get_json_from_dict,
    get_dict_from_json,
    set_in_nested_dict,
    create_csv,
    get_from_nested_dict,
    exists_in_nested_dict,
    del_in_nested_dict,
)
from src.f01_road.finance import FundNum, TimeLinePoint, default_fund_pool
from src.f01_road.road import (
    AcctName,
    OwnerName,
    FiscTitle,
    get_default_fisc_title,
)
from dataclasses import dataclass


class calc_magnitudeException(Exception):
    pass


class time_int_Exception(Exception):
    pass


def time_int_str() -> str:
    return "time_int"


def bridge_str() -> str:
    return "bridge"


def quota_str() -> str:
    return "quota"


def dealdepth_str() -> str:
    return "dealdepth"


def magnitude_str() -> str:
    return "magnitude"


def deal_net_str() -> str:
    return "deal_net"


def owner_name_str() -> str:
    return "owner_name"


def fisc_title_str() -> str:
    return "fisc_title"


DEFAULT_DEALDEPTH = 2


@dataclass
class TranUnit:
    src: AcctName = None
    dst: AcctName = None
    time_int: TimeLinePoint = None
    amount: FundNum = None


def tranunit_shop(
    src: AcctName, dst: AcctName, time_int: TimeLinePoint, amount: FundNum
) -> TranUnit:
    return TranUnit(src=src, dst=dst, time_int=time_int, amount=amount)


@dataclass
class TranBook:
    fisc_title: FiscTitle = None
    tranunits: dict[OwnerName, dict[AcctName, dict[TimeLinePoint, FundNum]]] = None
    _accts_net: dict[OwnerName, dict[AcctName, FundNum]] = None

    def set_tranunit(
        self,
        tranunit: TranUnit,
        blocked_time_ints: set[TimeLinePoint] = None,
        present_time: TimeLinePoint = None,
    ):
        self.add_tranunit(
            owner_name=tranunit.src,
            acct_name=tranunit.dst,
            time_int=tranunit.time_int,
            amount=tranunit.amount,
            blocked_time_ints=blocked_time_ints,
            present_time=present_time,
        )

    def add_tranunit(
        self,
        owner_name: OwnerName,
        acct_name: AcctName,
        time_int: TimeLinePoint,
        amount: FundNum,
        blocked_time_ints: set[TimeLinePoint] = None,
        present_time: TimeLinePoint = None,
    ):
        if time_int in get_empty_set_if_None(blocked_time_ints):
            exception_str = (
                f"Cannot set tranunit for time_int={time_int}, timelinepoint is blocked"
            )
            raise time_int_Exception(exception_str)
        if present_time != None and time_int >= present_time:
            exception_str = f"Cannot set tranunit for time_int={time_int}, timelinepoint is greater than current time={present_time}"
            raise time_int_Exception(exception_str)
        x_keylist = [owner_name, acct_name, time_int]
        set_in_nested_dict(self.tranunits, x_keylist, amount)

    def tranunit_exists(
        self, src: AcctName, dst: AcctName, time_int: TimeLinePoint
    ) -> bool:
        return get_from_nested_dict(self.tranunits, [src, dst, time_int], True) != None

    def get_tranunit(
        self, src: AcctName, dst: AcctName, time_int: TimeLinePoint
    ) -> TranUnit:
        x_amount = get_from_nested_dict(self.tranunits, [src, dst, time_int], True)
        if x_amount != None:
            return tranunit_shop(src, dst, time_int, x_amount)

    def get_amount(
        self, src: AcctName, dst: AcctName, time_int: TimeLinePoint
    ) -> TranUnit:
        return get_from_nested_dict(self.tranunits, [src, dst, time_int], True)

    def del_tranunit(
        self, src: AcctName, dst: AcctName, time_int: TimeLinePoint
    ) -> TranUnit:
        x_keylist = [src, dst, time_int]
        if exists_in_nested_dict(self.tranunits, x_keylist):
            del_in_nested_dict(self.tranunits, x_keylist)

    def get_time_ints(self) -> set[TimeLinePoint]:
        x_set = set()
        for dst_dict in self.tranunits.values():
            for time_int_dict in dst_dict.values():
                x_set.update(set(time_int_dict.keys()))
        return x_set

    def get_owners_accts_net(self) -> dict[OwnerName, dict[AcctName, FundNum]]:
        owners_accts_net_dict = {}
        for owner_name, owner_dict in self.tranunits.items():
            for acct_name, acct_dict in owner_dict.items():
                if owners_accts_net_dict.get(owner_name) is None:
                    owners_accts_net_dict[owner_name] = {}
                owner_net_dict = owners_accts_net_dict.get(owner_name)
                owner_net_dict[acct_name] = sum(acct_dict.values())
        return owners_accts_net_dict

    def get_accts_net_dict(self) -> dict[AcctName, FundNum]:
        accts_net_dict = {}
        for owner_dict in self.tranunits.values():
            for acct_name, acct_dict in sorted(owner_dict.items()):
                if accts_net_dict.get(acct_name) is None:
                    accts_net_dict[acct_name] = sum(acct_dict.values())
                else:
                    accts_net_dict[acct_name] += sum(acct_dict.values())
        return accts_net_dict

    def _get_accts_headers(self) -> list:
        return ["acct_name", "net_amount"]

    def _get_accts_net_array(self) -> list[list]:
        x_items = self.get_accts_net_dict().items()
        return [[acct_name, net_amount] for acct_name, net_amount in x_items]

    def get_accts_net_csv(self) -> str:
        return create_csv(self._get_accts_headers(), self._get_accts_net_array())

    def join(self, x_tranbook):
        sorted_tranunits = sorted(
            x_tranbook.tranunits.items(),
            key=lambda x: next(iter(next(iter(x[1].values())).keys())),
        )
        for src_acct_name, dst_dict in sorted_tranunits:
            for dst_acct_name, time_int_dict in dst_dict.items():
                for x_time_int, x_amount in time_int_dict.items():
                    self.add_tranunit(
                        src_acct_name, dst_acct_name, x_time_int, x_amount
                    )

    def get_dict(
        self,
    ) -> dict[FiscTitle, dict[OwnerName, dict[AcctName, dict[TimeLinePoint, FundNum]]]]:
        return {"fisc_title": self.fisc_title, "tranunits": self.tranunits}


def tranbook_shop(
    x_fisc_title: FiscTitle,
    x_tranunits: dict[OwnerName, dict[AcctName, dict[TimeLinePoint, FundNum]]] = None,
):
    return TranBook(
        fisc_title=x_fisc_title,
        tranunits=get_empty_dict_if_None(x_tranunits),
        _accts_net={},
    )


def get_tranbook_from_dict(x_dict: dict) -> TranBook:
    x_tranunits = x_dict.get("tranunits")
    new_tranunits = {}
    for x_owner_name, x_acct_dict in x_tranunits.items():
        for x_acct_name, x_time_int_dict in x_acct_dict.items():
            for x_time_int, x_amount in x_time_int_dict.items():
                x_key_list = [x_owner_name, x_acct_name, int(x_time_int)]
                set_in_nested_dict(new_tranunits, x_key_list, x_amount)
    return tranbook_shop(x_dict.get("fisc_title"), new_tranunits)


@dataclass
class DealUnit:
    time_int: TimeLinePoint = None
    quota: FundNum = None
    dealdepth: int = None  # non-negative
    _magnitude: FundNum = None  # how much of the actual quota is distributed
    _deal_net: dict[AcctName, FundNum] = None  # ledger of deal outcome

    def set_deal_net(self, x_acct_name: AcctName, deal_net: FundNum):
        self._deal_net[x_acct_name] = deal_net

    def deal_net_exists(self, x_acct_name: AcctName) -> bool:
        return self._deal_net.get(x_acct_name) != None

    def get_deal_net(self, x_acct_name: AcctName) -> FundNum:
        return self._deal_net.get(x_acct_name)

    def del_deal_net(self, x_acct_name: AcctName):
        self._deal_net.pop(x_acct_name)

    def calc_magnitude(self):
        deal_net = self._deal_net.values()
        x_cred_sum = sum(deal_net for deal_net in deal_net if deal_net > 0)
        x_debt_sum = sum(deal_net for deal_net in deal_net if deal_net < 0)
        if x_cred_sum + x_debt_sum != 0:
            exception_str = f"magnitude cannot be calculated: debt_deal_net={x_debt_sum}, cred_deal_net={x_cred_sum}"
            raise calc_magnitudeException(exception_str)
        self._magnitude = x_cred_sum

    def get_dict(self) -> dict[str,]:
        x_dict = {"time_int": self.time_int, "quota": self.quota}
        if self._deal_net:
            x_dict["deal_net"] = self._deal_net
        if self._magnitude:
            x_dict["magnitude"] = self._magnitude
        if self.dealdepth != DEFAULT_DEALDEPTH:
            x_dict["dealdepth"] = self.dealdepth
        return x_dict

    def get_json(self) -> dict[str,]:
        return get_json_from_dict(self.get_dict())


def dealunit_shop(
    time_int: TimeLinePoint,
    quota: FundNum = None,
    deal_net: dict[AcctName, FundNum] = None,
    magnitude: FundNum = None,
    dealdepth: int = None,
) -> DealUnit:
    if quota is None:
        quota = default_fund_pool()
    if dealdepth is None:
        dealdepth = DEFAULT_DEALDEPTH

    return DealUnit(
        time_int=time_int,
        quota=quota,
        dealdepth=dealdepth,
        _deal_net=get_empty_dict_if_None(deal_net),
        _magnitude=get_0_if_None(magnitude),
    )


@dataclass
class BrokerUnit:
    owner_name: OwnerName = None
    deals: dict[TimeLinePoint, DealUnit] = None
    _sum_dealunit_quota: FundNum = None
    _sum_acct_deal_nets: int = None
    _time_int_min: TimeLinePoint = None
    _time_int_max: TimeLinePoint = None

    def set_deal(self, x_deal: DealUnit):
        self.deals[x_deal.time_int] = x_deal

    def add_deal(
        self, x_time_int: TimeLinePoint, x_quota: FundNum, dealdepth: int = None
    ):
        dealunit = dealunit_shop(
            time_int=x_time_int, quota=x_quota, dealdepth=dealdepth
        )
        self.set_deal(dealunit)

    def deal_exists(self, x_time_int: TimeLinePoint) -> bool:
        return self.deals.get(x_time_int) != None

    def get_deal(self, x_time_int: TimeLinePoint) -> DealUnit:
        return self.deals.get(x_time_int)

    def del_deal(self, x_time_int: TimeLinePoint):
        self.deals.pop(x_time_int)

    def get_2d_array(self) -> list[list]:
        return [
            [self.owner_name, x_deal.time_int, x_deal.quota]
            for x_deal in self.deals.values()
        ]

    def get_headers(self) -> list:
        return ["owner_name", "time_int", "quota"]

    def get_dict(self) -> dict:
        return {"owner_name": self.owner_name, "deals": self._get_deals_dict()}

    def _get_deals_dict(self) -> dict:
        return {x_deal.time_int: x_deal.get_dict() for x_deal in self.deals.values()}

    def get_time_ints(self) -> set[TimeLinePoint]:
        return set(self.deals.keys())

    def get_tranbook(self, fisc_title: FiscTitle) -> TranBook:
        x_tranbook = tranbook_shop(fisc_title)
        for x_time_int, x_deal in self.deals.items():
            for dst_acct_name, x_quota in x_deal._deal_net.items():
                x_tranbook.add_tranunit(
                    owner_name=self.owner_name,
                    acct_name=dst_acct_name,
                    time_int=x_time_int,
                    amount=x_quota,
                )
        return x_tranbook


def brokerunit_shop(owner_name: OwnerName) -> BrokerUnit:
    return BrokerUnit(owner_name=owner_name, deals={}, _sum_acct_deal_nets={})


def get_dealunit_from_dict(x_dict: dict) -> DealUnit:
    x_time_int = x_dict.get("time_int")
    x_quota = x_dict.get("quota")
    x_deal_net = x_dict.get("deal_net")
    x_magnitude = x_dict.get("magnitude")
    x_dealdepth = x_dict.get("dealdepth")
    return dealunit_shop(
        x_time_int, x_quota, x_deal_net, x_magnitude, dealdepth=x_dealdepth
    )


def get_dealunit_from_json(x_json: str) -> DealUnit:
    return get_dealunit_from_dict(get_dict_from_json(x_json))


def get_brokerunit_from_dict(x_dict: dict) -> BrokerUnit:
    x_owner_name = x_dict.get("owner_name")
    x_brokerunit = brokerunit_shop(x_owner_name)
    x_brokerunit.deals = get_deals_from_dict(x_dict.get("deals"))
    return x_brokerunit


def get_deals_from_dict(deals_dict: dict) -> dict[TimeLinePoint, DealUnit]:
    x_dict = {}
    for x_deal_dict in deals_dict.values():
        x_dealunit = get_dealunit_from_dict(x_deal_dict)
        x_dict[x_dealunit.time_int] = x_dealunit
    return x_dict


@dataclass
class TimeConversion:
    fisc_title: str = None
    addin: str = None


def timeconversion_shop(
    fisc_title: FiscTitle = None, addin: int = None
) -> TimeConversion:
    if fisc_title is None:
        fisc_title = get_default_fisc_title()
    if addin is None:
        addin = 0
    return TimeConversion(fisc_title=fisc_title, addin=addin)
