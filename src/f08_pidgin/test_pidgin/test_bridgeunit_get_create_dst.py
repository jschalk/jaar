from src.f01_road.road import create_road
from src.f04_gift.atom_config import (
    type_RoadNode_str,
    type_RoadUnit_str,
    type_GroupID_str,
)
from src.f08_pidgin.pidgin import bridgeunit_shop


def test_BridgeUnit_reveal_inx_ReturnsObjAndSetsAttr_label():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    otx_r_wall = "/"
    casa_otx = "casa"
    casa_inx = "casa"
    inx_r_wall = ":"
    roadnode_bridgeunit = bridgeunit_shop("RoadNode", otx_r_wall, inx_r_wall)
    roadnode_bridgeunit.set_otx2inx(clean_otx, clean_inx)
    roadnode_bridgeunit.set_otx2inx(casa_otx, casa_inx)
    assert roadnode_bridgeunit.is_valid()

    # WHEN / THEN
    assert roadnode_bridgeunit.reveal_inx(clean_otx) == clean_inx
    assert roadnode_bridgeunit.reveal_inx(casa_otx) == casa_inx
    swim_str = "swim"
    assert roadnode_bridgeunit.reveal_inx(swim_str, False) is None
    assert roadnode_bridgeunit.otx_exists(swim_str) is False

    # WHEN
    assert roadnode_bridgeunit.reveal_inx(swim_str) == swim_str
    # THEN
    assert roadnode_bridgeunit.otx_exists(swim_str)

    # WHEN / THEN
    fail_clean_otx = f"clean{inx_r_wall}"
    assert roadnode_bridgeunit.otx_exists(fail_clean_otx) is False
    assert roadnode_bridgeunit.reveal_inx(fail_clean_otx) is None
    assert roadnode_bridgeunit.otx_exists(fail_clean_otx) is False


def test_BridgeUnit_reveal_inx_ReturnsObjAndSetsAttr_label_With_nub_label():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    otx_r_wall = "/"
    casa_otx = "casa"
    casa_inx = "house"
    inx_r_wall = ":"
    roadnode_bridgeunit = bridgeunit_shop("RoadNode", otx_r_wall, inx_r_wall)
    roadnode_bridgeunit.set_otx2inx(clean_otx, clean_inx)
    roadnode_bridgeunit.set_nub_label(casa_otx, casa_inx)
    assert casa_otx != casa_inx
    assert roadnode_bridgeunit.nub_label_exists(casa_otx, casa_inx)
    assert roadnode_bridgeunit.otx2inx_exists(casa_otx, casa_inx) is False

    # WHEN
    generated_inx = roadnode_bridgeunit.reveal_inx(casa_otx)

    # THEN
    assert generated_inx == casa_inx
    assert roadnode_bridgeunit.nub_label_exists(casa_otx, casa_inx)
    assert roadnode_bridgeunit.otx2inx_exists(casa_otx, casa_inx)
    print(f"{casa_inx=}")


def test_BridgeUnit_reveal_inx_ReturnsObjAndSetsAttr_road_Scenario0():
    # ESTABLISH
    otx_music45_str = "music45"
    otx_r_wall = "/"
    inx_r_wall = ":"
    road_bridgeunit = bridgeunit_shop("RoadUnit", otx_r_wall, inx_r_wall)
    assert road_bridgeunit.otx_exists(otx_music45_str) is False
    assert road_bridgeunit.otx2inx_exists(otx_music45_str, otx_music45_str) is False

    # WHEN
    gen_inx_road = road_bridgeunit.reveal_inx(otx_music45_str)

    # THEN
    assert gen_inx_road == otx_music45_str
    assert road_bridgeunit.otx_exists(otx_music45_str)
    assert road_bridgeunit.otx2inx_exists(otx_music45_str, otx_music45_str)


def test_BridgeUnit_reveal_inx_ReturnsObjAndSetsAttr_road_Scenario1():
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    otx_r_wall = "/"
    inx_r_wall = ":"
    clean_otx_str = "clean"
    clean_otx_road = f"{otx_music45_str}{otx_r_wall}{clean_otx_str}"
    road_bridgeunit = bridgeunit_shop("RoadUnit", otx_r_wall, inx_r_wall)
    assert road_bridgeunit.otx_exists(otx_music45_str) is False
    assert road_bridgeunit.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_bridgeunit.reveal_inx(clean_otx_road)

    # THEN
    assert gen_inx_road is None
    assert road_bridgeunit.otx_exists(otx_music45_str) is False
    assert road_bridgeunit.otx_exists(clean_otx_road) is False
    assert road_bridgeunit.otx2inx_exists(otx_music45_str, inx_music87_str) is False

    # ESTABLISH
    road_bridgeunit.set_otx2inx(otx_music45_str, inx_music87_str)
    assert road_bridgeunit.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert road_bridgeunit.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_bridgeunit.reveal_inx(clean_otx_road)

    # THEN
    assert road_bridgeunit.otx_exists(clean_otx_road)
    assert road_bridgeunit.otx2inx_exists(clean_otx_road, gen_inx_road)
    assert gen_inx_road == f"{inx_music87_str}{inx_r_wall}{clean_otx_str}"


