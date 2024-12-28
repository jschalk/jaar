from src.f01_road.road import (
    IdeaUnit,
    HealerName,
    OwnerName,
    AcctName,
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
    get_default_deal_idea_ideaunit as root_lx,
    get_diff_road,
    is_heir_road,
    default_bridge_if_None,
    replace_bridge,
    validate_ideaunit,
    roadunit_valid_dir_path,
    all_roadunits_between,
    is_ideaunit,
    WorldID,
    get_default_world_id,
    TimeLineIdea,
    FaceName,
    get_default_face_name,
    EventInt,
)
from pytest import raises as pytest_raises
from dataclasses import dataclass
from inspect import getdoc as inspect_getdoc
from platform import system as platform_system


def test_HealerName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_healer_name = HealerName(bob_str)
    # THEN
    assert bob_healer_name == bob_str
    doc_str = "A IdeaUnit used to identify a Problem's Healer"
    assert inspect_getdoc(bob_healer_name) == doc_str


def test_OwnerName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_owner_name = OwnerName(bob_str)
    # THEN
    assert bob_owner_name == bob_str
    doc_str = "A IdeaUnit used to identify a BudUnit's owner_name"
    assert inspect_getdoc(bob_owner_name) == doc_str


def test_AcctName_exists():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    bob_acct_name = AcctName(bob_str)
    # THEN
    assert bob_acct_name == bob_str
    doc_str = "Every AcctName object is OwnerName, must follow OwnerName format."
    assert inspect_getdoc(bob_acct_name) == doc_str


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
    doc_str = (
        "A string presentation of a tree node. Nodes cannot contain RoadUnit bridge"
    )
    assert inspect_getdoc(x_road) == doc_str


def test_default_bridge_if_None_ReturnsObj():
    # ESTABLISH
    semicolon_str = ";"
    slash_str = "/"
    colon_str = ":"
    buzz_str = "buzz"

    # WHEN / THEN
    assert default_bridge_if_None() == semicolon_str
    assert default_bridge_if_None(None) == semicolon_str
    x_nan = float("nan")
    assert default_bridge_if_None(x_nan) == semicolon_str
    assert default_bridge_if_None(slash_str) == slash_str
    assert default_bridge_if_None(colon_str) == colon_str
    assert default_bridge_if_None(buzz_str) == buzz_str


def test_IdeaUnit_is_idea_ReturnsObj_Scenario0():
    # WHEN / THEN
    assert IdeaUnit("").is_idea() is False
    assert IdeaUnit("A").is_idea()

    # WHEN / THEN
    x_s = default_bridge_if_None()
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
        "A string presentation of a tree path. IdeaUnits are seperated by road bridge"
    )
    assert inspect_getdoc(x_road) == doc_str


def test_DoarUnit_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_road = DoarUnit(empty_str)
    # THEN
    assert x_road == empty_str
    doc_str = "DoarUnit is a RoadUnit in reverse direction. A string presentation of a tree path. IdeaUnits are seperated by road bridge."
    assert inspect_getdoc(x_road) == doc_str


def test_TimeLineIdea_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_timelineidea = TimeLineIdea(empty_str)
    # THEN
    assert x_timelineidea == empty_str
    doc_str = "TimeLineIdea is required for every TimeLineUnit. It is a IdeaUnit that must not container the bridge."
    assert inspect_getdoc(x_timelineidea) == doc_str


def test_WorldID_Exists():
    # ESTABLISH / WHEN / THEN
    assert WorldID() == ""
    assert WorldID("cookie") == "cookie"


def test_get_default_world_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_world_id() == "TestingWorld3"


def test_FaceName_Exists():
    # ESTABLISH / WHEN / THEN
    assert FaceName() == ""
    assert FaceName("cookie") == "cookie"


def test_get_default_face_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_face_name() == "Face1234"


def test_EventInt_Exists():
    # ESTABLISH / WHEN / THEN
    assert EventInt() == 0
    assert EventInt(12) == 12
    assert EventInt(12.4) == 12


def test_create_road_ReturnsObj_Scenario0():
    # ESTABLISH
    rose_str = "rose"
    semicolon_bridge = ";"
    assert semicolon_bridge == default_bridge_if_None()
    semicolon_bridge_rose_road = f"{root_lx()}{semicolon_bridge}{rose_str}"

    # WHEN / THEN
    assert create_road(root_lx(), rose_str) == semicolon_bridge_rose_road


def test_create_road_ReturnsObj_Scenario1():
    # ESTABLISH
    rose_str = "rose"
    slash_bridge = "/"
    slash_bridge_rose_road = f"{root_lx()}{slash_bridge}{rose_str}"

    # WHEN
    generated_rose_road = create_road(root_lx(), rose_str, bridge=slash_bridge)
    # THEN
    assert generated_rose_road == slash_bridge_rose_road


