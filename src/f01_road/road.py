from src.f00_instrument.file import is_path_valid
from pathlib import Path as pathlib_Path


class InvalidRoadUnitException(Exception):
    pass


class IdeaUnit(str):
    """A string presentation of a tree node. Nodes cannot contain RoadUnit wall"""

    def is_idea(self, wall: str = None) -> bool:
        return self.find(default_wall_if_none(wall)) == -1


class FiscalID(IdeaUnit):  # Created to help track the concept
    pass


class OwnerID(IdeaUnit):  # Created to help track the concept
    """Must be idea thus not include road wall"""

    pass


class HealerID(OwnerID):
    """A IdeaUnit used to identify a Problem's Healer"""

    pass


class OwnerID(HealerID):
    """A IdeaUnit used to identify a BudUnit's owner_id"""

    pass


class AcctID(OwnerID):  # Created to help track the concept
    """Every AcctID object is OwnerID, must follow OwnerID format."""

    pass


class TimeLineLabel(IdeaUnit):
    "TimeLineLabel is required for every TimeLineUnit. It is a IdeaUnit that must not container the wall."

    pass


class RoadUnit(str):
    """A string presentation of a tree path. IdeaUnits are seperated by road wall"""

    pass


class DoarUnit(str):
    """DoarUnit is a RoadUnit in reverse direction. A string presentation of a tree path. IdeaUnits are seperated by road wall."""

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


def default_wall_if_none(wall: str = None) -> str:
    return wall if wall is not None else ";"


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


def is_heir_road(src: RoadUnit, heir: RoadUnit, wall: str = None) -> bool:
    return src == heir or heir.find(f"{src}{default_wall_if_none(wall)}") == 0


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


def get_all_road_ideas(road: RoadUnit, wall: str = None) -> list[IdeaUnit]:
    return road.split(default_wall_if_none(wall))


def get_terminus_idea(road: RoadUnit, wall: str = None) -> IdeaUnit:
    return get_all_road_ideas(road=road, wall=wall)[-1]


def get_parent_road(
    road: RoadUnit, wall: str = None
) -> RoadUnit:  # road without terminus idea
    parent_ideas = get_all_road_ideas(road=road, wall=wall)[:-1]
    return create_road_from_ideas(parent_ideas, wall=wall)


def create_road_without_root_idea(
    road: RoadUnit, wall: str = None
) -> RoadUnit:  # road without terminus ideaf
    if road[:1] == default_wall_if_none(wall):
        raise InvalidRoadUnitException(
            f"Cannot create_road_without_root_idea of '{road}' because it has no root idea."
        )
    road_without_root_idea = create_road_from_ideas(get_all_road_ideas(road=road)[1:])
    return f"{default_wall_if_none(wall)}{road_without_root_idea}"


def get_root_idea_from_road(road: RoadUnit, wall: str = None) -> IdeaUnit:
    return get_all_road_ideas(road=road, wall=wall)[0]


def road_validate(road: RoadUnit, wall: str, root_idea: IdeaUnit) -> RoadUnit:
    if road == "" or road is None:
        return RoadUnit("")
    x_root = get_root_idea_from_road(road, wall)
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


def get_default_fiscal_id_ideaunit() -> FiscalID:
    return "ZZ"


def create_road_from_ideas(ideas: list[IdeaUnit], wall: str = None) -> RoadUnit:
    return default_wall_if_none(wall).join(ideas)


def create_road(
    parent_road: RoadUnit, terminus_idea: IdeaUnit = None, wall: str = None
) -> RoadUnit:
    if terminus_idea is None:
        return RoadUnit(parent_road)
    else:
        return RoadUnit(
            terminus_idea
            if parent_road in {"", None}
            else f"{parent_road}{default_wall_if_none(wall)}{terminus_idea}"
        )


def get_diff_road(x_road: RoadUnit, sub_road: RoadUnit, wall: str = None):
    sub_road = f"{sub_road}{default_wall_if_none(wall)}"
    return x_road.replace(sub_road, "")


class InvalidwallReplaceException(Exception):
    pass


def is_string_in_road(string: str, road: RoadUnit) -> bool:
    return road.find(string) >= 0


def replace_wall(road: RoadUnit, old_wall: str, new_wall: str):
    if is_string_in_road(string=new_wall, road=road):
        raise InvalidwallReplaceException(
            f"Cannot replace_wall '{old_wall}' with '{new_wall}' because the new one exists in road '{road}'."
        )
    return road.replace(old_wall, new_wall)


class ValidateIdeaUnitException(Exception):
    pass


def is_ideaunit(x_ideaunit: IdeaUnit, x_wall: str):
    x_ideaunit = IdeaUnit(x_ideaunit)
    return x_ideaunit.is_idea(wall=x_wall)


def validate_ideaunit(
    x_ideaunit: IdeaUnit, x_wall: str, not_ideaunit_required: bool = False
):
    if is_ideaunit(x_ideaunit, x_wall) and not_ideaunit_required:
        raise ValidateIdeaUnitException(
            f"'{x_ideaunit}' needs to not be a IdeaUnit. Must contain wall: '{x_wall}'"
        )
    elif is_ideaunit(x_ideaunit, x_wall) is False and not not_ideaunit_required:
        raise ValidateIdeaUnitException(
            f"'{x_ideaunit}' needs to be a IdeaUnit. Cannot contain wall: '{x_wall}'"
        )

    return x_ideaunit


def roadunit_valid_dir_path(x_roadunit: RoadUnit, wall: str) -> bool:
    x_road_ideas = get_all_road_ideas(x_roadunit, wall)
    slash_str = "/"
    x_road_os_path = create_road_from_ideas(x_road_ideas, wall=slash_str)
    parts = pathlib_Path(x_road_os_path).parts
    if len(parts) != len(x_road_ideas):
        return False

    return is_path_valid(x_road_os_path)


def get_road_from_doar(x_doarunit: DoarUnit, wall: str = None) -> RoadUnit:
    x_wall = default_wall_if_none(wall)
    doar_ideas = get_all_road_ideas(x_doarunit, x_wall)
    return RoadUnit(create_road_from_ideas(doar_ideas[::-1], x_wall))


def get_doar_from_road(x_roadunit: RoadUnit, wall: str = None) -> DoarUnit:
    return DoarUnit(get_road_from_doar(x_roadunit, wall))
