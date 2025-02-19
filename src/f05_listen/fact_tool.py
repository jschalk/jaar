from src.f01_road.road import OwnerName, RoadUnit
from src.f02_bud.reason_item import FactUnit, get_factunit_from_tuple
from copy import copy as copy_copy


def get_nodes_with_weighted_facts(
    nodes_facts_dict: dict[tuple[OwnerName], dict[RoadUnit, FactUnit]],
    nodes_quota_ledger_dict: dict[OwnerName, float],
) -> dict[tuple[OwnerName], dict[RoadUnit, dict[str, any]]]:

    sorted_node_addrs = sorted(nodes_facts_dict.keys(), key=len)

    while sorted_node_addrs != []:
        # grab one of the longest length node_addr tuples
        node_addr = sorted_node_addrs.pop()
        node_input_facts = nodes_facts_dict.get(node_addr)
        quota_ledger = nodes_quota_ledger_dict.get(node_addr)

        print("")
        print(f"working {node_addr=} ")
        print("for every one of the quota ledger children grab child's factunits")
        print(
            " and assign each one to that fact.base dictionary as full_fact tuple pointing to quota_sum"
        )
        print(" add quota to full_fact tuple")
        to_eval_temp = {}
        for child_owner, child_quota in quota_ledger.items():
            node_addr_list = list(node_addr)
            node_addr_list.append(child_owner)
            child_addr = tuple(node_addr_list)
            print(f"{child_addr=}")
            if child_input_facts := nodes_facts_dict.get(child_addr):
                for child_fact in child_input_facts.values():
                    to_eval_temp[child_fact.base] = {
                        child_fact.get_tuple(): child_quota
                    }
                    print(f"{child_fact.get_tuple()=}")
            else:
                for node_fact in node_input_facts.values():
                    to_eval_temp[node_fact.base] = {node_fact.get_tuple(): child_quota}
                    print(f"{node_fact.get_tuple()=}")

        print(f"{to_eval_temp=}")
        evaluated_facts = {
            fact_base: get_factunit_from_tuple(max(wgt_facts, key=wgt_facts.get))
            for fact_base, wgt_facts in to_eval_temp.items()
        }
        print(f"{node_input_facts=}")
        print(f"{evaluated_facts=}")
        nodes_facts_dict[node_addr] = evaluated_facts

    return nodes_facts_dict
