from src.a18_etl_toolbox.pidgin_agg import (
    PidginHeartRow,
    PidginHeartUnit,
    PidginHeartBook,
    pidginheartbook_shop,
    pidginheartunit_shop,
    create_pidginheartunit,
)


def test_PidginHeartRow_Exists():
    # ESTABLISH
    sue_str = "Sue"
    x_event_int = 55
    x_otx_bridge = ";"
    x_inx_bridge = ";"
    x_unknown_word = "unknown33"

    # WHEN
    sue55_pidginheartrow = PidginHeartRow(
        sue_str, x_event_int, x_otx_bridge, x_inx_bridge, x_unknown_word
    )

    # THEN
    assert sue55_pidginheartrow
    assert sue55_pidginheartrow.face_name == sue_str
    assert sue55_pidginheartrow.event_int == x_event_int
    assert sue55_pidginheartrow.otx_bridge == x_otx_bridge
    assert sue55_pidginheartrow.inx_bridge == x_inx_bridge
    assert sue55_pidginheartrow.unknown_word == x_unknown_word


def test_PidginHeartUnit_Exists():
    # ESTABLISH
    x_pidginheartunit = PidginHeartUnit()

    # THEN
    assert x_pidginheartunit
    assert x_pidginheartunit.face_name is None
    assert x_pidginheartunit.event_int is None
    assert x_pidginheartunit.otx_bridges is None
    assert x_pidginheartunit.inx_bridges is None
    assert x_pidginheartunit.unknown_words is None


def test_pidginheartunit_shop_ReturnsObj_WithNoValues():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55

    # WHEN
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)

    # THEN
    assert x_pidginheartunit
    assert x_pidginheartunit.face_name == x_face_name
    assert x_pidginheartunit.event_int == x_event_int
    assert x_pidginheartunit.otx_bridges == set()
    assert x_pidginheartunit.inx_bridges == set()
    assert x_pidginheartunit.unknown_words == set()


def test_pidginheartunit_shop_ReturnsObj_WithCoreValues():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_otx_bridge_set = {";"}
    x_inx_bridge_set = {";"}
    x_unknown_word_set = {"unknown33"}

    # WHEN
    x_pidginheartunit = pidginheartunit_shop(
        x_face_name,
        x_event_int,
        x_otx_bridge_set,
        x_inx_bridge_set,
        x_unknown_word_set,
    )

    # THEN
    assert x_pidginheartunit
    assert x_pidginheartunit.face_name == x_face_name
    assert x_pidginheartunit.event_int == x_event_int
    assert x_pidginheartunit.otx_bridges == x_otx_bridge_set
    assert x_pidginheartunit.inx_bridges == x_inx_bridge_set
    assert ";" in x_pidginheartunit.inx_bridges
    assert x_pidginheartunit.unknown_words == x_unknown_word_set


def test_PidginHeartUnit_add_otx_bridge_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)
    colon_str = ":"
    print(f"{x_pidginheartunit.otx_bridges=}")
    print(f"{colon_str=}")
    assert colon_str not in x_pidginheartunit.otx_bridges
    assert colon_str not in x_pidginheartunit.inx_bridges
    assert colon_str not in x_pidginheartunit.unknown_words

    # WHEN
    x_pidginheartunit.add_otx_bridge(colon_str)

    # THEN
    assert colon_str in x_pidginheartunit.otx_bridges
    assert colon_str not in x_pidginheartunit.inx_bridges
    assert colon_str not in x_pidginheartunit.unknown_words


def test_PidginHeartUnit_add_otx_bridge_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)
    assert None not in x_pidginheartunit.otx_bridges
    assert None not in x_pidginheartunit.inx_bridges
    assert None not in x_pidginheartunit.unknown_words

    # WHEN
    x_pidginheartunit.add_otx_bridge(None)

    # THEN
    assert None in x_pidginheartunit.otx_bridges
    assert None not in x_pidginheartunit.inx_bridges
    assert None not in x_pidginheartunit.unknown_words


def test_PidginHeartUnit_add_otx_bridge_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)
    x_pidginheartunit.add_otx_bridge(None)
    assert None in x_pidginheartunit.otx_bridges

    # WHEN / THEN
    x_pidginheartunit.add_otx_bridge(None)
    assert None in x_pidginheartunit.otx_bridges

    # WHEN / THEN
    colon_str = ":"
    x_pidginheartunit.add_otx_bridge(colon_str)
    assert colon_str in x_pidginheartunit.otx_bridges
    assert None not in x_pidginheartunit.otx_bridges

    # WHEN / THEN
    x_pidginheartunit.add_otx_bridge(None)
    assert colon_str in x_pidginheartunit.otx_bridges
    assert None not in x_pidginheartunit.otx_bridges


