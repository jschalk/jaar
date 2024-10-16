from src.f04_gift.atom_config import label_str, road_str, group_id_str, acct_id_str
from src.f09_filter.bridge import bridgekind_shop, BridgeKind


def get_clean_roadnode_bridgekind() -> BridgeKind:
    clean_src = "clean"
    clean_dst = "prop"
    casa_src = "casa1"
    casa_dst = "casa2"
    slash_src_road_delimiter = "/"
    label_bridgekind = bridgekind_shop(None, label_str(), slash_src_road_delimiter)
    label_bridgekind.set_src_to_dst(clean_src, clean_dst)
    label_bridgekind.set_src_to_dst(casa_src, casa_dst)
    return label_bridgekind


def get_clean_roadunit_bridgekind() -> BridgeKind:
    src_music45_str = "music45"
    dst_music87_str = "music87"
    src_r_delimiter = "/"
    dst_r_delimiter = ":"
    clean_src_str = "clean"
    clean_dst_str = "prop"
    clean_src_road = f"{src_music45_str}{src_r_delimiter}{clean_src_str}"
    road_bridgekind = bridgekind_shop(
        None, road_str(), src_r_delimiter, dst_r_delimiter
    )
    road_bridgekind.set_explicit_label_map(clean_src_str, clean_dst_str)
    road_bridgekind.set_src_to_dst(src_music45_str, dst_music87_str)
    road_bridgekind.get_create_dst(clean_src_road)
    return road_bridgekind


def get_swim_groupid_bridgekind() -> BridgeKind:
    dst_r_delimiter = ":"
    src_r_delimiter = "/"
    swim_src = f"swim{src_r_delimiter}"
    climb_src = f"climb{src_r_delimiter}_{dst_r_delimiter}"
    return bridgekind_shop(None, group_id_str(), src_r_delimiter, dst_r_delimiter)


def get_suita_acctid_bridgekind() -> BridgeKind:
    xio_src = "Xio"
    sue_src = "Sue"
    bob_src = "Bob"
    zia_src = "Zia"
    xio_dst = "Xioita"
    sue_dst = "Suita"
    bob_dst = "Bobita"
    acct_id_bridgekind = bridgekind_shop(None, acct_id_str())
    acct_id_bridgekind.set_src_to_dst(xio_src, xio_dst)
    acct_id_bridgekind.set_src_to_dst(sue_src, sue_dst)
    acct_id_bridgekind.set_src_to_dst(bob_src, bob_dst)
    return acct_id_bridgekind
