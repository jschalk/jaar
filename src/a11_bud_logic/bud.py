from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    create_csv,
    del_in_nested_dict,
    exists_in_nested_dict,
    get_0_if_None,
    get_dict_from_json,
    get_empty_dict_if_None,
    get_empty_set_if_None,
    get_from_nested_dict,
    get_json_from_dict,
    set_in_nested_dict,
)
from src.a01_term_logic.term import BelieverName, CoinLabel, PartnerName
from src.a02_finance_logic.finance_config import FundNum, default_fund_pool
from src.a07_timeline_logic.timeline_main import TimeLinePoint


class calc_magnitudeException(Exception):
    pass


class tran_time_Exception(Exception):
    pass


DEFAULT_CELLDEPTH = 2


@dataclass
class TranUnit:
    src: BelieverName = None
    dst: PartnerName = None
    tran_time: TimeLinePoint = None
    amount: FundNum = None


def tranunit_shop(
    src: BelieverName, dst: PartnerName, tran_time: TimeLinePoint, amount: FundNum
) -> TranUnit:
    return TranUnit(src=src, dst=dst, tran_time=tran_time, amount=amount)


@dataclass
class TranBook:
    coin_label: CoinLabel = None
    tranunits: dict[BelieverName, dict[PartnerName, dict[TimeLinePoint, FundNum]]] = (
        None
    )
    _partners_net: dict[BelieverName, dict[PartnerName, FundNum]] = None

    def set_tranunit(
        self,
        tranunit: TranUnit,
        blocked_tran_times: set[TimeLinePoint] = None,
        _offi_time_max: TimeLinePoint = None,
    ):
        self.add_tranunit(
            believer_name=tranunit.src,
            partner_name=tranunit.dst,
            tran_time=tranunit.tran_time,
            amount=tranunit.amount,
            blocked_tran_times=blocked_tran_times,
            _offi_time_max=_offi_time_max,
        )

    def add_tranunit(
        self,
        believer_name: BelieverName,
        partner_name: PartnerName,
        tran_time: TimeLinePoint,
        amount: FundNum,
        blocked_tran_times: set[TimeLinePoint] = None,
        _offi_time_max: TimeLinePoint = None,
    ):
        if tran_time in get_empty_set_if_None(blocked_tran_times):
            exception_str = f"Cannot set tranunit for tran_time={tran_time}, TimeLinePoint is blocked"
            raise tran_time_Exception(exception_str)
        if _offi_time_max != None and tran_time >= _offi_time_max:
            exception_str = f"Cannot set tranunit for tran_time={tran_time}, TimeLinePoint is greater than current time={_offi_time_max}"
            raise tran_time_Exception(exception_str)
        x_keylist = [believer_name, partner_name, tran_time]
        set_in_nested_dict(self.tranunits, x_keylist, amount)

    def tranunit_exists(
        self, src: BelieverName, dst: PartnerName, tran_time: TimeLinePoint
    ) -> bool:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True) != None

    def get_tranunit(
        self, src: BelieverName, dst: PartnerName, tran_time: TimeLinePoint
    ) -> TranUnit:
        x_amount = get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)
        if x_amount != None:
            return tranunit_shop(src, dst, tran_time, x_amount)

    def get_amount(
        self, src: BelieverName, dst: PartnerName, tran_time: TimeLinePoint
    ) -> TranUnit:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)

    def del_tranunit(
        self, src: BelieverName, dst: PartnerName, tran_time: TimeLinePoint
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

    def get_believers_partners_net(
        self,
    ) -> dict[BelieverName, dict[PartnerName, FundNum]]:
        believers_partners_net_dict = {}
        for believer_name, believer_dict in self.tranunits.items():
            for partner_name, partner_dict in believer_dict.items():
                if believers_partners_net_dict.get(believer_name) is None:
                    believers_partners_net_dict[believer_name] = {}
                believer_net_dict = believers_partners_net_dict.get(believer_name)
                believer_net_dict[partner_name] = sum(partner_dict.values())
        return believers_partners_net_dict

    def get_partners_net_dict(self) -> dict[PartnerName, FundNum]:
        partners_net_dict = {}
        for believer_dict in self.tranunits.values():
            for partner_name, partner_dict in sorted(believer_dict.items()):
                if partners_net_dict.get(partner_name) is None:
                    partners_net_dict[partner_name] = sum(partner_dict.values())
                else:
                    partners_net_dict[partner_name] += sum(partner_dict.values())
        return partners_net_dict

    def _get_partners_headers(self) -> list:
        return ["partner_name", "net_amount"]

    def _get_partners_net_array(self) -> list[list]:
        x_plans = self.get_partners_net_dict().items()
        return [[partner_name, net_amount] for partner_name, net_amount in x_plans]

    def get_partners_net_csv(self) -> str:
        return create_csv(self._get_partners_headers(), self._get_partners_net_array())

    def join(self, x_tranbook):
        sorted_tranunits = sorted(
            x_tranbook.tranunits.items(),
            key=lambda x: next(iter(next(iter(x[1].values())).keys())),
        )
        for src_partner_name, dst_dict in sorted_tranunits:
            for dst_partner_name, tran_time_dict in dst_dict.items():
                for x_tran_time, x_amount in tran_time_dict.items():
                    self.add_tranunit(
                        src_partner_name, dst_partner_name, x_tran_time, x_amount
                    )

    def to_dict(
        self,
    ) -> dict[
        CoinLabel, dict[BelieverName, dict[PartnerName, dict[TimeLinePoint, FundNum]]]
    ]:
        return {"coin_label": self.coin_label, "tranunits": self.tranunits}


def tranbook_shop(
    x_coin_label: CoinLabel,
    x_tranunits: dict[
        BelieverName, dict[PartnerName, dict[TimeLinePoint, FundNum]]
    ] = None,
):
    return TranBook(
        coin_label=x_coin_label,
        tranunits=get_empty_dict_if_None(x_tranunits),
        _partners_net={},
    )


def get_tranbook_from_dict(x_dict: dict) -> TranBook:
    x_tranunits = x_dict.get("tranunits")
    new_tranunits = {}
    for x_believer_name, x_partner_dict in x_tranunits.items():
        for x_partner_name, x_tran_time_dict in x_partner_dict.items():
            for x_tran_time, x_amount in x_tran_time_dict.items():
                x_key_list = [x_believer_name, x_partner_name, int(x_tran_time)]
                set_in_nested_dict(new_tranunits, x_key_list, x_amount)
    return tranbook_shop(x_dict.get("coin_label"), new_tranunits)


@dataclass
class BudUnit:
    bud_time: TimeLinePoint = None
    quota: FundNum = None
    celldepth: int = None  # non-negative
    _magnitude: FundNum = None  # how much of the actual quota is distributed
    _bud_partner_nets: dict[PartnerName, FundNum] = None  # ledger of bud outcome

    def set_bud_partner_net(
        self, x_partner_name: PartnerName, bud_partner_net: FundNum
    ):
        self._bud_partner_nets[x_partner_name] = bud_partner_net

    def bud_partner_net_exists(self, x_partner_name: PartnerName) -> bool:
        return self._bud_partner_nets.get(x_partner_name) != None

    def get_bud_partner_net(self, x_partner_name: PartnerName) -> FundNum:
        return self._bud_partner_nets.get(x_partner_name)

    def del_bud_partner_net(self, x_partner_name: PartnerName):
        self._bud_partner_nets.pop(x_partner_name)

    def calc_magnitude(self):
        bud_partner_nets = self._bud_partner_nets.values()
        x_cred_sum = sum(da_net for da_net in bud_partner_nets if da_net > 0)
        x_debt_sum = sum(da_net for da_net in bud_partner_nets if da_net < 0)
        if x_cred_sum + x_debt_sum != 0:
            exception_str = f"magnitude cannot be calculated: debt_bud_partner_net={x_debt_sum}, cred_bud_partner_net={x_cred_sum}"
            raise calc_magnitudeException(exception_str)
        self._magnitude = x_cred_sum

    def to_dict(self) -> dict[str,]:
        x_dict = {"bud_time": self.bud_time, "quota": self.quota}
        if self._bud_partner_nets:
            x_dict["bud_partner_nets"] = self._bud_partner_nets
        if self._magnitude:
            x_dict["magnitude"] = self._magnitude
        if self.celldepth != DEFAULT_CELLDEPTH:
            x_dict["celldepth"] = self.celldepth
        return x_dict

    def get_json(self) -> dict[str,]:
        return get_json_from_dict(self.to_dict())


def budunit_shop(
    bud_time: TimeLinePoint,
    quota: FundNum = None,
    bud_partner_nets: dict[PartnerName, FundNum] = None,
    magnitude: FundNum = None,
    celldepth: int = None,
) -> BudUnit:
    if quota is None:
        quota = default_fund_pool()
    if celldepth is None:
        celldepth = DEFAULT_CELLDEPTH

    return BudUnit(
        bud_time=bud_time,
        quota=quota,
        celldepth=celldepth,
        _bud_partner_nets=get_empty_dict_if_None(bud_partner_nets),
        _magnitude=get_0_if_None(magnitude),
    )


@dataclass
class BrokerUnit:
    believer_name: BelieverName = None
    buds: dict[TimeLinePoint, BudUnit] = None
    _sum_budunit_quota: FundNum = None
    _sum_partner_bud_nets: int = None
    _bud_time_min: TimeLinePoint = None
    _bud_time_max: TimeLinePoint = None

    def set_bud(self, x_bud: BudUnit):
        self.buds[x_bud.bud_time] = x_bud

    def add_bud(
        self, x_bud_time: TimeLinePoint, x_quota: FundNum, celldepth: int = None
    ):
        budunit = budunit_shop(bud_time=x_bud_time, quota=x_quota, celldepth=celldepth)
        self.set_bud(budunit)

    def bud_exists(self, x_bud_time: TimeLinePoint) -> bool:
        return self.buds.get(x_bud_time) != None

    def get_bud(self, x_bud_time: TimeLinePoint) -> BudUnit:
        return self.buds.get(x_bud_time)

    def del_bud(self, x_bud_time: TimeLinePoint):
        self.buds.pop(x_bud_time)

    def get_2d_array(self) -> list[list]:
        return [
            [self.believer_name, x_bud.bud_time, x_bud.quota]
            for x_bud in self.buds.values()
        ]

    def get_headers(self) -> list:
        return ["believer_name", "bud_time", "quota"]

    def to_dict(self) -> dict:
        return {"believer_name": self.believer_name, "buds": self._get_buds_dict()}

    def _get_buds_dict(self) -> dict:
        return {x_bud.bud_time: x_bud.to_dict() for x_bud in self.buds.values()}

    def get_bud_times(self) -> set[TimeLinePoint]:
        return set(self.buds.keys())

    def get_tranbook(self, coin_label: CoinLabel) -> TranBook:
        x_tranbook = tranbook_shop(coin_label)
        for x_bud_time, x_bud in self.buds.items():
            for dst_partner_name, x_quota in x_bud._bud_partner_nets.items():
                x_tranbook.add_tranunit(
                    believer_name=self.believer_name,
                    partner_name=dst_partner_name,
                    tran_time=x_bud_time,
                    amount=x_quota,
                )
        return x_tranbook


def brokerunit_shop(believer_name: BelieverName) -> BrokerUnit:
    return BrokerUnit(believer_name=believer_name, buds={}, _sum_partner_bud_nets={})


def get_budunit_from_dict(x_dict: dict) -> BudUnit:
    x_bud_time = x_dict.get("bud_time")
    x_quota = x_dict.get("quota")
    x_bud_net = x_dict.get("bud_partner_nets")
    x_magnitude = x_dict.get("magnitude")
    x_celldepth = x_dict.get("celldepth")
    return budunit_shop(
        x_bud_time, x_quota, x_bud_net, x_magnitude, celldepth=x_celldepth
    )


def get_budunit_from_json(x_json: str) -> BudUnit:
    return get_budunit_from_dict(get_dict_from_json(x_json))


def get_brokerunit_from_dict(x_dict: dict) -> BrokerUnit:
    x_believer_name = x_dict.get("believer_name")
    x_brokerunit = brokerunit_shop(x_believer_name)
    x_brokerunit.buds = get_buds_from_dict(x_dict.get("buds"))
    return x_brokerunit


def get_buds_from_dict(buds_dict: dict) -> dict[TimeLinePoint, BudUnit]:
    x_dict = {}
    for x_bud_dict in buds_dict.values():
        x_budunit = get_budunit_from_dict(x_bud_dict)
        x_dict[x_budunit.bud_time] = x_budunit
    return x_dict
