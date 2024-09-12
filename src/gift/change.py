from src._instrument.python_tool import (
    get_empty_dict_if_none,
    get_json_from_dict,
    place_obj_in_dict,
    get_nested_value,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src.bud.reason_idea import FactUnit, ReasonUnit
from src.bud.acct import MemberShip, AcctID, AcctUnit
from src.bud.group import MemberShip, GroupID
from src.bud.idea import IdeaUnit
from src.bud.bud import BudUnit, budunit_shop
from src.bud.bud_tool import (
    bud_attr_exists,
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
    bud_get_obj,
)
from src.gift.atom_config import (
    CRUD_command,
    acct_id_str,
    group_id_str,
    healer_id_str,
    parent_road_str,
    label_str,
    road_str,
    base_str,
    pledge_str,
    addin_str,
    begin_str,
    close_str,
    denom_str,
    numor_str,
    morph_str,
    mass_str,
    credit_vote_str,
    debtit_vote_str,
    fopen_str,
    fnigh_str,
    base_idea_active_requisite_str,
    get_atom_config_required_args,
    get_atom_config_optional_args,
)
from src.gift.atom import (
    AtomUnit,
    atomunit_shop,
    modify_bud_with_atomunit,
    InvalidAtomUnitException,
    atom_delete,
    atom_insert,
    atom_update,
    optional_args_different,
    sift_atomunit,
)
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class ChangeUnit:
    atomunits: dict[CRUD_command : dict[str, AtomUnit]] = None
    _bud_build_validated: bool = None

    def _get_crud_atomunits_list(self) -> dict[CRUD_command, list[AtomUnit]]:
        return get_all_nondictionary_objs(self.atomunits)

    def get_category_sorted_atomunits_list(self) -> list[AtomUnit]:
        atoms_list = []
        for crud_list in self._get_crud_atomunits_list().values():
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
            if x_list[0].required_args.get(parent_road_str()) is not None:
                x_list = sorted(
                    x_list, key=lambda x: x.required_args.get(parent_road_str())
                )
            if x_list[0].required_args.get(road_str()) is not None:
                x_list = sorted(x_list, key=lambda x: x.required_args.get(road_str()))
            ordered_list.extend(x_list)
        return ordered_list

    def get_sorted_atomunits(self) -> list[AtomUnit]:
        atomunits_list = self.get_category_sorted_atomunits_list()
        return sorted(atomunits_list, key=lambda x: x.atom_order)

    def get_edited_bud(self, before_bud: BudUnit):
        edited_bud = copy_deepcopy(before_bud)
        for x_atomunit in self.get_sorted_atomunits():
            modify_bud_with_atomunit(edited_bud, x_atomunit)
        return edited_bud

    def set_atomunit(self, x_atomunit: AtomUnit):
        if x_atomunit.is_valid() is False:
            raise InvalidAtomUnitException(
                f"""'{x_atomunit.category}' {x_atomunit.crud_str} AtomUnit is invalid
                {x_atomunit.is_required_args_valid()=}
                {x_atomunit.is_optional_args_valid()=}"""
            )

        x_atomunit.set_atom_order()
        x_keylist = [
            x_atomunit.crud_str,
            x_atomunit.category,
            *x_atomunit.get_nesting_order_args(),
        ]
        place_obj_in_dict(self.atomunits, x_keylist, x_atomunit)

    def atomunit_exists(self, x_atomunit: AtomUnit) -> bool:
        if x_atomunit.is_valid() is False:
            raise InvalidAtomUnitException(
                f"""'{x_atomunit.category}' {x_atomunit.crud_str} AtomUnit is invalid
                {x_atomunit.is_required_args_valid()=}
                {x_atomunit.is_optional_args_valid()=}"""
            )

        x_atomunit.set_atom_order()
        x_keylist = [
            x_atomunit.crud_str,
            x_atomunit.category,
            *list(x_atomunit.get_nesting_order_args()),
        ]
        nested_atomunit = get_nested_value(self.atomunits, x_keylist, True)
        return nested_atomunit == x_atomunit

    def add_atomunit(
        self,
        category: str,
        crud_str: str,
        required_args: str = None,
        optional_args: str = None,
    ):
        x_atomunit = atomunit_shop(
            category=category,
            crud_str=crud_str,
            required_args=required_args,
            optional_args=optional_args,
        )
        self.set_atomunit(x_atomunit)

    def get_atomunit(
        self, crud_str: str, category: str, required_args: list[str]
    ) -> AtomUnit:
        x_keylist = [crud_str, category, *required_args]
        return get_nested_value(self.atomunits, x_keylist)

    def add_all_atomunits(self, after_bud: BudUnit):
        before_bud = budunit_shop(after_bud._owner_id, after_bud._pecun_id)
        self.add_all_different_atomunits(before_bud, after_bud)

    def add_all_different_atomunits(self, before_bud: BudUnit, after_bud: BudUnit):
        before_bud.settle_bud()
        after_bud.settle_bud()
        self.add_atomunits_budunit_simple_attrs(before_bud, after_bud)
        self.add_atomunits_accts(before_bud, after_bud)
        self.add_atomunits_ideas(before_bud, after_bud)

    def add_atomunits_budunit_simple_attrs(
        self, before_bud: BudUnit, after_bud: BudUnit
    ):
        if not optional_args_different(budunit_str(), before_bud, after_bud):
            return
        x_atomunit = atomunit_shop(budunit_str(), atom_update())
        if before_bud._max_tree_traverse != after_bud._max_tree_traverse:
            x_atomunit.set_optional_arg(
                "max_tree_traverse", after_bud._max_tree_traverse
            )
        if before_bud._monetary_desc != after_bud._monetary_desc:
            x_atomunit.set_optional_arg("monetary_desc", after_bud._monetary_desc)
        if before_bud._credor_respect != after_bud._credor_respect:
            x_atomunit.set_optional_arg("credor_respect", after_bud._credor_respect)
        if before_bud._debtor_respect != after_bud._debtor_respect:
            x_atomunit.set_optional_arg("debtor_respect", after_bud._debtor_respect)
        if before_bud._tally != after_bud._tally:
            x_atomunit.set_optional_arg("tally", after_bud._tally)
        if before_bud._fund_pool != after_bud._fund_pool:
            x_atomunit.set_optional_arg("fund_pool", after_bud._fund_pool)
        if before_bud._fund_coin != after_bud._fund_coin:
            x_atomunit.set_optional_arg("fund_coin", after_bud._fund_coin)
        if before_bud._bit != after_bud._bit:
            x_atomunit.set_optional_arg("bit", after_bud._bit)
        self.set_atomunit(x_atomunit)

    def add_atomunits_accts(self, before_bud: BudUnit, after_bud: BudUnit):
        before_acct_ids = set(before_bud._accts.keys())
        after_acct_ids = set(after_bud._accts.keys())

        self.add_atomunit_acctunit_inserts(
            after_bud=after_bud,
            insert_acct_ids=after_acct_ids.difference(before_acct_ids),
        )
        self.add_atomunit_acctunit_deletes(
            before_bud=before_bud,
            delete_acct_ids=before_acct_ids.difference(after_acct_ids),
        )
        self.add_atomunit_acctunit_updates(
            before_bud=before_bud,
            after_bud=after_bud,
            update_acct_ids=before_acct_ids.intersection(after_acct_ids),
        )

    def add_atomunit_acctunit_inserts(self, after_bud: BudUnit, insert_acct_ids: set):
        for insert_acct_id in insert_acct_ids:
            insert_acctunit = after_bud.get_acct(insert_acct_id)
            x_atomunit = atomunit_shop(bud_acctunit_str(), atom_insert())
            x_atomunit.set_required_arg(acct_id_str(), insert_acctunit.acct_id)
            if insert_acctunit.credit_belief is not None:
                x_atomunit.set_optional_arg(
                    "credit_belief", insert_acctunit.credit_belief
                )
            if insert_acctunit.debtit_belief is not None:
                x_atomunit.set_optional_arg(
                    "debtit_belief", insert_acctunit.debtit_belief
                )
            self.set_atomunit(x_atomunit)
            all_group_ids = set(insert_acctunit._memberships.keys())
            self.add_atomunit_memberships_inserts(
                after_acctunit=insert_acctunit,
                insert_membership_group_ids=all_group_ids,
            )

    def add_atomunit_acctunit_updates(
        self, before_bud: BudUnit, after_bud: BudUnit, update_acct_ids: set
    ):
        for acct_id in update_acct_ids:
            after_acctunit = after_bud.get_acct(acct_id)
            before_acctunit = before_bud.get_acct(acct_id)
            if optional_args_different(
                bud_acctunit_str(), after_acctunit, before_acctunit
            ):
                x_atomunit = atomunit_shop(bud_acctunit_str(), atom_update())
                x_atomunit.set_required_arg(acct_id_str(), after_acctunit.acct_id)
                if before_acctunit.credit_belief != after_acctunit.credit_belief:
                    x_atomunit.set_optional_arg(
                        "credit_belief", after_acctunit.credit_belief
                    )
                if before_acctunit.debtit_belief != after_acctunit.debtit_belief:
                    x_atomunit.set_optional_arg(
                        "debtit_belief", after_acctunit.debtit_belief
                    )
                self.set_atomunit(x_atomunit)
            self.add_atomunit_acctunit_update_memberships(
                after_acctunit=after_acctunit, before_acctunit=before_acctunit
            )

    def add_atomunit_acctunit_deletes(self, before_bud: BudUnit, delete_acct_ids: set):
        for delete_acct_id in delete_acct_ids:
            x_atomunit = atomunit_shop(bud_acctunit_str(), atom_delete())
            x_atomunit.set_required_arg(acct_id_str(), delete_acct_id)
            self.set_atomunit(x_atomunit)
            delete_acctunit = before_bud.get_acct(delete_acct_id)
            non_mirror_group_ids = {
                x_group_id
                for x_group_id in delete_acctunit._memberships.keys()
                if x_group_id != delete_acct_id
            }
            self.add_atomunit_memberships_delete(delete_acct_id, non_mirror_group_ids)

    def add_atomunit_acctunit_update_memberships(
        self, after_acctunit: AcctUnit, before_acctunit: AcctUnit
    ):
        # before_non_mirror_group_ids
        before_group_ids = {
            x_group_id
            for x_group_id in before_acctunit._memberships.keys()
            if x_group_id != before_acctunit.acct_id
        }
        # after_non_mirror_group_ids
        after_group_ids = {
            x_group_id
            for x_group_id in after_acctunit._memberships.keys()
            if x_group_id != after_acctunit.acct_id
        }

        self.add_atomunit_memberships_inserts(
            after_acctunit=after_acctunit,
            insert_membership_group_ids=after_group_ids.difference(before_group_ids),
        )

        self.add_atomunit_memberships_delete(
            before_acct_id=after_acctunit.acct_id,
            before_group_ids=before_group_ids.difference(after_group_ids),
        )

        update_group_ids = before_group_ids.intersection(after_group_ids)
        for update_acct_id in update_group_ids:
            before_membership = before_acctunit.get_membership(update_acct_id)
            after_membership = after_acctunit.get_membership(update_acct_id)
            if optional_args_different(
                bud_acct_membership_str(), before_membership, after_membership
            ):
                self.add_atomunit_membership_update(
                    acct_id=after_acctunit.acct_id,
                    before_membership=before_membership,
                    after_membership=after_membership,
                )

    def add_atomunit_memberships_inserts(
        self,
        after_acctunit: AcctUnit,
        insert_membership_group_ids: list[GroupID],
    ):
        after_acct_id = after_acctunit.acct_id
        for insert_group_id in insert_membership_group_ids:
            after_membership = after_acctunit.get_membership(insert_group_id)
            x_atomunit = atomunit_shop(bud_acct_membership_str(), atom_insert())
            x_atomunit.set_required_arg(acct_id_str(), after_acct_id)
            x_atomunit.set_required_arg(group_id_str(), after_membership.group_id)
            if after_membership.credit_vote is not None:
                x_atomunit.set_optional_arg(
                    credit_vote_str(), after_membership.credit_vote
                )
            if after_membership.debtit_vote is not None:
                x_atomunit.set_optional_arg(
                    debtit_vote_str(), after_membership.debtit_vote
                )
            self.set_atomunit(x_atomunit)

    def add_atomunit_membership_update(
        self,
        acct_id: AcctID,
        before_membership: MemberShip,
        after_membership: MemberShip,
    ):
        x_atomunit = atomunit_shop(bud_acct_membership_str(), atom_update())
        x_atomunit.set_required_arg(acct_id_str(), acct_id)
        x_atomunit.set_required_arg(group_id_str(), after_membership.group_id)
        if after_membership.credit_vote != before_membership.credit_vote:
            x_atomunit.set_optional_arg(credit_vote_str(), after_membership.credit_vote)
        if after_membership.debtit_vote != before_membership.debtit_vote:
            x_atomunit.set_optional_arg(debtit_vote_str(), after_membership.debtit_vote)
        self.set_atomunit(x_atomunit)

    def add_atomunit_memberships_delete(
        self, before_acct_id: AcctID, before_group_ids: GroupID
    ):
        for delete_group_id in before_group_ids:
            x_atomunit = atomunit_shop(bud_acct_membership_str(), atom_delete())
            x_atomunit.set_required_arg(acct_id_str(), before_acct_id)
            x_atomunit.set_required_arg(group_id_str(), delete_group_id)
            self.set_atomunit(x_atomunit)

    def add_atomunits_ideas(self, before_bud: BudUnit, after_bud: BudUnit):
        before_idea_roads = set(before_bud._idea_dict.keys())
        after_idea_roads = set(after_bud._idea_dict.keys())

        self.add_atomunit_idea_inserts(
            after_bud=after_bud,
            insert_idea_roads=after_idea_roads.difference(before_idea_roads),
        )
        self.add_atomunit_idea_deletes(
            before_bud=before_bud,
            delete_idea_roads=before_idea_roads.difference(after_idea_roads),
        )
        self.add_atomunit_idea_updates(
            before_bud=before_bud,
            after_bud=after_bud,
            update_roads=before_idea_roads.intersection(after_idea_roads),
        )

    def add_atomunit_idea_inserts(self, after_bud: BudUnit, insert_idea_roads: set):
        for insert_idea_road in insert_idea_roads:
            insert_ideaunit = after_bud.get_idea_obj(insert_idea_road)
            x_atomunit = atomunit_shop(bud_ideaunit_str(), atom_insert())
            x_atomunit.set_required_arg(parent_road_str(), insert_ideaunit._parent_road)
            x_atomunit.set_required_arg(label_str(), insert_ideaunit._label)
            x_atomunit.set_optional_arg(addin_str(), insert_ideaunit.addin)
            x_atomunit.set_optional_arg(begin_str(), insert_ideaunit.begin)
            x_atomunit.set_optional_arg(close_str(), insert_ideaunit.close)
            x_atomunit.set_optional_arg(denom_str(), insert_ideaunit.denom)
            x_atomunit.set_optional_arg(numor_str(), insert_ideaunit.numor)
            x_atomunit.set_optional_arg(morph_str(), insert_ideaunit.morph)
            x_atomunit.set_optional_arg(mass_str(), insert_ideaunit.mass)
            x_atomunit.set_optional_arg(pledge_str(), insert_ideaunit.pledge)
            self.set_atomunit(x_atomunit)

            self.add_atomunit_idea_factunit_inserts(
                ideaunit=insert_ideaunit,
                insert_factunit_bases=set(insert_ideaunit.factunits.keys()),
            )
            self.add_atomunit_idea_awardlink_inserts(
                after_ideaunit=insert_ideaunit,
                insert_awardlink_group_ids=set(insert_ideaunit.awardlinks.keys()),
            )
            self.add_atomunit_idea_reasonunit_inserts(
                after_ideaunit=insert_ideaunit,
                insert_reasonunit_bases=set(insert_ideaunit.reasonunits.keys()),
            )
            self.add_atomunit_idea_teamlink_insert(
                idea_road=insert_idea_road,
                insert_teamlink_group_ids=insert_ideaunit.teamunit._teamlinks,
            )
            self.add_atomunit_idea_healerlink_insert(
                idea_road=insert_idea_road,
                insert_healerlink_healer_ids=insert_ideaunit.healerlink._healer_ids,
            )

    def add_atomunit_idea_updates(
        self, before_bud: BudUnit, after_bud: BudUnit, update_roads: set
    ):
        for idea_road in update_roads:
            after_ideaunit = after_bud.get_idea_obj(idea_road)
            before_ideaunit = before_bud.get_idea_obj(idea_road)
            if optional_args_different(
                bud_ideaunit_str(), before_ideaunit, after_ideaunit
            ):
                x_atomunit = atomunit_shop(bud_ideaunit_str(), atom_update())
                x_atomunit.set_required_arg(
                    parent_road_str(), after_ideaunit._parent_road
                )
                x_atomunit.set_required_arg(label_str(), after_ideaunit._label)
                if before_ideaunit.addin != after_ideaunit.addin:
                    x_atomunit.set_optional_arg(addin_str(), after_ideaunit.addin)
                if before_ideaunit.begin != after_ideaunit.begin:
                    x_atomunit.set_optional_arg(begin_str(), after_ideaunit.begin)
                if before_ideaunit.close != after_ideaunit.close:
                    x_atomunit.set_optional_arg(close_str(), after_ideaunit.close)
                if before_ideaunit.denom != after_ideaunit.denom:
                    x_atomunit.set_optional_arg(denom_str(), after_ideaunit.denom)
                if before_ideaunit.numor != after_ideaunit.numor:
                    x_atomunit.set_optional_arg(numor_str(), after_ideaunit.numor)
                if before_ideaunit.morph != after_ideaunit.morph:
                    x_atomunit.set_optional_arg(morph_str(), after_ideaunit.morph)
                if before_ideaunit.mass != after_ideaunit.mass:
                    x_atomunit.set_optional_arg(mass_str(), after_ideaunit.mass)
                if before_ideaunit.pledge != after_ideaunit.pledge:
                    x_atomunit.set_optional_arg(pledge_str(), after_ideaunit.pledge)
                self.set_atomunit(x_atomunit)

            # insert / update / delete factunits
            before_factunit_bases = set(before_ideaunit.factunits.keys())
            after_factunit_bases = set(after_ideaunit.factunits.keys())
            self.add_atomunit_idea_factunit_inserts(
                ideaunit=after_ideaunit,
                insert_factunit_bases=after_factunit_bases.difference(
                    before_factunit_bases
                ),
            )
            self.add_atomunit_idea_factunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_factunit_bases=before_factunit_bases.intersection(
                    after_factunit_bases
                ),
            )
            self.add_atomunit_idea_factunit_deletes(
                idea_road=idea_road,
                delete_factunit_bases=before_factunit_bases.difference(
                    after_factunit_bases
                ),
            )

            # insert / update / delete awardunits
            before_awardlinks_group_ids = set(before_ideaunit.awardlinks.keys())
            after_awardlinks_group_ids = set(after_ideaunit.awardlinks.keys())
            self.add_atomunit_idea_awardlink_inserts(
                after_ideaunit=after_ideaunit,
                insert_awardlink_group_ids=after_awardlinks_group_ids.difference(
                    before_awardlinks_group_ids
                ),
            )
            self.add_atomunit_idea_awardlink_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_awardlink_group_ids=before_awardlinks_group_ids.intersection(
                    after_awardlinks_group_ids
                ),
            )
            self.add_atomunit_idea_awardlink_deletes(
                idea_road=idea_road,
                delete_awardlink_group_ids=before_awardlinks_group_ids.difference(
                    after_awardlinks_group_ids
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_bases = set(before_ideaunit.reasonunits.keys())
            after_reasonunit_bases = set(after_ideaunit.reasonunits.keys())
            self.add_atomunit_idea_reasonunit_inserts(
                after_ideaunit=after_ideaunit,
                insert_reasonunit_bases=after_reasonunit_bases.difference(
                    before_reasonunit_bases
                ),
            )
            self.add_atomunit_idea_reasonunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_reasonunit_bases=before_reasonunit_bases.intersection(
                    after_reasonunit_bases
                ),
            )
            self.add_atomunit_idea_reasonunit_deletes(
                before_ideaunit=before_ideaunit,
                delete_reasonunit_bases=before_reasonunit_bases.difference(
                    after_reasonunit_bases
                ),
            )
            # insert / update / delete reasonunits_permises
            # update reasonunits_permises insert_premise
            # update reasonunits_permises update_premise
            # update reasonunits_permises delete_premise

            # insert / update / delete teamlinks
            before_teamlinks_group_ids = set(before_ideaunit.teamunit._teamlinks)
            after_teamlinks_group_ids = set(after_ideaunit.teamunit._teamlinks)
            self.add_atomunit_idea_teamlink_insert(
                idea_road=idea_road,
                insert_teamlink_group_ids=after_teamlinks_group_ids.difference(
                    before_teamlinks_group_ids
                ),
            )
            self.add_atomunit_idea_teamlink_deletes(
                idea_road=idea_road,
                delete_teamlink_group_ids=before_teamlinks_group_ids.difference(
                    after_teamlinks_group_ids
                ),
            )

            # insert / update / delete healerlinks
            before_healerlinks_healer_ids = set(before_ideaunit.healerlink._healer_ids)
            after_healerlinks_healer_ids = set(after_ideaunit.healerlink._healer_ids)
            self.add_atomunit_idea_healerlink_insert(
                idea_road=idea_road,
                insert_healerlink_healer_ids=after_healerlinks_healer_ids.difference(
                    before_healerlinks_healer_ids
                ),
            )
            self.add_atomunit_idea_healerlink_deletes(
                idea_road=idea_road,
                delete_healerlink_healer_ids=before_healerlinks_healer_ids.difference(
                    after_healerlinks_healer_ids
                ),
            )

    def add_atomunit_idea_deletes(self, before_bud: BudUnit, delete_idea_roads: set):
        for delete_idea_road in delete_idea_roads:
            x_parent_road = get_parent_road(
                delete_idea_road, before_bud._road_delimiter
            )
            x_label = get_terminus_node(delete_idea_road, before_bud._road_delimiter)
            x_atomunit = atomunit_shop(bud_ideaunit_str(), atom_delete())
            x_atomunit.set_required_arg(parent_road_str(), x_parent_road)
            x_atomunit.set_required_arg(label_str(), x_label)
            self.set_atomunit(x_atomunit)

            delete_ideaunit = before_bud.get_idea_obj(delete_idea_road)
            self.add_atomunit_idea_factunit_deletes(
                idea_road=delete_idea_road,
                delete_factunit_bases=set(delete_ideaunit.factunits.keys()),
            )

            self.add_atomunit_idea_awardlink_deletes(
                idea_road=delete_idea_road,
                delete_awardlink_group_ids=set(delete_ideaunit.awardlinks.keys()),
            )
            self.add_atomunit_idea_reasonunit_deletes(
                before_ideaunit=delete_ideaunit,
                delete_reasonunit_bases=set(delete_ideaunit.reasonunits.keys()),
            )
            self.add_atomunit_idea_teamlink_deletes(
                idea_road=delete_idea_road,
                delete_teamlink_group_ids=delete_ideaunit.teamunit._teamlinks,
            )
            self.add_atomunit_idea_healerlink_deletes(
                idea_road=delete_idea_road,
                delete_healerlink_healer_ids=delete_ideaunit.healerlink._healer_ids,
            )

    def add_atomunit_idea_reasonunit_inserts(
        self, after_ideaunit: IdeaUnit, insert_reasonunit_bases: set
    ):
        for insert_reasonunit_base in insert_reasonunit_bases:
            after_reasonunit = after_ideaunit.get_reasonunit(insert_reasonunit_base)
            x_atomunit = atomunit_shop(bud_idea_reasonunit_str(), atom_insert())
            x_atomunit.set_required_arg(road_str(), after_ideaunit.get_road())
            x_atomunit.set_required_arg("base", after_reasonunit.base)
            if after_reasonunit.base_idea_active_requisite is not None:
                x_atomunit.set_optional_arg(
                    base_idea_active_requisite_str(),
                    after_reasonunit.base_idea_active_requisite,
                )
            self.set_atomunit(x_atomunit)

            self.add_atomunit_idea_reason_premiseunit_inserts(
                idea_road=after_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=set(after_reasonunit.premises.keys()),
            )

    def add_atomunit_idea_reasonunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_reasonunit_bases: set,
    ):
        for update_reasonunit_base in update_reasonunit_bases:
            before_reasonunit = before_ideaunit.get_reasonunit(update_reasonunit_base)
            after_reasonunit = after_ideaunit.get_reasonunit(update_reasonunit_base)
            if optional_args_different(
                bud_idea_reasonunit_str(), before_reasonunit, after_reasonunit
            ):
                x_atomunit = atomunit_shop(bud_idea_reasonunit_str(), atom_update())
                x_atomunit.set_required_arg(road_str(), before_ideaunit.get_road())
                x_atomunit.set_required_arg("base", after_reasonunit.base)
                if (
                    before_reasonunit.base_idea_active_requisite
                    != after_reasonunit.base_idea_active_requisite
                ):
                    x_atomunit.set_optional_arg(
                        base_idea_active_requisite_str(),
                        after_reasonunit.base_idea_active_requisite,
                    )
                self.set_atomunit(x_atomunit)

            before_premise_needs = set(before_reasonunit.premises.keys())
            after_premise_needs = set(after_reasonunit.premises.keys())
            self.add_atomunit_idea_reason_premiseunit_inserts(
                idea_road=before_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=after_premise_needs.difference(
                    before_premise_needs
                ),
            )
            self.add_atomunit_idea_reason_premiseunit_updates(
                idea_road=before_ideaunit.get_road(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_needs=after_premise_needs.intersection(
                    before_premise_needs
                ),
            )
            self.add_atomunit_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=update_reasonunit_base,
                delete_premise_needs=before_premise_needs.difference(
                    after_premise_needs
                ),
            )

    def add_atomunit_idea_reasonunit_deletes(
        self, before_ideaunit: IdeaUnit, delete_reasonunit_bases: set
    ):
        for delete_reasonunit_base in delete_reasonunit_bases:
            x_atomunit = atomunit_shop(bud_idea_reasonunit_str(), atom_delete())
            x_atomunit.set_required_arg(road_str(), before_ideaunit.get_road())
            x_atomunit.set_required_arg("base", delete_reasonunit_base)
            self.set_atomunit(x_atomunit)

            before_reasonunit = before_ideaunit.get_reasonunit(delete_reasonunit_base)
            self.add_atomunit_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=delete_reasonunit_base,
                delete_premise_needs=set(before_reasonunit.premises.keys()),
            )

    def add_atomunit_idea_reason_premiseunit_inserts(
        self,
        idea_road: RoadUnit,
        after_reasonunit: ReasonUnit,
        insert_premise_needs: set,
    ):
        for insert_premise_need in insert_premise_needs:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_need)
            x_atomunit = atomunit_shop(bud_idea_reason_premiseunit_str(), atom_insert())
            x_atomunit.set_required_arg(road_str(), idea_road)
            x_atomunit.set_required_arg("base", after_reasonunit.base)
            x_atomunit.set_required_arg("need", after_premiseunit.need)
            if after_premiseunit.open is not None:
                x_atomunit.set_optional_arg("open", after_premiseunit.open)
            if after_premiseunit.nigh is not None:
                x_atomunit.set_optional_arg("nigh", after_premiseunit.nigh)
            if after_premiseunit.divisor is not None:
                x_atomunit.set_optional_arg("divisor", after_premiseunit.divisor)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_reason_premiseunit_updates(
        self,
        idea_road: RoadUnit,
        before_reasonunit: ReasonUnit,
        after_reasonunit: ReasonUnit,
        update_premise_needs: set,
    ):
        for update_premise_need in update_premise_needs:
            before_premiseunit = before_reasonunit.get_premise(update_premise_need)
            after_premiseunit = after_reasonunit.get_premise(update_premise_need)
            if optional_args_different(
                bud_idea_reason_premiseunit_str(),
                before_premiseunit,
                after_premiseunit,
            ):
                x_atomunit = atomunit_shop(
                    bud_idea_reason_premiseunit_str(), atom_update()
                )
                x_atomunit.set_required_arg(road_str(), idea_road)
                x_atomunit.set_required_arg("base", before_reasonunit.base)
                x_atomunit.set_required_arg("need", after_premiseunit.need)
                if after_premiseunit.open != before_premiseunit.open:
                    x_atomunit.set_optional_arg("open", after_premiseunit.open)
                if after_premiseunit.nigh != before_premiseunit.nigh:
                    x_atomunit.set_optional_arg("nigh", after_premiseunit.nigh)
                if after_premiseunit.divisor != before_premiseunit.divisor:
                    x_atomunit.set_optional_arg("divisor", after_premiseunit.divisor)
                self.set_atomunit(x_atomunit)

    def add_atomunit_idea_reason_premiseunit_deletes(
        self,
        idea_road: RoadUnit,
        reasonunit_base: RoadUnit,
        delete_premise_needs: set,
    ):
        for delete_premise_need in delete_premise_needs:
            x_atomunit = atomunit_shop(bud_idea_reason_premiseunit_str(), atom_delete())
            x_atomunit.set_required_arg(road_str(), idea_road)
            x_atomunit.set_required_arg("base", reasonunit_base)
            x_atomunit.set_required_arg("need", delete_premise_need)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_teamlink_insert(
        self, idea_road: RoadUnit, insert_teamlink_group_ids: set
    ):
        for insert_teamlink_group_id in insert_teamlink_group_ids:
            x_atomunit = atomunit_shop(bud_idea_teamlink_str(), atom_insert())
            x_atomunit.set_required_arg(road_str(), idea_road)
            x_atomunit.set_required_arg(group_id_str(), insert_teamlink_group_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_teamlink_deletes(
        self, idea_road: RoadUnit, delete_teamlink_group_ids: set
    ):
        for delete_teamlink_group_id in delete_teamlink_group_ids:
            x_atomunit = atomunit_shop(bud_idea_teamlink_str(), atom_delete())
            x_atomunit.set_required_arg(road_str(), idea_road)
            x_atomunit.set_required_arg(group_id_str(), delete_teamlink_group_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_healerlink_insert(
        self, idea_road: RoadUnit, insert_healerlink_healer_ids: set
    ):
        for insert_healerlink_healer_id in insert_healerlink_healer_ids:
            x_atomunit = atomunit_shop(bud_idea_healerlink_str(), atom_insert())
            x_atomunit.set_required_arg(road_str(), idea_road)
            x_atomunit.set_required_arg(healer_id_str(), insert_healerlink_healer_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_healerlink_deletes(
        self, idea_road: RoadUnit, delete_healerlink_healer_ids: set
    ):
        for delete_healerlink_healer_id in delete_healerlink_healer_ids:
            x_atomunit = atomunit_shop(bud_idea_healerlink_str(), atom_delete())
            x_atomunit.set_required_arg(road_str(), idea_road)
            x_atomunit.set_required_arg(healer_id_str(), delete_healerlink_healer_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_awardlink_inserts(
        self, after_ideaunit: IdeaUnit, insert_awardlink_group_ids: set
    ):
        for after_awardlink_group_id in insert_awardlink_group_ids:
            after_awardlink = after_ideaunit.awardlinks.get(after_awardlink_group_id)
            x_atomunit = atomunit_shop(bud_idea_awardlink_str(), atom_insert())
            x_atomunit.set_required_arg(road_str(), after_ideaunit.get_road())
            x_atomunit.set_required_arg(group_id_str(), after_awardlink.group_id)
            x_atomunit.set_optional_arg("give_force", after_awardlink.give_force)
            x_atomunit.set_optional_arg("take_force", after_awardlink.take_force)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_awardlink_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_awardlink_group_ids: set,
    ):
        for update_awardlink_group_id in update_awardlink_group_ids:
            before_awardlink = before_ideaunit.awardlinks.get(update_awardlink_group_id)
            after_awardlink = after_ideaunit.awardlinks.get(update_awardlink_group_id)
            if optional_args_different(
                bud_idea_awardlink_str(), before_awardlink, after_awardlink
            ):
                x_atomunit = atomunit_shop(bud_idea_awardlink_str(), atom_update())
                x_atomunit.set_required_arg(road_str(), before_ideaunit.get_road())
                x_atomunit.set_required_arg(group_id_str(), after_awardlink.group_id)
                if before_awardlink.give_force != after_awardlink.give_force:
                    x_atomunit.set_optional_arg(
                        "give_force", after_awardlink.give_force
                    )
                if before_awardlink.take_force != after_awardlink.take_force:
                    x_atomunit.set_optional_arg(
                        "take_force", after_awardlink.take_force
                    )
                self.set_atomunit(x_atomunit)

    def add_atomunit_idea_awardlink_deletes(
        self, idea_road: RoadUnit, delete_awardlink_group_ids: set
    ):
        for delete_awardlink_group_id in delete_awardlink_group_ids:
            x_atomunit = atomunit_shop(bud_idea_awardlink_str(), atom_delete())
            x_atomunit.set_required_arg(road_str(), idea_road)
            x_atomunit.set_required_arg(group_id_str(), delete_awardlink_group_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_inserts(
        self, ideaunit: IdeaUnit, insert_factunit_bases: set
    ):
        for insert_factunit_base in insert_factunit_bases:
            insert_factunit = ideaunit.factunits.get(insert_factunit_base)
            x_atomunit = atomunit_shop(bud_idea_factunit_str(), atom_insert())
            x_atomunit.set_required_arg(road_str(), ideaunit.get_road())
            x_atomunit.set_required_arg("base", insert_factunit.base)
            if insert_factunit.pick is not None:
                x_atomunit.set_optional_arg("pick", insert_factunit.pick)
            if insert_factunit.fopen is not None:
                x_atomunit.set_optional_arg(fopen_str(), insert_factunit.fopen)
            if insert_factunit.fnigh is not None:
                x_atomunit.set_optional_arg(fnigh_str(), insert_factunit.fnigh)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_factunit_bases: set,
    ):
        for update_factunit_base in update_factunit_bases:
            before_factunit = before_ideaunit.factunits.get(update_factunit_base)
            after_factunit = after_ideaunit.factunits.get(update_factunit_base)
            if optional_args_different(
                bud_idea_factunit_str(), before_factunit, after_factunit
            ):
                x_atomunit = atomunit_shop(bud_idea_factunit_str(), atom_update())
                x_atomunit.set_required_arg(road_str(), before_ideaunit.get_road())
                x_atomunit.set_required_arg("base", after_factunit.base)
                if before_factunit.pick != after_factunit.pick:
                    x_atomunit.set_optional_arg("pick", after_factunit.pick)
                if before_factunit.fopen != after_factunit.fopen:
                    x_atomunit.set_optional_arg(fopen_str(), after_factunit.fopen)
                if before_factunit.fnigh != after_factunit.fnigh:
                    x_atomunit.set_optional_arg(fnigh_str(), after_factunit.fnigh)
                self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_deletes(
        self, idea_road: RoadUnit, delete_factunit_bases: FactUnit
    ):
        for delete_factunit_base in delete_factunit_bases:
            x_atomunit = atomunit_shop(bud_idea_factunit_str(), atom_delete())
            x_atomunit.set_required_arg(road_str(), idea_road)
            x_atomunit.set_required_arg("base", delete_factunit_base)
            self.set_atomunit(x_atomunit)

    def get_ordered_atomunits(self, x_count: int = None) -> dict[int, AtomUnit]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_atom in self.get_sorted_atomunits():
            x_dict[x_count] = x_atom
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int, str]:
        atom_tuples = self.get_ordered_atomunits(x_count).items()
        return {atom_num: atom_obj.get_dict() for atom_num, atom_obj in atom_tuples}

    def get_json(self, x_count: int = None) -> str:
        x_dict = self.get_ordered_dict(x_count)
        return get_json_from_dict(x_dict)


def changeunit_shop(atomunits: dict[str, AtomUnit] = None) -> ChangeUnit:
    return ChangeUnit(
        atomunits=get_empty_dict_if_none(atomunits),
        _bud_build_validated=False,
    )


def bud_built_from_change_is_valid(x_change: ChangeUnit, x_bud: BudUnit = None) -> bool:
    x_bud = budunit_shop() if x_bud is None else x_bud
    x_bud = x_change.get_edited_bud(x_bud)

    try:
        x_bud.settle_bud()
    except Exception:
        return False
    return True


def get_filtered_changeunit(
    x_changeunit: ChangeUnit, category_set: set[str], curd_set: set[str]
) -> ChangeUnit:
    new_changeunit = changeunit_shop()
    for x_atomunit in x_changeunit.get_sorted_atomunits():
        if x_atomunit.crud_str in curd_set and x_atomunit.category in category_set:
            new_changeunit.set_atomunit(x_atomunit)
    return new_changeunit


def sift_changeunit(x_changeunit: ChangeUnit, x_bud: BudUnit) -> ChangeUnit:
    new_changeunit = changeunit_shop()
    for x_atom in x_changeunit.get_sorted_atomunits():
        sifted_atom = sift_atomunit(x_bud, x_atom)
        if sifted_atom != None:
            new_changeunit.set_atomunit(sifted_atom)
    return new_changeunit
