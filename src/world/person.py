from dataclasses import dataclass
from src.culture.culture import CultureUnit, CultureHandle, cultureunit_shop
from src.world.pain import PainGenus, PainUnit, PersonName, painunit_shop


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None
    _cultures: dict[CultureHandle:CultureUnit] = None
    _pains: dict[PainGenus:PainUnit] = None

    def set_pains_empty_if_none(self):
        if self._pains is None:
            self._pains = {}

    def create_painunit_from_genus(self, pain_genus: PainGenus):
        self._pains[pain_genus] = painunit_shop(genus=pain_genus)

    def set_painunit(self, painunit: PainUnit):
        self._pains[painunit.genus] = painunit

    def get_painunit(self, pain_genus: PainGenus) -> PainUnit:
        return self._pains.get(pain_genus)

    def del_painunit(self, pain_genus: PainGenus):
        self._pains.pop(pain_genus)

    def set_painunits_weight_metrics(self):
        total_painunits_weight = sum(
            x_painunit.weight for x_painunit in self._pains.values()
        )
        for x_painunit in self._pains.values():
            x_painunit.set_relative_weight(x_painunit.weight / total_painunits_weight)

    def set_cultureunits_weight_metrics(self):
        self.set_painunits_weight_metrics()
        cultureunit_handles = {
            x_cultureunit.handle: 0 for x_cultureunit in self._cultures.values()
        }

        for x_painunit in self._pains.values():
            for x_healerlink in x_painunit._healerlinks.values():
                for x_culturelink in x_healerlink._culturelinks.values():
                    cultureunit_handles[
                        x_culturelink.handle
                    ] += x_culturelink._person_importance

        for (
            x_cultureunit_handle,
            x_cultureunit_person_importance,
        ) in cultureunit_handles.items():
            self._cultures.get(x_cultureunit_handle).set_person_importance(
                x_cultureunit_person_importance
            )

    def set_cultures_empty_if_none(self):
        if self._cultures is None:
            self._cultures = {}

    def set_cultureunit(self, culture_handle: CultureHandle):
        cultures_dir = f"{self.person_dir}/cultures"
        self._cultures[culture_handle] = cultureunit_shop(
            handle=culture_handle, cultures_dir=cultures_dir
        )

    def get_cultureunit(self, culture_handle: CultureHandle) -> CultureUnit:
        return self._cultures.get(culture_handle)

    def del_cultureunit(self, culture_handle: CultureHandle):
        self._cultures.pop(culture_handle)

    def get_cultures_dict(self) -> dict:
        return {cultureunit_x.handle: None for cultureunit_x in self._cultures.values()}

    def get_pains_dict(self) -> dict:
        return {
            painunit_x.genus: painunit_x.get_dict()
            for painunit_x in self._pains.values()
        }

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "_cultures": self.get_cultures_dict(),
            "_pains": self.get_pains_dict(),
        }


def personunit_shop(name: PersonName, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    person_x = PersonUnit(name=name, person_dir=person_dir)
    person_x.set_cultures_empty_if_none()
    person_x.set_pains_empty_if_none()
    return person_x


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
