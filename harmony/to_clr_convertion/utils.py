from harmony import core


def is_clr_color_count_invalid(color_count: int) -> bool:
    """Return `True` if the value is bigger than 0"""
    return color_count <= 0


def is_8_bit_signed_integer(integer_to_check: int) -> bool:
    """Return `True` if the value is between -127 and 127 including the bounds"""
    return (
        core.MINIMUM_8_BIT_SIGNED_INTEGER_VALUE
        <= integer_to_check
        <= core.MAXIMUM_8_BIT_SIGNED_INTEGER_VALUE
    )


def is_clr_color_component_near_one(component_as_decimal) -> bool:
    """Return `True` if the value is near one"""
    return core.are_almost_equal(
        component_as_decimal,
        1,
        tolerance=core.FloatComparisonTolerance.THREE_DECIMAL_PLACES,
    )


def is_clr_color_component_near_zero(component_as_decimal: float) -> bool:
    """Return `True` if the value is near zero"""
    return core.are_almost_equal(
        component_as_decimal, 0, core.FloatComparisonTolerance.THREE_DECIMAL_PLACES
    )
