from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a06_believer_logic.believer_main import BelieverUnit
from src.a08_believer_atom_logic.atom_main import BelieverAtom
from src.a09_pack_logic.delta import BelieverDelta


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_from_nested_dict(x_dict, x_keylist, if_missing_return_None=True)


def create_legible_list(x_delta: BelieverDelta, x_believer: BelieverUnit) -> list[str]:
    atoms_dict = x_delta.believeratoms
    believerunit_atom = get_leg_obj(atoms_dict, ["UPDATE", "believerunit"])

    partnerunit_insert_dict = get_leg_obj(
        atoms_dict, ["INSERT", "believer_partnerunit"]
    )
    partnerunit_update_dict = get_leg_obj(
        atoms_dict, ["UPDATE", "believer_partnerunit"]
    )
    partnerunit_delete_dict = get_leg_obj(
        atoms_dict, ["DELETE", "believer_partnerunit"]
    )

    x_list = ["INSERT", "believer_partner_membership"]
    partner_membership_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_partner_membership"]
    partner_membership_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_partner_membership"]
    partner_membership_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_planunit"]
    believer_planunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_planunit"]
    believer_planunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_planunit"]
    believer_planunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_awardunit"]
    believer_plan_awardunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_plan_awardunit"]
    believer_plan_awardunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_awardunit"]
    believer_plan_awardunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_reasonunit"]
    believer_plan_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_plan_reasonunit"]
    believer_plan_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_reasonunit"]
    believer_plan_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_reason_caseunit"]
    believer_plan_reason_caseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_plan_reason_caseunit"]
    believer_plan_reason_caseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_reason_caseunit"]
    believer_plan_reason_caseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_partyunit"]
    believer_plan_partyunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_partyunit"]
    believer_plan_partyunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_healerunit"]
    believer_plan_healerunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_healerunit"]
    believer_plan_healerunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_factunit"]
    believer_plan_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_plan_factunit"]
    believer_plan_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_factunit"]
    believer_plan_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    leg_list = []
    if believerunit_atom is not None:
        add_believerunit_legible_list(leg_list, believerunit_atom, x_believer)
    if partnerunit_insert_dict is not None:
        add_believer_partnerunit_insert_to_legible_list(
            leg_list, partnerunit_insert_dict, x_believer
        )
    if partnerunit_update_dict is not None:
        add_believer_partnerunit_update_to_legible_list(
            leg_list, partnerunit_update_dict, x_believer
        )
    if partnerunit_delete_dict is not None:
        add_believer_partnerunit_delete_to_legible_list(
            leg_list, partnerunit_delete_dict, x_believer
        )

    if partner_membership_insert_dict is not None:
        add_believer_partner_membership_insert_to_legible_list(
            leg_list, partner_membership_insert_dict, x_believer
        )
    if partner_membership_update_dict is not None:
        add_believer_partner_membership_update_to_legible_list(
            leg_list, partner_membership_update_dict, x_believer
        )
    if partner_membership_delete_dict is not None:
        add_believer_partner_membership_delete_to_legible_list(
            leg_list, partner_membership_delete_dict, x_believer
        )

    if believer_planunit_insert_dict is not None:
        add_believer_planunit_insert_to_legible_list(
            leg_list, believer_planunit_insert_dict, x_believer
        )
    if believer_planunit_update_dict is not None:
        add_believer_planunit_update_to_legible_list(
            leg_list, believer_planunit_update_dict, x_believer
        )
    if believer_planunit_delete_dict is not None:
        add_believer_planunit_delete_to_legible_list(
            leg_list, believer_planunit_delete_dict, x_believer
        )

    if believer_plan_awardunit_insert_dict is not None:
        add_believer_plan_awardunit_insert_to_legible_list(
            leg_list, believer_plan_awardunit_insert_dict, x_believer
        )
    if believer_plan_awardunit_update_dict is not None:
        add_believer_plan_awardunit_update_to_legible_list(
            leg_list, believer_plan_awardunit_update_dict, x_believer
        )
    if believer_plan_awardunit_delete_dict is not None:
        add_believer_plan_awardunit_delete_to_legible_list(
            leg_list, believer_plan_awardunit_delete_dict, x_believer
        )

    if believer_plan_reasonunit_insert_dict is not None:
        add_believer_plan_reasonunit_insert_to_legible_list(
            leg_list, believer_plan_reasonunit_insert_dict, x_believer
        )
    if believer_plan_reasonunit_update_dict is not None:
        add_believer_plan_reasonunit_update_to_legible_list(
            leg_list, believer_plan_reasonunit_update_dict, x_believer
        )
    if believer_plan_reasonunit_delete_dict is not None:
        add_believer_plan_reasonunit_delete_to_legible_list(
            leg_list, believer_plan_reasonunit_delete_dict, x_believer
        )

    if believer_plan_reason_caseunit_insert_dict is not None:
        add_believer_reason_caseunit_insert_to_legible_list(
            leg_list, believer_plan_reason_caseunit_insert_dict, x_believer
        )
    if believer_plan_reason_caseunit_update_dict is not None:
        add_believer_reason_caseunit_update_to_legible_list(
            leg_list, believer_plan_reason_caseunit_update_dict, x_believer
        )
    if believer_plan_reason_caseunit_delete_dict is not None:
        add_believer_reason_caseunit_delete_to_legible_list(
            leg_list, believer_plan_reason_caseunit_delete_dict, x_believer
        )

    if believer_plan_partyunit_insert_dict is not None:
        add_believer_plan_partyunit_insert_to_legible_list(
            leg_list, believer_plan_partyunit_insert_dict, x_believer
        )
    if believer_plan_partyunit_delete_dict is not None:
        add_believer_plan_partyunit_delete_to_legible_list(
            leg_list, believer_plan_partyunit_delete_dict, x_believer
        )

    if believer_plan_healerunit_insert_dict is not None:
        add_believer_plan_healerunit_insert_to_legible_list(
            leg_list, believer_plan_healerunit_insert_dict, x_believer
        )
    if believer_plan_healerunit_delete_dict is not None:
        add_believer_plan_healerunit_delete_to_legible_list(
            leg_list, believer_plan_healerunit_delete_dict, x_believer
        )

    if believer_plan_factunit_insert_dict is not None:
        add_believer_plan_factunit_insert_to_legible_list(
            leg_list, believer_plan_factunit_insert_dict, x_believer
        )
    if believer_plan_factunit_update_dict is not None:
        add_believer_plan_factunit_update_to_legible_list(
            leg_list, believer_plan_factunit_update_dict, x_believer
        )
    if believer_plan_factunit_delete_dict is not None:
        add_believer_plan_factunit_delete_to_legible_list(
            leg_list, believer_plan_factunit_delete_dict, x_believer
        )

    return leg_list


