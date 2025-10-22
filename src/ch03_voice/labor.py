from dataclasses import dataclass
from src.ch01_py.dict_toolbox import get_empty_dict_if_None, get_False_if_None
from src.ch03_voice.group import GroupTitle, GroupUnit
from src.ch03_voice.voice import VoiceName


class InvalidLaborHeirPopulateException(Exception):
    pass


@dataclass
class PartyUnit:
    party_title: GroupTitle = None
    solo: bool = None

    def to_dict(self) -> dict[str,]:
        """Returns dict that is serializable to JSON."""

        x_dict = {"party_title": self.party_title}
        if self.solo is True:
            x_dict["solo"] = self.solo
        return x_dict


def partyunit_shop(party_title: GroupTitle, solo: bool = None) -> PartyUnit:
    return PartyUnit(party_title=party_title, solo=get_False_if_None(solo))


def partyunit_get_from_dict(x_dict: dict) -> PartyUnit:
    return partyunit_shop(x_dict.get("party_title"), solo=x_dict.get("solo"))


@dataclass
class PartyHeir:
    party_title: GroupTitle = None
    solo: bool = None
    parent_solo: bool = None


def partyheir_shop(party_title: GroupTitle, solo: bool) -> PartyHeir:
    return PartyHeir(party_title=party_title, solo=solo)


@dataclass
class LaborUnit:
    partys: dict[GroupTitle, PartyUnit] = None

    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        partys_dict = {
            party_title: partyunit.to_dict()
            for party_title, partyunit in self.partys.items()
        }
        return {"partys": partys_dict}

    def add_party(self, party_title: GroupTitle, solo: bool = None):
        self.partys[party_title] = partyunit_shop(party_title, solo)

    def partyunit_exists(self, party_title: GroupTitle):
        return party_title in self.partys

    def del_partyunit(self, party_title: GroupTitle):
        self.partys.pop(party_title)

    def get_partyunit(self, party_title: GroupTitle) -> PartyUnit:
        if self.partyunit_exists(party_title):
            return self.partys.get(party_title)


def laborunit_shop(partys: dict[GroupTitle, PartyUnit] = None) -> LaborUnit:
    return LaborUnit(get_empty_dict_if_None(partys))


def get_laborunit_from_dict(laborunit_dict: dict) -> LaborUnit:
    x_laborunit = laborunit_shop()
    partys_dict = laborunit_dict.get("partys")
    for party_dict in partys_dict.values():
        x_laborunit.add_party(
            party_title=party_dict.get("party_title"), solo=party_dict.get("solo")
        )
    return x_laborunit


@dataclass
class LaborHeir:
    partys: dict[GroupTitle, PartyHeir] = None
    belief_name_is_labor: bool = None

    def is_empty(self) -> bool:
        return self.partys == {}

    def set_belief_name_is_labor(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        belief_name: VoiceName,
    ):
        self.belief_name_is_labor = self.get_belief_name_is_labor_bool(
            groupunits, belief_name
        )

    def get_belief_name_is_labor_bool(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        belief_name: VoiceName,
    ) -> bool:
        if self.partys == {}:
            return True

        for x_party_title, x_groupunit in groupunits.items():
            if x_party_title in self.partys:
                for x_voice_name in x_groupunit.memberships.keys():
                    if x_voice_name == belief_name:
                        return True
        return False

    def set_partys(
        self,
        parent_laborheir,
        laborunit: LaborUnit,
        groupunits: dict[GroupTitle, GroupUnit],
    ):
        self.partys = {}
        # there is no parent laborheir or parent laborheir is empty
        if parent_laborheir is None or parent_laborheir.partys == {}:
            for partyunit in laborunit.partys.values():
                _set_party_to_partys(self.partys, partyunit)
        # current laborunit is not empty and parent laborheir is empty
        elif laborunit.partys == {}:
            for parent_partyheir in parent_laborheir.partys.values():
                _set_party_to_partys(self.partys, parent_partyheir)
        # current laborunit is not empty and parent laborheir is not empty
        else:
            # grab all parent heirs first
            for parent_partyheir in parent_laborheir.partys.values():
                _set_party_to_partys(self.partys, parent_partyheir)
            # if it doesn't exist add current laborunit
            for partyunit in laborunit.partys.values():
                if self.partys.get(partyunit.party_title) is None:
                    _set_party_to_partys(self.partys, partyunit)

    def has_party(self, party_titles: set[GroupTitle]):
        return self.is_empty() or any(gn_x in self.partys for gn_x in party_titles)


def _set_party_to_partys(partys: dict, x_party):
    x_partyheir = partyheir_shop(party_title=x_party.party_title, solo=x_party.solo)
    partys[x_partyheir.party_title] = x_partyheir


def laborheir_shop(
    partys: dict[GroupTitle, PartyHeir] = None, belief_name_is_labor: bool = None
) -> LaborHeir:
    partys = get_empty_dict_if_None(partys)
    belief_name_is_labor = get_False_if_None(belief_name_is_labor)
    return LaborHeir(partys=partys, belief_name_is_labor=belief_name_is_labor)
