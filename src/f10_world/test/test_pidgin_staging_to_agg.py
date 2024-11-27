from src.f10_world.pidgin_staging_to_agg import (
    PidginCore,
    PidginAggBook,
    pidginaggbook_shop,
    pidgincore_shop,
    create_pidgincore,
    PidginRow,
)


def test_PidginRow_Exists():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    x_otx_wall = ";"
    x_inx_wall = ";"
    x_unknown_word = "unknown33"

    # WHEN
    sue55_pidginrow = PidginRow(
        sue_str, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
    )

    # THEN
    assert sue55_pidginrow
    assert sue55_pidginrow.face_id == sue_str
    assert sue55_pidginrow.event_id == x_event_id
    assert sue55_pidginrow.otx_wall == x_otx_wall
    assert sue55_pidginrow.inx_wall == x_inx_wall
    assert sue55_pidginrow.unknown_word == x_unknown_word


def test_PidginCore_Exists():
    # ESTABLISH
    x_pidgincore = PidginCore()

    # THEN
    assert x_pidgincore
    assert x_pidgincore.face_id is None
    assert x_pidgincore.event_id is None
    assert x_pidgincore.otx_walls is None
    assert x_pidgincore.inx_walls is None
    assert x_pidgincore.unknown_words is None


def test_pidgincore_shop_ReturnsObj_WithNoValues():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55

    # WHEN
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)

    # THEN
    assert x_pidgincore
    assert x_pidgincore.face_id == x_face_id
    assert x_pidgincore.event_id == x_event_id
    assert x_pidgincore.otx_walls == set()
    assert x_pidgincore.inx_walls == set()
    assert x_pidgincore.unknown_words == set()


def test_pidgincore_shop_ReturnsObj_WithCoreValues():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_otx_wall_set = {";"}
    x_inx_wall_set = {";"}
    x_unknown_word_set = {"unknown33"}

    # WHEN
    x_pidgincore = pidgincore_shop(
        x_face_id,
        x_event_id,
        x_otx_wall_set,
        x_inx_wall_set,
        x_unknown_word_set,
    )

    # THEN
    assert x_pidgincore
    assert x_pidgincore.face_id == x_face_id
    assert x_pidgincore.event_id == x_event_id
    assert x_pidgincore.otx_walls == x_otx_wall_set
    assert x_pidgincore.inx_walls == x_inx_wall_set
    assert ";" in x_pidgincore.inx_walls
    assert x_pidgincore.unknown_words == x_unknown_word_set


def test_PidginCore_add_otx_wall_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)
    colon_str = ":"
    print(f"{x_pidgincore.otx_walls=}")
    print(f"{colon_str=}")
    assert colon_str not in x_pidgincore.otx_walls
    assert colon_str not in x_pidgincore.inx_walls
    assert colon_str not in x_pidgincore.unknown_words

    # WHEN
    x_pidgincore.add_otx_wall(colon_str)

    # THEN
    assert colon_str in x_pidgincore.otx_walls
    assert colon_str not in x_pidgincore.inx_walls
    assert colon_str not in x_pidgincore.unknown_words


def test_PidginCore_add_otx_wall_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)
    assert None not in x_pidgincore.otx_walls
    assert None not in x_pidgincore.inx_walls
    assert None not in x_pidgincore.unknown_words

    # WHEN
    x_pidgincore.add_otx_wall(None)

    # THEN
    assert None in x_pidgincore.otx_walls
    assert None not in x_pidgincore.inx_walls
    assert None not in x_pidgincore.unknown_words


def test_PidginCore_add_otx_wall_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)
    x_pidgincore.add_otx_wall(None)
    assert None in x_pidgincore.otx_walls

    # WHEN / THEN
    x_pidgincore.add_otx_wall(None)
    assert None in x_pidgincore.otx_walls

    # WHEN / THEN
    colon_str = ":"
    x_pidgincore.add_otx_wall(colon_str)
    assert colon_str in x_pidgincore.otx_walls
    assert None not in x_pidgincore.otx_walls

    # WHEN / THEN
    x_pidgincore.add_otx_wall(None)
    assert colon_str in x_pidgincore.otx_walls
    assert None not in x_pidgincore.otx_walls


def test_PidginCore_add_inx_wall_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)
    colon_str = ":"
    assert colon_str not in x_pidgincore.otx_walls
    assert colon_str not in x_pidgincore.inx_walls
    assert colon_str not in x_pidgincore.unknown_words

    # WHEN
    x_pidgincore.add_inx_wall(colon_str)

    # THEN
    assert colon_str not in x_pidgincore.otx_walls
    assert colon_str in x_pidgincore.inx_walls
    assert colon_str not in x_pidgincore.unknown_words


