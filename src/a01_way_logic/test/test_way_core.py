from src.a01_way_logic.way import (
    WayStr,
    to_way,
    get_default_fisc_way,
    create_way,
    create_way_from_tags,
    rebuild_way,
    is_sub_way,
    get_all_way_tags,
    get_terminus_tag,
    find_replace_way_key_dict,
    get_parent_way,
    get_root_tag_from_way,
    get_ancestor_ways,
    get_forefather_ways,
    get_default_fisc_tag,
    get_default_fisc_way as root_way,
    is_heir_way,
    default_bridge_if_None,
    replace_bridge,
    validate_tagstr,
    waystr_valid_dir_path,
    all_waystrs_between,
    is_tagstr,
)
from pytest import raises as pytest_raises
from dataclasses import dataclass
from platform import system as platform_system


def test_to_way_ReturnsObj_WithDefault_bridge():
    # ESTABLISH
    x_tag = "run"
    x_bridge = default_bridge_if_None()

    # WHEN / THEN
    assert to_way(x_tag) == f"{x_bridge}{x_tag}"
    assert to_way(f"{x_bridge}{x_tag}") == f"{x_bridge}{x_tag}"
    assert to_way(f"{x_bridge}{x_bridge}{x_tag}") == f"{x_bridge}{x_bridge}{x_tag}"
    assert to_way(x_bridge) == x_bridge
    assert to_way(None) == x_bridge


def test_to_way_ReturnsObj_WithParameter_bridge():
    # ESTABLISH
    x_tag = "run"
    slash_bridge = "/"

    # WHEN / THEN
    assert to_way(x_tag, slash_bridge) == f"{slash_bridge}{x_tag}"
    assert to_way(f"{slash_bridge}{x_tag}", slash_bridge) == f"{slash_bridge}{x_tag}"
    assert (
        to_way(f"{slash_bridge}{slash_bridge}{x_tag}", slash_bridge)
        == f"{slash_bridge}{slash_bridge}{x_tag}"
    )
    assert to_way(slash_bridge, slash_bridge) == slash_bridge
    assert to_way(None, slash_bridge) == slash_bridge


def test_get_default_fisc_tag_ReturnsObj():
    assert get_default_fisc_tag() == "ZZ"


def test_get_default_fisc_way_ReturnsObj():
    # ESTABLISH
    default_bridge = default_bridge_if_None()
    default_root_tag = get_default_fisc_tag()
    slash_bridge = "/"

    # WHEN / THEN
    assert get_default_fisc_way() == to_way(default_root_tag)
    assert get_default_fisc_way(slash_bridge) == to_way(default_root_tag, slash_bridge)


def test_create_way_Scenario0_RaisesErrorIfBridgeNotAtPostionZeroOf_parent_way():
    # ESTABLISH
    rose_str = "rose"
    semicolon_bridge = ";"
    semicolon_bridge_rose_way = f"{semicolon_bridge}{rose_str}"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_way(
            "ZZ", rose_str, auto_add_first_bridge=False
        ) == semicolon_bridge_rose_way
    exception_str = (
        f"Parent way must have bridge '{semicolon_bridge}' at position 0 in string"
    )
    assert str(excinfo.value) == exception_str


def test_create_way_Scenario1_DoesNotRaiseError():
    # ESTABLISH
    rose_str = "rose"

    # WHEN / THEN
    assert create_way("ZZ", rose_str)


def test_create_way_ReturnsObj_Scenario3():
    # ESTABLISH
    rose_str = "rose"
    semicolon_bridge = ";"
    assert semicolon_bridge == default_bridge_if_None()
    semicolon_bridge_rose_way = f"{root_way()}{semicolon_bridge}{rose_str}"

    # WHEN / THEN
    assert create_way(root_way(), rose_str) == semicolon_bridge_rose_way


def test_create_way_ReturnsObj_Scenario4():
    # ESTABLISH
    rose_str = "rose"
    slash_bridge = "/"
    slash_bridge_rose_way = (
        f"{slash_bridge}{get_default_fisc_tag()}{slash_bridge}{rose_str}"
    )

    # WHEN
    generated_rose_way = create_way(
        get_default_fisc_tag(), rose_str, bridge=slash_bridge
    )
    # THEN
    assert generated_rose_way == slash_bridge_rose_way


