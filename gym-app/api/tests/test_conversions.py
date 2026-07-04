"""Unit tests for weight conversion functions.

Just checks the math is right - no Flask, no database involved.
"""
from conversions import kg_to_lb, lb_to_kg


def test_kg_to_lb():
    # Checks 1 kg converts to about 2.20 lb.
    assert round(kg_to_lb(1), 2) == 2.20


def test_lb_to_kg():
    # Checks the conversion factor in pounds converts back to 1 kg.
    assert round(lb_to_kg(2.20462), 2) == 1.0


def test_round_trip():
    # Converts kg to lb and back to kg - should land close to the
    # original number.
    original = 75
    converted = lb_to_kg(kg_to_lb(original))
    assert round(converted, 2) == original
