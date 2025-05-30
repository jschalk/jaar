from src.a00_data_toolbox.dict_toolbox import (
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
from src.a01_way_logic.way import (
    default_bridge_if_None,
    create_way,
    get_all_way_labels,
    create_way_from_labels,
    get_tail_label,
    get_parent_way,
    is_labelterm,
    WayTerm,
    LabelTerm,
    FaceName,
    EventInt,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_str_if_None
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_otx2inxException(Exception):
    pass


class set_label_Exception(Exception):
    pass


@dataclass
class MapCore:
    face_name: FaceName = None
    event_int: EventInt = None
    otx2inx: dict = None
    unknown_str: str = None
    otx_bridge: str = None
    inx_bridge: str = None

    def _unknown_str_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_str, self.otx2inx)

    def set_all_otx2inx(
        self, x_otx2inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_str, x_otx2inx):
            error_dict = get_str_in_sub_dict(self.unknown_str, x_otx2inx)
            exception_str = f"otx2inx cannot have unknown_str '{self.unknown_str}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx2inxException(exception_str)
        self.otx2inx = x_otx2inx

    def get_dict(self) -> dict:
        return {
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_bridge": self.otx_bridge,
            "inx_bridge": self.inx_bridge,
            "unknown_str": self.unknown_str,
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
    unknown_str: str = None,
) -> NameMap:
    unknown_str = default_unknown_str_if_None(unknown_str)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return NameMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_str=unknown_str,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_namemap_from_dict(x_dict: dict) -> NameMap:
    return namemap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_str=x_dict.get("unknown_str"),
    )


def get_namemap_from_json(x_json: str) -> NameMap:
    return get_namemap_from_dict(get_dict_from_json(x_json))


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

    def _is_inx_bridge_inclusion_correct(self):
        return str_in_all_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self):
        return str_in_all_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self):
        return (
            self._is_otx_bridge_inclusion_correct()
            and self._is_inx_bridge_inclusion_correct()
        )


def titlemap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_str: str = None,
) -> TitleMap:
    unknown_str = default_unknown_str_if_None(unknown_str)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return TitleMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_str=unknown_str,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_titlemap_from_dict(x_dict: dict) -> TitleMap:
    return titlemap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_str=x_dict.get("unknown_str"),
    )


def get_titlemap_from_json(x_json: str) -> TitleMap:
    return get_titlemap_from_dict(get_dict_from_json(x_json))


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

    def _is_inx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_bridge_inclusion_correct()
            and self._is_otx_bridge_inclusion_correct()
        )


def labelmap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_str: str = None,
) -> LabelMap:
    unknown_str = default_unknown_str_if_None(unknown_str)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return LabelMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_str=unknown_str,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_labelmap_from_dict(x_dict: dict) -> LabelMap:
    return labelmap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_str=x_dict.get("unknown_str"),
    )


def get_labelmap_from_json(x_json: str) -> LabelMap:
    return get_labelmap_from_dict(get_dict_from_json(x_json))


