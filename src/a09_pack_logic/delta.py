from src.a00_data_toolbox.dict_toolbox import (
    get_empty_dict_if_None,
    get_json_from_dict,
    set_in_nested_dict,
    get_from_nested_dict,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from src.a01_way_logic.way import WayStr, LabelStr
from src.a04_reason_logic.reason_idea import FactUnit, ReasonUnit
from src.a03_group_logic.acct import MemberShip, AcctName, AcctUnit
from src.a03_group_logic.group import MemberShip
from src.a05_idea_logic.idea import IdeaUnit
from src.a06_bud_logic.bud import BudUnit, budunit_shop
from src.a08_bud_atom_logic._utils.str_a08 import CRUD_command
from src.a08_bud_atom_logic.atom import (
    BudAtom,
    budatom_shop,
    modify_bud_with_budatom,
    InvalidBudAtomException,
    atom_delete,
    atom_insert,
    atom_update,
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
            if x_list[0].jkeys.get("idea_way") is not None:
                x_list = sorted(x_list, key=lambda x: x.jkeys.get("idea_way"))
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
        before_bud = budunit_shop(after_bud.owner_name, after_bud.fisc_tag)
        self.add_all_different_budatoms(before_bud, after_bud)

    def add_all_different_budatoms(self, before_bud: BudUnit, after_bud: BudUnit):
        before_bud.settle_bud()
        after_bud.settle_bud()
        self.add_budatoms_budunit_simple_attrs(before_bud, after_bud)
        self.add_budatoms_accts(before_bud, after_bud)
        self.add_budatoms_ideas(before_bud, after_bud)

    def add_budatoms_budunit_simple_attrs(
        self, before_bud: BudUnit, after_bud: BudUnit
    ):
        if not jvalues_different("budunit", before_bud, after_bud):
            return
        x_budatom = budatom_shop("budunit", atom_update())
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
            x_budatom = budatom_shop("bud_acctunit", atom_insert())
            x_budatom.set_jkey("acct_name", insert_acctunit.acct_name)
            if insert_acctunit.credit_belief is not None:
                x_budatom.set_jvalue("credit_belief", insert_acctunit.credit_belief)
            if insert_acctunit.debtit_belief is not None:
                x_budatom.set_jvalue("debtit_belief", insert_acctunit.debtit_belief)
            self.set_budatom(x_budatom)
            all_group_labels = set(insert_acctunit._memberships.keys())
            self.add_budatom_memberships_inserts(
                after_acctunit=insert_acctunit,
                insert_membership_group_labels=all_group_labels,
            )

    def add_budatom_acctunit_updates(
        self, before_bud: BudUnit, after_bud: BudUnit, update_acct_names: set
    ):
        for acct_name in update_acct_names:
            after_acctunit = after_bud.get_acct(acct_name)
            before_acctunit = before_bud.get_acct(acct_name)
            if jvalues_different("bud_acctunit", after_acctunit, before_acctunit):
                x_budatom = budatom_shop("bud_acctunit", atom_update())
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
            x_budatom = budatom_shop("bud_acctunit", atom_delete())
            x_budatom.set_jkey("acct_name", delete_acct_name)
            self.set_budatom(x_budatom)
            delete_acctunit = before_bud.get_acct(delete_acct_name)
            non_mirror_group_labels = {
                x_group_label
                for x_group_label in delete_acctunit._memberships.keys()
                if x_group_label != delete_acct_name
            }
            self.add_budatom_memberships_delete(
                delete_acct_name, non_mirror_group_labels
            )

    def add_budatom_acctunit_update_memberships(
        self, after_acctunit: AcctUnit, before_acctunit: AcctUnit
    ):
        # before_non_mirror_group_labels
        before_group_labels = {
            x_group_label
            for x_group_label in before_acctunit._memberships.keys()
            if x_group_label != before_acctunit.acct_name
        }
        # after_non_mirror_group_labels
        after_group_labels = {
            x_group_label
            for x_group_label in after_acctunit._memberships.keys()
            if x_group_label != after_acctunit.acct_name
        }

        self.add_budatom_memberships_inserts(
            after_acctunit=after_acctunit,
            insert_membership_group_labels=after_group_labels.difference(
                before_group_labels
            ),
        )

        self.add_budatom_memberships_delete(
            before_acct_name=after_acctunit.acct_name,
            before_group_labels=before_group_labels.difference(after_group_labels),
        )

        update_group_labels = before_group_labels.intersection(after_group_labels)
        for update_acct_name in update_group_labels:
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
        insert_membership_group_labels: list[LabelStr],
    ):
        after_acct_name = after_acctunit.acct_name
        for insert_group_label in insert_membership_group_labels:
            after_membership = after_acctunit.get_membership(insert_group_label)
            x_budatom = budatom_shop("bud_acct_membership", atom_insert())
            x_budatom.set_jkey("acct_name", after_acct_name)
            x_budatom.set_jkey("group_label", after_membership.group_label)
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
        x_budatom = budatom_shop("bud_acct_membership", atom_update())
        x_budatom.set_jkey("acct_name", acct_name)
        x_budatom.set_jkey("group_label", after_membership.group_label)
        if after_membership.credit_vote != before_membership.credit_vote:
            x_budatom.set_jvalue("credit_vote", after_membership.credit_vote)
        if after_membership.debtit_vote != before_membership.debtit_vote:
            x_budatom.set_jvalue("debtit_vote", after_membership.debtit_vote)
        self.set_budatom(x_budatom)

    def add_budatom_memberships_delete(
        self, before_acct_name: AcctName, before_group_labels: LabelStr
    ):
        for delete_group_label in before_group_labels:
            x_budatom = budatom_shop("bud_acct_membership", atom_delete())
            x_budatom.set_jkey("acct_name", before_acct_name)
            x_budatom.set_jkey("group_label", delete_group_label)
            self.set_budatom(x_budatom)

    def add_budatoms_ideas(self, before_bud: BudUnit, after_bud: BudUnit):
        before_idea_ways = set(before_bud._idea_dict.keys())
        after_idea_ways = set(after_bud._idea_dict.keys())

        self.add_budatom_idea_inserts(
            after_bud=after_bud,
            insert_idea_ways=after_idea_ways.difference(before_idea_ways),
        )
        self.add_budatom_idea_deletes(
            before_bud=before_bud,
            delete_idea_ways=before_idea_ways.difference(after_idea_ways),
        )
        self.add_budatom_idea_updates(
            before_bud=before_bud,
            after_bud=after_bud,
            update_ways=before_idea_ways.intersection(after_idea_ways),
        )

    def add_budatom_idea_inserts(self, after_bud: BudUnit, insert_idea_ways: set):
        for insert_idea_way in insert_idea_ways:
            insert_ideaunit = after_bud.get_idea_obj(insert_idea_way)
            x_budatom = budatom_shop("bud_ideaunit", atom_insert())
            x_budatom.set_jkey("idea_way", insert_ideaunit.get_idea_way())
            x_budatom.set_jvalue("addin", insert_ideaunit.addin)
            x_budatom.set_jvalue("begin", insert_ideaunit.begin)
            x_budatom.set_jvalue("close", insert_ideaunit.close)
            x_budatom.set_jvalue("denom", insert_ideaunit.denom)
            x_budatom.set_jvalue("numor", insert_ideaunit.numor)
            x_budatom.set_jvalue("morph", insert_ideaunit.morph)
            x_budatom.set_jvalue("mass", insert_ideaunit.mass)
            x_budatom.set_jvalue("pledge", insert_ideaunit.pledge)
            self.set_budatom(x_budatom)

            self.add_budatom_idea_factunit_inserts(
                ideaunit=insert_ideaunit,
                insert_factunit_rcontexts=set(insert_ideaunit.factunits.keys()),
            )
            self.add_budatom_idea_awardlink_inserts(
                after_ideaunit=insert_ideaunit,
                insert_awardlink_awardee_labels=set(insert_ideaunit.awardlinks.keys()),
            )
            self.add_budatom_idea_reasonunit_inserts(
                after_ideaunit=insert_ideaunit,
                insert_reasonunit_rcontexts=set(insert_ideaunit.reasonunits.keys()),
            )
            self.add_budatom_idea_teamlink_insert(
                idea_way=insert_idea_way,
                insert_teamlink_team_labels=insert_ideaunit.teamunit._teamlinks,
            )
            self.add_budatom_idea_healerlink_insert(
                idea_way=insert_idea_way,
                insert_healerlink_healer_names=insert_ideaunit.healerlink._healer_names,
            )

    def add_budatom_idea_updates(
        self, before_bud: BudUnit, after_bud: BudUnit, update_ways: set
    ):
        for idea_way in update_ways:
            after_ideaunit = after_bud.get_idea_obj(idea_way)
            before_ideaunit = before_bud.get_idea_obj(idea_way)
            if jvalues_different("bud_ideaunit", before_ideaunit, after_ideaunit):
                x_budatom = budatom_shop("bud_ideaunit", atom_update())
                x_budatom.set_jkey("idea_way", after_ideaunit.get_idea_way())
                if before_ideaunit.addin != after_ideaunit.addin:
                    x_budatom.set_jvalue("addin", after_ideaunit.addin)
                if before_ideaunit.begin != after_ideaunit.begin:
                    x_budatom.set_jvalue("begin", after_ideaunit.begin)
                if before_ideaunit.close != after_ideaunit.close:
                    x_budatom.set_jvalue("close", after_ideaunit.close)
                if before_ideaunit.denom != after_ideaunit.denom:
                    x_budatom.set_jvalue("denom", after_ideaunit.denom)
                if before_ideaunit.numor != after_ideaunit.numor:
                    x_budatom.set_jvalue("numor", after_ideaunit.numor)
                if before_ideaunit.morph != after_ideaunit.morph:
                    x_budatom.set_jvalue("morph", after_ideaunit.morph)
                if before_ideaunit.mass != after_ideaunit.mass:
                    x_budatom.set_jvalue("mass", after_ideaunit.mass)
                if before_ideaunit.pledge != after_ideaunit.pledge:
                    x_budatom.set_jvalue("pledge", after_ideaunit.pledge)
                self.set_budatom(x_budatom)

            # insert / update / delete factunits
            before_factunit_rcontexts = set(before_ideaunit.factunits.keys())
            after_factunit_rcontexts = set(after_ideaunit.factunits.keys())
            self.add_budatom_idea_factunit_inserts(
                ideaunit=after_ideaunit,
                insert_factunit_rcontexts=after_factunit_rcontexts.difference(
                    before_factunit_rcontexts
                ),
            )
            self.add_budatom_idea_factunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_factunit_rcontexts=before_factunit_rcontexts.intersection(
                    after_factunit_rcontexts
                ),
            )
            self.add_budatom_idea_factunit_deletes(
                idea_way=idea_way,
                delete_factunit_rcontexts=before_factunit_rcontexts.difference(
                    after_factunit_rcontexts
                ),
            )

            # insert / update / delete awardunits
            before_awardlinks_awardee_labels = set(before_ideaunit.awardlinks.keys())
            after_awardlinks_awardee_labels = set(after_ideaunit.awardlinks.keys())
            self.add_budatom_idea_awardlink_inserts(
                after_ideaunit=after_ideaunit,
                insert_awardlink_awardee_labels=after_awardlinks_awardee_labels.difference(
                    before_awardlinks_awardee_labels
                ),
            )
            self.add_budatom_idea_awardlink_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_awardlink_awardee_labels=before_awardlinks_awardee_labels.intersection(
                    after_awardlinks_awardee_labels
                ),
            )
            self.add_budatom_idea_awardlink_deletes(
                idea_way=idea_way,
                delete_awardlink_awardee_labels=before_awardlinks_awardee_labels.difference(
                    after_awardlinks_awardee_labels
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_rcontexts = set(before_ideaunit.reasonunits.keys())
            after_reasonunit_rcontexts = set(after_ideaunit.reasonunits.keys())
            self.add_budatom_idea_reasonunit_inserts(
                after_ideaunit=after_ideaunit,
                insert_reasonunit_rcontexts=after_reasonunit_rcontexts.difference(
                    before_reasonunit_rcontexts
                ),
            )
            self.add_budatom_idea_reasonunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_reasonunit_rcontexts=before_reasonunit_rcontexts.intersection(
                    after_reasonunit_rcontexts
                ),
            )
            self.add_budatom_idea_reasonunit_deletes(
                before_ideaunit=before_ideaunit,
                delete_reasonunit_rcontexts=before_reasonunit_rcontexts.difference(
                    after_reasonunit_rcontexts
                ),
            )
            # insert / update / delete reasonunits_permises
            # update reasonunits_permises insert_premise
            # update reasonunits_permises update_premise
            # update reasonunits_permises delete_premise

            # insert / update / delete teamlinks
            before_teamlinks_team_labels = set(before_ideaunit.teamunit._teamlinks)
            after_teamlinks_team_labels = set(after_ideaunit.teamunit._teamlinks)
            self.add_budatom_idea_teamlink_insert(
                idea_way=idea_way,
                insert_teamlink_team_labels=after_teamlinks_team_labels.difference(
                    before_teamlinks_team_labels
                ),
            )
            self.add_budatom_idea_teamlink_deletes(
                idea_way=idea_way,
                delete_teamlink_team_labels=before_teamlinks_team_labels.difference(
                    after_teamlinks_team_labels
                ),
            )

            # insert / update / delete healerlinks
            before_healerlinks_healer_names = set(
                before_ideaunit.healerlink._healer_names
            )
            after_healerlinks_healer_names = set(
                after_ideaunit.healerlink._healer_names
            )
            self.add_budatom_idea_healerlink_insert(
                idea_way=idea_way,
                insert_healerlink_healer_names=after_healerlinks_healer_names.difference(
                    before_healerlinks_healer_names
                ),
            )
            self.add_budatom_idea_healerlink_deletes(
                idea_way=idea_way,
                delete_healerlink_healer_names=before_healerlinks_healer_names.difference(
                    after_healerlinks_healer_names
                ),
            )

    def add_budatom_idea_deletes(self, before_bud: BudUnit, delete_idea_ways: set):
        for delete_idea_way in delete_idea_ways:
            x_budatom = budatom_shop("bud_ideaunit", atom_delete())
            x_budatom.set_jkey("idea_way", delete_idea_way)
            self.set_budatom(x_budatom)

            delete_ideaunit = before_bud.get_idea_obj(delete_idea_way)
            self.add_budatom_idea_factunit_deletes(
                idea_way=delete_idea_way,
                delete_factunit_rcontexts=set(delete_ideaunit.factunits.keys()),
            )

            self.add_budatom_idea_awardlink_deletes(
                idea_way=delete_idea_way,
                delete_awardlink_awardee_labels=set(delete_ideaunit.awardlinks.keys()),
            )
            self.add_budatom_idea_reasonunit_deletes(
                before_ideaunit=delete_ideaunit,
                delete_reasonunit_rcontexts=set(delete_ideaunit.reasonunits.keys()),
            )
            self.add_budatom_idea_teamlink_deletes(
                idea_way=delete_idea_way,
                delete_teamlink_team_labels=delete_ideaunit.teamunit._teamlinks,
            )
            self.add_budatom_idea_healerlink_deletes(
                idea_way=delete_idea_way,
                delete_healerlink_healer_names=delete_ideaunit.healerlink._healer_names,
            )

    def add_budatom_idea_reasonunit_inserts(
        self, after_ideaunit: IdeaUnit, insert_reasonunit_rcontexts: set
    ):
        for insert_reasonunit_rcontext in insert_reasonunit_rcontexts:
            after_reasonunit = after_ideaunit.get_reasonunit(insert_reasonunit_rcontext)
            x_budatom = budatom_shop("bud_idea_reasonunit", atom_insert())
            x_budatom.set_jkey("idea_way", after_ideaunit.get_idea_way())
            x_budatom.set_jkey("rcontext", after_reasonunit.rcontext)
            if after_reasonunit.rcontext_idea_active_requisite is not None:
                x_budatom.set_jvalue(
                    "rcontext_idea_active_requisite",
                    after_reasonunit.rcontext_idea_active_requisite,
                )
            self.set_budatom(x_budatom)

            self.add_budatom_idea_reason_premiseunit_inserts(
                idea_way=after_ideaunit.get_idea_way(),
                after_reasonunit=after_reasonunit,
                insert_premise_pbranchs=set(after_reasonunit.premises.keys()),
            )

    def add_budatom_idea_reasonunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_reasonunit_rcontexts: set,
    ):
        for update_reasonunit_rcontext in update_reasonunit_rcontexts:
            before_reasonunit = before_ideaunit.get_reasonunit(
                update_reasonunit_rcontext
            )
            after_reasonunit = after_ideaunit.get_reasonunit(update_reasonunit_rcontext)
            if jvalues_different(
                "bud_idea_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_budatom = budatom_shop("bud_idea_reasonunit", atom_update())
                x_budatom.set_jkey("idea_way", before_ideaunit.get_idea_way())
                x_budatom.set_jkey("rcontext", after_reasonunit.rcontext)
                if (
                    before_reasonunit.rcontext_idea_active_requisite
                    != after_reasonunit.rcontext_idea_active_requisite
                ):
                    x_budatom.set_jvalue(
                        "rcontext_idea_active_requisite",
                        after_reasonunit.rcontext_idea_active_requisite,
                    )
                self.set_budatom(x_budatom)

            before_premise_pbranchs = set(before_reasonunit.premises.keys())
            after_premise_pbranchs = set(after_reasonunit.premises.keys())
            self.add_budatom_idea_reason_premiseunit_inserts(
                idea_way=before_ideaunit.get_idea_way(),
                after_reasonunit=after_reasonunit,
                insert_premise_pbranchs=after_premise_pbranchs.difference(
                    before_premise_pbranchs
                ),
            )
            self.add_budatom_idea_reason_premiseunit_updates(
                idea_way=before_ideaunit.get_idea_way(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_pbranchs=after_premise_pbranchs.intersection(
                    before_premise_pbranchs
                ),
            )
            self.add_budatom_idea_reason_premiseunit_deletes(
                idea_way=before_ideaunit.get_idea_way(),
                reasonunit_rcontext=update_reasonunit_rcontext,
                delete_premise_pbranchs=before_premise_pbranchs.difference(
                    after_premise_pbranchs
                ),
            )

    def add_budatom_idea_reasonunit_deletes(
        self, before_ideaunit: IdeaUnit, delete_reasonunit_rcontexts: set
    ):
        for delete_reasonunit_rcontext in delete_reasonunit_rcontexts:
            x_budatom = budatom_shop("bud_idea_reasonunit", atom_delete())
            x_budatom.set_jkey("idea_way", before_ideaunit.get_idea_way())
            x_budatom.set_jkey("rcontext", delete_reasonunit_rcontext)
            self.set_budatom(x_budatom)

            before_reasonunit = before_ideaunit.get_reasonunit(
                delete_reasonunit_rcontext
            )
            self.add_budatom_idea_reason_premiseunit_deletes(
                idea_way=before_ideaunit.get_idea_way(),
                reasonunit_rcontext=delete_reasonunit_rcontext,
                delete_premise_pbranchs=set(before_reasonunit.premises.keys()),
            )

    def add_budatom_idea_reason_premiseunit_inserts(
        self,
        idea_way: WayStr,
        after_reasonunit: ReasonUnit,
        insert_premise_pbranchs: set,
    ):
        for insert_premise_pbranch in insert_premise_pbranchs:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_pbranch)
            x_budatom = budatom_shop("bud_idea_reason_premiseunit", atom_insert())
            x_budatom.set_jkey("idea_way", idea_way)
            x_budatom.set_jkey("rcontext", after_reasonunit.rcontext)
            x_budatom.set_jkey("pbranch", after_premiseunit.pbranch)
            if after_premiseunit.open is not None:
                x_budatom.set_jvalue("open", after_premiseunit.open)
            if after_premiseunit.pnigh is not None:
                x_budatom.set_jvalue("pnigh", after_premiseunit.pnigh)
            if after_premiseunit.pdivisor is not None:
                x_budatom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
            self.set_budatom(x_budatom)

    def add_budatom_idea_reason_premiseunit_updates(
        self,
        idea_way: WayStr,
        before_reasonunit: ReasonUnit,
        after_reasonunit: ReasonUnit,
        update_premise_pbranchs: set,
    ):
        for update_premise_pbranch in update_premise_pbranchs:
            before_premiseunit = before_reasonunit.get_premise(update_premise_pbranch)
            after_premiseunit = after_reasonunit.get_premise(update_premise_pbranch)
            if jvalues_different(
                "bud_idea_reason_premiseunit",
                before_premiseunit,
                after_premiseunit,
            ):
                x_budatom = budatom_shop("bud_idea_reason_premiseunit", atom_update())
                x_budatom.set_jkey("idea_way", idea_way)
                x_budatom.set_jkey("rcontext", before_reasonunit.rcontext)
                x_budatom.set_jkey("pbranch", after_premiseunit.pbranch)
                if after_premiseunit.open != before_premiseunit.open:
                    x_budatom.set_jvalue("open", after_premiseunit.open)
                if after_premiseunit.pnigh != before_premiseunit.pnigh:
                    x_budatom.set_jvalue("pnigh", after_premiseunit.pnigh)
                if after_premiseunit.pdivisor != before_premiseunit.pdivisor:
                    x_budatom.set_jvalue("pdivisor", after_premiseunit.pdivisor)
                self.set_budatom(x_budatom)

    def add_budatom_idea_reason_premiseunit_deletes(
        self,
        idea_way: WayStr,
        reasonunit_rcontext: WayStr,
        delete_premise_pbranchs: set,
    ):
        for delete_premise_pbranch in delete_premise_pbranchs:
            x_budatom = budatom_shop("bud_idea_reason_premiseunit", atom_delete())
            x_budatom.set_jkey("idea_way", idea_way)
            x_budatom.set_jkey("rcontext", reasonunit_rcontext)
            x_budatom.set_jkey("pbranch", delete_premise_pbranch)
            self.set_budatom(x_budatom)

    def add_budatom_idea_teamlink_insert(
        self, idea_way: WayStr, insert_teamlink_team_labels: set
    ):
        for insert_teamlink_team_label in insert_teamlink_team_labels:
            x_budatom = budatom_shop("bud_idea_teamlink", atom_insert())
            x_budatom.set_jkey("idea_way", idea_way)
            x_budatom.set_jkey("team_label", insert_teamlink_team_label)
            self.set_budatom(x_budatom)

    def add_budatom_idea_teamlink_deletes(
        self, idea_way: WayStr, delete_teamlink_team_labels: set
    ):
        for delete_teamlink_team_label in delete_teamlink_team_labels:
            x_budatom = budatom_shop("bud_idea_teamlink", atom_delete())
            x_budatom.set_jkey("idea_way", idea_way)
            x_budatom.set_jkey("team_label", delete_teamlink_team_label)
            self.set_budatom(x_budatom)

    def add_budatom_idea_healerlink_insert(
        self, idea_way: WayStr, insert_healerlink_healer_names: set
    ):
        for insert_healerlink_healer_name in insert_healerlink_healer_names:
            x_budatom = budatom_shop("bud_idea_healerlink", atom_insert())
            x_budatom.set_jkey("idea_way", idea_way)
            x_budatom.set_jkey("healer_name", insert_healerlink_healer_name)
            self.set_budatom(x_budatom)

    def add_budatom_idea_healerlink_deletes(
        self, idea_way: WayStr, delete_healerlink_healer_names: set
    ):
        for delete_healerlink_healer_name in delete_healerlink_healer_names:
            x_budatom = budatom_shop("bud_idea_healerlink", atom_delete())
            x_budatom.set_jkey("idea_way", idea_way)
            x_budatom.set_jkey("healer_name", delete_healerlink_healer_name)
            self.set_budatom(x_budatom)

    def add_budatom_idea_awardlink_inserts(
        self, after_ideaunit: IdeaUnit, insert_awardlink_awardee_labels: set
    ):
        for after_awardlink_awardee_label in insert_awardlink_awardee_labels:
            after_awardlink = after_ideaunit.awardlinks.get(
                after_awardlink_awardee_label
            )
            x_budatom = budatom_shop("bud_idea_awardlink", atom_insert())
            x_budatom.set_jkey("idea_way", after_ideaunit.get_idea_way())
            x_budatom.set_jkey("awardee_label", after_awardlink.awardee_label)
            x_budatom.set_jvalue("give_force", after_awardlink.give_force)
            x_budatom.set_jvalue("take_force", after_awardlink.take_force)
            self.set_budatom(x_budatom)

    def add_budatom_idea_awardlink_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_awardlink_awardee_labels: set,
    ):
        for update_awardlink_awardee_label in update_awardlink_awardee_labels:
            before_awardlink = before_ideaunit.awardlinks.get(
                update_awardlink_awardee_label
            )
            after_awardlink = after_ideaunit.awardlinks.get(
                update_awardlink_awardee_label
            )
            if jvalues_different(
                "bud_idea_awardlink", before_awardlink, after_awardlink
            ):
                x_budatom = budatom_shop("bud_idea_awardlink", atom_update())
                x_budatom.set_jkey("idea_way", before_ideaunit.get_idea_way())
                x_budatom.set_jkey("awardee_label", after_awardlink.awardee_label)
                if before_awardlink.give_force != after_awardlink.give_force:
                    x_budatom.set_jvalue("give_force", after_awardlink.give_force)
                if before_awardlink.take_force != after_awardlink.take_force:
                    x_budatom.set_jvalue("take_force", after_awardlink.take_force)
                self.set_budatom(x_budatom)

    def add_budatom_idea_awardlink_deletes(
        self, idea_way: WayStr, delete_awardlink_awardee_labels: set
    ):
        for delete_awardlink_awardee_label in delete_awardlink_awardee_labels:
            x_budatom = budatom_shop("bud_idea_awardlink", atom_delete())
            x_budatom.set_jkey("idea_way", idea_way)
            x_budatom.set_jkey("awardee_label", delete_awardlink_awardee_label)
            self.set_budatom(x_budatom)

    def add_budatom_idea_factunit_inserts(
        self, ideaunit: IdeaUnit, insert_factunit_rcontexts: set
    ):
        for insert_factunit_rcontext in insert_factunit_rcontexts:
            insert_factunit = ideaunit.factunits.get(insert_factunit_rcontext)
            x_budatom = budatom_shop("bud_idea_factunit", atom_insert())
            x_budatom.set_jkey("idea_way", ideaunit.get_idea_way())
            x_budatom.set_jkey("fcontext", insert_factunit.fcontext)
            if insert_factunit.fbranch is not None:
                x_budatom.set_jvalue("fbranch", insert_factunit.fbranch)
            if insert_factunit.fopen is not None:
                x_budatom.set_jvalue("fopen", insert_factunit.fopen)
            if insert_factunit.fnigh is not None:
                x_budatom.set_jvalue("fnigh", insert_factunit.fnigh)
            self.set_budatom(x_budatom)

    def add_budatom_idea_factunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_factunit_rcontexts: set,
    ):
        for update_factunit_rcontext in update_factunit_rcontexts:
            before_factunit = before_ideaunit.factunits.get(update_factunit_rcontext)
            after_factunit = after_ideaunit.factunits.get(update_factunit_rcontext)
            if jvalues_different("bud_idea_factunit", before_factunit, after_factunit):
                x_budatom = budatom_shop("bud_idea_factunit", atom_update())
                x_budatom.set_jkey("idea_way", before_ideaunit.get_idea_way())
                x_budatom.set_jkey("fcontext", after_factunit.fcontext)
                if before_factunit.fbranch != after_factunit.fbranch:
                    x_budatom.set_jvalue("fbranch", after_factunit.fbranch)
                if before_factunit.fopen != after_factunit.fopen:
                    x_budatom.set_jvalue("fopen", after_factunit.fopen)
                if before_factunit.fnigh != after_factunit.fnigh:
                    x_budatom.set_jvalue("fnigh", after_factunit.fnigh)
                self.set_budatom(x_budatom)

    def add_budatom_idea_factunit_deletes(
        self, idea_way: WayStr, delete_factunit_rcontexts: FactUnit
    ):
        for delete_factunit_rcontext in delete_factunit_rcontexts:
            x_budatom = budatom_shop("bud_idea_factunit", atom_delete())
            x_budatom.set_jkey("idea_way", idea_way)
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
