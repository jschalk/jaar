from src._instrument.python import get_nested_value
from src._world.world import WorldUnit
from src.gift.atom import atom_delete, atom_insert, atom_update, AtomUnit
from src.gift.change import ChangeUnit


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_nested_value(x_dict, x_keylist, if_missing_return_None=True)


def create_legible_list(x_change: ChangeUnit, x_world: WorldUnit) -> list[str]:
    atoms_dict = x_change.atomunits
    worldunit_atom = get_leg_obj(atoms_dict, [atom_update(), "worldunit"])

    charunit_insert_dict = get_leg_obj(atoms_dict, [atom_insert(), "world_charunit"])
    charunit_update_dict = get_leg_obj(atoms_dict, [atom_update(), "world_charunit"])
    charunit_delete_dict = get_leg_obj(atoms_dict, [atom_delete(), "world_charunit"])

    x_list = [atom_insert(), "world_char_belieflink"]
    char_belieflink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_char_belieflink"]
    char_belieflink_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_char_belieflink"]
    char_belieflink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_ideaunit"]
    world_ideaunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_ideaunit"]
    world_ideaunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_ideaunit"]
    world_ideaunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_fiscallink"]
    world_idea_fiscallink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_idea_fiscallink"]
    world_idea_fiscallink_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_fiscallink"]
    world_idea_fiscallink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_reasonunit"]
    world_idea_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_idea_reasonunit"]
    world_idea_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_reasonunit"]
    world_idea_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_reason_premiseunit"]
    world_idea_reason_premiseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_idea_reason_premiseunit"]
    world_idea_reason_premiseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_reason_premiseunit"]
    world_idea_reason_premiseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_allyhold"]
    world_idea_allyhold_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_allyhold"]
    world_idea_allyhold_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_healerhold"]
    world_idea_healerhold_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_healerhold"]
    world_idea_healerhold_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_factunit"]
    world_idea_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_idea_factunit"]
    world_idea_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_factunit"]
    world_idea_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    leg_list = []
    if worldunit_atom != None:
        add_worldunit_legible_list(leg_list, worldunit_atom, x_world)
    if charunit_insert_dict != None:
        add_world_charunit_insert_to_legible_list(
            leg_list, charunit_insert_dict, x_world
        )
    if charunit_update_dict != None:
        add_world_charunit_update_to_legible_list(
            leg_list, charunit_update_dict, x_world
        )
    if charunit_delete_dict != None:
        add_world_charunit_delete_to_legible_list(
            leg_list, charunit_delete_dict, x_world
        )

    if char_belieflink_insert_dict != None:
        add_world_char_belieflink_insert_to_legible_list(
            leg_list, char_belieflink_insert_dict, x_world
        )
    if char_belieflink_update_dict != None:
        add_world_char_belieflink_update_to_legible_list(
            leg_list, char_belieflink_update_dict, x_world
        )
    if char_belieflink_delete_dict != None:
        add_world_char_belieflink_delete_to_legible_list(
            leg_list, char_belieflink_delete_dict, x_world
        )

    if world_ideaunit_insert_dict != None:
        add_world_ideaunit_insert_to_legible_list(
            leg_list, world_ideaunit_insert_dict, x_world
        )
    if world_ideaunit_update_dict != None:
        add_world_ideaunit_update_to_legible_list(
            leg_list, world_ideaunit_update_dict, x_world
        )
    if world_ideaunit_delete_dict != None:
        add_world_ideaunit_delete_to_legible_list(
            leg_list, world_ideaunit_delete_dict, x_world
        )

    if world_idea_fiscallink_insert_dict != None:
        add_world_idea_fiscallink_insert_to_legible_list(
            leg_list, world_idea_fiscallink_insert_dict, x_world
        )
    if world_idea_fiscallink_update_dict != None:
        add_world_idea_fiscallink_update_to_legible_list(
            leg_list, world_idea_fiscallink_update_dict, x_world
        )
    if world_idea_fiscallink_delete_dict != None:
        add_world_idea_fiscallink_delete_to_legible_list(
            leg_list, world_idea_fiscallink_delete_dict, x_world
        )

    if world_idea_reasonunit_insert_dict != None:
        add_world_idea_reasonunit_insert_to_legible_list(
            leg_list, world_idea_reasonunit_insert_dict, x_world
        )
    if world_idea_reasonunit_update_dict != None:
        add_world_idea_reasonunit_update_to_legible_list(
            leg_list, world_idea_reasonunit_update_dict, x_world
        )
    if world_idea_reasonunit_delete_dict != None:
        add_world_idea_reasonunit_delete_to_legible_list(
            leg_list, world_idea_reasonunit_delete_dict, x_world
        )

    if world_idea_reason_premiseunit_insert_dict != None:
        add_world_reason_premiseunit_insert_to_legible_list(
            leg_list, world_idea_reason_premiseunit_insert_dict, x_world
        )
    if world_idea_reason_premiseunit_update_dict != None:
        add_world_reason_premiseunit_update_to_legible_list(
            leg_list, world_idea_reason_premiseunit_update_dict, x_world
        )
    if world_idea_reason_premiseunit_delete_dict != None:
        add_world_reason_premiseunit_delete_to_legible_list(
            leg_list, world_idea_reason_premiseunit_delete_dict, x_world
        )

    if world_idea_allyhold_insert_dict != None:
        add_world_idea_allyhold_insert_to_legible_list(
            leg_list, world_idea_allyhold_insert_dict, x_world
        )
    if world_idea_allyhold_delete_dict != None:
        add_world_idea_allyhold_delete_to_legible_list(
            leg_list, world_idea_allyhold_delete_dict, x_world
        )

    if world_idea_healerhold_insert_dict != None:
        add_world_idea_healerhold_insert_to_legible_list(
            leg_list, world_idea_healerhold_insert_dict, x_world
        )
    if world_idea_healerhold_delete_dict != None:
        add_world_idea_healerhold_delete_to_legible_list(
            leg_list, world_idea_healerhold_delete_dict, x_world
        )

    if world_idea_factunit_insert_dict != None:
        add_world_idea_factunit_insert_to_legible_list(
            leg_list, world_idea_factunit_insert_dict, x_world
        )
    if world_idea_factunit_update_dict != None:
        add_world_idea_factunit_update_to_legible_list(
            leg_list, world_idea_factunit_update_dict, x_world
        )
    if world_idea_factunit_delete_dict != None:
        add_world_idea_factunit_delete_to_legible_list(
            leg_list, world_idea_factunit_delete_dict, x_world
        )

    return leg_list


