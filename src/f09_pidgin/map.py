from src.f00_data_toolboxs.dict_toolbox import (
    get_empty_dict_if_None,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
    get_str_in_sub_dict,
    str_in_all_dict_keys,
    str_in_all_dict_values,
    get_json_from_dict,
    get_dict_from_json,
    get_0_if_None,
)
from src.f01_word_logic.road import (
    default_bridge_if_None,
    get_all_road_titles,
    create_road_from_titles,
    get_terminus_title,
    get_parent_road,
    combine_roads,
    is_titleunit,
    RoadUnit,
    TitleUnit,
    FaceName,
    EventInt,
)
from src.f09_pidgin.pidgin_config import default_unknown_word_if_None
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_otx2inxException(Exception):
    pass


class set_title_Exception(Exception):
    pass


@dataclass
class MapCore:
    face_name: FaceName = None
    event_int: EventInt = None
    otx2inx: dict = None
    unknown_word: str = None
    otx_bridge: str = None
    inx_bridge: str = None

    def _unknown_word_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_word, self.otx2inx)

    def set_all_otx2inx(
        self, x_otx2inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_word, x_otx2inx):
            error_dict = get_str_in_sub_dict(self.unknown_word, x_otx2inx)
            exception_str = f"otx2inx cannot have unknown_word '{self.unknown_word}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx2inxException(exception_str)
        self.otx2inx = x_otx2inx

    def get_dict(self) -> dict:
        return {
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_bridge": self.otx_bridge,
            "inx_bridge": self.inx_bridge,
            "unknown_word": self.unknown_word,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


class NameMap(MapCore):
    def set_otx2inx(self, otx_name: str, inx_name: str):
        self.otx2inx[otx_name] = inx_name

    def _get_inx_value(self, otx_name: str) -> str:
        return self.otx2inx.get(otx_name)

    def otx2inx_exists(self, otx_name: str, inx_name: str) -> bool:
        return self._get_inx_value(otx_name) == inx_name

    def otx_exists(self, otx_name: str) -> bool:
        return self._get_inx_value(otx_name) != None

    def del_otx2inx(self, otx_name: str):
        self.otx2inx.pop(otx_name)

    def reveal_inx(self, otx_name: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_name) is False:
            inx_name = copy_copy(otx_name)
            if self.inx_bridge in otx_name:
                return None
            otx_r_bridge = self.otx_bridge
            inx_r_bridge = self.inx_bridge
            inx_name = inx_name.replace(otx_r_bridge, inx_r_bridge)
            self.set_otx2inx(otx_name, inx_name)

        return self._get_inx_value(otx_name)

    def _is_inx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_bridge_inclusion_correct()
            and self._is_otx_bridge_inclusion_correct()
        )


def namemap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> NameMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return NameMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_namemap_from_dict(x_dict: dict) -> NameMap:
    return namemap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_namemap_from_json(x_json: str) -> NameMap:
    return get_namemap_from_dict(get_dict_from_json(x_json))


class LabelMap(MapCore):
    def set_otx2inx(self, otx_label: str, inx_label: str):
        self.otx2inx[otx_label] = inx_label

    def _get_inx_value(self, otx_label: str) -> str:
        return self.otx2inx.get(otx_label)

    def otx2inx_exists(self, otx_label: str, inx_label: str) -> bool:
        return self._get_inx_value(otx_label) == inx_label

    def otx_exists(self, otx_label: str) -> bool:
        return self._get_inx_value(otx_label) != None

    def del_otx2inx(self, otx_label: str):
        self.otx2inx.pop(otx_label)

    def reveal_inx(self, otx_label: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_label) is False:
            inx_label = copy_copy(otx_label)
            if self.inx_bridge in otx_label:
                return None
            otx_r_bridge = self.otx_bridge
            inx_r_bridge = self.inx_bridge
            inx_label = inx_label.replace(otx_r_bridge, inx_r_bridge)
            self.set_otx2inx(otx_label, inx_label)

        return self._get_inx_value(otx_label)

    def _is_inx_bridge_inclusion_correct(self):
        return str_in_all_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self):
        return str_in_all_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self):
        return (
            self._is_otx_bridge_inclusion_correct()
            and self._is_inx_bridge_inclusion_correct()
        )


