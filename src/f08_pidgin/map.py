from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f00_instrument.dict_toolbox import (
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
from src.f01_road.road import (
    default_bridge_if_None,
    get_all_road_ideas,
    create_road_from_ideas,
    get_terminus_idea,
    get_parent_road,
    combine_roads,
    is_ideaunit,
    RoadUnit,
    IdeaUnit,
    FaceName,
    EventInt,
)
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_otx2inxException(Exception):
    pass


class set_idea_Exception(Exception):
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


class AcctMap(MapCore):
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


def acctmap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> AcctMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return AcctMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_acctmap_from_dict(x_dict: dict) -> AcctMap:
    return acctmap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_acctmap_from_json(x_json: str) -> AcctMap:
    return get_acctmap_from_dict(get_dict_from_json(x_json))


class GroupMap(MapCore):
    def set_otx2inx(self, otx_group_label: str, inx_group_label: str):
        self.otx2inx[otx_group_label] = inx_group_label

    def _get_inx_value(self, otx_group_label: str) -> str:
        return self.otx2inx.get(otx_group_label)

    def otx2inx_exists(self, otx_group_label: str, inx_group_label: str) -> bool:
        return self._get_inx_value(otx_group_label) == inx_group_label

    def otx_exists(self, otx_group_label: str) -> bool:
        return self._get_inx_value(otx_group_label) != None

    def del_otx2inx(self, otx_group_label: str):
        self.otx2inx.pop(otx_group_label)

    def reveal_inx(self, otx_group_label: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_group_label) is False:
            inx_group_label = copy_copy(otx_group_label)
            if self.inx_bridge in otx_group_label:
                return None
            otx_r_bridge = self.otx_bridge
            inx_r_bridge = self.inx_bridge
            inx_group_label = inx_group_label.replace(otx_r_bridge, inx_r_bridge)
            self.set_otx2inx(otx_group_label, inx_group_label)

        return self._get_inx_value(otx_group_label)

    def _is_inx_bridge_inclusion_correct(self):
        return str_in_all_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self):
        return str_in_all_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self):
        return (
            self._is_otx_bridge_inclusion_correct()
            and self._is_inx_bridge_inclusion_correct()
        )


def groupmap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> GroupMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return GroupMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_groupmap_from_dict(x_dict: dict) -> GroupMap:
    return groupmap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_groupmap_from_json(x_json: str) -> GroupMap:
    return get_groupmap_from_dict(get_dict_from_json(x_json))


class IdeaMap(MapCore):
    def set_otx2inx(self, otx_idea: str, inx_idea: str):
        self.otx2inx[otx_idea] = inx_idea

    def _get_inx_value(self, otx_idea: str) -> str:
        return self.otx2inx.get(otx_idea)

    def otx2inx_exists(self, otx_idea: str, inx_idea: str) -> bool:
        return self._get_inx_value(otx_idea) == inx_idea

    def otx_exists(self, otx_idea: str) -> bool:
        return self._get_inx_value(otx_idea) != None

    def del_otx2inx(self, otx_idea: str):
        self.otx2inx.pop(otx_idea)

    def reveal_inx(self, otx_idea: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_idea) is False:
            inx_idea = copy_copy(otx_idea)
            if self.inx_bridge in otx_idea:
                return None
            otx_r_bridge = self.otx_bridge
            inx_r_bridge = self.inx_bridge
            inx_idea = inx_idea.replace(otx_r_bridge, inx_r_bridge)
            self.set_otx2inx(otx_idea, inx_idea)

        return self._get_inx_value(otx_idea)

    def _is_inx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_bridge_inclusion_correct()
            and self._is_otx_bridge_inclusion_correct()
        )


def ideamap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> IdeaMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return IdeaMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_ideamap_from_dict(x_dict: dict) -> IdeaMap:
    return ideamap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_ideamap_from_json(x_json: str) -> IdeaMap:
    return get_ideamap_from_dict(get_dict_from_json(x_json))