def add_worldunit_legible_list(
    legible_list: list[str], x_atom: AtomUnit, x_world: WorldUnit
):
    optional_args = x_atom.optional_args
    _weight_text = "_weight"
    _max_tree_traverse_text = "_max_tree_traverse"
    _meld_strategy_text = "_meld_strategy"
    _monetary_desc_text = "_monetary_desc"
    _char_credor_pool_text = "_char_credor_pool"
    _char_debtor_pool_text = "_char_debtor_pool"

    _max_tree_traverse_value = optional_args.get(_max_tree_traverse_text)
    _meld_strategy_value = optional_args.get(_meld_strategy_text)
    _monetary_desc_value = optional_args.get(_monetary_desc_text)
    _char_credor_pool_value = optional_args.get(_char_credor_pool_text)
    _char_debtor_pool_value = optional_args.get(_char_debtor_pool_text)
    _weight_value = optional_args.get(_weight_text)

    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = f"{x_world._owner_id}'s monetary_desc"

    if _max_tree_traverse_value != None:
        legible_list.append(
            f"{x_world._owner_id}'s maximum number of World output evaluations transited to {_max_tree_traverse_value}"
        )
    if _meld_strategy_value != None:
        legible_list.append(
            f"{x_world._owner_id}'s Meld strategy transited to '{_meld_strategy_value}'"
        )
    if _monetary_desc_value != None:
        legible_list.append(
            f"{x_world._owner_id}'s monetary_desc is now called '{_monetary_desc_value}'"
        )
    if (
        _char_credor_pool_value != None
        and _char_debtor_pool_value != None
        and _char_credor_pool_value == _char_debtor_pool_value
    ):
        legible_list.append(
            f"{x_monetary_desc} total pool is now {_char_credor_pool_value}"
        )
    elif _char_credor_pool_value != None:
        legible_list.append(
            f"{x_monetary_desc} credor pool is now {_char_credor_pool_value}"
        )
    elif _char_debtor_pool_value != None:
        legible_list.append(
            f"{x_monetary_desc} debtor pool is now {_char_debtor_pool_value}"
        )
    if _weight_value != None:
        legible_list.append(
            f"{x_world._owner_id}'s world weight was transited to {_weight_value}"
        )


