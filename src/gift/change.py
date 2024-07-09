from src._instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    place_obj_in_dict,
    get_nested_value,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src._world.reason_idea import FactUnit, ReasonUnit
from src._world.char import BeliefLink, CharID, CharUnit
from src._world.belieflink import BeliefLink, BeliefID
from src._world.idea import IdeaUnit
from src._world.world import WorldUnit, worldunit_shop
from src.gift.atom_config import CRUD_command
from src.gift.atom import (
    AtomUnit,
    atomunit_shop,
    modify_world_with_atomunit,
    InvalidAtomUnitException,
    atom_delete,
    atom_insert,
    atom_update,
    optional_args_different,
)
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class ChangeUnit:
    atomunits: dict[CRUD_command : dict[str, AtomUnit]] = None
    _world_build_validated: bool = None

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
            if x_list[0].required_args.get("parent_road") != None:
                x_list = sorted(
                    x_list, key=lambda x: x.required_args.get("parent_road")
                )
            if x_list[0].required_args.get("road") != None:
                x_list = sorted(x_list, key=lambda x: x.required_args.get("road"))
            ordered_list.extend(x_list)
        return ordered_list

    def get_sorted_atomunits(self) -> list[AtomUnit]:
        atomunits_list = self.get_category_sorted_atomunits_list()
        return sorted(atomunits_list, key=lambda x: x.atom_order)

    def get_edited_world(self, before_world: WorldUnit):
        edited_world = copy_deepcopy(before_world)
        for x_atomunit in self.get_sorted_atomunits():
            modify_world_with_atomunit(edited_world, x_atomunit)
        return edited_world

    def set_atomunit(self, x_atomunit: AtomUnit):
        if x_atomunit.is_valid() is False:
            raise InvalidAtomUnitException(
                f"""'{x_atomunit.category}' {x_atomunit.crud_text} AtomUnit is invalid
                {x_atomunit.is_required_args_valid()=}
                {x_atomunit.is_optional_args_valid()=}"""
            )

        x_atomunit.set_atom_order()
        x_keylist = [
            x_atomunit.crud_text,
            x_atomunit.category,
            *list(x_atomunit.required_args.values()),
        ]
        place_obj_in_dict(self.atomunits, x_keylist, x_atomunit)

    def atomunit_exists(self, x_atomunit: AtomUnit) -> bool:
        if x_atomunit.is_valid() is False:
            raise InvalidAtomUnitException(
                f"""'{x_atomunit.category}' {x_atomunit.crud_text} AtomUnit is invalid
                {x_atomunit.is_required_args_valid()=}
                {x_atomunit.is_optional_args_valid()=}"""
            )

        x_atomunit.set_atom_order()
        x_keylist = [
            x_atomunit.crud_text,
            x_atomunit.category,
            *list(x_atomunit.required_args.values()),
        ]
        try:
            nested_atomunit = get_nested_value(self.atomunits, x_keylist)
        except Exception:
            return False
        return nested_atomunit == x_atomunit

    def add_atomunit(
        self,
        category: str,
        crud_text: str,
        required_args: str = None,
        optional_args: str = None,
    ):
        x_atomunit = atomunit_shop(
            category=category,
            crud_text=crud_text,
            required_args=required_args,
            optional_args=optional_args,
        )
        self.set_atomunit(x_atomunit)

    def get_atomunit(
        self, crud_text: str, category: str, required_args: list[str]
    ) -> AtomUnit:
        x_keylist = [crud_text, category, *required_args]
        return get_nested_value(self.atomunits, x_keylist)

    def add_all_atomunits(self, after_world: WorldUnit):
        before_world = worldunit_shop(after_world._owner_id, after_world._real_id)
        self.add_all_different_atomunits(before_world, after_world)

    def add_all_different_atomunits(
        self, before_world: WorldUnit, after_world: WorldUnit
    ):
        before_world.calc_world_metrics()
        before_world._migrate_beliefunits_to_belieflinks()
        after_world.calc_world_metrics()
        after_world._migrate_beliefunits_to_belieflinks()
        self.add_atomunits_worldunit_simple_attrs(before_world, after_world)
        self.add_atomunits_chars(before_world, after_world)
        self.add_atomunits_ideas(before_world, after_world)

    def add_atomunits_worldunit_simple_attrs(
        self, before_world: WorldUnit, after_world: WorldUnit
    ):
        if not optional_args_different("worldunit", before_world, after_world):
            return
        x_atomunit = atomunit_shop("worldunit", atom_update())
        if before_world._max_tree_traverse != after_world._max_tree_traverse:
            x_atomunit.set_optional_arg(
                "_max_tree_traverse", after_world._max_tree_traverse
            )
        if before_world._meld_strategy != after_world._meld_strategy:
            x_atomunit.set_optional_arg("_meld_strategy", after_world._meld_strategy)
        if before_world._monetary_desc != after_world._monetary_desc:
            x_atomunit.set_optional_arg("_monetary_desc", after_world._monetary_desc)
        if before_world._char_credor_pool != after_world._char_credor_pool:
            x_atomunit.set_optional_arg(
                "_char_credor_pool", after_world._char_credor_pool
            )
        if before_world._char_debtor_pool != after_world._char_debtor_pool:
            x_atomunit.set_optional_arg(
                "_char_debtor_pool", after_world._char_debtor_pool
            )
        if before_world._weight != after_world._weight:
            x_atomunit.set_optional_arg("_weight", after_world._weight)
        if before_world._pixel != after_world._pixel:
            x_atomunit.set_optional_arg("_pixel", after_world._pixel)
        self.set_atomunit(x_atomunit)

    def add_atomunits_chars(self, before_world: WorldUnit, after_world: WorldUnit):
        before_char_ids = set(before_world._chars.keys())
        after_char_ids = set(after_world._chars.keys())

        self.add_atomunit_charunit_inserts(
            after_world=after_world,
            insert_char_ids=after_char_ids.difference(before_char_ids),
        )
        self.add_atomunit_charunit_deletes(
            before_world=before_world,
            delete_char_ids=before_char_ids.difference(after_char_ids),
        )
        self.add_atomunit_charunit_updates(
            before_world=before_world,
            after_world=after_world,
            update_char_ids=before_char_ids.intersection(after_char_ids),
        )

    def add_atomunit_charunit_inserts(
        self, after_world: WorldUnit, insert_char_ids: set
    ):
        for insert_char_id in insert_char_ids:
            insert_charunit = after_world.get_char(insert_char_id)
            x_atomunit = atomunit_shop("world_charunit", atom_insert())
            x_atomunit.set_required_arg("char_id", insert_charunit.char_id)
            if insert_charunit.credor_weight != None:
                x_atomunit.set_optional_arg(
                    "credor_weight", insert_charunit.credor_weight
                )
            if insert_charunit.debtor_weight != None:
                x_atomunit.set_optional_arg(
                    "debtor_weight", insert_charunit.debtor_weight
                )
            self.set_atomunit(x_atomunit)
            non_mirror_belief_ids = {
                x_belief_id
                for x_belief_id in insert_charunit._belieflinks.keys()
                if x_belief_id != insert_char_id
            }
            self.add_atomunit_belieflinks_inserts(
                after_charunit=insert_charunit,
                insert_belieflink_belief_ids=non_mirror_belief_ids,
            )

    def add_atomunit_charunit_updates(
        self, before_world: WorldUnit, after_world: WorldUnit, update_char_ids: set
    ):
        for char_id in update_char_ids:
            after_charunit = after_world.get_char(char_id)
            before_charunit = before_world.get_char(char_id)
            if optional_args_different(
                "world_charunit", after_charunit, before_charunit
            ):
                x_atomunit = atomunit_shop("world_charunit", atom_update())
                x_atomunit.set_required_arg("char_id", after_charunit.char_id)
                if before_charunit.credor_weight != after_charunit.credor_weight:
                    x_atomunit.set_optional_arg(
                        "credor_weight", after_charunit.credor_weight
                    )
                if before_charunit.debtor_weight != after_charunit.debtor_weight:
                    x_atomunit.set_optional_arg(
                        "debtor_weight", after_charunit.debtor_weight
                    )
                self.set_atomunit(x_atomunit)
            self.add_atomunit_beliefunit_update_belieflinks(
                after_charunit=after_charunit, before_charunit=before_charunit
            )

    def add_atomunit_charunit_deletes(
        self, before_world: WorldUnit, delete_char_ids: set
    ):
        for delete_char_id in delete_char_ids:
            x_atomunit = atomunit_shop("world_charunit", atom_delete())
            x_atomunit.set_required_arg("char_id", delete_char_id)
            self.set_atomunit(x_atomunit)
            delete_charunit = before_world.get_char(delete_char_id)
            non_mirror_belief_ids = {
                x_belief_id
                for x_belief_id in delete_charunit._belieflinks.keys()
                if x_belief_id != delete_char_id
            }
            self.add_atomunit_belieflinks_delete(delete_char_id, non_mirror_belief_ids)

    def add_atomunit_beliefunit_update_belieflinks(
        self, after_charunit: CharUnit, before_charunit: CharUnit
    ):
        # before_non_mirror_belief_ids
        before_belief_ids = {
            x_belief_id
            for x_belief_id in before_charunit._belieflinks.keys()
            if x_belief_id != before_charunit.char_id
        }
        # after_non_mirror_belief_ids
        after_belief_ids = {
            x_belief_id
            for x_belief_id in after_charunit._belieflinks.keys()
            if x_belief_id != after_charunit.char_id
        }

        self.add_atomunit_belieflinks_inserts(
            after_charunit=after_charunit,
            insert_belieflink_belief_ids=after_belief_ids.difference(before_belief_ids),
        )

        self.add_atomunit_belieflinks_delete(
            before_char_id=after_charunit.char_id,
            before_belief_ids=before_belief_ids.difference(after_belief_ids),
        )

        update_belief_ids = before_belief_ids.intersection(after_belief_ids)
        for update_char_id in update_belief_ids:
            before_belieflink = before_charunit.get_belieflink(update_char_id)
            after_belieflink = after_charunit.get_belieflink(update_char_id)
            if optional_args_different(
                "world_char_belieflink", before_belieflink, after_belieflink
            ):
                self.add_atomunit_belieflink_update(
                    char_id=after_charunit.char_id,
                    before_belieflink=before_belieflink,
                    after_belieflink=after_belieflink,
                )

    def add_atomunit_belieflinks_inserts(
        self,
        after_charunit: CharUnit,
        insert_belieflink_belief_ids: list[BeliefID],
    ):
        after_char_id = after_charunit.char_id
        for insert_belief_id in insert_belieflink_belief_ids:
            after_belieflink = after_charunit.get_belieflink(insert_belief_id)
            x_atomunit = atomunit_shop("world_char_belieflink", atom_insert())
            x_atomunit.set_required_arg("char_id", after_char_id)
            x_atomunit.set_required_arg("belief_id", after_belieflink.belief_id)
            if after_belieflink.credor_weight != None:
                x_atomunit.set_optional_arg(
                    "credor_weight", after_belieflink.credor_weight
                )
            if after_belieflink.debtor_weight != None:
                x_atomunit.set_optional_arg(
                    "debtor_weight", after_belieflink.debtor_weight
                )
            self.set_atomunit(x_atomunit)

    def add_atomunit_belieflink_update(
        self,
        char_id: CharID,
        before_belieflink: BeliefLink,
        after_belieflink: BeliefLink,
    ):
        x_atomunit = atomunit_shop("world_char_belieflink", atom_update())
        x_atomunit.set_required_arg("char_id", char_id)
        x_atomunit.set_required_arg("belief_id", after_belieflink.belief_id)
        if after_belieflink.credor_weight != before_belieflink.credor_weight:
            x_atomunit.set_optional_arg("credor_weight", after_belieflink.credor_weight)
        if after_belieflink.debtor_weight != before_belieflink.debtor_weight:
            x_atomunit.set_optional_arg("debtor_weight", after_belieflink.debtor_weight)
        self.set_atomunit(x_atomunit)

    def add_atomunit_belieflinks_delete(
        self, before_char_id: CharID, before_belief_ids: BeliefID
    ):
        for delete_belief_id in before_belief_ids:
            x_atomunit = atomunit_shop("world_char_belieflink", atom_delete())
            x_atomunit.set_required_arg("char_id", before_char_id)
            x_atomunit.set_required_arg("belief_id", delete_belief_id)
            self.set_atomunit(x_atomunit)

    def add_atomunits_ideas(self, before_world: WorldUnit, after_world: WorldUnit):
        before_idea_roads = set(before_world._idea_dict.keys())
        after_idea_roads = set(after_world._idea_dict.keys())

        self.add_atomunit_idea_inserts(
            after_world=after_world,
            insert_idea_roads=after_idea_roads.difference(before_idea_roads),
        )
        self.add_atomunit_idea_deletes(
            before_world=before_world,
            delete_idea_roads=before_idea_roads.difference(after_idea_roads),
        )
        self.add_atomunit_idea_updates(
            before_world=before_world,
            after_world=after_world,
            update_roads=before_idea_roads.intersection(after_idea_roads),
        )

    def add_atomunit_idea_inserts(self, after_world: WorldUnit, insert_idea_roads: set):
        for insert_idea_road in insert_idea_roads:
            insert_ideaunit = after_world.get_idea_obj(insert_idea_road)
            x_atomunit = atomunit_shop("world_ideaunit", atom_insert())
            x_atomunit.set_required_arg("parent_road", insert_ideaunit._parent_road)
            x_atomunit.set_required_arg("label", insert_ideaunit._label)
            x_atomunit.set_optional_arg("_addin", insert_ideaunit._addin)
            x_atomunit.set_optional_arg("_begin", insert_ideaunit._begin)
            x_atomunit.set_optional_arg("_close", insert_ideaunit._close)
            x_atomunit.set_optional_arg("_denom", insert_ideaunit._denom)
            x_atomunit.set_optional_arg(
                "_meld_strategy", insert_ideaunit._meld_strategy
            )
            x_atomunit.set_optional_arg("_numeric_road", insert_ideaunit._numeric_road)
            x_atomunit.set_optional_arg("_numor", insert_ideaunit._numor)
            x_atomunit.set_optional_arg(
                "_range_source_road", insert_ideaunit._range_source_road
            )
            x_atomunit.set_optional_arg("_reest", insert_ideaunit._reest)
            x_atomunit.set_optional_arg("_weight", insert_ideaunit._weight)
            x_atomunit.set_optional_arg("pledge", insert_ideaunit.pledge)
            self.set_atomunit(x_atomunit)

            self.add_atomunit_idea_factunit_inserts(
                ideaunit=insert_ideaunit,
                insert_factunit_bases=set(insert_ideaunit._factunits.keys()),
            )
            self.add_atomunit_idea_awardlink_inserts(
                after_ideaunit=insert_ideaunit,
                insert_awardlink_belief_ids=set(insert_ideaunit._awardlinks.keys()),
            )
            self.add_atomunit_idea_reasonunit_inserts(
                after_ideaunit=insert_ideaunit,
                insert_reasonunit_bases=set(insert_ideaunit._reasonunits.keys()),
            )
            self.add_atomunit_idea_allyhold_insert(
                idea_road=insert_idea_road,
                insert_allyhold_belief_ids=insert_ideaunit._cultureunit._allyholds,
            )

    def add_atomunit_idea_updates(
        self, before_world: WorldUnit, after_world: WorldUnit, update_roads: set
    ):
        for idea_road in update_roads:
            after_ideaunit = after_world.get_idea_obj(idea_road)
            before_ideaunit = before_world.get_idea_obj(idea_road)
            if optional_args_different(
                "world_ideaunit", before_ideaunit, after_ideaunit
            ):
                x_atomunit = atomunit_shop("world_ideaunit", atom_update())
                x_atomunit.set_required_arg("parent_road", after_ideaunit._parent_road)
                x_atomunit.set_required_arg("label", after_ideaunit._label)
                if before_ideaunit._addin != after_ideaunit._addin:
                    x_atomunit.set_optional_arg("_addin", after_ideaunit._addin)
                if before_ideaunit._begin != after_ideaunit._begin:
                    x_atomunit.set_optional_arg("_begin", after_ideaunit._begin)
                if before_ideaunit._close != after_ideaunit._close:
                    x_atomunit.set_optional_arg("_close", after_ideaunit._close)
                if before_ideaunit._denom != after_ideaunit._denom:
                    x_atomunit.set_optional_arg("_denom", after_ideaunit._denom)
                if before_ideaunit._meld_strategy != after_ideaunit._meld_strategy:
                    x_atomunit.set_optional_arg(
                        "_meld_strategy", after_ideaunit._meld_strategy
                    )
                if before_ideaunit._numeric_road != after_ideaunit._numeric_road:
                    x_atomunit.set_optional_arg(
                        "_numeric_road", after_ideaunit._numeric_road
                    )
                if before_ideaunit._numor != after_ideaunit._numor:
                    x_atomunit.set_optional_arg("_numor", after_ideaunit._numor)
                if (
                    before_ideaunit._range_source_road
                    != after_ideaunit._range_source_road
                ):
                    x_atomunit.set_optional_arg(
                        "_range_source_road", after_ideaunit._range_source_road
                    )
                if before_ideaunit._reest != after_ideaunit._reest:
                    x_atomunit.set_optional_arg("_reest", after_ideaunit._reest)
                if before_ideaunit._weight != after_ideaunit._weight:
                    x_atomunit.set_optional_arg("_weight", after_ideaunit._weight)
                if before_ideaunit.pledge != after_ideaunit.pledge:
                    x_atomunit.set_optional_arg("pledge", after_ideaunit.pledge)
                self.set_atomunit(x_atomunit)

            # insert / update / delete factunits
            before_factunit_bases = set(before_ideaunit._factunits.keys())
            after_factunit_bases = set(after_ideaunit._factunits.keys())
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
            before_awardlinks_belief_ids = set(before_ideaunit._awardlinks.keys())
            after_awardlinks_belief_ids = set(after_ideaunit._awardlinks.keys())
            self.add_atomunit_idea_awardlink_inserts(
                after_ideaunit=after_ideaunit,
                insert_awardlink_belief_ids=after_awardlinks_belief_ids.difference(
                    before_awardlinks_belief_ids
                ),
            )
            self.add_atomunit_idea_awardlink_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_awardlink_belief_ids=before_awardlinks_belief_ids.intersection(
                    after_awardlinks_belief_ids
                ),
            )
            self.add_atomunit_idea_awardlink_deletes(
                idea_road=idea_road,
                delete_awardlink_belief_ids=before_awardlinks_belief_ids.difference(
                    after_awardlinks_belief_ids
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_bases = set(before_ideaunit._reasonunits.keys())
            after_reasonunit_bases = set(after_ideaunit._reasonunits.keys())
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

            # insert / update / delete allyholds
            before_allyholds_belief_ids = set(before_ideaunit._cultureunit._allyholds)
            after_allyholds_belief_ids = set(after_ideaunit._cultureunit._allyholds)
            self.add_atomunit_idea_allyhold_insert(
                idea_road=idea_road,
                insert_allyhold_belief_ids=after_allyholds_belief_ids.difference(
                    before_allyholds_belief_ids
                ),
            )
            self.add_atomunit_idea_allyhold_deletes(
                idea_road=idea_road,
                delete_allyhold_belief_ids=before_allyholds_belief_ids.difference(
                    after_allyholds_belief_ids
                ),
            )

    def add_atomunit_idea_deletes(
        self, before_world: WorldUnit, delete_idea_roads: set
    ):
        for delete_idea_road in delete_idea_roads:
            x_parent_road = get_parent_road(
                delete_idea_road, before_world._road_delimiter
            )
            x_label = get_terminus_node(delete_idea_road, before_world._road_delimiter)
            x_atomunit = atomunit_shop("world_ideaunit", atom_delete())
            x_atomunit.set_required_arg("parent_road", x_parent_road)
            x_atomunit.set_required_arg("label", x_label)
            self.set_atomunit(x_atomunit)

            delete_ideaunit = before_world.get_idea_obj(delete_idea_road)
            self.add_atomunit_idea_factunit_deletes(
                idea_road=delete_idea_road,
                delete_factunit_bases=set(delete_ideaunit._factunits.keys()),
            )
            self.add_atomunit_idea_awardlink_deletes(
                idea_road=delete_idea_road,
                delete_awardlink_belief_ids=set(delete_ideaunit._awardlinks.keys()),
            )
            self.add_atomunit_idea_reasonunit_deletes(
                before_ideaunit=delete_ideaunit,
                delete_reasonunit_bases=set(delete_ideaunit._reasonunits.keys()),
            )
            self.add_atomunit_idea_allyhold_deletes(
                idea_road=delete_idea_road,
                delete_allyhold_belief_ids=set(delete_ideaunit._cultureunit._allyholds),
            )

    def add_atomunit_idea_reasonunit_inserts(
        self, after_ideaunit: IdeaUnit, insert_reasonunit_bases: set
    ):
        for insert_reasonunit_base in insert_reasonunit_bases:
            after_reasonunit = after_ideaunit.get_reasonunit(insert_reasonunit_base)
            x_atomunit = atomunit_shop("world_idea_reasonunit", atom_insert())
            x_atomunit.set_required_arg("road", after_ideaunit.get_road())
            x_atomunit.set_required_arg("base", after_reasonunit.base)
            if after_reasonunit.base_idea_active_requisite != None:
                x_atomunit.set_optional_arg(
                    "base_idea_active_requisite",
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
                "world_idea_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_atomunit = atomunit_shop("world_idea_reasonunit", atom_update())
                x_atomunit.set_required_arg("road", before_ideaunit.get_road())
                x_atomunit.set_required_arg("base", after_reasonunit.base)
                if (
                    before_reasonunit.base_idea_active_requisite
                    != after_reasonunit.base_idea_active_requisite
                ):
                    x_atomunit.set_optional_arg(
                        "base_idea_active_requisite",
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
            x_atomunit = atomunit_shop("world_idea_reasonunit", atom_delete())
            x_atomunit.set_required_arg("road", before_ideaunit.get_road())
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
            x_atomunit = atomunit_shop("world_idea_reason_premiseunit", atom_insert())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("base", after_reasonunit.base)
            x_atomunit.set_required_arg("need", after_premiseunit.need)
            if after_premiseunit.open != None:
                x_atomunit.set_optional_arg("open", after_premiseunit.open)
            if after_premiseunit.nigh != None:
                x_atomunit.set_optional_arg("nigh", after_premiseunit.nigh)
            if after_premiseunit.divisor != None:
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
                "world_idea_reason_premiseunit", before_premiseunit, after_premiseunit
            ):
                x_atomunit = atomunit_shop(
                    "world_idea_reason_premiseunit", atom_update()
                )
                x_atomunit.set_required_arg("road", idea_road)
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
            x_atomunit = atomunit_shop("world_idea_reason_premiseunit", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("base", reasonunit_base)
            x_atomunit.set_required_arg("need", delete_premise_need)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_allyhold_insert(
        self, idea_road: RoadUnit, insert_allyhold_belief_ids: set
    ):
        for insert_allyhold_belief_id in insert_allyhold_belief_ids:
            x_atomunit = atomunit_shop("world_idea_allyhold", atom_insert())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("belief_id", insert_allyhold_belief_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_allyhold_deletes(
        self, idea_road: RoadUnit, delete_allyhold_belief_ids: set
    ):
        for delete_allyhold_belief_id in delete_allyhold_belief_ids:
            x_atomunit = atomunit_shop("world_idea_allyhold", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("belief_id", delete_allyhold_belief_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_awardlink_inserts(
        self, after_ideaunit: IdeaUnit, insert_awardlink_belief_ids: set
    ):
        for after_awardlink_belief_id in insert_awardlink_belief_ids:
            after_awardlink = after_ideaunit._awardlinks.get(after_awardlink_belief_id)
            x_atomunit = atomunit_shop("world_idea_awardlink", atom_insert())
            x_atomunit.set_required_arg("road", after_ideaunit.get_road())
            x_atomunit.set_required_arg("belief_id", after_awardlink.belief_id)
            x_atomunit.set_optional_arg("credor_weight", after_awardlink.credor_weight)
            x_atomunit.set_optional_arg("debtor_weight", after_awardlink.debtor_weight)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_awardlink_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_awardlink_belief_ids: set,
    ):
        for update_awardlink_belief_id in update_awardlink_belief_ids:
            before_awardlink = before_ideaunit._awardlinks.get(
                update_awardlink_belief_id
            )
            after_awardlink = after_ideaunit._awardlinks.get(update_awardlink_belief_id)
            if optional_args_different(
                "world_idea_awardlink", before_awardlink, after_awardlink
            ):
                x_atomunit = atomunit_shop("world_idea_awardlink", atom_update())
                x_atomunit.set_required_arg("road", before_ideaunit.get_road())
                x_atomunit.set_required_arg("belief_id", after_awardlink.belief_id)
                if before_awardlink.credor_weight != after_awardlink.credor_weight:
                    x_atomunit.set_optional_arg(
                        "credor_weight", after_awardlink.credor_weight
                    )
                if before_awardlink.debtor_weight != after_awardlink.debtor_weight:
                    x_atomunit.set_optional_arg(
                        "debtor_weight", after_awardlink.debtor_weight
                    )
                self.set_atomunit(x_atomunit)

    def add_atomunit_idea_awardlink_deletes(
        self, idea_road: RoadUnit, delete_awardlink_belief_ids: set
    ):
        for delete_awardlink_belief_id in delete_awardlink_belief_ids:
            x_atomunit = atomunit_shop("world_idea_awardlink", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("belief_id", delete_awardlink_belief_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_inserts(
        self, ideaunit: IdeaUnit, insert_factunit_bases: set
    ):
        for insert_factunit_base in insert_factunit_bases:
            insert_factunit = ideaunit._factunits.get(insert_factunit_base)
            x_atomunit = atomunit_shop("world_idea_factunit", atom_insert())
            x_atomunit.set_required_arg("road", ideaunit.get_road())
            x_atomunit.set_required_arg("base", insert_factunit.base)
            if insert_factunit.pick != None:
                x_atomunit.set_optional_arg("pick", insert_factunit.pick)
            if insert_factunit.open != None:
                x_atomunit.set_optional_arg("open", insert_factunit.open)
            if insert_factunit.nigh != None:
                x_atomunit.set_optional_arg("nigh", insert_factunit.nigh)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_factunit_bases: set,
    ):
        for update_factunit_base in update_factunit_bases:
            before_factunit = before_ideaunit._factunits.get(update_factunit_base)
            after_factunit = after_ideaunit._factunits.get(update_factunit_base)
            if optional_args_different(
                "world_idea_factunit", before_factunit, after_factunit
            ):
                x_atomunit = atomunit_shop("world_idea_factunit", atom_update())
                x_atomunit.set_required_arg("road", before_ideaunit.get_road())
                x_atomunit.set_required_arg("base", after_factunit.base)
                if before_factunit.pick != after_factunit.pick:
                    x_atomunit.set_optional_arg("pick", after_factunit.pick)
                if before_factunit.open != after_factunit.open:
                    x_atomunit.set_optional_arg("open", after_factunit.open)
                if before_factunit.nigh != after_factunit.nigh:
                    x_atomunit.set_optional_arg("nigh", after_factunit.nigh)
                self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_deletes(
        self, idea_road: RoadUnit, delete_factunit_bases: FactUnit
    ):
        for delete_factunit_base in delete_factunit_bases:
            x_atomunit = atomunit_shop("world_idea_factunit", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
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
        _world_build_validated=False,
    )


def world_built_from_change_is_valid(
    x_change: ChangeUnit, x_world: WorldUnit = None
) -> bool:
    if x_world is None:
        x_world = worldunit_shop()

    x_world = x_change.get_edited_world(x_world)

    try:
        x_world.calc_world_metrics()
    except Exception:
        return False

    return True


def get_filtered_changeunit(
    x_changeunit: ChangeUnit, category_set: set[str], curd_set: set[str]
) -> ChangeUnit:
    new_changeunit = changeunit_shop()
    for x_atomunit in x_changeunit.get_sorted_atomunits():
        if x_atomunit.crud_text in curd_set and x_atomunit.category in category_set:
            new_changeunit.set_atomunit(x_atomunit)
    return new_changeunit