def labelmap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> LabelMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return LabelMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_labelmap_from_dict(x_dict: dict) -> LabelMap:
    return labelmap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_labelmap_from_json(x_json: str) -> LabelMap:
    return get_labelmap_from_dict(get_dict_from_json(x_json))


class TitleMap(MapCore):
    def set_otx2inx(self, otx_title: str, inx_title: str):
        self.otx2inx[otx_title] = inx_title

    def _get_inx_value(self, otx_title: str) -> str:
        return self.otx2inx.get(otx_title)

    def otx2inx_exists(self, otx_title: str, inx_title: str) -> bool:
        return self._get_inx_value(otx_title) == inx_title

    def otx_exists(self, otx_title: str) -> bool:
        return self._get_inx_value(otx_title) != None

    def del_otx2inx(self, otx_title: str):
        self.otx2inx.pop(otx_title)

    def reveal_inx(self, otx_title: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_title) is False:
            inx_title = copy_copy(otx_title)
            if self.inx_bridge in otx_title:
                return None
            otx_r_bridge = self.otx_bridge
            inx_r_bridge = self.inx_bridge
            inx_title = inx_title.replace(otx_r_bridge, inx_r_bridge)
            self.set_otx2inx(otx_title, inx_title)

        return self._get_inx_value(otx_title)

    def _is_inx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_bridge_inclusion_correct()
            and self._is_otx_bridge_inclusion_correct()
        )


def titlemap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> TitleMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return TitleMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_titlemap_from_dict(x_dict: dict) -> TitleMap:
    return titlemap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_titlemap_from_json(x_json: str) -> TitleMap:
    return get_titlemap_from_dict(get_dict_from_json(x_json))


