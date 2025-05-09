from src.a01_road_logic.road import (
    RoadUnit,
    to_road,
    get_default_fisc_road,
    create_road,
    create_road_from_tags,
    rebuild_road,
    is_sub_road,
    get_all_road_tags,
    get_terminus_tag,
    find_replace_road_key_dict,
    get_parent_road,
    get_root_tag_from_road,
    get_ancestor_roads,
    get_forefather_roads,
    get_default_fisc_tag,
    get_default_fisc_road as root_road,
    is_heir_road,
    default_bridge_if_None,
    replace_bridge,
    validate_tagunit,
    roadunit_valid_dir_path,
    all_roadunits_between,
    is_tagunit,
)
from pytest import raises as pytest_raises
from dataclasses import dataclass
from platform import system as platform_system


def test_to_road_ReturnsObj_WithDefault_bridge():
    # ESTABLISH
    x_tag = "run"
    x_bridge = default_bridge_if_None()

    # WHEN / THEN
    assert to_road(x_tag) == f"{x_bridge}{x_tag}"
    assert to_road(f"{x_bridge}{x_tag}") == f"{x_bridge}{x_tag}"
    assert to_road(f"{x_bridge}{x_bridge}{x_tag}") == f"{x_bridge}{x_bridge}{x_tag}"
    assert to_road(x_bridge) == x_bridge
    assert to_road(None) == x_bridge


def test_to_road_ReturnsObj_WithParameter_bridge():
    # ESTABLISH
    x_tag = "run"
    slash_bridge = "/"

    # WHEN / THEN
    assert to_road(x_tag, slash_bridge) == f"{slash_bridge}{x_tag}"
    assert to_road(f"{slash_bridge}{x_tag}", slash_bridge) == f"{slash_bridge}{x_tag}"
    assert (
        to_road(f"{slash_bridge}{slash_bridge}{x_tag}", slash_bridge)
        == f"{slash_bridge}{slash_bridge}{x_tag}"
    )
    assert to_road(slash_bridge, slash_bridge) == slash_bridge
    assert to_road(None, slash_bridge) == slash_bridge


def test_get_default_fisc_tag_ReturnsObj():
    assert get_default_fisc_tag() == "ZZ"


def test_get_default_fisc_road_ReturnsObj():
    # ESTABLISH
    default_bridge = default_bridge_if_None()
    default_root_tag = get_default_fisc_tag()
    slash_bridge = "/"

    # WHEN / THEN
    assert get_default_fisc_road() == to_road(default_root_tag)
    assert get_default_fisc_road(slash_bridge) == to_road(
        default_root_tag, slash_bridge
    )


def test_create_road_Scenario0_RaisesErrorIfBridgeNotAtPostionZeroOf_parent_road():
    # ESTABLISH
    rose_str = "rose"
    semicolon_bridge = ";"
    semicolon_bridge_rose_road = f"{semicolon_bridge}{rose_str}"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_road(
            "ZZ", rose_str, auto_add_first_bridge=False
        ) == semicolon_bridge_rose_road
    exception_str = (
        f"Parent road must have bridge '{semicolon_bridge}' at position 0 in string"
    )
    assert str(excinfo.value) == exception_str


def test_create_road_Scenario1_DoesNotRaiseError():
    # ESTABLISH
    rose_str = "rose"

    # WHEN / THEN
    assert create_road("ZZ", rose_str)


def test_create_road_ReturnsObj_Scenario3():
    # ESTABLISH
    rose_str = "rose"
    semicolon_bridge = ";"
    assert semicolon_bridge == default_bridge_if_None()
    semicolon_bridge_rose_road = f"{root_road()}{semicolon_bridge}{rose_str}"

    # WHEN / THEN
    assert create_road(root_road(), rose_str) == semicolon_bridge_rose_road


