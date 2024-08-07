from src._instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    get_dict_from_json,
)
from src._instrument.db_tool import create_insert_sqlstr, RowData
from src._road.road import create_road
from src.bud.reason_idea import factunit_shop
from src.bud.acct import acctunit_shop
from src.bud.group import awardlink_shop
from src.bud.idea import ideaunit_shop
from src.bud.bud import BudUnit
from src.gift.atom_config import (
    get_category_from_dict,
    atom_delete,
    atom_insert,
    atom_update,
    atom_hx_table_name,
    get_atom_order,
    get_atom_config_dict,
    is_category_ref,
    get_sorted_required_arg_keys,
    nesting_order_str,
    required_args_text,
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
        return self._get_category_dict().get("required_args")

    def _get_optional_args_dict(self) -> dict:
        return get_empty_dict_if_none(self._get_category_dict().get("optional_args"))

    def get_nesting_order_args(self) -> list[str]:
        # When ChangUnit places an AtomUnit in a nested dictionary ChangUnit.atomunits
        # the order of required argments decides the location. The order must always be
        # the same
        sorted_required_arg_keys = get_sorted_required_arg_keys(self.category)
        sorted_required_arg_values = []
        for required_arg in sorted_required_arg_keys:
            sorted_required_arg_values.append(self.required_args.get(required_arg))
        return sorted_required_arg_values

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


def _modify_bud_update_budunit(x_bud: BudUnit, x_atom: AtomUnit):
    x_arg = "_max_tree_traverse"
    if x_atom.get_value(x_arg) is not None:
        x_bud.set_max_tree_traverse(x_atom.get_value(x_arg))
    x_arg = "_credor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_bud.set_credor_respect(x_atom.get_value(x_arg))
    x_arg = "_debtor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_bud.set_debtor_respect(x_atom.get_value(x_arg))
    x_arg = "_fund_pool"
    if x_atom.get_value(x_arg) is not None:
        x_bud._fund_pool = x_atom.get_value(x_arg)
    x_arg = "_fund_coin"
    if x_atom.get_value(x_arg) is not None:
        x_bud._fund_coin = x_atom.get_value(x_arg)
    x_arg = "_tally"
    if x_atom.get_value(x_arg) is not None:
        x_bud._tally = x_atom.get_value(x_arg)
    x_arg = "_bit"
    if x_atom.get_value(x_arg) is not None:
        x_bud._bit = x_atom.get_value(x_arg)
    x_arg = "_penny"
    if x_atom.get_value(x_arg) is not None:
        x_bud._penny = x_atom.get_value(x_arg)


def _modify_bud_acct_membership_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_acct_id = x_atom.get_value("acct_id")
    x_group_id = x_atom.get_value("group_id")
    x_bud.get_acct(x_acct_id).delete_membership(x_group_id)


def _modify_bud_acct_membership_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_acct_id = x_atom.get_value("acct_id")
    x_group_id = x_atom.get_value("group_id")
    x_acctunit = x_bud.get_acct(x_acct_id)
    x_membership = x_acctunit.get_membership(x_group_id)
    x_credit_vote = x_atom.get_value("credit_vote")
    x_debtit_vote = x_atom.get_value("debtit_vote")
    x_membership.set_credit_vote(x_credit_vote)
    x_membership.set_debtit_vote(x_debtit_vote)


def _modify_bud_acct_membership_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_acct_id = x_atom.get_value("acct_id")
    x_group_id = x_atom.get_value("group_id")
    x_credit_vote = x_atom.get_value("credit_vote")
    x_debtit_vote = x_atom.get_value("debtit_vote")
    x_acctunit = x_bud.get_acct(x_acct_id)
    x_acctunit.add_membership(x_group_id, x_credit_vote, x_debtit_vote)


def _modify_bud_ideaunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    idea_road = create_road(
        x_atom.get_value("parent_road"),
        x_atom.get_value("label"),
        delimiter=x_bud._road_delimiter,
    )
    x_bud.del_idea_obj(idea_road, del_children=x_atom.get_value("del_children"))


def _modify_bud_ideaunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    idea_road = create_road(
        x_atom.get_value("parent_road"),
        x_atom.get_value("label"),
        delimiter=x_bud._road_delimiter,
    )
    x_bud.edit_idea_attr(
        road=idea_road,
        addin=x_atom.get_value("_addin"),
        begin=x_atom.get_value("_begin"),
        close=x_atom.get_value("_close"),
        denom=x_atom.get_value("_denom"),
        numeric_road=x_atom.get_value("_numeric_road"),
        numor=x_atom.get_value("_numor"),
        range_source_road=x_atom.get_value("_range_source_road"),
        reest=x_atom.get_value("_reest"),
        mass=x_atom.get_value("_mass"),
        pledge=x_atom.get_value("pledge"),
    )


def _modify_bud_ideaunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.set_idea(
        idea_kid=ideaunit_shop(
            _label=x_atom.get_value("label"),
            _addin=x_atom.get_value("_addin"),
            _begin=x_atom.get_value("_begin"),
            _close=x_atom.get_value("_close"),
            _denom=x_atom.get_value("_denom"),
            _numeric_road=x_atom.get_value("_numeric_road"),
            _numor=x_atom.get_value("_numor"),
            pledge=x_atom.get_value("pledge"),
        ),
        parent_road=x_atom.get_value("parent_road"),
        create_missing_ideas=False,
        filter_out_missing_awardlinks_group_ids=False,
        create_missing_ancestors=False,
    )


def _modify_bud_idea_awardlink_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_idea_attr(
        road=x_atom.get_value("road"),
        awardlink_del=x_atom.get_value("group_id"),
    )


def _modify_bud_idea_awardlink_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_idea = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_awardlink = x_idea._awardlinks.get(x_atom.get_value("group_id"))
    x_give_force = x_atom.get_value("give_force")
    if x_give_force is not None and x_awardlink.give_force != x_give_force:
        x_awardlink.give_force = x_give_force
    x_take_force = x_atom.get_value("take_force")
    if x_take_force is not None and x_awardlink.take_force != x_take_force:
        x_awardlink.take_force = x_take_force
    x_bud.edit_idea_attr(x_atom.get_value("road"), awardlink=x_awardlink)


def _modify_bud_idea_awardlink_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_awardlink = awardlink_shop(
        group_id=x_atom.get_value("group_id"),
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
        open=x_atom.get_value("open"),
        nigh=x_atom.get_value("nigh"),
    )
    # x_ideaunit.set_factunit(x_factunit)


def _modify_bud_idea_factunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_idea_attr(
        road=x_atom.get_value("road"),
        factunit=factunit_shop(
            base=x_atom.get_value("base"),
            pick=x_atom.get_value("pick"),
            open=x_atom.get_value("open"),
            nigh=x_atom.get_value("nigh"),
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
            "base_idea_active_requisite"
        ),
    )


def _modify_bud_idea_reasonunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_idea_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_base_idea_active_requisite=x_atom.get_value(
            "base_idea_active_requisite"
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


def _modify_bud_idea_grouphold_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit._doerunit.del_grouphold(group_id=x_atom.get_value("group_id"))


def _modify_bud_idea_grouphold_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_ideaunit = x_bud.get_idea_obj(x_atom.get_value("road"))
    x_ideaunit._doerunit.set_grouphold(group_id=x_atom.get_value("group_id"))


def _modify_bud_acctunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.del_acctunit(x_atom.get_value("acct_id"))


def _modify_bud_acctunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_acctunit(
        acct_id=x_atom.get_value("acct_id"),
        credit_score=x_atom.get_value("credit_score"),
        debtit_score=x_atom.get_value("debtit_score"),
    )


def _modify_bud_acctunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.set_acctunit(
        acctunit_shop(
            acct_id=x_atom.get_value("acct_id"),
            credit_score=x_atom.get_value("credit_score"),
            debtit_score=x_atom.get_value("debtit_score"),
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


def _modify_bud_idea_grouphold(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_idea_grouphold_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_idea_grouphold_insert(x_bud, x_atom)


def _modify_bud_acctunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_text == atom_delete():
        _modify_bud_acctunit_delete(x_bud, x_atom)
    elif x_atom.crud_text == atom_update():
        _modify_bud_acctunit_update(x_bud, x_atom)
    elif x_atom.crud_text == atom_insert():
        _modify_bud_acctunit_insert(x_bud, x_atom)


def modify_bud_with_atomunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.category == "budunit":
        _modify_bud_budunit(x_bud, x_atom)
    elif x_atom.category == "bud_acct_membership":
        _modify_bud_acct_membership(x_bud, x_atom)
    elif x_atom.category == "bud_ideaunit":
        _modify_bud_ideaunit(x_bud, x_atom)
    elif x_atom.category == "bud_idea_awardlink":
        _modify_bud_idea_awardlink(x_bud, x_atom)
    elif x_atom.category == "bud_idea_factunit":
        _modify_bud_idea_factunit(x_bud, x_atom)
    elif x_atom.category == "bud_idea_reasonunit":
        _modify_bud_idea_reasonunit(x_bud, x_atom)
    elif x_atom.category == "bud_idea_reason_premiseunit":
        _modify_bud_idea_reason_premiseunit(x_bud, x_atom)
    elif x_atom.category == "bud_idea_grouphold":
        _modify_bud_idea_grouphold(x_bud, x_atom)
    elif x_atom.category == "bud_acctunit":
        _modify_bud_acctunit(x_bud, x_atom)


def optional_args_different(category: str, x_obj: any, y_obj: any) -> bool:
    if category == "budunit":
        return (
            x_obj._tally != y_obj._tally
            or x_obj._max_tree_traverse != y_obj._max_tree_traverse
            or x_obj._credor_respect != y_obj._credor_respect
            or x_obj._debtor_respect != y_obj._debtor_respect
            or x_obj._bit != y_obj._bit
            or x_obj._fund_pool != y_obj._fund_pool
            or x_obj._fund_coin != y_obj._fund_coin
        )
    elif category in {"bud_acct_membership"}:
        return (x_obj.credit_vote != y_obj.credit_vote) or (
            x_obj.debtit_vote != y_obj.debtit_vote
        )
    elif category in {"bud_idea_awardlink"}:
        return (x_obj.give_force != y_obj.give_force) or (
            x_obj.take_force != y_obj.take_force
        )
    elif category == "bud_ideaunit":
        return (
            x_obj._addin != y_obj._addin
            or x_obj._begin != y_obj._begin
            or x_obj._close != y_obj._close
            or x_obj._denom != y_obj._denom
            or x_obj._numeric_road != y_obj._numeric_road
            or x_obj._numor != y_obj._numor
            or x_obj._range_source_road != y_obj._range_source_road
            or x_obj._reest != y_obj._reest
            or x_obj._mass != y_obj._mass
            or x_obj.pledge != y_obj.pledge
        )
    elif category == "bud_idea_factunit":
        return (
            (x_obj.pick != y_obj.pick)
            or (x_obj.open != y_obj.open)
            or (x_obj.nigh != y_obj.nigh)
        )
    elif category == "bud_idea_reasonunit":
        return x_obj.base_idea_active_requisite != y_obj.base_idea_active_requisite
    elif category == "bud_idea_reason_premiseunit":
        return (
            x_obj.open != y_obj.open
            or x_obj.nigh != y_obj.nigh
            or x_obj.divisor != y_obj.divisor
        )
    elif category == "bud_acctunit":
        return (x_obj.credit_score != y_obj.credit_score) or (
            x_obj.debtit_score != y_obj.debtit_score
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
