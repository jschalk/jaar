from src.a12_hub_tools.fact_tool import get_nodes_with_weighted_facts
from src.a13_bud_listen_logic._utils.example_listen import (
    example_casa_clean_factunit,
    example_casa_dirty_factunit,
    example_sky_blue_factunit,
)


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario00_RootOnly_NoFacts():
    # ESTABLISH
    nodes_facts_dict = {}
    nodes_quota_ledger_dict = {}

    # WHEN
    nodes_weighted_facts = get_nodes_with_weighted_facts(
        nodes_facts_dict, nodes_quota_ledger_dict
    )

    # THEN
    assert nodes_weighted_facts == {}


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario01_Multiple_Nodes_NoFacts():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    root_addr = ()
    bob_addr = (bob_str,)
    bob_yao_addr = (bob_str, yao_str)
    nodes_facts_dict = {root_addr: {}, bob_addr: {}, bob_yao_addr: {}}
    nodes_quota_dict = {
        root_addr: {bob_str: 1},
        bob_addr: {yao_str: 1},
        bob_yao_addr: {sue_str: 1},
    }

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    assert nodes_wgt_facts == nodes_facts_dict


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario02_RootHasOneFact():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    root_facts = {clean_fact.fbase: clean_fact}
    root_addr = ()
    bob_str = "Bob"
    nodes_facts_dict = {root_addr: root_facts}
    nodes_quota_dict = {root_addr: {bob_str: 1}}

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    assert nodes_wgt_facts == nodes_facts_dict


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario03_ChildHasOneFact():
    # ESTABLISH
    bob_str = "Bob"
    clean_fact = example_casa_clean_factunit()
    root_facts = {}
    bob_facts = {clean_fact.fbase: clean_fact}
    root_addr = ()
    bob_addr = (bob_str,)
    yao_str = "Yao"
    nodes_facts_dict = {root_addr: root_facts, bob_addr: bob_facts}
    nodes_quota_dict = {root_addr: {bob_str: 1}, bob_addr: {yao_str: 1}}

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {(): bob_facts, (bob_str,): bob_facts}
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario04_ChildHasOneFact():
    # ESTABLISH
    bob_str = "Bob"
    clean_fact = example_casa_clean_factunit()
    root_facts = {}
    bob_facts = {clean_fact.fbase: clean_fact}
    bob_str = "Bob"
    root_addr = ()
    bob_addr = (bob_str,)
    yao_str = "Yao"
    nodes_facts_dict = {root_addr: root_facts, bob_addr: bob_facts}
    nodes_quota_dict = {root_addr: {bob_str: 1}, bob_addr: {yao_str: 1}}
    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {(): bob_facts, (bob_str,): bob_facts}
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario05_Level2ChildHasOneFact():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    clean_fact = example_casa_clean_factunit()
    root_addr = ()
    bob_addr = (bob_str,)
    bob_yao_addr = (bob_str, yao_str)
    bob_yao_facts = {clean_fact.fbase: clean_fact}
    nodes_facts_dict = {root_addr: {}, bob_addr: {}, bob_yao_addr: bob_yao_facts}
    nodes_quota_dict = {
        root_addr: {bob_str: 1},
        bob_addr: {yao_str: 1},
        bob_yao_addr: {yao_str: 1},
    }

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {
        root_addr: bob_yao_facts,
        bob_addr: bob_yao_facts,
        bob_yao_addr: bob_yao_facts,
    }
    assert nodes_wgt_facts.get(bob_yao_addr) == bob_yao_facts
    assert nodes_wgt_facts.get(bob_addr) == bob_yao_facts
    assert nodes_wgt_facts.get(root_addr) == bob_yao_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario06_Level2ChildsHaveTwoFacts():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    clean_fact = example_casa_clean_factunit()
    sky_fact = example_sky_blue_factunit()
    root_addr = ()
    bob_addr = (bob_str,)
    bob_yao_addr = (bob_str, yao_str)
    bob_facts = {sky_fact.fbase: sky_fact}
    bob_yao_facts = {clean_fact.fbase: clean_fact}
    nodes_facts_dict = {root_addr: {}, bob_addr: bob_facts, bob_yao_addr: bob_yao_facts}
    nodes_quota_dict = {
        root_addr: {bob_str: 1},
        bob_addr: {yao_str: 1},
        bob_yao_addr: {yao_str: 1},
    }

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_bob_facts = {sky_fact.fbase: sky_fact, clean_fact.fbase: clean_fact}
    expected_nodes_weighted_facts = {
        root_addr: expected_bob_facts,
        bob_addr: expected_bob_facts,
        bob_yao_addr: bob_yao_facts,
    }
    assert nodes_wgt_facts.get(bob_yao_addr) == bob_yao_facts
    assert nodes_wgt_facts.get(bob_addr) == expected_bob_facts
    assert nodes_wgt_facts.get(root_addr) == expected_bob_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario07_Level2ChildFactOverridesAncestorFact():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    clean_fact = example_casa_clean_factunit()
    dirty_fact = example_casa_dirty_factunit()
    root_addr = ()
    bob_addr = (bob_str,)
    bob_yao_addr = (bob_str, yao_str)
    dirty_facts = {dirty_fact.fbase: dirty_fact}
    bob_yao_facts = {clean_fact.fbase: clean_fact}
    nodes_facts_dict = {
        root_addr: {},
        bob_addr: dirty_facts,
        bob_yao_addr: bob_yao_facts,
    }
    nodes_quota_dict = {
        root_addr: {bob_str: 1},
        bob_addr: {yao_str: 1},
        bob_yao_addr: {yao_str: 1},
    }

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_clean_facts = {clean_fact.fbase: clean_fact}
    expected_nodes_weighted_facts = {
        root_addr: expected_clean_facts,
        bob_addr: expected_clean_facts,
        bob_yao_addr: bob_yao_facts,
    }
    assert nodes_wgt_facts.get(bob_yao_addr) == bob_yao_facts
    assert nodes_wgt_facts.get(bob_addr) == expected_clean_facts
    assert nodes_wgt_facts.get(root_addr) == expected_clean_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario08_Level2ChildHasDiffentFacts():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    clean_fact = example_casa_clean_factunit()
    dirty_fact = example_casa_dirty_factunit()
    root_addr = ()
    bob_addr = (bob_str,)
    bob_quota_sue = 7
    bob_quota_yao = 7
    bob_yao_addr = (bob_str, yao_str)
    bob_sue_addr = (bob_str, sue_str)
    bob_facts = {}
    bob_yao_facts = {clean_fact.fbase: clean_fact}
    bob_sue_facts = {dirty_fact.fbase: dirty_fact}
    nodes_facts_dict = {
        root_addr: {},
        bob_addr: bob_facts,
        bob_yao_addr: bob_yao_facts,
        bob_sue_addr: bob_sue_facts,
    }
    nodes_quota_dict = {
        root_addr: {bob_str: 1},
        bob_addr: {yao_str: bob_quota_sue, sue_str: bob_quota_yao},
        bob_yao_addr: {yao_str: 1},
        bob_sue_addr: {yao_str: 1},
    }
    assert bob_quota_sue == bob_quota_yao

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    dirty_facts = {dirty_fact.fbase: dirty_fact}
    expected_clean_facts = {clean_fact.fbase: clean_fact}
    expected_nodes_weighted_facts = {
        root_addr: expected_clean_facts,
        bob_addr: expected_clean_facts,
        bob_yao_addr: bob_yao_facts,
        bob_sue_addr: dirty_facts,
    }
    assert nodes_wgt_facts.get(bob_sue_addr) == dirty_facts
    assert nodes_wgt_facts.get(bob_yao_addr) == expected_clean_facts
    assert nodes_wgt_facts.get(bob_addr) == expected_clean_facts
    assert nodes_wgt_facts.get(root_addr) == expected_clean_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario09_Level2ChildThreeChildFacts():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"
    clean_fact = example_casa_clean_factunit()
    dirty_fact = example_casa_dirty_factunit()
    root_addr = ()
    bob_addr = (bob_str,)
    bob_quota_yao = 7
    bob_quota_sue = 5
    bob_quota_zia = 5
    bob_yao_addr = (bob_str, yao_str)
    bob_sue_addr = (bob_str, sue_str)
    bob_zia_addr = (bob_str, zia_str)
    clean_facts = {clean_fact.fbase: clean_fact}
    dirty_facts = {dirty_fact.fbase: dirty_fact}
    nodes_facts_dict = {
        root_addr: {},
        bob_addr: {},
        bob_yao_addr: clean_facts,
        bob_sue_addr: dirty_facts,
        bob_zia_addr: dirty_facts,
    }
    nodes_quota_dict = {
        root_addr: {bob_str: 1},
        bob_addr: {
            yao_str: bob_quota_yao,
            sue_str: bob_quota_sue,
            zia_str: bob_quota_zia,
        },
        bob_yao_addr: {yao_str: 1},
        bob_sue_addr: {yao_str: 1},
        bob_zia_addr: {yao_str: 1},
    }
    assert bob_quota_yao < bob_quota_sue + bob_quota_zia

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {
        root_addr: dirty_facts,
        bob_addr: dirty_facts,
        bob_yao_addr: clean_facts,
        bob_sue_addr: dirty_facts,
        bob_zia_addr: dirty_facts,
    }
    assert nodes_wgt_facts.get(bob_zia_addr) == dirty_facts
    assert nodes_wgt_facts.get(bob_sue_addr) == dirty_facts
    assert nodes_wgt_facts.get(bob_yao_addr) == clean_facts
    assert nodes_wgt_facts.get(bob_addr) == dirty_facts
    assert nodes_wgt_facts.get(root_addr) == dirty_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnObj_Scenario10_Level2ChildTwoChildFactsOneMissing():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"
    clean_fact = example_casa_clean_factunit()
    dirty_fact = example_casa_dirty_factunit()
    root_addr = ()
    bob_addr = (bob_str,)
    bob_quota_yao = 7
    bob_quota_sue = 5
    bob_quota_zia = 5
    bob_yao_addr = (bob_str, yao_str)
    bob_sue_addr = (bob_str, sue_str)
    clean_facts = {clean_fact.fbase: clean_fact}
    dirty_facts = {dirty_fact.fbase: dirty_fact}
    nodes_facts_dict = {
        root_addr: {},
        bob_addr: dirty_facts,
        bob_yao_addr: clean_facts,
        bob_sue_addr: dirty_facts,
    }
    nodes_quota_dict = {
        root_addr: {bob_str: 1},
        bob_addr: {
            yao_str: bob_quota_yao,
            sue_str: bob_quota_sue,
            zia_str: bob_quota_zia,
        },
        bob_yao_addr: {yao_str: 1},
        bob_sue_addr: {yao_str: 1},
    }
    assert bob_quota_yao < bob_quota_sue + bob_quota_zia

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {
        root_addr: dirty_facts,
        bob_addr: dirty_facts,
        bob_yao_addr: clean_facts,
        bob_sue_addr: dirty_facts,
    }
    assert nodes_wgt_facts.get(bob_sue_addr) == dirty_facts
    assert nodes_wgt_facts.get(bob_yao_addr) == clean_facts
    assert nodes_wgt_facts.get(bob_addr) == dirty_facts
    assert nodes_wgt_facts.get(root_addr) == dirty_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts
