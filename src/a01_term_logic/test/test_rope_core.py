from dataclasses import dataclass
from platform import system as platform_system
from pytest import raises as pytest_raises
from src.a01_term_logic.rope import (
    RopeTerm,
    all_ropeterms_between,
    create_rope,
    create_rope_from_labels,
    find_replace_rope_key_dict,
    get_all_rope_labels,
    get_ancestor_ropes,
    get_default_central_label,
    get_default_central_rope,
    get_default_central_rope as root_rope,
    get_forefather_ropes,
    get_parent_rope,
    get_root_label_from_rope,
    get_tail_label,
    is_heir_rope,
    is_labelterm,
    is_sub_rope,
    rebuild_rope,
    replace_knot,
    ropeterm_valid_dir_path,
    to_rope,
    validate_labelterm,
)
from src.a01_term_logic.term import default_knot_if_None


def test_to_rope_ReturnsObj_WithDefault_knot():
    # ESTABLISH
    x_label = "run"
    x_knot = default_knot_if_None()

    # WHEN / THEN
    assert to_rope(x_label) == f"{x_knot}{x_label}{x_knot}"
    assert to_rope(f"{x_knot}{x_label}") == f"{x_knot}{x_label}{x_knot}"
    two_knot_in_front_one_back = f"{x_knot}{x_knot}{x_label}{x_knot}"
    assert to_rope(f"{x_knot}{x_knot}{x_label}") == two_knot_in_front_one_back
    assert to_rope(x_knot) == x_knot
    assert to_rope("", x_knot) == x_knot
    assert to_rope(None) == x_knot


def test_to_rope_ReturnsObj_WithParameter_knot():
    # ESTABLISH
    x_label = "run"
    s_knot = "/"

    # WHEN / THEN
    assert to_rope(x_label, s_knot) == f"{s_knot}{x_label}{s_knot}"
    assert to_rope(f"{s_knot}{x_label}", s_knot) == f"{s_knot}{x_label}{s_knot}"
    assert (
        to_rope(f"{s_knot}{s_knot}{x_label}", s_knot)
        == f"{s_knot}{s_knot}{x_label}{s_knot}"
    )
    assert to_rope(s_knot, s_knot) == s_knot
    assert to_rope(None, s_knot) == s_knot


def test_get_default_central_label_ReturnsObj():
    assert get_default_central_label() == "YY"
    assert get_default_central_label().is_label(default_knot_if_None())


def test_get_default_central_rope_ReturnsObj():
    # ESTABLISH
    default_knot = default_knot_if_None()
    default_root_label = get_default_central_label()
    slash_knot = "/"

    # WHEN / THEN
    assert get_default_central_rope() == to_rope(default_root_label)
    assert get_default_central_rope(slash_knot) == to_rope(
        default_root_label, slash_knot
    )


def test_create_rope_Scenario0_RaisesErrorIfKnotNotAtPostionZeroOf_parent_rope():
    # ESTABLISH
    rose_str = "rose"
    semicolon_knot = ";"
    semicolon_knot_rose_rope = f"{semicolon_knot}{rose_str}"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_rope(
            "ZZ", rose_str, auto_add_first_knot=False
        ) == semicolon_knot_rose_rope
    exception_str = (
        f"Parent rope must have knot '{semicolon_knot}' at position 0 in string"
    )
    assert str(excinfo.value) == exception_str


def test_create_rope_Scenario1_DoesNotRaiseError():
    # ESTABLISH
    rose_str = "rose"

    # WHEN / THEN
    assert create_rope("ZZ", rose_str)


def test_create_rope_ReturnsObj_Scenario3():
    # ESTABLISH
    rose_str = "rose"
    semicolon_knot = ";"
    assert semicolon_knot == default_knot_if_None()
    semicolon_knot_rose_rope = f"{root_rope()}{rose_str}{semicolon_knot}"
    print(f"{semicolon_knot_rose_rope=}")

    # WHEN / THEN
    assert create_rope(root_rope(), rose_str) == semicolon_knot_rose_rope


def test_create_rope_ReturnsObj_Scenario4():
    # ESTABLISH
    rose_str = "rose"
    slash_knot = "/"
    slash_knot_rose_rope = (
        f"{slash_knot}{get_default_central_label()}{slash_knot}{rose_str}{slash_knot}"
    )

    # WHEN
    generated_rose_rope = create_rope(
        get_default_central_label(), rose_str, knot=slash_knot
    )
    # THEN
    assert generated_rose_rope == slash_knot_rose_rope


