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
    DealIdea,
    get_default_deal_idea_ideaunit,
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
    deal_idea: DealIdea = None
    tranunits: dict[OwnerName, dict[AcctName, dict[TimeLinePoint, FundNum]]] = None
    _accts_net: dict[OwnerName, dict[AcctName, FundNum]] = None

    def set_tranunit(
        self,
        x_tranunit: TranUnit,
        x_blocked_time_ints: set[TimeLinePoint] = None,
        x_current_time: TimeLinePoint = None,
    ):
        self.add_tranunit(
            x_owner_name=x_tranunit.src,
            x_acct_name=x_tranunit.dst,
            x_time_int=x_tranunit.time_int,
            x_amount=x_tranunit.amount,
            x_blocked_time_ints=x_blocked_time_ints,
            x_current_time=x_current_time,
        )

    def add_tranunit(
        self,
        x_owner_name: OwnerName,
        x_acct_name: AcctName,
        x_time_int: TimeLinePoint,
        x_amount: FundNum,
        x_blocked_time_ints: set[TimeLinePoint] = None,
        x_current_time: TimeLinePoint = None,
    ):
        if x_time_int in get_empty_set_if_None(x_blocked_time_ints):
            exception_str = f"Cannot set tranunit for time_int={x_time_int}, timelinepoint is blocked"
            raise time_int_Exception(exception_str)
        if x_current_time != None and x_time_int >= x_current_time:
            exception_str = f"Cannot set tranunit for time_int={x_time_int}, timelinepoint is greater than current time={x_current_time}"
            raise time_int_Exception(exception_str)
        x_keylist = [x_owner_name, x_acct_name, x_time_int]
        set_in_nested_dict(self.tranunits, x_keylist, x_amount)

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

    # def join(self, x_tranbook):
    #     for src_acct_name, dst_dict in x_tranbook.tranunits.items():
    #         for dst_acct_name, time_int_dict in dst_dict.items():
    #             for x_time_int, x_amount in time_int_dict.items():
    #                 self.add_tranunit(src_acct_name, dst_acct_name, x_time_int, x_amount)

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

    # def get_dict(
    #     self,
    # ) -> dict[DealIdea, dict[OwnerName, dict[AcctName, dict[TimeLinePoint, FundNum]]]]:
    #     return {"deal_idea": self.deal_idea}


def tranbook_shop(
    x_deal_idea: DealIdea,
    x_tranunits: dict[OwnerName, dict[AcctName, dict[TimeLinePoint, FundNum]]] = None,
):
    return TranBook(
        deal_idea=x_deal_idea,
        tranunits=get_empty_dict_if_None(x_tranunits),
        _accts_net={},
    )


def get_tranbook_from_dict():
    pass


def get_tranbook_from_json():
    pass


@dataclass
class PurviewEpisode:
    time_int: TimeLinePoint = None
    quota: FundNum = None
    _magnitude: FundNum = None
    _net_purviews: dict[AcctName, FundNum] = None

    def set_net_purview(self, x_acct_name: AcctName, net_purview: FundNum):
        self._net_purviews[x_acct_name] = net_purview

    def net_purview_exists(self, x_acct_name: AcctName) -> bool:
        return self._net_purviews.get(x_acct_name) != None

    def get_net_purview(self, x_acct_name: AcctName) -> FundNum:
        return self._net_purviews.get(x_acct_name)

    def del_net_purview(self, x_acct_name: AcctName):
        self._net_purviews.pop(x_acct_name)

    def calc_magnitude(self):
        net_purviews = self._net_purviews.values()
        x_cred_sum = sum(net_purview for net_purview in net_purviews if net_purview > 0)
        x_debt_sum = sum(net_purview for net_purview in net_purviews if net_purview < 0)
        if x_cred_sum + x_debt_sum != 0:
            exception_str = f"magnitude cannot be calculated: debt_purview={x_debt_sum}, cred_purview={x_cred_sum}"
            raise calc_magnitudeException(exception_str)
        self._magnitude = x_cred_sum

    def get_dict(self) -> dict[str,]:
        x_dict = {"time_int": self.time_int, "quota": self.quota}
        if self._net_purviews:
            x_dict["net_purviews"] = self._net_purviews
        if self._magnitude:
            x_dict["magnitude"] = self._magnitude
        return x_dict

    def get_json(self) -> dict[str,]:
        return get_json_from_dict(self.get_dict())


