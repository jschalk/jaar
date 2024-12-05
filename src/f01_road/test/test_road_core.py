from src.f01_road.road import (
    IdeaUnit,
    HealerID,
    OwnerID,
    AcctID,
    RoadUnit,
    DoarUnit,
    GroupID,
    create_road,
    create_road_from_ideas,
    create_road_without_root_idea,
    combine_roads,
    rebuild_road,
    is_sub_road,
    get_all_road_ideas,
    get_terminus_idea,
    find_replace_road_key_dict,
    get_parent_road,
    get_root_idea_from_road,
    road_validate,
    get_ancestor_roads,
    get_forefather_roads,
    get_default_fiscal_id_ideaunit as root_label,
    get_diff_road,
    is_heir_road,
    default_wall_if_none,
    replace_wall,
    validate_ideaunit,
    roadunit_valid_dir_path,
    all_roadunits_between,
    is_ideaunit,
    WorldID,
    get_default_world_id,
    TimeLineLabel,
    FaceID,
    get_default_face_id,
)
from pytest import raises as pytest_raises
from dataclasses import dataclass
from inspect import getdoc as inspect_getdoc
from platform import system as platform_system


def test_HealerID_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_healer_id = HealerID(bob_str)
    # THEN
    assert bob_healer_id == bob_str
    doc_str = "A IdeaUnit used to identify a Problem's Healer"
    assert inspect_getdoc(bob_healer_id) == doc_str


def test_OwnerID_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_owner_id = OwnerID(bob_str)
    # THEN
    assert bob_owner_id == bob_str
    doc_str = "A IdeaUnit used to identify a BudUnit's owner_id"
    assert inspect_getdoc(bob_owner_id) == doc_str


def test_AcctID_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_acct_id = AcctID(bob_str)
    # THEN
    assert bob_acct_id == bob_str
    doc_str = "Every AcctID object is OwnerID, must follow OwnerID format."
    assert inspect_getdoc(bob_acct_id) == doc_str


def test_GroupID_exists():
    bikers_group_id = GroupID("bikers")
    assert bikers_group_id is not None
    assert str(type(bikers_group_id)).find("src.f01_road.road.GroupID") > 0


def test_IdeaUnit_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_road = IdeaUnit(empty_str)
    # THEN
    assert x_road == empty_str
    doc_str = "A string presentation of a tree node. Nodes cannot contain RoadUnit wall"
    assert inspect_getdoc(x_road) == doc_str


def test_IdeaUnit_is_idea_ReturnsObj_Scenario0():
    # WHEN / THEN
    assert IdeaUnit("").is_idea() is False
    assert IdeaUnit("A").is_idea()

    # WHEN / THEN
    x_s = default_wall_if_none()
    x_ideaunit = IdeaUnit(f"casa{x_s}kitchen")
    assert x_ideaunit.is_idea() is False


def test_IdeaUnit_is_idea_ReturnsObj_Scenario1():
    # ESTABLISH / WHEN / THEN
    slash_str = "/"
    x_ideaunit = IdeaUnit(f"casa{slash_str}kitchen")
    assert x_ideaunit.is_idea()
    assert x_ideaunit.is_idea(slash_str) is False


def test_RoadUnit_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_road = RoadUnit(empty_str)
    # THEN
    assert x_road == empty_str
    doc_str = (
        "A string presentation of a tree path. IdeaUnits are seperated by road wall"
    )
    assert inspect_getdoc(x_road) == doc_str


def test_DoarUnit_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_road = DoarUnit(empty_str)
    # THEN
    assert x_road == empty_str
    doc_str = "DoarUnit is a RoadUnit in reverse direction. A string presentation of a tree path. IdeaUnits are seperated by road wall."
    assert inspect_getdoc(x_road) == doc_str


def test_TimeLineLabel_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_timelinelabel = TimeLineLabel(empty_str)
    # THEN
    assert x_timelinelabel == empty_str
    doc_str = "TimeLineLabel is required for every TimeLineUnit. It is a IdeaUnit that must not container the wall."
    assert inspect_getdoc(x_timelinelabel) == doc_str


def test_WorldID_Exists():
    # ESTABLISH / WHEN / THEN
    assert WorldID() == ""
    assert WorldID("cookie") == "cookie"


