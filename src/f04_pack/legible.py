from src.a00_data_toolboxs.dict_toolbox import get_from_nested_dict
from src.a06_bud_logic.bud import BudUnit
from src.a06_bud_logic.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_factunit_str,
)
from src.f04_pack.atom import BudAtom
from src.f04_pack.atom_config import (
    atom_delete,
    atom_insert,
    atom_update,
    acct_name_str,
    awardee_tag_str,
    group_label_str,
    team_tag_str,
    healer_name_str,
    parent_road_str,
    item_title_str,
    base_item_active_requisite_str,
    pledge_str,
    addin_str,
    begin_str,
    close_str,
    denom_str,
    numor_str,
    morph_str,
    credit_vote_str,
    debtit_vote_str,
    credor_respect_str,
    debtor_respect_str,
    fnigh_str,
    fopen_str,
)
from src.f04_pack.delta import BudDelta


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_from_nested_dict(x_dict, x_keylist, if_missing_return_None=True)


def create_legible_list(x_delta: BudDelta, x_bud: BudUnit) -> list[str]:
    atoms_dict = x_delta.budatoms
    budunit_atom = get_leg_obj(atoms_dict, [atom_update(), budunit_str()])

    acctunit_insert_dict = get_leg_obj(atoms_dict, [atom_insert(), bud_acctunit_str()])
    acctunit_update_dict = get_leg_obj(atoms_dict, [atom_update(), bud_acctunit_str()])
    acctunit_delete_dict = get_leg_obj(atoms_dict, [atom_delete(), bud_acctunit_str()])

    x_list = [atom_insert(), bud_acct_membership_str()]
    acct_membership_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_acct_membership_str()]
    acct_membership_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_acct_membership_str()]
    acct_membership_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_itemunit_str()]
    bud_itemunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_itemunit_str()]
    bud_itemunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_itemunit_str()]
    bud_itemunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_item_awardlink_str()]
    bud_item_awardlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_item_awardlink_str()]
    bud_item_awardlink_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_item_awardlink_str()]
    bud_item_awardlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_item_reasonunit_str()]
    bud_item_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_item_reasonunit_str()]
    bud_item_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_item_reasonunit_str()]
    bud_item_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_item_reason_premiseunit_str()]
    bud_item_reason_premiseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_item_reason_premiseunit_str()]
    bud_item_reason_premiseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_item_reason_premiseunit_str()]
    bud_item_reason_premiseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_item_teamlink_str()]
    bud_item_teamlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_item_teamlink_str()]
    bud_item_teamlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_item_healerlink_str()]
    bud_item_healerlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_item_healerlink_str()]
    bud_item_healerlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_item_factunit_str()]
    bud_item_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_item_factunit_str()]
    bud_item_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_item_factunit_str()]
    bud_item_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    leg_list = []
    if budunit_atom is not None:
        add_budunit_legible_list(leg_list, budunit_atom, x_bud)
    if acctunit_insert_dict is not None:
        add_bud_acctunit_insert_to_legible_list(leg_list, acctunit_insert_dict, x_bud)
    if acctunit_update_dict is not None:
        add_bud_acctunit_update_to_legible_list(leg_list, acctunit_update_dict, x_bud)
    if acctunit_delete_dict is not None:
        add_bud_acctunit_delete_to_legible_list(leg_list, acctunit_delete_dict, x_bud)

    if acct_membership_insert_dict is not None:
        add_bud_acct_membership_insert_to_legible_list(
            leg_list, acct_membership_insert_dict, x_bud
        )
    if acct_membership_update_dict is not None:
        add_bud_acct_membership_update_to_legible_list(
            leg_list, acct_membership_update_dict, x_bud
        )
    if acct_membership_delete_dict is not None:
        add_bud_acct_membership_delete_to_legible_list(
            leg_list, acct_membership_delete_dict, x_bud
        )

    if bud_itemunit_insert_dict is not None:
        add_bud_itemunit_insert_to_legible_list(
            leg_list, bud_itemunit_insert_dict, x_bud
        )
    if bud_itemunit_update_dict is not None:
        add_bud_itemunit_update_to_legible_list(
            leg_list, bud_itemunit_update_dict, x_bud
        )
    if bud_itemunit_delete_dict is not None:
        add_bud_itemunit_delete_to_legible_list(
            leg_list, bud_itemunit_delete_dict, x_bud
        )

    if bud_item_awardlink_insert_dict is not None:
        add_bud_item_awardlink_insert_to_legible_list(
            leg_list, bud_item_awardlink_insert_dict, x_bud
        )
    if bud_item_awardlink_update_dict is not None:
        add_bud_item_awardlink_update_to_legible_list(
            leg_list, bud_item_awardlink_update_dict, x_bud
        )
    if bud_item_awardlink_delete_dict is not None:
        add_bud_item_awardlink_delete_to_legible_list(
            leg_list, bud_item_awardlink_delete_dict, x_bud
        )

    if bud_item_reasonunit_insert_dict is not None:
        add_bud_item_reasonunit_insert_to_legible_list(
            leg_list, bud_item_reasonunit_insert_dict, x_bud
        )
    if bud_item_reasonunit_update_dict is not None:
        add_bud_item_reasonunit_update_to_legible_list(
            leg_list, bud_item_reasonunit_update_dict, x_bud
        )
    if bud_item_reasonunit_delete_dict is not None:
        add_bud_item_reasonunit_delete_to_legible_list(
            leg_list, bud_item_reasonunit_delete_dict, x_bud
        )

    if bud_item_reason_premiseunit_insert_dict is not None:
        add_bud_reason_premiseunit_insert_to_legible_list(
            leg_list, bud_item_reason_premiseunit_insert_dict, x_bud
        )
    if bud_item_reason_premiseunit_update_dict is not None:
        add_bud_reason_premiseunit_update_to_legible_list(
            leg_list, bud_item_reason_premiseunit_update_dict, x_bud
        )
    if bud_item_reason_premiseunit_delete_dict is not None:
        add_bud_reason_premiseunit_delete_to_legible_list(
            leg_list, bud_item_reason_premiseunit_delete_dict, x_bud
        )

    if bud_item_teamlink_insert_dict is not None:
        add_bud_item_teamlink_insert_to_legible_list(
            leg_list, bud_item_teamlink_insert_dict, x_bud
        )
    if bud_item_teamlink_delete_dict is not None:
        add_bud_item_teamlink_delete_to_legible_list(
            leg_list, bud_item_teamlink_delete_dict, x_bud
        )

    if bud_item_healerlink_insert_dict is not None:
        add_bud_item_healerlink_insert_to_legible_list(
            leg_list, bud_item_healerlink_insert_dict, x_bud
        )
    if bud_item_healerlink_delete_dict is not None:
        add_bud_item_healerlink_delete_to_legible_list(
            leg_list, bud_item_healerlink_delete_dict, x_bud
        )

    if bud_item_factunit_insert_dict is not None:
        add_bud_item_factunit_insert_to_legible_list(
            leg_list, bud_item_factunit_insert_dict, x_bud
        )
    if bud_item_factunit_update_dict is not None:
        add_bud_item_factunit_update_to_legible_list(
            leg_list, bud_item_factunit_update_dict, x_bud
        )
    if bud_item_factunit_delete_dict is not None:
        add_bud_item_factunit_delete_to_legible_list(
            leg_list, bud_item_factunit_delete_dict, x_bud
        )

    return leg_list


