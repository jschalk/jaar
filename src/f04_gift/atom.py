from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_None,
    get_json_from_dict,
    get_dict_from_json,
)
from src.f00_instrument.db_toolbox import create_insert_sqlstr, RowData
from src.f01_road.finance import TimeLinePoint
from src.f01_road.road import (
    create_road,
    TitleUnit,
    RoadUnit,
    GroupLabel,
    AcctName,
    is_titleunit,
)
from src.f02_bud.reason_item import factunit_shop
from src.f02_bud.acct import acctunit_shop
from src.f02_bud.group import awardlink_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import BudUnit
from src.f02_bud.bud_tool import bud_attr_exists, bud_get_obj
from src.f04_gift.atom_config import (
    get_dimen_from_dict,
    get_atom_config_jkeys,
    atom_delete,
    atom_insert,
    atom_update,
    atom_hx_table_name,
    get_atom_order,
    get_atom_config_dict,
    is_bud_dimen,
    get_atom_config_args,
    get_sorted_jkey_keys,
    get_atom_args_class_types,
    CRUD_command,
)
from dataclasses import dataclass


class AtomUnitDescriptionException(Exception):
    pass


@dataclass
class AtomUnit:
    dimen: str = None
    crud_str: str = None
    jkeys: dict[str, str] = None
    jvalues: dict[str, str] = None
    atom_order: int = None

    def get_insert_sqlstr(self) -> str:
        if self.is_valid() is False:
            raise AtomUnitDescriptionException(
                f"Cannot get_insert_sqlstr '{self.dimen}' with is_valid=False."
            )

        x_columns = [
            f"{self.dimen}_{self.crud_str}_{jkey}"
            for jkey in get_sorted_jkey_keys(self.dimen)
        ]
        x_columns.extend(
            f"{self.dimen}_{self.crud_str}_{jvalue}" for jvalue in self.jvalues.keys()
        )
        x_values = self.get_nesting_order_args()
        x_values.extend(iter(self.jvalues.values()))
        return create_insert_sqlstr(atom_hx_table_name(), x_columns, x_values)

    def get_all_args_in_list(self):
        x_list = self.get_nesting_order_args()
        x_list.extend(list(self.jvalues.values()))
        return x_list

    def set_atom_order(self):
        self.atom_order = get_atom_order(self.crud_str, self.dimen)

    def set_arg(self, x_key: str, x_value: any):
        for jkey in self._get_jkeys_dict():
            if x_key == jkey:
                self.set_jkey(x_key, x_value)
        for jvalue in self._get_jvalues_dict():
            if x_key == jvalue:
                self.set_jvalue(x_key, x_value)

    def set_jkey(self, x_key: str, x_value: any):
        self.jkeys[x_key] = x_value

    def set_jvalue(self, x_key: str, x_value: any):
        self.jvalues[x_key] = x_value

    def _get_dimen_dict(self) -> dict:
        return get_atom_config_dict().get(self.dimen)

    def _get_crud_dict(self) -> dict:
        return self._get_dimen_dict().get(self.crud_str)

    def _get_jkeys_dict(self) -> dict:
        return self._get_dimen_dict().get("jkeys")

    def _get_jvalues_dict(self) -> dict:
        x_key = "jvalues"
        return get_empty_dict_if_None(self._get_dimen_dict().get(x_key))

    def get_nesting_order_args(self) -> list[str]:
        # When ChangUnit places an AtomUnit in a nested dictionary ChangUnit.atomunits
        # the order of required argments decides the location. The order must always be
        # the same
        sorted_jkey_keys = get_sorted_jkey_keys(self.dimen)
        return [self.jkeys.get(jkey) for jkey in sorted_jkey_keys]

    def is_jkeys_valid(self) -> bool:
        if self.crud_str not in {atom_delete(), atom_insert(), atom_update()}:
            return False
        jkeys_dict = self._get_jkeys_dict()
        return jkeys_dict.keys() == self.jkeys.keys()

    def is_jvalues_valid(self) -> bool:
        if self.crud_str == atom_delete() and self.jvalues == {}:
            return True
        if self.crud_str not in {atom_insert(), atom_update()}:
            return False
        jvalues_dict = self._get_jvalues_dict()
        return set(self.jvalues.keys()).issubset(set(jvalues_dict.keys()))

    def is_valid(self) -> bool:
        return (
            self.is_jkeys_valid()
            and self.is_jvalues_valid()
            and (self.jkeys != {} or self.jvalues != {})
        )

    def get_value(self, arg_key: str) -> any:
        required_value = self.jkeys.get(arg_key)
        return self.jvalues.get(arg_key) if required_value is None else required_value

    def get_jkeys_dict(self) -> dict[str, str]:
        return dict(self.jkeys.items())

    def get_jvalues_dict(self) -> dict[str, str]:
        return dict(self.jvalues.items())

    def get_dict(self) -> dict[str, str]:
        jkeys_dict = self.get_jkeys_dict()
        jvalues_dict = self.get_jvalues_dict()
        return {
            "dimen": self.dimen,
            "crud": self.crud_str,
            "jkeys": jkeys_dict,
            "jvalues": jvalues_dict,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def atomunit_shop(
    dimen: str,
    crud_str: str = None,
    jkeys: dict[str, str] = None,
    jvalues: dict[str, str] = None,
) -> AtomUnit:
    if is_bud_dimen(dimen):
        return AtomUnit(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=get_empty_dict_if_None(jkeys),
            jvalues=get_empty_dict_if_None(jvalues),
        )


def get_from_json(x_str: str) -> AtomUnit:
    x_dict = get_dict_from_json(x_str)
    x_atom = atomunit_shop(x_dict["dimen"], x_dict["crud"])
    for x_key, x_value in x_dict["jkeys"].items():
        x_atom.set_jkey(x_key, x_value)
    for x_key, x_value in x_dict["jvalues"].items():
        x_atom.set_jvalue(x_key, x_value)
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
        x_bud.fund_pool = x_atom.get_value(x_arg)
    x_arg = "fund_coin"
    if x_atom.get_value(x_arg) is not None:
        x_bud.fund_coin = x_atom.get_value(x_arg)
    x_arg = "tally"
    if x_atom.get_value(x_arg) is not None:
        x_bud.tally = x_atom.get_value(x_arg)
    x_arg = "respect_bit"
    if x_atom.get_value(x_arg) is not None:
        x_bud.respect_bit = x_atom.get_value(x_arg)
    x_arg = "deal_time_int"
    if x_atom.get_value(x_arg) is not None:
        x_bud.deal_time_int = x_atom.get_value(x_arg)
    x_arg = "penny"
    if x_atom.get_value(x_arg) is not None:
        x_bud.penny = x_atom.get_value(x_arg)


def _modify_bud_acct_membership_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_acct_name = x_atom.get_value("acct_name")
    x_group_label = x_atom.get_value("group_label")
    x_bud.get_acct(x_acct_name).delete_membership(x_group_label)


def _modify_bud_acct_membership_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_acct_name = x_atom.get_value("acct_name")
    x_group_label = x_atom.get_value("group_label")
    x_acctunit = x_bud.get_acct(x_acct_name)
    x_membership = x_acctunit.get_membership(x_group_label)
    x_credit_vote = x_atom.get_value("credit_vote")
    x_debtit_vote = x_atom.get_value("debtit_vote")
    x_membership.set_credit_vote(x_credit_vote)
    x_membership.set_debtit_vote(x_debtit_vote)


def _modify_bud_acct_membership_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_acct_name = x_atom.get_value("acct_name")
    x_group_label = x_atom.get_value("group_label")
    x_credit_vote = x_atom.get_value("credit_vote")
    x_debtit_vote = x_atom.get_value("debtit_vote")
    x_acctunit = x_bud.get_acct(x_acct_name)
    x_acctunit.add_membership(x_group_label, x_credit_vote, x_debtit_vote)


def _modify_bud_itemunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    item_road = create_road(
        x_atom.get_value("parent_road"),
        x_atom.get_value("item_title"),
        bridge=x_bud.bridge,
    )
    x_bud.del_item_obj(item_road, del_children=x_atom.get_value("del_children"))


def _modify_bud_itemunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    item_road = create_road(
        x_atom.get_value("parent_road"),
        x_atom.get_value("item_title"),
        bridge=x_bud.bridge,
    )
    x_bud.edit_item_attr(
        road=item_road,
        addin=x_atom.get_value("addin"),
        begin=x_atom.get_value("begin"),
        gogo_want=x_atom.get_value("gogo_want"),
        stop_want=x_atom.get_value("stop_want"),
        close=x_atom.get_value("close"),
        denom=x_atom.get_value("denom"),
        numor=x_atom.get_value("numor"),
        morph=x_atom.get_value("morph"),
        mass=x_atom.get_value("mass"),
        pledge=x_atom.get_value("pledge"),
    )


def _modify_bud_itemunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.set_item(
        item_kid=itemunit_shop(
            _item_title=x_atom.get_value("item_title"),
            addin=x_atom.get_value("addin"),
            begin=x_atom.get_value("begin"),
            close=x_atom.get_value("close"),
            gogo_want=x_atom.get_value("gogo_want"),
            stop_want=x_atom.get_value("stop_want"),
            denom=x_atom.get_value("denom"),
            numor=x_atom.get_value("numor"),
            pledge=x_atom.get_value("pledge"),
        ),
        parent_road=x_atom.get_value("parent_road"),
        create_missing_items=False,
        get_rid_of_missing_awardlinks_awardee_tags=False,
        create_missing_ancestors=False,
    )


def _modify_bud_item_awardlink_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_item_attr(
        road=x_atom.get_value("road"),
        awardlink_del=x_atom.get_value("awardee_tag"),
    )


def _modify_bud_item_awardlink_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_item = x_bud.get_item_obj(x_atom.get_value("road"))
    x_awardlink = x_item.awardlinks.get(x_atom.get_value("awardee_tag"))
    x_give_force = x_atom.get_value("give_force")
    if x_give_force is not None and x_awardlink.give_force != x_give_force:
        x_awardlink.give_force = x_give_force
    x_take_force = x_atom.get_value("take_force")
    if x_take_force is not None and x_awardlink.take_force != x_take_force:
        x_awardlink.take_force = x_take_force
    x_bud.edit_item_attr(x_atom.get_value("road"), awardlink=x_awardlink)


def _modify_bud_item_awardlink_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_awardlink = awardlink_shop(
        awardee_tag=x_atom.get_value("awardee_tag"),
        give_force=x_atom.get_value("give_force"),
        take_force=x_atom.get_value("take_force"),
    )
    x_bud.edit_item_attr(x_atom.get_value("road"), awardlink=x_awardlink)


def _modify_bud_item_factunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_itemunit = x_bud.get_item_obj(x_atom.get_value("road"))
    x_itemunit.del_factunit(x_atom.get_value("base"))


def _modify_bud_item_factunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_itemunit = x_bud.get_item_obj(x_atom.get_value("road"))
    x_factunit = x_itemunit.factunits.get(x_atom.get_value("base"))
    x_factunit.set_attr(
        pick=x_atom.get_value("pick"),
        fopen=x_atom.get_value("fopen"),
        fnigh=x_atom.get_value("fnigh"),
    )
    # x_itemunit.set_factunit(x_factunit)


def _modify_bud_item_factunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_item_attr(
        road=x_atom.get_value("road"),
        factunit=factunit_shop(
            base=x_atom.get_value("base"),
            pick=x_atom.get_value("pick"),
            fopen=x_atom.get_value("fopen"),
            fnigh=x_atom.get_value("fnigh"),
        ),
    )


def _modify_bud_item_reasonunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_itemunit = x_bud.get_item_obj(x_atom.get_value("road"))
    x_itemunit.del_reasonunit_base(x_atom.get_value("base"))


def _modify_bud_item_reasonunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_item_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_base_item_active_requisite=x_atom.get_value(
            "base_item_active_requisite"
        ),
    )


