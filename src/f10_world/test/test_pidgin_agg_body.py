# from src.f10_world.pidgin_agg import (
#     PidginBodyCore,
#     PidginBodyBook,
#     pidginBodybook_shop,
#     pidginBodycore_shop,
#     create_pidginBodycore,
#     PidginBodyRow,
# )


# def test_PidginBodyRow_Exists():
#     # ESTABLISH
#     sue_str = "Sue"
#     x_event_id = 55
#     x_otx_wall = ";"
#     x_inx_wall = ";"
#     x_unknown_word = "unknown33"

#     # WHEN
#     sue55_pidginBodyrow = PidginBodyRow(
#         sue_str, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
#     )

#     # THEN
#     assert sue55_pidginBodyrow
#     assert sue55_pidginBodyrow.face_id == sue_str
#     assert sue55_pidginBodyrow.event_id == x_event_id
#     assert sue55_pidginBodyrow.otx_wall == x_otx_wall
#     assert sue55_pidginBodyrow.inx_wall == x_inx_wall
#     assert sue55_pidginBodyrow.unknown_word == x_unknown_word


# def test_PidginBodyCore_Exists():
#     # ESTABLISH
#     x_pidginBodycore = PidginBodyCore()

#     # THEN
#     assert x_pidginBodycore
#     assert x_pidginBodycore.face_id is None
#     assert x_pidginBodycore.event_id is None
#     assert x_pidginBodycore.otx_walls is None
#     assert x_pidginBodycore.inx_walls is None
#     assert x_pidginBodycore.unknown_words is None


# def test_pidginBodycore_shop_ReturnsObj_WithNoValues():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55

#     # WHEN
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)

#     # THEN
#     assert x_pidginBodycore
#     assert x_pidginBodycore.face_id == x_face_id
#     assert x_pidginBodycore.event_id == x_event_id
#     assert x_pidginBodycore.otx_walls == set()
#     assert x_pidginBodycore.inx_walls == set()
#     assert x_pidginBodycore.unknown_words == set()


# def test_pidginBodycore_shop_ReturnsObj_WithCoreValues():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_otx_wall_set = {";"}
#     x_inx_wall_set = {";"}
#     x_unknown_word_set = {"unknown33"}

#     # WHEN
#     x_pidginBodycore = pidginBodycore_shop(
#         x_face_id,
#         x_event_id,
#         x_otx_wall_set,
#         x_inx_wall_set,
#         x_unknown_word_set,
#     )

#     # THEN
#     assert x_pidginBodycore
#     assert x_pidginBodycore.face_id == x_face_id
#     assert x_pidginBodycore.event_id == x_event_id
#     assert x_pidginBodycore.otx_walls == x_otx_wall_set
#     assert x_pidginBodycore.inx_walls == x_inx_wall_set
#     assert ";" in x_pidginBodycore.inx_walls
#     assert x_pidginBodycore.unknown_words == x_unknown_word_set


# def test_PidginBodyCore_add_otx_wall_ChangesAttr_Scenario0_AddToEmptySet():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)
#     colon_str = ":"
#     print(f"{x_pidginBodycore.otx_walls=}")
#     print(f"{colon_str=}")
#     assert colon_str not in x_pidginBodycore.otx_walls
#     assert colon_str not in x_pidginBodycore.inx_walls
#     assert colon_str not in x_pidginBodycore.unknown_words

#     # WHEN
#     x_pidginBodycore.add_otx_wall(colon_str)

#     # THEN
#     assert colon_str in x_pidginBodycore.otx_walls
#     assert colon_str not in x_pidginBodycore.inx_walls
#     assert colon_str not in x_pidginBodycore.unknown_words


# def test_PidginBodyCore_add_otx_wall_ChangesAttr_Scenario1_AddNoneToEmptySet():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)
#     assert None not in x_pidginBodycore.otx_walls
#     assert None not in x_pidginBodycore.inx_walls
#     assert None not in x_pidginBodycore.unknown_words

#     # WHEN
#     x_pidginBodycore.add_otx_wall(None)

#     # THEN
#     assert None in x_pidginBodycore.otx_walls
#     assert None not in x_pidginBodycore.inx_walls
#     assert None not in x_pidginBodycore.unknown_words


# def test_PidginBodyCore_add_otx_wall_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)
#     x_pidginBodycore.add_otx_wall(None)
#     assert None in x_pidginBodycore.otx_walls

#     # WHEN / THEN
#     x_pidginBodycore.add_otx_wall(None)
#     assert None in x_pidginBodycore.otx_walls

