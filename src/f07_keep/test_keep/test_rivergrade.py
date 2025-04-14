from src.f02_finance_toolboxs.deal import fisc_title_str
from src.f07_keep.examples.example_credorledgers import example_yao_hubunit
from src.f07_keep.rivercycle import RiverGrade, rivergrade_shop


def test_RiverGrade_Exists():
    # ESTABLISH / WHEN
    x_rivergrade = RiverGrade()

    # THEN
    #: Healer gut get_acct._debtit_belief (SELECT tax_due_amount FROM acct WHERE acct_name = bob_str)
    assert x_rivergrade.hubunit is None
    assert x_rivergrade.acct_name is None
    assert x_rivergrade.number is None
    #: Healer gut get_acct._debtit_belief (SELECT tax_due_amount FROM acct WHERE acct_name = bob_str)
    assert x_rivergrade.tax_bill_amount is None
    #: Healer gut get_acct._credit_belief (SELECT grant_amount FROM acct WHERE acct_name = bob_str)
    assert x_rivergrade.grant_amount is None
    #: SELECT COUNT(*) FROM acct WHERE tax_due_amount > (SELECT tax_due_amount FROM acct WHERE acct_name = bob_str)
    assert x_rivergrade.debtor_rank_num is None
    #: SELECT COUNT(*) FROM acct WHERE grant_amount > (SELECT tax_due_amount FROM acct WHERE acct_name = bob_str)
    assert x_rivergrade.credor_rank_num is None
    #: SELECT amount_paid FROM tax_ledger WHERE acct_name = bob_str
    assert x_rivergrade.tax_paid_amount is None
    #: bool (if tax_due_amount == tax_paid_amount)
    assert x_rivergrade.tax_paid_bool is None
    #: SELECT COUNT(*) FROM acct WHERE tax_paid_amount > (SELECT tax_paid_amount FROM acct WHERE acct_name = bob_str)
    assert x_rivergrade.tax_paid_rank_num is None
    #: tax_paid_rank_num / (SELECT COUNT(*) FROM acct WHERE tax_paid_amount>0)
    assert x_rivergrade.tax_paid_rank_percent is None
    #: SELECT COUNT(*) FROM acct WHERE tax_due_amount > 0
    assert x_rivergrade.debtor_count is None
    #: SELECT COUNT(*) FROM acct WHERE grant_amount > 0
    assert x_rivergrade.credor_count is None
    #: debtor_rank_num / SELECT COUNT(*) FROM acct WHERE tax_due_amount > 0
    assert x_rivergrade.debtor_rank_percent is None
    #: credor_rank_num / SELECT COUNT(*) FROM acct WHERE grant_amount > 0
    assert x_rivergrade.credor_rank_percent is None
    # SELECT COUNT(*) FROM rewards WHERE dst_acct_name = bob_str
    assert x_rivergrade.rewards_count is None
    # SELECT SUM(money_amount) FROM rewards WHERE dst_acct_name = bob_str
    assert x_rivergrade.rewards_magnitude is None


def test_rivergrade_shop_ReturnsObjWithArg():
    # ESTABLISH
    bob_str = "Bob"
    yao_hubunit = example_yao_hubunit()
    ten_int = 10
    x_debtor_count = 7
    x_credor_count = 9

    # WHEN
    x_rivergrade = rivergrade_shop(
        yao_hubunit, bob_str, ten_int, x_debtor_count, x_credor_count
    )

    # THEN
    assert x_rivergrade.hubunit == yao_hubunit
    assert x_rivergrade.acct_name == bob_str
    assert x_rivergrade.number == ten_int
    assert x_rivergrade.tax_bill_amount is None
    assert x_rivergrade.grant_amount is None
    assert x_rivergrade.debtor_rank_num is None
    assert x_rivergrade.credor_rank_num is None
    assert x_rivergrade.tax_paid_amount is None
    assert x_rivergrade.tax_paid_bool is None
    assert x_rivergrade.tax_paid_rank_num is None
    assert x_rivergrade.tax_paid_rank_percent is None
    assert x_rivergrade.debtor_count == x_debtor_count
    assert x_rivergrade.credor_count == x_credor_count
    assert x_rivergrade.debtor_rank_percent is None
    assert x_rivergrade.credor_rank_percent is None
    assert x_rivergrade.rewards_count is None
    assert x_rivergrade.rewards_magnitude is None


def test_rivergrade_shop_ReturnsObjWithoutArgs():
    # ESTABLISH
    bob_str = "Bob"
    yao_hubunit = example_yao_hubunit()

    # WHEN
    x_rivergrade = rivergrade_shop(yao_hubunit, bob_str)

    # THEN
    assert x_rivergrade.hubunit == yao_hubunit
    assert x_rivergrade.number == 0
    assert x_rivergrade.tax_bill_amount is None
    assert x_rivergrade.grant_amount is None
    assert x_rivergrade.debtor_rank_num is None
    assert x_rivergrade.credor_rank_num is None
    assert x_rivergrade.tax_paid_amount is None
    assert x_rivergrade.tax_paid_bool is None
    assert x_rivergrade.tax_paid_rank_num is None
    assert x_rivergrade.tax_paid_rank_percent is None
    assert x_rivergrade.debtor_count is None
    assert x_rivergrade.credor_count is None
    assert x_rivergrade.debtor_rank_percent is None
    assert x_rivergrade.credor_rank_percent is None
    assert x_rivergrade.rewards_count is None
    assert x_rivergrade.rewards_magnitude is None


