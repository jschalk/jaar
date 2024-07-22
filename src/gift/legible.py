from src._instrument.python import get_nested_value
from src.bud.bud import BudUnit
from src.gift.atom import atom_delete, atom_insert, atom_update, AtomUnit
from src.gift.change import ChangeUnit


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_nested_value(x_dict, x_keylist, if_missing_return_None=True)


def create_legible_list(x_change: ChangeUnit, x_bud: BudUnit) -> list[str]:
    atoms_dict = x_change.atomunits
    budunit_atom = get_leg_obj(atoms_dict, [atom_update(), "budunit"])

    acctunit_insert_dict = get_leg_obj(atoms_dict, [atom_insert(), "bud_acctunit"])
    acctunit_update_dict = get_leg_obj(atoms_dict, [atom_update(), "bud_acctunit"])
    acctunit_delete_dict = get_leg_obj(atoms_dict, [atom_delete(), "bud_acctunit"])

    x_list = [atom_insert(), "bud_acct_membership"]
    acct_membership_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "bud_acct_membership"]
    acct_membership_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "bud_acct_membership"]
    acct_membership_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "bud_ideaunit"]
    bud_ideaunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "bud_ideaunit"]
    bud_ideaunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "bud_ideaunit"]
    bud_ideaunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "bud_idea_awardlink"]
    bud_idea_awardlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "bud_idea_awardlink"]
    bud_idea_awardlink_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "bud_idea_awardlink"]
    bud_idea_awardlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "bud_idea_reasonunit"]
    bud_idea_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "bud_idea_reasonunit"]
    bud_idea_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "bud_idea_reasonunit"]
    bud_idea_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "bud_idea_reason_premiseunit"]
    bud_idea_reason_premiseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "bud_idea_reason_premiseunit"]
    bud_idea_reason_premiseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "bud_idea_reason_premiseunit"]
    bud_idea_reason_premiseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "bud_idea_grouphold"]
    bud_idea_grouphold_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "bud_idea_grouphold"]
    bud_idea_grouphold_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "bud_idea_healerhold"]
    bud_idea_healerhold_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "bud_idea_healerhold"]
    bud_idea_healerhold_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "bud_idea_factunit"]
    bud_idea_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "bud_idea_factunit"]
    bud_idea_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "bud_idea_factunit"]
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

    if bud_idea_grouphold_insert_dict is not None:
        add_bud_idea_grouphold_insert_to_legible_list(
            leg_list, bud_idea_grouphold_insert_dict, x_bud
        )
    if bud_idea_grouphold_delete_dict is not None:
        add_bud_idea_grouphold_delete_to_legible_list(
            leg_list, bud_idea_grouphold_delete_dict, x_bud
        )

    if bud_idea_healerhold_insert_dict is not None:
        add_bud_idea_healerhold_insert_to_legible_list(
            leg_list, bud_idea_healerhold_insert_dict, x_bud
        )
    if bud_idea_healerhold_delete_dict is not None:
        add_bud_idea_healerhold_delete_to_legible_list(
            leg_list, bud_idea_healerhold_delete_dict, x_bud
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
    _tally_text = "_tally"
    _max_tree_traverse_text = "_max_tree_traverse"
    _monetary_desc_text = "_monetary_desc"
    _credor_respect_text = "_credor_respect"
    _debtor_respect_text = "_debtor_respect"

    _max_tree_traverse_value = optional_args.get(_max_tree_traverse_text)
    _monetary_desc_value = optional_args.get(_monetary_desc_text)
    _credor_respect_value = optional_args.get(_credor_respect_text)
    _debtor_respect_value = optional_args.get(_debtor_respect_text)
    _tally_value = optional_args.get(_tally_text)

    x_monetary_desc = x_bud._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = f"{x_bud._owner_id}'s monetary_desc"

    if _max_tree_traverse_value is not None:
        legible_list.append(
            f"{x_bud._owner_id}'s maximum number of Bud output evaluations transited to {_max_tree_traverse_value}"
        )
    if _monetary_desc_value is not None:
        legible_list.append(
            f"{x_bud._owner_id}'s monetary_desc is now called '{_monetary_desc_value}'"
        )
    if (
        _credor_respect_value is not None
        and _debtor_respect_value is not None
        and _credor_respect_value == _debtor_respect_value
    ):
        legible_list.append(
            f"{x_monetary_desc} total pool is now {_credor_respect_value}"
        )
    elif _credor_respect_value is not None:
        legible_list.append(
            f"{x_monetary_desc} credor pool is now {_credor_respect_value}"
        )
    elif _debtor_respect_value is not None:
        legible_list.append(
            f"{x_monetary_desc} debtor pool is now {_debtor_respect_value}"
        )
    if _tally_value is not None:
        legible_list.append(
            f"{x_bud._owner_id}'s bud tally was transited to {_tally_value}"
        )


def add_bud_acctunit_insert_to_legible_list(
    legible_list: list[str], acctunit_dict: AtomUnit, x_bud: BudUnit
):
    x_monetary_desc = x_bud._monetary_desc
    x_monetary_desc = "monetary_desc" if x_monetary_desc is None else x_monetary_desc

    for acctunit_atom in acctunit_dict.values():
        acct_id = acctunit_atom.get_value("acct_id")
        credit_score_value = acctunit_atom.get_value("credit_score")
        debtit_score_value = acctunit_atom.get_value("debtit_score")
        x_str = f"{acct_id} was added with {credit_score_value} {x_monetary_desc} cred and {debtit_score_value} {x_monetary_desc} debt"
        legible_list.append(x_str)


def add_bud_acctunit_update_to_legible_list(
    legible_list: list[str], acctunit_dict: AtomUnit, x_bud: BudUnit
):
    x_monetary_desc = x_bud._monetary_desc
    x_monetary_desc = "monetary_desc" if x_monetary_desc is None else x_monetary_desc

    for acctunit_atom in acctunit_dict.values():
        acct_id = acctunit_atom.get_value("acct_id")
        credit_score_value = acctunit_atom.get_value("credit_score")
        debtit_score_value = acctunit_atom.get_value("debtit_score")
        if credit_score_value is not None and debtit_score_value is not None:
            x_str = f"{acct_id} now has {credit_score_value} {x_monetary_desc} cred and {debtit_score_value} {x_monetary_desc} debt."
        elif credit_score_value is not None and debtit_score_value is None:
            x_str = f"{acct_id} now has {credit_score_value} {x_monetary_desc} cred."
        elif credit_score_value is None and debtit_score_value is not None:
            x_str = f"{acct_id} now has {debtit_score_value} {x_monetary_desc} debt."
        legible_list.append(x_str)


def add_bud_acctunit_delete_to_legible_list(
    legible_list: list[str], acctunit_dict: AtomUnit, x_bud: BudUnit
):
    x_monetary_desc = x_bud._monetary_desc
    x_monetary_desc = "monetary_desc" if x_monetary_desc is None else x_monetary_desc
    for acctunit_atom in acctunit_dict.values():
        acct_id = acctunit_atom.get_value("acct_id")
        x_str = f"{acct_id} was removed from {x_monetary_desc} accts."
        legible_list.append(x_str)


def add_bud_acct_membership_insert_to_legible_list(
    legible_list: list[str], acct_membership_insert_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_insert_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_id = acct_membership_atom.get_value("group_id")
            acct_id = acct_membership_atom.get_value("acct_id")
            credit_weight_value = acct_membership_atom.get_value("credit_weight")
            debtit_weight_value = acct_membership_atom.get_value("debtit_weight")
            x_str = f"Group '{group_id}' has new membership {acct_id} with group_cred={credit_weight_value} and group_debt={debtit_weight_value}."
            legible_list.append(x_str)


def add_bud_acct_membership_update_to_legible_list(
    legible_list: list[str], acct_membership_update_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_update_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_id = acct_membership_atom.get_value("group_id")
            acct_id = acct_membership_atom.get_value("acct_id")
            credit_weight_value = acct_membership_atom.get_value("credit_weight")
            debtit_weight_value = acct_membership_atom.get_value("debtit_weight")
            if credit_weight_value is not None and debtit_weight_value is not None:
                x_str = f"Group '{group_id}' membership {acct_id} has new group_cred={credit_weight_value} and group_debt={debtit_weight_value}."
            elif credit_weight_value is not None and debtit_weight_value is None:
                x_str = f"Group '{group_id}' membership {acct_id} has new group_cred={credit_weight_value}."
            elif credit_weight_value is None and debtit_weight_value is not None:
                x_str = f"Group '{group_id}' membership {acct_id} has new group_debt={debtit_weight_value}."
            legible_list.append(x_str)


def add_bud_acct_membership_delete_to_legible_list(
    legible_list: list[str], acct_membership_delete_dict: dict, x_bud: BudUnit
):
    for acct_membership_dict in acct_membership_delete_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_id = acct_membership_atom.get_value("group_id")
            acct_id = acct_membership_atom.get_value("acct_id")
            x_str = f"Group '{group_id}' no longer has membership {acct_id}."
            legible_list.append(x_str)


def add_bud_ideaunit_insert_to_legible_list(
    legible_list: list[str], ideaunit_insert_dict: dict, x_bud: BudUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _mass_text = "_mass"
    pledge_text = "pledge"
    for parent_road_dict in ideaunit_insert_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_text)
            parent_road_value = ideaunit_atom.get_value(parent_road_text)
            _addin_value = ideaunit_atom.get_value(_addin_text)
            _begin_value = ideaunit_atom.get_value(_begin_text)
            _close_value = ideaunit_atom.get_value(_close_text)
            _denom_value = ideaunit_atom.get_value(_denom_text)
            _numeric_road_value = ideaunit_atom.get_value(_numeric_road_text)
            _numor_value = ideaunit_atom.get_value(_numor_text)
            _problem_bool_value = ideaunit_atom.get_value(_problem_bool_text)
            _range_source_road_value = ideaunit_atom.get_value(_range_source_road_text)
            _reest_value = ideaunit_atom.get_value(_reest_text)
            _mass_value = ideaunit_atom.get_value(_mass_text)
            pledge_value = ideaunit_atom.get_value(pledge_text)
            x_str = (
                f"Created Idea '{label_value}' with parent_road {parent_road_value}. "
            )
            if _addin_value is not None:
                x_str += f"_addin={_addin_value}."
            if _begin_value is not None:
                x_str += f"_begin={_begin_value}."
            if _close_value is not None:
                x_str += f"_close={_close_value}."
            if _denom_value is not None:
                x_str += f"_denom={_denom_value}."
            if _numeric_road_value is not None:
                x_str += f"_numeric_road={_numeric_road_value}."
            if _numor_value is not None:
                x_str += f"_numor={_numor_value}."
            if _problem_bool_value is not None:
                x_str += f"_problem_bool={_problem_bool_value}."
            if _range_source_road_value is not None:
                x_str += f"_range_source_road={_range_source_road_value}."
            if _reest_value is not None:
                x_str += f"_reest={_reest_value}."
            if _mass_value is not None:
                x_str += f"_mass={_mass_value}."
            if pledge_value is not None:
                x_str += f"pledge={pledge_value}."

            legible_list.append(x_str)


def add_bud_ideaunit_update_to_legible_list(
    legible_list: list[str], ideaunit_update_dict: dict, x_bud: BudUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _mass_text = "_mass"
    pledge_text = "pledge"
    for parent_road_dict in ideaunit_update_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_text)
            parent_road_value = ideaunit_atom.get_value(parent_road_text)
            _addin_value = ideaunit_atom.get_value(_addin_text)
            _begin_value = ideaunit_atom.get_value(_begin_text)
            _close_value = ideaunit_atom.get_value(_close_text)
            _denom_value = ideaunit_atom.get_value(_denom_text)
            _numeric_road_value = ideaunit_atom.get_value(_numeric_road_text)
            _numor_value = ideaunit_atom.get_value(_numor_text)
            _problem_bool_value = ideaunit_atom.get_value(_problem_bool_text)
            _range_source_road_value = ideaunit_atom.get_value(_range_source_road_text)
            _reest_value = ideaunit_atom.get_value(_reest_text)
            _mass_value = ideaunit_atom.get_value(_mass_text)
            pledge_value = ideaunit_atom.get_value(pledge_text)
            x_str = f"Idea '{label_value}' with parent_road {parent_road_value} transited these attributes: "
            if _addin_value is not None:
                x_str += f"_addin={_addin_value}."
            if _begin_value is not None:
                x_str += f"_begin={_begin_value}."
            if _close_value is not None:
                x_str += f"_close={_close_value}."
            if _denom_value is not None:
                x_str += f"_denom={_denom_value}."
            if _numeric_road_value is not None:
                x_str += f"_numeric_road={_numeric_road_value}."
            if _numor_value is not None:
                x_str += f"_numor={_numor_value}."
            if _problem_bool_value is not None:
                x_str += f"_problem_bool={_problem_bool_value}."
            if _range_source_road_value is not None:
                x_str += f"_range_source_road={_range_source_road_value}."
            if _reest_value is not None:
                x_str += f"_reest={_reest_value}."
            if _mass_value is not None:
                x_str += f"_mass={_mass_value}."
            if pledge_value is not None:
                x_str += f"pledge={pledge_value}."

            legible_list.append(x_str)


def add_bud_ideaunit_delete_to_legible_list(
    legible_list: list[str], ideaunit_delete_dict: dict, x_bud: BudUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    for parent_road_dict in ideaunit_delete_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_text)
            parent_road_value = ideaunit_atom.get_value(parent_road_text)
            x_str = f"Idea '{label_value}' with parent_road {parent_road_value} was deleted."
            legible_list.append(x_str)


def add_bud_idea_awardlink_insert_to_legible_list(
    legible_list: list[str], idea_awardlink_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_awardlink_insert_dict.values():
        for idea_awardlink_atom in road_dict.values():
            group_id_value = idea_awardlink_atom.get_value("group_id")
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
            group_id_value = idea_awardlink_atom.get_value("group_id")
            road_value = idea_awardlink_atom.get_value("road")
            give_force_value = idea_awardlink_atom.get_value("give_force")
            take_force_value = idea_awardlink_atom.get_value("take_force")
            if give_force_value is not None and take_force_value is not None:
                x_str = f"Awardlink has been transited for group {group_id_value} for idea '{road_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
            elif give_force_value is not None and take_force_value is None:
                x_str = f"Awardlink has been transited for group {group_id_value} for idea '{road_value}'. Now give_force={give_force_value}."
            elif give_force_value is None and take_force_value is not None:
                x_str = f"Awardlink has been transited for group {group_id_value} for idea '{road_value}'. Now take_force={take_force_value}."
            legible_list.append(x_str)


def add_bud_idea_awardlink_delete_to_legible_list(
    legible_list: list[str], idea_awardlink_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_awardlink_delete_dict.values():
        for idea_awardlink_atom in road_dict.values():
            group_id_value = idea_awardlink_atom.get_value("group_id")
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
                "base_idea_active_requisite"
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
                "base_idea_active_requisite"
            )
            if base_idea_active_requisite_value is not None:
                x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' transited with base_idea_active_requisite={base_idea_active_requisite_value}."
            elif base_idea_active_requisite_value is None:
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
    road_text = "road"
    base_text = "base"
    need_text = "need"
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_reason_premiseunit_insert_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_atom in base_dict.values():
                road_value = idea_reason_premiseunit_atom.get_value(road_text)
                base_value = idea_reason_premiseunit_atom.get_value(base_text)
                need_value = idea_reason_premiseunit_atom.get_value(need_text)
                divisor_value = idea_reason_premiseunit_atom.get_value(divisor_text)
                nigh_value = idea_reason_premiseunit_atom.get_value(nigh_text)
                open_value = idea_reason_premiseunit_atom.get_value(open_text)
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
    road_text = "road"
    base_text = "base"
    need_text = "need"
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_reason_premiseunit_update_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_atom in base_dict.values():
                road_value = idea_reason_premiseunit_atom.get_value(road_text)
                base_value = idea_reason_premiseunit_atom.get_value(base_text)
                need_value = idea_reason_premiseunit_atom.get_value(need_text)
                divisor_value = idea_reason_premiseunit_atom.get_value(divisor_text)
                nigh_value = idea_reason_premiseunit_atom.get_value(nigh_text)
                open_value = idea_reason_premiseunit_atom.get_value(open_text)
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
    road_text = "road"
    base_text = "base"
    need_text = "need"
    for road_dict in idea_reason_premiseunit_delete_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_atom in base_dict.values():
                road_value = idea_reason_premiseunit_atom.get_value(road_text)
                base_value = idea_reason_premiseunit_atom.get_value(base_text)
                need_value = idea_reason_premiseunit_atom.get_value(need_text)
                x_str = f"PremiseUnit '{need_value}' deleted from reason '{base_value}' for idea '{road_value}'."
                legible_list.append(x_str)


def add_bud_idea_grouphold_insert_to_legible_list(
    legible_list: list[str], idea_grouphold_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_grouphold_insert_dict.values():
        for idea_grouphold_atom in road_dict.values():
            group_id_value = idea_grouphold_atom.get_value("group_id")
            road_value = idea_grouphold_atom.get_value("road")
            x_str = f"grouphold '{group_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_bud_idea_grouphold_delete_to_legible_list(
    legible_list: list[str], idea_grouphold_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_grouphold_delete_dict.values():
        for idea_grouphold_atom in road_dict.values():
            group_id_value = idea_grouphold_atom.get_value("group_id")
            road_value = idea_grouphold_atom.get_value("road")
            x_str = f"grouphold '{group_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_bud_idea_healerhold_insert_to_legible_list(
    legible_list: list[str], idea_healerhold_insert_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_healerhold_insert_dict.values():
        for idea_healerhold_atom in road_dict.values():
            group_id_value = idea_healerhold_atom.get_value("group_id")
            road_value = idea_healerhold_atom.get_value("road")
            x_str = f"Healerhold '{group_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_bud_idea_healerhold_delete_to_legible_list(
    legible_list: list[str], idea_healerhold_delete_dict: dict, x_bud: BudUnit
):
    for road_dict in idea_healerhold_delete_dict.values():
        for idea_healerhold_atom in road_dict.values():
            group_id_value = idea_healerhold_atom.get_value("group_id")
            road_value = idea_healerhold_atom.get_value("road")
            x_str = f"Healerhold '{group_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_bud_idea_factunit_insert_to_legible_list(
    legible_list: list[str], idea_factunit_insert_dict: dict, x_bud: BudUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_factunit_insert_dict.values():
        for idea_factunit_atom in road_dict.values():
            road_value = idea_factunit_atom.get_value(road_text)
            base_value = idea_factunit_atom.get_value(base_text)
            pick_value = idea_factunit_atom.get_value(pick_text)
            nigh_value = idea_factunit_atom.get_value(nigh_text)
            open_value = idea_factunit_atom.get_value(open_text)
            x_str = f"FactUnit '{pick_value}' created for base '{base_value}' for idea '{road_value}'."
            if open_value is not None:
                x_str += f" Open={open_value}."
            if nigh_value is not None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_bud_idea_factunit_update_to_legible_list(
    legible_list: list[str], idea_factunit_update_dict: dict, x_bud: BudUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_factunit_update_dict.values():
        for idea_factunit_atom in road_dict.values():
            road_value = idea_factunit_atom.get_value(road_text)
            base_value = idea_factunit_atom.get_value(base_text)
            pick_value = idea_factunit_atom.get_value(pick_text)
            nigh_value = idea_factunit_atom.get_value(nigh_text)
            open_value = idea_factunit_atom.get_value(open_text)
            x_str = f"FactUnit '{pick_value}' updated for base '{base_value}' for idea '{road_value}'."
            if open_value is not None:
                x_str += f" Open={open_value}."
            if nigh_value is not None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_bud_idea_factunit_delete_to_legible_list(
    legible_list: list[str], idea_factunit_delete_dict: dict, x_bud: BudUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    for road_dict in idea_factunit_delete_dict.values():
        for idea_factunit_atom in road_dict.values():
            road_value = idea_factunit_atom.get_value(road_text)
            base_value = idea_factunit_atom.get_value(base_text)
            pick_value = idea_factunit_atom.get_value(pick_text)
            x_str = f"FactUnit '{pick_value}' deleted from base '{base_value}' for idea '{road_value}'."
            legible_list.append(x_str)
