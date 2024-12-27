from src.f02_bud.healer import healerlink_shop
from src.f02_bud.item import itemunit_shop
from src.f05_listen.hubunit import hubunit_shop
from src.f07_deal.deal import dealUnit, dealunit_shop
from src.f07_deal.examples.deal_env import get_test_deals_dir


# def create_example_deal1(graphics_bool) -> dealUnit:
#     # ESTABLISH
#     music_str = "music"
#     music_deal = dealunit_shop(music_str, get_test_deals_dir(), in_memory_journal=True)
#     yao_str = "Yao"
#     music_deal.init_owner_keeps(yao_str)
#     yao_hubunit = hubunit_shop(None, music_str, yao_str, None)
#     yao_voice_bud = yao_hubunit.get_voice_bud()

#     yao_voice_bud.set_credor_respect(101)
#     yao_voice_bud.set_debtor_respect(1000)

#     yao_voice_bud.add_acctunit(yao_str, 34, 600)
#     yao_voice_bud.settle_bud()
#     texas_str = "Texas"
#     texas_road = yao_voice_bud.make_l1_road(texas_str)
#     yao_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
#     dallas_str = "dallas"
#     dallas_road = yao_voice_bud.make_road(texas_road, dallas_str)
#     dallas_healerlink = healerlink_shop({yao_str})
#     dallas_item = itemunit_shop(dallas_str, healerlink=dallas_healerlink)
#     elpaso_str = "el paso"
#     elpaso_road = yao_voice_bud.make_road(texas_road, elpaso_str)
#     elpaso_healerlink = healerlink_shop({yao_str})
#     elpaso_item = itemunit_shop(elpaso_str, healerlink=elpaso_healerlink)

#     yao_voice_bud.set_item(dallas_item, texas_road)
#     yao_voice_bud.set_item(elpaso_item, texas_road)
#     display_itemtree(yao_voice_bud.settle_bud(), mode="Keep", graphics_bool=graphics_bool)
#     x_hubunit = hubunit_shop(
#         deals_dir=yao_hubunit.deals_dir,
#         deal_id=yao_hubunit.deal_id,
#         owner_id=yao_hubunit.owner_id,
#         keep_road=None,
#         wall=yao_hubunit.wall,
#         respect_bit=yao_hubunit.respect_bit,
#     )
#     x_hubunit.save_voice_bud(yao_voice_bud)
#     yao_hubunit.create_voice_treasury_db_files()

#     # WHEN
#     music_deal._set_all_healer_dutys(yao_str)

#     return music_deal


def create_example_deal2() -> dealUnit:
    # ESTABLISH
    music_str = "music"
    music_deal = dealunit_shop(music_str, get_test_deals_dir(), in_memory_journal=True)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    music_deal.init_owner_keeps(yao_str)
    yao_hubunit = hubunit_shop(None, music_str, yao_str, None)
    wei_hubunit = hubunit_shop(None, music_str, wei_str, None)
    zia_hubunit = hubunit_shop(None, music_str, zia_str, None)
    music_deal.init_owner_keeps(wei_str)
    music_deal.init_owner_keeps(zia_str)
    yao_voice_bud = yao_hubunit.get_voice_bud()
    wei_voice_bud = wei_hubunit.get_voice_bud()
    zia_voice_bud = zia_hubunit.get_voice_bud()

    yao_voice_bud.set_credor_respect(101)
    wei_voice_bud.set_credor_respect(75)
    zia_voice_bud.set_credor_respect(52)
    yao_voice_bud.set_debtor_respect(1000)
    wei_voice_bud.set_debtor_respect(750)
    zia_voice_bud.set_debtor_respect(500)

    yao_voice_bud.add_acctunit(yao_str, 34, 600)
    yao_voice_bud.add_acctunit(zia_str, 57, 300)
    yao_voice_bud.add_acctunit(wei_str, 10, 100)
    wei_voice_bud.add_acctunit(yao_str, 37, 100)
    wei_voice_bud.add_acctunit(wei_str, 11, 400)
    wei_voice_bud.add_acctunit(zia_str, 27, 250)
    zia_voice_bud.add_acctunit(yao_str, 14, 100)
    zia_voice_bud.add_acctunit(zia_str, 38, 400)
    texas_str = "Texas"
    texas_road = yao_voice_bud.make_l1_road(texas_str)
    yao_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    wei_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    zia_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_road = yao_voice_bud.make_road(texas_road, dallas_str)
    dallas_healerlink = healerlink_shop({yao_str, zia_str})
    dallas_item = itemunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_road = yao_voice_bud.make_road(texas_road, elpaso_str)
    elpaso_healerlink = healerlink_shop({yao_str})
    elpaso_item = itemunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    yao_voice_bud.set_item(dallas_item, texas_road)
    yao_voice_bud.set_item(elpaso_item, texas_road)
    wei_voice_bud.set_item(dallas_item, texas_road)
    wei_voice_bud.set_item(elpaso_item, texas_road)
    zia_voice_bud.set_item(dallas_item, texas_road)
    zia_voice_bud.set_item(elpaso_item, texas_road)
    yao_hubunit.save_voice_bud(yao_voice_bud)
    wei_hubunit.save_voice_bud(wei_voice_bud)
    zia_hubunit.save_voice_bud(zia_voice_bud)
    yao_hubunit.create_voice_treasury_db_files()
    wei_hubunit.create_voice_treasury_db_files()
    zia_hubunit.create_voice_treasury_db_files()
    music_deal._set_all_healer_dutys(yao_str)
    music_deal._set_all_healer_dutys(wei_str)
    music_deal._set_all_healer_dutys(zia_str)

    return music_deal


