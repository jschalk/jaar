from src._road.road import LobbyID
from src.bud.reason_doer import (
    DoerUnit,
    doerunit_shop,
    DoerHeir,
    doerheir_shop,
    create_doerunit,
)
from src.bud.lobby import lobbyship_shop
from src.bud.lobby import lobbybox_shop
from pytest import raises as pytest_raises


def test_DoerUnit_exists():
    # ESTABLISH
    x_lobbyholds = {1}

    # WHEN
    x_doerunit = DoerUnit(_lobbyholds=x_lobbyholds)

    # THEN
    assert x_doerunit
    assert x_doerunit._lobbyholds == x_lobbyholds


def test_doerunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    x_lobbyholds = {1}

    # WHEN
    x_doerunit = doerunit_shop(_lobbyholds=x_lobbyholds)

    # THEN
    assert x_doerunit
    assert x_doerunit._lobbyholds == x_lobbyholds


def test_doerunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_doerunit = doerunit_shop()

    # THEN
    assert x_doerunit
    assert x_doerunit._lobbyholds == set()


def test_create_doerunit_ReturnsCorrectObj():
    # ESTABLISH
    swim_lobby_id = LobbyID("swimmers")

    # WHEN
    swim_doerunit = create_doerunit(swim_lobby_id)

    # THEN
    assert swim_doerunit
    assert len(swim_doerunit._lobbyholds) == 1


def test_DoerUnit_get_dict_ReturnsCorrectDictWithSingle_lobbyhold():
    # ESTABLISH
    bob_lobby_id = LobbyID("Bob")
    x_lobbyholds = {bob_lobby_id: bob_lobby_id}
    x_doerunit = doerunit_shop(_lobbyholds=x_lobbyholds)

    # WHEN
    obj_dict = x_doerunit.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_lobbyholds": [bob_lobby_id]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_DoerUnit_set_lobbyhold_CorrectlySets_lobbyholds_v1():
    # ESTABLISH
    x_doerunit = doerunit_shop()
    assert len(x_doerunit._lobbyholds) == 0

    # WHEN
    yao_text = "Yao"
    x_doerunit.set_lobbyhold(lobby_id=yao_text)

    # THEN
    assert len(x_doerunit._lobbyholds) == 1


def test_DoerUnit_lobbyhold_exists_ReturnsCorrectObj():
    # ESTABLISH
    x_doerunit = doerunit_shop()
    yao_text = "Yao"
    assert x_doerunit.lobbyhold_exists(yao_text) is False

    # WHEN
    x_doerunit.set_lobbyhold(lobby_id=yao_text)

    # THEN
    assert x_doerunit.lobbyhold_exists(yao_text)


def test_DoerUnit_del_lobbyhold_CorrectlyDeletes_lobbyholds_v1():
    # ESTABLISH
    x_doerunit = doerunit_shop()
    yao_text = "Yao"
    sue_text = "Sue"
    x_doerunit.set_lobbyhold(lobby_id=yao_text)
    x_doerunit.set_lobbyhold(lobby_id=sue_text)
    assert len(x_doerunit._lobbyholds) == 2

    # WHEN
    x_doerunit.del_lobbyhold(lobby_id=sue_text)

    # THEN
    assert len(x_doerunit._lobbyholds) == 1


def test_DoerHeir_exists():
    # ESTABLISH
    x_lobbyholds = {1}
    _owner_id_x_doerunit = True

    # WHEN
    x_doerheir = DoerHeir(_lobbyholds=x_lobbyholds, _owner_id_doer=_owner_id_x_doerunit)

    # THEN
    assert x_doerheir
    assert x_doerheir._lobbyholds == x_lobbyholds
    assert x_doerheir._owner_id_doer == _owner_id_x_doerunit


