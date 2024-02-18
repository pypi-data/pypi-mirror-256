from collections import defaultdict
from typing import Any, Callable, Type
from unittest import mock

import pytest

from fastdi import FastDI
from fastdi._container import InjectorError, ProviderContainer, ProviderError

from .objects import (
    provider_func_int,
    provider_func_int_with_return_type_hint_any,
    provider_func_int_with_return_type_hint_union,
    provider_func_int_with_return_type_hint_union_new_style,
    provider_func_int_without_return_type_hint,
    target_func,
    target_func_bool,
    target_func_int,
    target_func_two_args_with_the_same_type,
    target_func_with_all_args_with_any_type_hint,
    target_func_with_all_args_with_union_type_hint_new_style,
    target_func_with_all_args_with_union_type_hint_old_style,
    target_func_with_first_arg_with_any_type_hint,
)


def test_fastdi_class_structure(di: FastDI) -> None:
    """
    Test FastDI class structure

    Args:
        di: FastDI instance fixture

    Returns: None

    """
    assert hasattr(di, "__slots__")
    assert not hasattr(di, "__dict__")
    assert hasattr(di, "__annotations__")
    assert hasattr(di, "_target_wrapper_registry")
    assert isinstance(di._target_wrapper_registry, dict)
    assert hasattr(di, "_dependencies_registry")
    assert isinstance(di._dependencies_registry, defaultdict)
    assert di._dependencies_registry.default_factory is set
    assert hasattr(di, "provider")
    assert isinstance(di.provider, Callable)  # type: ignore
    assert di.provider.__annotations__ == {
        "target_function": Callable[..., Any],
        "kwarg_name": str | None,
        "return": Callable[..., Any],
    }
    assert hasattr(di, "inject")
    assert isinstance(di.inject, Callable)  # type: ignore
    assert di.inject.__annotations__ == {
        "target_function": Callable[..., Any],
        "return": Callable[..., Any],
    }


def test_fastdi_provider_container_structure() -> None:
    """
    Test ProviderContainer class structure

    Returns: None

    """
    container = ProviderContainer(
        provider_function=lambda: None,
        kwarg_name=None,
    )

    assert hasattr(container, "__slots__")
    assert not hasattr(container, "__dict__")
    assert hasattr(container, "__annotations__")
    assert hasattr(container, "provider_function")
    assert isinstance(container.provider_function, Callable)  # type: ignore
    assert hasattr(container, "kwarg_name")
    assert container.kwarg_name in (str, None)
    assert container.__annotations__ == {
        "provider_function": Callable[..., Any],
        "kwarg_name": str | None,
    }


def test_fetch_dependency_provider_by_key_word_arg_name(di: FastDI) -> None:
    """
    Test FastDI._fetch_dependency_provider_by_key_word_arg_name method

    Returns: None

    """
    test_dependencies: list[ProviderContainer] = [
        ProviderContainer(
            provider_function=lambda: None,
            kwarg_name=f"kwarg_{i}",
        )
        for i in range(10)
    ]

    for provider_container in test_dependencies:
        assert (
            di._fetch_dependency_provider_by_key_word_arg_name(
                provider_container.kwarg_name, set(test_dependencies)  # type: ignore
            )
            == provider_container
        )

    assert (
        di._fetch_dependency_provider_by_key_word_arg_name(
            "nonexistent_kwarg", set(test_dependencies)
        )
        is None
    )


@pytest.mark.parametrize(
    "passed_args,passed_kwargs,function_annotations,expected_result",
    [
        # case 1: passed_args is not empty, passed_kwargs is empty
        ({int: 1}, {}, {"a": int, "b": str}, {"b": str}),
        # case 2:  passed_args is empty and passed_kwargs is not empty
        ({}, {"a": 1}, {"a": int, "b": str}, {"b": str}),
        # case 3: passed_args is not empty and passed_kwargs is not empty too
        ({int: 1}, {"a": 1}, {"a": int, "b": str}, {"b": str}),
        # case 4: both passed_args and passed_kwargs are empty
        ({}, {}, {"a": int, "b": str}, {"a": int, "b": str}),
    ],
)
def test_compose_deps_to_be_injected(
    di: FastDI,
    passed_args: dict[type, Any],
    passed_kwargs: dict[str, Any],
    function_annotations: dict[str, Any],
    expected_result: dict[str, Any],
) -> None:

    assert (
        di._compose_deps_to_be_injected(
            passed_args, passed_kwargs, function_annotations
        )
        == expected_result
    )


