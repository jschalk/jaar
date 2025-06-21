from src.a01_term_logic.term import AcctName, OwnerName
from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a14_keep_logic.rivercycle import get_credorledger
from src.a14_keep_logic.test._util.a14_env import (
    get_module_temp_dir,
    get_texas_rope,
    temp_bank_label,
)


def example_yao_hubunit() -> HubUnit:
    return hubunit_shop(get_module_temp_dir(), temp_bank_label(), "Yao")


def example_yao_texas_hubunit() -> HubUnit:
    bank_mstr_dir = get_module_temp_dir()
    return hubunit_shop(bank_mstr_dir, temp_bank_label(), "Yao", get_texas_rope())


def example_yao_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_credit_score = 7
    bob_credit_score = 3
    zia_credit_score = 10
    yao_plan = planunit_shop(yao_str)
    yao_plan.add_acctunit(yao_str, yao_credit_score)
    yao_plan.add_acctunit(bob_str, bob_credit_score)
    yao_plan.add_acctunit(zia_str, zia_credit_score)
    return get_credorledger(yao_plan)


def example_bob_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_credit_score = 1
    bob_credit_score = 7
    zia_credit_score = 42
    bob_plan = planunit_shop(bob_str)
    bob_plan.add_acctunit(yao_str, yao_credit_score)
    bob_plan.add_acctunit(bob_str, bob_credit_score)
    bob_plan.add_acctunit(zia_str, zia_credit_score)
    return get_credorledger(bob_plan)


def example_zia_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_credit_score = 89
    bob_credit_score = 150
    zia_credit_score = 61
    zia_plan = planunit_shop(zia_str)
    zia_plan.add_acctunit(yao_str, yao_credit_score)
    zia_plan.add_acctunit(bob_str, bob_credit_score)
    zia_plan.add_acctunit(zia_str, zia_credit_score)
    return get_credorledger(zia_plan)


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
