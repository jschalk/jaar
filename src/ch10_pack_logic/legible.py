from src.ch01_data_toolbox.dict_toolbox import get_from_nested_dict
from src.ch07_belief_logic.belief_main import BeliefUnit
from src.ch09_belief_atom_logic.atom_main import BeliefAtom
from src.ch10_pack_logic.delta import BeliefDelta


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_from_nested_dict(x_dict, x_keylist, if_missing_return_None=True)


def create_legible_list(x_delta: BeliefDelta, x_belief: BeliefUnit) -> list[str]:
    atoms_dict = x_delta.beliefatoms
    beliefunit_atom = get_leg_obj(atoms_dict, ["UPDATE", "beliefunit"])

    voiceunit_insert_dict = get_leg_obj(atoms_dict, ["INSERT", "belief_voiceunit"])
    voiceunit_update_dict = get_leg_obj(atoms_dict, ["UPDATE", "belief_voiceunit"])
    voiceunit_delete_dict = get_leg_obj(atoms_dict, ["DELETE", "belief_voiceunit"])

    x_list = ["INSERT", "belief_voice_membership"]
    voice_membership_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "belief_voice_membership"]
    voice_membership_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "belief_voice_membership"]
    voice_membership_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "belief_planunit"]
    belief_planunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "belief_planunit"]
    belief_planunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "belief_planunit"]
    belief_planunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "belief_plan_awardunit"]
    belief_plan_awardunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "belief_plan_awardunit"]
    belief_plan_awardunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "belief_plan_awardunit"]
    belief_plan_awardunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "belief_plan_reasonunit"]
    belief_plan_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "belief_plan_reasonunit"]
    belief_plan_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "belief_plan_reasonunit"]
    belief_plan_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "belief_plan_reason_caseunit"]
    belief_plan_reason_caseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "belief_plan_reason_caseunit"]
    belief_plan_reason_caseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "belief_plan_reason_caseunit"]
    belief_plan_reason_caseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "belief_plan_partyunit"]
    belief_plan_partyunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "belief_plan_partyunit"]
    belief_plan_partyunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "belief_plan_healerunit"]
    belief_plan_healerunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "belief_plan_healerunit"]
    belief_plan_healerunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "belief_plan_factunit"]
    belief_plan_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "belief_plan_factunit"]
    belief_plan_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "belief_plan_factunit"]
    belief_plan_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    leg_list = []
    if beliefunit_atom is not None:
        add_beliefunit_legible_list(leg_list, beliefunit_atom, x_belief)
    if voiceunit_insert_dict is not None:
        add_belief_voiceunit_insert_to_legible_list(
            leg_list, voiceunit_insert_dict, x_belief
        )
    if voiceunit_update_dict is not None:
        add_belief_voiceunit_update_to_legible_list(
            leg_list, voiceunit_update_dict, x_belief
        )
    if voiceunit_delete_dict is not None:
        add_belief_voiceunit_delete_to_legible_list(
            leg_list, voiceunit_delete_dict, x_belief
        )

    if voice_membership_insert_dict is not None:
        add_belief_voice_membership_insert_to_legible_list(
            leg_list, voice_membership_insert_dict, x_belief
        )
    if voice_membership_update_dict is not None:
        add_belief_voice_membership_update_to_legible_list(
            leg_list, voice_membership_update_dict, x_belief
        )
    if voice_membership_delete_dict is not None:
        add_belief_voice_membership_delete_to_legible_list(
            leg_list, voice_membership_delete_dict, x_belief
        )

    if belief_planunit_insert_dict is not None:
        add_belief_planunit_insert_to_legible_list(
            leg_list, belief_planunit_insert_dict, x_belief
        )
    if belief_planunit_update_dict is not None:
        add_belief_planunit_update_to_legible_list(
            leg_list, belief_planunit_update_dict, x_belief
        )
    if belief_planunit_delete_dict is not None:
        add_belief_planunit_delete_to_legible_list(
            leg_list, belief_planunit_delete_dict, x_belief
        )

    if belief_plan_awardunit_insert_dict is not None:
        add_belief_plan_awardunit_insert_to_legible_list(
            leg_list, belief_plan_awardunit_insert_dict, x_belief
        )
    if belief_plan_awardunit_update_dict is not None:
        add_belief_plan_awardunit_update_to_legible_list(
            leg_list, belief_plan_awardunit_update_dict, x_belief
        )
    if belief_plan_awardunit_delete_dict is not None:
        add_belief_plan_awardunit_delete_to_legible_list(
            leg_list, belief_plan_awardunit_delete_dict, x_belief
        )

    if belief_plan_reasonunit_insert_dict is not None:
        add_belief_plan_reasonunit_insert_to_legible_list(
            leg_list, belief_plan_reasonunit_insert_dict, x_belief
        )
    if belief_plan_reasonunit_update_dict is not None:
        add_belief_plan_reasonunit_update_to_legible_list(
            leg_list, belief_plan_reasonunit_update_dict, x_belief
        )
    if belief_plan_reasonunit_delete_dict is not None:
        add_belief_plan_reasonunit_delete_to_legible_list(
            leg_list, belief_plan_reasonunit_delete_dict, x_belief
        )

    if belief_plan_reason_caseunit_insert_dict is not None:
        add_belief_reason_caseunit_insert_to_legible_list(
            leg_list, belief_plan_reason_caseunit_insert_dict, x_belief
        )
    if belief_plan_reason_caseunit_update_dict is not None:
        add_belief_reason_caseunit_update_to_legible_list(
            leg_list, belief_plan_reason_caseunit_update_dict, x_belief
        )
    if belief_plan_reason_caseunit_delete_dict is not None:
        add_belief_reason_caseunit_delete_to_legible_list(
            leg_list, belief_plan_reason_caseunit_delete_dict, x_belief
        )

    if belief_plan_partyunit_insert_dict is not None:
        add_belief_plan_partyunit_insert_to_legible_list(
            leg_list, belief_plan_partyunit_insert_dict, x_belief
        )
    if belief_plan_partyunit_delete_dict is not None:
        add_belief_plan_partyunit_delete_to_legible_list(
            leg_list, belief_plan_partyunit_delete_dict, x_belief
        )

    if belief_plan_healerunit_insert_dict is not None:
        add_belief_plan_healerunit_insert_to_legible_list(
            leg_list, belief_plan_healerunit_insert_dict, x_belief
        )
    if belief_plan_healerunit_delete_dict is not None:
        add_belief_plan_healerunit_delete_to_legible_list(
            leg_list, belief_plan_healerunit_delete_dict, x_belief
        )

    if belief_plan_factunit_insert_dict is not None:
        add_belief_plan_factunit_insert_to_legible_list(
            leg_list, belief_plan_factunit_insert_dict, x_belief
        )
    if belief_plan_factunit_update_dict is not None:
        add_belief_plan_factunit_update_to_legible_list(
            leg_list, belief_plan_factunit_update_dict, x_belief
        )
    if belief_plan_factunit_delete_dict is not None:
        add_belief_plan_factunit_delete_to_legible_list(
            leg_list, belief_plan_factunit_delete_dict, x_belief
        )

    return leg_list


