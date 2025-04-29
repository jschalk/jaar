from src.a01_word_logic.road import OwnerName, AcctName
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from src.a14_keep_logic._utils.env_a14 import (
    get_module_temp_dir,
    temp_fisc_tag,
    get_texas_road,
)
from src.a14_keep_logic.rivercycle import get_credorledger


def example_yao_hubunit() -> HubUnit:
    return hubunit_shop(get_module_temp_dir(), temp_fisc_tag(), "Yao")


def example_yao_texas_hubunit() -> HubUnit:
    return hubunit_shop(get_module_temp_dir(), temp_fisc_tag(), "Yao", get_texas_road())


def example_yao_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_credit_belief = 7
    bob_credit_belief = 3
    zia_credit_belief = 10
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(yao_str, yao_credit_belief)
    yao_bud.add_acctunit(bob_str, bob_credit_belief)
    yao_bud.add_acctunit(zia_str, zia_credit_belief)
    return get_credorledger(yao_bud)


def example_bob_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_credit_belief = 1
    bob_credit_belief = 7
    zia_credit_belief = 42
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(yao_str, yao_credit_belief)
    bob_bud.add_acctunit(bob_str, bob_credit_belief)
    bob_bud.add_acctunit(zia_str, zia_credit_belief)
    return get_credorledger(bob_bud)


def example_zia_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_credit_belief = 89
    bob_credit_belief = 150
    zia_credit_belief = 61
    zia_bud = budunit_shop(zia_str)
    zia_bud.add_acctunit(yao_str, yao_credit_belief)
    zia_bud.add_acctunit(bob_str, bob_credit_belief)
    zia_bud.add_acctunit(zia_str, zia_credit_belief)
    return get_credorledger(zia_bud)


def example_yao_bob_zia_credorledgers() -> dict[OwnerName : dict[AcctName, float]]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    return {
        yao_str: example_yao_credorledger,
        bob_str: example_bob_credorledger,
        zia_str: example_zia_credorledger,
    }


def example_yao_bob_zia_tax_dues() -> dict[AcctName, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_sum = sum(example_yao_credorledger().values())
    bob_sum = sum(example_bob_credorledger().values())
    zia_sum = sum(example_zia_credorledger().values())

    return {
        yao_str: yao_sum - 60000,
        bob_str: bob_sum - 500000,
        zia_str: zia_sum - 4000,
    }
