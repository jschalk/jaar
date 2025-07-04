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
from src.a01_term_logic.term import RopeTerm, TitleTerm
from src.a03_group_logic.group import MemberShip
from src.a03_group_logic.person import MemberShip, PersonName, PersonUnit
from src.a04_reason_logic.reason_plan import FactUnit, ReasonUnit
from src.a05_plan_logic.plan import PlanUnit
from src.a06_believer_logic.believer import BelieverUnit, believerunit_shop
from src.a08_believer_atom_logic.atom import (
    BelieverAtom,
    InvalidBelieverAtomException,
    believeratom_shop,
    get_from_dict as get_believeratom_from_dict,
    jvalues_different,
    modify_believer_with_believeratom,
    sift_believeratom,
)
from src.a08_believer_atom_logic.atom_config import CRUD_command


@dataclass
class BelieverDelta:
    believeratoms: dict[CRUD_command : dict[str, BelieverAtom]] = None
    _believer_build_validated: bool = None

    def _get_crud_believeratoms_list(self) -> dict[CRUD_command, list[BelieverAtom]]:
        return get_all_nondictionary_objs(self.believeratoms)

    def get_dimen_sorted_believeratoms_list(self) -> list[BelieverAtom]:
        atoms_list = []
        for crud_list in self._get_crud_believeratoms_list().values():
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
            if x_list[0].jkeys.get("plan_rope") is not None:
                x_list = sorted(x_list, key=lambda x: x.jkeys.get("plan_rope"))
            ordered_list.extend(x_list)
        return ordered_list

    def get_sorted_believeratoms(self) -> list[BelieverAtom]:
        believeratoms_list = self.get_dimen_sorted_believeratoms_list()
        return sorted(believeratoms_list, key=lambda x: x.atom_order)

    def get_edited_believer(self, before_believer: BelieverUnit) -> BelieverUnit:
        edited_believer = copy_deepcopy(before_believer)
        for x_believeratom in self.get_sorted_believeratoms():
            modify_believer_with_believeratom(edited_believer, x_believeratom)
        return edited_believer

    def set_believeratom(self, x_believeratom: BelieverAtom):
        if x_believeratom.is_valid() is False:
            raise InvalidBelieverAtomException(
                f"""'{x_believeratom.dimen}' {x_believeratom.crud_str} BelieverAtom is invalid
                {x_believeratom.is_jkeys_valid()=}
                {x_believeratom.is_jvalues_valid()=}"""
            )

        x_believeratom.set_atom_order()
        x_keylist = [
            x_believeratom.crud_str,
            x_believeratom.dimen,
            *x_believeratom.get_nesting_order_args(),
        ]
        set_in_nested_dict(self.believeratoms, x_keylist, x_believeratom)

    def believeratom_exists(self, x_believeratom: BelieverAtom) -> bool:
        if x_believeratom.is_valid() is False:
            raise InvalidBelieverAtomException(
                f"""'{x_believeratom.dimen}' {x_believeratom.crud_str} BelieverAtom is invalid
                {x_believeratom.is_jkeys_valid()=}
                {x_believeratom.is_jvalues_valid()=}"""
            )

        x_believeratom.set_atom_order()
        x_keylist = [
            x_believeratom.crud_str,
            x_believeratom.dimen,
            *list(x_believeratom.get_nesting_order_args()),
        ]
        nested_believeratom = get_from_nested_dict(self.believeratoms, x_keylist, True)
        return nested_believeratom == x_believeratom

    def add_believeratom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        x_believeratom = believeratom_shop(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=jkeys,
            jvalues=jvalues,
        )
        self.set_believeratom(x_believeratom)

    def get_believeratom(
        self, crud_str: str, dimen: str, jkeys: list[str]
    ) -> BelieverAtom:
        x_keylist = [crud_str, dimen, *jkeys]
        return get_from_nested_dict(self.believeratoms, x_keylist)

    def add_all_believeratoms(self, after_believer: BelieverUnit):
        before_believer = believerunit_shop(
            after_believer.believer_name, after_believer.belief_label
        )
        self.add_all_different_believeratoms(before_believer, after_believer)

    def add_all_different_believeratoms(
        self, before_believer: BelieverUnit, after_believer: BelieverUnit
    ):
        before_believer.settle_believer()
        after_believer.settle_believer()
        self.add_believeratoms_believerunit_simple_attrs(
            before_believer, after_believer
        )
        self.add_believeratoms_persons(before_believer, after_believer)
        self.add_believeratoms_plans(before_believer, after_believer)

    def add_believeratoms_believerunit_simple_attrs(
        self, before_believer: BelieverUnit, after_believer: BelieverUnit
    ):
        if not jvalues_different("believerunit", before_believer, after_believer):
            return
        x_believeratom = believeratom_shop("believerunit", "UPDATE")
        if before_believer.max_tree_traverse != after_believer.max_tree_traverse:
            x_believeratom.set_jvalue(
                "max_tree_traverse", after_believer.max_tree_traverse
            )
        if before_believer.credor_respect != after_believer.credor_respect:
            x_believeratom.set_jvalue("credor_respect", after_believer.credor_respect)
        if before_believer.debtor_respect != after_believer.debtor_respect:
            x_believeratom.set_jvalue("debtor_respect", after_believer.debtor_respect)
        if before_believer.tally != after_believer.tally:
            x_believeratom.set_jvalue("tally", after_believer.tally)
        if before_believer.fund_pool != after_believer.fund_pool:
            x_believeratom.set_jvalue("fund_pool", after_believer.fund_pool)
        if before_believer.fund_iota != after_believer.fund_iota:
            x_believeratom.set_jvalue("fund_iota", after_believer.fund_iota)
        if before_believer.respect_bit != after_believer.respect_bit:
            x_believeratom.set_jvalue("respect_bit", after_believer.respect_bit)
        self.set_believeratom(x_believeratom)

    def add_believeratoms_persons(
        self, before_believer: BelieverUnit, after_believer: BelieverUnit
    ):
        before_person_names = set(before_believer.persons.keys())
        after_person_names = set(after_believer.persons.keys())

        self.add_believeratom_personunit_inserts(
            after_believer=after_believer,
            insert_person_names=after_person_names.difference(before_person_names),
        )
        self.add_believeratom_personunit_deletes(
            before_believer=before_believer,
            delete_person_names=before_person_names.difference(after_person_names),
        )
        self.add_believeratom_personunit_updates(
            before_believer=before_believer,
            after_believer=after_believer,
            update_person_names=before_person_names.intersection(after_person_names),
        )

    def add_believeratom_personunit_inserts(
        self, after_believer: BelieverUnit, insert_person_names: set
    ):
        for insert_person_name in insert_person_names:
            insert_personunit = after_believer.get_person(insert_person_name)
            x_believeratom = believeratom_shop("believer_personunit", "INSERT")
            x_believeratom.set_jkey("person_name", insert_personunit.person_name)
            if insert_personunit.person_cred_points is not None:
                x_believeratom.set_jvalue(
                    "person_cred_points", insert_personunit.person_cred_points
                )
            if insert_personunit.person_debt_points is not None:
                x_believeratom.set_jvalue(
                    "person_debt_points", insert_personunit.person_debt_points
                )
            self.set_believeratom(x_believeratom)
            all_group_titles = set(insert_personunit._memberships.keys())
            self.add_believeratom_memberships_inserts(
                after_personunit=insert_personunit,
                insert_membership_group_titles=all_group_titles,
            )

    def add_believeratom_personunit_updates(
        self,
        before_believer: BelieverUnit,
        after_believer: BelieverUnit,
        update_person_names: set,
    ):
        for person_name in update_person_names:
            after_personunit = after_believer.get_person(person_name)
            before_personunit = before_believer.get_person(person_name)
            if jvalues_different(
                "believer_personunit", after_personunit, before_personunit
            ):
                x_believeratom = believeratom_shop("believer_personunit", "UPDATE")
                x_believeratom.set_jkey("person_name", after_personunit.person_name)
                if (
                    before_personunit.person_cred_points
                    != after_personunit.person_cred_points
                ):
                    x_believeratom.set_jvalue(
                        "person_cred_points", after_personunit.person_cred_points
                    )
                if (
                    before_personunit.person_debt_points
                    != after_personunit.person_debt_points
                ):
                    x_believeratom.set_jvalue(
                        "person_debt_points", after_personunit.person_debt_points
                    )
                self.set_believeratom(x_believeratom)
            self.add_believeratom_personunit_update_memberships(
                after_personunit=after_personunit, before_personunit=before_personunit
            )

    def add_believeratom_personunit_deletes(
        self, before_believer: BelieverUnit, delete_person_names: set
    ):
        for delete_person_name in delete_person_names:
            x_believeratom = believeratom_shop("believer_personunit", "DELETE")
            x_believeratom.set_jkey("person_name", delete_person_name)
            self.set_believeratom(x_believeratom)
            delete_personunit = before_believer.get_person(delete_person_name)
            non_mirror_group_titles = {
                x_group_title
                for x_group_title in delete_personunit._memberships.keys()
                if x_group_title != delete_person_name
            }
            self.add_believeratom_memberships_delete(
                delete_person_name, non_mirror_group_titles
            )

    def add_believeratom_personunit_update_memberships(
        self, after_personunit: PersonUnit, before_personunit: PersonUnit
    ):
        # before_non_mirror_group_titles
        before_group_titles = {
            x_group_title
            for x_group_title in before_personunit._memberships.keys()
            if x_group_title != before_personunit.person_name
        }
        # after_non_mirror_group_titles
        after_group_titles = {
            x_group_title
            for x_group_title in after_personunit._memberships.keys()
            if x_group_title != after_personunit.person_name
        }

        self.add_believeratom_memberships_inserts(
            after_personunit=after_personunit,
            insert_membership_group_titles=after_group_titles.difference(
                before_group_titles
            ),
        )

        self.add_believeratom_memberships_delete(
            before_person_name=after_personunit.person_name,
            before_group_titles=before_group_titles.difference(after_group_titles),
        )

        update_group_titles = before_group_titles.intersection(after_group_titles)
        for update_person_name in update_group_titles:
            before_membership = before_personunit.get_membership(update_person_name)
            after_membership = after_personunit.get_membership(update_person_name)
            if jvalues_different(
                "believer_person_membership", before_membership, after_membership
            ):
                self.add_believeratom_membership_update(
                    person_name=after_personunit.person_name,
                    before_membership=before_membership,
                    after_membership=after_membership,
                )

    def add_believeratom_memberships_inserts(
        self,
        after_personunit: PersonUnit,
        insert_membership_group_titles: list[TitleTerm],
    ):
        after_person_name = after_personunit.person_name
        for insert_group_title in insert_membership_group_titles:
            after_membership = after_personunit.get_membership(insert_group_title)
            x_believeratom = believeratom_shop("believer_person_membership", "INSERT")
            x_believeratom.set_jkey("person_name", after_person_name)
            x_believeratom.set_jkey("group_title", after_membership.group_title)
            if after_membership.group_cred_points is not None:
                x_believeratom.set_jvalue(
                    "group_cred_points", after_membership.group_cred_points
                )
            if after_membership.group_debt_points is not None:
                x_believeratom.set_jvalue(
                    "group_debt_points", after_membership.group_debt_points
                )
            self.set_believeratom(x_believeratom)

    def add_believeratom_membership_update(
        self,
        person_name: PersonName,
        before_membership: MemberShip,
        after_membership: MemberShip,
    ):
        x_believeratom = believeratom_shop("believer_person_membership", "UPDATE")
        x_believeratom.set_jkey("person_name", person_name)
        x_believeratom.set_jkey("group_title", after_membership.group_title)
        if after_membership.group_cred_points != before_membership.group_cred_points:
            x_believeratom.set_jvalue(
                "group_cred_points", after_membership.group_cred_points
            )
        if after_membership.group_debt_points != before_membership.group_debt_points:
            x_believeratom.set_jvalue(
                "group_debt_points", after_membership.group_debt_points
            )
        self.set_believeratom(x_believeratom)

    def add_believeratom_memberships_delete(
        self, before_person_name: PersonName, before_group_titles: TitleTerm
    ):
        for delete_group_title in before_group_titles:
            x_believeratom = believeratom_shop("believer_person_membership", "DELETE")
            x_believeratom.set_jkey("person_name", before_person_name)
            x_believeratom.set_jkey("group_title", delete_group_title)
            self.set_believeratom(x_believeratom)

    def add_believeratoms_plans(
        self, before_believer: BelieverUnit, after_believer: BelieverUnit
    ):
        before_plan_ropes = set(before_believer._plan_dict.keys())
        after_plan_ropes = set(after_believer._plan_dict.keys())

        self.add_believeratom_plan_inserts(
            after_believer=after_believer,
            insert_plan_ropes=after_plan_ropes.difference(before_plan_ropes),
        )
        self.add_believeratom_plan_deletes(
            before_believer=before_believer,
            delete_plan_ropes=before_plan_ropes.difference(after_plan_ropes),
        )
        self.add_believeratom_plan_updates(
            before_believer=before_believer,
            after_believer=after_believer,
            update_ropes=before_plan_ropes.intersection(after_plan_ropes),
        )

    def add_believeratom_plan_inserts(
        self, after_believer: BelieverUnit, insert_plan_ropes: set
    ):
        for insert_plan_rope in insert_plan_ropes:
            insert_planunit = after_believer.get_plan_obj(insert_plan_rope)
            x_believeratom = believeratom_shop("believer_planunit", "INSERT")
            x_believeratom.set_jkey("plan_rope", insert_planunit.get_plan_rope())
            x_believeratom.set_jvalue("addin", insert_planunit.addin)
            x_believeratom.set_jvalue("begin", insert_planunit.begin)
            x_believeratom.set_jvalue("close", insert_planunit.close)
            x_believeratom.set_jvalue("denom", insert_planunit.denom)
            x_believeratom.set_jvalue("numor", insert_planunit.numor)
            x_believeratom.set_jvalue("morph", insert_planunit.morph)
            x_believeratom.set_jvalue("mass", insert_planunit.mass)
            x_believeratom.set_jvalue("task", insert_planunit.task)
            self.set_believeratom(x_believeratom)

            self.add_believeratom_plan_factunit_inserts(
                planunit=insert_planunit,
                insert_factunit_rcontexts=set(insert_planunit.factunits.keys()),
            )
            self.add_believeratom_plan_awardlink_inserts(
                after_planunit=insert_planunit,
                insert_awardlink_awardee_titles=set(insert_planunit.awardlinks.keys()),
            )
            self.add_believeratom_plan_reasonunit_inserts(
                after_planunit=insert_planunit,
                insert_reasonunit_rcontexts=set(insert_planunit.reasonunits.keys()),
            )
            self.add_believeratom_plan_laborlink_insert(
                plan_rope=insert_plan_rope,
                insert_laborlink_labor_titles=insert_planunit.laborunit._laborlinks,
            )
            self.add_believeratom_plan_healerlink_insert(
                plan_rope=insert_plan_rope,
                insert_healerlink_healer_names=insert_planunit.healerlink._healer_names,
            )

    def add_believeratom_plan_updates(
        self,
        before_believer: BelieverUnit,
        after_believer: BelieverUnit,
        update_ropes: set,
    ):
        for plan_rope in update_ropes:
            after_planunit = after_believer.get_plan_obj(plan_rope)
            before_planunit = before_believer.get_plan_obj(plan_rope)
            if jvalues_different("believer_planunit", before_planunit, after_planunit):
                x_believeratom = believeratom_shop("believer_planunit", "UPDATE")
                x_believeratom.set_jkey("plan_rope", after_planunit.get_plan_rope())
                if before_planunit.addin != after_planunit.addin:
                    x_believeratom.set_jvalue("addin", after_planunit.addin)
                if before_planunit.begin != after_planunit.begin:
                    x_believeratom.set_jvalue("begin", after_planunit.begin)
                if before_planunit.close != after_planunit.close:
                    x_believeratom.set_jvalue("close", after_planunit.close)
                if before_planunit.denom != after_planunit.denom:
                    x_believeratom.set_jvalue("denom", after_planunit.denom)
                if before_planunit.numor != after_planunit.numor:
                    x_believeratom.set_jvalue("numor", after_planunit.numor)
                if before_planunit.morph != after_planunit.morph:
                    x_believeratom.set_jvalue("morph", after_planunit.morph)
                if before_planunit.mass != after_planunit.mass:
                    x_believeratom.set_jvalue("mass", after_planunit.mass)
                if before_planunit.task != after_planunit.task:
                    x_believeratom.set_jvalue("task", after_planunit.task)
                self.set_believeratom(x_believeratom)

            # insert / update / delete factunits
            before_factunit_rcontexts = set(before_planunit.factunits.keys())
            after_factunit_rcontexts = set(after_planunit.factunits.keys())
            self.add_believeratom_plan_factunit_inserts(
                planunit=after_planunit,
                insert_factunit_rcontexts=after_factunit_rcontexts.difference(
                    before_factunit_rcontexts
                ),
            )
            self.add_believeratom_plan_factunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_factunit_rcontexts=before_factunit_rcontexts.intersection(
                    after_factunit_rcontexts
                ),
            )
            self.add_believeratom_plan_factunit_deletes(
                plan_rope=plan_rope,
                delete_factunit_rcontexts=before_factunit_rcontexts.difference(
                    after_factunit_rcontexts
                ),
            )

            # insert / update / delete awardunits
            before_awardlinks_awardee_titles = set(before_planunit.awardlinks.keys())
            after_awardlinks_awardee_titles = set(after_planunit.awardlinks.keys())
            self.add_believeratom_plan_awardlink_inserts(
                after_planunit=after_planunit,
                insert_awardlink_awardee_titles=after_awardlinks_awardee_titles.difference(
                    before_awardlinks_awardee_titles
                ),
            )
            self.add_believeratom_plan_awardlink_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_awardlink_awardee_titles=before_awardlinks_awardee_titles.intersection(
                    after_awardlinks_awardee_titles
                ),
            )
            self.add_believeratom_plan_awardlink_deletes(
                plan_rope=plan_rope,
                delete_awardlink_awardee_titles=before_awardlinks_awardee_titles.difference(
                    after_awardlinks_awardee_titles
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_rcontexts = set(before_planunit.reasonunits.keys())
            after_reasonunit_rcontexts = set(after_planunit.reasonunits.keys())
            self.add_believeratom_plan_reasonunit_inserts(
                after_planunit=after_planunit,
                insert_reasonunit_rcontexts=after_reasonunit_rcontexts.difference(
                    before_reasonunit_rcontexts
                ),
            )
            self.add_believeratom_plan_reasonunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_reasonunit_rcontexts=before_reasonunit_rcontexts.intersection(
                    after_reasonunit_rcontexts
                ),
            )
            self.add_believeratom_plan_reasonunit_deletes(
                before_planunit=before_planunit,
                delete_reasonunit_rcontexts=before_reasonunit_rcontexts.difference(
                    after_reasonunit_rcontexts
                ),
            )
            # insert / update / delete reasonunits_permises
            # update reasonunits_permises insert_premise
            # update reasonunits_permises update_premise
            # update reasonunits_permises delete_premise

            # insert / update / delete laborlinks
            before_laborlinks_labor_titles = set(before_planunit.laborunit._laborlinks)
            after_laborlinks_labor_titles = set(after_planunit.laborunit._laborlinks)
            self.add_believeratom_plan_laborlink_insert(
                plan_rope=plan_rope,
                insert_laborlink_labor_titles=after_laborlinks_labor_titles.difference(
                    before_laborlinks_labor_titles
                ),
            )
            self.add_believeratom_plan_laborlink_deletes(
                plan_rope=plan_rope,
                delete_laborlink_labor_titles=before_laborlinks_labor_titles.difference(
                    after_laborlinks_labor_titles
                ),
            )

            # insert / update / delete healerlinks
            before_healerlinks_healer_names = set(
                before_planunit.healerlink._healer_names
            )
            after_healerlinks_healer_names = set(
                after_planunit.healerlink._healer_names
            )
            self.add_believeratom_plan_healerlink_insert(
                plan_rope=plan_rope,
                insert_healerlink_healer_names=after_healerlinks_healer_names.difference(
                    before_healerlinks_healer_names
                ),
            )
            self.add_believeratom_plan_healerlink_deletes(
                plan_rope=plan_rope,
                delete_healerlink_healer_names=before_healerlinks_healer_names.difference(
                    after_healerlinks_healer_names
                ),
            )

    def add_believeratom_plan_deletes(
        self, before_believer: BelieverUnit, delete_plan_ropes: set
    ):
        for delete_plan_rope in delete_plan_ropes:
            x_believeratom = believeratom_shop("believer_planunit", "DELETE")
            x_believeratom.set_jkey("plan_rope", delete_plan_rope)
            self.set_believeratom(x_believeratom)

            delete_planunit = before_believer.get_plan_obj(delete_plan_rope)
            self.add_believeratom_plan_factunit_deletes(
                plan_rope=delete_plan_rope,
                delete_factunit_rcontexts=set(delete_planunit.factunits.keys()),
            )

            self.add_believeratom_plan_awardlink_deletes(
                plan_rope=delete_plan_rope,
                delete_awardlink_awardee_titles=set(delete_planunit.awardlinks.keys()),
            )
            self.add_believeratom_plan_reasonunit_deletes(
                before_planunit=delete_planunit,
                delete_reasonunit_rcontexts=set(delete_planunit.reasonunits.keys()),
            )
            self.add_believeratom_plan_laborlink_deletes(
                plan_rope=delete_plan_rope,
                delete_laborlink_labor_titles=delete_planunit.laborunit._laborlinks,
            )
            self.add_believeratom_plan_healerlink_deletes(
                plan_rope=delete_plan_rope,
                delete_healerlink_healer_names=delete_planunit.healerlink._healer_names,
            )

    def add_believeratom_plan_reasonunit_inserts(
        self, after_planunit: PlanUnit, insert_reasonunit_rcontexts: set
    ):
        for insert_reasonunit_rcontext in insert_reasonunit_rcontexts:
            after_reasonunit = after_planunit.get_reasonunit(insert_reasonunit_rcontext)
            x_believeratom = believeratom_shop("believer_plan_reasonunit", "INSERT")
            x_believeratom.set_jkey("plan_rope", after_planunit.get_plan_rope())
            x_believeratom.set_jkey("rcontext", after_reasonunit.rcontext)
            if after_reasonunit.rplan_active_requisite is not None:
                x_believeratom.set_jvalue(
                    "rplan_active_requisite",
                    after_reasonunit.rplan_active_requisite,
                )
            self.set_believeratom(x_believeratom)

            self.add_believeratom_plan_reason_premiseunit_inserts(
                plan_rope=after_planunit.get_plan_rope(),
                after_reasonunit=after_reasonunit,
                insert_premise_pstates=set(after_reasonunit.premises.keys()),
            )

    def add_believeratom_plan_reasonunit_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_reasonunit_rcontexts: set,
    ):
        for update_reasonunit_rcontext in update_reasonunit_rcontexts:
            before_reasonunit = before_planunit.get_reasonunit(
                update_reasonunit_rcontext
            )
            after_reasonunit = after_planunit.get_reasonunit(update_reasonunit_rcontext)
            if jvalues_different(
                "believer_plan_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_believeratom = believeratom_shop("believer_plan_reasonunit", "UPDATE")
                x_believeratom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_believeratom.set_jkey("rcontext", after_reasonunit.rcontext)
                if (
                    before_reasonunit.rplan_active_requisite
                    != after_reasonunit.rplan_active_requisite
                ):
                    x_believeratom.set_jvalue(
                        "rplan_active_requisite",
                        after_reasonunit.rplan_active_requisite,
                    )
                self.set_believeratom(x_believeratom)

            before_premise_pstates = set(before_reasonunit.premises.keys())
            after_premise_pstates = set(after_reasonunit.premises.keys())
            self.add_believeratom_plan_reason_premiseunit_inserts(
                plan_rope=before_planunit.get_plan_rope(),
                after_reasonunit=after_reasonunit,
                insert_premise_pstates=after_premise_pstates.difference(
                    before_premise_pstates
                ),
            )
            self.add_believeratom_plan_reason_premiseunit_updates(
                plan_rope=before_planunit.get_plan_rope(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_pstates=after_premise_pstates.intersection(
                    before_premise_pstates
                ),
            )
            self.add_believeratom_plan_reason_premiseunit_deletes(
                plan_rope=before_planunit.get_plan_rope(),
                reasonunit_rcontext=update_reasonunit_rcontext,
                delete_premise_pstates=before_premise_pstates.difference(
                    after_premise_pstates
                ),
            )

    def add_believeratom_plan_reasonunit_deletes(
        self, before_planunit: PlanUnit, delete_reasonunit_rcontexts: set
    ):
        for delete_reasonunit_rcontext in delete_reasonunit_rcontexts:
            x_believeratom = believeratom_shop("believer_plan_reasonunit", "DELETE")
            x_believeratom.set_jkey("plan_rope", before_planunit.get_plan_rope())
            x_believeratom.set_jkey("rcontext", delete_reasonunit_rcontext)
            self.set_believeratom(x_believeratom)

            before_reasonunit = before_planunit.get_reasonunit(
                delete_reasonunit_rcontext
            )
            self.add_believeratom_plan_reason_premiseunit_deletes(
                plan_rope=before_planunit.get_plan_rope(),
                reasonunit_rcontext=delete_reasonunit_rcontext,
                delete_premise_pstates=set(before_reasonunit.premises.keys()),
            )

    def add_believeratom_plan_reason_premiseunit_inserts(
        self,
        plan_rope: RopeTerm,
        after_reasonunit: ReasonUnit,
        insert_premise_pstates: set,
    ):
        for insert_premise_pstate in insert_premise_pstates:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_pstate)
            x_believeratom = believeratom_shop(
                "believer_plan_reason_premiseunit", "INSERT"
            )
            x_believeratom.set_jkey("plan_rope", plan_rope)
            x_believeratom.set_jkey("rcontext", after_reasonunit.rcontext)
            x_believeratom.set_jkey("pstate", after_premiseunit.pstate)
            if after_premiseunit.popen is not None:
                x_believeratom.set_jvalue("popen", after_premiseunit.popen)
            if after_premiseunit.pnigh is not None:
                x_believeratom.set_jvalue("pnigh", after_premiseunit.pnigh)
            if after_premiseunit.pdivisor is not None:
                x_believeratom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
            self.set_believeratom(x_believeratom)

    def add_believeratom_plan_reason_premiseunit_updates(
        self,
        plan_rope: RopeTerm,
        before_reasonunit: ReasonUnit,
        after_reasonunit: ReasonUnit,
        update_premise_pstates: set,
    ):
        for update_premise_pstate in update_premise_pstates:
            before_premiseunit = before_reasonunit.get_premise(update_premise_pstate)
            after_premiseunit = after_reasonunit.get_premise(update_premise_pstate)
            if jvalues_different(
                "believer_plan_reason_premiseunit",
                before_premiseunit,
                after_premiseunit,
            ):
                x_believeratom = believeratom_shop(
                    "believer_plan_reason_premiseunit", "UPDATE"
                )
                x_believeratom.set_jkey("plan_rope", plan_rope)
                x_believeratom.set_jkey("rcontext", before_reasonunit.rcontext)
                x_believeratom.set_jkey("pstate", after_premiseunit.pstate)
                if after_premiseunit.popen != before_premiseunit.popen:
                    x_believeratom.set_jvalue("popen", after_premiseunit.popen)
                if after_premiseunit.pnigh != before_premiseunit.pnigh:
                    x_believeratom.set_jvalue("pnigh", after_premiseunit.pnigh)
                if after_premiseunit.pdivisor != before_premiseunit.pdivisor:
                    x_believeratom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
                self.set_believeratom(x_believeratom)

    def add_believeratom_plan_reason_premiseunit_deletes(
        self,
        plan_rope: RopeTerm,
        reasonunit_rcontext: RopeTerm,
        delete_premise_pstates: set,
    ):
        for delete_premise_pstate in delete_premise_pstates:
            x_believeratom = believeratom_shop(
                "believer_plan_reason_premiseunit", "DELETE"
            )
            x_believeratom.set_jkey("plan_rope", plan_rope)
            x_believeratom.set_jkey("rcontext", reasonunit_rcontext)
            x_believeratom.set_jkey("pstate", delete_premise_pstate)
            self.set_believeratom(x_believeratom)

    def add_believeratom_plan_laborlink_insert(
        self, plan_rope: RopeTerm, insert_laborlink_labor_titles: set
    ):
        for insert_laborlink_labor_title in insert_laborlink_labor_titles:
            x_believeratom = believeratom_shop("believer_plan_laborlink", "INSERT")
            x_believeratom.set_jkey("plan_rope", plan_rope)
            x_believeratom.set_jkey("labor_title", insert_laborlink_labor_title)
            self.set_believeratom(x_believeratom)

    def add_believeratom_plan_laborlink_deletes(
        self, plan_rope: RopeTerm, delete_laborlink_labor_titles: set
    ):
        for delete_laborlink_labor_title in delete_laborlink_labor_titles:
            x_believeratom = believeratom_shop("believer_plan_laborlink", "DELETE")
            x_believeratom.set_jkey("plan_rope", plan_rope)
            x_believeratom.set_jkey("labor_title", delete_laborlink_labor_title)
            self.set_believeratom(x_believeratom)

    def add_believeratom_plan_healerlink_insert(
        self, plan_rope: RopeTerm, insert_healerlink_healer_names: set
    ):
        for insert_healerlink_healer_name in insert_healerlink_healer_names:
            x_believeratom = believeratom_shop("believer_plan_healerlink", "INSERT")
            x_believeratom.set_jkey("plan_rope", plan_rope)
            x_believeratom.set_jkey("healer_name", insert_healerlink_healer_name)
            self.set_believeratom(x_believeratom)

    def add_believeratom_plan_healerlink_deletes(
        self, plan_rope: RopeTerm, delete_healerlink_healer_names: set
    ):
        for delete_healerlink_healer_name in delete_healerlink_healer_names:
            x_believeratom = believeratom_shop("believer_plan_healerlink", "DELETE")
            x_believeratom.set_jkey("plan_rope", plan_rope)
            x_believeratom.set_jkey("healer_name", delete_healerlink_healer_name)
            self.set_believeratom(x_believeratom)

    def add_believeratom_plan_awardlink_inserts(
        self, after_planunit: PlanUnit, insert_awardlink_awardee_titles: set
    ):
        for after_awardlink_awardee_title in insert_awardlink_awardee_titles:
            after_awardlink = after_planunit.awardlinks.get(
                after_awardlink_awardee_title
            )
            x_believeratom = believeratom_shop("believer_plan_awardlink", "INSERT")
            x_believeratom.set_jkey("plan_rope", after_planunit.get_plan_rope())
            x_believeratom.set_jkey("awardee_title", after_awardlink.awardee_title)
            x_believeratom.set_jvalue("give_force", after_awardlink.give_force)
            x_believeratom.set_jvalue("take_force", after_awardlink.take_force)
            self.set_believeratom(x_believeratom)

    def add_believeratom_plan_awardlink_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_awardlink_awardee_titles: set,
    ):
        for update_awardlink_awardee_title in update_awardlink_awardee_titles:
            before_awardlink = before_planunit.awardlinks.get(
                update_awardlink_awardee_title
            )
            after_awardlink = after_planunit.awardlinks.get(
                update_awardlink_awardee_title
            )
            if jvalues_different(
                "believer_plan_awardlink", before_awardlink, after_awardlink
            ):
                x_believeratom = believeratom_shop("believer_plan_awardlink", "UPDATE")
                x_believeratom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_believeratom.set_jkey("awardee_title", after_awardlink.awardee_title)
                if before_awardlink.give_force != after_awardlink.give_force:
                    x_believeratom.set_jvalue("give_force", after_awardlink.give_force)
                if before_awardlink.take_force != after_awardlink.take_force:
                    x_believeratom.set_jvalue("take_force", after_awardlink.take_force)
                self.set_believeratom(x_believeratom)

    def add_believeratom_plan_awardlink_deletes(
        self, plan_rope: RopeTerm, delete_awardlink_awardee_titles: set
    ):
        for delete_awardlink_awardee_title in delete_awardlink_awardee_titles:
            x_believeratom = believeratom_shop("believer_plan_awardlink", "DELETE")
            x_believeratom.set_jkey("plan_rope", plan_rope)
            x_believeratom.set_jkey("awardee_title", delete_awardlink_awardee_title)
            self.set_believeratom(x_believeratom)

    def add_believeratom_plan_factunit_inserts(
        self, planunit: PlanUnit, insert_factunit_rcontexts: set
    ):
        for insert_factunit_rcontext in insert_factunit_rcontexts:
            insert_factunit = planunit.factunits.get(insert_factunit_rcontext)
            x_believeratom = believeratom_shop("believer_plan_factunit", "INSERT")
            x_believeratom.set_jkey("plan_rope", planunit.get_plan_rope())
            x_believeratom.set_jkey("fcontext", insert_factunit.fcontext)
            if insert_factunit.fstate is not None:
                x_believeratom.set_jvalue("fstate", insert_factunit.fstate)
            if insert_factunit.fopen is not None:
                x_believeratom.set_jvalue("fopen", insert_factunit.fopen)
            if insert_factunit.fnigh is not None:
                x_believeratom.set_jvalue("fnigh", insert_factunit.fnigh)
            self.set_believeratom(x_believeratom)

    def add_believeratom_plan_factunit_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_factunit_rcontexts: set,
    ):
        for update_factunit_rcontext in update_factunit_rcontexts:
            before_factunit = before_planunit.factunits.get(update_factunit_rcontext)
            after_factunit = after_planunit.factunits.get(update_factunit_rcontext)
            if jvalues_different(
                "believer_plan_factunit", before_factunit, after_factunit
            ):
                x_believeratom = believeratom_shop("believer_plan_factunit", "UPDATE")
                x_believeratom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_believeratom.set_jkey("fcontext", after_factunit.fcontext)
                if before_factunit.fstate != after_factunit.fstate:
                    x_believeratom.set_jvalue("fstate", after_factunit.fstate)
                if before_factunit.fopen != after_factunit.fopen:
                    x_believeratom.set_jvalue("fopen", after_factunit.fopen)
                if before_factunit.fnigh != after_factunit.fnigh:
                    x_believeratom.set_jvalue("fnigh", after_factunit.fnigh)
                self.set_believeratom(x_believeratom)

    def add_believeratom_plan_factunit_deletes(
        self, plan_rope: RopeTerm, delete_factunit_rcontexts: FactUnit
    ):
        for delete_factunit_rcontext in delete_factunit_rcontexts:
            x_believeratom = believeratom_shop("believer_plan_factunit", "DELETE")
            x_believeratom.set_jkey("plan_rope", plan_rope)
            x_believeratom.set_jkey("fcontext", delete_factunit_rcontext)
            self.set_believeratom(x_believeratom)

    def is_empty(self) -> bool:
        return self.believeratoms == {}

    def get_ordered_believeratoms(self, x_count: int = None) -> dict[int, BelieverAtom]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_atom in self.get_sorted_believeratoms():
            x_dict[x_count] = x_atom
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int, str]:
        atom_tuples = self.get_ordered_believeratoms(x_count).items()
        return {atom_num: atom_obj.get_dict() for atom_num, atom_obj in atom_tuples}

    def get_json(self, x_count: int = None) -> str:
        x_dict = self.get_ordered_dict(x_count)
        return get_json_from_dict(x_dict)


