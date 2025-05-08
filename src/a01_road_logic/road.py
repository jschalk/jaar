from src.a00_data_toolbox.file_toolbox import is_path_valid
from pathlib import Path as pathlib_Path


class InvalidRoadUnitException(Exception):
    pass


class TagUnit(str):
    """A string representation of a tree node. Nodes cannot contain RoadUnit bridge"""

    def is_tag(self, bridge: str = None) -> bool:
        return len(self) > 0 and self.contains_bridge(bridge)

    def contains_bridge(self, bridge: str = None) -> bool:
        return self.find(default_bridge_if_None(bridge)) == -1


class FiscTag(TagUnit):  # Created to help track the concept
    pass


class NameUnit(str):
    """All Name string classes should inherit from this class"""

    def is_name(self, bridge: str = None) -> bool:
        return len(self) > 0 and self.contains_bridge(bridge)

    def contains_bridge(self, bridge: str = None) -> bool:
        return self.find(default_bridge_if_None(bridge)) == -1


class OwnerName(NameUnit):
    """A TagUnit used to identify a BudUnit's owner_name"""

    pass


class AcctName(OwnerName):  # Created to help track the concept
    """Every AcctName object is OwnerName, must follow OwnerName format."""

    pass


class HealerName(OwnerName):
    """A TagUnit used to identify a Problem's Healer"""

    pass


class TimeLineTag(TagUnit):
    "TimeLineTag is required for every TimeLineUnit. It is a TagUnit that must not container the bridge."

    pass


class RoadUnit(str):
    """A string representation of a tree path. TagUnits are seperated by road bridge"""

    pass


class DoarUnit(str):
    """DoarUnit is a RoadUnit in reverse direction. A string representation of a tree path. TagUnits are seperated by road bridge."""

    pass


class LabelUnit(str):
    """Any Label and _title string classes should inherit from this class"""


class GroupLabel(LabelUnit):  # Created to help track the concept
    pass


class WorldID(str):
    pass


class FaceName(NameUnit):
    pass


def get_default_face_name() -> FaceName:
    return FaceName("Face1234")


class EventInt(int):
    pass


def default_bridge_if_None(bridge: any = None) -> str:
    if bridge != bridge:  # float("nan")
        bridge = None
    return bridge if bridge is not None else ";"


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


def is_heir_road(src: RoadUnit, heir: RoadUnit, bridge: str = None) -> bool:
    return src == heir or heir.find(f"{src}{default_bridge_if_None(bridge)}") == 0


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


def get_all_road_tags(road: RoadUnit, bridge: str = None) -> list[TagUnit]:
    return road.split(default_bridge_if_None(bridge))


def get_terminus_tag(road: RoadUnit, bridge: str = None) -> TagUnit:
    return get_all_road_tags(road=road, bridge=bridge)[-1]


def get_parent_road(
    road: RoadUnit, bridge: str = None
) -> RoadUnit:  # road without terminus tag
    parent_tags = get_all_road_tags(road=road, bridge=bridge)[:-1]
    return create_road_from_tags(parent_tags, bridge=bridge)


def create_road_without_root_tag(
    road: RoadUnit, bridge: str = None
) -> RoadUnit:  # road without terminus tagf
    if road[:1] == default_bridge_if_None(bridge):
        raise InvalidRoadUnitException(
            f"Cannot create_road_without_root_tag of '{road}' because it has no root tag."
        )
    road_without_root_tag = create_road_from_tags(get_all_road_tags(road=road)[1:])
    return f"{default_bridge_if_None(bridge)}{road_without_root_tag}"


def get_root_tag_from_road(road: RoadUnit, bridge: str = None) -> TagUnit:
    return get_all_road_tags(road=road, bridge=bridge)[0]


def road_validate(road: RoadUnit, bridge: str, root_tag: TagUnit) -> RoadUnit:
    if road == "" or road is None:
        return RoadUnit("")
    x_root = get_root_tag_from_road(road, bridge)
    return (
        rebuild_road(
            subj_road=road,
            old_road=x_root,
            new_road=root_tag,
        )
        if x_root != root_tag
        else road
    )


