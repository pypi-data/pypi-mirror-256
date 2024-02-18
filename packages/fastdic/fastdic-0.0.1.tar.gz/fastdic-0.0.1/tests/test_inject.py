from typing import Any, Callable, Type

import pytest

from fastdi import FastDI
from fastdi._container import InjectorError, ProviderError

from .function_factory import Arg, Kwarg, function_factory


@pytest.mark.parametrize(
    "kwarg_name,dependency_value,dependency_type_hint",
    [
        ("a", 42, int),
        ("a", -42, int),
        ("a", 0, int),
        (None, 43, int),
        (None, -43, int),
        (None, 0, int),
    ],
)
def test_inject_with_provider_in_valid_cases_single_argument(
    di: FastDI,
    kwarg_name: str | None,
    dependency_value: int,
    dependency_type_hint: type,
) -> None:
    """
    Test inject method with provider decorator. It should inject the target function with the dependency value.

    Args:
        di: FastDI instance fixture
        kwarg_name: name of the keyword argument
        dependency_value: value of the dependency
        dependency_type_hint: type hint of the dependency

    Returns: None

    """

    @di.inject
    def target_function(a: int) -> int:
        return a

    @di.provider(target_function, kwarg_name=kwarg_name)
    def provider_function() -> dependency_type_hint:  # type: ignore
        return dependency_value

    assert target_function() == dependency_value
    assert target_function() == dependency_value
    assert target_function(1) == 1
    assert target_function(1) == 1
    assert target_function(a=1) == 1
    assert target_function(a=1) == 1
    assert target_function() == dependency_value
    assert target_function() == dependency_value


@pytest.mark.parametrize(
    "kwarg_name,dependency_value,dependency_type_hint,custom_value",
    [
        ("a", "42", str, "42"),
        ("a", None, None, None),
        ("a", True, bool, True),
        ("a", list(), list, list()),
        ("a", dict(), dict, dict()),
        ("a", tuple(), tuple, tuple()),
        (None, "42", str, "42"),
        (None, None, None, None),
        (None, True, bool, True),
        (None, list(), list, list()),
        (None, dict(), dict, dict()),
        (None, tuple(), tuple, tuple()),
        ("b", "42", str, "42"),
        ("b", None, None, None),
        ("b", True, bool, True),
        ("b", list(), list, list()),
        ("b", dict(), dict, dict()),
        ("b", tuple(), tuple, tuple()),
    ],
)
def test_inject_with_provider_in_invalid_cases_single_argument(
    di: FastDI,
    kwarg_name: str | None,
    dependency_value: Any,
    dependency_type_hint: Any,
    custom_value: Any,
) -> None:
    """
    Test inject method with provider decorator. It should raise TypeError when the target function is called with
    invalid arguments.

    Args:
        di: FastDI instance fixture
        kwarg_name: name of the keyword argument
        dependency_value: value of the dependency
        dependency_type_hint: type hint of the dependency
        custom_value: custom value

    Returns: None

    """

    @di.inject
    def target_function(a: int) -> int:
        return a

    @di.provider(target_function, kwarg_name=kwarg_name)
    def provider_function() -> dependency_type_hint:
        return dependency_value

    with pytest.raises(InjectorError):
        target_function()

    with pytest.raises(InjectorError):
        target_function(custom_value)

    with pytest.raises(InjectorError):
        target_function(a=custom_value)

    with pytest.raises(InjectorError):
        target_function(aa=custom_value)

    with pytest.raises(InjectorError):
        target_function(custom_value, custom_value)

    with pytest.raises(InjectorError):
        target_function(custom_value, a=custom_value)

    with pytest.raises(InjectorError):
        target_function(custom_value, aa=custom_value)

    with pytest.raises(InjectorError):
        target_function(aa=custom_value, bb=custom_value)

    with pytest.raises(InjectorError):
        target_function(custom_value, aa=custom_value, bb=custom_value)