@dataclass
class WayMap:
    face_name: FaceName = None
    event_int: EventInt = None
    otx2inx: dict = None
    unknown_str: str = None
    otx_bridge: str = None
    inx_bridge: str = None
    labelmap: LabelMap = None

    def set_all_otx2inx(
        self, x_otx2inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_str, x_otx2inx):
            error_dict = get_str_in_sub_dict(self.unknown_str, x_otx2inx)
            exception_str = f"otx2inx cannot have unknown_str '{self.unknown_str}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx2inxException(exception_str)
        self.otx2inx = x_otx2inx

    def set_otx2inx(self, otx_way: str, inx_way: str):
        self.otx2inx[otx_way] = inx_way

    def _get_inx_value(self, otx_way: str) -> str:
        return self.otx2inx.get(otx_way)

    def reveal_inx(self, otx_way: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_way) is False:
            inx_way = copy_copy(otx_way)
            inx_way = self._reveal_wayterm_inx(otx_way)
            self.set_otx2inx(otx_way, inx_way)

        return self._get_inx_value(otx_way)

    def _reveal_wayterm_inx(self, otx_way) -> WayTerm:
        otx_parent_way = get_parent_way(otx_way, self.otx_bridge)
        if self.otx_exists(otx_parent_way) is False and otx_parent_way != "":
            return None
        otx_tail = get_tail_label(otx_way, self.otx_bridge)
        otx_tail = self._get_labelmap_labelterm(otx_tail)
        if otx_parent_way == "":
            inx_parent_way = ""
        else:
            inx_parent_way = self._get_inx_value(otx_parent_way)
        return create_way(inx_parent_way, otx_tail, self.inx_bridge)

    def _get_labelmap_labelterm(self, x_labelTerm: LabelTerm) -> LabelTerm:
        if self.otx_label_exists(x_labelTerm):
            return self.labelmap.reveal_inx(x_labelTerm)
        return x_labelTerm

    def otx2inx_exists(self, otx_way: str, inx_way: str) -> bool:
        return self._get_inx_value(otx_way) == inx_way

    def otx_exists(self, otx_way: str) -> bool:
        return self._get_inx_value(otx_way) != None

    def del_otx2inx(self, otx_way: str):
        self.otx2inx.pop(otx_way)

    def set_label(self, otx_label: LabelTerm, inx_label: LabelTerm):
        if self.otx_bridge in otx_label:
            exception_str = f"label cannot have otx_label '{otx_label}'. It must be not have bridge {self.otx_bridge}."
            raise set_label_Exception(exception_str)
        if self.inx_bridge in inx_label:
            exception_str = f"label cannot have inx_label '{inx_label}'. It must be not have bridge {self.inx_bridge}."
            raise set_label_Exception(exception_str)

        self.labelmap.set_otx2inx(otx_label, inx_label)
        self._set_new_label_to_otx_inx(otx_label, inx_label)

    def _set_new_label_to_otx_inx(self, otx_label, inx_label):
        for otx_way, inx_way in self.otx2inx.items():
            otx_labelterms = get_all_way_labels(otx_way, self.otx_bridge)
            inx_labelterms = get_all_way_labels(inx_way, self.inx_bridge)
            for x_count, otx_labelterm in enumerate(otx_labelterms):
                if otx_labelterm == otx_label:
                    inx_labelterms[x_count] = inx_label
            self.set_otx2inx(otx_way, create_way_from_labels(inx_labelterms))

    def _get_inx_label(self, otx_label: LabelTerm) -> LabelTerm:
        return self.labelmap.otx2inx.get(otx_label)

    def label_exists(self, otx_label: LabelTerm, inx_label: LabelTerm) -> bool:
        return self.labelmap.otx2inx_exists(otx_label, inx_label)

    def otx_label_exists(self, otx_label: LabelTerm) -> bool:
        return self.labelmap.otx_exists(otx_label)

    def del_label(self, otx_label: LabelTerm) -> bool:
        self.labelmap.del_otx2inx(otx_label)

    def _unknown_str_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_str, self.otx2inx)

    def all_otx_parent_ways_exist(self) -> bool:
        for x_way in self.otx2inx.keys():
            print(f"{x_way=}")
            parent_way = get_parent_way(x_way, self.otx_bridge)
            if parent_way and self.otx_exists(parent_way) is False:
                print("false")
                return False
        return True

    def is_valid(self) -> bool:
        return self.all_otx_parent_ways_exist()

    def get_dict(self) -> dict:
        return {
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_bridge": self.otx_bridge,
            "inx_bridge": self.inx_bridge,
            "unknown_str": self.unknown_str,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def waymap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    x_labelmap: LabelMap = None,
    otx2inx: dict = None,
    unknown_str: str = None,
) -> WayMap:
    unknown_str = default_unknown_str_if_None(unknown_str)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    if x_labelmap is None:
        x_labelmap = labelmap_shop(
            otx_bridge=otx_bridge,
            inx_bridge=inx_bridge,
            unknown_str=unknown_str,
            face_name=face_name,
            event_int=event_int,
        )

    return WayMap(
        otx2inx=get_empty_dict_if_None(otx2inx),
        unknown_str=unknown_str,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        labelmap=x_labelmap,
        face_name=face_name,
        event_int=get_0_if_None(event_int),
    )


def get_waymap_from_dict(x_dict: dict) -> WayMap:
    return waymap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_str=x_dict.get("unknown_str"),
    )


def get_waymap_from_json(x_json: str) -> WayMap:
    return get_waymap_from_dict(get_dict_from_json(x_json))


class MapCoreAttrConflictException(Exception):
    pass


def _check_core_attributes(new_obj, old_obj):
    if (
        old_obj.face_name != new_obj.face_name
        or old_obj.otx_bridge != new_obj.otx_bridge
        or old_obj.inx_bridge != new_obj.inx_bridge
        or old_obj.unknown_str != new_obj.unknown_str
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


def inherit_titlemap(new: TitleMap, old: TitleMap) -> TitleMap:
    return _inherit_mapunit(new, old)


def inherit_labelmap(new: LabelMap, old: LabelMap) -> LabelMap:
    return _inherit_mapunit(new, old)


def inherit_waymap(new: WayMap, old: WayMap) -> WayMap:
    return _inherit_mapunit(new, old)
