from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_partner_debt_points_str,
    _irrational_partner_debt_points_str,
    _memberships_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
)
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import _groupunits_str, partners_str
from src.a07_timeline_logic.test._util.a07_str import readable_str
from src.a22_belief_viewer.belief_viewer_tool import (
    add_small_dot,
    get_partners_view_dict,
)
from src.a22_belief_viewer.example22_beliefs import (
    best_run_str,
    best_soccer_str,
    best_sport_str,
    best_swim_str,
    get_beliefunit_irrational_example,
    get_sue_belief_with_facts_and_reasons,
    get_sue_beliefunit,
    play_run_str,
    play_soccer_str,
    play_str,
    play_swim_str,
)


def test_get_partners_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = beliefunit_shop(sue_str)
    sue_believer.cash_out()

    # WHEN
    partners_view_dict = get_partners_view_dict(sue_believer)

    # THEN
    assert partners_view_dict == {}


def add_readable(str: str) -> str:
    return f"{str}_{readable_str()}"


def test_get_partners_view_dict_ReturnsObj_Scenario1_partners():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = beliefunit_shop(sue_str)
    yao_str = "Yao"
    bob_str = "Bob"
    yao_cred_points = 110
    yao_debt_points = 130
    bob_cred_points = 230
    bob_debt_points = 290
    sue_believer.add_partnerunit(yao_str, yao_cred_points, yao_debt_points)
    sue_believer.add_partnerunit(bob_str, bob_cred_points, bob_debt_points)
    sue_believer.cash_out()

    # WHEN
    partners_view_dict = get_partners_view_dict(sue_believer)

    # THEN
    assert set(partners_view_dict.keys()) == {yao_str, bob_str}
    yao_partner_dict = partners_view_dict.get(yao_str)
    partner_cred_points_readable_key = add_readable(partner_cred_points_str())
    partner_debt_points_readable_key = add_readable(partner_debt_points_str())
    _memberships_readable_key = add_readable(_memberships_str())
    _credor_pool_readable_key = add_readable(_credor_pool_str())
    _debtor_pool_readable_key = add_readable(_debtor_pool_str())
    _irrational_partner_debt_points_readable_key = add_readable(
        _irrational_partner_debt_points_str()
    )
    _inallocable_partner_debt_points_readable_key = add_readable(
        _inallocable_partner_debt_points_str()
    )
    _fund_give_readable_key = add_readable(_fund_give_str())
    _fund_take_readable_key = add_readable(_fund_take_str())
    _fund_agenda_give_readable_key = add_readable(_fund_agenda_give_str())
    _fund_agenda_take_readable_key = add_readable(_fund_agenda_take_str())
    _fund_agenda_ratio_give_readable_key = add_readable(_fund_agenda_ratio_give_str())
    _fund_agenda_ratio_take_readable_key = add_readable(_fund_agenda_ratio_take_str())

    assert set(yao_partner_dict.keys()) == {
        partner_name_str(),
        partner_cred_points_str(),
        partner_debt_points_str(),
        _memberships_str(),
        _credor_pool_str(),
        _debtor_pool_str(),
        _irrational_partner_debt_points_str(),
        _inallocable_partner_debt_points_str(),
        _fund_give_str(),
        _fund_take_str(),
        _fund_agenda_give_str(),
        _fund_agenda_take_str(),
        _fund_agenda_ratio_give_str(),
        _fund_agenda_ratio_take_str(),
        partner_cred_points_readable_key,
        partner_debt_points_readable_key,
        _memberships_readable_key,
        _credor_pool_readable_key,
        _debtor_pool_readable_key,
        _irrational_partner_debt_points_readable_key,
        _inallocable_partner_debt_points_readable_key,
        _fund_give_readable_key,
        _fund_take_readable_key,
        _fund_agenda_give_readable_key,
        _fund_agenda_take_readable_key,
        _fund_agenda_ratio_give_readable_key,
        _fund_agenda_ratio_take_readable_key,
    }
    ypu = sue_believer.get_partner(yao_str)
    yp_dict = yao_partner_dict
    assert ypu.partner_name == yp_dict.get(partner_name_str())
    assert ypu.partner_cred_points == yp_dict.get(partner_cred_points_str())
    assert ypu.partner_debt_points == yp_dict.get(partner_debt_points_str())
    assert ypu._memberships == yp_dict.get(_memberships_str())
    assert ypu._credor_pool == yp_dict.get(_credor_pool_str())
    assert ypu._debtor_pool == yp_dict.get(_debtor_pool_str())
    assert ypu._irrational_partner_debt_points == yp_dict.get(
        _irrational_partner_debt_points_str()
    )
    assert ypu._inallocable_partner_debt_points == yp_dict.get(
        _inallocable_partner_debt_points_str()
    )
    assert ypu._fund_give == yp_dict.get(_fund_give_str())
    assert ypu._fund_take == yp_dict.get(_fund_take_str())
    assert ypu._fund_agenda_give == yp_dict.get(_fund_agenda_give_str())
    assert ypu._fund_agenda_take == yp_dict.get(_fund_agenda_take_str())
    assert ypu._fund_agenda_ratio_give == yp_dict.get(_fund_agenda_ratio_give_str())
    assert ypu._fund_agenda_ratio_take == yp_dict.get(_fund_agenda_ratio_take_str())

    expected_partner_cred_points_readable = (
        f"partner_cred_points: {ypu.partner_cred_points}"
    )
    expected_partner_debt_points_readable = (
        f"partner_debt_points: {ypu.partner_debt_points}"
    )
    expected__memberships_readable = f"_memberships: {ypu._memberships}"
    expected__credor_pool_readable = f"_credor_pool: {ypu._credor_pool}"
    expected__debtor_pool_readable = f"_debtor_pool: {ypu._debtor_pool}"
    expected__irrational_partner_debt_points_readable = (
        f"_irrational_partner_debt_points: {ypu._irrational_partner_debt_points}"
    )
    expected__inallocable_partner_debt_points_readable = (
        f"_inallocable_partner_debt_points: {ypu._inallocable_partner_debt_points}"
    )
    expected__fund_give_readable = f"_fund_give: {ypu._fund_give}"
    expected__fund_take_readable = f"_fund_take: {ypu._fund_take}"
    expected__fund_agenda_give_readable = f"_fund_agenda_give: {ypu._fund_agenda_give}"
    expected__fund_agenda_take_readable = f"_fund_agenda_take: {ypu._fund_agenda_take}"
    expected__fund_agenda_ratio_give_readable = (
        f"_fund_agenda_ratio_give: {ypu._fund_agenda_ratio_give}"
    )
    expected__fund_agenda_ratio_take_readable = (
        f"_fund_agenda_ratio_take: {ypu._fund_agenda_ratio_take}"
    )

    assert (
        yp_dict.get(partner_cred_points_readable_key)
        == expected_partner_cred_points_readable
    )
    assert (
        yp_dict.get(partner_debt_points_readable_key)
        == expected_partner_debt_points_readable
    )
    assert yp_dict.get(_memberships_readable_key) == expected__memberships_readable
    assert yp_dict.get(_credor_pool_readable_key) == expected__credor_pool_readable
    assert yp_dict.get(_debtor_pool_readable_key) == expected__debtor_pool_readable
    assert (
        yp_dict.get(_irrational_partner_debt_points_readable_key)
        == expected__irrational_partner_debt_points_readable
    )
    assert (
        yp_dict.get(_inallocable_partner_debt_points_readable_key)
        == expected__inallocable_partner_debt_points_readable
    )
    assert yp_dict.get(_fund_give_readable_key) == expected__fund_give_readable
    assert yp_dict.get(_fund_take_readable_key) == expected__fund_take_readable
    assert (
        yp_dict.get(_fund_agenda_give_readable_key)
        == expected__fund_agenda_give_readable
    )
    assert (
        yp_dict.get(_fund_agenda_take_readable_key)
        == expected__fund_agenda_take_readable
    )
    assert (
        yp_dict.get(_fund_agenda_ratio_give_readable_key)
        == expected__fund_agenda_ratio_give_readable
    )
    assert (
        yp_dict.get(_fund_agenda_ratio_take_readable_key)
        == expected__fund_agenda_ratio_take_readable
    )