def purviewepisode_shop(
    x_time_int: TimeLinePoint,
    x_quota: FundNum = None,
    net_purviews: dict[AcctName, FundNum] = None,
    x_magnitude: FundNum = None,
) -> PurviewEpisode:
    if x_quota is None:
        x_quota = default_fund_pool()

    return PurviewEpisode(
        time_int=x_time_int,
        quota=x_quota,
        _net_purviews=get_empty_dict_if_None(net_purviews),
        _magnitude=get_0_if_None(x_magnitude),
    )


@dataclass
class PurviewLog:
    owner_name: OwnerName = None
    episodes: dict[TimeLinePoint, PurviewEpisode] = None
    _sum_purviewepisode_quota: FundNum = None
    _sum_acct_purviews: int = None
    _time_int_min: TimeLinePoint = None
    _time_int_max: TimeLinePoint = None

    def set_episode(self, x_episode: PurviewEpisode):
        self.episodes[x_episode.time_int] = x_episode

    def add_episode(self, x_time_int: TimeLinePoint, x_quota: FundNum):
        self.set_episode(purviewepisode_shop(x_time_int, x_quota))

    def episode_exists(self, x_time_int: TimeLinePoint) -> bool:
        return self.episodes.get(x_time_int) != None

    def get_episode(self, x_time_int: TimeLinePoint) -> PurviewEpisode:
        return self.episodes.get(x_time_int)

    def del_episode(self, x_time_int: TimeLinePoint):
        self.episodes.pop(x_time_int)

    def get_2d_array(self) -> list[list]:
        return [
            [self.owner_name, x_episode.time_int, x_episode.quota]
            for x_episode in self.episodes.values()
        ]

    def get_headers(self) -> list:
        return ["owner_name", "time_int", "quota"]

    def get_dict(self) -> dict:
        return {"owner_name": self.owner_name, "episodes": self._get_episodes_dict()}

    def _get_episodes_dict(self) -> dict:
        return {
            x_episode.time_int: x_episode.get_dict()
            for x_episode in self.episodes.values()
        }

    def get_time_ints(self) -> set[TimeLinePoint]:
        return set(self.episodes.keys())

    def get_tranbook(self, deal_idea: DealIdea) -> TranBook:
        x_tranbook = tranbook_shop(deal_idea)
        for x_time_int, x_episode in self.episodes.items():
            for dst_acct_name, x_quota in x_episode._net_purviews.items():
                x_tranbook.add_tranunit(
                    x_owner_name=self.owner_name,
                    x_acct_name=dst_acct_name,
                    x_time_int=x_time_int,
                    x_amount=x_quota,
                )
        return x_tranbook


def purviewlog_shop(owner_name: OwnerName) -> PurviewLog:
    return PurviewLog(owner_name=owner_name, episodes={}, _sum_acct_purviews={})


def get_purviewepisode_from_dict(x_dict: dict) -> PurviewEpisode:
    x_time_int = x_dict.get("time_int")
    x_quota = x_dict.get("quota")
    x_net_purviews = x_dict.get("net_purviews")
    x_magnitude = x_dict.get("magnitude")
    return purviewepisode_shop(x_time_int, x_quota, x_net_purviews, x_magnitude)


def get_purviewepisode_from_json(x_json: str) -> PurviewEpisode:
    return get_purviewepisode_from_dict(get_dict_from_json(x_json))


def get_purviewlog_from_dict(x_dict: dict) -> PurviewLog:
    x_owner_name = x_dict.get("owner_name")
    x_purviewlog = purviewlog_shop(x_owner_name)
    x_purviewlog.episodes = get_episodes_from_dict(x_dict.get("episodes"))
    return x_purviewlog


def get_episodes_from_dict(episodes_dict: dict) -> dict[TimeLinePoint, PurviewEpisode]:
    x_dict = {}
    for x_episode_dict in episodes_dict.values():
        x_purview_episode = get_purviewepisode_from_dict(x_episode_dict)
        x_dict[x_purview_episode.time_int] = x_purview_episode
    return x_dict


@dataclass
class TimeConversion:
    deal_idea: str = None
    addin: str = None


def timeconversion_shop(
    deal_idea: DealIdea = None, addin: int = None
) -> TimeConversion:
    if deal_idea is None:
        deal_idea = get_default_deal_idea_ideaunit()
    if addin is None:
        addin = 0
    return TimeConversion(deal_idea=deal_idea, addin=addin)
