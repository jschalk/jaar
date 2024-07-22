from src._instrument.python import get_1_if_None, get_dict_from_json, get_0_if_None
from src._road.road import (
    AcctID,
    default_road_delimiter_if_none,
    validate_roadnode,
    is_roadnode,
)
from src._road.finance import default_bit_if_none, RespectNum, allot_scale
from src.bud.lobby import (
    LobbyID,
    LobbyShip,
    lobbyships_get_from_dict,
    lobbyship_shop,
)
from dataclasses import dataclass


class InvalidAcctException(Exception):
    pass


class Bad_acct_idLobbyShipException(Exception):
    pass


@dataclass
class AcctCore:
    acct_id: AcctID = None
    _road_delimiter: str = None
    _bit: float = None

    def set_acct_id(self, x_acct_id: AcctID):
        self.acct_id = validate_roadnode(x_acct_id, self._road_delimiter)


@dataclass
class AcctUnit(AcctCore):
    """This represents the BudUnit._owner_id's opinion of the AcctUnit.acct_id
    AcctUnit.credit_score represents how much credit_score the _owner_id projects to the acct_id
    AcctUnit.debtit_score represents how much debtit_score the _owner_id projects to the acct_id
    """

    credit_score: int = None
    debtit_score: int = None
    # special attribute: static in bud json, in memory it is deleted after loading and recalculated during saving.
    _lobbyships: dict[AcctID, LobbyShip] = None
    # calculated fields
    _credor_pool: RespectNum = None
    _debtor_pool: RespectNum = None
    _irrational_debtit_score: int = None  # set by listening process
    _inallocable_debtit_score: int = None  # set by listening process
    # set by Bud.settle_bud()
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _fund_agenda_ratio_give: float = None
    _fund_agenda_ratio_take: float = None

    def set_bit(self, x_bit: float):
        self._bit = x_bit

    def set_credor_debtit_score(
        self,
        credit_score: float = None,
        debtit_score: float = None,
    ):
        if credit_score is not None:
            self.set_credit_score(credit_score)
        if debtit_score is not None:
            self.set_debtit_score(debtit_score)

    def set_credit_score(self, credit_score: int):
        self.credit_score = credit_score

    def set_debtit_score(self, debtit_score: int):
        self.debtit_score = debtit_score

    def get_credit_score(self):
        return get_1_if_None(self.credit_score)

    def get_debtit_score(self):
        return get_1_if_None(self.debtit_score)

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        self._fund_agenda_ratio_give = 0
        self._fund_agenda_ratio_take = 0

    def add_irrational_debtit_score(self, x_irrational_debtit_score: float):
        self._irrational_debtit_score += x_irrational_debtit_score

    def add_inallocable_debtit_score(self, x_inallocable_debtit_score: float):
        self._inallocable_debtit_score += x_inallocable_debtit_score

    def reset_listen_calculated_attrs(self):
        self._irrational_debtit_score = 0
        self._inallocable_debtit_score = 0

    def add_fund_give(self, fund_give: float):
        self._fund_give += fund_give

    def add_fund_take(self, fund_take: float):
        self._fund_take += fund_take

    def add_fund_give_take(
        self,
        fund_give: float,
        fund_take,
        bud_agenda_cred: float,
        bud_agenda_debt,
    ):
        self.add_fund_give(fund_give)
        self.add_fund_take(fund_take)
        self._fund_agenda_give += bud_agenda_cred
        self._fund_agenda_take += bud_agenda_debt

    def set_fund_agenda_ratio_give_take(
        self,
        fund_agenda_ratio_give_sum: float,
        fund_agenda_ratio_take_sum: float,
        bud_acctunit_total_credit_score: float,
        bud_acctunit_total_debtit_score: float,
    ):
        if fund_agenda_ratio_give_sum == 0:
            self._fund_agenda_ratio_give = (
                self.get_credit_score() / bud_acctunit_total_credit_score
            )
        else:
            self._fund_agenda_ratio_give = (
                self._fund_agenda_give / fund_agenda_ratio_give_sum
            )

        if fund_agenda_ratio_take_sum == 0:
            self._fund_agenda_ratio_take = (
                self.get_debtit_score() / bud_acctunit_total_debtit_score
            )
        else:
            self._fund_agenda_ratio_take = (
                self._fund_agenda_take / fund_agenda_ratio_take_sum
            )

    def add_lobbyship(
        self,
        lobby_id: LobbyID,
        credit_score: float = None,
        debtit_score: float = None,
    ):
        x_lobbyship = lobbyship_shop(lobby_id, credit_score, debtit_score)
        self.set_lobbyship(x_lobbyship)

    def set_lobbyship(self, x_lobbyship: LobbyShip):
        x_lobby_id = x_lobbyship.lobby_id
        lobby_id_is_acct_id = is_roadnode(x_lobby_id, self._road_delimiter)
        if lobby_id_is_acct_id and self.acct_id != x_lobby_id:
            raise Bad_acct_idLobbyShipException(
                f"AcctUnit with acct_id='{self.acct_id}' cannot have link to '{x_lobby_id}'."
            )

        x_lobbyship._acct_id = self.acct_id
        self._lobbyships[x_lobbyship.lobby_id] = x_lobbyship

    def get_lobbyship(self, lobby_id: LobbyID) -> LobbyShip:
        return self._lobbyships.get(lobby_id)

    def lobbyship_exists(self, lobby_id: LobbyID) -> bool:
        return self._lobbyships.get(lobby_id) is not None

    def delete_lobbyship(self, lobby_id: LobbyID):
        return self._lobbyships.pop(lobby_id)

    def lobbyships_exist(self):
        return len(self._lobbyships) != 0

    def clear_lobbyships(self):
        self._lobbyships = {}

    def set_credor_pool(self, credor_pool: RespectNum):
        self._credor_pool = credor_pool
        ledger_dict = {
            x_lobbyship.lobby_id: x_lobbyship.credit_score
            for x_lobbyship in self._lobbyships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._credor_pool, self._bit)
        for x_lobby_id, lobby_credor_pool in allot_dict.items():
            self.get_lobbyship(x_lobby_id)._credor_pool = lobby_credor_pool

    def set_debtor_pool(self, debtor_pool: RespectNum):
        self._debtor_pool = debtor_pool
        ledger_dict = {
            x_lobbyship.lobby_id: x_lobbyship.debtit_score
            for x_lobbyship in self._lobbyships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._debtor_pool, self._bit)
        for x_lobby_id, lobby_debtor_pool in allot_dict.items():
            self.get_lobbyship(x_lobby_id)._debtor_pool = lobby_debtor_pool

    def get_lobbyships_dict(self) -> dict:
        return {
            x_lobbyship.lobby_id: {
                "lobby_id": x_lobbyship.lobby_id,
                "credit_score": x_lobbyship.credit_score,
                "debtit_score": x_lobbyship.debtit_score,
            }
            for x_lobbyship in self._lobbyships.values()
        }

    def get_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {
            "acct_id": self.acct_id,
            "credit_score": self.credit_score,
            "debtit_score": self.debtit_score,
            "_lobbyships": self.get_lobbyships_dict(),
        }
        if self._irrational_debtit_score not in [None, 0]:
            x_dict["_irrational_debtit_score"] = self._irrational_debtit_score
        if self._inallocable_debtit_score not in [None, 0]:
            x_dict["_inallocable_debtit_score"] = self._inallocable_debtit_score

        if all_attrs:
            self._all_attrs_necessary_in_dict(x_dict)
        return x_dict

    def _all_attrs_necessary_in_dict(self, x_dict):
        x_dict["_fund_give"] = self._fund_give
        x_dict["_fund_take"] = self._fund_take
        x_dict["_fund_agenda_give"] = self._fund_agenda_give
        x_dict["_fund_agenda_take"] = self._fund_agenda_take
        x_dict["_fund_agenda_ratio_give"] = self._fund_agenda_ratio_give
        x_dict["_fund_agenda_ratio_take"] = self._fund_agenda_ratio_take


