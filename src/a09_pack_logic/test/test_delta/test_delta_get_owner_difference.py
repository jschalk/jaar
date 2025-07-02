from copy import deepcopy as copy_deepcopy
from src.a00_data_toolbox.dict_toolbox import (
    get_empty_list_if_None,
    get_from_nested_dict,
)
from src.a03_group_logic.acct import acctunit_shop
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_plan import factunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    acct_name_str,
    awardee_title_str,
    begin_str,
    close_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    give_force_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    mass_str,
    owner_acct_membership_str,
    owner_acctunit_str,
    owner_plan_awardlink_str,
    owner_plan_factunit_str,
    owner_plan_healerlink_str,
    owner_plan_laborlink_str,
    owner_plan_reason_premiseunit_str,
    owner_plan_reasonunit_str,
    owner_planunit_str,
    ownerunit_str,
    plan_rope_str,
    rplan_active_requisite_str,
    take_force_str,
    task_str,
)
from src.a06_owner_logic.test._util.example_owners import get_ownerunit_with_4_levels
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import OwnerDelta, ownerdelta_shop


def print_owneratom_keys(x_ownerdelta: OwnerDelta):
    for x_owneratom in get_delete_owneratom_list(x_ownerdelta):
        print(f"DELETE {x_owneratom.dimen} {list(x_owneratom.jkeys.values())}")
    for x_owneratom in get_update_owneratom_list(x_ownerdelta):
        print(f"UPDATE {x_owneratom.dimen} {list(x_owneratom.jkeys.values())}")
    for x_owneratom in get_insert_owneratom_list(x_ownerdelta):
        print(f"INSERT {x_owneratom.dimen} {list(x_owneratom.jkeys.values())}")


def get_delete_owneratom_list(x_ownerdelta: OwnerDelta) -> list:
    return get_empty_list_if_None(
        x_ownerdelta._get_crud_owneratoms_list().get(DELETE_str())
    )


def get_insert_owneratom_list(x_ownerdelta: OwnerDelta):
    return get_empty_list_if_None(
        x_ownerdelta._get_crud_owneratoms_list().get(INSERT_str())
    )


def get_update_owneratom_list(x_ownerdelta: OwnerDelta):
    return get_empty_list_if_None(
        x_ownerdelta._get_crud_owneratoms_list().get(UPDATE_str())
    )


def get_owneratom_total_count(x_ownerdelta: OwnerDelta) -> int:
    return (
        len(get_delete_owneratom_list(x_ownerdelta))
        + len(get_insert_owneratom_list(x_ownerdelta))
        + len(get_update_owneratom_list(x_ownerdelta))
    )


