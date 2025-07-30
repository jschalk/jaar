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
from src.a01_term_logic.term import PartnerName
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import RespectNum, default_RespectBit_if_None
from src.a03_group_logic.group import (
    GroupTitle,
    MemberShip,
    membership_shop,
    memberships_get_from_dict,
)


class InvalidPartnerException(Exception):
    pass


class Bad_partner_nameMemberShipException(Exception):
    pass


@dataclass
class PartnerCore:
    partner_name: PartnerName = None
    knot: str = None
    respect_bit: float = None

    def set_nameterm(self, x_partner_name: PartnerName):
        self.partner_name = validate_labelterm(x_partner_name, self.knot)


@dataclass
class PartnerUnit(PartnerCore):
    """This represents the believer_name's opinion of the PartnerUnit.partner_name
    PartnerUnit.partner_cred_points represents how much partner_cred_points the _believer_name projects to the partner_name
    PartnerUnit.partner_debt_points represents how much partner_debt_points the _believer_name projects to the partner_name
    """

    partner_cred_points: int = None
    partner_debt_points: int = None
    # special attribute: static in believer json, in memory it is deleted after loading and recalculated during saving.
    _memberships: dict[PartnerName, MemberShip] = None
    # calculated fields
    _credor_pool: RespectNum = None
    _debtor_pool: RespectNum = None
    _irrational_partner_debt_points: int = None  # set by listening process
    _inallocable_partner_debt_points: int = None  # set by listening process
    # set by Believer.settle_believer()
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _fund_agenda_ratio_give: float = None
    _fund_agenda_ratio_take: float = None

    def set_respect_bit(self, x_respect_bit: float):
        self.respect_bit = x_respect_bit

    def set_credor_partner_debt_points(
        self,
        partner_cred_points: float = None,
        partner_debt_points: float = None,
    ):
        if partner_cred_points is not None:
            self.set_partner_cred_points(partner_cred_points)
        if partner_debt_points is not None:
            self.set_partner_debt_points(partner_debt_points)

    def set_partner_cred_points(self, partner_cred_points: int):
        self.partner_cred_points = partner_cred_points

    def set_partner_debt_points(self, partner_debt_points: int):
        self.partner_debt_points = partner_debt_points

    def get_partner_cred_points(self):
        return get_1_if_None(self.partner_cred_points)

    def get_partner_debt_points(self):
        return get_1_if_None(self.partner_debt_points)

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        self._fund_agenda_ratio_give = 0
        self._fund_agenda_ratio_take = 0

    def add_irrational_partner_debt_points(
        self, x_irrational_partner_debt_points: float
    ):
        self._irrational_partner_debt_points += x_irrational_partner_debt_points

    def add_inallocable_partner_debt_points(
        self, x_inallocable_partner_debt_points: float
    ):
        self._inallocable_partner_debt_points += x_inallocable_partner_debt_points

    def reset_listen_calculated_attrs(self):
        self._irrational_partner_debt_points = 0
        self._inallocable_partner_debt_points = 0

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
        partnerunits_partner_cred_points_sum: float,
        partnerunits_partner_debt_points_sum: float,
    ):
        total_partner_cred_points = partnerunits_partner_cred_points_sum
        ratio_give_sum = fund_agenda_ratio_give_sum
        self._fund_agenda_ratio_give = (
            self.get_partner_cred_points() / total_partner_cred_points
            if fund_agenda_ratio_give_sum == 0
            else self._fund_agenda_give / ratio_give_sum
        )
        if fund_agenda_ratio_take_sum == 0:
            total_partner_debt_points = partnerunits_partner_debt_points_sum
            self._fund_agenda_ratio_take = (
                self.get_partner_debt_points() / total_partner_debt_points
            )
        else:
            ratio_take_sum = fund_agenda_ratio_take_sum
            self._fund_agenda_ratio_take = self._fund_agenda_take / ratio_take_sum

    def add_membership(
        self,
        group_title: GroupTitle,
        group_cred_points: float = None,
        group_debt_points: float = None,
    ):
        x_membership = membership_shop(
            group_title, group_cred_points, group_debt_points
        )
        self.set_membership(x_membership)

    def set_membership(self, x_membership: MemberShip):
        x_group_title = x_membership.group_title
        group_title_is_partner_name = is_labelterm(x_group_title, self.knot)
        if group_title_is_partner_name and self.partner_name != x_group_title:
            raise Bad_partner_nameMemberShipException(
                f"PartnerUnit with partner_name='{self.partner_name}' cannot have link to '{x_group_title}'."
            )

        x_membership.partner_name = self.partner_name
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
            x_membership.group_title: x_membership.group_cred_points
            for x_membership in self._memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._credor_pool, self.respect_bit)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title)._credor_pool = alloted_pool

    def set_debtor_pool(self, debtor_pool: RespectNum):
        self._debtor_pool = debtor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.group_debt_points
            for x_membership in self._memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._debtor_pool, self.respect_bit)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title)._debtor_pool = alloted_pool

    def get_memberships_dict(self) -> dict:
        return {
            x_membership.group_title: x_membership.to_dict()
            for x_membership in self._memberships.values()
        }

    def to_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {
            "partner_name": self.partner_name,
            "partner_cred_points": self.partner_cred_points,
            "partner_debt_points": self.partner_debt_points,
            "_memberships": self.get_memberships_dict(),
        }
        if self._irrational_partner_debt_points not in [None, 0]:
            x_dict["_irrational_partner_debt_points"] = (
                self._irrational_partner_debt_points
            )
        if self._inallocable_partner_debt_points not in [None, 0]:
            x_dict["_inallocable_partner_debt_points"] = (
                self._inallocable_partner_debt_points
            )

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


