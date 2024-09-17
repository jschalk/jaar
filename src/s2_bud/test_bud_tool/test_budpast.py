from src.s2_bud.bud import budunit_shop
from src.s2_bud.bud_tool import BudEvent, budevent_shop


def test_BudEvent_Exists():
    # ESTABLISH / WHEN
    x_budevent = BudEvent()

    # THEN
    assert x_budevent
    assert not x_budevent.fiscal_id
    assert not x_budevent.owner_id
    assert not x_budevent.timestamp
    assert not x_budevent._bud
    assert not x_budevent._money_magnitude
    assert not x_budevent._money_desc


def test_budevent_shop_ReturnsObj():
    # ESTABLISH
    music_str = "Music45"
    sue_str = "Sue"

    # WHEN
    x_budevent = budevent_shop(music_str, sue_str)

    # THEN
    assert x_budevent
    assert x_budevent.fiscal_id == music_str
    assert x_budevent.owner_id == sue_str
    assert not x_budevent.timestamp
    assert not x_budevent._bud
    assert not x_budevent._money_magnitude
    assert not x_budevent._money_desc
