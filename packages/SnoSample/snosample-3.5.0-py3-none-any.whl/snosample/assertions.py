# Default Python packages.
from typing import Callable, Type, Optional, Union

# Packages from requirements.
from numpy import ndarray, array_equal, allclose

ALL = Union[bool, str, int, float, list, tuple, dict, ndarray]
NUMERIC = (Union[int, float, list[int], list[float], list[Union[int, float]],
           tuple[int], tuple[float], tuple[Union[int, float]], ndarray])


def assert_equal(calc: ALL, true: ALL) -> None:
    """
    Assert if two variables are equal.

    Parameters
    ----------
    calc: ALL
        Calculated or predicted variable value.
    true: ALL
        True or expected variable value.
    """
    # Raise error if numpy arrays are not equal.
    if isinstance(calc, ndarray) and isinstance(true, ndarray):
        if not array_equal(a1=calc, a2=true):
            raise AssertionError(f"calculated value {calc} is not equal to true value {true}")

    # Raise error if types are not equal.
    elif not isinstance(calc, type(true)):
        raise AssertionError(f"calculated {type(calc)} is not equal to true {type(true)}")

    # Raise error if variables with built-in types are not equal.
    elif calc != true:
        raise AssertionError(f"calculated value {calc} is not equal to true value {true}")


def assert_not_equal(calc: ALL, true: ALL) -> None:
    """
    Assert if two variables are not equal.

    Parameters
    ----------
    calc: ALL
        Calculated or predicted variable value.
    true: ALL
        True or expected variable value.
    """
    # Raise error if numpy arrays are equal.
    if isinstance(calc, ndarray) and isinstance(true, ndarray):
        if array_equal(a1=calc, a2=true):
            raise AssertionError(f"calculated value {calc} is equal to true value {true}")

    # Return if types are not equal.
    elif not isinstance(calc, type(true)):
        return

    # Raise error if variables with built-in types are equal.
    elif calc == true:
        raise AssertionError(f"calculated value {calc} is equal to true value {true}")


def assert_almost_equal(calc: NUMERIC, true: NUMERIC,
                        margin: float, relative: bool = True) -> None:
    """
    Assert if two variables are almost equal within a given margin.
    Supported accuracy: up to and including 10 ** -10.

    Parameters
    ----------
    calc: NUMERIC
        Calculated or predicted variable value.
    true: NUMERIC
        True or expected variable value.
    margin: float
        Allowed margin for the comparison.
        The true value is used as a reference.
    relative: bool
        The margin is a fraction of the reference value when True (relative),
        or the margin is used directly when False (absolute).
    """
    # Raise error if numpy arrays are not almost equal.
    if isinstance(calc, ndarray) and isinstance(true, ndarray):
        margin_rel = margin if relative else 0
        margin_abs = margin if not relative else 0

        if not allclose(a=calc, b=true, rtol=margin_rel, atol=margin_abs):
            raise AssertionError(f"calculated {calc} is not close to true {true}")

    # Check if variables are lists or tuples.
    elif isinstance(calc, (list, tuple)) and isinstance(true, (list, tuple)):
        if len(calc) != len(true):
            raise AssertionError(f"calculated {calc} is not the same size as true {true}")

        # Check each element if lengths match.
        for i, _ in enumerate(calc):
            # Calculate allowed margin.
            allowed = true[i] * margin if relative else margin
            value = round(abs(calc[i] - true[i]), 10)

            # Elements are not equal when calculated value lies outside allowed margin.
            if value >= allowed:
                raise AssertionError(f"calculated {calc} is not close to true {true}")

    # Perform single comparison if variables are integers or floats.
    elif isinstance(calc, (int, float)) and isinstance(true, (int, float)):
        # Calculate allowed margin.
        allowed = true * margin if relative else margin
        value = round(abs(calc - true), 10)

        # Variables are not equal when calculated value lies outside allowed margin.
        if value >= allowed:
            raise AssertionError(f"calculated {calc} is not close to true {true}")

    # Raise error if types are not equal.
    elif not isinstance(calc, type(true)):
        raise AssertionError(f"calculated {type(calc)} is not equal to true {type(true)}")


def assert_true(expr: bool) -> None:
    """
    Assert if an expression is True.

    Parameters
    ----------
    expr: bool
        Any expression which can be reduced to a boolean (e.g. non-empty list, operator).
    """
    if not expr:
        raise AssertionError(f"expression {expr} is not True")


def assert_false(expr: bool) -> None:
    """
    Assert if an expression is False.

    Parameters
    ----------
    expr: bool
        Any expression which can be reduced to a boolean (e.g. empty list, operator).
    """
    if expr:
        raise AssertionError(f"expression {expr} is not False")


def assert_raises(action: Callable, expected: Type[Exception],
                  args: Optional[tuple] = None, kwargs: Optional[dict] = None) -> None:
    """
    Assert if executing a callable raises an error.

    Parameters
    ----------
    action: Callable
        Any callable object to be executed.
    expected: Type[Exception]
        Expected error to be raised.
    args: Optional[tuple]
        Arguments for the callable, if any.
    kwargs: Optional[dict]
        Keyword arguments for the callable, if any.
    """
    args = () if args is None else args
    kwargs = {} if kwargs is None else kwargs

    try:
        action(*args, **kwargs)
        message = "no error is raised"

    except Exception as error:
        if not isinstance(error, expected):
            message = f"raised error is {error.__class__.__name__}: {error}"
        else:
            return

    raise AssertionError(message)
