from src.f01_road.road import default_road_delimiter_if_none
from src.f09_read.read import (
    BridgeUnit,
    bridgeunit_shop,
    default_unknown_word,
    get_bridgeunit_mapping,
)
from pytest import raises as pytest_raises

# from src.f09_read.examples.read_env import get_test_reads_dir, env_dir_setup_cleanup

# The goal of the read function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_default_unknown_word_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_word() == "UNKNOWN"


def test_BridgeUnit_Exists():
    # ESTABLISH
    x_bridgeunit = BridgeUnit()

    # WHEN / THEN
    assert not x_bridgeunit.word_map
    assert not x_bridgeunit.unknown_word
    assert not x_bridgeunit.src_road_delimiter
    assert not x_bridgeunit.dst_road_delimiter


def test_bridgeunit_shop_ReturnsObj_scenario0():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    word_map = {xio_str: sue_str}
    x_unknown_word = "UnknownAcctId"
    slash_src_road_delimiter = "/"
    colon_dst_road_delimiter = ":"

    # WHEN
    x_bridgeunit = bridgeunit_shop(
        x_word_map=word_map,
        x_unknown_word=x_unknown_word,
        x_src_road_delimiter=slash_src_road_delimiter,
        x_dst_road_delimiter=colon_dst_road_delimiter,
    )

    # THEN
    assert x_bridgeunit.word_map == word_map
    assert x_bridgeunit.unknown_word == x_unknown_word
    assert x_bridgeunit.src_road_delimiter == slash_src_road_delimiter
    assert x_bridgeunit.dst_road_delimiter == colon_dst_road_delimiter


def test_bridgeunit_shop_ReturnsObj_scenario1():
    # ESTABLISH

    # WHEN
    x_bridgeunit = bridgeunit_shop()

    # THEN
    assert x_bridgeunit.word_map == {}
    assert x_bridgeunit.unknown_word == default_unknown_word()
    assert x_bridgeunit.src_road_delimiter == default_road_delimiter_if_none()
    assert x_bridgeunit.dst_road_delimiter == default_road_delimiter_if_none()


def test_BridgeUnit_set_all_word_map_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_bridgeunit = bridgeunit_shop()
    x_word_map = {xio_str: sue_str, zia_str: zia_str}
    assert x_bridgeunit.word_map != x_word_map

    # WHEN
    x_bridgeunit.set_all_word_map(x_word_map)

    # THEN
    assert x_bridgeunit.word_map == x_word_map


def test_BridgeUnit_set_all_word_map_RaisesErrorIf_unknown_word_IsKeyIn_word_map():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    x_bridgeunit = bridgeunit_shop(x_unknown_word=x_unknown_word)
    x_word_map = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_bridgeunit.word_map != x_word_map

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_bridgeunit.set_all_word_map(x_word_map, raise_exception_if_invalid=True)
    exception_str = f"word_map cannot have unknown_word '{x_unknown_word}' in any str. Affected keys include ['{x_unknown_word}']."
    assert str(excinfo.value) == exception_str


def test_BridgeUnit_set_all_word_map_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    x_bridgeunit = bridgeunit_shop(x_unknown_word=x_unknown_word)
    x_word_map = {xio_str: sue_str, x_unknown_word: zia_str}
    assert x_bridgeunit.word_map != x_word_map

    # WHEN
    x_bridgeunit.set_all_word_map(x_word_map)

    # THEN
    assert x_bridgeunit.word_map == x_word_map


