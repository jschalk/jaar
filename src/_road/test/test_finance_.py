from src._road.finance import (
    PixelUnit,
    PennyUnit,
    default_pixel_if_none,
    default_penny_if_none,
    trim_pixel_excess,
    trim_penny_excess,
)
from inspect import getdoc as inspect_getdoc

# from pytest import raises as pytest_raises
# from dataclasses import dataclass


def test_PixelUnit_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_pixelunit = PixelUnit(x_float)
    # THEN
    assert y_pixelunit == x_float
    inspect_str = "Smallest Unit of credor_weight or debtor_weight"
    assert inspect_getdoc(y_pixelunit) == inspect_str


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


def test_PennyUnit_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_pennyunit = PennyUnit(x_float)
    # THEN
    assert y_pennyunit == x_float
    assert inspect_getdoc(y_pennyunit) == "Smallest Unit of Money"


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
