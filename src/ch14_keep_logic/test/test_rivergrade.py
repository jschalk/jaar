from src.ch14_keep_logic.rivercycle import RiverGrade, rivergrade_shop
from src.ch14_keep_logic.test._util.ch14_examples import temp_moment_label
from src.ref.ch14_keywords import Ch14Keywords as wx


def test_RiverGrade_Exists():
    # ESTABLISH / WHEN
    x_rivergrade = RiverGrade()

    # THEN
    #: Healer gut get_voice._voice_debt_lumen (SELECT tax_due_amount FROM voice WHERE voice_name = bob_str)
    assert not x_rivergrade.moment_label
    assert not x_rivergrade.belief_name
    assert not x_rivergrade.keep_rope
    assert not x_rivergrade.voice_name
    assert not x_rivergrade.number
    #: Healer gut get_voice._voice_debt_lumen (SELECT tax_due_amount FROM voice WHERE voice_name = bob_str)
    assert x_rivergrade.tax_bill_amount is None
    #: Healer gut get_voice._voice_cred_lumen (SELECT grant_amount FROM voice WHERE voice_name = bob_str)
    assert x_rivergrade.grant_amount is None
    #: SELECT COUNT(*) FROM voice WHERE tax_due_amount > (SELECT tax_due_amount FROM voice WHERE voice_name = bob_str)
    assert x_rivergrade.debtor_rank_num is None
    #: SELECT COUNT(*) FROM voice WHERE grant_amount > (SELECT tax_due_amount FROM voice WHERE voice_name = bob_str)
    assert x_rivergrade.credor_rank_num is None
    #: SELECT amount_paid FROM tax_ledger WHERE voice_name = bob_str
    assert x_rivergrade.tax_paid_amount is None
    #: bool (if tax_due_amount == tax_paid_amount)
    assert x_rivergrade.tax_paid_bool is None
    #: SELECT COUNT(*) FROM voice WHERE tax_paid_amount > (SELECT tax_paid_amount FROM voice WHERE voice_name = bob_str)
    assert x_rivergrade.tax_paid_rank_num is None
    #: tax_paid_rank_num / (SELECT COUNT(*) FROM voice WHERE tax_paid_amount>0)
    assert x_rivergrade.tax_paid_rank_percent is None
    #: SELECT COUNT(*) FROM voice WHERE tax_due_amount > 0
    assert x_rivergrade.debtor_count is None
    #: SELECT COUNT(*) FROM voice WHERE grant_amount > 0
    assert x_rivergrade.credor_count is None
    #: debtor_rank_num / SELECT COUNT(*) FROM voice WHERE tax_due_amount > 0
    assert x_rivergrade.debtor_rank_percent is None
    #: credor_rank_num / SELECT COUNT(*) FROM voice WHERE grant_amount > 0
    assert x_rivergrade.credor_rank_percent is None
    # SELECT COUNT(*) FROM rewards WHERE dst_voice_name = bob_str
    assert x_rivergrade.rewards_count is None
    # SELECT SUM(money_amount) FROM rewards WHERE dst_voice_name = bob_str
    assert x_rivergrade.rewards_magnitude is None
    assert set(x_rivergrade.__dict__.keys()) == {
        "moment_label",
        "belief_name",
        "keep_rope",
        "voice_name",
        "number",
        "tax_bill_amount",
        "grant_amount",
        "debtor_rank_num",
        "credor_rank_num",
        "tax_paid_amount",
        "tax_paid_bool",
        "tax_paid_rank_num",
        "tax_paid_rank_percent",
        "debtor_count",
        "credor_count",
        "debtor_rank_percent",
        "credor_rank_percent",
        "rewards_count",
        "rewards_magnitude",
    }
    # TODO replace above assert with below
    # assert set(x_rivergrade.__dict__.keys()) == {
    #     wx.moment_label,
    #     wx.belief_name,
    #     wx.keep_rope,
    #     wx.voice_name,
    #     wx.number,
    #     wx.tax_bill_amount,
    #     wx.grant_amount,
    #     wx.debtor_rank_num,
    #     wx.credor_rank_num,
    #     wx.tax_paid_amount,
    #     wx.tax_paid_bool,
    #     wx.tax_paid_rank_num,
    #     wx.tax_paid_rank_percent,
    #     wx.debtor_count,
    #     wx.credor_count,
    #     wx.debtor_rank_percent,
    #     wx.credor_rank_percent,
    #     wx.rewards_count,
    #     wx.rewards_magnitude,
    # }


