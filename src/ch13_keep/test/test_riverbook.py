from src.ch02_allot.allot import default_grain_num_if_None
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch13_keep.rivercycle import (
    RiverBook,
    create_riverbook,
    get_patientledger,
    riverbook_shop,
)
from src.ref.keywords import Ch13Keywords as kw


def test_RiverBook_Exists():
    # ESTABLISH / WHEN
    x_riverbook = RiverBook()

    # THEN
    assert not x_riverbook.belief_name
    assert not x_riverbook._rivercares
    assert not x_riverbook.mana_grain
    assert set(x_riverbook.__dict__.keys()) == {
        kw.belief_name,
        kw._rivercares,
        kw.mana_grain,
    }


def test_riverbook_shop_ReturnsObj_Scenario0_mana_grain_IsNone():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_riverbook = riverbook_shop(bob_str)

    # THEN
    assert bob_riverbook.belief_name == bob_str
    assert bob_riverbook._rivercares == {}
    assert bob_riverbook.mana_grain == default_grain_num_if_None()


def test_riverbook_shop_ReturnsObj_Scenario1_mana_grain_Exists():
    # ESTABLISH
    bob_str = "Bob"
    bob_mana_grain = 3
    assert bob_mana_grain != default_grain_num_if_None()

    # WHEN
    bob_riverbook = riverbook_shop(bob_str, bob_mana_grain)

    # THEN
    assert bob_riverbook.belief_name == bob_str
    assert bob_riverbook._rivercares == {}
    assert bob_riverbook.mana_grain == bob_mana_grain


def test_create_riverbook_ReturnsObj_Scenario0_mana_grain_IsNone():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(yao_str)
    yao_belief.add_voiceunit(sue_str)
    yao_book_point_amount = 500
    yao_patientledger = get_patientledger(yao_belief)

    # WHEN
    yao_riverbook = create_riverbook(yao_str, yao_patientledger, yao_book_point_amount)

    # THEN
    assert yao_riverbook.belief_name == yao_str
    assert yao_riverbook._rivercares == {yao_str: 250, sue_str: 250}
    assert sum(yao_riverbook._rivercares.values()) == yao_book_point_amount
    assert yao_riverbook.mana_grain == default_grain_num_if_None()


def test_create_riverbook_ReturnsObj_Scenario0_mana_grain_ArgPassed():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(yao_str)
    yao_belief.add_voiceunit(sue_str)
    yao_book_point_amount = 500
    yao_patientledger = get_patientledger(yao_belief)
    yao_mana_grain = 4

    # WHEN
    yao_riverbook = create_riverbook(
        yao_str, yao_patientledger, yao_book_point_amount, yao_mana_grain
    )

    # THEN
    assert yao_riverbook.belief_name == yao_str
    assert yao_riverbook._rivercares == {yao_str: 248, sue_str: 252}
    assert sum(yao_riverbook._rivercares.values()) == yao_book_point_amount
    assert yao_riverbook.mana_grain == yao_mana_grain
