from src.a01_rope_logic.rope import (
    default_knot_if_None,
    get_epor_from_rope,
    get_rope_from_epor,
    to_rope,
)


def test_get_rope_from_epor_ReturnsObj_default_knot():
    # ESTABLISH
    x_s = default_knot_if_None()
    casa_str = "casa"
    root_label = "amy23"
    casa_rope = f"{x_s}{root_label}{x_s}{casa_str}{x_s}"
    casa_epor = f"{x_s}{casa_str}{x_s}{root_label}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{x_s}{root_label}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}"
    bloomers_epor = f"{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    roses_str = "roses"
    roses_rope = (
        f"{x_s}{root_label}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"
    )
    roses_epor = (
        f"{x_s}{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    )

    # WHEN / THEN
    assert get_rope_from_epor("") == ""
    root_rope = to_rope(root_label)
    assert get_rope_from_epor(root_rope) == root_rope
    assert get_rope_from_epor(casa_rope) == casa_epor
    assert get_rope_from_epor(bloomers_rope) == bloomers_epor
    print(roses_rope)
    assert get_rope_from_epor(roses_rope) == roses_epor


def test_get_rope_from_epor_ReturnsObj_Not_default_knot():
    # ESTABLISH
    x_s = "/"
    root_label = "amy23"
    root_moment_rope = f"{x_s}{root_label}{x_s}"
    casa_str = "casa"
    casa_rope = f"{root_moment_rope}{casa_str}{x_s}"
    casa_epor = f"{x_s}{casa_str}{x_s}{root_label}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_moment_rope}{casa_str}{x_s}{bloomers_str}{x_s}"
    bloomers_epor = f"{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    roses_str = "roses"
    roses_rope = (
        f"{x_s}{root_label}{x_s}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"
    )
    roses_epor = (
        f"{x_s}{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    )

    # WHEN / THEN
    assert get_rope_from_epor("", x_s) == ""
    assert get_rope_from_epor(root_moment_rope, x_s) == root_moment_rope
    assert get_rope_from_epor(casa_rope, x_s) == casa_epor
    assert get_rope_from_epor(bloomers_rope, x_s) == bloomers_epor
    assert get_rope_from_epor(roses_rope, x_s) == roses_epor


def test_get_epor_from_rope_ReturnsObj_Not_default_knot():
    # ESTABLISH
    x_s = "/"
    root_label = "amy23"
    root_moment_rope = f"{x_s}{root_label}{x_s}"
    casa_str = "casa"
    casa_rope = f"{root_moment_rope}{casa_str}{x_s}"
    casa_epor = f"{x_s}{casa_str}{x_s}{root_label}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_moment_rope}{casa_str}{x_s}{bloomers_str}{x_s}"
    bloomers_epor = f"{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    roses_str = "roses"
    roses_rope = f"{root_moment_rope}{casa_str}{x_s}{bloomers_str}{x_s}{roses_str}{x_s}"
    roses_epor = (
        f"{x_s}{roses_str}{x_s}{bloomers_str}{x_s}{casa_str}{x_s}{root_label}{x_s}"
    )

    # WHEN / THEN
    assert get_epor_from_rope("", x_s) == ""
    assert get_epor_from_rope(root_moment_rope, x_s) == root_moment_rope
    assert get_epor_from_rope(casa_epor, x_s) == casa_rope
    assert get_epor_from_rope(bloomers_epor, x_s) == bloomers_rope
    assert get_epor_from_rope(roses_epor, x_s) == roses_rope
