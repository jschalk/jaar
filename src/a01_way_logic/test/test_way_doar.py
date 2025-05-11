from src.a01_way_logic.way import (
    get_default_fisc_tag as root_tag,
    get_default_fisc_way as root_way,
    default_bridge_if_None,
    get_way_from_yaw,
    get_yaw_from_way,
)


def test_get_way_from_yaw_ReturnsObj_default_bridge():
    # ESTABLISH
    x_s = default_bridge_if_None()
    casa_str = "casa"
    casa_way = f"{x_s}{root_tag()}{x_s}{casa_str}"
    casa_yaw = f"{x_s}{casa_str}{x_s}{root_tag()}"
    bloomers_str = "bloomers"
    bloomers_way = f"{x_s}{root_tag()}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_yaw = f"{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_tag()}"
    roses_str = "roses"
    roses_way = f"{x_s}{root_tag()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_yaw = f"{x_s}{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_tag()}"

    # WHEN / THEN
    assert get_way_from_yaw("") == ""
    assert get_way_from_yaw(root_way()) == root_way()
    assert get_way_from_yaw(casa_way) == casa_yaw
    assert get_way_from_yaw(bloomers_way) == bloomers_yaw
    print(roses_way)
    assert get_way_from_yaw(roses_way) == roses_yaw


def test_get_way_from_yaw_ReturnsObj_Not_default_bridge():
    # ESTABLISH
    x_s = "/"
    root_fisc_way = f"{x_s}{root_tag()}"
    casa_str = "casa"
    casa_way = f"{root_fisc_way}{x_s}{casa_str}"
    casa_yaw = f"{x_s}{casa_str}{x_s}{root_tag()}"
    bloomers_str = "bloomers"
    bloomers_way = f"{root_fisc_way}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_yaw = f"{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_tag()}"
    roses_str = "roses"
    roses_way = f"{x_s}{root_tag()}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_yaw = f"{x_s}{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_tag()}"

    # WHEN / THEN
    assert get_way_from_yaw("", x_s) == ""
    assert get_way_from_yaw(root_fisc_way, x_s) == root_fisc_way
    assert get_way_from_yaw(casa_way, x_s) == casa_yaw
    assert get_way_from_yaw(bloomers_way, x_s) == bloomers_yaw
    assert get_way_from_yaw(roses_way, x_s) == roses_yaw


def test_get_yaw_from_way_ReturnsObj_Not_default_bridge():
    # ESTABLISH
    x_s = "/"
    root_fisc_way = f"{x_s}{root_tag()}"
    casa_str = "casa"
    casa_way = f"{root_fisc_way}{x_s}{casa_str}"
    casa_yaw = f"{x_s}{casa_str}{x_s}{root_tag()}"
    bloomers_str = "bloomers"
    bloomers_way = f"{root_fisc_way}{x_s}{casa_str}{x_s}{bloomers_str}"
    bloomers_yaw = f"{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_tag()}"
    roses_str = "roses"
    roses_way = f"{root_fisc_way}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}"
    roses_yaw = f"{x_s}{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_tag()}"

    # WHEN / THEN
    assert get_yaw_from_way("", x_s) == ""
    assert get_yaw_from_way(root_fisc_way, x_s) == root_fisc_way
    assert get_yaw_from_way(casa_yaw, x_s) == casa_way
    assert get_yaw_from_way(bloomers_yaw, x_s) == bloomers_way
    assert get_yaw_from_way(roses_yaw, x_s) == roses_way