def test_doerheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    x_lobbyholds = {1}
    _owner_id_x_doerunit = "example"

    # WHEN
    x_doerheir = doerheir_shop(
        _lobbyholds=x_lobbyholds, _owner_id_doer=_owner_id_x_doerunit
    )

    # THEN
    assert x_doerheir
    assert x_doerheir._lobbyholds == x_lobbyholds
    assert x_doerheir._owner_id_doer == _owner_id_x_doerunit


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_Emptyx_lobbyholds():
    # ESTABLISH
    x_lobbyholds = set()
    x_doerheir = doerheir_shop(_lobbyholds=x_lobbyholds)
    assert x_doerheir._owner_id_doer is False

    # WHEN
    bud_lobbyboxs = {}
    x_doerheir.set_owner_id_doer(bud_lobbyboxs, bud_owner_id="")

    # THEN
    assert x_doerheir._owner_id_doer


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_NonEmptyx_lobbyholds_v1():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    yao_lobbybox = lobbybox_shop(yao_text)
    sue_lobbybox = lobbybox_shop(sue_text)
    yao_lobbybox.set_lobbyship(lobbyship_shop(yao_text, _char_id=yao_text))
    sue_lobbybox.set_lobbyship(lobbyship_shop(sue_text, _char_id=sue_text))
    x_lobbyboxs = {yao_text: yao_lobbybox, sue_text: sue_lobbybox}
    bud_owner_id = yao_text

    x_lobbyholds = {yao_text}
    x_doerheir = doerheir_shop(_lobbyholds=x_lobbyholds)
    assert x_doerheir._owner_id_doer is False

    # WHEN
    x_doerheir.set_owner_id_doer(x_lobbyboxs, bud_owner_id)

    # THEN
    assert x_doerheir._owner_id_doer


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_NonEmptyx_lobbyholds_v2():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    yao_lobbybox = lobbybox_shop(yao_text)
    sue_lobbybox = lobbybox_shop(sue_text)
    yao_lobbybox.set_lobbyship(lobbyship_shop(yao_text, _char_id=yao_text))
    sue_lobbybox.set_lobbyship(lobbyship_shop(sue_text, _char_id=sue_text))
    x_lobbyboxs = {yao_text: yao_lobbybox, sue_text: sue_lobbybox}
    x_lobbyholds = {sue_text}
    x_doerheir = doerheir_shop(_lobbyholds=x_lobbyholds)
    assert yao_lobbybox.get_lobbyship(yao_text) != None
    assert x_doerheir._owner_id_doer is False

    # WHEN
    x_doerheir.set_owner_id_doer(x_lobbyboxs, yao_text)

    # THEN
    assert x_doerheir._owner_id_doer is False


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_NonEmptyx_lobbyholds_v3():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    bob_text = "Bob"
    yao_lobbybox = lobbybox_shop(yao_text)
    sue_lobbybox = lobbybox_shop(sue_text)
    bob_lobbybox = lobbybox_shop(bob_text)
    yao_lobbybox.set_lobbyship(lobbyship_shop(yao_text, _char_id=yao_text))
    sue_lobbybox.set_lobbyship(lobbyship_shop(sue_text, _char_id=sue_text))

    swim_text = ",swim"
    swim_lobbybox = lobbybox_shop(lobby_id=swim_text)
    swim_lobbybox.set_lobbyship(lobbyship_shop(swim_text, _char_id=yao_text))
    swim_lobbybox.set_lobbyship(lobbyship_shop(swim_text, _char_id=sue_text))
    x_lobbyboxs = {
        yao_text: yao_lobbybox,
        sue_text: sue_lobbybox,
        bob_text: bob_lobbybox,
        swim_text: swim_lobbybox,
    }

    x_lobbyholds = {swim_text}
    x_doerheir = doerheir_shop(_lobbyholds=x_lobbyholds)
    assert x_doerheir._owner_id_doer is False
    x_doerheir.set_owner_id_doer(x_lobbyboxs, bud_owner_id=yao_text)
    assert x_doerheir._owner_id_doer

    # WHEN
    swim_lobbybox.del_lobbyship(yao_text)
    x_doerheir.set_owner_id_doer(x_lobbyboxs, yao_text)

    # THEN
    assert x_doerheir._owner_id_doer is False