def believerdelta_shop(believeratoms: dict[str, BelieverAtom] = None) -> BelieverDelta:
    return BelieverDelta(
        believeratoms=get_empty_dict_if_None(believeratoms),
        _believer_build_validated=False,
    )


def believer_built_from_delta_is_valid(
    x_delta: BelieverDelta, x_believer: BelieverUnit = None
) -> bool:
    x_believer = believerunit_shop() if x_believer is None else x_believer
    x_believer = x_delta.get_edited_believer(x_believer)
    try:
        x_believer.settle_believer()
    except Exception:
        return False
    return True


def get_dimens_cruds_believerdelta(
    x_believerdelta: BelieverDelta, dimen_set: set[str], curd_set: set[str]
) -> BelieverDelta:
    new_believerdelta = believerdelta_shop()
    for x_believeratom in x_believerdelta.get_sorted_believeratoms():
        if x_believeratom.crud_str in curd_set and x_believeratom.dimen in dimen_set:
            new_believerdelta.set_believeratom(x_believeratom)
    return new_believerdelta


def get_minimal_believerdelta(
    x_believerdelta: BelieverDelta, x_believer: BelieverUnit
) -> BelieverDelta:
    """Creates new BelieverDelta with only BelieverAtoms that would actually change the BelieverUnit"""
    new_believerdelta = believerdelta_shop()
    for x_atom in x_believerdelta.get_sorted_believeratoms():
        sifted_atom = sift_believeratom(x_believer, x_atom)
        if sifted_atom != None:
            new_believerdelta.set_believeratom(sifted_atom)
    return new_believerdelta


def get_believerdelta_from_ordered_dict(x_dict: dict) -> BelieverDelta:
    x_believerdelta = believerdelta_shop()
    for x_atom_dict in x_dict.values():
        x_believerdelta.set_believeratom(get_believeratom_from_dict(x_atom_dict))
    return x_believerdelta
