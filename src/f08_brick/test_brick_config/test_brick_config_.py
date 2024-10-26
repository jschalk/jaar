from src.f02_bud.bud_tool import (
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_item_awardlink_str,
    bud_item_factunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_reason_premiseunit_str,
    bud_item_reasonunit_str,
    bud_itemunit_str,
    budunit_str,
)
from src.f04_gift.atom_config import get_atom_config_dict
from src.f07_fiscal.fiscal_config import get_fiscal_config_dict
from src.f08_brick.brick_config import (
    brick_number_str,
    get_brickref_dict,
    config_file_dir,
    get_brick_config_file_name,
    get_brick_config_dict,
    get_brick_filenames,
    get_brick_numbers,
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
    assert bud_acct_membership_str() in brick_config_categorys
    assert bud_acctunit_str() in brick_config_categorys
    assert bud_item_awardlink_str() in brick_config_categorys
    assert bud_item_factunit_str() in brick_config_categorys
    assert bud_item_teamlink_str() in brick_config_categorys
    assert bud_item_healerlink_str() in brick_config_categorys
    assert bud_item_reason_premiseunit_str() in brick_config_categorys
    assert bud_item_reasonunit_str() in brick_config_categorys
    assert bud_itemunit_str() in brick_config_categorys
    assert budunit_str() in brick_config_categorys
    atom_config_categorys = set(get_atom_config_dict().keys())
    assert atom_config_categorys.issubset(brick_config_categorys)
    fiscal_config_categorys = set(get_fiscal_config_dict().keys())
    assert fiscal_config_categorys.issubset(brick_config_categorys)
    assert len(x_brick_config) == 17


def _validate_brick_files(brick_filenames: set[str]):
    # for every brick_format file there exists a unique brick_number always with leading zeros to make 5 digits
    brick_numbers_set = set()
    for brick_filename in brick_filenames:
        brickref_dict = get_brickref_dict(brick_filename)
        print(f"{brick_filename=} {brickref_dict.get(brick_number_str())=}")
        brick_number_value = brickref_dict.get(brick_number_str())
        assert brick_number_value
        assert brick_number_value[2:8] == brick_filename[13:18]
        brick_numbers_set.add(brick_number_value)

    # confirm every bricknumber is unique
    assert len(brick_numbers_set) == len(brick_filenames)
    assert brick_numbers_set == get_brick_numbers()

    # for category, category_dict in atom_config_dict.items():
    #     if category_dict.get(atom_insert()) is not None:
    #         category_insert = category_dict.get(atom_insert())
    #         if category_insert.get(atom_order_str) is None:
    #             x_str = f"Missing from {category} {atom_insert()} {category_insert.get(atom_order_str)=}"
    #             print(x_str)
    #             return False

    #     if category_dict.get(atom_update()) is not None:
    #         category_update = category_dict.get(atom_update())
    #         if category_update.get(atom_order_str) is None:
    #             x_str = f"Missing from {category} {atom_update()} {category_update.get(atom_order_str)=}"
    #             print(x_str)
    #             return False

    #     if category_dict.get(atom_delete()) is not None:
    #         category_delete = category_dict.get(atom_delete())
    #         if category_delete.get(atom_order_str) is None:
    #             x_str = f"Missing from {category} {atom_delete()} {category_delete.get(atom_order_str)=}"
    #             print(x_str)
    #             return False

    #     if category_dict.get(normal_specs_str()) is None:
    #         print(f"{category=} {normal_specs_str()} is missing")
    #         return False
    return True


def test_get_atom_config_dict_EveryCrudOperationHasDeltaOrderGroup():
    # ESTABLISH
    brick_filenames = get_brick_filenames()

    # WHEN / THEN
    assert _validate_brick_files(brick_filenames)
    # # Simple script for editing atom_config.json
    # set_mog(atom_insert(), bud_acctunit_str(), 0)
    # set_mog(atom_insert(), bud_acct_membership_str(), 1)
    # set_mog(atom_insert(), bud_itemunit_str(), 2)
    # set_mog(atom_insert(), bud_item_awardlink_str(), 3)
    # set_mog(atom_insert(), bud_item_teamlink_str(), 4)
    # set_mog(atom_insert(), bud_item_healerlink_str(), 5)
    # set_mog(atom_insert(), bud_item_factunit_str(), 6)
    # set_mog(atom_insert(), bud_item_reasonunit_str(), 7)
    # set_mog(atom_insert(), bud_item_reason_premiseunit_str(), 8)
    # set_mog(atom_update(), bud_acctunit_str(), 9)
    # set_mog(atom_update(), bud_acct_membership_str(), 10)
    # set_mog(atom_update(), bud_itemunit_str(), 11)
    # set_mog(atom_update(), bud_item_awardlink_str(), 12)
    # set_mog(atom_update(), bud_item_factunit_str(), 13)
    # set_mog(atom_update(), bud_item_reason_premiseunit_str(), 14)
    # set_mog(atom_update(), bud_item_reasonunit_str(), 15)
    # set_mog(atom_delete(), bud_item_reason_premiseunit_str(), 16)
    # set_mog(atom_delete(), bud_item_reasonunit_str(), 17)
    # set_mog(atom_delete(), bud_item_factunit_str(), 18)
    # set_mog(atom_delete(), bud_item_teamlink_str(), 19)
    # set_mog(atom_delete(), bud_item_healerlink_str(), 20)
    # set_mog(atom_delete(), bud_item_awardlink_str(), 21)
    # set_mog(atom_delete(), bud_itemunit_str(), 22)
    # set_mog(atom_delete(), bud_acct_membership_str(), 23)
    # set_mog(atom_delete(), bud_acctunit_str(), 24)
    # set_mog(atom_update(), budunit_str(), 25)

    # assert 0 == q_order(atom_insert(), bud_acctunit_str())
    # assert 1 == q_order(atom_insert(), bud_acct_membership_str())
    # assert 2 == q_order(atom_insert(), bud_itemunit_str())
    # assert 3 == q_order(atom_insert(), bud_item_awardlink_str())
    # assert 4 == q_order(atom_insert(), bud_item_teamlink_str())
    # assert 5 == q_order(atom_insert(), bud_item_healerlink_str())
    # assert 6 == q_order(atom_insert(), bud_item_factunit_str())
    # assert 7 == q_order(atom_insert(), bud_item_reasonunit_str())
    # assert 8 == q_order(atom_insert(), bud_item_reason_premiseunit_str())
    # assert 9 == q_order(atom_update(), bud_acctunit_str())
    # assert 10 == q_order(atom_update(), bud_acct_membership_str())
    # assert 11 == q_order(atom_update(), bud_itemunit_str())
    # assert 12 == q_order(atom_update(), bud_item_awardlink_str())
    # assert 13 == q_order(atom_update(), bud_item_factunit_str())
    # assert 14 == q_order(atom_update(), bud_item_reason_premiseunit_str())
    # assert 15 == q_order(atom_update(), bud_item_reasonunit_str())
    # assert 16 == q_order(atom_delete(), bud_item_reason_premiseunit_str())
    # assert 17 == q_order(atom_delete(), bud_item_reasonunit_str())
    # assert 18 == q_order(atom_delete(), bud_item_factunit_str())
    # assert 19 == q_order(atom_delete(), bud_item_teamlink_str())
    # assert 20 == q_order(atom_delete(), bud_item_healerlink_str())
    # assert 21 == q_order(atom_delete(), bud_item_awardlink_str())
    # assert 22 == q_order(atom_delete(), bud_itemunit_str())
    # assert 23 == q_order(atom_delete(), bud_acct_membership_str())
    # assert 24 == q_order(atom_delete(), bud_acctunit_str())
    # assert 25 == q_order(atom_update(), budunit_str())
