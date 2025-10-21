from src.ch04_rope.rope import RopeTerm, create_rope_from_labels
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch14_keep._ref.ch14_semantic_types import BeliefName, VoiceName
from src.ch14_keep.rivercycle import get_patientledger


def get_nation_texas_rope() -> RopeTerm:
    naton_str = "nation"
    usa_str = "usa"
    texas_str = "texas"
    return create_rope_from_labels([naton_str, usa_str, texas_str])


def example_yao_patientledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_voice_cred_lumen = 7
    bob_voice_cred_lumen = 3
    zia_voice_cred_lumen = 10
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(yao_str, yao_voice_cred_lumen)
    yao_belief.add_voiceunit(bob_str, bob_voice_cred_lumen)
    yao_belief.add_voiceunit(zia_str, zia_voice_cred_lumen)
    return get_patientledger(yao_belief)


def example_bob_patientledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_voice_cred_lumen = 1
    bob_voice_cred_lumen = 7
    zia_voice_cred_lumen = 42
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_voiceunit(yao_str, yao_voice_cred_lumen)
    bob_belief.add_voiceunit(bob_str, bob_voice_cred_lumen)
    bob_belief.add_voiceunit(zia_str, zia_voice_cred_lumen)
    return get_patientledger(bob_belief)


def example_zia_patientledger() -> dict[str, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_voice_cred_lumen = 89
    bob_voice_cred_lumen = 150
    zia_voice_cred_lumen = 61
    zia_belief = beliefunit_shop(zia_str)
    zia_belief.add_voiceunit(yao_str, yao_voice_cred_lumen)
    zia_belief.add_voiceunit(bob_str, bob_voice_cred_lumen)
    zia_belief.add_voiceunit(zia_str, zia_voice_cred_lumen)
    return get_patientledger(zia_belief)


def example_yao_bob_zia_patientledgers() -> dict[BeliefName : dict[VoiceName, float]]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    return {
        yao_str: example_yao_patientledger,
        bob_str: example_bob_patientledger,
        zia_str: example_zia_patientledger,
    }


def example_yao_bob_zia_need_dues() -> dict[VoiceName, float]:
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_sum = sum(example_yao_patientledger().values())
    bob_sum = sum(example_bob_patientledger().values())
    zia_sum = sum(example_zia_patientledger().values())

    return {
        yao_str: yao_sum - 60000,
        bob_str: bob_sum - 500000,
        zia_str: zia_sum - 4000,
    }