def test_get_default_world_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_world_id() == "TestingWorld3"


def test_FaceID_Exists():
    # ESTABLISH / WHEN / THEN
    assert FaceID() == ""
    assert FaceID("cookie") == "cookie"


def test_get_default_face_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_face_id() == "Face1234"


def test_create_road_ReturnsCorrectRoadUnitWith_wall():
    # ESTABLISH
    rose_str = "rose"
    semicolon_wall = ";"
    semicolon_wall_rose_road = f"{root_label()}{semicolon_wall}{rose_str}"
    assert create_road(root_label(), rose_str) == semicolon_wall_rose_road

    # WHEN
    slash_wall = "/"
    slash_wall_rose_road = f"{root_label()}{slash_wall}{rose_str}"
    generated_rose_road = create_road(root_label(), rose_str, wall=slash_wall)

    # THEN
    assert generated_rose_road != semicolon_wall_rose_road
    assert generated_rose_road == slash_wall_rose_road

    # WHEN
    brackets_road = create_road(root_label(), rose_str, wall=slash_wall)

    # THEN
    assert generated_rose_road == brackets_road
    assert slash_wall_rose_road == brackets_road


def test_combine_road_ReturnsObj_Scenario0_default_wall():
    # ESTABLISH
    rose_str = "rose"
    rose_road = create_road(root_label(), rose_str)
    casa_str = "casa"
    clean_str = "clean"
    clean_road = create_road(casa_str, clean_str)

    # WHEN
    gen_clean_road = combine_roads(rose_road, clean_road)

    # THEN
    example1_casa_road = create_road(rose_road, casa_str)
    example1_clean_road = create_road(example1_casa_road, clean_str)
    assert gen_clean_road == example1_clean_road


def test_combine_road_ReturnsObj_Scenario1_():
    # ESTABLISH
    slash_str = "/"
    rose_str = "rose"
    rose_road = create_road(root_label(), rose_str, slash_str)
    casa_str = "casa"
    clean_str = "clean"
    clean_road = create_road(casa_str, clean_str, slash_str)

    # WHEN
    gen_clean_road = combine_roads(rose_road, clean_road, slash_str)

    # THEN
    example1_casa_road = create_road(rose_road, casa_str, slash_str)
    example1_clean_road = create_road(example1_casa_road, clean_str, slash_str)
    assert gen_clean_road == example1_clean_road


def test_combine_road_ReturnsObj_Scenario1_():
    # ESTABLISH
    slash_str = "/"
    casa_str = "casa"

    # WHEN
    gen_casa_road = combine_roads("", casa_str, slash_str)

    # THEN
    example1_casa_road = create_road("", casa_str, slash_str)
    assert gen_casa_road == example1_casa_road
    assert gen_casa_road == casa_str


def test_road_is_sub_road_correctlyReturnsBool():
    # WHEN
    casa_str = "casa"
    casa_road = f"{root_label()}{default_wall_if_none()}{casa_str}"
    cleaning_str = "cleaning"
    cleaning_road = f"{casa_road}{default_wall_if_none()}{cleaning_str}"
    laundrys_str = "laundrys"
    laundrys_road = f"{cleaning_road}{default_wall_if_none()}{laundrys_str}"
    print(f"{cleaning_road=}")
    print(f"{laundrys_road=}")

    # WHEN / THEN
    assert is_sub_road(cleaning_road, cleaning_road)
    assert is_sub_road(laundrys_road, cleaning_road)
    assert is_sub_road(cleaning_road, laundrys_road) is False


def test_road_road_validate_correctlyReturnsRoadUnit():
    x_s = default_wall_if_none()
    _fiscal_id = "x"
    casa_road = f"{_fiscal_id}{x_s}casa"
    clean_road = f"{_fiscal_id}{x_s}clean"
    fun_road = f"{_fiscal_id}{x_s}fun"
    assert road_validate(None, x_s, _fiscal_id) == ""
    assert road_validate("", x_s, _fiscal_id) == ""
    assert road_validate(f"{_fiscal_id}{x_s}casa", x_s, _fiscal_id) == casa_road
    assert road_validate(f"A{x_s}casa", x_s, _fiscal_id) == casa_road
    assert road_validate(f"{x_s}clean", x_s, _fiscal_id) == clean_road
    assert road_validate(f"clean{x_s}fun", x_s, _fiscal_id) == fun_road
    assert road_validate("clean", x_s, _fiscal_id) == _fiscal_id
    assert road_validate(f"AA{x_s}casa", x_s, _fiscal_id) == casa_road


