from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.a06_str import (
    concept_rope_str,
    plan_concept_reasonunit_str,
    rconcept_active_requisite_str,
    rcontext_str,
)
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a08_plan_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import plandelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_reasonunit_INSERT_With_rconcept_active_requisite():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reasonunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    rcontext_value = f"{sue_plan.knot}Swimmers"
    rconcept_active_requisite_value = True
    swim_planatom = planatom_shop(dimen, INSERT_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    swim_planatom.set_arg(
        rconcept_active_requisite_str(), rconcept_active_requisite_value
    )
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit created for concept '{rope_value}' with rcontext '{rcontext_value}'. rconcept_active_requisite={rconcept_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reasonunit_INSERT_Without_rconcept_active_requisite():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reasonunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    rcontext_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, INSERT_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit created for concept '{rope_value}' with rcontext '{rcontext_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reasonunit_UPDATE_rconcept_active_requisite_IsTrue():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reasonunit_str()
    rcontext_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    rconcept_active_requisite_value = True
    swim_planatom = planatom_shop(dimen, UPDATE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    swim_planatom.set_arg(
        rconcept_active_requisite_str(), rconcept_active_requisite_value
    )
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit rcontext='{rcontext_value}' for concept '{rope_value}' set with rconcept_active_requisite={rconcept_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reasonunit_UPDATE_rconcept_active_requisite_IsNone():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reasonunit_str()
    rcontext_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    swim_planatom = planatom_shop(dimen, UPDATE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit rcontext='{rcontext_value}' for concept '{rope_value}' and no longer checks rcontext active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reasonunit_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reasonunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    rcontext_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, DELETE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit rcontext='{rcontext_value}' for concept '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
