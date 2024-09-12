from src._instrument.python_tool import get_1_if_None, get_dict_from_json, get_0_if_None
from src._road.road import (
    AcctID,
    default_road_delimiter_if_none,
    validate_roadnode,
    is_roadnode,
)
from src._road.finance import default_bit_if_none, RespectNum, allot_scale
from src.bud.group import (
    GroupID,
    MemberShip,
    memberships_get_from_dict,
    membership_shop,
)
from dataclasses import dataclass


class InvalidAcctException(Exception):
    pass


class Bad_acct_idMemberShipException(Exception):
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
    AcctUnit.credit_belief represents how much credit_belief the _owner_id projects to the acct_id
    AcctUnit.debtit_belief represents how much debtit_belief the _owner_id projects to the acct_id
    """

    credit_belief: int = None
    debtit_belief: int = None
    # special attribute: static in bud json, in memory it is deleted after loading and recalculated during saving.
    _memberships: dict[AcctID, MemberShip] = None
    # calculated fields
    _credor_pool: RespectNum = None
    _debtor_pool: RespectNum = None
    _irrational_debtit_belief: int = None  # set by listening process
    _inallocable_debtit_belief: int = None  # set by listening process
    # set by Bud.settle_bud()
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _fund_agenda_ratio_give: float = None
    _fund_agenda_ratio_take: float = None

    def set_bit(self, x_bit: float):
        self._bit = x_bit

    def set_credor_debtit_belief(
        self,
        credit_belief: float = None,
        debtit_belief: float = None,
    ):
        if credit_belief is not None:
            self.set_credit_belief(credit_belief)
        if debtit_belief is not None:
            self.set_debtit_belief(debtit_belief)

    def set_credit_belief(self, credit_belief: int):
        self.credit_belief = credit_belief

    def set_debtit_belief(self, debtit_belief: int):
        self.debtit_belief = debtit_belief

    def get_credit_belief(self):
        return get_1_if_None(self.credit_belief)

    def get_debtit_belief(self):
        return get_1_if_None(self.debtit_belief)

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        self._fund_agenda_ratio_give = 0
        self._fund_agenda_ratio_take = 0

    def add_irrational_debtit_belief(self, x_irrational_debtit_belief: float):
        self._irrational_debtit_belief += x_irrational_debtit_belief

    def add_inallocable_debtit_belief(self, x_inallocable_debtit_belief: float):
        self._inallocable_debtit_belief += x_inallocable_debtit_belief

    def reset_listen_calculated_attrs(self):
        self._irrational_debtit_belief = 0
        self._inallocable_debtit_belief = 0

    def add_fund_give(self, fund_give: float):
        self._fund_give += fund_give

    def add_fund_take(self, fund_take: float):
        self._fund_take += fund_take

    def add_fund_agenda_give(self, fund_agenda_give: float):
        self._fund_agenda_give += fund_agenda_give

    def add_fund_agenda_take(self, fund_agenda_take: float):
        self._fund_agenda_take += fund_agenda_take

    def add_fund_give_take(
        self,
        fund_give: float,
        fund_take,
        fund_agenda_give: float,
        fund_agenda_take,
    ):
        self.add_fund_give(fund_give)
        self.add_fund_take(fund_take)
        self._fund_agenda_give += fund_agenda_give
        self._fund_agenda_take += fund_agenda_take

    def set_fund_agenda_ratio_give_take(
        self,
        fund_agenda_ratio_give_sum: float,
        fund_agenda_ratio_take_sum: float,
        bud_acctunit_total_credit_belief: float,
        bud_acctunit_total_debtit_belief: float,
    ):
        total_credit_belief = bud_acctunit_total_credit_belief
        ratio_give_sum = fund_agenda_ratio_give_sum
        self._fund_agenda_ratio_give = (
            self.get_credit_belief() / total_credit_belief
            if fund_agenda_ratio_give_sum == 0
            else self._fund_agenda_give / ratio_give_sum
        )
        if fund_agenda_ratio_take_sum == 0:
            total_debtit_belief = bud_acctunit_total_debtit_belief
            self._fund_agenda_ratio_take = (
                self.get_debtit_belief() / total_debtit_belief
            )
        else:
            ratio_take_sum = fund_agenda_ratio_take_sum
            self._fund_agenda_ratio_take = self._fund_agenda_take / ratio_take_sum

    def add_membership(
        self,
        group_id: GroupID,
        credit_vote: float = None,
        debtit_vote: float = None,
    ):
        x_membership = membership_shop(group_id, credit_vote, debtit_vote)
        self.set_membership(x_membership)

    def set_membership(self, x_membership: MemberShip):
        x_group_id = x_membership.group_id
        group_id_is_acct_id = is_roadnode(x_group_id, self._road_delimiter)
        if group_id_is_acct_id and self.acct_id != x_group_id:
            raise Bad_acct_idMemberShipException(
                f"AcctUnit with acct_id='{self.acct_id}' cannot have link to '{x_group_id}'."
            )

        x_membership._acct_id = self.acct_id
        self._memberships[x_membership.group_id] = x_membership

    def get_membership(self, group_id: GroupID) -> MemberShip:
        return self._memberships.get(group_id)

    def membership_exists(self, group_id: GroupID) -> bool:
        return self._memberships.get(group_id) is not None

    def delete_membership(self, group_id: GroupID):
        return self._memberships.pop(group_id)

    def memberships_exist(self):
        return len(self._memberships) != 0

    def clear_memberships(self):
        self._memberships = {}

    def set_credor_pool(self, credor_pool: RespectNum):
        self._credor_pool = credor_pool
        ledger_dict = {
            x_membership.group_id: x_membership.credit_vote
            for x_membership in self._memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._credor_pool, self._bit)
        for x_group_id, group_credor_pool in allot_dict.items():
            self.get_membership(x_group_id)._credor_pool = group_credor_pool

    def set_debtor_pool(self, debtor_pool: RespectNum):
        self._debtor_pool = debtor_pool
        ledger_dict = {
            x_membership.group_id: x_membership.debtit_vote
            for x_membership in self._memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._debtor_pool, self._bit)
        for x_group_id, group_debtor_pool in allot_dict.items():
            self.get_membership(x_group_id)._debtor_pool = group_debtor_pool

    def get_memberships_dict(self) -> dict:
        return {
            x_membership.group_id: {
                "group_id": x_membership.group_id,
                "credit_vote": x_membership.credit_vote,
                "debtit_vote": x_membership.debtit_vote,
            }
            for x_membership in self._memberships.values()
        }

    def get_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {
            "acct_id": self.acct_id,
            "credit_belief": self.credit_belief,
            "debtit_belief": self.debtit_belief,
            "_memberships": self.get_memberships_dict(),
        }
        if self._irrational_debtit_belief not in [None, 0]:
            x_dict["_irrational_debtit_belief"] = self._irrational_debtit_belief
        if self._inallocable_debtit_belief not in [None, 0]:
            x_dict["_inallocable_debtit_belief"] = self._inallocable_debtit_belief

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
    acctunits_dict = get_dict_from_json(acctunits_json)
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
    x_credit_belief = acctunit_dict["credit_belief"]
    x_debtit_belief = acctunit_dict["debtit_belief"]
    x_memberships_dict = acctunit_dict["_memberships"]
    x_acctunit = acctunit_shop(
        x_acct_id, x_credit_belief, x_debtit_belief, _road_delimiter
    )
    x_acctunit._memberships = memberships_get_from_dict(x_memberships_dict, x_acct_id)
    _irrational_debtit_belief = acctunit_dict.get("_irrational_debtit_belief", 0)
    _inallocable_debtit_belief = acctunit_dict.get("_inallocable_debtit_belief", 0)
    x_acctunit.add_irrational_debtit_belief(get_0_if_None(_irrational_debtit_belief))
    x_acctunit.add_inallocable_debtit_belief(get_0_if_None(_inallocable_debtit_belief))

    return x_acctunit


def acctunit_shop(
    acct_id: AcctID,
    credit_belief: int = None,
    debtit_belief: int = None,
    _road_delimiter: str = None,
    _bit: float = None,
) -> AcctUnit:
    x_acctunit = AcctUnit(
        credit_belief=get_1_if_None(credit_belief),
        debtit_belief=get_1_if_None(debtit_belief),
        _memberships={},
        _credor_pool=0,
        _debtor_pool=0,
        _irrational_debtit_belief=0,
        _inallocable_debtit_belief=0,
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