def create_example_deal3() -> dealUnit:
    # ESTABLISH
    music_str = "music"
    music_deal = dealunit_shop(music_str, get_test_deals_dir(), in_memory_journal=True)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    music_deal.init_owner_keeps(yao_str)
    music_deal.init_owner_keeps(wei_str)
    music_deal.init_owner_keeps(zia_str)
    yao_hubunit = hubunit_shop(None, music_str, yao_str, None)
    wei_hubunit = hubunit_shop(None, music_str, wei_str, None)
    zia_hubunit = hubunit_shop(None, music_str, zia_str, None)
    yao_voice_bud = yao_hubunit.get_voice_bud()
    wei_voice_bud = wei_hubunit.get_voice_bud()
    zia_voice_bud = zia_hubunit.get_voice_bud()

    casa_str = "casa"
    casa_road = yao_voice_bud.make_l1_road(casa_str)
    yao_voice_bud.set_l1_item(itemunit_shop(casa_str))
    wei_voice_bud.set_l1_item(itemunit_shop(casa_str))
    zia_voice_bud.set_l1_item(itemunit_shop(casa_str))
    clean_str = "clean"
    clean_road = yao_voice_bud.make_road(casa_road, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_voice_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    yao_voice_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)
    yao_voice_bud.set_item(itemunit_shop(hall_str, pledge=True), clean_road)

    wei_voice_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    wei_voice_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)

    zia_voice_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    zia_voice_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)
    zia_voice_bud.set_item(itemunit_shop(hall_str, pledge=True), clean_road)

    yao_hubunit.save_voice_bud(yao_voice_bud)
    wei_hubunit.save_voice_bud(wei_voice_bud)
    zia_hubunit.save_voice_bud(zia_voice_bud)

    return music_deal


def create_example_deal4() -> dealUnit:
    # ESTABLISH
    music_str = "music"
    music_deal = dealunit_shop(music_str, get_test_deals_dir(), in_memory_journal=True)
    yao_str = "Yao"
    wei_str = "Wei"
    zia_str = "Zia"
    music_deal.init_owner_keeps(yao_str)
    music_deal.init_owner_keeps(wei_str)
    music_deal.init_owner_keeps(zia_str)
    yao_hubunit = hubunit_shop(None, music_str, yao_str, None)
    wei_hubunit = hubunit_shop(None, music_str, wei_str, None)
    zia_hubunit = hubunit_shop(None, music_str, zia_str, None)
    yao_voice_bud = yao_hubunit.get_voice_bud()
    wei_voice_bud = wei_hubunit.get_voice_bud()
    zia_voice_bud = zia_hubunit.get_voice_bud()

    casa_str = "casa"
    casa_road = yao_voice_bud.make_l1_road(casa_str)
    yao_voice_bud.set_l1_item(itemunit_shop(casa_str))
    wei_voice_bud.set_l1_item(itemunit_shop(casa_str))
    zia_voice_bud.set_l1_item(itemunit_shop(casa_str))
    clean_str = "clean"
    clean_road = yao_voice_bud.make_road(casa_road, clean_str)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_voice_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    yao_voice_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)
    yao_voice_bud.set_item(itemunit_shop(hall_str, pledge=True), clean_road)

    wei_voice_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    wei_voice_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)

    zia_voice_bud.set_item(itemunit_shop(clean_str, pledge=True), casa_road)
    zia_voice_bud.set_item(itemunit_shop(bath_str, pledge=True), clean_road)
    zia_voice_bud.set_item(itemunit_shop(hall_str, pledge=True), clean_road)

    yao_voice_bud.set_credor_respect(101)
    wei_voice_bud.set_credor_respect(75)
    zia_voice_bud.set_credor_respect(52)
    yao_voice_bud.set_debtor_respect(1000)
    wei_voice_bud.set_debtor_respect(750)
    zia_voice_bud.set_debtor_respect(500)

    yao_voice_bud.add_acctunit(yao_str, 34, 600)
    yao_voice_bud.add_acctunit(zia_str, 57, 300)
    yao_voice_bud.add_acctunit(wei_str, 10, 100)
    wei_voice_bud.add_acctunit(yao_str, 37, 100)
    wei_voice_bud.add_acctunit(wei_str, 11, 400)
    wei_voice_bud.add_acctunit(zia_str, 27, 250)
    zia_voice_bud.add_acctunit(yao_str, 14, 100)
    zia_voice_bud.add_acctunit(zia_str, 38, 400)

    texas_str = "Texas"
    texas_road = yao_voice_bud.make_l1_road(texas_str)
    yao_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    wei_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    zia_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_road = yao_voice_bud.make_road(texas_road, dallas_str)
    dallas_healerlink = healerlink_shop({yao_str, zia_str})
    dallas_item = itemunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_road = yao_voice_bud.make_road(texas_road, elpaso_str)
    elpaso_healerlink = healerlink_shop({yao_str})
    elpaso_item = itemunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    yao_voice_bud.set_item(dallas_item, texas_road)
    yao_voice_bud.set_item(elpaso_item, texas_road)
    wei_voice_bud.set_item(dallas_item, texas_road)
    wei_voice_bud.set_item(elpaso_item, texas_road)
    zia_voice_bud.set_item(dallas_item, texas_road)
    zia_voice_bud.set_item(elpaso_item, texas_road)

    yao_hubunit.save_voice_bud(yao_voice_bud)
    wei_hubunit.save_voice_bud(wei_voice_bud)
    zia_hubunit.save_voice_bud(zia_voice_bud)

    return music_deal