#     # WHEN / THEN
#     colon_str = ":"
#     x_pidginBodycore.add_otx_wall(colon_str)
#     assert colon_str in x_pidginBodycore.otx_walls
#     assert None not in x_pidginBodycore.otx_walls

#     # WHEN / THEN
#     x_pidginBodycore.add_otx_wall(None)
#     assert colon_str in x_pidginBodycore.otx_walls
#     assert None not in x_pidginBodycore.otx_walls


# def test_PidginBodyCore_add_inx_wall_ChangesAttr_Scenario0_AddToEmptySet():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)
#     colon_str = ":"
#     assert colon_str not in x_pidginBodycore.otx_walls
#     assert colon_str not in x_pidginBodycore.inx_walls
#     assert colon_str not in x_pidginBodycore.unknown_words

#     # WHEN
#     x_pidginBodycore.add_inx_wall(colon_str)

#     # THEN
#     assert colon_str not in x_pidginBodycore.otx_walls
#     assert colon_str in x_pidginBodycore.inx_walls
#     assert colon_str not in x_pidginBodycore.unknown_words


# def test_PidginBodyCore_add_inx_wall_ChangesAttr_Scenario1_AddNoneToEmptySet():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)
#     assert None not in x_pidginBodycore.otx_walls
#     assert None not in x_pidginBodycore.inx_walls
#     assert None not in x_pidginBodycore.unknown_words

#     # WHEN
#     x_pidginBodycore.add_inx_wall(None)

#     # THEN
#     assert None not in x_pidginBodycore.otx_walls
#     assert None in x_pidginBodycore.inx_walls
#     assert None not in x_pidginBodycore.unknown_words


# def test_PidginBodyCore_add_inx_wall_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)
#     x_pidginBodycore.add_inx_wall(None)
#     assert None in x_pidginBodycore.inx_walls

#     # WHEN / THEN
#     x_pidginBodycore.add_inx_wall(None)
#     assert None in x_pidginBodycore.inx_walls

#     # WHEN / THEN
#     colon_str = ":"
#     x_pidginBodycore.add_inx_wall(colon_str)
#     assert colon_str in x_pidginBodycore.inx_walls
#     assert None not in x_pidginBodycore.inx_walls

#     # WHEN / THEN
#     x_pidginBodycore.add_inx_wall(None)
#     assert colon_str in x_pidginBodycore.inx_walls
#     assert None not in x_pidginBodycore.inx_walls


# def test_PidginBodyCore_add_unknown_word_ChangesAttr_Scenario0_AddToEmptySet():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)
#     colon_str = ":"
#     assert colon_str not in x_pidginBodycore.otx_walls
#     assert colon_str not in x_pidginBodycore.inx_walls
#     assert colon_str not in x_pidginBodycore.unknown_words

#     # WHEN
#     x_pidginBodycore.add_unknown_word(colon_str)

#     # THEN
#     assert colon_str not in x_pidginBodycore.otx_walls
#     assert colon_str not in x_pidginBodycore.inx_walls
#     assert colon_str in x_pidginBodycore.unknown_words


# def test_PidginBodyCore_add_unknown_word_ChangesAttr_Scenario1_AddNoneToEmptySet():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)
#     assert None not in x_pidginBodycore.otx_walls
#     assert None not in x_pidginBodycore.inx_walls
#     assert None not in x_pidginBodycore.unknown_words

#     # WHEN
#     x_pidginBodycore.add_unknown_word(None)

#     # THEN
#     assert None not in x_pidginBodycore.otx_walls
#     assert None not in x_pidginBodycore.inx_walls
#     assert None in x_pidginBodycore.unknown_words


# def test_PidginBodyCore_add_unknown_word_ChangesAttr_Scenario2_SetWithNoneChangesWhenNonNoneElementAdded():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_pidginBodycore = pidginBodycore_shop(x_face_id, x_event_id)
#     x_pidginBodycore.add_unknown_word(None)
#     assert None in x_pidginBodycore.unknown_words

#     # WHEN / THEN
#     x_pidginBodycore.add_unknown_word(None)
#     assert None in x_pidginBodycore.unknown_words

#     # WHEN / THEN
#     colon_str = ":"
#     x_pidginBodycore.add_unknown_word(colon_str)
#     assert colon_str in x_pidginBodycore.unknown_words
#     assert None not in x_pidginBodycore.unknown_words

#     # WHEN / THEN
#     x_pidginBodycore.add_unknown_word(None)
#     assert colon_str in x_pidginBodycore.unknown_words
#     assert None not in x_pidginBodycore.unknown_words


