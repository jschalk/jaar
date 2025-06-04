from dataclasses import dataclass
from platform import system as platform_system
from pytest import raises as pytest_raises
from src.a01_term_logic.term import default_bridge_if_None
from src.a01_term_logic.way import (
    WayTerm,
    all_wayterms_between,
    create_way,
    create_way_from_labels,
    find_replace_way_key_dict,
    get_all_way_labels,
    get_ancestor_ways,
    get_default_fisc_label,
    get_default_fisc_way,
    get_default_fisc_way as root_way,
    get_forefather_ways,
    get_parent_way,
    get_root_label_from_way,
    get_tail_label,
    is_heir_way,
    is_labelterm,
    is_sub_way,
    rebuild_way,
    replace_bridge,
    to_way,
    validate_labelterm,
    wayterm_valid_dir_path,
)


def test_to_way_ReturnsObj_WithDefault_bridge():
    # ESTABLISH
    x_label = "run"
    x_bridge = default_bridge_if_None()

    # WHEN / THEN
    assert to_way(x_label) == f"{x_bridge}{x_label}{x_bridge}"
    assert to_way(f"{x_bridge}{x_label}") == f"{x_bridge}{x_label}{x_bridge}"
    two_bridge_in_front_one_back = f"{x_bridge}{x_bridge}{x_label}{x_bridge}"
    assert to_way(f"{x_bridge}{x_bridge}{x_label}") == two_bridge_in_front_one_back
    assert to_way(x_bridge) == x_bridge
    assert to_way("", x_bridge) == x_bridge
    assert to_way(None) == x_bridge


def test_to_way_ReturnsObj_WithParameter_bridge():
    # ESTABLISH
    x_label = "run"
    s_bridge = "/"

    # WHEN / THEN
    assert to_way(x_label, s_bridge) == f"{s_bridge}{x_label}{s_bridge}"
    assert to_way(f"{s_bridge}{x_label}", s_bridge) == f"{s_bridge}{x_label}{s_bridge}"
    assert (
        to_way(f"{s_bridge}{s_bridge}{x_label}", s_bridge)
        == f"{s_bridge}{s_bridge}{x_label}{s_bridge}"
    )
    assert to_way(s_bridge, s_bridge) == s_bridge
    assert to_way(None, s_bridge) == s_bridge


def test_get_default_fisc_label_ReturnsObj():
    assert get_default_fisc_label() == "ZZ"


def test_get_default_fisc_way_ReturnsObj():
    # ESTABLISH
    default_bridge = default_bridge_if_None()
    default_root_label = get_default_fisc_label()
    slash_bridge = "/"

    # WHEN / THEN
    assert get_default_fisc_way() == to_way(default_root_label)
    assert get_default_fisc_way(slash_bridge) == to_way(
        default_root_label, slash_bridge
    )


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
    semicolon_bridge_rose_way = f"{root_way()}{rose_str}{semicolon_bridge}"
    print(f"{semicolon_bridge_rose_way=}")

    # WHEN / THEN
    assert create_way(root_way(), rose_str) == semicolon_bridge_rose_way


def test_create_way_ReturnsObj_Scenario4():
    # ESTABLISH
    rose_str = "rose"
    slash_bridge = "/"
    slash_bridge_rose_way = f"{slash_bridge}{get_default_fisc_label()}{slash_bridge}{rose_str}{slash_bridge}"

    # WHEN
    generated_rose_way = create_way(
        get_default_fisc_label(), rose_str, bridge=slash_bridge
    )
    # THEN
    assert generated_rose_way == slash_bridge_rose_way


def test_way_create_way_ReturnsObj_Scenario5():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_way = f"{root_way()}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_way = f"{root_way()}{casa_str}{x_s}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_way = f"{root_way()}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"

    # WHEN / THEN
    assert create_way(None, get_default_fisc_label()) == root_way()
    assert create_way("", get_default_fisc_label()) == root_way()
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


def test_way_rebuild_way_ReturnsCorrectWayTerm():
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


