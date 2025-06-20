from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_dict_from_json,
)
from src.a01_term_logic.rope import (
    default_knot_if_None,
    is_labelterm,
    validate_labelterm,
)
from src.a01_term_logic.term import AcctName
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import RespectNum, default_RespectBit_if_None
from src.a03_group_logic.group import (
    GroupTitle,
    MemberShip,
    membership_shop,
    memberships_get_from_dict,
)


class InvalidAcctException(Exception):
    pass


class Bad_acct_nameMemberShipException(Exception):
    pass


@dataclass
class AcctCore:
    acct_name: AcctName = None
    knot: str = None
    respect_bit: float = None

    def set_nameterm(self, x_acct_name: AcctName):
        self.acct_name = validate_labelterm(x_acct_name, self.knot)


@dataclass
class AcctUnit(AcctCore):
    """This represents the owner_name's opinion of the AcctUnit.acct_name
    AcctUnit.credit_score represents how much credit_score the _owner_name projects to the acct_name
    AcctUnit.debt_score represents how much debt_score the _owner_name projects to the acct_name
    """

    credit_score: int = None
    debt_score: int = None
    # special attribute: static in plan json, in memory it is deleted after loading and recalculated during saving.
    _memberships: dict[AcctName, MemberShip] = None
    # calculated fields
    _credor_pool: RespectNum = None
    _debtor_pool: RespectNum = None
    _irrational_debt_score: int = None  # set by listening process
    _inallocable_debt_score: int = None  # set by listening process
    # set by Plan.settle_plan()
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _fund_agenda_ratio_give: float = None
    _fund_agenda_ratio_take: float = None

    def set_respect_bit(self, x_respect_bit: float):
        self.respect_bit = x_respect_bit

    def set_credor_debt_score(
        self,
        credit_score: float = None,
        debt_score: float = None,
    ):
        if credit_score is not None:
            self.set_credit_score(credit_score)
        if debt_score is not None:
            self.set_debt_score(debt_score)

    def set_credit_score(self, credit_score: int):
        self.credit_score = credit_score

    def set_debt_score(self, debt_score: int):
        self.debt_score = debt_score

    def get_credit_score(self):
        return get_1_if_None(self.credit_score)

    def get_debt_score(self):
        return get_1_if_None(self.debt_score)

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        self._fund_agenda_ratio_give = 0
        self._fund_agenda_ratio_take = 0

    def add_irrational_debt_score(self, x_irrational_debt_score: float):
        self._irrational_debt_score += x_irrational_debt_score

    def add_inallocable_debt_score(self, x_inallocable_debt_score: float):
        self._inallocable_debt_score += x_inallocable_debt_score

    def reset_listen_calculated_attrs(self):
        self._irrational_debt_score = 0
        self._inallocable_debt_score = 0

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
        self.add_fund_agenda_give(fund_agenda_give)
        self.add_fund_agenda_take(fund_agenda_take)

    def set_fund_agenda_ratio_give_take(
        self,
        fund_agenda_ratio_give_sum: float,
        fund_agenda_ratio_take_sum: float,
        acctunits_credit_score_sum: float,
        acctunits_debt_score_sum: float,
    ):
        total_credit_score = acctunits_credit_score_sum
        ratio_give_sum = fund_agenda_ratio_give_sum
        self._fund_agenda_ratio_give = (
            self.get_credit_score() / total_credit_score
            if fund_agenda_ratio_give_sum == 0
            else self._fund_agenda_give / ratio_give_sum
        )
        if fund_agenda_ratio_take_sum == 0:
            total_debt_score = acctunits_debt_score_sum
            self._fund_agenda_ratio_take = self.get_debt_score() / total_debt_score
        else:
            ratio_take_sum = fund_agenda_ratio_take_sum
            self._fund_agenda_ratio_take = self._fund_agenda_take / ratio_take_sum

    def add_membership(
        self,
        group_title: GroupTitle,
        credit_vote: float = None,
        debt_vote: float = None,
    ):
        x_membership = membership_shop(group_title, credit_vote, debt_vote)
        self.set_membership(x_membership)

    def set_membership(self, x_membership: MemberShip):
        x_group_title = x_membership.group_title
        group_title_is_acct_name = is_labelterm(x_group_title, self.knot)
        if group_title_is_acct_name and self.acct_name != x_group_title:
            raise Bad_acct_nameMemberShipException(
                f"AcctUnit with acct_name='{self.acct_name}' cannot have link to '{x_group_title}'."
            )

        x_membership.acct_name = self.acct_name
        self._memberships[x_membership.group_title] = x_membership

    def get_membership(self, group_title: GroupTitle) -> MemberShip:
        return self._memberships.get(group_title)

    def membership_exists(self, group_title: GroupTitle) -> bool:
        return self._memberships.get(group_title) is not None

    def delete_membership(self, group_title: GroupTitle):
        return self._memberships.pop(group_title)

    def memberships_exist(self):
        return len(self._memberships) != 0

    def clear_memberships(self):
        self._memberships = {}

    def set_credor_pool(self, credor_pool: RespectNum):
        self._credor_pool = credor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.credit_vote
            for x_membership in self._memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._credor_pool, self.respect_bit)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title)._credor_pool = alloted_pool

    def set_debtor_pool(self, debtor_pool: RespectNum):
        self._debtor_pool = debtor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.debt_vote
            for x_membership in self._memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._debtor_pool, self.respect_bit)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title)._debtor_pool = alloted_pool

    def get_memberships_dict(self) -> dict:
        return {
            x_membership.group_title: x_membership.get_dict()
            for x_membership in self._memberships.values()
        }

    def get_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {
            "acct_name": self.acct_name,
            "credit_score": self.credit_score,
            "debt_score": self.debt_score,
            "_memberships": self.get_memberships_dict(),
        }
        if self._irrational_debt_score not in [None, 0]:
            x_dict["_irrational_debt_score"] = self._irrational_debt_score
        if self._inallocable_debt_score not in [None, 0]:
            x_dict["_inallocable_debt_score"] = self._inallocable_debt_score

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