def test_fetch_dependency_provider_by_argument_type(di: FastDI) -> None:
    def test_provider() -> int:
        return 1

    test_dependencies: set[ProviderContainer] = {
        ProviderContainer(
            provider_function=test_provider,
            kwarg_name=f"kwarg_{i}",
        )
        for i in range(10)
    }

    assert (
        di._fetch_dependency_provider_by_argument_type(int, test_dependencies)
        == list(test_dependencies)[0]
    )
    assert (
        di._fetch_dependency_provider_by_argument_type(  # type: ignore
            int, test_dependencies
        ).provider_function()
        == 1
    )
    assert (
        di._fetch_dependency_provider_by_argument_type(float, test_dependencies) is None
    )
    assert (
        di._fetch_dependency_provider_by_argument_type(str, test_dependencies) is None
    )


def provider_int() -> int:
    return 1


def provider_str() -> str:
    return "a"


def provider_float() -> float:
    return 1.0


@pytest.mark.parametrize(
    "provider_by_arg_name,provider_by_arg_type,arg_name,arg_type,expected_result",
    [
        (
            ProviderContainer(provider_function=provider_int, kwarg_name="kwarg_int"),
            None,
            "kwarg_int",
            int,
            1,
        ),
        (
            None,
            ProviderContainer(provider_function=provider_int, kwarg_name="kwarg_int"),
            "kwarg_int",
            int,
            1,
        ),
        (
            ProviderContainer(provider_function=provider_str, kwarg_name="kwarg_str"),
            None,
            "kwarg_str",
            str,
            "a",
        ),
        (
            None,
            ProviderContainer(provider_function=provider_str, kwarg_name="kwarg_str"),
            "kwarg_str",
            str,
            "a",
        ),
        (
            None,
            None,
            "kwarg_int",
            int,
            InjectorError,
        ),
        (
            ProviderContainer(provider_function=provider_int, kwarg_name="kwarg_int"),
            ProviderContainer(provider_function=provider_int, kwarg_name="kwarg_int"),
            "kwarg_int",
            int,
            1,
        ),
    ],
)
def test_resolve_dependency(
    provider_by_arg_name: ProviderContainer,
    provider_by_arg_type: ProviderContainer,
    arg_name: str,
    arg_type: type,
    expected_result: Any | type,
) -> None:
    with (
        mock.patch.object(
            FastDI,
            "_fetch_dependency_provider_by_key_word_arg_name",
            return_value=provider_by_arg_name,
        ) as mock_fetch_dependency_provider_by_key_word_arg_name,
        mock.patch.object(
            FastDI,
            "_fetch_dependency_provider_by_argument_type",
            return_value=provider_by_arg_type,
        ) as mock_fetch_dependency_provider_by_argument_type,
    ):

        di = FastDI()

        if type(expected_result) is type and issubclass(expected_result, Exception):
            with pytest.raises(InjectorError):
                di._resolve_dependency(arg_name, arg_type, set())

        else:
            assert di._resolve_dependency(arg_name, arg_type, set()) == expected_result

        mock_fetch_dependency_provider_by_key_word_arg_name.assert_called_once()
        mock_fetch_dependency_provider_by_argument_type.assert_called_once()


