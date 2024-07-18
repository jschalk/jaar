from src._world.world import WorldUnit, worldunit_shop, ideaunit_shop, RealID
from src.money.examples.econ_env import temp_real_id


def get_1node_world() -> WorldUnit:
    x_world = worldunit_shop("A")
    x_world.set_real_id(temp_real_id())
    x_world.settle_world()
    return x_world


def get_Jnode2node_world() -> WorldUnit:
    x_world = worldunit_shop("J")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("A"))
    x_world.settle_world()
    return x_world


def get_2node_world(real_id: RealID = None) -> WorldUnit:
    if real_id is None:
        real_id = temp_real_id()
    a_text = "A"
    b_text = "B"
    x_world = worldunit_shop(_owner_id=a_text)
    x_world.set_real_id(real_id)
    idea_b = ideaunit_shop(b_text)
    x_world.add_idea(idea_b, parent_road=temp_real_id())
    x_world.settle_world()
    return x_world


def get_3node_world() -> WorldUnit:
    a_text = "A"
    x_world = worldunit_shop(a_text)
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("B"))
    x_world.add_l1_idea(ideaunit_shop("C"))
    x_world.settle_world()
    return x_world


def get_3node_D_E_F_world() -> WorldUnit:
    d_text = "D"
    x_world = worldunit_shop(d_text)
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("E"))
    x_world.add_l1_idea(ideaunit_shop("F"))
    x_world.settle_world()
    return x_world


def get_6node_world() -> WorldUnit:
    x_world = worldunit_shop("A")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("B"))
    x_world.add_l1_idea(ideaunit_shop("C"))
    c_road = x_world.make_l1_road("C")
    x_world.add_idea(ideaunit_shop("D"), c_road)
    x_world.add_idea(ideaunit_shop("E"), c_road)
    x_world.add_idea(ideaunit_shop("F"), c_road)
    x_world.settle_world()
    return x_world


def get_7nodeInsertH_world() -> WorldUnit:
    x_world = worldunit_shop("A")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("B"))
    x_world.add_l1_idea(ideaunit_shop("C"))
    c_road = x_world.make_l1_road("C")
    x_world.add_idea(ideaunit_shop("H"), c_road)
    x_world.add_idea(ideaunit_shop("D"), c_road)
    x_world.add_idea(ideaunit_shop("E"), c_road)
    x_world.add_idea(ideaunit_shop("F"), x_world.make_road(c_road, "H"))
    x_world.settle_world()
    return x_world


def get_5nodeHG_world() -> WorldUnit:
    x_world = worldunit_shop("A")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("B"))
    x_world.add_l1_idea(ideaunit_shop("C"))
    c_road = x_world.make_l1_road("C")
    x_world.add_idea(ideaunit_shop("H"), c_road)
    x_world.add_idea(ideaunit_shop("G"), c_road)
    x_world.settle_world()
    return x_world


def get_7nodeJRoot_world() -> WorldUnit:
    x_world = worldunit_shop("J")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("A"))

    a_road = x_world.make_l1_road("A")
    x_world.add_idea(ideaunit_shop("B"), a_road)
    x_world.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_world.make_l1_road("C")
    x_world.add_idea(ideaunit_shop("D"), c_road)
    x_world.add_idea(ideaunit_shop("E"), c_road)
    x_world.add_idea(ideaunit_shop("F"), c_road)
    x_world.settle_world()
    return x_world