def add_beliefunit_legible_list(
    legible_list: list[str], x_atom: BeliefAtom, x_belief: BeliefUnit
):
    jvalues = x_atom.jvalues
    _tally_str = "tally"
    _max_tree_traverse_str = "max_tree_traverse"
    _max_tree_traverse_value = jvalues.get(_max_tree_traverse_str)
    credor_respect_value = jvalues.get("credor_respect")
    debtor_respect_value = jvalues.get("debtor_respect")
    _tally_value = jvalues.get(_tally_str)

    if _max_tree_traverse_value is not None:
        x_str = f"{x_belief.belief_name}'s maximum number of Belief evaluations set to {_max_tree_traverse_value}"
        legible_list.append(x_str)
    if (
        credor_respect_value is not None
        and debtor_respect_value is not None
        and credor_respect_value == debtor_respect_value
    ):
        x_str = f"{x_belief.belief_name}'s total pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif credor_respect_value is not None:
        x_str = f"{x_belief.belief_name}'s credor pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif debtor_respect_value is not None:
        x_str = f"{x_belief.belief_name}'s debtor pool is now {debtor_respect_value}"
        legible_list.append(x_str)
    if _tally_value is not None:
        x_str = f"{x_belief.belief_name}'s belief tally set to {_tally_value}"
        legible_list.append(x_str)


