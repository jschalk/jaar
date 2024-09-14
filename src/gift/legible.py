from src._instrument.python_tool import get_nested_value
from src.bud.bud import BudUnit
from src.bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
)
from src.gift.atom import AtomUnit
from src.gift.atom_config import (
    atom_delete,
    atom_insert,
    atom_update,
    acct_id_str,
    group_id_str,
    healer_id_str,
    parent_road_str,
    label_str,
    base_idea_active_requisite_str,
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
from src.gift.delta import DeltaUnit


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_nested_value(x_dict, x_keylist, if_missing_return_None=True)


def create_legible_list(x_delta: DeltaUnit, x_bud: BudUnit) -> list[str]:
    atoms_dict = x_delta.atomunits
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

    x_list = [atom_insert(), bud_ideaunit_str()]
    bud_ideaunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_ideaunit_str()]
    bud_ideaunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_ideaunit_str()]
    bud_ideaunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_idea_awardlink_str()]
    bud_idea_awardlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_idea_awardlink_str()]
    bud_idea_awardlink_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_idea_awardlink_str()]
    bud_idea_awardlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_idea_reasonunit_str()]
    bud_idea_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_idea_reasonunit_str()]
    bud_idea_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_idea_reasonunit_str()]
    bud_idea_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_idea_reason_premiseunit_str()]
    bud_idea_reason_premiseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_idea_reason_premiseunit_str()]
    bud_idea_reason_premiseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_idea_reason_premiseunit_str()]
    bud_idea_reason_premiseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_idea_teamlink_str()]
    bud_idea_teamlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_idea_teamlink_str()]
    bud_idea_teamlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_idea_healerlink_str()]
    bud_idea_healerlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_idea_healerlink_str()]
    bud_idea_healerlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_idea_factunit_str()]
    bud_idea_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_idea_factunit_str()]
    bud_idea_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_idea_factunit_str()]
    bud_idea_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

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

    if bud_ideaunit_insert_dict is not None:
        add_bud_ideaunit_insert_to_legible_list(
            leg_list, bud_ideaunit_insert_dict, x_bud
        )
    if bud_ideaunit_update_dict is not None:
        add_bud_ideaunit_update_to_legible_list(
            leg_list, bud_ideaunit_update_dict, x_bud
        )
    if bud_ideaunit_delete_dict is not None:
        add_bud_ideaunit_delete_to_legible_list(
            leg_list, bud_ideaunit_delete_dict, x_bud
        )

    if bud_idea_awardlink_insert_dict is not None:
        add_bud_idea_awardlink_insert_to_legible_list(
            leg_list, bud_idea_awardlink_insert_dict, x_bud
        )
    if bud_idea_awardlink_update_dict is not None:
        add_bud_idea_awardlink_update_to_legible_list(
            leg_list, bud_idea_awardlink_update_dict, x_bud
        )
    if bud_idea_awardlink_delete_dict is not None:
        add_bud_idea_awardlink_delete_to_legible_list(
            leg_list, bud_idea_awardlink_delete_dict, x_bud
        )

    if bud_idea_reasonunit_insert_dict is not None:
        add_bud_idea_reasonunit_insert_to_legible_list(
            leg_list, bud_idea_reasonunit_insert_dict, x_bud
        )
    if bud_idea_reasonunit_update_dict is not None:
        add_bud_idea_reasonunit_update_to_legible_list(
            leg_list, bud_idea_reasonunit_update_dict, x_bud
        )
    if bud_idea_reasonunit_delete_dict is not None:
        add_bud_idea_reasonunit_delete_to_legible_list(
            leg_list, bud_idea_reasonunit_delete_dict, x_bud
        )

    if bud_idea_reason_premiseunit_insert_dict is not None:
        add_bud_reason_premiseunit_insert_to_legible_list(
            leg_list, bud_idea_reason_premiseunit_insert_dict, x_bud
        )
    if bud_idea_reason_premiseunit_update_dict is not None:
        add_bud_reason_premiseunit_update_to_legible_list(
            leg_list, bud_idea_reason_premiseunit_update_dict, x_bud
        )
    if bud_idea_reason_premiseunit_delete_dict is not None:
        add_bud_reason_premiseunit_delete_to_legible_list(
            leg_list, bud_idea_reason_premiseunit_delete_dict, x_bud
        )

    if bud_idea_teamlink_insert_dict is not None:
        add_bud_idea_teamlink_insert_to_legible_list(
            leg_list, bud_idea_teamlink_insert_dict, x_bud
        )
    if bud_idea_teamlink_delete_dict is not None:
        add_bud_idea_teamlink_delete_to_legible_list(
            leg_list, bud_idea_teamlink_delete_dict, x_bud
        )

    if bud_idea_healerlink_insert_dict is not None:
        add_bud_idea_healerlink_insert_to_legible_list(
            leg_list, bud_idea_healerlink_insert_dict, x_bud
        )
    if bud_idea_healerlink_delete_dict is not None:
        add_bud_idea_healerlink_delete_to_legible_list(
            leg_list, bud_idea_healerlink_delete_dict, x_bud
        )

    if bud_idea_factunit_insert_dict is not None:
        add_bud_idea_factunit_insert_to_legible_list(
            leg_list, bud_idea_factunit_insert_dict, x_bud
        )
    if bud_idea_factunit_update_dict is not None:
        add_bud_idea_factunit_update_to_legible_list(
            leg_list, bud_idea_factunit_update_dict, x_bud
        )
    if bud_idea_factunit_delete_dict is not None:
        add_bud_idea_factunit_delete_to_legible_list(
            leg_list, bud_idea_factunit_delete_dict, x_bud
        )

    return leg_list