def test_way_create_way_ReturnsObj_Scenario5():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_way = f"{root_way()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_way = f"{root_way()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_way = f"{root_way()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THEN
    assert create_way(None, get_default_fisc_tag()) == root_way()
    assert create_way("", get_default_fisc_tag()) == root_way()
    assert create_way(root_way(), casa_str) == casa_way
    assert create_way(casa_way, bloomers_str) == bloomers_way
    assert create_way(bloomers_way, roses_str) == roses_way
    assert create_way(roses_way, None) == roses_way


def test_way_is_sub_way_correctlyReturnsBool():
    # WHEN
    casa_str = "casa"
    casa_way = f"{root_way()}{default_bridge_if_None()}{casa_str}"
    cleaning_str = "cleaning"
    cleaning_way = f"{casa_way}{default_bridge_if_None()}{cleaning_str}"
    laundrys_str = "laundrys"
    laundrys_way = f"{cleaning_way}{default_bridge_if_None()}{laundrys_str}"
    print(f"{cleaning_way=}")
    print(f"{laundrys_way=}")

    # WHEN / THEN
    assert is_sub_way(cleaning_way, cleaning_way)
    assert is_sub_way(laundrys_way, cleaning_way)
    assert is_sub_way(cleaning_way, laundrys_way) is False


def test_way_rebuild_way_ReturnsCorrectWayStr():
    # ESTABLISH
    casa_str = "casa"
    casa_way = create_way(root_way(), casa_str)
    bloomers_str = "bloomers"
    bloomers_way = create_way(casa_way, bloomers_str)
    greenery_str = "greenery"
    greenery_way = create_way(casa_way, greenery_str)
    roses_str = "roses"
    old_roses_way = create_way(bloomers_way, roses_str)
    new_roses_way = create_way(greenery_way, roses_str)

    print(f"{rebuild_way(old_roses_way, bloomers_way, greenery_way)}")

    # WHEN / THEN
    assert rebuild_way(bloomers_way, bloomers_way, bloomers_way) == bloomers_way
    assert rebuild_way(old_roses_way, bloomers_way, greenery_way) == new_roses_way
    assert rebuild_way(old_roses_way, "random_str", greenery_way) == old_roses_way


def test_way_get_all_way_tags_ReturnsTagStrs():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_way = f"{root_way()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_way = f"{root_way()}{x_s}{casa_str}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_way = f"{root_way()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"

    # WHEN / THENs
    root_list = [get_default_fisc_tag()]
    assert get_all_way_tags(way=root_way()) == root_list
    casa_list = [get_default_fisc_tag(), casa_str]
    assert get_all_way_tags(way=casa_way) == casa_list
    bloomers_list = [get_default_fisc_tag(), casa_str, bloomers_str]
    assert get_all_way_tags(way=bloomers_way) == bloomers_list
    roses_list = [get_default_fisc_tag(), casa_str, bloomers_str, roses_str]
    assert get_all_way_tags(way=roses_way) == roses_list


def test_way_get_terminus_tag_ReturnsTagStr():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_way = f"{root_way()}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_way = f"{casa_way}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_way = f"{bloomers_way}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_terminus_tag(way=root_way()) == get_default_fisc_tag()
    assert get_terminus_tag(way=casa_way) == casa_str
    assert get_terminus_tag(way=bloomers_way) == bloomers_str
    assert get_terminus_tag(way=roses_way) == roses_str


def test_way_get_terminus_tag_ReturnsTagStrWhenNonDefaultbridge():
    # ESTABLISH
    casa_str = "casa"
    bloomers_str = "bloomers"
    roses_str = "roses"
    slash_str = "/"
    slash_casa_way = f"{slash_str}{get_default_fisc_tag()}{slash_str}{casa_str}"
    slash_bloomers_way = f"{slash_str}{slash_casa_way}{slash_str}{bloomers_str}"
    slash_roses_way = f"{slash_str}{slash_bloomers_way}{slash_str}{roses_str}"

    # WHEN / THENs
    assert get_terminus_tag(slash_casa_way, slash_str) == casa_str
    assert get_terminus_tag(slash_bloomers_way, slash_str) == bloomers_str
    assert get_terminus_tag(slash_roses_way, slash_str) == roses_str


def test_way_get_root_tag_from_way_ReturnsTagStr():
    # ESTABLISH
    casa_str = "casa"
    casa_way = create_way(root_way(), casa_str)
    bloomers_str = "bloomers"
    bloomers_way = create_way(casa_way, bloomers_str)
    roses_str = "roses"
    roses_way = create_way(casa_str, roses_str)

    # WHEN / THENs
    assert get_root_tag_from_way(root_way()) == get_default_fisc_tag()
    assert get_root_tag_from_way(casa_way) == get_default_fisc_tag()
    assert get_root_tag_from_way(bloomers_way) == get_default_fisc_tag()
    assert get_root_tag_from_way(roses_way) == casa_str


def test_way_get_parent_way_ReturnsObj_Scenario0():
    # ESTABLISH
    x_s = default_bridge_if_None()
    root_fisc_way = f"{x_s}{get_default_fisc_tag()}"
    casa_str = "casa"
    casa_way = f"{root_fisc_way}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_way = f"{casa_way}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_way = f"{bloomers_way}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_way(root_way(), x_s) == ""
    assert get_parent_way(casa_way, x_s) == root_fisc_way
    assert get_parent_way(bloomers_way, x_s) == casa_way
    assert get_parent_way(roses_way, x_s) == bloomers_way


def test_way_get_parent_way_ReturnsObj_Scenario1():
    # ESTABLISH
    x_s = "/"
    root_fisc_way = f"{x_s}{get_default_fisc_tag()}"
    casa_str = "casa"
    casa_way = f"{root_fisc_way}{x_s}{casa_str}"
    bloomers_str = "bloomers"
    bloomers_way = f"{casa_way}{x_s}{bloomers_str}"
    roses_str = "roses"
    roses_way = f"{bloomers_way}{x_s}{roses_str}"

    # WHEN / THENs
    assert get_parent_way(root_fisc_way, x_s) == ""
    assert get_parent_way(casa_way, x_s) == root_fisc_way
    assert get_parent_way(bloomers_way, x_s) == casa_way
    assert get_parent_way(roses_way, x_s) == bloomers_way


@dataclass
class TempTestingObj:
    x_way: WayStr = ""

    def find_replace_way(self, old_way, new_way):
        self.x_way = rebuild_way(self.x_way, old_way=old_way, new_way=new_way)

    def get_obj_key(self) -> WayStr:
        return self.x_way


def test_way_find_replace_way_key_dict_ReturnsCorrectDict_Scenario1():
    # ESTABLISH
    x_s = default_bridge_if_None()
    old_seasons_way = f"{root_way()}{x_s}casa{x_s}seasons"
    old_dict_x = {old_seasons_way: TempTestingObj(old_seasons_way)}
    assert old_dict_x.get(old_seasons_way) is not None

    # WHEN
    new_seasons_way = f"{root_way()}{x_s}casa{x_s}kookies"
    new_dict_x = find_replace_way_key_dict(
        dict_x=old_dict_x, old_way=old_seasons_way, new_way=new_seasons_way
    )

    # THEN
    assert new_dict_x != {}
    assert len(new_dict_x) == 1
    print(f"{new_dict_x=}")
    assert new_dict_x.get(new_seasons_way) is not None
    assert new_dict_x.get(old_seasons_way) is None


def test_way_get_ancestor_ways_ReturnsObj_Scenario0_default_bridge():
    # ESTABLISH
    x_s = default_bridge_if_None()
    nation_str = "nation-state"
    nation_way = f"{root_way()}{x_s}{nation_str}"
    usa_str = "USA"
    usa_way = f"{nation_way}{x_s}{usa_str}"
    texas_str = "Texas"
    texas_way = f"{usa_way}{x_s}{texas_str}"

    # WHEN
    texas_anc_ways = get_ancestor_ways(way=texas_way)

    # THEN
    print(f"     {texas_way=}")
    print(f"{texas_anc_ways=}")
    assert texas_anc_ways is not None
    texas_ancestor_ways = [
        texas_way,
        usa_way,
        nation_way,
        root_way(),
    ]
    assert texas_anc_ways == texas_ancestor_ways

    # WHEN
    assert get_ancestor_ways(None) == []
    assert get_ancestor_ways("") == []
    assert get_ancestor_ways(root_way()) == [root_way()]


def test_way_get_ancestor_ways_ReturnsObj_Scenario1_nondefault_bridge():
    # ESTABLISH
    x_s = "/"
    root_fisc_way = f"{x_s}accord23"
    nation_str = "nation-state"
    nation_way = f"{root_fisc_way}{x_s}{nation_str}"
    usa_str = "USA"
    usa_way = f"{nation_way}{x_s}{usa_str}"
    texas_str = "Texas"
    texas_way = f"{usa_way}{x_s}{texas_str}"

    # WHEN
    texas_anc_ways = get_ancestor_ways(way=texas_way, bridge=x_s)

    # THEN
    print(f"     {texas_way=}")
    print(f"{texas_anc_ways=}")
    assert texas_anc_ways is not None
    texas_ancestor_ways = [
        texas_way,
        usa_way,
        nation_way,
        root_fisc_way,
    ]
    assert texas_anc_ways == texas_ancestor_ways


def test_way_get_forefather_ways_ReturnsAncestorWayStrsWithoutClean():
    # ESTABLISH
    x_s = default_bridge_if_None()
    nation_str = "nation-state"
    nation_way = f"{root_way()}{x_s}{nation_str}"
    usa_str = "USA"
    usa_way = f"{nation_way}{x_s}{usa_str}"
    texas_str = "Texas"
    texas_way = f"{usa_way}{x_s}{texas_str}"

    # WHEN
    x_ways = get_forefather_ways(way=texas_way)

    # THEN
    print(f"{texas_way=}")
    assert x_ways is not None
    texas_forefather_ways = {
        nation_way: None,
        usa_way: None,
        root_way(): None,
    }
    assert x_ways == texas_forefather_ways


def test_way_get_default_fisc_tag_ReturnsObj():
    assert get_default_fisc_tag() == "ZZ"


def test_way_create_way_from_tags_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    root_list = get_all_way_tags(root_way())
    casa_str = "casa"
    casa_way = f"{root_way()}{x_s}{casa_str}"
    casa_list = get_all_way_tags(casa_way)
    bloomers_str = "bloomers"
    bloomers_way = f"{root_way()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_list = get_all_way_tags(bloomers_way)
    roses_str = "roses"
    roses_way = f"{root_way()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_list = get_all_way_tags(roses_way)

    # WHEN / THEN
    assert root_way() == create_way_from_tags(root_list)
    assert casa_way == create_way_from_tags(casa_list)
    assert bloomers_way == create_way_from_tags(bloomers_list)
    assert roses_way == create_way_from_tags(roses_list)


def test_is_tagstr_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()

    # WHEN / THEN
    assert is_tagstr("", x_bridge=x_s) is False
    assert is_tagstr("casa", x_bridge=x_s)
    assert not is_tagstr(f"ZZ{x_s}casa", x_s)
    assert not is_tagstr(WayStr(f"ZZ{x_s}casa"), x_s)
    assert is_tagstr(WayStr("ZZ"), x_s)


def test_is_heir_way_CorrectlyIdentifiesHeirs():
    # ESTABLISH
    x_s = default_bridge_if_None()
    usa_str = "USA"
    usa_way = f"{root_way()}{x_s}Nation-States{x_s}{usa_str}"
    texas_str = "Texas"
    texas_way = f"{usa_way}{x_s}{texas_str}"
    # earth_str = "earth"
    # earth_way = f"{earth_str}"
    # sea_str = "sea"
    # sea_way = f"{earth_way}{x_s}{sea_str}"
    # seaside_str = "seaside"
    # seaside_way = f"{earth_way}{x_s}{seaside_str}"

    # WHEN / THEN
    assert is_heir_way(src=usa_way, heir=usa_way)
    assert is_heir_way(src=usa_way, heir=texas_way)
    assert is_heir_way(f"earth{x_s}sea", f"earth{x_s}seaside{x_s}beach") is False
    assert is_heir_way(src=f"earth{x_s}sea", heir=f"earth{x_s}seaside") is False


def test_replace_bridge_ReturnsNewObj():
    # ESTABLISH
    casa_str = "casa"
    root_tag = get_default_fisc_tag()
    gen_casa_way = create_way(root_tag, casa_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_casa_way = (
        f"{semicolon_bridge}{root_tag}{semicolon_bridge}{casa_str}"
    )
    assert semicolon_bridge == ";"
    assert gen_casa_way == semicolon_bridge_casa_way

    # WHEN
    slash_bridge = "/"
    gen_casa_way = replace_bridge(
        gen_casa_way, old_bridge=semicolon_bridge, new_bridge=slash_bridge
    )

    # THEN
    slash_bridge_casa_way = f"{slash_bridge}{root_tag}{slash_bridge}{casa_str}"
    assert gen_casa_way == slash_bridge_casa_way


def test_replace_bridge_CorrectlyRaisesError():
    # ESTABLISH
    cooker_str = "cooker/cleaner"
    gen_cooker_way = create_way(root_way(), cooker_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_cooker_way = f"{root_way()}{semicolon_bridge}{cooker_str}"
    assert semicolon_bridge == ";"
    assert gen_cooker_way == semicolon_bridge_cooker_way

    # WHEN / THEN
    slash_bridge = "/"
    with pytest_raises(Exception) as excinfo:
        gen_cooker_way = replace_bridge(
            gen_cooker_way,
            old_bridge=semicolon_bridge,
            new_bridge=slash_bridge,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_bridge '{semicolon_bridge}' with '{slash_bridge}' because the new one exists in way '{gen_cooker_way}'."
    )


def test_replace_bridge_WhenNewbridgeIsFirstInWayStrRaisesError():
    # ESTABLISH
    cooker_str = "/cooker"
    cleaner_str = "cleaner"
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_cooker_way = f"{cooker_str}{semicolon_bridge}{cleaner_str}"
    assert semicolon_bridge == ";"

    # WHEN / THEN
    slash_bridge = "/"
    with pytest_raises(Exception) as excinfo:
        semicolon_bridge_cooker_way = replace_bridge(
            semicolon_bridge_cooker_way,
            old_bridge=semicolon_bridge,
            new_bridge=slash_bridge,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_bridge '{semicolon_bridge}' with '{slash_bridge}' because the new one exists in way '{semicolon_bridge_cooker_way}'."
    )


def test_validate_tagstr_RaisesErrorWhenNotTagStr():
    # ESTABLISH
    bob_str = "Bob, Tom"
    slash_str = "/"
    assert bob_str == validate_tagstr(bob_str, x_bridge=slash_str)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_tagstr(bob_str, x_bridge=comma_str)
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to be a TagStr. Cannot contain bridge: '{comma_str}'"
    )


def test_validate_tagstr_RaisesErrorWhenTagStr():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Tom"
    assert bob_str == validate_tagstr(
        bob_str, x_bridge=slash_str, not_tagstr_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_tagstr(
            bob_str, x_bridge=comma_str, not_tagstr_required=True
        )
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to not be a TagStr. Must contain bridge: '{comma_str}'"
    )


def test_waystr_valid_dir_path_ReturnsObj_simple_bridge():
    # ESTABLISH
    comma_str = ","
    # WHEN / THEN
    assert waystr_valid_dir_path(",run", bridge=comma_str)
    assert waystr_valid_dir_path(",run,sport", bridge=comma_str)
    print(f"{platform_system()=}")
    sport_question_valid_bool = waystr_valid_dir_path("run,sport?", comma_str)
    assert (
        platform_system() == "Windows" and sport_question_valid_bool is False
    ) or platform_system() == "Linux"


def test_waystr_valid_dir_path_ReturnsObj_complicated_bridge():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run,"
    lap_str = "lap"
    sport_way = create_way(sport_str, bridge=question_str)
    print(f"{sport_way=}")
    run_way = create_way(sport_way, run_str, bridge=question_str)
    lap_way = create_way(run_way, lap_str, bridge=question_str)
    assert lap_way == f"{sport_way}?{run_str}?{lap_str}"

    assert waystr_valid_dir_path(sport_way, bridge=question_str)
    assert waystr_valid_dir_path(run_way, bridge=question_str)
    assert waystr_valid_dir_path(lap_way, bridge=question_str)
    assert (
        platform_system() == "Windows"
        and waystr_valid_dir_path(lap_way, bridge=",") is False
    ) or platform_system() == "Linux"


def test_waystr_valid_dir_path_ReturnsObjWhereSlashNotbridgeEdgeCases():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run/swim"
    lap_str = "lap"
    sport_way = create_way(sport_str, bridge=question_str)
    run_way = create_way(sport_way, run_str, bridge=question_str)
    lap_way = create_way(run_way, lap_str, bridge=question_str)
    assert lap_way == f"{sport_way}?{run_str}?{lap_str}"

    assert waystr_valid_dir_path(sport_way, bridge=question_str)
    assert waystr_valid_dir_path(run_way, bridge=question_str) is False
    assert waystr_valid_dir_path(lap_way, bridge=question_str) is False
    assert waystr_valid_dir_path(lap_way, bridge=",") is False


def test_all_waystrs_between_ReturnsObj():
    casa_str = "casa"
    sport_str = "sport"
    run_str = "run/swim"
    lap_str = "lap"
    sport_way = create_way(casa_str, sport_str)
    run_way = create_way(sport_way, run_str)
    lap_way = create_way(run_way, lap_str)

    assert all_waystrs_between(sport_way, sport_way) == [sport_way]
    assert all_waystrs_between(sport_way, run_way) == [sport_way, run_way]
    assert all_waystrs_between(sport_way, lap_way) == [
        sport_way,
        run_way,
        lap_way,
    ]
