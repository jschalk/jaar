from src.f01_road.road import create_road
from src.f08_pidgin.bridge import roadbridge_shop


def test_RoadBridge_reveal_inx_ReturnsObjAndSetsAttr_road_Scenario0():
    # ESTABLISH
    otx_music45_str = "music45"
    otx_r_wall = "/"
    inx_r_wall = ":"
    road_roadbridge = roadbridge_shop(x_otx_wall=otx_r_wall, x_inx_wall=inx_r_wall)
    assert road_roadbridge.otx_exists(otx_music45_str) is False
    assert road_roadbridge.otx2inx_exists(otx_music45_str, otx_music45_str) is False

    # WHEN
    gen_inx_road = road_roadbridge.reveal_inx(otx_music45_str)

    # THEN
    assert gen_inx_road == otx_music45_str
    assert road_roadbridge.otx_exists(otx_music45_str)
    assert road_roadbridge.otx2inx_exists(otx_music45_str, otx_music45_str)


def test_RoadBridge_reveal_inx_ReturnsObjAndSetsAttr_road_Scenario1():
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    otx_r_wall = "/"
    inx_r_wall = ":"
    clean_otx_str = "clean"
    clean_otx_road = f"{otx_music45_str}{otx_r_wall}{clean_otx_str}"
    road_roadbridge = roadbridge_shop(x_otx_wall=otx_r_wall, x_inx_wall=inx_r_wall)
    assert road_roadbridge.otx_exists(otx_music45_str) is False
    assert road_roadbridge.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_roadbridge.reveal_inx(clean_otx_road)

    # THEN
    assert gen_inx_road is None
    assert road_roadbridge.otx_exists(otx_music45_str) is False
    assert road_roadbridge.otx_exists(clean_otx_road) is False
    assert road_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str) is False

    # ESTABLISH
    road_roadbridge.set_otx2inx(otx_music45_str, inx_music87_str)
    assert road_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert road_roadbridge.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_roadbridge.reveal_inx(clean_otx_road)

    # THEN
    assert road_roadbridge.otx_exists(clean_otx_road)
    assert road_roadbridge.otx2inx_exists(clean_otx_road, gen_inx_road)
    assert gen_inx_road == f"{inx_music87_str}{inx_r_wall}{clean_otx_str}"


def test_RoadBridge_reveal_inx_ReturnsObjAndSetsAttr_road_Scenario2_With_idea():
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    otx_r_wall = "/"
    inx_r_wall = ":"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    clean_otx_road = f"{otx_music45_str}{otx_r_wall}{clean_otx_str}"
    road_roadbridge = roadbridge_shop(x_otx_wall=otx_r_wall, x_inx_wall=inx_r_wall)
    road_roadbridge.set_idea(clean_otx_str, clean_inx_str)
    assert road_roadbridge.otx_exists(otx_music45_str) is False
    assert road_roadbridge.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_roadbridge.reveal_inx(clean_otx_road)

    # THEN
    assert gen_inx_road is None
    assert road_roadbridge.otx_exists(otx_music45_str) is False
    assert road_roadbridge.otx_exists(clean_otx_road) is False
    assert road_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str) is False

    # ESTABLISH
    road_roadbridge.set_otx2inx(otx_music45_str, inx_music87_str)
    assert road_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert road_roadbridge.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_roadbridge.reveal_inx(clean_otx_road)

    # THEN
    assert road_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert road_roadbridge.otx_exists(clean_otx_road)
    assert road_roadbridge.otx2inx_exists(clean_otx_road, gen_inx_road)
    assert gen_inx_road == f"{inx_music87_str}{inx_r_wall}{clean_inx_str}"


def test_RoadBridge_reveal_inx_AddsMissingObjsTo_otx2inx_RoadUnit():
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
    x_roadbridge = roadbridge_shop()
    x_roadbridge.set_idea(otx_music45_str, inx_music87_str)
    x_roadbridge.set_idea(casa_otx_str, casa_inx_str)
    x_roadbridge.set_idea(clean_otx_str, clean_inx_str)
    print(f"{x_roadbridge.ideabridge.otx2inx=}")
    print(f"{x_roadbridge.otx2inx=}")
    assert x_roadbridge.otx_exists(otx_music45_str) is False
    assert x_roadbridge.otx_exists(casa_otx_road) is False
    assert x_roadbridge.otx_exists(clean_otx_road) is False
    assert x_roadbridge.otx_exists(sweep_otx_road) is False
    assert x_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str) is False
    assert x_roadbridge.otx2inx_exists(casa_otx_road, casa_inx_road) is False
    assert x_roadbridge.otx2inx_exists(clean_otx_road, clean_inx_road) is False
    assert x_roadbridge.otx2inx_exists(sweep_otx_road, sweep_inx_road) is False

    # WHEN
    assert x_roadbridge.reveal_inx(otx_music45_str) == inx_music87_str
    print(f"{x_roadbridge.ideabridge.otx2inx=}")
    print(f"{x_roadbridge.otx2inx=}")
    # THEN
    assert x_roadbridge.otx_exists(otx_music45_str)
    assert x_roadbridge.otx_exists(casa_otx_road) is False
    assert x_roadbridge.otx_exists(clean_otx_road) is False
    assert x_roadbridge.otx_exists(sweep_otx_road) is False
    assert x_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert x_roadbridge.otx2inx_exists(casa_otx_road, casa_inx_road) is False
    assert x_roadbridge.otx2inx_exists(clean_otx_road, clean_inx_road) is False
    assert x_roadbridge.otx2inx_exists(sweep_otx_road, sweep_inx_road) is False

    # WHEN
    assert x_roadbridge.reveal_inx(casa_otx_road) == casa_inx_road
    # THEN
    assert x_roadbridge.otx_exists(otx_music45_str)
    assert x_roadbridge.otx_exists(casa_otx_road)
    assert x_roadbridge.otx_exists(clean_otx_road) is False
    assert x_roadbridge.otx_exists(sweep_otx_road) is False
    assert x_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert x_roadbridge.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert x_roadbridge.otx2inx_exists(clean_otx_road, clean_inx_road) is False
    assert x_roadbridge.otx2inx_exists(sweep_otx_road, sweep_inx_road) is False

    # WHEN
    assert x_roadbridge.reveal_inx(clean_otx_road) == clean_inx_road
    assert x_roadbridge.reveal_inx(sweep_otx_road) == sweep_inx_road
    # THEN
    assert x_roadbridge.otx2inx_exists(otx_music45_str, inx_music87_str)
    assert x_roadbridge.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert x_roadbridge.otx2inx_exists(clean_otx_road, clean_inx_road)
    assert x_roadbridge.otx2inx_exists(sweep_otx_road, sweep_inx_road)
