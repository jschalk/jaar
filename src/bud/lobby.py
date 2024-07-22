from src._instrument.python import get_1_if_None, get_dict_from_json
from src._road.finance import allot_scale, FundCoin, default_fund_coin_if_none
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
    credit_score: float = 1.0
    debtit_score: float = 1.0
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

    def set_credit_score(self, x_credit_score: float):
        if x_credit_score is not None:
            self.credit_score = x_credit_score

    def set_debtit_score(self, x_debtit_score: float):
        if x_debtit_score is not None:
            self.debtit_score = x_debtit_score

    def get_dict(self) -> dict[str, str]:
        return {
            "lobby_id": self.lobby_id,
            "credit_score": self.credit_score,
            "debtit_score": self.debtit_score,
        }

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        self._fund_agenda_ratio_give = 0
        self._fund_agenda_ratio_take = 0


def lobbyship_shop(
    lobby_id: LobbyID,
    credit_score: float = None,
    debtit_score: float = None,
    _acct_id: AcctID = None,
) -> LobbyShip:
    return LobbyShip(
        lobby_id=lobby_id,
        credit_score=get_1_if_None(credit_score),
        debtit_score=get_1_if_None(debtit_score),
        _credor_pool=0,
        _debtor_pool=0,
        _acct_id=_acct_id,
    )


def lobbyship_get_from_dict(x_dict: dict, x_acct_id: AcctID) -> LobbyShip:
    return lobbyship_shop(
        lobby_id=x_dict.get("lobby_id"),
        credit_score=x_dict.get("credit_score"),
        debtit_score=x_dict.get("debtit_score"),
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
        self.validate_fund_give_fund_take()
        self._fund_give += fund_give
        self._fund_take += fund_take

    def validate_fund_give_fund_take(self):
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
    _fund_coin: FundCoin = None

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

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        for lobbyship in self._lobbyships.values():
            lobbyship.clear_fund_give_take()

    def _set_lobbyship_fund_give_fund_take(self):
        credit_ledger = {}
        debtit_ledger = {}
        for x_acct_id, x_lobbyship in self._lobbyships.items():
            credit_ledger[x_acct_id] = x_lobbyship.credit_score
            debtit_ledger[x_acct_id] = x_lobbyship.debtit_score
        fund_give_allot = allot_scale(credit_ledger, self._fund_give, self._fund_coin)
        fund_take_allot = allot_scale(debtit_ledger, self._fund_take, self._fund_coin)
        for acct_id, x_lobbyship in self._lobbyships.items():
            x_lobbyship._fund_give = fund_give_allot.get(acct_id)
            x_lobbyship._fund_take = fund_take_allot.get(acct_id)
        x_a_give = self._fund_agenda_give
        x_a_take = self._fund_agenda_take
        fund_agenda_give_allot = allot_scale(credit_ledger, x_a_give, self._fund_coin)
        fund_agenda_take_allot = allot_scale(debtit_ledger, x_a_take, self._fund_coin)
        for acct_id, x_lobbyship in self._lobbyships.items():
            x_lobbyship._fund_agenda_give = fund_agenda_give_allot.get(acct_id)
            x_lobbyship._fund_agenda_take = fund_agenda_take_allot.get(acct_id)


def lobbybox_shop(
    lobby_id: LobbyID, _road_delimiter: str = None, _fund_coin: FundCoin = None
) -> LobbyBox:
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
        _fund_coin=default_fund_coin_if_none(_fund_coin),
    )
    # x_lobbybox.set_lobby_id(lobby_id=lobby_id)
    # return x_lobbybox
