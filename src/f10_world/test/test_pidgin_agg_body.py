from src.f10_world.pidgin_agg import (
    PidginHeartBook,
    pidginheartbook_shop,
    PidginBodyUnit,
    PidginBodyBook,
    pidginbodybook_shop,
    pidginbodyunit_shop,
    create_pidginbodyunit,
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


def test_PidginBodyUnit_Exists():
    # ESTABLISH
    x_pidginbodyunit = PidginBodyUnit()

    # THEN
    assert x_pidginbodyunit
    assert x_pidginbodyunit.face_id is None
    assert x_pidginbodyunit.event_id is None
    assert x_pidginbodyunit.otx_str is None
    assert x_pidginbodyunit.inx_strs is None


def test_pidginbodyunit_shop_ReturnsObj_WithNoValues():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_otx_str = "Bob"

    # WHEN
    x_pidginbodyunit = pidginbodyunit_shop(x_face_id, x_event_id, x_otx_str)

    # THEN
    assert x_pidginbodyunit
    assert x_pidginbodyunit.face_id == x_face_id
    assert x_pidginbodyunit.event_id == x_event_id
    assert x_pidginbodyunit.otx_str == x_otx_str
    assert x_pidginbodyunit.inx_strs == set()


def test_pidginbodyunit_shop_ReturnsObj_WithUnitValues():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob_inx = "Bobito"
    inx_str_set = {bob_inx}

    # WHEN
    x_pidginbodyunit = pidginbodyunit_shop(x_face_id, x_event_id, bob_otx, inx_str_set)

    # THEN
    assert x_pidginbodyunit
    assert x_pidginbodyunit.face_id == x_face_id
    assert x_pidginbodyunit.event_id == x_event_id
    assert x_pidginbodyunit.otx_str == bob_otx
    assert x_pidginbodyunit.inx_strs == inx_str_set
    assert bob_inx in x_pidginbodyunit.inx_strs


def test_PidginBodyUnit_add_inx_str_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob_inx = "Bobito"
    x_pidginbodyunit = pidginbodyunit_shop(x_face_id, x_event_id, bob_otx)
    assert bob_inx not in x_pidginbodyunit.inx_strs

    # WHEN
    x_pidginbodyunit.add_inx_str(bob_inx)

    # THEN
    assert bob_inx in x_pidginbodyunit.inx_strs


def test_PidginBodyUnit_add_inx_str_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    x_pidginbodyunit = pidginbodyunit_shop(x_face_id, x_event_id, bob_otx)
    assert None not in x_pidginbodyunit.inx_strs

    # WHEN
    x_pidginbodyunit.add_inx_str(None)

    # THEN
    assert None in x_pidginbodyunit.inx_strs


def test_PidginBodyUnit_add_inx_str_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    x_pidginbodyunit = pidginbodyunit_shop(x_face_id, x_event_id, bob_otx)
    assert None not in x_pidginbodyunit.inx_strs

    x_pidginbodyunit.add_inx_str(None)
    assert None in x_pidginbodyunit.inx_strs

    # WHEN / THEN
    x_pidginbodyunit.add_inx_str(None)
    assert None in x_pidginbodyunit.inx_strs

    # WHEN / THEN
    bob_inx = "Bobito"
    x_pidginbodyunit.add_inx_str(bob_inx)
    assert bob_inx in x_pidginbodyunit.inx_strs
    assert None not in x_pidginbodyunit.inx_strs

    # WHEN / THEN
    x_pidginbodyunit.add_inx_str(None)
    assert bob_inx in x_pidginbodyunit.inx_strs
    assert None not in x_pidginbodyunit.inx_strs


def test_create_pidginbodyunit_ReturnsObj():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob_inx = "Bobito"

    # WHEN
    x_pidginbodyunit = create_pidginbodyunit(x_face_id, x_event_id, bob_otx, bob_inx)

    # THEN
    x_face_id = x_face_id
    x_event_id = x_event_id
    x_inx_str_set = {bob_inx}
    assert x_pidginbodyunit
    assert x_pidginbodyunit.face_id == x_face_id
    assert x_pidginbodyunit.event_id == x_event_id
    assert x_pidginbodyunit.otx_str == bob_otx
    assert x_pidginbodyunit.inx_strs == x_inx_str_set


def test_PidginBodyUnit_is_valid_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    bob3_inx = "Bobby"

    # WHEN / THEN
    x_pidginbodyunit = pidginbodyunit_shop(sue_str, e55, bob2_inx)
    assert x_pidginbodyunit.is_valid() is False

    # WHEN / THEN
    x_pidginbodyunit = pidginbodyunit_shop(sue_str, e55, bob_otx, {bob2_inx})
    assert x_pidginbodyunit.is_valid()

    # WHEN / THEN
    x_pidginbodyunit = pidginbodyunit_shop(sue_str, e55, bob_otx, {None})
    assert x_pidginbodyunit.is_valid()

    # WHEN / THEN
    x_pidginbodyunit = pidginbodyunit_shop(sue_str, e55, bob_otx, {bob2_inx, bob3_inx})
    assert x_pidginbodyunit.is_valid() is False


def test_PidginBodyUnit_get_valid_pidginbodyrow_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"

    # WHEN / THEN
    x_pidginbodyunit = pidginbodyunit_shop(sue_str, e55, bob_otx)
    assert x_pidginbodyunit.is_valid() is False
    assert None == x_pidginbodyunit.get_valid_pidginbodyrow()


def test_PidginBodyUnit_get_valid_pidginbodyrow_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"
    bob_inx = "Bobito"

    # WHEN
    x_pidginbodyunit = pidginbodyunit_shop(sue_str, e55, bob_otx, {bob_inx})

    # THEN
    assert x_pidginbodyunit.is_valid()
    assert x_pidginbodyunit.get_valid_pidginbodyrow()
    s55_pidginbodyrow = x_pidginbodyunit.get_valid_pidginbodyrow()
    assert s55_pidginbodyrow.face_id == sue_str
    assert s55_pidginbodyrow.event_id == e55
    assert s55_pidginbodyrow.otx_str == bob_otx
    assert s55_pidginbodyrow.inx_str == bob_inx


def test_PidginBodyUnit_get_valid_pidginbodyrow_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"

    # WHEN
    x_pidginbodyunit = pidginbodyunit_shop(sue_str, e55, bob_otx, {None})
    assert x_pidginbodyunit.is_valid()
    assert x_pidginbodyunit.get_valid_pidginbodyrow()
    s55_pidginbodyrow = x_pidginbodyunit.get_valid_pidginbodyrow()
    assert s55_pidginbodyrow.face_id == sue_str
    assert s55_pidginbodyrow.event_id == e55
    assert s55_pidginbodyrow.otx_str == bob_otx
    assert s55_pidginbodyrow.inx_str is None


def test_PidginBodyUnit_get_valid_pidginbodyrow_ReturnsObj_Scenario3():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    bob3_inx = "Bobby"

    # WHEN
    x_pidginbodyunit = pidginbodyunit_shop(sue_str, e55, bob_otx, {bob2_inx, bob3_inx})

    # THEN
    assert x_pidginbodyunit.is_valid() is False
    assert not x_pidginbodyunit.get_valid_pidginbodyrow()


def test_PidginBodyBook_Exists():
    # ESTABLISH / WHEN
    x_pidginbodybook = PidginBodyBook()

    # THEN
    assert x_pidginbodybook
    assert x_pidginbodybook.pidginheartbook is None
    assert x_pidginbodybook.pidginbodyunits is None


def test_pidginbodybook_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginbodybook = pidginbodybook_shop()

    # THEN
    assert x_pidginbodybook
    assert x_pidginbodybook.pidginheartbook == pidginheartbook_shop()
    assert x_pidginbodybook.pidginbodyunits == {}


def test_pidginbodybook_shop_ReturnsObj_WithValues():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    colon_str = ":"
    uk44 = "unknown44"
    x_pidginheartbook = pidginheartbook_shop()
    x_pidginheartbook.add_pidginheartrow(sue_str, x_event_id, colon_str, None, uk44)

    # WHEN
    x_pidginbodybook = pidginbodybook_shop(x_pidginheartbook)

    # THEN
    assert x_pidginbodybook
    assert x_pidginbodybook.pidginheartbook.pidginheartunit_exists(x_event_id)
    assert x_pidginbodybook.pidginheartbook == x_pidginheartbook
    assert x_pidginbodybook.pidginbodyunits == {}


def test_PidginBodyBook_add_pidginheartrow_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    colon_str = ":"
    uk44 = "unknown44"
    x_pidginbodybook = pidginbodybook_shop()
    assert x_pidginbodybook.pidginheartbook.event_id_is_valid(x_event_id) is False

    # WHEN
    x_pidginbodybook.add_pidginheartrow(sue_str, x_event_id, colon_str, None, uk44)

    # THEN
    assert x_pidginbodybook
    assert x_pidginbodybook.pidginheartbook.event_id_is_valid(x_event_id)
    assert x_pidginbodybook.pidginheartbook.pidginheartunit_exists(x_event_id)
    y_pidginheartbook = pidginheartbook_shop()
    y_pidginheartbook.add_pidginheartrow(sue_str, x_event_id, colon_str, None, uk44)
    assert x_pidginbodybook.pidginheartbook == y_pidginheartbook
    assert x_pidginbodybook.pidginbodyunits == {}


def test_PidginBodyBook_overwrite_pidginbodyunit_SetsAttr_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    bob3_inx = "Bobby"
    sue55_agg = create_pidginbodyunit(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook = pidginbodybook_shop()
    pidginbody_key = (x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodyunits.get(pidginbody_key) is None

    # WHEN
    x_pidginbodybook._overwrite_pidginbodyunit(sue55_agg)

    # THEN
    assert x_pidginbodybook.pidginbodyunits.get(pidginbody_key) != None
    assert x_pidginbodybook.pidginbodyunits.get(pidginbody_key) == sue55_agg


def test_PidginBodyBook_pidginbodyunit_exists_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue55_agg = create_pidginbodyunit(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook = pidginbodybook_shop()
    pidginbody_key = (x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodyunit_exists(pidginbody_key) is False

    # WHEN
    x_pidginbodybook._overwrite_pidginbodyunit(sue55_agg)

    # THEN
    assert x_pidginbodybook.pidginbodyunit_exists(pidginbody_key)


def test_PidginBodyBook_get_pidginbodyunit_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x55_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue55_agg = create_pidginbodyunit(sue_str, x55_event_id, bob_otx, bob2_inx)
    x_pidginbodybook = pidginbodybook_shop()
    x_pidginbodybook._overwrite_pidginbodyunit(sue55_agg)
    event_otx_key = (x55_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodyunit_exists(event_otx_key)

    # WHEN
    gen_pidginbodyunit = x_pidginbodybook.get_pidginbodyunit(event_otx_key)

    # THEN
    assert gen_pidginbodyunit == sue55_agg


def test_PidginBodyBook_eval_pidginbodyrow_SetsAttr_Scenario0_EmptyDict():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue55_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook = pidginbodybook_shop()
    event_otx_key = (x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodyunit_exists(event_otx_key) is False

    # WHEN
    x_pidginbodybook.eval_pidginbodyrow(sue55_pidginbodyrow)

    # THEN
    assert x_pidginbodybook.pidginbodyunit_exists(event_otx_key)
    x_pidginbodyunit = x_pidginbodybook.get_pidginbodyunit(event_otx_key)
    assert x_pidginbodyunit.face_id == sue_str
    assert x_pidginbodyunit.event_id == x_event_id
    assert bob2_inx in x_pidginbodyunit.inx_strs


def test_PidginBodyBook_eval_pidginbodyrow_SetsAttr_Scenario1_MultipleRowsAtSameEvent():
    # ESTABLISH
    x_pidginbodybook = pidginbodybook_shop()
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue1_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook.eval_pidginbodyrow(sue1_pidginbodyrow)
    event_otx_key = (x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodyunit_exists(event_otx_key)

    # WHEN
    bob3_inx = "Bobby"
    sue2_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, bob3_inx)
    x_pidginbodybook.eval_pidginbodyrow(sue2_pidginbodyrow)

    # THEN
    assert x_pidginbodybook.pidginbodyunit_exists(event_otx_key)
    gen_pidginbodyunit = x_pidginbodybook.get_pidginbodyunit(event_otx_key)
    assert gen_pidginbodyunit.face_id == sue_str
    assert gen_pidginbodyunit.event_id == x_event_id
    assert gen_pidginbodyunit.otx_str == bob_otx
    assert gen_pidginbodyunit.inx_strs == {bob2_inx, bob3_inx}


def test_PidginBodyBook_eval_pidginbodyrow_SetsAttr_Scenario2_NoneElementIsHandledCorrectly():
    # ESTABLISH
    x_pidginbodybook = pidginbodybook_shop()
    sue_str = "Sue"
    x_event_id = 55
    bob_otx = "Bob"
    bob2_inx = "Bobito"
    sue1_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, bob2_inx)
    x_pidginbodybook.eval_pidginbodyrow(sue1_pidginbodyrow)
    event_otx_key = (x_event_id, bob_otx)
    assert x_pidginbodybook.pidginbodyunit_exists(event_otx_key)

    # WHEN
    sue2_pidginbodyrow = PidginBodyRow(sue_str, x_event_id, bob_otx, None)
    x_pidginbodybook.eval_pidginbodyrow(sue2_pidginbodyrow)

    # THEN
    assert x_pidginbodybook.pidginbodyunit_exists(event_otx_key)
    gen_pidginbodyunit = x_pidginbodybook.get_pidginbodyunit(event_otx_key)
    assert gen_pidginbodyunit.face_id == sue_str
    assert gen_pidginbodyunit.event_id == x_event_id
    assert gen_pidginbodyunit.otx_str == bob_otx
    assert gen_pidginbodyunit.inx_strs == {bob2_inx}
