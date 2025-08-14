from dataclasses import dataclass
from src.a00_data_toolbox.db_toolbox import RowData, create_type_reference_insert_sqlstr
from src.a00_data_toolbox.dict_toolbox import (
    get_dict_from_json,
    get_empty_dict_if_None,
    get_json_from_dict,
)
from src.a01_term_logic.rope import create_rope, get_parent_rope, get_tail_label
from src.a01_term_logic.term import LabelTerm, PartnerName, RopeTerm, TitleTerm
from src.a03_group_logic.group import awardlink_shop
from src.a03_group_logic.partner import partnerunit_shop
from src.a04_reason_logic.reason_plan import factunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import BelieverUnit
from src.a06_believer_logic.believer_tool import believer_attr_exists, believer_get_obj
from src.a08_believer_atom_logic.atom_config import (
    CRUD_command,
    get_atom_args_class_types,
    get_atom_config_args,
    get_atom_config_dict,
    get_atom_config_jkeys,
    get_atom_order,
    get_dimen_from_dict,
    get_sorted_jkey_keys,
    is_believer_dimen,
)


class BelieverAtomDescriptionException(Exception):
    pass


@dataclass
class BelieverAtom:
    dimen: str = None
    crud_str: str = None
    jkeys: dict[str, str] = None
    jvalues: dict[str, str] = None
    atom_order: int = None

    def get_insert_sqlstr(self) -> str:
        if self.is_valid() is False:
            raise BelieverAtomDescriptionException(
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
        return create_type_reference_insert_sqlstr("atom_hx", x_columns, x_values)

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
        # When ChangUnit places an BelieverAtom in a nested dictionary ChangUnit.believeratoms
        # the order of required argments decides the location. The order must be
        # the same
        sorted_jkey_keys = get_sorted_jkey_keys(self.dimen)
        return [self.jkeys.get(jkey) for jkey in sorted_jkey_keys]

    def is_jkeys_valid(self) -> bool:
        if self.crud_str not in {
            "DELETE",
            "INSERT",
            "UPDATE",
        }:
            return False
        jkeys_dict = self._get_jkeys_dict()
        return jkeys_dict.keys() == self.jkeys.keys()

    def is_jvalues_valid(self) -> bool:
        if self.crud_str == "DELETE" and self.jvalues == {}:
            return True
        if self.crud_str not in {"INSERT", "UPDATE"}:
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

    def to_dict(self) -> dict[str, str]:
        jkeys_dict = self.get_jkeys_dict()
        jvalues_dict = self.get_jvalues_dict()
        return {
            "dimen": self.dimen,
            "crud": self.crud_str,
            "jkeys": jkeys_dict,
            "jvalues": jvalues_dict,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.to_dict())


def believeratom_shop(
    dimen: str,
    crud_str: str = None,
    jkeys: dict[str, str] = None,
    jvalues: dict[str, str] = None,
) -> BelieverAtom:
    if is_believer_dimen(dimen):
        return BelieverAtom(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=get_empty_dict_if_None(jkeys),
            jvalues=get_empty_dict_if_None(jvalues),
        )


def get_from_dict(x_dict: dict) -> BelieverAtom:
    x_atom = believeratom_shop(x_dict["dimen"], x_dict["crud"])
    for x_key, x_value in x_dict["jkeys"].items():
        x_atom.set_jkey(x_key, x_value)
    for x_key, x_value in x_dict["jvalues"].items():
        x_atom.set_jvalue(x_key, x_value)
    return x_atom


def get_from_json(x_str: str) -> BelieverAtom:
    return get_from_dict(get_dict_from_json(x_str))


def _modify_believer_update_believerunit(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_arg = "max_tree_traverse"
    if x_atom.get_value(x_arg) is not None:
        x_believer.set_max_tree_traverse(x_atom.get_value(x_arg))
    x_arg = "credor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_believer.set_credor_respect(x_atom.get_value(x_arg))
    x_arg = "debtor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_believer.set_debtor_respect(x_atom.get_value(x_arg))
    x_arg = "fund_pool"
    if x_atom.get_value(x_arg) is not None:
        x_believer.fund_pool = x_atom.get_value(x_arg)
    x_arg = "fund_iota"
    if x_atom.get_value(x_arg) is not None:
        x_believer.fund_iota = x_atom.get_value(x_arg)
    x_arg = "tally"
    if x_atom.get_value(x_arg) is not None:
        x_believer.tally = x_atom.get_value(x_arg)
    x_arg = "respect_bit"
    if x_atom.get_value(x_arg) is not None:
        x_believer.respect_bit = x_atom.get_value(x_arg)
    x_arg = "penny"
    if x_atom.get_value(x_arg) is not None:
        x_believer.penny = x_atom.get_value(x_arg)


def _modify_believer_partner_membership_delete(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_partner_name = x_atom.get_value("partner_name")
    x_group_title = x_atom.get_value("group_title")
    x_believer.get_partner(x_partner_name).delete_membership(x_group_title)


def _modify_believer_partner_membership_update(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_partner_name = x_atom.get_value("partner_name")
    x_group_title = x_atom.get_value("group_title")
    x_partnerunit = x_believer.get_partner(x_partner_name)
    x_membership = x_partnerunit.get_membership(x_group_title)
    x_group_cred_points = x_atom.get_value("group_cred_points")
    x_group_debt_points = x_atom.get_value("group_debt_points")
    x_membership.set_group_cred_points(x_group_cred_points)
    x_membership.set_group_debt_points(x_group_debt_points)


def _modify_believer_partner_membership_insert(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_partner_name = x_atom.get_value("partner_name")
    x_group_title = x_atom.get_value("group_title")
    x_group_cred_points = x_atom.get_value("group_cred_points")
    x_group_debt_points = x_atom.get_value("group_debt_points")
    x_partnerunit = x_believer.get_partner(x_partner_name)
    x_partnerunit.add_membership(
        x_group_title, x_group_cred_points, x_group_debt_points
    )


def _modify_believer_planunit_delete(x_believer: BelieverUnit, x_atom: BelieverAtom):
    plan_rope = create_rope(x_atom.get_value("plan_rope"), knot=x_believer.knot)
    x_believer.del_plan_obj(plan_rope, del_children=x_atom.get_value("del_children"))


def _modify_believer_planunit_update(x_believer: BelieverUnit, x_atom: BelieverAtom):
    plan_rope = create_rope(x_atom.get_value("plan_rope"), knot=x_believer.knot)
    x_believer.edit_plan_attr(
        plan_rope,
        addin=x_atom.get_value("addin"),
        begin=x_atom.get_value("begin"),
        gogo_want=x_atom.get_value("gogo_want"),
        stop_want=x_atom.get_value("stop_want"),
        close=x_atom.get_value("close"),
        denom=x_atom.get_value("denom"),
        numor=x_atom.get_value("numor"),
        morph=x_atom.get_value("morph"),
        star=x_atom.get_value("star"),
        task=x_atom.get_value("task"),
    )


def _modify_believer_planunit_insert(x_believer: BelieverUnit, x_atom: BelieverAtom):
    plan_rope = x_atom.get_value("plan_rope")
    plan_label = get_tail_label(plan_rope)
    plan_parent_rope = get_parent_rope(plan_rope)
    x_believer.set_plan(
        plan_kid=planunit_shop(
            plan_label=plan_label,
            addin=x_atom.get_value("addin"),
            begin=x_atom.get_value("begin"),
            close=x_atom.get_value("close"),
            gogo_want=x_atom.get_value("gogo_want"),
            stop_want=x_atom.get_value("stop_want"),
            denom=x_atom.get_value("denom"),
            numor=x_atom.get_value("numor"),
            task=x_atom.get_value("task"),
        ),
        parent_rope=plan_parent_rope,
        create_missing_plans=False,
        get_rid_of_missing_awardlinks_awardee_titles=False,
        create_missing_ancestors=True,
    )


def _modify_believer_plan_awardlink_delete(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_believer.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        awardlink_del=x_atom.get_value("awardee_title"),
    )


def _modify_believer_plan_awardlink_update(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_plan = x_believer.get_plan_obj(x_atom.get_value("plan_rope"))
    x_awardlink = x_plan.awardlinks.get(x_atom.get_value("awardee_title"))
    x_give_force = x_atom.get_value("give_force")
    if x_give_force is not None and x_awardlink.give_force != x_give_force:
        x_awardlink.give_force = x_give_force
    x_take_force = x_atom.get_value("take_force")
    if x_take_force is not None and x_awardlink.take_force != x_take_force:
        x_awardlink.take_force = x_take_force
    x_believer.edit_plan_attr(x_atom.get_value("plan_rope"), awardlink=x_awardlink)


def _modify_believer_plan_awardlink_insert(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_awardlink = awardlink_shop(
        awardee_title=x_atom.get_value("awardee_title"),
        give_force=x_atom.get_value("give_force"),
        take_force=x_atom.get_value("take_force"),
    )
    x_believer.edit_plan_attr(x_atom.get_value("plan_rope"), awardlink=x_awardlink)


def _modify_believer_plan_factunit_delete(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_planunit = x_believer.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.del_factunit(x_atom.get_value("fact_context"))


def _modify_believer_plan_factunit_update(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_planunit = x_believer.get_plan_obj(x_atom.get_value("plan_rope"))
    x_factunit = x_planunit.factunits.get(x_atom.get_value("fact_context"))
    x_factunit.set_attr(
        fact_state=x_atom.get_value("fact_state"),
        fact_lower=x_atom.get_value("fact_lower"),
        fact_upper=x_atom.get_value("fact_upper"),
    )


def _modify_believer_plan_factunit_insert(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_believer.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        factunit=factunit_shop(
            fact_context=x_atom.get_value("fact_context"),
            fact_state=x_atom.get_value("fact_state"),
            fact_lower=x_atom.get_value("fact_lower"),
            fact_upper=x_atom.get_value("fact_upper"),
        ),
    )


def _modify_believer_plan_reasonunit_delete(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_planunit = x_believer.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.del_reasonunit_reason_context(x_atom.get_value("reason_context"))


def _modify_believer_plan_reasonunit_update(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_believer.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        reason_context=x_atom.get_value("reason_context"),
        reason_plan_active_requisite=x_atom.get_value("reason_active_requisite"),
    )


def _modify_believer_plan_reasonunit_insert(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_believer.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        reason_context=x_atom.get_value("reason_context"),
        reason_plan_active_requisite=x_atom.get_value("reason_active_requisite"),
    )


def _modify_believer_plan_reason_caseunit_delete(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_believer.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        reason_del_case_reason_context=x_atom.get_value("reason_context"),
        reason_del_case_reason_state=x_atom.get_value("reason_state"),
    )


def _modify_believer_plan_reason_caseunit_update(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_believer.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        reason_context=x_atom.get_value("reason_context"),
        reason_case=x_atom.get_value("reason_state"),
        reason_lower=x_atom.get_value("reason_lower"),
        reason_upper=x_atom.get_value("reason_upper"),
        reason_divisor=x_atom.get_value("reason_divisor"),
    )


def _modify_believer_plan_reason_caseunit_insert(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_planunit = x_believer.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.set_reason_case(
        reason_context=x_atom.get_value("reason_context"),
        case=x_atom.get_value("reason_state"),
        reason_lower=x_atom.get_value("reason_lower"),
        reason_upper=x_atom.get_value("reason_upper"),
        reason_divisor=x_atom.get_value("reason_divisor"),
    )


def _modify_believer_plan_partyunit_delete(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_planunit = x_believer.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.laborunit.del_partyunit(party_title=x_atom.get_value("party_title"))


def _modify_believer_plan_partyunit_insert(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_planunit = x_believer.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.laborunit.add_party(party_title=x_atom.get_value("party_title"))


def _modify_believer_plan_healerlink_delete(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_planunit = x_believer.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.healerlink.del_healer_name(x_atom.get_value("healer_name"))


def _modify_believer_plan_healerlink_insert(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    x_planunit = x_believer.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.healerlink.set_healer_name(x_atom.get_value("healer_name"))


def _modify_believer_partnerunit_delete(x_believer: BelieverUnit, x_atom: BelieverAtom):
    x_believer.del_partnerunit(x_atom.get_value("partner_name"))


def _modify_believer_partnerunit_update(x_believer: BelieverUnit, x_atom: BelieverAtom):
    x_believer.edit_partnerunit(
        partner_name=x_atom.get_value("partner_name"),
        partner_cred_points=x_atom.get_value("partner_cred_points"),
        partner_debt_points=x_atom.get_value("partner_debt_points"),
    )


def _modify_believer_partnerunit_insert(x_believer: BelieverUnit, x_atom: BelieverAtom):
    x_believer.set_partnerunit(
        partnerunit_shop(
            partner_name=x_atom.get_value("partner_name"),
            partner_cred_points=x_atom.get_value("partner_cred_points"),
            partner_debt_points=x_atom.get_value("partner_debt_points"),
        )
    )


def _modify_believer_believerunit(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.crud_str == "UPDATE":
        _modify_believer_update_believerunit(x_believer, x_atom)


def _modify_believer_partner_membership(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.crud_str == "DELETE":
        _modify_believer_partner_membership_delete(x_believer, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_believer_partner_membership_update(x_believer, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_believer_partner_membership_insert(x_believer, x_atom)


def _modify_believer_planunit(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.crud_str == "DELETE":
        _modify_believer_planunit_delete(x_believer, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_believer_planunit_update(x_believer, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_believer_planunit_insert(x_believer, x_atom)


def _modify_believer_plan_awardlink(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.crud_str == "DELETE":
        _modify_believer_plan_awardlink_delete(x_believer, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_believer_plan_awardlink_update(x_believer, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_believer_plan_awardlink_insert(x_believer, x_atom)


def _modify_believer_plan_factunit(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.crud_str == "DELETE":
        _modify_believer_plan_factunit_delete(x_believer, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_believer_plan_factunit_update(x_believer, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_believer_plan_factunit_insert(x_believer, x_atom)


def _modify_believer_plan_reasonunit(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.crud_str == "DELETE":
        _modify_believer_plan_reasonunit_delete(x_believer, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_believer_plan_reasonunit_update(x_believer, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_believer_plan_reasonunit_insert(x_believer, x_atom)


def _modify_believer_plan_reason_caseunit(
    x_believer: BelieverUnit, x_atom: BelieverAtom
):
    if x_atom.crud_str == "DELETE":
        _modify_believer_plan_reason_caseunit_delete(x_believer, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_believer_plan_reason_caseunit_update(x_believer, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_believer_plan_reason_caseunit_insert(x_believer, x_atom)


def _modify_believer_plan_partyunit(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.crud_str == "DELETE":
        _modify_believer_plan_partyunit_delete(x_believer, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_believer_plan_partyunit_insert(x_believer, x_atom)


def _modify_believer_plan_healerlink(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.crud_str == "DELETE":
        _modify_believer_plan_healerlink_delete(x_believer, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_believer_plan_healerlink_insert(x_believer, x_atom)


def _modify_believer_partnerunit(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.crud_str == "DELETE":
        _modify_believer_partnerunit_delete(x_believer, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_believer_partnerunit_update(x_believer, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_believer_partnerunit_insert(x_believer, x_atom)


def modify_believer_with_believeratom(x_believer: BelieverUnit, x_atom: BelieverAtom):
    if x_atom.dimen == "believerunit":
        _modify_believer_believerunit(x_believer, x_atom)
    elif x_atom.dimen == "believer_partner_membership":
        _modify_believer_partner_membership(x_believer, x_atom)
    elif x_atom.dimen == "believer_planunit":
        _modify_believer_planunit(x_believer, x_atom)
    elif x_atom.dimen == "believer_plan_awardlink":
        _modify_believer_plan_awardlink(x_believer, x_atom)
    elif x_atom.dimen == "believer_plan_factunit":
        _modify_believer_plan_factunit(x_believer, x_atom)
    elif x_atom.dimen == "believer_plan_reasonunit":
        _modify_believer_plan_reasonunit(x_believer, x_atom)
    elif x_atom.dimen == "believer_plan_reason_caseunit":
        _modify_believer_plan_reason_caseunit(x_believer, x_atom)
    elif x_atom.dimen == "believer_plan_healerlink":
        _modify_believer_plan_healerlink(x_believer, x_atom)
    elif x_atom.dimen == "believer_plan_partyunit":
        _modify_believer_plan_partyunit(x_believer, x_atom)
    elif x_atom.dimen == "believer_partnerunit":
        _modify_believer_partnerunit(x_believer, x_atom)


def jvalues_different(dimen: str, x_obj: any, y_obj: any) -> bool:
    if dimen == "believerunit":
        return (
            x_obj.tally != y_obj.tally
            or x_obj.max_tree_traverse != y_obj.max_tree_traverse
            or x_obj.credor_respect != y_obj.credor_respect
            or x_obj.debtor_respect != y_obj.debtor_respect
            or x_obj.respect_bit != y_obj.respect_bit
            or x_obj.fund_pool != y_obj.fund_pool
            or x_obj.fund_iota != y_obj.fund_iota
        )
    elif dimen in {"believer_partner_membership"}:
        return (x_obj.group_cred_points != y_obj.group_cred_points) or (
            x_obj.group_debt_points != y_obj.group_debt_points
        )
    elif dimen in {"believer_plan_awardlink"}:
        return (x_obj.give_force != y_obj.give_force) or (
            x_obj.take_force != y_obj.take_force
        )
    elif dimen == "believer_planunit":
        return (
            x_obj.addin != y_obj.addin
            or x_obj.begin != y_obj.begin
            or x_obj.close != y_obj.close
            or x_obj.denom != y_obj.denom
            or x_obj.numor != y_obj.numor
            or x_obj.morph != y_obj.morph
            or x_obj.star != y_obj.star
            or x_obj.task != y_obj.task
        )
    elif dimen == "believer_plan_factunit":
        return (
            (x_obj.fact_state != y_obj.fact_state)
            or (x_obj.reason_lower != y_obj.reason_lower)
            or (x_obj.reason_upper != y_obj.reason_upper)
        )
    elif dimen == "believer_plan_reasonunit":
        return x_obj.reason_active_requisite != y_obj.reason_active_requisite
    elif dimen == "believer_plan_reason_caseunit":
        return (
            x_obj.reason_lower != y_obj.reason_lower
            or x_obj.reason_upper != y_obj.reason_upper
            or x_obj.reason_divisor != y_obj.reason_divisor
        )
    elif dimen == "believer_partnerunit":
        return (x_obj.partner_cred_points != y_obj.partner_cred_points) or (
            x_obj.partner_debt_points != y_obj.partner_debt_points
        )


class InvalidBelieverAtomException(Exception):
    pass


def get_believeratom_from_rowdata(x_rowdata: RowData) -> BelieverAtom:
    dimen_str, crud_str = get_dimen_from_dict(x_rowdata.row_dict)
    x_atom = believeratom_shop(dimen=dimen_str, crud_str=crud_str)
    front_len = len(dimen_str) + len(crud_str) + 2
    for x_columnname, x_value in x_rowdata.row_dict.items():
        arg_key = x_columnname[front_len:]
        x_atom.set_arg(x_key=arg_key, x_value=x_value)
    return x_atom


@dataclass
class AtomRow:
    _atom_dimens: set[str] = None
    _crud_command: CRUD_command = None
    partner_name: PartnerName = None
    addin: float = None
    awardee_title: TitleTerm = None
    reason_context: RopeTerm = None
    reason_active_requisite: bool = None
    begin: float = None
    respect_bit: float = None
    close: float = None
    partner_cred_points: int = None
    group_cred_points: int = None
    credor_respect: int = None
    partner_debt_points: int = None
    group_debt_points: int = None
    debtor_respect: int = None
    denom: int = None
    reason_divisor: int = None
    fact_context: RopeTerm = None
    fact_upper: float = None
    fact_lower: float = None
    fund_iota: float = None
    fund_pool: float = None
    give_force: float = None
    gogo_want: float = None
    group_title: TitleTerm = None
    healer_name: TitleTerm = None
    star: int = None
    max_tree_traverse: int = None
    morph: bool = None
    reason_state: RopeTerm = None
    reason_upper: float = None
    numor: int = None
    reason_lower: float = None
    penny: float = None
    fact_state: RopeTerm = None
    task: bool = None
    problem_bool: bool = None
    plan_rope: RopeTerm = None
    solo: int = None
    stop_want: float = None
    take_force: float = None
    tally: int = None
    party_title: int = None

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
                if class_type == "NameTerm":
                    self.__dict__[x_arg] = PartnerName(x_value)
                elif class_type == "TitleTerm":
                    self.__dict__[x_arg] = TitleTerm(x_value)
                elif class_type == "RopeTerm":
                    self.__dict__[x_arg] = RopeTerm(x_value)
                elif class_type == "LabelTerm":
                    self.__dict__[x_arg] = LabelTerm(x_value)
                elif class_type == "str":
                    self.__dict__[x_arg] = str(x_value)
                elif class_type == "bool":
                    self.__dict__[x_arg] = bool(x_value)
                elif class_type == "int":
                    self.__dict__[x_arg] = int(x_value)
                elif class_type == "float":
                    self.__dict__[x_arg] = float(x_value)

    def get_believeratoms(self) -> list[BelieverAtom]:
        self._set_class_types()
        x_list = []
        for x_dimen in self._atom_dimens:
            x_atom = believeratom_shop(x_dimen, self._crud_command)
            x_args = get_atom_config_args(x_dimen)
            for x_arg in x_args:
                if self.__dict__[x_arg] != None:
                    x_atom.set_arg(x_arg, self.__dict__[x_arg])
            if x_atom.is_valid() > 0:
                x_list.append(x_atom)
        return x_list


def atomrow_shop(atom_dimens: set[str], crud_command: CRUD_command) -> AtomRow:
    return AtomRow(_atom_dimens=atom_dimens, _crud_command=crud_command)


def sift_believeratom(x_believer: BelieverUnit, x_atom: BelieverAtom) -> BelieverAtom:
    config_keys = get_atom_config_jkeys(x_atom.dimen)
    x_atom_reqs = {x_key: x_atom.get_value(x_key) for x_key in config_keys}

    x_exists = believer_attr_exists(x_atom.dimen, x_believer, x_atom_reqs)

    if x_atom.crud_str == "DELETE" and x_exists:
        return x_atom
    elif x_atom.crud_str == "INSERT" and not x_exists:
        return x_atom
    elif x_atom.crud_str == "INSERT":
        x_believer_obj = believer_get_obj(x_atom.dimen, x_believer, x_atom_reqs)
        x_jvalues = x_atom.get_jvalues_dict()
        update_atom = believeratom_shop(x_atom.dimen, "UPDATE", x_atom.jkeys)
        for jvalue in x_jvalues:
            optional_jvalue = x_atom.get_value(jvalue)
            obj_jvalue = x_believer_obj.__dict__[jvalue]
            if obj_jvalue != optional_jvalue:
                update_atom.set_arg(jvalue, optional_jvalue)

        if update_atom.get_jvalues_dict() != {}:
            return update_atom
    return None
