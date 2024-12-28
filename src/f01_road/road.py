from src.f00_instrument.file import is_path_valid
from pathlib import Path as pathlib_Path


class InvalidRoadUnitException(Exception):
    pass


class IdeaUnit(str):
    """A string presentation of a tree node. Nodes cannot contain RoadUnit bridge"""

    def is_idea(self, bridge: str = None) -> bool:
        return len(self) > 0 and self.is_bridge_in_str(bridge)

    def is_bridge_in_str(self, bridge: str = None) -> bool:
        return self.find(default_bridge_if_None(bridge)) == -1


class DealID(IdeaUnit):  # Created to help track the concept
    pass


class OwnerName(IdeaUnit):  # Created to help track the concept
    """Must be idea thus not include road bridge"""

    pass


class HealerName(OwnerName):
    """A IdeaUnit used to identify a Problem's Healer"""

    pass


class OwnerName(HealerName):
    """A IdeaUnit used to identify a BudUnit's owner_name"""

    pass


class AcctName(OwnerName):  # Created to help track the concept
    """Every AcctName object is OwnerName, must follow OwnerName format."""

    pass


class TimeLineIdea(IdeaUnit):
    "TimeLineIdea is required for every TimeLineUnit. It is a IdeaUnit that must not container the bridge."

    pass


class RoadUnit(str):
    """A string presentation of a tree path. IdeaUnits are seperated by road bridge"""

    pass


class DoarUnit(str):
    """DoarUnit is a RoadUnit in reverse direction. A string presentation of a tree path. IdeaUnits are seperated by road bridge."""

    pass


class GroupID(str):  # Created to help track the concept
    pass


class WorldID(str):
    pass


def get_default_world_id() -> WorldID:
    return WorldID("TestingWorld3")


class FaceName(str):
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


def get_all_road_ideas(road: RoadUnit, bridge: str = None) -> list[IdeaUnit]:
    return road.split(default_bridge_if_None(bridge))


def get_terminus_idea(road: RoadUnit, bridge: str = None) -> IdeaUnit:
    return get_all_road_ideas(road=road, bridge=bridge)[-1]


def get_parent_road(
    road: RoadUnit, bridge: str = None
) -> RoadUnit:  # road without terminus idea
    parent_ideas = get_all_road_ideas(road=road, bridge=bridge)[:-1]
    return create_road_from_ideas(parent_ideas, bridge=bridge)


def create_road_without_root_idea(
    road: RoadUnit, bridge: str = None
) -> RoadUnit:  # road without terminus ideaf
    if road[:1] == default_bridge_if_None(bridge):
        raise InvalidRoadUnitException(
            f"Cannot create_road_without_root_idea of '{road}' because it has no root idea."
        )
    road_without_root_idea = create_road_from_ideas(get_all_road_ideas(road=road)[1:])
    return f"{default_bridge_if_None(bridge)}{road_without_root_idea}"


def get_root_idea_from_road(road: RoadUnit, bridge: str = None) -> IdeaUnit:
    return get_all_road_ideas(road=road, bridge=bridge)[0]


def road_validate(road: RoadUnit, bridge: str, root_idea: IdeaUnit) -> RoadUnit:
    if road == "" or road is None:
        return RoadUnit("")
    x_root = get_root_idea_from_road(road, bridge)
    return (
        rebuild_road(
            subj_road=road,
            old_road=x_root,
            new_road=root_idea,
        )
        if x_root != root_idea
        else road
    )


def get_ancestor_roads(road: RoadUnit) -> list[RoadUnit]:
    if road is None:
        return []
    ideas = get_all_road_ideas(road)
    temp_road = ideas.pop(0)

    temp_roads = [temp_road]
    if ideas != []:
        while ideas != []:
            temp_road = create_road(temp_road, ideas.pop(0))
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


def get_default_deal_id_ideaunit() -> DealID:
    return "ZZ"


def create_road_from_ideas(ideas: list[IdeaUnit], bridge: str = None) -> RoadUnit:
    return default_bridge_if_None(bridge).join(ideas)


class bridge_in_idea_Exception(Exception):
    pass


def create_road(
    parent_road: RoadUnit, terminus_idea: IdeaUnit = None, bridge: str = None
) -> RoadUnit:

    if terminus_idea is None:
        return RoadUnit(parent_road)
    x_bridge = default_bridge_if_None(bridge)
    terminus_idea = IdeaUnit(terminus_idea)
    if terminus_idea.is_idea(x_bridge) is False:
        raise bridge_in_idea_Exception(f"bridge '{x_bridge}' is in {terminus_idea}")

    return RoadUnit(
        terminus_idea
        if parent_road in {"", None}
        else f"{parent_road}{x_bridge}{terminus_idea}"
    )


def combine_roads(
    parent_road: RoadUnit, ancestor_road: RoadUnit, bridge: str = None
) -> RoadUnit:
    if parent_road in {""}:
        return ancestor_road
    parent_road_ideas = get_all_road_ideas(parent_road, bridge)
    ancestor_road_ideas = get_all_road_ideas(ancestor_road, bridge)
    parent_road_ideas.extend(ancestor_road_ideas)
    return create_road_from_ideas(parent_road_ideas, bridge)


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


class ValidateIdeaUnitException(Exception):
    pass


def is_ideaunit(x_ideaunit: IdeaUnit, x_bridge: str):
    x_ideaunit = IdeaUnit(x_ideaunit)
    return x_ideaunit.is_idea(bridge=x_bridge)


def validate_ideaunit(
    x_ideaunit: IdeaUnit, x_bridge: str, not_ideaunit_required: bool = False
):
    if is_ideaunit(x_ideaunit, x_bridge) and not_ideaunit_required:
        raise ValidateIdeaUnitException(
            f"'{x_ideaunit}' needs to not be a IdeaUnit. Must contain bridge: '{x_bridge}'"
        )
    elif is_ideaunit(x_ideaunit, x_bridge) is False and not not_ideaunit_required:
        raise ValidateIdeaUnitException(
            f"'{x_ideaunit}' needs to be a IdeaUnit. Cannot contain bridge: '{x_bridge}'"
        )

    return x_ideaunit


def roadunit_valid_dir_path(x_roadunit: RoadUnit, bridge: str) -> bool:
    x_road_ideas = get_all_road_ideas(x_roadunit, bridge)
    slash_str = "/"
    x_road_os_path = create_road_from_ideas(x_road_ideas, bridge=slash_str)
    parts = pathlib_Path(x_road_os_path).parts
    if len(parts) != len(x_road_ideas):
        return False

    return is_path_valid(x_road_os_path)


def get_road_from_doar(x_doarunit: DoarUnit, bridge: str = None) -> RoadUnit:
    x_bridge = default_bridge_if_None(bridge)
    doar_ideas = get_all_road_ideas(x_doarunit, x_bridge)
    return RoadUnit(create_road_from_ideas(doar_ideas[::-1], x_bridge))


def get_doar_from_road(x_roadunit: RoadUnit, bridge: str = None) -> DoarUnit:
    return DoarUnit(get_road_from_doar(x_roadunit, bridge))
