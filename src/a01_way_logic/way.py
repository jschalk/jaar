from src.a00_data_toolbox.file_toolbox import is_path_valid
from pathlib import Path as pathlib_Path


class InvalidWayUnitException(Exception):
    pass


class TagUnit(str):
    """A string representation of a tree node. Nodes cannot contain WayUnit bridge"""

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


class WayUnit(str):
    """A string representation of a tree path. TagUnits are seperated by way bridge"""

    pass


class YawUnit(str):
    """YawUnit is a WayUnit in reverse direction. A string representation of a tree path. TagUnits are seperated by way bridge."""

    pass


class LabelUnit(str):
    """If a LabelUnit contains bridges it represents a group otherwise it's a single member group of an AcctName."""


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


class bridge_not_in_parent_way_Exception(Exception):
    pass


def get_default_fisc_tag() -> FiscTag:
    return "ZZ"


def to_way(tag: TagUnit, bridge: str = None):
    x_bridge = default_bridge_if_None(bridge)
    if tag is None:
        return x_bridge
    return tag if tag.find(x_bridge) == 0 else f"{x_bridge}{tag}"


def get_default_fisc_way(bridge: str = None) -> str:
    return to_way(get_default_fisc_tag(), bridge)


def default_bridge_if_None(bridge: any = None) -> str:
    if bridge != bridge:  # float("nan")
        bridge = None
    return bridge if bridge is not None else ";"


class init_bridge_not_presentException(Exception):
    pass


class bridge_in_tag_Exception(Exception):
    pass


def create_way(
    parent_way: WayUnit,
    terminus_tag: TagUnit = None,
    bridge: str = None,
    auto_add_first_bridge: bool = True,
) -> WayUnit:
    bridge = default_bridge_if_None(bridge)
    if terminus_tag in {"", None}:
        return to_way(parent_way, bridge)

    if parent_way and parent_way.find(bridge) != 0:
        if auto_add_first_bridge:
            parent_way = to_way(parent_way, bridge)
        else:
            exception_str = (
                f"Parent way must have bridge '{bridge}' at position 0 in string"
            )
            raise init_bridge_not_presentException(exception_str)

    terminus_tag = TagUnit(terminus_tag)
    if terminus_tag.is_tag(bridge) is False:
        raise bridge_in_tag_Exception(f"bridge '{bridge}' is in {terminus_tag}")
    if terminus_tag is None:
        return WayUnit(parent_way)
    if terminus_tag.is_tag(bridge) is False:
        raise bridge_in_tag_Exception(f"bridge '{bridge}' is in {terminus_tag}")

    if parent_way in {"", None}:
        x_way = terminus_tag
    else:
        x_way = f"{parent_way}{bridge}{terminus_tag}"
    return to_way(x_way, bridge)


def rebuild_way(subj_way: WayUnit, old_way: WayUnit, new_way: WayUnit) -> WayUnit:
    if subj_way is None:
        return subj_way
    elif is_sub_way(subj_way, old_way):
        return subj_way.replace(old_way, new_way, 1)
    else:
        return subj_way


def is_sub_way(ref_way: WayUnit, sub_way: WayUnit) -> bool:
    ref_way = "" if ref_way is None else ref_way
    return ref_way.find(sub_way) == 0


def is_heir_way(src: WayUnit, heir: WayUnit, bridge: str = None) -> bool:
    return src == heir or heir.find(f"{src}{default_bridge_if_None(bridge)}") == 0


def find_replace_way_key_dict(dict_x: dict, old_way: WayUnit, new_way: WayUnit) -> dict:
    keys_to_delete = []
    objs_to_add = []
    for x_key, x_obj in dict_x.items():
        if old_way != new_way and is_sub_way(ref_way=x_key, sub_way=old_way):
            x_obj.find_replace_way(old_way=old_way, new_way=new_way)
            objs_to_add.append(x_obj)
            keys_to_delete.append(x_key)

    for x_obj in objs_to_add:
        dict_x[x_obj.get_obj_key()] = x_obj

    for x_key in keys_to_delete:
        dict_x.pop(x_key)

    return dict_x


