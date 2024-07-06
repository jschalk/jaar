from src._world.healer import healerhold_shop
from src._world.idea import ideaunit_shop
from src.listen.hubunit import hubunit_shop
from src.real.real import RealUnit, realunit_shop
from src.real.examples.real_env import get_test_reals_dir

# from src._world.graphic import display_ideatree


def create_example_real1() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    music_real.init_owner_econs(yao_text)
    yao_hubunit = hubunit_shop(None, music_text, yao_text, None)
    yao_think_world = yao_hubunit.get_think_world()

    yao_think_world.set_char_credor_pool(101)
    yao_think_world.set_char_debtor_pool(1000)

    yao_think_world.add_charunit(yao_text, 34, 600)
    yao_think_world.calc_world_metrics()
    texas_text = "Texas"
    texas_road = yao_think_world.make_l1_road(texas_text)
    yao_think_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = yao_think_world.make_road(texas_road, dallas_text)
    dallas_healerhold = healerhold_shop({yao_text})
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=dallas_healerhold)
    elpaso_text = "el paso"
    elpaso_road = yao_think_world.make_road(texas_road, elpaso_text)
    elpaso_healerhold = healerhold_shop({yao_text})
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=elpaso_healerhold)

    yao_think_world.add_idea(dallas_idea, texas_road)
    yao_think_world.add_idea(elpaso_idea, texas_road)
    # display_world(yao_think_world.calc_world_metrics(), mode="Econ").show()
    x_hubunit = hubunit_shop(
        reals_dir=yao_hubunit.reals_dir,
        real_id=yao_hubunit.real_id,
        owner_id=yao_hubunit.owner_id,
        econ_road=None,
        road_delimiter=yao_hubunit.road_delimiter,
        pixel=yao_hubunit.pixel,
    )
    x_hubunit.save_think_world(yao_think_world)
    yao_hubunit.create_think_treasury_db_files()

    # WHEN
    music_real._set_all_healer_dutys(yao_text)

    return music_real


def create_example_real2() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    music_real.init_owner_econs(yao_text)
    yao_hubunit = hubunit_shop(None, music_text, yao_text, None)
    wei_hubunit = hubunit_shop(None, music_text, wei_text, None)
    zia_hubunit = hubunit_shop(None, music_text, zia_text, None)
    music_real.init_owner_econs(wei_text)
    music_real.init_owner_econs(zia_text)
    yao_think_world = yao_hubunit.get_think_world()
    wei_think_world = wei_hubunit.get_think_world()
    zia_think_world = zia_hubunit.get_think_world()

    yao_think_world.set_char_credor_pool(101)
    wei_think_world.set_char_credor_pool(75)
    zia_think_world.set_char_credor_pool(52)
    yao_think_world.set_char_debtor_pool(1000)
    wei_think_world.set_char_debtor_pool(750)
    zia_think_world.set_char_debtor_pool(500)

    yao_think_world.add_charunit(yao_text, 34, 600)
    yao_think_world.add_charunit(zia_text, 57, 300)
    yao_think_world.add_charunit(wei_text, 10, 100)
    wei_think_world.add_charunit(yao_text, 37, 100)
    wei_think_world.add_charunit(wei_text, 11, 400)
    wei_think_world.add_charunit(zia_text, 27, 250)
    zia_think_world.add_charunit(yao_text, 14, 100)
    zia_think_world.add_charunit(zia_text, 38, 400)
    texas_text = "Texas"
    texas_road = yao_think_world.make_l1_road(texas_text)
    yao_think_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    wei_think_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    zia_think_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = yao_think_world.make_road(texas_road, dallas_text)
    dallas_healerhold = healerhold_shop({yao_text, zia_text})
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=dallas_healerhold)
    elpaso_text = "el paso"
    elpaso_road = yao_think_world.make_road(texas_road, elpaso_text)
    elpaso_healerhold = healerhold_shop({yao_text})
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=elpaso_healerhold)

    yao_think_world.add_idea(dallas_idea, texas_road)
    yao_think_world.add_idea(elpaso_idea, texas_road)
    wei_think_world.add_idea(dallas_idea, texas_road)
    wei_think_world.add_idea(elpaso_idea, texas_road)
    zia_think_world.add_idea(dallas_idea, texas_road)
    zia_think_world.add_idea(elpaso_idea, texas_road)
    # display_world(yao_think_world.calc_world_metrics(), mode="Econ").show()
    yao_hubunit.save_think_world(yao_think_world)
    wei_hubunit.save_think_world(wei_think_world)
    zia_hubunit.save_think_world(zia_think_world)
    yao_hubunit.create_think_treasury_db_files()
    wei_hubunit.create_think_treasury_db_files()
    zia_hubunit.create_think_treasury_db_files()
    music_real._set_all_healer_dutys(yao_text)
    music_real._set_all_healer_dutys(wei_text)
    music_real._set_all_healer_dutys(zia_text)

    return music_real


