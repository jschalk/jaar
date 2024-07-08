from src._road.road import (
    RoadNode,
    HealerID,
    OwnerID,
    CharID,
    RoadUnit,
    rebuild_road,
    is_sub_road,
    get_all_road_nodes,
    get_terminus_node,
    find_replace_road_key_dict,
    get_parent_road,
    create_road_without_root_node,
    get_root_node_from_road,
    road_validate,
    get_ancestor_roads,
    get_forefather_roads,
    get_default_real_id_roadnode as root_label,
    create_road_from_nodes,
    create_road,
    get_diff_road,
    create_road,
    is_heir_road,
    default_road_delimiter_if_none,
    replace_road_delimiter,
    validate_roadnode,
    roadunit_valid_dir_path,
)
from pytest import raises as pytest_raises
from dataclasses import dataclass
from inspect import getdoc as inspect_getdoc
from platform import system as platform_system


def test_RoadNode_exists():
    # GIVEN
    empty_str = ""
    # WHEN
    x_road = RoadNode(empty_str)
    # THEN
    assert x_road == empty_str
    assert (
        inspect_getdoc(x_road)
        == "A string presentation of a tree node. Nodes cannot contain RoadUnit delimiter"
    )


def test_RoadUnit_exists():
    # GIVEN
    empty_str = ""
    # WHEN
    x_road = RoadUnit(empty_str)
    # THEN
    assert x_road == empty_str
    assert (
        inspect_getdoc(x_road)
        == "A string presentation of a tree path. RoadNodes are seperated by road delimiter"
    )


def test_road_is_sub_road_correctlyReturnsBool():
    # WHEN
    casa_text = "casa"
    casa_road = f"{root_label()}{default_road_delimiter_if_none()}{casa_text}"
    cleaning_text = "cleaning"
    cleaning_road = f"{casa_road}{default_road_delimiter_if_none()}{cleaning_text}"
    laundrys_text = "laundrys"
    laundrys_road = f"{cleaning_road}{default_road_delimiter_if_none()}{laundrys_text}"
    print(f"{cleaning_road=}")
    print(f"{laundrys_road=}")

    # WHEN / THEN
    assert is_sub_road(cleaning_road, cleaning_road)
    assert is_sub_road(laundrys_road, cleaning_road)
    assert is_sub_road(cleaning_road, laundrys_road) is False


def test_road_road_validate_correctlyReturnsRoadUnit():
    x_s = default_road_delimiter_if_none()
    _real_id = "x"
    casa_road = f"{_real_id}{x_s}casa"
    source_road = f"{_real_id}{x_s}source"
    fun_road = f"{_real_id}{x_s}fun"
    assert road_validate(None, x_s, _real_id) == ""
    assert road_validate("", x_s, _real_id) == ""
    assert road_validate(f"{_real_id}{x_s}casa", x_s, _real_id) == casa_road
    assert road_validate(f"A{x_s}casa", x_s, _real_id) == casa_road
    assert road_validate(f"{x_s}source", x_s, _real_id) == source_road
    assert road_validate(f"source{x_s}fun", x_s, _real_id) == fun_road
    assert road_validate("source", x_s, _real_id) == _real_id
    assert road_validate(f"AA{x_s}casa", x_s, _real_id) == casa_road


def test_road_create_road_ReturnsCorrectRoadUnitWith_delimiter():
    # GIVEN
    rose_text = "rose"
    comma_delimiter = ","
    comma_delimiter_rose_road = f"{root_label()}{comma_delimiter}{rose_text}"
    assert create_road(root_label(), rose_text) == comma_delimiter_rose_road

    # WHEN
    slash_delimiter = "/"
    slash_delimiter_rose_road = f"{root_label()}{slash_delimiter}{rose_text}"
    generated_rose_road = create_road(
        root_label(), rose_text, delimiter=slash_delimiter
    )

    # THEN
    assert generated_rose_road != comma_delimiter_rose_road
    assert generated_rose_road == slash_delimiter_rose_road

    # WHEN
    brackets_road = create_road(root_label(), rose_text, delimiter=slash_delimiter)

    # THEN
    assert generated_rose_road == brackets_road
    assert slash_delimiter_rose_road == brackets_road


