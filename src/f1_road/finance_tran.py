from src.f0_instrument.dict_tool import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_json_from_dict,
    get_dict_from_json,
    place_obj_in_dict,
    create_csv,
)
from src.f1_road.finance import FundNum, TimeLinePoint, default_fund_pool
from src.f1_road.road import AcctID, OwnerID, FiscalID
from dataclasses import dataclass


class calc_magnitudeException(Exception):
    pass


@dataclass
class PurviewEpisode:
    timestamp: TimeLinePoint = None
    amount: FundNum = None
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
            exception_text = f"magnitude cannot be calculated: debt_purview={x_debt_sum}, cred_purview={x_cred_sum}"
            raise calc_magnitudeException(exception_text)
        self._magnitude = x_cred_sum

    def get_dict(self) -> dict[str,]:
        x_dict = {"timestamp": self.timestamp, "amount": self.amount}
        if self._net_purviews:
            x_dict["net_purviews"] = self._net_purviews
        if self._magnitude:
            x_dict["magnitude"] = self._magnitude
        return x_dict

    def get_json(self) -> dict[str,]:
        return get_json_from_dict(self.get_dict())


def purviewepisode_shop(
    x_timestamp: TimeLinePoint,
    x_amount: FundNum = None,
    net_purviews: dict[AcctID, FundNum] = None,
    x_magnitude: FundNum = None,
) -> PurviewEpisode:
    if x_amount is None:
        x_amount = default_fund_pool()

    return PurviewEpisode(
        timestamp=x_timestamp,
        amount=x_amount,
        _net_purviews=get_empty_dict_if_none(net_purviews),
        _magnitude=get_0_if_None(x_magnitude),
    )


@dataclass
class PurviewLog:
    owner_id: OwnerID = None
    episodes: dict[TimeLinePoint, PurviewEpisode] = None
    _sum_purviewepisode_amount: FundNum = None
    _sum_acct_purviews: int = None
    _timestamp_min: TimeLinePoint = None
    _timestamp_max: TimeLinePoint = None

    def set_episode(self, x_episode: PurviewEpisode):
        self.episodes[x_episode.timestamp] = x_episode

    def add_episode(self, x_timestamp: TimeLinePoint, x_amount: FundNum):
        self.set_episode(purviewepisode_shop(x_timestamp, x_amount))

    def episode_exists(self, x_timestamp: TimeLinePoint) -> bool:
        return self.episodes.get(x_timestamp) != None

    def get_episode(self, x_timestamp: TimeLinePoint) -> PurviewEpisode:
        return self.episodes.get(x_timestamp)

    def del_episode(self, x_timestamp: TimeLinePoint):
        self.episodes.pop(x_timestamp)

    def get_2d_array(self) -> list[list]:
        return [
            [self.owner_id, x_episode.timestamp, x_episode.amount]
            for x_episode in self.episodes.values()
        ]

    def get_headers(self) -> list:
        return ["owner_id", "timestamp", "amount"]

    def get_dict(self) -> dict:
        return {"owner_id": self.owner_id, "episodes": self._get_episodes_dict()}

    def _get_episodes_dict(self) -> dict:
        return {
            x_episode.timestamp: x_episode.get_dict()
            for x_episode in self.episodes.values()
        }


def purviewlog_shop(owner_id: OwnerID) -> PurviewLog:
    return PurviewLog(owner_id=owner_id, episodes={}, _sum_acct_purviews={})


def get_purviewepisode_from_dict(x_dict: dict) -> PurviewEpisode:
    x_timestamp = x_dict.get("timestamp")
    x_amount = x_dict.get("amount")
    x_net_purviews = x_dict.get("net_purviews")
    x_magnitude = x_dict.get("magnitude")
    return purviewepisode_shop(x_timestamp, x_amount, x_net_purviews, x_magnitude)


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
        x_dict[x_purview_episode.timestamp] = x_purview_episode
    return x_dict


@dataclass
class TranBook:
    fiscal_id: FiscalID = None
    tranlogs: dict[OwnerID, dict[AcctID, dict[TimeLinePoint, FundNum]]] = None
    _accts_net: dict[OwnerID, dict[AcctID, FundNum]] = None

    def set_tranlog(
        self,
        x_owner_id: OwnerID,
        x_acct_id: AcctID,
        x_timestamp: TimeLinePoint,
        x_amount: FundNum,
    ):
        x_keylist = [x_owner_id, x_acct_id, x_timestamp]
        place_obj_in_dict(self.tranlogs, x_keylist, x_amount)

    def get_owners_accts_net(self) -> dict[OwnerID, dict[AcctID, FundNum]]:
        owners_accts_net_dict = {}
        for owner_id, owner_dict in self.tranlogs.items():
            for acct_id, acct_dict in owner_dict.items():
                if owners_accts_net_dict.get(owner_id) is None:
                    owners_accts_net_dict[owner_id] = {}
                owner_net_dict = owners_accts_net_dict.get(owner_id)
                owner_net_dict[acct_id] = sum(acct_dict.values())
        return owners_accts_net_dict

    def get_accts_net_dict(self) -> dict[AcctID, FundNum]:
        accts_net_dict = {}
        for owner_dict in self.tranlogs.values():
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
        print(f"{self._get_accts_net_array()=}")
        return create_csv(self._get_accts_headers(), self._get_accts_net_array())

    # def get_dict(
    #     self,
    # ) -> dict[FiscalID, dict[OwnerID, dict[AcctID, dict[TimeLinePoint, FundNum]]]]:
    #     return {"fiscal_id": self.fiscal_id}


def tranbook_shop(
    x_fiscal_id: FiscalID,
    x_tranlogs: dict[OwnerID, dict[AcctID, dict[TimeLinePoint, FundNum]]] = None,
):
    return TranBook(
        fiscal_id=x_fiscal_id,
        tranlogs=get_empty_dict_if_none(x_tranlogs),
        _accts_net={},
    )


def get_tranbook_from_dict():
    pass


def get_tranbook_from_json():
    pass