def add_belief_voiceunit_insert_to_legible_list(
    legible_list: list[str], voiceunit_dict: BeliefAtom, x_belief: BeliefUnit
):
    for voiceunit_atom in voiceunit_dict.values():
        voice_name = voiceunit_atom.get_value("voice_name")
        voice_cred_shares_value = voiceunit_atom.get_value("voice_cred_shares")
        voice_debt_shares_value = voiceunit_atom.get_value("voice_debt_shares")
        x_str = f"{voice_name} was added with {voice_cred_shares_value} score credit and {voice_debt_shares_value} score debt"
        legible_list.append(x_str)


def add_belief_voiceunit_update_to_legible_list(
    legible_list: list[str], voiceunit_dict: BeliefAtom, x_belief: BeliefUnit
):
    for voiceunit_atom in voiceunit_dict.values():
        voice_name = voiceunit_atom.get_value("voice_name")
        voice_cred_shares_value = voiceunit_atom.get_value("voice_cred_shares")
        voice_debt_shares_value = voiceunit_atom.get_value("voice_debt_shares")
        if voice_cred_shares_value is not None and voice_debt_shares_value is not None:
            x_str = f"{voice_name} now has {voice_cred_shares_value} score credit and {voice_debt_shares_value} score debt."
        elif voice_cred_shares_value is not None:
            x_str = f"{voice_name} now has {voice_cred_shares_value} score credit."
        elif voice_debt_shares_value is not None:
            x_str = f"{voice_name} now has {voice_debt_shares_value} score debt."
        legible_list.append(x_str)


def add_belief_voiceunit_delete_to_legible_list(
    legible_list: list[str], voiceunit_dict: BeliefAtom, x_belief: BeliefUnit
):
    for voiceunit_atom in voiceunit_dict.values():
        voice_name = voiceunit_atom.get_value("voice_name")
        x_str = f"{voice_name} was removed from score voices."
        legible_list.append(x_str)


def add_belief_voice_membership_insert_to_legible_list(
    legible_list: list[str],
    voice_membership_insert_dict: dict,
    x_belief: BeliefUnit,
):
    for voice_membership_dict in voice_membership_insert_dict.values():
        for voice_membership_atom in voice_membership_dict.values():
            group_title = voice_membership_atom.get_value("group_title")
            voice_name = voice_membership_atom.get_value("voice_name")
            group_cred_shares_value = voice_membership_atom.get_value(
                "group_cred_shares"
            )
            group_debt_shares_value = voice_membership_atom.get_value(
                "group_debt_shares"
            )
            x_str = f"Group '{group_title}' has new membership {voice_name} with group_cred_shares_value{group_cred_shares_value} and group_debt_shares_value={group_debt_shares_value}."
            legible_list.append(x_str)


