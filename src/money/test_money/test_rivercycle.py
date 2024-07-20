from src.bud.bud import budunit_shop
from src.listen.hubunit import hubunit_shop
from src.money.examples.example_credorledgers import (
    example_yao_credorledger,
    example_bob_credorledger,
    example_zia_credorledger,
)
from src.money.rivercycle import (
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
    assert x_rivercycle.econ_credorledgers is None
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
    assert one_rivercycle.econ_credorledgers == {}
    assert one_rivercycle.riverbooks == {}


def test_RiverCylce_set_complete_riverbook_CorrectlySetsAttr():
    # ESTABLISH
    one_int = 1
    yao_hubunit = hubunit_shop(None, None, "Yao")
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int)
    bob_book_money_amount = 555
    bob_text = "Bob"
    bob_riverbook = create_riverbook(yao_hubunit, bob_text, {}, bob_book_money_amount)
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle._set_complete_riverbook(bob_riverbook)

    # THEN
    assert one_rivercycle.riverbooks == {bob_text: bob_riverbook}


def test_RiverCylce_set_riverbook_CorrectlySetsAttr():
    # ESTABLISH
    one_int = 1
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(None, None, yao_text)
    bob_text = "Bob"
    econ_credorledger = {bob_text: {yao_text: 75, bob_text: 25}}
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int, econ_credorledger)
    bob_book_money_amount = 500
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle.set_riverbook(bob_text, bob_book_money_amount)

    # THEN
    bob_credorledger = econ_credorledger.get(bob_text)
    bob_riverbook = create_riverbook(
        yao_hubunit, bob_text, bob_credorledger, bob_book_money_amount
    )
    assert one_rivercycle.riverbooks == {bob_text: bob_riverbook}


