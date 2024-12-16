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
    default_wall_if_None,
    get_all_road_ideas,
    create_road_from_ideas,
    get_terminus_idea,
    get_parent_road,
    combine_roads,
    is_ideaunit,
    RoadUnit,
    IdeaUnit,
    FaceID,
    EventID,
)
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_otx2inxException(Exception):
    pass


class set_idea_Exception(Exception):
    pass


@dataclass
class BridgeCore:
    face_id: FaceID = None
    event_id: EventID = None
    otx2inx: dict = None
    unknown_word: str = None
    otx_wall: str = None
    inx_wall: str = None

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
            "face_id": self.face_id,
            "event_id": self.event_id,
            "otx_wall": self.otx_wall,
            "inx_wall": self.inx_wall,
            "unknown_word": self.unknown_word,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


class AcctBridge(BridgeCore):
    def set_otx2inx(self, otx_acct_id: str, inx_acct_id: str):
        self.otx2inx[otx_acct_id] = inx_acct_id

    def _get_inx_value(self, otx_acct_id: str) -> str:
        return self.otx2inx.get(otx_acct_id)

    def otx2inx_exists(self, otx_acct_id: str, inx_acct_id: str) -> bool:
        return self._get_inx_value(otx_acct_id) == inx_acct_id

    def otx_exists(self, otx_acct_id: str) -> bool:
        return self._get_inx_value(otx_acct_id) != None

    def del_otx2inx(self, otx_acct_id: str):
        self.otx2inx.pop(otx_acct_id)

    def reveal_inx(self, otx_acct_id: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_acct_id) is False:
            inx_acct_id = copy_copy(otx_acct_id)
            if self.inx_wall in otx_acct_id:
                return None
            otx_r_wall = self.otx_wall
            inx_r_wall = self.inx_wall
            inx_acct_id = inx_acct_id.replace(otx_r_wall, inx_r_wall)
            self.set_otx2inx(otx_acct_id, inx_acct_id)

        return self._get_inx_value(otx_acct_id)

    def _is_inx_wall_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_wall, self.otx2inx)

    def _is_otx_wall_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_wall, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_wall_inclusion_correct()
            and self._is_otx_wall_inclusion_correct()
        )