def test_road_rebuild_road_ReturnsCorrectRoadUnit():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str)
    bloomers_str = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_str)
    greenery_str = "greenery"
    greenery_road = create_road(casa_road, greenery_str)
    roses_str = "roses"
    old_roses_road = create_road(bloomers_road, roses_str)
    new_roses_road = create_road(greenery_road, roses_str)

    print(f"{rebuild_road(old_roses_road, bloomers_road, greenery_road)}")

    # WHEN / THEN
    assert rebuild_road(bloomers_road, bloomers_road, bloomers_road) == bloomers_road
    assert rebuild_road(old_roses_road, bloomers_road, greenery_road) == new_roses_road
    assert rebuild_road(old_roses_road, "random_str", greenery_road) == old_roses_road


def test_road_get_all_road_ideas_ReturnsIdeaUnits():
    # ESTABLISH
    x_s = default_wall_if_none()
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THENs
    root_list = [root_label()]
    assert get_all_road_ideas(road=root_label()) == root_list
    casa_list = [root_label(), casa_str]
    assert get_all_road_ideas(road=casa_road) == casa_list
    bloomers_list = [root_label(), casa_str, bloomers_str]
    assert get_all_road_ideas(road=bloomers_road) == bloomers_list
    roses_list = [root_label(), casa_str, bloomers_str, roses_str]
    assert get_all_road_ideas(road=roses_road) == roses_list


def test_road_get_terminus_idea_ReturnsIdeaUnit():
    # ESTABLISH
    x_s = default_wall_if_none()
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_terminus_idea(road=root_label()) == root_label()
    assert get_terminus_idea(road=casa_road) == casa_str
    assert get_terminus_idea(road=bloomers_road) == bloomers_str
    assert get_terminus_idea(road=roses_road) == roses_str


def test_road_get_terminus_idea_ReturnsIdeaUnitWhenNonDefaultwall():
    # ESTABLISH
    casa_str = "casa"
    bloomers_str = "bloomers"
    roses_str = "roses"
    slash_str = default_wall_if_none()
    slash_casa_road = f"{root_label()}{slash_str}{casa_str}"
    slash_bloomers_road = f"{slash_casa_road}{slash_str}{bloomers_str}"
    slash_roses_road = f"{slash_bloomers_road}{slash_str}{roses_str}"

    # WHEN / THENs
    assert get_terminus_idea(root_label(), slash_str) == root_label()
    assert get_terminus_idea(slash_casa_road, slash_str) == casa_str
    assert get_terminus_idea(slash_bloomers_road, slash_str) == bloomers_str
    assert get_terminus_idea(slash_roses_road, slash_str) == roses_str


def test_road_get_root_idea_from_road_ReturnsIdeaUnit():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_label(), casa_str)
    bloomers_str = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_str)
    roses_str = "roses"
    roses_road = create_road(casa_str, roses_str)

    # WHEN / THENs
    assert get_root_idea_from_road(root_label()) == root_label()
    assert get_root_idea_from_road(casa_road) == root_label()
    assert get_root_idea_from_road(bloomers_road) == root_label()
    assert get_root_idea_from_road(roses_road) == casa_str


def test_road_get_parent_road_ReturnsCorrectObj_Scenario0():
    # ESTABLISH
    x_s = default_wall_if_none()
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_road(root_label(), x_s) == ""
    assert get_parent_road(casa_road, x_s) == root_label()
    assert get_parent_road(bloomers_road, x_s) == casa_road
    assert get_parent_road(roses_road, x_s) == bloomers_road


def test_road_get_parent_road_ReturnsCorrectObj_Scenario1():
    # ESTABLISH
    x_s = "/"
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_road(root_label(), x_s) == ""
    assert get_parent_road(casa_road, x_s) == root_label()
    assert get_parent_road(bloomers_road, x_s) == casa_road
    assert get_parent_road(roses_road, x_s) == bloomers_road