def test_way_get_all_way_labels_ReturnsLabelTerms():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_way = f"{root_way()}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_way = f"{root_way()}{casa_str}{x_s}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_way = f"{root_way()}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"

    # WHEN / THENs
    root_list = [get_default_fisc_label()]
    assert get_all_way_labels(way=root_way()) == root_list
    casa_list = [get_default_fisc_label(), casa_str]
    assert get_all_way_labels(way=casa_way) == casa_list
    bloomers_list = [get_default_fisc_label(), casa_str, bloomers_str]
    assert get_all_way_labels(way=bloomers_way) == bloomers_list
    roses_list = [get_default_fisc_label(), casa_str, bloomers_str, roses_str]
    assert get_all_way_labels(way=roses_way) == roses_list


def test_way_get_tail_label_ReturnsLabelTerm():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_way = f"{root_way()}{x_s}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_way = f"{casa_way}{x_s}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_way = f"{bloomers_way}{x_s}{roses_str}{x_s}"

    # WHEN / THENs
    assert get_tail_label(way=root_way()) == get_default_fisc_label()
    assert get_tail_label(way=casa_way) == casa_str
    assert get_tail_label(way=bloomers_way) == bloomers_str
    assert get_tail_label(way=roses_way) == roses_str
    assert get_tail_label(way="") == ""


def test_way_get_tail_label_ReturnsLabelTermWhenNonDefaultbridge():
    # ESTABLISH
    casa_str = "casa"
    bloomers_str = "bloomers"
    roses_str = "roses"
    slash_str = "/"
    slash_casa_way = (
        f"{slash_str}{get_default_fisc_label()}{slash_str}{casa_str}{slash_str}"
    )
    slash_bloomers_way = f"{slash_casa_way}{bloomers_str}{slash_str}"
    slash_roses_way = f"{slash_bloomers_way}{roses_str}{slash_str}"

    # WHEN / THENs
    assert get_tail_label(slash_casa_way, slash_str) == casa_str
    assert get_tail_label(slash_bloomers_way, slash_str) == bloomers_str
    assert get_tail_label(slash_roses_way, slash_str) == roses_str


def test_way_get_root_label_from_way_ReturnsLabelTerm():
    # ESTABLISH
    casa_str = "casa"
    casa_way = create_way(root_way(), casa_str)
    bloomers_str = "bloomers"
    bloomers_way = create_way(casa_way, bloomers_str)
    roses_str = "roses"
    roses_way = create_way(casa_str, roses_str)

    # WHEN / THENs
    assert get_root_label_from_way(root_way()) == get_default_fisc_label()
    assert get_root_label_from_way(casa_way) == get_default_fisc_label()
    assert get_root_label_from_way(bloomers_way) == get_default_fisc_label()
    assert get_root_label_from_way(roses_way) == casa_str


def test_way_get_parent_way_ReturnsObj_Scenario0():
    # ESTABLISH
    x_s = default_bridge_if_None()
    root_fisc_way = f"{x_s}{get_default_fisc_label()}{x_s}"
    casa_str = "casa"
    casa_way = f"{root_fisc_way}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_way = f"{casa_way}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_way = f"{bloomers_way}{roses_str}{x_s}"

    # WHEN / THENs
    assert get_parent_way(root_way(), x_s) == ""
    assert get_parent_way(casa_way, x_s) == root_fisc_way
    assert get_parent_way(bloomers_way, x_s) == casa_way
    assert get_parent_way(roses_way, x_s) == bloomers_way


def test_way_get_parent_way_ReturnsObj_Scenario1():
    # ESTABLISH
    x_s = "/"
    root_fisc_way = f"{x_s}{get_default_fisc_label()}{x_s}"
    casa_str = "casa"
    casa_way = f"{root_fisc_way}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_way = f"{casa_way}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_way = f"{bloomers_way}{roses_str}{x_s}"

    # WHEN / THENs
    assert get_parent_way(root_fisc_way, x_s) == ""
    assert get_parent_way(casa_way, x_s) == root_fisc_way
    assert get_parent_way(bloomers_way, x_s) == casa_way
    assert get_parent_way(roses_way, x_s) == bloomers_way