def test_create_road_ReturnsObj_Scenario2():
    # ESTABLISH
    rose_str = "rose"
    slash_bridge = "/"
    slash_bridge_rose_road = f"{root_lx()}{slash_bridge}{rose_str}"

    # WHEN / THEN
    assert create_road(root_lx(), rose_str, slash_bridge) == slash_bridge_rose_road


def test_combine_road_ReturnsObj_Scenario0_default_bridge():
    # ESTABLISH
    rose_str = "rose"
    rose_road = create_road(root_lx(), rose_str)
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
    rose_road = create_road(root_lx(), rose_str, slash_str)
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
    casa_road = f"{root_lx()}{default_bridge_if_None()}{casa_str}"
    cleaning_str = "cleaning"
    cleaning_road = f"{casa_road}{default_bridge_if_None()}{cleaning_str}"
    laundrys_str = "laundrys"
    laundrys_road = f"{cleaning_road}{default_bridge_if_None()}{laundrys_str}"
    print(f"{cleaning_road=}")
    print(f"{laundrys_road=}")

    # WHEN / THEN
    assert is_sub_road(cleaning_road, cleaning_road)
    assert is_sub_road(laundrys_road, cleaning_road)
    assert is_sub_road(cleaning_road, laundrys_road) is False


def test_road_road_validate_correctlyReturnsRoadUnit():
    x_s = default_bridge_if_None()
    _deal_idea = "x"
    casa_road = f"{_deal_idea}{x_s}casa"
    clean_road = f"{_deal_idea}{x_s}clean"
    fun_road = f"{_deal_idea}{x_s}fun"
    assert road_validate(None, x_s, _deal_idea) == ""
    assert road_validate("", x_s, _deal_idea) == ""
    assert road_validate(f"{_deal_idea}{x_s}casa", x_s, _deal_idea) == casa_road
    assert road_validate(f"A{x_s}casa", x_s, _deal_idea) == casa_road
    assert road_validate(f"{x_s}clean", x_s, _deal_idea) == clean_road
    assert road_validate(f"clean{x_s}fun", x_s, _deal_idea) == fun_road
    assert road_validate("clean", x_s, _deal_idea) == _deal_idea
    assert road_validate(f"AA{x_s}casa", x_s, _deal_idea) == casa_road


def test_road_rebuild_road_ReturnsCorrectRoadUnit():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_lx(), casa_str)
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
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_lx()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_lx()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_lx()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THENs
    root_list = [root_lx()]
    assert get_all_road_ideas(road=root_lx()) == root_list
    casa_list = [root_lx(), casa_str]
    assert get_all_road_ideas(road=casa_road) == casa_list
    bloomers_list = [root_lx(), casa_str, bloomers_str]
    assert get_all_road_ideas(road=bloomers_road) == bloomers_list
    roses_list = [root_lx(), casa_str, bloomers_str, roses_str]
    assert get_all_road_ideas(road=roses_road) == roses_list


def test_road_get_terminus_idea_ReturnsIdeaUnit():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_lx()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_terminus_idea(road=root_lx()) == root_lx()
    assert get_terminus_idea(road=casa_road) == casa_str
    assert get_terminus_idea(road=bloomers_road) == bloomers_str
    assert get_terminus_idea(road=roses_road) == roses_str


def test_road_get_terminus_idea_ReturnsIdeaUnitWhenNonDefaultbridge():
    # ESTABLISH
    casa_str = "casa"
    bloomers_str = "bloomers"
    roses_str = "roses"
    slash_str = default_bridge_if_None()
    slash_casa_road = f"{root_lx()}{slash_str}{casa_str}"
    slash_bloomers_road = f"{slash_casa_road}{slash_str}{bloomers_str}"
    slash_roses_road = f"{slash_bloomers_road}{slash_str}{roses_str}"

    # WHEN / THENs
    assert get_terminus_idea(root_lx(), slash_str) == root_lx()
    assert get_terminus_idea(slash_casa_road, slash_str) == casa_str
    assert get_terminus_idea(slash_bloomers_road, slash_str) == bloomers_str
    assert get_terminus_idea(slash_roses_road, slash_str) == roses_str


def test_road_get_root_idea_from_road_ReturnsIdeaUnit():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_lx(), casa_str)
    bloomers_str = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_str)
    roses_str = "roses"
    roses_road = create_road(casa_str, roses_str)

    # WHEN / THENs
    assert get_root_idea_from_road(root_lx()) == root_lx()
    assert get_root_idea_from_road(casa_road) == root_lx()
    assert get_root_idea_from_road(bloomers_road) == root_lx()
    assert get_root_idea_from_road(roses_road) == casa_str