def test_DoerHeir_set_lobbyhold_DoerUnitEmpty_ParentDoerHeirEmpty():
    # ESTABLISH
    x_doerheir = doerheir_shop(_lobbyholds={})
    parent_doerheir_empty = doerheir_shop()
    x_doerunit = doerunit_shop()

    # WHEN
    x_doerheir.set_lobbyholds(
        parent_doerheir=parent_doerheir_empty,
        doerunit=x_doerunit,
        bud_lobbyboxs=None,
    )

    # THEN
    x_doerheir._lobbyholds = {}


def test_DoerHeir_set_lobbyhold_DoerUnitNotEmpty_ParentDoerHeirIsNone():
    # ESTABLISH
    kent_text = "kent"
    swim_text = ",swim"
    x_doerunit = doerunit_shop()
    x_doerunit.set_lobbyhold(lobby_id=kent_text)
    x_doerunit.set_lobbyhold(lobby_id=swim_text)

    # WHEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_lobbyholds(
        parent_doerheir=None, doerunit=x_doerunit, bud_lobbyboxs=None
    )

    # THEN
    assert x_doerheir._lobbyholds == x_doerunit._lobbyholds


def test_DoerHeir_set_lobbyhold_DoerUnitNotEmpty_ParentDoerHeirEmpty():
    # ESTABLISH
    kent_text = "kent"
    swim_text = ",swim"
    x_doerunit = doerunit_shop()
    x_doerunit.set_lobbyhold(lobby_id=kent_text)
    x_doerunit.set_lobbyhold(lobby_id=swim_text)

    # WHEN
    x_doerheir = doerheir_shop()
    parent_doerheir_empty = doerheir_shop()
    x_doerheir.set_lobbyholds(
        parent_doerheir_empty, doerunit=x_doerunit, bud_lobbyboxs=None
    )

    # THEN
    assert x_doerheir._lobbyholds == x_doerunit._lobbyholds


def test_DoerHeir_set_lobbyhold_DoerUnitEmpty_ParentDoerHeirNotEmpty():
    # ESTABLISH
    kent_text = "kent"
    swim_text = ",swim"
    doerunit_swim = doerunit_shop()
    doerunit_swim.set_lobbyhold(lobby_id=kent_text)
    doerunit_swim.set_lobbyhold(lobby_id=swim_text)
    empty_doerheir = doerheir_shop()

    parent_doerheir = doerheir_shop()
    parent_doerheir.set_lobbyholds(empty_doerheir, doerunit_swim, bud_lobbyboxs=None)

    doerunit_empty = doerunit_shop()

    # WHEN
    x_doerheir = doerheir_shop()
    assert x_doerheir._lobbyholds == set()
    x_doerheir.set_lobbyholds(
        parent_doerheir, doerunit=doerunit_empty, bud_lobbyboxs=None
    )

    # THEN
    assert len(x_doerheir._lobbyholds)
    assert x_doerheir._lobbyholds == parent_doerheir._lobbyholds


def test_DoerHeir_set_lobbyhold_DoerUnitEqualParentDoerHeir_NonEmpty():
    # ESTABLISH
    kent_text = "kent"
    swim_text = ",swim"
    doerunit_swim = doerunit_shop()
    doerunit_swim.set_lobbyhold(lobby_id=kent_text)
    doerunit_swim.set_lobbyhold(lobby_id=swim_text)
    empty_doerheir = doerheir_shop()

    parent_doerheir = doerheir_shop()
    parent_doerheir.set_lobbyholds(empty_doerheir, doerunit_swim, bud_lobbyboxs=None)

    # WHEN
    x_doerheir = doerheir_shop()
    assert x_doerheir._lobbyholds == set()
    x_doerheir.set_lobbyholds(
        parent_doerheir, doerunit=doerunit_swim, bud_lobbyboxs=None
    )

    # THEN
    assert x_doerheir._lobbyholds == parent_doerheir._lobbyholds