@dataclass
class TempTestingObj:
    x_way: WayTerm = ""

    def find_replace_way(self, old_way, new_way):
        self.x_way = rebuild_way(self.x_way, old_way=old_way, new_way=new_way)

    def get_obj_key(self) -> WayTerm:
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
    nation_str = "nation"
    nation_way = f"{root_way()}{nation_str}{x_s}"
    usa_str = "USA"
    usa_way = f"{nation_way}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_way = f"{usa_way}{texas_str}{x_s}"

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
    root_fisc_way = f"{x_s}accord23{x_s}"
    nation_str = "nation"
    nation_way = f"{root_fisc_way}{nation_str}{x_s}"
    usa_str = "USA"
    usa_way = f"{nation_way}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_way = f"{usa_way}{texas_str}{x_s}"

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


def test_way_get_forefather_ways_ReturnsAncestorWayTermsWithoutClean():
    # ESTABLISH
    x_s = default_bridge_if_None()
    nation_str = "nation"
    nation_way = f"{root_way()}{nation_str}{x_s}"
    usa_str = "USA"
    usa_way = f"{nation_way}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_way = f"{usa_way}{texas_str}{x_s}"

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


def test_way_get_default_fisc_label_ReturnsObj():
    assert get_default_fisc_label() == "ZZ"


def test_way_create_way_from_labels_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()
    root_list = get_all_way_labels(root_way())
    casa_str = "casa"
    casa_way = f"{root_way()}{casa_str}{x_s}"
    casa_list = get_all_way_labels(casa_way)
    bloomers_str = "bloomers"
    bloomers_way = f"{root_way()}{casa_str}{x_s}{bloomers_str}{x_s}"
    bloomers_list = get_all_way_labels(bloomers_way)
    roses_str = "roses"
    roses_way = f"{root_way()}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"
    roses_list = get_all_way_labels(roses_way)

    # WHEN / THEN
    assert root_way() == create_way_from_labels(root_list)
    assert casa_way == create_way_from_labels(casa_list)
    assert bloomers_way == create_way_from_labels(bloomers_list)
    assert roses_way == create_way_from_labels(roses_list)


def test_is_labelterm_ReturnsObj():
    # ESTABLISH
    x_s = default_bridge_if_None()

    # WHEN / THEN
    assert is_labelterm("", x_bridge=x_s) is False
    assert is_labelterm("casa", x_bridge=x_s)
    assert not is_labelterm(f"ZZ{x_s}casa", x_s)
    assert not is_labelterm(WayTerm(f"ZZ{x_s}casa"), x_s)
    assert is_labelterm(WayTerm("ZZ"), x_s)


def test_is_heir_way_CorrectlyIdentifiesHeirs():
    # ESTABLISH
    x_s = default_bridge_if_None()
    usa_str = "USA"
    usa_way = f"{root_way()}Nation-States{x_s}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_way = f"{usa_way}{texas_str}{x_s}"
    # earth_str = "earth"
    # earth_way = f"{earth_str}"
    # sea_str = "sea"
    # sea_way = f"{earth_way}{x_s}{sea_str}"
    # seaside_str = "seaside"
    # seaside_way = f"{earth_way}{x_s}{seaside_str}"

    # WHEN / THEN
    assert is_heir_way(src=usa_way, heir=usa_way)
    assert is_heir_way(src=usa_way, heir=texas_way)
    assert (
        is_heir_way(f"earth{x_s}sea{x_s}", f"earth{x_s}seaside{x_s}beach{x_s}") is False
    )
    assert (
        is_heir_way(src=f"earth{x_s}sea{x_s}", heir=f"earth{x_s}seaside{x_s}") is False
    )


