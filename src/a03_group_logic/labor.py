from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import get_empty_dict_if_None, get_False_if_None
from src.a03_group_logic.group import GroupTitle, GroupUnit
from src.a03_group_logic.partner import PartnerName


class InvalidLaborHeirPopulateException(Exception):
    pass


@dataclass
class PartyUnit:
    party_title: GroupTitle = None
    solo: bool = None

    def get_dict(self) -> dict[str,]:
        return {"party_title": self.party_title, "solo": self.solo}


def partyunit_shop(party_title: GroupTitle, solo: bool = None) -> PartyUnit:
    return PartyUnit(party_title=party_title, solo=get_False_if_None(solo))


@dataclass
class PartyHeir:
    party_title: GroupTitle = None
    solo: bool = None
    _parent_solo: bool = None


def partyheir_shop(party_title: GroupTitle, solo: bool) -> PartyHeir:
    return PartyHeir(party_title=party_title, solo=solo)


@dataclass
class LaborUnit:
    _partys: dict[GroupTitle, PartyUnit] = None

    def to_dict(self) -> dict[str, str]:
        return {"_partys": list(self._partys)}

    def add_partyunit(self, party_title: GroupTitle, solo: bool = None):
        self._partys[party_title] = partyunit_shop(party_title, solo)

    def partyunit_exists(self, party_title: GroupTitle):
        return party_title in self._partys

    def del_partyunit(self, party_title: GroupTitle):
        self._partys.pop(party_title)

    def get_partyunit(self, party_title: GroupTitle) -> GroupTitle:
        if self.partyunit_exists(party_title):
            return party_title


def laborunit_shop(_partys: dict[GroupTitle, PartyUnit] = None) -> LaborUnit:
    return LaborUnit(get_empty_dict_if_None(_partys))


def create_laborunit(partyunit: GroupTitle):
    x_laborunit = laborunit_shop()
    x_laborunit.add_partyunit(partyunit)
    return x_laborunit


@dataclass
class LaborHeir:
    _partys: dict[GroupTitle, PartyHeir] = None
    _believer_name_is_labor: bool = None

    def _get_all_partners(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        party_title_set: set[GroupTitle],
    ) -> dict[GroupTitle, GroupUnit]:
        dict_x = {}
        for x_party_title in party_title_set:
            dict_x |= groupunits.get(x_party_title)._memberships
        return dict_x

    def is_empty(self) -> bool:
        return self._partys == {}

    def set_believer_name_is_labor(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        believer_name: PartnerName,
    ):
        self._believer_name_is_labor = self.get_believer_name_is_labor_bool(
            groupunits, believer_name
        )

    def get_believer_name_is_labor_bool(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        believer_name: PartnerName,
    ) -> bool:
        if self._partys == {}:
            return True

        for x_party_title, x_groupunit in groupunits.items():
            if x_party_title in self._partys:
                for x_partner_name in x_groupunit._memberships.keys():
                    if x_partner_name == believer_name:
                        return True
        return False

    def set_partys(
        self,
        parent_laborheir,
        laborunit: LaborUnit,
        groupunits: dict[GroupTitle, GroupUnit],
    ):
        self._partys = {}
        # there is no parent laborheir or parent laborheir is empty
        if parent_laborheir is None or parent_laborheir._partys == {}:
            for partyunit in laborunit._partys.values():
                _add_party_to_partys(self._partys, partyunit)
        # current laborunit is not empty and parent laborheir is empty
        elif laborunit._partys == {}:
            for parent_partyheir in parent_laborheir._partys.values():
                _add_party_to_partys(self._partys, parent_partyheir)
        # current laborunit is not empty and parent laborheir is not empty
        else:
            # grab all parent heirs first
            for parent_partyheir in parent_laborheir._partys.values():
                _add_party_to_partys(self._partys, parent_partyheir)
            # if it doesn't exist add current laborunit
            for partyunit in laborunit._partys.values():
                if self._partys.get(partyunit.party_title) is None:
                    _add_party_to_partys(self._partys, partyunit)

        #     # get all_partners of parent laborheir groupunits
        #     all_parent_laborheir_partners = self._get_all_partners(
        #         groupunits=groupunits,
        #         party_title_set=parent_laborheir._partys,
        #     )
        #     # get all_partners of laborunit groupunits
        #     all_laborunit_partners = self._get_all_partners(
        #         groupunits=groupunits,
        #         party_title_set=laborunit._partys,
        #     )

        #     # set dict_x = to laborunit groupunits
        #     for partyunit in laborunit._partys:
        #         x_partys.add(partyunit)

    def has_party(self, party_titles: set[GroupTitle]):
        return self.is_empty() or any(gn_x in self._partys for gn_x in party_titles)


def _add_party_to_partys(partys: dict, x_party):
    x_partyheir = partyheir_shop(party_title=x_party.party_title, solo=x_party.solo)
    partys[x_partyheir.party_title] = x_partyheir


def laborheir_shop(
    _partys: dict[GroupTitle, PartyHeir] = None, _believer_name_is_labor: bool = None
) -> LaborHeir:
    _partys = get_empty_dict_if_None(_partys)
    _believer_name_is_labor = get_False_if_None(_believer_name_is_labor)
    return LaborHeir(_partys=_partys, _believer_name_is_labor=_believer_name_is_labor)


def laborunit_get_from_dict(laborunit_dict: dict) -> LaborUnit:
    x_laborunit = laborunit_shop()
    for x_party_title in laborunit_dict.get("_partys"):
        x_laborunit.add_partyunit(x_party_title)
    return x_laborunit
