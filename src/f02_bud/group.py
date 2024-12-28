from src.f00_instrument.dict_toolbox import get_1_if_None, get_dict_from_json
from src.f01_road.finance import allot_scale, FundCoin, default_fund_coin_if_None
from src.f01_road.road import GroupID, AcctName, default_bridge_if_None
from dataclasses import dataclass


class InvalidGroupException(Exception):
    pass


class membership_group_id_Exception(Exception):
    pass


@dataclass
class GroupCore:
    group_id: GroupID = None


@dataclass
class MemberShip(GroupCore):
    credit_vote: float = 1.0
    debtit_vote: float = 1.0
    # calculated fields
    _credor_pool: float = None
    _debtor_pool: float = None
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _fund_agenda_ratio_give: float = None
    _fund_agenda_ratio_take: float = None
    _acct_name: AcctName = None

    def set_credit_vote(self, x_credit_vote: float):
        if x_credit_vote is not None:
            self.credit_vote = x_credit_vote

    def set_debtit_vote(self, x_debtit_vote: float):
        if x_debtit_vote is not None:
            self.debtit_vote = x_debtit_vote

    def get_dict(self) -> dict[str, str]:
        return {
            "group_id": self.group_id,
            "credit_vote": self.credit_vote,
            "debtit_vote": self.debtit_vote,
        }

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        self._fund_agenda_ratio_give = 0
        self._fund_agenda_ratio_take = 0


def membership_shop(
    group_id: GroupID,
    credit_vote: float = None,
    debtit_vote: float = None,
    _acct_name: AcctName = None,
) -> MemberShip:
    return MemberShip(
        group_id=group_id,
        credit_vote=get_1_if_None(credit_vote),
        debtit_vote=get_1_if_None(debtit_vote),
        _credor_pool=0,
        _debtor_pool=0,
        _acct_name=_acct_name,
    )


def membership_get_from_dict(x_dict: dict, x_acct_name: AcctName) -> MemberShip:
    return membership_shop(
        group_id=x_dict.get("group_id"),
        credit_vote=x_dict.get("credit_vote"),
        debtit_vote=x_dict.get("debtit_vote"),
        _acct_name=x_acct_name,
    )


def memberships_get_from_dict(
    x_dict: dict, x_acct_name: AcctName
) -> dict[GroupID, MemberShip]:
    return {
        x_group_id: membership_get_from_dict(x_membership_dict, x_acct_name)
        for x_group_id, x_membership_dict in x_dict.items()
    }


@dataclass
class AwardCore:
    awardee_id: GroupID = None


@dataclass
class AwardLink(AwardCore):
    give_force: float = 1.0
    take_force: float = 1.0

    def get_dict(self) -> dict[str, str]:
        return {
            "awardee_id": self.awardee_id,
            "give_force": self.give_force,
            "take_force": self.take_force,
        }


# class AwardLinksshop:
def awardlinks_get_from_json(awardlinks_json: str) -> dict[GroupID, AwardLink]:
    awardlinks_dict = get_dict_from_json(awardlinks_json)
    return awardlinks_get_from_dict(awardlinks_dict)


def awardlinks_get_from_dict(x_dict: dict) -> dict[GroupID, AwardLink]:
    awardlinks = {}
    for awardlinks_dict in x_dict.values():
        x_group = awardlink_shop(
            awardee_id=awardlinks_dict["awardee_id"],
            give_force=awardlinks_dict["give_force"],
            take_force=awardlinks_dict["take_force"],
        )
        awardlinks[x_group.awardee_id] = x_group
    return awardlinks


def awardlink_shop(
    awardee_id: GroupID, give_force: float = None, take_force: float = None
) -> AwardLink:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardLink(awardee_id, give_force, take_force=take_force)


@dataclass
class AwardHeir(AwardCore):
    give_force: float = 1.0
    take_force: float = 1.0
    _fund_give: float = None
    _fund_take: float = None


