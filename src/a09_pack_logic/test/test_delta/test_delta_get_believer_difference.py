from copy import deepcopy as copy_deepcopy
from src.a00_data_toolbox.dict_toolbox import (
    get_empty_list_if_None,
    get_from_nested_dict,
)
from src.a03_group_logic.group import awardlink_shop
from src.a03_group_logic.partner import partnerunit_shop
from src.a04_reason_logic.reason_plan import factunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    awardee_title_str,
    begin_str,
    believer_partner_membership_str,
    believer_partnerunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_caseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    believerunit_str,
    close_str,
    f_context_str,
    f_lower_str,
    f_state_str,
    f_upper_str,
    give_force_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    mass_str,
    partner_name_str,
    plan_rope_str,
    r_plan_active_requisite_str,
    take_force_str,
    task_str,
)
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_with_4_levels,
)
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import BelieverDelta, believerdelta_shop


def print_believeratom_keys(x_believerdelta: BelieverDelta):
    for x_believeratom in get_delete_believeratom_list(x_believerdelta):
        print(f"DELETE {x_believeratom.dimen} {list(x_believeratom.jkeys.values())}")
    for x_believeratom in get_update_believeratom_list(x_believerdelta):
        print(f"UPDATE {x_believeratom.dimen} {list(x_believeratom.jkeys.values())}")
    for x_believeratom in get_insert_believeratom_list(x_believerdelta):
        print(f"INSERT {x_believeratom.dimen} {list(x_believeratom.jkeys.values())}")


def get_delete_believeratom_list(x_believerdelta: BelieverDelta) -> list:
    return get_empty_list_if_None(
        x_believerdelta._get_crud_believeratoms_list().get(DELETE_str())
    )


def get_insert_believeratom_list(x_believerdelta: BelieverDelta):
    return get_empty_list_if_None(
        x_believerdelta._get_crud_believeratoms_list().get(INSERT_str())
    )


def get_update_believeratom_list(x_believerdelta: BelieverDelta):
    return get_empty_list_if_None(
        x_believerdelta._get_crud_believeratoms_list().get(UPDATE_str())
    )


def get_believeratom_total_count(x_believerdelta: BelieverDelta) -> int:
    return (
        len(get_delete_believeratom_list(x_believerdelta))
        + len(get_insert_believeratom_list(x_believerdelta))
        + len(get_update_believeratom_list(x_believerdelta))
    )


