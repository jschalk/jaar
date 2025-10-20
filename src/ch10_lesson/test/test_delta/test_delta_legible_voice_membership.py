from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom.atom_main import beliefatom_shop
from src.ch10_lesson.delta import beliefdelta_shop
from src.ch10_lesson.legible import create_legible_list
from src.ref.keywords import Ch10Keywords as kw


def test_create_legible_list_ReturnsObj_voice_membership_INSERT():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_voice_membership
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    group_cred_lumen_value = 81
    group_debt_lumen_value = 43
    yao_beliefatom = beliefatom_shop(dimen, kw.INSERT)
    yao_beliefatom.set_arg(kw.group_title, swim_str)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    yao_beliefatom.set_arg(kw.group_cred_lumen, group_cred_lumen_value)
    yao_beliefatom.set_arg(kw.group_debt_lumen, group_debt_lumen_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' has new membership {yao_str} with group_cred_lumen_value{group_cred_lumen_value} and group_debt_lumen_value={group_debt_lumen_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voice_membership_UPDATE_group_cred_lumen_group_debt_lumen():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_voice_membership
    group_cred_lumen_str = "group_cred_lumen"
    group_debt_lumen_str = "group_debt_lumen"
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    group_cred_lumen_value = 81
    group_debt_lumen_value = 43
    yao_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    yao_beliefatom.set_arg(kw.group_title, swim_str)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    yao_beliefatom.set_arg(group_cred_lumen_str, group_cred_lumen_value)
    yao_beliefatom.set_arg(group_debt_lumen_str, group_debt_lumen_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new group_cred_lumen_value{group_cred_lumen_value} and group_debt_lumen_value={group_debt_lumen_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voice_membership_UPDATE_group_cred_lumen():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_voice_membership
    group_cred_lumen_str = "group_cred_lumen"
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    group_cred_lumen_value = 81
    yao_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    yao_beliefatom.set_arg(kw.group_title, swim_str)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    yao_beliefatom.set_arg(group_cred_lumen_str, group_cred_lumen_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new group_cred_lumen_value{group_cred_lumen_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voice_membership_UPDATE_group_debt_lumen():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_voice_membership
    group_debt_lumen_str = "group_debt_lumen"
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    group_debt_lumen_value = 43
    yao_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    yao_beliefatom.set_arg(kw.group_title, swim_str)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    yao_beliefatom.set_arg(group_debt_lumen_str, group_debt_lumen_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new group_debt_lumen_value={group_debt_lumen_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voice_membership_DELETE():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = kw.belief_voice_membership
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, kw.DELETE)
    yao_beliefatom.set_arg(kw.group_title, swim_str)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' no longer has membership {yao_str}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
