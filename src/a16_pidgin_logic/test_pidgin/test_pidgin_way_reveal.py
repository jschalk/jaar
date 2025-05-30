from src.a01_term_logic.way import create_way, to_way
from src.a16_pidgin_logic.map import waymap_shop


def test_WayMap_reveal_inx_ReturnsObjAndSetsAttr_way_Scenario0():
    # ESTABLISH
    a45_str = "accord45"
    otx_r_bridge = "/"
    otx_accord45_way = to_way(a45_str, otx_r_bridge)
    inx_r_bridge = ":"
    way_waymap = waymap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    assert way_waymap.otx_exists(otx_accord45_way) is False
    assert way_waymap.otx2inx_exists(otx_accord45_way, otx_accord45_way) is False

    # WHEN
    gen_inx_way = way_waymap.reveal_inx(otx_accord45_way)

    # THEN
    assert gen_inx_way[1:-1] == otx_accord45_way[1:-1]
    assert way_waymap.otx_exists(otx_accord45_way)
    inx_accord45_way = to_way(a45_str, inx_r_bridge)
    assert way_waymap.otx2inx_exists(otx_accord45_way, inx_accord45_way)


def test_WayMap_reveal_inx_ReturnsObjAndSetsAttr_way_Scenario1():
    # ESTABLISH
    otx_r_bridge = "/"
    inx_r_bridge = ":"
    otx_accord45_way = to_way("accord45", otx_r_bridge)
    inx_accord87_way = to_way("accord87", inx_r_bridge)
    clean_otx_str = "clean"
    clean_otx_way = f"{otx_accord45_way}{clean_otx_str}{otx_r_bridge}"
    way_waymap = waymap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    assert way_waymap.otx_exists(otx_accord45_way) is False
    assert way_waymap.otx_exists(clean_otx_way) is False

    # WHEN
    gen_inx_way = way_waymap.reveal_inx(clean_otx_way)

    # THEN
    assert gen_inx_way is None
    assert way_waymap.otx_exists(otx_accord45_way) is False
    assert way_waymap.otx_exists(clean_otx_way) is False
    assert way_waymap.otx2inx_exists(otx_accord45_way, inx_accord87_way) is False

    # ESTABLISH
    way_waymap.set_otx2inx(otx_accord45_way, inx_accord87_way)
    assert way_waymap.otx2inx_exists(otx_accord45_way, inx_accord87_way)
    assert way_waymap.otx_exists(clean_otx_way) is False

    # WHEN
    gen_inx_way = way_waymap.reveal_inx(clean_otx_way)

    # THEN
    assert way_waymap.otx_exists(clean_otx_way)
    assert way_waymap.otx2inx_exists(clean_otx_way, gen_inx_way)
    assert gen_inx_way == f"{inx_accord87_way}{clean_otx_str}{inx_r_bridge}"


def test_WayMap_reveal_inx_ReturnsObjAndSetsAttr_way_Scenario2_With_label():
    # ESTABLISH
    otx_r_bridge = "/"
    inx_r_bridge = ":"
    otx_accord45_way = to_way("accord45", otx_r_bridge)
    inx_accord87_way = to_way("accord87", inx_r_bridge)
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    clean_otx_way = f"{otx_accord45_way}{clean_otx_str}{otx_r_bridge}"
    way_waymap = waymap_shop(otx_bridge=otx_r_bridge, inx_bridge=inx_r_bridge)
    way_waymap.set_label(clean_otx_str, clean_inx_str)
    assert way_waymap.otx_exists(otx_accord45_way) is False
    assert way_waymap.otx_exists(clean_otx_way) is False

    # WHEN
    gen_inx_way = way_waymap.reveal_inx(clean_otx_way)

    # THEN
    assert gen_inx_way is None
    assert way_waymap.otx_exists(otx_accord45_way) is False
    assert way_waymap.otx_exists(clean_otx_way) is False
    assert way_waymap.otx2inx_exists(otx_accord45_way, inx_accord87_way) is False

    # ESTABLISH
    way_waymap.set_otx2inx(otx_accord45_way, inx_accord87_way)
    assert way_waymap.otx2inx_exists(otx_accord45_way, inx_accord87_way)
    assert way_waymap.otx_exists(clean_otx_way) is False

    # WHEN
    gen_inx_way = way_waymap.reveal_inx(clean_otx_way)

    # THEN
    assert way_waymap.otx2inx_exists(otx_accord45_way, inx_accord87_way)
    assert way_waymap.otx_exists(clean_otx_way)
    assert way_waymap.otx2inx_exists(clean_otx_way, gen_inx_way)
    assert gen_inx_way == f"{inx_accord87_way}{clean_inx_str}{inx_r_bridge}"


