from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file, save_file
from src.a06_plan_logic._util.a06_str import (
    acct_name_str,
    credit_score_str,
    debt_score_str,
    plan_acctunit_str,
)
from src.a06_plan_logic.plan import (
    get_from_json as planunit_get_from_json,
    planunit_shop,
)
from src.a08_plan_atom_logic._util.a08_str import INSERT_str
from src.a09_pack_logic.pack import get_packunit_from_json, packunit_shop
from src.a12_hub_toolbox.hub_path import (
    create_event_all_pack_path,
    create_event_expressed_pack_path,
    create_owner_event_dir_path,
)
from src.a18_etl_toolbox._util.a18_env import env_dir_setup_cleanup, get_module_temp_dir
from src.a18_etl_toolbox.transformers import (
    etl_event_pack_json_to_event_inherited_planunits,
)


def test_etl_event_pack_json_to_event_inherited_planunits_SetsFiles_plan_json(
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
    a23_str = "accord23"
    vow_mstr_dir = get_module_temp_dir()
    a23_bob_e3_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, bob_inx, event3)
    a23_bob_e7_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, bob_inx, event7)
    a23_bob_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    a23_bob_e7_pack = packunit_shop(bob_inx, None, a23_str, event_int=event7)
    plnacct_dimen = plan_acctunit_str()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {credit_score_str(): credit77, debt_score_str(): None}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {credit_score_str(): credit44, debt_score_str(): None}
    a23_bob_e3_pack.add_planatom(plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues)
    a23_bob_e3_pack.add_planatom(plnacct_dimen, INSERT_str(), yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {credit_score_str(): credit88, debt_score_str(): None}
    a23_bob_e7_pack.add_planatom(plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues)
    a23_bob_e7_pack.add_planatom(plnacct_dimen, INSERT_str(), sue_jkeys, sue_jvalues)
    e3_all_pack_path = create_event_all_pack_path(
        vow_mstr_dir, a23_str, bob_inx, event3
    )
    e7_all_pack_path = create_event_all_pack_path(
        vow_mstr_dir, a23_str, bob_inx, event7
    )
    save_file(e3_all_pack_path, None, a23_bob_e3_pack.get_json())
    save_file(e7_all_pack_path, None, a23_bob_e7_pack.get_json())
    assert os_path_exists(e3_all_pack_path)
    assert os_path_exists(e7_all_pack_path)
    plan_filename = "plan.json"
    e3_plan_path = create_path(a23_bob_e3_dir, plan_filename)
    e7_plan_path = create_path(a23_bob_e7_dir, plan_filename)
    assert os_path_exists(e3_plan_path) is False
    assert os_path_exists(e7_plan_path) is False

    # WHEN
    etl_event_pack_json_to_event_inherited_planunits(vow_mstr_dir)

    # THEN
    assert os_path_exists(e3_plan_path)
    assert os_path_exists(e7_plan_path)
    expected_e3_bob_plan = planunit_shop(bob_inx, a23_str)
    expected_e7_bob_plan = planunit_shop(bob_inx, a23_str)
    expected_e3_bob_plan.add_acctunit(bob_inx, credit77)
    expected_e3_bob_plan.add_acctunit(yao_inx, credit44)
    expected_e7_bob_plan.add_acctunit(bob_inx, credit77)
    expected_e7_bob_plan.add_acctunit(sue_inx, credit88)
    expected_e7_bob_plan.add_acctunit(yao_inx, credit44)
    generated_e3_plan = planunit_get_from_json(open_file(e3_plan_path))
    generated_e7_plan = planunit_get_from_json(open_file(e7_plan_path))
    assert generated_e3_plan.accts == expected_e3_bob_plan.accts
    assert generated_e3_plan == expected_e3_bob_plan
    assert generated_e3_plan.get_dict() == expected_e3_bob_plan.get_dict()
    assert generated_e7_plan.accts == expected_e7_bob_plan.accts
    assert generated_e7_plan.get_dict() == expected_e7_bob_plan.get_dict()


def test_etl_event_pack_json_to_event_inherited_planunits_SetsFiles_expressed_pack(
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
    a23_str = "accord23"
    vow_mstr_dir = get_module_temp_dir()
    a23_bob_e3_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    a23_bob_e7_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    plnacct_dimen = plan_acctunit_str()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {credit_score_str(): credit77}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {credit_score_str(): credit44}
    a23_bob_e3_pack.add_planatom(plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues)
    a23_bob_e3_pack.add_planatom(plnacct_dimen, INSERT_str(), yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {credit_score_str(): credit88}
    a23_bob_e7_pack.add_planatom(plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues)
    a23_bob_e7_pack.add_planatom(plnacct_dimen, INSERT_str(), sue_jkeys, sue_jvalues)
    a23_bob_e3_all_pack_path = create_event_all_pack_path(
        vow_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_all_pack_path = create_event_all_pack_path(
        vow_mstr_dir, a23_str, bob_inx, event7
    )
    save_file(a23_bob_e3_all_pack_path, None, a23_bob_e3_pack.get_json())
    save_file(a23_bob_e7_all_pack_path, None, a23_bob_e7_pack.get_json())
    e3_expressed_pack_path = create_event_expressed_pack_path(
        vow_mstr_dir, a23_str, bob_inx, event3
    )
    e7_expressed_pack_path = create_event_expressed_pack_path(
        vow_mstr_dir, a23_str, bob_inx, event7
    )
    assert os_path_exists(a23_bob_e3_all_pack_path)
    assert os_path_exists(a23_bob_e7_all_pack_path)
    assert os_path_exists(e3_expressed_pack_path) is False
    assert os_path_exists(e7_expressed_pack_path) is False

    # WHEN
    etl_event_pack_json_to_event_inherited_planunits(vow_mstr_dir)

    # THEN
    assert os_path_exists(e3_expressed_pack_path)
    assert os_path_exists(e7_expressed_pack_path)
    gen_e3_express_pack = get_packunit_from_json(open_file(e3_expressed_pack_path))
    gen_e7_express_pack = get_packunit_from_json(open_file(e7_expressed_pack_path))
    expected_e3_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    expected_e7_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    expected_e3_bob_pack.add_planatom(
        plnacct_dimen, INSERT_str(), bob_jkeys, bob_jvalues
    )
    expected_e3_bob_pack.add_planatom(
        plnacct_dimen, INSERT_str(), yao_jkeys, yao_jvalues
    )
    expected_e7_bob_pack.add_planatom(
        plnacct_dimen, INSERT_str(), sue_jkeys, sue_jvalues
    )
    assert expected_e3_bob_pack == a23_bob_e3_pack
    assert expected_e7_bob_pack._plandelta != a23_bob_e7_pack._plandelta
    assert expected_e7_bob_pack != a23_bob_e7_pack
    # expected_e3_bob_pack.add_planatom()
    # expected_e3_bob_pack.add_planatom()
    # expected_e7_bob_pack.add_planatom()
    # expected_e7_bob_pack.add_planatom()
    # expected_e7_bob_pack.add_planatom()
    assert gen_e3_express_pack == expected_e3_bob_pack
    gen_e7_express_delta = gen_e7_express_pack._plandelta
    expected_e7_delta = expected_e7_bob_pack._plandelta
    assert gen_e7_express_delta.planatoms == expected_e7_delta.planatoms
    assert gen_e7_express_pack._plandelta == expected_e7_bob_pack._plandelta
    assert gen_e7_express_pack == expected_e7_bob_pack
