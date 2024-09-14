from src.bud.bud import budunit_shop
from src.d_listen.hubunit import hubunit_shop
from src.keep.examples.example_credorledgers import (
    example_yao_credorledger,
    example_bob_credorledger,
    example_zia_credorledger,
)
from src.keep.rivercycle import (
    get_credorledger,
    create_riverbook,
    RiverCycle,
    rivercycle_shop,
    create_init_rivercycle,
    create_next_rivercycle,
)


def test_RiverCylce_Exists():
    # ESTABLISH / WHEN
    x_rivercycle = RiverCycle()

    # THEN
    assert x_rivercycle.hubunit is None
    assert x_rivercycle.number is None
    assert x_rivercycle.keep_credorledgers is None
    assert x_rivercycle.riverbooks is None


def test_rivercycle_shop_ReturnsCorrectObj():
    # ESTABLISH
    one_int = 1
    yao_hubunit = hubunit_shop(None, None, "Yao")

    # WHEN
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int)

    # THEN
    assert one_rivercycle.hubunit == yao_hubunit
    assert one_rivercycle.number == 1
    assert one_rivercycle.keep_credorledgers == {}
    assert one_rivercycle.riverbooks == {}


def test_RiverCylce_set_complete_riverbook_CorrectlySetsAttr():
    # ESTABLISH
    one_int = 1
    yao_hubunit = hubunit_shop(None, None, "Yao")
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int)
    bob_book_money_amount = 555
    bob_str = "Bob"
    bob_riverbook = create_riverbook(yao_hubunit, bob_str, {}, bob_book_money_amount)
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle._set_complete_riverbook(bob_riverbook)

    # THEN
    assert one_rivercycle.riverbooks == {bob_str: bob_riverbook}


def test_RiverCylce_set_riverbook_CorrectlySetsAttr():
    # ESTABLISH
    one_int = 1
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(None, None, yao_str)
    bob_str = "Bob"
    keep_credorledger = {bob_str: {yao_str: 75, bob_str: 25}}
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int, keep_credorledger)
    bob_book_money_amount = 500
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle.set_riverbook(bob_str, bob_book_money_amount)

    # THEN
    bob_credorledger = keep_credorledger.get(bob_str)
    bob_riverbook = create_riverbook(
        yao_hubunit, bob_str, bob_credorledger, bob_book_money_amount
    )
    assert one_rivercycle.riverbooks == {bob_str: bob_riverbook}