def add_budunit_legible_list(legible_list: list[str], x_atom: BudAtom, x_bud: BudUnit):
    jvalues = x_atom.jvalues
    _tally_str = "tally"
    _max_tree_traverse_str = "max_tree_traverse"
    _max_tree_traverse_value = jvalues.get(_max_tree_traverse_str)
    credor_respect_value = jvalues.get(credor_respect_str())
    debtor_respect_value = jvalues.get(debtor_respect_str())
    _tally_value = jvalues.get(_tally_str)

    if _max_tree_traverse_value is not None:
        x_str = f"{x_bud.owner_name}'s maximum number of Bud evaluations set to {_max_tree_traverse_value}"
        legible_list.append(x_str)
    if (
        credor_respect_value is not None
        and debtor_respect_value is not None
        and credor_respect_value == debtor_respect_value
    ):
        x_str = f"{x_bud.owner_name}'s total pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif credor_respect_value is not None:
        x_str = f"{x_bud.owner_name}'s credor pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif debtor_respect_value is not None:
        x_str = f"{x_bud.owner_name}'s debtor pool is now {debtor_respect_value}"
        legible_list.append(x_str)
    if _tally_value is not None:
        x_str = f"{x_bud.owner_name}'s bud tally set to {_tally_value}"
        legible_list.append(x_str)


