from src.f1_road.finance_tran import tranbook_shop, tranunit_shop
from src.f7_fiscal.fiscal import fiscalunit_shop


def test_FiscalUnit_set_cashpurchase_SetsAttr():
    # ESTABLISH
    x_fiscal = fiscalunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert x_fiscal.cashbook.tranunit_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    x_fiscal.set_cashpurchase(sue_bob_t55_tranunit)

    # THEN
    assert x_fiscal.cashbook.tranunit_exists(sue_str, bob_str, t55_t)


def test_FiscalUnit_cashpurchase_exists_ReturnsObj():
    # ESTABLISH
    x_fiscal = fiscalunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    t55_amount = 37
    x_fiscal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))

    # THEN
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t)


def test_FiscalUnit_get_cashpurchase_ReturnsObj():
    # ESTABLISH
    x_fiscal = fiscalunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_fiscal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t)

    # WHEN
    sue_gen_cashpurchase = x_fiscal.get_cashpurchase(sue_str, bob_str, t55_t)

    # THEN
    assert sue_gen_cashpurchase
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert sue_gen_cashpurchase == sue_bob_t55_tranunit


def test_FiscalUnit_del_cashpurchase_SetsAttr():
    # ESTABLISH
    x_fiscal = fiscalunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_fiscal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t)

    # WHEN
    x_fiscal.del_cashpurchase(sue_str, bob_str, t55_t)

    # THEN
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t) is False


# def test_FiscalUnit_add_cashpurchase_SetsAttr():
#     # ESTABLISH
#     x_fiscal = fiscalunit_shop()
#     assert x_fiscal.cashbook == tranbook_shop(x_fiscal.fiscal_id)

#     # WHEN
#     bob_str = "Bob"
#     bob_x0_timestamp = 702
#     bob_x0_magnitude = 33
#     sue_str = "Sue"
#     sue_x4_timestamp = 4
#     sue_x4_magnitude = 55
#     sue_x7_timestamp = 7
#     sue_x7_magnitude = 66
#     x_fiscal.add_cashpurchase(bob_str, bob_x0_timestamp, bob_x0_magnitude)
#     x_fiscal.add_cashpurchase(sue_str, sue_x4_timestamp, sue_x4_magnitude)
#     x_fiscal.add_cashpurchase(sue_str, sue_x7_timestamp, sue_x7_magnitude)

#     # THEN
#     assert x_fiscal.cashbook != {}
#     sue_cashpurchase = cashpurchase_shop(sue_str)
#     sue_cashpurchase.add_episode(sue_x4_timestamp, sue_x4_magnitude)
#     sue_cashpurchase.add_episode(sue_x7_timestamp, sue_x7_magnitude)
#     bob_cashpurchase = cashpurchase_shop(bob_str)
#     bob_cashpurchase.add_episode(bob_x0_timestamp, bob_x0_magnitude)
#     assert x_fiscal.get_cashpurchase(sue_str) == sue_cashpurchase
#     assert x_fiscal.get_cashpurchase(bob_str) == bob_cashpurchase