@pytest.mark.parametrize(
    "passed_args,passed_kwargs,target_function,expected_result",
    [
        # case 1: passed_args and passed kwargs are empty both but target functon has annotations for them
        ({}, {}, target_func, InjectorError),
        # case 2: passed_args and passed kwargs are empty both and target function has no annotations for them
        ({}, {}, lambda: None, None),
        # case 3: passed_args is not empty and passed_kwargs is empty, but passed_args doesn't contain all the expected
        # arguments
        ({int: 1}, {}, target_func, InjectorError),
        # case 4: passed_args is empty and passed_kwargs is not empty, but passed_kwargs doesn't contain all the
        # expected arguments
        ({}, {"b": "b"}, target_func, InjectorError),
        # case 5: passed_args is not empty and passed_kwargs is not empty, but passed_args and passed_kwargs don't
        # contain all the expected arguments
        ({int: 1}, {"c": "c"}, target_func, InjectorError),
        # case 6: passed args and passed kwargs contain all the expected arguments
        ({int: 1}, {"b": "b"}, target_func, None),
        # case 7: passed args and passed kwargs contain all the expected arguments
        ({int: 1}, {"a": 1, "b": "b"}, target_func, None),
        # case 8: passed args is empty, by passed kwargs contains all the expected arguments
        ({}, {"a": 1, "b": "b"}, target_func, None),
        # case 9: passed args contain all the expected arguments, but passed kwargs is empty
        ({int: 1, str: "b"}, {}, target_func, None),
        # case 10: passed args and passed kwargs are not empty by they are not expected by the target function
        ({float: 1}, {"c": "c"}, lambda: None, InjectorError),
        # case 11: passed args is not empty, but it is not expected by the target function, passed kwargs is empty
        ({float: 1, bool: True}, {}, lambda: None, InjectorError),
        # case 12: passed args is empty but passed kwargs is not empty, and it is not expected by the target function
        ({}, {"c": "c", "d": "d"}, lambda: None, InjectorError),
        # case 13: passed args contains bool but expected type is int
        ({bool: True}, {}, target_func_int, InjectorError),
        # case 14: passed kwargs contains bool but expected type is int
        ({}, {"a": True}, target_func_int, InjectorError),
        # case 15: passed args contains int but expected type is bool
        ({int: 1}, {}, target_func_bool, InjectorError),
        # case 16: passed kwargs contains int but expected type is bool
        ({}, {"a": 1}, target_func_bool, InjectorError),
    ],
)
def test_validate_arguments(
    di: FastDI,
    passed_args: dict[type, Any],
    passed_kwargs: dict[str, Any],
    target_function: Callable,
    expected_result: Type[Exception],
) -> None:
    if type(expected_result) is type and issubclass(expected_result, Exception):
        with pytest.raises(expected_result):
            di._validate_arguments_for_target_function_call(
                passed_args, passed_kwargs, target_function
            )

    else:
        assert (
            di._validate_arguments_for_target_function_call(
                passed_args, passed_kwargs, target_function
            )
            is None
        )


@pytest.mark.parametrize(
    "passed_args,passed_kwargs,dependencies,target_function,expected_result",
    [
        # case 1: passed_args and passed_kwargs are empty both and no provider functions were registered for the target
        (
            {},
            {},
            set(),
            target_func,
            InjectorError,
        ),
        # case 2: passed args is not empty, passed kwargs is empty and no provider functions were registered for the
        # target
        (
            {int: 1},
            {},
            set(),
            target_func,
            None,
        ),
        # case 3: passed args is empty, passed kwargs is not empty and no provider functions were registered for the
        # target
        (
            {},
            {"b": "b"},
            set(),
            target_func,
            None,
        ),
        # case 4: passed args and passed kwargs are not empty and no provider functions were registered for the target
        (
            {int: 1},
            {"b": "b"},
            set(),
            target_func,
            None,
        ),
        # case 5: passed args and passed kwargs are empty both and provider functions were registered for the target
        (
            {},
            {},
            {
                ProviderContainer(
                    provider_function=lambda: None, kwarg_name="kwarg_name"
                )
            },
            target_func,
            None,
        ),
    ],
)
def test_validate_passed_arguments_and_registered_dependencies(
    di: FastDI,
    passed_args: dict[type, Any],
    passed_kwargs: dict[str, Any],
    dependencies: set[ProviderContainer],
    target_function: Callable,
    expected_result: Type[Exception],
) -> None:
    if type(expected_result) is type and issubclass(expected_result, Exception):
        with pytest.raises(expected_result):
            di._validate_passed_arguments(
                passed_args, passed_kwargs, dependencies, target_function
            )
    else:
        assert (
            di._validate_passed_arguments(
                passed_args, passed_kwargs, dependencies, target_function
            )
            is None
        )


