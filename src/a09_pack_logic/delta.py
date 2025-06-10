from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_all_nondictionary_objs,
    get_empty_dict_if_None,
    get_from_nested_dict,
    get_json_from_dict,
    set_in_nested_dict,
)
from src.a01_term_logic.term import TitleTerm, WayTerm
from src.a03_group_logic.acct import AcctName, AcctUnit, MemberShip
from src.a03_group_logic.group import MemberShip
from src.a04_reason_logic.reason_concept import FactUnit, ReasonUnit
from src.a05_concept_logic.concept import ConceptUnit
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a08_plan_atom_logic.atom import (
    InvalidPlanAtomException,
    PlanAtom,
    get_from_dict as get_planatom_from_dict,
    jvalues_different,
    modify_plan_with_planatom,
    planatom_shop,
    sift_planatom,
)
from src.a08_plan_atom_logic.atom_config import CRUD_command


@dataclass
class PlanDelta:
    planatoms: dict[CRUD_command : dict[str, PlanAtom]] = None
    _plan_build_validated: bool = None

    def _get_crud_planatoms_list(self) -> dict[CRUD_command, list[PlanAtom]]:
        return get_all_nondictionary_objs(self.planatoms)

    def get_dimen_sorted_planatoms_list(self) -> list[PlanAtom]:
        atoms_list = []
        for crud_list in self._get_crud_planatoms_list().values():
            atoms_list.extend(iter(crud_list))

        atom_order_key_dict = {}
        for x_atom in atoms_list:
            atom_order_list = atom_order_key_dict.get(x_atom.atom_order)
            if atom_order_list is None:
                atom_order_key_dict[x_atom.atom_order] = [x_atom]
            else:
                atom_order_list.append(x_atom)

        ordered_list = []
        for x_list in atom_order_key_dict.values():
            if x_list[0].jkeys.get("concept_way") is not None:
                x_list = sorted(x_list, key=lambda x: x.jkeys.get("concept_way"))
            ordered_list.extend(x_list)
        return ordered_list

    def get_sorted_planatoms(self) -> list[PlanAtom]:
        planatoms_list = self.get_dimen_sorted_planatoms_list()
        return sorted(planatoms_list, key=lambda x: x.atom_order)

    def get_edited_plan(self, before_plan: PlanUnit) -> PlanUnit:
        edited_plan = copy_deepcopy(before_plan)
        for x_planatom in self.get_sorted_planatoms():
            modify_plan_with_planatom(edited_plan, x_planatom)
        return edited_plan

    def set_planatom(self, x_planatom: PlanAtom):
        if x_planatom.is_valid() is False:
            raise InvalidPlanAtomException(
                f"""'{x_planatom.dimen}' {x_planatom.crud_str} PlanAtom is invalid
                {x_planatom.is_jkeys_valid()=}
                {x_planatom.is_jvalues_valid()=}"""
            )

        x_planatom.set_atom_order()
        x_keylist = [
            x_planatom.crud_str,
            x_planatom.dimen,
            *x_planatom.get_nesting_order_args(),
        ]
        set_in_nested_dict(self.planatoms, x_keylist, x_planatom)

    def planatom_exists(self, x_planatom: PlanAtom) -> bool:
        if x_planatom.is_valid() is False:
            raise InvalidPlanAtomException(
                f"""'{x_planatom.dimen}' {x_planatom.crud_str} PlanAtom is invalid
                {x_planatom.is_jkeys_valid()=}
                {x_planatom.is_jvalues_valid()=}"""
            )

        x_planatom.set_atom_order()
        x_keylist = [
            x_planatom.crud_str,
            x_planatom.dimen,
            *list(x_planatom.get_nesting_order_args()),
        ]
        nested_planatom = get_from_nested_dict(self.planatoms, x_keylist, True)
        return nested_planatom == x_planatom

    def add_planatom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        x_planatom = planatom_shop(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=jkeys,
            jvalues=jvalues,
        )
        self.set_planatom(x_planatom)

    def get_planatom(self, crud_str: str, dimen: str, jkeys: list[str]) -> PlanAtom:
        x_keylist = [crud_str, dimen, *jkeys]
        return get_from_nested_dict(self.planatoms, x_keylist)

    def add_all_planatoms(self, after_plan: PlanUnit):
        before_plan = planunit_shop(after_plan.owner_name, after_plan.vow_label)
        self.add_all_different_planatoms(before_plan, after_plan)

    def add_all_different_planatoms(self, before_plan: PlanUnit, after_plan: PlanUnit):
        before_plan.settle_plan()
        after_plan.settle_plan()
        self.add_planatoms_planunit_simple_attrs(before_plan, after_plan)
        self.add_planatoms_accts(before_plan, after_plan)
        self.add_planatoms_concepts(before_plan, after_plan)

    def add_planatoms_planunit_simple_attrs(
        self, before_plan: PlanUnit, after_plan: PlanUnit
    ):
        if not jvalues_different("planunit", before_plan, after_plan):
            return
        x_planatom = planatom_shop("planunit", "UPDATE")
        if before_plan.max_tree_traverse != after_plan.max_tree_traverse:
            x_planatom.set_jvalue("max_tree_traverse", after_plan.max_tree_traverse)
        if before_plan.credor_respect != after_plan.credor_respect:
            x_planatom.set_jvalue("credor_respect", after_plan.credor_respect)
        if before_plan.debtor_respect != after_plan.debtor_respect:
            x_planatom.set_jvalue("debtor_respect", after_plan.debtor_respect)
        if before_plan.tally != after_plan.tally:
            x_planatom.set_jvalue("tally", after_plan.tally)
        if before_plan.fund_pool != after_plan.fund_pool:
            x_planatom.set_jvalue("fund_pool", after_plan.fund_pool)
        if before_plan.fund_iota != after_plan.fund_iota:
            x_planatom.set_jvalue("fund_iota", after_plan.fund_iota)
        if before_plan.respect_bit != after_plan.respect_bit:
            x_planatom.set_jvalue("respect_bit", after_plan.respect_bit)
        self.set_planatom(x_planatom)

    def add_planatoms_accts(self, before_plan: PlanUnit, after_plan: PlanUnit):
        before_acct_names = set(before_plan.accts.keys())
        after_acct_names = set(after_plan.accts.keys())

        self.add_planatom_acctunit_inserts(
            after_plan=after_plan,
            insert_acct_names=after_acct_names.difference(before_acct_names),
        )
        self.add_planatom_acctunit_deletes(
            before_plan=before_plan,
            delete_acct_names=before_acct_names.difference(after_acct_names),
        )
        self.add_planatom_acctunit_updates(
            before_plan=before_plan,
            after_plan=after_plan,
            update_acct_names=before_acct_names.intersection(after_acct_names),
        )

    def add_planatom_acctunit_inserts(
        self, after_plan: PlanUnit, insert_acct_names: set
    ):
        for insert_acct_name in insert_acct_names:
            insert_acctunit = after_plan.get_acct(insert_acct_name)
            x_planatom = planatom_shop("plan_acctunit", "INSERT")
            x_planatom.set_jkey("acct_name", insert_acctunit.acct_name)
            if insert_acctunit.credit_score is not None:
                x_planatom.set_jvalue("credit_score", insert_acctunit.credit_score)
            if insert_acctunit.debtit_score is not None:
                x_planatom.set_jvalue("debtit_score", insert_acctunit.debtit_score)
            self.set_planatom(x_planatom)
            all_group_titles = set(insert_acctunit._memberships.keys())
            self.add_planatom_memberships_inserts(
                after_acctunit=insert_acctunit,
                insert_membership_group_titles=all_group_titles,
            )

    def add_planatom_acctunit_updates(
        self, before_plan: PlanUnit, after_plan: PlanUnit, update_acct_names: set
    ):
        for acct_name in update_acct_names:
            after_acctunit = after_plan.get_acct(acct_name)
            before_acctunit = before_plan.get_acct(acct_name)
            if jvalues_different("plan_acctunit", after_acctunit, before_acctunit):
                x_planatom = planatom_shop("plan_acctunit", "UPDATE")
                x_planatom.set_jkey("acct_name", after_acctunit.acct_name)
                if before_acctunit.credit_score != after_acctunit.credit_score:
                    x_planatom.set_jvalue("credit_score", after_acctunit.credit_score)
                if before_acctunit.debtit_score != after_acctunit.debtit_score:
                    x_planatom.set_jvalue("debtit_score", after_acctunit.debtit_score)
                self.set_planatom(x_planatom)
            self.add_planatom_acctunit_update_memberships(
                after_acctunit=after_acctunit, before_acctunit=before_acctunit
            )

    def add_planatom_acctunit_deletes(
        self, before_plan: PlanUnit, delete_acct_names: set
    ):
        for delete_acct_name in delete_acct_names:
            x_planatom = planatom_shop("plan_acctunit", "DELETE")
            x_planatom.set_jkey("acct_name", delete_acct_name)
            self.set_planatom(x_planatom)
            delete_acctunit = before_plan.get_acct(delete_acct_name)
            non_mirror_group_titles = {
                x_group_title
                for x_group_title in delete_acctunit._memberships.keys()
                if x_group_title != delete_acct_name
            }
            self.add_planatom_memberships_delete(
                delete_acct_name, non_mirror_group_titles
            )

    def add_planatom_acctunit_update_memberships(
        self, after_acctunit: AcctUnit, before_acctunit: AcctUnit
    ):
        # before_non_mirror_group_titles
        before_group_titles = {
            x_group_title
            for x_group_title in before_acctunit._memberships.keys()
            if x_group_title != before_acctunit.acct_name
        }
        # after_non_mirror_group_titles
        after_group_titles = {
            x_group_title
            for x_group_title in after_acctunit._memberships.keys()
            if x_group_title != after_acctunit.acct_name
        }

        self.add_planatom_memberships_inserts(
            after_acctunit=after_acctunit,
            insert_membership_group_titles=after_group_titles.difference(
                before_group_titles
            ),
        )

        self.add_planatom_memberships_delete(
            before_acct_name=after_acctunit.acct_name,
            before_group_titles=before_group_titles.difference(after_group_titles),
        )

        update_group_titles = before_group_titles.intersection(after_group_titles)
        for update_acct_name in update_group_titles:
            before_membership = before_acctunit.get_membership(update_acct_name)
            after_membership = after_acctunit.get_membership(update_acct_name)
            if jvalues_different(
                "plan_acct_membership", before_membership, after_membership
            ):
                self.add_planatom_membership_update(
                    acct_name=after_acctunit.acct_name,
                    before_membership=before_membership,
                    after_membership=after_membership,
                )

    def add_planatom_memberships_inserts(
        self,
        after_acctunit: AcctUnit,
        insert_membership_group_titles: list[TitleTerm],
    ):
        after_acct_name = after_acctunit.acct_name
        for insert_group_title in insert_membership_group_titles:
            after_membership = after_acctunit.get_membership(insert_group_title)
            x_planatom = planatom_shop("plan_acct_membership", "INSERT")
            x_planatom.set_jkey("acct_name", after_acct_name)
            x_planatom.set_jkey("group_title", after_membership.group_title)
            if after_membership.credit_vote is not None:
                x_planatom.set_jvalue("credit_vote", after_membership.credit_vote)
            if after_membership.debtit_vote is not None:
                x_planatom.set_jvalue("debtit_vote", after_membership.debtit_vote)
            self.set_planatom(x_planatom)

    def add_planatom_membership_update(
        self,
        acct_name: AcctName,
        before_membership: MemberShip,
        after_membership: MemberShip,
    ):
        x_planatom = planatom_shop("plan_acct_membership", "UPDATE")
        x_planatom.set_jkey("acct_name", acct_name)
        x_planatom.set_jkey("group_title", after_membership.group_title)
        if after_membership.credit_vote != before_membership.credit_vote:
            x_planatom.set_jvalue("credit_vote", after_membership.credit_vote)
        if after_membership.debtit_vote != before_membership.debtit_vote:
            x_planatom.set_jvalue("debtit_vote", after_membership.debtit_vote)
        self.set_planatom(x_planatom)

    def add_planatom_memberships_delete(
        self, before_acct_name: AcctName, before_group_titles: TitleTerm
    ):
        for delete_group_title in before_group_titles:
            x_planatom = planatom_shop("plan_acct_membership", "DELETE")
            x_planatom.set_jkey("acct_name", before_acct_name)
            x_planatom.set_jkey("group_title", delete_group_title)
            self.set_planatom(x_planatom)

    def add_planatoms_concepts(self, before_plan: PlanUnit, after_plan: PlanUnit):
        before_concept_ways = set(before_plan._concept_dict.keys())
        after_concept_ways = set(after_plan._concept_dict.keys())

        self.add_planatom_concept_inserts(
            after_plan=after_plan,
            insert_concept_ways=after_concept_ways.difference(before_concept_ways),
        )
        self.add_planatom_concept_deletes(
            before_plan=before_plan,
            delete_concept_ways=before_concept_ways.difference(after_concept_ways),
        )
        self.add_planatom_concept_updates(
            before_plan=before_plan,
            after_plan=after_plan,
            update_ways=before_concept_ways.intersection(after_concept_ways),
        )

    def add_planatom_concept_inserts(
        self, after_plan: PlanUnit, insert_concept_ways: set
    ):
        for insert_concept_way in insert_concept_ways:
            insert_conceptunit = after_plan.get_concept_obj(insert_concept_way)
            x_planatom = planatom_shop("plan_conceptunit", "INSERT")
            x_planatom.set_jkey("concept_way", insert_conceptunit.get_concept_way())
            x_planatom.set_jvalue("addin", insert_conceptunit.addin)
            x_planatom.set_jvalue("begin", insert_conceptunit.begin)
            x_planatom.set_jvalue("close", insert_conceptunit.close)
            x_planatom.set_jvalue("denom", insert_conceptunit.denom)
            x_planatom.set_jvalue("numor", insert_conceptunit.numor)
            x_planatom.set_jvalue("morph", insert_conceptunit.morph)
            x_planatom.set_jvalue("mass", insert_conceptunit.mass)
            x_planatom.set_jvalue("task", insert_conceptunit.task)
            self.set_planatom(x_planatom)

            self.add_planatom_concept_factunit_inserts(
                conceptunit=insert_conceptunit,
                insert_factunit_rcontexts=set(insert_conceptunit.factunits.keys()),
            )
            self.add_planatom_concept_awardlink_inserts(
                after_conceptunit=insert_conceptunit,
                insert_awardlink_awardee_titles=set(
                    insert_conceptunit.awardlinks.keys()
                ),
            )
            self.add_planatom_concept_reasonunit_inserts(
                after_conceptunit=insert_conceptunit,
                insert_reasonunit_rcontexts=set(insert_conceptunit.reasonunits.keys()),
            )
            self.add_planatom_concept_laborlink_insert(
                concept_way=insert_concept_way,
                insert_laborlink_labor_titles=insert_conceptunit.laborunit._laborlinks,
            )
            self.add_planatom_concept_healerlink_insert(
                concept_way=insert_concept_way,
                insert_healerlink_healer_names=insert_conceptunit.healerlink._healer_names,
            )

    def add_planatom_concept_updates(
        self, before_plan: PlanUnit, after_plan: PlanUnit, update_ways: set
    ):
        for concept_way in update_ways:
            after_conceptunit = after_plan.get_concept_obj(concept_way)
            before_conceptunit = before_plan.get_concept_obj(concept_way)
            if jvalues_different(
                "plan_conceptunit", before_conceptunit, after_conceptunit
            ):
                x_planatom = planatom_shop("plan_conceptunit", "UPDATE")
                x_planatom.set_jkey("concept_way", after_conceptunit.get_concept_way())
                if before_conceptunit.addin != after_conceptunit.addin:
                    x_planatom.set_jvalue("addin", after_conceptunit.addin)
                if before_conceptunit.begin != after_conceptunit.begin:
                    x_planatom.set_jvalue("begin", after_conceptunit.begin)
                if before_conceptunit.close != after_conceptunit.close:
                    x_planatom.set_jvalue("close", after_conceptunit.close)
                if before_conceptunit.denom != after_conceptunit.denom:
                    x_planatom.set_jvalue("denom", after_conceptunit.denom)
                if before_conceptunit.numor != after_conceptunit.numor:
                    x_planatom.set_jvalue("numor", after_conceptunit.numor)
                if before_conceptunit.morph != after_conceptunit.morph:
                    x_planatom.set_jvalue("morph", after_conceptunit.morph)
                if before_conceptunit.mass != after_conceptunit.mass:
                    x_planatom.set_jvalue("mass", after_conceptunit.mass)
                if before_conceptunit.task != after_conceptunit.task:
                    x_planatom.set_jvalue("task", after_conceptunit.task)
                self.set_planatom(x_planatom)

            # insert / update / delete factunits
            before_factunit_rcontexts = set(before_conceptunit.factunits.keys())
            after_factunit_rcontexts = set(after_conceptunit.factunits.keys())
            self.add_planatom_concept_factunit_inserts(
                conceptunit=after_conceptunit,
                insert_factunit_rcontexts=after_factunit_rcontexts.difference(
                    before_factunit_rcontexts
                ),
            )
            self.add_planatom_concept_factunit_updates(
                before_conceptunit=before_conceptunit,
                after_conceptunit=after_conceptunit,
                update_factunit_rcontexts=before_factunit_rcontexts.intersection(
                    after_factunit_rcontexts
                ),
            )
            self.add_planatom_concept_factunit_deletes(
                concept_way=concept_way,
                delete_factunit_rcontexts=before_factunit_rcontexts.difference(
                    after_factunit_rcontexts
                ),
            )

            # insert / update / delete awardunits
            before_awardlinks_awardee_titles = set(before_conceptunit.awardlinks.keys())
            after_awardlinks_awardee_titles = set(after_conceptunit.awardlinks.keys())
            self.add_planatom_concept_awardlink_inserts(
                after_conceptunit=after_conceptunit,
                insert_awardlink_awardee_titles=after_awardlinks_awardee_titles.difference(
                    before_awardlinks_awardee_titles
                ),
            )
            self.add_planatom_concept_awardlink_updates(
                before_conceptunit=before_conceptunit,
                after_conceptunit=after_conceptunit,
                update_awardlink_awardee_titles=before_awardlinks_awardee_titles.intersection(
                    after_awardlinks_awardee_titles
                ),
            )
            self.add_planatom_concept_awardlink_deletes(
                concept_way=concept_way,
                delete_awardlink_awardee_titles=before_awardlinks_awardee_titles.difference(
                    after_awardlinks_awardee_titles
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_rcontexts = set(before_conceptunit.reasonunits.keys())
            after_reasonunit_rcontexts = set(after_conceptunit.reasonunits.keys())
            self.add_planatom_concept_reasonunit_inserts(
                after_conceptunit=after_conceptunit,
                insert_reasonunit_rcontexts=after_reasonunit_rcontexts.difference(
                    before_reasonunit_rcontexts
                ),
            )
            self.add_planatom_concept_reasonunit_updates(
                before_conceptunit=before_conceptunit,
                after_conceptunit=after_conceptunit,
                update_reasonunit_rcontexts=before_reasonunit_rcontexts.intersection(
                    after_reasonunit_rcontexts
                ),
            )
            self.add_planatom_concept_reasonunit_deletes(
                before_conceptunit=before_conceptunit,
                delete_reasonunit_rcontexts=before_reasonunit_rcontexts.difference(
                    after_reasonunit_rcontexts
                ),
            )
            # insert / update / delete reasonunits_permises
            # update reasonunits_permises insert_premise
            # update reasonunits_permises update_premise
            # update reasonunits_permises delete_premise

            # insert / update / delete laborlinks
            before_laborlinks_labor_titles = set(
                before_conceptunit.laborunit._laborlinks
            )
            after_laborlinks_labor_titles = set(after_conceptunit.laborunit._laborlinks)
            self.add_planatom_concept_laborlink_insert(
                concept_way=concept_way,
                insert_laborlink_labor_titles=after_laborlinks_labor_titles.difference(
                    before_laborlinks_labor_titles
                ),
            )
            self.add_planatom_concept_laborlink_deletes(
                concept_way=concept_way,
                delete_laborlink_labor_titles=before_laborlinks_labor_titles.difference(
                    after_laborlinks_labor_titles
                ),
            )

            # insert / update / delete healerlinks
            before_healerlinks_healer_names = set(
                before_conceptunit.healerlink._healer_names
            )
            after_healerlinks_healer_names = set(
                after_conceptunit.healerlink._healer_names
            )
            self.add_planatom_concept_healerlink_insert(
                concept_way=concept_way,
                insert_healerlink_healer_names=after_healerlinks_healer_names.difference(
                    before_healerlinks_healer_names
                ),
            )
            self.add_planatom_concept_healerlink_deletes(
                concept_way=concept_way,
                delete_healerlink_healer_names=before_healerlinks_healer_names.difference(
                    after_healerlinks_healer_names
                ),
            )

    def add_planatom_concept_deletes(
        self, before_plan: PlanUnit, delete_concept_ways: set
    ):
        for delete_concept_way in delete_concept_ways:
            x_planatom = planatom_shop("plan_conceptunit", "DELETE")
            x_planatom.set_jkey("concept_way", delete_concept_way)
            self.set_planatom(x_planatom)

            delete_conceptunit = before_plan.get_concept_obj(delete_concept_way)
            self.add_planatom_concept_factunit_deletes(
                concept_way=delete_concept_way,
                delete_factunit_rcontexts=set(delete_conceptunit.factunits.keys()),
            )

            self.add_planatom_concept_awardlink_deletes(
                concept_way=delete_concept_way,
                delete_awardlink_awardee_titles=set(
                    delete_conceptunit.awardlinks.keys()
                ),
            )
            self.add_planatom_concept_reasonunit_deletes(
                before_conceptunit=delete_conceptunit,
                delete_reasonunit_rcontexts=set(delete_conceptunit.reasonunits.keys()),
            )
            self.add_planatom_concept_laborlink_deletes(
                concept_way=delete_concept_way,
                delete_laborlink_labor_titles=delete_conceptunit.laborunit._laborlinks,
            )
            self.add_planatom_concept_healerlink_deletes(
                concept_way=delete_concept_way,
                delete_healerlink_healer_names=delete_conceptunit.healerlink._healer_names,
            )

    def add_planatom_concept_reasonunit_inserts(
        self, after_conceptunit: ConceptUnit, insert_reasonunit_rcontexts: set
    ):
        for insert_reasonunit_rcontext in insert_reasonunit_rcontexts:
            after_reasonunit = after_conceptunit.get_reasonunit(
                insert_reasonunit_rcontext
            )
            x_planatom = planatom_shop("plan_concept_reasonunit", "INSERT")
            x_planatom.set_jkey("concept_way", after_conceptunit.get_concept_way())
            x_planatom.set_jkey("rcontext", after_reasonunit.rcontext)
            if after_reasonunit.rconcept_active_requisite is not None:
                x_planatom.set_jvalue(
                    "rconcept_active_requisite",
                    after_reasonunit.rconcept_active_requisite,
                )
            self.set_planatom(x_planatom)

            self.add_planatom_concept_reason_premiseunit_inserts(
                concept_way=after_conceptunit.get_concept_way(),
                after_reasonunit=after_reasonunit,
                insert_premise_pstates=set(after_reasonunit.premises.keys()),
            )

    def add_planatom_concept_reasonunit_updates(
        self,
        before_conceptunit: ConceptUnit,
        after_conceptunit: ConceptUnit,
        update_reasonunit_rcontexts: set,
    ):
        for update_reasonunit_rcontext in update_reasonunit_rcontexts:
            before_reasonunit = before_conceptunit.get_reasonunit(
                update_reasonunit_rcontext
            )
            after_reasonunit = after_conceptunit.get_reasonunit(
                update_reasonunit_rcontext
            )
            if jvalues_different(
                "plan_concept_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_planatom = planatom_shop("plan_concept_reasonunit", "UPDATE")
                x_planatom.set_jkey("concept_way", before_conceptunit.get_concept_way())
                x_planatom.set_jkey("rcontext", after_reasonunit.rcontext)
                if (
                    before_reasonunit.rconcept_active_requisite
                    != after_reasonunit.rconcept_active_requisite
                ):
                    x_planatom.set_jvalue(
                        "rconcept_active_requisite",
                        after_reasonunit.rconcept_active_requisite,
                    )
                self.set_planatom(x_planatom)

            before_premise_pstates = set(before_reasonunit.premises.keys())
            after_premise_pstates = set(after_reasonunit.premises.keys())
            self.add_planatom_concept_reason_premiseunit_inserts(
                concept_way=before_conceptunit.get_concept_way(),
                after_reasonunit=after_reasonunit,
                insert_premise_pstates=after_premise_pstates.difference(
                    before_premise_pstates
                ),
            )
            self.add_planatom_concept_reason_premiseunit_updates(
                concept_way=before_conceptunit.get_concept_way(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_pstates=after_premise_pstates.intersection(
                    before_premise_pstates
                ),
            )
            self.add_planatom_concept_reason_premiseunit_deletes(
                concept_way=before_conceptunit.get_concept_way(),
                reasonunit_rcontext=update_reasonunit_rcontext,
                delete_premise_pstates=before_premise_pstates.difference(
                    after_premise_pstates
                ),
            )

    def add_planatom_concept_reasonunit_deletes(
        self, before_conceptunit: ConceptUnit, delete_reasonunit_rcontexts: set
    ):
        for delete_reasonunit_rcontext in delete_reasonunit_rcontexts:
            x_planatom = planatom_shop("plan_concept_reasonunit", "DELETE")
            x_planatom.set_jkey("concept_way", before_conceptunit.get_concept_way())
            x_planatom.set_jkey("rcontext", delete_reasonunit_rcontext)
            self.set_planatom(x_planatom)

            before_reasonunit = before_conceptunit.get_reasonunit(
                delete_reasonunit_rcontext
            )
            self.add_planatom_concept_reason_premiseunit_deletes(
                concept_way=before_conceptunit.get_concept_way(),
                reasonunit_rcontext=delete_reasonunit_rcontext,
                delete_premise_pstates=set(before_reasonunit.premises.keys()),
            )

    def add_planatom_concept_reason_premiseunit_inserts(
        self,
        concept_way: WayTerm,
        after_reasonunit: ReasonUnit,
        insert_premise_pstates: set,
    ):
        for insert_premise_pstate in insert_premise_pstates:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_pstate)
            x_planatom = planatom_shop("plan_concept_reason_premiseunit", "INSERT")
            x_planatom.set_jkey("concept_way", concept_way)
            x_planatom.set_jkey("rcontext", after_reasonunit.rcontext)
            x_planatom.set_jkey("pstate", after_premiseunit.pstate)
            if after_premiseunit.popen is not None:
                x_planatom.set_jvalue("popen", after_premiseunit.popen)
            if after_premiseunit.pnigh is not None:
                x_planatom.set_jvalue("pnigh", after_premiseunit.pnigh)
            if after_premiseunit.pdivisor is not None:
                x_planatom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
            self.set_planatom(x_planatom)

    def add_planatom_concept_reason_premiseunit_updates(
        self,
        concept_way: WayTerm,
        before_reasonunit: ReasonUnit,
        after_reasonunit: ReasonUnit,
        update_premise_pstates: set,
    ):
        for update_premise_pstate in update_premise_pstates:
            before_premiseunit = before_reasonunit.get_premise(update_premise_pstate)
            after_premiseunit = after_reasonunit.get_premise(update_premise_pstate)
            if jvalues_different(
                "plan_concept_reason_premiseunit",
                before_premiseunit,
                after_premiseunit,
            ):
                x_planatom = planatom_shop("plan_concept_reason_premiseunit", "UPDATE")
                x_planatom.set_jkey("concept_way", concept_way)
                x_planatom.set_jkey("rcontext", before_reasonunit.rcontext)
                x_planatom.set_jkey("pstate", after_premiseunit.pstate)
                if after_premiseunit.popen != before_premiseunit.popen:
                    x_planatom.set_jvalue("popen", after_premiseunit.popen)
                if after_premiseunit.pnigh != before_premiseunit.pnigh:
                    x_planatom.set_jvalue("pnigh", after_premiseunit.pnigh)
                if after_premiseunit.pdivisor != before_premiseunit.pdivisor:
                    x_planatom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
                self.set_planatom(x_planatom)

    def add_planatom_concept_reason_premiseunit_deletes(
        self,
        concept_way: WayTerm,
        reasonunit_rcontext: WayTerm,
        delete_premise_pstates: set,
    ):
        for delete_premise_pstate in delete_premise_pstates:
            x_planatom = planatom_shop("plan_concept_reason_premiseunit", "DELETE")
            x_planatom.set_jkey("concept_way", concept_way)
            x_planatom.set_jkey("rcontext", reasonunit_rcontext)
            x_planatom.set_jkey("pstate", delete_premise_pstate)
            self.set_planatom(x_planatom)

    def add_planatom_concept_laborlink_insert(
        self, concept_way: WayTerm, insert_laborlink_labor_titles: set
    ):
        for insert_laborlink_labor_title in insert_laborlink_labor_titles:
            x_planatom = planatom_shop("plan_concept_laborlink", "INSERT")
            x_planatom.set_jkey("concept_way", concept_way)
            x_planatom.set_jkey("labor_title", insert_laborlink_labor_title)
            self.set_planatom(x_planatom)

    def add_planatom_concept_laborlink_deletes(
        self, concept_way: WayTerm, delete_laborlink_labor_titles: set
    ):
        for delete_laborlink_labor_title in delete_laborlink_labor_titles:
            x_planatom = planatom_shop("plan_concept_laborlink", "DELETE")
            x_planatom.set_jkey("concept_way", concept_way)
            x_planatom.set_jkey("labor_title", delete_laborlink_labor_title)
            self.set_planatom(x_planatom)

    def add_planatom_concept_healerlink_insert(
        self, concept_way: WayTerm, insert_healerlink_healer_names: set
    ):
        for insert_healerlink_healer_name in insert_healerlink_healer_names:
            x_planatom = planatom_shop("plan_concept_healerlink", "INSERT")
            x_planatom.set_jkey("concept_way", concept_way)
            x_planatom.set_jkey("healer_name", insert_healerlink_healer_name)
            self.set_planatom(x_planatom)

    def add_planatom_concept_healerlink_deletes(
        self, concept_way: WayTerm, delete_healerlink_healer_names: set
    ):
        for delete_healerlink_healer_name in delete_healerlink_healer_names:
            x_planatom = planatom_shop("plan_concept_healerlink", "DELETE")
            x_planatom.set_jkey("concept_way", concept_way)
            x_planatom.set_jkey("healer_name", delete_healerlink_healer_name)
            self.set_planatom(x_planatom)

    def add_planatom_concept_awardlink_inserts(
        self, after_conceptunit: ConceptUnit, insert_awardlink_awardee_titles: set
    ):
        for after_awardlink_awardee_title in insert_awardlink_awardee_titles:
            after_awardlink = after_conceptunit.awardlinks.get(
                after_awardlink_awardee_title
            )
            x_planatom = planatom_shop("plan_concept_awardlink", "INSERT")
            x_planatom.set_jkey("concept_way", after_conceptunit.get_concept_way())
            x_planatom.set_jkey("awardee_title", after_awardlink.awardee_title)
            x_planatom.set_jvalue("give_force", after_awardlink.give_force)
            x_planatom.set_jvalue("take_force", after_awardlink.take_force)
            self.set_planatom(x_planatom)

    def add_planatom_concept_awardlink_updates(
        self,
        before_conceptunit: ConceptUnit,
        after_conceptunit: ConceptUnit,
        update_awardlink_awardee_titles: set,
    ):
        for update_awardlink_awardee_title in update_awardlink_awardee_titles:
            before_awardlink = before_conceptunit.awardlinks.get(
                update_awardlink_awardee_title
            )
            after_awardlink = after_conceptunit.awardlinks.get(
                update_awardlink_awardee_title
            )
            if jvalues_different(
                "plan_concept_awardlink", before_awardlink, after_awardlink
            ):
                x_planatom = planatom_shop("plan_concept_awardlink", "UPDATE")
                x_planatom.set_jkey("concept_way", before_conceptunit.get_concept_way())
                x_planatom.set_jkey("awardee_title", after_awardlink.awardee_title)
                if before_awardlink.give_force != after_awardlink.give_force:
                    x_planatom.set_jvalue("give_force", after_awardlink.give_force)
                if before_awardlink.take_force != after_awardlink.take_force:
                    x_planatom.set_jvalue("take_force", after_awardlink.take_force)
                self.set_planatom(x_planatom)

    def add_planatom_concept_awardlink_deletes(
        self, concept_way: WayTerm, delete_awardlink_awardee_titles: set
    ):
        for delete_awardlink_awardee_title in delete_awardlink_awardee_titles:
            x_planatom = planatom_shop("plan_concept_awardlink", "DELETE")
            x_planatom.set_jkey("concept_way", concept_way)
            x_planatom.set_jkey("awardee_title", delete_awardlink_awardee_title)
            self.set_planatom(x_planatom)

    def add_planatom_concept_factunit_inserts(
        self, conceptunit: ConceptUnit, insert_factunit_rcontexts: set
    ):
        for insert_factunit_rcontext in insert_factunit_rcontexts:
            insert_factunit = conceptunit.factunits.get(insert_factunit_rcontext)
            x_planatom = planatom_shop("plan_concept_factunit", "INSERT")
            x_planatom.set_jkey("concept_way", conceptunit.get_concept_way())
            x_planatom.set_jkey("fcontext", insert_factunit.fcontext)
            if insert_factunit.fstate is not None:
                x_planatom.set_jvalue("fstate", insert_factunit.fstate)
            if insert_factunit.fopen is not None:
                x_planatom.set_jvalue("fopen", insert_factunit.fopen)
            if insert_factunit.fnigh is not None:
                x_planatom.set_jvalue("fnigh", insert_factunit.fnigh)
            self.set_planatom(x_planatom)

    def add_planatom_concept_factunit_updates(
        self,
        before_conceptunit: ConceptUnit,
        after_conceptunit: ConceptUnit,
        update_factunit_rcontexts: set,
    ):
        for update_factunit_rcontext in update_factunit_rcontexts:
            before_factunit = before_conceptunit.factunits.get(update_factunit_rcontext)
            after_factunit = after_conceptunit.factunits.get(update_factunit_rcontext)
            if jvalues_different(
                "plan_concept_factunit", before_factunit, after_factunit
            ):
                x_planatom = planatom_shop("plan_concept_factunit", "UPDATE")
                x_planatom.set_jkey("concept_way", before_conceptunit.get_concept_way())
                x_planatom.set_jkey("fcontext", after_factunit.fcontext)
                if before_factunit.fstate != after_factunit.fstate:
                    x_planatom.set_jvalue("fstate", after_factunit.fstate)
                if before_factunit.fopen != after_factunit.fopen:
                    x_planatom.set_jvalue("fopen", after_factunit.fopen)
                if before_factunit.fnigh != after_factunit.fnigh:
                    x_planatom.set_jvalue("fnigh", after_factunit.fnigh)
                self.set_planatom(x_planatom)

    def add_planatom_concept_factunit_deletes(
        self, concept_way: WayTerm, delete_factunit_rcontexts: FactUnit
    ):
        for delete_factunit_rcontext in delete_factunit_rcontexts:
            x_planatom = planatom_shop("plan_concept_factunit", "DELETE")
            x_planatom.set_jkey("concept_way", concept_way)
            x_planatom.set_jkey("fcontext", delete_factunit_rcontext)
            self.set_planatom(x_planatom)

    def is_empty(self) -> bool:
        return self.planatoms == {}

    def get_ordered_planatoms(self, x_count: int = None) -> dict[int, PlanAtom]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_atom in self.get_sorted_planatoms():
            x_dict[x_count] = x_atom
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int, str]:
        atom_tuples = self.get_ordered_planatoms(x_count).items()
        return {atom_num: atom_obj.get_dict() for atom_num, atom_obj in atom_tuples}

    def get_json(self, x_count: int = None) -> str:
        x_dict = self.get_ordered_dict(x_count)
        return get_json_from_dict(x_dict)


def plandelta_shop(planatoms: dict[str, PlanAtom] = None) -> PlanDelta:
    return PlanDelta(
        planatoms=get_empty_dict_if_None(planatoms),
        _plan_build_validated=False,
    )


def plan_built_from_delta_is_valid(x_delta: PlanDelta, x_plan: PlanUnit = None) -> bool:
    x_plan = planunit_shop() if x_plan is None else x_plan
    x_plan = x_delta.get_edited_plan(x_plan)
    try:
        x_plan.settle_plan()
    except Exception:
        return False
    return True


def get_dimens_cruds_plandelta(
    x_plandelta: PlanDelta, dimen_set: set[str], curd_set: set[str]
) -> PlanDelta:
    new_plandelta = plandelta_shop()
    for x_planatom in x_plandelta.get_sorted_planatoms():
        if x_planatom.crud_str in curd_set and x_planatom.dimen in dimen_set:
            new_plandelta.set_planatom(x_planatom)
    return new_plandelta


def get_minimal_plandelta(x_plandelta: PlanDelta, x_plan: PlanUnit) -> PlanDelta:
    """Creates new PlanDelta with only PlanAtoms that would actually change the PlanUnit"""
    new_plandelta = plandelta_shop()
    for x_atom in x_plandelta.get_sorted_planatoms():
        sifted_atom = sift_planatom(x_plan, x_atom)
        if sifted_atom != None:
            new_plandelta.set_planatom(sifted_atom)
    return new_plandelta


def get_plandelta_from_ordered_dict(x_dict: dict) -> PlanDelta:
    x_plandelta = plandelta_shop()
    for x_atom_dict in x_dict.values():
        x_plandelta.set_planatom(get_planatom_from_dict(x_atom_dict))
    return x_plandelta