def test_WayMap_reveal_inx_AddsMissingObjsTo_otx2inx_WayTerm():
    # ESTABLISH
    otx_a45_str = "accord45"
    inx_a87_str = "accord87"
    otx_accord45_way = to_way(otx_a45_str)
    inx_accord87_way = to_way(inx_a87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_way = create_way(otx_accord45_way, casa_otx_str)
    casa_inx_way = create_way(inx_accord87_way, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_way = create_way(casa_otx_way, clean_otx_str)
    clean_inx_way = create_way(casa_inx_way, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_way = create_way(clean_otx_way, sweep_str)
    sweep_inx_way = create_way(clean_inx_way, sweep_str)
    x_waymap = waymap_shop()
    x_waymap.set_label(otx_a45_str, inx_a87_str)
    x_waymap.set_label(casa_otx_str, casa_inx_str)
    x_waymap.set_label(clean_otx_str, clean_inx_str)
    print(f"{x_waymap.labelmap.otx2inx=}")
    print(f"{x_waymap.otx2inx=}")
    assert x_waymap.otx_exists(otx_accord45_way) is False
    assert x_waymap.otx_exists(casa_otx_way) is False
    assert x_waymap.otx_exists(clean_otx_way) is False
    assert x_waymap.otx_exists(sweep_otx_way) is False
    assert x_waymap.otx2inx_exists(otx_accord45_way, inx_accord87_way) is False
    assert x_waymap.otx2inx_exists(casa_otx_way, casa_inx_way) is False
    assert x_waymap.otx2inx_exists(clean_otx_way, clean_inx_way) is False
    assert x_waymap.otx2inx_exists(sweep_otx_way, sweep_inx_way) is False

    # WHEN
    assert x_waymap.reveal_inx(otx_accord45_way) == inx_accord87_way
    print(f"{x_waymap.labelmap.otx2inx=}")
    print(f"{x_waymap.otx2inx=}")
    # THEN
    assert x_waymap.otx_exists(otx_accord45_way)
    assert x_waymap.otx_exists(casa_otx_way) is False
    assert x_waymap.otx_exists(clean_otx_way) is False
    assert x_waymap.otx_exists(sweep_otx_way) is False
    assert x_waymap.otx2inx_exists(otx_accord45_way, inx_accord87_way)
    assert x_waymap.otx2inx_exists(casa_otx_way, casa_inx_way) is False
    assert x_waymap.otx2inx_exists(clean_otx_way, clean_inx_way) is False
    assert x_waymap.otx2inx_exists(sweep_otx_way, sweep_inx_way) is False

    # WHEN
    assert x_waymap.reveal_inx(casa_otx_way) == casa_inx_way
    # THEN
    assert x_waymap.otx_exists(otx_accord45_way)
    assert x_waymap.otx_exists(casa_otx_way)
    assert x_waymap.otx_exists(clean_otx_way) is False
    assert x_waymap.otx_exists(sweep_otx_way) is False
    assert x_waymap.otx2inx_exists(otx_accord45_way, inx_accord87_way)
    assert x_waymap.otx2inx_exists(casa_otx_way, casa_inx_way)
    assert x_waymap.otx2inx_exists(clean_otx_way, clean_inx_way) is False
    assert x_waymap.otx2inx_exists(sweep_otx_way, sweep_inx_way) is False

    # WHEN
    assert x_waymap.reveal_inx(clean_otx_way) == clean_inx_way
    assert x_waymap.reveal_inx(sweep_otx_way) == sweep_inx_way
    # THEN
    assert x_waymap.otx2inx_exists(otx_accord45_way, inx_accord87_way)
    assert x_waymap.otx2inx_exists(casa_otx_way, casa_inx_way)
    assert x_waymap.otx2inx_exists(clean_otx_way, clean_inx_way)
    assert x_waymap.otx2inx_exists(sweep_otx_way, sweep_inx_way)
