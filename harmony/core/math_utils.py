from harmony.core.constants import FloatComparisonTolerance
from harmony.typing import Number


def difference_between(minuend: Number, subtrahend: Number) -> Number:
    """Return the result of the difference between both numbers passed"""
    return minuend - subtrahend


def absolute_difference_between(minuend: Number, subtrahend: Number) -> Number:
    """Return the absolute result of the difference between both numbers passed"""
    return abs(difference_between(minuend, subtrahend))


def are_almost_equal(
    number1: float,
    number2: float,
    tolerance: FloatComparisonTolerance = FloatComparisonTolerance.SEVEN_DECIMAL_PLACES,
) -> bool:
    """Return `True` if the difference between `first_number` and `second_number` is
    less than the `tolerance`"""
    return absolute_difference_between(number1, number2) < tolerance.value


def division_between(dividend: Number, divisor: Number) -> Number:
    """Return the quotient of the division between both numbers passed"""
    return dividend / divisor


def multiplication_between(multiplicand: Number, multiplier: Number) -> Number:
    """Return the multiplication between both numbers"""
    return multiplicand * multiplier


def addition_between(addend1: Number, addend2: Number) -> Number:
    """Return the addition between both numbers"""
    return addend1 + addend2
