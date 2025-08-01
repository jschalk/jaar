from src.a06_believer_logic.believer_main import believerunit_shop
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a14_keep_logic.rivercycle import get_debtorledger
from src.a14_keep_logic.riverrun import riverrun_shop
from src.a14_keep_logic.test._util.a14_env import temp_belief_mstr_dir
from src.a14_keep_logic.test._util.example_credorledgers import example_yao_hubunit


def test_RiverRun_set_partner_tax_yield_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    x_belief_mstr_dir = temp_belief_mstr_dir()
    bob_hubunit = hubunit_shop(x_belief_mstr_dir, None, bob_str)
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_str = "Yao"
    assert bob_riverrun._tax_yields.get(yao_str) is None

    # WHEN
    yao_tax_yield = 7
    bob_riverrun.set_partner_tax_yield(yao_str, yao_tax_yield)

    # THEN
    assert bob_riverrun._tax_yields.get(yao_str) == yao_tax_yield


def test_RiverRun_tax_yields_is_empty_ReturnsObj():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    x_riverrun = riverrun_shop(yao_hubunit)
    assert x_riverrun.tax_yields_is_empty()

    # WHEN
    yao_str = "Yao"
    yao_tax_yield = 500
    x_riverrun.set_partner_tax_yield(yao_str, yao_tax_yield)
    # THEN
    assert x_riverrun.tax_yields_is_empty() is False

    # WHEN
    x_riverrun.delete_tax_yield(yao_str)
    # THEN
    assert x_riverrun.tax_yields_is_empty()

    # WHEN
    bob_str = "Yao"
    bob_tax_yield = 300
    x_riverrun.set_partner_tax_yield(bob_str, bob_tax_yield)
    x_riverrun.set_partner_tax_yield(yao_str, yao_tax_yield)
    # THEN
    assert x_riverrun.tax_yields_is_empty() is False

    # WHEN
    x_riverrun.delete_tax_yield(yao_str)
    # THEN
    assert x_riverrun.tax_yields_is_empty()


def test_RiverRun_reset_tax_yields_CorrectlySetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_tax_yield = 38
    sue_tax_yield = 56
    yao_tax_yield = 6
    bob_riverrun.set_partner_tax_yield(bob_str, bob_tax_yield)
    bob_riverrun.set_partner_tax_yield(sue_str, sue_tax_yield)
    bob_riverrun.set_partner_tax_yield(yao_str, yao_tax_yield)
    assert bob_riverrun.tax_yields_is_empty() is False

    # WHEN
    bob_riverrun.reset_tax_yields()

    # THEN
    assert bob_riverrun.tax_yields_is_empty()


def test_RiverRun_partner_has_tax_yield_ReturnsCorrectBool():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"
    yao_tax_yield = 6
    bob_tax_yield = 38
    sue_tax_yield = 56
    bob_riverrun.set_partner_tax_yield(bob_str, bob_tax_yield)
    bob_riverrun.set_partner_tax_yield(sue_str, sue_tax_yield)
    bob_riverrun.set_partner_tax_yield(yao_str, yao_tax_yield)
    assert bob_riverrun.partner_has_tax_yield(bob_str)
    assert bob_riverrun.partner_has_tax_yield(sue_str)
    assert bob_riverrun.partner_has_tax_yield(yao_str)
    assert bob_riverrun.partner_has_tax_yield(zia_str) is False

    # WHEN
    bob_riverrun.reset_tax_yields()

    # THEN
    assert bob_riverrun.partner_has_tax_yield(bob_str) is False
    assert bob_riverrun.partner_has_tax_yield(sue_str) is False
    assert bob_riverrun.partner_has_tax_yield(yao_str) is False
    assert bob_riverrun.partner_has_tax_yield(zia_str) is False


def test_RiverRun_delete_tax_yield_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 88
    bob_penny = 11
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_str = "Yao"
    bob_riverrun.set_partner_tax_yield(yao_str, 5)
    assert bob_riverrun.partner_has_tax_yield(yao_str)

    # WHEN
    bob_riverrun.delete_tax_yield(yao_str)

    # THEN
    assert bob_riverrun.partner_has_tax_yield(yao_str) is False


def test_RiverRun_get_partner_tax_yield_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_tax_yield = 38
    sue_tax_yield = 56
    yao_tax_yield = 6
    bob_riverrun.set_partner_tax_yield(bob_str, bob_tax_yield)
    bob_riverrun.set_partner_tax_yield(sue_str, sue_tax_yield)
    bob_riverrun.set_partner_tax_yield(yao_str, yao_tax_yield)
    assert bob_riverrun.partner_has_tax_yield(bob_str)
    assert bob_riverrun.get_partner_tax_yield(bob_str) == bob_tax_yield
    assert bob_riverrun.partner_has_tax_yield(zia_str) is False
    assert bob_riverrun.get_partner_tax_yield(zia_str) == 0

    # WHEN
    bob_riverrun.reset_tax_yields()

    # THEN
    assert bob_riverrun.partner_has_tax_yield(bob_str) is False
    assert bob_riverrun.get_partner_tax_yield(bob_str) == 0
    assert bob_riverrun.partner_has_tax_yield(zia_str) is False
    assert bob_riverrun.get_partner_tax_yield(zia_str) == 0


