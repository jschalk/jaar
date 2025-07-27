from src.a01_term_logic.term import BelieverName, PartnerName
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a14_keep_logic.rivercycle import get_credorledger
from src.a14_keep_logic.test._util.a14_env import get_module_temp_dir, temp_belief_label
from src.a14_keep_logic.test._util.example_keep_believers import get_texas_rope


def example_yao_hubunit() -> HubUnit:
    return hubunit_shop(get_module_temp_dir(), temp_belief_label(), "Yao")


def example_yao_texas_hubunit() -> HubUnit:
    belief_mstr_dir = get_module_temp_dir()
    return hubunit_shop(belief_mstr_dir, temp_belief_label(), "Yao", get_texas_rope())


def example_yao_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_partner_cred_points = 7
    bob_partner_cred_points = 3
    zia_partner_cred_points = 10
    yao_believer = believerunit_shop(yao_str)
    yao_believer.add_partnerunit(yao_str, yao_partner_cred_points)
    yao_believer.add_partnerunit(bob_str, bob_partner_cred_points)
    yao_believer.add_partnerunit(zia_str, zia_partner_cred_points)
    return get_credorledger(yao_believer)


def example_bob_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_partner_cred_points = 1
    bob_partner_cred_points = 7
    zia_partner_cred_points = 42
    bob_believer = believerunit_shop(bob_str)
    bob_believer.add_partnerunit(yao_str, yao_partner_cred_points)
    bob_believer.add_partnerunit(bob_str, bob_partner_cred_points)
    bob_believer.add_partnerunit(zia_str, zia_partner_cred_points)
    return get_credorledger(bob_believer)


def example_zia_credorledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_partner_cred_points = 89
    bob_partner_cred_points = 150
    zia_partner_cred_points = 61
    zia_believer = believerunit_shop(zia_str)
    zia_believer.add_partnerunit(yao_str, yao_partner_cred_points)
    zia_believer.add_partnerunit(bob_str, bob_partner_cred_points)
    zia_believer.add_partnerunit(zia_str, zia_partner_cred_points)
    return get_credorledger(zia_believer)


def example_yao_bob_zia_credorledgers() -> (
    dict[BelieverName : dict[PartnerName, float]]
):
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