def test_create_road_ReturnsObj_Scenario4():
    # ESTABLISH
    rose_str = "rose"
    slash_bridge = "/"
    slash_bridge_rose_road = (
        f"{slash_bridge}{get_default_fisc_tag()}{slash_bridge}{rose_str}"
    )

    # WHEN
    generated_rose_road = create_road(
        get_default_fisc_tag(), rose_str, bridge=slash_bridge
    )
    # THEN
    assert generated_rose_road == slash_bridge_rose_road


def test_road_create_road_ReturnsObj_Scenario5():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_road()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_road()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_road()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THEN
    assert create_road(None, get_default_fisc_tag()) == root_road()
    assert create_road("", get_default_fisc_tag()) == root_road()
    assert create_road(root_road(), casa_str) == casa_road
    assert create_road(casa_road, bloomers_str) == bloomers_road
    assert create_road(bloomers_road, roses_str) == roses_road
    assert create_road(roses_road, None) == roses_road


def test_road_is_sub_road_correctlyReturnsBool():
    # WHEN
    casa_str = "casa"
    casa_road = f"{root_road()}{default_bridge_if_None()}{casa_str}"
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


def test_road_rebuild_road_ReturnsCorrectRoadUnit():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_road(), casa_str)
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


def test_road_get_all_road_tags_ReturnsTagUnits():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_road()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_road()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_road()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THENs
    root_list = [get_default_fisc_tag()]
    assert get_all_road_tags(road=root_road()) == root_list
    casa_list = [get_default_fisc_tag(), casa_str]
    assert get_all_road_tags(road=casa_road) == casa_list
    bloomers_list = [get_default_fisc_tag(), casa_str, bloomers_str]
    assert get_all_road_tags(road=bloomers_road) == bloomers_list
    roses_list = [get_default_fisc_tag(), casa_str, bloomers_str, roses_str]
    assert get_all_road_tags(road=roses_road) == roses_list


def test_road_get_terminus_tag_ReturnsTagUnit():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_road()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_terminus_tag(road=root_road()) == get_default_fisc_tag()
    assert get_terminus_tag(road=casa_road) == casa_str
    assert get_terminus_tag(road=bloomers_road) == bloomers_str
    assert get_terminus_tag(road=roses_road) == roses_str


def test_road_get_terminus_tag_ReturnsTagUnitWhenNonDefaultbridge():
    # ESTABLISH
    casa_str = "casa"
    bloomers_str = "bloomers"
    roses_str = "roses"
    slash_str = "/"
    slash_casa_road = f"{slash_str}{get_default_fisc_tag()}{slash_str}{casa_str}"
    slash_bloomers_road = f"{slash_str}{slash_casa_road}{slash_str}{bloomers_str}"
    slash_roses_road = f"{slash_str}{slash_bloomers_road}{slash_str}{roses_str}"

    # WHEN / THENs
    assert get_terminus_tag(slash_casa_road, slash_str) == casa_str
    assert get_terminus_tag(slash_bloomers_road, slash_str) == bloomers_str
    assert get_terminus_tag(slash_roses_road, slash_str) == roses_str


def test_road_get_root_tag_from_road_ReturnsTagUnit():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_road(), casa_str)
    bloomers_str = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_str)
    roses_str = "roses"
    roses_road = create_road(casa_str, roses_str)

    # WHEN / THENs
    assert get_root_tag_from_road(root_road()) == get_default_fisc_tag()
    assert get_root_tag_from_road(casa_road) == get_default_fisc_tag()
    assert get_root_tag_from_road(bloomers_road) == get_default_fisc_tag()
    assert get_root_tag_from_road(roses_road) == casa_str


def test_road_get_parent_road_ReturnsObj_Scenario0():
    # ESTABLISH
    x_s = default_bridge_if_None()
    root_fisc_road = f"{x_s}{get_default_fisc_tag()}"
    casa_str = "casa"
    casa_road = f"{root_fisc_road}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_road(root_road(), x_s) == ""
    assert get_parent_road(casa_road, x_s) == root_fisc_road
    assert get_parent_road(bloomers_road, x_s) == casa_road
    assert get_parent_road(roses_road, x_s) == bloomers_road