def test_road_create_road_without_root_idea_ReturnsCorrectObj():
    # ESTABLISH
    x_s = default_wall_if_none()
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    casa_without_root_road = f"{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_without_root_road = f"{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_without_root_road = f"{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THENs
    assert create_road_without_root_idea(road=root_label()) == x_s
    assert create_road_without_root_idea(road=casa_road) == casa_without_root_road
    assert (
        create_road_without_root_idea(road=bloomers_road) == bloomers_without_root_road
    )
    assert create_road_without_root_idea(road=roses_road) == roses_without_root_road
    road_without_idea = create_road_without_root_idea(road=roses_road)
    with pytest_raises(Exception) as excinfo:
        create_road_without_root_idea(road=road_without_idea)
    assert (
        str(excinfo.value)
        == f"Cannot create_road_without_root_idea of '{road_without_idea}' because it has no root idea."
    )


@dataclass
class TempTestingObj:
    x_road: RoadUnit = ""

    def find_replace_road(self, old_road, new_road):
        self.x_road = rebuild_road(self.x_road, old_road=old_road, new_road=new_road)

    def get_obj_key(self) -> RoadUnit:
        return self.x_road


def test_road_find_replace_road_key_dict_ReturnsCorrectDict_Scenario1():
    # ESTABLISH
    x_s = default_wall_if_none()
    old_seasons_road = f"{root_label()}{x_s}casa{x_s}seasons"
    old_dict_x = {old_seasons_road: TempTestingObj(old_seasons_road)}
    assert old_dict_x.get(old_seasons_road) is not None

    # WHEN
    new_seasons_road = f"{root_label()}{x_s}casa{x_s}kookies"
    new_dict_x = find_replace_road_key_dict(
        dict_x=old_dict_x, old_road=old_seasons_road, new_road=new_seasons_road
    )

    # THEN
    assert new_dict_x != {}
    assert len(new_dict_x) == 1
    print(f"{new_dict_x=}")
    assert new_dict_x.get(new_seasons_road) is not None
    assert new_dict_x.get(old_seasons_road) is None


def test_road_get_ancestor_roads_ReturnsAncestorRoadUnits():
    # ESTABLISH
    x_s = default_wall_if_none()
    nation_str = "nation-state"
    nation_road = f"{root_label()}{x_s}{nation_str}"
    usa_str = "USA"
    usa_road = f"{nation_road}{x_s}{usa_str}"
    texas_str = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_str}"

    # WHEN
    x_roads = get_ancestor_roads(road=texas_road)

    # THEN
    print(f"{texas_road=}")
    assert x_roads is not None
    texas_ancestor_roads = [
        texas_road,
        usa_road,
        nation_road,
        root_label(),
    ]
    assert x_roads == texas_ancestor_roads

    # WHEN
    assert get_ancestor_roads(None) == []
    assert get_ancestor_roads("") == [""]
    assert get_ancestor_roads(root_label()) == [root_label()]


def test_road_get_forefather_roads_ReturnsAncestorRoadUnitsWithoutClean():
    # ESTABLISH
    x_s = default_wall_if_none()
    nation_str = "nation-state"
    nation_road = f"{root_label()}{x_s}{nation_str}"
    usa_str = "USA"
    usa_road = f"{nation_road}{x_s}{usa_str}"
    texas_str = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_str}"

    # WHEN
    x_roads = get_forefather_roads(road=texas_road)

    # THEN
    print(f"{texas_road=}")
    assert x_roads is not None
    texas_forefather_roads = {
        nation_road: None,
        usa_road: None,
        root_label(): None,
    }
    assert x_roads == texas_forefather_roads


def test_road_get_default_fiscal_id_ideaunit_ReturnsCorrectObj():
    assert root_label() == "ZZ"


def test_road_create_road_from_ideas_ReturnsCorrectObj():
    # ESTABLISH
    x_s = default_wall_if_none()
    root_list = get_all_road_ideas(root_label())
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    casa_list = get_all_road_ideas(casa_road)
    bloomers_str = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_list = get_all_road_ideas(bloomers_road)
    roses_str = "roses"
    roses_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_list = get_all_road_ideas(roses_road)

    # WHEN / THEN
    assert root_label() == create_road_from_ideas(root_list)
    assert casa_road == create_road_from_ideas(casa_list)
    assert bloomers_road == create_road_from_ideas(bloomers_list)
    assert roses_road == create_road_from_ideas(roses_list)


