def pytest_addoption(parser):
    parser.addoption("--graphics_bool", action="store", default=False)
    parser.addoption("--big_volume", action="store", default=False)


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    graphics_bool_value = metafunc.config.option.graphics_bool
    graphics_bool_value = graphics_bool_value == "True"
    if "graphics_bool" in metafunc.fixturenames and graphics_bool_value is not None:
        metafunc.parametrize("graphics_bool", [graphics_bool_value])
    big_volume_value = metafunc.config.option.big_volume
    big_volume_value = big_volume_value == "True"
    if "big_volume" in metafunc.fixturenames and big_volume_value is not None:
        metafunc.parametrize("big_volume", [big_volume_value])
