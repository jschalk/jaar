from src.f00_instrument.dict_toolbox import get_max_key
from src.f01_road.road import OwnerName, RoadUnit
from src.f02_bud.reason_item import FactUnit, get_factunit_from_tuple


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

        to_eval_temp = {}
        for child_owner, child_quota in quota_ledger.items():
            node_addr_list = list(node_addr)
            node_addr_list.append(child_owner)
            child_addr = tuple(node_addr_list)
            if child_input_facts := nodes_facts_dict.get(child_addr):
                for child_fact in child_input_facts.values():
                    if not to_eval_temp.get(child_fact.base):
                        to_eval_temp[child_fact.base] = {}
                    base_to_eval = to_eval_temp.get(child_fact.base)
                    child_fact_tuple = child_fact.get_tuple()
                    if not base_to_eval.get(child_fact_tuple):
                        base_to_eval[child_fact_tuple] = 0
                    current_fact_tuple_quota = base_to_eval.get(child_fact_tuple)
                    base_to_eval[child_fact_tuple] = (
                        child_quota + current_fact_tuple_quota
                    )

            for node_fact in node_input_facts.values():
                if to_eval_temp.get(node_fact.base) is None:
                    to_eval_temp[node_fact.base] = {node_fact.get_tuple(): child_quota}

        evaluated_facts = {
            fact_base: get_factunit_from_tuple(get_max_key(wgt_facts))
            for fact_base, wgt_facts in to_eval_temp.items()
        }
        nodes_facts_dict[node_addr] = evaluated_facts

    return nodes_facts_dict
