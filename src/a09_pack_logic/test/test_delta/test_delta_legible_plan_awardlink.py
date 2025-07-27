from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    awardee_title_str,
    believer_plan_awardlink_str,
    give_force_str,
    plan_rope_str,
    take_force_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_awardlink_INSERT():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_awardlink_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_believer.knot}Swimmers"
    give_force_value = 81
    take_force_value = 43
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(awardee_title_str(), awardee_title_value)
    swim_believeratom.set_arg(give_force_str(), give_force_value)
    swim_believeratom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"Awardlink created for group {awardee_title_value} for plan '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardlink_UPDATE_give_force_take_force():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")

    dimen = believer_plan_awardlink_str()
    awardee_title_value = f"{sue_believer.knot}Swimmers"
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    take_force_value = 43
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(awardee_title_str(), awardee_title_value)
    swim_believeratom.set_arg(give_force_str(), give_force_value)
    swim_believeratom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardlink_UPDATE_give_force():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_awardlink_str()
    awardee_title_value = f"{sue_believer.knot}Swimmers"
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(awardee_title_str(), awardee_title_value)
    swim_believeratom.set_arg(give_force_str(), give_force_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardlink_UPDATE_take_force():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_awardlink_str()
    awardee_title_value = f"{sue_believer.knot}Swimmers"
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")

    take_force_value = 81
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(awardee_title_str(), awardee_title_value)
    swim_believeratom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for plan '{rope_value}'. Now take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardlink_DELETE():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_awardlink_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_believer.knot}Swimmers"
    swim_believeratom = believeratom_shop(dimen, DELETE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(awardee_title_str(), awardee_title_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"Awardlink for group {awardee_title_value}, plan '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
