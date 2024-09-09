from src._instrument.python_tool import (
    get_empty_dict_if_none,
    get_json_from_dict,
    get_dict_from_json,
)
from src._instrument.db_tool import create_insert_sqlstr, RowData
from src._road.road import create_road, RoadNode, RoadUnit, GroupID, AcctID, is_roadnode
from src.bud.reason_idea import factunit_shop
from src.bud.acct import acctunit_shop
from src.bud.group import awardlink_shop
from src.bud.idea import ideaunit_shop
from src.bud.bud import BudUnit
from src.bud.bud_tool import (
    bud_attr_exists,
    budunit_text,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text,
    bud_idea_teamlink_text,
    bud_idea_healerlink_text,
    bud_idea_factunit_text,
    bud_get_obj,
)
from src.gift.atom_config import (
    get_category_from_dict,
    get_atom_config_required_args,
    category_ref,
    atom_delete,
    atom_insert,
    atom_update,
    atom_hx_table_name,
    get_atom_order,
    get_atom_config_dict,
    is_category_ref,
    get_atom_config_args,
    get_sorted_required_arg_keys,
    get_atom_args_python_types,
    nesting_order_str,
    required_args_text,
    optional_args_text,
    category_text,
    crud_text_str,
    acct_id_str,
    group_id_str,
    healer_id_str,
    parent_road_str,
    road_str,
    label_str,
    pledge_str,
    addin_str,
    begin_str,
    close_str,
    denom_str,
    numor_str,
    morph_str,
    gogo_want_str,
    stop_want_str,
    mass_str,
    credit_vote_str,
    debtit_vote_str,
    credit_belief_str,
    debtit_belief_str,
    fopen_str,
    fnigh_str,
    base_idea_active_requisite_str,
    CRUD_command,
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
            for required_arg in get_sorted_required_arg_keys(self.category)
        ]
        x_columns.extend(
            f"{self.category}_{self.crud_text}_{optional_arg}"
            for optional_arg in self.optional_args.keys()
        )
        x_values = self.get_nesting_order_args()
        x_values.extend(iter(self.optional_args.values()))
        return create_insert_sqlstr(atom_hx_table_name(), x_columns, x_values)

    def get_all_args_in_list(self):
        x_list = self.get_nesting_order_args()
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
        return self._get_category_dict().get(required_args_text())

    def _get_optional_args_dict(self) -> dict:
        x_key = optional_args_text()
        return get_empty_dict_if_none(self._get_category_dict().get(x_key))

    def get_nesting_order_args(self) -> list[str]:
        # When ChangUnit places an AtomUnit in a nested dictionary ChangUnit.atomunits
        # the order of required argments decides the location. The order must always be
        # the same
        sorted_required_arg_keys = get_sorted_required_arg_keys(self.category)
        return [
            self.required_args.get(required_arg)
            for required_arg in sorted_required_arg_keys
        ]

    def is_required_args_valid(self) -> bool:
        if self.crud_text not in {atom_delete(), atom_insert(), atom_update()}:
            return False
        required_args_dict = self._get_required_args_dict()
        return required_args_dict.keys() == self.required_args.keys()

    def is_optional_args_valid(self) -> bool:
        if self.crud_text == atom_delete() and self.optional_args == {}:
            return True
        if self.crud_text not in {atom_insert(), atom_update()}:
            return False
        optional_args_dict = self._get_optional_args_dict()
        return set(self.optional_args.keys()).issubset(set(optional_args_dict.keys()))

    def is_valid(self) -> bool:
        return (
            self.is_required_args_valid()
            and self.is_optional_args_valid()
            and (self.required_args != {} or self.optional_args != {})
        )

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
        return {
            category_text(): self.category,
            crud_text_str(): self.crud_text,
            required_args_text(): required_args_dict,
            optional_args_text(): optional_args_dict,
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
    x_atom = atomunit_shop(x_dict[category_text()], x_dict[crud_text_str()])
    for x_key, x_value in x_dict[required_args_text()].items():
        x_atom.set_required_arg(x_key, x_value)
    for x_key, x_value in x_dict[optional_args_text()].items():
        x_atom.set_optional_arg(x_key, x_value)
    return x_atom


def _modify_bud_update_budunit(x_bud: BudUnit, x_atom: AtomUnit):
    x_arg = "max_tree_traverse"
    if x_atom.get_value(x_arg) is not None:
        x_bud.set_max_tree_traverse(x_atom.get_value(x_arg))
    x_arg = "credor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_bud.set_credor_respect(x_atom.get_value(x_arg))
    x_arg = "debtor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_bud.set_debtor_respect(x_atom.get_value(x_arg))
    x_arg = "fund_pool"
    if x_atom.get_value(x_arg) is not None:
        x_bud._fund_pool = x_atom.get_value(x_arg)
    x_arg = "fund_coin"
    if x_atom.get_value(x_arg) is not None:
        x_bud._fund_coin = x_atom.get_value(x_arg)
    x_arg = "tally"
    if x_atom.get_value(x_arg) is not None:
        x_bud._tally = x_atom.get_value(x_arg)
    x_arg = "bit"
    if x_atom.get_value(x_arg) is not None:
        x_bud._bit = x_atom.get_value(x_arg)
    x_arg = "penny"
    if x_atom.get_value(x_arg) is not None:
        x_bud._penny = x_atom.get_value(x_arg)


def _modify_bud_acct_membership_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_acct_id = x_atom.get_value(acct_id_str())
    x_group_id = x_atom.get_value(group_id_str())
    x_bud.get_acct(x_acct_id).delete_membership(x_group_id)


def _modify_bud_acct_membership_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_acct_id = x_atom.get_value(acct_id_str())
    x_group_id = x_atom.get_value(group_id_str())
    x_acctunit = x_bud.get_acct(x_acct_id)
    x_membership = x_acctunit.get_membership(x_group_id)
    x_credit_vote = x_atom.get_value(credit_vote_str())
    x_debtit_vote = x_atom.get_value(debtit_vote_str())
    x_membership.set_credit_vote(x_credit_vote)
    x_membership.set_debtit_vote(x_debtit_vote)


def _modify_bud_acct_membership_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_acct_id = x_atom.get_value(acct_id_str())
    x_group_id = x_atom.get_value(group_id_str())
    x_credit_vote = x_atom.get_value(credit_vote_str())
    x_debtit_vote = x_atom.get_value(debtit_vote_str())
    x_acctunit = x_bud.get_acct(x_acct_id)
    x_acctunit.add_membership(x_group_id, x_credit_vote, x_debtit_vote)


def _modify_bud_ideaunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    idea_road = create_road(
        x_atom.get_value(parent_road_str()),
        x_atom.get_value(label_str()),
        delimiter=x_bud._road_delimiter,
    )
    x_bud.del_idea_obj(idea_road, del_children=x_atom.get_value("del_children"))


def _modify_bud_ideaunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    idea_road = create_road(
        x_atom.get_value(parent_road_str()),
        x_atom.get_value(label_str()),
        delimiter=x_bud._road_delimiter,
    )
    x_bud.edit_idea_attr(
        road=idea_road,
        addin=x_atom.get_value(addin_str()),
        begin=x_atom.get_value(begin_str()),
        gogo_want=x_atom.get_value(gogo_want_str()),
        stop_want=x_atom.get_value(stop_want_str()),
        close=x_atom.get_value(close_str()),
        denom=x_atom.get_value(denom_str()),
        numor=x_atom.get_value(numor_str()),
        morph=x_atom.get_value(morph_str()),
        mass=x_atom.get_value(mass_str()),
        pledge=x_atom.get_value(pledge_str()),
    )


def _modify_bud_ideaunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.set_idea(
        idea_kid=ideaunit_shop(
            _label=x_atom.get_value(label_str()),
            addin=x_atom.get_value(addin_str()),
            _begin=x_atom.get_value(begin_str()),
            _close=x_atom.get_value(close_str()),
            _gogo_want=x_atom.get_value(gogo_want_str()),
            _stop_want=x_atom.get_value(stop_want_str()),
            _denom=x_atom.get_value(denom_str()),
            _numor=x_atom.get_value(numor_str()),
            pledge=x_atom.get_value(pledge_str()),
        ),
        parent_road=x_atom.get_value(parent_road_str()),
        create_missing_ideas=False,
        filter_out_missing_awardlinks_group_ids=False,
        create_missing_ancestors=False,
    )


def _modify_bud_idea_awardlink_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_idea_attr(
        road=x_atom.get_value("road"),
        awardlink_del=x_atom.get_value(group_id_str()),
    )


def _modify_bud_idea_awardlink_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_idea = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_awardlink = x_idea._awardlinks.get(x_atom.get_value(group_id_str()))
    x_give_force = x_atom.get_value("give_force")
    if x_give_force is not None and x_awardlink.give_force != x_give_force:
        x_awardlink.give_force = x_give_force
    x_take_force = x_atom.get_value("take_force")
    if x_take_force is not None and x_awardlink.take_force != x_take_force:
        x_awardlink.take_force = x_take_force
    x_bud.edit_idea_attr(x_atom.get_value("road"), awardlink=x_awardlink)


def _modify_bud_idea_awardlink_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_awardlink = awardlink_shop(
        group_id=x_atom.get_value(group_id_str()),
        give_force=x_atom.get_value("give_force"),
        take_force=x_atom.get_value("take_force"),
    )
    x_bud.edit_idea_attr(x_atom.get_value("road"), awardlink=x_awardlink)


def _modify_bud_idea_factunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit.del_factunit(x_atom.get_value("base"))


def _modify_bud_idea_factunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_factunit = x_ideaunit._factunits.get(x_atom.get_value("base"))
    x_factunit.set_attr(
        pick=x_atom.get_value("pick"),
        fopen=x_atom.get_value(fopen_str()),
        fnigh=x_atom.get_value(fnigh_str()),
    )
    # x_ideaunit.set_factunit(x_factunit)


def _modify_bud_idea_factunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_idea_attr(
        road=x_atom.get_value("road"),
        factunit=factunit_shop(
            base=x_atom.get_value("base"),
            pick=x_atom.get_value("pick"),
            fopen=x_atom.get_value(fopen_str()),
            fnigh=x_atom.get_value(fnigh_str()),
        ),
    )


def _modify_bud_idea_reasonunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit.del_reasonunit_base(x_atom.get_value("base"))


def _modify_bud_idea_reasonunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_idea_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_base_idea_active_requisite=x_atom.get_value(
            base_idea_active_requisite_str()
        ),
    )


