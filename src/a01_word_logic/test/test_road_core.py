from src.a01_word_logic.road import (
    RoadUnit,
    create_road,
    create_road_from_titles,
    create_road_without_root_title,
    combine_roads,
    rebuild_road,
    is_sub_road,
    get_all_road_titles,
    get_terminus_title,
    find_replace_road_key_dict,
    get_parent_road,
    get_root_title_from_road,
    road_validate,
    get_ancestor_roads,
    get_forefather_roads,
    get_default_fisc_title as root_title,
    get_diff_road,
    is_heir_road,
    default_bridge_if_None,
    replace_bridge,
    validate_titleunit,
    roadunit_valid_dir_path,
    all_roadunits_between,
    is_titleunit,
)
from pytest import raises as pytest_raises
from dataclasses import dataclass
from platform import system as platform_system


def test_create_road_ReturnsObj_Scenario0():
    # ESTABLISH
    rose_str = "rose"
    semicolon_bridge = ";"
    assert semicolon_bridge == default_bridge_if_None()
    semicolon_bridge_rose_road = f"{root_title()}{semicolon_bridge}{rose_str}"

    # WHEN / THEN
    assert create_road(root_title(), rose_str) == semicolon_bridge_rose_road


def test_create_road_ReturnsObj_Scenario1():
    # ESTABLISH
    rose_str = "rose"
    slash_bridge = "/"
    slash_bridge_rose_road = f"{root_title()}{slash_bridge}{rose_str}"

    # WHEN
    generated_rose_road = create_road(root_title(), rose_str, bridge=slash_bridge)
    # THEN
    assert generated_rose_road == slash_bridge_rose_road


def test_create_road_ReturnsObj_Scenario2():
    # ESTABLISH
    rose_str = "rose"
    slash_bridge = "/"
    slash_bridge_rose_road = f"{root_title()}{slash_bridge}{rose_str}"

    # WHEN / THEN
    assert create_road(root_title(), rose_str, slash_bridge) == slash_bridge_rose_road


def test_combine_road_ReturnsObj_Scenario0_default_bridge():
    # ESTABLISH
    rose_str = "rose"
    rose_road = create_road(root_title(), rose_str)
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
    rose_road = create_road(root_title(), rose_str, slash_str)
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
    casa_road = f"{root_title()}{default_bridge_if_None()}{casa_str}"
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
    _fisc_title = "x"
    casa_road = f"{_fisc_title}{x_s}casa"
    clean_road = f"{_fisc_title}{x_s}clean"
    fun_road = f"{_fisc_title}{x_s}fun"
    assert road_validate(None, x_s, _fisc_title) == ""
    assert road_validate("", x_s, _fisc_title) == ""
    assert road_validate(f"{_fisc_title}{x_s}casa", x_s, _fisc_title) == casa_road
    assert road_validate(f"A{x_s}casa", x_s, _fisc_title) == casa_road
    assert road_validate(f"{x_s}clean", x_s, _fisc_title) == clean_road
    assert road_validate(f"clean{x_s}fun", x_s, _fisc_title) == fun_road
    assert road_validate("clean", x_s, _fisc_title) == _fisc_title
    assert road_validate(f"AA{x_s}casa", x_s, _fisc_title) == casa_road


def test_road_rebuild_road_ReturnsCorrectRoadUnit():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_title(), casa_str)
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


def test_road_get_all_road_titles_ReturnsTitleUnits():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_title()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_title()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_title()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THENs
    root_list = [root_title()]
    assert get_all_road_titles(road=root_title()) == root_list
    casa_list = [root_title(), casa_str]
    assert get_all_road_titles(road=casa_road) == casa_list
    bloomers_list = [root_title(), casa_str, bloomers_str]
    assert get_all_road_titles(road=bloomers_road) == bloomers_list
    roses_list = [root_title(), casa_str, bloomers_str, roses_str]
    assert get_all_road_titles(road=roses_road) == roses_list