def test_RiverCylce_create_cylceledger_ReturnsCorrectObjOneRiverBook():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(None, None, yao_str)
    one_int = 1
    yao_credorledger = {yao_str: {yao_str: 334.0}}
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int, yao_credorledger)
    book_money_amount = 450
    one_rivercycle.set_riverbook(yao_str, book_money_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    assert one_cylceledger == {yao_str: book_money_amount}


def test_RiverCylce_create_cylceledger_ReturnsCorrectObjTwoRiverBooks():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    yao_hubunit = hubunit_shop(None, None, yao_str)
    one_int = 1
    keep_credorledgers = {
        yao_str: {yao_str: 75, bob_str: 25},
        bob_str: {yao_str: 49, bob_str: 51},
    }
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int, keep_credorledgers)
    yao_book_money_amount = 500
    bob_book_money_amount = 100000
    one_rivercycle.set_riverbook(yao_str, yao_book_money_amount)
    one_rivercycle.set_riverbook(bob_str, bob_book_money_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    yao_money = (yao_book_money_amount * 0.75) + (bob_book_money_amount * 0.49)
    bob_money = (yao_book_money_amount * 0.25) + (bob_book_money_amount * 0.51)
    assert one_cylceledger == {yao_str: yao_money, bob_str: bob_money}


def test_create_init_rivercycle_ReturnsObjScenarioOne_acctunit():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(None, None, yao_str)
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(yao_str)
    yao_credorledger = get_credorledger(yao_bud)
    keep_credorledgers = {yao_str: yao_credorledger}

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_hubunit, keep_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    assert yao_init_rivercycle.riverbooks.get(yao_str) is not None


def test_create_init_rivercycle_ReturnsObjScenarioThree_acctunit():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_credit_belief = 7
    bob_credit_belief = 3
    zia_credit_belief = 10
    yao_hubunit = hubunit_shop(None, None, yao_str)
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(yao_str, yao_credit_belief)
    yao_bud.add_acctunit(bob_str, bob_credit_belief)
    yao_bud.add_acctunit(zia_str, zia_credit_belief)
    yao_credorledger = get_credorledger(yao_bud)
    keep_credorledgers = {yao_str: yao_credorledger}
    print(f"{keep_credorledgers=}")

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_hubunit, keep_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    yao_riverbook = yao_init_rivercycle.riverbooks.get(yao_str)
    assert yao_riverbook is not None
    assert len(yao_riverbook._rivergrants) == 3
    assert yao_riverbook._rivergrants.get(yao_str) == 350000000
    assert yao_riverbook._rivergrants.get(bob_str) == 150000000
    assert yao_riverbook._rivergrants.get(zia_str) == 500000000


def test_create_next_rivercycle_ReturnsObjScenarioThree_acctunit():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_hubunit = hubunit_shop(None, None, yao_str)
    yao_credorledger = example_yao_credorledger()
    bob_credorledger = example_bob_credorledger()
    zia_credorledger = example_zia_credorledger()
    keep_credorledgers = {
        yao_str: yao_credorledger,
        bob_str: bob_credorledger,
        zia_str: zia_credorledger,
    }
    print(f"{keep_credorledgers=}")
    init_rivercycle = create_init_rivercycle(yao_hubunit, keep_credorledgers)
    init_cycleledger = init_rivercycle.create_cylceledger()
    print(f"{init_cycleledger=}")

    # WHEN
    next_rivercycle = create_next_rivercycle(init_rivercycle, init_cycleledger)

    # THEN
    assert next_rivercycle.number == init_rivercycle.number + 1
    assert len(next_rivercycle.riverbooks) == 3
    yao_riverbook = next_rivercycle.riverbooks.get(yao_str)
    bob_riverbook = next_rivercycle.riverbooks.get(bob_str)
    zia_riverbook = next_rivercycle.riverbooks.get(zia_str)
    assert yao_riverbook is not None
    assert bob_riverbook is not None
    assert zia_riverbook is not None
    assert len(yao_riverbook._rivergrants) == 3
    assert yao_riverbook._rivergrants.get(yao_str) == 122500000
    assert yao_riverbook._rivergrants.get(bob_str) == 52500000
    assert yao_riverbook._rivergrants.get(zia_str) == 175000000
    assert bob_riverbook._rivergrants.get(yao_str) == 3000000
    assert bob_riverbook._rivergrants.get(bob_str) == 21000000
    assert bob_riverbook._rivergrants.get(zia_str) == 126000000
    assert zia_riverbook._rivergrants.get(yao_str) == 148333333
    assert zia_riverbook._rivergrants.get(bob_str) == 250000000
    assert zia_riverbook._rivergrants.get(zia_str) == 101666667

    assert sum(zia_riverbook._rivergrants.values()) == init_cycleledger.get(zia_str)
    assert sum(bob_riverbook._rivergrants.values()) == init_cycleledger.get(bob_str)
    assert sum(yao_riverbook._rivergrants.values()) == init_cycleledger.get(yao_str)


def test_create_next_rivercycle_ReturnsObjDoesNotReference_cycleledger_From_prev_rivercycle():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_hubunit = hubunit_shop(None, None, yao_str)
    yao_credorledger = example_yao_credorledger()
    bob_credorledger = example_bob_credorledger()
    zia_credorledger = example_zia_credorledger()
    keep_credorledgers = {
        yao_str: yao_credorledger,
        bob_str: bob_credorledger,
        zia_str: zia_credorledger,
    }
    print(f"{keep_credorledgers=}")
    init_rivercycle = create_init_rivercycle(yao_hubunit, keep_credorledgers)
    init_cycleledger = init_rivercycle.create_cylceledger()
    print(f"{init_cycleledger=}")
    init_cycleledger[bob_str] = init_cycleledger.get(bob_str) - 500000

    # WHEN
    next_rivercycle = create_next_rivercycle(init_rivercycle, init_cycleledger)

    # THEN
    assert next_rivercycle.number == init_rivercycle.number + 1
    assert len(next_rivercycle.riverbooks) == 3
    yao_riverbook = next_rivercycle.riverbooks.get(yao_str)
    bob_riverbook = next_rivercycle.riverbooks.get(bob_str)
    zia_riverbook = next_rivercycle.riverbooks.get(zia_str)
    assert yao_riverbook is not None
    assert bob_riverbook is not None
    assert zia_riverbook is not None
    assert len(yao_riverbook._rivergrants) == 3
    assert yao_riverbook._rivergrants.get(yao_str) == 122500000
    assert yao_riverbook._rivergrants.get(bob_str) == 52500000
    assert yao_riverbook._rivergrants.get(zia_str) == 175000000

    assert bob_riverbook._rivergrants.get(yao_str) != 3000000
    assert bob_riverbook._rivergrants.get(yao_str) == 2990000
    assert bob_riverbook._rivergrants.get(bob_str) != 21000000
    assert bob_riverbook._rivergrants.get(bob_str) == 20930000
    assert bob_riverbook._rivergrants.get(zia_str) != 126000000
    assert bob_riverbook._rivergrants.get(zia_str) == 125580000

    assert zia_riverbook._rivergrants.get(yao_str) == 148333333
    assert zia_riverbook._rivergrants.get(bob_str) == 250000000
    assert zia_riverbook._rivergrants.get(zia_str) == 101666667

    assert sum(zia_riverbook._rivergrants.values()) == init_cycleledger.get(zia_str)
    assert sum(bob_riverbook._rivergrants.values()) == init_cycleledger.get(bob_str)
    assert sum(yao_riverbook._rivergrants.values()) == init_cycleledger.get(yao_str)
