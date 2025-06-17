from src.a06_plan_logic._util.a06_str import (
    concept_rope_str,
    labor_title_str,
    plan_concept_laborlink_str,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a08_plan_atom_logic._util.a08_str import DELETE_str, INSERT_str
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a09_pack_logic.delta import plandelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_laborlink_INSERT():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_laborlink_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    labor_title_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, INSERT_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(labor_title_str(), labor_title_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"laborlink '{labor_title_value}' created for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_laborlink_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_laborlink_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    labor_title_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, DELETE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(labor_title_str(), labor_title_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"laborlink '{labor_title_value}' deleted for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
