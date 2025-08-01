from src.a06_believer_logic.believer_main import believerunit_shop
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a14_keep_logic.rivercycle import (
    RiverCycle,
    create_init_rivercycle,
    create_next_rivercycle,
    create_riverbook,
    get_credorledger,
    rivercycle_shop,
)
from src.a14_keep_logic.test._util.a14_env import temp_belief_mstr_dir
from src.a14_keep_logic.test._util.example_credorledgers import (
    example_bob_credorledger,
    example_yao_credorledger,
    example_zia_credorledger,
)


def test_RiverCylce_Exists():
    # ESTABLISH / WHEN
    x_rivercycle = RiverCycle()

    # THEN
    assert x_rivercycle.hubunit is None
    assert x_rivercycle.number is None
    assert x_rivercycle.keep_credorledgers is None
    assert x_rivercycle.riverbooks is None


def test_rivercycle_shop_ReturnsObj():
    # ESTABLISH
    one_int = 1
    x_belief_mstr_dir = temp_belief_mstr_dir()
    yao_hubunit = hubunit_shop(x_belief_mstr_dir, None, "Yao")

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
    x_belief_mstr_dir = temp_belief_mstr_dir()
    yao_hubunit = hubunit_shop(x_belief_mstr_dir, None, "Yao")
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int)
    bob_book_point_amount = 555
    bob_str = "Bob"
    bob_riverbook = create_riverbook(yao_hubunit, bob_str, {}, bob_book_point_amount)
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle._set_complete_riverbook(bob_riverbook)

    # THEN
    assert one_rivercycle.riverbooks == {bob_str: bob_riverbook}


def test_RiverCylce_set_riverbook_CorrectlySetsAttr():
    # ESTABLISH
    one_int = 1
    yao_str = "Yao"
    x_belief_mstr_dir = temp_belief_mstr_dir()
    yao_hubunit = hubunit_shop(x_belief_mstr_dir, None, yao_str)
    bob_str = "Bob"
    keep_credorledger = {bob_str: {yao_str: 75, bob_str: 25}}
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int, keep_credorledger)
    bob_book_point_amount = 500
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle.set_riverbook(bob_str, bob_book_point_amount)

    # THEN
    bob_credorledger = keep_credorledger.get(bob_str)
    bob_riverbook = create_riverbook(
        yao_hubunit, bob_str, bob_credorledger, bob_book_point_amount
    )
    assert one_rivercycle.riverbooks == {bob_str: bob_riverbook}


def test_RiverCylce_create_cylceledger_ReturnsObjOneRiverBook():
    # ESTABLISH
    yao_str = "Yao"
    x_belief_mstr_dir = temp_belief_mstr_dir()
    yao_hubunit = hubunit_shop(x_belief_mstr_dir, None, yao_str)
    one_int = 1
    yao_credorledger = {yao_str: {yao_str: 334.0}}
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int, yao_credorledger)
    book_point_amount = 450
    one_rivercycle.set_riverbook(yao_str, book_point_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    assert one_cylceledger == {yao_str: book_point_amount}


def test_RiverCylce_create_cylceledger_ReturnsObjTwoRiverBooks():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    x_belief_mstr_dir = temp_belief_mstr_dir()
    yao_hubunit = hubunit_shop(x_belief_mstr_dir, None, yao_str)
    one_int = 1
    keep_credorledgers = {
        yao_str: {yao_str: 75, bob_str: 25},
        bob_str: {yao_str: 49, bob_str: 51},
    }
    one_rivercycle = rivercycle_shop(yao_hubunit, one_int, keep_credorledgers)
    yao_book_point_amount = 500
    bob_book_point_amount = 100000
    one_rivercycle.set_riverbook(yao_str, yao_book_point_amount)
    one_rivercycle.set_riverbook(bob_str, bob_book_point_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    yao_money = (yao_book_point_amount * 0.75) + (bob_book_point_amount * 0.49)
    bob_money = (yao_book_point_amount * 0.25) + (bob_book_point_amount * 0.51)
    assert one_cylceledger == {yao_str: yao_money, bob_str: bob_money}


def test_create_init_rivercycle_ReturnsObjScenarioOne_partnerunit():
    # ESTABLISH
    yao_str = "Yao"
    x_belief_mstr_dir = temp_belief_mstr_dir()
    yao_hubunit = hubunit_shop(x_belief_mstr_dir, None, yao_str)
    yao_believer = believerunit_shop(yao_str)
    yao_believer.add_partnerunit(yao_str)
    yao_credorledger = get_credorledger(yao_believer)
    keep_credorledgers = {yao_str: yao_credorledger}

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_hubunit, keep_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    assert yao_init_rivercycle.riverbooks.get(yao_str) is not None


def test_create_init_rivercycle_ReturnsObjScenarioThree_partnerunit():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_partner_cred_points = 7
    bob_partner_cred_points = 3
    zia_partner_cred_points = 10
    x_belief_mstr_dir = temp_belief_mstr_dir()
    yao_hubunit = hubunit_shop(x_belief_mstr_dir, None, yao_str)
    yao_believer = believerunit_shop(yao_str)
    yao_believer.add_partnerunit(yao_str, yao_partner_cred_points)
    yao_believer.add_partnerunit(bob_str, bob_partner_cred_points)
    yao_believer.add_partnerunit(zia_str, zia_partner_cred_points)
    yao_credorledger = get_credorledger(yao_believer)
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


def test_create_next_rivercycle_ReturnsObjScenarioThree_partnerunit():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    x_belief_mstr_dir = temp_belief_mstr_dir()
    yao_hubunit = hubunit_shop(x_belief_mstr_dir, None, yao_str)
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
    x_belief_mstr_dir = temp_belief_mstr_dir()
    yao_hubunit = hubunit_shop(x_belief_mstr_dir, None, yao_str)
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