def add_world_charunit_insert_to_legible_list(
    legible_list: list[str], charunit_dict: AtomUnit, x_world: WorldUnit
):
    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for charunit_atom in charunit_dict.values():
        char_id = charunit_atom.get_value("char_id")
        credor_weight_value = charunit_atom.get_value("credor_weight")
        debtor_weight_value = charunit_atom.get_value("debtor_weight")
        x_str = f"{char_id} was added with {credor_weight_value} {x_monetary_desc} cred and {debtor_weight_value} {x_monetary_desc} debt"
        legible_list.append(x_str)


def add_world_charunit_update_to_legible_list(
    legible_list: list[str], charunit_dict: AtomUnit, x_world: WorldUnit
):
    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for charunit_atom in charunit_dict.values():
        char_id = charunit_atom.get_value("char_id")
        credor_weight_value = charunit_atom.get_value("credor_weight")
        debtor_weight_value = charunit_atom.get_value("debtor_weight")
        if credor_weight_value != None and debtor_weight_value != None:
            x_str = f"{char_id} now has {credor_weight_value} {x_monetary_desc} cred and {debtor_weight_value} {x_monetary_desc} debt."
        elif credor_weight_value != None and debtor_weight_value is None:
            x_str = f"{char_id} now has {credor_weight_value} {x_monetary_desc} cred."
        elif credor_weight_value is None and debtor_weight_value != None:
            x_str = f"{char_id} now has {debtor_weight_value} {x_monetary_desc} debt."
        legible_list.append(x_str)


def add_world_charunit_delete_to_legible_list(
    legible_list: list[str], charunit_dict: AtomUnit, x_world: WorldUnit
):
    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for charunit_atom in charunit_dict.values():
        char_id = charunit_atom.get_value("char_id")
        x_str = f"{char_id} was removed from {x_monetary_desc} chars."
        legible_list.append(x_str)


def add_world_beliefunit_insert_to_legible_list(
    legible_list: list[str], beliefunit_dict: AtomUnit, x_world: WorldUnit
):
    for beliefunit_atom in beliefunit_dict.values():
        belief_id = beliefunit_atom.get_value("belief_id")
        x_str = f"The belief '{belief_id}' was created"
        x_str += "."
        legible_list.append(x_str)


def add_world_beliefunit_update_to_legible_list(
    legible_list: list[str], beliefunit_dict: AtomUnit, x_world: WorldUnit
):
    for beliefunit_atom in beliefunit_dict.values():
        belief_id = beliefunit_atom.get_value("belief_id")
        x_str = f"The belief '{belief_id}'"
        x_str += "."
        legible_list.append(x_str)


def add_world_beliefunit_delete_to_legible_list(
    legible_list: list[str], beliefunit_dict: AtomUnit, x_world: WorldUnit
):
    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for beliefunit_atom in beliefunit_dict.values():
        belief_id = beliefunit_atom.get_value("belief_id")
        x_str = f"The belief '{belief_id}' was deleted."
        legible_list.append(x_str)


def add_world_char_belieflink_insert_to_legible_list(
    legible_list: list[str], char_belieflink_insert_dict: dict, x_world: WorldUnit
):
    for char_belieflink_dict in char_belieflink_insert_dict.values():
        for char_belieflink_atom in char_belieflink_dict.values():
            belief_id = char_belieflink_atom.get_value("belief_id")
            char_id = char_belieflink_atom.get_value("char_id")
            credor_weight_value = char_belieflink_atom.get_value("credor_weight")
            debtor_weight_value = char_belieflink_atom.get_value("debtor_weight")
            x_str = f"Belief '{belief_id}' has new member {char_id} with belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
            legible_list.append(x_str)