def test_road_get_parent_road_ReturnsObj_Scenario1():
    # ESTABLISH
    x_s = "/"
    root_fisc_road = f"{x_s}{get_default_fisc_tag()}"
    casa_str = "casa"
    casa_road = f"{root_fisc_road}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_road(root_fisc_road, x_s) == ""
    assert get_parent_road(casa_road, x_s) == root_fisc_road
    assert get_parent_road(bloomers_road, x_s) == casa_road
    assert get_parent_road(roses_road, x_s) == bloomers_road


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
    old_seasons_road = f"{root_road()}{x_s}casa{x_s}seasons"
    old_dict_x = {old_seasons_road: TempTestingObj(old_seasons_road)}
    assert old_dict_x.get(old_seasons_road) is not None

    # WHEN
    new_seasons_road = f"{root_road()}{x_s}casa{x_s}kookies"
    new_dict_x = find_replace_road_key_dict(
        dict_x=old_dict_x, old_road=old_seasons_road, new_road=new_seasons_road
    )

    # THEN
    assert new_dict_x != {}
    assert len(new_dict_x) == 1
    print(f"{new_dict_x=}")
    assert new_dict_x.get(new_seasons_road) is not None
    assert new_dict_x.get(old_seasons_road) is None


def test_road_get_ancestor_roads_ReturnsObj_Scenario0_default_bridge():
    # ESTABLISH
    x_s = default_bridge_if_None()
    nation_str = "nation-state"
    nation_road = f"{root_road()}{x_s}{nation_str}"
    usa_str = "USA"
    usa_road = f"{nation_road}{x_s}{usa_str}"
    texas_str = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_str}"

    # WHEN
    texas_anc_roads = get_ancestor_roads(road=texas_road)

    # THEN
    print(f"     {texas_road=}")
    print(f"{texas_anc_roads=}")
    assert texas_anc_roads is not None
    texas_ancestor_roads = [
        texas_road,
        usa_road,
        nation_road,
        root_road(),
    ]
    assert texas_anc_roads == texas_ancestor_roads

    # WHEN
    assert get_ancestor_roads(None) == []
    assert get_ancestor_roads("") == []
    assert get_ancestor_roads(root_road()) == [root_road()]


def test_road_get_ancestor_roads_ReturnsObj_Scenario1_nondefault_bridge():
    # ESTABLISH
    x_s = "/"
    root_fisc_road = f"{x_s}accord23"
    nation_str = "nation-state"
    nation_road = f"{root_fisc_road}{x_s}{nation_str}"
    usa_str = "USA"
    usa_road = f"{nation_road}{x_s}{usa_str}"
    texas_str = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_str}"

    # WHEN
    texas_anc_roads = get_ancestor_roads(road=texas_road, bridge=x_s)

    # THEN
    print(f"     {texas_road=}")
    print(f"{texas_anc_roads=}")
    assert texas_anc_roads is not None
    texas_ancestor_roads = [
        texas_road,
        usa_road,
        nation_road,
        root_fisc_road,
    ]
    assert texas_anc_roads == texas_ancestor_roads


def test_road_get_forefather_roads_ReturnsAncestorRoadUnitsWithoutClean():
    # ESTABLISH
    x_s = default_bridge_if_None()
    nation_str = "nation-state"
    nation_road = f"{root_road()}{x_s}{nation_str}"
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
        root_road(): None,
    }
    assert x_roads == texas_forefather_roads


def test_road_get_default_fisc_tag_ReturnsObj():
    assert get_default_fisc_tag() == "ZZ"


