from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_keywords import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    awardee_title_str,
    belief_plan_awardunit_str,
    give_force_str,
    plan_rope_str,
    take_force_str,
)
from src.ch10_pack_logic.delta import beliefdelta_shop
from src.ch10_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_awardunit_INSERT():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_awardunit_str()
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_belief.knot}Swimmers"
    give_force_value = 81
    take_force_value = 43
    swim_beliefatom = beliefatom_shop(dimen, INSERT_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_beliefatom.set_arg(give_force_str(), give_force_value)
    swim_beliefatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"AwardUnit created for group {awardee_title_value} for plan '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardunit_UPDATE_give_force_take_force():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")

    dimen = belief_plan_awardunit_str()
    awardee_title_value = f"{sue_belief.knot}Swimmers"
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    take_force_value = 43
    swim_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_beliefatom.set_arg(give_force_str(), give_force_value)
    swim_beliefatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardunit_UPDATE_give_force():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_awardunit_str()
    awardee_title_value = f"{sue_belief.knot}Swimmers"
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    swim_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_beliefatom.set_arg(give_force_str(), give_force_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardunit_UPDATE_take_force():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_awardunit_str()
    awardee_title_value = f"{sue_belief.knot}Swimmers"
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")

    take_force_value = 81
    swim_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_beliefatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardunit_DELETE():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_awardunit_str()
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_belief.knot}Swimmers"
    swim_beliefatom = beliefatom_shop(dimen, DELETE_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(awardee_title_str(), awardee_title_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"AwardUnit for group {awardee_title_value}, plan '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
