from src.f04_kick.atom_config import face_name_str, event_int_str
from src.f09_pidgin.pidgin_config import (
    get_pidgin_config_args,
    map_name_str,
    map_label_str,
    map_title_str,
    map_road_str,
)
from src.f11_etl.pidgin_agg import PidginPrimeColumns


def test_PidginPrimeColumns_Exists():
    # ESTABLISH / WHEN
    x_pidginprimecols = PidginPrimeColumns()

    # THEN
    pidgin_name_agg_args = set(get_pidgin_config_args((map_name_str())).keys())
    pidgin_label_agg_args = set(get_pidgin_config_args((map_label_str())).keys())
    pidgin_title_agg_args = set(get_pidgin_config_args((map_title_str())).keys())
    pidgin_road_agg_args = set(get_pidgin_config_args((map_road_str())).keys())
    event_args = {face_name_str(), event_int_str()}
    pidgin_name_agg_args = pidgin_name_agg_args.union(event_args)
    pidgin_label_agg_args = pidgin_label_agg_args.union(event_args)
    pidgin_title_agg_args = pidgin_title_agg_args.union(event_args)
    pidgin_road_agg_args = pidgin_road_agg_args.union(event_args)
    staging_args = {"src_idea"}
    pidgin_name_staging_args = pidgin_name_agg_args.union(staging_args)
    pidgin_label_staging_args = pidgin_label_agg_args.union(staging_args)
    pidgin_title_staging_args = pidgin_title_agg_args.union(staging_args)
    pidgin_road_staging_args = pidgin_road_agg_args.union(staging_args)
    assert set(x_pidginprimecols.map_name_agg_columns) == pidgin_name_agg_args
    assert set(x_pidginprimecols.map_label_agg_columns) == pidgin_label_agg_args
    assert set(x_pidginprimecols.map_title_agg_columns) == pidgin_title_agg_args
    assert set(x_pidginprimecols.map_road_agg_columns) == pidgin_road_agg_args

    assert set(x_pidginprimecols.map_name_staging_columns) == pidgin_name_staging_args
    assert set(x_pidginprimecols.map_label_staging_columns) == pidgin_label_staging_args
    assert set(x_pidginprimecols.map_title_staging_columns) == pidgin_title_staging_args
    assert set(x_pidginprimecols.map_road_staging_columns) == pidgin_road_staging_args