def test_road_create_road_from_tags_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    root_list = get_all_road_tags(root_road())
    casa_str = "casa"
    casa_road = f"{root_road()}{x_s}{casa_str}"
    casa_list = get_all_road_tags(casa_road)
    bloomers_str = "bloomers"
    bloomers_road = f"{root_road()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_list = get_all_road_tags(bloomers_road)
    roses_str = "roses"
    roses_road = f"{root_road()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_list = get_all_road_tags(roses_road)

    # WHEN / THEN
    assert root_road() == create_road_from_tags(root_list)
    assert casa_road == create_road_from_tags(casa_list)
    assert bloomers_road == create_road_from_tags(bloomers_list)
    assert roses_road == create_road_from_tags(roses_list)


def test_is_tagunit_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()

    # WHEN / THEN
    assert is_tagunit("", x_bridge=x_s) is False
    assert is_tagunit("casa", x_bridge=x_s)
    assert not is_tagunit(f"ZZ{x_s}casa", x_s)
    assert not is_tagunit(RoadUnit(f"ZZ{x_s}casa"), x_s)
    assert is_tagunit(RoadUnit("ZZ"), x_s)


def test_is_heir_road_CorrectlyIdentifiesHeirs():
    # ESTABLISH
    x_s = default_bridge_if_None()
    usa_str = "USA"
    usa_road = f"{root_road()}{x_s}Nation-States{x_s}{usa_str}"
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
    root_tag = get_default_fisc_tag()
    gen_casa_road = create_road(root_tag, casa_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_casa_road = (
        f"{semicolon_bridge}{root_tag}{semicolon_bridge}{casa_str}"
    )
    assert semicolon_bridge == ";"
    assert gen_casa_road == semicolon_bridge_casa_road

    # WHEN
    slash_bridge = "/"
    gen_casa_road = replace_bridge(
        gen_casa_road, old_bridge=semicolon_bridge, new_bridge=slash_bridge
    )

    # THEN
    slash_bridge_casa_road = f"{slash_bridge}{root_tag}{slash_bridge}{casa_str}"
    assert gen_casa_road == slash_bridge_casa_road


def test_replace_bridge_CorrectlyRaisesError():
    # ESTABLISH
    cooker_str = "cooker/cleaner"
    gen_cooker_road = create_road(root_road(), cooker_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_cooker_road = f"{root_road()}{semicolon_bridge}{cooker_str}"
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


def test_validate_tagunit_RaisesErrorWhenNotTagUnit():
    # ESTABLISH
    bob_str = "Bob, Tom"
    slash_str = "/"
    assert bob_str == validate_tagunit(bob_str, x_bridge=slash_str)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_tagunit(bob_str, x_bridge=comma_str)
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to be a TagUnit. Cannot contain bridge: '{comma_str}'"
    )


def test_validate_tagunit_RaisesErrorWhenTagUnit():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Tom"
    assert bob_str == validate_tagunit(
        bob_str, x_bridge=slash_str, not_tagunit_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_tagunit(
            bob_str, x_bridge=comma_str, not_tagunit_required=True
        )
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to not be a TagUnit. Must contain bridge: '{comma_str}'"
    )


def test_roadunit_valid_dir_path_ReturnsObj_simple_bridge():
    # ESTABLISH
    comma_str = ","
    # WHEN / THEN
    assert roadunit_valid_dir_path(",run", bridge=comma_str)
    assert roadunit_valid_dir_path(",run,sport", bridge=comma_str)
    print(f"{platform_system()=}")
    sport_question_valid_bool = roadunit_valid_dir_path("run,sport?", comma_str)
    assert (
        platform_system() == "Windows" and sport_question_valid_bool is False
    ) or platform_system() == "Linux"


def test_roadunit_valid_dir_path_ReturnsObj_complicated_bridge():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run,"
    lap_str = "lap"
    sport_road = create_road(sport_str, bridge=question_str)
    print(f"{sport_road=}")
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


def test_roadunit_valid_dir_path_ReturnsObjWhereSlashNotbridgeEdgeCases():
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
