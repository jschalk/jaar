def pytest_addoption(parser):
    parser.addoption("--graphics_bool", action="store", default=False)


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.graphics_bool
    option_value = option_value == "True"
    if "graphics_bool" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("graphics_bool", [option_value])