def test_PidginCore_add_inx_wall_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)
    assert None not in x_pidgincore.otx_walls
    assert None not in x_pidgincore.inx_walls
    assert None not in x_pidgincore.unknown_words

    # WHEN
    x_pidgincore.add_inx_wall(None)

    # THEN
    assert None not in x_pidgincore.otx_walls
    assert None in x_pidgincore.inx_walls
    assert None not in x_pidgincore.unknown_words


def test_PidginCore_add_inx_wall_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)
    x_pidgincore.add_inx_wall(None)
    assert None in x_pidgincore.inx_walls

    # WHEN / THEN
    x_pidgincore.add_inx_wall(None)
    assert None in x_pidgincore.inx_walls

    # WHEN / THEN
    colon_str = ":"
    x_pidgincore.add_inx_wall(colon_str)
    assert colon_str in x_pidgincore.inx_walls
    assert None not in x_pidgincore.inx_walls

    # WHEN / THEN
    x_pidgincore.add_inx_wall(None)
    assert colon_str in x_pidgincore.inx_walls
    assert None not in x_pidgincore.inx_walls


def test_PidginCore_add_unknown_word_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)
    colon_str = ":"
    assert colon_str not in x_pidgincore.otx_walls
    assert colon_str not in x_pidgincore.inx_walls
    assert colon_str not in x_pidgincore.unknown_words

    # WHEN
    x_pidgincore.add_unknown_word(colon_str)

    # THEN
    assert colon_str not in x_pidgincore.otx_walls
    assert colon_str not in x_pidgincore.inx_walls
    assert colon_str in x_pidgincore.unknown_words


def test_PidginCore_add_unknown_word_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)
    assert None not in x_pidgincore.otx_walls
    assert None not in x_pidgincore.inx_walls
    assert None not in x_pidgincore.unknown_words

    # WHEN
    x_pidgincore.add_unknown_word(None)

    # THEN
    assert None not in x_pidgincore.otx_walls
    assert None not in x_pidgincore.inx_walls
    assert None in x_pidgincore.unknown_words


def test_PidginCore_add_unknown_word_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidgincore = pidgincore_shop(x_face_id, x_event_id)
    x_pidgincore.add_unknown_word(None)
    assert None in x_pidgincore.unknown_words

    # WHEN / THEN
    x_pidgincore.add_unknown_word(None)
    assert None in x_pidgincore.unknown_words

    # WHEN / THEN
    colon_str = ":"
    x_pidgincore.add_unknown_word(colon_str)
    assert colon_str in x_pidgincore.unknown_words
    assert None not in x_pidgincore.unknown_words

    # WHEN / THEN
    x_pidgincore.add_unknown_word(None)
    assert colon_str in x_pidgincore.unknown_words
    assert None not in x_pidgincore.unknown_words


def test_create_pidgincore_ReturnsObj():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_otx_wall = ";"
    x_inx_wall = ";"
    x_unknown_word = "unknown33"

    # WHEN
    x_pidgincore = create_pidgincore(
        x_face_id, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
    )

    # THEN
    x_face_id = x_face_id
    x_event_id = x_event_id
    x_otx_wall_set = {x_otx_wall}
    x_inx_wall_set = {x_inx_wall}
    x_unknown_word_set = {x_unknown_word}
    assert x_pidgincore
    assert x_pidgincore.face_id == x_face_id
    assert x_pidgincore.event_id == x_event_id
    assert x_pidgincore.otx_walls == x_otx_wall_set
    assert x_pidgincore.inx_walls == x_inx_wall_set
    assert x_pidgincore.unknown_words == x_unknown_word_set


def test_PidginCore_is_valid_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN / THEN
    x_pidgincore = pidgincore_shop(sue_str, e55)
    assert x_pidgincore.is_valid() is False

    # WHEN / THEN
    x_pidgincore = pidgincore_shop(sue_str, e55, {";"}, {":"}, {uk33})
    assert x_pidgincore.is_valid()

    # WHEN / THEN
    x_pidgincore = pidgincore_shop(sue_str, e55, {None}, {None}, {None})
    assert x_pidgincore.is_valid()

    # WHEN / THEN
    x_pidgincore = pidgincore_shop(sue_str, e55, {":", "/"}, {":"}, {uk33})
    assert x_pidgincore.is_valid() is False

    # WHEN / THEN
    x_pidgincore = pidgincore_shop(sue_str, e55, {":"}, {":", "/"}, {uk33})
    assert x_pidgincore.is_valid() is False

    # WHEN / THEN
    uk44 = "unknown44"
    x_pidgincore = pidgincore_shop(sue_str, e55, {":"}, {":"}, {uk33, uk44})
    assert x_pidgincore.is_valid() is False


