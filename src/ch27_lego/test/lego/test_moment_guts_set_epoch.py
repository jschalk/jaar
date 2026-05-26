from ch00_py.file_toolbox import save_json
from ch08_person_logic.person_main import personunit_shop
from ch10_person_lesson._ref.ch10_path import create_moment_json_path
from ch10_person_lesson.lasso import lassounit_shop
from ch10_person_lesson.lesson_filehandler import open_gut_file, save_gut_file
from ch14_time.epoch_main import epochunit_shop
from ch14_time.test._util.ch14_examples import get_five_config
from ch15_moment.moment_main import momentunit_shop
from ch27_lego.lego_core import add_lego_epoch_to_mind_guts
from ch99_glossary.ch_keyword import Ch27Keywords as kw, ExampleStrs as exx
from os.path import exists as os_path_exists


def test_add_lego_epoch_to_mind_guts_SetsFiles_Scenario0(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_moment.epoch = epochunit_shop(get_five_config())
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_lasso)
    save_json(moment_json_path, None, a23_moment.to_dict())
    assert os_path_exists(moment_json_path)
    init_sue_gut = personunit_shop(exx.sue, exx.a23)
    time_rope = init_sue_gut.make_l1_rope(kw.time)
    five_rope = init_sue_gut.make_rope(time_rope, kw.five)
    save_gut_file(moment_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    add_lego_epoch_to_mind_guts(moment_mstr_dir)

    # THEN
    post_sue_gut = open_gut_file(moment_mstr_dir, a23_lasso, exx.sue)
    assert post_sue_gut.plan_exists(five_rope)