def test_rope_create_rope_ReturnsObj_Scenario5():
    # ESTABLISH
    x_s = default_knot_if_None()
    casa_str = "casa"
    casa_rope = f"{root_rope()}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_rope()}{casa_str}{x_s}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_rope = f"{root_rope()}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"

    # WHEN / THEN
    assert create_rope(None, get_default_central_label()) == root_rope()
    assert create_rope("", get_default_central_label()) == root_rope()
    assert create_rope(root_rope(), casa_str) == casa_rope
    assert create_rope(casa_rope, bloomers_str) == bloomers_rope
    assert create_rope(bloomers_rope, roses_str) == roses_rope
    assert create_rope(roses_rope, None) == roses_rope


def test_rope_is_sub_rope_ReturnsObj_Scenario0_WhenNone_default_knot_if_None():
    # WHEN
    casa_str = "casa"
    casa_rope = f"{root_rope()}{default_knot_if_None()}{casa_str}"
    cleaning_str = "cleaning"
    cleaning_rope = f"{casa_rope}{default_knot_if_None()}{cleaning_str}"
    laundrys_str = "laundrys"
    laundrys_rope = f"{cleaning_rope}{default_knot_if_None()}{laundrys_str}"
    print(f"{cleaning_rope=}")
    print(f"{laundrys_rope=}")

    # WHEN / THEN
    assert is_sub_rope(cleaning_rope, cleaning_rope)
    assert is_sub_rope(laundrys_rope, cleaning_rope)
    assert is_sub_rope(cleaning_rope, laundrys_rope) is False


def test_rope_is_sub_rope_ReturnsObj_Scenario1_WhenNone_default_knot_if_None():
    # WHEN
    casa_str = "casa"
    slash_str = "/"
    casa_rope = f"{root_rope()}{slash_str}{casa_str}"
    cleaning_str = "cleaning"
    slash_cleaning_rope = f"{casa_rope}{slash_str}{cleaning_str}"
    default_cleaning_rope = f"{casa_rope}{default_knot_if_None()}{cleaning_str}"
    laundrys_str = "laundrys"
    slash_laundrys_rope = f"{slash_cleaning_rope}{slash_str}{laundrys_str}"
    default_laundrys_rope = f"{default_cleaning_rope}{slash_str}{laundrys_str}"
    print(f"{slash_cleaning_rope=}")
    print(f"{slash_laundrys_rope=}")
    print(f"{default_cleaning_rope=}")
    print(f"{default_laundrys_rope=}")

    # WHEN / THEN
    assert is_sub_rope(slash_cleaning_rope, slash_cleaning_rope)
    assert is_sub_rope(slash_laundrys_rope, slash_cleaning_rope)
    assert is_sub_rope(slash_cleaning_rope, slash_laundrys_rope) is False
    assert is_sub_rope(slash_cleaning_rope, default_cleaning_rope) is False
    assert is_sub_rope(slash_laundrys_rope, default_cleaning_rope) is False
    assert is_sub_rope(slash_cleaning_rope, default_laundrys_rope) is False


def test_rope_rebuild_rope_ReturnsCorrectRopeTerm():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_rope(), casa_str)
    bloomers_str = "bloomers"
    bloomers_rope = create_rope(casa_rope, bloomers_str)
    greenery_str = "greenery"
    greenery_rope = create_rope(casa_rope, greenery_str)
    roses_str = "roses"
    old_roses_rope = create_rope(bloomers_rope, roses_str)
    new_roses_rope = create_rope(greenery_rope, roses_str)

    print(f"{rebuild_rope(old_roses_rope, bloomers_rope, greenery_rope)}")

    # WHEN / THEN
    assert rebuild_rope(bloomers_rope, bloomers_rope, bloomers_rope) == bloomers_rope
    assert rebuild_rope(old_roses_rope, bloomers_rope, greenery_rope) == new_roses_rope
    assert rebuild_rope(old_roses_rope, "random_str", greenery_rope) == old_roses_rope


