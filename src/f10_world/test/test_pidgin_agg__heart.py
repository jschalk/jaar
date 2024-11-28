from src.f10_world.pidgin_agg import (
    PidginHeartRow,
    PidginHeartCore,
    PidginHeartBook,
    pidginheartbook_shop,
    pidginheartcore_shop,
    create_pidginheartcore,
)


def test_PidginHeartRow_Exists():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    x_otx_wall = ";"
    x_inx_wall = ";"
    x_unknown_word = "unknown33"

    # WHEN
    sue55_pidginheartrow = PidginHeartRow(
        sue_str, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
    )

    # THEN
    assert sue55_pidginheartrow
    assert sue55_pidginheartrow.face_id == sue_str
    assert sue55_pidginheartrow.event_id == x_event_id
    assert sue55_pidginheartrow.otx_wall == x_otx_wall
    assert sue55_pidginheartrow.inx_wall == x_inx_wall
    assert sue55_pidginheartrow.unknown_word == x_unknown_word


def test_PidginHeartCore_Exists():
    # ESTABLISH
    x_pidginheartcore = PidginHeartCore()

    # THEN
    assert x_pidginheartcore
    assert x_pidginheartcore.face_id is None
    assert x_pidginheartcore.event_id is None
    assert x_pidginheartcore.otx_walls is None
    assert x_pidginheartcore.inx_walls is None
    assert x_pidginheartcore.unknown_words is None


def test_pidginheartcore_shop_ReturnsObj_WithNoValues():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55

    # WHEN
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)

    # THEN
    assert x_pidginheartcore
    assert x_pidginheartcore.face_id == x_face_id
    assert x_pidginheartcore.event_id == x_event_id
    assert x_pidginheartcore.otx_walls == set()
    assert x_pidginheartcore.inx_walls == set()
    assert x_pidginheartcore.unknown_words == set()


def test_pidginheartcore_shop_ReturnsObj_WithCoreValues():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_otx_wall_set = {";"}
    x_inx_wall_set = {";"}
    x_unknown_word_set = {"unknown33"}

    # WHEN
    x_pidginheartcore = pidginheartcore_shop(
        x_face_id,
        x_event_id,
        x_otx_wall_set,
        x_inx_wall_set,
        x_unknown_word_set,
    )

    # THEN
    assert x_pidginheartcore
    assert x_pidginheartcore.face_id == x_face_id
    assert x_pidginheartcore.event_id == x_event_id
    assert x_pidginheartcore.otx_walls == x_otx_wall_set
    assert x_pidginheartcore.inx_walls == x_inx_wall_set
    assert ";" in x_pidginheartcore.inx_walls
    assert x_pidginheartcore.unknown_words == x_unknown_word_set


def test_PidginHeartCore_add_otx_wall_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)
    colon_str = ":"
    print(f"{x_pidginheartcore.otx_walls=}")
    print(f"{colon_str=}")
    assert colon_str not in x_pidginheartcore.otx_walls
    assert colon_str not in x_pidginheartcore.inx_walls
    assert colon_str not in x_pidginheartcore.unknown_words

    # WHEN
    x_pidginheartcore.add_otx_wall(colon_str)

    # THEN
    assert colon_str in x_pidginheartcore.otx_walls
    assert colon_str not in x_pidginheartcore.inx_walls
    assert colon_str not in x_pidginheartcore.unknown_words


def test_PidginHeartCore_add_otx_wall_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)
    assert None not in x_pidginheartcore.otx_walls
    assert None not in x_pidginheartcore.inx_walls
    assert None not in x_pidginheartcore.unknown_words

    # WHEN
    x_pidginheartcore.add_otx_wall(None)

    # THEN
    assert None in x_pidginheartcore.otx_walls
    assert None not in x_pidginheartcore.inx_walls
    assert None not in x_pidginheartcore.unknown_words


