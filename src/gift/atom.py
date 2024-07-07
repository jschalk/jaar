from src._instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    get_dict_from_json,
)
from src._instrument.sqlite import create_insert_sqlstr, RowData
from src._road.road import create_road
from src._world.reason_idea import factunit_shop
from src._world.char import charunit_shop, charlink_shop
from src._world.beliefunit import beliefunit_shop, fiscallink_shop
from src._world.idea import ideaunit_shop
from src._world.world import WorldUnit
from src.gift.atom_config import (
    get_category_from_dict,
    atom_delete,
    atom_insert,
    atom_update,
    atom_hx_table_name,
    get_atom_order,
    get_atom_config_dict,
    is_category_ref,
)
from dataclasses import dataclass


class AtomUnitDescriptionException(Exception):
    pass


@dataclass
class AtomUnit:
    category: str = None
    crud_text: str = None
    required_args: dict[str, str] = None
    optional_args: dict[str, str] = None
    atom_order: int = None

    def get_insert_sqlstr(self) -> str:
        if self.is_valid() is False:
            raise AtomUnitDescriptionException(
                f"Cannot get_insert_sqlstr '{self.category}' with is_valid=False."
            )

        x_columns = [
            f"{self.category}_{self.crud_text}_{required_arg}"
            for required_arg in self.required_args.keys()
        ]
        x_columns.extend(
            f"{self.category}_{self.crud_text}_{optional_arg}"
            for optional_arg in self.optional_args.keys()
        )
        x_values = list(self.required_args.values())
        x_values.extend(iter(self.optional_args.values()))
        return create_insert_sqlstr(atom_hx_table_name(), x_columns, x_values)

    def get_all_args_in_list(self):
        x_list = list(self.required_args.values())
        x_list.extend(list(self.optional_args.values()))
        return x_list

    def set_atom_order(self):
        self.atom_order = get_atom_order(self.crud_text, self.category)

    def set_arg(self, x_key: str, x_value: any):
        for required_arg in self._get_required_args_dict():
            if x_key == required_arg:
                self.set_required_arg(x_key, x_value)
        for optional_arg in self._get_optional_args_dict():
            if x_key == optional_arg:
                self.set_optional_arg(x_key, x_value)

    def set_required_arg(self, x_key: str, x_value: any):
        self.required_args[x_key] = x_value

    def set_optional_arg(self, x_key: str, x_value: any):
        self.optional_args[x_key] = x_value

    def _get_category_dict(self) -> dict:
        return get_atom_config_dict().get(self.category)

    def _get_crud_dict(self) -> dict:
        return self._get_category_dict().get(self.crud_text)

    def _get_required_args_dict(self) -> dict:
        return self._get_category_dict().get("required_args")

    def _get_optional_args_dict(self) -> dict:
        return get_empty_dict_if_none(self._get_category_dict().get("optional_args"))

    def is_required_args_valid(self) -> bool:
        if self.crud_text not in {atom_delete(), atom_insert(), atom_update()}:
            return False
        required_args_dict = self._get_required_args_dict()
        return required_args_dict.keys() == self.required_args.keys()

    def is_optional_args_valid(self) -> bool:
        if self.crud_text not in {atom_delete(), atom_insert(), atom_update()}:
            return False

        optional_args_dict = self._get_optional_args_dict()
        return set(self.optional_args.keys()).issubset(set(optional_args_dict.keys()))

    def is_valid(self) -> bool:
        return self.is_required_args_valid() and self.is_optional_args_valid()

    def get_value(self, arg_key: str) -> any:
        required_value = self.required_args.get(arg_key)
        if required_value is None:
            return self.optional_args.get(arg_key)
        return required_value

    def get_required_args_dict(self) -> dict[str, str]:
        return dict(self.required_args.items())

    def get_optional_args_dict(self) -> dict[str, str]:
        return dict(self.optional_args.items())

    def get_dict(self) -> dict[str, str]:
        required_args_dict = self.get_required_args_dict()
        optional_args_dict = self.get_optional_args_dict()
        # x_dict = {
        #     "category": self.category,
        #     "crud_text": self.crud_text,
        #     "required_args": required_args_dict,
        # }
        # if optional_args_dict != {}:
        #     x_dict["optional_args"] = optional_args_dict
        return {
            "category": self.category,
            "crud_text": self.crud_text,
            "required_args": required_args_dict,
            "optional_args": optional_args_dict,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def atomunit_shop(
    category: str,
    crud_text: str = None,
    required_args: dict[str, str] = None,
    optional_args: dict[str, str] = None,
) -> AtomUnit:
    if is_category_ref(category):
        return AtomUnit(
            category=category,
            crud_text=crud_text,
            required_args=get_empty_dict_if_none(required_args),
            optional_args=get_empty_dict_if_none(optional_args),
        )


def get_from_json(x_str: str) -> AtomUnit:
    x_dict = get_dict_from_json(x_str)
    x_atom = atomunit_shop(category=x_dict["category"], crud_text=x_dict["crud_text"])
    for x_key, x_value in x_dict["required_args"].items():
        x_atom.set_required_arg(x_key, x_value)
    for x_key, x_value in x_dict["optional_args"].items():
        x_atom.set_optional_arg(x_key, x_value)
    return x_atom


def _modify_world_update_worldunit(x_world: WorldUnit, x_atom: AtomUnit):
    x_arg = "_max_tree_traverse"
    if x_atom.get_value(x_arg) != None:
        x_world.set_max_tree_traverse(x_atom.get_value(x_arg))
    x_arg = "_char_credor_pool"
    if x_atom.get_value(x_arg) != None:
        x_world.set_char_credor_pool(x_atom.get_value(x_arg))
    x_arg = "_char_debtor_pool"
    if x_atom.get_value(x_arg) != None:
        x_world.set_char_debtor_pool(x_atom.get_value(x_arg))
    x_arg = "_meld_strategy"
    if x_atom.get_value(x_arg) != None:
        x_world.set_meld_strategy(x_atom.get_value(x_arg))
    x_arg = "_weight"
    if x_atom.get_value(x_arg) != None:
        x_world._weight = x_atom.get_value(x_arg)
    x_arg = "_pixel"
    if x_atom.get_value(x_arg) != None:
        x_world._pixel = x_atom.get_value(x_arg)
    x_arg = "_penny"
    if x_atom.get_value(x_arg) != None:
        x_world._penny = x_atom.get_value(x_arg)


def _modify_world_beliefunit_delete(x_world: WorldUnit, x_atom: AtomUnit):
    belief_id = x_atom.get_value("belief_id")
    x_world.del_beliefunit(belief_id)


def _modify_world_beliefunit_update(x_world: WorldUnit, x_atom: AtomUnit):
    x_beliefunit = x_world.get_beliefunit(x_atom.get_value("belief_id"))


def _modify_world_beliefunit_insert(x_world: WorldUnit, x_atom: AtomUnit):
    x_beliefunit = beliefunit_shop(belief_id=x_atom.get_value("belief_id"))
    x_world.set_beliefunit(
        x_beliefunit, create_missing_chars=False, replace=False, add_charlinks=False
    )


def _modify_world_char_beliefhold_delete(x_world: WorldUnit, x_atom: AtomUnit):
    x_char_id = x_atom.get_value("char_id")
    x_belief_id = x_atom.get_value("belief_id")
    x_world.get_beliefunit(x_belief_id).del_charlink(x_char_id)


def _modify_world_char_beliefhold_update(x_world: WorldUnit, x_atom: AtomUnit):
    x_beliefunit = x_world.get_beliefunit(x_atom.get_value("belief_id"))
    x_beliefunit.edit_charlink(
        char_id=x_atom.get_value("char_id"),
        credor_weight=x_atom.get_value("credor_weight"),
        debtor_weight=x_atom.get_value("debtor_weight"),
    )


def _modify_world_char_beliefhold_insert(x_world: WorldUnit, x_atom: AtomUnit):
    x_beliefunit = x_world.get_beliefunit(x_atom.get_value("belief_id"))
    x_beliefunit.set_charlink(
        charlink_shop(
            char_id=x_atom.get_value("char_id"),
            credor_weight=x_atom.get_value("credor_weight"),
            debtor_weight=x_atom.get_value("debtor_weight"),
        )
    )


def _modify_world_ideaunit_delete(x_world: WorldUnit, x_atom: AtomUnit):
    idea_road = create_road(
        x_atom.get_value("parent_road"),
        x_atom.get_value("label"),
        delimiter=x_world._road_delimiter,
    )
    x_world.del_idea_obj(idea_road, del_children=x_atom.get_value("del_children"))


def _modify_world_ideaunit_update(x_world: WorldUnit, x_atom: AtomUnit):
    idea_road = create_road(
        x_atom.get_value("parent_road"),
        x_atom.get_value("label"),
        delimiter=x_world._road_delimiter,
    )
    x_world.edit_idea_attr(
        road=idea_road,
        addin=x_atom.get_value("_addin"),
        begin=x_atom.get_value("_begin"),
        close=x_atom.get_value("_close"),
        denom=x_atom.get_value("_denom"),
        meld_strategy=x_atom.get_value("_meld_strategy"),
        numeric_road=x_atom.get_value("_numeric_road"),
        numor=x_atom.get_value("_numor"),
        range_source_road=x_atom.get_value("_range_source_road"),
        reest=x_atom.get_value("_reest"),
        weight=x_atom.get_value("_weight"),
        pledge=x_atom.get_value("pledge"),
    )


def _modify_world_ideaunit_insert(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.add_idea(
        idea_kid=ideaunit_shop(
            _label=x_atom.get_value("label"),
            _addin=x_atom.get_value("_addin"),
            _begin=x_atom.get_value("_begin"),
            _close=x_atom.get_value("_close"),
            _denom=x_atom.get_value("_denom"),
            _meld_strategy=x_atom.get_value("_meld_strategy"),
            _numeric_road=x_atom.get_value("_numeric_road"),
            _numor=x_atom.get_value("_numor"),
            pledge=x_atom.get_value("pledge"),
        ),
        parent_road=x_atom.get_value("parent_road"),
        create_missing_ideas=False,
        create_missing_beliefs=False,
        create_missing_ancestors=False,
    )


def _modify_world_idea_fiscallink_delete(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.edit_idea_attr(
        road=x_atom.get_value("road"),
        fiscallink_del=x_atom.get_value("belief_id"),
    )


def _modify_world_idea_fiscallink_update(x_world: WorldUnit, x_atom: AtomUnit):
    x_idea = x_world.get_idea_obj(x_atom.get_value("road"))
    x_fiscallink = x_idea._fiscallinks.get(x_atom.get_value("belief_id"))
    x_credor_weight = x_atom.get_value("credor_weight")
    if x_credor_weight != None and x_fiscallink.credor_weight != x_credor_weight:
        x_fiscallink.credor_weight = x_credor_weight
    x_debtor_weight = x_atom.get_value("debtor_weight")
    if x_debtor_weight != None and x_fiscallink.debtor_weight != x_debtor_weight:
        x_fiscallink.debtor_weight = x_debtor_weight
    x_world.edit_idea_attr(x_atom.get_value("road"), fiscallink=x_fiscallink)


def _modify_world_idea_fiscallink_insert(x_world: WorldUnit, x_atom: AtomUnit):
    x_fiscallink = fiscallink_shop(
        belief_id=x_atom.get_value("belief_id"),
        credor_weight=x_atom.get_value("credor_weight"),
        debtor_weight=x_atom.get_value("debtor_weight"),
    )
    x_world.edit_idea_attr(x_atom.get_value("road"), fiscallink=x_fiscallink)


def _modify_world_idea_factunit_delete(x_world: WorldUnit, x_atom: AtomUnit):
    x_ideaunit = x_world.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit.del_factunit(x_atom.get_value("base"))


def _modify_world_idea_factunit_update(x_world: WorldUnit, x_atom: AtomUnit):
    x_ideaunit = x_world.get_idea_obj(x_atom.get_value("road"))
    x_factunit = x_ideaunit._factunits.get(x_atom.get_value("base"))
    x_factunit.set_attr(
        pick=x_atom.get_value("pick"),
        open=x_atom.get_value("open"),
        nigh=x_atom.get_value("nigh"),
    )
    # x_ideaunit.set_factunit(x_factunit)


def _modify_world_idea_factunit_insert(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.edit_idea_attr(
        road=x_atom.get_value("road"),
        factunit=factunit_shop(
            base=x_atom.get_value("base"),
            pick=x_atom.get_value("pick"),
            open=x_atom.get_value("open"),
            nigh=x_atom.get_value("nigh"),
        ),
    )


def _modify_world_idea_reasonunit_delete(x_world: WorldUnit, x_atom: AtomUnit):
    x_ideaunit = x_world.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit.del_reasonunit_base(x_atom.get_value("base"))


def _modify_world_idea_reasonunit_update(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.edit_idea_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_base_idea_active_requisite=x_atom.get_value(
            "base_idea_active_requisite"
        ),
    )


def _modify_world_idea_reasonunit_insert(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.edit_idea_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_base_idea_active_requisite=x_atom.get_value(
            "base_idea_active_requisite"
        ),
    )


def _modify_world_idea_reason_premiseunit_delete(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.edit_idea_attr(
        road=x_atom.get_value("road"),
        reason_del_premise_base=x_atom.get_value("base"),
        reason_del_premise_need=x_atom.get_value("need"),
    )


def _modify_world_idea_reason_premiseunit_update(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.edit_idea_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_premise=x_atom.get_value("need"),
        reason_premise_open=x_atom.get_value("open"),
        reason_premise_nigh=x_atom.get_value("nigh"),
        reason_premise_divisor=x_atom.get_value("divisor"),
    )


def _modify_world_idea_reason_premiseunit_insert(x_world: WorldUnit, x_atom: AtomUnit):
    x_ideaunit = x_world.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit.set_reason_premise(
        base=x_atom.get_value("base"),
        premise=x_atom.get_value("need"),
        open=x_atom.get_value("open"),
        nigh=x_atom.get_value("nigh"),
        divisor=x_atom.get_value("divisor"),
    )


def _modify_world_idea_heldbelief_delete(x_world: WorldUnit, x_atom: AtomUnit):
    x_ideaunit = x_world.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit._cultureunit.del_heldbelief(belief_id=x_atom.get_value("belief_id"))


def _modify_world_idea_heldbelief_insert(x_world: WorldUnit, x_atom: AtomUnit):
    x_ideaunit = x_world.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit._cultureunit.set_heldbelief(belief_id=x_atom.get_value("belief_id"))


def _modify_world_charunit_delete(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.del_charunit(x_atom.get_value("char_id"))


def _modify_world_charunit_update(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.edit_charunit(
        char_id=x_atom.get_value("char_id"),
        credor_weight=x_atom.get_value("credor_weight"),
        debtor_weight=x_atom.get_value("debtor_weight"),
    )


def _modify_world_charunit_insert(x_world: WorldUnit, x_atom: AtomUnit):
    x_world.set_charunit(
        charunit_shop(
            char_id=x_atom.get_value("char_id"),
            credor_weight=x_atom.get_value("credor_weight"),
            debtor_weight=x_atom.get_value("debtor_weight"),
        )
    )


def _modify_world_worldunit(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_update():
        _modify_world_update_worldunit(x_world, x_atom)


def _modify_world_beliefunit(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_world_beliefunit_delete(x_world, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_world_beliefunit_update(x_world, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_world_beliefunit_insert(x_world, x_atom)


def _modify_world_char_beliefhold(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_world_char_beliefhold_delete(x_world, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_world_char_beliefhold_update(x_world, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_world_char_beliefhold_insert(x_world, x_atom)


def _modify_world_ideaunit(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_world_ideaunit_delete(x_world, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_world_ideaunit_update(x_world, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_world_ideaunit_insert(x_world, x_atom)


def _modify_world_idea_fiscallink(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_world_idea_fiscallink_delete(x_world, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_world_idea_fiscallink_update(x_world, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_world_idea_fiscallink_insert(x_world, x_atom)


def _modify_world_idea_factunit(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_world_idea_factunit_delete(x_world, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_world_idea_factunit_update(x_world, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_world_idea_factunit_insert(x_world, x_atom)


def _modify_world_idea_reasonunit(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_world_idea_reasonunit_delete(x_world, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_world_idea_reasonunit_update(x_world, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_world_idea_reasonunit_insert(x_world, x_atom)


def _modify_world_idea_reason_premiseunit(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_world_idea_reason_premiseunit_delete(x_world, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_world_idea_reason_premiseunit_update(x_world, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_world_idea_reason_premiseunit_insert(x_world, x_atom)


def _modify_world_idea_heldbelief(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_world_idea_heldbelief_delete(x_world, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_world_idea_heldbelief_insert(x_world, x_atom)


def _modify_world_charunit(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_world_charunit_delete(x_world, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_world_charunit_update(x_world, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_world_charunit_insert(x_world, x_atom)


def modify_world_with_atomunit(x_world: WorldUnit, x_atom: AtomUnit):
    if x_atom.category == "worldunit":
        _modify_world_worldunit(x_world, x_atom)
    elif x_atom.category == "world_beliefunit":
        _modify_world_beliefunit(x_world, x_atom)
    elif x_atom.category == "world_char_beliefhold":
        _modify_world_char_beliefhold(x_world, x_atom)
    elif x_atom.category == "world_ideaunit":
        _modify_world_ideaunit(x_world, x_atom)
    elif x_atom.category == "world_idea_fiscallink":
        _modify_world_idea_fiscallink(x_world, x_atom)
    elif x_atom.category == "world_idea_factunit":
        _modify_world_idea_factunit(x_world, x_atom)
    elif x_atom.category == "world_idea_reasonunit":
        _modify_world_idea_reasonunit(x_world, x_atom)
    elif x_atom.category == "world_idea_reason_premiseunit":
        _modify_world_idea_reason_premiseunit(x_world, x_atom)
    elif x_atom.category == "world_idea_heldbelief":
        _modify_world_idea_heldbelief(x_world, x_atom)
    elif x_atom.category == "world_charunit":
        _modify_world_charunit(x_world, x_atom)


def optional_args_different(category: str, x_obj: any, y_obj: any) -> bool:
    if category == "worldunit":
        return (
            x_obj._weight != y_obj._weight
            or x_obj._max_tree_traverse != y_obj._max_tree_traverse
            or x_obj._meld_strategy != y_obj._meld_strategy
            or x_obj._char_credor_pool != y_obj._char_credor_pool
            or x_obj._char_debtor_pool != y_obj._char_debtor_pool
            or x_obj._pixel != y_obj._pixel
        )
    elif category in {"world_char_beliefhold", "world_idea_fiscallink"}:
        return (x_obj.credor_weight != y_obj.credor_weight) or (
            x_obj.debtor_weight != y_obj.debtor_weight
        )
    elif category == "world_ideaunit":
        return (
            x_obj._addin != y_obj._addin
            or x_obj._begin != y_obj._begin
            or x_obj._close != y_obj._close
            or x_obj._denom != y_obj._denom
            or x_obj._meld_strategy != y_obj._meld_strategy
            or x_obj._numeric_road != y_obj._numeric_road
            or x_obj._numor != y_obj._numor
            or x_obj._range_source_road != y_obj._range_source_road
            or x_obj._reest != y_obj._reest
            or x_obj._weight != y_obj._weight
            or x_obj.pledge != y_obj.pledge
        )
    elif category == "world_idea_factunit":
        return (
            (x_obj.pick != y_obj.pick)
            or (x_obj.open != y_obj.open)
            or (x_obj.nigh != y_obj.nigh)
        )
    elif category == "world_idea_reasonunit":
        return x_obj.base_idea_active_requisite != y_obj.base_idea_active_requisite
    elif category == "world_idea_reason_premiseunit":
        return (
            x_obj.open != y_obj.open
            or x_obj.nigh != y_obj.nigh
            or x_obj.divisor != y_obj.divisor
        )
    elif category == "world_charunit":
        return (x_obj.credor_weight != y_obj.credor_weight) or (
            x_obj.debtor_weight != y_obj.debtor_weight
        )


class InvalidAtomUnitException(Exception):
    pass


def get_atomunit_from_rowdata(x_rowdata: RowData) -> AtomUnit:
    category_text, crud_text = get_category_from_dict(x_rowdata.row_dict)
    x_atom = atomunit_shop(category=category_text, crud_text=crud_text)
    front_len = len(category_text) + len(crud_text) + 2
    for x_columnname, x_value in x_rowdata.row_dict.items():
        arg_key = x_columnname[front_len:]
        x_atom.set_arg(x_key=arg_key, x_value=x_value)
    return x_atom
