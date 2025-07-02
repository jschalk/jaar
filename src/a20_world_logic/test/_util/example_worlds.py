from src.a01_term_logic.rope import create_rope
from src.a04_reason_logic.reason_concept import FactUnit, factunit_shop
from src.a06_owner_logic.owner import OwnerUnit, ownerunit_shop


def _example_empty_bob_ownerunit() -> OwnerUnit:
    a23_str = "amy23"
    return ownerunit_shop("Bob", a23_str)


def get_mop_with_no_reason_ownerunit_example() -> OwnerUnit:
    bob_owner = _example_empty_bob_ownerunit()
    casa_str = "casa"
    mop_str = "mop"
    casa_rope = bob_owner.make_l1_rope(casa_str)
    mop_rope = bob_owner.make_rope(casa_rope, mop_str)
    bob_owner.add_concept(mop_rope, task=True)
    return bob_owner


def get_bob_mop_with_reason_ownerunit_example() -> OwnerUnit:
    bob_owner = _example_empty_bob_ownerunit()
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_owner.make_l1_rope(casa_str)
    floor_rope = bob_owner.make_rope(casa_rope, floor_str)
    clean_rope = bob_owner.make_rope(floor_rope, clean_str)
    dirty_rope = bob_owner.make_rope(floor_rope, dirty_str)
    mop_rope = bob_owner.make_rope(casa_rope, mop_str)
    bob_owner.add_concept(floor_rope)
    bob_owner.add_concept(clean_rope)
    bob_owner.add_concept(dirty_rope)
    bob_owner.add_concept(mop_rope, task=True)
    bob_owner.edit_concept_attr(
        mop_rope, reason_rcontext=floor_rope, reason_premise=clean_rope
    )
    return bob_owner


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    floor_rope = create_rope(casa_rope, "floor status")
    clean_rope = create_rope(floor_rope, "clean")
    return factunit_shop(floor_rope, clean_rope)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    floor_rope = create_rope(casa_rope, "floor status")
    dirty_rope = create_rope(floor_rope, "dirty")
    return factunit_shop(floor_rope, dirty_rope)