def test_BridgeUnit_set_word_map_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    x_bridgeunit = bridgeunit_shop(x_unknown_word=x_unknown_word)
    assert x_bridgeunit.word_map == {}

    # WHEN
    x_bridgeunit.set_word_map(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.word_map == {xio_str: sue_str}


def test_BridgeUnit_get_word_map_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    x_bridgeunit = bridgeunit_shop(x_unknown_word=x_unknown_word)
    assert x_bridgeunit.get_word_map(xio_str) != sue_str

    # WHEN
    x_bridgeunit.set_word_map(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.get_word_map(xio_str) == sue_str


def test_BridgeUnit_word_map_exists_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    bob_str = "Bob"
    x_unknown_word = "UnknownAcctId"
    x_bridgeunit = bridgeunit_shop(x_unknown_word=x_unknown_word)
    assert x_bridgeunit.word_map_exists(xio_str, sue_str) is False
    assert x_bridgeunit.word_map_exists(xio_str, bob_str) is False

    # WHEN
    x_bridgeunit.set_word_map(xio_str, sue_str)

    # THEN
    assert x_bridgeunit.word_map_exists(xio_str, sue_str)
    assert x_bridgeunit.word_map_exists(xio_str, bob_str) is False


def test_BridgeUnit_del_word_map_SetsAttr():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    x_bridgeunit = bridgeunit_shop(x_unknown_word=x_unknown_word)
    x_bridgeunit.set_word_map(xio_str, sue_str)
    assert x_bridgeunit.word_map_exists(xio_str, sue_str)

    # WHEN
    x_bridgeunit.del_word_map(xio_str)

    # THEN
    assert x_bridgeunit.word_map_exists(xio_str, sue_str) is False


def test_BridgeUnit_unknown_word_in_word_map_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    zia_str = "Zia"
    x_unknown_word = "UnknownAcctId"
    x_bridgeunit = bridgeunit_shop(x_unknown_word=x_unknown_word)
    x_bridgeunit.set_word_map(xio_str, sue_str)
    assert x_bridgeunit._unknown_word_in_word_map() is False

    # WHEN
    x_bridgeunit.set_word_map(zia_str, x_unknown_word)

    # THEN
    assert x_bridgeunit._unknown_word_in_word_map()


def test_BridgeUnit_src_road_delimiter_in_src_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    src_road_delimiter = "/"
    zia_dst = "Zia"
    zia_src = f"Zia{src_road_delimiter}"
    x_bridgeunit = bridgeunit_shop(x_src_road_delimiter=src_road_delimiter)
    x_bridgeunit.set_word_map(xio_str, sue_str)
    assert x_bridgeunit._src_road_delimiter_in_src_words() is False

    # WHEN
    x_bridgeunit.set_word_map(zia_src, zia_dst)

    # THEN
    assert x_bridgeunit._src_road_delimiter_in_src_words()


def test_BridgeUnit_dst_road_delimiter_in_src_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    dst_road_delimiter = "/"
    zia_dst = "Zia"
    zia_src = f"Zia{dst_road_delimiter}"
    x_bridgeunit = bridgeunit_shop(x_dst_road_delimiter=dst_road_delimiter)
    x_bridgeunit.set_word_map(xio_str, sue_str)
    assert x_bridgeunit._dst_road_delimiter_in_src_words() is False

    # WHEN
    x_bridgeunit.set_word_map(zia_src, zia_dst)

    # THEN
    assert x_bridgeunit._dst_road_delimiter_in_src_words()


def test_BridgeUnit_src_road_delimiter_in_dst_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    src_road_delimiter = "/"
    zia_src = "Zia"
    zia_dst = f"Zia{src_road_delimiter}"
    x_bridgeunit = bridgeunit_shop(x_src_road_delimiter=src_road_delimiter)
    x_bridgeunit.set_word_map(xio_str, sue_str)
    assert x_bridgeunit._src_road_delimiter_in_dst_words() is False

    # WHEN
    x_bridgeunit.set_word_map(zia_src, zia_dst)

    # THEN
    assert x_bridgeunit._src_road_delimiter_in_dst_words()


def test_BridgeUnit_dst_road_delimiter_in_dst_words_ReturnsObj():
    # ESTABLISH
    xio_str = "Xio"
    sue_str = "Sue"
    dst_road_delimiter = "/"
    zia_src = "Zia"
    zia_dst = f"Zia{dst_road_delimiter}"
    x_bridgeunit = bridgeunit_shop(x_dst_road_delimiter=dst_road_delimiter)
    x_bridgeunit.set_word_map(xio_str, sue_str)
    assert x_bridgeunit._dst_road_delimiter_in_dst_words() is False

    # WHEN
    x_bridgeunit.set_word_map(zia_src, zia_dst)

    # THEN
    assert x_bridgeunit._dst_road_delimiter_in_dst_words()


# def test_get_bridgeunit_mapping_ReturnsObj():
#     # ESTABLISH
#     xio_str = "Xio"
#     sue_str = "Sue"
#     bob_str = "Bob"
#     word_map = {xio_str: sue_str, bob_str: bob_str}
#     x_unknown_word = "UnknownAcctId"
#     x_bridgeunit = bridgeunit_shop(word_map, x_unknown_word)
#     assert x_bridgeunit.word_map == word_map
#     assert x_bridgeunit.unknown_word == x_unknown_word

#     # WHEN / THEN
#     assert get_bridgeunit_mapping(x_bridgeunit, None) == None
#     assert get_bridgeunit_mapping(x_bridgeunit, bob_str) == bob_str
#     assert get_bridgeunit_mapping(x_bridgeunit, xio_str) == sue_str
#     assert get_bridgeunit_mapping(x_bridgeunit, sue_str) == x_unknown_word
