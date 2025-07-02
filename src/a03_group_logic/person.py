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
from src.a01_term_logic.term import PersonName
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import RespectNum, default_RespectBit_if_None
from src.a03_group_logic.group import (
    GroupTitle,
    MemberShip,
    membership_shop,
    memberships_get_from_dict,
)


class InvalidPersonException(Exception):
    pass


class Bad_person_nameMemberShipException(Exception):
    pass


@dataclass
class PersonCore:
    person_name: PersonName = None
    knot: str = None
    respect_bit: float = None

    def set_nameterm(self, x_person_name: PersonName):
        self.person_name = validate_labelterm(x_person_name, self.knot)


@dataclass
class PersonUnit(PersonCore):
    """This represents the believer_name's opinion of the PersonUnit.person_name
    PersonUnit.person_cred_points represents how much person_cred_points the _believer_name projects to the person_name
    PersonUnit.person_debt_points represents how much person_debt_points the _believer_name projects to the person_name
    """

    person_cred_points: int = None
    person_debt_points: int = None
    # special attribute: static in believer json, in memory it is deleted after loading and recalculated during saving.
    _memberships: dict[PersonName, MemberShip] = None
    # calculated fields
    _credor_pool: RespectNum = None
    _debtor_pool: RespectNum = None
    _irrational_person_debt_points: int = None  # set by listening process
    _inallocable_person_debt_points: int = None  # set by listening process
    # set by Believer.settle_believer()
    _fund_give: float = None
    _fund_take: float = None
    _fund_agenda_give: float = None
    _fund_agenda_take: float = None
    _fund_agenda_ratio_give: float = None
    _fund_agenda_ratio_take: float = None

    def set_respect_bit(self, x_respect_bit: float):
        self.respect_bit = x_respect_bit

    def set_credor_person_debt_points(
        self,
        person_cred_points: float = None,
        person_debt_points: float = None,
    ):
        if person_cred_points is not None:
            self.set_person_cred_points(person_cred_points)
        if person_debt_points is not None:
            self.set_person_debt_points(person_debt_points)

    def set_person_cred_points(self, person_cred_points: int):
        self.person_cred_points = person_cred_points

    def set_person_debt_points(self, person_debt_points: int):
        self.person_debt_points = person_debt_points

    def get_person_cred_points(self):
        return get_1_if_None(self.person_cred_points)

    def get_person_debt_points(self):
        return get_1_if_None(self.person_debt_points)

    def clear_fund_give_take(self):
        self._fund_give = 0
        self._fund_take = 0
        self._fund_agenda_give = 0
        self._fund_agenda_take = 0
        self._fund_agenda_ratio_give = 0
        self._fund_agenda_ratio_take = 0

    def add_irrational_person_debt_points(self, x_irrational_person_debt_points: float):
        self._irrational_person_debt_points += x_irrational_person_debt_points

    def add_inallocable_person_debt_points(
        self, x_inallocable_person_debt_points: float
    ):
        self._inallocable_person_debt_points += x_inallocable_person_debt_points

    def reset_listen_calculated_attrs(self):
        self._irrational_person_debt_points = 0
        self._inallocable_person_debt_points = 0

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
        personunits_person_cred_points_sum: float,
        personunits_person_debt_points_sum: float,
    ):
        total_person_cred_points = personunits_person_cred_points_sum
        ratio_give_sum = fund_agenda_ratio_give_sum
        self._fund_agenda_ratio_give = (
            self.get_person_cred_points() / total_person_cred_points
            if fund_agenda_ratio_give_sum == 0
            else self._fund_agenda_give / ratio_give_sum
        )
        if fund_agenda_ratio_take_sum == 0:
            total_person_debt_points = personunits_person_debt_points_sum
            self._fund_agenda_ratio_take = (
                self.get_person_debt_points() / total_person_debt_points
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
        group_title_is_person_name = is_labelterm(x_group_title, self.knot)
        if group_title_is_person_name and self.person_name != x_group_title:
            raise Bad_person_nameMemberShipException(
                f"PersonUnit with person_name='{self.person_name}' cannot have link to '{x_group_title}'."
            )

        x_membership.person_name = self.person_name
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
            x_membership.group_title: x_membership.get_dict()
            for x_membership in self._memberships.values()
        }

    def get_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {
            "person_name": self.person_name,
            "person_cred_points": self.person_cred_points,
            "person_debt_points": self.person_debt_points,
            "_memberships": self.get_memberships_dict(),
        }
        if self._irrational_person_debt_points not in [None, 0]:
            x_dict["_irrational_person_debt_points"] = (
                self._irrational_person_debt_points
            )
        if self._inallocable_person_debt_points not in [None, 0]:
            x_dict["_inallocable_person_debt_points"] = (
                self._inallocable_person_debt_points
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


def personunits_get_from_json(personunits_json: str) -> dict[str, PersonUnit]:
    personunits_dict = get_dict_from_json(personunits_json)
    return personunits_get_from_dict(x_dict=personunits_dict)


def personunits_get_from_dict(x_dict: dict, _knot: str = None) -> dict[str, PersonUnit]:
    personunits = {}
    for personunit_dict in x_dict.values():
        x_personunit = personunit_get_from_dict(personunit_dict, _knot)
        personunits[x_personunit.person_name] = x_personunit
    return personunits


def personunit_get_from_dict(personunit_dict: dict, _knot: str) -> PersonUnit:
    x_person_name = personunit_dict["person_name"]
    x_person_cred_points = personunit_dict["person_cred_points"]
    x_person_debt_points = personunit_dict["person_debt_points"]
    x_memberships_dict = personunit_dict["_memberships"]
    x_personunit = personunit_shop(
        x_person_name, x_person_cred_points, x_person_debt_points, _knot
    )
    x_personunit._memberships = memberships_get_from_dict(
        x_memberships_dict, x_person_name
    )
    _irrational_person_debt_points = personunit_dict.get(
        "_irrational_person_debt_points", 0
    )
    _inallocable_person_debt_points = personunit_dict.get(
        "_inallocable_person_debt_points", 0
    )
    x_personunit.add_irrational_person_debt_points(
        get_0_if_None(_irrational_person_debt_points)
    )
    x_personunit.add_inallocable_person_debt_points(
        get_0_if_None(_inallocable_person_debt_points)
    )

    return x_personunit


def personunit_shop(
    person_name: PersonName,
    person_cred_points: int = None,
    person_debt_points: int = None,
    knot: str = None,
    respect_bit: float = None,
) -> PersonUnit:
    x_personunit = PersonUnit(
        person_cred_points=get_1_if_None(person_cred_points),
        person_debt_points=get_1_if_None(person_debt_points),
        _memberships={},
        _credor_pool=0,
        _debtor_pool=0,
        _irrational_person_debt_points=0,
        _inallocable_person_debt_points=0,
        _fund_give=0,
        _fund_take=0,
        _fund_agenda_give=0,
        _fund_agenda_take=0,
        _fund_agenda_ratio_give=0,
        _fund_agenda_ratio_take=0,
        knot=default_knot_if_None(knot),
        respect_bit=default_RespectBit_if_None(respect_bit),
    )
    x_personunit.set_nameterm(x_person_name=person_name)
    return x_personunit
