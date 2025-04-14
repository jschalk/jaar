from src.f00_data_toolboxs.dict_toolbox import get_1_if_None, get_dict_from_json
from src.f01_word_logic.road import GroupLabel, AcctName, default_bridge_if_None
from src.f02_finance_toolboxs.allot import allot_scale
from src.f02_finance_toolboxs.finance_config import FundCoin, default_fund_coin_if_None
from dataclasses import dataclass


class InvalidGroupException(Exception):
    pass


class membership_group_label_Exception(Exception):
    pass


@dataclass
class GroupCore:
    group_label: GroupLabel = None


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
    acct_name: AcctName = None

    def set_credit_vote(self, x_credit_vote: float):
        if x_credit_vote is not None:
            self.credit_vote = x_credit_vote

    def set_debtit_vote(self, x_debtit_vote: float):
        if x_debtit_vote is not None:
            self.debtit_vote = x_debtit_vote

    def get_dict(self) -> dict[str, str]:
        return {
            "group_label": self.group_label,
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
    group_label: GroupLabel,
    credit_vote: float = None,
    debtit_vote: float = None,
    acct_name: AcctName = None,
) -> MemberShip:
    return MemberShip(
        group_label=group_label,
        credit_vote=get_1_if_None(credit_vote),
        debtit_vote=get_1_if_None(debtit_vote),
        _credor_pool=0,
        _debtor_pool=0,
        acct_name=acct_name,
    )


def membership_get_from_dict(x_dict: dict, x_acct_name: AcctName) -> MemberShip:
    return membership_shop(
        group_label=x_dict.get("group_label"),
        credit_vote=x_dict.get("credit_vote"),
        debtit_vote=x_dict.get("debtit_vote"),
        acct_name=x_acct_name,
    )


def memberships_get_from_dict(
    x_dict: dict, x_acct_name: AcctName
) -> dict[GroupLabel, MemberShip]:
    return {
        x_group_label: membership_get_from_dict(x_membership_dict, x_acct_name)
        for x_group_label, x_membership_dict in x_dict.items()
    }


@dataclass
class AwardCore:
    awardee_tag: GroupLabel = None


@dataclass
class AwardLink(AwardCore):
    give_force: float = 1.0
    take_force: float = 1.0

    def get_dict(self) -> dict[str, str]:
        return {
            "awardee_tag": self.awardee_tag,
            "give_force": self.give_force,
            "take_force": self.take_force,
        }


# class AwardLinksshop:
def awardlinks_get_from_json(awardlinks_json: str) -> dict[GroupLabel, AwardLink]:
    awardlinks_dict = get_dict_from_json(awardlinks_json)
    return awardlinks_get_from_dict(awardlinks_dict)


def awardlinks_get_from_dict(x_dict: dict) -> dict[GroupLabel, AwardLink]:
    awardlinks = {}
    for awardlinks_dict in x_dict.values():
        x_group = awardlink_shop(
            awardee_tag=awardlinks_dict["awardee_tag"],
            give_force=awardlinks_dict["give_force"],
            take_force=awardlinks_dict["take_force"],
        )
        awardlinks[x_group.awardee_tag] = x_group
    return awardlinks


def awardlink_shop(
    awardee_tag: GroupLabel, give_force: float = None, take_force: float = None
) -> AwardLink:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardLink(awardee_tag, give_force, take_force=take_force)


@dataclass
class AwardHeir(AwardCore):
    give_force: float = 1.0
    take_force: float = 1.0
    _fund_give: float = None
    _fund_take: float = None


def awardheir_shop(
    awardee_tag: GroupLabel,
    give_force: float = None,
    take_force: float = None,
    _fund_give: float = None,
    _fund_take: float = None,
) -> AwardHeir:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardHeir(awardee_tag, give_force, take_force, _fund_give, _fund_take)


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


def awardline_shop(awardee_tag: GroupLabel, _fund_give: float, _fund_take: float):
    return AwardLine(awardee_tag, _fund_give=_fund_give, _fund_take=_fund_take)


@dataclass
class GroupUnit(GroupCore):
    _memberships: dict[AcctName, MemberShip] = None  # set by BudUnit.set_acctunit()
    bridge: str = None  # calculated by BudUnit
    # calculated by BudUnit.settle_bud()
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _credor_pool: float = None
    _debtor_pool: float = None
    fund_coin: FundCoin = None

    def set_membership(self, x_membership: MemberShip):
        if x_membership.group_label != self.group_label:
            raise membership_group_label_Exception(
                f"GroupUnit.group_label={self.group_label} cannot set membership.group_label={x_membership.group_label}"
            )
        if x_membership.acct_name is None:
            raise membership_group_label_Exception(
                f"membership group_label={x_membership.group_label} cannot be set when _acct_name is None."
            )

        self._memberships[x_membership.acct_name] = x_membership
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
        fund_give_allot = allot_scale(credit_ledger, self._fund_give, self.fund_coin)
        fund_take_allot = allot_scale(debtit_ledger, self._fund_take, self.fund_coin)
        for acct_name, x_membership in self._memberships.items():
            x_membership._fund_give = fund_give_allot.get(acct_name)
            x_membership._fund_take = fund_take_allot.get(acct_name)
        x_a_give = self._fund_agenda_give
        x_a_take = self._fund_agenda_take
        fund_agenda_give_allot = allot_scale(credit_ledger, x_a_give, self.fund_coin)
        fund_agenda_take_allot = allot_scale(debtit_ledger, x_a_take, self.fund_coin)
        for acct_name, x_membership in self._memberships.items():
            x_membership._fund_agenda_give = fund_agenda_give_allot.get(acct_name)
            x_membership._fund_agenda_take = fund_agenda_take_allot.get(acct_name)


def groupunit_shop(
    group_label: GroupLabel, bridge: str = None, fund_coin: FundCoin = None
) -> GroupUnit:
    return GroupUnit(
        group_label=group_label,
        _memberships={},
        _fund_give=0,
        _fund_take=0,
        _fund_agenda_give=0,
        _fund_agenda_take=0,
        _credor_pool=0,
        _debtor_pool=0,
        bridge=default_bridge_if_None(bridge),
        fund_coin=default_fund_coin_if_None(fund_coin),
    )
    # x_groupunit.set_group_label(group_label=group_label)
    # return x_groupunit
