from src.a00_data_toolbox.dict_toolbox import (
    get_empty_dict_if_None,
    get_json_from_dict,
    set_in_nested_dict,
    get_from_nested_dict,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from src.a01_term_logic.way import WayTerm, TitleTerm
from src.a03_group_logic.acct import MemberShip, AcctName, AcctUnit
from src.a03_group_logic.group import MemberShip
from src.a04_reason_logic.reason_concept import FactUnit, ReasonUnit
from src.a05_concept_logic.concept import ConceptUnit
from src.a06_bud_logic.bud import BudUnit, budunit_shop
from src.a08_bud_atom_logic.atom_config import CRUD_command
from src.a08_bud_atom_logic.atom import (
    BudAtom,
    budatom_shop,
    modify_bud_with_budatom,
    InvalidBudAtomException,
    jvalues_different,
    sift_budatom,
    get_from_dict as get_budatom_from_dict,
)
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class BudDelta:
    budatoms: dict[CRUD_command : dict[str, BudAtom]] = None
    _bud_build_validated: bool = None

    def _get_crud_budatoms_list(self) -> dict[CRUD_command, list[BudAtom]]:
        return get_all_nondictionary_objs(self.budatoms)

    def get_dimen_sorted_budatoms_list(self) -> list[BudAtom]:
        atoms_list = []
        for crud_list in self._get_crud_budatoms_list().values():
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

    def get_sorted_budatoms(self) -> list[BudAtom]:
        budatoms_list = self.get_dimen_sorted_budatoms_list()
        return sorted(budatoms_list, key=lambda x: x.atom_order)

    def get_edited_bud(self, before_bud: BudUnit) -> BudUnit:
        edited_bud = copy_deepcopy(before_bud)
        for x_budatom in self.get_sorted_budatoms():
            modify_bud_with_budatom(edited_bud, x_budatom)
        return edited_bud

    def set_budatom(self, x_budatom: BudAtom):
        if x_budatom.is_valid() is False:
            raise InvalidBudAtomException(
                f"""'{x_budatom.dimen}' {x_budatom.crud_str} BudAtom is invalid
                {x_budatom.is_jkeys_valid()=}
                {x_budatom.is_jvalues_valid()=}"""
            )

        x_budatom.set_atom_order()
        x_keylist = [
            x_budatom.crud_str,
            x_budatom.dimen,
            *x_budatom.get_nesting_order_args(),
        ]
        set_in_nested_dict(self.budatoms, x_keylist, x_budatom)

    def budatom_exists(self, x_budatom: BudAtom) -> bool:
        if x_budatom.is_valid() is False:
            raise InvalidBudAtomException(
                f"""'{x_budatom.dimen}' {x_budatom.crud_str} BudAtom is invalid
                {x_budatom.is_jkeys_valid()=}
                {x_budatom.is_jvalues_valid()=}"""
            )

        x_budatom.set_atom_order()
        x_keylist = [
            x_budatom.crud_str,
            x_budatom.dimen,
            *list(x_budatom.get_nesting_order_args()),
        ]
        nested_budatom = get_from_nested_dict(self.budatoms, x_keylist, True)
        return nested_budatom == x_budatom

    def add_budatom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        x_budatom = budatom_shop(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=jkeys,
            jvalues=jvalues,
        )
        self.set_budatom(x_budatom)

    def get_budatom(self, crud_str: str, dimen: str, jkeys: list[str]) -> BudAtom:
        x_keylist = [crud_str, dimen, *jkeys]
        return get_from_nested_dict(self.budatoms, x_keylist)

    def add_all_budatoms(self, after_bud: BudUnit):
        before_bud = budunit_shop(after_bud.owner_name, after_bud.fisc_label)
        self.add_all_different_budatoms(before_bud, after_bud)

    def add_all_different_budatoms(self, before_bud: BudUnit, after_bud: BudUnit):
        before_bud.settle_bud()
        after_bud.settle_bud()
        self.add_budatoms_budunit_simple_attrs(before_bud, after_bud)
        self.add_budatoms_accts(before_bud, after_bud)
        self.add_budatoms_concepts(before_bud, after_bud)

    def add_budatoms_budunit_simple_attrs(
        self, before_bud: BudUnit, after_bud: BudUnit
    ):
        if not jvalues_different("budunit", before_bud, after_bud):
            return
        x_budatom = budatom_shop("budunit", "UPDATE")
        if before_bud.max_tree_traverse != after_bud.max_tree_traverse:
            x_budatom.set_jvalue("max_tree_traverse", after_bud.max_tree_traverse)
        if before_bud.credor_respect != after_bud.credor_respect:
            x_budatom.set_jvalue("credor_respect", after_bud.credor_respect)
        if before_bud.debtor_respect != after_bud.debtor_respect:
            x_budatom.set_jvalue("debtor_respect", after_bud.debtor_respect)
        if before_bud.tally != after_bud.tally:
            x_budatom.set_jvalue("tally", after_bud.tally)
        if before_bud.fund_pool != after_bud.fund_pool:
            x_budatom.set_jvalue("fund_pool", after_bud.fund_pool)
        if before_bud.fund_coin != after_bud.fund_coin:
            x_budatom.set_jvalue("fund_coin", after_bud.fund_coin)
        if before_bud.respect_bit != after_bud.respect_bit:
            x_budatom.set_jvalue("respect_bit", after_bud.respect_bit)
        self.set_budatom(x_budatom)

    def add_budatoms_accts(self, before_bud: BudUnit, after_bud: BudUnit):
        before_acct_names = set(before_bud.accts.keys())
        after_acct_names = set(after_bud.accts.keys())

        self.add_budatom_acctunit_inserts(
            after_bud=after_bud,
            insert_acct_names=after_acct_names.difference(before_acct_names),
        )
        self.add_budatom_acctunit_deletes(
            before_bud=before_bud,
            delete_acct_names=before_acct_names.difference(after_acct_names),
        )
        self.add_budatom_acctunit_updates(
            before_bud=before_bud,
            after_bud=after_bud,
            update_acct_names=before_acct_names.intersection(after_acct_names),
        )

    def add_budatom_acctunit_inserts(self, after_bud: BudUnit, insert_acct_names: set):
        for insert_acct_name in insert_acct_names:
            insert_acctunit = after_bud.get_acct(insert_acct_name)
            x_budatom = budatom_shop("bud_acctunit", "INSERT")
            x_budatom.set_jkey("acct_name", insert_acctunit.acct_name)
            if insert_acctunit.credit_belief is not None:
                x_budatom.set_jvalue("credit_belief", insert_acctunit.credit_belief)
            if insert_acctunit.debtit_belief is not None:
                x_budatom.set_jvalue("debtit_belief", insert_acctunit.debtit_belief)
            self.set_budatom(x_budatom)
            all_group_titles = set(insert_acctunit._memberships.keys())
            self.add_budatom_memberships_inserts(
                after_acctunit=insert_acctunit,
                insert_membership_group_titles=all_group_titles,
            )

    def add_budatom_acctunit_updates(
        self, before_bud: BudUnit, after_bud: BudUnit, update_acct_names: set
    ):
        for acct_name in update_acct_names:
            after_acctunit = after_bud.get_acct(acct_name)
            before_acctunit = before_bud.get_acct(acct_name)
            if jvalues_different("bud_acctunit", after_acctunit, before_acctunit):
                x_budatom = budatom_shop("bud_acctunit", "UPDATE")
                x_budatom.set_jkey("acct_name", after_acctunit.acct_name)
                if before_acctunit.credit_belief != after_acctunit.credit_belief:
                    x_budatom.set_jvalue("credit_belief", after_acctunit.credit_belief)
                if before_acctunit.debtit_belief != after_acctunit.debtit_belief:
                    x_budatom.set_jvalue("debtit_belief", after_acctunit.debtit_belief)
                self.set_budatom(x_budatom)
            self.add_budatom_acctunit_update_memberships(
                after_acctunit=after_acctunit, before_acctunit=before_acctunit
            )

    def add_budatom_acctunit_deletes(self, before_bud: BudUnit, delete_acct_names: set):
        for delete_acct_name in delete_acct_names:
            x_budatom = budatom_shop("bud_acctunit", "DELETE")
            x_budatom.set_jkey("acct_name", delete_acct_name)
            self.set_budatom(x_budatom)
            delete_acctunit = before_bud.get_acct(delete_acct_name)
            non_mirror_group_titles = {
                x_group_title
                for x_group_title in delete_acctunit._memberships.keys()
                if x_group_title != delete_acct_name
            }
            self.add_budatom_memberships_delete(
                delete_acct_name, non_mirror_group_titles
            )

    def add_budatom_acctunit_update_memberships(
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

        self.add_budatom_memberships_inserts(
            after_acctunit=after_acctunit,
            insert_membership_group_titles=after_group_titles.difference(
                before_group_titles
            ),
        )

        self.add_budatom_memberships_delete(
            before_acct_name=after_acctunit.acct_name,
            before_group_titles=before_group_titles.difference(after_group_titles),
        )

        update_group_titles = before_group_titles.intersection(after_group_titles)
        for update_acct_name in update_group_titles:
            before_membership = before_acctunit.get_membership(update_acct_name)
            after_membership = after_acctunit.get_membership(update_acct_name)
            if jvalues_different(
                "bud_acct_membership", before_membership, after_membership
            ):
                self.add_budatom_membership_update(
                    acct_name=after_acctunit.acct_name,
                    before_membership=before_membership,
                    after_membership=after_membership,
                )

    def add_budatom_memberships_inserts(
        self,
        after_acctunit: AcctUnit,
        insert_membership_group_titles: list[TitleTerm],
    ):
        after_acct_name = after_acctunit.acct_name
        for insert_group_title in insert_membership_group_titles:
            after_membership = after_acctunit.get_membership(insert_group_title)
            x_budatom = budatom_shop("bud_acct_membership", "INSERT")
            x_budatom.set_jkey("acct_name", after_acct_name)
            x_budatom.set_jkey("group_title", after_membership.group_title)
            if after_membership.credit_vote is not None:
                x_budatom.set_jvalue("credit_vote", after_membership.credit_vote)
            if after_membership.debtit_vote is not None:
                x_budatom.set_jvalue("debtit_vote", after_membership.debtit_vote)
            self.set_budatom(x_budatom)

    def add_budatom_membership_update(
        self,
        acct_name: AcctName,
        before_membership: MemberShip,
        after_membership: MemberShip,
    ):
        x_budatom = budatom_shop("bud_acct_membership", "UPDATE")
        x_budatom.set_jkey("acct_name", acct_name)
        x_budatom.set_jkey("group_title", after_membership.group_title)
        if after_membership.credit_vote != before_membership.credit_vote:
            x_budatom.set_jvalue("credit_vote", after_membership.credit_vote)
        if after_membership.debtit_vote != before_membership.debtit_vote:
            x_budatom.set_jvalue("debtit_vote", after_membership.debtit_vote)
        self.set_budatom(x_budatom)

    def add_budatom_memberships_delete(
        self, before_acct_name: AcctName, before_group_titles: TitleTerm
    ):
        for delete_group_title in before_group_titles:
            x_budatom = budatom_shop("bud_acct_membership", "DELETE")
            x_budatom.set_jkey("acct_name", before_acct_name)
            x_budatom.set_jkey("group_title", delete_group_title)
            self.set_budatom(x_budatom)

    def add_budatoms_concepts(self, before_bud: BudUnit, after_bud: BudUnit):
        before_concept_ways = set(before_bud._concept_dict.keys())
        after_concept_ways = set(after_bud._concept_dict.keys())

        self.add_budatom_concept_inserts(
            after_bud=after_bud,
            insert_concept_ways=after_concept_ways.difference(before_concept_ways),
        )
        self.add_budatom_concept_deletes(
            before_bud=before_bud,
            delete_concept_ways=before_concept_ways.difference(after_concept_ways),
        )
        self.add_budatom_concept_updates(
            before_bud=before_bud,
            after_bud=after_bud,
            update_ways=before_concept_ways.intersection(after_concept_ways),
        )

    def add_budatom_concept_inserts(self, after_bud: BudUnit, insert_concept_ways: set):
        for insert_concept_way in insert_concept_ways:
            insert_conceptunit = after_bud.get_concept_obj(insert_concept_way)
            x_budatom = budatom_shop("bud_conceptunit", "INSERT")
            x_budatom.set_jkey("concept_way", insert_conceptunit.get_concept_way())
            x_budatom.set_jvalue("addin", insert_conceptunit.addin)
            x_budatom.set_jvalue("begin", insert_conceptunit.begin)
            x_budatom.set_jvalue("close", insert_conceptunit.close)
            x_budatom.set_jvalue("denom", insert_conceptunit.denom)
            x_budatom.set_jvalue("numor", insert_conceptunit.numor)
            x_budatom.set_jvalue("morph", insert_conceptunit.morph)
            x_budatom.set_jvalue("mass", insert_conceptunit.mass)
            x_budatom.set_jvalue("pledge", insert_conceptunit.pledge)
            self.set_budatom(x_budatom)

            self.add_budatom_concept_factunit_inserts(
                conceptunit=insert_conceptunit,
                insert_factunit_rcontexts=set(insert_conceptunit.factunits.keys()),
            )
            self.add_budatom_concept_awardlink_inserts(
                after_conceptunit=insert_conceptunit,
                insert_awardlink_awardee_titles=set(
                    insert_conceptunit.awardlinks.keys()
                ),
            )
            self.add_budatom_concept_reasonunit_inserts(
                after_conceptunit=insert_conceptunit,
                insert_reasonunit_rcontexts=set(insert_conceptunit.reasonunits.keys()),
            )
            self.add_budatom_concept_laborlink_insert(
                concept_way=insert_concept_way,
                insert_laborlink_labor_titles=insert_conceptunit.laborunit._laborlinks,
            )
            self.add_budatom_concept_healerlink_insert(
                concept_way=insert_concept_way,
                insert_healerlink_healer_names=insert_conceptunit.healerlink._healer_names,
            )

    def add_budatom_concept_updates(
        self, before_bud: BudUnit, after_bud: BudUnit, update_ways: set
    ):
        for concept_way in update_ways:
            after_conceptunit = after_bud.get_concept_obj(concept_way)
            before_conceptunit = before_bud.get_concept_obj(concept_way)
            if jvalues_different(
                "bud_conceptunit", before_conceptunit, after_conceptunit
            ):
                x_budatom = budatom_shop("bud_conceptunit", "UPDATE")
                x_budatom.set_jkey("concept_way", after_conceptunit.get_concept_way())
                if before_conceptunit.addin != after_conceptunit.addin:
                    x_budatom.set_jvalue("addin", after_conceptunit.addin)
                if before_conceptunit.begin != after_conceptunit.begin:
                    x_budatom.set_jvalue("begin", after_conceptunit.begin)
                if before_conceptunit.close != after_conceptunit.close:
                    x_budatom.set_jvalue("close", after_conceptunit.close)
                if before_conceptunit.denom != after_conceptunit.denom:
                    x_budatom.set_jvalue("denom", after_conceptunit.denom)
                if before_conceptunit.numor != after_conceptunit.numor:
                    x_budatom.set_jvalue("numor", after_conceptunit.numor)
                if before_conceptunit.morph != after_conceptunit.morph:
                    x_budatom.set_jvalue("morph", after_conceptunit.morph)
                if before_conceptunit.mass != after_conceptunit.mass:
                    x_budatom.set_jvalue("mass", after_conceptunit.mass)
                if before_conceptunit.pledge != after_conceptunit.pledge:
                    x_budatom.set_jvalue("pledge", after_conceptunit.pledge)
                self.set_budatom(x_budatom)

            # insert / update / delete factunits
            before_factunit_rcontexts = set(before_conceptunit.factunits.keys())
            after_factunit_rcontexts = set(after_conceptunit.factunits.keys())
            self.add_budatom_concept_factunit_inserts(
                conceptunit=after_conceptunit,
                insert_factunit_rcontexts=after_factunit_rcontexts.difference(
                    before_factunit_rcontexts
                ),
            )
            self.add_budatom_concept_factunit_updates(
                before_conceptunit=before_conceptunit,
                after_conceptunit=after_conceptunit,
                update_factunit_rcontexts=before_factunit_rcontexts.intersection(
                    after_factunit_rcontexts
                ),
            )
            self.add_budatom_concept_factunit_deletes(
                concept_way=concept_way,
                delete_factunit_rcontexts=before_factunit_rcontexts.difference(
                    after_factunit_rcontexts
                ),
            )

            # insert / update / delete awardunits
            before_awardlinks_awardee_titles = set(before_conceptunit.awardlinks.keys())
            after_awardlinks_awardee_titles = set(after_conceptunit.awardlinks.keys())
            self.add_budatom_concept_awardlink_inserts(
                after_conceptunit=after_conceptunit,
                insert_awardlink_awardee_titles=after_awardlinks_awardee_titles.difference(
                    before_awardlinks_awardee_titles
                ),
            )
            self.add_budatom_concept_awardlink_updates(
                before_conceptunit=before_conceptunit,
                after_conceptunit=after_conceptunit,
                update_awardlink_awardee_titles=before_awardlinks_awardee_titles.intersection(
                    after_awardlinks_awardee_titles
                ),
            )
            self.add_budatom_concept_awardlink_deletes(
                concept_way=concept_way,
                delete_awardlink_awardee_titles=before_awardlinks_awardee_titles.difference(
                    after_awardlinks_awardee_titles
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_rcontexts = set(before_conceptunit.reasonunits.keys())
            after_reasonunit_rcontexts = set(after_conceptunit.reasonunits.keys())
            self.add_budatom_concept_reasonunit_inserts(
                after_conceptunit=after_conceptunit,
                insert_reasonunit_rcontexts=after_reasonunit_rcontexts.difference(
                    before_reasonunit_rcontexts
                ),
            )
            self.add_budatom_concept_reasonunit_updates(
                before_conceptunit=before_conceptunit,
                after_conceptunit=after_conceptunit,
                update_reasonunit_rcontexts=before_reasonunit_rcontexts.intersection(
                    after_reasonunit_rcontexts
                ),
            )
            self.add_budatom_concept_reasonunit_deletes(
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
            self.add_budatom_concept_laborlink_insert(
                concept_way=concept_way,
                insert_laborlink_labor_titles=after_laborlinks_labor_titles.difference(
                    before_laborlinks_labor_titles
                ),
            )
            self.add_budatom_concept_laborlink_deletes(
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
            self.add_budatom_concept_healerlink_insert(
                concept_way=concept_way,
                insert_healerlink_healer_names=after_healerlinks_healer_names.difference(
                    before_healerlinks_healer_names
                ),
            )
            self.add_budatom_concept_healerlink_deletes(
                concept_way=concept_way,
                delete_healerlink_healer_names=before_healerlinks_healer_names.difference(
                    after_healerlinks_healer_names
                ),
            )

    def add_budatom_concept_deletes(
        self, before_bud: BudUnit, delete_concept_ways: set
    ):
        for delete_concept_way in delete_concept_ways:
            x_budatom = budatom_shop("bud_conceptunit", "DELETE")
            x_budatom.set_jkey("concept_way", delete_concept_way)
            self.set_budatom(x_budatom)

            delete_conceptunit = before_bud.get_concept_obj(delete_concept_way)
            self.add_budatom_concept_factunit_deletes(
                concept_way=delete_concept_way,
                delete_factunit_rcontexts=set(delete_conceptunit.factunits.keys()),
            )

            self.add_budatom_concept_awardlink_deletes(
                concept_way=delete_concept_way,
                delete_awardlink_awardee_titles=set(
                    delete_conceptunit.awardlinks.keys()
                ),
            )
            self.add_budatom_concept_reasonunit_deletes(
                before_conceptunit=delete_conceptunit,
                delete_reasonunit_rcontexts=set(delete_conceptunit.reasonunits.keys()),
            )
            self.add_budatom_concept_laborlink_deletes(
                concept_way=delete_concept_way,
                delete_laborlink_labor_titles=delete_conceptunit.laborunit._laborlinks,
            )
            self.add_budatom_concept_healerlink_deletes(
                concept_way=delete_concept_way,
                delete_healerlink_healer_names=delete_conceptunit.healerlink._healer_names,
            )

    def add_budatom_concept_reasonunit_inserts(
        self, after_conceptunit: ConceptUnit, insert_reasonunit_rcontexts: set
    ):
        for insert_reasonunit_rcontext in insert_reasonunit_rcontexts:
            after_reasonunit = after_conceptunit.get_reasonunit(
                insert_reasonunit_rcontext
            )
            x_budatom = budatom_shop("bud_concept_reasonunit", "INSERT")
            x_budatom.set_jkey("concept_way", after_conceptunit.get_concept_way())
            x_budatom.set_jkey("rcontext", after_reasonunit.rcontext)
            if after_reasonunit.rconcept_active_requisite is not None:
                x_budatom.set_jvalue(
                    "rconcept_active_requisite",
                    after_reasonunit.rconcept_active_requisite,
                )
            self.set_budatom(x_budatom)

            self.add_budatom_concept_reason_premiseunit_inserts(
                concept_way=after_conceptunit.get_concept_way(),
                after_reasonunit=after_reasonunit,
                insert_premise_pstates=set(after_reasonunit.premises.keys()),
            )

    def add_budatom_concept_reasonunit_updates(
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
                "bud_concept_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_budatom = budatom_shop("bud_concept_reasonunit", "UPDATE")
                x_budatom.set_jkey("concept_way", before_conceptunit.get_concept_way())
                x_budatom.set_jkey("rcontext", after_reasonunit.rcontext)
                if (
                    before_reasonunit.rconcept_active_requisite
                    != after_reasonunit.rconcept_active_requisite
                ):
                    x_budatom.set_jvalue(
                        "rconcept_active_requisite",
                        after_reasonunit.rconcept_active_requisite,
                    )
                self.set_budatom(x_budatom)

            before_premise_pstates = set(before_reasonunit.premises.keys())
            after_premise_pstates = set(after_reasonunit.premises.keys())
            self.add_budatom_concept_reason_premiseunit_inserts(
                concept_way=before_conceptunit.get_concept_way(),
                after_reasonunit=after_reasonunit,
                insert_premise_pstates=after_premise_pstates.difference(
                    before_premise_pstates
                ),
            )
            self.add_budatom_concept_reason_premiseunit_updates(
                concept_way=before_conceptunit.get_concept_way(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_pstates=after_premise_pstates.intersection(
                    before_premise_pstates
                ),
            )
            self.add_budatom_concept_reason_premiseunit_deletes(
                concept_way=before_conceptunit.get_concept_way(),
                reasonunit_rcontext=update_reasonunit_rcontext,
                delete_premise_pstates=before_premise_pstates.difference(
                    after_premise_pstates
                ),
            )

    def add_budatom_concept_reasonunit_deletes(
        self, before_conceptunit: ConceptUnit, delete_reasonunit_rcontexts: set
    ):
        for delete_reasonunit_rcontext in delete_reasonunit_rcontexts:
            x_budatom = budatom_shop("bud_concept_reasonunit", "DELETE")
            x_budatom.set_jkey("concept_way", before_conceptunit.get_concept_way())
            x_budatom.set_jkey("rcontext", delete_reasonunit_rcontext)
            self.set_budatom(x_budatom)

            before_reasonunit = before_conceptunit.get_reasonunit(
                delete_reasonunit_rcontext
            )
            self.add_budatom_concept_reason_premiseunit_deletes(
                concept_way=before_conceptunit.get_concept_way(),
                reasonunit_rcontext=delete_reasonunit_rcontext,
                delete_premise_pstates=set(before_reasonunit.premises.keys()),
            )

    def add_budatom_concept_reason_premiseunit_inserts(
        self,
        concept_way: WayTerm,
        after_reasonunit: ReasonUnit,
        insert_premise_pstates: set,
    ):
        for insert_premise_pstate in insert_premise_pstates:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_pstate)
            x_budatom = budatom_shop("bud_concept_reason_premiseunit", "INSERT")
            x_budatom.set_jkey("concept_way", concept_way)
            x_budatom.set_jkey("rcontext", after_reasonunit.rcontext)
            x_budatom.set_jkey("pstate", after_premiseunit.pstate)
            if after_premiseunit.popen is not None:
                x_budatom.set_jvalue("popen", after_premiseunit.popen)
            if after_premiseunit.pnigh is not None:
                x_budatom.set_jvalue("pnigh", after_premiseunit.pnigh)
            if after_premiseunit.pdivisor is not None:
                x_budatom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
            self.set_budatom(x_budatom)

    def add_budatom_concept_reason_premiseunit_updates(
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
                "bud_concept_reason_premiseunit",
                before_premiseunit,
                after_premiseunit,
            ):
                x_budatom = budatom_shop("bud_concept_reason_premiseunit", "UPDATE")
                x_budatom.set_jkey("concept_way", concept_way)
                x_budatom.set_jkey("rcontext", before_reasonunit.rcontext)
                x_budatom.set_jkey("pstate", after_premiseunit.pstate)
                if after_premiseunit.popen != before_premiseunit.popen:
                    x_budatom.set_jvalue("popen", after_premiseunit.popen)
                if after_premiseunit.pnigh != before_premiseunit.pnigh:
                    x_budatom.set_jvalue("pnigh", after_premiseunit.pnigh)
                if after_premiseunit.pdivisor != before_premiseunit.pdivisor:
                    x_budatom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
                self.set_budatom(x_budatom)

    def add_budatom_concept_reason_premiseunit_deletes(
        self,
        concept_way: WayTerm,
        reasonunit_rcontext: WayTerm,
        delete_premise_pstates: set,
    ):
        for delete_premise_pstate in delete_premise_pstates:
            x_budatom = budatom_shop("bud_concept_reason_premiseunit", "DELETE")
            x_budatom.set_jkey("concept_way", concept_way)
            x_budatom.set_jkey("rcontext", reasonunit_rcontext)
            x_budatom.set_jkey("pstate", delete_premise_pstate)
            self.set_budatom(x_budatom)

    def add_budatom_concept_laborlink_insert(
        self, concept_way: WayTerm, insert_laborlink_labor_titles: set
    ):
        for insert_laborlink_labor_title in insert_laborlink_labor_titles:
            x_budatom = budatom_shop("bud_concept_laborlink", "INSERT")
            x_budatom.set_jkey("concept_way", concept_way)
            x_budatom.set_jkey("labor_title", insert_laborlink_labor_title)
            self.set_budatom(x_budatom)

    def add_budatom_concept_laborlink_deletes(
        self, concept_way: WayTerm, delete_laborlink_labor_titles: set
    ):
        for delete_laborlink_labor_title in delete_laborlink_labor_titles:
            x_budatom = budatom_shop("bud_concept_laborlink", "DELETE")
            x_budatom.set_jkey("concept_way", concept_way)
            x_budatom.set_jkey("labor_title", delete_laborlink_labor_title)
            self.set_budatom(x_budatom)

    def add_budatom_concept_healerlink_insert(
        self, concept_way: WayTerm, insert_healerlink_healer_names: set
    ):
        for insert_healerlink_healer_name in insert_healerlink_healer_names:
            x_budatom = budatom_shop("bud_concept_healerlink", "INSERT")
            x_budatom.set_jkey("concept_way", concept_way)
            x_budatom.set_jkey("healer_name", insert_healerlink_healer_name)
            self.set_budatom(x_budatom)

    def add_budatom_concept_healerlink_deletes(
        self, concept_way: WayTerm, delete_healerlink_healer_names: set
    ):
        for delete_healerlink_healer_name in delete_healerlink_healer_names:
            x_budatom = budatom_shop("bud_concept_healerlink", "DELETE")
            x_budatom.set_jkey("concept_way", concept_way)
            x_budatom.set_jkey("healer_name", delete_healerlink_healer_name)
            self.set_budatom(x_budatom)

    def add_budatom_concept_awardlink_inserts(
        self, after_conceptunit: ConceptUnit, insert_awardlink_awardee_titles: set
    ):
        for after_awardlink_awardee_title in insert_awardlink_awardee_titles:
            after_awardlink = after_conceptunit.awardlinks.get(
                after_awardlink_awardee_title
            )
            x_budatom = budatom_shop("bud_concept_awardlink", "INSERT")
            x_budatom.set_jkey("concept_way", after_conceptunit.get_concept_way())
            x_budatom.set_jkey("awardee_title", after_awardlink.awardee_title)
            x_budatom.set_jvalue("give_force", after_awardlink.give_force)
            x_budatom.set_jvalue("take_force", after_awardlink.take_force)
            self.set_budatom(x_budatom)

    def add_budatom_concept_awardlink_updates(
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
                "bud_concept_awardlink", before_awardlink, after_awardlink
            ):
                x_budatom = budatom_shop("bud_concept_awardlink", "UPDATE")
                x_budatom.set_jkey("concept_way", before_conceptunit.get_concept_way())
                x_budatom.set_jkey("awardee_title", after_awardlink.awardee_title)
                if before_awardlink.give_force != after_awardlink.give_force:
                    x_budatom.set_jvalue("give_force", after_awardlink.give_force)
                if before_awardlink.take_force != after_awardlink.take_force:
                    x_budatom.set_jvalue("take_force", after_awardlink.take_force)
                self.set_budatom(x_budatom)

    def add_budatom_concept_awardlink_deletes(
        self, concept_way: WayTerm, delete_awardlink_awardee_titles: set
    ):
        for delete_awardlink_awardee_title in delete_awardlink_awardee_titles:
            x_budatom = budatom_shop("bud_concept_awardlink", "DELETE")
            x_budatom.set_jkey("concept_way", concept_way)
            x_budatom.set_jkey("awardee_title", delete_awardlink_awardee_title)
            self.set_budatom(x_budatom)

    def add_budatom_concept_factunit_inserts(
        self, conceptunit: ConceptUnit, insert_factunit_rcontexts: set
    ):
        for insert_factunit_rcontext in insert_factunit_rcontexts:
            insert_factunit = conceptunit.factunits.get(insert_factunit_rcontext)
            x_budatom = budatom_shop("bud_concept_factunit", "INSERT")
            x_budatom.set_jkey("concept_way", conceptunit.get_concept_way())
            x_budatom.set_jkey("fcontext", insert_factunit.fcontext)
            if insert_factunit.fstate is not None:
                x_budatom.set_jvalue("fstate", insert_factunit.fstate)
            if insert_factunit.fopen is not None:
                x_budatom.set_jvalue("fopen", insert_factunit.fopen)
            if insert_factunit.fnigh is not None:
                x_budatom.set_jvalue("fnigh", insert_factunit.fnigh)
            self.set_budatom(x_budatom)

    def add_budatom_concept_factunit_updates(
        self,
        before_conceptunit: ConceptUnit,
        after_conceptunit: ConceptUnit,
        update_factunit_rcontexts: set,
    ):
        for update_factunit_rcontext in update_factunit_rcontexts:
            before_factunit = before_conceptunit.factunits.get(update_factunit_rcontext)
            after_factunit = after_conceptunit.factunits.get(update_factunit_rcontext)
            if jvalues_different(
                "bud_concept_factunit", before_factunit, after_factunit
            ):
                x_budatom = budatom_shop("bud_concept_factunit", "UPDATE")
                x_budatom.set_jkey("concept_way", before_conceptunit.get_concept_way())
                x_budatom.set_jkey("fcontext", after_factunit.fcontext)
                if before_factunit.fstate != after_factunit.fstate:
                    x_budatom.set_jvalue("fstate", after_factunit.fstate)
                if before_factunit.fopen != after_factunit.fopen:
                    x_budatom.set_jvalue("fopen", after_factunit.fopen)
                if before_factunit.fnigh != after_factunit.fnigh:
                    x_budatom.set_jvalue("fnigh", after_factunit.fnigh)
                self.set_budatom(x_budatom)

    def add_budatom_concept_factunit_deletes(
        self, concept_way: WayTerm, delete_factunit_rcontexts: FactUnit
    ):
        for delete_factunit_rcontext in delete_factunit_rcontexts:
            x_budatom = budatom_shop("bud_concept_factunit", "DELETE")
            x_budatom.set_jkey("concept_way", concept_way)
            x_budatom.set_jkey("fcontext", delete_factunit_rcontext)
            self.set_budatom(x_budatom)

    def is_empty(self) -> bool:
        return self.budatoms == {}

    def get_ordered_budatoms(self, x_count: int = None) -> dict[int, BudAtom]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_atom in self.get_sorted_budatoms():
            x_dict[x_count] = x_atom
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int, str]:
        atom_tuples = self.get_ordered_budatoms(x_count).items()
        return {atom_num: atom_obj.get_dict() for atom_num, atom_obj in atom_tuples}

    def get_json(self, x_count: int = None) -> str:
        x_dict = self.get_ordered_dict(x_count)
        return get_json_from_dict(x_dict)


def buddelta_shop(budatoms: dict[str, BudAtom] = None) -> BudDelta:
    return BudDelta(
        budatoms=get_empty_dict_if_None(budatoms),
        _bud_build_validated=False,
    )


def bud_built_from_delta_is_valid(x_delta: BudDelta, x_bud: BudUnit = None) -> bool:
    x_bud = budunit_shop() if x_bud is None else x_bud
    x_bud = x_delta.get_edited_bud(x_bud)
    try:
        x_bud.settle_bud()
    except Exception:
        return False
    return True


def get_dimens_cruds_buddelta(
    x_buddelta: BudDelta, dimen_set: set[str], curd_set: set[str]
) -> BudDelta:
    new_buddelta = buddelta_shop()
    for x_budatom in x_buddelta.get_sorted_budatoms():
        if x_budatom.crud_str in curd_set and x_budatom.dimen in dimen_set:
            new_buddelta.set_budatom(x_budatom)
    return new_buddelta


def get_minimal_buddelta(x_buddelta: BudDelta, x_bud: BudUnit) -> BudDelta:
    """Creates new BudDelta with only BudAtoms that would actually change the BudUnit"""
    new_buddelta = buddelta_shop()
    for x_atom in x_buddelta.get_sorted_budatoms():
        sifted_atom = sift_budatom(x_bud, x_atom)
        if sifted_atom != None:
            new_buddelta.set_budatom(sifted_atom)
    return new_buddelta


def get_buddelta_from_ordered_dict(x_dict: dict) -> BudDelta:
    x_buddelta = buddelta_shop()
    for x_atom_dict in x_dict.values():
        x_buddelta.set_budatom(get_budatom_from_dict(x_atom_dict))
    return x_buddelta
