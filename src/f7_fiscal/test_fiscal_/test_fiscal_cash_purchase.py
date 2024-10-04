# from src.f1_road.finance_tran import tranbook_shop
# from src.f7_fiscal.fiscal import fiscalunit_shop


# def test_FiscalUnit_set_cashpurchase_SetsAttr():
#     # ESTABLISH
#     x_fiscal = fiscalunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     t55_t = 5505
#     assert x_fiscal.cashbook.tranunit_exists(sue_str, bob_str, t55_t)

#     # WHEN
#     x_fiscal.cashbook(sue_cashpurchase)

#     # THEN
#     assert x_fiscal.cashbook != {}
#     assert x_fiscal.cashbook.get(sue_str) == sue_cashpurchase


# def test_FiscalUnit_cashpurchase_exists_ReturnsObj():
#     # ESTABLISH
#     music_str = "music"
#     x_fiscal = fiscalunit_shop()
#     sue_str = "Sue"
#     assert x_fiscal.cashpurchase_exists(sue_str) is False

#     # WHEN
#     sue_cashpurchase = cashpurchase_shop(sue_str)
#     x_fiscal.set_cashpurchase(sue_cashpurchase)

#     # THEN
#     assert x_fiscal.cashpurchase_exists(sue_str)


# def test_FiscalUnit_get_cashpurchase_ReturnsObj():
#     # ESTABLISH
#     music_str = "music"
#     x_fiscal = fiscalunit_shop()
#     sue_str = "Sue"
#     sue_cashpurchase = cashpurchase_shop(sue_str)
#     x_fiscal.set_cashpurchase(sue_cashpurchase)
#     assert x_fiscal.cashpurchase_exists(sue_str)

#     # WHEN
#     sue_gen_cashpurchase = x_fiscal.get_cashpurchase(sue_str)

#     # THEN
#     assert sue_cashpurchase
#     assert sue_cashpurchase == sue_gen_cashpurchase


# def test_FiscalUnit_del_cashpurchase_SetsAttr():
#     # ESTABLISH
#     music_str = "music"
#     x_fiscal = fiscalunit_shop()
#     sue_str = "Sue"
#     sue_cashpurchase = cashpurchase_shop(sue_str)
#     x_fiscal.set_cashpurchase(sue_cashpurchase)
#     assert x_fiscal.cashpurchase_exists(sue_str)

#     # WHEN
#     x_fiscal.del_cashpurchase(sue_str)

#     # THEN
#     assert x_fiscal.cashpurchase_exists(sue_str) is False


# def test_FiscalUnit_add_cashpurchase_SetsAttr():
#     # ESTABLISH
#     music_str = "music"
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
