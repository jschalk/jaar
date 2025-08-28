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
from src.a01_term_logic.term import VoiceName
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import RespectNum, default_RespectBit_if_None
from src.a03_group_logic.group import (
    GroupTitle,
    MemberShip,
    membership_shop,
    memberships_get_from_dict,
)


class InvalidVoiceException(Exception):
    pass


class Bad_voice_nameMemberShipException(Exception):
    pass


@dataclass
class VoiceCore:
    voice_name: VoiceName = None
    knot: str = None
    respect_bit: float = None

    def set_nameterm(self, x_voice_name: VoiceName):
        self.voice_name = validate_labelterm(x_voice_name, self.knot)


@dataclass
class VoiceUnit(VoiceCore):
    """This represents the belief_name's opinion of the VoiceUnit.voice_name
    VoiceUnit.voice_cred_points represents how much voice_cred_points the _belief_name projects to the voice_name
    VoiceUnit.voice_debt_points represents how much voice_debt_points the _belief_name projects to the voice_name
    """

    voice_cred_points: int = None
    voice_debt_points: int = None
    # special attribute: static in belief json, in memory it is deleted after loading and recalculated during saving.
    _memberships: dict[VoiceName, MemberShip] = None
    # calculated fields
    credor_pool: RespectNum = None
    debtor_pool: RespectNum = None
    irrational_voice_debt_points: int = None  # set by listening process
    inallocable_voice_debt_points: int = None  # set by listening process
    # set by Belief.cash_out()
    fund_give: float = None
    fund_take: float = None
    fund_agenda_give: float = None
    fund_agenda_take: float = None
    fund_agenda_ratio_give: float = None
    fund_agenda_ratio_take: float = None

    def set_respect_bit(self, x_respect_bit: float):
        self.respect_bit = x_respect_bit

    def set_credor_voice_debt_points(
        self,
        voice_cred_points: float = None,
        voice_debt_points: float = None,
    ):
        if voice_cred_points is not None:
            self.set_voice_cred_points(voice_cred_points)
        if voice_debt_points is not None:
            self.set_voice_debt_points(voice_debt_points)

    def set_voice_cred_points(self, voice_cred_points: int):
        self.voice_cred_points = voice_cred_points

    def set_voice_debt_points(self, voice_debt_points: int):
        self.voice_debt_points = voice_debt_points

    def get_voice_cred_points(self):
        return get_1_if_None(self.voice_cred_points)

    def get_voice_debt_points(self):
        return get_1_if_None(self.voice_debt_points)

    def clear_fund_give_take(self):
        self.fund_give = 0
        self.fund_take = 0
        self.fund_agenda_give = 0
        self.fund_agenda_take = 0
        self.fund_agenda_ratio_give = 0
        self.fund_agenda_ratio_take = 0

    def add_irrational_voice_debt_points(self, x_irrational_voice_debt_points: float):
        self.irrational_voice_debt_points += x_irrational_voice_debt_points

    def add_inallocable_voice_debt_points(self, x_inallocable_voice_debt_points: float):
        self.inallocable_voice_debt_points += x_inallocable_voice_debt_points

    def reset_listen_calculated_attrs(self):
        self.irrational_voice_debt_points = 0
        self.inallocable_voice_debt_points = 0

    def add_fund_give(self, fund_give: float):
        self.fund_give += fund_give

    def add_fund_take(self, fund_take: float):
        self.fund_take += fund_take

    def add_fund_agenda_give(self, fund_agenda_give: float):
        self.fund_agenda_give += fund_agenda_give

    def add_fund_agenda_take(self, fund_agenda_take: float):
        self.fund_agenda_take += fund_agenda_take

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
        voiceunits_voice_cred_points_sum: float,
        voiceunits_voice_debt_points_sum: float,
    ):
        total_voice_cred_points = voiceunits_voice_cred_points_sum
        ratio_give_sum = fund_agenda_ratio_give_sum
        self.fund_agenda_ratio_give = (
            self.get_voice_cred_points() / total_voice_cred_points
            if fund_agenda_ratio_give_sum == 0
            else self.fund_agenda_give / ratio_give_sum
        )
        if fund_agenda_ratio_take_sum == 0:
            total_voice_debt_points = voiceunits_voice_debt_points_sum
            self.fund_agenda_ratio_take = (
                self.get_voice_debt_points() / total_voice_debt_points
            )
        else:
            ratio_take_sum = fund_agenda_ratio_take_sum
            self.fund_agenda_ratio_take = self.fund_agenda_take / ratio_take_sum

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
        group_title_is_voice_name = is_labelterm(x_group_title, self.knot)
        if group_title_is_voice_name and self.voice_name != x_group_title:
            raise Bad_voice_nameMemberShipException(
                f"VoiceUnit with voice_name='{self.voice_name}' cannot have link to '{x_group_title}'."
            )

        x_membership.voice_name = self.voice_name
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
        self.credor_pool = credor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.group_cred_points
            for x_membership in self._memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self.credor_pool, self.respect_bit)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title).credor_pool = alloted_pool

    def set_debtor_pool(self, debtor_pool: RespectNum):
        self.debtor_pool = debtor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.group_debt_points
            for x_membership in self._memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self.debtor_pool, self.respect_bit)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title).debtor_pool = alloted_pool

    def get_memberships_dict(self) -> dict:
        return {
            x_membership.group_title: x_membership.to_dict()
            for x_membership in self._memberships.values()
        }

    def to_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {
            "voice_name": self.voice_name,
            "voice_cred_points": self.voice_cred_points,
            "voice_debt_points": self.voice_debt_points,
            "_memberships": self.get_memberships_dict(),
        }
        if self.irrational_voice_debt_points not in [None, 0]:
            x_dict["irrational_voice_debt_points"] = self.irrational_voice_debt_points
        if self.inallocable_voice_debt_points not in [None, 0]:
            x_dict["inallocable_voice_debt_points"] = self.inallocable_voice_debt_points

        if all_attrs:
            self._all_attrs_necessary_in_dict(x_dict)
        return x_dict

    def _all_attrs_necessary_in_dict(self, x_dict):
        x_dict["fund_give"] = self.fund_give
        x_dict["fund_take"] = self.fund_take
        x_dict["fund_agenda_give"] = self.fund_agenda_give
        x_dict["fund_agenda_take"] = self.fund_agenda_take
        x_dict["fund_agenda_ratio_give"] = self.fund_agenda_ratio_give
        x_dict["fund_agenda_ratio_take"] = self.fund_agenda_ratio_take