def test_PidginHeartUnit_add_otx_bridge_ChangesAttr_Scenario3_NumpyType():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)

    # WHEN / THEN
    x_pidginheartunit.add_otx_bridge(float("nan"))
    assert None in x_pidginheartunit.otx_bridges
    assert len(x_pidginheartunit.otx_bridges) == 1

    # WHEN / THEN
    x_pidginheartunit.add_otx_bridge(float("nan"))
    assert None in x_pidginheartunit.otx_bridges
    assert len(x_pidginheartunit.otx_bridges) == 1


def test_PidginHeartUnit_add_inx_bridge_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)
    colon_str = ":"
    assert colon_str not in x_pidginheartunit.otx_bridges
    assert colon_str not in x_pidginheartunit.inx_bridges
    assert colon_str not in x_pidginheartunit.unknown_words

    # WHEN
    x_pidginheartunit.add_inx_bridge(colon_str)

    # THEN
    assert colon_str not in x_pidginheartunit.otx_bridges
    assert colon_str in x_pidginheartunit.inx_bridges
    assert colon_str not in x_pidginheartunit.unknown_words


def test_PidginHeartUnit_add_inx_bridge_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)
    assert None not in x_pidginheartunit.otx_bridges
    assert None not in x_pidginheartunit.inx_bridges
    assert None not in x_pidginheartunit.unknown_words

    # WHEN
    x_pidginheartunit.add_inx_bridge(None)

    # THEN
    assert None not in x_pidginheartunit.otx_bridges
    assert None in x_pidginheartunit.inx_bridges
    assert None not in x_pidginheartunit.unknown_words


def test_PidginHeartUnit_add_inx_bridge_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)
    x_pidginheartunit.add_inx_bridge(None)
    assert None in x_pidginheartunit.inx_bridges

    # WHEN / THEN
    x_pidginheartunit.add_inx_bridge(None)
    assert None in x_pidginheartunit.inx_bridges

    # WHEN / THEN
    colon_str = ":"
    x_pidginheartunit.add_inx_bridge(colon_str)
    assert colon_str in x_pidginheartunit.inx_bridges
    assert None not in x_pidginheartunit.inx_bridges

    # WHEN / THEN
    x_pidginheartunit.add_inx_bridge(None)
    assert colon_str in x_pidginheartunit.inx_bridges
    assert None not in x_pidginheartunit.inx_bridges


def test_PidginHeartUnit_add_inx_bridge_ChangesAttr_Scenario3_NumpyType():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)

    # WHEN / THEN
    x_pidginheartunit.add_inx_bridge(float("nan"))
    assert None in x_pidginheartunit.inx_bridges
    assert len(x_pidginheartunit.inx_bridges) == 1

    # WHEN / THEN
    x_pidginheartunit.add_inx_bridge(float("nan"))
    assert None in x_pidginheartunit.inx_bridges
    assert len(x_pidginheartunit.inx_bridges) == 1


def test_PidginHeartUnit_add_unknown_word_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)
    colon_str = ":"
    assert colon_str not in x_pidginheartunit.otx_bridges
    assert colon_str not in x_pidginheartunit.inx_bridges
    assert colon_str not in x_pidginheartunit.unknown_words

    # WHEN
    x_pidginheartunit.add_unknown_word(colon_str)

    # THEN
    assert colon_str not in x_pidginheartunit.otx_bridges
    assert colon_str not in x_pidginheartunit.inx_bridges
    assert colon_str in x_pidginheartunit.unknown_words


def test_PidginHeartUnit_add_unknown_word_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)
    assert None not in x_pidginheartunit.otx_bridges
    assert None not in x_pidginheartunit.inx_bridges
    assert None not in x_pidginheartunit.unknown_words

    # WHEN
    x_pidginheartunit.add_unknown_word(None)

    # THEN
    assert None not in x_pidginheartunit.otx_bridges
    assert None not in x_pidginheartunit.inx_bridges
    assert None in x_pidginheartunit.unknown_words


def test_PidginHeartUnit_add_unknown_word_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)
    x_pidginheartunit.add_unknown_word(None)
    assert None in x_pidginheartunit.unknown_words

    # WHEN / THEN
    x_pidginheartunit.add_unknown_word(None)
    assert None in x_pidginheartunit.unknown_words

    # WHEN / THEN
    colon_str = ":"
    x_pidginheartunit.add_unknown_word(colon_str)
    assert colon_str in x_pidginheartunit.unknown_words
    assert None not in x_pidginheartunit.unknown_words

    # WHEN / THEN
    x_pidginheartunit.add_unknown_word(None)
    assert colon_str in x_pidginheartunit.unknown_words
    assert None not in x_pidginheartunit.unknown_words