@pytest.mark.parametrize(
    "target_function,provider_functions",
    [
        # target_function - one positional arg, one keyword arg with default value;
        # provider_functions - one function that returns object with type of positional arg from target function,
        # and another function that returns object with type of keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[Arg(name="a", type_hint=int)],
                kwargs=[
                    Kwarg(
                        name="b",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value",
                    )
                ],
                return_type=tuple,
                body="return a,b",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
            ],
        ),
        # target_function - one positional arg, one keyword arg without default value;
        # provider_functions - one function that returns object with type of positional arg from target function,
        # and another function that returns object with type of keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[Arg(name="a", type_hint=int)],
                kwargs=[Kwarg(name="b", type_hint=str)],
                return_type=tuple,
                body="return a,b",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
            ],
        ),
        # target_function - two positional args, one keyword arg with default value;
        # provider_functions - one function that returns object with type of first positional arg from target function,
        # and another function that returns object with type of second positional arg from target function,
        # and another function that returns object with type of keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                ],
                kwargs=[
                    Kwarg(
                        name="c",
                        type_hint=bool,
                        has_default=True,
                        default_value=True,
                    )
                ],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
        ),
        # target_function - two positional args, one keyword arg without default value;
        # provider_functions - one function that returns object with type of first positional arg from target function,
        # and another function that returns object with type of second positional arg from target function,
        # and another function that returns object with type of keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                ],
                kwargs=[Kwarg(name="c", type_hint=bool)],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
        ),
        # target_function - one positional args, two keyword args with default value;
        # provider_functions - one function that returns object with type of positional arg from target function,
        # and another function that returns object with type of first keyword arg from target function,
        # and another function that returns object with type of second keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[Arg(name="a", type_hint=int)],
                kwargs=[
                    Kwarg(
                        name="b",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value",
                    ),
                    Kwarg(
                        name="c",
                        type_hint=bool,
                        has_default=True,
                        default_value=True,
                    ),
                ],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
        ),
        # target_function - one positional args, two keyword args without default value;
        # provider_functions - one function that returns object with type of positional arg from target function,
        # and another function that returns object with type of first keyword arg from target function,
        # and another function that returns object with type of second keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[Arg(name="a", type_hint=int)],
                kwargs=[
                    Kwarg(name="b", type_hint=str),
                    Kwarg(name="c", type_hint=bool),
                ],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
        ),
        # target_function - two positional args, two keyword args with default value;
        # provider_functions - one function that returns object with type of first positional arg from target function,
        # and another function that returns object with type of second positional arg from target function,
        # and another function that returns object with type of first keyword arg from target function,
        # and another function that returns object with type of second keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                ],
                kwargs=[
                    Kwarg(
                        name="c",
                        type_hint=bool,
                        has_default=True,
                        default_value=True,
                    ),
                    Kwarg(
                        name="d",
                        type_hint=list,
                        has_default=True,
                        default_value=[1, 2, 3],
                    ),
                ],
                return_type=tuple,
                body="return a,b,c,d",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type=list,
                    body="return [1, 2, 3]",
                    is_async=False,
                ),
            ],
        ),
        # target_function - two positional args, two keyword args without default value;
        # provider_functions - one function that returns object with type of first positional arg from target function,
        # and another function that returns object with type of second positional arg from target function,
        # and another function that returns object with type of first keyword arg from target function,
        # and another function that returns object with type of second keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                ],
                kwargs=[
                    Kwarg(name="c", type_hint=bool),
                    Kwarg(name="d", type_hint=list),
                ],
                return_type=tuple,
                body="return a,b,c,d",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type=list,
                    body="return [1, 2, 3]",
                    is_async=False,
                ),
            ],
        ),
    ],
)
def test_inject_with_provider_in_valid_cases_multiple_arguments(
    di: FastDI, target_function: Callable, provider_functions: list[Callable]
) -> None:
    target_function: Callable = di.inject(target_function)  # type: ignore

    for provider_function in provider_functions:
        di.provider(target_function)(provider_function)

    # call w/o passing any arguments
    assert target_function() == tuple(
        provider_function() for provider_function in provider_functions
    )

    # call w/ passing kwargs based on function annotation
    kwarg_to_be_passed = {
        arg: provider_function()
        for arg, provider_function in zip(
            target_function.__annotations__.keys(), provider_functions
        )
    }
    assert target_function(**kwarg_to_be_passed) == tuple(
        provider_function() for provider_function in provider_functions
    )