def test_rope_get_all_rope_labels_ReturnsLabelTerms():
    # ESTABLISH
    x_s = default_knot_if_None()
    casa_str = "casa"
    casa_rope = f"{root_rope()}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_rope()}{casa_str}{x_s}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_rope = f"{root_rope()}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"

    # WHEN / THENs
    root_list = [get_default_central_label()]
    assert get_all_rope_labels(rope=root_rope()) == root_list
    casa_list = [get_default_central_label(), casa_str]
    assert get_all_rope_labels(rope=casa_rope) == casa_list
    bloomers_list = [get_default_central_label(), casa_str, bloomers_str]
    assert get_all_rope_labels(rope=bloomers_rope) == bloomers_list
    roses_list = [get_default_central_label(), casa_str, bloomers_str, roses_str]
    assert get_all_rope_labels(rope=roses_rope) == roses_list


def test_rope_get_tail_label_ReturnsLabelTerm():
    # ESTABLISH
    x_s = default_knot_if_None()
    casa_str = "casa"
    casa_rope = f"{root_rope()}{x_s}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{casa_rope}{x_s}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_rope = f"{bloomers_rope}{x_s}{roses_str}{x_s}"

    # WHEN / THENs
    assert get_tail_label(rope=root_rope()) == get_default_central_label()
    assert get_tail_label(rope=casa_rope) == casa_str
    assert get_tail_label(rope=bloomers_rope) == bloomers_str
    assert get_tail_label(rope=roses_rope) == roses_str
    assert get_tail_label(rope="") == ""


def test_rope_get_tail_label_ReturnsLabelTermWhenNonDefaultknot():
    # ESTABLISH
    casa_str = "casa"
    bloomers_str = "bloomers"
    roses_str = "roses"
    slash_str = "/"
    slash_casa_rope = (
        f"{slash_str}{get_default_central_label()}{slash_str}{casa_str}{slash_str}"
    )
    slash_bloomers_rope = f"{slash_casa_rope}{bloomers_str}{slash_str}"
    slash_roses_rope = f"{slash_bloomers_rope}{roses_str}{slash_str}"

    # WHEN / THENs
    assert get_tail_label(slash_casa_rope, slash_str) == casa_str
    assert get_tail_label(slash_bloomers_rope, slash_str) == bloomers_str
    assert get_tail_label(slash_roses_rope, slash_str) == roses_str


def test_rope_get_root_label_from_rope_ReturnsLabelTerm():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_rope(), casa_str)
    bloomers_str = "bloomers"
    bloomers_rope = create_rope(casa_rope, bloomers_str)
    roses_str = "roses"
    roses_rope = create_rope(casa_str, roses_str)

    # WHEN / THENs
    assert get_root_label_from_rope(root_rope()) == get_default_central_label()
    assert get_root_label_from_rope(casa_rope) == get_default_central_label()
    assert get_root_label_from_rope(bloomers_rope) == get_default_central_label()
    assert get_root_label_from_rope(roses_rope) == casa_str


def test_rope_get_parent_rope_ReturnsObj_Scenario0():
    # ESTABLISH
    x_s = default_knot_if_None()
    root_belief_rope = f"{x_s}{get_default_central_label()}{x_s}"
    casa_str = "casa"
    casa_rope = f"{root_belief_rope}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{casa_rope}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_rope = f"{bloomers_rope}{roses_str}{x_s}"

    # WHEN / THENs
    assert get_parent_rope(root_rope(), x_s) == ""
    assert get_parent_rope(casa_rope, x_s) == root_belief_rope
    assert get_parent_rope(bloomers_rope, x_s) == casa_rope
    assert get_parent_rope(roses_rope, x_s) == bloomers_rope


def test_rope_get_parent_rope_ReturnsObj_Scenario1():
    # ESTABLISH
    x_s = "/"
    root_belief_rope = f"{x_s}{get_default_central_label()}{x_s}"
    casa_str = "casa"
    casa_rope = f"{root_belief_rope}{casa_str}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{casa_rope}{bloomers_str}{x_s}"
    roses_str = "roses"
    roses_rope = f"{bloomers_rope}{roses_str}{x_s}"

    # WHEN / THENs
    assert get_parent_rope(root_belief_rope, x_s) == ""
    assert get_parent_rope(casa_rope, x_s) == root_belief_rope
    assert get_parent_rope(bloomers_rope, x_s) == casa_rope
    assert get_parent_rope(roses_rope, x_s) == bloomers_rope


@dataclass
class TempTestingObj:
    x_rope: RopeTerm = ""

    def find_replace_rope(self, old_rope, new_rope):
        self.x_rope = rebuild_rope(self.x_rope, old_rope=old_rope, new_rope=new_rope)

    def get_obj_key(self) -> RopeTerm:
        return self.x_rope