def add_believerunit_legible_list(
    legible_list: list[str], x_atom: BelieverAtom, x_believer: BelieverUnit
):
    jvalues = x_atom.jvalues
    _tally_str = "tally"
    _max_tree_traverse_str = "max_tree_traverse"
    _max_tree_traverse_value = jvalues.get(_max_tree_traverse_str)
    credor_respect_value = jvalues.get("credor_respect")
    debtor_respect_value = jvalues.get("debtor_respect")
    _tally_value = jvalues.get(_tally_str)

    if _max_tree_traverse_value is not None:
        x_str = f"{x_believer.believer_name}'s maximum number of Believer evaluations set to {_max_tree_traverse_value}"
        legible_list.append(x_str)
    if (
        credor_respect_value is not None
        and debtor_respect_value is not None
        and credor_respect_value == debtor_respect_value
    ):
        x_str = f"{x_believer.believer_name}'s total pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif credor_respect_value is not None:
        x_str = (
            f"{x_believer.believer_name}'s credor pool is now {credor_respect_value}"
        )
        legible_list.append(x_str)
    elif debtor_respect_value is not None:
        x_str = (
            f"{x_believer.believer_name}'s debtor pool is now {debtor_respect_value}"
        )
        legible_list.append(x_str)
    if _tally_value is not None:
        x_str = f"{x_believer.believer_name}'s believer tally set to {_tally_value}"
        legible_list.append(x_str)