def test_road_rebuild_road_ReturnsCorrectRoadUnit():
    # GIVEN
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_text)
    greenery_text = "greenery"
    greenery_road = create_road(casa_road, greenery_text)
    roses_text = "roses"
    old_roses_road = create_road(bloomers_road, roses_text)
    new_roses_road = create_road(greenery_road, roses_text)

    print(f"{rebuild_road(old_roses_road, bloomers_road, greenery_road)}")

    # WHEN / THEN
    assert rebuild_road(bloomers_road, bloomers_road, bloomers_road) == bloomers_road
    assert rebuild_road(old_roses_road, bloomers_road, greenery_road) == new_roses_road
    assert rebuild_road(old_roses_road, "random_text", greenery_road) == old_roses_road


def test_road_get_all_road_nodes_ReturnsRoadNodes():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"

    # WHEN/THENs
    root_list = [root_label()]
    assert get_all_road_nodes(road=root_label()) == root_list
    casa_list = [root_label(), casa_text]
    assert get_all_road_nodes(road=casa_road) == casa_list
    bloomers_list = [root_label(), casa_text, bloomers_text]
    assert get_all_road_nodes(road=bloomers_road) == bloomers_list
    roses_list = [root_label(), casa_text, bloomers_text, roses_text]
    assert get_all_road_nodes(road=roses_road) == roses_list


def test_road_get_terminus_node_ReturnsRoadNode():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_text}"

    # WHEN/THENs
    assert get_terminus_node(road=root_label()) == root_label()
    assert get_terminus_node(road=casa_road) == casa_text
    assert get_terminus_node(road=bloomers_road) == bloomers_text
    assert get_terminus_node(road=roses_road) == roses_text


def test_road_get_terminus_node_ReturnsRoadNodeWhenNonDefaultDelimiter():
    # GIVEN
    casa_text = "casa"
    bloomers_text = "bloomers"
    roses_text = "roses"
    slash_text = default_road_delimiter_if_none()
    slash_casa_road = f"{root_label()}{slash_text}{casa_text}"
    slash_bloomers_road = f"{slash_casa_road}{slash_text}{bloomers_text}"
    slash_roses_road = f"{slash_bloomers_road}{slash_text}{roses_text}"

    # WHEN/THENs
    assert get_terminus_node(root_label(), slash_text) == root_label()
    assert get_terminus_node(slash_casa_road, slash_text) == casa_text
    assert get_terminus_node(slash_bloomers_road, slash_text) == bloomers_text
    assert get_terminus_node(slash_roses_road, slash_text) == roses_text


def test_road_get_root_node_from_road_ReturnsRoadNode():
    # GIVEN
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_text)
    roses_text = "roses"
    roses_road = create_road(casa_text, roses_text)

    # WHEN/THENs
    assert get_root_node_from_road(root_label()) == root_label()
    assert get_root_node_from_road(casa_road) == root_label()
    assert get_root_node_from_road(bloomers_road) == root_label()
    assert get_root_node_from_road(roses_road) == casa_text


def test_road_get_parent_road_ReturnsCorrectObj():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_text}"

    # WHEN/THENs
    assert get_parent_road(road=root_label()) == ""
    assert get_parent_road(road=casa_road) == root_label()
    assert get_parent_road(road=bloomers_road) == casa_road
    assert get_parent_road(road=roses_road) == bloomers_road


def test_road_create_road_without_root_node_ReturnsCorrectObj():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    casa_without_root_road = f"{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}"
    bloomers_without_root_road = f"{x_s}{casa_text}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"
    roses_without_root_road = f"{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"

    # WHEN/THENs
    assert create_road_without_root_node(road=root_label()) == x_s
    assert create_road_without_root_node(road=casa_road) == casa_without_root_road
    assert (
        create_road_without_root_node(road=bloomers_road) == bloomers_without_root_road
    )
    assert create_road_without_root_node(road=roses_road) == roses_without_root_road
    road_without_node = create_road_without_root_node(road=roses_road)
    with pytest_raises(Exception) as excinfo:
        create_road_without_root_node(road=road_without_node)
    assert (
        str(excinfo.value)
        == f"Cannot create_road_without_root_node of '{road_without_node}' because it has no root node."
    )