def test_PidginHeartCore_add_otx_wall_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)
    x_pidginheartcore.add_otx_wall(None)
    assert None in x_pidginheartcore.otx_walls

    # WHEN / THEN
    x_pidginheartcore.add_otx_wall(None)
    assert None in x_pidginheartcore.otx_walls

    # WHEN / THEN
    colon_str = ":"
    x_pidginheartcore.add_otx_wall(colon_str)
    assert colon_str in x_pidginheartcore.otx_walls
    assert None not in x_pidginheartcore.otx_walls

    # WHEN / THEN
    x_pidginheartcore.add_otx_wall(None)
    assert colon_str in x_pidginheartcore.otx_walls
    assert None not in x_pidginheartcore.otx_walls


def test_PidginHeartCore_add_inx_wall_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)
    colon_str = ":"
    assert colon_str not in x_pidginheartcore.otx_walls
    assert colon_str not in x_pidginheartcore.inx_walls
    assert colon_str not in x_pidginheartcore.unknown_words

    # WHEN
    x_pidginheartcore.add_inx_wall(colon_str)

    # THEN
    assert colon_str not in x_pidginheartcore.otx_walls
    assert colon_str in x_pidginheartcore.inx_walls
    assert colon_str not in x_pidginheartcore.unknown_words


def test_PidginHeartCore_add_inx_wall_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)
    assert None not in x_pidginheartcore.otx_walls
    assert None not in x_pidginheartcore.inx_walls
    assert None not in x_pidginheartcore.unknown_words

    # WHEN
    x_pidginheartcore.add_inx_wall(None)

    # THEN
    assert None not in x_pidginheartcore.otx_walls
    assert None in x_pidginheartcore.inx_walls
    assert None not in x_pidginheartcore.unknown_words


def test_PidginHeartCore_add_inx_wall_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)
    x_pidginheartcore.add_inx_wall(None)
    assert None in x_pidginheartcore.inx_walls

    # WHEN / THEN
    x_pidginheartcore.add_inx_wall(None)
    assert None in x_pidginheartcore.inx_walls

    # WHEN / THEN
    colon_str = ":"
    x_pidginheartcore.add_inx_wall(colon_str)
    assert colon_str in x_pidginheartcore.inx_walls
    assert None not in x_pidginheartcore.inx_walls

    # WHEN / THEN
    x_pidginheartcore.add_inx_wall(None)
    assert colon_str in x_pidginheartcore.inx_walls
    assert None not in x_pidginheartcore.inx_walls


def test_PidginHeartCore_add_unknown_word_ChangesAttr_Scenario0_AddToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)
    colon_str = ":"
    assert colon_str not in x_pidginheartcore.otx_walls
    assert colon_str not in x_pidginheartcore.inx_walls
    assert colon_str not in x_pidginheartcore.unknown_words

    # WHEN
    x_pidginheartcore.add_unknown_word(colon_str)

    # THEN
    assert colon_str not in x_pidginheartcore.otx_walls
    assert colon_str not in x_pidginheartcore.inx_walls
    assert colon_str in x_pidginheartcore.unknown_words


def test_PidginHeartCore_add_unknown_word_ChangesAttr_Scenario1_AddNoneToEmptySet():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)
    assert None not in x_pidginheartcore.otx_walls
    assert None not in x_pidginheartcore.inx_walls
    assert None not in x_pidginheartcore.unknown_words

    # WHEN
    x_pidginheartcore.add_unknown_word(None)

    # THEN
    assert None not in x_pidginheartcore.otx_walls
    assert None not in x_pidginheartcore.inx_walls
    assert None in x_pidginheartcore.unknown_words


def test_PidginHeartCore_add_unknown_word_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_pidginheartcore = pidginheartcore_shop(x_face_id, x_event_id)
    x_pidginheartcore.add_unknown_word(None)
    assert None in x_pidginheartcore.unknown_words

    # WHEN / THEN
    x_pidginheartcore.add_unknown_word(None)
    assert None in x_pidginheartcore.unknown_words

    # WHEN / THEN
    colon_str = ":"
    x_pidginheartcore.add_unknown_word(colon_str)
    assert colon_str in x_pidginheartcore.unknown_words
    assert None not in x_pidginheartcore.unknown_words

    # WHEN / THEN
    x_pidginheartcore.add_unknown_word(None)
    assert colon_str in x_pidginheartcore.unknown_words
    assert None not in x_pidginheartcore.unknown_words