def test_rope_find_replace_rope_key_dict_ReturnsCorrectDict_Scenario1():
    # ESTABLISH
    x_s = default_knot_if_None()
    old_seasons_rope = f"{root_rope()}{x_s}casa{x_s}seasons"
    old_dict_x = {old_seasons_rope: TempTestingObj(old_seasons_rope)}
    assert old_dict_x.get(old_seasons_rope) is not None

    # WHEN
    new_seasons_rope = f"{root_rope()}{x_s}casa{x_s}kookies"
    new_dict_x = find_replace_rope_key_dict(
        dict_x=old_dict_x, old_rope=old_seasons_rope, new_rope=new_seasons_rope
    )

    # THEN
    assert new_dict_x != {}
    assert len(new_dict_x) == 1
    print(f"{new_dict_x=}")
    assert new_dict_x.get(new_seasons_rope) is not None
    assert new_dict_x.get(old_seasons_rope) is None


def test_rope_get_ancestor_ropes_ReturnsObj_Scenario0_default_knot():
    # ESTABLISH
    x_s = default_knot_if_None()
    nation_str = "nation"
    nation_rope = f"{root_rope()}{nation_str}{x_s}"
    usa_str = "USA"
    usa_rope = f"{nation_rope}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_rope = f"{usa_rope}{texas_str}{x_s}"

    # WHEN
    texas_anc_ropes = get_ancestor_ropes(rope=texas_rope)

    # THEN
    print(f"     {texas_rope=}")
    print(f"{texas_anc_ropes=}")
    assert texas_anc_ropes is not None
    texas_ancestor_ropes = [
        texas_rope,
        usa_rope,
        nation_rope,
        root_rope(),
    ]
    assert texas_anc_ropes == texas_ancestor_ropes

    # WHEN
    assert get_ancestor_ropes(None) == []
    assert get_ancestor_ropes("") == []
    assert get_ancestor_ropes(root_rope()) == [root_rope()]


def test_rope_get_ancestor_ropes_ReturnsObj_Scenario1_nondefault_knot():
    # ESTABLISH
    x_s = "/"
    root_belief_rope = f"{x_s}amy23{x_s}"
    nation_str = "nation"
    nation_rope = f"{root_belief_rope}{nation_str}{x_s}"
    usa_str = "USA"
    usa_rope = f"{nation_rope}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_rope = f"{usa_rope}{texas_str}{x_s}"

    # WHEN
    texas_anc_ropes = get_ancestor_ropes(rope=texas_rope, knot=x_s)

    # THEN
    print(f"     {texas_rope=}")
    print(f"{texas_anc_ropes=}")
    assert texas_anc_ropes is not None
    texas_ancestor_ropes = [
        texas_rope,
        usa_rope,
        nation_rope,
        root_belief_rope,
    ]
    assert texas_anc_ropes == texas_ancestor_ropes


def test_rope_get_forefather_ropes_ReturnsAncestorRopeTermsWithoutClean():
    # ESTABLISH
    x_s = default_knot_if_None()
    nation_str = "nation"
    nation_rope = f"{root_rope()}{nation_str}{x_s}"
    usa_str = "USA"
    usa_rope = f"{nation_rope}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_rope = f"{usa_rope}{texas_str}{x_s}"

    # WHEN
    x_ropes = get_forefather_ropes(rope=texas_rope)

    # THEN
    print(f"{texas_rope=}")
    assert x_ropes is not None
    texas_forefather_ropes = {
        nation_rope: None,
        usa_rope: None,
        root_rope(): None,
    }
    assert x_ropes == texas_forefather_ropes


def test_rope_get_default_central_label_ReturnsObj():
    assert get_default_central_label() == "YY"


def test_rope_create_rope_from_labels_ReturnsObj():
    # ESTABLISH
    x_s = default_knot_if_None()
    root_list = get_all_rope_labels(root_rope())
    casa_str = "casa"
    casa_rope = f"{root_rope()}{casa_str}{x_s}"
    casa_list = get_all_rope_labels(casa_rope)
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_rope()}{casa_str}{x_s}{bloomers_str}{x_s}"
    bloomers_list = get_all_rope_labels(bloomers_rope)
    roses_str = "roses"
    roses_rope = f"{root_rope()}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"
    roses_list = get_all_rope_labels(roses_rope)

    # WHEN / THEN
    assert root_rope() == create_rope_from_labels(root_list)
    assert casa_rope == create_rope_from_labels(casa_list)
    assert bloomers_rope == create_rope_from_labels(bloomers_list)
    assert roses_rope == create_rope_from_labels(roses_list)


