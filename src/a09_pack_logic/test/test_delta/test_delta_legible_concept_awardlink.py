from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.a06_str import (
    awardee_title_str,
    concept_rope_str,
    give_force_str,
    plan_concept_awardlink_str,
    take_force_str,
)
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a08_plan_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import plandelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_awardlink_INSERT():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_awardlink_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    give_force_value = 81
    take_force_value = 43
    swim_planatom = planatom_shop(dimen, INSERT_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_planatom.set_arg(give_force_str(), give_force_value)
    swim_planatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Awardlink created for group {awardee_title_value} for concept '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_UPDATE_give_force_take_force():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")

    dimen = plan_concept_awardlink_str()
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    take_force_value = 43
    swim_planatom = planatom_shop(dimen, UPDATE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_planatom.set_arg(give_force_str(), give_force_value)
    swim_planatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_UPDATE_give_force():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_awardlink_str()
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    swim_planatom = planatom_shop(dimen, UPDATE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_planatom.set_arg(give_force_str(), give_force_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{rope_value}'. Now give_force={give_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_UPDATE_take_force():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_awardlink_str()
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")

    take_force_value = 81
    swim_planatom = planatom_shop(dimen, UPDATE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_planatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{rope_value}'. Now take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_awardlink_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, DELETE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(awardee_title_str(), awardee_title_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Awardlink for group {awardee_title_value}, concept '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