def test_create_pidginheartcore_ReturnsObj():
    # ESTABLISH
    x_face_id = "Sue"
    x_event_id = 55
    x_otx_wall = ";"
    x_inx_wall = ";"
    x_unknown_word = "unknown33"

    # WHEN
    x_pidginheartcore = create_pidginheartcore(
        x_face_id, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
    )

    # THEN
    x_face_id = x_face_id
    x_event_id = x_event_id
    x_otx_wall_set = {x_otx_wall}
    x_inx_wall_set = {x_inx_wall}
    x_unknown_word_set = {x_unknown_word}
    assert x_pidginheartcore
    assert x_pidginheartcore.face_id == x_face_id
    assert x_pidginheartcore.event_id == x_event_id
    assert x_pidginheartcore.otx_walls == x_otx_wall_set
    assert x_pidginheartcore.inx_walls == x_inx_wall_set
    assert x_pidginheartcore.unknown_words == x_unknown_word_set


def test_PidginHeartCore_is_valid_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN / THEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55)
    assert x_pidginheartcore.is_valid() is False

    # WHEN / THEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {";"}, {":"}, {uk33})
    assert x_pidginheartcore.is_valid()

    # WHEN / THEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {None}, {None}, {None})
    assert x_pidginheartcore.is_valid()

    # WHEN / THEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {":", "/"}, {":"}, {uk33})
    assert x_pidginheartcore.is_valid() is False

    # WHEN / THEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {":"}, {":", "/"}, {uk33})
    assert x_pidginheartcore.is_valid() is False

    # WHEN / THEN
    uk44 = "unknown44"
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {":"}, {":"}, {uk33, uk44})
    assert x_pidginheartcore.is_valid() is False


def test_PidginHeartCore_get_valid_pidginheartrow_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN / THEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55)
    assert x_pidginheartcore.is_valid() is False
    assert None == x_pidginheartcore.get_valid_pidginheartrow()


def test_PidginHeartCore_get_valid_pidginheartrow_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {";"}, {":"}, {uk33})

    # THEN
    assert x_pidginheartcore.is_valid()
    assert x_pidginheartcore.get_valid_pidginheartrow()
    s55_pidginheartrow = x_pidginheartcore.get_valid_pidginheartrow()
    assert s55_pidginheartrow.face_id == sue_str
    assert s55_pidginheartrow.event_id == e55
    assert s55_pidginheartrow.otx_wall == ";"
    assert s55_pidginheartrow.inx_wall == ":"
    assert s55_pidginheartrow.unknown_word == uk33


def test_PidginHeartCore_get_valid_pidginheartrow_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {None}, {None}, {None})
    assert x_pidginheartcore.is_valid()
    assert x_pidginheartcore.get_valid_pidginheartrow()
    s55_pidginheartrow = x_pidginheartcore.get_valid_pidginheartrow()
    assert s55_pidginheartrow.face_id == sue_str
    assert s55_pidginheartrow.event_id == e55
    assert s55_pidginheartrow.otx_wall is None
    assert s55_pidginheartrow.inx_wall is None
    assert s55_pidginheartrow.unknown_word is None


def test_PidginHeartCore_get_valid_pidginheartrow_ReturnsObj_Scenario3():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {":", "/"}, {":"}, {uk33})

    # THEN
    assert x_pidginheartcore.is_valid() is False
    assert not x_pidginheartcore.get_valid_pidginheartrow()


def test_PidginHeartCore_get_valid_pidginheartrow_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {":"}, {":", "/"}, {uk33})

    # THEN
    assert x_pidginheartcore.is_valid() is False
    assert not x_pidginheartcore.get_valid_pidginheartrow()


