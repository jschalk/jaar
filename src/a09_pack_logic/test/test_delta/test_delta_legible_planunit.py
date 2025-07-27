from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    addin_str,
    begin_str,
    believer_planunit_str,
    close_str,
    denom_str,
    mass_str,
    morph_str,
    numor_str,
    plan_rope_str,
    task_str,
)
from src.a08_believer_atom_logic.atom_main import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_planunit_INSERT():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_planunit_str()
    _problem_bool_str = "problem_bool"
    clean_label = "clean fridge"
    casa_rope = sue_believer.make_l1_rope("casa")
    clean_rope = sue_believer.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    mass_value = 43
    task_value = False
    clean_believeratom = believeratom_shop(dimen, INSERT_str())
    clean_believeratom.set_arg(plan_rope_str(), clean_rope)
    clean_believeratom.set_arg(addin_str(), addin_value)
    clean_believeratom.set_arg(begin_str(), begin_value)
    clean_believeratom.set_arg(close_str(), close_value)
    clean_believeratom.set_arg(denom_str(), denom_value)
    clean_believeratom.set_arg(numor_str(), numor_value)
    clean_believeratom.set_arg(_problem_bool_str, problem_bool_value)
    clean_believeratom.set_arg(morph_str(), morph_value)
    clean_believeratom.set_arg(mass_str(), mass_value)
    clean_believeratom.set_arg(task_str(), task_value)

    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(clean_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"Created Plan '{clean_rope}'. addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.mass={mass_value}.task={task_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_planunit_UPDATE():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_planunit_str()
    _problem_bool_str = "problem_bool"
    clean_label = "clean fridge"
    casa_rope = sue_believer.make_l1_rope("casa")
    clean_rope = sue_believer.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    mass_value = 43
    task_value = False
    clean_believeratom = believeratom_shop(dimen, UPDATE_str())
    clean_believeratom.set_arg(plan_rope_str(), clean_rope)
    clean_believeratom.set_arg(addin_str(), addin_value)
    clean_believeratom.set_arg(begin_str(), begin_value)
    clean_believeratom.set_arg(close_str(), close_value)
    clean_believeratom.set_arg(denom_str(), denom_value)
    clean_believeratom.set_arg(numor_str(), numor_value)
    clean_believeratom.set_arg(_problem_bool_str, problem_bool_value)
    clean_believeratom.set_arg(morph_str(), morph_value)
    clean_believeratom.set_arg(mass_str(), mass_value)
    clean_believeratom.set_arg(task_str(), task_value)

    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(clean_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"Plan '{clean_rope}' set these attributes: addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.mass={mass_value}.task={task_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_planunit_DELETE():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_planunit_str()
    clean_label = "clean fridge"
    casa_rope = sue_believer.make_l1_rope("casa")
    clean_rope = sue_believer.make_rope(casa_rope, clean_label)
    clean_believeratom = believeratom_shop(dimen, DELETE_str())
    clean_believeratom.set_arg(plan_rope_str(), clean_rope)

    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(clean_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"Plan '{clean_rope}' was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