def test_rivergrade_shop_ReturnsObjWithArg():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = temp_moment_label()
    x_keep_rope = None
    ten_int = 10
    x_debtor_count = 7
    x_credor_count = 9

    # WHEN
    x_rivergrade = rivergrade_shop(
        a23_str, yao_str, x_keep_rope, bob_str, ten_int, x_debtor_count, x_credor_count
    )

    # THEN
    assert x_rivergrade.moment_label == a23_str
    assert x_rivergrade.belief_name == yao_str
    assert x_rivergrade.keep_rope == x_keep_rope
    assert x_rivergrade.voice_name == bob_str
    assert x_rivergrade.number == ten_int
    assert not x_rivergrade.tax_bill_amount
    assert not x_rivergrade.grant_amount
    assert not x_rivergrade.debtor_rank_num
    assert not x_rivergrade.credor_rank_num
    assert not x_rivergrade.tax_paid_amount
    assert not x_rivergrade.tax_paid_bool
    assert not x_rivergrade.tax_paid_rank_num
    assert not x_rivergrade.tax_paid_rank_percent
    assert x_rivergrade.debtor_count == x_debtor_count
    assert x_rivergrade.credor_count == x_credor_count
    assert not x_rivergrade.debtor_rank_percent
    assert not x_rivergrade.credor_rank_percent
    assert not x_rivergrade.rewards_count
    assert not x_rivergrade.rewards_magnitude


def test_rivergrade_shop_ReturnsObjWithoutArgs():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = temp_moment_label()
    x_keep_rope = None

    # WHEN
    x_rivergrade = rivergrade_shop(a23_str, yao_str, x_keep_rope, bob_str)

    # THEN
    assert x_rivergrade.moment_label == a23_str
    assert x_rivergrade.belief_name == yao_str
    assert x_rivergrade.keep_rope == x_keep_rope
    assert x_rivergrade.voice_name == bob_str
    assert x_rivergrade.number == 0
    assert not x_rivergrade.tax_bill_amount
    assert not x_rivergrade.grant_amount
    assert not x_rivergrade.debtor_rank_num
    assert not x_rivergrade.credor_rank_num
    assert not x_rivergrade.tax_paid_amount
    assert not x_rivergrade.tax_paid_bool
    assert not x_rivergrade.tax_paid_rank_num
    assert not x_rivergrade.tax_paid_rank_percent
    assert not x_rivergrade.debtor_count
    assert not x_rivergrade.credor_count
    assert not x_rivergrade.debtor_rank_percent
    assert not x_rivergrade.credor_rank_percent
    assert not x_rivergrade.rewards_count
    assert not x_rivergrade.rewards_magnitude


def test_RiverGrade_set_tax_due_amount_SetsAttrs():
    # ESTABLISH
    x_rivergrade = RiverGrade()
    assert not x_rivergrade.tax_bill_amount
    assert not x_rivergrade.tax_paid_amount
    assert not x_rivergrade.tax_paid_bool

    # WHEN
    x_tax_due_amount = 88
    x_rivergrade.set_tax_bill_amount(x_tax_due_amount)
    # THEN
    assert x_rivergrade.tax_bill_amount == x_tax_due_amount
    assert not x_rivergrade.tax_paid_amount
    assert not x_rivergrade.tax_paid_bool

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


def test_RiverGrade_to_dict_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = temp_moment_label()
    x_keep_rope = None
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
        a23_str, yao_str, x_keep_rope, bob_str, ten_int, x_debtor_count, x_credor_count
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
    rivergrade_dict = x_rivergrade.to_dict()

    # THEN
    assert rivergrade_dict.get(wx.moment_label) == a23_str
    assert rivergrade_dict.get(wx.healer_name) == yao_str
    assert rivergrade_dict.get("keep_rope") == x_keep_rope
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
    yao_str = "Yao"
    a23_str = temp_moment_label()
    x_keep_rope = None
    ten_int = 10
    x_debtor_count = 101
    x_credor_count = 103

    x_rivergrade = rivergrade_shop(
        a23_str, yao_str, x_keep_rope, bob_str, ten_int, x_debtor_count, x_credor_count
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
  "grant_amount": null, 
  "healer_name": "Yao", 
  "keep_rope": null, 
  "moment_label": "ex_keep04", 
  "rewards_count": null, 
  "rewards_magnitude": null, 
  "tax_bill_amount": null, 
  "tax_paid_amount": null, 
  "tax_paid_bool": null, 
  "tax_paid_rank_num": null, 
  "tax_paid_rank_percent": null
}"""

    assert rivergrade_json == static_json
