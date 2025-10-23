from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_belief_atom.atom_main import beliefatom_shop
from src.ch09_belief_lesson.delta import beliefdelta_shop
from src.ch09_belief_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_plan_reasonunit_INSERT_With_active_requisite():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_plan_reasonunit
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    reason_context_value = f"{sue_belief.knot}Swimmers"
    active_requisite_value = True
    swim_beliefatom = beliefatom_shop(dimen, kw.INSERT)
    swim_beliefatom.set_arg(kw.plan_rope, rope_value)
    swim_beliefatom.set_arg(kw.reason_context, reason_context_value)
    swim_beliefatom.set_arg(kw.active_requisite, active_requisite_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"ReasonUnit created for plan '{rope_value}' with reason_context '{reason_context_value}'. active_requisite={active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_INSERT_Without_active_requisite():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_plan_reasonunit
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    reason_context_value = f"{sue_belief.knot}Swimmers"
    swim_beliefatom = beliefatom_shop(dimen, kw.INSERT)
    swim_beliefatom.set_arg(kw.plan_rope, rope_value)
    swim_beliefatom.set_arg(kw.reason_context, reason_context_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"ReasonUnit created for plan '{rope_value}' with reason_context '{reason_context_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_UPDATE_active_requisite_IsTrue():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_plan_reasonunit
    reason_context_value = f"{sue_belief.knot}Swimmers"
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    active_requisite_value = True
    swim_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    swim_beliefatom.set_arg(kw.plan_rope, rope_value)
    swim_beliefatom.set_arg(kw.reason_context, reason_context_value)
    swim_beliefatom.set_arg(kw.active_requisite, active_requisite_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' set with active_requisite={active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_UPDATE_active_requisite_IsNone():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_plan_reasonunit
    reason_context_value = f"{sue_belief.knot}Swimmers"
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    swim_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    swim_beliefatom.set_arg(kw.plan_rope, rope_value)
    swim_beliefatom.set_arg(kw.reason_context, reason_context_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' and no longer checks reason_context active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_DELETE():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_plan_reasonunit
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    reason_context_value = f"{sue_belief.knot}Swimmers"
    swim_beliefatom = beliefatom_shop(dimen, kw.DELETE)
    swim_beliefatom.set_arg(kw.plan_rope, rope_value)
    swim_beliefatom.set_arg(kw.reason_context, reason_context_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