def test_road_create_road_ReturnsCorrectObj():
    # ESTABLISH
    x_s = default_wall_if_none()
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THEN
    assert root_label() == create_road(None, root_label())
    assert root_label() == create_road("", root_label())
    assert casa_road == create_road(root_label(), casa_str)
    assert bloomers_road == create_road(casa_road, bloomers_str)
    assert roses_road == create_road(bloomers_road, roses_str)
    assert roses_road == create_road(roses_road, None)


def test_is_ideaunit_ReturnsObj():
    # ESTABLISH
    x_s = default_wall_if_none()

    # WHEN / THEN
    assert is_ideaunit("", x_wall=x_s) is False
    assert is_ideaunit("casa", x_wall=x_s)
    assert not is_ideaunit(f"ZZ{x_s}casa", x_s)
    assert not is_ideaunit(RoadUnit(f"ZZ{x_s}casa"), x_s)
    assert is_ideaunit(RoadUnit("ZZ"), x_s)


def test_get_diff_road_ReturnsCorrectObj():
    # ESTABLISH
    x_s = default_wall_if_none()
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THEN
    print(f"{casa_road=}")
    print(f"{bloomers_road=}")
    assert get_diff_road(bloomers_road, casa_road) == bloomers_str
    assert get_diff_road(roses_road, bloomers_road) == roses_str
    bloomers_rose_road = create_road(bloomers_str, roses_str)
    print(f"{bloomers_rose_road=}")
    assert get_diff_road(roses_road, casa_road) == bloomers_rose_road


def test_is_heir_road_CorrectlyIdentifiesHeirs():
    # ESTABLISH
    x_s = default_wall_if_none()
    usa_str = "USA"
    usa_road = f"{root_label()}{x_s}Nation-States{x_s}{usa_str}"
    texas_str = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_str}"
    # earth_str = "earth"
    # earth_road = f"{earth_str}"
    # sea_str = "sea"
    # sea_road = f"{earth_road}{x_s}{sea_str}"
    # seaside_str = "seaside"
    # seaside_road = f"{earth_road}{x_s}{seaside_str}"

    # WHEN / THEN
    assert is_heir_road(src=usa_road, heir=usa_road)
    assert is_heir_road(src=usa_road, heir=texas_road)
    assert is_heir_road(f"earth{x_s}sea", f"earth{x_s}seaside{x_s}beach") is False
    assert is_heir_road(src=f"earth{x_s}sea", heir=f"earth{x_s}seaside") is False


def test_replace_wall_ReturnsNewObj():
    # ESTABLISH
    casa_str = "casa"
    gen_casa_road = create_road(root_label(), casa_str)
    semicolon_wall = default_wall_if_none()
    semicolon_wall_casa_road = f"{root_label()}{semicolon_wall}{casa_str}"
    assert semicolon_wall == ";"
    assert gen_casa_road == semicolon_wall_casa_road

    # WHEN
    slash_wall = "/"
    gen_casa_road = replace_wall(
        gen_casa_road, old_wall=semicolon_wall, new_wall=slash_wall
    )

    # THEN
    slash_wall_casa_road = f"{root_label()}{slash_wall}{casa_str}"
    assert gen_casa_road == slash_wall_casa_road


def test_replace_wall_CorrectlyRaisesError():
    # ESTABLISH
    cooker_str = "cooker/cleaner"
    gen_cooker_road = create_road(root_label(), cooker_str)
    semicolon_wall = default_wall_if_none()
    semicolon_wall_cooker_road = f"{root_label()}{semicolon_wall}{cooker_str}"
    assert semicolon_wall == ";"
    assert gen_cooker_road == semicolon_wall_cooker_road

    # WHEN / THEN
    slash_wall = "/"
    with pytest_raises(Exception) as excinfo:
        gen_cooker_road = replace_wall(
            gen_cooker_road,
            old_wall=semicolon_wall,
            new_wall=slash_wall,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_wall '{semicolon_wall}' with '{slash_wall}' because the new one exists in road '{gen_cooker_road}'."
    )


