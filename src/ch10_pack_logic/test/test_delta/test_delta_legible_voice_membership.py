from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_keywords import (
    Ch01Keywords as wx,
    Ch04Keywords as wx,
    Ch09Keywords as wx,
    DELETE_str,
    belief_voice_membership_str,
)
from src.ch10_pack_logic.delta import beliefdelta_shop
from src.ch10_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_voice_membership_INSERT():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_voice_membership_str()
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    group_cred_points_value = 81
    group_debt_points_value = 43
    yao_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    yao_beliefatom.set_arg(wx.group_title, swim_str)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    yao_beliefatom.set_arg(wx.group_cred_points, group_cred_points_value)
    yao_beliefatom.set_arg(wx.group_debt_points, group_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' has new membership {yao_str} with group_cred_points_value{group_cred_points_value} and group_debt_points_value={group_debt_points_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voice_membership_UPDATE_group_cred_points_group_debt_points():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_voice_membership_str()
    group_cred_points_str = "group_cred_points"
    group_debt_points_str = "group_debt_points"
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    group_cred_points_value = 81
    group_debt_points_value = 43
    yao_beliefatom = beliefatom_shop(dimen, wx.UPDATE)
    yao_beliefatom.set_arg(wx.group_title, swim_str)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    yao_beliefatom.set_arg(group_cred_points_str, group_cred_points_value)
    yao_beliefatom.set_arg(group_debt_points_str, group_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new group_cred_points_value{group_cred_points_value} and group_debt_points_value={group_debt_points_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voice_membership_UPDATE_group_cred_points():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_voice_membership_str()
    group_cred_points_str = "group_cred_points"
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    group_cred_points_value = 81
    yao_beliefatom = beliefatom_shop(dimen, wx.UPDATE)
    yao_beliefatom.set_arg(wx.group_title, swim_str)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    yao_beliefatom.set_arg(group_cred_points_str, group_cred_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new group_cred_points_value{group_cred_points_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voice_membership_UPDATE_group_debt_points():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_voice_membership_str()
    group_debt_points_str = "group_debt_points"
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    group_debt_points_value = 43
    yao_beliefatom = beliefatom_shop(dimen, wx.UPDATE)
    yao_beliefatom.set_arg(wx.group_title, swim_str)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    yao_beliefatom.set_arg(group_debt_points_str, group_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new group_debt_points_value={group_debt_points_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voice_membership_DELETE():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_voice_membership_str()
    swim_str = f"{sue_belief.knot}Swimmers"
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, DELETE_str())
    yao_beliefatom.set_arg(wx.group_title, swim_str)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"Group '{swim_str}' no longer has membership {yao_str}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
