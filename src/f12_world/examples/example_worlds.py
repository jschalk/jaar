from src.a01_word_logic.road import create_road
from src.f02_bud.item import itemunit_shop
from src.f02_bud.reason_item import factunit_shop, reasonunit_shop, FactUnit
from src.f02_bud.bud import BudUnit, budunit_shop


def _example_empty_bob_budunit() -> BudUnit:
    a23_str = "accord23"
    return budunit_shop("Bob", a23_str)


def get_mop_with_no_reason_budunit_example() -> BudUnit:
    bob_bud = _example_empty_bob_budunit()
    casa_str = "casa"
    mop_str = "mop"
    casa_road = bob_bud.make_l1_road(casa_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.add_item(mop_road, pledge=True)
    return bob_bud


def get_bob_mop_with_reason_budunit_example() -> BudUnit:
    bob_bud = _example_empty_bob_budunit()
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_road = bob_bud.make_l1_road(casa_str)
    floor_road = bob_bud.make_road(casa_road, floor_str)
    clean_road = bob_bud.make_road(floor_road, clean_str)
    dirty_road = bob_bud.make_road(floor_road, dirty_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.add_item(floor_road)
    bob_bud.add_item(clean_road)
    bob_bud.add_item(dirty_road)
    bob_bud.add_item(mop_road, pledge=True)
    bob_bud.edit_item_attr(mop_road, reason_base=floor_road, reason_premise=clean_road)
    return bob_bud


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_road = create_road(a23_str, "casa")
    floor_road = create_road(casa_road, "floor status")
    clean_road = create_road(floor_road, "clean")
    return factunit_shop(floor_road, clean_road)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_road = create_road(a23_str, "casa")
    floor_road = create_road(casa_road, "floor status")
    dirty_road = create_road(floor_road, "dirty")
    return factunit_shop(floor_road, dirty_road)
