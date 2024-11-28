from src.f10_world.pidgin_agg import (
    PidginBodyCore,
    PidginBodyBook,
    pidginbodybook_shop,
    pidginbodycore_shop,
    create_pidginbodycore,
    PidginBodyRow,
)


def test_PidginBodyRow_Exists():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    x_otx_str = ";"
    x_inx_str = ";"

    # WHEN
    sue55_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, x_otx_str, x_inx_str)

    # THEN
    assert sue55_pidginbodyrow
    assert sue55_pidginbodyrow.face_id == sue_str
    assert sue55_pidginbodyrow.event_id == x_event_id
    assert sue55_pidginbodyrow.otx_str == x_otx_str
    assert sue55_pidginbodyrow.inx_str == x_inx_str


def test_PidginBodyCore_Exists():
    # ESTABLISH
    x_pidginbodycore = PidginBodyCore()

    # THEN
    assert x_pidginbodycore
    assert x_pidginbodycore.face_id is None
    assert x_pidginbodycore.event_id is None
    assert x_pidginbodycore.otx_str is None
    assert x_pidginbodycore.inx_strs is None


def test_pidginbodycore_shop_ReturnsObj_WithNoValues():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_otx_str = "Bob"

    # WHEN
    x_pidginbodycore = pidginbodycore_shop(x_face_id, x_event_id, x_otx_str)

    # THEN
    assert x_pidginbodycore
    assert x_pidginbodycore.face_id == x_face_id
    assert x_pidginbodycore.event_id == x_event_id
    assert x_pidginbodycore.otx_str == x_otx_str
    assert x_pidginbodycore.inx_strs == set()


def test_pidginbodycore_shop_ReturnsObj_WithCoreValues():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob_inx = "Bobito"
    inx_str_set = {bob_inx}

    # WHEN
    x_pidginbodycore = pidginbodycore_shop(x_face_id, x_event_id, bob_otx, inx_str_set)

    # THEN
    assert x_pidginbodycore
    assert x_pidginbodycore.face_id == x_face_id
    assert x_pidginbodycore.event_id == x_event_id
    assert x_pidginbodycore.otx_str == bob_otx
    assert x_pidginbodycore.inx_strs == inx_str_set
    assert bob_inx in x_pidginbodycore.inx_strs


def test_PidginBodyCore_add_inx_str_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob_inx = "Bobito"
    x_pidginbodycore = pidginbodycore_shop(x_face_id, x_event_id, bob_otx)
    assert bob_inx not in x_pidginbodycore.inx_strs

    # WHEN
    x_pidginbodycore.add_inx_str(bob_inx)

    # THEN
    assert bob_inx in x_pidginbodycore.inx_strs


def test_PidginBodyCore_add_inx_str_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    x_pidginbodycore = pidginbodycore_shop(x_face_id, x_event_id, bob_otx)
    assert None not in x_pidginbodycore.inx_strs

    # WHEN
    x_pidginbodycore.add_inx_str(None)

    # THEN
    assert None in x_pidginbodycore.inx_strs


def test_PidginBodyCore_add_inx_str_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    x_pidginbodycore = pidginbodycore_shop(x_face_id, x_event_id, bob_otx)
    assert None not in x_pidginbodycore.inx_strs

    x_pidginbodycore.add_inx_str(None)
    assert None in x_pidginbodycore.inx_strs

    # WHEN / THEN
    x_pidginbodycore.add_inx_str(None)
    assert None in x_pidginbodycore.inx_strs

    # WHEN / THEN
    bob_inx = "Bobito"
    x_pidginbodycore.add_inx_str(bob_inx)
    assert bob_inx in x_pidginbodycore.inx_strs
    assert None not in x_pidginbodycore.inx_strs

    # WHEN / THEN
    x_pidginbodycore.add_inx_str(None)
    assert bob_inx in x_pidginbodycore.inx_strs
    assert None not in x_pidginbodycore.inx_strs


