from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_all_nondictionary_objs,
    get_empty_dict_if_None,
    get_from_nested_dict,
    get_json_from_dict,
    set_in_nested_dict,
)
from src.ch01_rope_logic.term import RopePointer, TitleTerm
from src.ch03_group_logic.group import MemberShip
from src.ch03_group_logic.voice import MemberShip, VoiceName, VoiceUnit
from src.ch04_reason_logic.reason import FactUnit, ReasonUnit
from src.ch05_plan_logic.plan import PlanUnit
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch09_belief_atom_logic.atom_config import CRUD_command
from src.ch09_belief_atom_logic.atom_main import (
    BeliefAtom,
    InvalidBeliefAtomException,
    beliefatom_shop,
    get_from_dict as get_beliefatom_from_dict,
    jvalues_different,
    modify_belief_with_beliefatom,
    sift_beliefatom,
)


@dataclass
class BeliefDelta:
    beliefatoms: dict[CRUD_command : dict[str, BeliefAtom]] = None
    _belief_build_validated: bool = None

    def _get_crud_beliefatoms_list(self) -> dict[CRUD_command, list[BeliefAtom]]:
        return get_all_nondictionary_objs(self.beliefatoms)

    def get_dimen_sorted_beliefatoms_list(self) -> list[BeliefAtom]:
        atoms_list = []
        for crud_list in self._get_crud_beliefatoms_list().values():
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

    def get_sorted_beliefatoms(self) -> list[BeliefAtom]:
        beliefatoms_list = self.get_dimen_sorted_beliefatoms_list()
        return sorted(beliefatoms_list, key=lambda x: x.atom_order)

    def get_edited_belief(self, before_belief: BeliefUnit) -> BeliefUnit:
        edited_belief = copy_deepcopy(before_belief)
        for x_beliefatom in self.get_sorted_beliefatoms():
            modify_belief_with_beliefatom(edited_belief, x_beliefatom)
        return edited_belief

    def set_beliefatom(self, x_beliefatom: BeliefAtom):
        if x_beliefatom.is_valid() is False:
            raise InvalidBeliefAtomException(
                f"""'{x_beliefatom.dimen}' {x_beliefatom.crud_str} BeliefAtom is invalid
                {x_beliefatom.is_jkeys_valid()=}
                {x_beliefatom.is_jvalues_valid()=}"""
            )

        x_beliefatom.set_atom_order()
        x_keylist = [
            x_beliefatom.crud_str,
            x_beliefatom.dimen,
            *x_beliefatom.get_nesting_order_args(),
        ]
        set_in_nested_dict(self.beliefatoms, x_keylist, x_beliefatom)

    def beliefatom_exists(self, x_beliefatom: BeliefAtom) -> bool:
        if x_beliefatom.is_valid() is False:
            raise InvalidBeliefAtomException(
                f"""'{x_beliefatom.dimen}' {x_beliefatom.crud_str} BeliefAtom is invalid
                {x_beliefatom.is_jkeys_valid()=}
                {x_beliefatom.is_jvalues_valid()=}"""
            )

        x_beliefatom.set_atom_order()
        x_keylist = [
            x_beliefatom.crud_str,
            x_beliefatom.dimen,
            *list(x_beliefatom.get_nesting_order_args()),
        ]
        nested_beliefatom = get_from_nested_dict(self.beliefatoms, x_keylist, True)
        return nested_beliefatom == x_beliefatom

    def add_beliefatom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        x_beliefatom = beliefatom_shop(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=jkeys,
            jvalues=jvalues,
        )
        self.set_beliefatom(x_beliefatom)

    def get_beliefatom(self, crud_str: str, dimen: str, jkeys: list[str]) -> BeliefAtom:
        x_keylist = [crud_str, dimen, *jkeys]
        return get_from_nested_dict(self.beliefatoms, x_keylist)

    def add_all_beliefatoms(self, after_belief: BeliefUnit):
        before_belief = beliefunit_shop(
            after_belief.belief_name, after_belief.moment_label
        )
        self.add_all_different_beliefatoms(before_belief, after_belief)

    def add_all_different_beliefatoms(
        self, before_belief: BeliefUnit, after_belief: BeliefUnit
    ):
        before_belief.cashout()
        after_belief.cashout()
        self.add_beliefatoms_beliefunit_simple_attrs(before_belief, after_belief)
        self.add_beliefatoms_voices(before_belief, after_belief)
        self.add_beliefatoms_plans(before_belief, after_belief)

    def add_beliefatoms_beliefunit_simple_attrs(
        self, before_belief: BeliefUnit, after_belief: BeliefUnit
    ):
        if not jvalues_different("beliefunit", before_belief, after_belief):
            return
        x_beliefatom = beliefatom_shop("beliefunit", "UPDATE")
        if before_belief.max_tree_traverse != after_belief.max_tree_traverse:
            x_beliefatom.set_jvalue("max_tree_traverse", after_belief.max_tree_traverse)
        if before_belief.credor_respect != after_belief.credor_respect:
            x_beliefatom.set_jvalue("credor_respect", after_belief.credor_respect)
        if before_belief.debtor_respect != after_belief.debtor_respect:
            x_beliefatom.set_jvalue("debtor_respect", after_belief.debtor_respect)
        if before_belief.tally != after_belief.tally:
            x_beliefatom.set_jvalue("tally", after_belief.tally)
        if before_belief.fund_pool != after_belief.fund_pool:
            x_beliefatom.set_jvalue("fund_pool", after_belief.fund_pool)
        if before_belief.fund_iota != after_belief.fund_iota:
            x_beliefatom.set_jvalue("fund_iota", after_belief.fund_iota)
        if before_belief.respect_bit != after_belief.respect_bit:
            x_beliefatom.set_jvalue("respect_bit", after_belief.respect_bit)
        self.set_beliefatom(x_beliefatom)

    def add_beliefatoms_voices(
        self, before_belief: BeliefUnit, after_belief: BeliefUnit
    ):
        before_voice_names = set(before_belief.voices.keys())
        after_voice_names = set(after_belief.voices.keys())

        self.add_beliefatom_voiceunit_inserts(
            after_belief=after_belief,
            insert_voice_names=after_voice_names.difference(before_voice_names),
        )
        self.add_beliefatom_voiceunit_deletes(
            before_belief=before_belief,
            delete_voice_names=before_voice_names.difference(after_voice_names),
        )
        self.add_beliefatom_voiceunit_updates(
            before_belief=before_belief,
            after_belief=after_belief,
            update_voice_names=before_voice_names.intersection(after_voice_names),
        )

    def add_beliefatom_voiceunit_inserts(
        self, after_belief: BeliefUnit, insert_voice_names: set
    ):
        for insert_voice_name in insert_voice_names:
            insert_voiceunit = after_belief.get_voice(insert_voice_name)
            x_beliefatom = beliefatom_shop("belief_voiceunit", "INSERT")
            x_beliefatom.set_jkey("voice_name", insert_voiceunit.voice_name)
            if insert_voiceunit.voice_cred_points is not None:
                x_beliefatom.set_jvalue(
                    "voice_cred_points", insert_voiceunit.voice_cred_points
                )
            if insert_voiceunit.voice_debt_points is not None:
                x_beliefatom.set_jvalue(
                    "voice_debt_points", insert_voiceunit.voice_debt_points
                )
            self.set_beliefatom(x_beliefatom)
            all_group_titles = set(insert_voiceunit.memberships.keys())
            self.add_beliefatom_memberships_inserts(
                after_voiceunit=insert_voiceunit,
                insert_membership_group_titles=all_group_titles,
            )

    def add_beliefatom_voiceunit_updates(
        self,
        before_belief: BeliefUnit,
        after_belief: BeliefUnit,
        update_voice_names: set,
    ):
        for voice_name in update_voice_names:
            after_voiceunit = after_belief.get_voice(voice_name)
            before_voiceunit = before_belief.get_voice(voice_name)
            if jvalues_different("belief_voiceunit", after_voiceunit, before_voiceunit):
                x_beliefatom = beliefatom_shop("belief_voiceunit", "UPDATE")
                x_beliefatom.set_jkey("voice_name", after_voiceunit.voice_name)
                if (
                    before_voiceunit.voice_cred_points
                    != after_voiceunit.voice_cred_points
                ):
                    x_beliefatom.set_jvalue(
                        "voice_cred_points", after_voiceunit.voice_cred_points
                    )
                if (
                    before_voiceunit.voice_debt_points
                    != after_voiceunit.voice_debt_points
                ):
                    x_beliefatom.set_jvalue(
                        "voice_debt_points", after_voiceunit.voice_debt_points
                    )
                self.set_beliefatom(x_beliefatom)
            self.add_beliefatom_voiceunit_update_memberships(
                after_voiceunit=after_voiceunit,
                before_voiceunit=before_voiceunit,
            )

    def add_beliefatom_voiceunit_deletes(
        self, before_belief: BeliefUnit, delete_voice_names: set
    ):
        for delete_voice_name in delete_voice_names:
            x_beliefatom = beliefatom_shop("belief_voiceunit", "DELETE")
            x_beliefatom.set_jkey("voice_name", delete_voice_name)
            self.set_beliefatom(x_beliefatom)
            delete_voiceunit = before_belief.get_voice(delete_voice_name)
            non_mirror_group_titles = {
                x_group_title
                for x_group_title in delete_voiceunit.memberships.keys()
                if x_group_title != delete_voice_name
            }
            self.add_beliefatom_memberships_delete(
                delete_voice_name, non_mirror_group_titles
            )

    def add_beliefatom_voiceunit_update_memberships(
        self, after_voiceunit: VoiceUnit, before_voiceunit: VoiceUnit
    ):
        # before_non_mirror_group_titles
        before_group_titles = {
            x_group_title
            for x_group_title in before_voiceunit.memberships.keys()
            if x_group_title != before_voiceunit.voice_name
        }
        # after_non_mirror_group_titles
        after_group_titles = {
            x_group_title
            for x_group_title in after_voiceunit.memberships.keys()
            if x_group_title != after_voiceunit.voice_name
        }

        self.add_beliefatom_memberships_inserts(
            after_voiceunit=after_voiceunit,
            insert_membership_group_titles=after_group_titles.difference(
                before_group_titles
            ),
        )

        self.add_beliefatom_memberships_delete(
            before_voice_name=after_voiceunit.voice_name,
            before_group_titles=before_group_titles.difference(after_group_titles),
        )

        update_group_titles = before_group_titles.intersection(after_group_titles)
        for update_voice_name in update_group_titles:
            before_membership = before_voiceunit.get_membership(update_voice_name)
            after_membership = after_voiceunit.get_membership(update_voice_name)
            if jvalues_different(
                "belief_voice_membership", before_membership, after_membership
            ):
                self.add_beliefatom_membership_update(
                    voice_name=after_voiceunit.voice_name,
                    before_membership=before_membership,
                    after_membership=after_membership,
                )

    def add_beliefatom_memberships_inserts(
        self,
        after_voiceunit: VoiceUnit,
        insert_membership_group_titles: list[TitleTerm],
    ):
        after_voice_name = after_voiceunit.voice_name
        for insert_group_title in insert_membership_group_titles:
            after_membership = after_voiceunit.get_membership(insert_group_title)
            x_beliefatom = beliefatom_shop("belief_voice_membership", "INSERT")
            x_beliefatom.set_jkey("voice_name", after_voice_name)
            x_beliefatom.set_jkey("group_title", after_membership.group_title)
            if after_membership.group_cred_points is not None:
                x_beliefatom.set_jvalue(
                    "group_cred_points", after_membership.group_cred_points
                )
            if after_membership.group_debt_points is not None:
                x_beliefatom.set_jvalue(
                    "group_debt_points", after_membership.group_debt_points
                )
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_membership_update(
        self,
        voice_name: VoiceName,
        before_membership: MemberShip,
        after_membership: MemberShip,
    ):
        x_beliefatom = beliefatom_shop("belief_voice_membership", "UPDATE")
        x_beliefatom.set_jkey("voice_name", voice_name)
        x_beliefatom.set_jkey("group_title", after_membership.group_title)
        if after_membership.group_cred_points != before_membership.group_cred_points:
            x_beliefatom.set_jvalue(
                "group_cred_points", after_membership.group_cred_points
            )
        if after_membership.group_debt_points != before_membership.group_debt_points:
            x_beliefatom.set_jvalue(
                "group_debt_points", after_membership.group_debt_points
            )
        self.set_beliefatom(x_beliefatom)

    def add_beliefatom_memberships_delete(
        self, before_voice_name: VoiceName, before_group_titles: TitleTerm
    ):
        for delete_group_title in before_group_titles:
            x_beliefatom = beliefatom_shop("belief_voice_membership", "DELETE")
            x_beliefatom.set_jkey("voice_name", before_voice_name)
            x_beliefatom.set_jkey("group_title", delete_group_title)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatoms_plans(
        self, before_belief: BeliefUnit, after_belief: BeliefUnit
    ):
        before_plan_ropes = set(before_belief._plan_dict.keys())
        after_plan_ropes = set(after_belief._plan_dict.keys())

        self.add_beliefatom_plan_inserts(
            after_belief=after_belief,
            insert_plan_ropes=after_plan_ropes.difference(before_plan_ropes),
        )
        self.add_beliefatom_plan_deletes(
            before_belief=before_belief,
            delete_plan_ropes=before_plan_ropes.difference(after_plan_ropes),
        )
        self.add_beliefatom_plan_updates(
            before_belief=before_belief,
            after_belief=after_belief,
            update_ropes=before_plan_ropes.intersection(after_plan_ropes),
        )

    def add_beliefatom_plan_inserts(
        self, after_belief: BeliefUnit, insert_plan_ropes: set
    ):
        for insert_plan_rope in insert_plan_ropes:
            insert_planunit = after_belief.get_plan_obj(insert_plan_rope)
            x_beliefatom = beliefatom_shop("belief_planunit", "INSERT")
            x_beliefatom.set_jkey("plan_rope", insert_planunit.get_plan_rope())
            x_beliefatom.set_jvalue("addin", insert_planunit.addin)
            x_beliefatom.set_jvalue("begin", insert_planunit.begin)
            x_beliefatom.set_jvalue("close", insert_planunit.close)
            x_beliefatom.set_jvalue("denom", insert_planunit.denom)
            x_beliefatom.set_jvalue("numor", insert_planunit.numor)
            x_beliefatom.set_jvalue("morph", insert_planunit.morph)
            x_beliefatom.set_jvalue("star", insert_planunit.star)
            x_beliefatom.set_jvalue("task", insert_planunit.task)
            self.set_beliefatom(x_beliefatom)

            self.add_beliefatom_plan_factunit_inserts(
                planunit=insert_planunit,
                insert_factunit_reason_contexts=set(insert_planunit.factunits.keys()),
            )
            self.add_beliefatom_plan_awardunit_inserts(
                after_planunit=insert_planunit,
                insert_awardunit_awardee_titles=set(insert_planunit.awardunits.keys()),
            )
            self.add_beliefatom_plan_reasonunit_inserts(
                after_planunit=insert_planunit,
                insert_reasonunit_reason_contexts=set(
                    insert_planunit.reasonunits.keys()
                ),
            )
            self.add_beliefatom_plan_partyunit_insert(
                plan_rope=insert_plan_rope,
                insert_partyunit_party_titles=insert_planunit.laborunit._partys,
            )
            self.add_beliefatom_plan_healerunit_insert(
                plan_rope=insert_plan_rope,
                insert_healerunit_healer_names=insert_planunit.healerunit._healer_names,
            )

    def add_beliefatom_plan_updates(
        self,
        before_belief: BeliefUnit,
        after_belief: BeliefUnit,
        update_ropes: set,
    ):
        for plan_rope in update_ropes:
            after_planunit = after_belief.get_plan_obj(plan_rope)
            before_planunit = before_belief.get_plan_obj(plan_rope)
            if jvalues_different("belief_planunit", before_planunit, after_planunit):
                x_beliefatom = beliefatom_shop("belief_planunit", "UPDATE")
                x_beliefatom.set_jkey("plan_rope", after_planunit.get_plan_rope())
                if before_planunit.addin != after_planunit.addin:
                    x_beliefatom.set_jvalue("addin", after_planunit.addin)
                if before_planunit.begin != after_planunit.begin:
                    x_beliefatom.set_jvalue("begin", after_planunit.begin)
                if before_planunit.close != after_planunit.close:
                    x_beliefatom.set_jvalue("close", after_planunit.close)
                if before_planunit.denom != after_planunit.denom:
                    x_beliefatom.set_jvalue("denom", after_planunit.denom)
                if before_planunit.numor != after_planunit.numor:
                    x_beliefatom.set_jvalue("numor", after_planunit.numor)
                if before_planunit.morph != after_planunit.morph:
                    x_beliefatom.set_jvalue("morph", after_planunit.morph)
                if before_planunit.star != after_planunit.star:
                    x_beliefatom.set_jvalue("star", after_planunit.star)
                if before_planunit.task != after_planunit.task:
                    x_beliefatom.set_jvalue("task", after_planunit.task)
                self.set_beliefatom(x_beliefatom)

            # insert / update / delete factunits
            before_factunit_reason_contexts = set(before_planunit.factunits.keys())
            after_factunit_reason_contexts = set(after_planunit.factunits.keys())
            self.add_beliefatom_plan_factunit_inserts(
                planunit=after_planunit,
                insert_factunit_reason_contexts=after_factunit_reason_contexts.difference(
                    before_factunit_reason_contexts
                ),
            )
            self.add_beliefatom_plan_factunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_factunit_reason_contexts=before_factunit_reason_contexts.intersection(
                    after_factunit_reason_contexts
                ),
            )
            self.add_beliefatom_plan_factunit_deletes(
                plan_rope=plan_rope,
                delete_factunit_reason_contexts=before_factunit_reason_contexts.difference(
                    after_factunit_reason_contexts
                ),
            )

            # insert / update / delete awardunits
            before_awardunits_awardee_titles = set(before_planunit.awardunits.keys())
            after_awardunits_awardee_titles = set(after_planunit.awardunits.keys())
            self.add_beliefatom_plan_awardunit_inserts(
                after_planunit=after_planunit,
                insert_awardunit_awardee_titles=after_awardunits_awardee_titles.difference(
                    before_awardunits_awardee_titles
                ),
            )
            self.add_beliefatom_plan_awardunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_awardunit_awardee_titles=before_awardunits_awardee_titles.intersection(
                    after_awardunits_awardee_titles
                ),
            )
            self.add_beliefatom_plan_awardunit_deletes(
                plan_rope=plan_rope,
                delete_awardunit_awardee_titles=before_awardunits_awardee_titles.difference(
                    after_awardunits_awardee_titles
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_reason_contexts = set(before_planunit.reasonunits.keys())
            after_reasonunit_reason_contexts = set(after_planunit.reasonunits.keys())
            self.add_beliefatom_plan_reasonunit_inserts(
                after_planunit=after_planunit,
                insert_reasonunit_reason_contexts=after_reasonunit_reason_contexts.difference(
                    before_reasonunit_reason_contexts
                ),
            )
            self.add_beliefatom_plan_reasonunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_reasonunit_reason_contexts=before_reasonunit_reason_contexts.intersection(
                    after_reasonunit_reason_contexts
                ),
            )
            self.add_beliefatom_plan_reasonunit_deletes(
                before_planunit=before_planunit,
                delete_reasonunit_reason_contexts=before_reasonunit_reason_contexts.difference(
                    after_reasonunit_reason_contexts
                ),
            )
            # insert / update / delete reasonunits_permises
            # update reasonunits_permises insert_case
            # update reasonunits_permises update_case
            # update reasonunits_permises delete_case

            # insert / update / delete partyunits
            before_partys_party_titles = set(before_planunit.laborunit._partys)
            after_partys_party_titles = set(after_planunit.laborunit._partys)
            self.add_beliefatom_plan_partyunit_insert(
                plan_rope=plan_rope,
                insert_partyunit_party_titles=after_partys_party_titles.difference(
                    before_partys_party_titles
                ),
            )
            self.add_beliefatom_plan_partyunit_deletes(
                plan_rope=plan_rope,
                delete_partyunit_party_titles=before_partys_party_titles.difference(
                    after_partys_party_titles
                ),
            )

            # insert / update / delete healerunits
            before_healerunits_healer_names = set(
                before_planunit.healerunit._healer_names
            )
            after_healerunits_healer_names = set(
                after_planunit.healerunit._healer_names
            )
            self.add_beliefatom_plan_healerunit_insert(
                plan_rope=plan_rope,
                insert_healerunit_healer_names=after_healerunits_healer_names.difference(
                    before_healerunits_healer_names
                ),
            )
            self.add_beliefatom_plan_healerunit_deletes(
                plan_rope=plan_rope,
                delete_healerunit_healer_names=before_healerunits_healer_names.difference(
                    after_healerunits_healer_names
                ),
            )

    def add_beliefatom_plan_deletes(
        self, before_belief: BeliefUnit, delete_plan_ropes: set
    ):
        for delete_plan_rope in delete_plan_ropes:
            x_beliefatom = beliefatom_shop("belief_planunit", "DELETE")
            x_beliefatom.set_jkey("plan_rope", delete_plan_rope)
            self.set_beliefatom(x_beliefatom)

            delete_planunit = before_belief.get_plan_obj(delete_plan_rope)
            self.add_beliefatom_plan_factunit_deletes(
                plan_rope=delete_plan_rope,
                delete_factunit_reason_contexts=set(delete_planunit.factunits.keys()),
            )

            self.add_beliefatom_plan_awardunit_deletes(
                plan_rope=delete_plan_rope,
                delete_awardunit_awardee_titles=set(delete_planunit.awardunits.keys()),
            )
            self.add_beliefatom_plan_reasonunit_deletes(
                before_planunit=delete_planunit,
                delete_reasonunit_reason_contexts=set(
                    delete_planunit.reasonunits.keys()
                ),
            )
            self.add_beliefatom_plan_partyunit_deletes(
                plan_rope=delete_plan_rope,
                delete_partyunit_party_titles=delete_planunit.laborunit._partys,
            )
            self.add_beliefatom_plan_healerunit_deletes(
                plan_rope=delete_plan_rope,
                delete_healerunit_healer_names=delete_planunit.healerunit._healer_names,
            )

    def add_beliefatom_plan_reasonunit_inserts(
        self, after_planunit: PlanUnit, insert_reasonunit_reason_contexts: set
    ):
        for insert_reasonunit_reason_context in insert_reasonunit_reason_contexts:
            after_reasonunit = after_planunit.get_reasonunit(
                insert_reasonunit_reason_context
            )
            x_beliefatom = beliefatom_shop("belief_plan_reasonunit", "INSERT")
            x_beliefatom.set_jkey("plan_rope", after_planunit.get_plan_rope())
            x_beliefatom.set_jkey("reason_context", after_reasonunit.reason_context)
            if after_reasonunit.reason_active_requisite is not None:
                x_beliefatom.set_jvalue(
                    "reason_active_requisite",
                    after_reasonunit.reason_active_requisite,
                )
            self.set_beliefatom(x_beliefatom)

            self.add_beliefatom_plan_reason_caseunit_inserts(
                plan_rope=after_planunit.get_plan_rope(),
                after_reasonunit=after_reasonunit,
                insert_case_reason_states=set(after_reasonunit.cases.keys()),
            )

    def add_beliefatom_plan_reasonunit_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_reasonunit_reason_contexts: set,
    ):
        for update_reasonunit_reason_context in update_reasonunit_reason_contexts:
            before_reasonunit = before_planunit.get_reasonunit(
                update_reasonunit_reason_context
            )
            after_reasonunit = after_planunit.get_reasonunit(
                update_reasonunit_reason_context
            )
            if jvalues_different(
                "belief_plan_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_beliefatom = beliefatom_shop("belief_plan_reasonunit", "UPDATE")
                x_beliefatom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_beliefatom.set_jkey("reason_context", after_reasonunit.reason_context)
                if (
                    before_reasonunit.reason_active_requisite
                    != after_reasonunit.reason_active_requisite
                ):
                    x_beliefatom.set_jvalue(
                        "reason_active_requisite",
                        after_reasonunit.reason_active_requisite,
                    )
                self.set_beliefatom(x_beliefatom)

            before_case_reason_states = set(before_reasonunit.cases.keys())
            after_case_reason_states = set(after_reasonunit.cases.keys())
            self.add_beliefatom_plan_reason_caseunit_inserts(
                plan_rope=before_planunit.get_plan_rope(),
                after_reasonunit=after_reasonunit,
                insert_case_reason_states=after_case_reason_states.difference(
                    before_case_reason_states
                ),
            )
            self.add_beliefatom_plan_reason_caseunit_updates(
                plan_rope=before_planunit.get_plan_rope(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_case_reason_states=after_case_reason_states.intersection(
                    before_case_reason_states
                ),
            )
            self.add_beliefatom_plan_reason_caseunit_deletes(
                plan_rope=before_planunit.get_plan_rope(),
                reasonunit_reason_context=update_reasonunit_reason_context,
                delete_case_reason_states=before_case_reason_states.difference(
                    after_case_reason_states
                ),
            )

    def add_beliefatom_plan_reasonunit_deletes(
        self, before_planunit: PlanUnit, delete_reasonunit_reason_contexts: set
    ):
        for delete_reasonunit_reason_context in delete_reasonunit_reason_contexts:
            x_beliefatom = beliefatom_shop("belief_plan_reasonunit", "DELETE")
            x_beliefatom.set_jkey("plan_rope", before_planunit.get_plan_rope())
            x_beliefatom.set_jkey("reason_context", delete_reasonunit_reason_context)
            self.set_beliefatom(x_beliefatom)

            before_reasonunit = before_planunit.get_reasonunit(
                delete_reasonunit_reason_context
            )
            self.add_beliefatom_plan_reason_caseunit_deletes(
                plan_rope=before_planunit.get_plan_rope(),
                reasonunit_reason_context=delete_reasonunit_reason_context,
                delete_case_reason_states=set(before_reasonunit.cases.keys()),
            )

    def add_beliefatom_plan_reason_caseunit_inserts(
        self,
        plan_rope: RopePointer,
        after_reasonunit: ReasonUnit,
        insert_case_reason_states: set,
    ):
        for insert_case_reason_state in insert_case_reason_states:
            after_caseunit = after_reasonunit.get_case(insert_case_reason_state)
            x_beliefatom = beliefatom_shop("belief_plan_reason_caseunit", "INSERT")
            x_beliefatom.set_jkey("plan_rope", plan_rope)
            x_beliefatom.set_jkey("reason_context", after_reasonunit.reason_context)
            x_beliefatom.set_jkey("reason_state", after_caseunit.reason_state)
            if after_caseunit.reason_lower is not None:
                x_beliefatom.set_jvalue("reason_lower", after_caseunit.reason_lower)
            if after_caseunit.reason_upper is not None:
                x_beliefatom.set_jvalue("reason_upper", after_caseunit.reason_upper)
            if after_caseunit.reason_divisor is not None:
                x_beliefatom.set_jvalue("reason_divisor", after_caseunit.reason_divisor)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_reason_caseunit_updates(
        self,
        plan_rope: RopePointer,
        before_reasonunit: ReasonUnit,
        after_reasonunit: ReasonUnit,
        update_case_reason_states: set,
    ):
        for update_case_reason_state in update_case_reason_states:
            before_caseunit = before_reasonunit.get_case(update_case_reason_state)
            after_caseunit = after_reasonunit.get_case(update_case_reason_state)
            if jvalues_different(
                "belief_plan_reason_caseunit",
                before_caseunit,
                after_caseunit,
            ):
                x_beliefatom = beliefatom_shop("belief_plan_reason_caseunit", "UPDATE")
                x_beliefatom.set_jkey("plan_rope", plan_rope)
                x_beliefatom.set_jkey(
                    "reason_context", before_reasonunit.reason_context
                )
                x_beliefatom.set_jkey("reason_state", after_caseunit.reason_state)
                if after_caseunit.reason_lower != before_caseunit.reason_lower:
                    x_beliefatom.set_jvalue("reason_lower", after_caseunit.reason_lower)
                if after_caseunit.reason_upper != before_caseunit.reason_upper:
                    x_beliefatom.set_jvalue("reason_upper", after_caseunit.reason_upper)
                if after_caseunit.reason_divisor != before_caseunit.reason_divisor:
                    x_beliefatom.set_jvalue(
                        "reason_divisor", after_caseunit.reason_divisor
                    )
                self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_reason_caseunit_deletes(
        self,
        plan_rope: RopePointer,
        reasonunit_reason_context: RopePointer,
        delete_case_reason_states: set,
    ):
        for delete_case_reason_state in delete_case_reason_states:
            x_beliefatom = beliefatom_shop("belief_plan_reason_caseunit", "DELETE")
            x_beliefatom.set_jkey("plan_rope", plan_rope)
            x_beliefatom.set_jkey("reason_context", reasonunit_reason_context)
            x_beliefatom.set_jkey("reason_state", delete_case_reason_state)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_partyunit_insert(
        self, plan_rope: RopePointer, insert_partyunit_party_titles: set
    ):
        for insert_partyunit_party_title in insert_partyunit_party_titles:
            x_beliefatom = beliefatom_shop("belief_plan_partyunit", "INSERT")
            x_beliefatom.set_jkey("plan_rope", plan_rope)
            x_beliefatom.set_jkey("party_title", insert_partyunit_party_title)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_partyunit_deletes(
        self, plan_rope: RopePointer, delete_partyunit_party_titles: set
    ):
        for delete_partyunit_party_title in delete_partyunit_party_titles:
            x_beliefatom = beliefatom_shop("belief_plan_partyunit", "DELETE")
            x_beliefatom.set_jkey("plan_rope", plan_rope)
            x_beliefatom.set_jkey("party_title", delete_partyunit_party_title)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_healerunit_insert(
        self, plan_rope: RopePointer, insert_healerunit_healer_names: set
    ):
        for insert_healerunit_healer_name in insert_healerunit_healer_names:
            x_beliefatom = beliefatom_shop("belief_plan_healerunit", "INSERT")
            x_beliefatom.set_jkey("plan_rope", plan_rope)
            x_beliefatom.set_jkey("healer_name", insert_healerunit_healer_name)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_healerunit_deletes(
        self, plan_rope: RopePointer, delete_healerunit_healer_names: set
    ):
        for delete_healerunit_healer_name in delete_healerunit_healer_names:
            x_beliefatom = beliefatom_shop("belief_plan_healerunit", "DELETE")
            x_beliefatom.set_jkey("plan_rope", plan_rope)
            x_beliefatom.set_jkey("healer_name", delete_healerunit_healer_name)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_awardunit_inserts(
        self, after_planunit: PlanUnit, insert_awardunit_awardee_titles: set
    ):
        for after_awardunit_awardee_title in insert_awardunit_awardee_titles:
            after_awardunit = after_planunit.awardunits.get(
                after_awardunit_awardee_title
            )
            x_beliefatom = beliefatom_shop("belief_plan_awardunit", "INSERT")
            x_beliefatom.set_jkey("plan_rope", after_planunit.get_plan_rope())
            x_beliefatom.set_jkey("awardee_title", after_awardunit.awardee_title)
            x_beliefatom.set_jvalue("give_force", after_awardunit.give_force)
            x_beliefatom.set_jvalue("take_force", after_awardunit.take_force)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_awardunit_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_awardunit_awardee_titles: set,
    ):
        for update_awardunit_awardee_title in update_awardunit_awardee_titles:
            before_awardunit = before_planunit.awardunits.get(
                update_awardunit_awardee_title
            )
            after_awardunit = after_planunit.awardunits.get(
                update_awardunit_awardee_title
            )
            if jvalues_different(
                "belief_plan_awardunit", before_awardunit, after_awardunit
            ):
                x_beliefatom = beliefatom_shop("belief_plan_awardunit", "UPDATE")
                x_beliefatom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_beliefatom.set_jkey("awardee_title", after_awardunit.awardee_title)
                if before_awardunit.give_force != after_awardunit.give_force:
                    x_beliefatom.set_jvalue("give_force", after_awardunit.give_force)
                if before_awardunit.take_force != after_awardunit.take_force:
                    x_beliefatom.set_jvalue("take_force", after_awardunit.take_force)
                self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_awardunit_deletes(
        self, plan_rope: RopePointer, delete_awardunit_awardee_titles: set
    ):
        for delete_awardunit_awardee_title in delete_awardunit_awardee_titles:
            x_beliefatom = beliefatom_shop("belief_plan_awardunit", "DELETE")
            x_beliefatom.set_jkey("plan_rope", plan_rope)
            x_beliefatom.set_jkey("awardee_title", delete_awardunit_awardee_title)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_factunit_inserts(
        self, planunit: PlanUnit, insert_factunit_reason_contexts: set
    ):
        for insert_factunit_reason_context in insert_factunit_reason_contexts:
            insert_factunit = planunit.factunits.get(insert_factunit_reason_context)
            x_beliefatom = beliefatom_shop("belief_plan_factunit", "INSERT")
            x_beliefatom.set_jkey("plan_rope", planunit.get_plan_rope())
            x_beliefatom.set_jkey("fact_context", insert_factunit.fact_context)
            if insert_factunit.fact_state is not None:
                x_beliefatom.set_jvalue("fact_state", insert_factunit.fact_state)
            if insert_factunit.fact_lower is not None:
                x_beliefatom.set_jvalue("fact_lower", insert_factunit.fact_lower)
            if insert_factunit.fact_upper is not None:
                x_beliefatom.set_jvalue("fact_upper", insert_factunit.fact_upper)
            self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_factunit_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_factunit_reason_contexts: set,
    ):
        for update_factunit_reason_context in update_factunit_reason_contexts:
            before_factunit = before_planunit.factunits.get(
                update_factunit_reason_context
            )
            after_factunit = after_planunit.factunits.get(
                update_factunit_reason_context
            )
            if jvalues_different(
                "belief_plan_factunit", before_factunit, after_factunit
            ):
                x_beliefatom = beliefatom_shop("belief_plan_factunit", "UPDATE")
                x_beliefatom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_beliefatom.set_jkey("fact_context", after_factunit.fact_context)
                if before_factunit.fact_state != after_factunit.fact_state:
                    x_beliefatom.set_jvalue("fact_state", after_factunit.fact_state)
                if before_factunit.fact_lower != after_factunit.fact_lower:
                    x_beliefatom.set_jvalue("fact_lower", after_factunit.fact_lower)
                if before_factunit.fact_upper != after_factunit.fact_upper:
                    x_beliefatom.set_jvalue("fact_upper", after_factunit.fact_upper)
                self.set_beliefatom(x_beliefatom)

    def add_beliefatom_plan_factunit_deletes(
        self, plan_rope: RopePointer, delete_factunit_reason_contexts: FactUnit
    ):
        for delete_factunit_reason_context in delete_factunit_reason_contexts:
            x_beliefatom = beliefatom_shop("belief_plan_factunit", "DELETE")
            x_beliefatom.set_jkey("plan_rope", plan_rope)
            x_beliefatom.set_jkey("fact_context", delete_factunit_reason_context)
            self.set_beliefatom(x_beliefatom)

    def is_empty(self) -> bool:
        return self.beliefatoms == {}

    def get_ordered_beliefatoms(self, x_count: int = None) -> dict[int, BeliefAtom]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_atom in self.get_sorted_beliefatoms():
            x_dict[x_count] = x_atom
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int, str]:
        atom_tuples = self.get_ordered_beliefatoms(x_count).items()
        return {atom_num: atom_obj.to_dict() for atom_num, atom_obj in atom_tuples}

    def get_json(self, x_count: int = None) -> str:
        x_dict = self.get_ordered_dict(x_count)
        return get_json_from_dict(x_dict)