def add_budunit_legible_list(legible_list: list[str], x_atom: AtomUnit, x_bud: BudUnit):
    optional_args = x_atom.optional_args
    _tally_str = "tally"
    _max_tree_traverse_str = "max_tree_traverse"
    _monetary_desc_str = "monetary_desc"
    _max_tree_traverse_value = optional_args.get(_max_tree_traverse_str)
    _monetary_desc_value = optional_args.get(_monetary_desc_str)
    credor_respect_value = optional_args.get(credor_respect_str())
    debtor_respect_value = optional_args.get(debtor_respect_str())
    _tally_value = optional_args.get(_tally_str)

    x_monetary_desc = x_bud.monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = f"{x_bud._owner_id}'s monetary_desc"

    if _max_tree_traverse_value is not None:
        x_str = f"{x_bud._owner_id}'s maximum number of Bud evaluations transited to {_max_tree_traverse_value}"
        legible_list.append(x_str)
    if _monetary_desc_value is not None:
        x_str = (
            f"{x_bud._owner_id}'s monetary_desc is now called '{_monetary_desc_value}'"
        )
        legible_list.append(x_str)
    if (
        credor_respect_value is not None
        and debtor_respect_value is not None
        and credor_respect_value == debtor_respect_value
    ):
        x_str = f"{x_monetary_desc} total pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif credor_respect_value is not None:
        x_str = f"{x_monetary_desc} credor pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif debtor_respect_value is not None:
        x_str = f"{x_monetary_desc} debtor pool is now {debtor_respect_value}"
        legible_list.append(x_str)
    if _tally_value is not None:
        x_str = f"{x_bud._owner_id}'s bud tally was transited to {_tally_value}"
        legible_list.append(x_str)


def add_bud_acctunit_insert_to_legible_list(
    legible_list: list[str], acctunit_dict: AtomUnit, x_bud: BudUnit
):
    x_monetary_desc = x_bud.monetary_desc
    x_monetary_desc = "monetary_desc" if x_monetary_desc is None else x_monetary_desc

    for acctunit_atom in acctunit_dict.values():
        acct_id = acctunit_atom.get_value(acct_id_str())
        credit_belief_value = acctunit_atom.get_value("credit_belief")
        debtit_belief_value = acctunit_atom.get_value("debtit_belief")
        x_str = f"{acct_id} was added with {credit_belief_value} {x_monetary_desc} cred and {debtit_belief_value} {x_monetary_desc} debt"
        legible_list.append(x_str)


