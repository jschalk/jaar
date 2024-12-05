from src.f00_instrument.dict_toolbox import (
    get_empty_dict_if_none,
    get_json_from_dict,
    set_in_nested_dict,
    get_from_nested_dict,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from src.f01_road.road import RoadUnit, get_terminus_idea, get_parent_road
from src.f02_bud.reason_item import FactUnit, ReasonUnit
from src.f02_bud.acct import MemberShip, AcctID, AcctUnit
from src.f02_bud.group import MemberShip, GroupID
from src.f02_bud.item import ItemUnit
from src.f02_bud.bud import BudUnit, budunit_shop
from src.f02_bud.bud_tool import (
    bud_attr_exists,
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_factunit_str,
    bud_get_obj,
)
from src.f04_gift.atom_config import (
    CRUD_command,
    acct_id_str,
    awardee_id_str,
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
    base_item_active_requisite_str,
    get_atom_config_jkeys,
    get_atom_config_jvalues,
)
from src.f04_gift.atom import (
    AtomUnit,
    atomunit_shop,
    modify_bud_with_atomunit,
    InvalidAtomUnitException,
    atom_delete,
    atom_insert,
    atom_update,
    jvalues_different,
    sift_atomunit,
)
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class DeltaUnit:
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
            if x_list[0].jkeys.get(parent_road_str()) is not None:
                x_list = sorted(x_list, key=lambda x: x.jkeys.get(parent_road_str()))
            if x_list[0].jkeys.get(road_str()) is not None:
                x_list = sorted(x_list, key=lambda x: x.jkeys.get(road_str()))
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
                {x_atomunit.is_jkeys_valid()=}
                {x_atomunit.is_jvalues_valid()=}"""
            )

        x_atomunit.set_atom_order()
        x_keylist = [
            x_atomunit.crud_str,
            x_atomunit.category,
            *x_atomunit.get_nesting_order_args(),
        ]
        set_in_nested_dict(self.atomunits, x_keylist, x_atomunit)

    def atomunit_exists(self, x_atomunit: AtomUnit) -> bool:
        if x_atomunit.is_valid() is False:
            raise InvalidAtomUnitException(
                f"""'{x_atomunit.category}' {x_atomunit.crud_str} AtomUnit is invalid
                {x_atomunit.is_jkeys_valid()=}
                {x_atomunit.is_jvalues_valid()=}"""
            )

        x_atomunit.set_atom_order()
        x_keylist = [
            x_atomunit.crud_str,
            x_atomunit.category,
            *list(x_atomunit.get_nesting_order_args()),
        ]
        nested_atomunit = get_from_nested_dict(self.atomunits, x_keylist, True)
        return nested_atomunit == x_atomunit

    def add_atomunit(
        self,
        category: str,
        crud_str: str,
        jkeys: str = None,
        jvalues: str = None,
    ):
        x_atomunit = atomunit_shop(
            category=category,
            crud_str=crud_str,
            jkeys=jkeys,
            jvalues=jvalues,
        )
        self.set_atomunit(x_atomunit)

    def get_atomunit(self, crud_str: str, category: str, jkeys: list[str]) -> AtomUnit:
        x_keylist = [crud_str, category, *jkeys]
        return get_from_nested_dict(self.atomunits, x_keylist)

    def add_all_atomunits(self, after_bud: BudUnit):
        before_bud = budunit_shop(after_bud._owner_id, after_bud._fiscal_id)
        self.add_all_different_atomunits(before_bud, after_bud)

    def add_all_different_atomunits(self, before_bud: BudUnit, after_bud: BudUnit):
        before_bud.settle_bud()
        after_bud.settle_bud()
        self.add_atomunits_budunit_simple_attrs(before_bud, after_bud)
        self.add_atomunits_accts(before_bud, after_bud)
        self.add_atomunits_items(before_bud, after_bud)

    def add_atomunits_budunit_simple_attrs(
        self, before_bud: BudUnit, after_bud: BudUnit
    ):
        if not jvalues_different(budunit_str(), before_bud, after_bud):
            return
        x_atomunit = atomunit_shop(budunit_str(), atom_update())
        if before_bud.max_tree_traverse != after_bud.max_tree_traverse:
            x_atomunit.set_jvalue("max_tree_traverse", after_bud.max_tree_traverse)
        if before_bud.credor_respect != after_bud.credor_respect:
            x_atomunit.set_jvalue("credor_respect", after_bud.credor_respect)
        if before_bud.debtor_respect != after_bud.debtor_respect:
            x_atomunit.set_jvalue("debtor_respect", after_bud.debtor_respect)
        if before_bud.tally != after_bud.tally:
            x_atomunit.set_jvalue("tally", after_bud.tally)
        if before_bud.fund_pool != after_bud.fund_pool:
            x_atomunit.set_jvalue("fund_pool", after_bud.fund_pool)
        if before_bud.fund_coin != after_bud.fund_coin:
            x_atomunit.set_jvalue("fund_coin", after_bud.fund_coin)
        if before_bud.purview_time_id != after_bud.purview_time_id:
            x_atomunit.set_jvalue("purview_time_id", after_bud.purview_time_id)
        if before_bud.respect_bit != after_bud.respect_bit:
            x_atomunit.set_jvalue("respect_bit", after_bud.respect_bit)
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
            x_atomunit.set_jkey(acct_id_str(), insert_acctunit.acct_id)
            if insert_acctunit.credit_belief is not None:
                x_atomunit.set_jvalue("credit_belief", insert_acctunit.credit_belief)
            if insert_acctunit.debtit_belief is not None:
                x_atomunit.set_jvalue("debtit_belief", insert_acctunit.debtit_belief)
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
            if jvalues_different(bud_acctunit_str(), after_acctunit, before_acctunit):
                x_atomunit = atomunit_shop(bud_acctunit_str(), atom_update())
                x_atomunit.set_jkey(acct_id_str(), after_acctunit.acct_id)
                if before_acctunit.credit_belief != after_acctunit.credit_belief:
                    x_atomunit.set_jvalue("credit_belief", after_acctunit.credit_belief)
                if before_acctunit.debtit_belief != after_acctunit.debtit_belief:
                    x_atomunit.set_jvalue("debtit_belief", after_acctunit.debtit_belief)
                self.set_atomunit(x_atomunit)
            self.add_atomunit_acctunit_update_memberships(
                after_acctunit=after_acctunit, before_acctunit=before_acctunit
            )

    def add_atomunit_acctunit_deletes(self, before_bud: BudUnit, delete_acct_ids: set):
        for delete_acct_id in delete_acct_ids:
            x_atomunit = atomunit_shop(bud_acctunit_str(), atom_delete())
            x_atomunit.set_jkey(acct_id_str(), delete_acct_id)
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
            if jvalues_different(
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
            x_atomunit.set_jkey(acct_id_str(), after_acct_id)
            x_atomunit.set_jkey(group_id_str(), after_membership.group_id)
            if after_membership.credit_vote is not None:
                x_atomunit.set_jvalue(credit_vote_str(), after_membership.credit_vote)
            if after_membership.debtit_vote is not None:
                x_atomunit.set_jvalue(debtit_vote_str(), after_membership.debtit_vote)
            self.set_atomunit(x_atomunit)

    def add_atomunit_membership_update(
        self,
        acct_id: AcctID,
        before_membership: MemberShip,
        after_membership: MemberShip,
    ):
        x_atomunit = atomunit_shop(bud_acct_membership_str(), atom_update())
        x_atomunit.set_jkey(acct_id_str(), acct_id)
        x_atomunit.set_jkey(group_id_str(), after_membership.group_id)
        if after_membership.credit_vote != before_membership.credit_vote:
            x_atomunit.set_jvalue(credit_vote_str(), after_membership.credit_vote)
        if after_membership.debtit_vote != before_membership.debtit_vote:
            x_atomunit.set_jvalue(debtit_vote_str(), after_membership.debtit_vote)
        self.set_atomunit(x_atomunit)

    def add_atomunit_memberships_delete(
        self, before_acct_id: AcctID, before_group_ids: GroupID
    ):
        for delete_group_id in before_group_ids:
            x_atomunit = atomunit_shop(bud_acct_membership_str(), atom_delete())
            x_atomunit.set_jkey(acct_id_str(), before_acct_id)
            x_atomunit.set_jkey(group_id_str(), delete_group_id)
            self.set_atomunit(x_atomunit)

    def add_atomunits_items(self, before_bud: BudUnit, after_bud: BudUnit):
        before_item_roads = set(before_bud._item_dict.keys())
        after_item_roads = set(after_bud._item_dict.keys())

        self.add_atomunit_item_inserts(
            after_bud=after_bud,
            insert_item_roads=after_item_roads.difference(before_item_roads),
        )
        self.add_atomunit_item_deletes(
            before_bud=before_bud,
            delete_item_roads=before_item_roads.difference(after_item_roads),
        )
        self.add_atomunit_item_updates(
            before_bud=before_bud,
            after_bud=after_bud,
            update_roads=before_item_roads.intersection(after_item_roads),
        )

    def add_atomunit_item_inserts(self, after_bud: BudUnit, insert_item_roads: set):
        for insert_item_road in insert_item_roads:
            insert_itemunit = after_bud.get_item_obj(insert_item_road)
            x_atomunit = atomunit_shop(bud_itemunit_str(), atom_insert())
            x_atomunit.set_jkey(parent_road_str(), insert_itemunit._parent_road)
            x_atomunit.set_jkey(label_str(), insert_itemunit._label)
            x_atomunit.set_jvalue(addin_str(), insert_itemunit.addin)
            x_atomunit.set_jvalue(begin_str(), insert_itemunit.begin)
            x_atomunit.set_jvalue(close_str(), insert_itemunit.close)
            x_atomunit.set_jvalue(denom_str(), insert_itemunit.denom)
            x_atomunit.set_jvalue(numor_str(), insert_itemunit.numor)
            x_atomunit.set_jvalue(morph_str(), insert_itemunit.morph)
            x_atomunit.set_jvalue(mass_str(), insert_itemunit.mass)
            x_atomunit.set_jvalue(pledge_str(), insert_itemunit.pledge)
            self.set_atomunit(x_atomunit)

            self.add_atomunit_item_factunit_inserts(
                itemunit=insert_itemunit,
                insert_factunit_bases=set(insert_itemunit.factunits.keys()),
            )
            self.add_atomunit_item_awardlink_inserts(
                after_itemunit=insert_itemunit,
                insert_awardlink_awardee_ids=set(insert_itemunit.awardlinks.keys()),
            )
            self.add_atomunit_item_reasonunit_inserts(
                after_itemunit=insert_itemunit,
                insert_reasonunit_bases=set(insert_itemunit.reasonunits.keys()),
            )
            self.add_atomunit_item_teamlink_insert(
                item_road=insert_item_road,
                insert_teamlink_team_ids=insert_itemunit.teamunit._teamlinks,
            )
            self.add_atomunit_item_healerlink_insert(
                item_road=insert_item_road,
                insert_healerlink_healer_ids=insert_itemunit.healerlink._healer_ids,
            )

    def add_atomunit_item_updates(
        self, before_bud: BudUnit, after_bud: BudUnit, update_roads: set
    ):
        for item_road in update_roads:
            after_itemunit = after_bud.get_item_obj(item_road)
            before_itemunit = before_bud.get_item_obj(item_road)
            if jvalues_different(bud_itemunit_str(), before_itemunit, after_itemunit):
                x_atomunit = atomunit_shop(bud_itemunit_str(), atom_update())
                x_atomunit.set_jkey(parent_road_str(), after_itemunit._parent_road)
                x_atomunit.set_jkey(label_str(), after_itemunit._label)
                if before_itemunit.addin != after_itemunit.addin:
                    x_atomunit.set_jvalue(addin_str(), after_itemunit.addin)
                if before_itemunit.begin != after_itemunit.begin:
                    x_atomunit.set_jvalue(begin_str(), after_itemunit.begin)
                if before_itemunit.close != after_itemunit.close:
                    x_atomunit.set_jvalue(close_str(), after_itemunit.close)
                if before_itemunit.denom != after_itemunit.denom:
                    x_atomunit.set_jvalue(denom_str(), after_itemunit.denom)
                if before_itemunit.numor != after_itemunit.numor:
                    x_atomunit.set_jvalue(numor_str(), after_itemunit.numor)
                if before_itemunit.morph != after_itemunit.morph:
                    x_atomunit.set_jvalue(morph_str(), after_itemunit.morph)
                if before_itemunit.mass != after_itemunit.mass:
                    x_atomunit.set_jvalue(mass_str(), after_itemunit.mass)
                if before_itemunit.pledge != after_itemunit.pledge:
                    x_atomunit.set_jvalue(pledge_str(), after_itemunit.pledge)
                self.set_atomunit(x_atomunit)

            # insert / update / delete factunits
            before_factunit_bases = set(before_itemunit.factunits.keys())
            after_factunit_bases = set(after_itemunit.factunits.keys())
            self.add_atomunit_item_factunit_inserts(
                itemunit=after_itemunit,
                insert_factunit_bases=after_factunit_bases.difference(
                    before_factunit_bases
                ),
            )
            self.add_atomunit_item_factunit_updates(
                before_itemunit=before_itemunit,
                after_itemunit=after_itemunit,
                update_factunit_bases=before_factunit_bases.intersection(
                    after_factunit_bases
                ),
            )
            self.add_atomunit_item_factunit_deletes(
                item_road=item_road,
                delete_factunit_bases=before_factunit_bases.difference(
                    after_factunit_bases
                ),
            )

            # insert / update / delete awardunits
            before_awardlinks_awardee_ids = set(before_itemunit.awardlinks.keys())
            after_awardlinks_awardee_ids = set(after_itemunit.awardlinks.keys())
            self.add_atomunit_item_awardlink_inserts(
                after_itemunit=after_itemunit,
                insert_awardlink_awardee_ids=after_awardlinks_awardee_ids.difference(
                    before_awardlinks_awardee_ids
                ),
            )
            self.add_atomunit_item_awardlink_updates(
                before_itemunit=before_itemunit,
                after_itemunit=after_itemunit,
                update_awardlink_awardee_ids=before_awardlinks_awardee_ids.intersection(
                    after_awardlinks_awardee_ids
                ),
            )
            self.add_atomunit_item_awardlink_deletes(
                item_road=item_road,
                delete_awardlink_awardee_ids=before_awardlinks_awardee_ids.difference(
                    after_awardlinks_awardee_ids
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_bases = set(before_itemunit.reasonunits.keys())
            after_reasonunit_bases = set(after_itemunit.reasonunits.keys())
            self.add_atomunit_item_reasonunit_inserts(
                after_itemunit=after_itemunit,
                insert_reasonunit_bases=after_reasonunit_bases.difference(
                    before_reasonunit_bases
                ),
            )
            self.add_atomunit_item_reasonunit_updates(
                before_itemunit=before_itemunit,
                after_itemunit=after_itemunit,
                update_reasonunit_bases=before_reasonunit_bases.intersection(
                    after_reasonunit_bases
                ),
            )
            self.add_atomunit_item_reasonunit_deletes(
                before_itemunit=before_itemunit,
                delete_reasonunit_bases=before_reasonunit_bases.difference(
                    after_reasonunit_bases
                ),
            )
            # insert / update / delete reasonunits_permises
            # update reasonunits_permises insert_premise
            # update reasonunits_permises update_premise
            # update reasonunits_permises delete_premise

            # insert / update / delete teamlinks
            before_teamlinks_team_ids = set(before_itemunit.teamunit._teamlinks)
            after_teamlinks_team_ids = set(after_itemunit.teamunit._teamlinks)
            self.add_atomunit_item_teamlink_insert(
                item_road=item_road,
                insert_teamlink_team_ids=after_teamlinks_team_ids.difference(
                    before_teamlinks_team_ids
                ),
            )
            self.add_atomunit_item_teamlink_deletes(
                item_road=item_road,
                delete_teamlink_team_ids=before_teamlinks_team_ids.difference(
                    after_teamlinks_team_ids
                ),
            )

            # insert / update / delete healerlinks
            before_healerlinks_healer_ids = set(before_itemunit.healerlink._healer_ids)
            after_healerlinks_healer_ids = set(after_itemunit.healerlink._healer_ids)
            self.add_atomunit_item_healerlink_insert(
                item_road=item_road,
                insert_healerlink_healer_ids=after_healerlinks_healer_ids.difference(
                    before_healerlinks_healer_ids
                ),
            )
            self.add_atomunit_item_healerlink_deletes(
                item_road=item_road,
                delete_healerlink_healer_ids=before_healerlinks_healer_ids.difference(
                    after_healerlinks_healer_ids
                ),
            )

    def add_atomunit_item_deletes(self, before_bud: BudUnit, delete_item_roads: set):
        for delete_item_road in delete_item_roads:
            x_parent_road = get_parent_road(delete_item_road, before_bud._wall)
            x_label = get_terminus_idea(delete_item_road, before_bud._wall)
            x_atomunit = atomunit_shop(bud_itemunit_str(), atom_delete())
            x_atomunit.set_jkey(parent_road_str(), x_parent_road)
            x_atomunit.set_jkey(label_str(), x_label)
            self.set_atomunit(x_atomunit)

            delete_itemunit = before_bud.get_item_obj(delete_item_road)
            self.add_atomunit_item_factunit_deletes(
                item_road=delete_item_road,
                delete_factunit_bases=set(delete_itemunit.factunits.keys()),
            )

            self.add_atomunit_item_awardlink_deletes(
                item_road=delete_item_road,
                delete_awardlink_awardee_ids=set(delete_itemunit.awardlinks.keys()),
            )
            self.add_atomunit_item_reasonunit_deletes(
                before_itemunit=delete_itemunit,
                delete_reasonunit_bases=set(delete_itemunit.reasonunits.keys()),
            )
            self.add_atomunit_item_teamlink_deletes(
                item_road=delete_item_road,
                delete_teamlink_team_ids=delete_itemunit.teamunit._teamlinks,
            )
            self.add_atomunit_item_healerlink_deletes(
                item_road=delete_item_road,
                delete_healerlink_healer_ids=delete_itemunit.healerlink._healer_ids,
            )

    def add_atomunit_item_reasonunit_inserts(
        self, after_itemunit: ItemUnit, insert_reasonunit_bases: set
    ):
        for insert_reasonunit_base in insert_reasonunit_bases:
            after_reasonunit = after_itemunit.get_reasonunit(insert_reasonunit_base)
            x_atomunit = atomunit_shop(bud_item_reasonunit_str(), atom_insert())
            x_atomunit.set_jkey(road_str(), after_itemunit.get_road())
            x_atomunit.set_jkey("base", after_reasonunit.base)
            if after_reasonunit.base_item_active_requisite is not None:
                x_atomunit.set_jvalue(
                    base_item_active_requisite_str(),
                    after_reasonunit.base_item_active_requisite,
                )
            self.set_atomunit(x_atomunit)

            self.add_atomunit_item_reason_premiseunit_inserts(
                item_road=after_itemunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=set(after_reasonunit.premises.keys()),
            )

    def add_atomunit_item_reasonunit_updates(
        self,
        before_itemunit: ItemUnit,
        after_itemunit: ItemUnit,
        update_reasonunit_bases: set,
    ):
        for update_reasonunit_base in update_reasonunit_bases:
            before_reasonunit = before_itemunit.get_reasonunit(update_reasonunit_base)
            after_reasonunit = after_itemunit.get_reasonunit(update_reasonunit_base)
            if jvalues_different(
                bud_item_reasonunit_str(), before_reasonunit, after_reasonunit
            ):
                x_atomunit = atomunit_shop(bud_item_reasonunit_str(), atom_update())
                x_atomunit.set_jkey(road_str(), before_itemunit.get_road())
                x_atomunit.set_jkey("base", after_reasonunit.base)
                if (
                    before_reasonunit.base_item_active_requisite
                    != after_reasonunit.base_item_active_requisite
                ):
                    x_atomunit.set_jvalue(
                        base_item_active_requisite_str(),
                        after_reasonunit.base_item_active_requisite,
                    )
                self.set_atomunit(x_atomunit)

            before_premise_needs = set(before_reasonunit.premises.keys())
            after_premise_needs = set(after_reasonunit.premises.keys())
            self.add_atomunit_item_reason_premiseunit_inserts(
                item_road=before_itemunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=after_premise_needs.difference(
                    before_premise_needs
                ),
            )
            self.add_atomunit_item_reason_premiseunit_updates(
                item_road=before_itemunit.get_road(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_needs=after_premise_needs.intersection(
                    before_premise_needs
                ),
            )
            self.add_atomunit_item_reason_premiseunit_deletes(
                item_road=before_itemunit.get_road(),
                reasonunit_base=update_reasonunit_base,
                delete_premise_needs=before_premise_needs.difference(
                    after_premise_needs
                ),
            )

    def add_atomunit_item_reasonunit_deletes(
        self, before_itemunit: ItemUnit, delete_reasonunit_bases: set
    ):
        for delete_reasonunit_base in delete_reasonunit_bases:
            x_atomunit = atomunit_shop(bud_item_reasonunit_str(), atom_delete())
            x_atomunit.set_jkey(road_str(), before_itemunit.get_road())
            x_atomunit.set_jkey("base", delete_reasonunit_base)
            self.set_atomunit(x_atomunit)

            before_reasonunit = before_itemunit.get_reasonunit(delete_reasonunit_base)
            self.add_atomunit_item_reason_premiseunit_deletes(
                item_road=before_itemunit.get_road(),
                reasonunit_base=delete_reasonunit_base,
                delete_premise_needs=set(before_reasonunit.premises.keys()),
            )

    def add_atomunit_item_reason_premiseunit_inserts(
        self,
        item_road: RoadUnit,
        after_reasonunit: ReasonUnit,
        insert_premise_needs: set,
    ):
        for insert_premise_need in insert_premise_needs:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_need)
            x_atomunit = atomunit_shop(bud_item_reason_premiseunit_str(), atom_insert())
            x_atomunit.set_jkey(road_str(), item_road)
            x_atomunit.set_jkey("base", after_reasonunit.base)
            x_atomunit.set_jkey("need", after_premiseunit.need)
            if after_premiseunit.open is not None:
                x_atomunit.set_jvalue("open", after_premiseunit.open)
            if after_premiseunit.nigh is not None:
                x_atomunit.set_jvalue("nigh", after_premiseunit.nigh)
            if after_premiseunit.divisor is not None:
                x_atomunit.set_jvalue("divisor", after_premiseunit.divisor)
            self.set_atomunit(x_atomunit)

    def add_atomunit_item_reason_premiseunit_updates(
        self,
        item_road: RoadUnit,
        before_reasonunit: ReasonUnit,
        after_reasonunit: ReasonUnit,
        update_premise_needs: set,
    ):
        for update_premise_need in update_premise_needs:
            before_premiseunit = before_reasonunit.get_premise(update_premise_need)
            after_premiseunit = after_reasonunit.get_premise(update_premise_need)
            if jvalues_different(
                bud_item_reason_premiseunit_str(),
                before_premiseunit,
                after_premiseunit,
            ):
                x_atomunit = atomunit_shop(
                    bud_item_reason_premiseunit_str(), atom_update()
                )
                x_atomunit.set_jkey(road_str(), item_road)
                x_atomunit.set_jkey("base", before_reasonunit.base)
                x_atomunit.set_jkey("need", after_premiseunit.need)
                if after_premiseunit.open != before_premiseunit.open:
                    x_atomunit.set_jvalue("open", after_premiseunit.open)
                if after_premiseunit.nigh != before_premiseunit.nigh:
                    x_atomunit.set_jvalue("nigh", after_premiseunit.nigh)
                if after_premiseunit.divisor != before_premiseunit.divisor:
                    x_atomunit.set_jvalue("divisor", after_premiseunit.divisor)
                self.set_atomunit(x_atomunit)

    def add_atomunit_item_reason_premiseunit_deletes(
        self,
        item_road: RoadUnit,
        reasonunit_base: RoadUnit,
        delete_premise_needs: set,
    ):
        for delete_premise_need in delete_premise_needs:
            x_atomunit = atomunit_shop(bud_item_reason_premiseunit_str(), atom_delete())
            x_atomunit.set_jkey(road_str(), item_road)
            x_atomunit.set_jkey("base", reasonunit_base)
            x_atomunit.set_jkey("need", delete_premise_need)
            self.set_atomunit(x_atomunit)

    def add_atomunit_item_teamlink_insert(
        self, item_road: RoadUnit, insert_teamlink_team_ids: set
    ):
        for insert_teamlink_team_id in insert_teamlink_team_ids:
            x_atomunit = atomunit_shop(bud_item_teamlink_str(), atom_insert())
            x_atomunit.set_jkey(road_str(), item_road)
            x_atomunit.set_jkey("team_id", insert_teamlink_team_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_item_teamlink_deletes(
        self, item_road: RoadUnit, delete_teamlink_team_ids: set
    ):
        for delete_teamlink_team_id in delete_teamlink_team_ids:
            x_atomunit = atomunit_shop(bud_item_teamlink_str(), atom_delete())
            x_atomunit.set_jkey(road_str(), item_road)
            x_atomunit.set_jkey("team_id", delete_teamlink_team_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_item_healerlink_insert(
        self, item_road: RoadUnit, insert_healerlink_healer_ids: set
    ):
        for insert_healerlink_healer_id in insert_healerlink_healer_ids:
            x_atomunit = atomunit_shop(bud_item_healerlink_str(), atom_insert())
            x_atomunit.set_jkey(road_str(), item_road)
            x_atomunit.set_jkey(healer_id_str(), insert_healerlink_healer_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_item_healerlink_deletes(
        self, item_road: RoadUnit, delete_healerlink_healer_ids: set
    ):
        for delete_healerlink_healer_id in delete_healerlink_healer_ids:
            x_atomunit = atomunit_shop(bud_item_healerlink_str(), atom_delete())
            x_atomunit.set_jkey(road_str(), item_road)
            x_atomunit.set_jkey(healer_id_str(), delete_healerlink_healer_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_item_awardlink_inserts(
        self, after_itemunit: ItemUnit, insert_awardlink_awardee_ids: set
    ):
        for after_awardlink_awardee_id in insert_awardlink_awardee_ids:
            after_awardlink = after_itemunit.awardlinks.get(after_awardlink_awardee_id)
            x_atomunit = atomunit_shop(bud_item_awardlink_str(), atom_insert())
            x_atomunit.set_jkey(road_str(), after_itemunit.get_road())
            x_atomunit.set_jkey(awardee_id_str(), after_awardlink.awardee_id)
            x_atomunit.set_jvalue("give_force", after_awardlink.give_force)
            x_atomunit.set_jvalue("take_force", after_awardlink.take_force)
            self.set_atomunit(x_atomunit)

    def add_atomunit_item_awardlink_updates(
        self,
        before_itemunit: ItemUnit,
        after_itemunit: ItemUnit,
        update_awardlink_awardee_ids: set,
    ):
        for update_awardlink_awardee_id in update_awardlink_awardee_ids:
            before_awardlink = before_itemunit.awardlinks.get(
                update_awardlink_awardee_id
            )
            after_awardlink = after_itemunit.awardlinks.get(update_awardlink_awardee_id)
            if jvalues_different(
                bud_item_awardlink_str(), before_awardlink, after_awardlink
            ):
                x_atomunit = atomunit_shop(bud_item_awardlink_str(), atom_update())
                x_atomunit.set_jkey(road_str(), before_itemunit.get_road())
                x_atomunit.set_jkey(awardee_id_str(), after_awardlink.awardee_id)
                if before_awardlink.give_force != after_awardlink.give_force:
                    x_atomunit.set_jvalue("give_force", after_awardlink.give_force)
                if before_awardlink.take_force != after_awardlink.take_force:
                    x_atomunit.set_jvalue("take_force", after_awardlink.take_force)
                self.set_atomunit(x_atomunit)

    def add_atomunit_item_awardlink_deletes(
        self, item_road: RoadUnit, delete_awardlink_awardee_ids: set
    ):
        for delete_awardlink_awardee_id in delete_awardlink_awardee_ids:
            x_atomunit = atomunit_shop(bud_item_awardlink_str(), atom_delete())
            x_atomunit.set_jkey(road_str(), item_road)
            x_atomunit.set_jkey(awardee_id_str(), delete_awardlink_awardee_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_item_factunit_inserts(
        self, itemunit: ItemUnit, insert_factunit_bases: set
    ):
        for insert_factunit_base in insert_factunit_bases:
            insert_factunit = itemunit.factunits.get(insert_factunit_base)
            x_atomunit = atomunit_shop(bud_item_factunit_str(), atom_insert())
            x_atomunit.set_jkey(road_str(), itemunit.get_road())
            x_atomunit.set_jkey("base", insert_factunit.base)
            if insert_factunit.pick is not None:
                x_atomunit.set_jvalue("pick", insert_factunit.pick)
            if insert_factunit.fopen is not None:
                x_atomunit.set_jvalue(fopen_str(), insert_factunit.fopen)
            if insert_factunit.fnigh is not None:
                x_atomunit.set_jvalue(fnigh_str(), insert_factunit.fnigh)
            self.set_atomunit(x_atomunit)

    def add_atomunit_item_factunit_updates(
        self,
        before_itemunit: ItemUnit,
        after_itemunit: ItemUnit,
        update_factunit_bases: set,
    ):
        for update_factunit_base in update_factunit_bases:
            before_factunit = before_itemunit.factunits.get(update_factunit_base)
            after_factunit = after_itemunit.factunits.get(update_factunit_base)
            if jvalues_different(
                bud_item_factunit_str(), before_factunit, after_factunit
            ):
                x_atomunit = atomunit_shop(bud_item_factunit_str(), atom_update())
                x_atomunit.set_jkey(road_str(), before_itemunit.get_road())
                x_atomunit.set_jkey("base", after_factunit.base)
                if before_factunit.pick != after_factunit.pick:
                    x_atomunit.set_jvalue("pick", after_factunit.pick)
                if before_factunit.fopen != after_factunit.fopen:
                    x_atomunit.set_jvalue(fopen_str(), after_factunit.fopen)
                if before_factunit.fnigh != after_factunit.fnigh:
                    x_atomunit.set_jvalue(fnigh_str(), after_factunit.fnigh)
                self.set_atomunit(x_atomunit)

    def add_atomunit_item_factunit_deletes(
        self, item_road: RoadUnit, delete_factunit_bases: FactUnit
    ):
        for delete_factunit_base in delete_factunit_bases:
            x_atomunit = atomunit_shop(bud_item_factunit_str(), atom_delete())
            x_atomunit.set_jkey(road_str(), item_road)
            x_atomunit.set_jkey("base", delete_factunit_base)
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


def deltaunit_shop(atomunits: dict[str, AtomUnit] = None) -> DeltaUnit:
    return DeltaUnit(
        atomunits=get_empty_dict_if_none(atomunits),
        _bud_build_validated=False,
    )


def bud_built_from_delta_is_valid(x_delta: DeltaUnit, x_bud: BudUnit = None) -> bool:
    x_bud = budunit_shop() if x_bud is None else x_bud
    x_bud = x_delta.get_edited_bud(x_bud)

    try:
        x_bud.settle_bud()
    except Exception:
        return False
    return True


def get_categorys_cruds_deltaunit(
    x_deltaunit: DeltaUnit, category_set: set[str], curd_set: set[str]
) -> DeltaUnit:
    new_deltaunit = deltaunit_shop()
    for x_atomunit in x_deltaunit.get_sorted_atomunits():
        if x_atomunit.crud_str in curd_set and x_atomunit.category in category_set:
            new_deltaunit.set_atomunit(x_atomunit)
    return new_deltaunit


def sift_deltaunit(x_deltaunit: DeltaUnit, x_bud: BudUnit) -> DeltaUnit:
    new_deltaunit = deltaunit_shop()
    for x_atom in x_deltaunit.get_sorted_atomunits():
        sifted_atom = sift_atomunit(x_bud, x_atom)
        if sifted_atom != None:
            new_deltaunit.set_atomunit(sifted_atom)
    return new_deltaunit
