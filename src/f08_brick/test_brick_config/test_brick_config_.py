from src.f04_gift.atom_config import get_atom_config_dict
from src.f08_brick.brick_config import (
    config_file_dir,
    get_brick_config_file_name,
    get_brick_config_dict,
)
from os import getcwd as os_getcwd


def test_get_brick_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_brick_config_file_name() == "brick_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    assert config_file_dir() == f"{os_getcwd()}/src/f08_brick"


def test_get_brick_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    x_brick_config = get_brick_config_dict()

    # THEN
    assert x_brick_config
    brick_config_categorys = set(x_brick_config.keys())
    assert "fiscalunit" in brick_config_categorys
    assert "fiscal_purviewlog" in brick_config_categorys
    assert "fiscal_purview_episode" in brick_config_categorys
    assert "fiscal_cashbook" in brick_config_categorys
    assert "fiscal_timeline_hour" in brick_config_categorys
    assert "fiscal_timeline_month" in brick_config_categorys
    assert "fiscal_timeline_weekday" in brick_config_categorys
    assert "bud_acct_membership" in brick_config_categorys
    assert "bud_acctunit" in brick_config_categorys
    assert "bud_item_awardlink" in brick_config_categorys
    assert "bud_item_factunit" in brick_config_categorys
    assert "bud_item_teamlink" in brick_config_categorys
    assert "bud_item_healerlink" in brick_config_categorys
    assert "bud_item_reason_premiseunit" in brick_config_categorys
    assert "bud_item_reasonunit" in brick_config_categorys
    assert "bud_itemunit" in brick_config_categorys
    assert "budunit" in brick_config_categorys
    atom_config_categorys = set(get_atom_config_dict().keys())
    assert atom_config_categorys.issubset(brick_config_categorys)
    assert len(x_brick_config) == 17


# def get_atom_config_dict() -> dict:
#     return get_dict_from_json(open_file(config_file_dir(), get_atom_config_file_name()))
