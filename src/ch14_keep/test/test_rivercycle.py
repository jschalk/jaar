from src.ch02_allot.allot import default_grain_num_if_None
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch14_keep.rivercycle import (
    RiverCycle,
    create_init_rivercycle,
    create_next_rivercycle,
    create_riverbook,
    get_credorledger,
    rivercycle_shop,
)
from src.ch14_keep.test._util.ch14_examples import (
    example_bob_credorledger,
    example_yao_credorledger,
    example_zia_credorledger,
)
from src.ref.keywords import Ch14Keywords as wv


def test_RiverCylce_Exists():
    # ESTABLISH / WHEN
    x_rivercycle = RiverCycle()

    # THEN
    assert not x_rivercycle.healer_name
    assert not x_rivercycle.number
    assert not x_rivercycle.keep_credorledgers
    assert not x_rivercycle.riverbooks
    assert set(x_rivercycle.__dict__.keys()) == {
        wv.healer_name,
        "number",
        wv.keep_credorledgers,
        wv.riverbooks,
        wv.mana_grain,
    }


def test_rivercycle_shop_ReturnsObj_Scenario0_SomeParametersNotPassed():
    # ESTABLISH
    one_int = 1
    yao_str = "Yao"

    # WHEN
    one_rivercycle = rivercycle_shop(yao_str, one_int)

    # THEN
    assert one_rivercycle.healer_name == yao_str
    assert one_rivercycle.number == 1
    assert one_rivercycle.keep_credorledgers == {}
    assert one_rivercycle.riverbooks == {}
    assert one_rivercycle.mana_grain == default_grain_num_if_None()


def test_rivercycle_shop_ReturnsObj_Scenario1_ParametersPassed():
    # ESTABLISH
    one_int = 1
    yao_str = "Yao"
    yao_mana_grain = 4

    # WHEN
    one_rivercycle = rivercycle_shop(yao_str, one_int, mana_grain=yao_mana_grain)

    # THEN
    assert one_rivercycle.healer_name == yao_str
    assert one_rivercycle.number == 1
    assert one_rivercycle.keep_credorledgers == {}
    assert one_rivercycle.riverbooks == {}
    assert one_rivercycle.mana_grain == yao_mana_grain


def test_RiverCylce_set_complete_riverbook_SetsAttr():
    # ESTABLISH
    one_int = 1
    yao_str = "Yao"
    one_rivercycle = rivercycle_shop(yao_str, one_int)
    bob_book_point_amount = 555
    bob_str = "Bob"
    bob_riverbook = create_riverbook(bob_str, {}, bob_book_point_amount)
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle._set_complete_riverbook(bob_riverbook)

    # THEN
    assert one_rivercycle.riverbooks == {bob_str: bob_riverbook}


def test_RiverCylce_set_riverbook_SetsAttr():
    # ESTABLISH
    one_int = 1
    yao_str = "Yao"
    bob_str = "Bob"
    keep_credorledger = {bob_str: {yao_str: 75, bob_str: 25}}
    one_rivercycle = rivercycle_shop(yao_str, one_int, keep_credorledger)
    bob_book_point_amount = 500
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle.set_riverbook(bob_str, bob_book_point_amount)

    # THEN
    bob_credorledger = keep_credorledger.get(bob_str)
    bob_riverbook = create_riverbook(bob_str, bob_credorledger, bob_book_point_amount)
    assert one_rivercycle.riverbooks == {bob_str: bob_riverbook}


