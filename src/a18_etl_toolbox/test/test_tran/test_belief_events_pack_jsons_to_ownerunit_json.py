from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file, save_file
from src.a06_owner_logic.owner import (
    get_from_json as ownerunit_get_from_json,
    ownerunit_shop,
)
from src.a06_owner_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    owner_acctunit_str,
)
from src.a08_owner_atom_logic.test._util.a08_str import INSERT_str
from src.a09_pack_logic.pack import get_packunit_from_json, packunit_shop
from src.a12_hub_toolbox.hub_path import (
    create_event_all_pack_path,
    create_event_expressed_pack_path,
    create_owner_event_dir_path,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.transformers import (
    etl_event_pack_json_to_event_inherited_ownerunits,
)


def test_etl_event_pack_json_to_event_inherited_ownerunits_SetsFiles_owner_json(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    event3 = 3
    event7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "amy23"
    belief_mstr_dir = get_module_temp_dir()
    a23_bob_e3_dir = create_owner_event_dir_path(
        belief_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_owner_event_dir_path(
        belief_mstr_dir, a23_str, bob_inx, event7
    )
    a23_bob_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    a23_bob_e7_pack = packunit_shop(bob_inx, None, a23_str, event_int=event7)
    plnacct_dimen = owner_acctunit_str()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {acct_cred_points_str(): credit77, acct_debt_points_str(): None}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {acct_cred_points_str(): credit44, acct_debt_points_str(): None}
    a23_bob_e3_pack.add_owneratom(plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues)
    a23_bob_e3_pack.add_owneratom(plnacct_dimen, INSERT_str(), yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {acct_cred_points_str(): credit88, acct_debt_points_str(): None}
    a23_bob_e7_pack.add_owneratom(plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues)
    a23_bob_e7_pack.add_owneratom(plnacct_dimen, INSERT_str(), sue_jkeys, sue_jvalues)
    e3_all_pack_path = create_event_all_pack_path(
        belief_mstr_dir, a23_str, bob_inx, event3
    )
    e7_all_pack_path = create_event_all_pack_path(
        belief_mstr_dir, a23_str, bob_inx, event7
    )
    save_file(e3_all_pack_path, None, a23_bob_e3_pack.get_json())
    save_file(e7_all_pack_path, None, a23_bob_e7_pack.get_json())
    assert os_path_exists(e3_all_pack_path)
    assert os_path_exists(e7_all_pack_path)
    owner_filename = "owner.json"
    e3_owner_path = create_path(a23_bob_e3_dir, owner_filename)
    e7_owner_path = create_path(a23_bob_e7_dir, owner_filename)
    assert os_path_exists(e3_owner_path) is False
    assert os_path_exists(e7_owner_path) is False

    # WHEN
    etl_event_pack_json_to_event_inherited_ownerunits(belief_mstr_dir)

    # THEN
    assert os_path_exists(e3_owner_path)
    assert os_path_exists(e7_owner_path)
    expected_e3_bob_owner = ownerunit_shop(bob_inx, a23_str)
    expected_e7_bob_owner = ownerunit_shop(bob_inx, a23_str)
    expected_e3_bob_owner.add_acctunit(bob_inx, credit77)
    expected_e3_bob_owner.add_acctunit(yao_inx, credit44)
    expected_e7_bob_owner.add_acctunit(bob_inx, credit77)
    expected_e7_bob_owner.add_acctunit(sue_inx, credit88)
    expected_e7_bob_owner.add_acctunit(yao_inx, credit44)
    generated_e3_owner = ownerunit_get_from_json(open_file(e3_owner_path))
    generated_e7_owner = ownerunit_get_from_json(open_file(e7_owner_path))
    assert generated_e3_owner.accts == expected_e3_bob_owner.accts
    assert generated_e3_owner == expected_e3_bob_owner
    assert generated_e3_owner.get_dict() == expected_e3_bob_owner.get_dict()
    assert generated_e7_owner.accts == expected_e7_bob_owner.accts
    assert generated_e7_owner.get_dict() == expected_e7_bob_owner.get_dict()


def test_etl_event_pack_json_to_event_inherited_ownerunits_SetsFiles_expressed_pack(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    xia_inx = "Xia"
    event3 = 3
    event7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "amy23"
    belief_mstr_dir = get_module_temp_dir()
    a23_bob_e3_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    a23_bob_e7_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    plnacct_dimen = owner_acctunit_str()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {acct_cred_points_str(): credit77}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {acct_cred_points_str(): credit44}
    a23_bob_e3_pack.add_owneratom(plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues)
    a23_bob_e3_pack.add_owneratom(plnacct_dimen, INSERT_str(), yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {acct_cred_points_str(): credit88}
    a23_bob_e7_pack.add_owneratom(plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues)
    a23_bob_e7_pack.add_owneratom(plnacct_dimen, INSERT_str(), sue_jkeys, sue_jvalues)
    a23_bob_e3_all_pack_path = create_event_all_pack_path(
        belief_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_all_pack_path = create_event_all_pack_path(
        belief_mstr_dir, a23_str, bob_inx, event7
    )
    save_file(a23_bob_e3_all_pack_path, None, a23_bob_e3_pack.get_json())
    save_file(a23_bob_e7_all_pack_path, None, a23_bob_e7_pack.get_json())
    e3_expressed_pack_path = create_event_expressed_pack_path(
        belief_mstr_dir, a23_str, bob_inx, event3
    )
    e7_expressed_pack_path = create_event_expressed_pack_path(
        belief_mstr_dir, a23_str, bob_inx, event7
    )
    assert os_path_exists(a23_bob_e3_all_pack_path)
    assert os_path_exists(a23_bob_e7_all_pack_path)
    assert os_path_exists(e3_expressed_pack_path) is False
    assert os_path_exists(e7_expressed_pack_path) is False

    # WHEN
    etl_event_pack_json_to_event_inherited_ownerunits(belief_mstr_dir)

    # THEN
    assert os_path_exists(e3_expressed_pack_path)
    assert os_path_exists(e7_expressed_pack_path)
    gen_e3_express_pack = get_packunit_from_json(open_file(e3_expressed_pack_path))
    gen_e7_express_pack = get_packunit_from_json(open_file(e7_expressed_pack_path))
    expected_e3_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    expected_e7_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    expected_e3_bob_pack.add_owneratom(
        plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues
    )
    expected_e3_bob_pack.add_owneratom(
        plnacct_dimen, INSERT_str(), yao_jkeys, yao_jvalues
    )
    expected_e7_bob_pack.add_owneratom(
        plnacct_dimen, INSERT_str(), sue_jkeys, sue_jvalues
    )
    assert expected_e3_bob_pack == a23_bob_e3_pack
    assert expected_e7_bob_pack._ownerdelta != a23_bob_e7_pack._ownerdelta
    assert expected_e7_bob_pack != a23_bob_e7_pack
    # expected_e3_bob_pack.add_owneratom()
    # expected_e3_bob_pack.add_owneratom()
    # expected_e7_bob_pack.add_owneratom()
    # expected_e7_bob_pack.add_owneratom()
    # expected_e7_bob_pack.add_owneratom()
    assert gen_e3_express_pack == expected_e3_bob_pack
    gen_e7_express_delta = gen_e7_express_pack._ownerdelta
    expected_e7_delta = expected_e7_bob_pack._ownerdelta
    assert gen_e7_express_delta.owneratoms == expected_e7_delta.owneratoms
    assert gen_e7_express_pack._ownerdelta == expected_e7_bob_pack._ownerdelta
    assert gen_e7_express_pack == expected_e7_bob_pack
