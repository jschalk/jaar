def pytest_addoption(parser):
    parser.addoption("--graphics_bool", action="store", default=False)
    parser.addoption("--run_big_tests", action="store", default=False)
    parser.addoption("--rebuild_bool", action="store", default=False)


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    graphics_bool_value = metafunc.config.option.graphics_bool
    graphics_bool_value = str(graphics_bool_value).lower() == "true"
    if "graphics_bool" in metafunc.fixturenames and graphics_bool_value is not None:
        metafunc.parametrize("graphics_bool", [graphics_bool_value])
    run_big_tests_value = metafunc.config.option.run_big_tests
    run_big_tests_value = run_big_tests_value == "True"
    if "run_big_tests" in metafunc.fixturenames and run_big_tests_value is not None:
        metafunc.parametrize("run_big_tests", [run_big_tests_value])
    rebuild_bool_value = metafunc.config.option.rebuild_bool
    rebuild_bool_value = rebuild_bool_value == "True"
    if "rebuild_bool" in metafunc.fixturenames and rebuild_bool_value is not None:
        metafunc.parametrize("rebuild_bool", [rebuild_bool_value])