def add_belief_voice_membership_update_to_legible_list(
    legible_list: list[str],
    voice_membership_update_dict: dict,
    x_belief: BeliefUnit,
):
    for voice_membership_dict in voice_membership_update_dict.values():
        for voice_membership_atom in voice_membership_dict.values():
            group_title = voice_membership_atom.get_value("group_title")
            voice_name = voice_membership_atom.get_value("voice_name")
            group_cred_shares_value = voice_membership_atom.get_value(
                "group_cred_shares"
            )
            group_debt_shares_value = voice_membership_atom.get_value(
                "group_debt_shares"
            )
            if (
                group_cred_shares_value is not None
                and group_debt_shares_value is not None
            ):
                x_str = f"Group '{group_title}' membership {voice_name} has new group_cred_shares_value{group_cred_shares_value} and group_debt_shares_value={group_debt_shares_value}."
            elif group_cred_shares_value is not None:
                x_str = f"Group '{group_title}' membership {voice_name} has new group_cred_shares_value{group_cred_shares_value}."
            elif group_debt_shares_value is not None:
                x_str = f"Group '{group_title}' membership {voice_name} has new group_debt_shares_value={group_debt_shares_value}."
            legible_list.append(x_str)


def add_belief_voice_membership_delete_to_legible_list(
    legible_list: list[str],
    voice_membership_delete_dict: dict,
    x_belief: BeliefUnit,
):
    for voice_membership_dict in voice_membership_delete_dict.values():
        for voice_membership_atom in voice_membership_dict.values():
            group_title = voice_membership_atom.get_value("group_title")
            voice_name = voice_membership_atom.get_value("voice_name")
            x_str = f"Group '{group_title}' no longer has membership {voice_name}."
            legible_list.append(x_str)


