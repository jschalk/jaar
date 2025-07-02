from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import get_empty_set_if_None
from src.a03_group_logic.acct import AcctName
from src.a03_group_logic.group import GroupTitle, GroupUnit


class InvalidLaborHeirPopulateException(Exception):
    pass


@dataclass
class LaborUnit:
    _laborlinks: set[GroupTitle]

    def get_dict(self) -> dict[str, str]:
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
    _owner_name_labor: bool

    def _get_all_accts(
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

    def set_owner_name_labor(
        self, groupunits: dict[GroupTitle, GroupUnit], owner_owner_name: AcctName
    ):
        self._owner_name_labor = self.get_owner_name_labor_bool(
            groupunits, owner_owner_name
        )

    def get_owner_name_labor_bool(
        self, groupunits: dict[GroupTitle, GroupUnit], owner_owner_name: AcctName
    ) -> bool:
        if self._laborlinks == set():
            return True

        for x_labor_title, x_groupunit in groupunits.items():
            if x_labor_title in self._laborlinks:
                for x_acct_name in x_groupunit._memberships.keys():
                    if x_acct_name == owner_owner_name:
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
            # get all_accts of parent laborheir groupunits
            all_parent_laborheir_accts = self._get_all_accts(
                groupunits=groupunits,
                labor_title_set=parent_laborheir._laborlinks,
            )
            # get all_accts of laborunit groupunits
            all_laborunit_accts = self._get_all_accts(
                groupunits=groupunits,
                labor_title_set=laborunit._laborlinks,
            )
            if not set(all_laborunit_accts).issubset(set(all_parent_laborheir_accts)):
                # else raise error
                raise InvalidLaborHeirPopulateException(
                    f"parent_laborheir does not contain all accts of the plan's laborunit\n{set(all_parent_laborheir_accts)=}\n\n{set(all_laborunit_accts)=}"
                )

            # set dict_x = to laborunit groupunits
            for laborlink in laborunit._laborlinks:
                x_laborlinks.add(laborlink)
        self._laborlinks = x_laborlinks

    def has_labor(self, labor_titles: set[GroupTitle]):
        return self.is_empty() or any(gn_x in self._laborlinks for gn_x in labor_titles)


def laborheir_shop(
    _laborlinks: set[GroupTitle] = None, _owner_name_labor: bool = None
) -> LaborHeir:
    _laborlinks = get_empty_set_if_None(_laborlinks)
    if _owner_name_labor is None:
        _owner_name_labor = False

    return LaborHeir(_laborlinks=_laborlinks, _owner_name_labor=_owner_name_labor)


def laborunit_get_from_dict(laborunit_dict: dict) -> LaborUnit:
    x_laborunit = laborunit_shop()
    for x_labor_title in laborunit_dict.get("_laborlinks"):
        x_laborunit.set_laborlink(x_labor_title)

    return x_laborunit