def test_BridgeUnit_reveal_inx_ReturnsObjAndSetsAttr_road_Scenario2_With_nub_label():
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    otx_r_wall = "/"
    inx_r_wall = ":"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    clean_otx_road = f"{otx_music45_str}{otx_r_wall}{clean_otx_str}"
    road_bridgeunit = bridgeunit_shop("RoadUnit", otx_r_wall, inx_r_wall)
    road_bridgeunit.set_nub_label(clean_otx_str, clean_inx_str)
    assert road_bridgeunit.otx_exists(otx_music45_str) is False
    assert road_bridgeunit.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_bridgeunit.reveal_inx(clean_otx_road)

    # THEN
    assert gen_inx_road is None
    assert road_bridgeunit.otx_exists(otx_music45_str) is False
    assert road_bridgeunit.otx_exists(clean_otx_road) is False
    assert road_bridgeunit.otx2inx_exists(otx_music45_str, inx_music87_str) is False

    # ESTABLISH
    road_bridgeunit.set_otx2inx(otx_music45_str, inx_music87_str)
    assert road_bridgeunit.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert road_bridgeunit.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_bridgeunit.reveal_inx(clean_otx_road)

    # THEN
    assert road_bridgeunit.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert road_bridgeunit.otx_exists(clean_otx_road)
    assert road_bridgeunit.otx2inx_exists(clean_otx_road, gen_inx_road)
    assert gen_inx_road == f"{inx_music87_str}{inx_r_wall}{clean_inx_str}"


def test_BridgeUnit_reveal_inx_ReturnsObjAndSetsAttr_group_id():
    # ESTABLISH
    inx_r_wall = ":"
    otx_r_wall = "/"
    swim_otx = f"swim{otx_r_wall}"
    climb_otx = f"climb{otx_r_wall}_{inx_r_wall}"
    group_id_bridgeunit = bridgeunit_shop("GroupID", otx_r_wall, inx_r_wall)
    group_id_bridgeunit.otx_exists(swim_otx) is False
    group_id_bridgeunit.otx_exists(climb_otx) is False

    # WHEN
    swim_inx = f"swim{inx_r_wall}"
    assert group_id_bridgeunit.reveal_inx(swim_otx) == swim_inx

    # THEN
    assert group_id_bridgeunit.otx_exists(swim_otx)
    assert group_id_bridgeunit.otx_exists(climb_otx) is False
    assert group_id_bridgeunit._get_inx_value(swim_otx) == swim_inx

    # WHEN
    assert group_id_bridgeunit.reveal_inx(climb_otx) is None
    # THEN
    assert group_id_bridgeunit.otx_exists(swim_otx)
    assert group_id_bridgeunit.otx_exists(climb_otx) is False


def test_BridgeUnit_reveal_inx_AddsMissingObjsTo_otx2inx_RoadNode():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    otx_r_wall = "/"
    casa_otx = "casa"
    casa_inx = "casa"
    inx_r_wall = ":"
    roadnode_bridgeunit = bridgeunit_shop("RoadNode", otx_r_wall, inx_r_wall)
    roadnode_bridgeunit.set_otx2inx(clean_otx, clean_inx)
    roadnode_bridgeunit.set_otx2inx(casa_otx, casa_inx)
    swim_str = "swim"
    assert roadnode_bridgeunit.otx_exists(swim_str) is False

    # WHEN
    assert roadnode_bridgeunit.reveal_inx(swim_str, True) == swim_str

    # THEN
    assert roadnode_bridgeunit.otx_exists(swim_str)
    assert roadnode_bridgeunit.otx2inx_exists(swim_str, swim_str)


def test_BridgeUnit_reveal_inx_AddsMissingObjsTo_otx2inx_RoadUnit():
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_music45_str, casa_otx_str)
    casa_inx_road = create_road(inx_music87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)
    road_bd = bridgeunit_shop("RoadUnit")
    road_bd.set_nub_label(otx_music45_str, inx_music87_str)
    road_bd.set_nub_label(casa_otx_str, casa_inx_str)
    road_bd.set_nub_label(clean_otx_str, clean_inx_str)
    assert road_bd.otx_exists(otx_music45_str) is False
    assert road_bd.otx_exists(casa_otx_road) is False
    assert road_bd.otx_exists(clean_otx_road) is False
    assert road_bd.otx_exists(sweep_otx_road) is False
    assert road_bd.otx2inx_exists(otx_music45_str, inx_music87_str) is False
    assert road_bd.otx2inx_exists(casa_otx_road, casa_inx_road) is False
    assert road_bd.otx2inx_exists(clean_otx_road, clean_inx_road) is False
    assert road_bd.otx2inx_exists(sweep_otx_road, sweep_inx_road) is False

    # WHEN
    assert road_bd.reveal_inx(otx_music45_str) == inx_music87_str
    # THEN
    assert road_bd.otx_exists(otx_music45_str)
    assert road_bd.otx_exists(casa_otx_road) is False
    assert road_bd.otx_exists(clean_otx_road) is False
    assert road_bd.otx_exists(sweep_otx_road) is False
    assert road_bd.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert road_bd.otx2inx_exists(casa_otx_road, casa_inx_road) is False
    assert road_bd.otx2inx_exists(clean_otx_road, clean_inx_road) is False
    assert road_bd.otx2inx_exists(sweep_otx_road, sweep_inx_road) is False

    # WHEN
    assert road_bd.reveal_inx(casa_otx_road) == casa_inx_road
    # THEN
    assert road_bd.otx_exists(otx_music45_str)
    assert road_bd.otx_exists(casa_otx_road)
    assert road_bd.otx_exists(clean_otx_road) is False
    assert road_bd.otx_exists(sweep_otx_road) is False
    assert road_bd.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert road_bd.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert road_bd.otx2inx_exists(clean_otx_road, clean_inx_road) is False
    assert road_bd.otx2inx_exists(sweep_otx_road, sweep_inx_road) is False

    # WHEN
    assert road_bd.reveal_inx(clean_otx_road) == clean_inx_road
    assert road_bd.reveal_inx(sweep_otx_road) == sweep_inx_road
    # THEN
    assert road_bd.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert road_bd.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert road_bd.otx2inx_exists(clean_otx_road, clean_inx_road)
    assert road_bd.otx2inx_exists(sweep_otx_road, sweep_inx_road)