def test_PidginHeartUnit_add_unknown_word_ChangesAttr_Scenario3_NumpyType():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_pidginheartunit = pidginheartunit_shop(x_face_name, x_event_int)

    # WHEN / THEN
    x_pidginheartunit.add_unknown_word(float("nan"))
    assert None in x_pidginheartunit.unknown_words
    assert len(x_pidginheartunit.unknown_words) == 1

    # WHEN / THEN
    x_pidginheartunit.add_unknown_word(float("nan"))
    assert None in x_pidginheartunit.unknown_words
    assert len(x_pidginheartunit.unknown_words) == 1


def test_create_pidginheartunit_ReturnsObj():
    # ESTABLISH
    x_face_name = "Sue"
    x_event_int = 55
    x_otx_bridge = ";"
    x_inx_bridge = ";"
    x_unknown_word = "unknown33"

    # WHEN
    x_pidginheartunit = create_pidginheartunit(
        x_face_name, x_event_int, x_otx_bridge, x_inx_bridge, x_unknown_word
    )

    # THEN
    x_face_name = x_face_name
    x_event_int = x_event_int
    x_otx_bridge_set = {x_otx_bridge}
    x_inx_bridge_set = {x_inx_bridge}
    x_unknown_word_set = {x_unknown_word}
    assert x_pidginheartunit
    assert x_pidginheartunit.face_name == x_face_name
    assert x_pidginheartunit.event_int == x_event_int
    assert x_pidginheartunit.otx_bridges == x_otx_bridge_set
    assert x_pidginheartunit.inx_bridges == x_inx_bridge_set
    assert x_pidginheartunit.unknown_words == x_unknown_word_set


def test_PidginHeartUnit_is_valid_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN / THEN
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55)
    assert x_pidginheartunit.is_valid() is False

    # WHEN / THEN
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55, {";"}, {":"}, {uk33})
    assert x_pidginheartunit.is_valid()

    # WHEN / THEN
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55, {None}, {None}, {None})
    assert x_pidginheartunit.is_valid()

    # WHEN / THEN
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55, {":", "/"}, {":"}, {uk33})
    assert x_pidginheartunit.is_valid() is False

    # WHEN / THEN
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55, {":"}, {":", "/"}, {uk33})
    assert x_pidginheartunit.is_valid() is False

    # WHEN / THEN
    uk44 = "unknown44"
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55, {":"}, {":"}, {uk33, uk44})
    assert x_pidginheartunit.is_valid() is False


def test_PidginHeartUnit_get_valid_pidginheartrow_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN / THEN
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55)
    assert x_pidginheartunit.is_valid() is False
    assert None == x_pidginheartunit.get_valid_pidginheartrow()


def test_PidginHeartUnit_get_valid_pidginheartrow_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55, {";"}, {":"}, {uk33})

    # THEN
    assert x_pidginheartunit.is_valid()
    assert x_pidginheartunit.get_valid_pidginheartrow()
    s55_pidginheartrow = x_pidginheartunit.get_valid_pidginheartrow()
    assert s55_pidginheartrow.face_name == sue_str
    assert s55_pidginheartrow.event_int == e55
    assert s55_pidginheartrow.otx_bridge == ";"
    assert s55_pidginheartrow.inx_bridge == ":"
    assert s55_pidginheartrow.unknown_word == uk33


def test_PidginHeartUnit_get_valid_pidginheartrow_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55, {None}, {None}, {None})
    assert x_pidginheartunit.is_valid()
    assert x_pidginheartunit.get_valid_pidginheartrow()
    s55_pidginheartrow = x_pidginheartunit.get_valid_pidginheartrow()
    assert s55_pidginheartrow.face_name == sue_str
    assert s55_pidginheartrow.event_int == e55
    assert s55_pidginheartrow.otx_bridge is None
    assert s55_pidginheartrow.inx_bridge is None
    assert s55_pidginheartrow.unknown_word is None


def test_PidginHeartUnit_get_valid_pidginheartrow_ReturnsObj_Scenario3():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidginheartunit = pidginheartunit_shop(sue_str, e55, {":", "/"}, {":"}, {uk33})

    # THEN
    assert x_pidginheartunit.is_valid() is False
    assert not x_pidginheartunit.get_valid_pidginheartrow()