@dataclass
class EmptyObj:
    x_road: RoadUnit = ""

    def find_replace_road(self, old_road, new_road):
        self.x_road = rebuild_road(self.x_road, old_road=old_road, new_road=new_road)

    def get_obj_key(self) -> RoadUnit:
        return self.x_road


def test_road_find_replace_road_key_dict_ReturnsCorrectDict_Scenario1():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    old_seasons_road = f"{root_label()}{x_s}casa{x_s}seasons"
    old_dict_x = {old_seasons_road: EmptyObj(old_seasons_road)}
    assert old_dict_x.get(old_seasons_road) != None

    # WHEN
    new_seasons_road = f"{root_label()}{x_s}casa{x_s}kookies"
    new_dict_x = find_replace_road_key_dict(
        dict_x=old_dict_x, old_road=old_seasons_road, new_road=new_seasons_road
    )

    assert new_dict_x != {}
    assert len(new_dict_x) == 1
    print(f"{new_dict_x=}")
    assert new_dict_x.get(new_seasons_road) != None
    assert new_dict_x.get(old_seasons_road) is None


def test_road_get_ancestor_roads_ReturnsAncestorRoadUnits():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    nation_text = "nation-state"
    nation_road = f"{root_label()}{x_s}{nation_text}"
    usa_text = "USA"
    usa_road = f"{nation_road}{x_s}{usa_text}"
    texas_text = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_text}"

    # WHEN
    x_roads = get_ancestor_roads(road=texas_road)

    # THEN
    print(f"{texas_road=}")
    assert x_roads != None
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


def test_road_get_forefather_roads_ReturnsAncestorRoadUnitsWithoutSource():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    nation_text = "nation-state"
    nation_road = f"{root_label()}{x_s}{nation_text}"
    usa_text = "USA"
    usa_road = f"{nation_road}{x_s}{usa_text}"
    texas_text = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_text}"

    # WHEN
    x_roads = get_forefather_roads(road=texas_road)

    # THEN
    print(f"{texas_road=}")
    assert x_roads != None
    texas_forefather_roads = {
        nation_road: None,
        usa_road: None,
        root_label(): None,
    }
    assert x_roads == texas_forefather_roads


def test_road_get_default_real_id_roadnode_ReturnsCorrectObj():
    assert root_label() == "ZZ"


def test_road_create_road_from_nodes_ReturnsCorrectObj():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    root_list = get_all_road_nodes(root_label())
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    casa_list = get_all_road_nodes(casa_road)
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}"
    bloomers_list = get_all_road_nodes(bloomers_road)
    roses_text = "roses"
    roses_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"
    roses_list = get_all_road_nodes(roses_road)

    # WHEN / THEN
    assert root_label() == create_road_from_nodes(root_list)
    assert casa_road == create_road_from_nodes(casa_list)
    assert bloomers_road == create_road_from_nodes(bloomers_list)
    assert roses_road == create_road_from_nodes(roses_list)


def test_road_create_road_ReturnsCorrectObj():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"

    # WHEN / THEN
    assert root_label() == create_road(None, root_label())
    assert root_label() == create_road("", root_label())
    assert casa_road == create_road(root_label(), casa_text)
    assert bloomers_road == create_road(casa_road, bloomers_text)
    assert roses_road == create_road(bloomers_road, roses_text)
    assert roses_road == create_road(roses_road, None)


def test_Roadnode_exists():
    # GIVEN
    empty_text = ""

    # WHEN
    new_obj = RoadNode(empty_text)

    # THEN
    assert new_obj == empty_text


def test_Roadnode_is_node_ReturnsCorrectBool():
    # WHEN / THEN
    x_roadnode = RoadNode("")
    assert x_roadnode.is_node()

    # WHEN / THEN
    x_s = default_road_delimiter_if_none()
    x_roadnode = RoadNode(f"casa{x_s}kitchen")
    assert x_roadnode.is_node() is False


