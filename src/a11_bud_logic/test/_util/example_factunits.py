from src.a01_term_logic.rope import create_rope
from src.a04_reason_logic.reason_concept import FactUnit, factunit_shop


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_rope = create_rope(a23_str, "casa")
    clean_rope = create_rope(casa_rope, "clean")
    return factunit_shop(casa_rope, clean_rope)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_rope = create_rope(a23_str, "casa")
    dirty_rope = create_rope(casa_rope, "dirty")
    return factunit_shop(casa_rope, dirty_rope)


def example_casa_grimy_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_rope = create_rope(a23_str, "casa")
    grimy_rope = create_rope(casa_rope, "grimy")
    return factunit_shop(casa_rope, grimy_rope)


def example_sky_blue_factunit() -> FactUnit:
    a23_str = "accord23"
    sky_rope = create_rope(a23_str, "sky color")
    blue_rope = create_rope(sky_rope, "blue")
    return factunit_shop(sky_rope, blue_rope)
