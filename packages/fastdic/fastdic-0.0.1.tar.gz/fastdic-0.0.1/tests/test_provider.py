from typing import Any, Callable, Type

import pytest

from fastdi import FastDI
from fastdi._container import ProviderContainer, ProviderError


@pytest.mark.parametrize(
    "syntactic_sugar,kwarg_name,dependency_value,dependency_type_hint",
    [
        (True, None, 41, int),
        (True, "a", 42, int),
        (False, None, 43, int),
        (False, "b", 44, int),
    ],
)
def test_provider_decorator_in_valid_cases(
    di: FastDI,
    syntactic_sugar: bool,
    kwarg_name: str | None,
    dependency_value: int,
    dependency_type_hint: type,
) -> None:
    """
    Test provider decorator method. It should add target function to `self._dependencies_registry` default dict field
    of the FastDI instance.

    Args:
        di: FastDI instance fixture
        syntactic_sugar: Whether to use syntactic sugar or not
        kwarg_name: Keyword argument name
        dependency_value: Dependency value
        dependency_type_hint: Dependency type hint

    Returns: None

    """

    def target_function(a: int) -> None:
        print(a)

    if syntactic_sugar is True:

        @di.provider(target_function, kwarg_name=kwarg_name)
        def dependency_provider_function() -> dependency_type_hint:  # type: ignore
            return dependency_value

    else:

        def dependency_provider_function() -> int:
            return dependency_value

        di.provider(target_function, kwarg_name=kwarg_name)(
            dependency_provider_function
        )

    assert target_function in di._dependencies_registry
    assert len(di._dependencies_registry) == 1
    assert len(di._dependencies_registry[target_function]) == 1
    assert isinstance(
        list(di._dependencies_registry[target_function])[0], ProviderContainer
    )
    assert isinstance(
        list(di._dependencies_registry[target_function])[0].provider_function, Callable  # type: ignore
    )
    assert (
        list(di._dependencies_registry[target_function])[0].provider_function()
        == dependency_value
    )
    assert isinstance(
        list(di._dependencies_registry[target_function])[0].kwarg_name, type(kwarg_name)
    )
    assert list(di._dependencies_registry[target_function])[0].kwarg_name == kwarg_name


@pytest.mark.parametrize(
    "syntactic_sugar,target_function,kwarg_name,expected_exception",
    [
        (True, None, "a", ProviderError),
        (True, lambda x: x, 1, ProviderError),
        (True, None, 1, ProviderError),
        (True, "None", "a", ProviderError),
        (True, lambda x: x, list, ProviderError),
        (True, "None", list, ProviderError),
        (False, None, "a", ProviderError),
        (False, lambda x: x, 1, ProviderError),
        (False, None, 1, ProviderError),
        (False, "None", "a", ProviderError),
        (False, lambda x: x, list, ProviderError),
        (False, "None", list, ProviderError),
    ],
)
def test_provider_decorator_in_invalid_cases(
    di: FastDI,
    syntactic_sugar: bool,
    target_function: Any,
    kwarg_name: Any,
    expected_exception: Type[Exception],
) -> None:
    """
    Test provider decorator method with invalid cases. It should raise a TypeError exception.

    Args:
        di: FastDI instance fixture
        syntactic_sugar: Whether to use syntactic sugar or not
        target_function: some object that is not a function
        kwarg_name: some object that is not a string
        expected_exception: Expected exception decorator should raise

    Returns: None

    """
    if syntactic_sugar is True:

        with pytest.raises(expected_exception):

            @di.provider(target_function, kwarg_name=kwarg_name)
            def dependency_provider_function() -> int:
                return 1

    else:

        def dependency_provider_function() -> int:
            return 1

        with pytest.raises(expected_exception):
            di.provider(target_function, kwarg_name=kwarg_name)(
                dependency_provider_function
            )