def add_bud_acctunit_update_to_legible_list(
    legible_list: list[str], acctunit_dict: AtomUnit, x_bud: BudUnit
):
    x_monetary_desc = x_bud.monetary_desc
    x_monetary_desc = "monetary_desc" if x_monetary_desc is None else x_monetary_desc

    for acctunit_atom in acctunit_dict.values():
        acct_id = acctunit_atom.get_value(acct_id_str())
        credit_belief_value = acctunit_atom.get_value("credit_belief")
        debtit_belief_value = acctunit_atom.get_value("debtit_belief")
        if credit_belief_value is not None and debtit_belief_value is not None:
            x_str = f"{acct_id} now has {credit_belief_value} {x_monetary_desc} cred and {debtit_belief_value} {x_monetary_desc} debt."
        elif credit_belief_value is not None:
            x_str = f"{acct_id} now has {credit_belief_value} {x_monetary_desc} cred."
        elif debtit_belief_value is not None:
            x_str = f"{acct_id} now has {debtit_belief_value} {x_monetary_desc} debt."
        legible_list.append(x_str)


def add_bud_acctunit_delete_to_legible_list(
    legible_list: list[str], acctunit_dict: AtomUnit, x_bud: BudUnit
):
    x_monetary_desc = x_bud.monetary_desc
    x_monetary_desc = "monetary_desc" if x_monetary_desc is None else x_monetary_desc
    for acctunit_atom in acctunit_dict.values():
        acct_id = acctunit_atom.get_value(acct_id_str())
        x_str = f"{acct_id} was removed from {x_monetary_desc} accts."
        legible_list.append(x_str)


def add_bud_acct_membership_insert_to_legible_list(
    legible_list: list[str], acct_membership_insert_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_insert_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_id = acct_membership_atom.get_value(group_id_str())
            acct_id = acct_membership_atom.get_value(acct_id_str())
            credit_vote_value = acct_membership_atom.get_value(credit_vote_str())
            debtit_vote_value = acct_membership_atom.get_value(debtit_vote_str())
            x_str = f"Group '{group_id}' has new membership {acct_id} with {credit_vote_str()}_value{credit_vote_value} and {debtit_vote_str()}_value={debtit_vote_value}."
            legible_list.append(x_str)


def add_bud_acct_membership_update_to_legible_list(
    legible_list: list[str], acct_membership_update_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_update_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_id = acct_membership_atom.get_value(group_id_str())
            acct_id = acct_membership_atom.get_value(acct_id_str())
            credit_vote_value = acct_membership_atom.get_value(credit_vote_str())
            debtit_vote_value = acct_membership_atom.get_value(debtit_vote_str())
            if credit_vote_value is not None and debtit_vote_value is not None:
                x_str = f"Group '{group_id}' membership {acct_id} has new {credit_vote_str()}_value{credit_vote_value} and {debtit_vote_str()}_value={debtit_vote_value}."
            elif credit_vote_value is not None:
                x_str = f"Group '{group_id}' membership {acct_id} has new {credit_vote_str()}_value{credit_vote_value}."
            elif debtit_vote_value is not None:
                x_str = f"Group '{group_id}' membership {acct_id} has new {debtit_vote_str()}_value={debtit_vote_value}."
            legible_list.append(x_str)


def add_bud_acct_membership_delete_to_legible_list(
    legible_list: list[str], acct_membership_delete_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_delete_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_id = acct_membership_atom.get_value(group_id_str())
            acct_id = acct_membership_atom.get_value(acct_id_str())
            x_str = f"Group '{group_id}' no longer has membership {acct_id}."
            legible_list.append(x_str)


def add_bud_ideaunit_insert_to_legible_list(
    legible_list: list[str], ideaunit_insert_dict: dict, x_bud: BudUnit
):
    _problem_bool_str = "problem_bool"
    _morph_str = "morph"
    _mass_str = "mass"
    for parent_road_dict in ideaunit_insert_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_str())
            parent_road_value = ideaunit_atom.get_value(parent_road_str())
            _addin_value = ideaunit_atom.get_value(addin_str())
            _begin_value = ideaunit_atom.get_value(begin_str())
            _close_value = ideaunit_atom.get_value(close_str())
            _denom_value = ideaunit_atom.get_value(denom_str())
            _numor_value = ideaunit_atom.get_value(numor_str())
            _problem_bool_value = ideaunit_atom.get_value(_problem_bool_str)
            _morph_value = ideaunit_atom.get_value(_morph_str)
            _mass_value = ideaunit_atom.get_value(_mass_str)
            pledge_value = ideaunit_atom.get_value(pledge_str())
            x_str = (
                f"Created Idea '{label_value}' with parent_road {parent_road_value}. "
            )
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


def add_bud_ideaunit_update_to_legible_list(
    legible_list: list[str], ideaunit_update_dict: dict, x_bud: BudUnit
):
    _problem_bool_str = "problem_bool"
    _mass_str = "mass"
    for parent_road_dict in ideaunit_update_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_str())
            parent_road_value = ideaunit_atom.get_value(parent_road_str())
            addin_value = ideaunit_atom.get_value(addin_str())
            begin_value = ideaunit_atom.get_value(begin_str())
            close_value = ideaunit_atom.get_value(close_str())
            denom_value = ideaunit_atom.get_value(denom_str())
            numor_value = ideaunit_atom.get_value(numor_str())
            problem_bool_value = ideaunit_atom.get_value(_problem_bool_str)
            morph_value = ideaunit_atom.get_value(morph_str())
            mass_value = ideaunit_atom.get_value(_mass_str)
            pledge_value = ideaunit_atom.get_value(pledge_str())
            x_str = f"Idea '{label_value}' with parent_road {parent_road_value} transited these attributes: "
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


def add_bud_ideaunit_delete_to_legible_list(
    legible_list: list[str], ideaunit_delete_dict: dict, x_bud: BudUnit
):
    for parent_road_dict in ideaunit_delete_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_str())
            parent_road_value = ideaunit_atom.get_value(parent_road_str())
            x_str = f"Idea '{label_value}' with parent_road {parent_road_value} was deleted."
            legible_list.append(x_str)