def test_replace_bridge_ReturnsNewObj():
    # ESTABLISH
    casa_str = "casa"
    root_label = get_default_fisc_label()
    gen_casa_way = create_way(root_label, casa_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_casa_way = (
        f"{semicolon_bridge}{root_label}{semicolon_bridge}{casa_str}{semicolon_bridge}"
    )
    assert semicolon_bridge == ";"
    assert gen_casa_way == semicolon_bridge_casa_way

    # WHEN
    slash_bridge = "/"
    gen_casa_way = replace_bridge(
        gen_casa_way, old_bridge=semicolon_bridge, new_bridge=slash_bridge
    )

    # THEN
    slash_bridge_casa_way = (
        f"{slash_bridge}{root_label}{slash_bridge}{casa_str}{slash_bridge}"
    )
    assert gen_casa_way == slash_bridge_casa_way


def test_replace_bridge_CorrectlyRaisesError():
    # ESTABLISH
    cooker_str = "cooker/cleaner"
    gen_cooker_way = create_way(root_way(), cooker_str)
    semicolon_bridge = default_bridge_if_None()
    semicolon_bridge_cooker_way = f"{root_way()}{cooker_str}{semicolon_bridge}"
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


def test_replace_bridge_WhenNewbridgeIsFirstInWayTermRaisesError():
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


def test_validate_labelterm_RaisesErrorWhenNotLabelTerm():
    # ESTABLISH
    bob_str = "Bob, Tom"
    slash_str = "/"
    assert bob_str == validate_labelterm(bob_str, x_bridge=slash_str)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_labelterm(bob_str, x_bridge=comma_str)
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to be a LabelTerm. Cannot contain bridge: '{comma_str}'"
    )


def test_validate_labelterm_RaisesErrorWhenLabelTerm():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Tom"
    assert bob_str == validate_labelterm(
        bob_str, x_bridge=slash_str, not_labelterm_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_labelterm(
            bob_str, x_bridge=comma_str, not_labelterm_required=True
        )
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to not be a LabelTerm. Must contain bridge: '{comma_str}'"
    )


def test_wayterm_valid_dir_path_ReturnsObj_simple_bridge():
    # ESTABLISH
    comma_str = ","
    # WHEN / THEN
    assert wayterm_valid_dir_path(",run,", bridge=comma_str)
    assert wayterm_valid_dir_path(",run,sport,", bridge=comma_str)
    print(f"{platform_system()=}")
    sport_question_valid_bool = wayterm_valid_dir_path("run,sport?,", comma_str)
    assert (
        platform_system() == "Windows" and sport_question_valid_bool is False
    ) or platform_system() == "Linux"


def test_wayterm_valid_dir_path_ReturnsObj_complicated_bridge():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run,"
    lap_str = "lap"
    sport_way = create_way(sport_str, bridge=question_str)
    print(f"{sport_way=}")
    run_way = create_way(sport_way, run_str, bridge=question_str)
    lap_way = create_way(run_way, lap_str, bridge=question_str)
    assert lap_way == f"{sport_way}{run_str}?{lap_str}?"

    assert wayterm_valid_dir_path(sport_way, bridge=question_str)
    assert wayterm_valid_dir_path(run_way, bridge=question_str)
    assert wayterm_valid_dir_path(lap_way, bridge=question_str)
    assert (
        platform_system() == "Windows"
        and wayterm_valid_dir_path(lap_way, bridge=",") is False
    ) or platform_system() == "Linux"


def test_wayterm_valid_dir_path_ReturnsObjWhereSlashNotbridgeEdgeCases():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run/swim"
    lap_str = "lap"
    sport_way = create_way(sport_str, bridge=question_str)
    run_way = create_way(sport_way, run_str, bridge=question_str)
    lap_way = create_way(run_way, lap_str, bridge=question_str)
    assert lap_way == f"{sport_way}{run_str}?{lap_str}?"

    assert wayterm_valid_dir_path(sport_way, bridge=question_str)
    assert wayterm_valid_dir_path(run_way, bridge=question_str) is False
    assert wayterm_valid_dir_path(lap_way, bridge=question_str) is False
    assert wayterm_valid_dir_path(lap_way, bridge=",") is False


def test_all_wayterms_between_ReturnsObj():
    casa_str = "casa"
    sport_str = "sport"
    run_str = "run/swim"
    lap_str = "lap"
    sport_way = create_way(casa_str, sport_str)
    run_way = create_way(sport_way, run_str)
    lap_way = create_way(run_way, lap_str)

    assert all_wayterms_between(sport_way, sport_way) == [sport_way]
    assert all_wayterms_between(sport_way, run_way) == [sport_way, run_way]
    assert all_wayterms_between(sport_way, lap_way) == [
        sport_way,
        run_way,
        lap_way,
    ]
