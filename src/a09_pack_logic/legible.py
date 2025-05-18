from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a06_bud_logic.bud import BudUnit
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_conceptunit_str,
    bud_concept_awardlink_str,
    bud_concept_reasonunit_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_laborlink_str,
    bud_concept_healerlink_str,
    bud_concept_factunit_str,
)
from src.a08_bud_atom_logic.atom import BudAtom
from src.a06_bud_logic._utils.str_a06 import (
    acct_name_str,
    awardee_title_str,
    group_title_str,
    labor_title_str,
    healer_name_str,
    concept_way_str,
    rcontext_concept_active_requisite_str,
    pledge_str,
    addin_str,
    begin_str,
    close_str,
    credit_vote_str,
    credor_respect_str,
    debtit_vote_str,
    debtor_respect_str,
    denom_str,
    fcontext_str,
    fbranch_str,
    fnigh_str,
    fopen_str,
    mass_str,
    morph_str,
    numor_str,
    rcontext_str,
    pbranch_str,
    pnigh_str,
    popen_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import atom_delete, atom_insert, atom_update
from src.a09_pack_logic.delta import BudDelta


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

    x_list = [atom_insert(), bud_conceptunit_str()]
    bud_conceptunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_conceptunit_str()]
    bud_conceptunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_conceptunit_str()]
    bud_conceptunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_concept_awardlink_str()]
    bud_concept_awardlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_concept_awardlink_str()]
    bud_concept_awardlink_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_concept_awardlink_str()]
    bud_concept_awardlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_concept_reasonunit_str()]
    bud_concept_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_concept_reasonunit_str()]
    bud_concept_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_concept_reasonunit_str()]
    bud_concept_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_concept_reason_premiseunit_str()]
    bud_concept_reason_premiseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_concept_reason_premiseunit_str()]
    bud_concept_reason_premiseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_concept_reason_premiseunit_str()]
    bud_concept_reason_premiseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_concept_laborlink_str()]
    bud_concept_laborlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_concept_laborlink_str()]
    bud_concept_laborlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_concept_healerlink_str()]
    bud_concept_healerlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_concept_healerlink_str()]
    bud_concept_healerlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), bud_concept_factunit_str()]
    bud_concept_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), bud_concept_factunit_str()]
    bud_concept_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), bud_concept_factunit_str()]
    bud_concept_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

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

    if bud_conceptunit_insert_dict is not None:
        add_bud_conceptunit_insert_to_legible_list(
            leg_list, bud_conceptunit_insert_dict, x_bud
        )
    if bud_conceptunit_update_dict is not None:
        add_bud_conceptunit_update_to_legible_list(
            leg_list, bud_conceptunit_update_dict, x_bud
        )
    if bud_conceptunit_delete_dict is not None:
        add_bud_conceptunit_delete_to_legible_list(
            leg_list, bud_conceptunit_delete_dict, x_bud
        )

    if bud_concept_awardlink_insert_dict is not None:
        add_bud_concept_awardlink_insert_to_legible_list(
            leg_list, bud_concept_awardlink_insert_dict, x_bud
        )
    if bud_concept_awardlink_update_dict is not None:
        add_bud_concept_awardlink_update_to_legible_list(
            leg_list, bud_concept_awardlink_update_dict, x_bud
        )
    if bud_concept_awardlink_delete_dict is not None:
        add_bud_concept_awardlink_delete_to_legible_list(
            leg_list, bud_concept_awardlink_delete_dict, x_bud
        )

    if bud_concept_reasonunit_insert_dict is not None:
        add_bud_concept_reasonunit_insert_to_legible_list(
            leg_list, bud_concept_reasonunit_insert_dict, x_bud
        )
    if bud_concept_reasonunit_update_dict is not None:
        add_bud_concept_reasonunit_update_to_legible_list(
            leg_list, bud_concept_reasonunit_update_dict, x_bud
        )
    if bud_concept_reasonunit_delete_dict is not None:
        add_bud_concept_reasonunit_delete_to_legible_list(
            leg_list, bud_concept_reasonunit_delete_dict, x_bud
        )

    if bud_concept_reason_premiseunit_insert_dict is not None:
        add_bud_reason_premiseunit_insert_to_legible_list(
            leg_list, bud_concept_reason_premiseunit_insert_dict, x_bud
        )
    if bud_concept_reason_premiseunit_update_dict is not None:
        add_bud_reason_premiseunit_update_to_legible_list(
            leg_list, bud_concept_reason_premiseunit_update_dict, x_bud
        )
    if bud_concept_reason_premiseunit_delete_dict is not None:
        add_bud_reason_premiseunit_delete_to_legible_list(
            leg_list, bud_concept_reason_premiseunit_delete_dict, x_bud
        )

    if bud_concept_laborlink_insert_dict is not None:
        add_bud_concept_laborlink_insert_to_legible_list(
            leg_list, bud_concept_laborlink_insert_dict, x_bud
        )
    if bud_concept_laborlink_delete_dict is not None:
        add_bud_concept_laborlink_delete_to_legible_list(
            leg_list, bud_concept_laborlink_delete_dict, x_bud
        )

    if bud_concept_healerlink_insert_dict is not None:
        add_bud_concept_healerlink_insert_to_legible_list(
            leg_list, bud_concept_healerlink_insert_dict, x_bud
        )
    if bud_concept_healerlink_delete_dict is not None:
        add_bud_concept_healerlink_delete_to_legible_list(
            leg_list, bud_concept_healerlink_delete_dict, x_bud
        )

    if bud_concept_factunit_insert_dict is not None:
        add_bud_concept_factunit_insert_to_legible_list(
            leg_list, bud_concept_factunit_insert_dict, x_bud
        )
    if bud_concept_factunit_update_dict is not None:
        add_bud_concept_factunit_update_to_legible_list(
            leg_list, bud_concept_factunit_update_dict, x_bud
        )
    if bud_concept_factunit_delete_dict is not None:
        add_bud_concept_factunit_delete_to_legible_list(
            leg_list, bud_concept_factunit_delete_dict, x_bud
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
            group_title = acct_membership_atom.get_value(group_title_str())
            acct_name = acct_membership_atom.get_value(acct_name_str())
            credit_vote_value = acct_membership_atom.get_value(credit_vote_str())
            debtit_vote_value = acct_membership_atom.get_value(debtit_vote_str())
            x_str = f"Group '{group_title}' has new membership {acct_name} with {credit_vote_str()}_value{credit_vote_value} and {debtit_vote_str()}_value={debtit_vote_value}."
            legible_list.append(x_str)


def add_bud_acct_membership_update_to_legible_list(
    legible_list: list[str], acct_membership_update_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_update_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_title = acct_membership_atom.get_value(group_title_str())
            acct_name = acct_membership_atom.get_value(acct_name_str())
            credit_vote_value = acct_membership_atom.get_value(credit_vote_str())
            debtit_vote_value = acct_membership_atom.get_value(debtit_vote_str())
            if credit_vote_value is not None and debtit_vote_value is not None:
                x_str = f"Group '{group_title}' membership {acct_name} has new {credit_vote_str()}_value{credit_vote_value} and {debtit_vote_str()}_value={debtit_vote_value}."
            elif credit_vote_value is not None:
                x_str = f"Group '{group_title}' membership {acct_name} has new {credit_vote_str()}_value{credit_vote_value}."
            elif debtit_vote_value is not None:
                x_str = f"Group '{group_title}' membership {acct_name} has new {debtit_vote_str()}_value={debtit_vote_value}."
            legible_list.append(x_str)


def add_bud_acct_membership_delete_to_legible_list(
    legible_list: list[str], acct_membership_delete_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_delete_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_title = acct_membership_atom.get_value(group_title_str())
            acct_name = acct_membership_atom.get_value(acct_name_str())
            x_str = f"Group '{group_title}' no longer has membership {acct_name}."
            legible_list.append(x_str)


def add_bud_conceptunit_insert_to_legible_list(
    legible_list: list[str], conceptunit_insert_dict: dict, x_bud: BudUnit
):
    _problem_bool_str = "problem_bool"
    for conceptunit_atom in conceptunit_insert_dict.values():
        way_value = conceptunit_atom.get_value(concept_way_str())
        _addin_value = conceptunit_atom.get_value(addin_str())
        _begin_value = conceptunit_atom.get_value(begin_str())
        _close_value = conceptunit_atom.get_value(close_str())
        _denom_value = conceptunit_atom.get_value(denom_str())
        _numor_value = conceptunit_atom.get_value(numor_str())
        _problem_bool_value = conceptunit_atom.get_value(_problem_bool_str)
        _morph_value = conceptunit_atom.get_value(morph_str())
        _mass_value = conceptunit_atom.get_value(mass_str())
        pledge_value = conceptunit_atom.get_value(pledge_str())
        x_str = f"Created Concept '{way_value}'. "
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


def add_bud_conceptunit_update_to_legible_list(
    legible_list: list[str], conceptunit_update_dict: dict, x_bud: BudUnit
):
    _problem_bool_str = "problem_bool"
    for conceptunit_atom in conceptunit_update_dict.values():
        way_value = conceptunit_atom.get_value(concept_way_str())
        addin_value = conceptunit_atom.get_value(addin_str())
        begin_value = conceptunit_atom.get_value(begin_str())
        close_value = conceptunit_atom.get_value(close_str())
        denom_value = conceptunit_atom.get_value(denom_str())
        numor_value = conceptunit_atom.get_value(numor_str())
        problem_bool_value = conceptunit_atom.get_value(_problem_bool_str)
        morph_value = conceptunit_atom.get_value(morph_str())
        mass_value = conceptunit_atom.get_value(mass_str())
        pledge_value = conceptunit_atom.get_value(pledge_str())
        x_str = f"Concept '{way_value}' set these attributes: "
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


def add_bud_conceptunit_delete_to_legible_list(
    legible_list: list[str], conceptunit_delete_dict: dict, x_bud: BudUnit
):
    for conceptunit_atom in conceptunit_delete_dict.values():
        way_value = conceptunit_atom.get_value(concept_way_str())
        x_str = f"Concept '{way_value}' was deleted."
        legible_list.append(x_str)


def add_bud_concept_awardlink_insert_to_legible_list(
    legible_list: list[str], concept_awardlink_insert_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_awardlink_insert_dict.values():
        for concept_awardlink_atom in way_dict.values():
            awardee_title_value = concept_awardlink_atom.get_value(awardee_title_str())
            way_value = concept_awardlink_atom.get_value("concept_way")
            give_force_value = concept_awardlink_atom.get_value("give_force")
            take_force_value = concept_awardlink_atom.get_value("take_force")
            x_str = f"Awardlink created for group {awardee_title_value} for concept '{way_value}' with give_force={give_force_value} and take_force={take_force_value}."
            legible_list.append(x_str)


def add_bud_concept_awardlink_update_to_legible_list(
    legible_list: list[str], concept_awardlink_update_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_awardlink_update_dict.values():
        for concept_awardlink_atom in way_dict.values():
            awardee_title_value = concept_awardlink_atom.get_value(awardee_title_str())
            way_value = concept_awardlink_atom.get_value("concept_way")
            give_force_value = concept_awardlink_atom.get_value("give_force")
            take_force_value = concept_awardlink_atom.get_value("take_force")
            if give_force_value is not None and take_force_value is not None:
                x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{way_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
            elif give_force_value is not None:
                x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{way_value}'. Now give_force={give_force_value}."
            elif take_force_value is not None:
                x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{way_value}'. Now take_force={take_force_value}."
            legible_list.append(x_str)


def add_bud_concept_awardlink_delete_to_legible_list(
    legible_list: list[str], concept_awardlink_delete_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_awardlink_delete_dict.values():
        for concept_awardlink_atom in way_dict.values():
            awardee_title_value = concept_awardlink_atom.get_value(awardee_title_str())
            way_value = concept_awardlink_atom.get_value("concept_way")
            x_str = f"Awardlink for group {awardee_title_value}, concept '{way_value}' has been deleted."
            legible_list.append(x_str)


def add_bud_concept_reasonunit_insert_to_legible_list(
    legible_list: list[str], concept_reasonunit_insert_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_reasonunit_insert_dict.values():
        for concept_reasonunit_atom in way_dict.values():
            way_value = concept_reasonunit_atom.get_value("concept_way")
            rcontext_value = concept_reasonunit_atom.get_value("rcontext")
            rcontext_concept_active_requisite_value = concept_reasonunit_atom.get_value(
                rcontext_concept_active_requisite_str()
            )
            x_str = f"ReasonUnit created for concept '{way_value}' with rcontext '{rcontext_value}'."
            if rcontext_concept_active_requisite_value is not None:
                x_str += f" rcontext_concept_active_requisite={rcontext_concept_active_requisite_value}."
            legible_list.append(x_str)


def add_bud_concept_reasonunit_update_to_legible_list(
    legible_list: list[str], concept_reasonunit_update_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_reasonunit_update_dict.values():
        for concept_reasonunit_atom in way_dict.values():
            way_value = concept_reasonunit_atom.get_value("concept_way")
            rcontext_value = concept_reasonunit_atom.get_value("rcontext")
            rcontext_concept_active_requisite_value = concept_reasonunit_atom.get_value(
                rcontext_concept_active_requisite_str()
            )
            if rcontext_concept_active_requisite_value is not None:
                x_str = f"ReasonUnit rcontext='{rcontext_value}' for concept '{way_value}' set with rcontext_concept_active_requisite={rcontext_concept_active_requisite_value}."
            else:
                x_str = f"ReasonUnit rcontext='{rcontext_value}' for concept '{way_value}' and no longer checks rcontext active mode."
            legible_list.append(x_str)


def add_bud_concept_reasonunit_delete_to_legible_list(
    legible_list: list[str], concept_reasonunit_delete_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_reasonunit_delete_dict.values():
        for concept_reasonunit_atom in way_dict.values():
            way_value = concept_reasonunit_atom.get_value("concept_way")
            rcontext_value = concept_reasonunit_atom.get_value("rcontext")
            x_str = f"ReasonUnit rcontext='{rcontext_value}' for concept '{way_value}' has been deleted."
            legible_list.append(x_str)


def add_bud_reason_premiseunit_insert_to_legible_list(
    legible_list: list[str],
    concept_reason_premiseunit_insert_dict: dict,
    x_bud: BudUnit,
):
    for way_dict in concept_reason_premiseunit_insert_dict.values():
        for rcontext_dict in way_dict.values():
            for concept_reason_premiseunit_atom in rcontext_dict.values():
                way_value = concept_reason_premiseunit_atom.get_value(concept_way_str())
                rcontext_value = concept_reason_premiseunit_atom.get_value(
                    rcontext_str()
                )
                pbranch_value = concept_reason_premiseunit_atom.get_value(pbranch_str())
                pdivisor_value = concept_reason_premiseunit_atom.get_value("pdivisor")
                pnigh_value = concept_reason_premiseunit_atom.get_value(pnigh_str())
                popen_value = concept_reason_premiseunit_atom.get_value(popen_str())
                x_str = f"PremiseUnit '{pbranch_value}' created for reason '{rcontext_value}' for concept '{way_value}'."
                if popen_value is not None:
                    x_str += f" Popen={popen_value}."
                if pnigh_value is not None:
                    x_str += f" Pnigh={pnigh_value}."
                if pdivisor_value is not None:
                    x_str += f" Pdivisor={pdivisor_value}."
                legible_list.append(x_str)


def add_bud_reason_premiseunit_update_to_legible_list(
    legible_list: list[str],
    concept_reason_premiseunit_update_dict: dict,
    x_bud: BudUnit,
):
    for way_dict in concept_reason_premiseunit_update_dict.values():
        for rcontext_dict in way_dict.values():
            for concept_reason_premiseunit_atom in rcontext_dict.values():
                way_value = concept_reason_premiseunit_atom.get_value(concept_way_str())
                rcontext_value = concept_reason_premiseunit_atom.get_value(
                    rcontext_str()
                )
                pbranch_value = concept_reason_premiseunit_atom.get_value(pbranch_str())
                pdivisor_value = concept_reason_premiseunit_atom.get_value("pdivisor")
                pnigh_value = concept_reason_premiseunit_atom.get_value(pnigh_str())
                popen_value = concept_reason_premiseunit_atom.get_value(popen_str())
                x_str = f"PremiseUnit '{pbranch_value}' updated for reason '{rcontext_value}' for concept '{way_value}'."
                if popen_value is not None:
                    x_str += f" Popen={popen_value}."
                if pnigh_value is not None:
                    x_str += f" Pnigh={pnigh_value}."
                if pdivisor_value is not None:
                    x_str += f" Pdivisor={pdivisor_value}."
                legible_list.append(x_str)


def add_bud_reason_premiseunit_delete_to_legible_list(
    legible_list: list[str],
    concept_reason_premiseunit_delete_dict: dict,
    x_bud: BudUnit,
):
    for way_dict in concept_reason_premiseunit_delete_dict.values():
        for rcontext_dict in way_dict.values():
            for concept_reason_premiseunit_atom in rcontext_dict.values():
                way_value = concept_reason_premiseunit_atom.get_value(concept_way_str())
                rcontext_value = concept_reason_premiseunit_atom.get_value(
                    rcontext_str()
                )
                pbranch_value = concept_reason_premiseunit_atom.get_value(pbranch_str())
                x_str = f"PremiseUnit '{pbranch_value}' deleted from reason '{rcontext_value}' for concept '{way_value}'."
                legible_list.append(x_str)


def add_bud_concept_laborlink_insert_to_legible_list(
    legible_list: list[str], concept_laborlink_insert_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_laborlink_insert_dict.values():
        for concept_laborlink_atom in way_dict.values():
            labor_title_value = concept_laborlink_atom.get_value(labor_title_str())
            way_value = concept_laborlink_atom.get_value("concept_way")
            x_str = (
                f"laborlink '{labor_title_value}' created for concept '{way_value}'."
            )
            legible_list.append(x_str)


def add_bud_concept_laborlink_delete_to_legible_list(
    legible_list: list[str], concept_laborlink_delete_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_laborlink_delete_dict.values():
        for concept_laborlink_atom in way_dict.values():
            labor_title_value = concept_laborlink_atom.get_value(labor_title_str())
            way_value = concept_laborlink_atom.get_value("concept_way")
            x_str = (
                f"laborlink '{labor_title_value}' deleted for concept '{way_value}'."
            )
            legible_list.append(x_str)


def add_bud_concept_healerlink_insert_to_legible_list(
    legible_list: list[str], concept_healerlink_insert_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_healerlink_insert_dict.values():
        for concept_healerlink_atom in way_dict.values():
            healer_name_value = concept_healerlink_atom.get_value(healer_name_str())
            way_value = concept_healerlink_atom.get_value("concept_way")
            x_str = (
                f"HealerLink '{healer_name_value}' created for concept '{way_value}'."
            )
            legible_list.append(x_str)


def add_bud_concept_healerlink_delete_to_legible_list(
    legible_list: list[str], concept_healerlink_delete_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_healerlink_delete_dict.values():
        for concept_healerlink_atom in way_dict.values():
            healer_name_value = concept_healerlink_atom.get_value(healer_name_str())
            way_value = concept_healerlink_atom.get_value("concept_way")
            x_str = (
                f"HealerLink '{healer_name_value}' deleted for concept '{way_value}'."
            )
            legible_list.append(x_str)


def add_bud_concept_factunit_insert_to_legible_list(
    legible_list: list[str], concept_factunit_insert_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_factunit_insert_dict.values():
        for concept_factunit_atom in way_dict.values():
            way_value = concept_factunit_atom.get_value(concept_way_str())
            fcontext_value = concept_factunit_atom.get_value(fcontext_str())
            fbranch_value = concept_factunit_atom.get_value(fbranch_str())
            fnigh_value = concept_factunit_atom.get_value(fnigh_str())
            fopen_value = concept_factunit_atom.get_value(fopen_str())
            x_str = f"FactUnit '{fbranch_value}' created for rcontext '{fcontext_value}' for concept '{way_value}'."
            if fopen_value is not None:
                x_str += f" fopen={fopen_value}."
            if fnigh_value is not None:
                x_str += f" fnigh={fnigh_value}."
            legible_list.append(x_str)


def add_bud_concept_factunit_update_to_legible_list(
    legible_list: list[str], concept_factunit_update_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_factunit_update_dict.values():
        for concept_factunit_atom in way_dict.values():
            way_value = concept_factunit_atom.get_value(concept_way_str())
            fcontext_value = concept_factunit_atom.get_value(fcontext_str())
            fbranch_value = concept_factunit_atom.get_value(fbranch_str())
            fnigh_value = concept_factunit_atom.get_value(fnigh_str())
            fopen_value = concept_factunit_atom.get_value(fopen_str())
            x_str = f"FactUnit '{fbranch_value}' updated for rcontext '{fcontext_value}' for concept '{way_value}'."
            if fopen_value is not None:
                x_str += f" fopen={fopen_value}."
            if fnigh_value is not None:
                x_str += f" fnigh={fnigh_value}."
            legible_list.append(x_str)


def add_bud_concept_factunit_delete_to_legible_list(
    legible_list: list[str], concept_factunit_delete_dict: dict, x_bud: BudUnit
):
    for way_dict in concept_factunit_delete_dict.values():
        for concept_factunit_atom in way_dict.values():
            way_value = concept_factunit_atom.get_value(concept_way_str())
            fcontext_value = concept_factunit_atom.get_value(fcontext_str())
            fbranch_value = concept_factunit_atom.get_value(fbranch_str())
            x_str = f"FactUnit rcontext '{fcontext_value}' deleted for concept '{way_value}'."
            legible_list.append(x_str)