def test_create_pidginbodycore_ReturnsObj():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob_inx = "Bobito"

    # WHEN
    x_pidginbodycore = create_pidginbodycore(x_face_id, x_event_id, bob_otx, bob_inx)

    # THEN
    x_face_id = x_face_id
    x_event_id = x_event_id
    x_inx_str_set = {bob_inx}
    assert x_pidginbodycore
    assert x_pidginbodycore.face_id == x_face_id
    assert x_pidginbodycore.event_id == x_event_id
    assert x_pidginbodycore.otx_str == bob_otx
    assert x_pidginbodycore.inx_strs == x_inx_str_set


def test_PidginBodyCore_is_valid_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    bob3_inx = "Bobby"

    # WHEN / THEN
    x_pidginbodycore = pidginbodycore_shop(sue_str, e55, bob2_inx)
    assert x_pidginbodycore.is_valid() is False

    # WHEN / THEN
    x_pidginbodycore = pidginbodycore_shop(sue_str, e55, bob_otx, {bob2_inx})
    assert x_pidginbodycore.is_valid()

    # WHEN / THEN
    x_pidginbodycore = pidginbodycore_shop(sue_str, e55, bob_otx, {None})
    assert x_pidginbodycore.is_valid()

    # WHEN / THEN
    x_pidginbodycore = pidginbodycore_shop(sue_str, e55, bob_otx, {bob2_inx, bob3_inx})
    assert x_pidginbodycore.is_valid() is False


def test_PidginBodyCore_get_valid_pidginbodyrow_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"

    # WHEN / THEN
    x_pidginbodycore = pidginbodycore_shop(sue_str, e55, bob_otx)
    assert x_pidginbodycore.is_valid() is False
    assert None == x_pidginbodycore.get_valid_pidginbodyrow()


def test_PidginBodyCore_get_valid_pidginbodyrow_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"
    bob_inx = "Bobito"

    # WHEN
    x_pidginbodycore = pidginbodycore_shop(sue_str, e55, bob_otx, {bob_inx})

    # THEN
    assert x_pidginbodycore.is_valid()
    assert x_pidginbodycore.get_valid_pidginbodyrow()
    s55_pidginbodyrow = x_pidginbodycore.get_valid_pidginbodyrow()
    assert s55_pidginbodyrow.face_id == sue_str
    assert s55_pidginbodyrow.event_id == e55
    assert s55_pidginbodyrow.otx_str == bob_otx
    assert s55_pidginbodyrow.inx_str == bob_inx


def test_PidginBodyCore_get_valid_pidginbodyrow_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"

    # WHEN
    x_pidginbodycore = pidginbodycore_shop(sue_str, e55, bob_otx, {None})
    assert x_pidginbodycore.is_valid()
    assert x_pidginbodycore.get_valid_pidginbodyrow()
    s55_pidginbodyrow = x_pidginbodycore.get_valid_pidginbodyrow()
    assert s55_pidginbodyrow.face_id == sue_str
    assert s55_pidginbodyrow.event_id == e55
    assert s55_pidginbodyrow.otx_str == bob_otx
    assert s55_pidginbodyrow.inx_str is None


def test_PidginBodyCore_get_valid_pidginbodyrow_ReturnsObj_Scenario3():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    bob3_inx = "Bobby"

    # WHEN
    x_pidginbodycore = pidginbodycore_shop(sue_str, e55, bob_otx, {bob2_inx, bob3_inx})

    # THEN
    assert x_pidginbodycore.is_valid() is False
    assert not x_pidginbodycore.get_valid_pidginbodyrow()


def test_PidginBodyBook_Exists():
    # ESTABLISH / WHEN
    x_pidginbodybook = PidginBodyBook()

    # THEN
    assert x_pidginbodybook
    assert x_pidginbodybook.pidginbodycores is None


def test_eventsaggs_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginbodybook = pidginbodybook_shop()

    # THEN
    assert x_pidginbodybook
    assert x_pidginbodybook.pidginbodycores == {}