def add_bud_acctunit_insert_to_legible_list(
    legible_list: list[str], acctunit_dict: BudAtom, x_bud: BudUnit
):
    for acctunit_atom in acctunit_dict.values():
        acct_name = acctunit_atom.get_value(acct_name_str())
        credit_belief_value = acctunit_atom.get_value("credit_belief")
        debtit_belief_value = acctunit_atom.get_value("debtit_belief")
        x_str = f"{acct_name} was added with {credit_belief_value} belief credit and {debtit_belief_value} belief debtit"
        legible_list.append(x_str)


def add_bud_acctunit_update_to_legible_list(
    legible_list: list[str], acctunit_dict: BudAtom, x_bud: BudUnit
):
    for acctunit_atom in acctunit_dict.values():
        acct_name = acctunit_atom.get_value(acct_name_str())
        credit_belief_value = acctunit_atom.get_value("credit_belief")
        debtit_belief_value = acctunit_atom.get_value("debtit_belief")
        if credit_belief_value is not None and debtit_belief_value is not None:
            x_str = f"{acct_name} now has {credit_belief_value} belief credit and {debtit_belief_value} belief debtit."
        elif credit_belief_value is not None:
            x_str = f"{acct_name} now has {credit_belief_value} belief credit."
        elif debtit_belief_value is not None:
            x_str = f"{acct_name} now has {debtit_belief_value} belief debtit."
        legible_list.append(x_str)


def add_bud_acctunit_delete_to_legible_list(
    legible_list: list[str], acctunit_dict: BudAtom, x_bud: BudUnit
):
    for acctunit_atom in acctunit_dict.values():
        acct_name = acctunit_atom.get_value(acct_name_str())
        x_str = f"{acct_name} was removed from belief accts."
        legible_list.append(x_str)