def test_road_get_parent_road_ReturnsCorrectObj_Scenario0():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_lx()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_road(root_lx(), x_s) == ""
    assert get_parent_road(casa_road, x_s) == root_lx()
    assert get_parent_road(bloomers_road, x_s) == casa_road
    assert get_parent_road(roses_road, x_s) == bloomers_road


def test_road_get_parent_road_ReturnsCorrectObj_Scenario1():
    # ESTABLISH
    x_s = "/"
    casa_str = "casa"
    casa_road = f"{root_lx()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_road(root_lx(), x_s) == ""
    assert get_parent_road(casa_road, x_s) == root_lx()
    assert get_parent_road(bloomers_road, x_s) == casa_road
    assert get_parent_road(roses_road, x_s) == bloomers_road


def test_road_create_road_without_root_idea_ReturnsCorrectObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_lx()}{x_s}{casa_str}"
    casa_without_root_road = f"{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_lx()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_without_root_road = f"{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_lx()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_without_root_road = f"{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THENs
    assert create_road_without_root_idea(road=root_lx()) == x_s
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
    x_s = default_bridge_if_None()
    old_seasons_road = f"{root_lx()}{x_s}casa{x_s}seasons"
    old_dict_x = {old_seasons_road: TempTestingObj(old_seasons_road)}
    assert old_dict_x.get(old_seasons_road) is not None

    # WHEN
    new_seasons_road = f"{root_lx()}{x_s}casa{x_s}kookies"
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
    x_s = default_bridge_if_None()
    nation_str = "nation-state"
    nation_road = f"{root_lx()}{x_s}{nation_str}"
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
        root_lx(),
    ]
    assert x_roads == texas_ancestor_roads

    # WHEN
    assert get_ancestor_roads(None) == []
    assert get_ancestor_roads("") == [""]
    assert get_ancestor_roads(root_lx()) == [root_lx()]


def test_road_get_forefather_roads_ReturnsAncestorRoadUnitsWithoutClean():
    # ESTABLISH
    x_s = default_bridge_if_None()
    nation_str = "nation-state"
    nation_road = f"{root_lx()}{x_s}{nation_str}"
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
        root_lx(): None,
    }
    assert x_roads == texas_forefather_roads


def test_road_get_default_deal_idea_ideaunit_ReturnsCorrectObj():
    assert root_lx() == "ZZ"


def test_road_create_road_from_ideas_ReturnsCorrectObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    root_list = get_all_road_ideas(root_lx())
    casa_str = "casa"
    casa_road = f"{root_lx()}{x_s}{casa_str}"
    casa_list = get_all_road_ideas(casa_road)
    bloomers_str = "bloomers"
    bloomers_road = f"{root_lx()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_list = get_all_road_ideas(bloomers_road)
    roses_str = "roses"
    roses_road = f"{root_lx()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_list = get_all_road_ideas(roses_road)

    # WHEN / THEN
    assert root_lx() == create_road_from_ideas(root_list)
    assert casa_road == create_road_from_ideas(casa_list)
    assert bloomers_road == create_road_from_ideas(bloomers_list)
    assert roses_road == create_road_from_ideas(roses_list)


def test_road_create_road_ReturnsCorrectObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_lx()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_lx()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_lx()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THEN
    assert root_lx() == create_road(None, root_lx())
    assert root_lx() == create_road("", root_lx())
    assert casa_road == create_road(root_lx(), casa_str)
    assert bloomers_road == create_road(casa_road, bloomers_str)
    assert roses_road == create_road(bloomers_road, roses_str)
    assert roses_road == create_road(roses_road, None)


def test_is_ideaunit_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()

    # WHEN / THEN
    assert is_ideaunit("", x_bridge=x_s) is False
    assert is_ideaunit("casa", x_bridge=x_s)
    assert not is_ideaunit(f"ZZ{x_s}casa", x_s)
    assert not is_ideaunit(RoadUnit(f"ZZ{x_s}casa"), x_s)
    assert is_ideaunit(RoadUnit("ZZ"), x_s)


def test_get_diff_road_ReturnsCorrectObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_lx()}{x_s}{casa_str}"
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
    x_s = default_bridge_if_None()
    usa_str = "USA"
    usa_road = f"{root_lx()}{x_s}Nation-States{x_s}{usa_str}"
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


