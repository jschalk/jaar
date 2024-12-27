from src.f01_road.road import (
    get_default_deal_id_ideaunit as root_label,
    default_wall_if_None,
    get_road_from_doar,
    get_doar_from_road,
)


def test_get_road_from_doar_ReturnsObj_default_wall():
    # ESTABLISH
    x_s = default_wall_if_None()
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    casa_doar = f"{casa_str}{x_s}{root_label()}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_doar = f"{bloomers_str}{x_s}{casa_str}{x_s}{root_label()}"
    roses_str = "roses"
    roses_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_doar = f"{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label()}"

    # WHEN / THEN
    assert get_road_from_doar("") == ""
    assert get_road_from_doar(root_label()) == root_label()
    assert get_road_from_doar(casa_road) == casa_doar
    assert get_road_from_doar(bloomers_road) == bloomers_doar
    assert get_road_from_doar(roses_road) == roses_doar


def test_get_road_from_doar_ReturnsObj_Not_default_wall():
    # ESTABLISH
    x_s = "/"
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    casa_doar = f"{casa_str}{x_s}{root_label()}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_doar = f"{bloomers_str}{x_s}{casa_str}{x_s}{root_label()}"
    roses_str = "roses"
    roses_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_doar = f"{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label()}"

    # WHEN / THEN
    assert get_road_from_doar("", x_s) == ""
    assert get_road_from_doar(root_label(), x_s) == root_label()
    assert get_road_from_doar(casa_road, x_s) == casa_doar
    assert get_road_from_doar(bloomers_road, x_s) == bloomers_doar
    assert get_road_from_doar(roses_road, x_s) == roses_doar


def test_get_doar_from_road_ReturnsObj_Not_default_wall():
    # ESTABLISH
    x_s = "/"
    casa_str = "casa"
    casa_road = f"{root_label()}{x_s}{casa_str}"
    casa_doar = f"{casa_str}{x_s}{root_label()}"
    bloomers_str = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_doar = f"{bloomers_str}{x_s}{casa_str}{x_s}{root_label()}"
    roses_str = "roses"
    roses_road = f"{root_label()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_doar = f"{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label()}"

    # WHEN / THEN
    assert get_doar_from_road("", x_s) == ""
    assert get_doar_from_road(root_label(), x_s) == root_label()
    assert get_doar_from_road(casa_doar, x_s) == casa_road
    assert get_doar_from_road(bloomers_doar, x_s) == bloomers_road
    assert get_doar_from_road(roses_doar, x_s) == roses_road
