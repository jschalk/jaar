from src.a01_term_logic.rope import (
    default_knot_if_None,
    get_rope_from_yaw,
    get_yaw_from_rope,
    to_rope,
)


def test_get_rope_from_yaw_ReturnsObj_default_knot():
    # ESTABLISH
    x_s = default_knot_if_None()
    casa_str = "casa"
    root_label = "accord23"
    casa_rope = f"{x_s}{root_label}{x_s}{casa_str}{x_s}"
    casa_yaw = f"{x_s}{casa_str}{x_s}{root_label}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{x_s}{root_label}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}"
    bloomers_yaw = f"{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    roses_str = "roses"
    roses_rope = (
        f"{x_s}{root_label}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"
    )
    roses_yaw = (
        f"{x_s}{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    )

    # WHEN / THEN
    assert get_rope_from_yaw("") == ""
    root_rope = to_rope(root_label)
    assert get_rope_from_yaw(root_rope) == root_rope
    assert get_rope_from_yaw(casa_rope) == casa_yaw
    assert get_rope_from_yaw(bloomers_rope) == bloomers_yaw
    print(roses_rope)
    assert get_rope_from_yaw(roses_rope) == roses_yaw


def test_get_rope_from_yaw_ReturnsObj_Not_default_knot():
    # ESTABLISH
    x_s = "/"
    root_label = "accord23"
    root_vow_rope = f"{x_s}{root_label}{x_s}"
    casa_str = "casa"
    casa_rope = f"{root_vow_rope}{casa_str}{x_s}"
    casa_yaw = f"{x_s}{casa_str}{x_s}{root_label}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_vow_rope}{casa_str}{x_s}{bloomers_str}{x_s}"
    bloomers_yaw = f"{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    roses_str = "roses"
    roses_rope = (
        f"{x_s}{root_label}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"
    )
    roses_yaw = (
        f"{x_s}{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    )

    # WHEN / THEN
    assert get_rope_from_yaw("", x_s) == ""
    assert get_rope_from_yaw(root_vow_rope, x_s) == root_vow_rope
    assert get_rope_from_yaw(casa_rope, x_s) == casa_yaw
    assert get_rope_from_yaw(bloomers_rope, x_s) == bloomers_yaw
    assert get_rope_from_yaw(roses_rope, x_s) == roses_yaw


def test_get_yaw_from_rope_ReturnsObj_Not_default_knot():
    # ESTABLISH
    x_s = "/"
    root_label = "accord23"
    root_vow_rope = f"{x_s}{root_label}{x_s}"
    casa_str = "casa"
    casa_rope = f"{root_vow_rope}{casa_str}{x_s}"
    casa_yaw = f"{x_s}{casa_str}{x_s}{root_label}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_vow_rope}{casa_str}{x_s}{bloomers_str}{x_s}"
    bloomers_yaw = f"{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    roses_str = "roses"
    roses_rope = f"{root_vow_rope}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"
    roses_yaw = (
        f"{x_s}{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    )

    # WHEN / THEN
    assert get_yaw_from_rope("", x_s) == ""
    assert get_yaw_from_rope(root_vow_rope, x_s) == root_vow_rope
    assert get_yaw_from_rope(casa_yaw, x_s) == casa_rope
    assert get_yaw_from_rope(bloomers_yaw, x_s) == bloomers_rope
    assert get_yaw_from_rope(roses_yaw, x_s) == roses_rope