def _modify_bud_idea_reasonunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_idea_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_base_idea_active_requisite=x_atom.get_value(
            base_idea_active_requisite_str()
        ),
    )


def _modify_bud_idea_reason_premiseunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_idea_attr(
        road=x_atom.get_value("road"),
        reason_del_premise_base=x_atom.get_value("base"),
        reason_del_premise_need=x_atom.get_value("need"),
    )


def _modify_bud_idea_reason_premiseunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_idea_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_premise=x_atom.get_value("need"),
        reason_premise_open=x_atom.get_value("open"),
        reason_premise_nigh=x_atom.get_value("nigh"),
        reason_premise_divisor=x_atom.get_value("divisor"),
    )


def _modify_bud_idea_reason_premiseunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit.set_reason_premise(
        base=x_atom.get_value("base"),
        premise=x_atom.get_value("need"),
        open=x_atom.get_value("open"),
        nigh=x_atom.get_value("nigh"),
        divisor=x_atom.get_value("divisor"),
    )


def _modify_bud_idea_teamlink_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit._teamunit.del_teamlink(group_id=x_atom.get_value(group_id_str()))


def _modify_bud_idea_teamlink_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit._teamunit.set_teamlink(group_id=x_atom.get_value(group_id_str()))


def _modify_bud_idea_healerlink_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit._healerlink.del_healer_id(x_atom.get_value(healer_id_str()))