def add_believer_partnerunit_insert_to_legible_list(
    legible_list: list[str], partnerunit_dict: BelieverAtom, x_believer: BelieverUnit
):
    for partnerunit_atom in partnerunit_dict.values():
        partner_name = partnerunit_atom.get_value("partner_name")
        partner_cred_points_value = partnerunit_atom.get_value("partner_cred_points")
        partner_debt_points_value = partnerunit_atom.get_value("partner_debt_points")
        x_str = f"{partner_name} was added with {partner_cred_points_value} score credit and {partner_debt_points_value} score debt"
        legible_list.append(x_str)


def add_believer_partnerunit_update_to_legible_list(
    legible_list: list[str], partnerunit_dict: BelieverAtom, x_believer: BelieverUnit
):
    for partnerunit_atom in partnerunit_dict.values():
        partner_name = partnerunit_atom.get_value("partner_name")
        partner_cred_points_value = partnerunit_atom.get_value("partner_cred_points")
        partner_debt_points_value = partnerunit_atom.get_value("partner_debt_points")
        if (
            partner_cred_points_value is not None
            and partner_debt_points_value is not None
        ):
            x_str = f"{partner_name} now has {partner_cred_points_value} score credit and {partner_debt_points_value} score debt."
        elif partner_cred_points_value is not None:
            x_str = f"{partner_name} now has {partner_cred_points_value} score credit."
        elif partner_debt_points_value is not None:
            x_str = f"{partner_name} now has {partner_debt_points_value} score debt."
        legible_list.append(x_str)


def add_believer_partnerunit_delete_to_legible_list(
    legible_list: list[str], partnerunit_dict: BelieverAtom, x_believer: BelieverUnit
):
    for partnerunit_atom in partnerunit_dict.values():
        partner_name = partnerunit_atom.get_value("partner_name")
        x_str = f"{partner_name} was removed from score partners."
        legible_list.append(x_str)


def add_believer_partner_membership_insert_to_legible_list(
    legible_list: list[str],
    partner_membership_insert_dict: dict,
    x_believer: BelieverUnit,
):
    for partner_membership_dict in partner_membership_insert_dict.values():
        for partner_membership_atom in partner_membership_dict.values():
            group_title = partner_membership_atom.get_value("group_title")
            partner_name = partner_membership_atom.get_value("partner_name")
            group_cred_points_value = partner_membership_atom.get_value(
                "group_cred_points"
            )
            group_debt_points_value = partner_membership_atom.get_value(
                "group_debt_points"
            )
            x_str = f"Group '{group_title}' has new membership {partner_name} with group_cred_points_value{group_cred_points_value} and group_debt_points_value={group_debt_points_value}."
            legible_list.append(x_str)


def add_believer_partner_membership_update_to_legible_list(
    legible_list: list[str],
    partner_membership_update_dict: dict,
    x_believer: BelieverUnit,
):
    for partner_membership_dict in partner_membership_update_dict.values():
        for partner_membership_atom in partner_membership_dict.values():
            group_title = partner_membership_atom.get_value("group_title")
            partner_name = partner_membership_atom.get_value("partner_name")
            group_cred_points_value = partner_membership_atom.get_value(
                "group_cred_points"
            )
            group_debt_points_value = partner_membership_atom.get_value(
                "group_debt_points"
            )
            if (
                group_cred_points_value is not None
                and group_debt_points_value is not None
            ):
                x_str = f"Group '{group_title}' membership {partner_name} has new group_cred_points_value{group_cred_points_value} and group_debt_points_value={group_debt_points_value}."
            elif group_cred_points_value is not None:
                x_str = f"Group '{group_title}' membership {partner_name} has new group_cred_points_value{group_cred_points_value}."
            elif group_debt_points_value is not None:
                x_str = f"Group '{group_title}' membership {partner_name} has new group_debt_points_value={group_debt_points_value}."
            legible_list.append(x_str)


def add_believer_partner_membership_delete_to_legible_list(
    legible_list: list[str],
    partner_membership_delete_dict: dict,
    x_believer: BelieverUnit,
):
    for partner_membership_dict in partner_membership_delete_dict.values():
        for partner_membership_atom in partner_membership_dict.values():
            group_title = partner_membership_atom.get_value("group_title")
            partner_name = partner_membership_atom.get_value("partner_name")
            x_str = f"Group '{group_title}' no longer has membership {partner_name}."
            legible_list.append(x_str)