def awardheir_shop(
    awardee_id: GroupID,
    give_force: float = None,
    take_force: float = None,
    _fund_give: float = None,
    _fund_take: float = None,
) -> AwardHeir:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardHeir(awardee_id, give_force, take_force, _fund_give, _fund_take)


@dataclass
class AwardLine(AwardCore):
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


def awardline_shop(awardee_id: GroupID, _fund_give: float, _fund_take: float):
    return AwardLine(awardee_id, _fund_give=_fund_give, _fund_take=_fund_take)


@dataclass
class GroupUnit(GroupCore):
    _memberships: dict[AcctName, MemberShip] = None  # set by BudUnit.set_acctunit()
    _bridge: str = None  # calculated by BudUnit
    # calculated by BudUnit.settle_bud()
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _credor_pool: float = None
    _debtor_pool: float = None
    _fund_coin: FundCoin = None

    def set_membership(self, x_membership: MemberShip):
        if x_membership.group_id != self.group_id:
            raise membership_group_id_Exception(
                f"GroupUnit.group_id={self.group_id} cannot set membership.group_id={x_membership.group_id}"
            )
        if x_membership._acct_name is None:
            raise membership_group_id_Exception(
                f"membership group_id={x_membership.group_id} cannot be set when _acct_name is None."
            )

        self._memberships[x_membership._acct_name] = x_membership
        self._add_credor_pool(x_membership._credor_pool)
        self._add_debtor_pool(x_membership._debtor_pool)

    def _add_credor_pool(self, x_credor_pool: float):
        self._credor_pool += x_credor_pool

    def _add_debtor_pool(self, x_debtor_pool: float):
        self._debtor_pool += x_debtor_pool

    def get_membership(self, x_acct_name: AcctName) -> MemberShip:
        return self._memberships.get(x_acct_name)

    def membership_exists(self, x_acct_name: AcctName) -> bool:
        return self.get_membership(x_acct_name) is not None

    def del_membership(self, acct_name):
        self._memberships.pop(acct_name)

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        for membership in self._memberships.values():
            membership.clear_fund_give_take()

    def _set_membership_fund_give_fund_take(self):
        credit_ledger = {}
        debtit_ledger = {}
        for x_acct_name, x_membership in self._memberships.items():
            credit_ledger[x_acct_name] = x_membership.credit_vote
            debtit_ledger[x_acct_name] = x_membership.debtit_vote
        fund_give_allot = allot_scale(credit_ledger, self._fund_give, self._fund_coin)
        fund_take_allot = allot_scale(debtit_ledger, self._fund_take, self._fund_coin)
        for acct_name, x_membership in self._memberships.items():
            x_membership._fund_give = fund_give_allot.get(acct_name)
            x_membership._fund_take = fund_take_allot.get(acct_name)
        x_a_give = self._fund_agenda_give
        x_a_take = self._fund_agenda_take
        fund_agenda_give_allot = allot_scale(credit_ledger, x_a_give, self._fund_coin)
        fund_agenda_take_allot = allot_scale(debtit_ledger, x_a_take, self._fund_coin)
        for acct_name, x_membership in self._memberships.items():
            x_membership._fund_agenda_give = fund_agenda_give_allot.get(acct_name)
            x_membership._fund_agenda_take = fund_agenda_take_allot.get(acct_name)


def groupunit_shop(
    group_id: GroupID, _bridge: str = None, _fund_coin: FundCoin = None
) -> GroupUnit:
    return GroupUnit(
        group_id=group_id,
        _memberships={},
        _fund_give=0,
        _fund_take=0,
        _fund_agenda_give=0,
        _fund_agenda_take=0,
        _credor_pool=0,
        _debtor_pool=0,
        _bridge=default_bridge_if_None(_bridge),
        _fund_coin=default_fund_coin_if_None(_fund_coin),
    )
    # x_groupunit.set_group_id(group_id=group_id)
    # return x_groupunit
