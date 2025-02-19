from src.f01_road.road import OwnerName, RoadUnit
from copy import copy as copy_copy


def get_nodes_with_weighted_facts(
    nodes_input_facts_dict: dict[tuple[OwnerName], dict[RoadUnit, dict[str, any]]]
) -> dict[tuple[OwnerName], dict[RoadUnit, dict[str, any]]]:

    print(f"{nodes_input_facts_dict.keys()=}")
    to_eval_nodes_dict = {node_addr: {} for node_addr in nodes_input_facts_dict}
    sorted_node_addrs = sorted(nodes_input_facts_dict.keys(), key=len)

    while sorted_node_addrs != []:
        # grab one of the longest length tuples
        node_addr = sorted_node_addrs.pop()
        print(f"working {node_addr=}")
        node_input_facts = nodes_input_facts_dict.get(node_addr)
        to_eval_node_dict = to_eval_nodes_dict.get(node_addr)
        # if node has no children set to_evaluate to it's own fact
        if not to_eval_node_dict:
            to_eval_node_dict[node_addr] = node_input_facts

        # set parent_node's to_evaluate fact
        if len(node_addr) > 0:
            parent_node_addr = copy_copy(list(node_addr))
            parent_node_addr.pop()
            parent_node_addr = tuple(parent_node_addr)
            parent_to_eval_node = to_eval_nodes_dict.get(parent_node_addr)
            parent_to_eval_node[node_addr] = node_input_facts
            print(
                f" added to parent {parent_node_addr} to_eval: {parent_to_eval_node.keys()=}"
            )

    output_facts = {}
    for node_addr, to_eval_node_dict in to_eval_nodes_dict.items():
        output_facts[node_addr] = {}
        for to_eval_addr, facts in to_eval_node_dict.items():
            output_facts[node_addr] = facts

    print(f"{to_eval_nodes_dict=}")
    print(f"{output_facts=}")
    # node_be_facts_str = "node_be_facts"
    # to_eval_facts_str = "to_eval_facts"
    # output_facts_str = "output_facts"
    # x_found_dict = {node_be_facts_str: {}, to_eval_facts_str: {}, output_facts_str: {}}

    # while sorted_owners_tuples != []:
    #     # grab one of the longest length tuples
    #     node_owners = sorted_owners_tuples.pop()
    #     node_be_facts = node_be_facts_dict.get(node_owners)
    #     # if node has no children set to_evaluate to it's own fact
    #     if not to_eval_facts_dict.get(node_owners):

    #         print(f"{to_eval_facts_dict=}")
    #         to_eval_facts_dict.get(node_owners)[node_owners] = node_be_facts

    #     # set it's output facts
    #     print(f"{to_eval_facts_dict.get(node_owners)=}")
    #     this_node_to_evaluate_dict = to_eval_facts_dict.get(node_owners)
    #     for  this_node_to_evaluate_dict.get()
    #     if not to_eval_facts_dict.get(node_owners):
    #         print(f"{to_eval_facts_dict}")
    #         to_eval_facts_dict.get(node_owners)[node_owners] = node_be_facts
    #         print(f"{to_eval_facts_dict}")

    #     # set parent_node's to_evaluate fact
    #     if len(node_owners) > 0:
    #         parent_node_owners = copy_copy(list(node_owners))
    #         parent_node_owners.pop()
    #         parent_node_owners = tuple(parent_node_owners)
    #         to_eval_facts_dict.get(parent_node_owners)[node_owners] = node_be_facts
    #         # print(x_found_dict)

    return output_facts
