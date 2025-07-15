from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file, save_file
from src.a06_believer_logic.believer import (
    believerunit_shop,
    get_from_json as believerunit_get_from_json,
)
from src.a06_believer_logic.test._util.a06_str import (
    believer_partnerunit_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
)
from src.a08_believer_atom_logic.test._util.a08_str import INSERT_str
from src.a09_pack_logic.pack import get_packunit_from_json, packunit_shop
from src.a12_hub_toolbox.a12_path import (
    create_believer_event_dir_path,
    create_event_all_pack_path,
    create_event_expressed_pack_path,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.transformers import (
    etl_event_pack_json_to_event_inherited_believerunits,
)


def test_etl_event_pack_json_to_event_inherited_believerunits_SetsFiles_believer_json(
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
    a23_bob_e3_dir = create_believer_event_dir_path(
        belief_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_believer_event_dir_path(
        belief_mstr_dir, a23_str, bob_inx, event7
    )
    a23_bob_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    a23_bob_e7_pack = packunit_shop(bob_inx, None, a23_str, event_int=event7)
    blrpern_dimen = believer_partnerunit_str()
    bob_jkeys = {partner_name_str(): bob_inx}
    bob_jvalues = {partner_cred_points_str(): credit77, partner_debt_points_str(): None}
    yao_jkeys = {partner_name_str(): yao_inx}
    yao_jvalues = {partner_cred_points_str(): credit44, partner_debt_points_str(): None}
    a23_bob_e3_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), bob_jkeys, bob_jvalues
    )
    a23_bob_e3_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), yao_jkeys, yao_jvalues
    )
    sue_jkeys = {partner_name_str(): sue_inx}
    sue_jvalues = {partner_cred_points_str(): credit88, partner_debt_points_str(): None}
    a23_bob_e7_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), bob_jkeys, bob_jvalues
    )
    a23_bob_e7_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), sue_jkeys, sue_jvalues
    )
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
    believer_filename = "believer.json"
    e3_believer_path = create_path(a23_bob_e3_dir, believer_filename)
    e7_believer_path = create_path(a23_bob_e7_dir, believer_filename)
    assert os_path_exists(e3_believer_path) is False
    assert os_path_exists(e7_believer_path) is False

    # WHEN
    etl_event_pack_json_to_event_inherited_believerunits(belief_mstr_dir)

    # THEN
    assert os_path_exists(e3_believer_path)
    assert os_path_exists(e7_believer_path)
    expected_e3_bob_believer = believerunit_shop(bob_inx, a23_str)
    expected_e7_bob_believer = believerunit_shop(bob_inx, a23_str)
    expected_e3_bob_believer.add_partnerunit(bob_inx, credit77)
    expected_e3_bob_believer.add_partnerunit(yao_inx, credit44)
    expected_e7_bob_believer.add_partnerunit(bob_inx, credit77)
    expected_e7_bob_believer.add_partnerunit(sue_inx, credit88)
    expected_e7_bob_believer.add_partnerunit(yao_inx, credit44)
    generated_e3_believer = believerunit_get_from_json(open_file(e3_believer_path))
    generated_e7_believer = believerunit_get_from_json(open_file(e7_believer_path))
    assert generated_e3_believer.partners == expected_e3_bob_believer.partners
    assert generated_e3_believer == expected_e3_bob_believer
    assert generated_e3_believer.get_dict() == expected_e3_bob_believer.get_dict()
    assert generated_e7_believer.partners == expected_e7_bob_believer.partners
    assert generated_e7_believer.get_dict() == expected_e7_bob_believer.get_dict()


def test_etl_event_pack_json_to_event_inherited_believerunits_SetsFiles_expressed_pack(
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
    blrpern_dimen = believer_partnerunit_str()
    bob_jkeys = {partner_name_str(): bob_inx}
    bob_jvalues = {partner_cred_points_str(): credit77}
    yao_jkeys = {partner_name_str(): yao_inx}
    yao_jvalues = {partner_cred_points_str(): credit44}
    a23_bob_e3_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), bob_jkeys, bob_jvalues
    )
    a23_bob_e3_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), yao_jkeys, yao_jvalues
    )
    sue_jkeys = {partner_name_str(): sue_inx}
    sue_jvalues = {partner_cred_points_str(): credit88}
    a23_bob_e7_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), bob_jkeys, bob_jvalues
    )
    a23_bob_e7_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), sue_jkeys, sue_jvalues
    )
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
    etl_event_pack_json_to_event_inherited_believerunits(belief_mstr_dir)

    # THEN
    assert os_path_exists(e3_expressed_pack_path)
    assert os_path_exists(e7_expressed_pack_path)
    gen_e3_express_pack = get_packunit_from_json(open_file(e3_expressed_pack_path))
    gen_e7_express_pack = get_packunit_from_json(open_file(e7_expressed_pack_path))
    expected_e3_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    expected_e7_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    expected_e3_bob_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), bob_jkeys, bob_jvalues
    )
    expected_e3_bob_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), yao_jkeys, yao_jvalues
    )
    expected_e7_bob_pack.add_believeratom(
        blrpern_dimen, INSERT_str(), sue_jkeys, sue_jvalues
    )
    assert expected_e3_bob_pack == a23_bob_e3_pack
    assert expected_e7_bob_pack._believerdelta != a23_bob_e7_pack._believerdelta
    assert expected_e7_bob_pack != a23_bob_e7_pack
    # expected_e3_bob_pack.add_believeratom()
    # expected_e3_bob_pack.add_believeratom()
    # expected_e7_bob_pack.add_believeratom()
    # expected_e7_bob_pack.add_believeratom()
    # expected_e7_bob_pack.add_believeratom()
    assert gen_e3_express_pack == expected_e3_bob_pack
    gen_e7_express_delta = gen_e7_express_pack._believerdelta
    expected_e7_delta = expected_e7_bob_pack._believerdelta
    assert gen_e7_express_delta.believeratoms == expected_e7_delta.believeratoms
    assert gen_e7_express_pack._believerdelta == expected_e7_bob_pack._believerdelta
    assert gen_e7_express_pack == expected_e7_bob_pack