def test_RiverGrade_set_tax_due_amount_SetsCorrectAttrs():
    # ESTABLISH
    x_rivergrade = RiverGrade()
    assert x_rivergrade.tax_bill_amount is None
    assert x_rivergrade.tax_paid_amount is None
    assert x_rivergrade.tax_paid_bool is None

    # WHEN
    x_tax_due_amount = 88
    x_rivergrade.set_tax_bill_amount(x_tax_due_amount)
    # THEN
    assert x_rivergrade.tax_bill_amount == x_tax_due_amount
    assert x_rivergrade.tax_paid_amount is None
    assert x_rivergrade.tax_paid_bool is False

    # WHEN
    x_tax_paid_amount = 77
    x_rivergrade.set_tax_paid_amount(x_tax_paid_amount)
    # THEN
    assert x_rivergrade.tax_bill_amount == x_tax_due_amount
    assert x_rivergrade.tax_paid_amount == x_tax_paid_amount
    assert x_rivergrade.tax_paid_bool is False

    # WHEN
    x_rivergrade.set_tax_paid_amount(x_tax_due_amount)
    # THEN
    assert x_rivergrade.tax_bill_amount == x_rivergrade.tax_paid_amount
    assert x_rivergrade.tax_paid_bool is True


def test_RiverGrade_get_dict_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_hubunit = example_yao_hubunit()
    ten_int = 10
    x_tax_bill_amount = 90
    x_grant_amount = 91
    x_debtor_rank_num = 92
    x_credor_rank_num = 93
    x_tax_paid_amount = 94
    x_tax_paid_bool = 95
    x_tax_paid_rank_num = 97
    x_tax_paid_rank_percent = 99
    x_debtor_count = 101
    x_credor_count = 103
    x_debtor_rank_percent = 105
    x_credor_rank_percent = 107
    x_rewards_count = 108
    x_rewards_magnitude = 109
    x_rivergrade = rivergrade_shop(
        yao_hubunit, bob_str, ten_int, x_debtor_count, x_credor_count
    )
    x_rivergrade.tax_bill_amount = x_tax_bill_amount
    x_rivergrade.grant_amount = x_grant_amount
    x_rivergrade.debtor_rank_num = x_debtor_rank_num
    x_rivergrade.credor_rank_num = x_credor_rank_num
    x_rivergrade.tax_paid_amount = x_tax_paid_amount
    x_rivergrade.tax_paid_bool = x_tax_paid_bool
    x_rivergrade.tax_paid_rank_num = x_tax_paid_rank_num
    x_rivergrade.tax_paid_rank_percent = x_tax_paid_rank_percent
    x_rivergrade.debtor_count = x_debtor_count
    x_rivergrade.credor_count = x_credor_count
    x_rivergrade.debtor_rank_percent = x_debtor_rank_percent
    x_rivergrade.credor_rank_percent = x_credor_rank_percent
    x_rivergrade.rewards_count = x_rewards_count
    x_rivergrade.rewards_magnitude = x_rewards_magnitude

    # WHEN
    rivergrade_dict = x_rivergrade.get_dict()

    # THEN
    assert rivergrade_dict.get(fisc_title_str()) == yao_hubunit.fisc_title
    assert rivergrade_dict.get("healer_name") == yao_hubunit.owner_name
    assert rivergrade_dict.get("keep_road") == yao_hubunit.keep_road
    assert rivergrade_dict.get("tax_bill_amount") == x_tax_bill_amount
    assert rivergrade_dict.get("grant_amount") == x_grant_amount
    assert rivergrade_dict.get("debtor_rank_num") == x_debtor_rank_num
    assert rivergrade_dict.get("credor_rank_num") == x_credor_rank_num
    assert rivergrade_dict.get("tax_paid_amount") == x_tax_paid_amount
    assert rivergrade_dict.get("tax_paid_bool") == x_tax_paid_bool
    assert rivergrade_dict.get("tax_paid_rank_num") == x_tax_paid_rank_num
    assert rivergrade_dict.get("tax_paid_rank_percent") == x_tax_paid_rank_percent
    assert rivergrade_dict.get("debtor_count") == x_debtor_count
    assert rivergrade_dict.get("credor_count") == x_credor_count
    assert rivergrade_dict.get("debtor_rank_percent") == x_debtor_rank_percent
    assert rivergrade_dict.get("credor_rank_percent") == x_credor_rank_percent
    assert rivergrade_dict.get("rewards_count") == x_rewards_count
    assert rivergrade_dict.get("rewards_magnitude") == x_rewards_magnitude


def test_RiverGrade_get_json_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_hubunit = example_yao_hubunit()
    ten_int = 10
    x_debtor_count = 101
    x_credor_count = 103
    x_rivergrade = rivergrade_shop(
        yao_hubunit, bob_str, ten_int, x_debtor_count, x_credor_count
    )

    # WHEN
    rivergrade_json = x_rivergrade.get_json()

    # THEN
    static_json = """{
  "credor_count": 103,
  "credor_rank_num": null,
  "credor_rank_percent": null,
  "debtor_count": 101,
  "debtor_rank_num": null,
  "debtor_rank_percent": null,
  "fisc_title": "ex_keep04",
  "grant_amount": null,
  "healer_name": "Yao",
  "keep_road": null,
  "rewards_count": null,
  "rewards_magnitude": null,
  "tax_bill_amount": null,
  "tax_paid_amount": null,
  "tax_paid_bool": null,
  "tax_paid_rank_num": null,
  "tax_paid_rank_percent": null
}"""

    assert rivergrade_json == static_json