def acctunits_get_from_json(acctunits_json: str) -> dict[str, AcctUnit]:
    acctunits_dict = get_dict_from_json(acctunits_json)
    return acctunits_get_from_dict(x_dict=acctunits_dict)


def acctunits_get_from_dict(x_dict: dict, _knot: str = None) -> dict[str, AcctUnit]:
    acctunits = {}
    for acctunit_dict in x_dict.values():
        x_acctunit = acctunit_get_from_dict(acctunit_dict, _knot)
        acctunits[x_acctunit.acct_name] = x_acctunit
    return acctunits


def acctunit_get_from_dict(acctunit_dict: dict, _knot: str) -> AcctUnit:
    x_acct_name = acctunit_dict["acct_name"]
    x_credit_score = acctunit_dict["credit_score"]
    x_debt_score = acctunit_dict["debt_score"]
    x_memberships_dict = acctunit_dict["_memberships"]
    x_acctunit = acctunit_shop(x_acct_name, x_credit_score, x_debt_score, _knot)
    x_acctunit._memberships = memberships_get_from_dict(x_memberships_dict, x_acct_name)
    _irrational_debt_score = acctunit_dict.get("_irrational_debt_score", 0)
    _inallocable_debt_score = acctunit_dict.get("_inallocable_debt_score", 0)
    x_acctunit.add_irrational_debt_score(get_0_if_None(_irrational_debt_score))
    x_acctunit.add_inallocable_debt_score(get_0_if_None(_inallocable_debt_score))

    return x_acctunit


def acctunit_shop(
    acct_name: AcctName,
    credit_score: int = None,
    debt_score: int = None,
    knot: str = None,
    respect_bit: float = None,
) -> AcctUnit:
    x_acctunit = AcctUnit(
        credit_score=get_1_if_None(credit_score),
        debt_score=get_1_if_None(debt_score),
        _memberships={},
        _credor_pool=0,
        _debtor_pool=0,
        _irrational_debt_score=0,
        _inallocable_debt_score=0,
        _fund_give=0,
        _fund_take=0,
        _fund_agenda_give=0,
        _fund_agenda_take=0,
        _fund_agenda_ratio_give=0,
        _fund_agenda_ratio_take=0,
        knot=default_knot_if_None(knot),
        respect_bit=default_RespectBit_if_None(respect_bit),
    )
    x_acctunit.set_nameterm(x_acct_name=acct_name)
    return x_acctunit