def add_believer_planunit_insert_to_legible_list(
    legible_list: list[str], planunit_insert_dict: dict, x_believer: BelieverUnit
):
    _problem_bool_str = "problem_bool"
    for planunit_atom in planunit_insert_dict.values():
        rope_value = planunit_atom.get_value("plan_rope")
        _addin_value = planunit_atom.get_value("addin")
        _begin_value = planunit_atom.get_value("begin")
        _close_value = planunit_atom.get_value("close")
        _denom_value = planunit_atom.get_value("denom")
        _numor_value = planunit_atom.get_value("numor")
        _problem_bool_value = planunit_atom.get_value(_problem_bool_str)
        _morph_value = planunit_atom.get_value("morph")
        _star_value = planunit_atom.get_value("star")
        task_value = planunit_atom.get_value("task")
        x_str = f"Created Plan '{rope_value}'. "
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
        if _star_value is not None:
            x_str += f"star={_star_value}."
        if task_value is not None:
            x_str += f"task={task_value}."

        legible_list.append(x_str)


def add_believer_planunit_update_to_legible_list(
    legible_list: list[str], planunit_update_dict: dict, x_believer: BelieverUnit
):
    _problem_bool_str = "problem_bool"
    for planunit_atom in planunit_update_dict.values():
        rope_value = planunit_atom.get_value("plan_rope")
        addin_value = planunit_atom.get_value("addin")
        begin_value = planunit_atom.get_value("begin")
        close_value = planunit_atom.get_value("close")
        denom_value = planunit_atom.get_value("denom")
        numor_value = planunit_atom.get_value("numor")
        problem_bool_value = planunit_atom.get_value(_problem_bool_str)
        morph_value = planunit_atom.get_value("morph")
        star_value = planunit_atom.get_value("star")
        task_value = planunit_atom.get_value("task")
        x_str = f"Plan '{rope_value}' set these attributes: "
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
        if star_value is not None:
            x_str += f"star={star_value}."
        if task_value is not None:
            x_str += f"task={task_value}."

        legible_list.append(x_str)


def add_believer_planunit_delete_to_legible_list(
    legible_list: list[str], planunit_delete_dict: dict, x_believer: BelieverUnit
):
    for planunit_atom in planunit_delete_dict.values():
        rope_value = planunit_atom.get_value("plan_rope")
        x_str = f"Plan '{rope_value}' was deleted."
        legible_list.append(x_str)


