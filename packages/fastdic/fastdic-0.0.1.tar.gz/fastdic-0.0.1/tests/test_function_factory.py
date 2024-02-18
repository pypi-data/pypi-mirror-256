import inspect
from typing import Any, Callable

import pytest

from .function_factory import Arg, Kwarg, function_factory


@pytest.mark.parametrize(
    "f_name, args, kwargs, return_type, body, is_async",
    [
        # single arg with type int, single kwarg with type str and default value
        (
            "target_function",
            [
                Arg(
                    name="a",
                    type_hint=int,
                )
            ],
            [
                Kwarg(
                    name="b",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                )
            ],
            tuple,
            "return a, b",
            False,
        ),
        # multiple args with type int, single kwarg with type str and default value
        (
            "target_function",
            [
                Arg(
                    name="a",
                    type_hint=int,
                ),
                Arg(
                    name="b",
                    type_hint=int,
                ),
            ],
            [
                Kwarg(
                    name="c",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                )
            ],
            tuple,
            "return a, b, c",
            False,
        ),
        # single arg with type int, multiple kwargs with type str and default value
        (
            "target_function",
            [
                Arg(
                    name="a",
                    type_hint=int,
                )
            ],
            [
                Kwarg(
                    name="b",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
                Kwarg(
                    name="c",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
            ],
            tuple,
            "return a, b, c",
            False,
        ),
        # multiple args with type int, multiple kwargs with type str and default value
        (
            "target_function",
            [
                Arg(
                    name="a",
                    type_hint=int,
                ),
                Arg(
                    name="b",
                    type_hint=int,
                ),
            ],
            [
                Kwarg(
                    name="c",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
                Kwarg(
                    name="d",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
            ],
            tuple,
            "return a, b, c, d",
            False,
        ),
        # multiple args with mixed types, multiple kwargs with mixed types and default value
        (
            "target_function",
            [
                Arg(
                    name="a",
                    type_hint=int,
                ),
                Arg(
                    name="b",
                    type_hint=str,
                ),
            ],
            [
                Kwarg(
                    name="c",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
                Kwarg(
                    name="d",
                    type_hint=int,
                    has_default=True,
                    default_value=0,
                ),
            ],
            tuple,
            "return a, b, c, d",
            False,
        ),
        # single arg with type int, single kwarg with type str and default value, async function
        (
            "target_function",
            [
                Arg(
                    name="a",
                    type_hint=int,
                )
            ],
            [
                Kwarg(
                    name="b",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                )
            ],
            tuple,
            "return a, b",
            True,
        ),
        # multiple args with type int, single kwarg with type str and default value, async function
        (
            "target_function",
            [
                Arg(
                    name="a",
                    type_hint=int,
                ),
                Arg(
                    name="b",
                    type_hint=int,
                ),
            ],
            [
                Kwarg(
                    name="c",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                )
            ],
            tuple,
            "return a, b, c",
            True,
        ),
        # single arg with type int, multiple kwargs with type str and default value, async function
        (
            "target_function",
            [
                Arg(
                    name="a",
                    type_hint=int,
                )
            ],
            [
                Kwarg(
                    name="b",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
                Kwarg(
                    name="c",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
            ],
            tuple,
            "return a, b, c",
            True,
        ),
        # multiple args with mixed types, multiple kwargs with mixed types and default value, async function
        (
            "target_function",
            [
                Arg(
                    name="a",
                    type_hint=int,
                ),
                Arg(
                    name="b",
                    type_hint=str,
                ),
            ],
            [
                Kwarg(
                    name="c",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
                Kwarg(
                    name="d",
                    type_hint=int,
                    has_default=True,
                    default_value=0,
                ),
            ],
            tuple,
            "return a, b, c, d",
            True,
        ),
        # no args, one kwarg with default value
        (
            "target_function",
            [],
            [
                Kwarg(
                    name="a",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                )
            ],
            tuple,
            "return a",
            False,
        ),
        # no args, multiple kwargs with default value
        (
            "target_function",
            [],
            [
                Kwarg(
                    name="a",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
                Kwarg(
                    name="b",
                    type_hint=int,
                    has_default=True,
                    default_value=0,
                ),
            ],
            tuple,
            "return a, b",
            False,
        ),
        # no args, one kwarg with default value, async function
        (
            "target_function",
            [],
            [
                Kwarg(
                    name="a",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                )
            ],
            tuple,
            "return a",
            True,
        ),
        # one arg, no kwargs
        (
            "target_function",
            [Arg(name="a", type_hint=int)],
            [],
            tuple,
            "return a",
            False,
        ),
        # one arg, no kwargs, async function
        (
            "target_function",
            [Arg(name="a", type_hint=int)],
            [],
            tuple,
            "return a",
            True,
        ),
        # no args, no kwargs
        (
            "target_function",
            [],
            [],
            tuple,
            "return",
            False,
        ),
        # no args, no kwargs, async function
        (
            "target_function",
            [],
            [],
            tuple,
            "return",
            True,
        ),
        # 2 args without type hints, 2 kwargs with type hints and default values
        (
            "target_function",
            [Arg(name="a"), Arg(name="b")],
            [
                Kwarg(
                    name="c",
                    type_hint=str,
                    has_default=True,
                    default_value="default_value",
                ),
                Kwarg(
                    name="d",
                    type_hint=int,
                    has_default=True,
                    default_value=0,
                ),
            ],
            tuple,
            "return a, b, c, d",
            False,
        ),
        # 2 args with type hints, 2 kwargs without type hints
        (
            "target_function",
            [Arg(name="a", type_hint=int), Arg(name="b", type_hint=str)],
            [Kwarg(name="c"), Kwarg(name="d")],
            tuple,
            "return a, b, c, d",
            False,
        ),
        # 2 args without type hints, 2 kwargs without type hints
        (
            "target_function",
            [Arg(name="a"), Arg(name="b")],
            [Kwarg(name="c"), Kwarg(name="d")],
            tuple,
            "return a, b, c, d",
            False,
        ),
        # 2 args without type hints, 2 kwargs without type hints. no return type hint
        (
            "target_function",
            [Arg(name="a"), Arg(name="b")],
            [Kwarg(name="c"), Kwarg(name="d")],
            "",
            "return a, b, c, d",
            False,
        ),
    ],
)
def test_function_factory_valid_parameters(
    f_name: str,
    args: list[Arg],
    kwargs: list[Kwarg],
    return_type: type | None,
    body: str,
    is_async: bool,
) -> None:
    f: Callable = function_factory(
        f_name,
        args=args,
        kwargs=kwargs,
        return_type=return_type,
        body=body,
        is_async=is_async,
    )

    assert isinstance(f, Callable)  # type: ignore
    assert f.__name__ == f_name
    assert "return" in f.__function_str__  # type: ignore
    assert f.__all_args__ == args  # type: ignore
    assert f.__all_kwargs__ == kwargs  # type: ignore

    for arg in args:
        arg: Arg  # type: ignore
        if arg.type_hint:
            assert arg.name in f.__annotations__
            assert f.__annotations__[arg.name] == arg.type_hint
        else:
            assert arg.name not in f.__annotations__

    for kwarg in kwargs:
        kwarg: Kwarg  # type: ignore
        if kwarg.type_hint:
            assert kwarg.name in f.__annotations__
            assert f.__annotations__[kwarg.name] == kwarg.type_hint
        else:
            assert kwarg.name not in f.__annotations__

    if return_type != "":
        assert f.__annotations__["return"] == return_type
    else:
        assert "return" not in f.__annotations__

    assert inspect.iscoroutinefunction(f) == is_async


@pytest.mark.parametrize(
    "has_default,type_hint,default_value",
    [
        (True, str, "default_value"),
        (True, int, 0),
        (True, float, 0.0),
        (True, bool, True),
        (True, bool, False),
        (False, str, "default_value"),
        (False, int, 0),
        (False, float, 0.0),
        (False, bool, True),
        (False, bool, False),
    ],
)
def test_produced_function_call(
    has_default: bool, type_hint: type, default_value: Any
) -> None:
    f: Callable = function_factory(
        "target_function",
        args=[Arg(name="a", type_hint=int)],
        kwargs=[
            Kwarg(
                name="b",
                type_hint=type_hint,
                has_default=has_default,
                default_value=default_value,
            )
        ],
        return_type=tuple,
        body="return a, b",
        is_async=False,
    )

    assert f(1) == (1, default_value) if has_default else (1,)
    assert f(1, "value") == (1, "value")
    assert f(a=1) == (1, default_value) if has_default else (1,)
    assert f(a=1, b="value") == (1, "value")
    assert f(b="value", a=1) == (1, "value")
    assert f(1, b="value") == (1, "value")