def test_replace_wall_WhenNewwallIsFirstInRoadUnitRaisesError():
    # ESTABLISH
    cooker_str = "/cooker"
    cleaner_str = "cleaner"
    semicolon_wall = default_wall_if_none()
    semicolon_wall_cooker_road = f"{cooker_str}{semicolon_wall}{cleaner_str}"
    assert semicolon_wall == ";"

    # WHEN / THEN
    slash_wall = "/"
    with pytest_raises(Exception) as excinfo:
        semicolon_wall_cooker_road = replace_wall(
            semicolon_wall_cooker_road,
            old_wall=semicolon_wall,
            new_wall=slash_wall,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_wall '{semicolon_wall}' with '{slash_wall}' because the new one exists in road '{semicolon_wall_cooker_road}'."
    )


def test_validate_ideaunit_RaisesErrorWhenNotIdeaUnit():
    # ESTABLISH
    bob_str = "Bob, Tom"
    slash_str = "/"
    assert bob_str == validate_ideaunit(bob_str, x_wall=slash_str)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_ideaunit(bob_str, x_wall=comma_str)
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to be a IdeaUnit. Cannot contain wall: '{comma_str}'"
    )


def test_validate_ideaunit_RaisesErrorWhenIdeaUnit():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Tom"
    assert bob_str == validate_ideaunit(
        bob_str, x_wall=slash_str, not_ideaunit_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_ideaunit(
            bob_str, x_wall=comma_str, not_ideaunit_required=True
        )
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to not be a IdeaUnit. Must contain wall: '{comma_str}'"
    )


def test_roadunit_valid_dir_path_ReturnsCorrectObj_simple_wall():
    # ESTABLISH
    comma_str = ","
    # WHEN / THEN
    assert roadunit_valid_dir_path("run", wall=comma_str)
    assert roadunit_valid_dir_path("run,sport", wall=comma_str)
    print(f"{platform_system()=}")
    sport_question_valid_bool = roadunit_valid_dir_path("run,sport?", comma_str)
    assert (
        platform_system() == "Windows" and sport_question_valid_bool is False
    ) or platform_system() == "Linux"


def test_roadunit_valid_dir_path_ReturnsCorrectObj_complicated_wall():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run,"
    lap_str = "lap"
    sport_road = create_road(sport_str, wall=question_str)
    run_road = create_road(sport_road, run_str, wall=question_str)
    lap_road = create_road(run_road, lap_str, wall=question_str)
    assert lap_road == f"{sport_road}?{run_str}?{lap_str}"

    assert roadunit_valid_dir_path(sport_road, wall=question_str)
    assert roadunit_valid_dir_path(run_road, wall=question_str)
    assert roadunit_valid_dir_path(lap_road, wall=question_str)
    assert (
        platform_system() == "Windows"
        and roadunit_valid_dir_path(lap_road, wall=",") is False
    ) or platform_system() == "Linux"


def test_roadunit_valid_dir_path_ReturnsCorrectObjWhereSlashNotwallEdgeCases():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run/swim"
    lap_str = "lap"
    sport_road = create_road(sport_str, wall=question_str)
    run_road = create_road(sport_road, run_str, wall=question_str)
    lap_road = create_road(run_road, lap_str, wall=question_str)
    assert lap_road == f"{sport_road}?{run_str}?{lap_str}"

    assert roadunit_valid_dir_path(sport_road, wall=question_str)
    assert roadunit_valid_dir_path(run_road, wall=question_str) is False
    assert roadunit_valid_dir_path(lap_road, wall=question_str) is False
    assert roadunit_valid_dir_path(lap_road, wall=",") is False


def test_all_roadunits_between_ReturnsObj():
    casa_str = "casa"
    sport_str = "sport"
    run_str = "run/swim"
    lap_str = "lap"
    sport_road = create_road(casa_str, sport_str)
    run_road = create_road(sport_road, run_str)
    lap_road = create_road(run_road, lap_str)

    assert all_roadunits_between(sport_road, sport_road) == [sport_road]
    assert all_roadunits_between(sport_road, run_road) == [sport_road, run_road]
    assert all_roadunits_between(sport_road, lap_road) == [
        sport_road,
        run_road,
        lap_road,
    ]
