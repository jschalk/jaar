from src.f00_instrument.file import is_path_valid
from pathlib import Path as pathlib_Path


class InvalidRoadUnitException(Exception):
    pass


class RoadNode(str):
    """A string presentation of a tree node. Nodes cannot contain RoadUnit delimiter"""

    def is_node(self, delimiter: str = None) -> bool:
        return self.find(default_road_delimiter_if_none(delimiter)) == -1


class FiscalID(RoadNode):  # Created to help track the concept
    pass


class OwnerID(RoadNode):  # Created to help track the concept
    """Must be node thus not include road delimiter"""

    pass


class HealerID(OwnerID):
    """A RoadNode used to identify a Problem's Healer"""

    pass


class OwnerID(HealerID):
    """A RoadNode used to identify a BudUnit's owner_id"""

    pass


class AcctID(OwnerID):  # Created to help track the concept
    """Every AcctID object is OwnerID, must follow OwnerID format."""

    pass


class TimeLineLabel(RoadNode):
    "TimeLineLabel is required for every TimeLineUnit. It is a RoadNode that must not container the road_delimiter."

    pass


class RoadUnit(str):
    """A string presentation of a tree path. RoadNodes are seperated by road delimiter"""

    pass


class DoarUnit(str):
    """DoarUnit is a RoadUnit in reverse direction. A string presentation of a tree path. RoadNodes are seperated by road delimiter."""

    pass


class GroupID(str):  # Created to help track the concept
    pass


class WorldID(str):
    pass


def get_default_world_id() -> WorldID:
    return WorldID("TestingWorld3")


class FaceID(str):
    pass


def get_default_face_id() -> FaceID:
    return FaceID("Face1234")


def default_road_delimiter_if_none(delimiter: str = None) -> str:
    return delimiter if delimiter is not None else ";"


def rebuild_road(
    subj_road: RoadUnit, old_road: RoadUnit, new_road: RoadUnit
) -> RoadUnit:
    if subj_road is None:
        return subj_road
    elif is_sub_road(subj_road, old_road):
        return subj_road.replace(old_road, new_road, 1)
    else:
        return subj_road


def is_sub_road(ref_road: RoadUnit, sub_road: RoadUnit) -> bool:
    ref_road = "" if ref_road is None else ref_road
    return ref_road.find(sub_road) == 0


def is_heir_road(src: RoadUnit, heir: RoadUnit, delimiter: str = None) -> bool:
    return (
        src == heir
        or heir.find(f"{src}{default_road_delimiter_if_none(delimiter)}") == 0
    )


def find_replace_road_key_dict(
    dict_x: dict, old_road: RoadUnit, new_road: RoadUnit
) -> dict:
    keys_to_delete = []
    objs_to_add = []
    for x_key, x_obj in dict_x.items():
        if old_road != new_road and is_sub_road(ref_road=x_key, sub_road=old_road):
            x_obj.find_replace_road(old_road=old_road, new_road=new_road)
            objs_to_add.append(x_obj)
            keys_to_delete.append(x_key)

    for x_obj in objs_to_add:
        dict_x[x_obj.get_obj_key()] = x_obj

    for x_key in keys_to_delete:
        dict_x.pop(x_key)

    return dict_x


def get_all_road_nodes(road: RoadUnit, delimiter: str = None) -> list[RoadNode]:
    return road.split(default_road_delimiter_if_none(delimiter))


def get_terminus_node(road: RoadUnit, delimiter: str = None) -> RoadNode:
    return get_all_road_nodes(road=road, delimiter=delimiter)[-1]


def get_parent_road(
    road: RoadUnit, delimiter: str = None
) -> RoadUnit:  # road without terminus node
    parent_nodes = get_all_road_nodes(road=road, delimiter=delimiter)[:-1]
    return create_road_from_nodes(parent_nodes, delimiter=delimiter)


def create_road_without_root_node(
    road: RoadUnit, delimiter: str = None
) -> RoadUnit:  # road without terminus nodef
    if road[:1] == default_road_delimiter_if_none(delimiter):
        raise InvalidRoadUnitException(
            f"Cannot create_road_without_root_node of '{road}' because it has no root node."
        )
    road_without_root_node = create_road_from_nodes(get_all_road_nodes(road=road)[1:])
    return f"{default_road_delimiter_if_none(delimiter)}{road_without_root_node}"


def get_root_node_from_road(road: RoadUnit, delimiter: str = None) -> RoadNode:
    return get_all_road_nodes(road=road, delimiter=delimiter)[0]


def road_validate(road: RoadUnit, delimiter: str, root_node: RoadNode) -> RoadUnit:
    if road == "" or road is None:
        return RoadUnit("")
    x_root = get_root_node_from_road(road, delimiter)
    return (
        rebuild_road(
            subj_road=road,
            old_road=x_root,
            new_road=root_node,
        )
        if x_root != root_node
        else road
    )


