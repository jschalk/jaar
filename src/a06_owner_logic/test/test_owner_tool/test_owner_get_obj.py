from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.owner_tool import (
    owner_acct_membership_get_obj,
    owner_acctunit_get_obj,
    owner_concept_awardlink_get_obj,
    owner_concept_factunit_get_obj,
    owner_concept_reason_premiseunit_get_obj as premiseunit_get_obj,
    owner_concept_reasonunit_get_obj,
    owner_conceptunit_get_obj,
    owner_get_obj,
)
from src.a06_owner_logic.test._util.a06_str import (
    concept_rope_str,
    fcontext_str,
    fstate_str,
    owner_acct_membership_str,
    owner_acctunit_str,
    owner_concept_awardlink_str,
    owner_concept_factunit_str,
    owner_concept_healerlink_str,
    owner_concept_laborlink_str,
    owner_concept_reason_premiseunit_str as premiseunit_str,
    owner_concept_reasonunit_str,
    owner_conceptunit_str,
    ownerunit_str,
    pstate_str,
    rcontext_str,
)


def test_owner_acctunit_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_owner = ownerunit_shop("Sue")
    jkeys = {"acct_name": yao_str}
    sue_owner.add_acctunit(yao_str)

    # WHEN
    x_obj = owner_acctunit_get_obj(sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_acct(yao_str)


def test_owner_acct_membership_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_owner = ownerunit_shop("Sue")
    jkeys = {"acct_name": yao_str, "group_title": swim_str}
    sue_owner.add_acctunit(yao_str)
    sue_owner.get_acct(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = owner_acct_membership_get_obj(sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_acct(yao_str).get_membership(swim_str)


def test_owner_conceptunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    sue_owner.add_concept(casa_rope)
    jkeys = {concept_rope_str(): casa_rope}

    # WHEN
    x_obj = owner_conceptunit_get_obj(sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_concept_obj(casa_rope)


def test_owner_concept_awardlink_get_obj_ReturnsObj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    sue_owner.add_concept(casa_rope)
    jkeys = {concept_rope_str(): casa_rope, "awardee_title": swim_str}
    sue_owner.add_concept(casa_rope)
    sue_owner.get_concept_obj(casa_rope).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = owner_concept_awardlink_get_obj(sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_concept_obj(casa_rope).get_awardlink(swim_str)


def test_owner_concept_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    wk_rope = sue_owner.make_l1_rope("wk")
    sue_owner.add_concept(casa_rope)
    jkeys = {concept_rope_str(): casa_rope, rcontext_str(): wk_rope}
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(wk_rope)
    sue_owner.get_concept_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = owner_concept_reasonunit_get_obj(sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_concept_obj(casa_rope).get_reasonunit(wk_rope)


def test_owner_concept_reason_premiseunit_get_obj_ReturnsObj():
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    wk_str = "wk"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    thur_rope = sue_owner.make_rope(wk_rope, "thur")
    casa_jkeys = {
        concept_rope_str(): casa_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(wk_rope)
    sue_owner.add_concept(thur_rope)
    casa_concept = sue_owner.get_concept_obj(casa_rope)
    casa_concept.set_reasonunit(reasonunit_shop(wk_rope))
    casa_concept.get_reasonunit(wk_rope).set_premise(thur_rope)

    # WHEN
    x_obj = premiseunit_get_obj(sue_owner, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_concept.get_reasonunit(wk_rope).get_premise(thur_rope)


def test_owner_concept_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    wk_rope = sue_owner.make_l1_rope("wk")
    sue_owner.add_concept(casa_rope)
    jkeys = {concept_rope_str(): casa_rope, fcontext_str(): wk_rope}
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(wk_rope)
    sue_owner.get_concept_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = owner_concept_factunit_get_obj(sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_concept_obj(casa_rope).factunits.get(wk_rope)


def test_owner_get_obj_ReturnsObj_OwnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_owner = ownerunit_shop("Sue")
    jkeys = {"acct_name": yao_str}
    sue_owner.add_acctunit(yao_str)

    # WHEN
    x_obj = owner_get_obj(ownerunit_str(), sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner


def test_owner_get_obj_ReturnsObj_owner_acctunit_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    sue_owner = ownerunit_shop("Sue")
    jkeys = {"acct_name": yao_str}
    sue_owner.add_acctunit(yao_str)

    # WHEN
    x_obj = owner_get_obj(owner_acctunit_str(), sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_acct(yao_str)


def test_owner_get_obj_ReturnsObj_owner_acct_membership_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_owner = ownerunit_shop("Sue")
    jkeys = {"acct_name": yao_str, "group_title": swim_str}
    sue_owner.add_acctunit(yao_str)
    sue_owner.get_acct(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = owner_get_obj(owner_acct_membership_str(), sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_acct(yao_str).get_membership(swim_str)


def test_owner_get_obj_ReturnsObj_owner_conceptunit_get_obj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    sue_owner.add_concept(casa_rope)
    jkeys = {concept_rope_str(): casa_rope}

    # WHEN
    x_obj = owner_get_obj(owner_conceptunit_str(), sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_concept_obj(casa_rope)


def test_owner_get_obj_ReturnsObj_owner_concept_awardlink_get_obj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    sue_owner.add_concept(casa_rope)
    jkeys = {concept_rope_str(): casa_rope, "awardee_title": swim_str}
    sue_owner.add_concept(casa_rope)
    sue_owner.get_concept_obj(casa_rope).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = owner_get_obj(owner_concept_awardlink_str(), sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_concept_obj(casa_rope).get_awardlink(swim_str)


def test_owner_get_obj_ReturnsObj_owner_concept_reasonunit_get_obj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    wk_rope = sue_owner.make_l1_rope("wk")
    sue_owner.add_concept(casa_rope)
    jkeys = {concept_rope_str(): casa_rope, rcontext_str(): wk_rope}
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(wk_rope)
    sue_owner.get_concept_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = owner_get_obj(owner_concept_reasonunit_str(), sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_concept_obj(casa_rope).get_reasonunit(wk_rope)


def test_owner_get_obj_ReturnsObj_owner_concept_reason_premiseunit_get_obj():
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    wk_str = "wk"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    thur_rope = sue_owner.make_rope(wk_rope, "thur")
    casa_jkeys = {
        concept_rope_str(): casa_rope,
        rcontext_str(): wk_rope,
        pstate_str(): thur_rope,
    }
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(wk_rope)
    sue_owner.add_concept(thur_rope)
    casa_concept = sue_owner.get_concept_obj(casa_rope)
    casa_concept.set_reasonunit(reasonunit_shop(wk_rope))
    casa_concept.get_reasonunit(wk_rope).set_premise(thur_rope)

    # WHEN
    x_obj = owner_get_obj(premiseunit_str(), sue_owner, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_concept.get_reasonunit(wk_rope).get_premise(thur_rope)


def test_owner_get_obj_ReturnsObj_owner_concept_factunit_get_obj():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    wk_rope = sue_owner.make_l1_rope("wk")
    sue_owner.add_concept(casa_rope)
    jkeys = {concept_rope_str(): casa_rope, fcontext_str(): wk_rope}
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(wk_rope)
    sue_owner.get_concept_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = owner_get_obj(owner_concept_factunit_str(), sue_owner, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_owner.get_concept_obj(casa_rope).factunits.get(wk_rope)