def _modify_bud_item_reasonunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_item_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_base_item_active_requisite=x_atom.get_value(
            "base_item_active_requisite"
        ),
    )


def _modify_bud_item_reason_premiseunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_item_attr(
        road=x_atom.get_value("road"),
        reason_del_premise_base=x_atom.get_value("base"),
        reason_del_premise_need=x_atom.get_value("need"),
    )


def _modify_bud_item_reason_premiseunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_item_attr(
        road=x_atom.get_value("road"),
        reason_base=x_atom.get_value("base"),
        reason_premise=x_atom.get_value("need"),
        reason_premise_open=x_atom.get_value("open"),
        reason_premise_nigh=x_atom.get_value("nigh"),
        reason_premise_divisor=x_atom.get_value("divisor"),
    )


def _modify_bud_item_reason_premiseunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_itemunit = x_bud.get_item_obj(x_atom.get_value("road"))
    x_itemunit.set_reason_premise(
        base=x_atom.get_value("base"),
        premise=x_atom.get_value("need"),
        open=x_atom.get_value("open"),
        nigh=x_atom.get_value("nigh"),
        divisor=x_atom.get_value("divisor"),
    )


def _modify_bud_item_teamlink_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_itemunit = x_bud.get_item_obj(x_atom.get_value("road"))
    x_itemunit.teamunit.del_teamlink(team_tag=x_atom.get_value("team_tag"))


