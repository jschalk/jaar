from src.a01_term_logic.way import create_way
from src.a04_reason_logic.reason_concept import factunit_shop, FactUnit


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    clean_way = create_way(casa_way, "clean")
    return factunit_shop(casa_way, clean_way)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    dirty_way = create_way(casa_way, "dirty")
    return factunit_shop(casa_way, dirty_way)


def example_casa_grimy_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    grimy_way = create_way(casa_way, "grimy")
    return factunit_shop(casa_way, grimy_way)


def example_sky_blue_factunit() -> FactUnit:
    a23_str = "accord23"
    sky_way = create_way(a23_str, "sky color")
    blue_way = create_way(sky_way, "blue")
    return factunit_shop(sky_way, blue_way)