def partnerunits_get_from_json(partnerunits_json: str) -> dict[str, PartnerUnit]:
    partnerunits_dict = get_dict_from_json(partnerunits_json)
    return partnerunits_get_from_dict(x_dict=partnerunits_dict)


def partnerunits_get_from_dict(
    x_dict: dict, _knot: str = None
) -> dict[str, PartnerUnit]:
    partnerunits = {}
    for partnerunit_dict in x_dict.values():
        x_partnerunit = partnerunit_get_from_dict(partnerunit_dict, _knot)
        partnerunits[x_partnerunit.partner_name] = x_partnerunit
    return partnerunits


def partnerunit_get_from_dict(partnerunit_dict: dict, _knot: str) -> PartnerUnit:
    x_partner_name = partnerunit_dict["partner_name"]
    x_partner_cred_points = partnerunit_dict["partner_cred_points"]
    x_partner_debt_points = partnerunit_dict["partner_debt_points"]
    x_memberships_dict = partnerunit_dict["_memberships"]
    x_partnerunit = partnerunit_shop(
        x_partner_name, x_partner_cred_points, x_partner_debt_points, _knot
    )
    x_partnerunit._memberships = memberships_get_from_dict(
        x_memberships_dict, x_partner_name
    )
    _irrational_partner_debt_points = partnerunit_dict.get(
        "_irrational_partner_debt_points", 0
    )
    _inallocable_partner_debt_points = partnerunit_dict.get(
        "_inallocable_partner_debt_points", 0
    )
    x_partnerunit.add_irrational_partner_debt_points(
        get_0_if_None(_irrational_partner_debt_points)
    )
    x_partnerunit.add_inallocable_partner_debt_points(
        get_0_if_None(_inallocable_partner_debt_points)
    )

    return x_partnerunit


def partnerunit_shop(
    partner_name: PartnerName,
    partner_cred_points: int = None,
    partner_debt_points: int = None,
    knot: str = None,
    respect_bit: float = None,
) -> PartnerUnit:
    x_partnerunit = PartnerUnit(
        partner_cred_points=get_1_if_None(partner_cred_points),
        partner_debt_points=get_1_if_None(partner_debt_points),
        _memberships={},
        _credor_pool=0,
        _debtor_pool=0,
        _irrational_partner_debt_points=0,
        _inallocable_partner_debt_points=0,
        _fund_give=0,
        _fund_take=0,
        _fund_agenda_give=0,
        _fund_agenda_take=0,
        _fund_agenda_ratio_give=0,
        _fund_agenda_ratio_take=0,
        knot=default_knot_if_None(knot),
        respect_bit=default_RespectBit_if_None(respect_bit),
    )
    x_partnerunit.set_nameterm(x_partner_name=partner_name)
    return x_partnerunit