def test_PidginHeartBook_Exists():
    # ESTABLISH / WHEN
    x_pidginheartbook = PidginHeartBook()

    # THEN
    assert x_pidginheartbook
    assert x_pidginheartbook.pidginheartunits is None


def test_eventsaggs_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginheartbook = pidginheartbook_shop()

    # THEN
    assert x_pidginheartbook
    assert x_pidginheartbook.pidginheartunits == {}


def test_PidginHeartBook_overwrite_pidginheartunit_SetsAttr_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    x_event_int = 55
    sue55_agg = create_pidginheartunit(sue_str, x_event_int, ";", ":", "uk33")
    x_pidginheartbook = pidginheartbook_shop()
    assert x_pidginheartbook.pidginheartunits.get(x_event_int) is None

    # WHEN
    x_pidginheartbook._overwrite_pidginheartunit(sue55_agg)

    # THEN
    assert x_pidginheartbook.pidginheartunits.get(x_event_int) != None
    assert x_pidginheartbook.pidginheartunits.get(x_event_int) == sue55_agg


def test_PidginHeartBook_pidginheartunit_exists_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x_event_int = 55
    sue55_agg = create_pidginheartunit(sue_str, x_event_int, ";", ":", "uk33")
    x_pidginheartbook = pidginheartbook_shop()
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int) is False

    # WHEN
    x_pidginheartbook._overwrite_pidginheartunit(sue55_agg)

    # THEN
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)


def test_PidginHeartBook_get_pidginheartunit_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x55_event_int = 55
    sue55_agg = create_pidginheartunit(sue_str, x55_event_int, ";", ":", "uk33")
    x_pidginheartbook = pidginheartbook_shop()
    x_pidginheartbook._overwrite_pidginheartunit(sue55_agg)
    assert x_pidginheartbook.pidginheartunit_exists(x55_event_int)

    # WHEN
    gen_pidginheartunit = x_pidginheartbook.get_pidginheartunit(x55_event_int)

    # THEN
    assert gen_pidginheartunit == sue55_agg


def test_PidginHeartBook_eval_pidginheartrow_SetsAttr_Scenario0_EmptyDict():
    # ESTABLISH
    sue_str = "Sue"
    x_event_int = 55
    x_otx_bridge = ";"
    x_inx_bridge = ";"
    x_unknown_word = "unknown33"
    sue55_pidginheartrow = PidginHeartRow(
        sue_str, x_event_int, x_otx_bridge, x_inx_bridge, x_unknown_word
    )
    x_pidginheartbook = pidginheartbook_shop()
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int) is False

    # WHEN
    x_pidginheartbook.eval_pidginheartrow(sue55_pidginheartrow)

    # THEN
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)
    x_pidginheartunit = x_pidginheartbook.get_pidginheartunit(x_event_int)
    assert x_pidginheartunit.face_name == sue_str
    assert x_pidginheartunit.event_int == x_event_int
    assert x_otx_bridge in x_pidginheartunit.otx_bridges
    assert x_inx_bridge in x_pidginheartunit.inx_bridges
    assert x_unknown_word in x_pidginheartunit.unknown_words


def test_PidginHeartBook_eval_pidginheartrow_SetsAttr_Scenario0_EmptyDict():
    # ESTABLISH
    sue_str = "Sue"
    x_event_int = 55
    x_otx_bridge = ";"
    x_inx_bridge = ";"
    x_unknown_word = "unknown33"
    sue55_pidginheartrow = PidginHeartRow(
        sue_str, x_event_int, x_otx_bridge, x_inx_bridge, x_unknown_word
    )
    x_pidginheartbook = pidginheartbook_shop()
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int) is False

    # WHEN
    x_pidginheartbook.eval_pidginheartrow(sue55_pidginheartrow)

    # THEN
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)
    x_pidginheartunit = x_pidginheartbook.get_pidginheartunit(x_event_int)
    assert x_pidginheartunit.face_name == sue_str
    assert x_pidginheartunit.event_int == x_event_int
    assert x_otx_bridge in x_pidginheartunit.otx_bridges
    assert x_inx_bridge in x_pidginheartunit.inx_bridges
    assert x_unknown_word in x_pidginheartunit.unknown_words


