from src._road.road import OwnerID, CharID
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
    yao_credor_weight = 7
    bob_credor_weight = 3
    zia_credor_weight = 10
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_charunit(yao_text, yao_credor_weight)
    yao_bud.add_charunit(bob_text, bob_credor_weight)
    yao_bud.add_charunit(zia_text, zia_credor_weight)
    return get_credorledger(yao_bud)


def example_bob_credorledger() -> dict[str, float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credor_weight = 1
    bob_credor_weight = 7
    zia_credor_weight = 42
    bob_bud = budunit_shop(bob_text)
    bob_bud.add_charunit(yao_text, yao_credor_weight)
    bob_bud.add_charunit(bob_text, bob_credor_weight)
    bob_bud.add_charunit(zia_text, zia_credor_weight)
    return get_credorledger(bob_bud)


def example_zia_credorledger() -> dict[str, float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credor_weight = 89
    bob_credor_weight = 150
    zia_credor_weight = 61
    zia_bud = budunit_shop(zia_text)
    zia_bud.add_charunit(yao_text, yao_credor_weight)
    zia_bud.add_charunit(bob_text, bob_credor_weight)
    zia_bud.add_charunit(zia_text, zia_credor_weight)
    return get_credorledger(zia_bud)


def example_yao_bob_zia_credorledgers() -> dict[OwnerID : dict[CharID, float]]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    return {
        yao_text: example_yao_credorledger,
        bob_text: example_bob_credorledger,
        zia_text: example_zia_credorledger,
    }


def example_yao_bob_zia_tax_dues() -> dict[CharID, float]:
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
