from src.ch04_rope.rope import create_rope, default_knot_if_None, get_unique_short_ropes
from src.ref.keywords import Ch04Keywords as kw


def test_get_unique_short_ropes_ReturnsObj_Scenario0_RootOnly():
    # ESTABLISH
    a23_str = "Amy23"
    knot = default_knot_if_None()
    a23_rope = create_rope(a23_str, None, knot)
    rope_set = {a23_rope}

    # WHEN
    unique_short_ropes = get_unique_short_ropes(rope_set, knot)

    # THEN
    assert unique_short_ropes == {a23_rope: a23_str}


def test_get_unique_short_ropess_ReturnsObj_Scenario1_WithUniqueLabels():
    # ESTABLISH
    a23_str = "Amy23"
    knot = default_knot_if_None()
    a23_rope = create_rope(a23_str, None, knot)
    casa_str = "casa"
    mop_str = "mop"
    casa_rope = create_rope(a23_rope, casa_str)
    mop_rope = create_rope(a23_rope, mop_str)
    rope_set = {a23_rope, casa_rope, mop_rope}

    # WHEN
    unique_short_ropes = get_unique_short_ropes(rope_set, knot)

    # THEN
    assert unique_short_ropes == {
        a23_rope: a23_str,
        casa_rope: casa_str,
        mop_rope: mop_str,
    }


def test_get_unique_short_ropess_ReturnsObj_Scenario2_WithCommonLabels():
    # ESTABLISH
    a23_str = "Amy23"
    knot = default_knot_if_None()
    a23_rope = create_rope(a23_str, None, knot)
    casa_str = "casa"
    mop_str = "mop"
    casa_rope = create_rope(a23_rope, casa_str)
    casa_mop_rope = create_rope(casa_rope, mop_str)
    sports_str = "sports"
    sports_rope = create_rope(a23_rope, sports_str)
    sports_mop_rope = create_rope(sports_rope, mop_str)
    rope_set = {a23_rope, casa_rope, casa_mop_rope, sports_rope, sports_mop_rope}

    # WHEN
    unique_short_ropes = get_unique_short_ropes(rope_set, knot)

    # THEN
    expected_short_casa_mop = f"{casa_str}{knot}{mop_str}"
    assert unique_short_ropes.get(casa_mop_rope) == expected_short_casa_mop
    assert unique_short_ropes == {
        a23_rope: a23_str,
        casa_rope: casa_str,
        casa_mop_rope: expected_short_casa_mop,
        sports_rope: sports_str,
        sports_mop_rope: f"{sports_str}{knot}{mop_str}",
    }
