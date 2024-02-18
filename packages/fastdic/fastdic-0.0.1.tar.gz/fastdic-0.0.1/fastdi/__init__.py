#!/usr/bin/env python3
"""FastDI - Fast & Simple Dependency Injection Container.

This module contains the following classes:

    - FastDI - Dependency Injection Container

Base usage examples (default functionaloty):

    >>> from fastdi import di
    >>> from dataclasses import dataclass
    >>>
    >>>
    >>> @dataclass
    ... class MyType1:
    ...     field: int
    >>>
    >>>
    >>> @dataclass
    ... class MyType2:
    ...     field: str
    >>>
    >>> @dataclass
    ... class MyType3:
    ...     field: bool
    >>>
    >>>
    >>> @di.inject                  # `@di.inject` is supposed to automatically resolve and inject all the dependencies `my_func` expects
    ... def my_func(a: MyType1, b: MyType2) -> None:
    ...     print(a, b)
    >>>
    >>>
    >>> def my_func2(c: MyType2, d: MyType3) -> None:
    ...     print(c, d)
    >>>
    >>>
    >>> @di.provider(my_func)       # `my_func` is the function that needs such dependency `MyType1()`
    ... def my_type1_provider() -> MyType1:
    ...     return MyType1(field=1)
    >>>
    >>>
    >>> @di.provider(my_func)       # `my_func` and `my_func2` are the functions which need such dependency `MyType2()` at the same time
    ... @di.provider(my_func2)
    ... def my_type2_provider() -> MyType2:
    ...     return MyType2(field="a")
    ...
    >>> @di.provider(my_func2)
    ... def my_type3_provider() -> MyType3:
    ...     return MyType3(field=True)
    ...
    >>>
    >>>
    >>> my_func()                   # if no arguments passed - all dependencies will be resolved and injected
    ...                             # automatically if the corresponding providers were registered via `@di.provider`
    <MyType1(field=1)> <MyType2(field="a")>
    >>>
    >>> my_func(a=MyType1(field=2)) # same, but with one kwarg is passed
    <MyType1(field=2)> <MyType2(field="a")>
    >>>
    >>> di.inject(my_func2)()       # same here, but w/o syntactic sugar (@)
    <MyType2(field="a")> <MyType3(field=True)>
    >>>
    >>> di.inject(my_func2)(c=MyType2(field="b"))   # same, but one kwarg is passed
    <MyType2(field="b")> <MyType3(field=True)>

By default, `di` object should be imported from the module if basic functionality is enough, but if you need to customize
the process of dependency injection - it's allowed to import class `FastDI` and instantiate it manually with a custom
config.
"""

from ._container import FastDI

__all__ = ["di", "FastDI"]

di = FastDI()