def add_world_char_belieflink_update_to_legible_list(
    legible_list: list[str], char_belieflink_update_dict: dict, x_world: WorldUnit
):
    for char_belieflink_dict in char_belieflink_update_dict.values():
        for char_belieflink_atom in char_belieflink_dict.values():
            belief_id = char_belieflink_atom.get_value("belief_id")
            char_id = char_belieflink_atom.get_value("char_id")
            credor_weight_value = char_belieflink_atom.get_value("credor_weight")
            debtor_weight_value = char_belieflink_atom.get_value("debtor_weight")
            if credor_weight_value != None and debtor_weight_value != None:
                x_str = f"Belief '{belief_id}' member {char_id} has new belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
            elif credor_weight_value != None and debtor_weight_value is None:
                x_str = f"Belief '{belief_id}' member {char_id} has new belief_cred={credor_weight_value}."
            elif credor_weight_value is None and debtor_weight_value != None:
                x_str = f"Belief '{belief_id}' member {char_id} has new belief_debt={debtor_weight_value}."
            legible_list.append(x_str)


def add_world_char_belieflink_delete_to_legible_list(
    legible_list: list[str], char_belieflink_delete_dict: dict, x_world: WorldUnit
):
    for char_belieflink_dict in char_belieflink_delete_dict.values():
        for char_belieflink_atom in char_belieflink_dict.values():
            belief_id = char_belieflink_atom.get_value("belief_id")
            char_id = char_belieflink_atom.get_value("char_id")
            x_str = f"Belief '{belief_id}' no longer has member {char_id}."
            legible_list.append(x_str)


def add_world_ideaunit_insert_to_legible_list(
    legible_list: list[str], ideaunit_insert_dict: dict, x_world: WorldUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _meld_strategy_text = "_meld_strategy"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _weight_text = "_weight"
    pledge_text = "pledge"
    for parent_road_dict in ideaunit_insert_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_text)
            parent_road_value = ideaunit_atom.get_value(parent_road_text)
            _addin_value = ideaunit_atom.get_value(_addin_text)
            _begin_value = ideaunit_atom.get_value(_begin_text)
            _close_value = ideaunit_atom.get_value(_close_text)
            _denom_value = ideaunit_atom.get_value(_denom_text)
            _meld_strategy_value = ideaunit_atom.get_value(_meld_strategy_text)
            _numeric_road_value = ideaunit_atom.get_value(_numeric_road_text)
            _numor_value = ideaunit_atom.get_value(_numor_text)
            _problem_bool_value = ideaunit_atom.get_value(_problem_bool_text)
            _range_source_road_value = ideaunit_atom.get_value(_range_source_road_text)
            _reest_value = ideaunit_atom.get_value(_reest_text)
            _weight_value = ideaunit_atom.get_value(_weight_text)
            pledge_value = ideaunit_atom.get_value(pledge_text)
            x_str = (
                f"Created Idea '{label_value}' with parent_road {parent_road_value}. "
            )
            if _addin_value != None:
                x_str += f"_addin={_addin_value}."
            if _begin_value != None:
                x_str += f"_begin={_begin_value}."
            if _close_value != None:
                x_str += f"_close={_close_value}."
            if _denom_value != None:
                x_str += f"_denom={_denom_value}."
            if _meld_strategy_value != None:
                x_str += f"_meld_strategy={_meld_strategy_value}."
            if _numeric_road_value != None:
                x_str += f"_numeric_road={_numeric_road_value}."
            if _numor_value != None:
                x_str += f"_numor={_numor_value}."
            if _problem_bool_value != None:
                x_str += f"_problem_bool={_problem_bool_value}."
            if _range_source_road_value != None:
                x_str += f"_range_source_road={_range_source_road_value}."
            if _reest_value != None:
                x_str += f"_reest={_reest_value}."
            if _weight_value != None:
                x_str += f"_weight={_weight_value}."
            if pledge_value != None:
                x_str += f"pledge={pledge_value}."

            legible_list.append(x_str)


