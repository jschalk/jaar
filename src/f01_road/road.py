from src.f00_instrument.file_toolbox import is_path_valid
from pathlib import Path as pathlib_Path


class InvalidRoadUnitException(Exception):
    pass


class TitleUnit(str):
    """A string representation of a tree node. Nodes cannot contain RoadUnit bridge"""

    def is_title(self, bridge: str = None) -> bool:
        return len(self) > 0 and self.contains_bridge(bridge)

    def contains_bridge(self, bridge: str = None) -> bool:
        return self.find(default_bridge_if_None(bridge)) == -1


class FiscTitle(TitleUnit):  # Created to help track the concept
    pass


class NameUnit(str):
    """All Name string classes should inherit from this class"""

    def is_name(self, bridge: str = None) -> bool:
        return len(self) > 0 and self.contains_bridge(bridge)

    def contains_bridge(self, bridge: str = None) -> bool:
        return self.find(default_bridge_if_None(bridge)) == -1


class OwnerName(NameUnit):
    """A TitleUnit used to identify a BudUnit's owner_name"""

    pass


class AcctName(OwnerName):  # Created to help track the concept
    """Every AcctName object is OwnerName, must follow OwnerName format."""

    pass


class HealerName(OwnerName):
    """A TitleUnit used to identify a Problem's Healer"""

    pass


class TimeLineTitle(TitleUnit):
    "TimeLineTitle is required for every TimeLineUnit. It is a TitleUnit that must not container the bridge."

    pass


class RoadUnit(str):
    """A string representation of a tree path. TitleUnits are seperated by road bridge"""

    pass


class DoarUnit(str):
    """DoarUnit is a RoadUnit in reverse direction. A string representation of a tree path. TitleUnits are seperated by road bridge."""

    pass


class LabelUnit(str):
    """Any Label and Tag string classes should inherit from this class"""


class GroupLabel(LabelUnit):  # Created to help track the concept
    pass


class WorldID(str):
    pass


def get_default_world_id() -> WorldID:
    return WorldID("TestingWorld3")


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


def get_all_road_titles(road: RoadUnit, bridge: str = None) -> list[TitleUnit]:
    return road.split(default_bridge_if_None(bridge))


def get_terminus_title(road: RoadUnit, bridge: str = None) -> TitleUnit:
    return get_all_road_titles(road=road, bridge=bridge)[-1]


def get_parent_road(
    road: RoadUnit, bridge: str = None
) -> RoadUnit:  # road without terminus title
    parent_titles = get_all_road_titles(road=road, bridge=bridge)[:-1]
    return create_road_from_titles(parent_titles, bridge=bridge)


def create_road_without_root_title(
    road: RoadUnit, bridge: str = None
) -> RoadUnit:  # road without terminus titlef
    if road[:1] == default_bridge_if_None(bridge):
        raise InvalidRoadUnitException(
            f"Cannot create_road_without_root_title of '{road}' because it has no root title."
        )
    road_without_root_title = create_road_from_titles(
        get_all_road_titles(road=road)[1:]
    )
    return f"{default_bridge_if_None(bridge)}{road_without_root_title}"


def get_root_title_from_road(road: RoadUnit, bridge: str = None) -> TitleUnit:
    return get_all_road_titles(road=road, bridge=bridge)[0]


def road_validate(road: RoadUnit, bridge: str, root_title: TitleUnit) -> RoadUnit:
    if road == "" or road is None:
        return RoadUnit("")
    x_root = get_root_title_from_road(road, bridge)
    return (
        rebuild_road(
            subj_road=road,
            old_road=x_root,
            new_road=root_title,
        )
        if x_root != root_title
        else road
    )


def get_ancestor_roads(road: RoadUnit) -> list[RoadUnit]:
    if road is None:
        return []
    titles = get_all_road_titles(road)
    temp_road = titles.pop(0)

    temp_roads = [temp_road]
    if titles != []:
        while titles != []:
            temp_road = create_road(temp_road, titles.pop(0))
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


def get_default_fisc_title() -> FiscTitle:
    return "ZZ"


def create_road_from_titles(titles: list[TitleUnit], bridge: str = None) -> RoadUnit:
    return default_bridge_if_None(bridge).join(titles)


class bridge_in_title_Exception(Exception):
    pass


def create_road(
    parent_road: RoadUnit, terminus_title: TitleUnit = None, bridge: str = None
) -> RoadUnit:

    if terminus_title is None:
        return RoadUnit(parent_road)
    x_bridge = default_bridge_if_None(bridge)
    terminus_title = TitleUnit(terminus_title)
    if terminus_title.is_title(x_bridge) is False:
        raise bridge_in_title_Exception(f"bridge '{x_bridge}' is in {terminus_title}")

    return RoadUnit(
        terminus_title
        if parent_road in {"", None}
        else f"{parent_road}{x_bridge}{terminus_title}"
    )


def combine_roads(
    parent_road: RoadUnit, ancestor_road: RoadUnit, bridge: str = None
) -> RoadUnit:
    if parent_road in {""}:
        return ancestor_road
    parent_road_titles = get_all_road_titles(parent_road, bridge)
    ancestor_road_titles = get_all_road_titles(ancestor_road, bridge)
    parent_road_titles.extend(ancestor_road_titles)
    return create_road_from_titles(parent_road_titles, bridge)


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


class ValidateTitleUnitException(Exception):
    pass


def is_titleunit(x_titleunit: TitleUnit, x_bridge: str):
    x_titleunit = TitleUnit(x_titleunit)
    return x_titleunit.is_title(bridge=x_bridge)


def validate_titleunit(
    x_titleunit: TitleUnit, x_bridge: str, not_titleunit_required: bool = False
):
    if is_titleunit(x_titleunit, x_bridge) and not_titleunit_required:
        raise ValidateTitleUnitException(
            f"'{x_titleunit}' needs to not be a TitleUnit. Must contain bridge: '{x_bridge}'"
        )
    elif is_titleunit(x_titleunit, x_bridge) is False and not not_titleunit_required:
        raise ValidateTitleUnitException(
            f"'{x_titleunit}' needs to be a TitleUnit. Cannot contain bridge: '{x_bridge}'"
        )

    return x_titleunit


def roadunit_valid_dir_path(x_roadunit: RoadUnit, bridge: str) -> bool:
    x_road_titles = get_all_road_titles(x_roadunit, bridge)
    slash_str = "/"
    x_road_os_path = create_road_from_titles(x_road_titles, bridge=slash_str)
    parts = pathlib_Path(x_road_os_path).parts
    if len(parts) != len(x_road_titles):
        return False

    return is_path_valid(x_road_os_path)


def get_road_from_doar(x_doarunit: DoarUnit, bridge: str = None) -> RoadUnit:
    x_bridge = default_bridge_if_None(bridge)
    doar_titles = get_all_road_titles(x_doarunit, x_bridge)
    return RoadUnit(create_road_from_titles(doar_titles[::-1], x_bridge))


def get_doar_from_road(x_roadunit: RoadUnit, bridge: str = None) -> DoarUnit:
    return DoarUnit(get_road_from_doar(x_roadunit, bridge))
