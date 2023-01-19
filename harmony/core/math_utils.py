from harmony.core.constants import FloatComparisonTolerance
from harmony.typing import Number


def difference_between(first_number: Number, second_number: Number) -> Number:
    """Return the result of the difference between both numbers passed"""
    return first_number - second_number


def quotient_between(first_number: Number, second_number: Number) -> Number:
    """Return the quotient of the division between both numbers passed"""
    return first_number / second_number


def absolute_difference_between(first_number: Number, second_number: Number) -> Number:
    """Return the absolute result of the difference between both numbers passed"""
    return abs(difference_between(first_number, second_number))


def are_almost_equal(
    first_number: float,
    second_number: float,
    tolerance: FloatComparisonTolerance = FloatComparisonTolerance.SEVEN_DECIMAL_PLACES,
) -> bool:
    """Return `True` if the difference between `first_number` and `second_number` is
    less than the `tolerance`"""
    return absolute_difference_between(first_number, second_number) < tolerance.value
