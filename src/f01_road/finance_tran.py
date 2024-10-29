from src.f00_instrument.dict_tool import (
    get_empty_dict_if_none,
    get_empty_set_if_none,
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
from src.f01_road.road import AcctID, OwnerID, FiscalID, get_default_fiscal_id_roadnode
from dataclasses import dataclass


class calc_magnitudeException(Exception):
    pass


class time_id_Exception(Exception):
    pass


def time_id_str() -> str:
    return "time_id"


def quota_str() -> str:
    return "quota"


@dataclass
class TranUnit:
    src: AcctID = None
    dst: AcctID = None
    time_id: TimeLinePoint = None
    amount: FundNum = None


def tranunit_shop(
    src: AcctID, dst: AcctID, time_id: TimeLinePoint, amount: FundNum
) -> TranUnit:
    return TranUnit(src=src, dst=dst, time_id=time_id, amount=amount)


@dataclass
class TranBook:
    fiscal_id: FiscalID = None
    tranunits: dict[OwnerID, dict[AcctID, dict[TimeLinePoint, FundNum]]] = None
    _accts_net: dict[OwnerID, dict[AcctID, FundNum]] = None

    def set_tranunit(
        self,
        x_tranunit: TranUnit,
        x_blocked_time_ids: set[TimeLinePoint] = None,
        x_current_time: TimeLinePoint = None,
    ):
        self.add_tranunit(
            x_owner_id=x_tranunit.src,
            x_acct_id=x_tranunit.dst,
            x_time_id=x_tranunit.time_id,
            x_amount=x_tranunit.amount,
            x_blocked_time_ids=x_blocked_time_ids,
            x_current_time=x_current_time,
        )

    def add_tranunit(
        self,
        x_owner_id: OwnerID,
        x_acct_id: AcctID,
        x_time_id: TimeLinePoint,
        x_amount: FundNum,
        x_blocked_time_ids: set[TimeLinePoint] = None,
        x_current_time: TimeLinePoint = None,
    ):
        if x_time_id in get_empty_set_if_none(x_blocked_time_ids):
            exception_str = (
                f"Cannot set tranunit for time_id={x_time_id}, timelinepoint is blocked"
            )
            raise time_id_Exception(exception_str)
        if x_current_time != None and x_time_id >= x_current_time:
            exception_str = f"Cannot set tranunit for time_id={x_time_id}, timelinepoint is greater than current time={x_current_time}"
            raise time_id_Exception(exception_str)
        x_keylist = [x_owner_id, x_acct_id, x_time_id]
        set_in_nested_dict(self.tranunits, x_keylist, x_amount)

    def tranunit_exists(self, src: AcctID, dst: AcctID, time_id: TimeLinePoint) -> bool:
        return get_from_nested_dict(self.tranunits, [src, dst, time_id], True) != None

    def get_tranunit(
        self, src: AcctID, dst: AcctID, time_id: TimeLinePoint
    ) -> TranUnit:
        x_amount = get_from_nested_dict(self.tranunits, [src, dst, time_id], True)
        if x_amount != None:
            return tranunit_shop(src, dst, time_id, x_amount)

    def get_amount(self, src: AcctID, dst: AcctID, time_id: TimeLinePoint) -> TranUnit:
        return get_from_nested_dict(self.tranunits, [src, dst, time_id], True)

    def del_tranunit(
        self, src: AcctID, dst: AcctID, time_id: TimeLinePoint
    ) -> TranUnit:
        x_keylist = [src, dst, time_id]
        if exists_in_nested_dict(self.tranunits, x_keylist):
            del_in_nested_dict(self.tranunits, x_keylist)

    def get_time_ids(self) -> set[TimeLinePoint]:
        x_set = set()
        for dst_dict in self.tranunits.values():
            for time_id_dict in dst_dict.values():
                x_set.update(set(time_id_dict.keys()))
        return x_set

    def get_owners_accts_net(self) -> dict[OwnerID, dict[AcctID, FundNum]]:
        owners_accts_net_dict = {}
        for owner_id, owner_dict in self.tranunits.items():
            for acct_id, acct_dict in owner_dict.items():
                if owners_accts_net_dict.get(owner_id) is None:
                    owners_accts_net_dict[owner_id] = {}
                owner_net_dict = owners_accts_net_dict.get(owner_id)
                owner_net_dict[acct_id] = sum(acct_dict.values())
        return owners_accts_net_dict

    def get_accts_net_dict(self) -> dict[AcctID, FundNum]:
        accts_net_dict = {}
        for owner_dict in self.tranunits.values():
            for acct_id, acct_dict in sorted(owner_dict.items()):
                if accts_net_dict.get(acct_id) is None:
                    accts_net_dict[acct_id] = sum(acct_dict.values())
                else:
                    accts_net_dict[acct_id] += sum(acct_dict.values())
        return accts_net_dict

    def _get_accts_headers(self) -> list:
        return ["acct_id", "net_amount"]

    def _get_accts_net_array(self) -> list[list]:
        x_items = self.get_accts_net_dict().items()
        return [[acct_id, net_amount] for acct_id, net_amount in x_items]

    def get_accts_net_csv(self) -> str:
        return create_csv(self._get_accts_headers(), self._get_accts_net_array())

    # def join(self, x_tranbook):
    #     for src_acct_id, dst_dict in x_tranbook.tranunits.items():
    #         for dst_acct_id, time_id_dict in dst_dict.items():
    #             for x_time_id, x_amount in time_id_dict.items():
    #                 self.add_tranunit(src_acct_id, dst_acct_id, x_time_id, x_amount)

    def join(self, x_tranbook):
        sorted_tranunits = sorted(
            x_tranbook.tranunits.items(),
            key=lambda x: next(iter(next(iter(x[1].values())).keys())),
        )
        for src_acct_id, dst_dict in sorted_tranunits:
            for dst_acct_id, time_id_dict in dst_dict.items():
                for x_time_id, x_amount in time_id_dict.items():
                    self.add_tranunit(src_acct_id, dst_acct_id, x_time_id, x_amount)

    # def get_dict(
    #     self,
    # ) -> dict[FiscalID, dict[OwnerID, dict[AcctID, dict[TimeLinePoint, FundNum]]]]:
    #     return {"fiscal_id": self.fiscal_id}


def tranbook_shop(
    x_fiscal_id: FiscalID,
    x_tranunits: dict[OwnerID, dict[AcctID, dict[TimeLinePoint, FundNum]]] = None,
):
    return TranBook(
        fiscal_id=x_fiscal_id,
        tranunits=get_empty_dict_if_none(x_tranunits),
        _accts_net={},
    )


def get_tranbook_from_dict():
    pass


def get_tranbook_from_json():
    pass


@dataclass
class PurviewEpisode:
    time_id: TimeLinePoint = None
    quota: FundNum = None
    _magnitude: FundNum = None
    _net_purviews: dict[AcctID, FundNum] = None

    def set_net_purview(self, x_acct_id: AcctID, net_purview: FundNum):
        self._net_purviews[x_acct_id] = net_purview

    def net_purview_exists(self, x_acct_id: AcctID) -> bool:
        return self._net_purviews.get(x_acct_id) != None

    def get_net_purview(self, x_acct_id: AcctID) -> FundNum:
        return self._net_purviews.get(x_acct_id)

    def del_net_purview(self, x_acct_id: AcctID):
        self._net_purviews.pop(x_acct_id)

    def calc_magnitude(self):
        net_purviews = self._net_purviews.values()
        x_cred_sum = sum(net_purview for net_purview in net_purviews if net_purview > 0)
        x_debt_sum = sum(net_purview for net_purview in net_purviews if net_purview < 0)
        if x_cred_sum + x_debt_sum != 0:
            exception_str = f"magnitude cannot be calculated: debt_purview={x_debt_sum}, cred_purview={x_cred_sum}"
            raise calc_magnitudeException(exception_str)
        self._magnitude = x_cred_sum

    def get_dict(self) -> dict[str,]:
        x_dict = {"time_id": self.time_id, "quota": self.quota}
        if self._net_purviews:
            x_dict["net_purviews"] = self._net_purviews
        if self._magnitude:
            x_dict["magnitude"] = self._magnitude
        return x_dict

    def get_json(self) -> dict[str,]:
        return get_json_from_dict(self.get_dict())


def purviewepisode_shop(
    x_time_id: TimeLinePoint,
    x_quota: FundNum = None,
    net_purviews: dict[AcctID, FundNum] = None,
    x_magnitude: FundNum = None,
) -> PurviewEpisode:
    if x_quota is None:
        x_quota = default_fund_pool()

    return PurviewEpisode(
        time_id=x_time_id,
        quota=x_quota,
        _net_purviews=get_empty_dict_if_none(net_purviews),
        _magnitude=get_0_if_None(x_magnitude),
    )


@dataclass
class PurviewLog:
    owner_id: OwnerID = None
    episodes: dict[TimeLinePoint, PurviewEpisode] = None
    _sum_purviewepisode_quota: FundNum = None
    _sum_acct_purviews: int = None
    _time_id_min: TimeLinePoint = None
    _time_id_max: TimeLinePoint = None

    def set_episode(self, x_episode: PurviewEpisode):
        self.episodes[x_episode.time_id] = x_episode

    def add_episode(self, x_time_id: TimeLinePoint, x_quota: FundNum):
        self.set_episode(purviewepisode_shop(x_time_id, x_quota))

    def episode_exists(self, x_time_id: TimeLinePoint) -> bool:
        return self.episodes.get(x_time_id) != None

    def get_episode(self, x_time_id: TimeLinePoint) -> PurviewEpisode:
        return self.episodes.get(x_time_id)

    def del_episode(self, x_time_id: TimeLinePoint):
        self.episodes.pop(x_time_id)

    def get_2d_array(self) -> list[list]:
        return [
            [self.owner_id, x_episode.time_id, x_episode.quota]
            for x_episode in self.episodes.values()
        ]

    def get_headers(self) -> list:
        return ["owner_id", "time_id", "quota"]

    def get_dict(self) -> dict:
        return {"owner_id": self.owner_id, "episodes": self._get_episodes_dict()}

    def _get_episodes_dict(self) -> dict:
        return {
            x_episode.time_id: x_episode.get_dict()
            for x_episode in self.episodes.values()
        }

    def get_time_ids(self) -> set[TimeLinePoint]:
        return set(self.episodes.keys())

    def get_tranbook(self, fiscal_id: FiscalID) -> TranBook:
        x_tranbook = tranbook_shop(fiscal_id)
        for x_time_id, x_episode in self.episodes.items():
            for dst_acct_id, x_quota in x_episode._net_purviews.items():
                x_tranbook.add_tranunit(
                    x_owner_id=self.owner_id,
                    x_acct_id=dst_acct_id,
                    x_time_id=x_time_id,
                    x_amount=x_quota,
                )
        return x_tranbook


def purviewlog_shop(owner_id: OwnerID) -> PurviewLog:
    return PurviewLog(owner_id=owner_id, episodes={}, _sum_acct_purviews={})


def get_purviewepisode_from_dict(x_dict: dict) -> PurviewEpisode:
    x_time_id = x_dict.get("time_id")
    x_quota = x_dict.get("quota")
    x_net_purviews = x_dict.get("net_purviews")
    x_magnitude = x_dict.get("magnitude")
    return purviewepisode_shop(x_time_id, x_quota, x_net_purviews, x_magnitude)


def get_purviewepisode_from_json(x_json: str) -> PurviewEpisode:
    return get_purviewepisode_from_dict(get_dict_from_json(x_json))


def get_purviewlog_from_dict(x_dict: dict) -> PurviewLog:
    x_owner_id = x_dict.get("owner_id")
    x_purviewlog = purviewlog_shop(x_owner_id)
    x_purviewlog.episodes = get_episodes_from_dict(x_dict.get("episodes"))
    return x_purviewlog


def get_episodes_from_dict(episodes_dict: dict) -> dict[TimeLinePoint, PurviewEpisode]:
    x_dict = {}
    for x_episode_dict in episodes_dict.values():
        x_purview_episode = get_purviewepisode_from_dict(x_episode_dict)
        x_dict[x_purview_episode.time_id] = x_purview_episode
    return x_dict


@dataclass
class TimeConversion:
    fiscal_id: str = None
    addin: str = None


def timeconversion_shop(
    fiscal_id: FiscalID = None, addin: int = None
) -> TimeConversion:
    if fiscal_id is None:
        fiscal_id = get_default_fiscal_id_roadnode()
    if addin is None:
        addin = 0
    return TimeConversion(fiscal_id=fiscal_id, addin=addin)
