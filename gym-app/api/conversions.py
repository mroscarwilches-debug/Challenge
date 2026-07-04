"""Weight conversion helpers shared by the API endpoints.

Kept in their own file instead of inside app.py, so we can test the
math on its own, without needing Flask or a database running.
"""

CONVERSION_FACTOR = 2.20462


def kg_to_lb(kg_value):
    """Convert kilograms to pounds."""
    return kg_value * CONVERSION_FACTOR


def lb_to_kg(lb_value):
    """Convert pounds to kilograms."""
    return lb_value / CONVERSION_FACTOR
