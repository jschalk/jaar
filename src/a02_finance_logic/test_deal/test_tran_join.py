from src.a02_finance_logic.deal import tranunit_shop, tranbook_shop


def test_TranBook_join_SetsAttr():
    # ESTABLISH
    m23_tranbook = tranbook_shop("accord23")
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    t66_t = 6606
    t66_yao_amount = -66
    m23_tranbook.set_tranunit(tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount))
    m23_tranbook.set_tranunit(tranunit_shop(sue_str, yao_str, t66_t, t66_yao_amount))
    bob_str = "Bob"

    t55_bob_amount = 600
    m24_tranbook = tranbook_shop("accord24")
    m24_tranbook.set_tranunit(tranunit_shop(sue_str, bob_str, t55_t, t55_bob_amount))

    assert m23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)
    assert m23_tranbook.tranunit_exists(sue_str, yao_str, t66_t)
    assert m23_tranbook.tranunit_exists(sue_str, bob_str, t55_t) is False
    assert m24_tranbook.tranunit_exists(sue_str, bob_str, t55_t)

    # WHEN
    m23_tranbook.join(m24_tranbook)

    # THEN
    assert m23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)
    assert m23_tranbook.tranunit_exists(sue_str, yao_str, t66_t)
    assert m23_tranbook.tranunit_exists(sue_str, bob_str, t55_t)
    assert m24_tranbook.tranunit_exists(sue_str, bob_str, t55_t)