def test_replace_bridge_ReturnsNewObj():
    # ESTABLISH
    casa_str = "casa"
    gen_casa_road = create_road(root_lx(), casa_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_casa_road = f"{root_lx()}{semicolon_bridge}{casa_str}"
    assert semicolon_bridge == ";"
    assert gen_casa_road == semicolon_bridge_casa_road

    # WHEN
    slash_bridge = "/"
    gen_casa_road = replace_bridge(
        gen_casa_road, old_bridge=semicolon_bridge, new_bridge=slash_bridge
    )

    # THEN
    slash_bridge_casa_road = f"{root_lx()}{slash_bridge}{casa_str}"
    assert gen_casa_road == slash_bridge_casa_road


def test_replace_bridge_CorrectlyRaisesError():
    # ESTABLISH
    cooker_str = "cooker/cleaner"
    gen_cooker_road = create_road(root_lx(), cooker_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_cooker_road = f"{root_lx()}{semicolon_bridge}{cooker_str}"
    assert semicolon_bridge == ";"
    assert gen_cooker_road == semicolon_bridge_cooker_road

    # WHEN / THEN
    slash_bridge = "/"
    with pytest_raises(Exception) as excinfo:
        gen_cooker_road = replace_bridge(
            gen_cooker_road,
            old_bridge=semicolon_bridge,
            new_bridge=slash_bridge,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_bridge '{semicolon_bridge}' with '{slash_bridge}' because the new one exists in road '{gen_cooker_road}'."
    )


def test_replace_bridge_WhenNewbridgeIsFirstInRoadUnitRaisesError():
    # ESTABLISH
    cooker_str = "/cooker"
    cleaner_str = "cleaner"
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_cooker_road = f"{cooker_str}{semicolon_bridge}{cleaner_str}"
    assert semicolon_bridge == ";"

    # WHEN / THEN
    slash_bridge = "/"
    with pytest_raises(Exception) as excinfo:
        semicolon_bridge_cooker_road = replace_bridge(
            semicolon_bridge_cooker_road,
            old_bridge=semicolon_bridge,
            new_bridge=slash_bridge,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_bridge '{semicolon_bridge}' with '{slash_bridge}' because the new one exists in road '{semicolon_bridge_cooker_road}'."
    )


def test_validate_ideaunit_RaisesErrorWhenNotIdeaUnit():
    # ESTABLISH
    bob_str = "Bob, Tom"
    slash_str = "/"
    assert bob_str == validate_ideaunit(bob_str, x_bridge=slash_str)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_ideaunit(bob_str, x_bridge=comma_str)
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to be a IdeaUnit. Cannot contain bridge: '{comma_str}'"
    )


def test_validate_ideaunit_RaisesErrorWhenIdeaUnit():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Tom"
    assert bob_str == validate_ideaunit(
        bob_str, x_bridge=slash_str, not_ideaunit_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_ideaunit(
            bob_str, x_bridge=comma_str, not_ideaunit_required=True
        )
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to not be a IdeaUnit. Must contain bridge: '{comma_str}'"
    )


def test_roadunit_valid_dir_path_ReturnsCorrectObj_simple_bridge():
    # ESTABLISH
    comma_str = ","
    # WHEN / THEN
    assert roadunit_valid_dir_path("run", bridge=comma_str)
    assert roadunit_valid_dir_path("run,sport", bridge=comma_str)
    print(f"{platform_system()=}")
    sport_question_valid_bool = roadunit_valid_dir_path("run,sport?", comma_str)
    assert (
        platform_system() == "Windows" and sport_question_valid_bool is False
    ) or platform_system() == "Linux"


def test_roadunit_valid_dir_path_ReturnsCorrectObj_complicated_bridge():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run,"
    lap_str = "lap"
    sport_road = create_road(sport_str, bridge=question_str)
    run_road = create_road(sport_road, run_str, bridge=question_str)
    lap_road = create_road(run_road, lap_str, bridge=question_str)
    assert lap_road == f"{sport_road}?{run_str}?{lap_str}"

    assert roadunit_valid_dir_path(sport_road, bridge=question_str)
    assert roadunit_valid_dir_path(run_road, bridge=question_str)
    assert roadunit_valid_dir_path(lap_road, bridge=question_str)
    assert (
        platform_system() == "Windows"
        and roadunit_valid_dir_path(lap_road, bridge=",") is False
    ) or platform_system() == "Linux"


def test_roadunit_valid_dir_path_ReturnsCorrectObjWhereSlashNotbridgeEdgeCases():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run/swim"
    lap_str = "lap"
    sport_road = create_road(sport_str, bridge=question_str)
    run_road = create_road(sport_road, run_str, bridge=question_str)
    lap_road = create_road(run_road, lap_str, bridge=question_str)
    assert lap_road == f"{sport_road}?{run_str}?{lap_str}"

    assert roadunit_valid_dir_path(sport_road, bridge=question_str)
    assert roadunit_valid_dir_path(run_road, bridge=question_str) is False
    assert roadunit_valid_dir_path(lap_road, bridge=question_str) is False
    assert roadunit_valid_dir_path(lap_road, bridge=",") is False


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
