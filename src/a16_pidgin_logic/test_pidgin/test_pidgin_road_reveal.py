from src.a01_word_logic.road import create_road
from src.a16_pidgin_logic.map import roadmap_shop


def test_RoadMap_reveal_inx_ReturnsObjAndSetsAttr_road_Scenario0():
    # ESTABLISH
    otx_accord45_str = "accord45"
    otx_r_bridge = "/"
    inx_r_bridge = ":"
    road_roadmap = roadmap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    assert road_roadmap.otx_exists(otx_accord45_str) is False
    assert road_roadmap.otx2inx_exists(otx_accord45_str, otx_accord45_str) is False

    # WHEN
    gen_inx_road = road_roadmap.reveal_inx(otx_accord45_str)

    # THEN
    assert gen_inx_road == otx_accord45_str
    assert road_roadmap.otx_exists(otx_accord45_str)
    assert road_roadmap.otx2inx_exists(otx_accord45_str, otx_accord45_str)


def test_RoadMap_reveal_inx_ReturnsObjAndSetsAttr_road_Scenario1():
    # ESTABLISH
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    otx_r_bridge = "/"
    inx_r_bridge = ":"
    clean_otx_str = "clean"
    clean_otx_road = f"{otx_accord45_str}{otx_r_bridge}{clean_otx_str}"
    road_roadmap = roadmap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    assert road_roadmap.otx_exists(otx_accord45_str) is False
    assert road_roadmap.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_roadmap.reveal_inx(clean_otx_road)

    # THEN
    assert gen_inx_road is None
    assert road_roadmap.otx_exists(otx_accord45_str) is False
    assert road_roadmap.otx_exists(clean_otx_road) is False
    assert road_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str) is False

    # ESTABLISH
    road_roadmap.set_otx2inx(otx_accord45_str, inx_accord87_str)
    assert road_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert road_roadmap.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_roadmap.reveal_inx(clean_otx_road)

    # THEN
    assert road_roadmap.otx_exists(clean_otx_road)
    assert road_roadmap.otx2inx_exists(clean_otx_road, gen_inx_road)
    assert gen_inx_road == f"{inx_accord87_str}{inx_r_bridge}{clean_otx_str}"


def test_RoadMap_reveal_inx_ReturnsObjAndSetsAttr_road_Scenario2_With_tag():
    # ESTABLISH
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    otx_r_bridge = "/"
    inx_r_bridge = ":"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    clean_otx_road = f"{otx_accord45_str}{otx_r_bridge}{clean_otx_str}"
    road_roadmap = roadmap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    road_roadmap.set_tag(clean_otx_str, clean_inx_str)
    assert road_roadmap.otx_exists(otx_accord45_str) is False
    assert road_roadmap.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_roadmap.reveal_inx(clean_otx_road)

    # THEN
    assert gen_inx_road is None
    assert road_roadmap.otx_exists(otx_accord45_str) is False
    assert road_roadmap.otx_exists(clean_otx_road) is False
    assert road_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str) is False

    # ESTABLISH
    road_roadmap.set_otx2inx(otx_accord45_str, inx_accord87_str)
    assert road_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert road_roadmap.otx_exists(clean_otx_road) is False

    # WHEN
    gen_inx_road = road_roadmap.reveal_inx(clean_otx_road)

    # THEN
    assert road_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert road_roadmap.otx_exists(clean_otx_road)
    assert road_roadmap.otx2inx_exists(clean_otx_road, gen_inx_road)
    assert gen_inx_road == f"{inx_accord87_str}{inx_r_bridge}{clean_inx_str}"


def test_RoadMap_reveal_inx_AddsMissingObjsTo_otx2inx_RoadUnit():
    # ESTABLISH
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_accord45_str, casa_otx_str)
    casa_inx_road = create_road(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)
    x_roadmap = roadmap_shop()
    x_roadmap.set_tag(otx_accord45_str, inx_accord87_str)
    x_roadmap.set_tag(casa_otx_str, casa_inx_str)
    x_roadmap.set_tag(clean_otx_str, clean_inx_str)
    print(f"{x_roadmap.tagmap.otx2inx=}")
    print(f"{x_roadmap.otx2inx=}")
    assert x_roadmap.otx_exists(otx_accord45_str) is False
    assert x_roadmap.otx_exists(casa_otx_road) is False
    assert x_roadmap.otx_exists(clean_otx_road) is False
    assert x_roadmap.otx_exists(sweep_otx_road) is False
    assert x_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str) is False
    assert x_roadmap.otx2inx_exists(casa_otx_road, casa_inx_road) is False
    assert x_roadmap.otx2inx_exists(clean_otx_road, clean_inx_road) is False
    assert x_roadmap.otx2inx_exists(sweep_otx_road, sweep_inx_road) is False

    # WHEN
    assert x_roadmap.reveal_inx(otx_accord45_str) == inx_accord87_str
    print(f"{x_roadmap.tagmap.otx2inx=}")
    print(f"{x_roadmap.otx2inx=}")
    # THEN
    assert x_roadmap.otx_exists(otx_accord45_str)
    assert x_roadmap.otx_exists(casa_otx_road) is False
    assert x_roadmap.otx_exists(clean_otx_road) is False
    assert x_roadmap.otx_exists(sweep_otx_road) is False
    assert x_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert x_roadmap.otx2inx_exists(casa_otx_road, casa_inx_road) is False
    assert x_roadmap.otx2inx_exists(clean_otx_road, clean_inx_road) is False
    assert x_roadmap.otx2inx_exists(sweep_otx_road, sweep_inx_road) is False

    # WHEN
    assert x_roadmap.reveal_inx(casa_otx_road) == casa_inx_road
    # THEN
    assert x_roadmap.otx_exists(otx_accord45_str)
    assert x_roadmap.otx_exists(casa_otx_road)
    assert x_roadmap.otx_exists(clean_otx_road) is False
    assert x_roadmap.otx_exists(sweep_otx_road) is False
    assert x_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert x_roadmap.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert x_roadmap.otx2inx_exists(clean_otx_road, clean_inx_road) is False
    assert x_roadmap.otx2inx_exists(sweep_otx_road, sweep_inx_road) is False

    # WHEN
    assert x_roadmap.reveal_inx(clean_otx_road) == clean_inx_road
    assert x_roadmap.reveal_inx(sweep_otx_road) == sweep_inx_road
    # THEN
    assert x_roadmap.otx2inx_exists(otx_accord45_str, inx_accord87_str)
    assert x_roadmap.otx2inx_exists(casa_otx_road, casa_inx_road)
    assert x_roadmap.otx2inx_exists(clean_otx_road, clean_inx_road)
    assert x_roadmap.otx2inx_exists(sweep_otx_road, sweep_inx_road)