def test_RiverCylce_create_cylceledger_ReturnsCorrectObjOneRiverBook():
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(None, None, yao_text)
    one_int = 1
    yao_credorledger = {yao_text: {yao_text: 334.0}}
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int, yao_credorledger)
    book_money_amount = 450
    one_rivercycle.set_riverbook(yao_text, book_money_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    assert one_cylceledger == {yao_text: book_money_amount}


def test_RiverCylce_create_cylceledger_ReturnsCorrectObjTwoRiverBooks():
    # ESTABLISH
    yao_text = "Yao"
    bob_text = "Bob"
    yao_hubunit = hubunit_shop(None, None, yao_text)
    one_int = 1
    econ_credorledgers = {
        yao_text: {yao_text: 75, bob_text: 25},
        bob_text: {yao_text: 49, bob_text: 51},
    }
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int, econ_credorledgers)
    yao_book_money_amount = 500
    bob_book_money_amount = 100000
    one_rivercycle.set_riverbook(yao_text, yao_book_money_amount)
    one_rivercycle.set_riverbook(bob_text, bob_book_money_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    yao_money = (yao_book_money_amount * 0.75) + (bob_book_money_amount * 0.49)
    bob_money = (yao_book_money_amount * 0.25) + (bob_book_money_amount * 0.51)
    assert one_cylceledger == {yao_text: yao_money, bob_text: bob_money}


def test_create_init_rivercycle_ReturnsObjScenarioOne_acctunit():
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(None, None, yao_text)
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_acctunit(yao_text)
    yao_credorledger = get_credorledger(yao_bud)
    econ_credorledgers = {yao_text: yao_credorledger}

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_hubunit, econ_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    assert yao_init_rivercycle.riverbooks.get(yao_text) is not None


def test_create_init_rivercycle_ReturnsObjScenarioThree_acctunit():
    # ESTABLISH
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credor_weight = 7
    bob_credor_weight = 3
    zia_credor_weight = 10
    yao_hubunit = hubunit_shop(None, None, yao_text)
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_acctunit(yao_text, yao_credor_weight)
    yao_bud.add_acctunit(bob_text, bob_credor_weight)
    yao_bud.add_acctunit(zia_text, zia_credor_weight)
    yao_credorledger = get_credorledger(yao_bud)
    econ_credorledgers = {yao_text: yao_credorledger}
    print(f"{econ_credorledgers=}")

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_hubunit, econ_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    yao_riverbook = yao_init_rivercycle.riverbooks.get(yao_text)
    assert yao_riverbook is not None
    assert len(yao_riverbook._rivergrants) == 3
    assert yao_riverbook._rivergrants.get(yao_text) == 350000000
    assert yao_riverbook._rivergrants.get(bob_text) == 150000000
    assert yao_riverbook._rivergrants.get(zia_text) == 500000000


def test_create_next_rivercycle_ReturnsObjScenarioThree_acctunit():
    # ESTABLISH
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_hubunit = hubunit_shop(None, None, yao_text)
    yao_credorledger = example_yao_credorledger()
    bob_credorledger = example_bob_credorledger()
    zia_credorledger = example_zia_credorledger()
    econ_credorledgers = {
        yao_text: yao_credorledger,
        bob_text: bob_credorledger,
        zia_text: zia_credorledger,
    }
    print(f"{econ_credorledgers=}")
    init_rivercycle = create_init_rivercycle(yao_hubunit, econ_credorledgers)
    init_cycleledger = init_rivercycle.create_cylceledger()
    print(f"{init_cycleledger=}")

    # WHEN
    next_rivercycle = create_next_rivercycle(init_rivercycle, init_cycleledger)

    # THEN
    assert next_rivercycle.number == init_rivercycle.number + 1
    assert len(next_rivercycle.riverbooks) == 3
    yao_riverbook = next_rivercycle.riverbooks.get(yao_text)
    bob_riverbook = next_rivercycle.riverbooks.get(bob_text)
    zia_riverbook = next_rivercycle.riverbooks.get(zia_text)
    assert yao_riverbook is not None
    assert bob_riverbook is not None
    assert zia_riverbook is not None
    assert len(yao_riverbook._rivergrants) == 3
    assert yao_riverbook._rivergrants.get(yao_text) == 122500000
    assert yao_riverbook._rivergrants.get(bob_text) == 52500000
    assert yao_riverbook._rivergrants.get(zia_text) == 175000000
    assert bob_riverbook._rivergrants.get(yao_text) == 3000000
    assert bob_riverbook._rivergrants.get(bob_text) == 21000000
    assert bob_riverbook._rivergrants.get(zia_text) == 126000000
    assert zia_riverbook._rivergrants.get(yao_text) == 148333333
    assert zia_riverbook._rivergrants.get(bob_text) == 250000000
    assert zia_riverbook._rivergrants.get(zia_text) == 101666667

    assert sum(zia_riverbook._rivergrants.values()) == init_cycleledger.get(zia_text)
    assert sum(bob_riverbook._rivergrants.values()) == init_cycleledger.get(bob_text)
    assert sum(yao_riverbook._rivergrants.values()) == init_cycleledger.get(yao_text)


def test_create_next_rivercycle_ReturnsObjDoesNotReference_cycleledger_From_prev_rivercycle():
    # ESTABLISH
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_hubunit = hubunit_shop(None, None, yao_text)
    yao_credorledger = example_yao_credorledger()
    bob_credorledger = example_bob_credorledger()
    zia_credorledger = example_zia_credorledger()
    econ_credorledgers = {
        yao_text: yao_credorledger,
        bob_text: bob_credorledger,
        zia_text: zia_credorledger,
    }
    print(f"{econ_credorledgers=}")
    init_rivercycle = create_init_rivercycle(yao_hubunit, econ_credorledgers)
    init_cycleledger = init_rivercycle.create_cylceledger()
    print(f"{init_cycleledger=}")
    init_cycleledger[bob_text] = init_cycleledger.get(bob_text) - 500000

    # WHEN
    next_rivercycle = create_next_rivercycle(init_rivercycle, init_cycleledger)

    # THEN
    assert next_rivercycle.number == init_rivercycle.number + 1
    assert len(next_rivercycle.riverbooks) == 3
    yao_riverbook = next_rivercycle.riverbooks.get(yao_text)
    bob_riverbook = next_rivercycle.riverbooks.get(bob_text)
    zia_riverbook = next_rivercycle.riverbooks.get(zia_text)
    assert yao_riverbook is not None
    assert bob_riverbook is not None
    assert zia_riverbook is not None
    assert len(yao_riverbook._rivergrants) == 3
    assert yao_riverbook._rivergrants.get(yao_text) == 122500000
    assert yao_riverbook._rivergrants.get(bob_text) == 52500000
    assert yao_riverbook._rivergrants.get(zia_text) == 175000000

    assert bob_riverbook._rivergrants.get(yao_text) != 3000000
    assert bob_riverbook._rivergrants.get(yao_text) == 2990000
    assert bob_riverbook._rivergrants.get(bob_text) != 21000000
    assert bob_riverbook._rivergrants.get(bob_text) == 20930000
    assert bob_riverbook._rivergrants.get(zia_text) != 126000000
    assert bob_riverbook._rivergrants.get(zia_text) == 125580000

    assert zia_riverbook._rivergrants.get(yao_text) == 148333333
    assert zia_riverbook._rivergrants.get(bob_text) == 250000000
    assert zia_riverbook._rivergrants.get(zia_text) == 101666667

    assert sum(zia_riverbook._rivergrants.values()) == init_cycleledger.get(zia_text)
    assert sum(bob_riverbook._rivergrants.values()) == init_cycleledger.get(bob_text)
    assert sum(yao_riverbook._rivergrants.values()) == init_cycleledger.get(yao_text)
