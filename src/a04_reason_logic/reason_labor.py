from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import get_empty_set_if_None
from src.a03_group_logic.group import GroupTitle, GroupUnit
from src.a03_group_logic.partner import PartnerName


class InvalidLaborHeirPopulateException(Exception):
    pass


@dataclass
class LaborUnit:
    _laborlinks: set[GroupTitle]

    def to_dict(self) -> dict[str, str]:
        return {"_laborlinks": list(self._laborlinks)}

    def set_laborlink(self, labor_title: GroupTitle):
        self._laborlinks.add(labor_title)

    def laborlink_exists(self, labor_title: GroupTitle):
        return labor_title in self._laborlinks

    def del_laborlink(self, labor_title: GroupTitle):
        self._laborlinks.remove(labor_title)

    def get_laborlink(self, labor_title: GroupTitle) -> GroupTitle:
        if self.laborlink_exists(labor_title):
            return labor_title


def laborunit_shop(_laborlinks: set[GroupTitle] = None) -> LaborUnit:
    return LaborUnit(get_empty_set_if_None(_laborlinks))


def create_laborunit(laborlink: GroupTitle):
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(laborlink)
    return x_laborunit


@dataclass
class LaborHeir:
    _laborlinks: set[GroupTitle]
    _believer_name_labor: bool

    def _get_all_partners(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        labor_title_set: set[GroupTitle],
    ) -> dict[GroupTitle, GroupUnit]:
        dict_x = {}
        for x_labor_title in labor_title_set:
            dict_x |= groupunits.get(x_labor_title)._memberships
        return dict_x

    def is_empty(self) -> bool:
        return self._laborlinks == set()

    def set_believer_name_labor(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        believer_believer_name: PartnerName,
    ):
        self._believer_name_labor = self.get_believer_name_labor_bool(
            groupunits, believer_believer_name
        )

    def get_believer_name_labor_bool(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        believer_believer_name: PartnerName,
    ) -> bool:
        if self._laborlinks == set():
            return True

        for x_labor_title, x_groupunit in groupunits.items():
            if x_labor_title in self._laborlinks:
                for x_partner_name in x_groupunit._memberships.keys():
                    if x_partner_name == believer_believer_name:
                        return True
        return False

    def set_laborlinks(
        self,
        parent_laborheir,
        laborunit: LaborUnit,
        groupunits: dict[GroupTitle, GroupUnit],
    ):
        x_laborlinks = set()
        if parent_laborheir is None or parent_laborheir._laborlinks == set():
            for laborlink in laborunit._laborlinks:
                x_laborlinks.add(laborlink)
        elif laborunit._laborlinks == set() or (
            parent_laborheir._laborlinks == laborunit._laborlinks
        ):
            for laborlink in parent_laborheir._laborlinks:
                x_laborlinks.add(laborlink)
        else:
            # get all_partners of parent laborheir groupunits
            all_parent_laborheir_partners = self._get_all_partners(
                groupunits=groupunits,
                labor_title_set=parent_laborheir._laborlinks,
            )
            # get all_partners of laborunit groupunits
            all_laborunit_partners = self._get_all_partners(
                groupunits=groupunits,
                labor_title_set=laborunit._laborlinks,
            )
            if not set(all_laborunit_partners).issubset(
                set(all_parent_laborheir_partners)
            ):
                # else raise error
                raise InvalidLaborHeirPopulateException(
                    f"parent_laborheir does not contain all partners of the plan's laborunit\n{set(all_parent_laborheir_partners)=}\n\n{set(all_laborunit_partners)=}"
                )

            # set dict_x = to laborunit groupunits
            for laborlink in laborunit._laborlinks:
                x_laborlinks.add(laborlink)
        self._laborlinks = x_laborlinks

    def has_labor(self, labor_titles: set[GroupTitle]):
        return self.is_empty() or any(gn_x in self._laborlinks for gn_x in labor_titles)


def laborheir_shop(
    _laborlinks: set[GroupTitle] = None, _believer_name_labor: bool = None
) -> LaborHeir:
    _laborlinks = get_empty_set_if_None(_laborlinks)
    if _believer_name_labor is None:
        _believer_name_labor = False

    return LaborHeir(_laborlinks=_laborlinks, _believer_name_labor=_believer_name_labor)


def laborunit_get_from_dict(laborunit_dict: dict) -> LaborUnit:
    x_laborunit = laborunit_shop()
    for x_labor_title in laborunit_dict.get("_laborlinks"):
        x_laborunit.set_laborlink(x_labor_title)

    return x_laborunit