def test_PidginCore_get_valid_pidginrow_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN / THEN
    x_pidgincore = pidgincore_shop(sue_str, e55)
    assert x_pidgincore.is_valid() is False
    assert None == x_pidgincore.get_valid_pidginrow()


def test_PidginCore_get_valid_pidginrow_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidgincore = pidgincore_shop(sue_str, e55, {";"}, {":"}, {uk33})

    # THEN
    assert x_pidgincore.is_valid()
    assert x_pidgincore.get_valid_pidginrow()
    s55_pidginrow = x_pidgincore.get_valid_pidginrow()
    assert s55_pidginrow.face_id == sue_str
    assert s55_pidginrow.event_id == e55
    assert s55_pidginrow.otx_wall == ";"
    assert s55_pidginrow.inx_wall == ":"
    assert s55_pidginrow.unknown_word == uk33


def test_PidginCore_get_valid_pidginrow_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidgincore = pidgincore_shop(sue_str, e55, {None}, {None}, {None})
    assert x_pidgincore.is_valid()
    assert x_pidgincore.get_valid_pidginrow()
    s55_pidginrow = x_pidgincore.get_valid_pidginrow()
    assert s55_pidginrow.face_id == sue_str
    assert s55_pidginrow.event_id == e55
    assert s55_pidginrow.otx_wall is None
    assert s55_pidginrow.inx_wall is None
    assert s55_pidginrow.unknown_word is None


def test_PidginCore_get_valid_pidginrow_ReturnsObj_Scenario3():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidgincore = pidgincore_shop(sue_str, e55, {":", "/"}, {":"}, {uk33})

    # THEN
    assert x_pidgincore.is_valid() is False
    assert not x_pidgincore.get_valid_pidginrow()


def test_PidginCore_get_valid_pidginrow_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidgincore = pidgincore_shop(sue_str, e55, {":"}, {":", "/"}, {uk33})

    # THEN
    assert x_pidgincore.is_valid() is False
    assert not x_pidgincore.get_valid_pidginrow()


def test_PidginCore_get_valid_pidginrow_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    uk44 = "unknown44"
    x_pidgincore = pidgincore_shop(sue_str, e55, {":"}, {":"}, {uk33, uk44})

    # THEN
    assert x_pidgincore.is_valid() is False
    assert not x_pidgincore.get_valid_pidginrow()


def test_PidginAggBook_Exists():
    # ESTABLISH / WHEN
    x_pidginaggbook = PidginAggBook()

    # THEN
    assert x_pidginaggbook
    assert x_pidginaggbook.pidgincores is None


def test_eventsaggs_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginaggbook = pidginaggbook_shop()

    # THEN
    assert x_pidginaggbook
    assert x_pidginaggbook.pidgincores == {}


def test_PidginAggBook_overwrite_pidgincore_SetsAttr_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    sue55_agg = create_pidgincore(sue_str, x_event_id, ";", ":", "uk33")
    x_pidginaggbook = pidginaggbook_shop()
    assert x_pidginaggbook.pidgincores.get((sue_str, x_event_id)) is None

    # WHEN
    x_pidginaggbook._overwrite_pidgincore(sue55_agg)

    # THEN
    assert x_pidginaggbook.pidgincores.get((sue_str, x_event_id)) != None
    assert x_pidginaggbook.pidgincores.get((sue_str, x_event_id)) == sue55_agg


def test_PidginAggBook_pidgincore_exists_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    sue55_agg = create_pidgincore(sue_str, x_event_id, ";", ":", "uk33")
    x_pidginaggbook = pidginaggbook_shop()
    assert x_pidginaggbook.pidgincore_exists((sue_str, x_event_id)) is False

    # WHEN
    x_pidginaggbook._overwrite_pidgincore(sue55_agg)

    # THEN
    assert x_pidginaggbook.pidgincore_exists((sue_str, x_event_id))


def test_PidginAggBook_get_pidgincore_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x55_event_id = 55
    sue55_agg = create_pidgincore(sue_str, x55_event_id, ";", ":", "uk33")
    x_pidginaggbook = pidginaggbook_shop()
    x_pidginaggbook._overwrite_pidgincore(sue55_agg)
    sue55_key = (sue_str, x55_event_id)
    assert x_pidginaggbook.pidgincore_exists(sue55_key)

    # WHEN
    gen_pidgincore = x_pidginaggbook.get_pidgincore(sue55_key)

    # THEN
    assert gen_pidgincore == sue55_agg


