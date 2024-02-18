"""Format tests"""

import pytest
from zero.format import Quantity


@pytest.mark.parametrize(
    "quantity,expected",
    (
        # Floats.
        (Quantity(1.23), 1.23),
        (Quantity(5.3e6), 5.3e6),
        (Quantity(-765e3), -765e3),
        # Strings (simple).
        (Quantity("1.23"), 1.23),
        (Quantity("-765e3"), -765e3),
        # Strings (SI).
        (Quantity("1.23y"), 1.23e-24),
        (Quantity("1.23z"), 1.23e-21),
        (Quantity("1.23a"), 1.23e-18),
        (Quantity("1.23f"), 1.23e-15),
        (Quantity("1.23p"), 1.23e-12),
        (Quantity("1.23n"), 1.23e-9),
        (Quantity("1.23µ"), 1.23e-6),
        (Quantity("1.23u"), 1.23e-6),
        (Quantity("1.23m"), 1.23e-3),
        (Quantity("1.23k"), 1.23e3),
        (Quantity("1.23M"), 1.23e6),
        (Quantity("1.23G"), 1.23e9),
        (Quantity("1.23T"), 1.23e12),
        (Quantity("1.23P"), 1.23e15),
        (Quantity("1.23E"), 1.23e18),
        (Quantity("1.23Z"), 1.23e21),
        (Quantity("1.23Y"), 1.23e24),

    )
)
def test_values(quantity, expected):
    assert quantity == expected


@pytest.mark.parametrize(
    "quantity,value,unit",
    (
        (Quantity("1.23"), 1.23, ""),
        (Quantity("1.23 Hz"), 1.23, "Hz"),
        (Quantity("1.69pF"), 1.69e-12, "F"),
        (Quantity("3.21uH"), 3.21e-6, "H"),
        (Quantity("4.88MΩ"), 4.88e6, "Ω"),
    )
)
def test_units_and_si_scales(quantity, value, unit):
    assert quantity == value
    assert quantity.units == unit


@pytest.mark.parametrize(
    "quantity",
    (
        Quantity("1.50"),
        Quantity("1.23MHz"),
        Quantity("1.23 MHz"),
        Quantity("1.50 pF"),
        Quantity("4.88 MΩ"),
        Quantity("4 nH"),
    )
)
def test_copy(quantity):
    # Objects equal.
    assert quantity == Quantity(quantity)
    # Floats equal.
    assert float(quantity) == float(Quantity(quantity))
    # Strings equal.
    assert str(quantity) == str(Quantity(quantity))