def test_RiverRun_add_partner_tax_yield_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_tax_yield = 38
    sue_tax_yield = 56
    yao_tax_yield = 6
    bob_riverrun.set_partner_tax_yield(bob_str, bob_tax_yield)
    bob_riverrun.set_partner_tax_yield(sue_str, sue_tax_yield)
    bob_riverrun.set_partner_tax_yield(yao_str, yao_tax_yield)
    assert bob_riverrun.get_partner_tax_yield(bob_str) == bob_tax_yield
    assert bob_riverrun.get_partner_tax_yield(sue_str) == sue_tax_yield
    assert bob_riverrun.get_partner_tax_yield(zia_str) == 0

    # WHEN
    bob_riverrun.add_partner_tax_yield(sue_str, 5)
    bob_riverrun.add_partner_tax_yield(zia_str, 10)

    # THEN
    assert bob_riverrun.get_partner_tax_yield(bob_str) == bob_tax_yield
    assert bob_riverrun.get_partner_tax_yield(sue_str) == sue_tax_yield + 5
    assert bob_riverrun.get_partner_tax_yield(zia_str) == 10


def test_RiverRun_levy_tax_due_SetsAttr_ScenarioY():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_tax_yield = 38
    sue_tax_yield = 56
    yao_tax_yield = 6
    bob_believer = believerunit_shop(bob_str)
    bob_believer.add_partnerunit(bob_str, 2, bob_tax_yield)
    bob_believer.add_partnerunit(sue_str, 2, sue_tax_yield)
    bob_believer.add_partnerunit(yao_str, 2, yao_tax_yield)
    bob_debtorledger = get_debtorledger(bob_believer)
    bob_riverrun.set_tax_dues(bob_debtorledger)
    assert bob_riverrun.get_partner_tax_due(bob_str) == 380
    assert bob_riverrun.get_partner_tax_yield(bob_str) == 0

    # WHEN
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(bob_str, 5)
    # THEN
    assert excess_chargeer_points == 0
    assert bob_riverrun.get_partner_tax_due(bob_str) == 375
    assert bob_riverrun.get_partner_tax_yield(bob_str) == 5

    # WHEN
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(bob_str, 375)
    # THEN
    assert excess_chargeer_points == 0
    assert bob_riverrun.get_partner_tax_due(bob_str) == 0
    assert bob_riverrun.get_partner_tax_yield(bob_str) == 380

    # ESTABLISH
    assert bob_riverrun.get_partner_tax_due(sue_str) == 560
    assert bob_riverrun.get_partner_tax_yield(sue_str) == 0
    # WHEN
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(sue_str, 1000)
    # THEN
    assert excess_chargeer_points == 440
    assert bob_riverrun.get_partner_tax_due(sue_str) == 0
    assert bob_riverrun.get_partner_tax_yield(sue_str) == 560

    # ESTABLISH
    zia_str = "Zia"
    assert bob_riverrun.get_partner_tax_due(zia_str) == 0
    assert bob_riverrun.get_partner_tax_yield(zia_str) == 0
    # WHEN
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(zia_str, 1000)
    # THEN
    assert excess_chargeer_points == 1000
    assert bob_riverrun.get_partner_tax_due(zia_str) == 0
    assert bob_riverrun.get_partner_tax_yield(zia_str) == 0

    # ESTABLISH
    assert bob_riverrun.get_partner_tax_due(yao_str) == 60
    assert bob_riverrun.get_partner_tax_yield(yao_str) == 0
    # WHEN
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(yao_str, 81)
    # THEN
    assert excess_chargeer_points == 21
    assert bob_riverrun.get_partner_tax_due(yao_str) == 0
    assert bob_riverrun.get_partner_tax_yield(yao_str) == 60


def test_RiverRun_set_tax_got_attrs_SetsAttrs():
    # ESTABLISH
    six_tax_got = 6
    ten_tax_got = 10
    x_riverrun = riverrun_shop(example_yao_hubunit())
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._tax_got_prev == 0

    # WHEN
    x_riverrun._set_tax_got_attrs(six_tax_got)
    # THEN
    assert x_riverrun._tax_got_curr == six_tax_got
    assert x_riverrun._tax_got_prev == 0

    # WHEN
    x_riverrun._set_tax_got_attrs(ten_tax_got)
    # THEN
    assert x_riverrun._tax_got_curr == ten_tax_got
    assert x_riverrun._tax_got_prev == six_tax_got


def test_RiverRun_tax_gotten_ReturnsObj():
    # ESTABLISH
    six_tax_got = 6
    ten_tax_got = 10
    x_riverrun = riverrun_shop(example_yao_hubunit())
    assert x_riverrun._tax_got_prev == 0
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._tax_gotten() is False

    # WHEN
    x_riverrun._set_tax_got_attrs(six_tax_got)
    # THEN
    assert x_riverrun._tax_got_prev == 0
    assert x_riverrun._tax_got_curr == six_tax_got
    assert x_riverrun._tax_gotten()

    # ESTABLISH
    x_riverrun._set_tax_got_attrs(six_tax_got)
    # THEN
    assert x_riverrun._tax_got_prev == six_tax_got
    assert x_riverrun._tax_got_curr == six_tax_got
    assert x_riverrun._tax_gotten()

    # WHEN
    x_riverrun._set_tax_got_attrs(0)
    # THEN
    assert x_riverrun._tax_got_prev == six_tax_got
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._tax_gotten()

    # WHEN
    x_riverrun._set_tax_got_attrs(0)
    # THEN
    assert x_riverrun._tax_got_prev == 0
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._tax_gotten() is False
