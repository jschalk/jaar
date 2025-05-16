from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_name_str,
    pidgin_label_str,
    pidgin_word_str,
    pidgin_way_str,
)
from src.a16_pidgin_logic.pidgin_config import get_pidgin_config_args
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns


def test_PidginPrimeColumns_Exists():
    # ESTABLISH / WHEN
    x_pidginprimecols = PidginPrimeColumns()

    # THEN
    pidgin_name_agg_args = set(get_pidgin_config_args((pidgin_name_str())).keys())
    pidgin_label_agg_args = set(get_pidgin_config_args((pidgin_label_str())).keys())
    pidgin_word_agg_args = set(get_pidgin_config_args((pidgin_word_str())).keys())
    pidgin_way_agg_args = set(get_pidgin_config_args((pidgin_way_str())).keys())
    event_args = {face_name_str(), event_int_str()}
    pidgin_name_agg_args = pidgin_name_agg_args.union(event_args)
    pidgin_label_agg_args = pidgin_label_agg_args.union(event_args)
    pidgin_word_agg_args = pidgin_word_agg_args.union(event_args)
    pidgin_way_agg_args = pidgin_way_agg_args.union(event_args)
    raw_args = {"creed_number"}
    pidgin_name_raw_args = pidgin_name_agg_args.union(raw_args)
    pidgin_label_raw_args = pidgin_label_agg_args.union(raw_args)
    pidgin_word_raw_args = pidgin_word_agg_args.union(raw_args)
    pidgin_way_raw_args = pidgin_way_agg_args.union(raw_args)
    assert set(x_pidginprimecols.pidgin_name_agg_columns) == pidgin_name_agg_args
    assert set(x_pidginprimecols.pidgin_label_agg_columns) == pidgin_label_agg_args
    assert set(x_pidginprimecols.pidgin_word_agg_columns) == pidgin_word_agg_args
    assert set(x_pidginprimecols.pidgin_way_agg_columns) == pidgin_way_agg_args

    assert set(x_pidginprimecols.pidgin_name_raw_columns) == pidgin_name_raw_args
    assert set(x_pidginprimecols.pidgin_label_raw_columns) == pidgin_label_raw_args
    assert set(x_pidginprimecols.pidgin_word_raw_columns) == pidgin_word_raw_args
    assert set(x_pidginprimecols.pidgin_way_raw_columns) == pidgin_way_raw_args