def add_believer_plan_awardunit_insert_to_legible_list(
    legible_list: list[str], plan_awardunit_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_awardunit_insert_dict.values():
        for plan_awardunit_atom in rope_dict.values():
            awardee_title_value = plan_awardunit_atom.get_value("awardee_title")
            rope_value = plan_awardunit_atom.get_value("plan_rope")
            give_force_value = plan_awardunit_atom.get_value("give_force")
            take_force_value = plan_awardunit_atom.get_value("take_force")
            x_str = f"AwardUnit created for group {awardee_title_value} for plan '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
            legible_list.append(x_str)


def add_believer_plan_awardunit_update_to_legible_list(
    legible_list: list[str], plan_awardunit_update_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_awardunit_update_dict.values():
        for plan_awardunit_atom in rope_dict.values():
            awardee_title_value = plan_awardunit_atom.get_value("awardee_title")
            rope_value = plan_awardunit_atom.get_value("plan_rope")
            give_force_value = plan_awardunit_atom.get_value("give_force")
            take_force_value = plan_awardunit_atom.get_value("take_force")
            if give_force_value is not None and take_force_value is not None:
                x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
            elif give_force_value is not None:
                x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value}."
            elif take_force_value is not None:
                x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now take_force={take_force_value}."
            legible_list.append(x_str)


def add_believer_plan_awardunit_delete_to_legible_list(
    legible_list: list[str], plan_awardunit_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_awardunit_delete_dict.values():
        for plan_awardunit_atom in rope_dict.values():
            awardee_title_value = plan_awardunit_atom.get_value("awardee_title")
            rope_value = plan_awardunit_atom.get_value("plan_rope")
            x_str = f"AwardUnit for group {awardee_title_value}, plan '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_believer_plan_reasonunit_insert_to_legible_list(
    legible_list: list[str], plan_reasonunit_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_reasonunit_insert_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            reason_context_value = plan_reasonunit_atom.get_value("reason_context")
            reason_active_requisite_value = plan_reasonunit_atom.get_value(
                "reason_active_requisite"
            )
            x_str = f"ReasonUnit created for plan '{rope_value}' with reason_context '{reason_context_value}'."
            if reason_active_requisite_value is not None:
                x_str += f" reason_active_requisite={reason_active_requisite_value}."
            legible_list.append(x_str)


def add_believer_plan_reasonunit_update_to_legible_list(
    legible_list: list[str], plan_reasonunit_update_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_reasonunit_update_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            reason_context_value = plan_reasonunit_atom.get_value("reason_context")
            reason_active_requisite_value = plan_reasonunit_atom.get_value(
                "reason_active_requisite"
            )
            if reason_active_requisite_value is not None:
                x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' set with reason_active_requisite={reason_active_requisite_value}."
            else:
                x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' and no longer checks reason_context active mode."
            legible_list.append(x_str)


def add_believer_plan_reasonunit_delete_to_legible_list(
    legible_list: list[str], plan_reasonunit_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_reasonunit_delete_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            reason_context_value = plan_reasonunit_atom.get_value("reason_context")
            x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_believer_reason_caseunit_insert_to_legible_list(
    legible_list: list[str],
    plan_reason_caseunit_insert_dict: dict,
    x_believer: BelieverUnit,
):
    for rope_dict in plan_reason_caseunit_insert_dict.values():
        for reason_context_dict in rope_dict.values():
            for plan_reason_caseunit_atom in reason_context_dict.values():
                rope_value = plan_reason_caseunit_atom.get_value("plan_rope")
                reason_context_value = plan_reason_caseunit_atom.get_value(
                    "reason_context"
                )
                reason_state_value = plan_reason_caseunit_atom.get_value("reason_state")
                reason_divisor_value = plan_reason_caseunit_atom.get_value(
                    "reason_divisor"
                )
                reason_upper_value = plan_reason_caseunit_atom.get_value("reason_upper")
                reason_lower_value = plan_reason_caseunit_atom.get_value("reason_lower")
                x_str = f"CaseUnit '{reason_state_value}' created for reason '{reason_context_value}' for plan '{rope_value}'."
                if reason_lower_value is not None:
                    x_str += f" reason_lower={reason_lower_value}."
                if reason_upper_value is not None:
                    x_str += f" reason_upper={reason_upper_value}."
                if reason_divisor_value is not None:
                    x_str += f" reason_divisor={reason_divisor_value}."
                legible_list.append(x_str)


def add_believer_reason_caseunit_update_to_legible_list(
    legible_list: list[str],
    plan_reason_caseunit_update_dict: dict,
    x_believer: BelieverUnit,
):
    for rope_dict in plan_reason_caseunit_update_dict.values():
        for reason_context_dict in rope_dict.values():
            for plan_reason_caseunit_atom in reason_context_dict.values():
                rope_value = plan_reason_caseunit_atom.get_value("plan_rope")
                reason_context_value = plan_reason_caseunit_atom.get_value(
                    "reason_context"
                )
                reason_state_value = plan_reason_caseunit_atom.get_value("reason_state")
                reason_divisor_value = plan_reason_caseunit_atom.get_value(
                    "reason_divisor"
                )
                reason_upper_value = plan_reason_caseunit_atom.get_value("reason_upper")
                reason_lower_value = plan_reason_caseunit_atom.get_value("reason_lower")
                x_str = f"CaseUnit '{reason_state_value}' updated for reason '{reason_context_value}' for plan '{rope_value}'."
                if reason_lower_value is not None:
                    x_str += f" reason_lower={reason_lower_value}."
                if reason_upper_value is not None:
                    x_str += f" reason_upper={reason_upper_value}."
                if reason_divisor_value is not None:
                    x_str += f" reason_divisor={reason_divisor_value}."
                legible_list.append(x_str)


def add_believer_reason_caseunit_delete_to_legible_list(
    legible_list: list[str],
    plan_reason_caseunit_delete_dict: dict,
    x_believer: BelieverUnit,
):
    for rope_dict in plan_reason_caseunit_delete_dict.values():
        for reason_context_dict in rope_dict.values():
            for plan_reason_caseunit_atom in reason_context_dict.values():
                rope_value = plan_reason_caseunit_atom.get_value("plan_rope")
                reason_context_value = plan_reason_caseunit_atom.get_value(
                    "reason_context"
                )
                reason_state_value = plan_reason_caseunit_atom.get_value("reason_state")
                x_str = f"CaseUnit '{reason_state_value}' deleted from reason '{reason_context_value}' for plan '{rope_value}'."
                legible_list.append(x_str)


def add_believer_plan_partyunit_insert_to_legible_list(
    legible_list: list[str], plan_partyunit_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_partyunit_insert_dict.values():
        for plan_partyunit_atom in rope_dict.values():
            party_title_value = plan_partyunit_atom.get_value("party_title")
            rope_value = plan_partyunit_atom.get_value("plan_rope")
            x_str = f"partyunit '{party_title_value}' created for plan '{rope_value}'."
            legible_list.append(x_str)


def add_believer_plan_partyunit_delete_to_legible_list(
    legible_list: list[str], plan_partyunit_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_partyunit_delete_dict.values():
        for plan_partyunit_atom in rope_dict.values():
            party_title_value = plan_partyunit_atom.get_value("party_title")
            rope_value = plan_partyunit_atom.get_value("plan_rope")
            x_str = f"partyunit '{party_title_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)


def add_believer_plan_healerunit_insert_to_legible_list(
    legible_list: list[str], plan_healerunit_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_healerunit_insert_dict.values():
        for plan_healerunit_atom in rope_dict.values():
            healer_name_value = plan_healerunit_atom.get_value("healer_name")
            rope_value = plan_healerunit_atom.get_value("plan_rope")
            x_str = f"HealerUnit '{healer_name_value}' created for plan '{rope_value}'."
            legible_list.append(x_str)


def add_believer_plan_healerunit_delete_to_legible_list(
    legible_list: list[str], plan_healerunit_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_healerunit_delete_dict.values():
        for plan_healerunit_atom in rope_dict.values():
            healer_name_value = plan_healerunit_atom.get_value("healer_name")
            rope_value = plan_healerunit_atom.get_value("plan_rope")
            x_str = f"HealerUnit '{healer_name_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)


def add_believer_plan_factunit_insert_to_legible_list(
    legible_list: list[str], plan_factunit_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_factunit_insert_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fact_context_value = plan_factunit_atom.get_value("fact_context")
            fact_state_value = plan_factunit_atom.get_value("fact_state")
            fact_upper_value = plan_factunit_atom.get_value("fact_upper")
            fact_lower_value = plan_factunit_atom.get_value("fact_lower")
            x_str = f"FactUnit '{fact_state_value}' created for reason_context '{fact_context_value}' for plan '{rope_value}'."
            if fact_lower_value is not None:
                x_str += f" fact_lower={fact_lower_value}."
            if fact_upper_value is not None:
                x_str += f" fact_upper={fact_upper_value}."
            legible_list.append(x_str)


def add_believer_plan_factunit_update_to_legible_list(
    legible_list: list[str], plan_factunit_update_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_factunit_update_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fact_context_value = plan_factunit_atom.get_value("fact_context")
            fact_state_value = plan_factunit_atom.get_value("fact_state")
            fact_upper_value = plan_factunit_atom.get_value("fact_upper")
            fact_lower_value = plan_factunit_atom.get_value("fact_lower")
            x_str = f"FactUnit '{fact_state_value}' updated for reason_context '{fact_context_value}' for plan '{rope_value}'."
            if fact_lower_value is not None:
                x_str += f" fact_lower={fact_lower_value}."
            if fact_upper_value is not None:
                x_str += f" fact_upper={fact_upper_value}."
            legible_list.append(x_str)


def add_believer_plan_factunit_delete_to_legible_list(
    legible_list: list[str], plan_factunit_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_factunit_delete_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fact_context_value = plan_factunit_atom.get_value("fact_context")
            fact_state_value = plan_factunit_atom.get_value("fact_state")
            x_str = f"FactUnit reason_context '{fact_context_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)
