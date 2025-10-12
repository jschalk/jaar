from src.ch03_allot_toolbox.allot import default_grain_num_if_None
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch14_keep_logic.rivercycle import (
    RiverBook,
    create_riverbook,
    get_credorledger,
    riverbook_shop,
)
from src.ch14_keep_logic.test._util.ch14_env import temp_moment_mstr_dir
from src.ref.ch14_keywords import Ch14Keywords as wx


def test_RiverBook_Exists():
    # ESTABLISH / WHEN
    x_riverbook = RiverBook()

    # THEN
    assert not x_riverbook.belief_name
    assert not x_riverbook._rivergrants
    assert not x_riverbook.money_grain
    assert set(x_riverbook.__dict__.keys()) == {
        wx.belief_name,
        wx._rivergrants,
        wx.money_grain,
    }


def test_riverbook_shop_ReturnsObj_Scenario0_money_grain_IsNone():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_riverbook = riverbook_shop(bob_str)

    # THEN
    assert bob_riverbook.belief_name == bob_str
    assert bob_riverbook._rivergrants == {}
    assert bob_riverbook.money_grain == default_grain_num_if_None()


def test_riverbook_shop_ReturnsObj_Scenario1_money_grain_Exists():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_grain = 3
    assert bob_money_grain != default_grain_num_if_None()

    # WHEN
    bob_riverbook = riverbook_shop(bob_str, bob_money_grain)

    # THEN
    assert bob_riverbook.belief_name == bob_str
    assert bob_riverbook._rivergrants == {}
    assert bob_riverbook.money_grain == bob_money_grain


def test_create_riverbook_ReturnsObj_Scenario0_money_grain_IsNone():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(yao_str)
    yao_belief.add_voiceunit(sue_str)
    yao_book_point_amount = 500
    yao_credorledger = get_credorledger(yao_belief)

    # WHEN
    yao_riverbook = create_riverbook(yao_str, yao_credorledger, yao_book_point_amount)

    # THEN
    assert yao_riverbook.belief_name == yao_str
    assert yao_riverbook._rivergrants == {yao_str: 250, sue_str: 250}
    assert sum(yao_riverbook._rivergrants.values()) == yao_book_point_amount
    assert yao_riverbook.money_grain == default_grain_num_if_None()


def test_create_riverbook_ReturnsObj_Scenario0_money_grain_ArgPassed():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(yao_str)
    yao_belief.add_voiceunit(sue_str)
    yao_book_point_amount = 500
    yao_credorledger = get_credorledger(yao_belief)
    yao_money_grain = 4

    # WHEN
    yao_riverbook = create_riverbook(
        yao_str, yao_credorledger, yao_book_point_amount, yao_money_grain
    )

    # THEN
    assert yao_riverbook.belief_name == yao_str
    assert yao_riverbook._rivergrants == {yao_str: 248, sue_str: 252}
    assert sum(yao_riverbook._rivergrants.values()) == yao_book_point_amount
    assert yao_riverbook.money_grain == yao_money_grain