@dataclass
class RoadMap:
    face_name: FaceName = None
    event_int: EventInt = None
    otx2inx: dict = None
    unknown_word: str = None
    otx_bridge: str = None
    inx_bridge: str = None
    ideamap: IdeaMap = None

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
        otx_terminus = get_terminus_idea(otx_road, self.otx_bridge)
        otx_terminus = self._get_ideamap_ideaunit(otx_terminus)
        if otx_parent_road == "":
            inx_parent_road = ""
        else:
            inx_parent_road = self._get_inx_value(otx_parent_road)
        return combine_roads(inx_parent_road, otx_terminus, self.inx_bridge)

    def _get_ideamap_ideaunit(self, x_ideaUnit: IdeaUnit) -> IdeaUnit:
        if self.otx_idea_exists(x_ideaUnit):
            return self.ideamap.reveal_inx(x_ideaUnit)
        return x_ideaUnit

    def otx2inx_exists(self, otx_road: str, inx_road: str) -> bool:
        return self._get_inx_value(otx_road) == inx_road

    def otx_exists(self, otx_road: str) -> bool:
        return self._get_inx_value(otx_road) != None

    def del_otx2inx(self, otx_road: str):
        self.otx2inx.pop(otx_road)

    def set_idea(self, otx_idea: IdeaUnit, inx_idea: IdeaUnit):
        if self.otx_bridge in otx_idea:
            exception_str = f"idea cannot have otx_idea '{otx_idea}'. It must be not have bridge {self.otx_bridge}."
            raise set_idea_Exception(exception_str)
        if self.inx_bridge in inx_idea:
            exception_str = f"idea cannot have inx_idea '{inx_idea}'. It must be not have bridge {self.inx_bridge}."
            raise set_idea_Exception(exception_str)

        self.ideamap.set_otx2inx(otx_idea, inx_idea)
        self._set_new_idea_to_otx_inx(otx_idea, inx_idea)

    def _set_new_idea_to_otx_inx(self, otx_idea, inx_idea):
        for otx_road, inx_road in self.otx2inx.items():
            otx_ideaunits = get_all_road_ideas(otx_road, self.otx_bridge)
            inx_ideaunits = get_all_road_ideas(inx_road, self.inx_bridge)
            for x_count, otx_ideaunit in enumerate(otx_ideaunits):
                if otx_ideaunit == otx_idea:
                    inx_ideaunits[x_count] = inx_idea
            self.set_otx2inx(otx_road, create_road_from_ideas(inx_ideaunits))

    def _get_inx_idea(self, otx_idea: IdeaUnit) -> IdeaUnit:
        return self.ideamap.otx2inx.get(otx_idea)

    def idea_exists(self, otx_idea: IdeaUnit, inx_idea: IdeaUnit) -> bool:
        return self.ideamap.otx2inx_exists(otx_idea, inx_idea)

    def otx_idea_exists(self, otx_idea: IdeaUnit) -> bool:
        return self.ideamap.otx_exists(otx_idea)

    def del_idea(self, otx_idea: IdeaUnit) -> bool:
        self.ideamap.del_otx2inx(otx_idea)

    def _unknown_word_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_word, self.otx2inx)

    def all_otx_parent_roads_exist(self) -> bool:
        for x_road in self.otx2inx.keys():
            if is_ideaunit(x_road, self.otx_bridge) is False:
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
    x_ideamap: IdeaMap = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> RoadMap:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    if x_ideamap is None:
        x_ideamap = ideamap_shop(
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
        ideamap=x_ideamap,
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


def inherit_acctmap(new: AcctMap, old: AcctMap) -> AcctMap:
    return _inherit_mapunit(new, old)


def inherit_groupmap(new: GroupMap, old: GroupMap) -> GroupMap:
    return _inherit_mapunit(new, old)


def inherit_ideamap(new: IdeaMap, old: IdeaMap) -> IdeaMap:
    return _inherit_mapunit(new, old)


def inherit_roadmap(new: RoadMap, old: RoadMap) -> RoadMap:
    return _inherit_mapunit(new, old)
