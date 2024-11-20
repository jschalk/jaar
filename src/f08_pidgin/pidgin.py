from src.f01_road.jaar_config import default_unknown_word
from src.f00_instrument.dict_toolbox import (
    get_0_if_None,
    get_json_from_dict,
    get_dict_from_json,
)
from src.f01_road.finance import TimeLinePoint
from src.f01_road.road import default_wall_if_none, OwnerID
from src.f08_pidgin.bridge import (
    GroupBridge,
    AcctBridge,
    NodeBridge,
    RoadBridge,
    groupbridge_shop,
    acctbridge_shop,
    nodebridge_shop,
    roadbridge_shop,
    get_acctbridge_from_dict,
    get_groupbridge_from_dict,
    get_nodebridge_from_dict,
    get_roadbridge_from_dict,
)
from dataclasses import dataclass


class check_attrException(Exception):
    pass


def pidginable_jaar_types() -> set:
    return {"AcctID", "GroupID", "RoadNode", "RoadUnit"}


def pidginable_atom_args() -> set:
    return {
        "acct_id",
        "awardee_id",
        "road",
        "parent_road",
        "label",
        "healer_id",
        "need",
        "base",
        "pick",
        "group_id",
        "team_id",
    }


@dataclass
class PidginUnit:
    """Per face object that translates any translatable str.
    otx is the reference for the outside, what the face says
    inx is the reference for the inside, what the same inteprets from the face
    Contains a bridgeunit for each translatable type: RoadUnit, AcctID, GroupID...
    """

    event_id: TimeLinePoint = None
    face_id: OwnerID = None
    groupbridge: GroupBridge = None
    acctbridge: AcctBridge = None
    nodebridge: NodeBridge = None
    roadbridge: RoadBridge = None
    unknown_word: str = None
    otx_wall: str = None
    inx_wall: str = None

    def set_groupbridge(self, x_groupbridge: GroupBridge):
        self._check_all_core_attrs_match(x_groupbridge)
        self.groupbridge = x_groupbridge

    def get_groupbridge(self) -> GroupBridge:
        return self.groupbridge

    def set_group_id(self, otx_group_id: str, inx_group_id: str):
        self.groupbridge.set_otx2inx(otx_group_id, inx_group_id)

    def group_id_exists(self, otx_group_id: str, inx_group_id: str):
        return self.groupbridge.otx2inx_exists(otx_group_id, inx_group_id)

    def _get_inx_group_id(self, otx_group_id: str):
        return self.groupbridge._get_inx_value(otx_group_id)

    def del_group_id(self, otx_group_id: str):
        return self.groupbridge.del_otx2inx(otx_group_id)

    def get_bridgeunit(self, x_jaar_type: str):
        if x_jaar_type == "AcctID":
            return self.acctbridge
        elif x_jaar_type == "GroupID":
            return self.groupbridge
        elif x_jaar_type == "RoadNode":
            return self.nodebridge
        elif x_jaar_type == "RoadUnit":
            return self.roadbridge

    def set_acctbridge(self, x_acctbridge: AcctBridge):
        self._check_all_core_attrs_match(x_acctbridge)
        self.acctbridge = x_acctbridge

    def get_acctbridge(self) -> AcctBridge:
        return self.acctbridge

    def set_acct_id(self, otx_acct_id: str, inx_acct_id: str):
        self.acctbridge.set_otx2inx(otx_acct_id, inx_acct_id)

    def acct_id_exists(self, otx_acct_id: str, inx_acct_id: str):
        return self.acctbridge.otx2inx_exists(otx_acct_id, inx_acct_id)

    def _get_inx_acct_id(self, otx_acct_id: str):
        return self.acctbridge._get_inx_value(otx_acct_id)

    def del_acct_id(self, otx_acct_id: str):
        return self.acctbridge.del_otx2inx(otx_acct_id)

    def set_nodebridge(self, x_nodebridge: NodeBridge):
        self._check_all_core_attrs_match(x_nodebridge)
        self.nodebridge = x_nodebridge

    def get_nodebridge(self) -> NodeBridge:
        return self.nodebridge

    def set_node(self, otx_node: str, inx_node: str):
        self.nodebridge.set_otx2inx(otx_node, inx_node)

    def node_exists(self, otx_node: str, inx_node: str):
        return self.nodebridge.otx2inx_exists(otx_node, inx_node)

    def _get_inx_node(self, otx_node: str):
        return self.nodebridge._get_inx_value(otx_node)

    def del_node(self, otx_node: str):
        return self.nodebridge.del_otx2inx(otx_node)

    def set_roadbridge(self, x_roadbridge: RoadBridge):
        self._check_all_core_attrs_match(x_roadbridge)
        self.roadbridge = x_roadbridge

    def get_roadbridge(self) -> RoadBridge:
        return self.roadbridge

    def set_road(self, otx_road: str, inx_road: str):
        self.roadbridge.set_otx2inx(otx_road, inx_road)

    def road_exists(self, otx_road: str, inx_road: str):
        return self.roadbridge.otx2inx_exists(otx_road, inx_road)

    def _get_inx_road(self, otx_road: str):
        return self.roadbridge._get_inx_value(otx_road)

    def del_road(self, otx_road: str):
        return self.roadbridge.del_otx2inx(otx_road)

    def _check_all_core_attrs_match(self, x_bridgecore):
        self._check_attr_match("face_id", x_bridgecore)
        self._check_attr_match("otx_wall", x_bridgecore)
        self._check_attr_match("inx_wall", x_bridgecore)
        self._check_attr_match("unknown_word", x_bridgecore)

    def _check_attr_match(self, attr: str, bridgecore):
        self_attr = getattr(self, attr)
        unit_attr = getattr(bridgecore, attr)
        if self_attr != unit_attr:
            exception_str = f"set_bridgecore Error: PidginUnit {attr} is '{self_attr}', BridgeCore is '{unit_attr}'."
            raise check_attrException(exception_str)

    def is_valid(self) -> bool:
        return (
            self.acctbridge.is_valid()
            and self.groupbridge.is_valid()
            and self.nodebridge.is_valid()
            and self.roadbridge.is_valid()
        )

    def set_otx2inx(self, x_jaar_type: str, x_otx: str, x_inx: str):
        if x_jaar_type == "AcctID":
            self.acctbridge.set_otx2inx(x_otx, x_inx)
        elif x_jaar_type == "GroupID":
            self.groupbridge.set_otx2inx(x_otx, x_inx)
        elif x_jaar_type == "RoadNode":
            self.nodebridge.set_otx2inx(x_otx, x_inx)
        elif x_jaar_type == "RoadUnit":
            self.roadbridge.set_otx2inx(x_otx, x_inx)

    def _get_inx_value(self, x_jaar_type: str, x_otx: str) -> str:
        if x_jaar_type == "AcctID":
            return self.acctbridge._get_inx_value(x_otx)
        elif x_jaar_type == "GroupID":
            return self.groupbridge._get_inx_value(x_otx)
        elif x_jaar_type == "RoadNode":
            return self.nodebridge._get_inx_value(x_otx)
        elif x_jaar_type == "RoadUnit":
            return self.roadbridge._get_inx_value(x_otx)

    def otx2inx_exists(self, x_jaar_type: str, x_otx: str, x_inx: str) -> bool:
        if x_jaar_type == "AcctID":
            return self.acctbridge.otx2inx_exists(x_otx, x_inx)
        elif x_jaar_type == "GroupID":
            return self.groupbridge.otx2inx_exists(x_otx, x_inx)
        elif x_jaar_type == "RoadNode":
            return self.nodebridge.otx2inx_exists(x_otx, x_inx)
        elif x_jaar_type == "RoadUnit":
            return self.roadbridge.otx2inx_exists(x_otx, x_inx)

    def del_otx2inx(self, x_jaar_type: str, x_otx: str):
        if x_jaar_type == "AcctID":
            self.acctbridge.del_otx2inx(x_otx)
        elif x_jaar_type == "GroupID":
            self.groupbridge.del_otx2inx(x_otx)
        elif x_jaar_type == "RoadNode":
            self.nodebridge.del_otx2inx(x_otx)
        elif x_jaar_type == "RoadUnit":
            self.roadbridge.del_otx2inx(x_otx)

    def set_nub_label(self, x_otx: str, x_inx: str):
        self.roadbridge.set_nub_label(x_otx, x_inx)

    def _get_nub_inx_label(self, x_otx: str) -> str:
        return self.roadbridge._get_nub_inx_label(x_otx)

    def nub_label_exists(self, x_otx: str, x_inx: str) -> bool:
        return self.roadbridge.nub_label_exists(x_otx, x_inx)

    def del_nub_label(self, x_otx: str):
        self.roadbridge.del_nub_label(x_otx)

    def get_dict(self) -> dict:
        return {
            "face_id": self.face_id,
            "event_id": self.event_id,
            "otx_wall": self.otx_wall,
            "inx_wall": self.inx_wall,
            "unknown_word": self.unknown_word,
            "acctbridge": self.acctbridge.get_dict(),
            "nodebridge": self.nodebridge.get_dict(),
            "groupbridge": self.groupbridge.get_dict(),
            "roadbridge": self.roadbridge.get_dict(),
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def pidginunit_shop(
    x_face_id: OwnerID,
    x_event_id: TimeLinePoint = None,
    x_otx_wall: str = None,
    x_inx_wall: str = None,
    x_unknown_word: str = None,
) -> PidginUnit:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_otx_wall is None:
        x_otx_wall = default_wall_if_none()
    if x_inx_wall is None:
        x_inx_wall = default_wall_if_none()

    return PidginUnit(
        face_id=x_face_id,
        event_id=get_0_if_None(x_event_id),
        unknown_word=x_unknown_word,
        otx_wall=x_otx_wall,
        inx_wall=x_inx_wall,
        groupbridge=groupbridge_shop(
            x_otx_wall=x_otx_wall,
            x_inx_wall=x_inx_wall,
            x_unknown_word=x_unknown_word,
            x_face_id=x_face_id,
        ),
        acctbridge=acctbridge_shop(
            x_otx_wall=x_otx_wall,
            x_inx_wall=x_inx_wall,
            x_unknown_word=x_unknown_word,
            x_face_id=x_face_id,
        ),
        nodebridge=nodebridge_shop(
            x_otx_wall=x_otx_wall,
            x_inx_wall=x_inx_wall,
            x_unknown_word=x_unknown_word,
            x_face_id=x_face_id,
        ),
        roadbridge=roadbridge_shop(
            x_otx_wall=x_otx_wall,
            x_inx_wall=x_inx_wall,
            x_unknown_word=x_unknown_word,
            x_face_id=x_face_id,
        ),
    )


def get_pidginunit_from_dict(x_dict: dict) -> PidginUnit:
    return PidginUnit(
        face_id=x_dict.get("face_id"),
        event_id=x_dict.get("event_id"),
        otx_wall=x_dict.get("otx_wall"),
        inx_wall=x_dict.get("inx_wall"),
        unknown_word=x_dict.get("unknown_word"),
        acctbridge=get_acctbridge_from_dict(x_dict.get("acctbridge")),
        groupbridge=get_groupbridge_from_dict(x_dict.get("groupbridge")),
        roadbridge=get_roadbridge_from_dict(x_dict.get("roadbridge")),
    )


def get_pidginunit_from_json(x_json: str) -> PidginUnit:
    return get_pidginunit_from_dict(get_dict_from_json(x_json))