def add_world_ideaunit_update_to_legible_list(
    legible_list: list[str], ideaunit_update_dict: dict, x_world: WorldUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _meld_strategy_text = "_meld_strategy"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _weight_text = "_weight"
    pledge_text = "pledge"
    for parent_road_dict in ideaunit_update_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_text)
            parent_road_value = ideaunit_atom.get_value(parent_road_text)
            _addin_value = ideaunit_atom.get_value(_addin_text)
            _begin_value = ideaunit_atom.get_value(_begin_text)
            _close_value = ideaunit_atom.get_value(_close_text)
            _denom_value = ideaunit_atom.get_value(_denom_text)
            _meld_strategy_value = ideaunit_atom.get_value(_meld_strategy_text)
            _numeric_road_value = ideaunit_atom.get_value(_numeric_road_text)
            _numor_value = ideaunit_atom.get_value(_numor_text)
            _problem_bool_value = ideaunit_atom.get_value(_problem_bool_text)
            _range_source_road_value = ideaunit_atom.get_value(_range_source_road_text)
            _reest_value = ideaunit_atom.get_value(_reest_text)
            _weight_value = ideaunit_atom.get_value(_weight_text)
            pledge_value = ideaunit_atom.get_value(pledge_text)
            x_str = f"Idea '{label_value}' with parent_road {parent_road_value} transited these attributes: "
            if _addin_value != None:
                x_str += f"_addin={_addin_value}."
            if _begin_value != None:
                x_str += f"_begin={_begin_value}."
            if _close_value != None:
                x_str += f"_close={_close_value}."
            if _denom_value != None:
                x_str += f"_denom={_denom_value}."
            if _meld_strategy_value != None:
                x_str += f"_meld_strategy={_meld_strategy_value}."
            if _numeric_road_value != None:
                x_str += f"_numeric_road={_numeric_road_value}."
            if _numor_value != None:
                x_str += f"_numor={_numor_value}."
            if _problem_bool_value != None:
                x_str += f"_problem_bool={_problem_bool_value}."
            if _range_source_road_value != None:
                x_str += f"_range_source_road={_range_source_road_value}."
            if _reest_value != None:
                x_str += f"_reest={_reest_value}."
            if _weight_value != None:
                x_str += f"_weight={_weight_value}."
            if pledge_value != None:
                x_str += f"pledge={pledge_value}."

            legible_list.append(x_str)


def add_world_ideaunit_delete_to_legible_list(
    legible_list: list[str], ideaunit_delete_dict: dict, x_world: WorldUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    for parent_road_dict in ideaunit_delete_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_text)
            parent_road_value = ideaunit_atom.get_value(parent_road_text)
            x_str = f"Idea '{label_value}' with parent_road {parent_road_value} was deleted."
            legible_list.append(x_str)


