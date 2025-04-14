from src.f00_data_toolboxs.dict_toolbox import (
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
from src.f01_road.finance_config import FundNum, TimeLinePoint, default_fund_pool
from src.f01_road.road import (
    AcctName,
    OwnerName,
    FiscTitle,
    get_default_fisc_title,
)
from dataclasses import dataclass


class calc_magnitudeException(Exception):
    pass


class tran_time_Exception(Exception):
    pass


def world_id_str() -> str:
    return "world_id"


def tran_time_str() -> str:
    return "tran_time"


def deal_time_str() -> str:
    return "deal_time"


def bridge_str() -> str:
    return "bridge"


def quota_str() -> str:
    return "quota"


def celldepth_str() -> str:
    return "celldepth"


def magnitude_str() -> str:
    return "magnitude"


def deal_acct_nets_str() -> str:
    return "deal_acct_nets"


def owner_name_str() -> str:
    return "owner_name"


def fisc_title_str() -> str:
    return "fisc_title"


DEFAULT_CELLDEPTH = 2


@dataclass
class TranUnit:
    src: AcctName = None
    dst: AcctName = None
    tran_time: TimeLinePoint = None
    amount: FundNum = None


def tranunit_shop(
    src: AcctName, dst: AcctName, tran_time: TimeLinePoint, amount: FundNum
) -> TranUnit:
    return TranUnit(src=src, dst=dst, tran_time=tran_time, amount=amount)


@dataclass
class TranBook:
    fisc_title: FiscTitle = None
    tranunits: dict[OwnerName, dict[AcctName, dict[TimeLinePoint, FundNum]]] = None
    _accts_net: dict[OwnerName, dict[AcctName, FundNum]] = None

    def set_tranunit(
        self,
        tranunit: TranUnit,
        blocked_tran_times: set[TimeLinePoint] = None,
        _offi_time_max: TimeLinePoint = None,
    ):
        self.add_tranunit(
            owner_name=tranunit.src,
            acct_name=tranunit.dst,
            tran_time=tranunit.tran_time,
            amount=tranunit.amount,
            blocked_tran_times=blocked_tran_times,
            _offi_time_max=_offi_time_max,
        )

    def add_tranunit(
        self,
        owner_name: OwnerName,
        acct_name: AcctName,
        tran_time: TimeLinePoint,
        amount: FundNum,
        blocked_tran_times: set[TimeLinePoint] = None,
        _offi_time_max: TimeLinePoint = None,
    ):
        if tran_time in get_empty_set_if_None(blocked_tran_times):
            exception_str = f"Cannot set tranunit for tran_time={tran_time}, timelinepoint is blocked"
            raise tran_time_Exception(exception_str)
        if _offi_time_max != None and tran_time >= _offi_time_max:
            exception_str = f"Cannot set tranunit for tran_time={tran_time}, timelinepoint is greater than current time={_offi_time_max}"
            raise tran_time_Exception(exception_str)
        x_keylist = [owner_name, acct_name, tran_time]
        set_in_nested_dict(self.tranunits, x_keylist, amount)

    def tranunit_exists(
        self, src: AcctName, dst: AcctName, tran_time: TimeLinePoint
    ) -> bool:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True) != None

    def get_tranunit(
        self, src: AcctName, dst: AcctName, tran_time: TimeLinePoint
    ) -> TranUnit:
        x_amount = get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)
        if x_amount != None:
            return tranunit_shop(src, dst, tran_time, x_amount)

    def get_amount(
        self, src: AcctName, dst: AcctName, tran_time: TimeLinePoint
    ) -> TranUnit:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)

    def del_tranunit(
        self, src: AcctName, dst: AcctName, tran_time: TimeLinePoint
    ) -> TranUnit:
        x_keylist = [src, dst, tran_time]
        if exists_in_nested_dict(self.tranunits, x_keylist):
            del_in_nested_dict(self.tranunits, x_keylist)

    def get_tran_times(self) -> set[TimeLinePoint]:
        x_set = set()
        for dst_dict in self.tranunits.values():
            for tran_time_dict in dst_dict.values():
                x_set.update(set(tran_time_dict.keys()))
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
            for dst_acct_name, tran_time_dict in dst_dict.items():
                for x_tran_time, x_amount in tran_time_dict.items():
                    self.add_tranunit(
                        src_acct_name, dst_acct_name, x_tran_time, x_amount
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
        for x_acct_name, x_tran_time_dict in x_acct_dict.items():
            for x_tran_time, x_amount in x_tran_time_dict.items():
                x_key_list = [x_owner_name, x_acct_name, int(x_tran_time)]
                set_in_nested_dict(new_tranunits, x_key_list, x_amount)
    return tranbook_shop(x_dict.get("fisc_title"), new_tranunits)


@dataclass
class DealUnit:
    deal_time: TimeLinePoint = None
    quota: FundNum = None
    celldepth: int = None  # non-negative
    _magnitude: FundNum = None  # how much of the actual quota is distributed
    _deal_acct_nets: dict[AcctName, FundNum] = None  # ledger of deal outcome

    def set_deal_acct_net(self, x_acct_name: AcctName, deal_acct_net: FundNum):
        self._deal_acct_nets[x_acct_name] = deal_acct_net

    def deal_acct_net_exists(self, x_acct_name: AcctName) -> bool:
        return self._deal_acct_nets.get(x_acct_name) != None

    def get_deal_acct_net(self, x_acct_name: AcctName) -> FundNum:
        return self._deal_acct_nets.get(x_acct_name)

    def del_deal_acct_net(self, x_acct_name: AcctName):
        self._deal_acct_nets.pop(x_acct_name)

    def calc_magnitude(self):
        deal_acct_nets = self._deal_acct_nets.values()
        x_cred_sum = sum(da_net for da_net in deal_acct_nets if da_net > 0)
        x_debt_sum = sum(da_net for da_net in deal_acct_nets if da_net < 0)
        if x_cred_sum + x_debt_sum != 0:
            exception_str = f"magnitude cannot be calculated: debt_deal_acct_net={x_debt_sum}, cred_deal_acct_net={x_cred_sum}"
            raise calc_magnitudeException(exception_str)
        self._magnitude = x_cred_sum

    def get_dict(self) -> dict[str,]:
        x_dict = {"deal_time": self.deal_time, "quota": self.quota}
        if self._deal_acct_nets:
            x_dict["deal_acct_nets"] = self._deal_acct_nets
        if self._magnitude:
            x_dict["magnitude"] = self._magnitude
        if self.celldepth != DEFAULT_CELLDEPTH:
            x_dict["celldepth"] = self.celldepth
        return x_dict

    def get_json(self) -> dict[str,]:
        return get_json_from_dict(self.get_dict())


def dealunit_shop(
    deal_time: TimeLinePoint,
    quota: FundNum = None,
    deal_acct_nets: dict[AcctName, FundNum] = None,
    magnitude: FundNum = None,
    celldepth: int = None,
) -> DealUnit:
    if quota is None:
        quota = default_fund_pool()
    if celldepth is None:
        celldepth = DEFAULT_CELLDEPTH

    return DealUnit(
        deal_time=deal_time,
        quota=quota,
        celldepth=celldepth,
        _deal_acct_nets=get_empty_dict_if_None(deal_acct_nets),
        _magnitude=get_0_if_None(magnitude),
    )


@dataclass
class BrokerUnit:
    owner_name: OwnerName = None
    deals: dict[TimeLinePoint, DealUnit] = None
    _sum_dealunit_quota: FundNum = None
    _sum_acct_deal_nets: int = None
    _deal_time_min: TimeLinePoint = None
    _deal_time_max: TimeLinePoint = None

    def set_deal(self, x_deal: DealUnit):
        self.deals[x_deal.deal_time] = x_deal

    def add_deal(
        self, x_deal_time: TimeLinePoint, x_quota: FundNum, celldepth: int = None
    ):
        dealunit = dealunit_shop(
            deal_time=x_deal_time, quota=x_quota, celldepth=celldepth
        )
        self.set_deal(dealunit)

    def deal_exists(self, x_deal_time: TimeLinePoint) -> bool:
        return self.deals.get(x_deal_time) != None

    def get_deal(self, x_deal_time: TimeLinePoint) -> DealUnit:
        return self.deals.get(x_deal_time)

    def del_deal(self, x_deal_time: TimeLinePoint):
        self.deals.pop(x_deal_time)

    def get_2d_array(self) -> list[list]:
        return [
            [self.owner_name, x_deal.deal_time, x_deal.quota]
            for x_deal in self.deals.values()
        ]

    def get_headers(self) -> list:
        return ["owner_name", "deal_time", "quota"]

    def get_dict(self) -> dict:
        return {"owner_name": self.owner_name, "deals": self._get_deals_dict()}

    def _get_deals_dict(self) -> dict:
        return {x_deal.deal_time: x_deal.get_dict() for x_deal in self.deals.values()}

    def get_deal_times(self) -> set[TimeLinePoint]:
        return set(self.deals.keys())

    def get_tranbook(self, fisc_title: FiscTitle) -> TranBook:
        x_tranbook = tranbook_shop(fisc_title)
        for x_deal_time, x_deal in self.deals.items():
            for dst_acct_name, x_quota in x_deal._deal_acct_nets.items():
                x_tranbook.add_tranunit(
                    owner_name=self.owner_name,
                    acct_name=dst_acct_name,
                    tran_time=x_deal_time,
                    amount=x_quota,
                )
        return x_tranbook


def brokerunit_shop(owner_name: OwnerName) -> BrokerUnit:
    return BrokerUnit(owner_name=owner_name, deals={}, _sum_acct_deal_nets={})


def get_dealunit_from_dict(x_dict: dict) -> DealUnit:
    x_deal_time = x_dict.get("deal_time")
    x_quota = x_dict.get("quota")
    x_deal_net = x_dict.get("deal_acct_nets")
    x_magnitude = x_dict.get("magnitude")
    x_celldepth = x_dict.get("celldepth")
    return dealunit_shop(
        x_deal_time, x_quota, x_deal_net, x_magnitude, celldepth=x_celldepth
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
        x_dict[x_dealunit.deal_time] = x_dealunit
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
