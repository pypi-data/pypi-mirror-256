#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import wraps
from types import UnionType
from typing import Any, Callable, Union, get_origin

__all__ = ["FastDI"]


class DependencyInjectionError(Exception):
    """Base class for all dependency injection errors."""

    pass  # noqa: PIE790


class InjectorError(DependencyInjectionError):
    """Raised when an error occurs in the injector or during the injection process."""

    pass  # noqa: PIE790


class ProviderError(DependencyInjectionError):
    """Raised when an error occurs in the provider or during the provider registering process."""

    pass  # noqa: PIE790


@dataclass(slots=True, frozen=True, kw_only=True)
class ProviderContainer:
    """Provider dataclass is used to store provider function and kwarg name (if it was passed)."""

    provider_function: Callable[..., Any]
    kwarg_name: str | None


@dataclass(slots=True, kw_only=True)
class FastDI:
    """Fast and Simple Dependency Injection Container.

    How to use:

    1. Define a function (callable) that requires some dependencies to be injected (let's call it a "target" function).
    Use type hints to specify types of dependencies.

    Example:
    -------
        >>> def my_func(a: MyType) -> None:
        >>>    print(a)

    2. Define a function (callable) that will be used to provide concrete dependency objects (let's call it a "provider"
    function). Register provider for target using `di.provider` decorator. This decorator accepts reference to the
    target function as a parameter and should be assigned to the desired provider function. Provider function should
    return concrete object that's supposed to be injected into the target function.

    Example:
    -------
        >>> from fastdi import di
        >>>
        >>> @dataclass
        >>> class MyType:
        ...     field: int
        >>>
        >>> di.provider(my_func)
        >>> def my_type_provider() -> MyType:
        >>>     return MyType(field=1)

    3. Now it's time to inject dependencies into the target function. There are two ways to do it:

    3.1. Use `di.inject` decorator assigned to the target function via syntactic sugar (@).

    Example:
    -------
        >>> @di.inject
        >>> def my_func(a: MyType) -> None:
        >>>    print(a)

    Now, when you call `my_func()`, all dependencies, which were registered for `my_func` will be injected into
    it automatically.

    Example:
    -------
        >>> my_func()
        <MyType(field=1)>

    3.2 Use `di.inject` decorator directly, w/o syntactic sugar (@).

    Example:
    -------
        >>> def my_func_2(a: MyType) -> None:
        >>>    print(a)
        >>>
        >>> my_func_2 = di.inject(my_func_2)
        >>> my_func_2()
        <MyType(field=1)>

    This option - direct decorator usage w/o syntactic sugar - may be useful in the following cases:

        - when you need to inject dependencies into a function that's defined in a third-party library you don't
        control, or in code you control but don't want to change it.

        - when you use Clean Architecture (CA) approach, and you need to inject dependencies into a function
        that's defined in some inner layer (let's say "Use Cases" layer), so you are not allowed to import `di`
        from outer layers (let's say from "Application" or "Web" layer). But the opposite is allowed - you are
        allowed to import the desired function from some inner layer to outer layer. Thus, you can import `di`
        object into outer layer and use it to inject dependencies into the function that's imported from an
        inner layer. Example of CA:

        W    ------- Application (Web) layer -------       from use_cases.some_use_case import my_func
        |                                                  di.inject(my_func)(...)
        |       ---- Infrastructure layer ----
        |
        |          --- Use Cases layer ---                 def my_func(...): ...
        |
        V            -- Domain Model --

    """

    # map of target functions and their wrappers
    _target_wrapper_registry: dict[Callable, Callable] = field(default_factory=dict)

    # registry of providers and registered targets for them
    _dependencies_registry: defaultdict[Callable, set[ProviderContainer]] = field(
        default_factory=lambda: defaultdict(set)
    )

    @staticmethod
    def _fetch_dependency_provider_by_key_word_arg_name(
        kwarg_name: str, dependencies: set[ProviderContainer]
    ) -> ProviderContainer | None:
        """Fetch stored dependency provider function by kwarg name.

        Args:
        ----
            kwarg_name: name of kwarg for which dependency provider function should be fetched
            dependencies: list of stored provider containers for the target callable

        Returns: _ProviderContainer instance or None

        """

        # filter out all dicts from deps_for_target_func and check if kwarg_name is in any of them
        for provider_container in dependencies:
            if provider_container.kwarg_name == kwarg_name:
                return provider_container

        return None

    @staticmethod
    def _fetch_dependency_provider_by_argument_type(
        arg_type: type, dependencies: set[ProviderContainer]
    ) -> ProviderContainer | None:
        """Fetch stored dependency provider function by argument (arg or kwarg) type.

        Args:
        ----
            arg_type: type of argument for which dependency provider function should be fetched
            dependencies: list of stored dependency provider functions for the target callable

        Returns: _ProviderContainer instance or None

        """

        # filter out all callables from deps_for_target_func and check if arg_type is in any of them
        for provider_container in dependencies:
            provider_container: ProviderContainer  # type: ignore

            if (
                provider_container.provider_function.__annotations__.get("return")
                is arg_type
            ):
                return provider_container

        return None

    @staticmethod
    def _compose_deps_to_be_injected(  # noqa: C901
        passed_args: dict[type, Any],
        passed_kwargs: dict[str, Any],
        function_annotations: dict[str, type],
    ) -> dict[str, type]:
        """Compare passed arguments and function annotations.

        It compares passed arguments and fetches dependencies for those arguments values were not passed for.

        Args:
        ----
            passed_args: passed args dict {arg_type: arg_value, ...}
            passed_kwargs: passed kwargs dict {arg_name: arg_value, ...}
            function_annotations: function annotations dict {arg_name: arg_type, ...}

        Returns: dict of dependencies to be injected {arg_name: arg_type, ...}

        """
        dependencies: dict[str, type] = {}

        # case 1: passed_args is not empty, passed_kwargs is empty
        if passed_args and not passed_kwargs:
            for arg_name, arg_type in function_annotations.items():
                # if arg type not in passed_args - mark it as should be injected
                if arg_type not in passed_args:
                    dependencies[arg_name] = arg_type

        # case 2:  passed_args is empty and passed_kwargs is not empty
        elif not passed_args and passed_kwargs:
            for arg_name, arg_type in function_annotations.items():
                if arg_name not in passed_kwargs:
                    dependencies[arg_name] = arg_type
                else:
                    # check type of passed kwarg value
                    if not isinstance(passed_kwargs[arg_name], arg_type):
                        # wrong type of passed kwarg value, will override
                        dependencies[arg_name] = arg_type

        # case 3: passed_args is not empty and passed_kwargs is not empty too
        elif passed_args and passed_kwargs:
            for arg_name, arg_type in function_annotations.items():
                # check if arg name is in passed kwargs
                if arg_name not in passed_kwargs:
                    # check if arg type in passed args
                    if arg_type not in passed_args:
                        # this arg is absent
                        dependencies[arg_name] = arg_type
                else:
                    # check type of passed kwarg value
                    if not isinstance(passed_kwargs[arg_name], arg_type):
                        # wrong type of passed kwarg value, will override
                        dependencies[arg_name] = arg_type

        # case 4: both passed_args and passed_kwargs are empty
        else:
            dependencies = function_annotations

        return dependencies

    @staticmethod
    def _validate_inject_before_decoration(target_function: Callable) -> None:
        expected_arguments_names_and_types: dict[str, type] = dict(
            (k, v) for k, v in target_function.__annotations__.items() if k != "return"
        )

        # validate that target_function has annotations for all its arguments (positional and keyword)
        if not expected_arguments_names_and_types:
            raise InjectorError(
                "Target function must have annotations for all its arguments"
            )

        # validate that annotations for all arguments of target_function are not Any
        if Any in target_function.__annotations__.values():
            raise InjectorError("Target function annotations must not contain Any type")

        # validate that annotations for all arguments target_function are not Union
        for type_hint in target_function.__annotations__.values():
            if get_origin(type_hint) is Union or get_origin(type_hint) is UnionType:
                raise InjectorError(
                    "Target function annotations must not contain Union type"
                )

    @staticmethod
    def _validate_arguments_for_target_function_call(
        passed_args: dict[type, Any],
        passed_kwargs: dict[str, Any],
        target_function: Callable,
    ) -> None:
        # compose all expected arguments and their types from target function annotations
        expected_arguments_names_and_types: dict[str, type] = dict(
            (k, v) for k, v in target_function.__annotations__.items() if k != "return"
        )

        expected_argument_names: set = set(expected_arguments_names_and_types.keys())
        expected_argument_types: set = set(expected_arguments_names_and_types.values())
        all_expected_arguments: set = expected_argument_names | expected_argument_types

        # compose all passed arguments and their types
        passed_argument_names: set = set(passed_kwargs.keys())
        passed_argument_types: set = set(passed_args.keys()) | set(
            type(v) for k, v in passed_kwargs.items() if k != "return"
        )
        all_passed_arguments = passed_argument_names | passed_argument_types

        # validate passes arguments (args and kwargs) are not empty while target function has annotations for them
        if not all_passed_arguments and all_expected_arguments:
            raise InjectorError(
                "No arguments were passed for the target function, but it has annotations for them"
            )

        # validate all required arguments were passed either as positional or as keyword arguments
        for arg_name, arg_type in expected_arguments_names_and_types.items():
            if (
                arg_name not in passed_argument_names
                and arg_type not in passed_argument_types  # noqa: W503
            ):
                raise InjectorError(
                    f"Argument {arg_name=} was not passed for the target function"
                )

        # validate passed args and their types
        for arg_type, arg_value in passed_args.items():
            # check if arg_type is expected by the target function, raise an error if it's not
            if arg_type not in expected_argument_types:
                raise InjectorError(
                    f"Positional argument {arg_value=} with is not expected by the target function"
                )

        # validate passed kwargs and their types
        for arg_name, arg_value in passed_kwargs.items():
            # check if arg_name is expected by the target function, raise an error if it's not
            if arg_name not in expected_argument_names:
                raise InjectorError(
                    f"Argument {arg_name=} is not expected by the target function"
                )

            # get expected type for the passed kwarg
            expected_arg_type: type = expected_arguments_names_and_types[arg_name]

            # handle cases when expected type is bool but passed type is int which is a superclass of bool
            if expected_arg_type is bool and type(arg_value) is int:
                raise InjectorError(
                    f"Argument {arg_name=} with value {arg_value=} has wrong type {type(arg_value)}, "
                    f"expected {expected_arg_type=}"
                )

            # handle cases when expected type is int but passed type is bool which is a subclass of int
            if (
                expected_arg_type is int and isinstance(arg_value, bool)
            ) or not isinstance(arg_value, expected_arg_type):
                raise InjectorError(
                    f"Argument {arg_name=} with value {arg_value=} has wrong type {type(arg_value)}, "
                    f"expected {expected_arg_type=}"
                )

    @staticmethod
    def _validate_passed_arguments(
        passed_args: dict[type, Any],
        passed_kwargs: dict[str, Any],
        dependencies: set[ProviderContainer],
        target_function: Callable,
    ) -> None:
        # if no args and kwargs were passed and no provider functions were registered
        # for the target function - raise an error
        if not passed_args and not passed_kwargs and not dependencies:
            raise InjectorError(
                f"No dependencies were registered for the target function: {target_function}. Use `di.provider` to "
                f"register dependencies for the target function."
            )

    @staticmethod
    def _validate_provider_before_decoration(
        kwarg_name: Any, target_function: Any
    ) -> None:
        # validate that passed target_function is a callable
        if not isinstance(target_function, Callable):  # type: ignore
            raise ProviderError(
                f"Target function must be a callable, but got {type(target_function)}"
            )

        # validate that passed kwarg_name is a string or None
        if kwarg_name is not None and not isinstance(kwarg_name, str):
            raise ProviderError("Kwarg name of passed target function must be a string")

        # validate that passed kwarg_name is not en empty string
        if isinstance(kwarg_name, str) and kwarg_name == "":
            raise ProviderError(
                "Kwarg name of passed target function must not be an empty string"
            )

    @staticmethod
    def _validate_provider_during_decoration(
        provider_function: Callable, kwarg_name: str | None, target_function: Callable
    ) -> None:
        # validate that provider function has 'return type hint'
        try:
            provider_function_return_type: type = provider_function.__annotations__[
                "return"
            ]
        except KeyError:
            raise ProviderError("Target function must return a concrete type hint")

        # validate that provider's 'return type hint' is not Any
        if provider_function_return_type is Any:
            raise ProviderError(
                "Target function return type hint must by a concrete type, not Any"
            )

        # validate that provider's 'return type hint' is not Union type
        if (
            get_origin(provider_function_return_type) is Union
            or get_origin(provider_function_return_type) is UnionType  # noqa: W503
        ):
            raise ProviderError(
                "Target function return type hint must by a concrete type, not Union"
            )

        # validate the case, when target function has multiple arguments with the same type,
        # and provider function was not decorated with kwarg_name, so it's not clear for which
        # argument provider function should be used, so we have conflict here.
        if kwarg_name is None and (
            Counter(
                arg_value
                for arg_name, arg_value in target_function.__annotations__.items()
                if arg_name != "return"
            ).get(provider_function_return_type, 0)
            > 1  # noqa: W503
        ):
            raise ProviderError(
                f"Target function {target_function} has multiple arguments with the same type "
                f"{provider_function_return_type}, so you must specify kwarg_name for the provider function"
            )

    def inject(self, target_function: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator is used to inject dependencies into the target callable.

        Examples
        --------
            # Example 1: decorator is used via syntactic sugar (@)
            >>> from fastdi import di
            >>> from dataclasses import dataclass
            >>>
            >>> @dataclass
            >>> class Type1:
            ...     field: int
            >>>
            >>> @dataclass
            >>> class Type2:
            ...     field: str
            >>>
            >>> @di.inject
            >>> def my_func(a: Type1, b: Type2) -> None:
            ...     print(a, b)
            >>>
            >>> @di.provider(my_func)
            >>> def type1_provider() -> Type1:
            ...     return Type1(field=1)
            >>>
            >>> @di.provider(my_func)
            >>> def type2_provider() -> Type2:
            ...     return Type2(field="a")
            >>>
            >>> my_func()
            <Type1(field=1)> <Type2(field="a")>

            # Example 2: decorator is used directly w/o syntactic sugar
            >>> def my_func(a: Type1, b: Type2) -> None:
            ...     print(a, b)
            >>>
            >>> @di.provider(my_func)
            >>> def type1_provider() -> Type1:
            ...     return Type1(field=1)
            >>>
            >>> @di.provider(my_func)
            >>> def type2_provider() -> Type2:
            ...     return Type2(field="a")
            >>>
            >>> my_func = di.inject(my_func)
            >>> my_func()
            <Type1(field=1)> <Type2(field="a")>

        Args:
        ----
            target_function: callable for which dependencies should be injected

        Returns: wrapper function with injected dependencies

        """

        self._validate_inject_before_decoration(target_function)

        @wraps(target_function)
        def wrapper(*args, **kwargs) -> Any:  # type: ignore
            """Wrapper function for the target callable.

            There are to possible cases:
            1. target_function was not wrapped before
            2. target_function was wrapped before
            so we need to search for stored dependencies in both cases.

            Args:
            ----
                *args: passed args
                **kwargs: passed kwargs

            Returns: result of the target callable

            """

            # get all stored dependencies for the target function or its wrapper (if it was wrapped before)
            for clb in {
                target_function,
                self._target_wrapper_registry[target_function],
            }:
                dependencies: set[ProviderContainer] = self._dependencies_registry.get(
                    clb, set()
                )
                if dependencies != set():
                    break

            # get all passed arguments to function {arg_name: arg_type, ...}, and all passed kwargs
            # {arg_name: arg_value, ...}. we convert args to dict to be able to fetch arg type by arg value
            passed_args: dict[type, Any] = dict((type(arg), arg) for arg in args)
            passed_kwargs: dict[str, Any] = kwargs

            self._validate_passed_arguments(
                passed_args, passed_kwargs, dependencies, target_function
            )

            # get annotations {arg_name: arg_type, ...} from the target function
            function_annotations: dict[str, type] = dict(
                (arg_name, arg_type)
                for arg_name, arg_type in target_function.__annotations__.items()
                if arg_name != "return"
            )

            # compose dependencies to be injected from passed args and kwargs as well as from function annotations
            deps_to_be_injected: dict = self._compose_deps_to_be_injected(
                passed_args, passed_kwargs, function_annotations
            )

            # resolve all required dependencies for arg and kwargs which were not passed
            kwargs_to_be_injected: dict[str, Any] = dict(
                (
                    arg_name,
                    self._resolve_dependency(arg_name, arg_type, dependencies),
                )
                for arg_name, arg_type in deps_to_be_injected.items()
            )

            # merge passed kwargs and kwargs to be injected, thus injecting dependencies into the target function via
            # kwargs only
            injected_kwargs = {**kwargs, **kwargs_to_be_injected}

            self._validate_arguments_for_target_function_call(
                passed_args, injected_kwargs, target_function
            )

            return target_function(*args, **injected_kwargs)

        # store original target function in the map to be able to fetch all registered dependencies for it
        self._target_wrapper_registry[target_function] = wrapper

        return wrapper

    def provider(
        self, target_function: Callable[..., Any], kwarg_name: str | None = None
    ) -> Callable[..., Any]:
        """Decorator is used to register provider function for the target function.

        Args:
        ----
            target_function: target function for which provider function should be registered
            kwarg_name: name of kwarg for which provider function should be registered (optional)

        Example:
        -------
                >>> from fastdi import di
                >>> from dataclasses import dataclass
                >>>
                >>> @dataclass
                >>> class MyType:
                ...     field: int
                >>>
                >>> def my_func(a: MyType) -> None:
                ...     print(a)
                >>>
                >>> @di.provider(my_func)
                >>> def my_type_provider() -> MyType:
                ...     return MyType(field=1)

        Returns: decorator

        """

        self._validate_provider_before_decoration(kwarg_name, target_function)

        def decorator(provider_function: Callable[..., Any]) -> Callable[..., Any]:

            self._validate_provider_during_decoration(
                provider_function, kwarg_name, target_function
            )

            @wraps(provider_function)
            def wrapper(*args, **kwargs) -> Any:  # type: ignore
                return provider_function(*args, **kwargs)

            self._dependencies_registry[target_function].add(
                ProviderContainer(
                    provider_function=provider_function, kwarg_name=kwarg_name
                )
            )

            return wrapper

        return decorator

    def _resolve_dependency(
        self,
        arg_name: str,
        arg_type: type,
        dependencies: set[ProviderContainer],
    ) -> Any:
        """Resolve dependency provider function for the target function.

        Args:
        ----
            arg_name: name of kwarg for which dependency provider function should be fetched
            arg_type: value of kwarg for which dependency provider function should be fetched
            dependencies: list of ProviderContainer instances for the target callable

        Returns: concrete dependency object (resolved) or None

        """
        for provider_container in [
            # order is important here: first, try to fetch dependency provider by arg name, then by arg type
            self._fetch_dependency_provider_by_key_word_arg_name(
                arg_name, dependencies
            ),
            self._fetch_dependency_provider_by_argument_type(arg_type, dependencies),
        ]:
            provider_container: ProviderContainer | None  # type: ignore

            if provider_container is not None:
                return provider_container.provider_function()

        raise InjectorError(
            f"No dependency was registered for argument {arg_name=} with type {arg_type=}."
        )
