from src._instrument.python import get_1_if_None, get_dict_from_json
from src._road.road import LobbyID, AcctID, default_road_delimiter_if_none
from dataclasses import dataclass


class InvalidLobbyException(Exception):
    pass


class lobbyship_lobby_id_Exception(Exception):
    pass


@dataclass
class LobbyCore:
    lobby_id: LobbyID = None


@dataclass
class LobbyShip(LobbyCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    # calculated fields
    _credor_pool: float = None
    _debtor_pool: float = None
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _fund_agenda_ratio_give: float = None
    _fund_agenda_ratio_take: float = None
    _acct_id: AcctID = None

    def set_credor_weight(self, x_credor_weight: float):
        if x_credor_weight is not None:
            self.credor_weight = x_credor_weight

    def set_debtor_weight(self, x_debtor_weight: float):
        if x_debtor_weight is not None:
            self.debtor_weight = x_debtor_weight

    def get_dict(self) -> dict[str, str]:
        return {
            "lobby_id": self.lobby_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def reset_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        self._fund_agenda_ratio_give = 0
        self._fund_agenda_ratio_take = 0

    def set_fund_give_take(
        self,
        lobbyships_credor_weight_sum: float,
        lobbyships_debtor_weight_sum: float,
        lobby_fund_give: float,
        lobby_fund_take: float,
        lobby_fund_agenda_give: float,
        lobby_fund_agenda_take: float,
    ):
        lobby_fund_give = get_1_if_None(lobby_fund_give)
        lobby_fund_take = get_1_if_None(lobby_fund_take)
        credor_ratio = self.credor_weight / lobbyships_credor_weight_sum
        debtor_ratio = self.debtor_weight / lobbyships_debtor_weight_sum

        self._fund_give = lobby_fund_give * credor_ratio
        self._fund_take = lobby_fund_take * debtor_ratio
        self._fund_agenda_give = lobby_fund_agenda_give * credor_ratio
        self._fund_agenda_take = lobby_fund_agenda_take * debtor_ratio


def lobbyship_shop(
    lobby_id: LobbyID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _acct_id: AcctID = None,
) -> LobbyShip:
    return LobbyShip(
        lobby_id=lobby_id,
        credor_weight=get_1_if_None(credor_weight),
        debtor_weight=get_1_if_None(debtor_weight),
        _credor_pool=0,
        _debtor_pool=0,
        _acct_id=_acct_id,
    )


def lobbyship_get_from_dict(x_dict: dict, x_acct_id: AcctID) -> LobbyShip:
    return lobbyship_shop(
        lobby_id=x_dict.get("lobby_id"),
        credor_weight=x_dict.get("credor_weight"),
        debtor_weight=x_dict.get("debtor_weight"),
        _acct_id=x_acct_id,
    )


def lobbyships_get_from_dict(
    x_dict: dict, x_acct_id: AcctID
) -> dict[LobbyID, LobbyShip]:
    return {
        x_lobby_id: lobbyship_get_from_dict(x_lobbyship_dict, x_acct_id)
        for x_lobby_id, x_lobbyship_dict in x_dict.items()
    }


@dataclass
class AwardLink(LobbyCore):
    give_force: float = 1.0
    take_force: float = 1.0

    def get_dict(self) -> dict[str, str]:
        return {
            "lobby_id": self.lobby_id,
            "give_force": self.give_force,
            "take_force": self.take_force,
        }


# class AwardLinksshop:
def awardlinks_get_from_json(awardlinks_json: str) -> dict[LobbyID, AwardLink]:
    awardlinks_dict = get_dict_from_json(json_x=awardlinks_json)
    return awardlinks_get_from_dict(x_dict=awardlinks_dict)


def awardlinks_get_from_dict(x_dict: dict) -> dict[LobbyID, AwardLink]:
    awardlinks = {}
    for awardlinks_dict in x_dict.values():
        x_lobby = awardlink_shop(
            lobby_id=awardlinks_dict["lobby_id"],
            give_force=awardlinks_dict["give_force"],
            take_force=awardlinks_dict["take_force"],
        )
        awardlinks[x_lobby.lobby_id] = x_lobby
    return awardlinks


def awardlink_shop(
    lobby_id: LobbyID, give_force: float = None, take_force: float = None
) -> AwardLink:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardLink(lobby_id, give_force, take_force=take_force)


@dataclass
class AwardHeir(LobbyCore):
    give_force: float = 1.0
    take_force: float = 1.0
    _fund_give: float = None
    _fund_take: float = None

    def set_fund_give_take(
        self,
        idea_fund_share,
        awardheirs_give_force_sum: float,
        awardheirs_take_force_sum: float,
    ):
        credor_share_ratio = self.give_force / awardheirs_give_force_sum
        self._fund_give = idea_fund_share * credor_share_ratio
        debtor_share_ratio = self.take_force / awardheirs_take_force_sum
        self._fund_take = idea_fund_share * debtor_share_ratio


def awardheir_shop(
    lobby_id: LobbyID,
    give_force: float = None,
    take_force: float = None,
    _fund_give: float = None,
    _fund_take: float = None,
) -> AwardHeir:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardHeir(lobby_id, give_force, take_force, _fund_give, _fund_take)


@dataclass
class AwardLine(LobbyCore):
    _fund_give: float = None
    _fund_take: float = None

    def add_fund_give_take(self, fund_give: float, fund_take: float):
        self.set_fund_give_take_zero_if_none()
        self._fund_give += fund_give
        self._fund_take += fund_take

    def set_fund_give_take_zero_if_none(self):
        if self._fund_give is None:
            self._fund_give = 0
        if self._fund_take is None:
            self._fund_take = 0


def awardline_shop(lobby_id: LobbyID, _fund_give: float, _fund_take: float):
    return AwardLine(lobby_id, _fund_give=_fund_give, _fund_take=_fund_take)


@dataclass
class LobbyBox(LobbyCore):
    _lobbyships: dict[AcctID, LobbyShip] = None  # set by BudUnit.set_acctunit()
    _road_delimiter: str = None  # calculated by BudUnit
    # calculated by BudUnit.settle_bud()
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _credor_pool: float = None
    _debtor_pool: float = None

    def set_lobbyship(self, x_lobbyship: LobbyShip):
        if x_lobbyship.lobby_id != self.lobby_id:
            raise lobbyship_lobby_id_Exception(
                f"LobbyBox.lobby_id={self.lobby_id} cannot set lobbyship.lobby_id={x_lobbyship.lobby_id}"
            )
        if x_lobbyship._acct_id is None:
            raise lobbyship_lobby_id_Exception(
                f"lobbyship lobby_id={x_lobbyship.lobby_id} cannot be set when _acct_id is None."
            )

        self._lobbyships[x_lobbyship._acct_id] = x_lobbyship
        self._add_credor_pool(x_lobbyship._credor_pool)
        self._add_debtor_pool(x_lobbyship._debtor_pool)

    def _add_credor_pool(self, x_credor_pool: float):
        self._credor_pool += x_credor_pool

    def _add_debtor_pool(self, x_debtor_pool: float):
        self._debtor_pool += x_debtor_pool

    def get_lobbyship(self, x_acct_id: AcctID) -> LobbyShip:
        return self._lobbyships.get(x_acct_id)

    def lobbyship_exists(self, x_acct_id: AcctID) -> bool:
        return self.get_lobbyship(x_acct_id) is not None

    def del_lobbyship(self, acct_id):
        self._lobbyships.pop(acct_id)

    def reset_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        for lobbyship in self._lobbyships.values():
            lobbyship.reset_fund_give_take()

    def _set_lobbyship_fund_give_take(self):
        lobbyships_credor_weight_sum = sum(
            lobbyship.credor_weight for lobbyship in self._lobbyships.values()
        )
        lobbyships_debtor_weight_sum = sum(
            lobbyship.debtor_weight for lobbyship in self._lobbyships.values()
        )

        for lobbyship in self._lobbyships.values():
            lobbyship.set_fund_give_take(
                lobbyships_credor_weight_sum=lobbyships_credor_weight_sum,
                lobbyships_debtor_weight_sum=lobbyships_debtor_weight_sum,
                lobby_fund_give=self._fund_give,
                lobby_fund_take=self._fund_take,
                lobby_fund_agenda_give=self._fund_agenda_give,
                lobby_fund_agenda_take=self._fund_agenda_take,
            )


def lobbybox_shop(lobby_id: LobbyID, _road_delimiter: str = None) -> LobbyBox:
    return LobbyBox(
        lobby_id=lobby_id,
        _lobbyships={},
        _fund_give=0,
        _fund_take=0,
        _fund_agenda_give=0,
        _fund_agenda_take=0,
        _credor_pool=0,
        _debtor_pool=0,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    # x_lobbybox.set_lobby_id(lobby_id=lobby_id)
    # return x_lobbybox
