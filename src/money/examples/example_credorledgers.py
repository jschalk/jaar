from src._road.road import OwnerID, AcctID
from src.bud.bud import budunit_shop
from src.listen.hubunit import HubUnit, hubunit_shop
from src.money.examples.econ_env import temp_reals_dir, temp_real_id, get_texas_road
from src.money.rivercycle import get_credorledger


def example_yao_hubunit() -> HubUnit:
    return hubunit_shop(temp_reals_dir(), temp_real_id(), "Yao")


def example_yao_texas_hubunit() -> HubUnit:
    return hubunit_shop(temp_reals_dir(), temp_real_id(), "Yao", get_texas_road())


def example_yao_credorledger() -> dict[str, float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credit_score = 7
    bob_credit_score = 3
    zia_credit_score = 10
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_acctunit(yao_text, yao_credit_score)
    yao_bud.add_acctunit(bob_text, bob_credit_score)
    yao_bud.add_acctunit(zia_text, zia_credit_score)
    return get_credorledger(yao_bud)


def example_bob_credorledger() -> dict[str, float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credit_score = 1
    bob_credit_score = 7
    zia_credit_score = 42
    bob_bud = budunit_shop(bob_text)
    bob_bud.add_acctunit(yao_text, yao_credit_score)
    bob_bud.add_acctunit(bob_text, bob_credit_score)
    bob_bud.add_acctunit(zia_text, zia_credit_score)
    return get_credorledger(bob_bud)


def example_zia_credorledger() -> dict[str, float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credit_score = 89
    bob_credit_score = 150
    zia_credit_score = 61
    zia_bud = budunit_shop(zia_text)
    zia_bud.add_acctunit(yao_text, yao_credit_score)
    zia_bud.add_acctunit(bob_text, bob_credit_score)
    zia_bud.add_acctunit(zia_text, zia_credit_score)
    return get_credorledger(zia_bud)


def example_yao_bob_zia_credorledgers() -> dict[OwnerID : dict[AcctID, float]]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    return {
        yao_text: example_yao_credorledger,
        bob_text: example_bob_credorledger,
        zia_text: example_zia_credorledger,
    }


def example_yao_bob_zia_tax_dues() -> dict[AcctID, float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_sum = sum(example_yao_credorledger().values())
    bob_sum = sum(example_bob_credorledger().values())
    zia_sum = sum(example_zia_credorledger().values())

    return {
        yao_text: yao_sum - 60000,
        bob_text: bob_sum - 500000,
        zia_text: zia_sum - 4000,
    }