def test_road_get_terminus_title_ReturnsTitleUnit():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_title()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_terminus_title(road=root_title()) == root_title()
    assert get_terminus_title(road=casa_road) == casa_str
    assert get_terminus_title(road=bloomers_road) == bloomers_str
    assert get_terminus_title(road=roses_road) == roses_str


def test_road_get_terminus_title_ReturnsTitleUnitWhenNonDefaultbridge():
    # ESTABLISH
    casa_str = "casa"
    bloomers_str = "bloomers"
    roses_str = "roses"
    slash_str = default_bridge_if_None()
    slash_casa_road = f"{root_title()}{slash_str}{casa_str}"
    slash_bloomers_road = f"{slash_casa_road}{slash_str}{bloomers_str}"
    slash_roses_road = f"{slash_bloomers_road}{slash_str}{roses_str}"

    # WHEN / THENs
    assert get_terminus_title(root_title(), slash_str) == root_title()
    assert get_terminus_title(slash_casa_road, slash_str) == casa_str
    assert get_terminus_title(slash_bloomers_road, slash_str) == bloomers_str
    assert get_terminus_title(slash_roses_road, slash_str) == roses_str


def test_road_get_root_title_from_road_ReturnsTitleUnit():
    # ESTABLISH
    casa_str = "casa"
    casa_road = create_road(root_title(), casa_str)
    bloomers_str = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_str)
    roses_str = "roses"
    roses_road = create_road(casa_str, roses_str)

    # WHEN / THENs
    assert get_root_title_from_road(root_title()) == root_title()
    assert get_root_title_from_road(casa_road) == root_title()
    assert get_root_title_from_road(bloomers_road) == root_title()
    assert get_root_title_from_road(roses_road) == casa_str


def test_road_get_parent_road_ReturnsObj_Scenario0():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_title()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_road(root_title(), x_s) == ""
    assert get_parent_road(casa_road, x_s) == root_title()
    assert get_parent_road(bloomers_road, x_s) == casa_road
    assert get_parent_road(roses_road, x_s) == bloomers_road


def test_road_get_parent_road_ReturnsObj_Scenario1():
    # ESTABLISH
    x_s = "/"
    casa_str = "casa"
    casa_road = f"{root_title()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_road(root_title(), x_s) == ""
    assert get_parent_road(casa_road, x_s) == root_title()
    assert get_parent_road(bloomers_road, x_s) == casa_road
    assert get_parent_road(roses_road, x_s) == bloomers_road


def test_road_create_road_without_root_title_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_title()}{x_s}{casa_str}"
    casa_without_root_road = f"{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_title()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_without_root_road = f"{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_title()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_without_root_road = f"{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THENs
    assert create_road_without_root_title(road=root_title()) == x_s
    assert create_road_without_root_title(road=casa_road) == casa_without_root_road
    assert (
        create_road_without_root_title(road=bloomers_road) == bloomers_without_root_road
    )
    assert create_road_without_root_title(road=roses_road) == roses_without_root_road
    road_without_title = create_road_without_root_title(road=roses_road)
    with pytest_raises(Exception) as excinfo:
        create_road_without_root_title(road=road_without_title)
    assert (
        str(excinfo.value)
        == f"Cannot create_road_without_root_title of '{road_without_title}' because it has no root title."
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
    old_seasons_road = f"{root_title()}{x_s}casa{x_s}seasons"
    old_dict_x = {old_seasons_road: TempTestingObj(old_seasons_road)}
    assert old_dict_x.get(old_seasons_road) is not None

    # WHEN
    new_seasons_road = f"{root_title()}{x_s}casa{x_s}kookies"
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
    nation_road = f"{root_title()}{x_s}{nation_str}"
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
        root_title(),
    ]
    assert x_roads == texas_ancestor_roads

    # WHEN
    assert get_ancestor_roads(None) == []
    assert get_ancestor_roads("") == [""]
    assert get_ancestor_roads(root_title()) == [root_title()]


def test_road_get_forefather_roads_ReturnsAncestorRoadUnitsWithoutClean():
    # ESTABLISH
    x_s = default_bridge_if_None()
    nation_str = "nation-state"
    nation_road = f"{root_title()}{x_s}{nation_str}"
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
        root_title(): None,
    }
    assert x_roads == texas_forefather_roads