def create_example_real3() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    music_real.init_owner_econs(yao_text)
    music_real.init_owner_econs(wei_text)
    music_real.init_owner_econs(zia_text)
    yao_hubunit = hubunit_shop(None, music_text, yao_text, None)
    wei_hubunit = hubunit_shop(None, music_text, wei_text, None)
    zia_hubunit = hubunit_shop(None, music_text, zia_text, None)
    yao_think_world = yao_hubunit.get_think_world()
    wei_think_world = wei_hubunit.get_think_world()
    zia_think_world = zia_hubunit.get_think_world()

    casa_text = "casa"
    casa_road = yao_think_world.make_l1_road(casa_text)
    yao_think_world.add_l1_idea(ideaunit_shop(casa_text))
    wei_think_world.add_l1_idea(ideaunit_shop(casa_text))
    zia_think_world.add_l1_idea(ideaunit_shop(casa_text))
    clean_text = "clean"
    clean_road = yao_think_world.make_road(casa_road, clean_text)
    bath_text = "clean bathroom"
    hall_text = "clean hall"

    yao_think_world.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    yao_think_world.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)
    yao_think_world.add_idea(ideaunit_shop(hall_text, pledge=True), clean_road)
    # yao_think_world.calc_world_metrics()
    # display_ideatree(yao_think_world, mode="Econ").show()

    wei_think_world.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    wei_think_world.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)

    zia_think_world.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    zia_think_world.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)
    zia_think_world.add_idea(ideaunit_shop(hall_text, pledge=True), clean_road)

    # display_ideatree(yao_think_world, mode="Econ").show()
    yao_hubunit.save_think_world(yao_think_world)
    wei_hubunit.save_think_world(wei_think_world)
    zia_hubunit.save_think_world(zia_think_world)

    return music_real


def create_example_real4() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    music_real.init_owner_econs(yao_text)
    music_real.init_owner_econs(wei_text)
    music_real.init_owner_econs(zia_text)
    yao_hubunit = hubunit_shop(None, music_text, yao_text, None)
    wei_hubunit = hubunit_shop(None, music_text, wei_text, None)
    zia_hubunit = hubunit_shop(None, music_text, zia_text, None)
    yao_think_world = yao_hubunit.get_think_world()
    wei_think_world = wei_hubunit.get_think_world()
    zia_think_world = zia_hubunit.get_think_world()

    casa_text = "casa"
    casa_road = yao_think_world.make_l1_road(casa_text)
    yao_think_world.add_l1_idea(ideaunit_shop(casa_text))
    wei_think_world.add_l1_idea(ideaunit_shop(casa_text))
    zia_think_world.add_l1_idea(ideaunit_shop(casa_text))
    clean_text = "clean"
    clean_road = yao_think_world.make_road(casa_road, clean_text)
    bath_text = "clean bathroom"
    hall_text = "clean hall"

    yao_think_world.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    yao_think_world.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)
    yao_think_world.add_idea(ideaunit_shop(hall_text, pledge=True), clean_road)
    # yao_think_world.calc_world_metrics()
    # display_ideatree(yao_think_world, mode="Econ").show()

    wei_think_world.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    wei_think_world.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)

    zia_think_world.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    zia_think_world.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)
    zia_think_world.add_idea(ideaunit_shop(hall_text, pledge=True), clean_road)

    # display_ideatree(yao_think_world, mode="Econ").show()
    yao_think_world.set_char_credor_pool(101)
    wei_think_world.set_char_credor_pool(75)
    zia_think_world.set_char_credor_pool(52)
    yao_think_world.set_char_debtor_pool(1000)
    wei_think_world.set_char_debtor_pool(750)
    zia_think_world.set_char_debtor_pool(500)

    yao_think_world.add_charunit(yao_text, 34, 600)
    yao_think_world.add_charunit(zia_text, 57, 300)
    yao_think_world.add_charunit(wei_text, 10, 100)
    wei_think_world.add_charunit(yao_text, 37, 100)
    wei_think_world.add_charunit(wei_text, 11, 400)
    wei_think_world.add_charunit(zia_text, 27, 250)
    zia_think_world.add_charunit(yao_text, 14, 100)
    zia_think_world.add_charunit(zia_text, 38, 400)

    texas_text = "Texas"
    texas_road = yao_think_world.make_l1_road(texas_text)
    yao_think_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    wei_think_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    zia_think_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = yao_think_world.make_road(texas_road, dallas_text)
    dallas_healerhold = healerhold_shop({yao_text, zia_text})
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=dallas_healerhold)
    elpaso_text = "el paso"
    elpaso_road = yao_think_world.make_road(texas_road, elpaso_text)
    elpaso_healerhold = healerhold_shop({yao_text})
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=elpaso_healerhold)

    yao_think_world.add_idea(dallas_idea, texas_road)
    yao_think_world.add_idea(elpaso_idea, texas_road)
    wei_think_world.add_idea(dallas_idea, texas_road)
    wei_think_world.add_idea(elpaso_idea, texas_road)
    zia_think_world.add_idea(dallas_idea, texas_road)
    zia_think_world.add_idea(elpaso_idea, texas_road)
    # display_world(yao_think_world.calc_world_metrics(), mode="Econ").show()
    yao_hubunit.save_think_world(yao_think_world)
    wei_hubunit.save_think_world(wei_think_world)
    zia_hubunit.save_think_world(zia_think_world)

    return music_real