# def test_create_pidginBodycore_ReturnsObj():
#     # ESTABLISH
#     x_face_id = "Sue"
#     x_event_id = 55
#     x_otx_wall = ";"
#     x_inx_wall = ";"
#     x_unknown_word = "unknown33"

#     # WHEN
#     x_pidginBodycore = create_pidginBodycore(
#         x_face_id, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
#     )

#     # THEN
#     x_face_id = x_face_id
#     x_event_id = x_event_id
#     x_otx_wall_set = {x_otx_wall}
#     x_inx_wall_set = {x_inx_wall}
#     x_unknown_word_set = {x_unknown_word}
#     assert x_pidginBodycore
#     assert x_pidginBodycore.face_id == x_face_id
#     assert x_pidginBodycore.event_id == x_event_id
#     assert x_pidginBodycore.otx_walls == x_otx_wall_set
#     assert x_pidginBodycore.inx_walls == x_inx_wall_set
#     assert x_pidginBodycore.unknown_words == x_unknown_word_set


# def test_PidginBodyCore_is_valid_ReturnsObj():
#     # ESTABLISH
#     sue_str = "Sue"
#     e55 = 55
#     uk33 = "unknown33"

#     # WHEN / THEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55)
#     assert x_pidginBodycore.is_valid() is False

#     # WHEN / THEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {";"}, {":"}, {uk33})
#     assert x_pidginBodycore.is_valid()

#     # WHEN / THEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {None}, {None}, {None})
#     assert x_pidginBodycore.is_valid()

#     # WHEN / THEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {":", "/"}, {":"}, {uk33})
#     assert x_pidginBodycore.is_valid() is False

#     # WHEN / THEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {":"}, {":", "/"}, {uk33})
#     assert x_pidginBodycore.is_valid() is False

#     # WHEN / THEN
#     uk44 = "unknown44"
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {":"}, {":"}, {uk33, uk44})
#     assert x_pidginBodycore.is_valid() is False


# def test_PidginBodyCore_get_valid_pidginBodyrow_ReturnsObj_Scenario0():
#     # ESTABLISH
#     sue_str = "Sue"
#     e55 = 55
#     uk33 = "unknown33"

#     # WHEN / THEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55)
#     assert x_pidginBodycore.is_valid() is False
#     assert None == x_pidginBodycore.get_valid_pidginBodyrow()


# def test_PidginBodyCore_get_valid_pidginBodyrow_ReturnsObj_Scenario1():
#     # ESTABLISH
#     sue_str = "Sue"
#     e55 = 55
#     uk33 = "unknown33"

#     # WHEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {";"}, {":"}, {uk33})

#     # THEN
#     assert x_pidginBodycore.is_valid()
#     assert x_pidginBodycore.get_valid_pidginBodyrow()
#     s55_pidginBodyrow = x_pidginBodycore.get_valid_pidginBodyrow()
#     assert s55_pidginBodyrow.face_id == sue_str
#     assert s55_pidginBodyrow.event_id == e55
#     assert s55_pidginBodyrow.otx_wall == ";"
#     assert s55_pidginBodyrow.inx_wall == ":"
#     assert s55_pidginBodyrow.unknown_word == uk33


# def test_PidginBodyCore_get_valid_pidginBodyrow_ReturnsObj_Scenario2():
#     # ESTABLISH
#     sue_str = "Sue"
#     e55 = 55
#     uk33 = "unknown33"

#     # WHEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {None}, {None}, {None})
#     assert x_pidginBodycore.is_valid()
#     assert x_pidginBodycore.get_valid_pidginBodyrow()
#     s55_pidginBodyrow = x_pidginBodycore.get_valid_pidginBodyrow()
#     assert s55_pidginBodyrow.face_id == sue_str
#     assert s55_pidginBodyrow.event_id == e55
#     assert s55_pidginBodyrow.otx_wall is None
#     assert s55_pidginBodyrow.inx_wall is None
#     assert s55_pidginBodyrow.unknown_word is None


# def test_PidginBodyCore_get_valid_pidginBodyrow_ReturnsObj_Scenario3():
#     # ESTABLISH
#     sue_str = "Sue"
#     e55 = 55
#     uk33 = "unknown33"

#     # WHEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {":", "/"}, {":"}, {uk33})

#     # THEN
#     assert x_pidginBodycore.is_valid() is False
#     assert not x_pidginBodycore.get_valid_pidginBodyrow()


# def test_PidginBodyCore_get_valid_pidginBodyrow_ReturnsObj_Scenario1():
#     # ESTABLISH
#     sue_str = "Sue"
#     e55 = 55
#     uk33 = "unknown33"

