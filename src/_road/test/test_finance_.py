from src._road.finance import (
    default_pixel_if_none,
    trim_pixel_excess,
    FinanceUnit,
    default_penny_if_none,
    trim_penny_excess,
)
from inspect import getdoc as inspect_getdoc

# from pytest import raises as pytest_raises
# from dataclasses import dataclass


def test_FinanceUnit_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_financeunit = FinanceUnit(x_float)
    # THEN
    assert y_financeunit == x_float
    assert (
        inspect_getdoc(y_financeunit)
        == "A number that can be used for financial calculations."
    )


def test_default_pixel_if_none_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert default_pixel_if_none() == 1
    assert default_pixel_if_none(5) == 5
    assert default_pixel_if_none(0.03) == 0.03


def test_trim_pixel_excess_ReturnsCorrectedFloat():
    # GIVEN / WHEN / THEN
    assert trim_pixel_excess(num=5.5, pixel=1) == 5
    assert trim_pixel_excess(num=0.5, pixel=1) == 0
    assert trim_pixel_excess(num=5.5, pixel=0.1) == 5.5
    assert trim_pixel_excess(num=0.5, pixel=0.01) == 0.5
    assert trim_pixel_excess(num=0.56, pixel=0.1) == 0.5
    assert trim_pixel_excess(num=0.56, pixel=0.133) == 0.532


def test_default_penny_if_none_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert default_penny_if_none() == 1
    assert default_penny_if_none(5) == 5
    assert default_penny_if_none(0.03) == 1


def test_trim_penny_excess_ReturnsCorrectedFloat():
    # GIVEN / WHEN / THEN
    assert trim_penny_excess(num=5.5, pixel=1) == 5
    assert trim_penny_excess(num=0.5, pixel=1) == 0
    assert trim_penny_excess(num=5.5, pixel=0.1) == 5.5
    assert trim_penny_excess(num=0.5, pixel=0.01) == 0.5
    assert trim_penny_excess(num=0.56, pixel=0.1) == 0.5
    assert trim_penny_excess(num=0.56, pixel=0.133) == 0.532