# class AcctUnitsshop:
def acctunits_get_from_json(acctunits_json: str) -> dict[str, AcctUnit]:
    acctunits_dict = get_dict_from_json(json_x=acctunits_json)
    return acctunits_get_from_dict(x_dict=acctunits_dict)


def acctunits_get_from_dict(
    x_dict: dict, _road_delimiter: str = None
) -> dict[str, AcctUnit]:
    acctunits = {}
    for acctunit_dict in x_dict.values():
        x_acctunit = acctunit_get_from_dict(acctunit_dict, _road_delimiter)
        acctunits[x_acctunit.acct_id] = x_acctunit
    return acctunits


def acctunit_get_from_dict(acctunit_dict: dict, _road_delimiter: str) -> AcctUnit:
    x_acct_id = acctunit_dict["acct_id"]
    x_credit_score = acctunit_dict["credit_score"]
    x_debtit_score = acctunit_dict["debtit_score"]
    x_lobbyships_dict = acctunit_dict["_lobbyships"]
    x_acctunit = acctunit_shop(
        x_acct_id, x_credit_score, x_debtit_score, _road_delimiter
    )
    x_acctunit._lobbyships = lobbyships_get_from_dict(x_lobbyships_dict, x_acct_id)
    _irrational_debtit_score = acctunit_dict.get("_irrational_debtit_score", 0)
    _inallocable_debtit_score = acctunit_dict.get("_inallocable_debtit_score", 0)
    x_acctunit.add_irrational_debtit_score(get_0_if_None(_irrational_debtit_score))
    x_acctunit.add_inallocable_debtit_score(get_0_if_None(_inallocable_debtit_score))

    return x_acctunit


def acctunit_shop(
    acct_id: AcctID,
    credit_score: int = None,
    debtit_score: int = None,
    _road_delimiter: str = None,
    _bit: float = None,
) -> AcctUnit:
    x_acctunit = AcctUnit(
        credit_score=get_1_if_None(credit_score),
        debtit_score=get_1_if_None(debtit_score),
        _lobbyships={},
        _credor_pool=0,
        _debtor_pool=0,
        _irrational_debtit_score=0,
        _inallocable_debtit_score=0,
        _fund_give=0,
        _fund_take=0,
        _fund_agenda_give=0,
        _fund_agenda_take=0,
        _fund_agenda_ratio_give=0,
        _fund_agenda_ratio_take=0,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _bit=default_bit_if_none(_bit),
    )
    x_acctunit.set_acct_id(x_acct_id=acct_id)
    return x_acctunit
