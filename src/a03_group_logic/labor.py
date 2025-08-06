from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import get_empty_set_if_None, get_False_if_None
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
    _partys: dict[GroupTitle, PartyUnit]

    def to_dict(self) -> dict[str, str]:
        return {"_partys": list(self._partys)}

    def set_partyunit(self, party_title: GroupTitle):
        self._partys.add(party_title)

    def partyunit_exists(self, party_title: GroupTitle):
        return party_title in self._partys

    def del_partyunit(self, party_title: GroupTitle):
        self._partys.remove(party_title)

    def get_partyunit(self, party_title: GroupTitle) -> GroupTitle:
        if self.partyunit_exists(party_title):
            return party_title


def laborunit_shop(_partys: set[GroupTitle] = None) -> LaborUnit:
    return LaborUnit(get_empty_set_if_None(_partys))


def create_laborunit(partyunit: GroupTitle):
    x_laborunit = laborunit_shop()
    x_laborunit.set_partyunit(partyunit)
    return x_laborunit


@dataclass
class LaborHeir:
    _partys: set[GroupTitle]
    _believer_name_is_labor: bool

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
        return self._partys == set()

    def set_believer_name_is_labor(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        believer_believer_name: PartnerName,
    ):
        self._believer_name_is_labor = self.get_believer_name_is_labor_bool(
            groupunits, believer_believer_name
        )

    def get_believer_name_is_labor_bool(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        believer_believer_name: PartnerName,
    ) -> bool:
        if self._partys == set():
            return True

        for x_party_title, x_groupunit in groupunits.items():
            if x_party_title in self._partys:
                for x_partner_name in x_groupunit._memberships.keys():
                    if x_partner_name == believer_believer_name:
                        return True
        return False

    def set_partys(
        self,
        parent_laborheir,
        laborunit: LaborUnit,
        groupunits: dict[GroupTitle, GroupUnit],
    ):
        x_partys = set()
        if parent_laborheir is None or parent_laborheir._partys == set():
            for partyunit in laborunit._partys:
                x_partys.add(partyunit)
        elif laborunit._partys == set() or (
            parent_laborheir._partys == laborunit._partys
        ):
            for partyunit in parent_laborheir._partys:
                x_partys.add(partyunit)
        else:
            # get all_partners of parent laborheir groupunits
            all_parent_laborheir_partners = self._get_all_partners(
                groupunits=groupunits,
                party_title_set=parent_laborheir._partys,
            )
            # get all_partners of laborunit groupunits
            all_laborunit_partners = self._get_all_partners(
                groupunits=groupunits,
                party_title_set=laborunit._partys,
            )
            if not set(all_laborunit_partners).issubset(
                set(all_parent_laborheir_partners)
            ):
                # else raise error
                raise InvalidLaborHeirPopulateException(
                    f"parent_laborheir does not contain all partners of the plan's laborunit\n{set(all_parent_laborheir_partners)=}\n\n{set(all_laborunit_partners)=}"
                )

            # set dict_x = to laborunit groupunits
            for partyunit in laborunit._partys:
                x_partys.add(partyunit)
        self._partys = x_partys

    def has_labor(self, party_titles: set[GroupTitle]):
        return self.is_empty() or any(gn_x in self._partys for gn_x in party_titles)


def laborheir_shop(
    _partys: set[GroupTitle] = None, _believer_name_is_labor: bool = None
) -> LaborHeir:
    _partys = get_empty_set_if_None(_partys)
    if _believer_name_is_labor is None:
        _believer_name_is_labor = False

    return LaborHeir(_partys=_partys, _believer_name_is_labor=_believer_name_is_labor)


def laborunit_get_from_dict(laborunit_dict: dict) -> LaborUnit:
    x_laborunit = laborunit_shop()
    for x_party_title in laborunit_dict.get("_partys"):
        x_laborunit.set_partyunit(x_party_title)

    return x_laborunit