@pytest.mark.parametrize(
    (
        "target_function,"
        "provider_functions,"
        "expected_exception_during_provider_registering,"
        "expected_exception_during_inject_applying,"
        "expected_exception_during_target_function_call,"
        "case_is_valid"
    ),
    [
        # INVALID CASE
        # target_function - two positional args with the same type, one keyword arg with another type and default value;
        # provider_functions - one function that returns object with type of positional arg from target function,
        # and another function that returns object with type of keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[Arg(name="a", type_hint=int), Arg(name="b", type_hint=int)],
                kwargs=[
                    Kwarg(
                        name="c",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value",
                    )
                ],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            InjectorError,
            False,
        ),
        # INVALID CASE
        # target_function - two positional args with the same type, one keyword arg with another type and without
        # default value; provider_functions - one function that returns object with type of positional arg from target
        # function, and another function that returns object with type of keyword arg from target function
        (
            function_factory(
                "target_function",
                args=[Arg(name="a", type_hint=int), Arg(name="b", type_hint=int)],
                kwargs=[Kwarg(name="c", type_hint=str)],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            InjectorError,
            False,
        ),
        # INVALID CASE
        # target_function - one positional arg with int type, two keyword args with str type both and both with default
        # values; provider_functions - one function that returns object with type of positional arg from target
        # function, and another function that returns object with type of keyword args from target function
        (
            function_factory(
                "target_function",
                args=[Arg(name="a", type_hint=int)],
                kwargs=[
                    Kwarg(
                        name="b",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value1",
                    ),
                    Kwarg(
                        name="c",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value2",
                    ),
                ],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            InjectorError,
            False,
        ),
        # INVALID CASE
        # target_function - one positional arg with int type, two keyword args with str type both and both without
        # default values; provider_functions - one function that returns object with type of positional arg from target
        # function, and another function that returns object with type of keyword args from target function
        (
            function_factory(
                "target_function",
                args=[Arg(name="a", type_hint=int)],
                kwargs=[Kwarg(name="b", type_hint=str), Kwarg(name="c", type_hint=str)],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            InjectorError,
            False,
        ),
        # INVALID CASE
        # target_function - 3 positional args with int type, 3 keyword args with str type, and all with default
        # values; provider_functions - one function that returns object with type of positional arg from target
        # function, and another function that returns object with type of keyword args from target function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=int),
                    Arg(name="c", type_hint=int),
                ],
                kwargs=[
                    Kwarg(
                        name="d",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value1",
                    ),
                    Kwarg(
                        name="e",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value2",
                    ),
                    Kwarg(
                        name="f",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value3",
                    ),
                ],
                return_type=tuple,
                body="return a,b,c,d,e,f",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            InjectorError,
            False,
        ),
        # INVALID CASE
        # target_function - 3 positional args with int type, 3 keyword args with str type, and all without default
        # values; provider_functions - one function that returns object with type of positional arg from target
        # function, and another function that returns object with type of keyword args from target function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=int),
                    Arg(name="c", type_hint=int),
                ],
                kwargs=[
                    Kwarg(name="d", type_hint=str),
                    Kwarg(name="e", type_hint=str),
                    Kwarg(name="f", type_hint=str),
                ],
                return_type=tuple,
                body="return a,b,c,d,e,f",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            InjectorError,
            False,
        ),
        # INVALID CASE
        # target_function - 3 positional args with different types, 3 keyword args with mixed types too and with default
        # values; provider_functions - 6 functions that returns object with type of all args and kwargs from target
        # function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                    Arg(name="c", type_hint=bool),
                ],
                kwargs=[
                    Kwarg(
                        name="d",
                        type_hint=int,
                        has_default=True,
                        default_value=1,
                    ),
                    Kwarg(
                        name="e",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value",
                    ),
                    Kwarg(
                        name="f",
                        type_hint=bool,
                        has_default=True,
                        default_value=True,
                    ),
                ],
                return_type=tuple,
                body="return a,b,c,d,e,f",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_5",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_6",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            InjectorError,
            False,
        ),
        # INVALID CASE
        # target_function - 3 positional args with different types, 3 keyword args with mixed types too and without
        # default values; provider_functions - 6 functions that returns object with type of all args and kwargs from
        # target function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                    Arg(name="c", type_hint=bool),
                ],
                kwargs=[
                    Kwarg(name="d", type_hint=int),
                    Kwarg(name="e", type_hint=str),
                    Kwarg(name="f", type_hint=bool),
                ],
                return_type=tuple,
                body="return a,b,c,d,e,f",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_5",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_6",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            InjectorError,
            False,
        ),
        # VALID CASE
        # target_function - 3 positional args with different types, 3 keyword args with mixed types too and with default
        # values; provider_functions - 6 functions that returns object with type of all args and kwargs from target
        # function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                    Arg(name="c", type_hint=bool),
                ],
                kwargs=[
                    Kwarg(
                        name="d",
                        type_hint=int,
                        has_default=True,
                        default_value=1,
                    ),
                    Kwarg(
                        name="e",
                        type_hint=str,
                        has_default=True,
                        default_value="default_value",
                    ),
                    Kwarg(
                        name="f",
                        type_hint=bool,
                        has_default=True,
                        default_value=True,
                    ),
                ],
                return_type=tuple,
                body="return a,b,c,d,e,f",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_5",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_6",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
            None,
            None,
            None,
            True,
        ),
        # VALID CASE
        # target_function - 3 positional args with different types, 3 keyword args with mixed types too and without
        # default values; provider_functions - 6 functions that returns object with type of all args and kwargs from
        # target function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                    Arg(name="c", type_hint=bool),
                ],
                kwargs=[
                    Kwarg(name="d", type_hint=int),
                    Kwarg(name="e", type_hint=str),
                    Kwarg(name="f", type_hint=bool),
                ],
                return_type=tuple,
                body="return a,b,c,d,e,f",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_5",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_6",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
            None,
            None,
            None,
            True,
        ),
        # VALID CASE
        # target_function - 3 positional args with different types, 0 keyword args; provider_functions - 3 functions
        # that return object with type of all args from target function
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                    Arg(name="c", type_hint=bool),
                ],
                kwargs=[],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
            None,
            None,
            None,
            True,
        ),
        # VALID CASE
        # target_function - 0 positional args, 3 keyword args  with different types; provider_functions - 3 functions
        # that return object with type of all keyword args from target function
        (
            function_factory(
                "target_function",
                args=[],
                kwargs=[
                    Kwarg(name="a", type_hint=int),
                    Kwarg(name="b", type_hint=str),
                    Kwarg(name="c", type_hint=bool),
                ],
                return_type=tuple,
                body="return a,b,c",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
            None,
            None,
            None,
            True,
        ),
        # INVALID CASE
        # target function - has 3 positional args and 3 keyword args with default values, but no type hint for any of
        # them; provider functions - 6 functions that return object with mixed types
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a"),
                    Arg(name="b"),
                    Arg(name="c"),
                ],
                kwargs=[
                    Kwarg(
                        name="d",
                        has_default=True,
                        default_value=1,
                    ),
                    Kwarg(
                        name="e",
                        has_default=True,
                        default_value="default_value",
                    ),
                    Kwarg(
                        name="f",
                        has_default=True,
                        default_value=True,
                    ),
                ],
                return_type=tuple,
                body="return a,b,c,d,e,f",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_5",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_6",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
            None,
            InjectorError,
            None,
            False,
        ),
        # INVALID CASE
        # target function - has 3 positional args and 3 keyword args with default values, but no type hint for any of
        # them as well as has no return type hint; provider functions - 6 functions that return object with mixed types
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a"),
                    Arg(name="b"),
                    Arg(name="c"),
                ],
                kwargs=[
                    Kwarg(
                        name="d",
                        has_default=True,
                        default_value=1,
                    ),
                    Kwarg(
                        name="e",
                        has_default=True,
                        default_value="default_value",
                    ),
                    Kwarg(
                        name="f",
                        has_default=True,
                        default_value=True,
                    ),
                ],
                return_type=None,
                body="return a,b,c,d,e,f",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type=int,
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_5",
                    args=[],
                    kwargs=[],
                    return_type=str,
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_6",
                    args=[],
                    kwargs=[],
                    return_type=bool,
                    body="return True",
                    is_async=False,
                ),
            ],
            None,
            InjectorError,
            None,
            False,
        ),
        # INVALID CASE
        # target function - has 2 positional args and 2 keyword args with default values with type hints specified;
        # provider functions - 4 functions without return type hint that return object with mixed types
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                ],
                kwargs=[
                    Kwarg(
                        name="c",
                        type_hint=bool,
                        has_default=True,
                        default_value=True,
                    ),
                    Kwarg(
                        name="d",
                        type_hint=float,
                        has_default=True,
                        default_value=1.0,
                    ),
                ],
                return_type=tuple,
                body="return a,b,c,d",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body="return 1.0",
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            None,
            False,
        ),
        # INVALID CASE
        # target function - has 2 positional args with type hints specified and 0 keyword args;
        # provider functions - 2 functions without return type hint that return object with mixed types
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a", type_hint=int),
                    Arg(name="b", type_hint=str),
                ],
                kwargs=[],
                return_type=tuple,
                body="return a,b",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body='return "string"',
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            None,
            False,
        ),
        # INVALID CASE
        # target function - has 2 key word args with type hints specified and 0 positional args;
        # provider functions - 2 functions without return type hint that return object with mixed types
        (
            function_factory(
                "target_function",
                args=[],
                kwargs=[
                    Kwarg(name="a", type_hint=int),
                    Kwarg(name="b", type_hint=str),
                ],
                return_type=tuple,
                body="return a,b",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body='return "string"',
                    is_async=False,
                ),
            ],
            ProviderError,
            None,
            None,
            False,
        ),
        # INVALID CASE
        # target function - has 2 positional args and 2 keyword args with default values and all without type hints
        # specified; provider functions - 4 functions without return type hint that return object with mixed types
        (
            function_factory(
                "target_function",
                args=[
                    Arg(name="a"),
                    Arg(name="b"),
                ],
                kwargs=[
                    Kwarg(
                        name="c",
                        has_default=True,
                        default_value=True,
                    ),
                    Kwarg(
                        name="d",
                        has_default=True,
                        default_value=1.0,
                    ),
                ],
                return_type=tuple,
                body="return a,b,c,d",
                is_async=False,
            ),
            [
                function_factory(
                    "provider_function_1",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body="return 1",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_2",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body='return "string"',
                    is_async=False,
                ),
                function_factory(
                    "provider_function_3",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body="return True",
                    is_async=False,
                ),
                function_factory(
                    "provider_function_4",
                    args=[],
                    kwargs=[],
                    return_type="",
                    body="return 1.0",
                    is_async=False,
                ),
            ],
            ProviderError,
            InjectorError,
            None,
            False,
        ),
    ],
)
def test_inject_with_provider_with_multiple_arguments_for_valid_and_invalid_cases(
    di: FastDI,
    target_function: Callable,
    provider_functions: list[Callable],
    expected_exception_during_provider_registering: Type[Exception] | None,
    expected_exception_during_inject_applying: Type[Exception] | None,
    expected_exception_during_target_function_call: Type[Exception] | None,
    case_is_valid: bool,
) -> None:
    if case_is_valid is True:
        # for valid cases, we should not expect an exception during inject applying, as well as during provider
        # registering. Also, the result of the target_function call should be equal to the tuple of results of provider
        # functions

        target_function = di.inject(target_function)

        all_expected_arguments = [
            *target_function.__all_args__,  # type: ignore
            *target_function.__all_kwargs__,  # type: ignore
        ]

        c = 0
        for provider_function in provider_functions:
            di.provider(target_function, kwarg_name=all_expected_arguments[c].name)(
                provider_function
            )
            c += 1

        assert target_function() == tuple(
            provider_function() for provider_function in provider_functions
        )

    else:
        # for invalid cases, we should expect an exception during inject applying, as well as during provider
        # registering, and during target function call
        if expected_exception_during_inject_applying is not None:
            with pytest.raises(expected_exception_during_inject_applying):
                target_function = di.inject(target_function)
        else:
            target_function = di.inject(target_function)

        if expected_exception_during_provider_registering:
            with pytest.raises(expected_exception_during_provider_registering):
                for provider_function in provider_functions:
                    di.provider(target_function)(provider_function)
        else:
            for provider_function in provider_functions:
                di.provider(target_function)(provider_function)

        # call the target function
        if expected_exception_during_target_function_call:
            with pytest.raises(expected_exception_during_target_function_call):
                target_function()
