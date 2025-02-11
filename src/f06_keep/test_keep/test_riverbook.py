from src.f02_bud.bud import budunit_shop
from src.f05_listen.hubunit import hubunit_shop
from src.f06_keep.rivercycle import (
    RiverBook,
    riverbook_shop,
    create_riverbook,
    get_credorledger,
)
from src.f06_keep.examples.keep_env import temp_fisc_mstr_dir


def test_RiverBook_Exists():
    # ESTABLISH / WHEN
    x_riverbook = RiverBook()

    # THEN
    assert x_riverbook.owner_name is None
    assert x_riverbook.hubunit is None
    assert x_riverbook._rivergrants is None


def test_riverbook_shop_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    x_fisc_mstr_dir = temp_fisc_mstr_dir()
    yao_hubunit = hubunit_shop(x_fisc_mstr_dir, None, yao_str)

    # WHEN
    bob_str = "Bob"
    bob_riverbook = riverbook_shop(yao_hubunit, bob_str)

    # THEN
    assert bob_riverbook.owner_name == bob_str
    assert bob_riverbook.hubunit == yao_hubunit
    assert bob_riverbook._rivergrants == {}


def test_create_riverbook_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(sue_str)
    x_fisc_mstr_dir = temp_fisc_mstr_dir()
    yao_hubunit = hubunit_shop(x_fisc_mstr_dir, None, yao_str)
    yao_book_point_amount = 500

    # WHEN
    yao_credorledger = get_credorledger(yao_bud)
    yao_riverbook = create_riverbook(
        yao_hubunit, yao_str, yao_credorledger, yao_book_point_amount
    )

    # THEN
    assert yao_riverbook.hubunit == yao_hubunit
    assert yao_riverbook.owner_name == yao_str
    assert yao_riverbook._rivergrants == {yao_str: 250, sue_str: 250}
    assert sum(yao_riverbook._rivergrants.values()) == yao_book_point_amount
