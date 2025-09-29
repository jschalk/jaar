from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_keywords import (
    Ch01Keywords as wx,
    Ch06Keywords as wx,
    Ch09Keywords as wx,
    belief_planunit_str,
    denom_str,
    morph_str,
    numor_str,
    plan_rope_str,
    pledge_str,
    star_str,
)
from src.ch10_pack_logic.delta import beliefdelta_shop
from src.ch10_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_planunit_INSERT():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_planunit_str()
    _problem_bool_str = "problem_bool"
    clean_label = "clean fridge"
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    star_value = 43
    pledge_value = False
    clean_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    clean_beliefatom.set_arg(plan_rope_str(), clean_rope)
    clean_beliefatom.set_arg(wx.addin, addin_value)
    clean_beliefatom.set_arg(wx.begin, begin_value)
    clean_beliefatom.set_arg(wx.close, close_value)
    clean_beliefatom.set_arg(denom_str(), denom_value)
    clean_beliefatom.set_arg(numor_str(), numor_value)
    clean_beliefatom.set_arg(_problem_bool_str, problem_bool_value)
    clean_beliefatom.set_arg(morph_str(), morph_value)
    clean_beliefatom.set_arg(star_str(), star_value)
    clean_beliefatom.set_arg(pledge_str(), pledge_value)

    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(clean_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Created Plan '{clean_rope}'. addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.star={star_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_planunit_UPDATE():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_planunit_str()
    _problem_bool_str = "problem_bool"
    clean_label = "clean fridge"
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    star_value = 43
    pledge_value = False
    clean_beliefatom = beliefatom_shop(dimen, wx.UPDATE)
    clean_beliefatom.set_arg(plan_rope_str(), clean_rope)
    clean_beliefatom.set_arg(wx.addin, addin_value)
    clean_beliefatom.set_arg(wx.begin, begin_value)
    clean_beliefatom.set_arg(wx.close, close_value)
    clean_beliefatom.set_arg(denom_str(), denom_value)
    clean_beliefatom.set_arg(numor_str(), numor_value)
    clean_beliefatom.set_arg(_problem_bool_str, problem_bool_value)
    clean_beliefatom.set_arg(morph_str(), morph_value)
    clean_beliefatom.set_arg(star_str(), star_value)
    clean_beliefatom.set_arg(pledge_str(), pledge_value)

    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(clean_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Plan '{clean_rope}' set these attributes: addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.star={star_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_planunit_DELETE():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_planunit_str()
    clean_label = "clean fridge"
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_rope(casa_rope, clean_label)
    clean_beliefatom = beliefatom_shop(dimen, wx.DELETE)
    clean_beliefatom.set_arg(plan_rope_str(), clean_rope)

    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(clean_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Plan '{clean_rope}' was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
