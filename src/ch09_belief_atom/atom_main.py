from dataclasses import dataclass
from src.ch01_py.db_toolbox import RowData, create_type_reference_insert_sqlstr
from src.ch01_py.dict_toolbox import get_empty_dict_if_None
from src.ch02_rope.rope import create_rope, get_parent_rope, get_tail_label
from src.ch04_voice.group import awardunit_shop
from src.ch04_voice.voice import voiceunit_shop
from src.ch05_reason.reason import factunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import BeliefUnit
from src.ch07_belief_logic.belief_tool import belief_attr_exists, belief_get_obj
from src.ch09_belief_atom._ref.ch09_semantic_types import (
    LabelTerm,
    RopeTerm,
    TitleTerm,
    VoiceName,
)
from src.ch09_belief_atom.atom_config import (
    CRUD_command,
    get_atom_args_class_types,
    get_atom_config_args,
    get_atom_config_dict,
    get_atom_config_jkeys,
    get_atom_order,
    get_dimen_from_dict,
    get_sorted_jkey_keys,
    is_belief_dimen,
)


class BeliefAtomDescriptionException(Exception):
    pass


@dataclass
class BeliefAtom:
    dimen: str = None
    crud_str: str = None
    jkeys: dict[str, str] = None
    jvalues: dict[str, str] = None
    atom_order: int = None

    def get_insert_sqlstr(self) -> str:
        if self.is_valid() is False:
            raise BeliefAtomDescriptionException(
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
        # When ChangUnit places an BeliefAtom in a nested dictionary ChangUnit.beliefatoms
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
        """Returns dict that is serializable to JSON."""

        jkeys_dict = self.get_jkeys_dict()
        jvalues_dict = self.get_jvalues_dict()
        return {
            "dimen": self.dimen,
            "crud": self.crud_str,
            "jkeys": jkeys_dict,
            "jvalues": jvalues_dict,
        }


def beliefatom_shop(
    dimen: str,
    crud_str: str = None,
    jkeys: dict[str, str] = None,
    jvalues: dict[str, str] = None,
) -> BeliefAtom:
    if is_belief_dimen(dimen):
        return BeliefAtom(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=get_empty_dict_if_None(jkeys),
            jvalues=get_empty_dict_if_None(jvalues),
        )


def get_beliefatom_from_dict(x_dict: dict) -> BeliefAtom:
    x_atom = beliefatom_shop(x_dict["dimen"], x_dict["crud"])
    for x_key, x_value in x_dict["jkeys"].items():
        x_atom.set_jkey(x_key, x_value)
    for x_key, x_value in x_dict["jvalues"].items():
        x_atom.set_jvalue(x_key, x_value)
    return x_atom


def _modify_belief_update_beliefunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_arg = "max_tree_traverse"
    if x_atom.get_value(x_arg) is not None:
        x_belief.set_max_tree_traverse(x_atom.get_value(x_arg))
    x_arg = "credor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_belief.set_credor_respect(x_atom.get_value(x_arg))
    x_arg = "debtor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_belief.set_debtor_respect(x_atom.get_value(x_arg))
    x_arg = "fund_pool"
    if x_atom.get_value(x_arg) is not None:
        x_belief.fund_pool = x_atom.get_value(x_arg)
    x_arg = "fund_grain"
    if x_atom.get_value(x_arg) is not None:
        x_belief.fund_grain = x_atom.get_value(x_arg)
    x_arg = "tally"
    if x_atom.get_value(x_arg) is not None:
        x_belief.tally = x_atom.get_value(x_arg)
    x_arg = "respect_grain"
    if x_atom.get_value(x_arg) is not None:
        x_belief.respect_grain = x_atom.get_value(x_arg)
    x_arg = "money_grain"
    if x_atom.get_value(x_arg) is not None:
        x_belief.money_grain = x_atom.get_value(x_arg)


def _modify_belief_voice_membership_delete(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_voice_name = x_atom.get_value("voice_name")
    x_group_title = x_atom.get_value("group_title")
    x_belief.get_voice(x_voice_name).delete_membership(x_group_title)


def _modify_belief_voice_membership_update(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_voice_name = x_atom.get_value("voice_name")
    x_group_title = x_atom.get_value("group_title")
    x_voiceunit = x_belief.get_voice(x_voice_name)
    x_membership = x_voiceunit.get_membership(x_group_title)
    x_group_cred_lumen = x_atom.get_value("group_cred_lumen")
    x_group_debt_lumen = x_atom.get_value("group_debt_lumen")
    x_membership.set_group_cred_lumen(x_group_cred_lumen)
    x_membership.set_group_debt_lumen(x_group_debt_lumen)


def _modify_belief_voice_membership_insert(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_voice_name = x_atom.get_value("voice_name")
    x_group_title = x_atom.get_value("group_title")
    x_group_cred_lumen = x_atom.get_value("group_cred_lumen")
    x_group_debt_lumen = x_atom.get_value("group_debt_lumen")
    x_voiceunit = x_belief.get_voice(x_voice_name)
    x_voiceunit.add_membership(x_group_title, x_group_cred_lumen, x_group_debt_lumen)


def _modify_belief_planunit_delete(x_belief: BeliefUnit, x_atom: BeliefAtom):
    plan_rope = create_rope(x_atom.get_value("plan_rope"), knot=x_belief.knot)
    x_belief.del_plan_obj(plan_rope, del_children=x_atom.get_value("del_children"))


def _modify_belief_planunit_update(x_belief: BeliefUnit, x_atom: BeliefAtom):
    plan_rope = create_rope(x_atom.get_value("plan_rope"), knot=x_belief.knot)
    x_belief.edit_plan_attr(
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
        pledge=x_atom.get_value("pledge"),
    )


def _modify_belief_planunit_insert(x_belief: BeliefUnit, x_atom: BeliefAtom):
    plan_rope = x_atom.get_value("plan_rope")
    plan_label = get_tail_label(plan_rope)
    plan_parent_rope = get_parent_rope(plan_rope)
    x_belief.set_plan(
        plan_kid=planunit_shop(
            plan_label=plan_label,
            addin=x_atom.get_value("addin"),
            begin=x_atom.get_value("begin"),
            close=x_atom.get_value("close"),
            gogo_want=x_atom.get_value("gogo_want"),
            stop_want=x_atom.get_value("stop_want"),
            denom=x_atom.get_value("denom"),
            numor=x_atom.get_value("numor"),
            pledge=x_atom.get_value("pledge"),
        ),
        parent_rope=plan_parent_rope,
        create_missing_plans=False,
        get_rid_of_missing_awardunits_awardee_titles=False,
        create_missing_ancestors=True,
    )


def _modify_belief_plan_awardunit_delete(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_belief.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        awardunit_del=x_atom.get_value("awardee_title"),
    )


def _modify_belief_plan_awardunit_update(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_plan = x_belief.get_plan_obj(x_atom.get_value("plan_rope"))
    x_awardunit = x_plan.awardunits.get(x_atom.get_value("awardee_title"))
    x_give_force = x_atom.get_value("give_force")
    if x_give_force is not None and x_awardunit.give_force != x_give_force:
        x_awardunit.give_force = x_give_force
    x_take_force = x_atom.get_value("take_force")
    if x_take_force is not None and x_awardunit.take_force != x_take_force:
        x_awardunit.take_force = x_take_force
    x_belief.edit_plan_attr(x_atom.get_value("plan_rope"), awardunit=x_awardunit)


def _modify_belief_plan_awardunit_insert(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_awardunit = awardunit_shop(
        awardee_title=x_atom.get_value("awardee_title"),
        give_force=x_atom.get_value("give_force"),
        take_force=x_atom.get_value("take_force"),
    )
    x_belief.edit_plan_attr(x_atom.get_value("plan_rope"), awardunit=x_awardunit)


def _modify_belief_plan_factunit_delete(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_planunit = x_belief.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.del_factunit(x_atom.get_value("fact_context"))


def _modify_belief_plan_factunit_update(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_planunit = x_belief.get_plan_obj(x_atom.get_value("plan_rope"))
    x_factunit = x_planunit.factunits.get(x_atom.get_value("fact_context"))
    x_factunit.set_attr(
        fact_state=x_atom.get_value("fact_state"),
        fact_lower=x_atom.get_value("fact_lower"),
        fact_upper=x_atom.get_value("fact_upper"),
    )


def _modify_belief_plan_factunit_insert(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_belief.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        factunit=factunit_shop(
            fact_context=x_atom.get_value("fact_context"),
            fact_state=x_atom.get_value("fact_state"),
            fact_lower=x_atom.get_value("fact_lower"),
            fact_upper=x_atom.get_value("fact_upper"),
        ),
    )


def _modify_belief_plan_reasonunit_delete(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_planunit = x_belief.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.del_reasonunit_reason_context(x_atom.get_value("reason_context"))


def _modify_belief_plan_reasonunit_update(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_belief.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        reason_context=x_atom.get_value("reason_context"),
        plan_active_requisite=x_atom.get_value("active_requisite"),
    )


def _modify_belief_plan_reasonunit_insert(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_belief.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        reason_context=x_atom.get_value("reason_context"),
        plan_active_requisite=x_atom.get_value("active_requisite"),
    )


def _modify_belief_plan_reason_caseunit_delete(
    x_belief: BeliefUnit, x_atom: BeliefAtom
):
    x_belief.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        reason_del_case_reason_context=x_atom.get_value("reason_context"),
        reason_del_case_reason_state=x_atom.get_value("reason_state"),
    )


def _modify_belief_plan_reason_caseunit_update(
    x_belief: BeliefUnit, x_atom: BeliefAtom
):
    x_belief.edit_plan_attr(
        x_atom.get_value("plan_rope"),
        reason_context=x_atom.get_value("reason_context"),
        reason_case=x_atom.get_value("reason_state"),
        reason_lower=x_atom.get_value("reason_lower"),
        reason_upper=x_atom.get_value("reason_upper"),
        reason_divisor=x_atom.get_value("reason_divisor"),
    )


def _modify_belief_plan_reason_caseunit_insert(
    x_belief: BeliefUnit, x_atom: BeliefAtom
):
    x_planunit = x_belief.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.set_reason_case(
        reason_context=x_atom.get_value("reason_context"),
        case=x_atom.get_value("reason_state"),
        reason_lower=x_atom.get_value("reason_lower"),
        reason_upper=x_atom.get_value("reason_upper"),
        reason_divisor=x_atom.get_value("reason_divisor"),
    )


def _modify_belief_plan_partyunit_delete(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_planunit = x_belief.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.laborunit.del_partyunit(party_title=x_atom.get_value("party_title"))


def _modify_belief_plan_partyunit_insert(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_planunit = x_belief.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.laborunit.add_party(party_title=x_atom.get_value("party_title"))


def _modify_belief_plan_healerunit_delete(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_planunit = x_belief.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.healerunit.del_healer_name(x_atom.get_value("healer_name"))


def _modify_belief_plan_healerunit_insert(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_planunit = x_belief.get_plan_obj(x_atom.get_value("plan_rope"))
    x_planunit.healerunit.set_healer_name(x_atom.get_value("healer_name"))


def _modify_belief_voiceunit_delete(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_belief.del_voiceunit(x_atom.get_value("voice_name"))


def _modify_belief_voiceunit_update(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_belief.edit_voiceunit(
        voice_name=x_atom.get_value("voice_name"),
        voice_cred_lumen=x_atom.get_value("voice_cred_lumen"),
        voice_debt_lumen=x_atom.get_value("voice_debt_lumen"),
    )


def _modify_belief_voiceunit_insert(x_belief: BeliefUnit, x_atom: BeliefAtom):
    x_belief.set_voiceunit(
        voiceunit_shop(
            voice_name=x_atom.get_value("voice_name"),
            voice_cred_lumen=x_atom.get_value("voice_cred_lumen"),
            voice_debt_lumen=x_atom.get_value("voice_debt_lumen"),
        )
    )


def _modify_belief_beliefunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "UPDATE":
        _modify_belief_update_beliefunit(x_belief, x_atom)


def _modify_belief_voice_membership(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "DELETE":
        _modify_belief_voice_membership_delete(x_belief, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_belief_voice_membership_update(x_belief, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_belief_voice_membership_insert(x_belief, x_atom)


def _modify_belief_planunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "DELETE":
        _modify_belief_planunit_delete(x_belief, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_belief_planunit_update(x_belief, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_belief_planunit_insert(x_belief, x_atom)


def _modify_belief_plan_awardunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "DELETE":
        _modify_belief_plan_awardunit_delete(x_belief, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_belief_plan_awardunit_update(x_belief, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_belief_plan_awardunit_insert(x_belief, x_atom)


def _modify_belief_plan_factunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "DELETE":
        _modify_belief_plan_factunit_delete(x_belief, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_belief_plan_factunit_update(x_belief, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_belief_plan_factunit_insert(x_belief, x_atom)


def _modify_belief_plan_reasonunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "DELETE":
        _modify_belief_plan_reasonunit_delete(x_belief, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_belief_plan_reasonunit_update(x_belief, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_belief_plan_reasonunit_insert(x_belief, x_atom)


def _modify_belief_plan_reason_caseunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "DELETE":
        _modify_belief_plan_reason_caseunit_delete(x_belief, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_belief_plan_reason_caseunit_update(x_belief, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_belief_plan_reason_caseunit_insert(x_belief, x_atom)


def _modify_belief_plan_partyunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "DELETE":
        _modify_belief_plan_partyunit_delete(x_belief, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_belief_plan_partyunit_insert(x_belief, x_atom)


def _modify_belief_plan_healerunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "DELETE":
        _modify_belief_plan_healerunit_delete(x_belief, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_belief_plan_healerunit_insert(x_belief, x_atom)


def _modify_belief_voiceunit(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.crud_str == "DELETE":
        _modify_belief_voiceunit_delete(x_belief, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_belief_voiceunit_update(x_belief, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_belief_voiceunit_insert(x_belief, x_atom)


def modify_belief_with_beliefatom(x_belief: BeliefUnit, x_atom: BeliefAtom):
    if x_atom.dimen == "beliefunit":
        _modify_belief_beliefunit(x_belief, x_atom)
    elif x_atom.dimen == "belief_voice_membership":
        _modify_belief_voice_membership(x_belief, x_atom)
    elif x_atom.dimen == "belief_planunit":
        _modify_belief_planunit(x_belief, x_atom)
    elif x_atom.dimen == "belief_plan_awardunit":
        _modify_belief_plan_awardunit(x_belief, x_atom)
    elif x_atom.dimen == "belief_plan_factunit":
        _modify_belief_plan_factunit(x_belief, x_atom)
    elif x_atom.dimen == "belief_plan_reasonunit":
        _modify_belief_plan_reasonunit(x_belief, x_atom)
    elif x_atom.dimen == "belief_plan_reason_caseunit":
        _modify_belief_plan_reason_caseunit(x_belief, x_atom)
    elif x_atom.dimen == "belief_plan_healerunit":
        _modify_belief_plan_healerunit(x_belief, x_atom)
    elif x_atom.dimen == "belief_plan_partyunit":
        _modify_belief_plan_partyunit(x_belief, x_atom)
    elif x_atom.dimen == "belief_voiceunit":
        _modify_belief_voiceunit(x_belief, x_atom)


def jvalues_different(dimen: str, x_obj: any, y_obj: any) -> bool:
    if dimen == "beliefunit":
        return (
            x_obj.tally != y_obj.tally
            or x_obj.max_tree_traverse != y_obj.max_tree_traverse
            or x_obj.credor_respect != y_obj.credor_respect
            or x_obj.debtor_respect != y_obj.debtor_respect
            or x_obj.respect_grain != y_obj.respect_grain
            or x_obj.fund_pool != y_obj.fund_pool
            or x_obj.fund_grain != y_obj.fund_grain
        )
    elif dimen in {"belief_voice_membership"}:
        return (x_obj.group_cred_lumen != y_obj.group_cred_lumen) or (
            x_obj.group_debt_lumen != y_obj.group_debt_lumen
        )
    elif dimen in {"belief_plan_awardunit"}:
        return (x_obj.give_force != y_obj.give_force) or (
            x_obj.take_force != y_obj.take_force
        )
    elif dimen == "belief_planunit":
        return (
            x_obj.addin != y_obj.addin
            or x_obj.begin != y_obj.begin
            or x_obj.close != y_obj.close
            or x_obj.denom != y_obj.denom
            or x_obj.numor != y_obj.numor
            or x_obj.morph != y_obj.morph
            or x_obj.star != y_obj.star
            or x_obj.pledge != y_obj.pledge
        )
    elif dimen == "belief_plan_factunit":
        return (
            (x_obj.fact_state != y_obj.fact_state)
            or (x_obj.reason_lower != y_obj.reason_lower)
            or (x_obj.reason_upper != y_obj.reason_upper)
        )
    elif dimen == "belief_plan_reasonunit":
        return x_obj.active_requisite != y_obj.active_requisite
    elif dimen == "belief_plan_reason_caseunit":
        return (
            x_obj.reason_lower != y_obj.reason_lower
            or x_obj.reason_upper != y_obj.reason_upper
            or x_obj.reason_divisor != y_obj.reason_divisor
        )
    elif dimen == "belief_voiceunit":
        return (x_obj.voice_cred_lumen != y_obj.voice_cred_lumen) or (
            x_obj.voice_debt_lumen != y_obj.voice_debt_lumen
        )


class InvalidBeliefAtomException(Exception):
    pass


def get_beliefatom_from_rowdata(x_rowdata: RowData) -> BeliefAtom:
    dimen_str, crud_str = get_dimen_from_dict(x_rowdata.row_dict)
    x_atom = beliefatom_shop(dimen=dimen_str, crud_str=crud_str)
    front_len = len(dimen_str) + len(crud_str) + 2
    for x_columnname, x_value in x_rowdata.row_dict.items():
        arg_key = x_columnname[front_len:]
        x_atom.set_arg(x_key=arg_key, x_value=x_value)
    return x_atom


@dataclass
class AtomRow:
    _atom_dimens: set[str] = None
    _crud_command: CRUD_command = None
    voice_name: VoiceName = None
    addin: float = None
    awardee_title: TitleTerm = None
    reason_context: RopeTerm = None
    active_requisite: bool = None
    begin: float = None
    respect_grain: float = None
    close: float = None
    voice_cred_lumen: int = None
    group_cred_lumen: int = None
    credor_respect: int = None
    voice_debt_lumen: int = None
    group_debt_lumen: int = None
    debtor_respect: int = None
    denom: int = None
    reason_divisor: int = None
    fact_context: RopeTerm = None
    fact_upper: float = None
    fact_lower: float = None
    fund_grain: float = None
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
    money_grain: float = None
    fact_state: RopeTerm = None
    pledge: bool = None
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
                    self.__dict__[x_arg] = VoiceName(x_value)
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

    def get_beliefatoms(self) -> list[BeliefAtom]:
        self._set_class_types()
        x_list = []
        for x_dimen in self._atom_dimens:
            x_atom = beliefatom_shop(x_dimen, self._crud_command)
            x_args = get_atom_config_args(x_dimen)
            for x_arg in x_args:
                if self.__dict__[x_arg] != None:
                    x_atom.set_arg(x_arg, self.__dict__[x_arg])
            if x_atom.is_valid() > 0:
                x_list.append(x_atom)
        return x_list


def atomrow_shop(atom_dimens: set[str], crud_command: CRUD_command) -> AtomRow:
    return AtomRow(_atom_dimens=atom_dimens, _crud_command=crud_command)


def sift_beliefatom(x_belief: BeliefUnit, x_atom: BeliefAtom) -> BeliefAtom:
    config_keys = get_atom_config_jkeys(x_atom.dimen)
    x_atom_reqs = {x_key: x_atom.get_value(x_key) for x_key in config_keys}

    x_exists = belief_attr_exists(x_atom.dimen, x_belief, x_atom_reqs)

    if x_atom.crud_str == "DELETE" and x_exists:
        return x_atom
    elif x_atom.crud_str == "INSERT" and not x_exists:
        return x_atom
    elif x_atom.crud_str == "INSERT":
        x_belief_obj = belief_get_obj(x_atom.dimen, x_belief, x_atom_reqs)
        x_jvalues = x_atom.get_jvalues_dict()
        update_atom = beliefatom_shop(x_atom.dimen, "UPDATE", x_atom.jkeys)
        for jvalue in x_jvalues:
            optional_jvalue = x_atom.get_value(jvalue)
            obj_jvalue = x_belief_obj.__dict__[jvalue]
            if obj_jvalue != optional_jvalue:
                update_atom.set_arg(jvalue, optional_jvalue)

        if update_atom.get_jvalues_dict() != {}:
            return update_atom
    return None