@pytest.mark.parametrize(
    "kwarg_name,target_function,expected_result",
    [
        # case 1: passed target_function is not a callable
        ("kwarg_name", None, ProviderError),
        # case 2: passed kwarg_name is not a string or None
        (1, target_func, ProviderError),
        (1.0, target_func, ProviderError),
        (True, target_func, ProviderError),
        # case 3: passed kwarg_name is an empty string
        ("", target_func, ProviderError),
        # case 4: passed kwarg_name is a string or None
        ("kwarg_name", target_func, None),
        (None, target_func, None),
    ],
)
def test_validate_provider_before_decoration(
    di: FastDI, kwarg_name: Any, target_function: Any, expected_result: Type[Exception]
) -> None:

    if type(expected_result) is type and issubclass(expected_result, Exception):
        with pytest.raises(expected_result):
            di._validate_provider_before_decoration(kwarg_name, target_function)
    else:
        assert (
            di._validate_provider_before_decoration(kwarg_name, target_function) is None
        )


@pytest.mark.parametrize(
    "provider_function,kwarg_name,target_function,expected_result",
    [
        # case 1: provider function has no return type hint
        (
            provider_func_int_without_return_type_hint,
            "kwarg_name",
            target_func,
            ProviderError,
        ),
        # case 2: provider function has return type hint of type Any
        (
            provider_func_int_with_return_type_hint_any,
            "kwarg_name",
            target_func,
            ProviderError,
        ),
        # case 3: provider function has return type hint of type Union (old style)
        (
            provider_func_int_with_return_type_hint_union,
            "kwarg_name",
            target_func,
            ProviderError,
        ),
        # case 4: provider function has return type hint of type Union (new style)
        (
            provider_func_int_with_return_type_hint_union_new_style,
            "kwarg_name",
            target_func,
            ProviderError,
        ),
        # case 5: target function has multiple arguments with the same type,
        # and provider function was not decorated with kwarg_name, so it's not clear for which
        # argument provider function should be used, so we have conflict here
        (
            provider_func_int,
            None,
            target_func_two_args_with_the_same_type,
            ProviderError,
        ),
    ],
)
def test_validate_provider_during_decoration(
    di: FastDI,
    provider_function: Callable,
    kwarg_name: str | None,
    target_function: Callable,
    expected_result: Type[Exception],
) -> None:
    if type(expected_result) is type and issubclass(expected_result, Exception):
        with pytest.raises(expected_result):
            di._validate_provider_during_decoration(
                provider_function, kwarg_name, target_function
            )
    else:
        assert (
            di._validate_provider_during_decoration(
                provider_function, kwarg_name, target_function
            )
            is None
        )


@pytest.mark.parametrize(
    "target_function,expected_result",
    [
        # case 1: target function has no annotations for its arguments
        (lambda: None, InjectorError),
        # case 2: target function has type hint of type Any for all its arguments
        (target_func_with_all_args_with_any_type_hint, InjectorError),
        # case 2: target function has type hint of type Any for one of its arguments
        (target_func_with_first_arg_with_any_type_hint, InjectorError),
        # case 3 (old style of Union): target function has type hint of type Union for all its arguments
        (target_func_with_all_args_with_union_type_hint_old_style, InjectorError),
        # case 3 (new style of Union): target function has type hint of type Union for all its arguments
        (target_func_with_all_args_with_union_type_hint_new_style, InjectorError),
    ],
)
def test_validate_inject_before_decoration(
    di: FastDI, target_function: Callable, expected_result: Type[Exception]
) -> None:
    if type(expected_result) is type and issubclass(expected_result, Exception):
        with pytest.raises(expected_result):
            di._validate_inject_before_decoration(target_function)
    else:
        assert di._validate_inject_before_decoration(target_function) is None


def test_provider() -> None:
    with mock.patch.object(
        FastDI,
        "_validate_provider_before_decoration",
        return_value=None,
    ) as mock_validate_provider_before_decoration:
        with mock.patch.object(
            FastDI,
            "_validate_provider_during_decoration",
            return_value=None,
        ) as mock_validate_provider_during_decoration:
            di = FastDI()
            decorator = di.provider(target_func_int, "kwarg_name")
            wrapper = decorator(provider_func_int)
            assert wrapper() == 1
            mock_validate_provider_before_decoration.assert_called_once()
            mock_validate_provider_during_decoration.assert_called_once()