def beliefdelta_shop(beliefatoms: dict[str, BeliefAtom] = None) -> BeliefDelta:
    return BeliefDelta(
        beliefatoms=get_empty_dict_if_None(beliefatoms),
        _belief_build_validated=False,
    )


def belief_built_from_delta_is_valid(
    x_delta: BeliefDelta, x_belief: BeliefUnit = None
) -> bool:
    x_belief = beliefunit_shop() if x_belief is None else x_belief
    x_belief = x_delta.get_edited_belief(x_belief)
    try:
        x_belief.cashout()
    except Exception:
        return False
    return True


def get_dimens_cruds_beliefdelta(
    x_beliefdelta: BeliefDelta, dimen_set: set[str], curd_set: set[str]
) -> BeliefDelta:
    new_beliefdelta = beliefdelta_shop()
    for x_beliefatom in x_beliefdelta.get_sorted_beliefatoms():
        if x_beliefatom.crud_str in curd_set and x_beliefatom.dimen in dimen_set:
            new_beliefdelta.set_beliefatom(x_beliefatom)
    return new_beliefdelta


def get_minimal_beliefdelta(
    x_beliefdelta: BeliefDelta, x_belief: BeliefUnit
) -> BeliefDelta:
    """Creates new BeliefDelta with only BeliefAtoms that would actually change the BeliefUnit"""
    new_beliefdelta = beliefdelta_shop()
    for x_atom in x_beliefdelta.get_sorted_beliefatoms():
        sifted_atom = sift_beliefatom(x_belief, x_atom)
        if sifted_atom != None:
            new_beliefdelta.set_beliefatom(sifted_atom)
    return new_beliefdelta


def get_beliefdelta_from_ordered_dict(x_dict: dict) -> BeliefDelta:
    x_beliefdelta = beliefdelta_shop()
    for x_atom_dict in x_dict.values():
        x_beliefdelta.set_beliefatom(get_beliefatom_from_dict(x_atom_dict))
    return x_beliefdelta
