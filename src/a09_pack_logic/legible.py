from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a06_believer_logic.believer import BelieverUnit
from src.a08_believer_atom_logic.atom import BelieverAtom
from src.a09_pack_logic.delta import BelieverDelta


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_from_nested_dict(x_dict, x_keylist, if_missing_return_None=True)


def create_legible_list(x_delta: BelieverDelta, x_believer: BelieverUnit) -> list[str]:
    atoms_dict = x_delta.believeratoms
    believerunit_atom = get_leg_obj(atoms_dict, ["UPDATE", "believerunit"])

    acctunit_insert_dict = get_leg_obj(atoms_dict, ["INSERT", "believer_acctunit"])
    acctunit_update_dict = get_leg_obj(atoms_dict, ["UPDATE", "believer_acctunit"])
    acctunit_delete_dict = get_leg_obj(atoms_dict, ["DELETE", "believer_acctunit"])

    x_list = ["INSERT", "believer_acct_membership"]
    acct_membership_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_acct_membership"]
    acct_membership_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_acct_membership"]
    acct_membership_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_planunit"]
    believer_planunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_planunit"]
    believer_planunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_planunit"]
    believer_planunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_awardlink"]
    believer_plan_awardlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_plan_awardlink"]
    believer_plan_awardlink_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_awardlink"]
    believer_plan_awardlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_reasonunit"]
    believer_plan_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_plan_reasonunit"]
    believer_plan_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_reasonunit"]
    believer_plan_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_reason_premiseunit"]
    believer_plan_reason_premiseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_plan_reason_premiseunit"]
    believer_plan_reason_premiseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_reason_premiseunit"]
    believer_plan_reason_premiseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_laborlink"]
    believer_plan_laborlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_laborlink"]
    believer_plan_laborlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_healerlink"]
    believer_plan_healerlink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_healerlink"]
    believer_plan_healerlink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "believer_plan_factunit"]
    believer_plan_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "believer_plan_factunit"]
    believer_plan_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "believer_plan_factunit"]
    believer_plan_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    leg_list = []
    if believerunit_atom is not None:
        add_believerunit_legible_list(leg_list, believerunit_atom, x_believer)
    if acctunit_insert_dict is not None:
        add_believer_acctunit_insert_to_legible_list(
            leg_list, acctunit_insert_dict, x_believer
        )
    if acctunit_update_dict is not None:
        add_believer_acctunit_update_to_legible_list(
            leg_list, acctunit_update_dict, x_believer
        )
    if acctunit_delete_dict is not None:
        add_believer_acctunit_delete_to_legible_list(
            leg_list, acctunit_delete_dict, x_believer
        )

    if acct_membership_insert_dict is not None:
        add_believer_acct_membership_insert_to_legible_list(
            leg_list, acct_membership_insert_dict, x_believer
        )
    if acct_membership_update_dict is not None:
        add_believer_acct_membership_update_to_legible_list(
            leg_list, acct_membership_update_dict, x_believer
        )
    if acct_membership_delete_dict is not None:
        add_believer_acct_membership_delete_to_legible_list(
            leg_list, acct_membership_delete_dict, x_believer
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

    if believer_plan_awardlink_insert_dict is not None:
        add_believer_plan_awardlink_insert_to_legible_list(
            leg_list, believer_plan_awardlink_insert_dict, x_believer
        )
    if believer_plan_awardlink_update_dict is not None:
        add_believer_plan_awardlink_update_to_legible_list(
            leg_list, believer_plan_awardlink_update_dict, x_believer
        )
    if believer_plan_awardlink_delete_dict is not None:
        add_believer_plan_awardlink_delete_to_legible_list(
            leg_list, believer_plan_awardlink_delete_dict, x_believer
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

    if believer_plan_reason_premiseunit_insert_dict is not None:
        add_believer_reason_premiseunit_insert_to_legible_list(
            leg_list, believer_plan_reason_premiseunit_insert_dict, x_believer
        )
    if believer_plan_reason_premiseunit_update_dict is not None:
        add_believer_reason_premiseunit_update_to_legible_list(
            leg_list, believer_plan_reason_premiseunit_update_dict, x_believer
        )
    if believer_plan_reason_premiseunit_delete_dict is not None:
        add_believer_reason_premiseunit_delete_to_legible_list(
            leg_list, believer_plan_reason_premiseunit_delete_dict, x_believer
        )

    if believer_plan_laborlink_insert_dict is not None:
        add_believer_plan_laborlink_insert_to_legible_list(
            leg_list, believer_plan_laborlink_insert_dict, x_believer
        )
    if believer_plan_laborlink_delete_dict is not None:
        add_believer_plan_laborlink_delete_to_legible_list(
            leg_list, believer_plan_laborlink_delete_dict, x_believer
        )

    if believer_plan_healerlink_insert_dict is not None:
        add_believer_plan_healerlink_insert_to_legible_list(
            leg_list, believer_plan_healerlink_insert_dict, x_believer
        )
    if believer_plan_healerlink_delete_dict is not None:
        add_believer_plan_healerlink_delete_to_legible_list(
            leg_list, believer_plan_healerlink_delete_dict, x_believer
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


def add_believer_acctunit_insert_to_legible_list(
    legible_list: list[str], acctunit_dict: BelieverAtom, x_believer: BelieverUnit
):
    for acctunit_atom in acctunit_dict.values():
        acct_name = acctunit_atom.get_value("acct_name")
        acct_cred_points_value = acctunit_atom.get_value("acct_cred_points")
        acct_debt_points_value = acctunit_atom.get_value("acct_debt_points")
        x_str = f"{acct_name} was added with {acct_cred_points_value} score credit and {acct_debt_points_value} score debt"
        legible_list.append(x_str)


def add_believer_acctunit_update_to_legible_list(
    legible_list: list[str], acctunit_dict: BelieverAtom, x_believer: BelieverUnit
):
    for acctunit_atom in acctunit_dict.values():
        acct_name = acctunit_atom.get_value("acct_name")
        acct_cred_points_value = acctunit_atom.get_value("acct_cred_points")
        acct_debt_points_value = acctunit_atom.get_value("acct_debt_points")
        if acct_cred_points_value is not None and acct_debt_points_value is not None:
            x_str = f"{acct_name} now has {acct_cred_points_value} score credit and {acct_debt_points_value} score debt."
        elif acct_cred_points_value is not None:
            x_str = f"{acct_name} now has {acct_cred_points_value} score credit."
        elif acct_debt_points_value is not None:
            x_str = f"{acct_name} now has {acct_debt_points_value} score debt."
        legible_list.append(x_str)


def add_believer_acctunit_delete_to_legible_list(
    legible_list: list[str], acctunit_dict: BelieverAtom, x_believer: BelieverUnit
):
    for acctunit_atom in acctunit_dict.values():
        acct_name = acctunit_atom.get_value("acct_name")
        x_str = f"{acct_name} was removed from score accts."
        legible_list.append(x_str)


def add_believer_acct_membership_insert_to_legible_list(
    legible_list: list[str], acct_membership_insert_dict: dict, x_believer: BelieverUnit
):
    for acct_membership_dict in acct_membership_insert_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_title = acct_membership_atom.get_value("group_title")
            acct_name = acct_membership_atom.get_value("acct_name")
            group_cred_points_value = acct_membership_atom.get_value(
                "group_cred_points"
            )
            group_debt_points_value = acct_membership_atom.get_value(
                "group_debt_points"
            )
            x_str = f"Group '{group_title}' has new membership {acct_name} with group_cred_points_value{group_cred_points_value} and group_debt_points_value={group_debt_points_value}."
            legible_list.append(x_str)


def add_believer_acct_membership_update_to_legible_list(
    legible_list: list[str], acct_membership_update_dict: dict, x_believer: BelieverUnit
):
    for acct_membership_dict in acct_membership_update_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_title = acct_membership_atom.get_value("group_title")
            acct_name = acct_membership_atom.get_value("acct_name")
            group_cred_points_value = acct_membership_atom.get_value(
                "group_cred_points"
            )
            group_debt_points_value = acct_membership_atom.get_value(
                "group_debt_points"
            )
            if (
                group_cred_points_value is not None
                and group_debt_points_value is not None
            ):
                x_str = f"Group '{group_title}' membership {acct_name} has new group_cred_points_value{group_cred_points_value} and group_debt_points_value={group_debt_points_value}."
            elif group_cred_points_value is not None:
                x_str = f"Group '{group_title}' membership {acct_name} has new group_cred_points_value{group_cred_points_value}."
            elif group_debt_points_value is not None:
                x_str = f"Group '{group_title}' membership {acct_name} has new group_debt_points_value={group_debt_points_value}."
            legible_list.append(x_str)


def add_believer_acct_membership_delete_to_legible_list(
    legible_list: list[str], acct_membership_delete_dict: dict, x_believer: BelieverUnit
):
    for acct_membership_dict in acct_membership_delete_dict.values():
        for acct_membership_atom in acct_membership_dict.values():
            group_title = acct_membership_atom.get_value("group_title")
            acct_name = acct_membership_atom.get_value("acct_name")
            x_str = f"Group '{group_title}' no longer has membership {acct_name}."
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
        _mass_value = planunit_atom.get_value("mass")
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
        if _mass_value is not None:
            x_str += f"mass={_mass_value}."
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
        mass_value = planunit_atom.get_value("mass")
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
        if mass_value is not None:
            x_str += f"mass={mass_value}."
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


def add_believer_plan_awardlink_insert_to_legible_list(
    legible_list: list[str], plan_awardlink_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_awardlink_insert_dict.values():
        for plan_awardlink_atom in rope_dict.values():
            awardee_title_value = plan_awardlink_atom.get_value("awardee_title")
            rope_value = plan_awardlink_atom.get_value("plan_rope")
            give_force_value = plan_awardlink_atom.get_value("give_force")
            take_force_value = plan_awardlink_atom.get_value("take_force")
            x_str = f"Awardlink created for group {awardee_title_value} for plan '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
            legible_list.append(x_str)


def add_believer_plan_awardlink_update_to_legible_list(
    legible_list: list[str], plan_awardlink_update_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_awardlink_update_dict.values():
        for plan_awardlink_atom in rope_dict.values():
            awardee_title_value = plan_awardlink_atom.get_value("awardee_title")
            rope_value = plan_awardlink_atom.get_value("plan_rope")
            give_force_value = plan_awardlink_atom.get_value("give_force")
            take_force_value = plan_awardlink_atom.get_value("take_force")
            if give_force_value is not None and take_force_value is not None:
                x_str = f"Awardlink has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
            elif give_force_value is not None:
                x_str = f"Awardlink has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value}."
            elif take_force_value is not None:
                x_str = f"Awardlink has been set for group {awardee_title_value} for plan '{rope_value}'. Now take_force={take_force_value}."
            legible_list.append(x_str)


def add_believer_plan_awardlink_delete_to_legible_list(
    legible_list: list[str], plan_awardlink_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_awardlink_delete_dict.values():
        for plan_awardlink_atom in rope_dict.values():
            awardee_title_value = plan_awardlink_atom.get_value("awardee_title")
            rope_value = plan_awardlink_atom.get_value("plan_rope")
            x_str = f"Awardlink for group {awardee_title_value}, plan '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_believer_plan_reasonunit_insert_to_legible_list(
    legible_list: list[str], plan_reasonunit_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_reasonunit_insert_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            rcontext_value = plan_reasonunit_atom.get_value("rcontext")
            rplan_active_requisite_value = plan_reasonunit_atom.get_value(
                "rplan_active_requisite"
            )
            x_str = f"ReasonUnit created for plan '{rope_value}' with rcontext '{rcontext_value}'."
            if rplan_active_requisite_value is not None:
                x_str += f" rplan_active_requisite={rplan_active_requisite_value}."
            legible_list.append(x_str)


def add_believer_plan_reasonunit_update_to_legible_list(
    legible_list: list[str], plan_reasonunit_update_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_reasonunit_update_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            rcontext_value = plan_reasonunit_atom.get_value("rcontext")
            rplan_active_requisite_value = plan_reasonunit_atom.get_value(
                "rplan_active_requisite"
            )
            if rplan_active_requisite_value is not None:
                x_str = f"ReasonUnit rcontext='{rcontext_value}' for plan '{rope_value}' set with rplan_active_requisite={rplan_active_requisite_value}."
            else:
                x_str = f"ReasonUnit rcontext='{rcontext_value}' for plan '{rope_value}' and no longer checks rcontext active mode."
            legible_list.append(x_str)


def add_believer_plan_reasonunit_delete_to_legible_list(
    legible_list: list[str], plan_reasonunit_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_reasonunit_delete_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            rcontext_value = plan_reasonunit_atom.get_value("rcontext")
            x_str = f"ReasonUnit rcontext='{rcontext_value}' for plan '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_believer_reason_premiseunit_insert_to_legible_list(
    legible_list: list[str],
    plan_reason_premiseunit_insert_dict: dict,
    x_believer: BelieverUnit,
):
    for rope_dict in plan_reason_premiseunit_insert_dict.values():
        for rcontext_dict in rope_dict.values():
            for plan_reason_premiseunit_atom in rcontext_dict.values():
                rope_value = plan_reason_premiseunit_atom.get_value("plan_rope")
                rcontext_value = plan_reason_premiseunit_atom.get_value("rcontext")
                pstate_value = plan_reason_premiseunit_atom.get_value("pstate")
                pdivisor_value = plan_reason_premiseunit_atom.get_value("pdivisor")
                pnigh_value = plan_reason_premiseunit_atom.get_value("pnigh")
                popen_value = plan_reason_premiseunit_atom.get_value("popen")
                x_str = f"PremiseUnit '{pstate_value}' created for reason '{rcontext_value}' for plan '{rope_value}'."
                if popen_value is not None:
                    x_str += f" Popen={popen_value}."
                if pnigh_value is not None:
                    x_str += f" Pnigh={pnigh_value}."
                if pdivisor_value is not None:
                    x_str += f" Pdivisor={pdivisor_value}."
                legible_list.append(x_str)


def add_believer_reason_premiseunit_update_to_legible_list(
    legible_list: list[str],
    plan_reason_premiseunit_update_dict: dict,
    x_believer: BelieverUnit,
):
    for rope_dict in plan_reason_premiseunit_update_dict.values():
        for rcontext_dict in rope_dict.values():
            for plan_reason_premiseunit_atom in rcontext_dict.values():
                rope_value = plan_reason_premiseunit_atom.get_value("plan_rope")
                rcontext_value = plan_reason_premiseunit_atom.get_value("rcontext")
                pstate_value = plan_reason_premiseunit_atom.get_value("pstate")
                pdivisor_value = plan_reason_premiseunit_atom.get_value("pdivisor")
                pnigh_value = plan_reason_premiseunit_atom.get_value("pnigh")
                popen_value = plan_reason_premiseunit_atom.get_value("popen")
                x_str = f"PremiseUnit '{pstate_value}' updated for reason '{rcontext_value}' for plan '{rope_value}'."
                if popen_value is not None:
                    x_str += f" Popen={popen_value}."
                if pnigh_value is not None:
                    x_str += f" Pnigh={pnigh_value}."
                if pdivisor_value is not None:
                    x_str += f" Pdivisor={pdivisor_value}."
                legible_list.append(x_str)


def add_believer_reason_premiseunit_delete_to_legible_list(
    legible_list: list[str],
    plan_reason_premiseunit_delete_dict: dict,
    x_believer: BelieverUnit,
):
    for rope_dict in plan_reason_premiseunit_delete_dict.values():
        for rcontext_dict in rope_dict.values():
            for plan_reason_premiseunit_atom in rcontext_dict.values():
                rope_value = plan_reason_premiseunit_atom.get_value("plan_rope")
                rcontext_value = plan_reason_premiseunit_atom.get_value("rcontext")
                pstate_value = plan_reason_premiseunit_atom.get_value("pstate")
                x_str = f"PremiseUnit '{pstate_value}' deleted from reason '{rcontext_value}' for plan '{rope_value}'."
                legible_list.append(x_str)


def add_believer_plan_laborlink_insert_to_legible_list(
    legible_list: list[str], plan_laborlink_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_laborlink_insert_dict.values():
        for plan_laborlink_atom in rope_dict.values():
            labor_title_value = plan_laborlink_atom.get_value("labor_title")
            rope_value = plan_laborlink_atom.get_value("plan_rope")
            x_str = f"laborlink '{labor_title_value}' created for plan '{rope_value}'."
            legible_list.append(x_str)


def add_believer_plan_laborlink_delete_to_legible_list(
    legible_list: list[str], plan_laborlink_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_laborlink_delete_dict.values():
        for plan_laborlink_atom in rope_dict.values():
            labor_title_value = plan_laborlink_atom.get_value("labor_title")
            rope_value = plan_laborlink_atom.get_value("plan_rope")
            x_str = f"laborlink '{labor_title_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)


def add_believer_plan_healerlink_insert_to_legible_list(
    legible_list: list[str], plan_healerlink_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_healerlink_insert_dict.values():
        for plan_healerlink_atom in rope_dict.values():
            healer_name_value = plan_healerlink_atom.get_value("healer_name")
            rope_value = plan_healerlink_atom.get_value("plan_rope")
            x_str = f"HealerLink '{healer_name_value}' created for plan '{rope_value}'."
            legible_list.append(x_str)


def add_believer_plan_healerlink_delete_to_legible_list(
    legible_list: list[str], plan_healerlink_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_healerlink_delete_dict.values():
        for plan_healerlink_atom in rope_dict.values():
            healer_name_value = plan_healerlink_atom.get_value("healer_name")
            rope_value = plan_healerlink_atom.get_value("plan_rope")
            x_str = f"HealerLink '{healer_name_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)


def add_believer_plan_factunit_insert_to_legible_list(
    legible_list: list[str], plan_factunit_insert_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_factunit_insert_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fcontext_value = plan_factunit_atom.get_value("fcontext")
            fstate_value = plan_factunit_atom.get_value("fstate")
            fnigh_value = plan_factunit_atom.get_value("fnigh")
            fopen_value = plan_factunit_atom.get_value("fopen")
            x_str = f"FactUnit '{fstate_value}' created for rcontext '{fcontext_value}' for plan '{rope_value}'."
            if fopen_value is not None:
                x_str += f" fopen={fopen_value}."
            if fnigh_value is not None:
                x_str += f" fnigh={fnigh_value}."
            legible_list.append(x_str)


def add_believer_plan_factunit_update_to_legible_list(
    legible_list: list[str], plan_factunit_update_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_factunit_update_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fcontext_value = plan_factunit_atom.get_value("fcontext")
            fstate_value = plan_factunit_atom.get_value("fstate")
            fnigh_value = plan_factunit_atom.get_value("fnigh")
            fopen_value = plan_factunit_atom.get_value("fopen")
            x_str = f"FactUnit '{fstate_value}' updated for rcontext '{fcontext_value}' for plan '{rope_value}'."
            if fopen_value is not None:
                x_str += f" fopen={fopen_value}."
            if fnigh_value is not None:
                x_str += f" fnigh={fnigh_value}."
            legible_list.append(x_str)


def add_believer_plan_factunit_delete_to_legible_list(
    legible_list: list[str], plan_factunit_delete_dict: dict, x_believer: BelieverUnit
):
    for rope_dict in plan_factunit_delete_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fcontext_value = plan_factunit_atom.get_value("fcontext")
            fstate_value = plan_factunit_atom.get_value("fstate")
            x_str = (
                f"FactUnit rcontext '{fcontext_value}' deleted for plan '{rope_value}'."
            )
            legible_list.append(x_str)
