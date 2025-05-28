from src.a02_finance_logic.deal import dealunit_shop, DealUnit


def get_dealunit_55_example() -> DealUnit:
    x_deal_time = 55
    return dealunit_shop(x_deal_time)


def get_dealunit_66_example() -> DealUnit:
    t66_deal_time = 66
    t66_dealunit = dealunit_shop(t66_deal_time)
    t66_dealunit.set_deal_acct_net("Sue", -5)
    t66_dealunit.set_deal_acct_net("Bob", 5)
    return t66_dealunit


def get_dealunit_88_example() -> DealUnit:
    t88_deal_time = 88
    t88_dealunit = dealunit_shop(t88_deal_time)
    t88_dealunit.quota = 800
    return t88_dealunit


def get_dealunit_invalid_example() -> DealUnit:
    t55_deal_time = 55
    t55_dealunit = dealunit_shop(t55_deal_time)
    t55_dealunit.set_deal_acct_net("Sue", -5)
    t55_dealunit.set_deal_acct_net("Bob", 3)
    return t55_dealunit