def test_get_diff_road_ReturnsCorrectObj():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_text}"

    # WHEN / THEN
    print(f"{casa_road=}")
    print(f"{bloomers_road=}")
    assert get_diff_road(bloomers_road, casa_road) == bloomers_text
    assert get_diff_road(roses_road, bloomers_road) == roses_text
    bloomers_rose_road = create_road(bloomers_text, roses_text)
    print(f"{bloomers_rose_road=}")
    assert get_diff_road(roses_road, casa_road) == bloomers_rose_road


def test_is_heir_road_CorrectlyIdentifiesHeirs():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    usa_text = "USA"
    usa_road = f"{root_label()}{x_s}Nation-States{x_s}{usa_text}"
    texas_text = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_text}"
    # earth_text = "earth"
    # earth_road = f"{earth_text}"
    # sea_text = "sea"
    # sea_road = f"{earth_road}{x_s}{sea_text}"
    # seaside_text = "seaside"
    # seaside_road = f"{earth_road}{x_s}{seaside_text}"

    # WHEN / THEN
    assert is_heir_road(src=usa_road, heir=usa_road)
    assert is_heir_road(src=usa_road, heir=texas_road)
    assert is_heir_road(f"earth{x_s}sea", f"earth{x_s}seaside{x_s}beach") is False
    assert is_heir_road(src=f"earth{x_s}sea", heir=f"earth{x_s}seaside") is False


def test_replace_road_delimiter_ReturnsNewObj():
    # GIVEN
    casa_text = "casa"
    gen_casa_road = create_road(root_label(), casa_text)
    comma_delimiter = default_road_delimiter_if_none()
    comma_delimiter_casa_road = f"{root_label()}{comma_delimiter}{casa_text}"
    assert comma_delimiter == ","
    assert gen_casa_road == comma_delimiter_casa_road

    # WHEN
    slash_delimiter = "/"
    gen_casa_road = replace_road_delimiter(
        gen_casa_road, old_delimiter=comma_delimiter, new_delimiter=slash_delimiter
    )

    # THEN
    slash_delimiter_casa_road = f"{root_label()}{slash_delimiter}{casa_text}"
    assert gen_casa_road == slash_delimiter_casa_road


def test_replace_road_delimiter_CorrectlyRaisesError():
    # GIVEN
    cooker_text = "cooker/cleaner"
    gen_cooker_road = create_road(root_label(), cooker_text)
    comma_delimiter = default_road_delimiter_if_none()
    comma_delimiter_cooker_road = f"{root_label()}{comma_delimiter}{cooker_text}"
    assert comma_delimiter == ","
    assert gen_cooker_road == comma_delimiter_cooker_road

    # WHEN / THEN
    slash_delimiter = "/"
    with pytest_raises(Exception) as excinfo:
        gen_cooker_road = replace_road_delimiter(
            gen_cooker_road,
            old_delimiter=comma_delimiter,
            new_delimiter=slash_delimiter,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_road_delimiter '{comma_delimiter}' with '{slash_delimiter}' because the new one already exists in road '{gen_cooker_road}'."
    )


def test_replace_road_delimiter_WhenNewdelimiterIsFirstInRoadUnitRaisesError():
    # GIVEN
    cooker_text = "/cooker"
    cleaner_text = "cleaner"
    comma_delimiter = default_road_delimiter_if_none()
    comma_delimiter_cooker_road = f"{cooker_text}{comma_delimiter}{cleaner_text}"
    assert comma_delimiter == ","

    # WHEN / THEN
    slash_delimiter = "/"
    with pytest_raises(Exception) as excinfo:
        comma_delimiter_cooker_road = replace_road_delimiter(
            comma_delimiter_cooker_road,
            old_delimiter=comma_delimiter,
            new_delimiter=slash_delimiter,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_road_delimiter '{comma_delimiter}' with '{slash_delimiter}' because the new one already exists in road '{comma_delimiter_cooker_road}'."
    )


