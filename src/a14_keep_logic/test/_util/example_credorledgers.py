from src.a01_term_logic.term import BeliefName, PartnerName
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a14_keep_logic.rivercycle import get_credorledger
from src.a14_keep_logic.test._util.a14_env import get_module_temp_dir, temp_moment_label
from src.a14_keep_logic.test._util.example_keep_beliefs import get_texas_rope


def example_yao_hubunit() -> HubUnit:
    return hubunit_shop(get_module_temp_dir(), temp_moment_label(), "Yao")


def example_yao_texas_hubunit() -> HubUnit:
    moment_mstr_dir = get_module_temp_dir()
    return hubunit_shop(moment_mstr_dir, temp_moment_label(), "Yao", get_texas_rope())


def example_yao_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_partner_cred_points = 7
    bob_partner_cred_points = 3
    zia_partner_cred_points = 10
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_partnerunit(yao_str, yao_partner_cred_points)
    yao_belief.add_partnerunit(bob_str, bob_partner_cred_points)
    yao_belief.add_partnerunit(zia_str, zia_partner_cred_points)
    return get_credorledger(yao_belief)


def example_bob_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_partner_cred_points = 1
    bob_partner_cred_points = 7
    zia_partner_cred_points = 42
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_partnerunit(yao_str, yao_partner_cred_points)
    bob_belief.add_partnerunit(bob_str, bob_partner_cred_points)
    bob_belief.add_partnerunit(zia_str, zia_partner_cred_points)
    return get_credorledger(bob_belief)


def example_zia_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_partner_cred_points = 89
    bob_partner_cred_points = 150
    zia_partner_cred_points = 61
    zia_belief = beliefunit_shop(zia_str)
    zia_belief.add_partnerunit(yao_str, yao_partner_cred_points)
    zia_belief.add_partnerunit(bob_str, bob_partner_cred_points)
    zia_belief.add_partnerunit(zia_str, zia_partner_cred_points)
    return get_credorledger(zia_belief)


def example_yao_bob_zia_credorledgers() -> dict[BeliefName : dict[PartnerName, float]]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    return {
        yao_str: example_yao_credorledger,
        bob_str: example_bob_credorledger,
        zia_str: example_zia_credorledger,
    }


def example_yao_bob_zia_tax_dues() -> dict[PartnerName, float]:
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
