from src.a01_term_logic.term import AcctName, OwnerName
from src.a06_owner_logic.owner import ownerunit_shop
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a14_keep_logic.rivercycle import get_credorledger
from src.a14_keep_logic.test._util.a14_env import (
    get_module_temp_dir,
    get_texas_rope,
    temp_belief_label,
)


def example_yao_hubunit() -> HubUnit:
    return hubunit_shop(get_module_temp_dir(), temp_belief_label(), "Yao")


def example_yao_texas_hubunit() -> HubUnit:
    belief_mstr_dir = get_module_temp_dir()
    return hubunit_shop(belief_mstr_dir, temp_belief_label(), "Yao", get_texas_rope())


def example_yao_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_acct_cred_points = 7
    bob_acct_cred_points = 3
    zia_acct_cred_points = 10
    yao_owner = ownerunit_shop(yao_str)
    yao_owner.add_acctunit(yao_str, yao_acct_cred_points)
    yao_owner.add_acctunit(bob_str, bob_acct_cred_points)
    yao_owner.add_acctunit(zia_str, zia_acct_cred_points)
    return get_credorledger(yao_owner)


def example_bob_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_acct_cred_points = 1
    bob_acct_cred_points = 7
    zia_acct_cred_points = 42
    bob_owner = ownerunit_shop(bob_str)
    bob_owner.add_acctunit(yao_str, yao_acct_cred_points)
    bob_owner.add_acctunit(bob_str, bob_acct_cred_points)
    bob_owner.add_acctunit(zia_str, zia_acct_cred_points)
    return get_credorledger(bob_owner)


def example_zia_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_acct_cred_points = 89
    bob_acct_cred_points = 150
    zia_acct_cred_points = 61
    zia_owner = ownerunit_shop(zia_str)
    zia_owner.add_acctunit(yao_str, yao_acct_cred_points)
    zia_owner.add_acctunit(bob_str, bob_acct_cred_points)
    zia_owner.add_acctunit(zia_str, zia_acct_cred_points)
    return get_credorledger(zia_owner)


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