#     # WHEN
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {":"}, {":", "/"}, {uk33})

#     # THEN
#     assert x_pidginBodycore.is_valid() is False
#     assert not x_pidginBodycore.get_valid_pidginBodyrow()


# def test_PidginBodyCore_get_valid_pidginBodyrow_ReturnsObj_Scenario1():
#     # ESTABLISH
#     sue_str = "Sue"
#     e55 = 55
#     uk33 = "unknown33"

#     # WHEN
#     uk44 = "unknown44"
#     x_pidginBodycore = pidginBodycore_shop(sue_str, e55, {":"}, {":"}, {uk33, uk44})

#     # THEN
#     assert x_pidginBodycore.is_valid() is False
#     assert not x_pidginBodycore.get_valid_pidginBodyrow()


# def test_PidginBodyBook_Exists():
#     # ESTABLISH / WHEN
#     x_pidginBodybook = PidginBodyBook()

#     # THEN
#     assert x_pidginBodybook
#     assert x_pidginBodybook.pidginBodycores is None


# def test_eventsaggs_shop_ReturnsObj():
#     # ESTABLISH / WHEN
#     x_pidginBodybook = pidginBodybook_shop()

#     # THEN
#     assert x_pidginBodybook
#     assert x_pidginBodybook.pidginBodycores == {}


# def test_PidginBodyBook_overwrite_pidginBodycore_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_str = "Sue"
#     x_event_id = 55
#     sue55_agg = create_pidginBodycore(sue_str, x_event_id, ";", ":", "uk33")
#     x_pidginBodybook = pidginBodybook_shop()
#     assert x_pidginBodybook.pidginBodycores.get((sue_str, x_event_id)) is None

#     # WHEN
#     x_pidginBodybook._overwrite_pidginBodycore(sue55_agg)

#     # THEN
#     assert x_pidginBodybook.pidginBodycores.get((sue_str, x_event_id)) != None
#     assert x_pidginBodybook.pidginBodycores.get((sue_str, x_event_id)) == sue55_agg


# def test_PidginBodyBook_pidginBodycore_exists_ReturnsObj():
#     # ESTABLISH
#     sue_str = "Sue"
#     x_event_id = 55
#     sue55_agg = create_pidginBodycore(sue_str, x_event_id, ";", ":", "uk33")
#     x_pidginBodybook = pidginBodybook_shop()
#     assert x_pidginBodybook.pidginBodycore_exists((sue_str, x_event_id)) is False

#     # WHEN
#     x_pidginBodybook._overwrite_pidginBodycore(sue55_agg)

#     # THEN
#     assert x_pidginBodybook.pidginBodycore_exists((sue_str, x_event_id))


# def test_PidginBodyBook_get_pidginBodycore_ReturnsObj():
#     # ESTABLISH
#     sue_str = "Sue"
#     x55_event_id = 55
#     sue55_agg = create_pidginBodycore(sue_str, x55_event_id, ";", ":", "uk33")
#     x_pidginBodybook = pidginBodybook_shop()
#     x_pidginBodybook._overwrite_pidginBodycore(sue55_agg)
#     sue55_key = (sue_str, x55_event_id)
#     assert x_pidginBodybook.pidginBodycore_exists(sue55_key)

#     # WHEN
#     gen_pidginBodycore = x_pidginBodybook.get_pidginBodycore(sue55_key)

#     # THEN
#     assert gen_pidginBodycore == sue55_agg


# def test_PidginBodyBook_eval_pidginBodyrow_SetsAttr_Scenario0_EmptyDict():
#     # ESTABLISH
#     sue_str = "Sue"
#     x_event_id = 55
#     x_otx_wall = ";"
#     x_inx_wall = ";"
#     x_unknown_word = "unknown33"
#     sue55_pidginBodyrow = PidginBodyRow(
#         sue_str, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
#     )
#     x_pidginBodybook = pidginBodybook_shop()
#     sue55_key = (sue_str, x_event_id)
#     assert x_pidginBodybook.pidginBodycore_exists(sue55_key) is False

#     # WHEN
#     x_pidginBodybook.eval_pidginBodyrow(sue55_pidginBodyrow)

#     # THEN
#     assert x_pidginBodybook.pidginBodycore_exists(sue55_key)
#     x_pidginBodycore = x_pidginBodybook.get_pidginBodycore(sue55_key)
#     assert x_pidginBodycore.face_id == sue_str
#     assert x_pidginBodycore.event_id == x_event_id
#     assert x_otx_wall in x_pidginBodycore.otx_walls
#     assert x_inx_wall in x_pidginBodycore.inx_walls
#     assert x_unknown_word in x_pidginBodycore.unknown_words