def test_PidginHeartCore_get_valid_pidginheartrow_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    e55 = 55
    uk33 = "unknown33"

    # WHEN
    uk44 = "unknown44"
    x_pidginheartcore = pidginheartcore_shop(sue_str, e55, {":"}, {":"}, {uk33, uk44})

    # THEN
    assert x_pidginheartcore.is_valid() is False
    assert not x_pidginheartcore.get_valid_pidginheartrow()


def test_PidginHeartBook_Exists():
    # ESTABLISH / WHEN
    x_pidginheartbook = PidginHeartBook()

    # THEN
    assert x_pidginheartbook
    assert x_pidginheartbook.pidginheartcores is None


def test_eventsaggs_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginheartbook = pidginheartbook_shop()

    # THEN
    assert x_pidginheartbook
    assert x_pidginheartbook.pidginheartcores == {}


def test_PidginHeartBook_overwrite_pidginheartcore_SetsAttr_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    sue55_agg = create_pidginheartcore(sue_str, x_event_id, ";", ":", "uk33")
    x_pidginheartbook = pidginheartbook_shop()
    assert x_pidginheartbook.pidginheartcores.get((sue_str, x_event_id)) is None

    # WHEN
    x_pidginheartbook._overwrite_pidginheartcore(sue55_agg)

    # THEN
    assert x_pidginheartbook.pidginheartcores.get((sue_str, x_event_id)) != None
    assert x_pidginheartbook.pidginheartcores.get((sue_str, x_event_id)) == sue55_agg


def test_PidginHeartBook_pidginheartcore_exists_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    sue55_agg = create_pidginheartcore(sue_str, x_event_id, ";", ":", "uk33")
    x_pidginheartbook = pidginheartbook_shop()
    assert x_pidginheartbook.pidginheartcore_exists((sue_str, x_event_id)) is False

    # WHEN
    x_pidginheartbook._overwrite_pidginheartcore(sue55_agg)

    # THEN
    assert x_pidginheartbook.pidginheartcore_exists((sue_str, x_event_id))


def test_PidginHeartBook_get_pidginheartcore_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x55_event_id = 55
    sue55_agg = create_pidginheartcore(sue_str, x55_event_id, ";", ":", "uk33")
    x_pidginheartbook = pidginheartbook_shop()
    x_pidginheartbook._overwrite_pidginheartcore(sue55_agg)
    sue55_key = (sue_str, x55_event_id)
    assert x_pidginheartbook.pidginheartcore_exists(sue55_key)

    # WHEN
    gen_pidginheartcore = x_pidginheartbook.get_pidginheartcore(sue55_key)

    # THEN
    assert gen_pidginheartcore == sue55_agg


def test_PidginHeartBook_eval_pidginheartrow_SetsAttr_Scenario0_EmptyDict():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    x_otx_wall = ";"
    x_inx_wall = ";"
    x_unknown_word = "unknown33"
    sue55_pidginheartrow = PidginHeartRow(
        sue_str, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
    )
    x_pidginheartbook = pidginheartbook_shop()
    sue55_key = (sue_str, x_event_id)
    assert x_pidginheartbook.pidginheartcore_exists(sue55_key) is False

    # WHEN
    x_pidginheartbook.eval_pidginheartrow(sue55_pidginheartrow)

    # THEN
    assert x_pidginheartbook.pidginheartcore_exists(sue55_key)
    x_pidginheartcore = x_pidginheartbook.get_pidginheartcore(sue55_key)
    assert x_pidginheartcore.face_id == sue_str
    assert x_pidginheartcore.event_id == x_event_id
    assert x_otx_wall in x_pidginheartcore.otx_walls
    assert x_inx_wall in x_pidginheartcore.inx_walls
    assert x_unknown_word in x_pidginheartcore.unknown_words


