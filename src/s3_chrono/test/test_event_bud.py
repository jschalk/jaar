from src.s2_bud.bud import budunit_shop
from src.s3_chrono.bud_event import (
    OwnerBudEvent,
    ownerbudevent_shop,
    OwnerBudEvents,
    ownerbudevents_shop,
)


def test_OwnerBudEvent_Exists():
    # ESTABLISH / WHEN
    x_ownerbudevent = OwnerBudEvent()

    # THEN
    assert x_ownerbudevent
    assert not x_ownerbudevent.fiscal_id
    assert not x_ownerbudevent.owner_id
    assert not x_ownerbudevent.timestamp
    assert not x_ownerbudevent._bud
    assert not x_ownerbudevent._money_magnitude
    assert not x_ownerbudevent._money_desc


def test_ownerbudevent_shop_ReturnsObj():
    # ESTABLISH
    music_str = "Music45"
    sue_str = "Sue"

    # WHEN
    x_ownerbudevent = ownerbudevent_shop(music_str, sue_str)

    # THEN
    assert x_ownerbudevent
    assert x_ownerbudevent.fiscal_id == music_str
    assert x_ownerbudevent.owner_id == sue_str
    assert not x_ownerbudevent.timestamp
    assert not x_ownerbudevent._bud
    assert not x_ownerbudevent._money_magnitude
    assert not x_ownerbudevent._money_desc


def test_OwnerBudEvents_Exists():
    # ESTABLISH / WHEN
    x_ownerbudevents = OwnerBudEvents()

    # THEN
    assert x_ownerbudevents
    assert not x_ownerbudevents.fiscal_id
    assert not x_ownerbudevents.owner_id
    assert not x_ownerbudevents.events
    assert not x_ownerbudevents._sum_money_magnitude
    assert not x_ownerbudevents._sum_acct_outlays
    assert not x_ownerbudevents._timestamp_min
    assert not x_ownerbudevents._timestamp_max


def test_ownerbudevents_shop_ReturnsObj():
    # ESTABLISH
    music_str = "Music45"
    sue_str = "Sue"

    # WHEN
    x_ownerbudevents = ownerbudevents_shop(music_str, sue_str)

    # THEN
    assert x_ownerbudevents
    assert x_ownerbudevents.fiscal_id == music_str
    assert x_ownerbudevents.owner_id == sue_str
    assert x_ownerbudevents.events == {}
    assert not x_ownerbudevents._sum_money_magnitude
    assert x_ownerbudevents._sum_acct_outlays == {}
    assert not x_ownerbudevents._timestamp_min
    assert not x_ownerbudevents._timestamp_max