def test_DoerHeir_set_lobbyhold_DoerUnit_NotEqual_ParentDoerHeir_NonEmpty():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_lobbybox = lobbybox_shop(yao_text)
    sue_lobbybox = lobbybox_shop(sue_text)
    bob_lobbybox = lobbybox_shop(bob_text)
    bob_lobbybox = lobbybox_shop(zia_text)
    yao_lobbybox.set_lobbyship(lobbyship_shop(yao_text, _char_id=yao_text))
    sue_lobbybox.set_lobbyship(lobbyship_shop(sue_text, _char_id=sue_text))

    swim2_text = ",swim2"
    swim2_lobbybox = lobbybox_shop(lobby_id=swim2_text)
    swim2_lobbybox.set_lobbyship(lobbyship_shop(swim2_text, _char_id=yao_text))
    swim2_lobbybox.set_lobbyship(lobbyship_shop(swim2_text, _char_id=sue_text))

    swim3_text = ",swim3"
    swim3_lobbybox = lobbybox_shop(lobby_id=swim3_text)
    swim3_lobbybox.set_lobbyship(lobbyship_shop(swim3_text, _char_id=yao_text))
    swim3_lobbybox.set_lobbyship(lobbyship_shop(swim3_text, _char_id=sue_text))
    swim3_lobbybox.set_lobbyship(lobbyship_shop(swim3_text, _char_id=zia_text))

    x_lobbyboxs = {
        yao_text: yao_lobbybox,
        sue_text: sue_lobbybox,
        bob_text: bob_lobbybox,
        swim2_text: swim2_lobbybox,
        swim3_text: swim3_lobbybox,
    }

    parent_doerunit = doerunit_shop()
    parent_doerunit.set_lobbyhold(lobby_id=swim3_text)
    parent_doerheir = doerheir_shop()
    parent_doerheir.set_lobbyholds(
        parent_doerheir=None, doerunit=parent_doerunit, bud_lobbyboxs=None
    )

    doerunit_swim2 = doerunit_shop()
    doerunit_swim2.set_lobbyhold(lobby_id=swim2_text)

    # WHEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_lobbyholds(parent_doerheir, doerunit_swim2, x_lobbyboxs)

    # THEN
    assert x_doerheir._lobbyholds == doerunit_swim2._lobbyholds
    assert len(x_doerheir._lobbyholds) == 1
    assert list(x_doerheir._lobbyholds) == [swim2_text]


# def test_DoerHeir_set_lobbyhold_DoerUnit_NotEqualParentDoerHeir_RaisesError():
#     # ESTABLISH
#     yao_text = "Yao"
#     sue_text = "Sue"
#     bob_text = "Bob"
#     zia_text = "Zia"
#     yao_lobbybox = lobbybox_shop(yao_text)
#     sue_lobbybox = lobbybox_shop(sue_text)
#     bob_lobbybox = lobbybox_shop(bob_text)
#     bob_lobbybox = lobbybox_shop(zia_text)
#     yao_lobbybox.set_lobbyship(lobbyship_shop(yao_text))
#     sue_lobbybox.set_lobbyship(lobbyship_shop(sue_text))

#     swim2_text = ",swim2"
#     swim2_lobbybox = lobbybox_shop(swim2_text)
#     swim2_lobbybox.set_lobbyship(lobbyship_shop(swim2_text, _char_id=yao_text))
#     swim2_lobbybox.set_lobbyship(lobbyship_shop(swim2_text, _char_id=sue_text))

#     swim3_text = ",swim3"
#     swim3_lobbybox = lobbybox_shop(lobby_id=swim3_text)
#     swim3_lobbybox.set_lobbyship(lobbyship_shop(swim3_text, _char_id=yao_text))
#     swim3_lobbybox.set_lobbyship(lobbyship_shop(swim3_text, _char_id=sue_text))
#     swim3_lobbybox.set_lobbyship(lobbyship_shop(swim3_text, _char_id=zia_text))