def test_OwnerDelta_create_owneratoms_EmptyOwners():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()
    sue_ownerdelta = ownerdelta_shop()
    assert sue_ownerdelta.owneratoms == {}

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(sue_owner, sue_owner)

    # THEN
    assert sue_ownerdelta.owneratoms == {}


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_acctunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    after_sue_owner = copy_deepcopy(before_sue_owner)
    xio_str = "Xio"
    xio_acct_cred_points = 33
    xio_acct_debt_points = 44
    xio_acctunit = acctunit_shop(xio_str, xio_acct_cred_points, xio_acct_debt_points)
    after_sue_owner.set_acctunit(xio_acctunit, auto_set_membership=False)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    assert (
        len(sue_ownerdelta.owneratoms.get(INSERT_str()).get(owner_acctunit_str())) == 1
    )
    sue_insert_dict = sue_ownerdelta.owneratoms.get(INSERT_str())
    sue_acctunit_dict = sue_insert_dict.get(owner_acctunit_str())
    xio_owneratom = sue_acctunit_dict.get(xio_str)
    assert xio_owneratom.get_value(acct_name_str()) == xio_str
    assert xio_owneratom.get_value("acct_cred_points") == xio_acct_cred_points
    assert xio_owneratom.get_value("acct_debt_points") == xio_acct_debt_points

    print(f"{get_owneratom_total_count(sue_ownerdelta)=}")
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_acctunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    before_sue_owner.add_acctunit("Yao")
    before_sue_owner.add_acctunit("Zia")

    after_sue_owner = copy_deepcopy(before_sue_owner)

    xio_str = "Xio"
    before_sue_owner.add_acctunit(xio_str)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    xio_owneratom = get_from_nested_dict(
        sue_ownerdelta.owneratoms, [DELETE_str(), owner_acctunit_str(), xio_str]
    )
    assert xio_owneratom.get_value(acct_name_str()) == xio_str

    print(f"{get_owneratom_total_count(sue_ownerdelta)=}")
    print_owneratom_keys(sue_ownerdelta)
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_acctunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    after_sue_owner = copy_deepcopy(before_sue_owner)
    xio_str = "Xio"
    before_sue_owner.add_acctunit(xio_str)
    xio_acct_cred_points = 33
    xio_acct_debt_points = 44
    after_sue_owner.add_acctunit(xio_str, xio_acct_cred_points, xio_acct_debt_points)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    x_keylist = [UPDATE_str(), owner_acctunit_str(), xio_str]
    xio_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert xio_owneratom.get_value(acct_name_str()) == xio_str
    assert xio_owneratom.get_value("acct_cred_points") == xio_acct_cred_points
    assert xio_owneratom.get_value("acct_debt_points") == xio_acct_debt_points

    print(f"{get_owneratom_total_count(sue_ownerdelta)=}")
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_OwnerUnit_simple_attrs_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    after_sue_owner = copy_deepcopy(before_sue_owner)
    x_ownerunit_tally = 55
    x_fund_pool = 8000000
    x_fund_iota = 8
    x_respect_bit = 5
    x_max_tree_traverse = 66
    x_credor_respect = 770
    x_debtor_respect = 880
    after_sue_owner.tally = x_ownerunit_tally
    after_sue_owner.fund_pool = x_fund_pool
    after_sue_owner.fund_iota = x_fund_iota
    after_sue_owner.respect_bit = x_respect_bit
    after_sue_owner.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_owner.set_credor_respect(x_credor_respect)
    after_sue_owner.set_debtor_respect(x_debtor_respect)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    x_keylist = [UPDATE_str(), ownerunit_str()]
    xio_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert xio_owneratom.get_value("max_tree_traverse") == x_max_tree_traverse
    assert xio_owneratom.get_value("credor_respect") == x_credor_respect
    assert xio_owneratom.get_value("debtor_respect") == x_debtor_respect
    assert xio_owneratom.get_value("tally") == x_ownerunit_tally
    assert xio_owneratom.get_value("fund_pool") == x_fund_pool
    assert xio_owneratom.get_value("fund_iota") == x_fund_iota
    assert xio_owneratom.get_value("respect_bit") == x_respect_bit

    print(f"{get_owneratom_total_count(sue_ownerdelta)=}")
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_acct_membership_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    after_sue_owner = copy_deepcopy(before_sue_owner)
    yao_str = "Yao"
    zia_str = "Zia"
    temp_yao_acctunit = acctunit_shop(yao_str)
    temp_zia_acctunit = acctunit_shop(zia_str)
    after_sue_owner.set_acctunit(temp_yao_acctunit, auto_set_membership=False)
    after_sue_owner.set_acctunit(temp_zia_acctunit, auto_set_membership=False)
    after_yao_acctunit = after_sue_owner.get_acct(yao_str)
    after_zia_acctunit = after_sue_owner.get_acct(zia_str)
    run_str = ";runners"
    zia_run_credit_w = 77
    zia_run_debt_w = 88
    after_zia_acctunit.add_membership(run_str, zia_run_credit_w, zia_run_debt_w)
    print(f"{after_sue_owner.get_acctunit_group_titles_dict()=}")

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    print(f"{after_sue_owner.get_acct(zia_str)._memberships=}")
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)
    # print(f"{sue_ownerdelta.owneratoms.get(INSERT_str()).keys()=}")
    # print(
    #     sue_ownerdelta.owneratoms.get(INSERT_str()).get(owner_acct_membership_str()).keys()
    # )

    # THEN
    x_keylist = [INSERT_str(), owner_acctunit_str(), yao_str]
    yao_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert yao_owneratom.get_value(acct_name_str()) == yao_str

    x_keylist = [INSERT_str(), owner_acctunit_str(), zia_str]
    zia_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert zia_owneratom.get_value(acct_name_str()) == zia_str
    print(f"\n{sue_ownerdelta.owneratoms=}")
    # print(f"\n{zia_owneratom=}")

    x_keylist = [INSERT_str(), owner_acct_membership_str(), zia_str, run_str]
    run_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert run_owneratom.get_value(acct_name_str()) == zia_str
    assert run_owneratom.get_value(group_title_str()) == run_str
    assert run_owneratom.get_value("group_cred_points") == zia_run_credit_w
    assert run_owneratom.get_value("group_debt_points") == zia_run_debt_w

    print_owneratom_keys(sue_ownerdelta)
    print(f"{get_owneratom_total_count(sue_ownerdelta)=}")
    assert len(get_delete_owneratom_list(sue_ownerdelta)) == 0
    assert len(get_insert_owneratom_list(sue_ownerdelta)) == 3
    assert len(get_delete_owneratom_list(sue_ownerdelta)) == 0
    assert get_owneratom_total_count(sue_ownerdelta) == 3


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_acct_membership_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    before_sue_owner.add_acctunit(xio_str)
    before_sue_owner.add_acctunit(zia_str)
    run_str = ";runners"
    before_xio_credit_w = 77
    before_xio_debt_w = 88
    before_xio_acct = before_sue_owner.get_acct(xio_str)
    before_xio_acct.add_membership(run_str, before_xio_credit_w, before_xio_debt_w)
    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_xio_acctunit = after_sue_owner.get_acct(xio_str)
    after_xio_credit_w = 55
    after_xio_debt_w = 66
    after_xio_acctunit.add_membership(run_str, after_xio_credit_w, after_xio_debt_w)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    # x_keylist = [UPDATE_str(), owner_acctunit_str(), xio_str]
    # xio_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    # assert xio_owneratom.get_value(acct_name_str()) == xio_str
    # print(f"\n{sue_ownerdelta.owneratoms=}")
    # print(f"\n{xio_owneratom=}")

    x_keylist = [UPDATE_str(), owner_acct_membership_str(), xio_str, run_str]
    xio_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert xio_owneratom.get_value(acct_name_str()) == xio_str
    assert xio_owneratom.get_value(group_title_str()) == run_str
    assert xio_owneratom.get_value("group_cred_points") == after_xio_credit_w
    assert xio_owneratom.get_value("group_debt_points") == after_xio_debt_w

    print(f"{get_owneratom_total_count(sue_ownerdelta)=}")
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_acct_membership_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_owner.add_acctunit(xio_str)
    before_sue_owner.add_acctunit(zia_str)
    before_sue_owner.add_acctunit(bob_str)
    before_xio_acctunit = before_sue_owner.get_acct(xio_str)
    before_zia_acctunit = before_sue_owner.get_acct(zia_str)
    before_bob_acctunit = before_sue_owner.get_acct(bob_str)
    run_str = ";runners"
    before_xio_acctunit.add_membership(run_str)
    before_zia_acctunit.add_membership(run_str)
    fly_str = ";flyers"
    before_xio_acctunit.add_membership(fly_str)
    before_zia_acctunit.add_membership(fly_str)
    before_bob_acctunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_owner.get_acctunit_group_titles_dict()

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_xio_acctunit = after_sue_owner.get_acct(xio_str)
    after_zia_acctunit = after_sue_owner.get_acct(zia_str)
    after_bob_acctunit = after_sue_owner.get_acct(bob_str)
    after_xio_acctunit.delete_membership(run_str)
    after_zia_acctunit.delete_membership(run_str)
    after_bob_acctunit.delete_membership(fly_str)
    after_group_titles_dict = after_sue_owner.get_acctunit_group_titles_dict()
    assert len(before_group_titles_dict.get(fly_str)) == 3
    assert len(before_group_titles_dict.get(run_str)) == 2
    assert len(after_group_titles_dict.get(fly_str)) == 2
    assert after_group_titles_dict.get(run_str) is None

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    x_keylist = [DELETE_str(), owner_acct_membership_str(), bob_str, fly_str]
    xio_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert xio_owneratom.get_value(acct_name_str()) == bob_str
    assert xio_owneratom.get_value(group_title_str()) == fly_str

    print(f"{get_owneratom_total_count(sue_ownerdelta)=}")
    print_owneratom_keys(sue_ownerdelta)
    assert len(get_delete_owneratom_list(sue_ownerdelta)) == 3
    assert len(get_insert_owneratom_list(sue_ownerdelta)) == 0
    assert len(get_update_owneratom_list(sue_ownerdelta)) == 0
    assert get_owneratom_total_count(sue_ownerdelta) == 3


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_owner.make_rope(ball_rope, street_str)
    before_sue_owner.set_plan(planunit_shop(street_str), ball_rope)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_owner.make_rope(sports_rope, disc_str)
    amy45_str = "amy45"
    before_sue_owner.set_l1_plan(planunit_shop(amy45_str))
    before_sue_owner.set_plan(planunit_shop(disc_str), sports_rope)
    # create after without ball_plan and street_plan
    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_sue_owner.del_plan_obj(ball_rope)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    x_dimen = owner_planunit_str()
    print(f"{sue_ownerdelta.owneratoms.get(DELETE_str()).get(x_dimen).keys()=}")

    x_keylist = [DELETE_str(), owner_planunit_str(), street_rope]
    street_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert street_owneratom.get_value(plan_rope_str()) == street_rope

    x_keylist = [DELETE_str(), owner_planunit_str(), ball_rope]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope

    print(f"{get_owneratom_total_count(sue_ownerdelta)=}")
    assert get_owneratom_total_count(sue_ownerdelta) == 2


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_owner.make_rope(ball_rope, street_str)
    before_sue_owner.set_plan(planunit_shop(street_str), ball_rope)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    disc_str = "Ultimate Disc"
    disc_rope = after_sue_owner.make_rope(sports_rope, disc_str)
    after_sue_owner.set_plan(planunit_shop(disc_str), sports_rope)
    amy45_str = "amy45"
    amy_begin = 34
    amy_close = 78
    amy_mass = 55
    amy_task = True
    amy_rope = after_sue_owner.make_l1_rope(amy45_str)
    after_sue_owner.set_l1_plan(
        planunit_shop(
            amy45_str,
            begin=amy_begin,
            close=amy_close,
            mass=amy_mass,
            task=amy_task,
        )
    )

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print_owneratom_keys(sue_ownerdelta)

    x_keylist = [INSERT_str(), owner_planunit_str(), disc_rope]
    street_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert street_owneratom.get_value(plan_rope_str()) == disc_rope

    a45_rope = after_sue_owner.make_l1_rope(amy45_str)
    x_keylist = [INSERT_str(), owner_planunit_str(), a45_rope]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == a45_rope
    assert ball_owneratom.get_value(begin_str()) == amy_begin
    assert ball_owneratom.get_value(close_str()) == amy_close
    assert ball_owneratom.get_value(mass_str()) == amy_mass
    assert ball_owneratom.get_value(task_str()) == amy_task

    assert get_owneratom_total_count(sue_ownerdelta) == 2


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    amy45_str = "amy45"
    amy45_rope = before_sue_owner.make_l1_rope(amy45_str)
    before_amy_begin = 34
    before_amy_close = 78
    before_amy_mass = 55
    before_amy_task = True
    amy_rope = before_sue_owner.make_l1_rope(amy45_str)
    before_sue_owner.set_l1_plan(
        planunit_shop(
            amy45_str,
            begin=before_amy_begin,
            close=before_amy_close,
            mass=before_amy_mass,
            task=before_amy_task,
        )
    )

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_amy_begin = 99
    after_amy_close = 111
    after_amy_mass = 22
    after_amy_task = False
    after_sue_owner.edit_plan_attr(
        amy_rope,
        begin=after_amy_begin,
        close=after_amy_close,
        mass=after_amy_mass,
        task=after_amy_task,
    )

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print_owneratom_keys(sue_ownerdelta)

    x_keylist = [UPDATE_str(), owner_planunit_str(), amy45_rope]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == amy45_rope
    assert ball_owneratom.get_value(begin_str()) == after_amy_begin
    assert ball_owneratom.get_value(close_str()) == after_amy_close
    assert ball_owneratom.get_value(mass_str()) == after_amy_mass
    assert ball_owneratom.get_value(task_str()) == after_amy_task

    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_awardlink_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = ownerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_au.add_acctunit(xio_str)
    before_sue_au.add_acctunit(zia_str)
    before_sue_au.add_acctunit(bob_str)
    xio_acctunit = before_sue_au.get_acct(xio_str)
    zia_acctunit = before_sue_au.get_acct(zia_str)
    bob_acctunit = before_sue_au.get_acct(bob_str)
    run_str = ";runners"
    xio_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    fly_str = ";flyers"
    xio_acctunit.add_membership(fly_str)
    zia_acctunit.add_membership(fly_str)
    bob_acctunit.add_membership(fly_str)
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

    after_sue_owner = copy_deepcopy(before_sue_au)
    after_sue_owner.edit_plan_attr(disc_rope, awardlink_del=run_str)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_au, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")

    x_keylist = [DELETE_str(), owner_plan_awardlink_str(), disc_rope, run_str]
    run_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert run_owneratom.get_value(plan_rope_str()) == disc_rope
    assert run_owneratom.get_value(awardee_title_str()) == run_str

    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_awardlink_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = ownerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    bob_str = "Bob"
    before_sue_au.add_acctunit(xio_str)
    before_sue_au.add_acctunit(zia_str)
    before_sue_au.add_acctunit(bob_str)
    xio_acctunit = before_sue_au.get_acct(xio_str)
    zia_acctunit = before_sue_au.get_acct(zia_str)
    bob_acctunit = before_sue_au.get_acct(bob_str)
    run_str = ";runners"
    xio_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    fly_str = ";flyers"
    xio_acctunit.add_membership(fly_str)
    zia_acctunit.add_membership(fly_str)
    bob_acctunit.add_membership(fly_str)
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
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")

    x_keylist = [INSERT_str(), owner_plan_awardlink_str(), disc_rope, run_str]
    run_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert run_owneratom.get_value(plan_rope_str()) == disc_rope
    assert run_owneratom.get_value(awardee_title_str()) == run_str
    assert run_owneratom.get_value(plan_rope_str()) == disc_rope
    assert run_owneratom.get_value(awardee_title_str()) == run_str
    assert run_owneratom.get_value(give_force_str()) == after_run_give_force
    assert run_owneratom.get_value(take_force_str()) == after_run_take_force

    assert get_owneratom_total_count(sue_ownerdelta) == 2


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_awardlink_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_au = ownerunit_shop(sue_str)
    xio_str = "Xio"
    zia_str = "Zia"
    before_sue_au.add_acctunit(xio_str)
    before_sue_au.add_acctunit(zia_str)
    xio_acctunit = before_sue_au.get_acct(xio_str)
    run_str = ";runners"
    xio_acctunit.add_membership(run_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan(planunit_shop(ball_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardlink=awardlink_shop(run_str))
    run_awardlink = before_sue_au.get_plan_obj(ball_rope).awardlinks.get(run_str)

    after_sue_owner = copy_deepcopy(before_sue_au)
    after_give_force = 55
    after_take_force = 66
    after_sue_owner.edit_plan_attr(
        ball_rope,
        awardlink=awardlink_shop(
            awardee_title=run_str,
            give_force=after_give_force,
            take_force=after_take_force,
        ),
    )
    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_au, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")

    x_keylist = [UPDATE_str(), owner_plan_awardlink_str(), ball_rope, run_str]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(awardee_title_str()) == run_str
    assert ball_owneratom.get_value(give_force_str()) == after_give_force
    assert ball_owneratom.get_value(take_force_str()) == after_take_force
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_factunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_owner.make_l1_rope(knee_str)
    bend_str = "bendable"
    bend_rope = before_sue_owner.make_rope(knee_rope, bend_str)
    before_sue_owner.set_plan(planunit_shop(bend_str), knee_rope)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_owner.make_rope(knee_rope, damaged_str)
    before_sue_owner.set_l1_plan(planunit_shop(knee_str))
    before_sue_owner.set_plan(planunit_shop(damaged_str), knee_rope)
    before_fopen = 11
    before_fnigh = 22
    before_fact = factunit_shop(knee_rope, bend_rope, before_fopen, before_fnigh)
    before_sue_owner.edit_plan_attr(ball_rope, factunit=before_fact)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_fopen = 55
    after_fnigh = 66
    knee_fact = factunit_shop(knee_rope, damaged_rope, after_fopen, after_fnigh)
    after_sue_owner.edit_plan_attr(ball_rope, factunit=knee_fact)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")

    x_keylist = [UPDATE_str(), owner_plan_factunit_str(), ball_rope, knee_rope]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(fcontext_str()) == knee_rope
    assert ball_owneratom.get_value(fstate_str()) == damaged_rope
    assert ball_owneratom.get_value(fopen_str()) == after_fopen
    assert ball_owneratom.get_value(fnigh_str()) == after_fnigh
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_factunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_owner.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_owner.make_rope(knee_rope, damaged_str)
    before_sue_owner.set_l1_plan(planunit_shop(knee_str))
    before_sue_owner.set_plan(planunit_shop(damaged_str), knee_rope)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_fopen = 55
    after_fnigh = 66
    after_fact = factunit_shop(knee_rope, damaged_rope, after_fopen, after_fnigh)
    after_sue_owner.edit_plan_attr(ball_rope, factunit=after_fact)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [INSERT_str(), owner_plan_factunit_str(), ball_rope, knee_rope]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    print(f"{ball_owneratom=}")
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(fcontext_str()) == knee_rope
    assert ball_owneratom.get_value(fstate_str()) == damaged_rope
    assert ball_owneratom.get_value(fopen_str()) == after_fopen
    assert ball_owneratom.get_value(fnigh_str()) == after_fnigh
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_factunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_owner.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_owner.make_rope(knee_rope, damaged_str)
    before_sue_owner.set_l1_plan(planunit_shop(knee_str))
    before_sue_owner.set_plan(planunit_shop(damaged_str), knee_rope)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    before_damaged_popen = 55
    before_damaged_pnigh = 66
    before_fact = factunit_shop(
        fcontext=knee_rope,
        fstate=damaged_rope,
        fopen=before_damaged_popen,
        fnigh=before_damaged_pnigh,
    )
    before_sue_owner.edit_plan_attr(ball_rope, factunit=before_fact)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [DELETE_str(), owner_plan_factunit_str(), ball_rope, knee_rope]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(fcontext_str()) == knee_rope
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_reason_premiseunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_owner.make_l1_rope(knee_str)
    before_sue_owner.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_owner.make_rope(knee_rope, damaged_str)
    before_sue_owner.set_plan(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_owner.make_rope(knee_rope, bend_str)
    before_sue_owner.set_plan(planunit_shop(bend_str), knee_rope)
    before_sue_owner.edit_plan_attr(
        ball_rope, reason_rcontext=knee_rope, reason_premise=bend_rope
    )

    after_sue_owner = copy_deepcopy(before_sue_owner)
    damaged_popen = 45
    damaged_pnigh = 77
    damaged_pdivisor = 3
    after_sue_owner.edit_plan_attr(
        ball_rope,
        reason_rcontext=knee_rope,
        reason_premise=damaged_rope,
        popen=damaged_popen,
        reason_pnigh=damaged_pnigh,
        pdivisor=damaged_pdivisor,
    )

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        INSERT_str(),
        owner_plan_reason_premiseunit_str(),
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value("rcontext") == knee_rope
    assert ball_owneratom.get_value("pstate") == damaged_rope
    assert ball_owneratom.get_value("popen") == damaged_popen
    assert ball_owneratom.get_value("pnigh") == damaged_pnigh
    assert ball_owneratom.get_value("pdivisor") == damaged_pdivisor
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_reason_premiseunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_owner.make_l1_rope(knee_str)
    before_sue_owner.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_owner.make_rope(knee_rope, damaged_str)
    before_sue_owner.set_plan(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_owner.make_rope(knee_rope, bend_str)
    before_sue_owner.set_plan(planunit_shop(bend_str), knee_rope)
    before_sue_owner.edit_plan_attr(
        ball_rope, reason_rcontext=knee_rope, reason_premise=bend_rope
    )
    damaged_popen = 45
    damaged_pnigh = 77
    damaged_pdivisor = 3
    before_sue_owner.edit_plan_attr(
        ball_rope,
        reason_rcontext=knee_rope,
        reason_premise=damaged_rope,
        popen=damaged_popen,
        reason_pnigh=damaged_pnigh,
        pdivisor=damaged_pdivisor,
    )
    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_sue_owner.edit_plan_attr(
        ball_rope,
        reason_del_premise_rcontext=knee_rope,
        reason_del_premise_pstate=damaged_rope,
    )

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        DELETE_str(),
        owner_plan_reason_premiseunit_str(),
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value("rcontext") == knee_rope
    assert ball_owneratom.get_value("pstate") == damaged_rope
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_reason_premiseunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_owner.make_l1_rope(knee_str)
    before_sue_owner.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_owner.make_rope(knee_rope, damaged_str)
    before_sue_owner.set_plan(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_owner.make_rope(knee_rope, bend_str)
    before_sue_owner.set_plan(planunit_shop(bend_str), knee_rope)
    before_sue_owner.edit_plan_attr(
        ball_rope, reason_rcontext=knee_rope, reason_premise=bend_rope
    )
    before_damaged_popen = 111
    before_damaged_pnigh = 777
    before_damaged_pdivisor = 13
    before_sue_owner.edit_plan_attr(
        ball_rope,
        reason_rcontext=knee_rope,
        reason_premise=damaged_rope,
        popen=before_damaged_popen,
        reason_pnigh=before_damaged_pnigh,
        pdivisor=before_damaged_pdivisor,
    )

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_damaged_popen = 333
    after_damaged_pnigh = 555
    after_damaged_pdivisor = 78
    after_sue_owner.edit_plan_attr(
        ball_rope,
        reason_rcontext=knee_rope,
        reason_premise=damaged_rope,
        popen=after_damaged_popen,
        reason_pnigh=after_damaged_pnigh,
        pdivisor=after_damaged_pdivisor,
    )

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        UPDATE_str(),
        owner_plan_reason_premiseunit_str(),
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value("rcontext") == knee_rope
    assert ball_owneratom.get_value("pstate") == damaged_rope
    assert ball_owneratom.get_value("popen") == after_damaged_popen
    assert ball_owneratom.get_value("pnigh") == after_damaged_pnigh
    assert ball_owneratom.get_value("pdivisor") == after_damaged_pdivisor
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_reasonunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_owner.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_owner.make_rope(knee_rope, medical_str)
    before_sue_owner.set_l1_plan(planunit_shop(knee_str))
    before_sue_owner.set_plan(planunit_shop(medical_str), knee_rope)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_medical_rplan_active_requisite = False
    after_sue_owner.edit_plan_attr(
        ball_rope,
        reason_rcontext=medical_rope,
        reason_rplan_active_requisite=after_medical_rplan_active_requisite,
    )

    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        INSERT_str(),
        owner_plan_reasonunit_str(),
        ball_rope,
        medical_rope,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value("rcontext") == medical_rope
    assert (
        ball_owneratom.get_value(rplan_active_requisite_str())
        == after_medical_rplan_active_requisite
    )
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_reasonunit_update():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_owner.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_owner.make_rope(knee_rope, medical_str)
    before_sue_owner.set_l1_plan(planunit_shop(knee_str))
    before_sue_owner.set_plan(planunit_shop(medical_str), knee_rope)
    before_medical_rplan_active_requisite = True
    before_sue_owner.edit_plan_attr(
        ball_rope,
        reason_rcontext=medical_rope,
        reason_rplan_active_requisite=before_medical_rplan_active_requisite,
    )

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_medical_rplan_active_requisite = False
    after_sue_owner.edit_plan_attr(
        ball_rope,
        reason_rcontext=medical_rope,
        reason_rplan_active_requisite=after_medical_rplan_active_requisite,
    )

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        UPDATE_str(),
        owner_plan_reasonunit_str(),
        ball_rope,
        medical_rope,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value("rcontext") == medical_rope
    assert (
        ball_owneratom.get_value(rplan_active_requisite_str())
        == after_medical_rplan_active_requisite
    )
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_reasonunit_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_owner.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_owner.make_rope(knee_rope, medical_str)
    before_sue_owner.set_l1_plan(planunit_shop(knee_str))
    before_sue_owner.set_plan(planunit_shop(medical_str), knee_rope)
    before_medical_rplan_active_requisite = True
    before_sue_owner.edit_plan_attr(
        ball_rope,
        reason_rcontext=medical_rope,
        reason_rplan_active_requisite=before_medical_rplan_active_requisite,
    )

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_ball_plan = after_sue_owner.get_plan_obj(ball_rope)
    after_ball_plan.del_reasonunit_rcontext(medical_rope)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        DELETE_str(),
        owner_plan_reasonunit_str(),
        ball_rope,
        medical_rope,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value("rcontext") == medical_rope
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_laborlink_insert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_owner.add_acctunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_ball_planunit = after_sue_owner.get_plan_obj(ball_rope)
    after_ball_planunit.laborunit.set_laborlink(xio_str)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        INSERT_str(),
        owner_plan_laborlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(labor_title_str()) == xio_str
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_laborlink_delete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_owner.add_acctunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_owner.get_plan_obj(ball_rope)
    before_ball_planunit.laborunit.set_laborlink(xio_str)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_ball_planunit = after_sue_owner.get_plan_obj(ball_rope)
    after_ball_planunit.laborunit.del_laborlink(xio_str)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        DELETE_str(),
        owner_plan_laborlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(labor_title_str()) == xio_str
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_healerlink_insert_PlanUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_owner.add_acctunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_ball_planunit = after_sue_owner.get_plan_obj(ball_rope)
    after_ball_planunit.healerlink.set_healer_name(xio_str)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        INSERT_str(),
        owner_plan_healerlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist)
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(healer_name_str()) == xio_str
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_healerlink_insert_PlanUnitInsert():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_owner.add_acctunit(xio_str)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    after_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    after_ball_planunit = after_sue_owner.get_plan_obj(ball_rope)
    after_ball_planunit.healerlink.set_healer_name(xio_str)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        INSERT_str(),
        owner_plan_healerlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_owneratom = get_from_nested_dict(sue_ownerdelta.owneratoms, x_keylist, True)
    assert ball_owneratom
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(healer_name_str()) == xio_str
    assert get_owneratom_total_count(sue_ownerdelta) == 3


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_healerlink_delete_PlanUnitUpdate():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_owner.add_acctunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_owner.get_plan_obj(ball_rope)
    before_ball_planunit.healerlink.set_healer_name(xio_str)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_ball_planunit = after_sue_owner.get_plan_obj(ball_rope)
    after_ball_planunit.healerlink.del_healer_name(xio_str)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        DELETE_str(),
        owner_plan_healerlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_owneratom = get_from_nested_dict(
        sue_ownerdelta.owneratoms, x_keylist, if_missing_return_None=True
    )
    assert ball_owneratom
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(healer_name_str()) == xio_str
    assert get_owneratom_total_count(sue_ownerdelta) == 1


def test_OwnerDelta_add_all_different_owneratoms_Creates_OwnerAtom_plan_healerlink_delete_PlanUnitDelete():
    # ESTABLISH
    sue_str = "Sue"
    before_sue_owner = ownerunit_shop(sue_str)
    xio_str = "Xio"
    before_sue_owner.add_acctunit(xio_str)
    sports_str = "sports"
    sports_rope = before_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_owner.make_rope(sports_rope, ball_str)
    before_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_owner.get_plan_obj(ball_rope)
    before_ball_planunit.healerlink.set_healer_name(xio_str)

    after_sue_owner = copy_deepcopy(before_sue_owner)
    after_sue_owner.del_plan_obj(ball_rope)

    # WHEN
    sue_ownerdelta = ownerdelta_shop()
    sue_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)

    # THEN
    print(f"{print_owneratom_keys(sue_ownerdelta)=}")
    x_keylist = [
        DELETE_str(),
        owner_plan_healerlink_str(),
        ball_rope,
        xio_str,
    ]
    ball_owneratom = get_from_nested_dict(
        sue_ownerdelta.owneratoms, x_keylist, if_missing_return_None=True
    )
    assert ball_owneratom
    assert ball_owneratom.get_value(plan_rope_str()) == ball_rope
    assert ball_owneratom.get_value(healer_name_str()) == xio_str
    assert get_owneratom_total_count(sue_ownerdelta) == 2


def test_OwnerDelta_add_all_owneratoms_CorrectlyCreates_OwnerAtoms():
    # ESTABLISH
    sue_str = "Sue"

    after_sue_owner = ownerunit_shop(sue_str)
    xio_str = "Xio"
    temp_xio_acctunit = acctunit_shop(xio_str)
    after_sue_owner.set_acctunit(temp_xio_acctunit, auto_set_membership=False)
    sports_str = "sports"
    sports_rope = after_sue_owner.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = after_sue_owner.make_rope(sports_rope, ball_str)
    after_sue_owner.set_plan(planunit_shop(ball_str), sports_rope)
    after_ball_planunit = after_sue_owner.get_plan_obj(ball_rope)
    after_ball_planunit.laborunit.set_laborlink(xio_str)

    before_sue_owner = ownerunit_shop(sue_str)
    sue1_ownerdelta = ownerdelta_shop()
    sue1_ownerdelta.add_all_different_owneratoms(before_sue_owner, after_sue_owner)
    print(f"{sue1_ownerdelta.get_ordered_owneratoms()}")
    assert len(sue1_ownerdelta.get_ordered_owneratoms()) == 4

    # WHEN
    sue2_ownerdelta = ownerdelta_shop()
    sue2_ownerdelta.add_all_owneratoms(after_sue_owner)

    # THEN
    assert len(sue2_ownerdelta.get_ordered_owneratoms()) == 4
    assert sue2_ownerdelta == sue1_ownerdelta