def acctbridge_shop(
    face_id: FaceID = None,
    event_id: EventID = None,
    otx_wall: str = None,
    inx_wall: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> AcctBridge:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_wall = default_wall_if_None(otx_wall)
    inx_wall = default_wall_if_None(inx_wall)

    return AcctBridge(
        face_id=face_id,
        event_id=get_0_if_None(event_id),
        otx_wall=otx_wall,
        inx_wall=inx_wall,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_acctbridge_from_dict(x_dict: dict) -> AcctBridge:
    return acctbridge_shop(
        face_id=x_dict.get("face_id"),
        event_id=x_dict.get("event_id"),
        otx_wall=x_dict.get("otx_wall"),
        inx_wall=x_dict.get("inx_wall"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_acctbridge_from_json(x_json: str) -> AcctBridge:
    return get_acctbridge_from_dict(get_dict_from_json(x_json))


class GroupBridge(BridgeCore):
    def set_otx2inx(self, otx_group_id: str, inx_group_id: str):
        self.otx2inx[otx_group_id] = inx_group_id

    def _get_inx_value(self, otx_group_id: str) -> str:
        return self.otx2inx.get(otx_group_id)

    def otx2inx_exists(self, otx_group_id: str, inx_group_id: str) -> bool:
        return self._get_inx_value(otx_group_id) == inx_group_id

    def otx_exists(self, otx_group_id: str) -> bool:
        return self._get_inx_value(otx_group_id) != None

    def del_otx2inx(self, otx_group_id: str):
        self.otx2inx.pop(otx_group_id)

    def reveal_inx(self, otx_group_id: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_group_id) is False:
            inx_group_id = copy_copy(otx_group_id)
            if self.inx_wall in otx_group_id:
                return None
            otx_r_wall = self.otx_wall
            inx_r_wall = self.inx_wall
            inx_group_id = inx_group_id.replace(otx_r_wall, inx_r_wall)
            self.set_otx2inx(otx_group_id, inx_group_id)

        return self._get_inx_value(otx_group_id)

    def _is_inx_wall_inclusion_correct(self):
        return str_in_all_dict_values(self.inx_wall, self.otx2inx)

    def _is_otx_wall_inclusion_correct(self):
        return str_in_all_dict_keys(self.otx_wall, self.otx2inx)

    def is_valid(self):
        return (
            self._is_otx_wall_inclusion_correct()
            and self._is_inx_wall_inclusion_correct()
        )


def groupbridge_shop(
    face_id: FaceID = None,
    event_id: EventID = None,
    otx_wall: str = None,
    inx_wall: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> GroupBridge:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_wall = default_wall_if_None(otx_wall)
    inx_wall = default_wall_if_None(inx_wall)

    return GroupBridge(
        face_id=face_id,
        event_id=get_0_if_None(event_id),
        otx_wall=otx_wall,
        inx_wall=inx_wall,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_groupbridge_from_dict(x_dict: dict) -> GroupBridge:
    return groupbridge_shop(
        face_id=x_dict.get("face_id"),
        event_id=x_dict.get("event_id"),
        otx_wall=x_dict.get("otx_wall"),
        inx_wall=x_dict.get("inx_wall"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_groupbridge_from_json(x_json: str) -> GroupBridge:
    return get_groupbridge_from_dict(get_dict_from_json(x_json))


class IdeaBridge(BridgeCore):
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
            if self.inx_wall in otx_idea:
                return None
            otx_r_wall = self.otx_wall
            inx_r_wall = self.inx_wall
            inx_idea = inx_idea.replace(otx_r_wall, inx_r_wall)
            self.set_otx2inx(otx_idea, inx_idea)

        return self._get_inx_value(otx_idea)

    def _is_inx_wall_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_wall, self.otx2inx)

    def _is_otx_wall_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_wall, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_wall_inclusion_correct()
            and self._is_otx_wall_inclusion_correct()
        )


def ideabridge_shop(
    face_id: FaceID = None,
    event_id: EventID = None,
    otx_wall: str = None,
    inx_wall: str = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> IdeaBridge:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_wall = default_wall_if_None(otx_wall)
    inx_wall = default_wall_if_None(inx_wall)

    return IdeaBridge(
        face_id=face_id,
        event_id=get_0_if_None(event_id),
        otx_wall=otx_wall,
        inx_wall=inx_wall,
        unknown_word=unknown_word,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_ideabridge_from_dict(x_dict: dict) -> IdeaBridge:
    return ideabridge_shop(
        face_id=x_dict.get("face_id"),
        event_id=x_dict.get("event_id"),
        otx_wall=x_dict.get("otx_wall"),
        inx_wall=x_dict.get("inx_wall"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_ideabridge_from_json(x_json: str) -> IdeaBridge:
    return get_ideabridge_from_dict(get_dict_from_json(x_json))


@dataclass
class RoadBridge:
    face_id: FaceID = None
    event_id: EventID = None
    otx2inx: dict = None
    unknown_word: str = None
    otx_wall: str = None
    inx_wall: str = None
    ideabridge: IdeaBridge = None

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
        otx_parent_road = get_parent_road(otx_road, self.otx_wall)
        if self.otx_exists(otx_parent_road) is False and otx_parent_road != "":
            return None
        otx_terminus = get_terminus_idea(otx_road, self.otx_wall)
        otx_terminus = self._get_ideabridge_ideaunit(otx_terminus)
        if otx_parent_road == "":
            inx_parent_road = ""
        else:
            inx_parent_road = self._get_inx_value(otx_parent_road)
        return combine_roads(inx_parent_road, otx_terminus, self.inx_wall)

    def _get_ideabridge_ideaunit(self, x_ideaUnit: IdeaUnit) -> IdeaUnit:
        if self.otx_idea_exists(x_ideaUnit):
            return self.ideabridge.reveal_inx(x_ideaUnit)
        return x_ideaUnit

    def otx2inx_exists(self, otx_road: str, inx_road: str) -> bool:
        return self._get_inx_value(otx_road) == inx_road

    def otx_exists(self, otx_road: str) -> bool:
        return self._get_inx_value(otx_road) != None

    def del_otx2inx(self, otx_road: str):
        self.otx2inx.pop(otx_road)

    def set_idea(self, otx_idea: IdeaUnit, inx_idea: IdeaUnit):
        if self.otx_wall in otx_idea:
            exception_str = f"idea cannot have otx_idea '{otx_idea}'. It must be not have wall {self.otx_wall}."
            raise set_idea_Exception(exception_str)
        if self.inx_wall in inx_idea:
            exception_str = f"idea cannot have inx_idea '{inx_idea}'. It must be not have wall {self.inx_wall}."
            raise set_idea_Exception(exception_str)

        self.ideabridge.set_otx2inx(otx_idea, inx_idea)
        self._set_new_idea_to_otx_inx(otx_idea, inx_idea)

    def _set_new_idea_to_otx_inx(self, otx_idea, inx_idea):
        for otx_road, inx_road in self.otx2inx.items():
            otx_ideaunits = get_all_road_ideas(otx_road, self.otx_wall)
            inx_ideaunits = get_all_road_ideas(inx_road, self.inx_wall)
            for x_count, otx_ideaunit in enumerate(otx_ideaunits):
                if otx_ideaunit == otx_idea:
                    inx_ideaunits[x_count] = inx_idea
            self.set_otx2inx(otx_road, create_road_from_ideas(inx_ideaunits))

    def _get_inx_idea(self, otx_idea: IdeaUnit) -> IdeaUnit:
        return self.ideabridge.otx2inx.get(otx_idea)

    def idea_exists(self, otx_idea: IdeaUnit, inx_idea: IdeaUnit) -> bool:
        return self.ideabridge.otx2inx_exists(otx_idea, inx_idea)

    def otx_idea_exists(self, otx_idea: IdeaUnit) -> bool:
        return self.ideabridge.otx_exists(otx_idea)

    def del_idea(self, otx_idea: IdeaUnit) -> bool:
        self.ideabridge.del_otx2inx(otx_idea)

    def _unknown_word_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_word, self.otx2inx)

    def all_otx_parent_roads_exist(self) -> bool:
        for x_road in self.otx2inx.keys():
            if is_ideaunit(x_road, self.otx_wall) is False:
                parent_road = get_parent_road(x_road, self.otx_wall)
                if self.otx_exists(parent_road) is False:
                    return False
        return True

    def is_valid(self) -> bool:
        return self.all_otx_parent_roads_exist()

    def get_dict(self) -> dict:
        return {
            "face_id": self.face_id,
            "event_id": self.event_id,
            "otx_wall": self.otx_wall,
            "inx_wall": self.inx_wall,
            "unknown_word": self.unknown_word,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def roadbridge_shop(
    face_id: FaceID = None,
    event_id: EventID = None,
    otx_wall: str = None,
    inx_wall: str = None,
    x_ideabridge: IdeaBridge = None,
    otx2inx: dict = None,
    unknown_word: str = None,
) -> RoadBridge:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_wall = default_wall_if_None(otx_wall)
    inx_wall = default_wall_if_None(inx_wall)

    if x_ideabridge is None:
        x_ideabridge = ideabridge_shop(
            otx_wall=otx_wall,
            inx_wall=inx_wall,
            unknown_word=unknown_word,
            face_id=face_id,
            event_id=event_id,
        )

    return RoadBridge(
        otx2inx=get_empty_dict_if_None(otx2inx),
        unknown_word=unknown_word,
        otx_wall=otx_wall,
        inx_wall=inx_wall,
        ideabridge=x_ideabridge,
        face_id=face_id,
        event_id=get_0_if_None(event_id),
    )


def get_roadbridge_from_dict(x_dict: dict) -> RoadBridge:
    return roadbridge_shop(
        face_id=x_dict.get("face_id"),
        event_id=x_dict.get("event_id"),
        otx_wall=x_dict.get("otx_wall"),
        inx_wall=x_dict.get("inx_wall"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_word=x_dict.get("unknown_word"),
    )


def get_roadbridge_from_json(x_json: str) -> RoadBridge:
    return get_roadbridge_from_dict(get_dict_from_json(x_json))


class BridgeCoreAttrConflictException(Exception):
    pass


def _check_core_attributes(new_obj, old_obj):
    if (
        old_obj.face_id != new_obj.face_id
        or old_obj.otx_wall != new_obj.otx_wall
        or old_obj.inx_wall != new_obj.inx_wall
        or old_obj.unknown_word != new_obj.unknown_word
    ):
        raise BridgeCoreAttrConflictException("Core attributes in conflict")
    if old_obj.event_id >= new_obj.event_id:
        raise BridgeCoreAttrConflictException("older bridgeunit is not older")


def _inherit_bridgeunit(new, old):
    _check_core_attributes(new, old)
    for otx_key, old_inx in old.otx2inx.items():
        if new.otx_exists(otx_key) is False:
            new.set_otx2inx(otx_key, old_inx)
    return new


def inherit_acctbridge(new: AcctBridge, old: AcctBridge) -> AcctBridge:
    return _inherit_bridgeunit(new, old)


def inherit_groupbridge(new: GroupBridge, old: GroupBridge) -> GroupBridge:
    return _inherit_bridgeunit(new, old)


def inherit_ideabridge(new: IdeaBridge, old: IdeaBridge) -> IdeaBridge:
    return _inherit_bridgeunit(new, old)


def inherit_roadbridge(new: RoadBridge, old: RoadBridge) -> RoadBridge:
    return _inherit_bridgeunit(new, old)