def _modify_bud_idea_healerlink_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit._healerlink.set_healer_id(x_atom.get_value(healer_id_str()))


def _modify_bud_acctunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.del_acctunit(x_atom.get_value(acct_id_str()))


def _modify_bud_acctunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_acctunit(
        acct_id=x_atom.get_value(acct_id_str()),
        credit_belief=x_atom.get_value(credit_belief_str()),
        debtit_belief=x_atom.get_value(debtit_belief_str()),
    )


def _modify_bud_acctunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.set_acctunit(
        acctunit_shop(
            acct_id=x_atom.get_value(acct_id_str()),
            credit_belief=x_atom.get_value(credit_belief_str()),
            debtit_belief=x_atom.get_value(debtit_belief_str()),
        )
    )


def _modify_bud_budunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_update():
        _modify_bud_update_budunit(x_bud, x_atom)


def _modify_bud_acct_membership(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_acct_membership_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_bud_acct_membership_update(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_acct_membership_insert(x_bud, x_atom)


def _modify_bud_ideaunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_ideaunit_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_bud_ideaunit_update(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_ideaunit_insert(x_bud, x_atom)


def _modify_bud_idea_awardlink(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_idea_awardlink_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_bud_idea_awardlink_update(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_idea_awardlink_insert(x_bud, x_atom)


def _modify_bud_idea_factunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_idea_factunit_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_bud_idea_factunit_update(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_idea_factunit_insert(x_bud, x_atom)


def _modify_bud_idea_reasonunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_idea_reasonunit_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_bud_idea_reasonunit_update(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_idea_reasonunit_insert(x_bud, x_atom)


def _modify_bud_idea_reason_premiseunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_idea_reason_premiseunit_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_bud_idea_reason_premiseunit_update(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_idea_reason_premiseunit_insert(x_bud, x_atom)


def _modify_bud_idea_teamlink(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_idea_teamlink_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_idea_teamlink_insert(x_bud, x_atom)


def _modify_bud_idea_healerlink(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_idea_healerlink_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_idea_healerlink_insert(x_bud, x_atom)


def _modify_bud_acctunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_acctunit_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_bud_acctunit_update(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_acctunit_insert(x_bud, x_atom)


def modify_bud_with_atomunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.category == budunit_text():
        _modify_bud_budunit(x_bud, x_atom)
    elif x_atom.category == bud_acct_membership_text():
        _modify_bud_acct_membership(x_bud, x_atom)
    elif x_atom.category == bud_ideaunit_text():
        _modify_bud_ideaunit(x_bud, x_atom)
    elif x_atom.category == bud_idea_awardlink_text():
        _modify_bud_idea_awardlink(x_bud, x_atom)
    elif x_atom.category == bud_idea_factunit_text():
        _modify_bud_idea_factunit(x_bud, x_atom)
    elif x_atom.category == bud_idea_reasonunit_text():
        _modify_bud_idea_reasonunit(x_bud, x_atom)
    elif x_atom.category == bud_idea_reason_premiseunit_text():
        _modify_bud_idea_reason_premiseunit(x_bud, x_atom)
    elif x_atom.category == bud_idea_healerlink_text():
        _modify_bud_idea_healerlink(x_bud, x_atom)
    elif x_atom.category == bud_idea_teamlink_text():
        _modify_bud_idea_teamlink(x_bud, x_atom)
    elif x_atom.category == bud_acctunit_text():
        _modify_bud_acctunit(x_bud, x_atom)


def optional_args_different(category: str, x_obj: any, y_obj: any) -> bool:
    if category == budunit_text():
        return (
            x_obj._tally != y_obj._tally
            or x_obj._max_tree_traverse != y_obj._max_tree_traverse
            or x_obj._credor_respect != y_obj._credor_respect
            or x_obj._debtor_respect != y_obj._debtor_respect
            or x_obj._bit != y_obj._bit
            or x_obj._fund_pool != y_obj._fund_pool
            or x_obj._fund_coin != y_obj._fund_coin
        )
    elif category in {bud_acct_membership_text()}:
        return (x_obj.credit_vote != y_obj.credit_vote) or (
            x_obj.debtit_vote != y_obj.debtit_vote
        )
    elif category in {bud_idea_awardlink_text()}:
        return (x_obj.give_force != y_obj.give_force) or (
            x_obj.take_force != y_obj.take_force
        )
    elif category == bud_ideaunit_text():
        return (
            x_obj.addin != y_obj.addin
            or x_obj._begin != y_obj._begin
            or x_obj._close != y_obj._close
            or x_obj._denom != y_obj._denom
            or x_obj._numor != y_obj._numor
            or x_obj._morph != y_obj._morph
            or x_obj.mass != y_obj.mass
            or x_obj.pledge != y_obj.pledge
        )
    elif category == bud_idea_factunit_text():
        return (
            (x_obj.pick != y_obj.pick)
            or (x_obj.open != y_obj.open)
            or (x_obj.nigh != y_obj.nigh)
        )
    elif category == bud_idea_reasonunit_text():
        return x_obj.base_idea_active_requisite != y_obj.base_idea_active_requisite
    elif category == bud_idea_reason_premiseunit_text():
        return (
            x_obj.open != y_obj.open
            or x_obj.nigh != y_obj.nigh
            or x_obj.divisor != y_obj.divisor
        )
    elif category == bud_acctunit_text():
        return (x_obj.credit_belief != y_obj.credit_belief) or (
            x_obj.debtit_belief != y_obj.debtit_belief
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


@dataclass
class AtomRow:
    _atom_categorys: set[str] = None
    _crud_command: CRUD_command = None
    acct_id: AcctID = None
    addin: float = None
    base: RoadUnit = None
    base_idea_active_requisite: bool = None
    begin: float = None
    bit: float = None
    close: float = None
    credit_belief: int = None
    credit_vote: int = None
    credor_respect: int = None
    debtit_belief: int = None
    debtit_vote: int = None
    debtor_respect: int = None
    denom: int = None
    divisor: int = None
    fnigh: float = None
    fopen: float = None
    fund_coin: float = None
    fund_pool: float = None
    give_force: float = None
    gogo_want: float = None
    group_id: GroupID = None
    healer_id: GroupID = None
    label: RoadNode = None
    mass: int = None
    max_tree_traverse: int = None
    monetary_desc: str = None
    morph: bool = None
    need: RoadUnit = None
    nigh: float = None
    numor: int = None
    open: float = None
    parent_road: RoadUnit = None
    penny: float = None
    pick: RoadUnit = None
    pledge: bool = None
    problem_bool: bool = None
    road: RoadUnit = None
    stop_want: float = None
    take_force: float = None
    tally: int = None

    def set_atom_category(self, atom_category: str):
        self._atom_categorys.add(atom_category)

    def atom_category_exists(self, atom_category: str) -> bool:
        return atom_category in self._atom_categorys

    def delete_atom_category(self, atom_category: str):
        self._atom_categorys.remove(atom_category)

    def _set_python_types(self):
        for x_arg, python_type in get_atom_args_python_types().items():
            x_value = self.__dict__.get(x_arg)
            if x_value != None:
                if python_type == "AcctID":
                    self.__dict__[x_arg] = AcctID(x_value)
                elif python_type == "GroupID":
                    self.__dict__[x_arg] = GroupID(x_value)
                elif python_type == "RoadUnit":
                    self.__dict__[x_arg] = RoadUnit(x_value)
                elif python_type == "RoadNode":
                    self.__dict__[x_arg] = RoadNode(x_value)
                elif python_type == "str":
                    self.__dict__[x_arg] = str(x_value)
                elif python_type == "bool":
                    self.__dict__[x_arg] = bool(x_value)
                elif python_type == "int":
                    self.__dict__[x_arg] = int(x_value)
                elif python_type == "float":
                    self.__dict__[x_arg] = float(x_value)
        if self.label != None and self.parent_road != None and self.road == None:
            self.road = create_road(self.parent_road, self.label)

    def get_atomunits(self) -> list[AtomUnit]:
        self._set_python_types()
        x_list = []
        for x_category in self._atom_categorys:
            x_atom = atomunit_shop(x_category, self._crud_command)
            x_args = get_atom_config_args(x_category)
            for x_arg in x_args:
                if self.__dict__[x_arg] != None:
                    x_atom.set_arg(x_arg, self.__dict__[x_arg])
            if x_atom.is_valid() > 0:
                x_list.append(x_atom)
        return x_list


def atomrow_shop(atom_categorys: set[str], crud_command: CRUD_command) -> AtomRow:
    return AtomRow(_atom_categorys=atom_categorys, _crud_command=crud_command)


def sift_atomunit(x_bud: BudUnit, x_atom: AtomUnit) -> AtomUnit:
    x_category = x_atom.category
    config_req_args = get_atom_config_required_args(x_category)
    x_atom_reqs = {req_arg: x_atom.get_value(req_arg) for req_arg in config_req_args}
    x_parent_road = x_atom_reqs.get(parent_road_str())
    x_label = x_atom_reqs.get(label_str())
    if x_parent_road != None and x_label != None:
        x_atom_reqs[road_str()] = x_bud.make_road(x_parent_road, x_label)
        x_road_delimiter = x_bud._road_delimiter
        is_idearoot_road = is_roadnode(x_atom_reqs.get(road_str()), x_road_delimiter)
        if is_idearoot_road is True:
            return None

    x_exists = bud_attr_exists(x_category, x_bud, x_atom_reqs)
    print(f"{x_atom.crud_text=} {x_exists=}")

    if x_atom.crud_text == atom_delete() and x_exists:
        return x_atom
    elif x_atom.crud_text == atom_insert() and not x_exists:
        return x_atom
    elif x_atom.crud_text == atom_insert() and x_exists:
        x_bud_obj = bud_get_obj(x_category, x_bud, x_atom_reqs)
        x_optional_args = x_atom.get_optional_args_dict()
        update_atom = atomunit_shop(x_category, atom_update(), x_atom.required_args)
        for optional_arg in x_optional_args:
            optional_value = x_atom.get_value(optional_arg)
            if x_bud_obj.__dict__.get(optional_arg) != optional_value:
                update_atom.set_arg(optional_arg, optional_value)

        if update_atom.get_optional_args_dict() != {}:
            print(f"{update_atom=}")
            return update_atom
    return None