def get_ancestor_roads(road: RoadUnit) -> list[RoadUnit]:
    if road is None:
        return []
    nodes = get_all_road_nodes(road)
    temp_road = nodes.pop(0)

    temp_roads = [temp_road]
    if nodes != []:
        while nodes != []:
            temp_road = create_road(temp_road, nodes.pop(0))
            temp_roads.append(temp_road)

    x_roads = []
    while temp_roads != []:
        x_roads.append(temp_roads.pop(len(temp_roads) - 1))
    return x_roads


def all_roadunits_between(src_road, dst_road) -> list[RoadUnit]:
    x_list = []
    anc_roads = get_ancestor_roads(dst_road)
    while anc_roads != []:
        anc_road = anc_roads.pop()
        if is_sub_road(anc_road, src_road):
            x_list.append(anc_road)
    return x_list


class ForeFatherException(Exception):
    pass


def get_forefather_roads(road: RoadUnit) -> dict[RoadUnit]:
    ancestor_roads = get_ancestor_roads(road=road)
    popped_road = ancestor_roads.pop(0)
    if popped_road != road:
        raise ForeFatherException(
            f"Incorrect road {popped_road} from out of ancestor_roads."
        )
    return {a_road: None for a_road in ancestor_roads}


def get_default_fiscal_id_roadnode() -> FiscalID:
    return "ZZ"


def create_road_from_nodes(nodes: list[RoadNode], delimiter: str = None) -> RoadUnit:
    return default_road_delimiter_if_none(delimiter).join(nodes)


def create_road(
    parent_road: RoadUnit, terminus_node: RoadNode = None, delimiter: str = None
) -> RoadUnit:
    if terminus_node is None:
        return RoadUnit(parent_road)
    else:
        return RoadUnit(
            terminus_node
            if parent_road in {"", None}
            else f"{parent_road}{default_road_delimiter_if_none(delimiter)}{terminus_node}"
        )


def get_diff_road(x_road: RoadUnit, sub_road: RoadUnit, delimiter: str = None):
    sub_road = f"{sub_road}{default_road_delimiter_if_none(delimiter)}"
    return x_road.replace(sub_road, "")


class InvaliddelimiterReplaceException(Exception):
    pass


def is_string_in_road(string: str, road: RoadUnit) -> bool:
    return road.find(string) >= 0


def replace_road_delimiter(road: RoadUnit, old_delimiter: str, new_delimiter: str):
    if is_string_in_road(string=new_delimiter, road=road):
        raise InvaliddelimiterReplaceException(
            f"Cannot replace_road_delimiter '{old_delimiter}' with '{new_delimiter}' because the new one exists in road '{road}'."
        )
    return road.replace(old_delimiter, new_delimiter)


class ValidateRoadNodeException(Exception):
    pass


def is_roadnode(x_roadnode: RoadNode, x_delimiter: str):
    x_roadnode = RoadNode(x_roadnode)
    return x_roadnode.is_node(delimiter=x_delimiter)


def validate_roadnode(
    x_roadnode: RoadNode, x_delimiter: str, not_roadnode_required: bool = False
):
    if is_roadnode(x_roadnode, x_delimiter) and not_roadnode_required:
        raise ValidateRoadNodeException(
            f"'{x_roadnode}' needs to not be a RoadNode. Must contain delimiter: '{x_delimiter}'"
        )
    elif is_roadnode(x_roadnode, x_delimiter) is False and not not_roadnode_required:
        raise ValidateRoadNodeException(
            f"'{x_roadnode}' needs to be a RoadNode. Cannot contain delimiter: '{x_delimiter}'"
        )

    return x_roadnode


def roadunit_valid_dir_path(x_roadunit: RoadUnit, delimiter: str) -> bool:
    x_road_nodes = get_all_road_nodes(x_roadunit, delimiter)
    slash_str = "/"
    x_road_os_path = create_road_from_nodes(x_road_nodes, delimiter=slash_str)
    parts = pathlib_Path(x_road_os_path).parts
    if len(parts) != len(x_road_nodes):
        return False

    return is_path_valid(x_road_os_path)


def get_road_from_doar(x_doarunit: DoarUnit, delimiter: str = None) -> RoadUnit:
    x_delimiter = default_road_delimiter_if_none(delimiter)
    doar_nodes = get_all_road_nodes(x_doarunit, x_delimiter)
    return RoadUnit(create_road_from_nodes(doar_nodes[::-1], x_delimiter))


def get_doar_from_road(x_roadunit: RoadUnit, delimiter: str = None) -> DoarUnit:
    return DoarUnit(get_road_from_doar(x_roadunit, delimiter))