def test_PidginAggBook_eval_pidginrow_SetsAttr_Scenario0_EmptyDict():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    x_otx_wall = ";"
    x_inx_wall = ";"
    x_unknown_word = "unknown33"
    sue55_pidginrow = PidginRow(
        sue_str, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
    )
    x_pidginaggbook = pidginaggbook_shop()
    sue55_key = (sue_str, x_event_id)
    assert x_pidginaggbook.pidgincore_exists(sue55_key) is False

    # WHEN
    x_pidginaggbook.eval_pidginrow(sue55_pidginrow)

    # THEN
    assert x_pidginaggbook.pidgincore_exists(sue55_key)
    x_pidgincore = x_pidginaggbook.get_pidgincore(sue55_key)
    assert x_pidgincore.face_id == sue_str
    assert x_pidgincore.event_id == x_event_id
    assert x_otx_wall in x_pidgincore.otx_walls
    assert x_inx_wall in x_pidgincore.inx_walls
    assert x_unknown_word in x_pidgincore.unknown_words


def test_PidginAggBook_eval_pidginrow_SetsAttr_Scenario0_EmptyDict():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    x_otx_wall = ";"
    x_inx_wall = ";"
    x_unknown_word = "unknown33"
    sue55_pidginrow = PidginRow(
        sue_str, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
    )
    x_pidginaggbook = pidginaggbook_shop()
    sue55_key = (sue_str, x_event_id)
    assert x_pidginaggbook.pidgincore_exists(sue55_key) is False

    # WHEN
    x_pidginaggbook.eval_pidginrow(sue55_pidginrow)

    # THEN
    assert x_pidginaggbook.pidgincore_exists(sue55_key)
    x_pidgincore = x_pidginaggbook.get_pidgincore(sue55_key)
    assert x_pidgincore.face_id == sue_str
    assert x_pidgincore.event_id == x_event_id
    assert x_otx_wall in x_pidgincore.otx_walls
    assert x_inx_wall in x_pidgincore.inx_walls
    assert x_unknown_word in x_pidgincore.unknown_words


def test_PidginAggBook_eval_pidginrow_SetsAttr_Scenario1_MultipleRowsAtSameEvent():
    # ESTABLISH
    x_pidginaggbook = pidginaggbook_shop()
    sue_str = "Sue"
    x_event_id = 55
    colon_str = ":"
    comma_str = ","
    x_unk33 = "unknown33"
    sue1_pidginrow = PidginRow(sue_str, x_event_id, colon_str, comma_str, x_unk33)
    x_pidginaggbook.eval_pidginrow(sue1_pidginrow)
    sue55_key = (sue_str, x_event_id)
    assert x_pidginaggbook.pidgincore_exists(sue55_key)

    # WHEN
    slash_str = "/"
    semic_str = ";"
    x_unk44 = "unknown44"
    sue2_pidginrow = PidginRow(sue_str, x_event_id, slash_str, semic_str, x_unk44)
    x_pidginaggbook.eval_pidginrow(sue2_pidginrow)

    # THEN
    assert x_pidginaggbook.pidgincore_exists(sue55_key)
    gen_pidgincore = x_pidginaggbook.get_pidgincore(sue55_key)
    assert gen_pidgincore.face_id == sue_str
    assert gen_pidgincore.event_id == x_event_id
    assert gen_pidgincore.otx_walls == {colon_str, slash_str}
    assert gen_pidgincore.inx_walls == {comma_str, semic_str}
    assert gen_pidgincore.unknown_words == {x_unk33, x_unk44}


def test_PidginAggBook_eval_pidginrow_SetsAttr_Scenario2_NoneElementIsHandledCorrectly():
    # ESTABLISH
    x_pidginaggbook = pidginaggbook_shop()
    sue_str = "Sue"
    x_event_id = 55
    colon_str = ":"
    sue1_pidginrow = PidginRow(sue_str, x_event_id, colon_str, None, None)
    x_pidginaggbook.eval_pidginrow(sue1_pidginrow)
    sue55_key = (sue_str, x_event_id)
    assert x_pidginaggbook.pidgincore_exists(sue55_key)

    # WHEN
    slash_str = "/"
    x_unk44 = "unknown44"
    sue2_pidginrow = PidginRow(sue_str, x_event_id, slash_str, None, x_unk44)
    x_pidginaggbook.eval_pidginrow(sue2_pidginrow)

    # THEN
    assert x_pidginaggbook.pidgincore_exists(sue55_key)
    gen_pidgincore = x_pidginaggbook.get_pidgincore(sue55_key)
    assert gen_pidgincore.face_id == sue_str
    assert gen_pidgincore.event_id == x_event_id
    assert gen_pidgincore.otx_walls == {colon_str, slash_str}
    assert gen_pidgincore.inx_walls == {None}
    assert gen_pidgincore.unknown_words == {x_unk44}
