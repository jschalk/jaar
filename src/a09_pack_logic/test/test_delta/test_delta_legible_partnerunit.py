from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import (
    belief_partnerunit_str,
    partner_name_str,
)
from src.a08_belief_atom_logic.atom_main import beliefatom_shop
from src.a08_belief_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import beliefdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_partnerunit_INSERT():
    # ESTABLISH
    dimen = belief_partnerunit_str()
    partner_cred_points_str = "partner_cred_points"
    partner_debt_points_str = "partner_debt_points"
    partner_cred_points_value = 81
    partner_debt_points_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, INSERT_str())
    yao_beliefatom.set_arg(partner_name_str(), yao_str)
    yao_beliefatom.set_arg(partner_cred_points_str, partner_cred_points_value)
    yao_beliefatom.set_arg(partner_debt_points_str, partner_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} was added with {partner_cred_points_value} score credit and {partner_debt_points_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_INSERT_score():
    # ESTABLISH
    dimen = belief_partnerunit_str()
    partner_cred_points_str = "partner_cred_points"
    partner_debt_points_str = "partner_debt_points"
    partner_cred_points_value = 81
    partner_debt_points_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, INSERT_str())
    yao_beliefatom.set_arg(partner_name_str(), yao_str)
    yao_beliefatom.set_arg(partner_cred_points_str, partner_cred_points_value)
    yao_beliefatom.set_arg(partner_debt_points_str, partner_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} was added with {partner_cred_points_value} score credit and {partner_debt_points_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_UPDATE_partner_cred_points_partner_debt_points():
    # ESTABLISH
    dimen = belief_partnerunit_str()
    partner_cred_points_str = "partner_cred_points"
    partner_debt_points_str = "partner_debt_points"
    partner_cred_points_value = 81
    partner_debt_points_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    yao_beliefatom.set_arg(partner_name_str(), yao_str)
    yao_beliefatom.set_arg(partner_cred_points_str, partner_cred_points_value)
    yao_beliefatom.set_arg(partner_debt_points_str, partner_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} now has {partner_cred_points_value} score credit and {partner_debt_points_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_UPDATE_partner_cred_points():
    # ESTABLISH
    dimen = belief_partnerunit_str()
    partner_cred_points_str = "partner_cred_points"
    partner_cred_points_value = 81
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    yao_beliefatom.set_arg(partner_name_str(), yao_str)
    yao_beliefatom.set_arg(partner_cred_points_str, partner_cred_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} now has {partner_cred_points_value} score credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_UPDATE_partner_debt_points():
    # ESTABLISH
    dimen = belief_partnerunit_str()
    partner_debt_points_str = "partner_debt_points"
    partner_debt_points_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    yao_beliefatom.set_arg(partner_name_str(), yao_str)
    yao_beliefatom.set_arg(partner_debt_points_str, partner_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} now has {partner_debt_points_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_DELETE():
    # ESTABLISH
    dimen = belief_partnerunit_str()
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, DELETE_str())
    yao_beliefatom.set_arg(partner_name_str(), yao_str)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} was removed from score partners."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