@dataclass
class RoadMap:
    face_name: FaceName = None
    event_int: EventInt = None
    otx2inx: dict = None
    unknown_word: str = None
    otx_bridge: str = None
    inx_bridge: str = None
    titlemap: TitleMap = None

    def set_all_otx2inx(
        self, x_otx2inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_word, x_otx2inx):
            error_dict = get_str_in_sub_dict(self.unknown_word, x_otx2inx)
            exception_str = f"otx2inx cannot have unknown_word '{self.unknown_word}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx2inxException(exception_str)
        self.otx2inx = x_otx2inx

    def set_otx2inx(self, otx_road: str, inx_road: str):
        self.otx2inx[otx_road] = inx_road

    def _get_inx_value(self, otx_road: str) -> str:
        return self.otx2inx.get(otx_road)

    def reveal_inx(self, otx_road: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_road) is False:
            inx_road = copy_copy(otx_road)
            inx_road = self._reveal_roadunit_inx(otx_road)
            self.set_otx2inx(otx_road, inx_road)

        return self._get_inx_value(otx_road)

    def _reveal_roadunit_inx(self, otx_road) -> RoadUnit:
        otx_parent_road = get_parent_road(otx_road, self.otx_bridge)
        if self.otx_exists(otx_parent_road) is False and otx_parent_road != "":
            return None
        otx_terminus = get_terminus_title(otx_road, self.otx_bridge)
        otx_terminus = self._get_titlemap_titleunit(otx_terminus)
        if otx_parent_road == "":
            inx_parent_road = ""
        else:
            inx_parent_road = self._get_inx_value(otx_parent_road)
        return combine_roads(inx_parent_road, otx_terminus, self.inx_bridge)

    def _get_titlemap_titleunit(self, x_titleUnit: TitleUnit) -> TitleUnit:
        if self.otx_title_exists(x_titleUnit):
            return self.titlemap.reveal_inx(x_titleUnit)
        return x_titleUnit

    def otx2inx_exists(self, otx_road: str, inx_road: str) -> bool:
        return self._get_inx_value(otx_road) == inx_road

    def otx_exists(self, otx_road: str) -> bool:
        return self._get_inx_value(otx_road) != None

    def del_otx2inx(self, otx_road: str):
        self.otx2inx.pop(otx_road)

    def set_title(self, otx_title: TitleUnit, inx_title: TitleUnit):
        if self.otx_bridge in otx_title:
            exception_str = f"title cannot have otx_title '{otx_title}'. It must be not have bridge {self.otx_bridge}."
            raise set_title_Exception(exception_str)
        if self.inx_bridge in inx_title:
            exception_str = f"title cannot have inx_title '{inx_title}'. It must be not have bridge {self.inx_bridge}."
            raise set_title_Exception(exception_str)

        self.titlemap.set_otx2inx(otx_title, inx_title)
        self._set_new_title_to_otx_inx(otx_title, inx_title)

    def _set_new_title_to_otx_inx(self, otx_title, inx_title):
        for otx_road, inx_road in self.otx2inx.items():
            otx_titleunits = get_all_road_titles(otx_road, self.otx_bridge)
            inx_titleunits = get_all_road_titles(inx_road, self.inx_bridge)
            for x_count, otx_titleunit in enumerate(otx_titleunits):
                if otx_titleunit == otx_title:
                    inx_titleunits[x_count] = inx_title
            self.set_otx2inx(otx_road, create_road_from_titles(inx_titleunits))

    def _get_inx_title(self, otx_title: TitleUnit) -> TitleUnit:
        return self.titlemap.otx2inx.get(otx_title)

    def title_exists(self, otx_title: TitleUnit, inx_title: TitleUnit) -> bool:
        return self.titlemap.otx2inx_exists(otx_title, inx_title)

    def otx_title_exists(self, otx_title: TitleUnit) -> bool:
        return self.titlemap.otx_exists(otx_title)

    def del_title(self, otx_title: TitleUnit) -> bool:
        self.titlemap.del_otx2inx(otx_title)

    def _unknown_word_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_word, self.otx2inx)

    def all_otx_parent_roads_exist(self) -> bool:
        for x_road in self.otx2inx.keys():
            if is_titleunit(x_road, self.otx_bridge) is False:
                parent_road = get_parent_road(x_road, self.otx_bridge)
                if self.otx_exists(parent_road) is False:
                    return False
        return True

    def is_valid(self) -> bool:
        return self.all_otx_parent_roads_exist()

    def get_dict(self) -> dict:
        return {
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_bridge": self.otx_bridge,
            "inx_bridge": self.inx_bridge,
            "unknown_word": self.unknown_word,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def roadmap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    x_titlemap: TitleMap = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> RoadMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    if x_titlemap is None:
        x_titlemap = titlemap_shop(
            otx_bridge=otx_bridge,
            inx_bridge=inx_bridge,
            unknown_word=unknown_word,
            face_name=face_name,
            event_int=event_int,
        )

    return RoadMap(
        otx2inx=get_empty_dict_if_None(otx2inx),
        unknown_word=unknown_word,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        titlemap=x_titlemap,
        face_name=face_name,
        event_int=get_0_if_None(event_int),
    )


def get_roadmap_from_dict(x_dict: dict) -> RoadMap:
    return roadmap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_roadmap_from_json(x_json: str) -> RoadMap:
    return get_roadmap_from_dict(get_dict_from_json(x_json))


class MapCoreAttrConflictException(Exception):
    pass


def _check_core_attributes(new_obj, old_obj):
    if (
        old_obj.face_name != new_obj.face_name
        or old_obj.otx_bridge != new_obj.otx_bridge
        or old_obj.inx_bridge != new_obj.inx_bridge
        or old_obj.unknown_word != new_obj.unknown_word
    ):
        raise MapCoreAttrConflictException("Core attributes in conflict")
    if old_obj.event_int >= new_obj.event_int:
        raise MapCoreAttrConflictException("older mapunit is not older")


def _inherit_mapunit(new, old):
    _check_core_attributes(new, old)
    for otx_key, old_inx in old.otx2inx.items():
        if new.otx_exists(otx_key) is False:
            new.set_otx2inx(otx_key, old_inx)
    return new


def inherit_namemap(new: NameMap, old: NameMap) -> NameMap:
    return _inherit_mapunit(new, old)


def inherit_labelmap(new: LabelMap, old: LabelMap) -> LabelMap:
    return _inherit_mapunit(new, old)


def inherit_titlemap(new: TitleMap, old: TitleMap) -> TitleMap:
    return _inherit_mapunit(new, old)


def inherit_roadmap(new: RoadMap, old: RoadMap) -> RoadMap:
    return _inherit_mapunit(new, old)