def add_bud_acct_membership_insert_to_legible_list(
    legible_list: list[str], acct_membership_insert_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_insert_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_label = acct_membership_atom.get_value(group_label_str())
            acct_name = acct_membership_atom.get_value(acct_name_str())
            credit_vote_value = acct_membership_atom.get_value(credit_vote_str())
            debtit_vote_value = acct_membership_atom.get_value(debtit_vote_str())
            x_str = f"Group '{group_label}' has new membership {acct_name} with {credit_vote_str()}_value{credit_vote_value} and {debtit_vote_str()}_value={debtit_vote_value}."
            legible_list.append(x_str)


def add_bud_acct_membership_update_to_legible_list(
    legible_list: list[str], acct_membership_update_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_update_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_label = acct_membership_atom.get_value(group_label_str())
            acct_name = acct_membership_atom.get_value(acct_name_str())
            credit_vote_value = acct_membership_atom.get_value(credit_vote_str())
            debtit_vote_value = acct_membership_atom.get_value(debtit_vote_str())
            if credit_vote_value is not None and debtit_vote_value is not None:
                x_str = f"Group '{group_label}' membership {acct_name} has new {credit_vote_str()}_value{credit_vote_value} and {debtit_vote_str()}_value={debtit_vote_value}."
            elif credit_vote_value is not None:
                x_str = f"Group '{group_label}' membership {acct_name} has new {credit_vote_str()}_value{credit_vote_value}."
            elif debtit_vote_value is not None:
                x_str = f"Group '{group_label}' membership {acct_name} has new {debtit_vote_str()}_value={debtit_vote_value}."
            legible_list.append(x_str)


def add_bud_acct_membership_delete_to_legible_list(
    legible_list: list[str], acct_membership_delete_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_delete_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_label = acct_membership_atom.get_value(group_label_str())
            acct_name = acct_membership_atom.get_value(acct_name_str())
            x_str = f"Group '{group_label}' no longer has membership {acct_name}."
            legible_list.append(x_str)


def add_bud_itemunit_insert_to_legible_list(
    legible_list: list[str], itemunit_insert_dict: dict, x_bud: BudUnit
):
    _problem_bool_str = "problem_bool"
    _morph_str = "morph"
    _mass_str = "mass"
    for parent_road_dict in itemunit_insert_dict.values():
        for itemunit_atom in parent_road_dict.values():
            item_title_value = itemunit_atom.get_value(item_title_str())
            parent_road_value = itemunit_atom.get_value(parent_road_str())
            _addin_value = itemunit_atom.get_value(addin_str())
            _begin_value = itemunit_atom.get_value(begin_str())
            _close_value = itemunit_atom.get_value(close_str())
            _denom_value = itemunit_atom.get_value(denom_str())
            _numor_value = itemunit_atom.get_value(numor_str())
            _problem_bool_value = itemunit_atom.get_value(_problem_bool_str)
            _morph_value = itemunit_atom.get_value(_morph_str)
            _mass_value = itemunit_atom.get_value(_mass_str)
            pledge_value = itemunit_atom.get_value(pledge_str())
            x_str = f"Created Item '{item_title_value}' with parent_road {parent_road_value}. "
            if _addin_value is not None:
                x_str += f"addin={_addin_value}."
            if _begin_value is not None:
                x_str += f"begin={_begin_value}."
            if _close_value is not None:
                x_str += f"close={_close_value}."
            if _denom_value is not None:
                x_str += f"denom={_denom_value}."
            if _numor_value is not None:
                x_str += f"numor={_numor_value}."
            if _problem_bool_value is not None:
                x_str += f"problem_bool={_problem_bool_value}."
            if _morph_value is not None:
                x_str += f"morph={_morph_value}."
            if _mass_value is not None:
                x_str += f"mass={_mass_value}."
            if pledge_value is not None:
                x_str += f"pledge={pledge_value}."

            legible_list.append(x_str)


def add_bud_itemunit_update_to_legible_list(
    legible_list: list[str], itemunit_update_dict: dict, x_bud: BudUnit
):
    _problem_bool_str = "problem_bool"
    _mass_str = "mass"
    for parent_road_dict in itemunit_update_dict.values():
        for itemunit_atom in parent_road_dict.values():
            item_title_value = itemunit_atom.get_value(item_title_str())
            parent_road_value = itemunit_atom.get_value(parent_road_str())
            addin_value = itemunit_atom.get_value(addin_str())
            begin_value = itemunit_atom.get_value(begin_str())
            close_value = itemunit_atom.get_value(close_str())
            denom_value = itemunit_atom.get_value(denom_str())
            numor_value = itemunit_atom.get_value(numor_str())
            problem_bool_value = itemunit_atom.get_value(_problem_bool_str)
            morph_value = itemunit_atom.get_value(morph_str())
            mass_value = itemunit_atom.get_value(_mass_str)
            pledge_value = itemunit_atom.get_value(pledge_str())
            x_str = f"Item '{item_title_value}' with parent_road {parent_road_value} set these attributes: "
            if addin_value is not None:
                x_str += f"addin={addin_value}."
            if begin_value is not None:
                x_str += f"begin={begin_value}."
            if close_value is not None:
                x_str += f"close={close_value}."
            if denom_value is not None:
                x_str += f"denom={denom_value}."
            if numor_value is not None:
                x_str += f"numor={numor_value}."
            if problem_bool_value is not None:
                x_str += f"problem_bool={problem_bool_value}."
            if morph_value is not None:
                x_str += f"morph={morph_value}."
            if mass_value is not None:
                x_str += f"mass={mass_value}."
            if pledge_value is not None:
                x_str += f"pledge={pledge_value}."

            legible_list.append(x_str)


def add_bud_itemunit_delete_to_legible_list(
    legible_list: list[str], itemunit_delete_dict: dict, x_bud: BudUnit
):
    for parent_road_dict in itemunit_delete_dict.values():
        for itemunit_atom in parent_road_dict.values():
            item_title_value = itemunit_atom.get_value(item_title_str())
            parent_road_value = itemunit_atom.get_value(parent_road_str())
            x_str = f"Item '{item_title_value}' with parent_road {parent_road_value} was deleted."
            legible_list.append(x_str)


def add_bud_item_awardlink_insert_to_legible_list(
    legible_list: list[str], item_awardlink_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in item_awardlink_insert_dict.values():
        for item_awardlink_atom in road_dict.values():
            awardee_tag_value = item_awardlink_atom.get_value(awardee_tag_str())
            road_value = item_awardlink_atom.get_value("road")
            give_force_value = item_awardlink_atom.get_value("give_force")
            take_force_value = item_awardlink_atom.get_value("take_force")
            x_str = f"Awardlink created for group {awardee_tag_value} for item '{road_value}' with give_force={give_force_value} and take_force={take_force_value}."
            legible_list.append(x_str)


def add_bud_item_awardlink_update_to_legible_list(
    legible_list: list[str], item_awardlink_update_dict: dict, x_bud: BudUnit
):
    for road_dict in item_awardlink_update_dict.values():
        for item_awardlink_atom in road_dict.values():
            awardee_tag_value = item_awardlink_atom.get_value(awardee_tag_str())
            road_value = item_awardlink_atom.get_value("road")
            give_force_value = item_awardlink_atom.get_value("give_force")
            take_force_value = item_awardlink_atom.get_value("take_force")
            if give_force_value is not None and take_force_value is not None:
                x_str = f"Awardlink has been set for group {awardee_tag_value} for item '{road_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
            elif give_force_value is not None:
                x_str = f"Awardlink has been set for group {awardee_tag_value} for item '{road_value}'. Now give_force={give_force_value}."
            elif take_force_value is not None:
                x_str = f"Awardlink has been set for group {awardee_tag_value} for item '{road_value}'. Now take_force={take_force_value}."
            legible_list.append(x_str)


def add_bud_item_awardlink_delete_to_legible_list(
    legible_list: list[str], item_awardlink_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in item_awardlink_delete_dict.values():
        for item_awardlink_atom in road_dict.values():
            awardee_tag_value = item_awardlink_atom.get_value(awardee_tag_str())
            road_value = item_awardlink_atom.get_value("road")
            x_str = f"Awardlink for group {awardee_tag_value}, item '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_bud_item_reasonunit_insert_to_legible_list(
    legible_list: list[str], item_reasonunit_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in item_reasonunit_insert_dict.values():
        for item_reasonunit_atom in road_dict.values():
            road_value = item_reasonunit_atom.get_value("road")
            base_value = item_reasonunit_atom.get_value("base")
            base_item_active_requisite_value = item_reasonunit_atom.get_value(
                base_item_active_requisite_str()
            )
            x_str = (
                f"ReasonUnit created for item '{road_value}' with base '{base_value}'."
            )
            if base_item_active_requisite_value is not None:
                x_str += (
                    f" base_item_active_requisite={base_item_active_requisite_value}."
                )
            legible_list.append(x_str)


def add_bud_item_reasonunit_update_to_legible_list(
    legible_list: list[str], item_reasonunit_update_dict: dict, x_bud: BudUnit
):
    for road_dict in item_reasonunit_update_dict.values():
        for item_reasonunit_atom in road_dict.values():
            road_value = item_reasonunit_atom.get_value("road")
            base_value = item_reasonunit_atom.get_value("base")
            base_item_active_requisite_value = item_reasonunit_atom.get_value(
                base_item_active_requisite_str()
            )
            if base_item_active_requisite_value is not None:
                x_str = f"ReasonUnit base='{base_value}' for item '{road_value}' set with base_item_active_requisite={base_item_active_requisite_value}."
            else:
                x_str = f"ReasonUnit base='{base_value}' for item '{road_value}' and no longer checks base active mode."
            legible_list.append(x_str)


def add_bud_item_reasonunit_delete_to_legible_list(
    legible_list: list[str], item_reasonunit_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in item_reasonunit_delete_dict.values():
        for item_reasonunit_atom in road_dict.values():
            road_value = item_reasonunit_atom.get_value("road")
            base_value = item_reasonunit_atom.get_value("base")
            x_str = f"ReasonUnit base='{base_value}' for item '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_bud_reason_premiseunit_insert_to_legible_list(
    legible_list: list[str],
    item_reason_premiseunit_insert_dict: dict,
    x_bud: BudUnit,
):
    road_str = "road"
    base_str = "base"
    need_str = "need"
    divisor_str = "divisor"
    nigh_str = "nigh"
    open_str = "open"
    for road_dict in item_reason_premiseunit_insert_dict.values():
        for base_dict in road_dict.values():
            for item_reason_premiseunit_atom in base_dict.values():
                road_value = item_reason_premiseunit_atom.get_value(road_str)
                base_value = item_reason_premiseunit_atom.get_value(base_str)
                need_value = item_reason_premiseunit_atom.get_value(need_str)
                divisor_value = item_reason_premiseunit_atom.get_value(divisor_str)
                nigh_value = item_reason_premiseunit_atom.get_value(nigh_str)
                open_value = item_reason_premiseunit_atom.get_value(open_str)
                x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for item '{road_value}'."
                if open_value is not None:
                    x_str += f" Open={open_value}."
                if nigh_value is not None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value is not None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_bud_reason_premiseunit_update_to_legible_list(
    legible_list: list[str],
    item_reason_premiseunit_update_dict: dict,
    x_bud: BudUnit,
):
    road_str = "road"
    base_str = "base"
    need_str = "need"
    divisor_str = "divisor"
    nigh_str = "nigh"
    open_str = "open"
    for road_dict in item_reason_premiseunit_update_dict.values():
        for base_dict in road_dict.values():
            for item_reason_premiseunit_atom in base_dict.values():
                road_value = item_reason_premiseunit_atom.get_value(road_str)
                base_value = item_reason_premiseunit_atom.get_value(base_str)
                need_value = item_reason_premiseunit_atom.get_value(need_str)
                divisor_value = item_reason_premiseunit_atom.get_value(divisor_str)
                nigh_value = item_reason_premiseunit_atom.get_value(nigh_str)
                open_value = item_reason_premiseunit_atom.get_value(open_str)
                x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for item '{road_value}'."
                if open_value is not None:
                    x_str += f" Open={open_value}."
                if nigh_value is not None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value is not None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_bud_reason_premiseunit_delete_to_legible_list(
    legible_list: list[str],
    item_reason_premiseunit_delete_dict: dict,
    x_bud: BudUnit,
):
    road_str = "road"
    base_str = "base"
    need_str = "need"
    for road_dict in item_reason_premiseunit_delete_dict.values():
        for base_dict in road_dict.values():
            for item_reason_premiseunit_atom in base_dict.values():
                road_value = item_reason_premiseunit_atom.get_value(road_str)
                base_value = item_reason_premiseunit_atom.get_value(base_str)
                need_value = item_reason_premiseunit_atom.get_value(need_str)
                x_str = f"PremiseUnit '{need_value}' deleted from reason '{base_value}' for item '{road_value}'."
                legible_list.append(x_str)


def add_bud_item_teamlink_insert_to_legible_list(
    legible_list: list[str], item_teamlink_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in item_teamlink_insert_dict.values():
        for item_teamlink_atom in road_dict.values():
            team_tag_value = item_teamlink_atom.get_value(team_tag_str())
            road_value = item_teamlink_atom.get_value("road")
            x_str = f"teamlink '{team_tag_value}' created for item '{road_value}'."
            legible_list.append(x_str)


def add_bud_item_teamlink_delete_to_legible_list(
    legible_list: list[str], item_teamlink_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in item_teamlink_delete_dict.values():
        for item_teamlink_atom in road_dict.values():
            team_tag_value = item_teamlink_atom.get_value(team_tag_str())
            road_value = item_teamlink_atom.get_value("road")
            x_str = f"teamlink '{team_tag_value}' deleted for item '{road_value}'."
            legible_list.append(x_str)


def add_bud_item_healerlink_insert_to_legible_list(
    legible_list: list[str], item_healerlink_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in item_healerlink_insert_dict.values():
        for item_healerlink_atom in road_dict.values():
            healer_name_value = item_healerlink_atom.get_value(healer_name_str())
            road_value = item_healerlink_atom.get_value("road")
            x_str = f"HealerLink '{healer_name_value}' created for item '{road_value}'."
            legible_list.append(x_str)


def add_bud_item_healerlink_delete_to_legible_list(
    legible_list: list[str], item_healerlink_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in item_healerlink_delete_dict.values():
        for item_healerlink_atom in road_dict.values():
            healer_name_value = item_healerlink_atom.get_value(healer_name_str())
            road_value = item_healerlink_atom.get_value("road")
            x_str = f"HealerLink '{healer_name_value}' deleted for item '{road_value}'."
            legible_list.append(x_str)


def add_bud_item_factunit_insert_to_legible_list(
    legible_list: list[str], item_factunit_insert_dict: dict, x_bud: BudUnit
):
    road_str = "road"
    base_str = "base"
    pick_str = "pick"
    for road_dict in item_factunit_insert_dict.values():
        for item_factunit_atom in road_dict.values():
            road_value = item_factunit_atom.get_value(road_str)
            base_value = item_factunit_atom.get_value(base_str)
            pick_value = item_factunit_atom.get_value(pick_str)
            fnigh_value = item_factunit_atom.get_value(fnigh_str())
            fopen_value = item_factunit_atom.get_value(fopen_str())
            x_str = f"FactUnit '{pick_value}' created for base '{base_value}' for item '{road_value}'."
            if fopen_value is not None:
                x_str += f" fOpen={fopen_value}."
            if fnigh_value is not None:
                x_str += f" fNigh={fnigh_value}."
            legible_list.append(x_str)


def add_bud_item_factunit_update_to_legible_list(
    legible_list: list[str], item_factunit_update_dict: dict, x_bud: BudUnit
):
    road_str = "road"
    base_str = "base"
    pick_str = "pick"
    for road_dict in item_factunit_update_dict.values():
        for item_factunit_atom in road_dict.values():
            road_value = item_factunit_atom.get_value(road_str)
            base_value = item_factunit_atom.get_value(base_str)
            pick_value = item_factunit_atom.get_value(pick_str)
            fnigh_value = item_factunit_atom.get_value(fnigh_str())
            fopen_value = item_factunit_atom.get_value(fopen_str())
            x_str = f"FactUnit '{pick_value}' updated for base '{base_value}' for item '{road_value}'."
            if fopen_value is not None:
                x_str += f" fOpen={fopen_value}."
            if fnigh_value is not None:
                x_str += f" fNigh={fnigh_value}."
            legible_list.append(x_str)


def add_bud_item_factunit_delete_to_legible_list(
    legible_list: list[str], item_factunit_delete_dict: dict, x_bud: BudUnit
):
    road_str = "road"
    base_str = "base"
    pick_str = "pick"
    for road_dict in item_factunit_delete_dict.values():
        for item_factunit_atom in road_dict.values():
            road_value = item_factunit_atom.get_value(road_str)
            base_value = item_factunit_atom.get_value(base_str)
            pick_value = item_factunit_atom.get_value(pick_str)
            x_str = f"FactUnit base '{base_value}' deleted for item '{road_value}'."
            legible_list.append(x_str)
