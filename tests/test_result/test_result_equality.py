# -*- coding: utf-8 -*-

import pytest

from returns.primitives.container import (
    Bindable,
    Fixable,
    Mappable,
    Rescueable,
    Unwrapable,
    UnwrapableFailure,
)
from returns.primitives.exceptions import ImmutableStateError
from returns.result import Failure, Success


@pytest.mark.parametrize('container', [
    Failure(1),
    Success(1),
])
@pytest.mark.parametrize('protocol', [
    Bindable,
    Mappable,
    Fixable,
    Rescueable,
    Unwrapable,
    UnwrapableFailure,
])
def test_protocols(container, protocol):
    """Ensures that Result has all the right protocols."""
    assert isinstance(container, protocol)


def test_nonequality():
    """Ensures that containers are not compared to regular values."""
    input_value = 5

    assert Failure(input_value) != input_value
    assert Success(input_value) != input_value
    assert Failure(input_value) != Success(input_value)


def test_is_compare():
    """Ensures that `is` operator works correctly."""
    left = Failure(1)
    right = Success(1)

    assert left.bind(lambda state: state) is left
    assert right.rescue(lambda state: state) is right
    assert right is not Success(1)


def test_immutability_failure():
    """Ensures that Failure container is immutable."""
    with pytest.raises(ImmutableStateError):
        Failure(0)._inner_state = 1  # noqa: WPS437

    with pytest.raises(ImmutableStateError):
        Failure(1).missing = 2

    with pytest.raises(ImmutableStateError):
        del Failure(0)._inner_state  # type: ignore # noqa: WPS420, WPS437

    with pytest.raises(AttributeError):
        Failure(1).missing  # type: ignore # noqa: WPS428


def test_immutability_success():
    """Ensures that Success container is immutable."""
    with pytest.raises(ImmutableStateError):
        Success(0)._inner_state = 1  # noqa: WPS437

    with pytest.raises(ImmutableStateError):
        Success(1).missing = 2

    with pytest.raises(ImmutableStateError):
        del Success(0)._inner_state  # type: ignore # noqa: WPS420, WPS437

    with pytest.raises(AttributeError):
        Success(1).missing  # type: ignore # noqa: WPS428
