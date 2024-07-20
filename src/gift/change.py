from src._instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    place_obj_in_dict,
    get_nested_value,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src.bud.reason_idea import FactUnit, ReasonUnit
from src.bud.acct import LobbyShip, AcctID, AcctUnit
from src.bud.lobby import LobbyShip, LobbyID
from src.bud.idea import IdeaUnit
from src.bud.bud import BudUnit, budunit_shop
from src.gift.atom_config import CRUD_command
from src.gift.atom import (
    AtomUnit,
    atomunit_shop,
    modify_bud_with_atomunit,
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
            if x_list[0].required_args.get("parent_road") is not None:
                x_list = sorted(
                    x_list, key=lambda x: x.required_args.get("parent_road")
                )
            if x_list[0].required_args.get("road") is not None:
                x_list = sorted(x_list, key=lambda x: x.required_args.get("road"))
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

    def add_all_atomunits(self, after_bud: BudUnit):
        before_bud = budunit_shop(after_bud._owner_id, after_bud._real_id)
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
        if not optional_args_different("budunit", before_bud, after_bud):
            return
        x_atomunit = atomunit_shop("budunit", atom_update())
        if before_bud._max_tree_traverse != after_bud._max_tree_traverse:
            x_atomunit.set_optional_arg(
                "_max_tree_traverse", after_bud._max_tree_traverse
            )
        if before_bud._monetary_desc != after_bud._monetary_desc:
            x_atomunit.set_optional_arg("_monetary_desc", after_bud._monetary_desc)
        if before_bud._credor_respect != after_bud._credor_respect:
            x_atomunit.set_optional_arg("_credor_respect", after_bud._credor_respect)
        if before_bud._debtor_respect != after_bud._debtor_respect:
            x_atomunit.set_optional_arg("_debtor_respect", after_bud._debtor_respect)
        if before_bud._weight != after_bud._weight:
            x_atomunit.set_optional_arg("_weight", after_bud._weight)
        if before_bud._fund_pool != after_bud._fund_pool:
            x_atomunit.set_optional_arg("_fund_pool", after_bud._fund_pool)
        if before_bud._fund_coin != after_bud._fund_coin:
            x_atomunit.set_optional_arg("_fund_coin", after_bud._fund_coin)
        if before_bud._bit != after_bud._bit:
            x_atomunit.set_optional_arg("_bit", after_bud._bit)
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
            x_atomunit = atomunit_shop("bud_acctunit", atom_insert())
            x_atomunit.set_required_arg("acct_id", insert_acctunit.acct_id)
            if insert_acctunit.credor_weight is not None:
                x_atomunit.set_optional_arg(
                    "credor_weight", insert_acctunit.credor_weight
                )
            if insert_acctunit.debtor_weight is not None:
                x_atomunit.set_optional_arg(
                    "debtor_weight", insert_acctunit.debtor_weight
                )
            self.set_atomunit(x_atomunit)
            all_lobby_ids = set(insert_acctunit._lobbyships.keys())
            self.add_atomunit_lobbyships_inserts(
                after_acctunit=insert_acctunit,
                insert_lobbyship_lobby_ids=all_lobby_ids,
            )

    def add_atomunit_acctunit_updates(
        self, before_bud: BudUnit, after_bud: BudUnit, update_acct_ids: set
    ):
        for acct_id in update_acct_ids:
            after_acctunit = after_bud.get_acct(acct_id)
            before_acctunit = before_bud.get_acct(acct_id)
            if optional_args_different("bud_acctunit", after_acctunit, before_acctunit):
                x_atomunit = atomunit_shop("bud_acctunit", atom_update())
                x_atomunit.set_required_arg("acct_id", after_acctunit.acct_id)
                if before_acctunit.credor_weight != after_acctunit.credor_weight:
                    x_atomunit.set_optional_arg(
                        "credor_weight", after_acctunit.credor_weight
                    )
                if before_acctunit.debtor_weight != after_acctunit.debtor_weight:
                    x_atomunit.set_optional_arg(
                        "debtor_weight", after_acctunit.debtor_weight
                    )
                self.set_atomunit(x_atomunit)
            self.add_atomunit_acctunit_update_lobbyships(
                after_acctunit=after_acctunit, before_acctunit=before_acctunit
            )

    def add_atomunit_acctunit_deletes(self, before_bud: BudUnit, delete_acct_ids: set):
        for delete_acct_id in delete_acct_ids:
            x_atomunit = atomunit_shop("bud_acctunit", atom_delete())
            x_atomunit.set_required_arg("acct_id", delete_acct_id)
            self.set_atomunit(x_atomunit)
            delete_acctunit = before_bud.get_acct(delete_acct_id)
            non_mirror_lobby_ids = {
                x_lobby_id
                for x_lobby_id in delete_acctunit._lobbyships.keys()
                if x_lobby_id != delete_acct_id
            }
            self.add_atomunit_lobbyships_delete(delete_acct_id, non_mirror_lobby_ids)

    def add_atomunit_acctunit_update_lobbyships(
        self, after_acctunit: AcctUnit, before_acctunit: AcctUnit
    ):
        # before_non_mirror_lobby_ids
        before_lobby_ids = {
            x_lobby_id
            for x_lobby_id in before_acctunit._lobbyships.keys()
            if x_lobby_id != before_acctunit.acct_id
        }
        # after_non_mirror_lobby_ids
        after_lobby_ids = {
            x_lobby_id
            for x_lobby_id in after_acctunit._lobbyships.keys()
            if x_lobby_id != after_acctunit.acct_id
        }

        self.add_atomunit_lobbyships_inserts(
            after_acctunit=after_acctunit,
            insert_lobbyship_lobby_ids=after_lobby_ids.difference(before_lobby_ids),
        )

        self.add_atomunit_lobbyships_delete(
            before_acct_id=after_acctunit.acct_id,
            before_lobby_ids=before_lobby_ids.difference(after_lobby_ids),
        )

        update_lobby_ids = before_lobby_ids.intersection(after_lobby_ids)
        for update_acct_id in update_lobby_ids:
            before_lobbyship = before_acctunit.get_lobbyship(update_acct_id)
            after_lobbyship = after_acctunit.get_lobbyship(update_acct_id)
            if optional_args_different(
                "bud_acct_lobbyship", before_lobbyship, after_lobbyship
            ):
                self.add_atomunit_lobbyship_update(
                    acct_id=after_acctunit.acct_id,
                    before_lobbyship=before_lobbyship,
                    after_lobbyship=after_lobbyship,
                )

    def add_atomunit_lobbyships_inserts(
        self,
        after_acctunit: AcctUnit,
        insert_lobbyship_lobby_ids: list[LobbyID],
    ):
        after_acct_id = after_acctunit.acct_id
        for insert_lobby_id in insert_lobbyship_lobby_ids:
            after_lobbyship = after_acctunit.get_lobbyship(insert_lobby_id)
            x_atomunit = atomunit_shop("bud_acct_lobbyship", atom_insert())
            x_atomunit.set_required_arg("acct_id", after_acct_id)
            x_atomunit.set_required_arg("lobby_id", after_lobbyship.lobby_id)
            if after_lobbyship.credor_weight is not None:
                x_atomunit.set_optional_arg(
                    "credor_weight", after_lobbyship.credor_weight
                )
            if after_lobbyship.debtor_weight is not None:
                x_atomunit.set_optional_arg(
                    "debtor_weight", after_lobbyship.debtor_weight
                )
            self.set_atomunit(x_atomunit)

    def add_atomunit_lobbyship_update(
        self,
        acct_id: AcctID,
        before_lobbyship: LobbyShip,
        after_lobbyship: LobbyShip,
    ):
        x_atomunit = atomunit_shop("bud_acct_lobbyship", atom_update())
        x_atomunit.set_required_arg("acct_id", acct_id)
        x_atomunit.set_required_arg("lobby_id", after_lobbyship.lobby_id)
        if after_lobbyship.credor_weight != before_lobbyship.credor_weight:
            x_atomunit.set_optional_arg("credor_weight", after_lobbyship.credor_weight)
        if after_lobbyship.debtor_weight != before_lobbyship.debtor_weight:
            x_atomunit.set_optional_arg("debtor_weight", after_lobbyship.debtor_weight)
        self.set_atomunit(x_atomunit)

    def add_atomunit_lobbyships_delete(
        self, before_acct_id: AcctID, before_lobby_ids: LobbyID
    ):
        for delete_lobby_id in before_lobby_ids:
            x_atomunit = atomunit_shop("bud_acct_lobbyship", atom_delete())
            x_atomunit.set_required_arg("acct_id", before_acct_id)
            x_atomunit.set_required_arg("lobby_id", delete_lobby_id)
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
            x_atomunit = atomunit_shop("bud_ideaunit", atom_insert())
            x_atomunit.set_required_arg("parent_road", insert_ideaunit._parent_road)
            x_atomunit.set_required_arg("label", insert_ideaunit._label)
            x_atomunit.set_optional_arg("_addin", insert_ideaunit._addin)
            x_atomunit.set_optional_arg("_begin", insert_ideaunit._begin)
            x_atomunit.set_optional_arg("_close", insert_ideaunit._close)
            x_atomunit.set_optional_arg("_denom", insert_ideaunit._denom)
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
                insert_awardlink_lobby_ids=set(insert_ideaunit._awardlinks.keys()),
            )
            self.add_atomunit_idea_reasonunit_inserts(
                after_ideaunit=insert_ideaunit,
                insert_reasonunit_bases=set(insert_ideaunit._reasonunits.keys()),
            )
            self.add_atomunit_idea_lobbyhold_insert(
                idea_road=insert_idea_road,
                insert_lobbyhold_lobby_ids=insert_ideaunit._doerunit._lobbyholds,
            )

    def add_atomunit_idea_updates(
        self, before_bud: BudUnit, after_bud: BudUnit, update_roads: set
    ):
        for idea_road in update_roads:
            after_ideaunit = after_bud.get_idea_obj(idea_road)
            before_ideaunit = before_bud.get_idea_obj(idea_road)
            if optional_args_different("bud_ideaunit", before_ideaunit, after_ideaunit):
                x_atomunit = atomunit_shop("bud_ideaunit", atom_update())
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
            before_awardlinks_lobby_ids = set(before_ideaunit._awardlinks.keys())
            after_awardlinks_lobby_ids = set(after_ideaunit._awardlinks.keys())
            self.add_atomunit_idea_awardlink_inserts(
                after_ideaunit=after_ideaunit,
                insert_awardlink_lobby_ids=after_awardlinks_lobby_ids.difference(
                    before_awardlinks_lobby_ids
                ),
            )
            self.add_atomunit_idea_awardlink_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_awardlink_lobby_ids=before_awardlinks_lobby_ids.intersection(
                    after_awardlinks_lobby_ids
                ),
            )
            self.add_atomunit_idea_awardlink_deletes(
                idea_road=idea_road,
                delete_awardlink_lobby_ids=before_awardlinks_lobby_ids.difference(
                    after_awardlinks_lobby_ids
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

            # insert / update / delete lobbyholds
            before_lobbyholds_lobby_ids = set(before_ideaunit._doerunit._lobbyholds)
            after_lobbyholds_lobby_ids = set(after_ideaunit._doerunit._lobbyholds)
            self.add_atomunit_idea_lobbyhold_insert(
                idea_road=idea_road,
                insert_lobbyhold_lobby_ids=after_lobbyholds_lobby_ids.difference(
                    before_lobbyholds_lobby_ids
                ),
            )
            self.add_atomunit_idea_lobbyhold_deletes(
                idea_road=idea_road,
                delete_lobbyhold_lobby_ids=before_lobbyholds_lobby_ids.difference(
                    after_lobbyholds_lobby_ids
                ),
            )

    def add_atomunit_idea_deletes(self, before_bud: BudUnit, delete_idea_roads: set):
        for delete_idea_road in delete_idea_roads:
            x_parent_road = get_parent_road(
                delete_idea_road, before_bud._road_delimiter
            )
            x_label = get_terminus_node(delete_idea_road, before_bud._road_delimiter)
            x_atomunit = atomunit_shop("bud_ideaunit", atom_delete())
            x_atomunit.set_required_arg("parent_road", x_parent_road)
            x_atomunit.set_required_arg("label", x_label)
            self.set_atomunit(x_atomunit)

            delete_ideaunit = before_bud.get_idea_obj(delete_idea_road)
            self.add_atomunit_idea_factunit_deletes(
                idea_road=delete_idea_road,
                delete_factunit_bases=set(delete_ideaunit._factunits.keys()),
            )
            self.add_atomunit_idea_awardlink_deletes(
                idea_road=delete_idea_road,
                delete_awardlink_lobby_ids=set(delete_ideaunit._awardlinks.keys()),
            )
            self.add_atomunit_idea_reasonunit_deletes(
                before_ideaunit=delete_ideaunit,
                delete_reasonunit_bases=set(delete_ideaunit._reasonunits.keys()),
            )
            self.add_atomunit_idea_lobbyhold_deletes(
                idea_road=delete_idea_road,
                delete_lobbyhold_lobby_ids=set(delete_ideaunit._doerunit._lobbyholds),
            )

    def add_atomunit_idea_reasonunit_inserts(
        self, after_ideaunit: IdeaUnit, insert_reasonunit_bases: set
    ):
        for insert_reasonunit_base in insert_reasonunit_bases:
            after_reasonunit = after_ideaunit.get_reasonunit(insert_reasonunit_base)
            x_atomunit = atomunit_shop("bud_idea_reasonunit", atom_insert())
            x_atomunit.set_required_arg("road", after_ideaunit.get_road())
            x_atomunit.set_required_arg("base", after_reasonunit.base)
            if after_reasonunit.base_idea_active_requisite is not None:
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
                "bud_idea_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_atomunit = atomunit_shop("bud_idea_reasonunit", atom_update())
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
            x_atomunit = atomunit_shop("bud_idea_reasonunit", atom_delete())
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
            x_atomunit = atomunit_shop("bud_idea_reason_premiseunit", atom_insert())
            x_atomunit.set_required_arg("road", idea_road)
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
                "bud_idea_reason_premiseunit", before_premiseunit, after_premiseunit
            ):
                x_atomunit = atomunit_shop("bud_idea_reason_premiseunit", atom_update())
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
            x_atomunit = atomunit_shop("bud_idea_reason_premiseunit", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("base", reasonunit_base)
            x_atomunit.set_required_arg("need", delete_premise_need)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_lobbyhold_insert(
        self, idea_road: RoadUnit, insert_lobbyhold_lobby_ids: set
    ):
        for insert_lobbyhold_lobby_id in insert_lobbyhold_lobby_ids:
            x_atomunit = atomunit_shop("bud_idea_lobbyhold", atom_insert())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("lobby_id", insert_lobbyhold_lobby_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_lobbyhold_deletes(
        self, idea_road: RoadUnit, delete_lobbyhold_lobby_ids: set
    ):
        for delete_lobbyhold_lobby_id in delete_lobbyhold_lobby_ids:
            x_atomunit = atomunit_shop("bud_idea_lobbyhold", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("lobby_id", delete_lobbyhold_lobby_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_awardlink_inserts(
        self, after_ideaunit: IdeaUnit, insert_awardlink_lobby_ids: set
    ):
        for after_awardlink_lobby_id in insert_awardlink_lobby_ids:
            after_awardlink = after_ideaunit._awardlinks.get(after_awardlink_lobby_id)
            x_atomunit = atomunit_shop("bud_idea_awardlink", atom_insert())
            x_atomunit.set_required_arg("road", after_ideaunit.get_road())
            x_atomunit.set_required_arg("lobby_id", after_awardlink.lobby_id)
            x_atomunit.set_optional_arg("give_weight", after_awardlink.give_weight)
            x_atomunit.set_optional_arg("take_weight", after_awardlink.take_weight)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_awardlink_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_awardlink_lobby_ids: set,
    ):
        for update_awardlink_lobby_id in update_awardlink_lobby_ids:
            before_awardlink = before_ideaunit._awardlinks.get(
                update_awardlink_lobby_id
            )
            after_awardlink = after_ideaunit._awardlinks.get(update_awardlink_lobby_id)
            if optional_args_different(
                "bud_idea_awardlink", before_awardlink, after_awardlink
            ):
                x_atomunit = atomunit_shop("bud_idea_awardlink", atom_update())
                x_atomunit.set_required_arg("road", before_ideaunit.get_road())
                x_atomunit.set_required_arg("lobby_id", after_awardlink.lobby_id)
                if before_awardlink.give_weight != after_awardlink.give_weight:
                    x_atomunit.set_optional_arg(
                        "give_weight", after_awardlink.give_weight
                    )
                if before_awardlink.take_weight != after_awardlink.take_weight:
                    x_atomunit.set_optional_arg(
                        "take_weight", after_awardlink.take_weight
                    )
                self.set_atomunit(x_atomunit)

    def add_atomunit_idea_awardlink_deletes(
        self, idea_road: RoadUnit, delete_awardlink_lobby_ids: set
    ):
        for delete_awardlink_lobby_id in delete_awardlink_lobby_ids:
            x_atomunit = atomunit_shop("bud_idea_awardlink", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("lobby_id", delete_awardlink_lobby_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_inserts(
        self, ideaunit: IdeaUnit, insert_factunit_bases: set
    ):
        for insert_factunit_base in insert_factunit_bases:
            insert_factunit = ideaunit._factunits.get(insert_factunit_base)
            x_atomunit = atomunit_shop("bud_idea_factunit", atom_insert())
            x_atomunit.set_required_arg("road", ideaunit.get_road())
            x_atomunit.set_required_arg("base", insert_factunit.base)
            if insert_factunit.pick is not None:
                x_atomunit.set_optional_arg("pick", insert_factunit.pick)
            if insert_factunit.open is not None:
                x_atomunit.set_optional_arg("open", insert_factunit.open)
            if insert_factunit.nigh is not None:
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
                "bud_idea_factunit", before_factunit, after_factunit
            ):
                x_atomunit = atomunit_shop("bud_idea_factunit", atom_update())
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
            x_atomunit = atomunit_shop("bud_idea_factunit", atom_delete())
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
        if x_atomunit.crud_text in curd_set and x_atomunit.category in category_set:
            new_changeunit.set_atomunit(x_atomunit)
    return new_changeunit
