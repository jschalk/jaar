from pytest import raises as pytest_raises
from src.ch04_voice.voice import calc_give_take_net


def test_calc_give_take_net_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert calc_give_take_net(x_give=5, x_take=6) == -1
    assert calc_give_take_net(x_give=55, x_take=6) == 49
    assert calc_give_take_net(x_give=55, x_take=None) == 55
    assert calc_give_take_net(x_give=None, x_take=44) == -44
    assert calc_give_take_net(x_give=None, x_take=None) == 0

    with pytest_raises(Exception) as excinfo:
        calc_give_take_net(x_give=-1, x_take=14)
    assert (
        str(excinfo.value)
        == "calc_give_take_net x_give=-1. Only non-negative numbers allowed."
    )

    with pytest_raises(Exception) as excinfo:
        calc_give_take_net(x_give=15, x_take=-5)
    assert (
        str(excinfo.value)
        == "calc_give_take_net x_take=-5. Only non-negative numbers allowed."
    )

    with pytest_raises(Exception) as excinfo:
        calc_give_take_net(x_give=-4, x_take=-5)
    assert (
        str(excinfo.value)
        == "calc_give_take_net x_give=-4 and x_take=-5. Only non-negative numbers allowed."
    )
