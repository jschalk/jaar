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
from src.a03_group_logic.acct import AcctName, AcctUnit, MemberShip
from src.a03_group_logic.group import MemberShip
from src.a04_reason_logic.reason_plan import FactUnit, ReasonUnit
from src.a05_plan_logic.plan import PlanUnit
from src.a06_owner_logic.owner import OwnerUnit, ownerunit_shop
from src.a08_owner_atom_logic.atom import (
    InvalidOwnerAtomException,
    OwnerAtom,
    get_from_dict as get_owneratom_from_dict,
    jvalues_different,
    modify_owner_with_owneratom,
    owneratom_shop,
    sift_owneratom,
)
from src.a08_owner_atom_logic.atom_config import CRUD_command


@dataclass
class OwnerDelta:
    owneratoms: dict[CRUD_command : dict[str, OwnerAtom]] = None
    _owner_build_validated: bool = None

    def _get_crud_owneratoms_list(self) -> dict[CRUD_command, list[OwnerAtom]]:
        return get_all_nondictionary_objs(self.owneratoms)

    def get_dimen_sorted_owneratoms_list(self) -> list[OwnerAtom]:
        atoms_list = []
        for crud_list in self._get_crud_owneratoms_list().values():
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

    def get_sorted_owneratoms(self) -> list[OwnerAtom]:
        owneratoms_list = self.get_dimen_sorted_owneratoms_list()
        return sorted(owneratoms_list, key=lambda x: x.atom_order)

    def get_edited_owner(self, before_owner: OwnerUnit) -> OwnerUnit:
        edited_owner = copy_deepcopy(before_owner)
        for x_owneratom in self.get_sorted_owneratoms():
            modify_owner_with_owneratom(edited_owner, x_owneratom)
        return edited_owner

    def set_owneratom(self, x_owneratom: OwnerAtom):
        if x_owneratom.is_valid() is False:
            raise InvalidOwnerAtomException(
                f"""'{x_owneratom.dimen}' {x_owneratom.crud_str} OwnerAtom is invalid
                {x_owneratom.is_jkeys_valid()=}
                {x_owneratom.is_jvalues_valid()=}"""
            )

        x_owneratom.set_atom_order()
        x_keylist = [
            x_owneratom.crud_str,
            x_owneratom.dimen,
            *x_owneratom.get_nesting_order_args(),
        ]
        set_in_nested_dict(self.owneratoms, x_keylist, x_owneratom)

    def owneratom_exists(self, x_owneratom: OwnerAtom) -> bool:
        if x_owneratom.is_valid() is False:
            raise InvalidOwnerAtomException(
                f"""'{x_owneratom.dimen}' {x_owneratom.crud_str} OwnerAtom is invalid
                {x_owneratom.is_jkeys_valid()=}
                {x_owneratom.is_jvalues_valid()=}"""
            )

        x_owneratom.set_atom_order()
        x_keylist = [
            x_owneratom.crud_str,
            x_owneratom.dimen,
            *list(x_owneratom.get_nesting_order_args()),
        ]
        nested_owneratom = get_from_nested_dict(self.owneratoms, x_keylist, True)
        return nested_owneratom == x_owneratom

    def add_owneratom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        x_owneratom = owneratom_shop(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=jkeys,
            jvalues=jvalues,
        )
        self.set_owneratom(x_owneratom)

    def get_owneratom(self, crud_str: str, dimen: str, jkeys: list[str]) -> OwnerAtom:
        x_keylist = [crud_str, dimen, *jkeys]
        return get_from_nested_dict(self.owneratoms, x_keylist)

    def add_all_owneratoms(self, after_owner: OwnerUnit):
        before_owner = ownerunit_shop(after_owner.owner_name, after_owner.belief_label)
        self.add_all_different_owneratoms(before_owner, after_owner)

    def add_all_different_owneratoms(
        self, before_owner: OwnerUnit, after_owner: OwnerUnit
    ):
        before_owner.settle_owner()
        after_owner.settle_owner()
        self.add_owneratoms_ownerunit_simple_attrs(before_owner, after_owner)
        self.add_owneratoms_accts(before_owner, after_owner)
        self.add_owneratoms_plans(before_owner, after_owner)

    def add_owneratoms_ownerunit_simple_attrs(
        self, before_owner: OwnerUnit, after_owner: OwnerUnit
    ):
        if not jvalues_different("ownerunit", before_owner, after_owner):
            return
        x_owneratom = owneratom_shop("ownerunit", "UPDATE")
        if before_owner.max_tree_traverse != after_owner.max_tree_traverse:
            x_owneratom.set_jvalue("max_tree_traverse", after_owner.max_tree_traverse)
        if before_owner.credor_respect != after_owner.credor_respect:
            x_owneratom.set_jvalue("credor_respect", after_owner.credor_respect)
        if before_owner.debtor_respect != after_owner.debtor_respect:
            x_owneratom.set_jvalue("debtor_respect", after_owner.debtor_respect)
        if before_owner.tally != after_owner.tally:
            x_owneratom.set_jvalue("tally", after_owner.tally)
        if before_owner.fund_pool != after_owner.fund_pool:
            x_owneratom.set_jvalue("fund_pool", after_owner.fund_pool)
        if before_owner.fund_iota != after_owner.fund_iota:
            x_owneratom.set_jvalue("fund_iota", after_owner.fund_iota)
        if before_owner.respect_bit != after_owner.respect_bit:
            x_owneratom.set_jvalue("respect_bit", after_owner.respect_bit)
        self.set_owneratom(x_owneratom)

    def add_owneratoms_accts(self, before_owner: OwnerUnit, after_owner: OwnerUnit):
        before_acct_names = set(before_owner.accts.keys())
        after_acct_names = set(after_owner.accts.keys())

        self.add_owneratom_acctunit_inserts(
            after_owner=after_owner,
            insert_acct_names=after_acct_names.difference(before_acct_names),
        )
        self.add_owneratom_acctunit_deletes(
            before_owner=before_owner,
            delete_acct_names=before_acct_names.difference(after_acct_names),
        )
        self.add_owneratom_acctunit_updates(
            before_owner=before_owner,
            after_owner=after_owner,
            update_acct_names=before_acct_names.intersection(after_acct_names),
        )

    def add_owneratom_acctunit_inserts(
        self, after_owner: OwnerUnit, insert_acct_names: set
    ):
        for insert_acct_name in insert_acct_names:
            insert_acctunit = after_owner.get_acct(insert_acct_name)
            x_owneratom = owneratom_shop("owner_acctunit", "INSERT")
            x_owneratom.set_jkey("acct_name", insert_acctunit.acct_name)
            if insert_acctunit.acct_cred_points is not None:
                x_owneratom.set_jvalue(
                    "acct_cred_points", insert_acctunit.acct_cred_points
                )
            if insert_acctunit.acct_debt_points is not None:
                x_owneratom.set_jvalue(
                    "acct_debt_points", insert_acctunit.acct_debt_points
                )
            self.set_owneratom(x_owneratom)
            all_group_titles = set(insert_acctunit._memberships.keys())
            self.add_owneratom_memberships_inserts(
                after_acctunit=insert_acctunit,
                insert_membership_group_titles=all_group_titles,
            )

    def add_owneratom_acctunit_updates(
        self, before_owner: OwnerUnit, after_owner: OwnerUnit, update_acct_names: set
    ):
        for acct_name in update_acct_names:
            after_acctunit = after_owner.get_acct(acct_name)
            before_acctunit = before_owner.get_acct(acct_name)
            if jvalues_different("owner_acctunit", after_acctunit, before_acctunit):
                x_owneratom = owneratom_shop("owner_acctunit", "UPDATE")
                x_owneratom.set_jkey("acct_name", after_acctunit.acct_name)
                if before_acctunit.acct_cred_points != after_acctunit.acct_cred_points:
                    x_owneratom.set_jvalue(
                        "acct_cred_points", after_acctunit.acct_cred_points
                    )
                if before_acctunit.acct_debt_points != after_acctunit.acct_debt_points:
                    x_owneratom.set_jvalue(
                        "acct_debt_points", after_acctunit.acct_debt_points
                    )
                self.set_owneratom(x_owneratom)
            self.add_owneratom_acctunit_update_memberships(
                after_acctunit=after_acctunit, before_acctunit=before_acctunit
            )

    def add_owneratom_acctunit_deletes(
        self, before_owner: OwnerUnit, delete_acct_names: set
    ):
        for delete_acct_name in delete_acct_names:
            x_owneratom = owneratom_shop("owner_acctunit", "DELETE")
            x_owneratom.set_jkey("acct_name", delete_acct_name)
            self.set_owneratom(x_owneratom)
            delete_acctunit = before_owner.get_acct(delete_acct_name)
            non_mirror_group_titles = {
                x_group_title
                for x_group_title in delete_acctunit._memberships.keys()
                if x_group_title != delete_acct_name
            }
            self.add_owneratom_memberships_delete(
                delete_acct_name, non_mirror_group_titles
            )

    def add_owneratom_acctunit_update_memberships(
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

        self.add_owneratom_memberships_inserts(
            after_acctunit=after_acctunit,
            insert_membership_group_titles=after_group_titles.difference(
                before_group_titles
            ),
        )

        self.add_owneratom_memberships_delete(
            before_acct_name=after_acctunit.acct_name,
            before_group_titles=before_group_titles.difference(after_group_titles),
        )

        update_group_titles = before_group_titles.intersection(after_group_titles)
        for update_acct_name in update_group_titles:
            before_membership = before_acctunit.get_membership(update_acct_name)
            after_membership = after_acctunit.get_membership(update_acct_name)
            if jvalues_different(
                "owner_acct_membership", before_membership, after_membership
            ):
                self.add_owneratom_membership_update(
                    acct_name=after_acctunit.acct_name,
                    before_membership=before_membership,
                    after_membership=after_membership,
                )

    def add_owneratom_memberships_inserts(
        self,
        after_acctunit: AcctUnit,
        insert_membership_group_titles: list[TitleTerm],
    ):
        after_acct_name = after_acctunit.acct_name
        for insert_group_title in insert_membership_group_titles:
            after_membership = after_acctunit.get_membership(insert_group_title)
            x_owneratom = owneratom_shop("owner_acct_membership", "INSERT")
            x_owneratom.set_jkey("acct_name", after_acct_name)
            x_owneratom.set_jkey("group_title", after_membership.group_title)
            if after_membership.group_cred_points is not None:
                x_owneratom.set_jvalue(
                    "group_cred_points", after_membership.group_cred_points
                )
            if after_membership.group_debt_points is not None:
                x_owneratom.set_jvalue(
                    "group_debt_points", after_membership.group_debt_points
                )
            self.set_owneratom(x_owneratom)

    def add_owneratom_membership_update(
        self,
        acct_name: AcctName,
        before_membership: MemberShip,
        after_membership: MemberShip,
    ):
        x_owneratom = owneratom_shop("owner_acct_membership", "UPDATE")
        x_owneratom.set_jkey("acct_name", acct_name)
        x_owneratom.set_jkey("group_title", after_membership.group_title)
        if after_membership.group_cred_points != before_membership.group_cred_points:
            x_owneratom.set_jvalue(
                "group_cred_points", after_membership.group_cred_points
            )
        if after_membership.group_debt_points != before_membership.group_debt_points:
            x_owneratom.set_jvalue(
                "group_debt_points", after_membership.group_debt_points
            )
        self.set_owneratom(x_owneratom)

    def add_owneratom_memberships_delete(
        self, before_acct_name: AcctName, before_group_titles: TitleTerm
    ):
        for delete_group_title in before_group_titles:
            x_owneratom = owneratom_shop("owner_acct_membership", "DELETE")
            x_owneratom.set_jkey("acct_name", before_acct_name)
            x_owneratom.set_jkey("group_title", delete_group_title)
            self.set_owneratom(x_owneratom)

    def add_owneratoms_plans(self, before_owner: OwnerUnit, after_owner: OwnerUnit):
        before_plan_ropes = set(before_owner._plan_dict.keys())
        after_plan_ropes = set(after_owner._plan_dict.keys())

        self.add_owneratom_plan_inserts(
            after_owner=after_owner,
            insert_plan_ropes=after_plan_ropes.difference(before_plan_ropes),
        )
        self.add_owneratom_plan_deletes(
            before_owner=before_owner,
            delete_plan_ropes=before_plan_ropes.difference(after_plan_ropes),
        )
        self.add_owneratom_plan_updates(
            before_owner=before_owner,
            after_owner=after_owner,
            update_ropes=before_plan_ropes.intersection(after_plan_ropes),
        )

    def add_owneratom_plan_inserts(
        self, after_owner: OwnerUnit, insert_plan_ropes: set
    ):
        for insert_plan_rope in insert_plan_ropes:
            insert_planunit = after_owner.get_plan_obj(insert_plan_rope)
            x_owneratom = owneratom_shop("owner_planunit", "INSERT")
            x_owneratom.set_jkey("plan_rope", insert_planunit.get_plan_rope())
            x_owneratom.set_jvalue("addin", insert_planunit.addin)
            x_owneratom.set_jvalue("begin", insert_planunit.begin)
            x_owneratom.set_jvalue("close", insert_planunit.close)
            x_owneratom.set_jvalue("denom", insert_planunit.denom)
            x_owneratom.set_jvalue("numor", insert_planunit.numor)
            x_owneratom.set_jvalue("morph", insert_planunit.morph)
            x_owneratom.set_jvalue("mass", insert_planunit.mass)
            x_owneratom.set_jvalue("task", insert_planunit.task)
            self.set_owneratom(x_owneratom)

            self.add_owneratom_plan_factunit_inserts(
                planunit=insert_planunit,
                insert_factunit_rcontexts=set(insert_planunit.factunits.keys()),
            )
            self.add_owneratom_plan_awardlink_inserts(
                after_planunit=insert_planunit,
                insert_awardlink_awardee_titles=set(insert_planunit.awardlinks.keys()),
            )
            self.add_owneratom_plan_reasonunit_inserts(
                after_planunit=insert_planunit,
                insert_reasonunit_rcontexts=set(insert_planunit.reasonunits.keys()),
            )
            self.add_owneratom_plan_laborlink_insert(
                plan_rope=insert_plan_rope,
                insert_laborlink_labor_titles=insert_planunit.laborunit._laborlinks,
            )
            self.add_owneratom_plan_healerlink_insert(
                plan_rope=insert_plan_rope,
                insert_healerlink_healer_names=insert_planunit.healerlink._healer_names,
            )

    def add_owneratom_plan_updates(
        self, before_owner: OwnerUnit, after_owner: OwnerUnit, update_ropes: set
    ):
        for plan_rope in update_ropes:
            after_planunit = after_owner.get_plan_obj(plan_rope)
            before_planunit = before_owner.get_plan_obj(plan_rope)
            if jvalues_different("owner_planunit", before_planunit, after_planunit):
                x_owneratom = owneratom_shop("owner_planunit", "UPDATE")
                x_owneratom.set_jkey("plan_rope", after_planunit.get_plan_rope())
                if before_planunit.addin != after_planunit.addin:
                    x_owneratom.set_jvalue("addin", after_planunit.addin)
                if before_planunit.begin != after_planunit.begin:
                    x_owneratom.set_jvalue("begin", after_planunit.begin)
                if before_planunit.close != after_planunit.close:
                    x_owneratom.set_jvalue("close", after_planunit.close)
                if before_planunit.denom != after_planunit.denom:
                    x_owneratom.set_jvalue("denom", after_planunit.denom)
                if before_planunit.numor != after_planunit.numor:
                    x_owneratom.set_jvalue("numor", after_planunit.numor)
                if before_planunit.morph != after_planunit.morph:
                    x_owneratom.set_jvalue("morph", after_planunit.morph)
                if before_planunit.mass != after_planunit.mass:
                    x_owneratom.set_jvalue("mass", after_planunit.mass)
                if before_planunit.task != after_planunit.task:
                    x_owneratom.set_jvalue("task", after_planunit.task)
                self.set_owneratom(x_owneratom)

            # insert / update / delete factunits
            before_factunit_rcontexts = set(before_planunit.factunits.keys())
            after_factunit_rcontexts = set(after_planunit.factunits.keys())
            self.add_owneratom_plan_factunit_inserts(
                planunit=after_planunit,
                insert_factunit_rcontexts=after_factunit_rcontexts.difference(
                    before_factunit_rcontexts
                ),
            )
            self.add_owneratom_plan_factunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_factunit_rcontexts=before_factunit_rcontexts.intersection(
                    after_factunit_rcontexts
                ),
            )
            self.add_owneratom_plan_factunit_deletes(
                plan_rope=plan_rope,
                delete_factunit_rcontexts=before_factunit_rcontexts.difference(
                    after_factunit_rcontexts
                ),
            )

            # insert / update / delete awardunits
            before_awardlinks_awardee_titles = set(before_planunit.awardlinks.keys())
            after_awardlinks_awardee_titles = set(after_planunit.awardlinks.keys())
            self.add_owneratom_plan_awardlink_inserts(
                after_planunit=after_planunit,
                insert_awardlink_awardee_titles=after_awardlinks_awardee_titles.difference(
                    before_awardlinks_awardee_titles
                ),
            )
            self.add_owneratom_plan_awardlink_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_awardlink_awardee_titles=before_awardlinks_awardee_titles.intersection(
                    after_awardlinks_awardee_titles
                ),
            )
            self.add_owneratom_plan_awardlink_deletes(
                plan_rope=plan_rope,
                delete_awardlink_awardee_titles=before_awardlinks_awardee_titles.difference(
                    after_awardlinks_awardee_titles
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_rcontexts = set(before_planunit.reasonunits.keys())
            after_reasonunit_rcontexts = set(after_planunit.reasonunits.keys())
            self.add_owneratom_plan_reasonunit_inserts(
                after_planunit=after_planunit,
                insert_reasonunit_rcontexts=after_reasonunit_rcontexts.difference(
                    before_reasonunit_rcontexts
                ),
            )
            self.add_owneratom_plan_reasonunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_reasonunit_rcontexts=before_reasonunit_rcontexts.intersection(
                    after_reasonunit_rcontexts
                ),
            )
            self.add_owneratom_plan_reasonunit_deletes(
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
            self.add_owneratom_plan_laborlink_insert(
                plan_rope=plan_rope,
                insert_laborlink_labor_titles=after_laborlinks_labor_titles.difference(
                    before_laborlinks_labor_titles
                ),
            )
            self.add_owneratom_plan_laborlink_deletes(
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
            self.add_owneratom_plan_healerlink_insert(
                plan_rope=plan_rope,
                insert_healerlink_healer_names=after_healerlinks_healer_names.difference(
                    before_healerlinks_healer_names
                ),
            )
            self.add_owneratom_plan_healerlink_deletes(
                plan_rope=plan_rope,
                delete_healerlink_healer_names=before_healerlinks_healer_names.difference(
                    after_healerlinks_healer_names
                ),
            )

    def add_owneratom_plan_deletes(
        self, before_owner: OwnerUnit, delete_plan_ropes: set
    ):
        for delete_plan_rope in delete_plan_ropes:
            x_owneratom = owneratom_shop("owner_planunit", "DELETE")
            x_owneratom.set_jkey("plan_rope", delete_plan_rope)
            self.set_owneratom(x_owneratom)

            delete_planunit = before_owner.get_plan_obj(delete_plan_rope)
            self.add_owneratom_plan_factunit_deletes(
                plan_rope=delete_plan_rope,
                delete_factunit_rcontexts=set(delete_planunit.factunits.keys()),
            )

            self.add_owneratom_plan_awardlink_deletes(
                plan_rope=delete_plan_rope,
                delete_awardlink_awardee_titles=set(delete_planunit.awardlinks.keys()),
            )
            self.add_owneratom_plan_reasonunit_deletes(
                before_planunit=delete_planunit,
                delete_reasonunit_rcontexts=set(delete_planunit.reasonunits.keys()),
            )
            self.add_owneratom_plan_laborlink_deletes(
                plan_rope=delete_plan_rope,
                delete_laborlink_labor_titles=delete_planunit.laborunit._laborlinks,
            )
            self.add_owneratom_plan_healerlink_deletes(
                plan_rope=delete_plan_rope,
                delete_healerlink_healer_names=delete_planunit.healerlink._healer_names,
            )

    def add_owneratom_plan_reasonunit_inserts(
        self, after_planunit: PlanUnit, insert_reasonunit_rcontexts: set
    ):
        for insert_reasonunit_rcontext in insert_reasonunit_rcontexts:
            after_reasonunit = after_planunit.get_reasonunit(insert_reasonunit_rcontext)
            x_owneratom = owneratom_shop("owner_plan_reasonunit", "INSERT")
            x_owneratom.set_jkey("plan_rope", after_planunit.get_plan_rope())
            x_owneratom.set_jkey("rcontext", after_reasonunit.rcontext)
            if after_reasonunit.rplan_active_requisite is not None:
                x_owneratom.set_jvalue(
                    "rplan_active_requisite",
                    after_reasonunit.rplan_active_requisite,
                )
            self.set_owneratom(x_owneratom)

            self.add_owneratom_plan_reason_premiseunit_inserts(
                plan_rope=after_planunit.get_plan_rope(),
                after_reasonunit=after_reasonunit,
                insert_premise_pstates=set(after_reasonunit.premises.keys()),
            )

    def add_owneratom_plan_reasonunit_updates(
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
                "owner_plan_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_owneratom = owneratom_shop("owner_plan_reasonunit", "UPDATE")
                x_owneratom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_owneratom.set_jkey("rcontext", after_reasonunit.rcontext)
                if (
                    before_reasonunit.rplan_active_requisite
                    != after_reasonunit.rplan_active_requisite
                ):
                    x_owneratom.set_jvalue(
                        "rplan_active_requisite",
                        after_reasonunit.rplan_active_requisite,
                    )
                self.set_owneratom(x_owneratom)

            before_premise_pstates = set(before_reasonunit.premises.keys())
            after_premise_pstates = set(after_reasonunit.premises.keys())
            self.add_owneratom_plan_reason_premiseunit_inserts(
                plan_rope=before_planunit.get_plan_rope(),
                after_reasonunit=after_reasonunit,
                insert_premise_pstates=after_premise_pstates.difference(
                    before_premise_pstates
                ),
            )
            self.add_owneratom_plan_reason_premiseunit_updates(
                plan_rope=before_planunit.get_plan_rope(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_pstates=after_premise_pstates.intersection(
                    before_premise_pstates
                ),
            )
            self.add_owneratom_plan_reason_premiseunit_deletes(
                plan_rope=before_planunit.get_plan_rope(),
                reasonunit_rcontext=update_reasonunit_rcontext,
                delete_premise_pstates=before_premise_pstates.difference(
                    after_premise_pstates
                ),
            )

    def add_owneratom_plan_reasonunit_deletes(
        self, before_planunit: PlanUnit, delete_reasonunit_rcontexts: set
    ):
        for delete_reasonunit_rcontext in delete_reasonunit_rcontexts:
            x_owneratom = owneratom_shop("owner_plan_reasonunit", "DELETE")
            x_owneratom.set_jkey("plan_rope", before_planunit.get_plan_rope())
            x_owneratom.set_jkey("rcontext", delete_reasonunit_rcontext)
            self.set_owneratom(x_owneratom)

            before_reasonunit = before_planunit.get_reasonunit(
                delete_reasonunit_rcontext
            )
            self.add_owneratom_plan_reason_premiseunit_deletes(
                plan_rope=before_planunit.get_plan_rope(),
                reasonunit_rcontext=delete_reasonunit_rcontext,
                delete_premise_pstates=set(before_reasonunit.premises.keys()),
            )

    def add_owneratom_plan_reason_premiseunit_inserts(
        self,
        plan_rope: RopeTerm,
        after_reasonunit: ReasonUnit,
        insert_premise_pstates: set,
    ):
        for insert_premise_pstate in insert_premise_pstates:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_pstate)
            x_owneratom = owneratom_shop("owner_plan_reason_premiseunit", "INSERT")
            x_owneratom.set_jkey("plan_rope", plan_rope)
            x_owneratom.set_jkey("rcontext", after_reasonunit.rcontext)
            x_owneratom.set_jkey("pstate", after_premiseunit.pstate)
            if after_premiseunit.popen is not None:
                x_owneratom.set_jvalue("popen", after_premiseunit.popen)
            if after_premiseunit.pnigh is not None:
                x_owneratom.set_jvalue("pnigh", after_premiseunit.pnigh)
            if after_premiseunit.pdivisor is not None:
                x_owneratom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
            self.set_owneratom(x_owneratom)

    def add_owneratom_plan_reason_premiseunit_updates(
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
                "owner_plan_reason_premiseunit",
                before_premiseunit,
                after_premiseunit,
            ):
                x_owneratom = owneratom_shop("owner_plan_reason_premiseunit", "UPDATE")
                x_owneratom.set_jkey("plan_rope", plan_rope)
                x_owneratom.set_jkey("rcontext", before_reasonunit.rcontext)
                x_owneratom.set_jkey("pstate", after_premiseunit.pstate)
                if after_premiseunit.popen != before_premiseunit.popen:
                    x_owneratom.set_jvalue("popen", after_premiseunit.popen)
                if after_premiseunit.pnigh != before_premiseunit.pnigh:
                    x_owneratom.set_jvalue("pnigh", after_premiseunit.pnigh)
                if after_premiseunit.pdivisor != before_premiseunit.pdivisor:
                    x_owneratom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
                self.set_owneratom(x_owneratom)

    def add_owneratom_plan_reason_premiseunit_deletes(
        self,
        plan_rope: RopeTerm,
        reasonunit_rcontext: RopeTerm,
        delete_premise_pstates: set,
    ):
        for delete_premise_pstate in delete_premise_pstates:
            x_owneratom = owneratom_shop("owner_plan_reason_premiseunit", "DELETE")
            x_owneratom.set_jkey("plan_rope", plan_rope)
            x_owneratom.set_jkey("rcontext", reasonunit_rcontext)
            x_owneratom.set_jkey("pstate", delete_premise_pstate)
            self.set_owneratom(x_owneratom)

    def add_owneratom_plan_laborlink_insert(
        self, plan_rope: RopeTerm, insert_laborlink_labor_titles: set
    ):
        for insert_laborlink_labor_title in insert_laborlink_labor_titles:
            x_owneratom = owneratom_shop("owner_plan_laborlink", "INSERT")
            x_owneratom.set_jkey("plan_rope", plan_rope)
            x_owneratom.set_jkey("labor_title", insert_laborlink_labor_title)
            self.set_owneratom(x_owneratom)

    def add_owneratom_plan_laborlink_deletes(
        self, plan_rope: RopeTerm, delete_laborlink_labor_titles: set
    ):
        for delete_laborlink_labor_title in delete_laborlink_labor_titles:
            x_owneratom = owneratom_shop("owner_plan_laborlink", "DELETE")
            x_owneratom.set_jkey("plan_rope", plan_rope)
            x_owneratom.set_jkey("labor_title", delete_laborlink_labor_title)
            self.set_owneratom(x_owneratom)

    def add_owneratom_plan_healerlink_insert(
        self, plan_rope: RopeTerm, insert_healerlink_healer_names: set
    ):
        for insert_healerlink_healer_name in insert_healerlink_healer_names:
            x_owneratom = owneratom_shop("owner_plan_healerlink", "INSERT")
            x_owneratom.set_jkey("plan_rope", plan_rope)
            x_owneratom.set_jkey("healer_name", insert_healerlink_healer_name)
            self.set_owneratom(x_owneratom)

    def add_owneratom_plan_healerlink_deletes(
        self, plan_rope: RopeTerm, delete_healerlink_healer_names: set
    ):
        for delete_healerlink_healer_name in delete_healerlink_healer_names:
            x_owneratom = owneratom_shop("owner_plan_healerlink", "DELETE")
            x_owneratom.set_jkey("plan_rope", plan_rope)
            x_owneratom.set_jkey("healer_name", delete_healerlink_healer_name)
            self.set_owneratom(x_owneratom)

    def add_owneratom_plan_awardlink_inserts(
        self, after_planunit: PlanUnit, insert_awardlink_awardee_titles: set
    ):
        for after_awardlink_awardee_title in insert_awardlink_awardee_titles:
            after_awardlink = after_planunit.awardlinks.get(
                after_awardlink_awardee_title
            )
            x_owneratom = owneratom_shop("owner_plan_awardlink", "INSERT")
            x_owneratom.set_jkey("plan_rope", after_planunit.get_plan_rope())
            x_owneratom.set_jkey("awardee_title", after_awardlink.awardee_title)
            x_owneratom.set_jvalue("give_force", after_awardlink.give_force)
            x_owneratom.set_jvalue("take_force", after_awardlink.take_force)
            self.set_owneratom(x_owneratom)

    def add_owneratom_plan_awardlink_updates(
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
                "owner_plan_awardlink", before_awardlink, after_awardlink
            ):
                x_owneratom = owneratom_shop("owner_plan_awardlink", "UPDATE")
                x_owneratom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_owneratom.set_jkey("awardee_title", after_awardlink.awardee_title)
                if before_awardlink.give_force != after_awardlink.give_force:
                    x_owneratom.set_jvalue("give_force", after_awardlink.give_force)
                if before_awardlink.take_force != after_awardlink.take_force:
                    x_owneratom.set_jvalue("take_force", after_awardlink.take_force)
                self.set_owneratom(x_owneratom)

    def add_owneratom_plan_awardlink_deletes(
        self, plan_rope: RopeTerm, delete_awardlink_awardee_titles: set
    ):
        for delete_awardlink_awardee_title in delete_awardlink_awardee_titles:
            x_owneratom = owneratom_shop("owner_plan_awardlink", "DELETE")
            x_owneratom.set_jkey("plan_rope", plan_rope)
            x_owneratom.set_jkey("awardee_title", delete_awardlink_awardee_title)
            self.set_owneratom(x_owneratom)

    def add_owneratom_plan_factunit_inserts(
        self, planunit: PlanUnit, insert_factunit_rcontexts: set
    ):
        for insert_factunit_rcontext in insert_factunit_rcontexts:
            insert_factunit = planunit.factunits.get(insert_factunit_rcontext)
            x_owneratom = owneratom_shop("owner_plan_factunit", "INSERT")
            x_owneratom.set_jkey("plan_rope", planunit.get_plan_rope())
            x_owneratom.set_jkey("fcontext", insert_factunit.fcontext)
            if insert_factunit.fstate is not None:
                x_owneratom.set_jvalue("fstate", insert_factunit.fstate)
            if insert_factunit.fopen is not None:
                x_owneratom.set_jvalue("fopen", insert_factunit.fopen)
            if insert_factunit.fnigh is not None:
                x_owneratom.set_jvalue("fnigh", insert_factunit.fnigh)
            self.set_owneratom(x_owneratom)

    def add_owneratom_plan_factunit_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_factunit_rcontexts: set,
    ):
        for update_factunit_rcontext in update_factunit_rcontexts:
            before_factunit = before_planunit.factunits.get(update_factunit_rcontext)
            after_factunit = after_planunit.factunits.get(update_factunit_rcontext)
            if jvalues_different(
                "owner_plan_factunit", before_factunit, after_factunit
            ):
                x_owneratom = owneratom_shop("owner_plan_factunit", "UPDATE")
                x_owneratom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_owneratom.set_jkey("fcontext", after_factunit.fcontext)
                if before_factunit.fstate != after_factunit.fstate:
                    x_owneratom.set_jvalue("fstate", after_factunit.fstate)
                if before_factunit.fopen != after_factunit.fopen:
                    x_owneratom.set_jvalue("fopen", after_factunit.fopen)
                if before_factunit.fnigh != after_factunit.fnigh:
                    x_owneratom.set_jvalue("fnigh", after_factunit.fnigh)
                self.set_owneratom(x_owneratom)

    def add_owneratom_plan_factunit_deletes(
        self, plan_rope: RopeTerm, delete_factunit_rcontexts: FactUnit
    ):
        for delete_factunit_rcontext in delete_factunit_rcontexts:
            x_owneratom = owneratom_shop("owner_plan_factunit", "DELETE")
            x_owneratom.set_jkey("plan_rope", plan_rope)
            x_owneratom.set_jkey("fcontext", delete_factunit_rcontext)
            self.set_owneratom(x_owneratom)

    def is_empty(self) -> bool:
        return self.owneratoms == {}

    def get_ordered_owneratoms(self, x_count: int = None) -> dict[int, OwnerAtom]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_atom in self.get_sorted_owneratoms():
            x_dict[x_count] = x_atom
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int, str]:
        atom_tuples = self.get_ordered_owneratoms(x_count).items()
        return {atom_num: atom_obj.get_dict() for atom_num, atom_obj in atom_tuples}

    def get_json(self, x_count: int = None) -> str:
        x_dict = self.get_ordered_dict(x_count)
        return get_json_from_dict(x_dict)


def ownerdelta_shop(owneratoms: dict[str, OwnerAtom] = None) -> OwnerDelta:
    return OwnerDelta(
        owneratoms=get_empty_dict_if_None(owneratoms),
        _owner_build_validated=False,
    )


def owner_built_from_delta_is_valid(
    x_delta: OwnerDelta, x_owner: OwnerUnit = None
) -> bool:
    x_owner = ownerunit_shop() if x_owner is None else x_owner
    x_owner = x_delta.get_edited_owner(x_owner)
    try:
        x_owner.settle_owner()
    except Exception:
        return False
    return True


def get_dimens_cruds_ownerdelta(
    x_ownerdelta: OwnerDelta, dimen_set: set[str], curd_set: set[str]
) -> OwnerDelta:
    new_ownerdelta = ownerdelta_shop()
    for x_owneratom in x_ownerdelta.get_sorted_owneratoms():
        if x_owneratom.crud_str in curd_set and x_owneratom.dimen in dimen_set:
            new_ownerdelta.set_owneratom(x_owneratom)
    return new_ownerdelta


def get_minimal_ownerdelta(x_ownerdelta: OwnerDelta, x_owner: OwnerUnit) -> OwnerDelta:
    """Creates new OwnerDelta with only OwnerAtoms that would actually change the OwnerUnit"""
    new_ownerdelta = ownerdelta_shop()
    for x_atom in x_ownerdelta.get_sorted_owneratoms():
        sifted_atom = sift_owneratom(x_owner, x_atom)
        if sifted_atom != None:
            new_ownerdelta.set_owneratom(sifted_atom)
    return new_ownerdelta


def get_ownerdelta_from_ordered_dict(x_dict: dict) -> OwnerDelta:
    x_ownerdelta = ownerdelta_shop()
    for x_atom_dict in x_dict.values():
        x_ownerdelta.set_owneratom(get_owneratom_from_dict(x_atom_dict))
    return x_ownerdelta