def test_HealerID_exists():
    # GIVEN
    bob_text = "Bob"
    # WHEN
    bob_healer_id = HealerID(bob_text)
    # THEN
    assert bob_healer_id == bob_text
    assert (
        inspect_getdoc(bob_healer_id)
        == "A RoadNode used to identify a Problem's Healer"
    )


def test_OwnerID_exists():
    # GIVEN
    bob_text = "Bob"
    # WHEN
    bob_owner_id = OwnerID(bob_text)
    # THEN
    assert bob_owner_id == bob_text
    assert (
        inspect_getdoc(bob_owner_id)
        == "A RoadNode used to identify a WorldUnit's owner_id"
    )


def test_CharID_exists():
    # GIVEN
    bob_text = "Bob"
    # WHEN
    bob_char_id = CharID(bob_text)
    # THEN
    assert bob_char_id == bob_text
    assert (
        inspect_getdoc(bob_char_id)
        == "Every CharID object is OwnerID, must follow OwnerID format."
    )


def test_validate_roadnode_RaisesErrorWhenNotRoadNode():
    # GIVEN
    bob_text = "Bob, Tom"
    slash_text = "/"
    assert bob_text == validate_roadnode(bob_text, x_delimiter=slash_text)

    # WHEN
    comma_text = ","
    with pytest_raises(Exception) as excinfo:
        bob_text == validate_roadnode(bob_text, x_delimiter=comma_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{comma_text}'"
    )


def test_validate_roadnode_RaisesErrorWhenRoadNode():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Tom"
    assert bob_text == validate_roadnode(
        bob_text, x_delimiter=slash_text, not_roadnode_required=True
    )

    # WHEN
    comma_text = ","
    with pytest_raises(Exception) as excinfo:
        bob_text == validate_roadnode(
            bob_text, x_delimiter=comma_text, not_roadnode_required=True
        )
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to not be a RoadNode. Must contain delimiter: '{comma_text}'"
    )


def test_roadunit_valid_dir_path_ReturnsCorrectObj_simple_delimiter():
    # GIVEN
    comma_text = ","
    # WHEN / THEN
    assert roadunit_valid_dir_path("run", delimiter=comma_text)
    assert roadunit_valid_dir_path("run,sport", delimiter=comma_text)
    print(f"{platform_system()=}")
    sport_question_valid_bool = roadunit_valid_dir_path("run,sport?", comma_text)
    assert (
        platform_system() == "Windows" and sport_question_valid_bool is False
    ) or platform_system() == "Linux"


def test_roadunit_valid_dir_path_ReturnsCorrectObj_complicated_delimiter():
    # GIVEN
    question_text = "?"
    sport_text = "sport"
    run_text = "run,"
    lap_text = "lap"
    sport_road = create_road(sport_text, delimiter=question_text)
    run_road = create_road(sport_road, run_text, delimiter=question_text)
    lap_road = create_road(run_road, lap_text, delimiter=question_text)
    assert lap_road == f"{sport_road}?{run_text}?{lap_text}"

    assert roadunit_valid_dir_path(sport_road, delimiter=question_text)
    assert roadunit_valid_dir_path(run_road, delimiter=question_text)
    assert roadunit_valid_dir_path(lap_road, delimiter=question_text)
    assert (
        platform_system() == "Windows"
        and roadunit_valid_dir_path(lap_road, delimiter=",") is False
    ) or platform_system() == "Linux"


def test_roadunit_valid_dir_path_ReturnsCorrectObjGivenSlashNotDelimiterEdgeCases():
    # GIVEN
    question_text = "?"
    sport_text = "sport"
    run_text = "run/swim"
    lap_text = "lap"
    sport_road = create_road(sport_text, delimiter=question_text)
    run_road = create_road(sport_road, run_text, delimiter=question_text)
    lap_road = create_road(run_road, lap_text, delimiter=question_text)
    assert lap_road == f"{sport_road}?{run_text}?{lap_text}"

    assert roadunit_valid_dir_path(sport_road, delimiter=question_text)
    assert roadunit_valid_dir_path(run_road, delimiter=question_text) is False
    assert roadunit_valid_dir_path(lap_road, delimiter=question_text) is False
    assert roadunit_valid_dir_path(lap_road, delimiter=",") is False