def test_road_get_default_fisc_title_ReturnsObj():
    assert root_title() == "ZZ"


def test_road_create_road_from_titles_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    root_list = get_all_road_titles(root_title())
    casa_str = "casa"
    casa_road = f"{root_title()}{x_s}{casa_str}"
    casa_list = get_all_road_titles(casa_road)
    bloomers_str = "bloomers"
    bloomers_road = f"{root_title()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_list = get_all_road_titles(bloomers_road)
    roses_str = "roses"
    roses_road = f"{root_title()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_list = get_all_road_titles(roses_road)

    # WHEN / THEN
    assert root_title() == create_road_from_titles(root_list)
    assert casa_road == create_road_from_titles(casa_list)
    assert bloomers_road == create_road_from_titles(bloomers_list)
    assert roses_road == create_road_from_titles(roses_list)


def test_road_create_road_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_title()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_title()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_road = f"{root_title()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THEN
    assert root_title() == create_road(None, root_title())
    assert root_title() == create_road("", root_title())
    assert casa_road == create_road(root_title(), casa_str)
    assert bloomers_road == create_road(casa_road, bloomers_str)
    assert roses_road == create_road(bloomers_road, roses_str)
    assert roses_road == create_road(roses_road, None)


def test_is_titleunit_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()

    # WHEN / THEN
    assert is_titleunit("", x_bridge=x_s) is False
    assert is_titleunit("casa", x_bridge=x_s)
    assert not is_titleunit(f"ZZ{x_s}casa", x_s)
    assert not is_titleunit(RoadUnit(f"ZZ{x_s}casa"), x_s)
    assert is_titleunit(RoadUnit("ZZ"), x_s)


def test_get_diff_road_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_road = f"{root_title()}{x_s}{casa_str}"
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
    usa_road = f"{root_title()}{x_s}Nation-States{x_s}{usa_str}"
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
    gen_casa_road = create_road(root_title(), casa_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_casa_road = f"{root_title()}{semicolon_bridge}{casa_str}"
    assert semicolon_bridge == ";"
    assert gen_casa_road == semicolon_bridge_casa_road

    # WHEN
    slash_bridge = "/"
    gen_casa_road = replace_bridge(
        gen_casa_road, old_bridge=semicolon_bridge, new_bridge=slash_bridge
    )

    # THEN
    slash_bridge_casa_road = f"{root_title()}{slash_bridge}{casa_str}"
    assert gen_casa_road == slash_bridge_casa_road


def test_replace_bridge_CorrectlyRaisesError():
    # ESTABLISH
    cooker_str = "cooker/cleaner"
    gen_cooker_road = create_road(root_title(), cooker_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_cooker_road = f"{root_title()}{semicolon_bridge}{cooker_str}"
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


def test_validate_titleunit_RaisesErrorWhenNotTitleUnit():
    # ESTABLISH
    bob_str = "Bob, Tom"
    slash_str = "/"
    assert bob_str == validate_titleunit(bob_str, x_bridge=slash_str)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_titleunit(bob_str, x_bridge=comma_str)
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to be a TitleUnit. Cannot contain bridge: '{comma_str}'"
    )


def test_validate_titleunit_RaisesErrorWhenTitleUnit():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Tom"
    assert bob_str == validate_titleunit(
        bob_str, x_bridge=slash_str, not_titleunit_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_titleunit(
            bob_str, x_bridge=comma_str, not_titleunit_required=True
        )
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to not be a TitleUnit. Must contain bridge: '{comma_str}'"
    )


def test_roadunit_valid_dir_path_ReturnsObj_simple_bridge():
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


def test_roadunit_valid_dir_path_ReturnsObj_complicated_bridge():
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
