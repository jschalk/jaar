from src.a00_data_toolbox.file_toolbox import is_path_valid
from pathlib import Path as pathlib_Path


class InvalidWayTermException(Exception):
    pass


class LabelTerm(str):
    """A string representation of a tree node. Nodes cannot contain WayTerm bridge"""

    def is_label(self, bridge: str = None) -> bool:
        return len(self) > 0 and self.contains_bridge(bridge)

    def contains_bridge(self, bridge: str = None) -> bool:
        return self.find(default_bridge_if_None(bridge)) == -1


class FiscLabel(LabelTerm):  # Created to help track the object class relations
    pass


class NameTerm(str):
    """All Name string classes should inherit from this class"""

    def is_name(self, bridge: str = None) -> bool:
        return len(self) > 0 and self.contains_bridge(bridge)

    def contains_bridge(self, bridge: str = None) -> bool:
        return self.find(default_bridge_if_None(bridge)) == -1


class OwnerName(NameTerm):
    """A NameTerm used to identify a BudUnit's owner"""

    pass


class AcctName(OwnerName):  # Created to help track the object class relations
    """Every AcctName object is OwnerName, must follow OwnerName format."""

    pass


class HealerName(OwnerName):
    """A LabelTerm used to identify a Problem's Healer"""

    pass


class WayTerm(str):
    """A string representation of a tree path. LabelTerms are seperated by way bridge"""

    pass


class YawTerm(str):
    """YawTerm is a WayTerm in reverse direction. A string representation of a tree path. LabelTerms are seperated by way bridge."""

    pass


class TitleTerm(str):
    """If a TitleTerm contains bridges it represents a group otherwise it's a single member group of an AcctName."""


class GroupTitle(TitleTerm):  # Created to help track the object class relations
    pass


class WorldID(str):
    pass


class FaceName(NameTerm):
    pass


class EventInt(int):
    pass


class bridge_not_in_parent_way_Exception(Exception):
    pass


def get_default_fisc_label() -> FiscLabel:
    return "ZZ"


def to_way(label: LabelTerm, bridge: str = None):
    x_bridge = default_bridge_if_None(bridge)
    if label is None:
        return x_bridge
    label = label if label.find(x_bridge) == 0 else f"{x_bridge}{label}"
    return label if label.endswith(x_bridge) else f"{label}{x_bridge}"


def get_default_fisc_way(bridge: str = None) -> str:
    return to_way(get_default_fisc_label(), bridge)


def default_bridge_if_None(bridge: any = None) -> str:
    if bridge != bridge:  # float("nan")
        bridge = None
    return bridge if bridge is not None else ";"


class init_bridge_not_presentException(Exception):
    pass


class bridge_in_label_Exception(Exception):
    pass


def create_way(
    parent_way: WayTerm,
    tail_label: LabelTerm = None,
    bridge: str = None,
    auto_add_first_bridge: bool = True,
) -> WayTerm:
    bridge = default_bridge_if_None(bridge)
    if tail_label in {"", None}:
        return to_way(parent_way, bridge)

    if parent_way and parent_way.find(bridge) != 0:
        if auto_add_first_bridge:
            parent_way = to_way(parent_way, bridge)
        else:
            exception_str = (
                f"Parent way must have bridge '{bridge}' at position 0 in string"
            )
            raise init_bridge_not_presentException(exception_str)

    tail_label = LabelTerm(tail_label)
    if tail_label.is_label(bridge) is False:
        raise bridge_in_label_Exception(f"bridge '{bridge}' is in {tail_label}")
    if tail_label is None:
        return WayTerm(parent_way)
    if tail_label.is_label(bridge) is False:
        raise bridge_in_label_Exception(f"bridge '{bridge}' is in {tail_label}")
    if parent_way in {"", None}:
        x_way = to_way(tail_label, bridge)
    elif parent_way.endswith(bridge):
        x_way = f"{parent_way}{tail_label}{bridge}"
    else:
        x_way = f"{parent_way}{bridge}{tail_label}{bridge}"
    return to_way(x_way, bridge)


def rebuild_way(subj_way: WayTerm, old_way: WayTerm, new_way: WayTerm) -> WayTerm:
    if subj_way is None:
        return subj_way
    elif is_sub_way(subj_way, old_way):
        return subj_way.replace(old_way, new_way, 1)
    else:
        return subj_way


def is_sub_way(ref_way: WayTerm, sub_way: WayTerm) -> bool:
    ref_way = "" if ref_way is None else ref_way
    return ref_way.find(sub_way) == 0


def is_heir_way(src: WayTerm, heir: WayTerm, bridge: str = None) -> bool:
    # return src == heir or heir.startswith(src + default_bridge_if_None(bridge))
    return src == heir or heir.find(src) == 0


def find_replace_way_key_dict(dict_x: dict, old_way: WayTerm, new_way: WayTerm) -> dict:
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