# def test_PidginBodyBook_eval_pidginBodyrow_SetsAttr_Scenario0_EmptyDict():
#     # ESTABLISH
#     sue_str = "Sue"
#     x_event_id = 55
#     x_otx_wall = ";"
#     x_inx_wall = ";"
#     x_unknown_word = "unknown33"
#     sue55_pidginBodyrow = PidginBodyRow(
#         sue_str, x_event_id, x_otx_wall, x_inx_wall, x_unknown_word
#     )
#     x_pidginBodybook = pidginBodybook_shop()
#     sue55_key = (sue_str, x_event_id)
#     assert x_pidginBodybook.pidginBodycore_exists(sue55_key) is False

#     # WHEN
#     x_pidginBodybook.eval_pidginBodyrow(sue55_pidginBodyrow)

#     # THEN
#     assert x_pidginBodybook.pidginBodycore_exists(sue55_key)
#     x_pidginBodycore = x_pidginBodybook.get_pidginBodycore(sue55_key)
#     assert x_pidginBodycore.face_id == sue_str
#     assert x_pidginBodycore.event_id == x_event_id
#     assert x_otx_wall in x_pidginBodycore.otx_walls
#     assert x_inx_wall in x_pidginBodycore.inx_walls
#     assert x_unknown_word in x_pidginBodycore.unknown_words


# def test_PidginBodyBook_eval_pidginBodyrow_SetsAttr_Scenario1_MultipleRowsAtSameEvent():
#     # ESTABLISH
#     x_pidginBodybook = pidginBodybook_shop()
#     sue_str = "Sue"
#     x_event_id = 55
#     colon_str = ":"
#     comma_str = ","
#     x_unk33 = "unknown33"
#     sue1_pidginBodyrow = PidginBodyRow(
#         sue_str, x_event_id, colon_str, comma_str, x_unk33
#     )
#     x_pidginBodybook.eval_pidginBodyrow(sue1_pidginBodyrow)
#     sue55_key = (sue_str, x_event_id)
#     assert x_pidginBodybook.pidginBodycore_exists(sue55_key)

#     # WHEN
#     slash_str = "/"
#     semic_str = ";"
#     x_unk44 = "unknown44"
#     sue2_pidginBodyrow = PidginBodyRow(
#         sue_str, x_event_id, slash_str, semic_str, x_unk44
#     )
#     x_pidginBodybook.eval_pidginBodyrow(sue2_pidginBodyrow)

#     # THEN
#     assert x_pidginBodybook.pidginBodycore_exists(sue55_key)
#     gen_pidginBodycore = x_pidginBodybook.get_pidginBodycore(sue55_key)
#     assert gen_pidginBodycore.face_id == sue_str
#     assert gen_pidginBodycore.event_id == x_event_id
#     assert gen_pidginBodycore.otx_walls == {colon_str, slash_str}
#     assert gen_pidginBodycore.inx_walls == {comma_str, semic_str}
#     assert gen_pidginBodycore.unknown_words == {x_unk33, x_unk44}


# def test_PidginBodyBook_eval_pidginBodyrow_SetsAttr_Scenario2_NoneElementIsHandledCorrectly():
#     # ESTABLISH
#     x_pidginBodybook = pidginBodybook_shop()
#     sue_str = "Sue"
#     x_event_id = 55
#     colon_str = ":"
#     sue1_pidginBodyrow = PidginBodyRow(sue_str, x_event_id, colon_str, None, None)
#     x_pidginBodybook.eval_pidginBodyrow(sue1_pidginBodyrow)
#     sue55_key = (sue_str, x_event_id)
#     assert x_pidginBodybook.pidginBodycore_exists(sue55_key)

#     # WHEN
#     slash_str = "/"
#     x_unk44 = "unknown44"
#     sue2_pidginBodyrow = PidginBodyRow(sue_str, x_event_id, slash_str, None, x_unk44)
#     x_pidginBodybook.eval_pidginBodyrow(sue2_pidginBodyrow)

#     # THEN
#     assert x_pidginBodybook.pidginBodycore_exists(sue55_key)
#     gen_pidginBodycore = x_pidginBodybook.get_pidginBodycore(sue55_key)
#     assert gen_pidginBodycore.face_id == sue_str
#     assert gen_pidginBodycore.event_id == x_event_id
#     assert gen_pidginBodycore.otx_walls == {colon_str, slash_str}
#     assert gen_pidginBodycore.inx_walls == {None}
#     assert gen_pidginBodycore.unknown_words == {x_unk44}