def test_is_labelterm_ReturnsObj():
    # ESTABLISH
    x_s = default_knot_if_None()

    # WHEN / THEN
    assert is_labelterm("", x_knot=x_s) is False
    assert is_labelterm("casa", x_knot=x_s)
    assert not is_labelterm(f"ZZ{x_s}casa", x_s)
    assert not is_labelterm(RopeTerm(f"ZZ{x_s}casa"), x_s)
    assert is_labelterm(RopeTerm("ZZ"), x_s)


def test_is_heir_rope_CorrectlyIdentifiesHeirs():
    # ESTABLISH
    x_s = default_knot_if_None()
    usa_str = "USA"
    usa_rope = f"{root_rope()}Nation-States{x_s}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_rope = f"{usa_rope}{texas_str}{x_s}"
    # earth_str = "earth"
    # earth_rope = f"{earth_str}"
    # sea_str = "sea"
    # sea_rope = f"{earth_rope}{x_s}{sea_str}"
    # seaside_str = "seaside"
    # seaside_rope = f"{earth_rope}{x_s}{seaside_str}"

    # WHEN / THEN
    assert is_heir_rope(src=usa_rope, heir=usa_rope)
    assert is_heir_rope(src=usa_rope, heir=texas_rope)
    assert (
        is_heir_rope(f"earth{x_s}sea{x_s}", f"earth{x_s}seaside{x_s}beach{x_s}")
        is False
    )
    assert (
        is_heir_rope(src=f"earth{x_s}sea{x_s}", heir=f"earth{x_s}seaside{x_s}") is False
    )


def test_replace_knot_ReturnsNewObj():
    # ESTABLISH
    casa_str = "casa"
    root_label = get_default_central_label()
    gen_casa_rope = create_rope(root_label, casa_str)
    semicolon_knot = default_knot_if_None()
    semicolon_knot_casa_rope = (
        f"{semicolon_knot}{root_label}{semicolon_knot}{casa_str}{semicolon_knot}"
    )
    assert semicolon_knot == ";"
    assert gen_casa_rope == semicolon_knot_casa_rope

    # WHEN
    slash_knot = "/"
    gen_casa_rope = replace_knot(
        gen_casa_rope, old_knot=semicolon_knot, new_knot=slash_knot
    )

    # THEN
    slash_knot_casa_rope = f"{slash_knot}{root_label}{slash_knot}{casa_str}{slash_knot}"
    assert gen_casa_rope == slash_knot_casa_rope


def test_replace_knot_CorrectlyRaisesError():
    # ESTABLISH
    cooker_str = "cooker/cleaner"
    gen_cooker_rope = create_rope(root_rope(), cooker_str)
    semicolon_knot = default_knot_if_None()
    semicolon_knot_cooker_rope = f"{root_rope()}{cooker_str}{semicolon_knot}"
    assert semicolon_knot == ";"
    assert gen_cooker_rope == semicolon_knot_cooker_rope

    # WHEN / THEN
    slash_knot = "/"
    with pytest_raises(Exception) as excinfo:
        gen_cooker_rope = replace_knot(
            gen_cooker_rope,
            old_knot=semicolon_knot,
            new_knot=slash_knot,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_knot '{semicolon_knot}' with '{slash_knot}' because the new one exists in rope '{gen_cooker_rope}'."
    )


def test_replace_knot_WhenNewknotIsFirstInRopeTermRaisesError():
    # ESTABLISH
    cooker_str = "/cooker"
    cleaner_str = "cleaner"
    semicolon_knot = default_knot_if_None()
    semicolon_knot_cooker_rope = f"{cooker_str}{semicolon_knot}{cleaner_str}"
    assert semicolon_knot == ";"

    # WHEN / THEN
    slash_knot = "/"
    with pytest_raises(Exception) as excinfo:
        semicolon_knot_cooker_rope = replace_knot(
            semicolon_knot_cooker_rope,
            old_knot=semicolon_knot,
            new_knot=slash_knot,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_knot '{semicolon_knot}' with '{slash_knot}' because the new one exists in rope '{semicolon_knot_cooker_rope}'."
    )