def get_all_way_labels(way: WayTerm, bridge: str = None) -> list[LabelTerm]:
    return way.split(default_bridge_if_None(bridge))[1:-1]


def get_tail_label(way: WayTerm, bridge: str = None) -> LabelTerm:
    bridge = default_bridge_if_None(bridge)
    if way in ["", bridge]:
        return ""
    all_way_labels = get_all_way_labels(way=way, bridge=bridge)
    return all_way_labels[0] if len(all_way_labels) == 1 else all_way_labels[-1]


def get_parent_way(
    way: WayTerm, bridge: str = None
) -> WayTerm:  # way without tail label
    parent_labels = get_all_way_labels(way=way, bridge=bridge)[:-1]
    return create_way_from_labels(parent_labels, bridge=bridge)


def get_root_label_from_way(way: WayTerm, bridge: str = None) -> LabelTerm:
    return get_all_way_labels(way=way, bridge=bridge)[0]


def get_ancestor_ways(way: WayTerm, bridge: str = None) -> list[WayTerm]:
    bridge = default_bridge_if_None(bridge)
    if not way:
        return []
    labels = get_all_way_labels(way, bridge)
    temp_way = to_way(labels.pop(0), bridge)

    temp_ways = [temp_way]
    if labels != []:
        while labels != []:
            temp_way = create_way(temp_way, labels.pop(0), bridge)
            temp_ways.append(temp_way)

    x_ways = []
    while temp_ways != []:
        x_ways.append(temp_ways.pop(len(temp_ways) - 1))
    return x_ways


def all_wayterms_between(src_way, dst_way) -> list[WayTerm]:
    x_list = []
    anc_ways = get_ancestor_ways(dst_way)
    while anc_ways != []:
        anc_way = anc_ways.pop()
        if is_sub_way(anc_way, src_way):
            x_list.append(anc_way)
    return x_list


class ForeFatherException(Exception):
    pass


def get_forefather_ways(way: WayTerm) -> dict[WayTerm]:
    ancestor_ways = get_ancestor_ways(way=way)
    popped_way = ancestor_ways.pop(0)
    if popped_way != way:
        raise ForeFatherException(
            f"Incorrect way {popped_way} from out of ancestor_ways."
        )
    return {a_way: None for a_way in ancestor_ways}


def create_way_from_labels(labels: list[LabelTerm], bridge: str = None) -> WayTerm:
    if not labels:
        return ""
    return to_way(default_bridge_if_None(bridge).join(labels), bridge)


class InvalidbridgeReplaceException(Exception):
    pass


def is_string_in_way(string: str, way: WayTerm) -> bool:
    return way.find(string) >= 0


def replace_bridge(way: WayTerm, old_bridge: str, new_bridge: str):
    if is_string_in_way(string=new_bridge, way=way):
        raise InvalidbridgeReplaceException(
            f"Cannot replace_bridge '{old_bridge}' with '{new_bridge}' because the new one exists in way '{way}'."
        )
    return way.replace(old_bridge, new_bridge)


class ValidateLabelTermException(Exception):
    pass


def is_labelterm(x_labelterm: LabelTerm, x_bridge: str):
    x_labelterm = LabelTerm(x_labelterm)
    return x_labelterm.is_label(bridge=x_bridge)


def validate_labelterm(
    x_labelterm: LabelTerm, x_bridge: str, not_labelterm_required: bool = False
):
    if is_labelterm(x_labelterm, x_bridge) and not_labelterm_required:
        raise ValidateLabelTermException(
            f"'{x_labelterm}' needs to not be a LabelTerm. Must contain bridge: '{x_bridge}'"
        )
    elif is_labelterm(x_labelterm, x_bridge) is False and not not_labelterm_required:
        raise ValidateLabelTermException(
            f"'{x_labelterm}' needs to be a LabelTerm. Cannot contain bridge: '{x_bridge}'"
        )

    return x_labelterm


def wayterm_valid_dir_path(x_wayterm: WayTerm, bridge: str) -> bool:
    x_way_labels = get_all_way_labels(x_wayterm, bridge)
    slash_str = "/"
    x_way_os_path = create_way_from_labels(x_way_labels, bridge=slash_str)
    parts = pathlib_Path(x_way_os_path).parts
    parts = parts[1:]
    return False if len(parts) != len(x_way_labels) else is_path_valid(x_way_os_path)


def get_way_from_yaw(x_yawterm: YawTerm, bridge: str = None) -> WayTerm:
    x_bridge = default_bridge_if_None(bridge)
    yaw_labels = get_all_way_labels(x_yawterm, x_bridge)
    return WayTerm(create_way_from_labels(yaw_labels[::-1], x_bridge))


def get_yaw_from_way(x_wayterm: WayTerm, bridge: str = None) -> YawTerm:
    return YawTerm(get_way_from_yaw(x_wayterm, bridge))
