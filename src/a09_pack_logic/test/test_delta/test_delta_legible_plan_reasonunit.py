from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_plan_reasonunit_str,
    plan_rope_str,
    r_context_str,
    r_plan_active_requisite_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_reasonunit_INSERT_With_r_plan_active_requisite():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reasonunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    r_context_value = f"{sue_believer.knot}Swimmers"
    r_plan_active_requisite_value = True
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(r_context_str(), r_context_value)
    swim_believeratom.set_arg(
        r_plan_active_requisite_str(), r_plan_active_requisite_value
    )
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"ReasonUnit created for plan '{rope_value}' with r_context '{r_context_value}'. r_plan_active_requisite={r_plan_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_INSERT_Without_r_plan_active_requisite():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reasonunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    r_context_value = f"{sue_believer.knot}Swimmers"
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(r_context_str(), r_context_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"ReasonUnit created for plan '{rope_value}' with r_context '{r_context_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_UPDATE_r_plan_active_requisite_IsTrue():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reasonunit_str()
    r_context_value = f"{sue_believer.knot}Swimmers"
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    r_plan_active_requisite_value = True
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(r_context_str(), r_context_value)
    swim_believeratom.set_arg(
        r_plan_active_requisite_str(), r_plan_active_requisite_value
    )
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"ReasonUnit r_context='{r_context_value}' for plan '{rope_value}' set with r_plan_active_requisite={r_plan_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_UPDATE_r_plan_active_requisite_IsNone():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reasonunit_str()
    r_context_value = f"{sue_believer.knot}Swimmers"
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(r_context_str(), r_context_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"ReasonUnit r_context='{r_context_value}' for plan '{rope_value}' and no longer checks r_context active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_DELETE():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reasonunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    r_context_value = f"{sue_believer.knot}Swimmers"
    swim_believeratom = believeratom_shop(dimen, DELETE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(r_context_str(), r_context_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"ReasonUnit r_context='{r_context_value}' for plan '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
