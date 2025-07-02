from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    concept_rope_str,
    labor_title_str,
    owner_concept_laborlink_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import DELETE_str, INSERT_str
from src.a09_pack_logic.delta import ownerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_laborlink_INSERT():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_concept_laborlink_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    labor_title_value = f"{sue_owner.knot}Swimmers"
    swim_owneratom = owneratom_shop(dimen, INSERT_str())
    swim_owneratom.set_arg(concept_rope_str(), rope_value)
    swim_owneratom.set_arg(labor_title_str(), labor_title_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"laborlink '{labor_title_value}' created for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_laborlink_DELETE():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_concept_laborlink_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    labor_title_value = f"{sue_owner.knot}Swimmers"
    swim_owneratom = owneratom_shop(dimen, DELETE_str())
    swim_owneratom.set_arg(concept_rope_str(), rope_value)
    swim_owneratom.set_arg(labor_title_str(), labor_title_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"laborlink '{labor_title_value}' deleted for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
