from src.f01_road.deal import dealunit_shop, DealUnit


def get_dealunit_55_example() -> DealUnit:
    x_time_int = 55
    return dealunit_shop(x_time_int)


def get_dealunit_66_example() -> DealUnit:
    t66_time_int = 66
    t66_dealunit = dealunit_shop(t66_time_int)
    t66_dealunit.set_deal_net("Sue", -5)
    t66_dealunit.set_deal_net("Bob", 5)
    return t66_dealunit


def get_dealunit_88_example() -> DealUnit:
    t88_time_int = 88
    t88_dealunit = dealunit_shop(t88_time_int)
    t88_dealunit.quota = 800
    return t88_dealunit


def get_dealunit_invalid_example() -> DealUnit:
    t55_time_int = 55
    t55_dealunit = dealunit_shop(t55_time_int)
    t55_dealunit.set_deal_net("Sue", -5)
    t55_dealunit.set_deal_net("Bob", 3)
    return t55_dealunit
