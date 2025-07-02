from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    owner_plan_reasonunit_str,
    plan_rope_str,
    rcontext_str,
    rplan_active_requisite_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import ownerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_reasonunit_INSERT_With_rplan_active_requisite():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reasonunit_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    rcontext_value = f"{sue_owner.knot}Swimmers"
    rplan_active_requisite_value = True
    swim_owneratom = owneratom_shop(dimen, INSERT_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    swim_owneratom.set_arg(rplan_active_requisite_str(), rplan_active_requisite_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"ReasonUnit created for plan '{rope_value}' with rcontext '{rcontext_value}'. rplan_active_requisite={rplan_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_INSERT_Without_rplan_active_requisite():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reasonunit_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    rcontext_value = f"{sue_owner.knot}Swimmers"
    swim_owneratom = owneratom_shop(dimen, INSERT_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = (
        f"ReasonUnit created for plan '{rope_value}' with rcontext '{rcontext_value}'."
    )
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_UPDATE_rplan_active_requisite_IsTrue():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reasonunit_str()
    rcontext_value = f"{sue_owner.knot}Swimmers"
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    rplan_active_requisite_value = True
    swim_owneratom = owneratom_shop(dimen, UPDATE_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    swim_owneratom.set_arg(rplan_active_requisite_str(), rplan_active_requisite_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"ReasonUnit rcontext='{rcontext_value}' for plan '{rope_value}' set with rplan_active_requisite={rplan_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_UPDATE_rplan_active_requisite_IsNone():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reasonunit_str()
    rcontext_value = f"{sue_owner.knot}Swimmers"
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    swim_owneratom = owneratom_shop(dimen, UPDATE_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"ReasonUnit rcontext='{rcontext_value}' for plan '{rope_value}' and no longer checks rcontext active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_DELETE():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reasonunit_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    rcontext_value = f"{sue_owner.knot}Swimmers"
    swim_owneratom = owneratom_shop(dimen, DELETE_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"ReasonUnit rcontext='{rcontext_value}' for plan '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
