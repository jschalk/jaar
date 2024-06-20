from src._road.finance import default_penny_if_none, default_money_magnitude
from src.agenda.agenda import agendaunit_shop
from src.money.river_cycle import (
    RiverBook,
    riverbook_shop,
    create_riverbook,
    RiverCycle,
    rivercycle_shop,
    create_init_rivercycle,
)
from src.money.scale_distribution import get_credorledger


def test_RiverBook_Exists():
    # GIVEN / WHEN
    x_riverbook = RiverBook()

    # THEN
    assert x_riverbook._owner_id is None
    assert x_riverbook._money_amount is None
    assert x_riverbook._rivergrants is None
    assert x_riverbook.penny is None


def test_riverbook_shop_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"

    # WHEN
    yao_riverbook = riverbook_shop(yao_text, default_money_magnitude(), penny=None)

    # THEN
    assert yao_riverbook._owner_id == yao_text
    assert yao_riverbook._money_amount == default_money_magnitude()
    assert yao_riverbook._rivergrants == {}
    assert yao_riverbook.penny == default_penny_if_none()


def test_create_riverbook_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(yao_text)
    yao_agenda.add_otherunit(sue_text)
    yao_money_amount = 500

    # WHEN
    yao_credorledger = get_credorledger(yao_agenda)
    yao_riverbook = create_riverbook(yao_text, yao_credorledger, yao_money_amount)

    # THEN
    assert yao_riverbook._owner_id == yao_text
    assert yao_riverbook._money_amount == yao_money_amount
    assert yao_riverbook._rivergrants == {yao_text: 250, sue_text: 250}


def test_RiverCylce_Exists():
    # GIVEN / WHEN
    x_rivercycle = RiverCycle()

    # THEN
    assert x_rivercycle.number is None
    assert x_rivercycle.credorledgers is None
    assert x_rivercycle.riverbooks is None
    assert x_rivercycle.money_amount is None
    assert x_rivercycle.penny is None


def test_rivercycle_shop_ReturnsCorrectObj():
    # GIVEN
    one_int = 1

    # WHEN
    one_rivercycle = rivercycle_shop(one_int)

    # THEN
    assert one_rivercycle.number == 1
    assert one_rivercycle.credorledgers == {}
    assert one_rivercycle.riverbooks == {}
    assert one_rivercycle.money_amount == default_money_magnitude()
    assert one_rivercycle.penny == default_penny_if_none()


def test_RiverCylce_set_riverbook_CorrectlySetsAttr():
    # GIVEN
    one_int = 1
    one_rivercycle = rivercycle_shop(one_int)
    yao_text = "Yao"
    yao_riverbook = riverbook_shop(yao_text, default_money_magnitude(), penny=None)
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle.set_riverbook(yao_riverbook)

    # THEN
    assert one_rivercycle.riverbooks == {yao_text: yao_riverbook}


def test_create_zebra_WorksForSingleUser():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(yao_text)
    yao_credorledger = get_credorledger(yao_agenda)
    all_credorledgers = {yao_text: yao_credorledger}

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_text, all_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    assert yao_init_rivercycle.riverbooks.get(yao_text) != None