def voiceunits_get_from_json(voiceunits_json: str) -> dict[str, VoiceUnit]:
    voiceunits_dict = get_dict_from_json(voiceunits_json)
    return voiceunits_get_from_dict(x_dict=voiceunits_dict)


def voiceunits_get_from_dict(x_dict: dict, _knot: str = None) -> dict[str, VoiceUnit]:
    voiceunits = {}
    for voiceunit_dict in x_dict.values():
        x_voiceunit = voiceunit_get_from_dict(voiceunit_dict, _knot)
        voiceunits[x_voiceunit.voice_name] = x_voiceunit
    return voiceunits


def voiceunit_get_from_dict(voiceunit_dict: dict, _knot: str) -> VoiceUnit:
    x_voice_name = voiceunit_dict["voice_name"]
    x_voice_cred_points = voiceunit_dict["voice_cred_points"]
    x_voice_debt_points = voiceunit_dict["voice_debt_points"]
    x_memberships_dict = voiceunit_dict["_memberships"]
    x_voiceunit = voiceunit_shop(
        x_voice_name, x_voice_cred_points, x_voice_debt_points, _knot
    )
    x_voiceunit._memberships = memberships_get_from_dict(
        x_memberships_dict, x_voice_name
    )
    irrational_voice_debt_points = voiceunit_dict.get("irrational_voice_debt_points", 0)
    inallocable_voice_debt_points = voiceunit_dict.get(
        "inallocable_voice_debt_points", 0
    )
    x_voiceunit.add_irrational_voice_debt_points(
        get_0_if_None(irrational_voice_debt_points)
    )
    x_voiceunit.add_inallocable_voice_debt_points(
        get_0_if_None(inallocable_voice_debt_points)
    )

    return x_voiceunit


def voiceunit_shop(
    voice_name: VoiceName,
    voice_cred_points: int = None,
    voice_debt_points: int = None,
    knot: str = None,
    respect_bit: float = None,
) -> VoiceUnit:
    x_voiceunit = VoiceUnit(
        voice_cred_points=get_1_if_None(voice_cred_points),
        voice_debt_points=get_1_if_None(voice_debt_points),
        _memberships={},
        credor_pool=0,
        debtor_pool=0,
        irrational_voice_debt_points=0,
        inallocable_voice_debt_points=0,
        fund_give=0,
        fund_take=0,
        fund_agenda_give=0,
        fund_agenda_take=0,
        fund_agenda_ratio_give=0,
        fund_agenda_ratio_take=0,
        knot=default_knot_if_None(knot),
        respect_bit=default_RespectBit_if_None(respect_bit),
    )
    x_voiceunit.set_nameterm(x_voice_name=voice_name)
    return x_voiceunit