def test_validate_labelterm_RaisesErrorWhenNotLabelTerm():
    # ESTABLISH
    bob_str = "Bob, Tom"
    slash_str = "/"
    assert bob_str == validate_labelterm(bob_str, x_knot=slash_str)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_labelterm(bob_str, x_knot=comma_str)
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to be a LabelTerm. Cannot contain knot: '{comma_str}'"
    )


def test_validate_labelterm_RaisesErrorWhenLabelTerm():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Tom"
    assert bob_str == validate_labelterm(
        bob_str, x_knot=slash_str, not_labelterm_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_labelterm(
            bob_str, x_knot=comma_str, not_labelterm_required=True
        )
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to not be a LabelTerm. Must contain knot: '{comma_str}'"
    )


def test_ropeterm_valid_dir_path_ReturnsObj_simple_knot():
    # ESTABLISH
    comma_str = ","
    # WHEN / THEN
    assert ropeterm_valid_dir_path(",run,", knot=comma_str)
    assert ropeterm_valid_dir_path(",run,sport,", knot=comma_str)
    print(f"{platform_system()=}")
    sport_question_valid_bool = ropeterm_valid_dir_path("run,sport?,", comma_str)
    assert (
        platform_system() == "Windows" and sport_question_valid_bool is False
    ) or platform_system() == "Linux"


def test_ropeterm_valid_dir_path_ReturnsObj_complicated_knot():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run,"
    lap_str = "lap"
    sport_rope = create_rope(sport_str, knot=question_str)
    print(f"{sport_rope=}")
    run_rope = create_rope(sport_rope, run_str, knot=question_str)
    lap_rope = create_rope(run_rope, lap_str, knot=question_str)
    assert lap_rope == f"{sport_rope}{run_str}?{lap_str}?"

    assert ropeterm_valid_dir_path(sport_rope, knot=question_str)
    assert ropeterm_valid_dir_path(run_rope, knot=question_str)
    assert ropeterm_valid_dir_path(lap_rope, knot=question_str)
    assert (
        platform_system() == "Windows"
        and ropeterm_valid_dir_path(lap_rope, knot=",") is False
    ) or platform_system() == "Linux"


def test_ropeterm_valid_dir_path_ReturnsObjWhereSlashNotknotEdgeCases():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run/swim"
    lap_str = "lap"
    sport_rope = create_rope(sport_str, knot=question_str)
    run_rope = create_rope(sport_rope, run_str, knot=question_str)
    lap_rope = create_rope(run_rope, lap_str, knot=question_str)
    assert lap_rope == f"{sport_rope}{run_str}?{lap_str}?"

    assert ropeterm_valid_dir_path(sport_rope, knot=question_str)
    assert ropeterm_valid_dir_path(run_rope, knot=question_str) is False
    assert ropeterm_valid_dir_path(lap_rope, knot=question_str) is False
    assert ropeterm_valid_dir_path(lap_rope, knot=",") is False


def test_all_ropeterms_between_ReturnsObj_Scenario0_Default_knot():
    casa_str = "casa"
    sport_str = "sport"
    run_str = "run/swim"
    lap_str = "lap"
    sport_rope = create_rope(casa_str, sport_str)
    run_rope = create_rope(sport_rope, run_str)
    lap_rope = create_rope(run_rope, lap_str)

    assert all_ropeterms_between(sport_rope, sport_rope) == [sport_rope]
    assert all_ropeterms_between(sport_rope, run_rope) == [sport_rope, run_rope]
    assert all_ropeterms_between(sport_rope, lap_rope) == [
        sport_rope,
        run_rope,
        lap_rope,
    ]


def test_all_ropeterms_between_ReturnsObj_Scenario1_NonDefault_knot():
    casa_str = "casa"
    sport_str = "sport"
    run_str = "run,swim"
    lap_str = "lap"
    slash_str = "/"
    sport_rope = create_rope(casa_str, sport_str, knot=slash_str)
    run_rope = create_rope(sport_rope, run_str, knot=slash_str)
    lap_rope = create_rope(run_rope, lap_str, knot=slash_str)

    assert all_ropeterms_between(sport_rope, sport_rope, slash_str) == [sport_rope]
    assert all_ropeterms_between(sport_rope, run_rope, slash_str) == [
        sport_rope,
        run_rope,
    ]
    assert all_ropeterms_between(sport_rope, lap_rope, slash_str) == [
        sport_rope,
        run_rope,
        lap_rope,
    ]
