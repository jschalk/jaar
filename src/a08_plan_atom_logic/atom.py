from dataclasses import dataclass
from src.a00_data_toolbox.db_toolbox import RowData, create_type_reference_insert_sqlstr
from src.a00_data_toolbox.dict_toolbox import (
    get_dict_from_json,
    get_empty_dict_if_None,
    get_json_from_dict,
)
from src.a01_term_logic.term import AcctName, LabelTerm, TitleTerm, WayTerm
from src.a01_term_logic.way import create_way, get_parent_way, get_tail_label
from src.a03_group_logic.acct import acctunit_shop
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import PlanUnit
from src.a06_plan_logic.plan_tool import plan_attr_exists, plan_get_obj
from src.a08_plan_atom_logic.atom_config import (
    CRUD_command,
    get_atom_args_class_types,
    get_atom_config_args,
    get_atom_config_dict,
    get_atom_config_jkeys,
    get_atom_order,
    get_dimen_from_dict,
    get_sorted_jkey_keys,
    is_plan_dimen,
)


class PlanAtomDescriptionException(Exception):
    pass


@dataclass
class PlanAtom:
    dimen: str = None
    crud_str: str = None
    jkeys: dict[str, str] = None
    jvalues: dict[str, str] = None
    atom_order: int = None

    def get_insert_sqlstr(self) -> str:
        if self.is_valid() is False:
            raise PlanAtomDescriptionException(
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
        # When ChangUnit places an PlanAtom in a nested dictionary ChangUnit.planatoms
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


def planatom_shop(
    dimen: str,
    crud_str: str = None,
    jkeys: dict[str, str] = None,
    jvalues: dict[str, str] = None,
) -> PlanAtom:
    if is_plan_dimen(dimen):
        return PlanAtom(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=get_empty_dict_if_None(jkeys),
            jvalues=get_empty_dict_if_None(jvalues),
        )


def get_from_dict(x_dict: dict) -> PlanAtom:
    x_atom = planatom_shop(x_dict["dimen"], x_dict["crud"])
    for x_key, x_value in x_dict["jkeys"].items():
        x_atom.set_jkey(x_key, x_value)
    for x_key, x_value in x_dict["jvalues"].items():
        x_atom.set_jvalue(x_key, x_value)
    return x_atom


def get_from_json(x_str: str) -> PlanAtom:
    return get_from_dict(get_dict_from_json(x_str))


def _modify_plan_update_planunit(x_plan: PlanUnit, x_atom: PlanAtom):
    x_arg = "max_tree_traverse"
    if x_atom.get_value(x_arg) is not None:
        x_plan.set_max_tree_traverse(x_atom.get_value(x_arg))
    x_arg = "credor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_plan.set_credor_respect(x_atom.get_value(x_arg))
    x_arg = "debtor_respect"
    if x_atom.get_value(x_arg) is not None:
        x_plan.set_debtor_respect(x_atom.get_value(x_arg))
    x_arg = "fund_pool"
    if x_atom.get_value(x_arg) is not None:
        x_plan.fund_pool = x_atom.get_value(x_arg)
    x_arg = "fund_iota"
    if x_atom.get_value(x_arg) is not None:
        x_plan.fund_iota = x_atom.get_value(x_arg)
    x_arg = "tally"
    if x_atom.get_value(x_arg) is not None:
        x_plan.tally = x_atom.get_value(x_arg)
    x_arg = "respect_bit"
    if x_atom.get_value(x_arg) is not None:
        x_plan.respect_bit = x_atom.get_value(x_arg)
    x_arg = "penny"
    if x_atom.get_value(x_arg) is not None:
        x_plan.penny = x_atom.get_value(x_arg)


def _modify_plan_acct_membership_delete(x_plan: PlanUnit, x_atom: PlanAtom):
    x_acct_name = x_atom.get_value("acct_name")
    x_group_title = x_atom.get_value("group_title")
    x_plan.get_acct(x_acct_name).delete_membership(x_group_title)


def _modify_plan_acct_membership_update(x_plan: PlanUnit, x_atom: PlanAtom):
    x_acct_name = x_atom.get_value("acct_name")
    x_group_title = x_atom.get_value("group_title")
    x_acctunit = x_plan.get_acct(x_acct_name)
    x_membership = x_acctunit.get_membership(x_group_title)
    x_credit_vote = x_atom.get_value("credit_vote")
    x_debtit_vote = x_atom.get_value("debtit_vote")
    x_membership.set_credit_vote(x_credit_vote)
    x_membership.set_debtit_vote(x_debtit_vote)


def _modify_plan_acct_membership_insert(x_plan: PlanUnit, x_atom: PlanAtom):
    x_acct_name = x_atom.get_value("acct_name")
    x_group_title = x_atom.get_value("group_title")
    x_credit_vote = x_atom.get_value("credit_vote")
    x_debtit_vote = x_atom.get_value("debtit_vote")
    x_acctunit = x_plan.get_acct(x_acct_name)
    x_acctunit.add_membership(x_group_title, x_credit_vote, x_debtit_vote)


def _modify_plan_conceptunit_delete(x_plan: PlanUnit, x_atom: PlanAtom):
    concept_way = create_way(x_atom.get_value("concept_way"), bridge=x_plan.bridge)
    x_plan.del_concept_obj(concept_way, del_children=x_atom.get_value("del_children"))


def _modify_plan_conceptunit_update(x_plan: PlanUnit, x_atom: PlanAtom):
    concept_way = create_way(x_atom.get_value("concept_way"), bridge=x_plan.bridge)
    x_plan.edit_concept_attr(
        concept_way,
        addin=x_atom.get_value("addin"),
        begin=x_atom.get_value("begin"),
        gogo_want=x_atom.get_value("gogo_want"),
        stop_want=x_atom.get_value("stop_want"),
        close=x_atom.get_value("close"),
        denom=x_atom.get_value("denom"),
        numor=x_atom.get_value("numor"),
        morph=x_atom.get_value("morph"),
        mass=x_atom.get_value("mass"),
        task=x_atom.get_value("task"),
    )


def _modify_plan_conceptunit_insert(x_plan: PlanUnit, x_atom: PlanAtom):
    concept_way = x_atom.get_value("concept_way")
    concept_label = get_tail_label(concept_way)
    concept_parent_way = get_parent_way(concept_way)
    x_plan.set_concept(
        concept_kid=conceptunit_shop(
            concept_label=concept_label,
            addin=x_atom.get_value("addin"),
            begin=x_atom.get_value("begin"),
            close=x_atom.get_value("close"),
            gogo_want=x_atom.get_value("gogo_want"),
            stop_want=x_atom.get_value("stop_want"),
            denom=x_atom.get_value("denom"),
            numor=x_atom.get_value("numor"),
            task=x_atom.get_value("task"),
        ),
        parent_way=concept_parent_way,
        create_missing_concepts=False,
        get_rid_of_missing_awardlinks_awardee_titles=False,
        create_missing_ancestors=True,
    )


def _modify_plan_concept_awardlink_delete(x_plan: PlanUnit, x_atom: PlanAtom):
    x_plan.edit_concept_attr(
        x_atom.get_value("concept_way"),
        awardlink_del=x_atom.get_value("awardee_title"),
    )


def _modify_plan_concept_awardlink_update(x_plan: PlanUnit, x_atom: PlanAtom):
    x_concept = x_plan.get_concept_obj(x_atom.get_value("concept_way"))
    x_awardlink = x_concept.awardlinks.get(x_atom.get_value("awardee_title"))
    x_give_force = x_atom.get_value("give_force")
    if x_give_force is not None and x_awardlink.give_force != x_give_force:
        x_awardlink.give_force = x_give_force
    x_take_force = x_atom.get_value("take_force")
    if x_take_force is not None and x_awardlink.take_force != x_take_force:
        x_awardlink.take_force = x_take_force
    x_plan.edit_concept_attr(x_atom.get_value("concept_way"), awardlink=x_awardlink)


def _modify_plan_concept_awardlink_insert(x_plan: PlanUnit, x_atom: PlanAtom):
    x_awardlink = awardlink_shop(
        awardee_title=x_atom.get_value("awardee_title"),
        give_force=x_atom.get_value("give_force"),
        take_force=x_atom.get_value("take_force"),
    )
    x_plan.edit_concept_attr(x_atom.get_value("concept_way"), awardlink=x_awardlink)


def _modify_plan_concept_factunit_delete(x_plan: PlanUnit, x_atom: PlanAtom):
    x_conceptunit = x_plan.get_concept_obj(x_atom.get_value("concept_way"))
    x_conceptunit.del_factunit(x_atom.get_value("fcontext"))


def _modify_plan_concept_factunit_update(x_plan: PlanUnit, x_atom: PlanAtom):
    x_conceptunit = x_plan.get_concept_obj(x_atom.get_value("concept_way"))
    x_factunit = x_conceptunit.factunits.get(x_atom.get_value("fcontext"))
    x_factunit.set_attr(
        fstate=x_atom.get_value("fstate"),
        fopen=x_atom.get_value("fopen"),
        fnigh=x_atom.get_value("fnigh"),
    )


def _modify_plan_concept_factunit_insert(x_plan: PlanUnit, x_atom: PlanAtom):
    x_plan.edit_concept_attr(
        x_atom.get_value("concept_way"),
        factunit=factunit_shop(
            fcontext=x_atom.get_value("fcontext"),
            fstate=x_atom.get_value("fstate"),
            fopen=x_atom.get_value("fopen"),
            fnigh=x_atom.get_value("fnigh"),
        ),
    )


def _modify_plan_concept_reasonunit_delete(x_plan: PlanUnit, x_atom: PlanAtom):
    x_conceptunit = x_plan.get_concept_obj(x_atom.get_value("concept_way"))
    x_conceptunit.del_reasonunit_rcontext(x_atom.get_value("rcontext"))


def _modify_plan_concept_reasonunit_update(x_plan: PlanUnit, x_atom: PlanAtom):
    x_plan.edit_concept_attr(
        x_atom.get_value("concept_way"),
        reason_rcontext=x_atom.get_value("rcontext"),
        reason_rconcept_active_requisite=x_atom.get_value("rconcept_active_requisite"),
    )


def _modify_plan_concept_reasonunit_insert(x_plan: PlanUnit, x_atom: PlanAtom):
    x_plan.edit_concept_attr(
        x_atom.get_value("concept_way"),
        reason_rcontext=x_atom.get_value("rcontext"),
        reason_rconcept_active_requisite=x_atom.get_value("rconcept_active_requisite"),
    )


def _modify_plan_concept_reason_premiseunit_delete(x_plan: PlanUnit, x_atom: PlanAtom):
    x_plan.edit_concept_attr(
        x_atom.get_value("concept_way"),
        reason_del_premise_rcontext=x_atom.get_value("rcontext"),
        reason_del_premise_pstate=x_atom.get_value("pstate"),
    )


def _modify_plan_concept_reason_premiseunit_update(x_plan: PlanUnit, x_atom: PlanAtom):
    x_plan.edit_concept_attr(
        x_atom.get_value("concept_way"),
        reason_rcontext=x_atom.get_value("rcontext"),
        reason_premise=x_atom.get_value("pstate"),
        popen=x_atom.get_value("popen"),
        reason_pnigh=x_atom.get_value("pnigh"),
        pdivisor=x_atom.get_value("pdivisor"),
    )


def _modify_plan_concept_reason_premiseunit_insert(x_plan: PlanUnit, x_atom: PlanAtom):
    x_conceptunit = x_plan.get_concept_obj(x_atom.get_value("concept_way"))
    x_conceptunit.set_reason_premise(
        rcontext=x_atom.get_value("rcontext"),
        premise=x_atom.get_value("pstate"),
        popen=x_atom.get_value("popen"),
        pnigh=x_atom.get_value("pnigh"),
        pdivisor=x_atom.get_value("pdivisor"),
    )


def _modify_plan_concept_laborlink_delete(x_plan: PlanUnit, x_atom: PlanAtom):
    x_conceptunit = x_plan.get_concept_obj(x_atom.get_value("concept_way"))
    x_conceptunit.laborunit.del_laborlink(labor_title=x_atom.get_value("labor_title"))


def _modify_plan_concept_laborlink_insert(x_plan: PlanUnit, x_atom: PlanAtom):
    x_conceptunit = x_plan.get_concept_obj(x_atom.get_value("concept_way"))
    x_conceptunit.laborunit.set_laborlink(labor_title=x_atom.get_value("labor_title"))


def _modify_plan_concept_healerlink_delete(x_plan: PlanUnit, x_atom: PlanAtom):
    x_conceptunit = x_plan.get_concept_obj(x_atom.get_value("concept_way"))
    x_conceptunit.healerlink.del_healer_name(x_atom.get_value("healer_name"))


def _modify_plan_concept_healerlink_insert(x_plan: PlanUnit, x_atom: PlanAtom):
    x_conceptunit = x_plan.get_concept_obj(x_atom.get_value("concept_way"))
    x_conceptunit.healerlink.set_healer_name(x_atom.get_value("healer_name"))


def _modify_plan_acctunit_delete(x_plan: PlanUnit, x_atom: PlanAtom):
    x_plan.del_acctunit(x_atom.get_value("acct_name"))


def _modify_plan_acctunit_update(x_plan: PlanUnit, x_atom: PlanAtom):
    x_plan.edit_acctunit(
        acct_name=x_atom.get_value("acct_name"),
        credit_belief=x_atom.get_value("credit_belief"),
        debtit_belief=x_atom.get_value("debtit_belief"),
    )


def _modify_plan_acctunit_insert(x_plan: PlanUnit, x_atom: PlanAtom):
    x_plan.set_acctunit(
        acctunit_shop(
            acct_name=x_atom.get_value("acct_name"),
            credit_belief=x_atom.get_value("credit_belief"),
            debtit_belief=x_atom.get_value("debtit_belief"),
        )
    )


def _modify_plan_planunit(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "UPDATE":
        _modify_plan_update_planunit(x_plan, x_atom)


def _modify_plan_acct_membership(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "DELETE":
        _modify_plan_acct_membership_delete(x_plan, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_plan_acct_membership_update(x_plan, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_plan_acct_membership_insert(x_plan, x_atom)


def _modify_plan_conceptunit(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "DELETE":
        _modify_plan_conceptunit_delete(x_plan, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_plan_conceptunit_update(x_plan, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_plan_conceptunit_insert(x_plan, x_atom)


def _modify_plan_concept_awardlink(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "DELETE":
        _modify_plan_concept_awardlink_delete(x_plan, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_plan_concept_awardlink_update(x_plan, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_plan_concept_awardlink_insert(x_plan, x_atom)


def _modify_plan_concept_factunit(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "DELETE":
        _modify_plan_concept_factunit_delete(x_plan, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_plan_concept_factunit_update(x_plan, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_plan_concept_factunit_insert(x_plan, x_atom)


def _modify_plan_concept_reasonunit(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "DELETE":
        _modify_plan_concept_reasonunit_delete(x_plan, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_plan_concept_reasonunit_update(x_plan, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_plan_concept_reasonunit_insert(x_plan, x_atom)


def _modify_plan_concept_reason_premiseunit(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "DELETE":
        _modify_plan_concept_reason_premiseunit_delete(x_plan, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_plan_concept_reason_premiseunit_update(x_plan, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_plan_concept_reason_premiseunit_insert(x_plan, x_atom)


def _modify_plan_concept_laborlink(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "DELETE":
        _modify_plan_concept_laborlink_delete(x_plan, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_plan_concept_laborlink_insert(x_plan, x_atom)


def _modify_plan_concept_healerlink(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "DELETE":
        _modify_plan_concept_healerlink_delete(x_plan, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_plan_concept_healerlink_insert(x_plan, x_atom)


def _modify_plan_acctunit(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.crud_str == "DELETE":
        _modify_plan_acctunit_delete(x_plan, x_atom)
    elif x_atom.crud_str == "UPDATE":
        _modify_plan_acctunit_update(x_plan, x_atom)
    elif x_atom.crud_str == "INSERT":
        _modify_plan_acctunit_insert(x_plan, x_atom)


def modify_plan_with_planatom(x_plan: PlanUnit, x_atom: PlanAtom):
    if x_atom.dimen == "planunit":
        _modify_plan_planunit(x_plan, x_atom)
    elif x_atom.dimen == "plan_acct_membership":
        _modify_plan_acct_membership(x_plan, x_atom)
    elif x_atom.dimen == "plan_conceptunit":
        _modify_plan_conceptunit(x_plan, x_atom)
    elif x_atom.dimen == "plan_concept_awardlink":
        _modify_plan_concept_awardlink(x_plan, x_atom)
    elif x_atom.dimen == "plan_concept_factunit":
        _modify_plan_concept_factunit(x_plan, x_atom)
    elif x_atom.dimen == "plan_concept_reasonunit":
        _modify_plan_concept_reasonunit(x_plan, x_atom)
    elif x_atom.dimen == "plan_concept_reason_premiseunit":
        _modify_plan_concept_reason_premiseunit(x_plan, x_atom)
    elif x_atom.dimen == "plan_concept_healerlink":
        _modify_plan_concept_healerlink(x_plan, x_atom)
    elif x_atom.dimen == "plan_concept_laborlink":
        _modify_plan_concept_laborlink(x_plan, x_atom)
    elif x_atom.dimen == "plan_acctunit":
        _modify_plan_acctunit(x_plan, x_atom)


def jvalues_different(dimen: str, x_obj: any, y_obj: any) -> bool:
    if dimen == "planunit":
        return (
            x_obj.tally != y_obj.tally
            or x_obj.max_tree_traverse != y_obj.max_tree_traverse
            or x_obj.credor_respect != y_obj.credor_respect
            or x_obj.debtor_respect != y_obj.debtor_respect
            or x_obj.respect_bit != y_obj.respect_bit
            or x_obj.fund_pool != y_obj.fund_pool
            or x_obj.fund_iota != y_obj.fund_iota
        )
    elif dimen in {"plan_acct_membership"}:
        return (x_obj.credit_vote != y_obj.credit_vote) or (
            x_obj.debtit_vote != y_obj.debtit_vote
        )
    elif dimen in {"plan_concept_awardlink"}:
        return (x_obj.give_force != y_obj.give_force) or (
            x_obj.take_force != y_obj.take_force
        )
    elif dimen == "plan_conceptunit":
        return (
            x_obj.addin != y_obj.addin
            or x_obj.begin != y_obj.begin
            or x_obj.close != y_obj.close
            or x_obj.denom != y_obj.denom
            or x_obj.numor != y_obj.numor
            or x_obj.morph != y_obj.morph
            or x_obj.mass != y_obj.mass
            or x_obj.task != y_obj.task
        )
    elif dimen == "plan_concept_factunit":
        return (
            (x_obj.fstate != y_obj.fstate)
            or (x_obj.popen != y_obj.popen)
            or (x_obj.pnigh != y_obj.pnigh)
        )
    elif dimen == "plan_concept_reasonunit":
        return x_obj.rconcept_active_requisite != y_obj.rconcept_active_requisite
    elif dimen == "plan_concept_reason_premiseunit":
        return (
            x_obj.popen != y_obj.popen
            or x_obj.pnigh != y_obj.pnigh
            or x_obj.pdivisor != y_obj.pdivisor
        )
    elif dimen == "plan_acctunit":
        return (x_obj.credit_belief != y_obj.credit_belief) or (
            x_obj.debtit_belief != y_obj.debtit_belief
        )


class InvalidPlanAtomException(Exception):
    pass


def get_planatom_from_rowdata(x_rowdata: RowData) -> PlanAtom:
    dimen_str, crud_str = get_dimen_from_dict(x_rowdata.row_dict)
    x_atom = planatom_shop(dimen=dimen_str, crud_str=crud_str)
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
    awardee_title: TitleTerm = None
    rcontext: WayTerm = None
    rconcept_active_requisite: bool = None
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
    pdivisor: int = None
    fcontext: WayTerm = None
    fnigh: float = None
    fopen: float = None
    fund_iota: float = None
    fund_pool: float = None
    give_force: float = None
    gogo_want: float = None
    group_title: TitleTerm = None
    healer_name: TitleTerm = None
    mass: int = None
    max_tree_traverse: int = None
    morph: bool = None
    pstate: WayTerm = None
    pnigh: float = None
    numor: int = None
    popen: float = None
    penny: float = None
    fstate: WayTerm = None
    task: bool = None
    problem_bool: bool = None
    concept_way: WayTerm = None
    stop_want: float = None
    take_force: float = None
    tally: int = None
    labor_title: int = None

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
                    self.__dict__[x_arg] = AcctName(x_value)
                elif class_type == "TitleTerm":
                    self.__dict__[x_arg] = TitleTerm(x_value)
                elif class_type == "WayTerm":
                    self.__dict__[x_arg] = WayTerm(x_value)
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

    def get_planatoms(self) -> list[PlanAtom]:
        self._set_class_types()
        x_list = []
        for x_dimen in self._atom_dimens:
            x_atom = planatom_shop(x_dimen, self._crud_command)
            x_args = get_atom_config_args(x_dimen)
            for x_arg in x_args:
                if self.__dict__[x_arg] != None:
                    x_atom.set_arg(x_arg, self.__dict__[x_arg])
            if x_atom.is_valid() > 0:
                x_list.append(x_atom)
        return x_list


def atomrow_shop(atom_dimens: set[str], crud_command: CRUD_command) -> AtomRow:
    return AtomRow(_atom_dimens=atom_dimens, _crud_command=crud_command)


def sift_planatom(x_plan: PlanUnit, x_atom: PlanAtom) -> PlanAtom:
    config_keys = get_atom_config_jkeys(x_atom.dimen)
    x_atom_reqs = {x_key: x_atom.get_value(x_key) for x_key in config_keys}

    x_exists = plan_attr_exists(x_atom.dimen, x_plan, x_atom_reqs)
    print(f"{x_exists=}")

    if x_atom.crud_str == "DELETE" and x_exists:
        return x_atom
    elif x_atom.crud_str == "INSERT" and not x_exists:
        return x_atom
    elif x_atom.crud_str == "INSERT":
        x_plan_obj = plan_get_obj(x_atom.dimen, x_plan, x_atom_reqs)
        x_jvalues = x_atom.get_jvalues_dict()
        update_atom = planatom_shop(x_atom.dimen, "UPDATE", x_atom.jkeys)
        for jvalue in x_jvalues:
            optional_jvalue = x_atom.get_value(jvalue)
            obj_jvalue = x_plan_obj.__dict__[jvalue]
            if obj_jvalue != optional_jvalue:
                update_atom.set_arg(jvalue, optional_jvalue)

        if update_atom.get_jvalues_dict() != {}:
            return update_atom
    return None
