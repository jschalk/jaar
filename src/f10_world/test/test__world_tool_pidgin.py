from src.f04_gift.atom_config import face_id_str
from src.f08_pidgin.pidgin_config import (
    event_id_str,
    inx_wall_str,
    otx_wall_str,
    unknown_word_str,
    inx_label_str,
    otx_label_str,
)
from src.f10_world.world_tool import get_pidgin_core_report_df
from pandas import DataFrame


def test_WorldUnit_get_pidgin_core_report_df_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    rd2 = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    # THEN
    nub_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_label_str(),
        inx_label_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    b3 = "br00114"
    b4 = "br00041"
    e1_nub3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rd2, ukx]
    e1_nub4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rd2, ukx]
    e1_nub5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    e1_nub0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
    e1_nub1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]
    e1_nub_rows = [e1_nub3, e1_nub4, e1_nub5, e1_nub0, e1_nub1]
    e1_nub_df = DataFrame(e1_nub_rows, columns=nub_file_columns)
    print(f" {e1_nub_df.to_csv()=}")

    # WHEN
    pidgin_core_report = get_pidgin_core_report_df(e1_nub_df)

    # THEN
    pidgin_core_columns = [
        face_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    print(f"{list(pidgin_core_report.columns)}")
    assert list(pidgin_core_report.columns) == pidgin_core_columns
    assert len(pidgin_core_report) == 2
    e1_core_sue = [sue_str, [rdx, None], [rd2, None], [ukx, None]]
    e1_core_yao = [yao_str, [rdx], [rdx], [ukx]]
    e1_core_rows = [e1_core_sue, e1_core_yao]
    e1_core_df = DataFrame(e1_core_rows, columns=pidgin_core_columns)
    assert pidgin_core_report.to_csv(index=False) == e1_core_df.to_csv(index=False)