def get_ancestor_roads(road: RoadUnit) -> list[RoadUnit]:
    if road is None:
        return []
    tags = get_all_road_tags(road)
    temp_road = tags.pop(0)

    temp_roads = [temp_road]
    if tags != []:
        while tags != []:
            temp_road = create_road(temp_road, tags.pop(0))
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


def get_default_fisc_tag() -> FiscTag:
    return "ZZ"


def create_road_from_tags(tags: list[TagUnit], bridge: str = None) -> RoadUnit:
    return default_bridge_if_None(bridge).join(tags)


class bridge_in_tag_Exception(Exception):
    pass


def create_road(
    parent_road: RoadUnit, terminus_tag: TagUnit = None, bridge: str = None
) -> RoadUnit:

    if terminus_tag is None:
        return RoadUnit(parent_road)
    x_bridge = default_bridge_if_None(bridge)
    terminus_tag = TagUnit(terminus_tag)
    if terminus_tag.is_tag(x_bridge) is False:
        raise bridge_in_tag_Exception(f"bridge '{x_bridge}' is in {terminus_tag}")

    return RoadUnit(
        terminus_tag
        if parent_road in {"", None}
        else f"{parent_road}{x_bridge}{terminus_tag}"
    )


def combine_roads(
    parent_road: RoadUnit, ancestor_road: RoadUnit, bridge: str = None
) -> RoadUnit:
    if parent_road in {""}:
        return ancestor_road
    parent_road_tags = get_all_road_tags(parent_road, bridge)
    ancestor_road_tags = get_all_road_tags(ancestor_road, bridge)
    parent_road_tags.extend(ancestor_road_tags)
    return create_road_from_tags(parent_road_tags, bridge)


def get_diff_road(x_road: RoadUnit, sub_road: RoadUnit, bridge: str = None):
    sub_road = f"{sub_road}{default_bridge_if_None(bridge)}"
    return x_road.replace(sub_road, "")


class InvalidbridgeReplaceException(Exception):
    pass


def is_string_in_road(string: str, road: RoadUnit) -> bool:
    return road.find(string) >= 0


def replace_bridge(road: RoadUnit, old_bridge: str, new_bridge: str):
    if is_string_in_road(string=new_bridge, road=road):
        raise InvalidbridgeReplaceException(
            f"Cannot replace_bridge '{old_bridge}' with '{new_bridge}' because the new one exists in road '{road}'."
        )
    return road.replace(old_bridge, new_bridge)


class ValidateTagUnitException(Exception):
    pass


def is_tagunit(x_tagunit: TagUnit, x_bridge: str):
    x_tagunit = TagUnit(x_tagunit)
    return x_tagunit.is_tag(bridge=x_bridge)


def validate_tagunit(
    x_tagunit: TagUnit, x_bridge: str, not_tagunit_required: bool = False
):
    if is_tagunit(x_tagunit, x_bridge) and not_tagunit_required:
        raise ValidateTagUnitException(
            f"'{x_tagunit}' needs to not be a TagUnit. Must contain bridge: '{x_bridge}'"
        )
    elif is_tagunit(x_tagunit, x_bridge) is False and not not_tagunit_required:
        raise ValidateTagUnitException(
            f"'{x_tagunit}' needs to be a TagUnit. Cannot contain bridge: '{x_bridge}'"
        )

    return x_tagunit


def roadunit_valid_dir_path(x_roadunit: RoadUnit, bridge: str) -> bool:
    x_road_tags = get_all_road_tags(x_roadunit, bridge)
    slash_str = "/"
    x_road_os_path = create_road_from_tags(x_road_tags, bridge=slash_str)
    parts = pathlib_Path(x_road_os_path).parts
    if len(parts) != len(x_road_tags):
        return False

    return is_path_valid(x_road_os_path)


def get_road_from_doar(x_doarunit: DoarUnit, bridge: str = None) -> RoadUnit:
    x_bridge = default_bridge_if_None(bridge)
    doar_tags = get_all_road_tags(x_doarunit, x_bridge)
    return RoadUnit(create_road_from_tags(doar_tags[::-1], x_bridge))


def get_doar_from_road(x_roadunit: RoadUnit, bridge: str = None) -> DoarUnit:
    return DoarUnit(get_road_from_doar(x_roadunit, bridge))