def test_PidginHeartBook_eval_pidginheartrow_SetsAttr_Scenario1_MultipleRowsAtSameEvent():
    # ESTABLISH
    x_pidginheartbook = pidginheartbook_shop()
    sue_str = "Sue"
    x_event_int = 55
    colon_str = ":"
    comma_str = ","
    x_unk33 = "unknown33"
    sue1_pidginheartrow = PidginHeartRow(
        sue_str, x_event_int, colon_str, comma_str, x_unk33
    )
    x_pidginheartbook.eval_pidginheartrow(sue1_pidginheartrow)
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)

    # WHEN
    slash_str = "/"
    semic_str = ";"
    x_unk44 = "unknown44"
    sue2_pidginheartrow = PidginHeartRow(
        sue_str, x_event_int, slash_str, semic_str, x_unk44
    )
    x_pidginheartbook.eval_pidginheartrow(sue2_pidginheartrow)

    # THEN
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)
    gen_pidginheartunit = x_pidginheartbook.get_pidginheartunit(x_event_int)
    assert gen_pidginheartunit.face_name == sue_str
    assert gen_pidginheartunit.event_int == x_event_int
    assert gen_pidginheartunit.otx_bridges == {colon_str, slash_str}
    assert gen_pidginheartunit.inx_bridges == {comma_str, semic_str}
    assert gen_pidginheartunit.unknown_words == {x_unk33, x_unk44}


def test_PidginHeartBook_eval_pidginheartrow_SetsAttr_Scenario2_NoneElementIsChangedCorrectly():
    # ESTABLISH
    x_pidginheartbook = pidginheartbook_shop()
    sue_str = "Sue"
    x_event_int = 55
    colon_str = ":"
    sue1_pidginheartrow = PidginHeartRow(sue_str, x_event_int, colon_str, None, None)
    x_pidginheartbook.eval_pidginheartrow(sue1_pidginheartrow)
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)

    # WHEN
    slash_str = "/"
    x_unk44 = "unknown44"
    sue2_pidginheartrow = PidginHeartRow(sue_str, x_event_int, slash_str, None, x_unk44)
    x_pidginheartbook.eval_pidginheartrow(sue2_pidginheartrow)

    # THEN
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)
    gen_pidginheartunit = x_pidginheartbook.get_pidginheartunit(x_event_int)
    assert gen_pidginheartunit.face_name == sue_str
    assert gen_pidginheartunit.event_int == x_event_int
    assert gen_pidginheartunit.otx_bridges == {colon_str, slash_str}
    assert gen_pidginheartunit.inx_bridges == {None}
    assert gen_pidginheartunit.unknown_words == {x_unk44}


def test_PidginHeartBook_add_pidginheartrow_SetsAttr_Scenario2_NoneElementIsChangedCorrectly():
    # ESTABLISH
    x_pidginheartbook = pidginheartbook_shop()
    sue_str = "Sue"
    x_event_int = 55
    colon_str = ":"
    uk44 = "unknown44"
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int) is False

    # WHEN
    x_pidginheartbook.add_pidginheartrow(sue_str, x_event_int, colon_str, None, uk44)

    # THEN
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)
    gen_pidginheartunit = x_pidginheartbook.get_pidginheartunit(x_event_int)
    assert gen_pidginheartunit.face_name == sue_str
    assert gen_pidginheartunit.event_int == x_event_int
    assert gen_pidginheartunit.otx_bridges == {colon_str}
    assert gen_pidginheartunit.inx_bridges == {None}
    assert gen_pidginheartunit.unknown_words == {uk44}


def test_PidginHeartBook_event_int_is_valid_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    x_pidginheartbook = pidginheartbook_shop()
    x_event_int = 55

    # WHEN / THEN
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int) is False
    assert x_pidginheartbook.event_int_is_valid(x_event_int) is False


def test_PidginHeartBook_event_int_is_valid_ReturnsObj_Scenario1_SingleEntry():
    # ESTABLISH
    x_pidginheartbook = pidginheartbook_shop()
    x_event_int = 55
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int) is False
    assert x_pidginheartbook.event_int_is_valid(x_event_int) is False
    sue_str = "Sue"
    colon_str = ":"
    sue1_pidginheartrow = PidginHeartRow(sue_str, x_event_int, colon_str, None, None)
    x_pidginheartbook.eval_pidginheartrow(sue1_pidginheartrow)
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)
    assert x_pidginheartbook.event_int_is_valid(x_event_int)

    # WHEN
    slash_str = "/"
    x_unk44 = "unknown44"
    sue2_pidginheartrow = PidginHeartRow(sue_str, x_event_int, slash_str, None, x_unk44)
    x_pidginheartbook.eval_pidginheartrow(sue2_pidginheartrow)

    # THEN
    assert x_pidginheartbook.pidginheartunit_exists(x_event_int)
    assert x_pidginheartbook.event_int_is_valid(x_event_int) is False