def add_belief_planunit_insert_to_legible_list(
    legible_list: list[str], planunit_insert_dict: dict, x_belief: BeliefUnit
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
        pledge_value = planunit_atom.get_value("pledge")
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
        if pledge_value is not None:
            x_str += f"pledge={pledge_value}."

        legible_list.append(x_str)


def add_belief_planunit_update_to_legible_list(
    legible_list: list[str], planunit_update_dict: dict, x_belief: BeliefUnit
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
        pledge_value = planunit_atom.get_value("pledge")
        x_str = f"Plan '{rope_value}' set these attrs: "
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
        if pledge_value is not None:
            x_str += f"pledge={pledge_value}."

        legible_list.append(x_str)


def add_belief_planunit_delete_to_legible_list(
    legible_list: list[str], planunit_delete_dict: dict, x_belief: BeliefUnit
):
    for planunit_atom in planunit_delete_dict.values():
        rope_value = planunit_atom.get_value("plan_rope")
        x_str = f"Plan '{rope_value}' was deleted."
        legible_list.append(x_str)


def add_belief_plan_awardunit_insert_to_legible_list(
    legible_list: list[str], plan_awardunit_insert_dict: dict, x_belief: BeliefUnit
):
    for rope_dict in plan_awardunit_insert_dict.values():
        for plan_awardunit_atom in rope_dict.values():
            awardee_title_value = plan_awardunit_atom.get_value("awardee_title")
            rope_value = plan_awardunit_atom.get_value("plan_rope")
            give_force_value = plan_awardunit_atom.get_value("give_force")
            take_force_value = plan_awardunit_atom.get_value("take_force")
            x_str = f"AwardUnit created for group {awardee_title_value} for plan '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
            legible_list.append(x_str)


def add_belief_plan_awardunit_update_to_legible_list(
    legible_list: list[str], plan_awardunit_update_dict: dict, x_belief: BeliefUnit
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


def add_belief_plan_awardunit_delete_to_legible_list(
    legible_list: list[str], plan_awardunit_delete_dict: dict, x_belief: BeliefUnit
):
    for rope_dict in plan_awardunit_delete_dict.values():
        for plan_awardunit_atom in rope_dict.values():
            awardee_title_value = plan_awardunit_atom.get_value("awardee_title")
            rope_value = plan_awardunit_atom.get_value("plan_rope")
            x_str = f"AwardUnit for group {awardee_title_value}, plan '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_belief_plan_reasonunit_insert_to_legible_list(
    legible_list: list[str], plan_reasonunit_insert_dict: dict, x_belief: BeliefUnit
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


def add_belief_plan_reasonunit_update_to_legible_list(
    legible_list: list[str], plan_reasonunit_update_dict: dict, x_belief: BeliefUnit
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


def add_belief_plan_reasonunit_delete_to_legible_list(
    legible_list: list[str], plan_reasonunit_delete_dict: dict, x_belief: BeliefUnit
):
    for rope_dict in plan_reasonunit_delete_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            reason_context_value = plan_reasonunit_atom.get_value("reason_context")
            x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_belief_reason_caseunit_insert_to_legible_list(
    legible_list: list[str],
    plan_reason_caseunit_insert_dict: dict,
    x_belief: BeliefUnit,
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


def add_belief_reason_caseunit_update_to_legible_list(
    legible_list: list[str],
    plan_reason_caseunit_update_dict: dict,
    x_belief: BeliefUnit,
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


def add_belief_reason_caseunit_delete_to_legible_list(
    legible_list: list[str],
    plan_reason_caseunit_delete_dict: dict,
    x_belief: BeliefUnit,
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


def add_belief_plan_partyunit_insert_to_legible_list(
    legible_list: list[str], plan_partyunit_insert_dict: dict, x_belief: BeliefUnit
):
    for rope_dict in plan_partyunit_insert_dict.values():
        for plan_partyunit_atom in rope_dict.values():
            party_title_value = plan_partyunit_atom.get_value("party_title")
            rope_value = plan_partyunit_atom.get_value("plan_rope")
            x_str = f"partyunit '{party_title_value}' created for plan '{rope_value}'."
            legible_list.append(x_str)


def add_belief_plan_partyunit_delete_to_legible_list(
    legible_list: list[str], plan_partyunit_delete_dict: dict, x_belief: BeliefUnit
):
    for rope_dict in plan_partyunit_delete_dict.values():
        for plan_partyunit_atom in rope_dict.values():
            party_title_value = plan_partyunit_atom.get_value("party_title")
            rope_value = plan_partyunit_atom.get_value("plan_rope")
            x_str = f"partyunit '{party_title_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)


def add_belief_plan_healerunit_insert_to_legible_list(
    legible_list: list[str], plan_healerunit_insert_dict: dict, x_belief: BeliefUnit
):
    for rope_dict in plan_healerunit_insert_dict.values():
        for plan_healerunit_atom in rope_dict.values():
            healer_name_value = plan_healerunit_atom.get_value("healer_name")
            rope_value = plan_healerunit_atom.get_value("plan_rope")
            x_str = f"HealerUnit '{healer_name_value}' created for plan '{rope_value}'."
            legible_list.append(x_str)


def add_belief_plan_healerunit_delete_to_legible_list(
    legible_list: list[str], plan_healerunit_delete_dict: dict, x_belief: BeliefUnit
):
    for rope_dict in plan_healerunit_delete_dict.values():
        for plan_healerunit_atom in rope_dict.values():
            healer_name_value = plan_healerunit_atom.get_value("healer_name")
            rope_value = plan_healerunit_atom.get_value("plan_rope")
            x_str = f"HealerUnit '{healer_name_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)


def add_belief_plan_factunit_insert_to_legible_list(
    legible_list: list[str], plan_factunit_insert_dict: dict, x_belief: BeliefUnit
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


def add_belief_plan_factunit_update_to_legible_list(
    legible_list: list[str], plan_factunit_update_dict: dict, x_belief: BeliefUnit
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


def add_belief_plan_factunit_delete_to_legible_list(
    legible_list: list[str], plan_factunit_delete_dict: dict, x_belief: BeliefUnit
):
    for rope_dict in plan_factunit_delete_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fact_context_value = plan_factunit_atom.get_value("fact_context")
            fact_state_value = plan_factunit_atom.get_value("fact_state")
            x_str = f"FactUnit reason_context '{fact_context_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)