def add_bud_idea_awardlink_insert_to_legible_list(
    legible_list: list[str], idea_awardlink_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_awardlink_insert_dict.values():
        for idea_awardlink_atom in road_dict.values():
            group_id_value = idea_awardlink_atom.get_value(group_id_str())
            road_value = idea_awardlink_atom.get_value("road")
            give_force_value = idea_awardlink_atom.get_value("give_force")
            take_force_value = idea_awardlink_atom.get_value("take_force")
            x_str = f"Awardlink created for group {group_id_value} for idea '{road_value}' with give_force={give_force_value} and take_force={take_force_value}."
            legible_list.append(x_str)


def add_bud_idea_awardlink_update_to_legible_list(
    legible_list: list[str], idea_awardlink_update_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_awardlink_update_dict.values():
        for idea_awardlink_atom in road_dict.values():
            group_id_value = idea_awardlink_atom.get_value(group_id_str())
            road_value = idea_awardlink_atom.get_value("road")
            give_force_value = idea_awardlink_atom.get_value("give_force")
            take_force_value = idea_awardlink_atom.get_value("take_force")
            if give_force_value is not None and take_force_value is not None:
                x_str = f"Awardlink has been transited for group {group_id_value} for idea '{road_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
            elif give_force_value is not None:
                x_str = f"Awardlink has been transited for group {group_id_value} for idea '{road_value}'. Now give_force={give_force_value}."
            elif take_force_value is not None:
                x_str = f"Awardlink has been transited for group {group_id_value} for idea '{road_value}'. Now take_force={take_force_value}."
            legible_list.append(x_str)


def add_bud_idea_awardlink_delete_to_legible_list(
    legible_list: list[str], idea_awardlink_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_awardlink_delete_dict.values():
        for idea_awardlink_atom in road_dict.values():
            group_id_value = idea_awardlink_atom.get_value(group_id_str())
            road_value = idea_awardlink_atom.get_value("road")
            x_str = f"Awardlink for group {group_id_value}, idea '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_bud_idea_reasonunit_insert_to_legible_list(
    legible_list: list[str], idea_reasonunit_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_reasonunit_insert_dict.values():
        for idea_reasonunit_atom in road_dict.values():
            road_value = idea_reasonunit_atom.get_value("road")
            base_value = idea_reasonunit_atom.get_value("base")
            base_idea_active_requisite_value = idea_reasonunit_atom.get_value(
                base_idea_active_requisite_str()
            )
            x_str = (
                f"ReasonUnit created for idea '{road_value}' with base '{base_value}'."
            )
            if base_idea_active_requisite_value is not None:
                x_str += (
                    f" base_idea_active_requisite={base_idea_active_requisite_value}."
                )
            legible_list.append(x_str)


def add_bud_idea_reasonunit_update_to_legible_list(
    legible_list: list[str], idea_reasonunit_update_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_reasonunit_update_dict.values():
        for idea_reasonunit_atom in road_dict.values():
            road_value = idea_reasonunit_atom.get_value("road")
            base_value = idea_reasonunit_atom.get_value("base")
            base_idea_active_requisite_value = idea_reasonunit_atom.get_value(
                base_idea_active_requisite_str()
            )
            if base_idea_active_requisite_value is not None:
                x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' transited with base_idea_active_requisite={base_idea_active_requisite_value}."
            else:
                x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' and no longer checks base active mode."
            legible_list.append(x_str)


def add_bud_idea_reasonunit_delete_to_legible_list(
    legible_list: list[str], idea_reasonunit_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_reasonunit_delete_dict.values():
        for idea_reasonunit_atom in road_dict.values():
            road_value = idea_reasonunit_atom.get_value("road")
            base_value = idea_reasonunit_atom.get_value("base")
            x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_bud_reason_premiseunit_insert_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_insert_dict: dict,
    x_bud: BudUnit,
):
    road_str = "road"
    base_str = "base"
    need_str = "need"
    divisor_str = "divisor"
    nigh_str = "nigh"
    open_str = "open"
    for road_dict in idea_reason_premiseunit_insert_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_atom in base_dict.values():
                road_value = idea_reason_premiseunit_atom.get_value(road_str)
                base_value = idea_reason_premiseunit_atom.get_value(base_str)
                need_value = idea_reason_premiseunit_atom.get_value(need_str)
                divisor_value = idea_reason_premiseunit_atom.get_value(divisor_str)
                nigh_value = idea_reason_premiseunit_atom.get_value(nigh_str)
                open_value = idea_reason_premiseunit_atom.get_value(open_str)
                x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for idea '{road_value}'."
                if open_value is not None:
                    x_str += f" Open={open_value}."
                if nigh_value is not None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value is not None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_bud_reason_premiseunit_update_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_update_dict: dict,
    x_bud: BudUnit,
):
    road_str = "road"
    base_str = "base"
    need_str = "need"
    divisor_str = "divisor"
    nigh_str = "nigh"
    open_str = "open"
    for road_dict in idea_reason_premiseunit_update_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_atom in base_dict.values():
                road_value = idea_reason_premiseunit_atom.get_value(road_str)
                base_value = idea_reason_premiseunit_atom.get_value(base_str)
                need_value = idea_reason_premiseunit_atom.get_value(need_str)
                divisor_value = idea_reason_premiseunit_atom.get_value(divisor_str)
                nigh_value = idea_reason_premiseunit_atom.get_value(nigh_str)
                open_value = idea_reason_premiseunit_atom.get_value(open_str)
                x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for idea '{road_value}'."
                if open_value is not None:
                    x_str += f" Open={open_value}."
                if nigh_value is not None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value is not None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_bud_reason_premiseunit_delete_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_delete_dict: dict,
    x_bud: BudUnit,
):
    road_str = "road"
    base_str = "base"
    need_str = "need"
    for road_dict in idea_reason_premiseunit_delete_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_atom in base_dict.values():
                road_value = idea_reason_premiseunit_atom.get_value(road_str)
                base_value = idea_reason_premiseunit_atom.get_value(base_str)
                need_value = idea_reason_premiseunit_atom.get_value(need_str)
                x_str = f"PremiseUnit '{need_value}' deleted from reason '{base_value}' for idea '{road_value}'."
                legible_list.append(x_str)


def add_bud_idea_teamlink_insert_to_legible_list(
    legible_list: list[str], idea_teamlink_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_teamlink_insert_dict.values():
        for idea_teamlink_atom in road_dict.values():
            group_id_value = idea_teamlink_atom.get_value(group_id_str())
            road_value = idea_teamlink_atom.get_value("road")
            x_str = f"teamlink '{group_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_bud_idea_teamlink_delete_to_legible_list(
    legible_list: list[str], idea_teamlink_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_teamlink_delete_dict.values():
        for idea_teamlink_atom in road_dict.values():
            group_id_value = idea_teamlink_atom.get_value(group_id_str())
            road_value = idea_teamlink_atom.get_value("road")
            x_str = f"teamlink '{group_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_bud_idea_healerlink_insert_to_legible_list(
    legible_list: list[str], idea_healerlink_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_healerlink_insert_dict.values():
        for idea_healerlink_atom in road_dict.values():
            healer_id_value = idea_healerlink_atom.get_value(healer_id_str())
            road_value = idea_healerlink_atom.get_value("road")
            x_str = f"HealerLink '{healer_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_bud_idea_healerlink_delete_to_legible_list(
    legible_list: list[str], idea_healerlink_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_healerlink_delete_dict.values():
        for idea_healerlink_atom in road_dict.values():
            healer_id_value = idea_healerlink_atom.get_value(healer_id_str())
            road_value = idea_healerlink_atom.get_value("road")
            x_str = f"HealerLink '{healer_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_bud_idea_factunit_insert_to_legible_list(
    legible_list: list[str], idea_factunit_insert_dict: dict, x_bud: BudUnit
):
    road_str = "road"
    base_str = "base"
    pick_str = "pick"
    for road_dict in idea_factunit_insert_dict.values():
        for idea_factunit_atom in road_dict.values():
            road_value = idea_factunit_atom.get_value(road_str)
            base_value = idea_factunit_atom.get_value(base_str)
            pick_value = idea_factunit_atom.get_value(pick_str)
            fnigh_value = idea_factunit_atom.get_value(fnigh_str())
            fopen_value = idea_factunit_atom.get_value(fopen_str())
            x_str = f"FactUnit '{pick_value}' created for base '{base_value}' for idea '{road_value}'."
            if fopen_value is not None:
                x_str += f" fOpen={fopen_value}."
            if fnigh_value is not None:
                x_str += f" fNigh={fnigh_value}."
            legible_list.append(x_str)


def add_bud_idea_factunit_update_to_legible_list(
    legible_list: list[str], idea_factunit_update_dict: dict, x_bud: BudUnit
):
    road_str = "road"
    base_str = "base"
    pick_str = "pick"
    for road_dict in idea_factunit_update_dict.values():
        for idea_factunit_atom in road_dict.values():
            road_value = idea_factunit_atom.get_value(road_str)
            base_value = idea_factunit_atom.get_value(base_str)
            pick_value = idea_factunit_atom.get_value(pick_str)
            fnigh_value = idea_factunit_atom.get_value(fnigh_str())
            fopen_value = idea_factunit_atom.get_value(fopen_str())
            x_str = f"FactUnit '{pick_value}' updated for base '{base_value}' for idea '{road_value}'."
            if fopen_value is not None:
                x_str += f" fOpen={fopen_value}."
            if fnigh_value is not None:
                x_str += f" fNigh={fnigh_value}."
            legible_list.append(x_str)


def add_bud_idea_factunit_delete_to_legible_list(
    legible_list: list[str], idea_factunit_delete_dict: dict, x_bud: BudUnit
):
    road_str = "road"
    base_str = "base"
    pick_str = "pick"
    for road_dict in idea_factunit_delete_dict.values():
        for idea_factunit_atom in road_dict.values():
            road_value = idea_factunit_atom.get_value(road_str)
            base_value = idea_factunit_atom.get_value(base_str)
            pick_value = idea_factunit_atom.get_value(pick_str)
            x_str = f"FactUnit base '{base_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)