def test_PidginHeartBook_eval_pidginheartrow_SetsAttr_Scenario0_EmptyDict():
    # ESTABLISH
    sue_str = "Sue"
    x_event_id = 55
    x_otx_wall = ";"
    x_inx_wall = ";"
    x_unknown_word = "unknown33"
    sue55_pidginheartrow = PidginHeartRow(
        sue_str, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
    )
    x_pidginheartbook = pidginheartbook_shop()
    sue55_key = (sue_str, x_event_id)
    assert x_pidginheartbook.pidginheartcore_exists(sue55_key) is False

    # WHEN
    x_pidginheartbook.eval_pidginheartrow(sue55_pidginheartrow)

    # THEN
    assert x_pidginheartbook.pidginheartcore_exists(sue55_key)
    x_pidginheartcore = x_pidginheartbook.get_pidginheartcore(sue55_key)
    assert x_pidginheartcore.face_id == sue_str
    assert x_pidginheartcore.event_id == x_event_id
    assert x_otx_wall in x_pidginheartcore.otx_walls
    assert x_inx_wall in x_pidginheartcore.inx_walls
    assert x_unknown_word in x_pidginheartcore.unknown_words


def test_PidginHeartBook_eval_pidginheartrow_SetsAttr_Scenario1_MultipleRowsAtSameEvent():
    # ESTABLISH
    x_pidginheartbook = pidginheartbook_shop()
    sue_str = "Sue"
    x_event_id = 55
    colon_str = ":"
    comma_str = ","
    x_unk33 = "unknown33"
    sue1_pidginheartrow = PidginHeartRow(
        sue_str, x_event_id, colon_str, comma_str, x_unk33
    )
    x_pidginheartbook.eval_pidginheartrow(sue1_pidginheartrow)
    sue55_key = (sue_str, x_event_id)
    assert x_pidginheartbook.pidginheartcore_exists(sue55_key)

    # WHEN
    slash_str = "/"
    semic_str = ";"
    x_unk44 = "unknown44"
    sue2_pidginheartrow = PidginHeartRow(
        sue_str, x_event_id, slash_str, semic_str, x_unk44
    )
    x_pidginheartbook.eval_pidginheartrow(sue2_pidginheartrow)

    # THEN
    assert x_pidginheartbook.pidginheartcore_exists(sue55_key)
    gen_pidginheartcore = x_pidginheartbook.get_pidginheartcore(sue55_key)
    assert gen_pidginheartcore.face_id == sue_str
    assert gen_pidginheartcore.event_id == x_event_id
    assert gen_pidginheartcore.otx_walls == {colon_str, slash_str}
    assert gen_pidginheartcore.inx_walls == {comma_str, semic_str}
    assert gen_pidginheartcore.unknown_words == {x_unk33, x_unk44}


def test_PidginHeartBook_eval_pidginheartrow_SetsAttr_Scenario2_NoneElementIsHandledCorrectly():
    # ESTABLISH
    x_pidginheartbook = pidginheartbook_shop()
    sue_str = "Sue"
    x_event_id = 55
    colon_str = ":"
    sue1_pidginheartrow = PidginHeartRow(sue_str, x_event_id, colon_str, None, None)
    x_pidginheartbook.eval_pidginheartrow(sue1_pidginheartrow)
    sue55_key = (sue_str, x_event_id)
    assert x_pidginheartbook.pidginheartcore_exists(sue55_key)

    # WHEN
    slash_str = "/"
    x_unk44 = "unknown44"
    sue2_pidginheartrow = PidginHeartRow(sue_str, x_event_id, slash_str, None, x_unk44)
    x_pidginheartbook.eval_pidginheartrow(sue2_pidginheartrow)

    # THEN
    assert x_pidginheartbook.pidginheartcore_exists(sue55_key)
    gen_pidginheartcore = x_pidginheartbook.get_pidginheartcore(sue55_key)
    assert gen_pidginheartcore.face_id == sue_str
    assert gen_pidginheartcore.event_id == x_event_id
    assert gen_pidginheartcore.otx_walls == {colon_str, slash_str}
    assert gen_pidginheartcore.inx_walls == {None}
    assert gen_pidginheartcore.unknown_words == {x_unk44}