def test_BelieverDelta_create_believeratoms_EmptyBelievers():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    sue_believerdelta = believerdelta_shop()
    assert sue_believerdelta.believeratoms == {}

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(sue_believer, sue_believer)

    # THEN
    assert sue_believerdelta.believeratoms == {}


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_partnerunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    after_sue_believer = copy_deepcopy(before_sue_believer)
    xio_str = "Xio"
    xio_partner_cred_points = 33
    xio_partner_debt_points = 44
    xio_partnerunit = partnerunit_shop(
        xio_str, xio_partner_cred_points, xio_partner_debt_points
    )
    after_sue_believer.set_partnerunit(xio_partnerunit, auto_set_membership=False)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    assert (
        len(
            sue_believerdelta.believeratoms.get(INSERT_str()).get(
                believer_partnerunit_str()
            )
        )
        == 1
    )
    sue_insert_dict = sue_believerdelta.believeratoms.get(INSERT_str())
    sue_partnerunit_dict = sue_insert_dict.get(believer_partnerunit_str())
    xio_believeratom = sue_partnerunit_dict.get(xio_str)
    assert xio_believeratom.get_value(partner_name_str()) == xio_str
    assert xio_believeratom.get_value("partner_cred_points") == xio_partner_cred_points
    assert xio_believeratom.get_value("partner_debt_points") == xio_partner_debt_points

    print(f"{get_believeratom_total_count(sue_believerdelta)=}")
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_partnerunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    before_sue_believer.add_partnerunit("Yao")
    before_sue_believer.add_partnerunit("Zia")

    after_sue_believer = copy_deepcopy(before_sue_believer)

    xio_str = "Xio"
    before_sue_believer.add_partnerunit(xio_str)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    xio_believeratom = get_from_nested_dict(
        sue_believerdelta.believeratoms,
        [DELETE_str(), believer_partnerunit_str(), xio_str],
    )
    assert xio_believeratom.get_value(partner_name_str()) == xio_str

    print(f"{get_believeratom_total_count(sue_believerdelta)=}")
    print_believeratom_keys(sue_believerdelta)
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_partnerunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    after_sue_believer = copy_deepcopy(before_sue_believer)
    xio_str = "Xio"
    before_sue_believer.add_partnerunit(xio_str)
    xio_partner_cred_points = 33
    xio_partner_debt_points = 44
    after_sue_believer.add_partnerunit(
        xio_str, xio_partner_cred_points, xio_partner_debt_points
    )

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    x_keylist = [UPDATE_str(), believer_partnerunit_str(), xio_str]
    xio_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert xio_believeratom.get_value(partner_name_str()) == xio_str
    assert xio_believeratom.get_value("partner_cred_points") == xio_partner_cred_points
    assert xio_believeratom.get_value("partner_debt_points") == xio_partner_debt_points

    print(f"{get_believeratom_total_count(sue_believerdelta)=}")
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_BelieverUnit_simple_attrs_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    after_sue_believer = copy_deepcopy(before_sue_believer)
    x_believerunit_tally = 55
    x_fund_pool = 8000000
    x_fund_iota = 8
    x_respect_bit = 5
    x_max_tree_traverse = 66
    x_credor_respect = 770
    x_debtor_respect = 880
    after_sue_believer.tally = x_believerunit_tally
    after_sue_believer.fund_pool = x_fund_pool
    after_sue_believer.fund_iota = x_fund_iota
    after_sue_believer.respect_bit = x_respect_bit
    after_sue_believer.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_believer.set_credor_respect(x_credor_respect)
    after_sue_believer.set_debtor_respect(x_debtor_respect)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    x_keylist = [UPDATE_str(), believerunit_str()]
    xio_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert xio_believeratom.get_value("max_tree_traverse") == x_max_tree_traverse
    assert xio_believeratom.get_value("credor_respect") == x_credor_respect
    assert xio_believeratom.get_value("debtor_respect") == x_debtor_respect
    assert xio_believeratom.get_value("tally") == x_believerunit_tally
    assert xio_believeratom.get_value("fund_pool") == x_fund_pool
    assert xio_believeratom.get_value("fund_iota") == x_fund_iota
    assert xio_believeratom.get_value("respect_bit") == x_respect_bit

    print(f"{get_believeratom_total_count(sue_believerdelta)=}")
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_partner_membership_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    after_sue_believer = copy_deepcopy(before_sue_believer)
    yao_str = "Yao"
    zia_str = "Zia"
    temp_yao_partnerunit = partnerunit_shop(yao_str)
    temp_zia_partnerunit = partnerunit_shop(zia_str)
    after_sue_believer.set_partnerunit(temp_yao_partnerunit, auto_set_membership=False)
    after_sue_believer.set_partnerunit(temp_zia_partnerunit, auto_set_membership=False)
    after_yao_partnerunit = after_sue_believer.get_partner(yao_str)
    after_zia_partnerunit = after_sue_believer.get_partner(zia_str)
    run_str = ";runners"
    zia_run_credit_w = 77
    zia_run_debt_w = 88
    after_zia_partnerunit.add_membership(run_str, zia_run_credit_w, zia_run_debt_w)
    print(f"{after_sue_believer.get_partnerunit_group_titles_dict()=}")

    # WHEN
    sue_believerdelta = believerdelta_shop()
    print(f"{after_sue_believer.get_partner(zia_str)._memberships=}")
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )
    # print(f"{sue_believerdelta.believeratoms.get(INSERT_str()).keys()=}")
    # print(
    #     sue_believerdelta.believeratoms.get(INSERT_str()).get(believer_partner_membership_str()).keys()
    # )

    # THEN
    x_keylist = [INSERT_str(), believer_partnerunit_str(), yao_str]
    yao_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert yao_believeratom.get_value(partner_name_str()) == yao_str

    x_keylist = [INSERT_str(), believer_partnerunit_str(), zia_str]
    zia_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert zia_believeratom.get_value(partner_name_str()) == zia_str
    print(f"\n{sue_believerdelta.believeratoms=}")
    # print(f"\n{zia_believeratom=}")

    x_keylist = [INSERT_str(), believer_partner_membership_str(), zia_str, run_str]
    run_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert run_believeratom.get_value(partner_name_str()) == zia_str
    assert run_believeratom.get_value(group_title_str()) == run_str
    assert run_believeratom.get_value("group_cred_points") == zia_run_credit_w
    assert run_believeratom.get_value("group_debt_points") == zia_run_debt_w

    print_believeratom_keys(sue_believerdelta)
    print(f"{get_believeratom_total_count(sue_believerdelta)=}")
    assert len(get_delete_believeratom_list(sue_believerdelta)) == 0
    assert len(get_insert_believeratom_list(sue_believerdelta)) == 3
    assert len(get_delete_believeratom_list(sue_believerdelta)) == 0
    assert get_believeratom_total_count(sue_believerdelta) == 3


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_partner_membership_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    before_sue_believer.add_partnerunit(xio_str)
    before_sue_believer.add_partnerunit(zia_str)
    run_str = ";runners"
    before_xio_credit_w = 77
    before_xio_debt_w = 88
    before_xio_partner = before_sue_believer.get_partner(xio_str)
    before_xio_partner.add_membership(run_str, before_xio_credit_w, before_xio_debt_w)
    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_xio_partnerunit = after_sue_believer.get_partner(xio_str)
    after_xio_credit_w = 55
    after_xio_debt_w = 66
    after_xio_partnerunit.add_membership(run_str, after_xio_credit_w, after_xio_debt_w)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    # x_keylist = [UPDATE_str(), believer_partnerunit_str(), xio_str]
    # xio_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    # assert xio_believeratom.get_value(partner_name_str()) == xio_str
    # print(f"\n{sue_believerdelta.believeratoms=}")
    # print(f"\n{xio_believeratom=}")

    x_keylist = [UPDATE_str(), believer_partner_membership_str(), xio_str, run_str]
    xio_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert xio_believeratom.get_value(partner_name_str()) == xio_str
    assert xio_believeratom.get_value(group_title_str()) == run_str
    assert xio_believeratom.get_value("group_cred_points") == after_xio_credit_w
    assert xio_believeratom.get_value("group_debt_points") == after_xio_debt_w

    print(f"{get_believeratom_total_count(sue_believerdelta)=}")
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_partner_membership_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_believer.add_partnerunit(xio_str)
    before_sue_believer.add_partnerunit(zia_str)
    before_sue_believer.add_partnerunit(bob_str)
    before_xio_partnerunit = before_sue_believer.get_partner(xio_str)
    before_zia_partnerunit = before_sue_believer.get_partner(zia_str)
    before_bob_partnerunit = before_sue_believer.get_partner(bob_str)
    run_str = ";runners"
    before_xio_partnerunit.add_membership(run_str)
    before_zia_partnerunit.add_membership(run_str)
    fly_str = ";flyers"
    before_xio_partnerunit.add_membership(fly_str)
    before_zia_partnerunit.add_membership(fly_str)
    before_bob_partnerunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_believer.get_partnerunit_group_titles_dict()

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_xio_partnerunit = after_sue_believer.get_partner(xio_str)
    after_zia_partnerunit = after_sue_believer.get_partner(zia_str)
    after_bob_partnerunit = after_sue_believer.get_partner(bob_str)
    after_xio_partnerunit.delete_membership(run_str)
    after_zia_partnerunit.delete_membership(run_str)
    after_bob_partnerunit.delete_membership(fly_str)
    after_group_titles_dict = after_sue_believer.get_partnerunit_group_titles_dict()
    assert len(before_group_titles_dict.get(fly_str)) == 3
    assert len(before_group_titles_dict.get(run_str)) == 2
    assert len(after_group_titles_dict.get(fly_str)) == 2
    assert after_group_titles_dict.get(run_str) is None

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    x_keylist = [DELETE_str(), believer_partner_membership_str(), bob_str, fly_str]
    xio_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert xio_believeratom.get_value(partner_name_str()) == bob_str
    assert xio_believeratom.get_value(group_title_str()) == fly_str

    print(f"{get_believeratom_total_count(sue_believerdelta)=}")
    print_believeratom_keys(sue_believerdelta)
    assert len(get_delete_believeratom_list(sue_believerdelta)) == 3
    assert len(get_insert_believeratom_list(sue_believerdelta)) == 0
    assert len(get_update_believeratom_list(sue_believerdelta)) == 0
    assert get_believeratom_total_count(sue_believerdelta) == 3


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_believer.make_rope(ball_rope, street_str)
    before_sue_believer.set_plan(planunit_shop(street_str), ball_rope)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_believer.make_rope(sports_rope, disc_str)
    amy45_str = "amy45"
    before_sue_believer.set_l1_plan(planunit_shop(amy45_str))
    before_sue_believer.set_plan(planunit_shop(disc_str), sports_rope)
    # create after without ball_plan and street_plan
    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_sue_believer.del_plan_obj(ball_rope)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    x_dimen = believer_planunit_str()
    print(f"{sue_believerdelta.believeratoms.get(DELETE_str()).get(x_dimen).keys()=}")

    x_keylist = [DELETE_str(), believer_planunit_str(), street_rope]
    street_believeratom = get_from_nested_dict(
        sue_believerdelta.believeratoms, x_keylist
    )
    assert street_believeratom.get_value(plan_rope_str()) == street_rope

    x_keylist = [DELETE_str(), believer_planunit_str(), ball_rope]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope

    print(f"{get_believeratom_total_count(sue_believerdelta)=}")
    assert get_believeratom_total_count(sue_believerdelta) == 2


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_believer.make_rope(ball_rope, street_str)
    before_sue_believer.set_plan(planunit_shop(street_str), ball_rope)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    disc_str = "Ultimate Disc"
    disc_rope = after_sue_believer.make_rope(sports_rope, disc_str)
    after_sue_believer.set_plan(planunit_shop(disc_str), sports_rope)
    amy45_str = "amy45"
    amy_begin = 34
    amy_close = 78
    amy_mass = 55
    amy_task = True
    amy_rope = after_sue_believer.make_l1_rope(amy45_str)
    after_sue_believer.set_l1_plan(
        planunit_shop(
            amy45_str,
            begin=amy_begin,
            close=amy_close,
            mass=amy_mass,
            task=amy_task,
        )
    )

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print_believeratom_keys(sue_believerdelta)

    x_keylist = [INSERT_str(), believer_planunit_str(), disc_rope]
    street_believeratom = get_from_nested_dict(
        sue_believerdelta.believeratoms, x_keylist
    )
    assert street_believeratom.get_value(plan_rope_str()) == disc_rope

    a45_rope = after_sue_believer.make_l1_rope(amy45_str)
    x_keylist = [INSERT_str(), believer_planunit_str(), a45_rope]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == a45_rope
    assert ball_believeratom.get_value(begin_str()) == amy_begin
    assert ball_believeratom.get_value(close_str()) == amy_close
    assert ball_believeratom.get_value(mass_str()) == amy_mass
    assert ball_believeratom.get_value(task_str()) == amy_task

    assert get_believeratom_total_count(sue_believerdelta) == 2


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    amy45_str = "amy45"
    amy45_rope = before_sue_believer.make_l1_rope(amy45_str)
    before_amy_begin = 34
    before_amy_close = 78
    before_amy_mass = 55
    before_amy_task = True
    amy_rope = before_sue_believer.make_l1_rope(amy45_str)
    before_sue_believer.set_l1_plan(
        planunit_shop(
            amy45_str,
            begin=before_amy_begin,
            close=before_amy_close,
            mass=before_amy_mass,
            task=before_amy_task,
        )
    )

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_amy_begin = 99
    after_amy_close = 111
    after_amy_mass = 22
    after_amy_task = False
    after_sue_believer.edit_plan_attr(
        amy_rope,
        begin=after_amy_begin,
        close=after_amy_close,
        mass=after_amy_mass,
        task=after_amy_task,
    )

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print_believeratom_keys(sue_believerdelta)

    x_keylist = [UPDATE_str(), believer_planunit_str(), amy45_rope]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == amy45_rope
    assert ball_believeratom.get_value(begin_str()) == after_amy_begin
    assert ball_believeratom.get_value(close_str()) == after_amy_close
    assert ball_believeratom.get_value(mass_str()) == after_amy_mass
    assert ball_believeratom.get_value(task_str()) == after_amy_task

    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_awardlink_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_au.add_partnerunit(xio_str)
    before_sue_au.add_partnerunit(zia_str)
    before_sue_au.add_partnerunit(bob_str)
    xio_partnerunit = before_sue_au.get_partner(xio_str)
    zia_partnerunit = before_sue_au.get_partner(zia_str)
    bob_partnerunit = before_sue_au.get_partner(bob_str)
    run_str = ";runners"
    xio_partnerunit.add_membership(run_str)
    zia_partnerunit.add_membership(run_str)
    fly_str = ";flyers"
    xio_partnerunit.add_membership(fly_str)
    zia_partnerunit.add_membership(fly_str)
    bob_partnerunit.add_membership(fly_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_au.make_rope(sports_rope, disc_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_au.set_plan(planunit_shop(disc_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardlink=awardlink_shop(run_str))
    before_sue_au.edit_plan_attr(ball_rope, awardlink=awardlink_shop(fly_str))
    before_sue_au.edit_plan_attr(disc_rope, awardlink=awardlink_shop(run_str))
    before_sue_au.edit_plan_attr(disc_rope, awardlink=awardlink_shop(fly_str))

    after_sue_believer = copy_deepcopy(before_sue_au)
    after_sue_believer.edit_plan_attr(disc_rope, awardlink_del=run_str)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(before_sue_au, after_sue_believer)

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")

    x_keylist = [DELETE_str(), believer_plan_awardlink_str(), disc_rope, run_str]
    run_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert run_believeratom.get_value(plan_rope_str()) == disc_rope
    assert run_believeratom.get_value(awardee_title_str()) == run_str

    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_awardlink_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_au.add_partnerunit(xio_str)
    before_sue_au.add_partnerunit(zia_str)
    before_sue_au.add_partnerunit(bob_str)
    xio_partnerunit = before_sue_au.get_partner(xio_str)
    zia_partnerunit = before_sue_au.get_partner(zia_str)
    bob_partnerunit = before_sue_au.get_partner(bob_str)
    run_str = ";runners"
    xio_partnerunit.add_membership(run_str)
    zia_partnerunit.add_membership(run_str)
    fly_str = ";flyers"
    xio_partnerunit.add_membership(fly_str)
    zia_partnerunit.add_membership(fly_str)
    bob_partnerunit.add_membership(fly_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_au.make_rope(sports_rope, disc_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_au.set_plan(planunit_shop(disc_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardlink=awardlink_shop(run_str))
    before_sue_au.edit_plan_attr(disc_rope, awardlink=awardlink_shop(fly_str))
    after_sue_au = copy_deepcopy(before_sue_au)
    after_sue_au.edit_plan_attr(ball_rope, awardlink=awardlink_shop(fly_str))
    after_run_give_force = 44
    after_run_take_force = 66
    x_awardlink = awardlink_shop(run_str, after_run_give_force, after_run_take_force)
    after_sue_au.edit_plan_attr(disc_rope, awardlink=x_awardlink)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")

    x_keylist = [INSERT_str(), believer_plan_awardlink_str(), disc_rope, run_str]
    run_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert run_believeratom.get_value(plan_rope_str()) == disc_rope
    assert run_believeratom.get_value(awardee_title_str()) == run_str
    assert run_believeratom.get_value(plan_rope_str()) == disc_rope
    assert run_believeratom.get_value(awardee_title_str()) == run_str
    assert run_believeratom.get_value(give_force_str()) == after_run_give_force
    assert run_believeratom.get_value(take_force_str()) == after_run_take_force

    assert get_believeratom_total_count(sue_believerdelta) == 2


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_awardlink_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = believerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    before_sue_au.add_partnerunit(xio_str)
    before_sue_au.add_partnerunit(zia_str)
    xio_partnerunit = before_sue_au.get_partner(xio_str)
    run_str = ";runners"
    xio_partnerunit.add_membership(run_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardlink=awardlink_shop(run_str))
    run_awardlink = before_sue_au.get_plan_obj(ball_rope).awardlinks.get(run_str)

    after_sue_believer = copy_deepcopy(before_sue_au)
    after_give_force = 55
    after_take_force = 66
    after_sue_believer.edit_plan_attr(
        ball_rope,
        awardlink=awardlink_shop(
            awardee_title=run_str,
            give_force=after_give_force,
            take_force=after_take_force,
        ),
    )
    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(before_sue_au, after_sue_believer)

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")

    x_keylist = [UPDATE_str(), believer_plan_awardlink_str(), ball_rope, run_str]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(awardee_title_str()) == run_str
    assert ball_believeratom.get_value(give_force_str()) == after_give_force
    assert ball_believeratom.get_value(take_force_str()) == after_take_force
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_factunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_believer.make_l1_rope(knee_str)
    bend_str = "bendable"
    bend_rope = before_sue_believer.make_rope(knee_rope, bend_str)
    before_sue_believer.set_plan(planunit_shop(bend_str), knee_rope)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_believer.make_rope(knee_rope, damaged_str)
    before_sue_believer.set_l1_plan(planunit_shop(knee_str))
    before_sue_believer.set_plan(planunit_shop(damaged_str), knee_rope)
    before_f_lower = 11
    before_f_upper = 22
    before_fact = factunit_shop(knee_rope, bend_rope, before_f_lower, before_f_upper)
    before_sue_believer.edit_plan_attr(ball_rope, factunit=before_fact)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_f_lower = 55
    after_f_upper = 66
    knee_fact = factunit_shop(knee_rope, damaged_rope, after_f_lower, after_f_upper)
    after_sue_believer.edit_plan_attr(ball_rope, factunit=knee_fact)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")

    x_keylist = [UPDATE_str(), believer_plan_factunit_str(), ball_rope, knee_rope]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(f_context_str()) == knee_rope
    assert ball_believeratom.get_value(f_state_str()) == damaged_rope
    assert ball_believeratom.get_value(f_lower_str()) == after_f_lower
    assert ball_believeratom.get_value(f_upper_str()) == after_f_upper
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_factunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_believer.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_believer.make_rope(knee_rope, damaged_str)
    before_sue_believer.set_l1_plan(planunit_shop(knee_str))
    before_sue_believer.set_plan(planunit_shop(damaged_str), knee_rope)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_f_lower = 55
    after_f_upper = 66
    after_fact = factunit_shop(knee_rope, damaged_rope, after_f_lower, after_f_upper)
    after_sue_believer.edit_plan_attr(ball_rope, factunit=after_fact)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [INSERT_str(), believer_plan_factunit_str(), ball_rope, knee_rope]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    print(f"{ball_believeratom=}")
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(f_context_str()) == knee_rope
    assert ball_believeratom.get_value(f_state_str()) == damaged_rope
    assert ball_believeratom.get_value(f_lower_str()) == after_f_lower
    assert ball_believeratom.get_value(f_upper_str()) == after_f_upper
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_factunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_believer.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_believer.make_rope(knee_rope, damaged_str)
    before_sue_believer.set_l1_plan(planunit_shop(knee_str))
    before_sue_believer.set_plan(planunit_shop(damaged_str), knee_rope)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    before_damaged_r_lower = 55
    before_damaged_r_upper = 66
    before_fact = factunit_shop(
        f_context=knee_rope,
        f_state=damaged_rope,
        f_lower=before_damaged_r_lower,
        f_upper=before_damaged_r_upper,
    )
    before_sue_believer.edit_plan_attr(ball_rope, factunit=before_fact)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [DELETE_str(), believer_plan_factunit_str(), ball_rope, knee_rope]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(f_context_str()) == knee_rope
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_reason_caseunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_believer.make_l1_rope(knee_str)
    before_sue_believer.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_believer.make_rope(knee_rope, damaged_str)
    before_sue_believer.set_plan(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_believer.make_rope(knee_rope, bend_str)
    before_sue_believer.set_plan(planunit_shop(bend_str), knee_rope)
    before_sue_believer.edit_plan_attr(
        ball_rope, reason_r_context=knee_rope, reason_case=bend_rope
    )

    after_sue_believer = copy_deepcopy(before_sue_believer)
    damaged_r_lower = 45
    damaged_r_upper = 77
    damaged_r_divisor = 3
    after_sue_believer.edit_plan_attr(
        ball_rope,
        reason_r_context=knee_rope,
        reason_case=damaged_rope,
        r_lower=damaged_r_lower,
        reason_r_upper=damaged_r_upper,
        r_divisor=damaged_r_divisor,
    )

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        INSERT_str(),
        believer_plan_reason_caseunit_str(),
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value("r_context") == knee_rope
    assert ball_believeratom.get_value("r_state") == damaged_rope
    assert ball_believeratom.get_value("r_lower") == damaged_r_lower
    assert ball_believeratom.get_value("r_upper") == damaged_r_upper
    assert ball_believeratom.get_value("r_divisor") == damaged_r_divisor
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_reason_caseunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_believer.make_l1_rope(knee_str)
    before_sue_believer.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_believer.make_rope(knee_rope, damaged_str)
    before_sue_believer.set_plan(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_believer.make_rope(knee_rope, bend_str)
    before_sue_believer.set_plan(planunit_shop(bend_str), knee_rope)
    before_sue_believer.edit_plan_attr(
        ball_rope, reason_r_context=knee_rope, reason_case=bend_rope
    )
    damaged_r_lower = 45
    damaged_r_upper = 77
    damaged_r_divisor = 3
    before_sue_believer.edit_plan_attr(
        ball_rope,
        reason_r_context=knee_rope,
        reason_case=damaged_rope,
        r_lower=damaged_r_lower,
        reason_r_upper=damaged_r_upper,
        r_divisor=damaged_r_divisor,
    )
    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_sue_believer.edit_plan_attr(
        ball_rope,
        reason_del_case_r_context=knee_rope,
        reason_del_case_r_state=damaged_rope,
    )

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        DELETE_str(),
        believer_plan_reason_caseunit_str(),
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value("r_context") == knee_rope
    assert ball_believeratom.get_value("r_state") == damaged_rope
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_reason_caseunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_believer.make_l1_rope(knee_str)
    before_sue_believer.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_believer.make_rope(knee_rope, damaged_str)
    before_sue_believer.set_plan(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_believer.make_rope(knee_rope, bend_str)
    before_sue_believer.set_plan(planunit_shop(bend_str), knee_rope)
    before_sue_believer.edit_plan_attr(
        ball_rope, reason_r_context=knee_rope, reason_case=bend_rope
    )
    before_damaged_r_lower = 111
    before_damaged_r_upper = 777
    before_damaged_r_divisor = 13
    before_sue_believer.edit_plan_attr(
        ball_rope,
        reason_r_context=knee_rope,
        reason_case=damaged_rope,
        r_lower=before_damaged_r_lower,
        reason_r_upper=before_damaged_r_upper,
        r_divisor=before_damaged_r_divisor,
    )

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_damaged_r_lower = 333
    after_damaged_r_upper = 555
    after_damaged_r_divisor = 78
    after_sue_believer.edit_plan_attr(
        ball_rope,
        reason_r_context=knee_rope,
        reason_case=damaged_rope,
        r_lower=after_damaged_r_lower,
        reason_r_upper=after_damaged_r_upper,
        r_divisor=after_damaged_r_divisor,
    )

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        UPDATE_str(),
        believer_plan_reason_caseunit_str(),
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value("r_context") == knee_rope
    assert ball_believeratom.get_value("r_state") == damaged_rope
    assert ball_believeratom.get_value("r_lower") == after_damaged_r_lower
    assert ball_believeratom.get_value("r_upper") == after_damaged_r_upper
    assert ball_believeratom.get_value("r_divisor") == after_damaged_r_divisor
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_reasonunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_believer.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_believer.make_rope(knee_rope, medical_str)
    before_sue_believer.set_l1_plan(planunit_shop(knee_str))
    before_sue_believer.set_plan(planunit_shop(medical_str), knee_rope)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_medical_r_plan_active_requisite = False
    after_sue_believer.edit_plan_attr(
        ball_rope,
        reason_r_context=medical_rope,
        reason_r_plan_active_requisite=after_medical_r_plan_active_requisite,
    )

    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        INSERT_str(),
        believer_plan_reasonunit_str(),
        ball_rope,
        medical_rope,
    ]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value("r_context") == medical_rope
    assert (
        ball_believeratom.get_value(r_plan_active_requisite_str())
        == after_medical_r_plan_active_requisite
    )
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_reasonunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_believer.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_believer.make_rope(knee_rope, medical_str)
    before_sue_believer.set_l1_plan(planunit_shop(knee_str))
    before_sue_believer.set_plan(planunit_shop(medical_str), knee_rope)
    before_medical_r_plan_active_requisite = True
    before_sue_believer.edit_plan_attr(
        ball_rope,
        reason_r_context=medical_rope,
        reason_r_plan_active_requisite=before_medical_r_plan_active_requisite,
    )

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_medical_r_plan_active_requisite = False
    after_sue_believer.edit_plan_attr(
        ball_rope,
        reason_r_context=medical_rope,
        reason_r_plan_active_requisite=after_medical_r_plan_active_requisite,
    )

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        UPDATE_str(),
        believer_plan_reasonunit_str(),
        ball_rope,
        medical_rope,
    ]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value("r_context") == medical_rope
    assert (
        ball_believeratom.get_value(r_plan_active_requisite_str())
        == after_medical_r_plan_active_requisite
    )
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_reasonunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_believer.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_believer.make_rope(knee_rope, medical_str)
    before_sue_believer.set_l1_plan(planunit_shop(knee_str))
    before_sue_believer.set_plan(planunit_shop(medical_str), knee_rope)
    before_medical_r_plan_active_requisite = True
    before_sue_believer.edit_plan_attr(
        ball_rope,
        reason_r_context=medical_rope,
        reason_r_plan_active_requisite=before_medical_r_plan_active_requisite,
    )

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_ball_plan = after_sue_believer.get_plan_obj(ball_rope)
    after_ball_plan.del_reasonunit_r_context(medical_rope)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        DELETE_str(),
        believer_plan_reasonunit_str(),
        ball_rope,
        medical_rope,
    ]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value("r_context") == medical_rope
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_laborlink_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_believer.add_partnerunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_ball_planunit = after_sue_believer.get_plan_obj(ball_rope)
    after_ball_planunit.laborunit.set_laborlink(xio_str)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        INSERT_str(),
        believer_plan_laborlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(labor_title_str()) == xio_str
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_laborlink_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_believer.add_partnerunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_believer.get_plan_obj(ball_rope)
    before_ball_planunit.laborunit.set_laborlink(xio_str)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_ball_planunit = after_sue_believer.get_plan_obj(ball_rope)
    after_ball_planunit.laborunit.del_laborlink(xio_str)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        DELETE_str(),
        believer_plan_laborlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(labor_title_str()) == xio_str
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_healerlink_insert_PlanUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_believer.add_partnerunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_ball_planunit = after_sue_believer.get_plan_obj(ball_rope)
    after_ball_planunit.healerlink.set_healer_name(xio_str)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        INSERT_str(),
        believer_plan_healerlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_believeratom = get_from_nested_dict(sue_believerdelta.believeratoms, x_keylist)
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(healer_name_str()) == xio_str
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_healerlink_insert_PlanUnitInsert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_believer.add_partnerunit(xio_str)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    after_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    after_ball_planunit = after_sue_believer.get_plan_obj(ball_rope)
    after_ball_planunit.healerlink.set_healer_name(xio_str)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        INSERT_str(),
        believer_plan_healerlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_believeratom = get_from_nested_dict(
        sue_believerdelta.believeratoms, x_keylist, True
    )
    assert ball_believeratom
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(healer_name_str()) == xio_str
    assert get_believeratom_total_count(sue_believerdelta) == 3


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_healerlink_delete_PlanUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_believer.add_partnerunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_believer.get_plan_obj(ball_rope)
    before_ball_planunit.healerlink.set_healer_name(xio_str)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_ball_planunit = after_sue_believer.get_plan_obj(ball_rope)
    after_ball_planunit.healerlink.del_healer_name(xio_str)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        DELETE_str(),
        believer_plan_healerlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_believeratom = get_from_nested_dict(
        sue_believerdelta.believeratoms, x_keylist, if_missing_return_None=True
    )
    assert ball_believeratom
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(healer_name_str()) == xio_str
    assert get_believeratom_total_count(sue_believerdelta) == 1


def test_BelieverDelta_add_all_different_believeratoms_Creates_BelieverAtom_plan_healerlink_delete_PlanUnitDelete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_believer = believerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_believer.add_partnerunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_believer.make_rope(sports_rope, ball_str)
    before_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_believer.get_plan_obj(ball_rope)
    before_ball_planunit.healerlink.set_healer_name(xio_str)

    after_sue_believer = copy_deepcopy(before_sue_believer)
    after_sue_believer.del_plan_obj(ball_rope)

    # WHEN
    sue_believerdelta = believerdelta_shop()
    sue_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    # THEN
    print(f"{print_believeratom_keys(sue_believerdelta)=}")
    x_keylist = [
        DELETE_str(),
        believer_plan_healerlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_believeratom = get_from_nested_dict(
        sue_believerdelta.believeratoms, x_keylist, if_missing_return_None=True
    )
    assert ball_believeratom
    assert ball_believeratom.get_value(plan_rope_str()) == ball_rope
    assert ball_believeratom.get_value(healer_name_str()) == xio_str
    assert get_believeratom_total_count(sue_believerdelta) == 2


def test_BelieverDelta_add_all_believeratoms_CorrectlyCreates_BelieverAtoms():
    # ESTABLISH
    sue_str = "Sue"

    after_sue_believer = believerunit_shop(sue_str)
    xio_str = "Xio"
    temp_xio_partnerunit = partnerunit_shop(xio_str)
    after_sue_believer.set_partnerunit(temp_xio_partnerunit, auto_set_membership=False)
    sports_str = "sports"
    sports_rope = after_sue_believer.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = after_sue_believer.make_rope(sports_rope, ball_str)
    after_sue_believer.set_plan(planunit_shop(ball_str), sports_rope)
    after_ball_planunit = after_sue_believer.get_plan_obj(ball_rope)
    after_ball_planunit.laborunit.set_laborlink(xio_str)

    before_sue_believer = believerunit_shop(sue_str)
    sue1_believerdelta = believerdelta_shop()
    sue1_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )
    print(f"{sue1_believerdelta.get_ordered_believeratoms()}")
    assert len(sue1_believerdelta.get_ordered_believeratoms()) == 4

    # WHEN
    sue2_believerdelta = believerdelta_shop()
    sue2_believerdelta.add_all_believeratoms(after_sue_believer)

    # THEN
    assert len(sue2_believerdelta.get_ordered_believeratoms()) == 4
    assert sue2_believerdelta == sue1_believerdelta
