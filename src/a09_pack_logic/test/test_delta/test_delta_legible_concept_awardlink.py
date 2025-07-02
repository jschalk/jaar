from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    awardee_title_str,
    concept_rope_str,
    give_force_str,
    owner_concept_awardlink_str,
    take_force_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import ownerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_awardlink_INSERT():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_concept_awardlink_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_owner.knot}Swimmers"
    give_force_value = 81
    take_force_value = 43
    swim_owneratom = owneratom_shop(dimen, INSERT_str())
    swim_owneratom.set_arg(concept_rope_str(), rope_value)
    swim_owneratom.set_arg(awardee_title_str(), awardee_title_value)
    swim_owneratom.set_arg(give_force_str(), give_force_value)
    swim_owneratom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Awardlink created for group {awardee_title_value} for concept '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_UPDATE_give_force_take_force():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")

    dimen = owner_concept_awardlink_str()
    awardee_title_value = f"{sue_owner.knot}Swimmers"
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    take_force_value = 43
    swim_owneratom = owneratom_shop(dimen, UPDATE_str())
    swim_owneratom.set_arg(concept_rope_str(), rope_value)
    swim_owneratom.set_arg(awardee_title_str(), awardee_title_value)
    swim_owneratom.set_arg(give_force_str(), give_force_value)
    swim_owneratom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_UPDATE_give_force():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_concept_awardlink_str()
    awardee_title_value = f"{sue_owner.knot}Swimmers"
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    swim_owneratom = owneratom_shop(dimen, UPDATE_str())
    swim_owneratom.set_arg(concept_rope_str(), rope_value)
    swim_owneratom.set_arg(awardee_title_str(), awardee_title_value)
    swim_owneratom.set_arg(give_force_str(), give_force_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{rope_value}'. Now give_force={give_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_UPDATE_take_force():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_concept_awardlink_str()
    awardee_title_value = f"{sue_owner.knot}Swimmers"
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")

    take_force_value = 81
    swim_owneratom = owneratom_shop(dimen, UPDATE_str())
    swim_owneratom.set_arg(concept_rope_str(), rope_value)
    swim_owneratom.set_arg(awardee_title_str(), awardee_title_value)
    swim_owneratom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{rope_value}'. Now take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_DELETE():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_concept_awardlink_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_owner.knot}Swimmers"
    swim_owneratom = owneratom_shop(dimen, DELETE_str())
    swim_owneratom.set_arg(concept_rope_str(), rope_value)
    swim_owneratom.set_arg(awardee_title_str(), awardee_title_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Awardlink for group {awardee_title_value}, concept '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