def test_RiverCylce_create_cylceledger_ReturnsObjOneRiverBook():
    # ESTABLISH
    yao_str = "Yao"
    one_int = 1
    yao_credorledger = {yao_str: {yao_str: 334.0}}
    one_rivercycle = rivercycle_shop(yao_str, one_int, yao_credorledger)
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
    one_int = 1
    keep_credorledgers = {
        yao_str: {yao_str: 75, bob_str: 25},
        bob_str: {yao_str: 49, bob_str: 51},
    }
    one_rivercycle = rivercycle_shop(yao_str, one_int, keep_credorledgers)
    yao_book_point_amount = 500
    bob_book_point_amount = 100000
    one_rivercycle.set_riverbook(yao_str, yao_book_point_amount)
    one_rivercycle.set_riverbook(bob_str, bob_book_point_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    yao_mana = (yao_book_point_amount * 0.75) + (bob_book_point_amount * 0.49)
    bob_mana = (yao_book_point_amount * 0.25) + (bob_book_point_amount * 0.51)
    assert one_cylceledger == {yao_str: yao_mana, bob_str: bob_mana}


def test_create_init_rivercycle_ReturnsObj_Scenario1_voiceunit():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(yao_str)
    yao_credorledger = get_credorledger(yao_belief)
    keep_credorledgers = {yao_str: yao_credorledger}
    keep_magnitude = 1200

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(
        yao_str, keep_credorledgers, keep_magnitude
    )

    # THEN
    assert yao_init_rivercycle.healer_name == yao_str
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    assert yao_init_rivercycle.riverbooks.get(yao_str) is not None


def test_create_init_rivercycle_ReturnsObj_Scenario2_magnitude_Default():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_voice_cred_lumen = 7
    bob_voice_cred_lumen = 3
    zia_voice_cred_lumen = 10
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(yao_str, yao_voice_cred_lumen)
    yao_belief.add_voiceunit(bob_str, bob_voice_cred_lumen)
    yao_belief.add_voiceunit(zia_str, zia_voice_cred_lumen)
    yao_credorledger = get_credorledger(yao_belief)
    keep_credorledgers = {yao_str: yao_credorledger}
    print(f"{keep_credorledgers=}")

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_str, keep_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    yao_riverbook = yao_init_rivercycle.riverbooks.get(yao_str)
    assert yao_riverbook is not None
    assert len(yao_riverbook._rivergrants) == 3
    assert yao_riverbook._rivergrants.get(yao_str) == 350000000
    assert yao_riverbook._rivergrants.get(bob_str) == 150000000
    assert yao_riverbook._rivergrants.get(zia_str) == 500000000


def test_create_init_rivercycle_ReturnsObj_Scenario3_voiceunit():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_voice_cred_lumen = 7
    bob_voice_cred_lumen = 3
    zia_voice_cred_lumen = 10
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(yao_str, yao_voice_cred_lumen)
    yao_belief.add_voiceunit(bob_str, bob_voice_cred_lumen)
    yao_belief.add_voiceunit(zia_str, zia_voice_cred_lumen)
    yao_credorledger = get_credorledger(yao_belief)
    keep_credorledgers = {yao_str: yao_credorledger}
    print(f"{keep_credorledgers=}")

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(
        yao_str, keep_credorledgers, keep_point_magnitude=1001
    )

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    yao_riverbook = yao_init_rivercycle.riverbooks.get(yao_str)
    assert yao_riverbook is not None
    assert len(yao_riverbook._rivergrants) == 3
    assert yao_riverbook._rivergrants.get(yao_str) == 350
    assert yao_riverbook._rivergrants.get(bob_str) == 150
    assert yao_riverbook._rivergrants.get(zia_str) == 501


def test_create_next_rivercycle_ReturnsObj_ScenarioThree_voiceunit():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_credorledger = example_yao_credorledger()
    bob_credorledger = example_bob_credorledger()
    zia_credorledger = example_zia_credorledger()
    keep_credorledgers = {
        yao_str: yao_credorledger,
        bob_str: bob_credorledger,
        zia_str: zia_credorledger,
    }
    print(f"{keep_credorledgers=}")
    init_rivercycle = create_init_rivercycle(yao_str, keep_credorledgers)
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
    yao_credorledger = example_yao_credorledger()
    bob_credorledger = example_bob_credorledger()
    zia_credorledger = example_zia_credorledger()
    keep_credorledgers = {
        yao_str: yao_credorledger,
        bob_str: bob_credorledger,
        zia_str: zia_credorledger,
    }
    print(f"{keep_credorledgers=}")
    init_rivercycle = create_init_rivercycle(yao_str, keep_credorledgers)
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
