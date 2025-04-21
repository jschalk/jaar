from src.a00_data_toolboxs.dict_toolbox import (
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
from src.a01_word_logic.road import (
    default_bridge_if_None,
    get_all_road_tags,
    create_road_from_tags,
    get_terminus_tag,
    get_parent_road,
    combine_roads,
    is_tagunit,
    RoadUnit,
    TagUnit,
    FaceName,
    EventInt,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_word_if_None
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_otx2inxException(Exception):
    pass


class set_tag_Exception(Exception):
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


class TagMap(MapCore):
    def set_otx2inx(self, otx_tag: str, inx_tag: str):
        self.otx2inx[otx_tag] = inx_tag

    def _get_inx_value(self, otx_tag: str) -> str:
        return self.otx2inx.get(otx_tag)

    def otx2inx_exists(self, otx_tag: str, inx_tag: str) -> bool:
        return self._get_inx_value(otx_tag) == inx_tag

    def otx_exists(self, otx_tag: str) -> bool:
        return self._get_inx_value(otx_tag) != None

    def del_otx2inx(self, otx_tag: str):
        self.otx2inx.pop(otx_tag)

    def reveal_inx(self, otx_tag: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_tag) is False:
            inx_tag = copy_copy(otx_tag)
            if self.inx_bridge in otx_tag:
                return None
            otx_r_bridge = self.otx_bridge
            inx_r_bridge = self.inx_bridge
            inx_tag = inx_tag.replace(otx_r_bridge, inx_r_bridge)
            self.set_otx2inx(otx_tag, inx_tag)

        return self._get_inx_value(otx_tag)

    def _is_inx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_bridge_inclusion_correct()
            and self._is_otx_bridge_inclusion_correct()
        )


def tagmap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> TagMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return TagMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_tagmap_from_dict(x_dict: dict) -> TagMap:
    return tagmap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_tagmap_from_json(x_json: str) -> TagMap:
    return get_tagmap_from_dict(get_dict_from_json(x_json))


@dataclass
class RoadMap:
    face_name: FaceName = None
    event_int: EventInt = None
    otx2inx: dict = None
    unknown_word: str = None
    otx_bridge: str = None
    inx_bridge: str = None
    tagmap: TagMap = None

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
        otx_terminus = get_terminus_tag(otx_road, self.otx_bridge)
        otx_terminus = self._get_tagmap_tagunit(otx_terminus)
        if otx_parent_road == "":
            inx_parent_road = ""
        else:
            inx_parent_road = self._get_inx_value(otx_parent_road)
        return combine_roads(inx_parent_road, otx_terminus, self.inx_bridge)

    def _get_tagmap_tagunit(self, x_tagUnit: TagUnit) -> TagUnit:
        if self.otx_tag_exists(x_tagUnit):
            return self.tagmap.reveal_inx(x_tagUnit)
        return x_tagUnit

    def otx2inx_exists(self, otx_road: str, inx_road: str) -> bool:
        return self._get_inx_value(otx_road) == inx_road

    def otx_exists(self, otx_road: str) -> bool:
        return self._get_inx_value(otx_road) != None

    def del_otx2inx(self, otx_road: str):
        self.otx2inx.pop(otx_road)

    def set_tag(self, otx_tag: TagUnit, inx_tag: TagUnit):
        if self.otx_bridge in otx_tag:
            exception_str = f"tag cannot have otx_tag '{otx_tag}'. It must be not have bridge {self.otx_bridge}."
            raise set_tag_Exception(exception_str)
        if self.inx_bridge in inx_tag:
            exception_str = f"tag cannot have inx_tag '{inx_tag}'. It must be not have bridge {self.inx_bridge}."
            raise set_tag_Exception(exception_str)

        self.tagmap.set_otx2inx(otx_tag, inx_tag)
        self._set_new_tag_to_otx_inx(otx_tag, inx_tag)

    def _set_new_tag_to_otx_inx(self, otx_tag, inx_tag):
        for otx_road, inx_road in self.otx2inx.items():
            otx_tagunits = get_all_road_tags(otx_road, self.otx_bridge)
            inx_tagunits = get_all_road_tags(inx_road, self.inx_bridge)
            for x_count, otx_tagunit in enumerate(otx_tagunits):
                if otx_tagunit == otx_tag:
                    inx_tagunits[x_count] = inx_tag
            self.set_otx2inx(otx_road, create_road_from_tags(inx_tagunits))

    def _get_inx_tag(self, otx_tag: TagUnit) -> TagUnit:
        return self.tagmap.otx2inx.get(otx_tag)

    def tag_exists(self, otx_tag: TagUnit, inx_tag: TagUnit) -> bool:
        return self.tagmap.otx2inx_exists(otx_tag, inx_tag)

    def otx_tag_exists(self, otx_tag: TagUnit) -> bool:
        return self.tagmap.otx_exists(otx_tag)

    def del_tag(self, otx_tag: TagUnit) -> bool:
        self.tagmap.del_otx2inx(otx_tag)

    def _unknown_word_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_word, self.otx2inx)

    def all_otx_parent_roads_exist(self) -> bool:
        for x_road in self.otx2inx.keys():
            if is_tagunit(x_road, self.otx_bridge) is False:
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
    x_tagmap: TagMap = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> RoadMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    if x_tagmap is None:
        x_tagmap = tagmap_shop(
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
        tagmap=x_tagmap,
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


def inherit_tagmap(new: TagMap, old: TagMap) -> TagMap:
    return _inherit_mapunit(new, old)


def inherit_roadmap(new: RoadMap, old: RoadMap) -> RoadMap:
    return _inherit_mapunit(new, old)
