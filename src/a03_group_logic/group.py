from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import get_1_if_None, get_dict_from_json
from src.a01_term_logic.term import GroupTitle, PartnerName, default_knot_if_None
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import FundIota, default_fund_iota_if_None


class InvalidGroupException(Exception):
    pass


class membership_group_title_Exception(Exception):
    pass


@dataclass
class GroupCore:
    group_title: GroupTitle = None


@dataclass
class MemberShip(GroupCore):
    group_cred_points: float = 1.0
    group_debt_points: float = 1.0
    # calculated fields
    _credor_pool: float = None
    _debtor_pool: float = None
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _fund_agenda_ratio_give: float = None
    _fund_agenda_ratio_take: float = None
    partner_name: PartnerName = None

    def set_group_cred_points(self, x_group_cred_points: float):
        if x_group_cred_points is not None:
            self.group_cred_points = x_group_cred_points

    def set_group_debt_points(self, x_group_debt_points: float):
        if x_group_debt_points is not None:
            self.group_debt_points = x_group_debt_points

    def to_dict(self) -> dict[str, str]:
        return {
            "group_title": self.group_title,
            "group_cred_points": self.group_cred_points,
            "group_debt_points": self.group_debt_points,
        }

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        self._fund_agenda_ratio_give = 0
        self._fund_agenda_ratio_take = 0


def membership_shop(
    group_title: GroupTitle,
    group_cred_points: float = None,
    group_debt_points: float = None,
    partner_name: PartnerName = None,
) -> MemberShip:
    return MemberShip(
        group_title=group_title,
        group_cred_points=get_1_if_None(group_cred_points),
        group_debt_points=get_1_if_None(group_debt_points),
        _credor_pool=0,
        _debtor_pool=0,
        partner_name=partner_name,
    )


def membership_get_from_dict(x_dict: dict, x_partner_name: PartnerName) -> MemberShip:
    return membership_shop(
        group_title=x_dict.get("group_title"),
        group_cred_points=x_dict.get("group_cred_points"),
        group_debt_points=x_dict.get("group_debt_points"),
        partner_name=x_partner_name,
    )


def memberships_get_from_dict(
    x_dict: dict, x_partner_name: PartnerName
) -> dict[GroupTitle, MemberShip]:
    return {
        x_group_title: membership_get_from_dict(x_membership_dict, x_partner_name)
        for x_group_title, x_membership_dict in x_dict.items()
    }


@dataclass
class AwardCore:
    awardee_title: GroupTitle = None


@dataclass
class AwardLink(AwardCore):
    give_force: float = 1.0
    take_force: float = 1.0

    def to_dict(self) -> dict[str, str]:
        return {
            "awardee_title": self.awardee_title,
            "give_force": self.give_force,
            "take_force": self.take_force,
        }


def awardlinks_get_from_json(awardlinks_json: str) -> dict[GroupTitle, AwardLink]:
    awardlinks_dict = get_dict_from_json(awardlinks_json)
    return awardlinks_get_from_dict(awardlinks_dict)


def awardlinks_get_from_dict(x_dict: dict) -> dict[GroupTitle, AwardLink]:
    awardlinks = {}
    for awardlinks_dict in x_dict.values():
        x_group = awardlink_shop(
            awardee_title=awardlinks_dict["awardee_title"],
            give_force=awardlinks_dict["give_force"],
            take_force=awardlinks_dict["take_force"],
        )
        awardlinks[x_group.awardee_title] = x_group
    return awardlinks


def awardlink_shop(
    awardee_title: GroupTitle,
    give_force: float = None,
    take_force: float = None,
) -> AwardLink:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardLink(awardee_title, give_force, take_force=take_force)


@dataclass
class AwardHeir(AwardCore):
    give_force: float = 1.0
    take_force: float = 1.0
    _fund_give: float = None
    _fund_take: float = None


def awardheir_shop(
    awardee_title: GroupTitle,
    give_force: float = None,
    take_force: float = None,
    _fund_give: float = None,
    _fund_take: float = None,
) -> AwardHeir:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardHeir(awardee_title, give_force, take_force, _fund_give, _fund_take)


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


def awardline_shop(awardee_title: GroupTitle, _fund_give: float, _fund_take: float):
    return AwardLine(awardee_title, _fund_give=_fund_give, _fund_take=_fund_take)


@dataclass
class GroupUnit(GroupCore):
    _memberships: dict[PartnerName, MemberShip] = (
        None  # set by BelieverUnit.set_partnerunit()
    )
    knot: str = None  # calculated by BelieverUnit
    # calculated by BelieverUnit.settle_believer()
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _credor_pool: float = None
    _debtor_pool: float = None
    fund_iota: FundIota = None

    def set_membership(self, x_membership: MemberShip):
        if x_membership.group_title != self.group_title:
            raise membership_group_title_Exception(
                f"GroupUnit.group_title={self.group_title} cannot set membership.group_title={x_membership.group_title}"
            )
        if x_membership.partner_name is None:
            raise membership_group_title_Exception(
                f"membership group_title={x_membership.group_title} cannot be set when _partner_name is None."
            )

        self._memberships[x_membership.partner_name] = x_membership
        self._add_credor_pool(x_membership._credor_pool)
        self._add_debtor_pool(x_membership._debtor_pool)

    def _add_credor_pool(self, x_credor_pool: float):
        self._credor_pool += x_credor_pool

    def _add_debtor_pool(self, x_debtor_pool: float):
        self._debtor_pool += x_debtor_pool

    def get_membership(self, x_partner_name: PartnerName) -> MemberShip:
        return self._memberships.get(x_partner_name)

    def membership_exists(self, x_partner_name: PartnerName) -> bool:
        return self.get_membership(x_partner_name) is not None

    def del_membership(self, partner_name):
        self._memberships.pop(partner_name)

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        for membership in self._memberships.values():
            membership.clear_fund_give_take()

    def _set_membership_fund_give_fund_take(self):
        credit_ledger = {}
        debt_ledger = {}
        for x_partner_name, x_membership in self._memberships.items():
            credit_ledger[x_partner_name] = x_membership.group_cred_points
            debt_ledger[x_partner_name] = x_membership.group_debt_points
        fund_give_allot = allot_scale(credit_ledger, self._fund_give, self.fund_iota)
        fund_take_allot = allot_scale(debt_ledger, self._fund_take, self.fund_iota)
        for partner_name, x_membership in self._memberships.items():
            x_membership._fund_give = fund_give_allot.get(partner_name)
            x_membership._fund_take = fund_take_allot.get(partner_name)
        x_a_give = self._fund_agenda_give
        x_a_take = self._fund_agenda_take
        fund_agenda_give_allot = allot_scale(credit_ledger, x_a_give, self.fund_iota)
        fund_agenda_take_allot = allot_scale(debt_ledger, x_a_take, self.fund_iota)
        for partner_name, x_membership in self._memberships.items():
            x_membership._fund_agenda_give = fund_agenda_give_allot.get(partner_name)
            x_membership._fund_agenda_take = fund_agenda_take_allot.get(partner_name)


def groupunit_shop(
    group_title: GroupTitle, knot: str = None, fund_iota: FundIota = None
) -> GroupUnit:
    return GroupUnit(
        group_title=group_title,
        _memberships={},
        _fund_give=0,
        _fund_take=0,
        _fund_agenda_give=0,
        _fund_agenda_take=0,
        _credor_pool=0,
        _debtor_pool=0,
        knot=default_knot_if_None(knot),
        fund_iota=default_fund_iota_if_None(fund_iota),
    )
    # x_groupunit.set_group_title(group_title=group_title)
    # return x_groupunit