def _modify_bud_item_teamlink_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_itemunit = x_bud.get_item_obj(x_atom.get_value("road"))
    x_itemunit.teamunit.set_teamlink(team_tag=x_atom.get_value("team_tag"))


def _modify_bud_item_healerlink_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_itemunit = x_bud.get_item_obj(x_atom.get_value("road"))
    x_itemunit.healerlink.del_healer_name(x_atom.get_value("healer_name"))


def _modify_bud_item_healerlink_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_itemunit = x_bud.get_item_obj(x_atom.get_value("road"))
    x_itemunit.healerlink.set_healer_name(x_atom.get_value("healer_name"))


def _modify_bud_acctunit_delete(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.del_acctunit(x_atom.get_value("acct_name"))


def _modify_bud_acctunit_update(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.edit_acctunit(
        acct_name=x_atom.get_value("acct_name"),
        credit_belief=x_atom.get_value("credit_belief"),
        debtit_belief=x_atom.get_value("debtit_belief"),
    )


def _modify_bud_acctunit_insert(x_bud: BudUnit, x_atom: AtomUnit):
    x_bud.set_acctunit(
        acctunit_shop(
            acct_name=x_atom.get_value("acct_name"),
            credit_belief=x_atom.get_value("credit_belief"),
            debtit_belief=x_atom.get_value("debtit_belief"),
        )
    )


def _modify_bud_budunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_update():
        _modify_bud_update_budunit(x_bud, x_atom)


def _modify_bud_acct_membership(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_delete():
        _modify_bud_acct_membership_delete(x_bud, x_atom)
    elif x_atom.crud_str == atom_update():
        _modify_bud_acct_membership_update(x_bud, x_atom)
    elif x_atom.crud_str == atom_insert():
        _modify_bud_acct_membership_insert(x_bud, x_atom)


def _modify_bud_itemunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_delete():
        _modify_bud_itemunit_delete(x_bud, x_atom)
    elif x_atom.crud_str == atom_update():
        _modify_bud_itemunit_update(x_bud, x_atom)
    elif x_atom.crud_str == atom_insert():
        _modify_bud_itemunit_insert(x_bud, x_atom)


def _modify_bud_item_awardlink(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_delete():
        _modify_bud_item_awardlink_delete(x_bud, x_atom)
    elif x_atom.crud_str == atom_update():
        _modify_bud_item_awardlink_update(x_bud, x_atom)
    elif x_atom.crud_str == atom_insert():
        _modify_bud_item_awardlink_insert(x_bud, x_atom)


def _modify_bud_item_factunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_delete():
        _modify_bud_item_factunit_delete(x_bud, x_atom)
    elif x_atom.crud_str == atom_update():
        _modify_bud_item_factunit_update(x_bud, x_atom)
    elif x_atom.crud_str == atom_insert():
        _modify_bud_item_factunit_insert(x_bud, x_atom)


def _modify_bud_item_reasonunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_delete():
        _modify_bud_item_reasonunit_delete(x_bud, x_atom)
    elif x_atom.crud_str == atom_update():
        _modify_bud_item_reasonunit_update(x_bud, x_atom)
    elif x_atom.crud_str == atom_insert():
        _modify_bud_item_reasonunit_insert(x_bud, x_atom)


def _modify_bud_item_reason_premiseunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_delete():
        _modify_bud_item_reason_premiseunit_delete(x_bud, x_atom)
    elif x_atom.crud_str == atom_update():
        _modify_bud_item_reason_premiseunit_update(x_bud, x_atom)
    elif x_atom.crud_str == atom_insert():
        _modify_bud_item_reason_premiseunit_insert(x_bud, x_atom)


def _modify_bud_item_teamlink(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_delete():
        _modify_bud_item_teamlink_delete(x_bud, x_atom)
    elif x_atom.crud_str == atom_insert():
        _modify_bud_item_teamlink_insert(x_bud, x_atom)


def _modify_bud_item_healerlink(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_delete():
        _modify_bud_item_healerlink_delete(x_bud, x_atom)
    elif x_atom.crud_str == atom_insert():
        _modify_bud_item_healerlink_insert(x_bud, x_atom)


def _modify_bud_acctunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.crud_str == atom_delete():
        _modify_bud_acctunit_delete(x_bud, x_atom)
    elif x_atom.crud_str == atom_update():
        _modify_bud_acctunit_update(x_bud, x_atom)
    elif x_atom.crud_str == atom_insert():
        _modify_bud_acctunit_insert(x_bud, x_atom)


def modify_bud_with_atomunit(x_bud: BudUnit, x_atom: AtomUnit):
    if x_atom.dimen == "budunit":
        _modify_bud_budunit(x_bud, x_atom)
    elif x_atom.dimen == "bud_acct_membership":
        _modify_bud_acct_membership(x_bud, x_atom)
    elif x_atom.dimen == "bud_itemunit":
        _modify_bud_itemunit(x_bud, x_atom)
    elif x_atom.dimen == "bud_item_awardlink":
        _modify_bud_item_awardlink(x_bud, x_atom)
    elif x_atom.dimen == "bud_item_factunit":
        _modify_bud_item_factunit(x_bud, x_atom)
    elif x_atom.dimen == "bud_item_reasonunit":
        _modify_bud_item_reasonunit(x_bud, x_atom)
    elif x_atom.dimen == "bud_item_reason_premiseunit":
        _modify_bud_item_reason_premiseunit(x_bud, x_atom)
    elif x_atom.dimen == "bud_item_healerlink":
        _modify_bud_item_healerlink(x_bud, x_atom)
    elif x_atom.dimen == "bud_item_teamlink":
        _modify_bud_item_teamlink(x_bud, x_atom)
    elif x_atom.dimen == "bud_acctunit":
        _modify_bud_acctunit(x_bud, x_atom)


def jvalues_different(dimen: str, x_obj: any, y_obj: any) -> bool:
    if dimen == "budunit":
        return (
            x_obj.tally != y_obj.tally
            or x_obj.max_tree_traverse != y_obj.max_tree_traverse
            or x_obj.credor_respect != y_obj.credor_respect
            or x_obj.debtor_respect != y_obj.debtor_respect
            or x_obj.respect_bit != y_obj.respect_bit
            or x_obj.fund_pool != y_obj.fund_pool
            or x_obj.fund_coin != y_obj.fund_coin
        )
    elif dimen in {"bud_acct_membership"}:
        return (x_obj.credit_vote != y_obj.credit_vote) or (
            x_obj.debtit_vote != y_obj.debtit_vote
        )
    elif dimen in {"bud_item_awardlink"}:
        return (x_obj.give_force != y_obj.give_force) or (
            x_obj.take_force != y_obj.take_force
        )
    elif dimen == "bud_itemunit":
        return (
            x_obj.addin != y_obj.addin
            or x_obj.begin != y_obj.begin
            or x_obj.close != y_obj.close
            or x_obj.denom != y_obj.denom
            or x_obj.numor != y_obj.numor
            or x_obj.morph != y_obj.morph
            or x_obj.mass != y_obj.mass
            or x_obj.pledge != y_obj.pledge
        )
    elif dimen == "bud_item_factunit":
        return (
            (x_obj.pick != y_obj.pick)
            or (x_obj.open != y_obj.open)
            or (x_obj.nigh != y_obj.nigh)
        )
    elif dimen == "bud_item_reasonunit":
        return x_obj.base_item_active_requisite != y_obj.base_item_active_requisite
    elif dimen == "bud_item_reason_premiseunit":
        return (
            x_obj.open != y_obj.open
            or x_obj.nigh != y_obj.nigh
            or x_obj.divisor != y_obj.divisor
        )
    elif dimen == "bud_acctunit":
        return (x_obj.credit_belief != y_obj.credit_belief) or (
            x_obj.debtit_belief != y_obj.debtit_belief
        )


class InvalidAtomUnitException(Exception):
    pass


def get_atomunit_from_rowdata(x_rowdata: RowData) -> AtomUnit:
    dimen_str, crud_str = get_dimen_from_dict(x_rowdata.row_dict)
    x_atom = atomunit_shop(dimen=dimen_str, crud_str=crud_str)
    front_len = len(dimen_str) + len(crud_str) + 2
    for x_columnname, x_value in x_rowdata.row_dict.items():
        arg_key = x_columnname[front_len:]
        x_atom.set_arg(x_key=arg_key, x_value=x_value)
    return x_atom


@dataclass
class AtomRow:
    _atom_dimens: set[str] = None
    _crud_command: CRUD_command = None
    acct_name: AcctName = None
    addin: float = None
    awardee_tag: GroupLabel = None
    base: RoadUnit = None
    base_item_active_requisite: bool = None
    begin: float = None
    respect_bit: float = None
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
    group_label: GroupLabel = None
    healer_name: GroupLabel = None
    item_title: TitleUnit = None
    mass: int = None
    max_tree_traverse: int = None
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
    deal_time_int: TimeLinePoint = None
    road: RoadUnit = None
    stop_want: float = None
    take_force: float = None
    tally: int = None
    team_tag: int = None

    def set_atom_dimen(self, atom_dimen: str):
        self._atom_dimens.add(atom_dimen)

    def atom_dimen_exists(self, atom_dimen: str) -> bool:
        return atom_dimen in self._atom_dimens

    def delete_atom_dimen(self, atom_dimen: str):
        self._atom_dimens.remove(atom_dimen)

    def _set_class_types(self):
        for x_arg, class_type in get_atom_args_class_types().items():
            x_value = self.__dict__.get(x_arg)
            if x_value != None:
                if class_type == "AcctName":
                    self.__dict__[x_arg] = AcctName(x_value)
                elif class_type == "GroupLabel":
                    self.__dict__[x_arg] = GroupLabel(x_value)
                elif class_type == "RoadUnit":
                    self.__dict__[x_arg] = RoadUnit(x_value)
                elif class_type == "TitleUnit":
                    self.__dict__[x_arg] = TitleUnit(x_value)
                elif class_type == "str":
                    self.__dict__[x_arg] = str(x_value)
                elif class_type == "bool":
                    self.__dict__[x_arg] = bool(x_value)
                elif class_type == "int":
                    self.__dict__[x_arg] = int(x_value)
                elif class_type == "float":
                    self.__dict__[x_arg] = float(x_value)
        if self.item_title != None and self.parent_road != None and self.road == None:
            self.road = create_road(self.parent_road, self.item_title)

    def get_atomunits(self) -> list[AtomUnit]:
        self._set_class_types()
        x_list = []
        for x_dimen in self._atom_dimens:
            x_atom = atomunit_shop(x_dimen, self._crud_command)
            x_args = get_atom_config_args(x_dimen)
            for x_arg in x_args:
                if self.__dict__[x_arg] != None:
                    x_atom.set_arg(x_arg, self.__dict__[x_arg])
            if x_atom.is_valid() > 0:
                x_list.append(x_atom)
        return x_list


def atomrow_shop(atom_dimens: set[str], crud_command: CRUD_command) -> AtomRow:
    return AtomRow(_atom_dimens=atom_dimens, _crud_command=crud_command)


def sift_atomunit(x_bud: BudUnit, x_atom: AtomUnit) -> AtomUnit:
    x_dimen = x_atom.dimen
    config_req_args = get_atom_config_jkeys(x_dimen)
    x_atom_reqs = {req_arg: x_atom.get_value(req_arg) for req_arg in config_req_args}
    x_parent_road = x_atom_reqs.get("parent_road")
    x_item_title = x_atom_reqs.get("item_title")
    if x_parent_road != None and x_item_title != None:
        x_atom_reqs["road"] = x_bud.make_road(x_parent_road, x_item_title)
        x_bridge = x_bud.bridge
        is_itemroot_road = is_titleunit(x_atom_reqs.get("road"), x_bridge)
        if is_itemroot_road is True:
            return None

    x_exists = bud_attr_exists(x_dimen, x_bud, x_atom_reqs)

    if x_atom.crud_str == atom_delete() and x_exists:
        return x_atom
    elif x_atom.crud_str == atom_insert() and not x_exists:
        return x_atom
    elif x_atom.crud_str == atom_insert() and x_exists:
        x_bud_obj = bud_get_obj(x_dimen, x_bud, x_atom_reqs)
        x_jvalues = x_atom.get_jvalues_dict()
        update_atom = atomunit_shop(x_dimen, atom_update(), x_atom.jkeys)
        for jvalue in x_jvalues:
            optional_value = x_atom.get_value(jvalue)
            obj_value = x_bud_obj.__dict__[jvalue]
            if obj_value != optional_value:
                update_atom.set_arg(jvalue, optional_value)

        if update_atom.get_jvalues_dict() != {}:
            return update_atom
    return None