def add_world_idea_fiscallink_insert_to_legible_list(
    legible_list: list[str], idea_fiscallink_insert_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_fiscallink_insert_dict.values():
        for idea_fiscallink_atom in road_dict.values():
            belief_id_value = idea_fiscallink_atom.get_value("belief_id")
            road_value = idea_fiscallink_atom.get_value("road")
            credor_weight_value = idea_fiscallink_atom.get_value("credor_weight")
            debtor_weight_value = idea_fiscallink_atom.get_value("debtor_weight")
            x_str = f"Fiscallink created for belief {belief_id_value} for idea '{road_value}' with credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
            legible_list.append(x_str)


def add_world_idea_fiscallink_update_to_legible_list(
    legible_list: list[str], idea_fiscallink_update_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_fiscallink_update_dict.values():
        for idea_fiscallink_atom in road_dict.values():
            belief_id_value = idea_fiscallink_atom.get_value("belief_id")
            road_value = idea_fiscallink_atom.get_value("road")
            credor_weight_value = idea_fiscallink_atom.get_value("credor_weight")
            debtor_weight_value = idea_fiscallink_atom.get_value("debtor_weight")
            if credor_weight_value != None and debtor_weight_value != None:
                x_str = f"Fiscallink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
            elif credor_weight_value != None and debtor_weight_value is None:
                x_str = f"Fiscallink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value}."
            elif credor_weight_value is None and debtor_weight_value != None:
                x_str = f"Fiscallink has been transited for belief {belief_id_value} for idea '{road_value}'. Now debtor_weight={debtor_weight_value}."
            legible_list.append(x_str)


def add_world_idea_fiscallink_delete_to_legible_list(
    legible_list: list[str], idea_fiscallink_delete_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_fiscallink_delete_dict.values():
        for idea_fiscallink_atom in road_dict.values():
            belief_id_value = idea_fiscallink_atom.get_value("belief_id")
            road_value = idea_fiscallink_atom.get_value("road")
            x_str = f"Fiscallink for belief {belief_id_value}, idea '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_world_idea_reasonunit_insert_to_legible_list(
    legible_list: list[str], idea_reasonunit_insert_dict: dict, x_world: WorldUnit
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
            if base_idea_active_requisite_value != None:
                x_str += (
                    f" base_idea_active_requisite={base_idea_active_requisite_value}."
                )
            legible_list.append(x_str)


def add_world_idea_reasonunit_update_to_legible_list(
    legible_list: list[str], idea_reasonunit_update_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_reasonunit_update_dict.values():
        for idea_reasonunit_atom in road_dict.values():
            road_value = idea_reasonunit_atom.get_value("road")
            base_value = idea_reasonunit_atom.get_value("base")
            base_idea_active_requisite_value = idea_reasonunit_atom.get_value(
                "base_idea_active_requisite"
            )
            if base_idea_active_requisite_value != None:
                x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' transited with base_idea_active_requisite={base_idea_active_requisite_value}."
            elif base_idea_active_requisite_value is None:
                x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' and no longer checks base active mode."
            legible_list.append(x_str)


def add_world_idea_reasonunit_delete_to_legible_list(
    legible_list: list[str], idea_reasonunit_delete_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_reasonunit_delete_dict.values():
        for idea_reasonunit_atom in road_dict.values():
            road_value = idea_reasonunit_atom.get_value("road")
            base_value = idea_reasonunit_atom.get_value("base")
            x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_world_reason_premiseunit_insert_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_insert_dict: dict,
    x_world: WorldUnit,
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
                if open_value != None:
                    x_str += f" Open={open_value}."
                if nigh_value != None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value != None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_world_reason_premiseunit_update_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_update_dict: dict,
    x_world: WorldUnit,
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
                if open_value != None:
                    x_str += f" Open={open_value}."
                if nigh_value != None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value != None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_world_reason_premiseunit_delete_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_delete_dict: dict,
    x_world: WorldUnit,
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


def add_world_idea_allyhold_insert_to_legible_list(
    legible_list: list[str], idea_allyhold_insert_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_allyhold_insert_dict.values():
        for idea_allyhold_atom in road_dict.values():
            belief_id_value = idea_allyhold_atom.get_value("belief_id")
            road_value = idea_allyhold_atom.get_value("road")
            x_str = f"allyhold '{belief_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_world_idea_allyhold_delete_to_legible_list(
    legible_list: list[str], idea_allyhold_delete_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_allyhold_delete_dict.values():
        for idea_allyhold_atom in road_dict.values():
            belief_id_value = idea_allyhold_atom.get_value("belief_id")
            road_value = idea_allyhold_atom.get_value("road")
            x_str = f"allyhold '{belief_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_world_idea_healerhold_insert_to_legible_list(
    legible_list: list[str], idea_healerhold_insert_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_healerhold_insert_dict.values():
        for idea_healerhold_atom in road_dict.values():
            belief_id_value = idea_healerhold_atom.get_value("belief_id")
            road_value = idea_healerhold_atom.get_value("road")
            x_str = f"Healerhold '{belief_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_world_idea_healerhold_delete_to_legible_list(
    legible_list: list[str], idea_healerhold_delete_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_healerhold_delete_dict.values():
        for idea_healerhold_atom in road_dict.values():
            belief_id_value = idea_healerhold_atom.get_value("belief_id")
            road_value = idea_healerhold_atom.get_value("road")
            x_str = f"Healerhold '{belief_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_world_idea_factunit_insert_to_legible_list(
    legible_list: list[str], idea_factunit_insert_dict: dict, x_world: WorldUnit
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
            if open_value != None:
                x_str += f" Open={open_value}."
            if nigh_value != None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_world_idea_factunit_update_to_legible_list(
    legible_list: list[str], idea_factunit_update_dict: dict, x_world: WorldUnit
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
            if open_value != None:
                x_str += f" Open={open_value}."
            if nigh_value != None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_world_idea_factunit_delete_to_legible_list(
    legible_list: list[str], idea_factunit_delete_dict: dict, x_world: WorldUnit
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
