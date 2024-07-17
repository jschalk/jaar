from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.gift.atom import atom_insert
from src.gift.atom_config import world_charunit_text
from src.gift.change import changeunit_shop, get_filtered_changeunit


def test_ChangeUnit_get_filtered_changeunit_ReturnsObjFilteredBy_charunit_insert():
    # ESTABLISH
    sue_text = "Sue"
    yao_text = "Yao"
    before_sue_world = worldunit_shop(sue_text)
    before_sue_world.add_charunit(yao_text)
    after_sue_world = worldunit_shop(sue_text)
    bob_text = "Bob"
    bob_credor_weight = 33
    bob_debtor_weight = 44
    after_sue_world.add_charunit(bob_text, bob_credor_weight, bob_debtor_weight)
    after_sue_world.add_l1_idea(ideaunit_shop("casa"))
    old_changeunit = changeunit_shop()
    old_changeunit.add_all_different_atomunits(before_sue_world, after_sue_world)

    category_set = [world_charunit_text()]
    curd_set = {atom_insert()}
    new_changeunit = get_filtered_changeunit(old_changeunit, category_set, curd_set)

    # THEN
    new_changeunit.get_category_sorted_atomunits_list()
    assert len(new_changeunit.get_category_sorted_atomunits_list()) == 1
    sue_insert_dict = new_changeunit.atomunits.get(atom_insert())
    sue_charunit_dict = sue_insert_dict.get("world_charunit")
    bob_atomunit = sue_charunit_dict.get(bob_text)
    assert bob_atomunit.get_value("char_id") == bob_text
    assert bob_atomunit.get_value("credor_weight") == bob_credor_weight
    assert bob_atomunit.get_value("debtor_weight") == bob_debtor_weight
