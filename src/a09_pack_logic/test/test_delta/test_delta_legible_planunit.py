from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    addin_str,
    begin_str,
    close_str,
    denom_str,
    mass_str,
    morph_str,
    numor_str,
    owner_planunit_str,
    plan_rope_str,
    task_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import ownerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_planunit_INSERT():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_planunit_str()
    _problem_bool_str = "problem_bool"
    clean_label = "clean fridge"
    casa_rope = sue_owner.make_l1_rope("casa")
    clean_rope = sue_owner.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    mass_value = 43
    task_value = False
    clean_owneratom = owneratom_shop(dimen, INSERT_str())
    clean_owneratom.set_arg(plan_rope_str(), clean_rope)
    clean_owneratom.set_arg(addin_str(), addin_value)
    clean_owneratom.set_arg(begin_str(), begin_value)
    clean_owneratom.set_arg(close_str(), close_value)
    clean_owneratom.set_arg(denom_str(), denom_value)
    clean_owneratom.set_arg(numor_str(), numor_value)
    clean_owneratom.set_arg(_problem_bool_str, problem_bool_value)
    clean_owneratom.set_arg(morph_str(), morph_value)
    clean_owneratom.set_arg(mass_str(), mass_value)
    clean_owneratom.set_arg(task_str(), task_value)

    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(clean_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Created Plan '{clean_rope}'. addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.mass={mass_value}.task={task_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_planunit_UPDATE():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_planunit_str()
    _problem_bool_str = "problem_bool"
    clean_label = "clean fridge"
    casa_rope = sue_owner.make_l1_rope("casa")
    clean_rope = sue_owner.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    mass_value = 43
    task_value = False
    clean_owneratom = owneratom_shop(dimen, UPDATE_str())
    clean_owneratom.set_arg(plan_rope_str(), clean_rope)
    clean_owneratom.set_arg(addin_str(), addin_value)
    clean_owneratom.set_arg(begin_str(), begin_value)
    clean_owneratom.set_arg(close_str(), close_value)
    clean_owneratom.set_arg(denom_str(), denom_value)
    clean_owneratom.set_arg(numor_str(), numor_value)
    clean_owneratom.set_arg(_problem_bool_str, problem_bool_value)
    clean_owneratom.set_arg(morph_str(), morph_value)
    clean_owneratom.set_arg(mass_str(), mass_value)
    clean_owneratom.set_arg(task_str(), task_value)

    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(clean_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Plan '{clean_rope}' set these attributes: addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.mass={mass_value}.task={task_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_planunit_DELETE():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_planunit_str()
    clean_label = "clean fridge"
    casa_rope = sue_owner.make_l1_rope("casa")
    clean_rope = sue_owner.make_rope(casa_rope, clean_label)
    clean_owneratom = owneratom_shop(dimen, DELETE_str())
    clean_owneratom.set_arg(plan_rope_str(), clean_rope)

    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(clean_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Plan '{clean_rope}' was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