def test_PidginBodyBook_overwrite_pidginbodycore_SetsAttr_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    bob3_inx = "Bobby"
    sue55_agg = create_pidginbodycore(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook = pidginbodybook_shop()
    pidgincore_key = (sue_str, x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodycores.get(pidgincore_key) is None

    # WHEN
    x_pidginbodybook._overwrite_pidginbodycore(sue55_agg)

    # THEN
    assert x_pidginbodybook.pidginbodycores.get(pidgincore_key) != None
    assert x_pidginbodybook.pidginbodycores.get(pidgincore_key) == sue55_agg


def test_PidginBodyBook_pidginbodycore_exists_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue55_agg = create_pidginbodycore(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook = pidginbodybook_shop()
    pidgincore_key = (sue_str, x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodycore_exists(pidgincore_key) is False

    # WHEN
    x_pidginbodybook._overwrite_pidginbodycore(sue55_agg)

    # THEN
    assert x_pidginbodybook.pidginbodycore_exists(pidgincore_key)


def test_PidginBodyBook_get_pidginbodycore_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x55_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue55_agg = create_pidginbodycore(sue_str, x55_event_id, bob_otx, bob2_inx)
    x_pidginbodybook = pidginbodybook_shop()
    x_pidginbodybook._overwrite_pidginbodycore(sue55_agg)
    sue55_key = (sue_str, x55_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodycore_exists(sue55_key)

    # WHEN
    gen_pidginbodycore = x_pidginbodybook.get_pidginbodycore(sue55_key)

    # THEN
    assert gen_pidginbodycore == sue55_agg


def test_PidginBodyBook_eval_pidginbodyrow_SetsAttr_Scenario0_EmptyDict():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue55_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook = pidginbodybook_shop()
    sue55_key = (sue_str, x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodycore_exists(sue55_key) is False

    # WHEN
    x_pidginbodybook.eval_pidginbodyrow(sue55_pidginbodyrow)

    # THEN
    assert x_pidginbodybook.pidginbodycore_exists(sue55_key)
    x_pidginbodycore = x_pidginbodybook.get_pidginbodycore(sue55_key)
    assert x_pidginbodycore.face_id == sue_str
    assert x_pidginbodycore.event_id == x_event_id
    assert bob2_inx in x_pidginbodycore.inx_strs


def test_PidginBodyBook_eval_pidginbodyrow_SetsAttr_Scenario1_MultipleRowsAtSameEvent():
    # ESTABLISH
    x_pidginbodybook = pidginbodybook_shop()
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue1_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook.eval_pidginbodyrow(sue1_pidginbodyrow)
    sue55_key = (sue_str, x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodycore_exists(sue55_key)

    # WHEN
    bob3_inx = "Bobby"
    sue2_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, bob3_inx)
    x_pidginbodybook.eval_pidginbodyrow(sue2_pidginbodyrow)

    # THEN
    assert x_pidginbodybook.pidginbodycore_exists(sue55_key)
    gen_pidginbodycore = x_pidginbodybook.get_pidginbodycore(sue55_key)
    assert gen_pidginbodycore.face_id == sue_str
    assert gen_pidginbodycore.event_id == x_event_id
    assert gen_pidginbodycore.otx_str == bob_otx
    assert gen_pidginbodycore.inx_strs == {bob2_inx, bob3_inx}


def test_PidginBodyBook_eval_pidginbodyrow_SetsAttr_Scenario2_NoneElementIsHandledCorrectly():
    # ESTABLISH
    x_pidginbodybook = pidginbodybook_shop()
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue1_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook.eval_pidginbodyrow(sue1_pidginbodyrow)
    sue55_key = (sue_str, x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodycore_exists(sue55_key)

    # WHEN
    sue2_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, None)
    x_pidginbodybook.eval_pidginbodyrow(sue2_pidginbodyrow)

    # THEN
    assert x_pidginbodybook.pidginbodycore_exists(sue55_key)
    gen_pidginbodycore = x_pidginbodybook.get_pidginbodycore(sue55_key)
    assert gen_pidginbodycore.face_id == sue_str
    assert gen_pidginbodycore.event_id == x_event_id
    assert gen_pidginbodycore.otx_str == bob_otx
    assert gen_pidginbodycore.inx_strs == {bob2_inx}