def get_all_way_tags(way: WayUnit, bridge: str = None) -> list[TagUnit]:
    return way.split(default_bridge_if_None(bridge))[1:]


def get_terminus_tag(way: WayUnit, bridge: str = None) -> TagUnit:
    return get_all_way_tags(way=way, bridge=bridge)[-1]


def get_parent_way(
    way: WayUnit, bridge: str = None
) -> WayUnit:  # way without terminus tag
    parent_tags = get_all_way_tags(way=way, bridge=bridge)[:-1]
    return create_way_from_tags(parent_tags, bridge=bridge)


def get_root_tag_from_way(way: WayUnit, bridge: str = None) -> TagUnit:
    return get_all_way_tags(way=way, bridge=bridge)[0]


def get_ancestor_ways(way: WayUnit, bridge: str = None) -> list[WayUnit]:
    bridge = default_bridge_if_None(bridge)
    if not way:
        return []
    tags = get_all_way_tags(way, bridge)
    temp_way = to_way(tags.pop(0), bridge)

    temp_ways = [temp_way]
    if tags != []:
        while tags != []:
            temp_way = create_way(temp_way, tags.pop(0), bridge)
            temp_ways.append(temp_way)

    x_ways = []
    while temp_ways != []:
        x_ways.append(temp_ways.pop(len(temp_ways) - 1))
    return x_ways


def all_wayunits_between(src_way, dst_way) -> list[WayUnit]:
    x_list = []
    anc_ways = get_ancestor_ways(dst_way)
    while anc_ways != []:
        anc_way = anc_ways.pop()
        if is_sub_way(anc_way, src_way):
            x_list.append(anc_way)
    return x_list


class ForeFatherException(Exception):
    pass


def get_forefather_ways(way: WayUnit) -> dict[WayUnit]:
    ancestor_ways = get_ancestor_ways(way=way)
    popped_way = ancestor_ways.pop(0)
    if popped_way != way:
        raise ForeFatherException(
            f"Incorrect way {popped_way} from out of ancestor_ways."
        )
    return {a_way: None for a_way in ancestor_ways}


def get_default_fisc_tag() -> FiscTag:
    return "ZZ"


def create_way_from_tags(tags: list[TagUnit], bridge: str = None) -> WayUnit:
    if not tags:
        return ""
    return to_way(default_bridge_if_None(bridge).join(tags), bridge)


class InvalidbridgeReplaceException(Exception):
    pass


def is_string_in_way(string: str, way: WayUnit) -> bool:
    return way.find(string) >= 0


def replace_bridge(way: WayUnit, old_bridge: str, new_bridge: str):
    if is_string_in_way(string=new_bridge, way=way):
        raise InvalidbridgeReplaceException(
            f"Cannot replace_bridge '{old_bridge}' with '{new_bridge}' because the new one exists in way '{way}'."
        )
    return way.replace(old_bridge, new_bridge)


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


def wayunit_valid_dir_path(x_wayunit: WayUnit, bridge: str) -> bool:
    x_way_tags = get_all_way_tags(x_wayunit, bridge)
    slash_str = "/"
    x_way_os_path = create_way_from_tags(x_way_tags, bridge=slash_str)
    parts = pathlib_Path(x_way_os_path).parts
    parts = parts[1:]
    return False if len(parts) != len(x_way_tags) else is_path_valid(x_way_os_path)


def get_way_from_yaw(x_yawunit: YawUnit, bridge: str = None) -> WayUnit:
    x_bridge = default_bridge_if_None(bridge)
    yaw_tags = get_all_way_tags(x_yawunit, x_bridge)
    return WayUnit(create_way_from_tags(yaw_tags[::-1], x_bridge))


def get_yaw_from_way(x_wayunit: WayUnit, bridge: str = None) -> YawUnit:
    return YawUnit(get_way_from_yaw(x_wayunit, bridge))