#     x_lobbyboxs = {
#         yao_text: yao_lobbybox,
#         sue_text: sue_lobbybox,
#         bob_text: bob_lobbybox,
#         swim2_text: swim2_lobbybox,
#         swim3_text: swim3_lobbybox,
#     }

#     parent_doerunit = doerunit_shop()
#     parent_doerunit.set_lobbyhold(swim2_text)
#     parent_doerheir = doerheir_shop()
#     parent_doerheir.set_lobbyholds(None, parent_doerunit, x_lobbyboxs)

#     doerunit_swim3 = doerunit_shop()
#     doerunit_swim3.set_lobbyhold(lobby_id=swim3_text)

#     # WHEN / THEN
#     x_doerheir = doerheir_shop()
#     all_parent_doerheir_chars = {yao_text, sue_text}
#     all_doerunit_chars = {yao_text, sue_text, zia_text}
#     with pytest_raises(Exception) as excinfo:
#         x_doerheir.set_lobbyholds(parent_doerheir, doerunit_swim3, x_lobbyboxs)
#     assert (
#         str(excinfo.value)
#         == f"parent_doerheir does not contain all chars of the idea's doerunit\n{set(all_parent_doerheir_chars)=}\n\n{set(all_doerunit_chars)=}"
#     )


def test_DoerUnit_get_lobbyhold_ReturnsCorrectObj():
    # ESTABLISH
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_doerunit = doerunit_shop()
    x_doerunit.set_lobbyhold(climb_text)
    x_doerunit.set_lobbyhold(walk_text)
    x_doerunit.set_lobbyhold(swim_text)

    # WHEN / THEN
    assert x_doerunit.get_lobbyhold(walk_text) != None
    assert x_doerunit.get_lobbyhold(swim_text) != None
    assert x_doerunit.get_lobbyhold(run_text) is None


def test_DoerHeir_lobby_id_in_ReturnsCorrectBoolWhen_lobbyholdsNotEmpty():
    # ESTABLISH
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text}
    hike_dict = {hike_text}
    x_doerunit = doerunit_shop()
    x_doerunit.set_lobbyhold(lobby_id=swim_text)
    x_doerunit.set_lobbyhold(lobby_id=hike_text)
    x_doerheir = doerheir_shop()
    x_doerheir.set_lobbyholds(
        parent_doerheir=None, doerunit=x_doerunit, bud_lobbyboxs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert swim_text in x_doerheir._lobbyholds
    assert hike_text in x_doerheir._lobbyholds
    print(f"{hunt_text in x_doerheir._lobbyholds=}")
    assert hunt_text not in x_doerheir._lobbyholds
    assert play_text not in x_doerheir._lobbyholds
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_doerheir.has_lobby(swim_dict)
    assert x_doerheir.has_lobby(hike_dict)
    assert x_doerheir.has_lobby(hunt_dict) is False
    assert x_doerheir.has_lobby(hunt_hike_dict)
    assert x_doerheir.has_lobby(hunt_play_dict) is False


def test_DoerHeir_has_lobby_ReturnsCorrectBoolWhen_lobbyholdsEmpty():
    # ESTABLISH
    hike_text = ",hike"
    hike_dict = {hike_text}
    x_doerunit = doerunit_shop()
    x_doerheir = doerheir_shop()
    x_doerheir.set_lobbyholds(
        parent_doerheir=None, doerunit=x_doerunit, bud_lobbyboxs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert x_doerheir._lobbyholds == set()
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_doerheir.has_lobby(hike_dict)
    assert x_doerheir.has_lobby(hunt_dict)
    assert x_doerheir.has_lobby(play_dict)
    assert x_doerheir.has_lobby(hunt_hike_dict)
    assert x_doerheir.has_lobby(hunt_play_dict)
