from typing import Any

import pytest

from fastdi import FastDI

from .objects import Type1, Type2, Type3


@pytest.mark.parametrize(
    "inject_decorators_number,provider_decorators_number,use_kwarg_name",
    [
        # same number of inject and provider decorators
        (1, 1, True),
        (1, 1, False),
        (2, 2, True),
        (2, 2, False),
        (3, 3, True),
        (3, 3, False),
        (4, 4, True),
        (4, 4, False),
        (5, 5, True),
        (5, 5, False),
        (6, 6, True),
        (6, 6, False),
        (7, 7, True),
        (7, 7, False),
        (8, 8, True),
        (8, 8, False),
        (9, 9, True),
        (9, 9, False),
        (10, 10, True),
        (10, 10, False),
        (50, 50, True),
        (50, 50, False),
        (100, 100, True),
        (100, 100, False),
        (500, 500, True),
        (500, 500, False),
        (900, 900, True),
        (900, 900, False),
        # different number of inject and provider decorators
        (1, 900, True),
        (1, 900, False),
        (2, 500, True),
        (2, 500, False),
        (3, 100, True),
        (3, 100, False),
        (4, 50, True),
        (4, 50, False),
        (5, 10, True),
        (5, 10, False),
        (6, 5, True),
        (6, 5, False),
        (7, 4, True),
        (7, 4, False),
        (8, 3, True),
        (8, 3, False),
        (9, 2, True),
        (9, 2, False),
        (10, 1, True),
        (10, 1, False),
        (100, 1, True),
        (100, 1, False),
        (500, 1, True),
        (500, 1, False),
        (900, 1, True),
        (900, 1, False),
    ],
)
def test_my_func_call(
    di: FastDI,
    calls_data: list[dict[str, Any]],
    inject_decorators_number: int,
    provider_decorators_number: int,
    use_kwarg_name: bool,
) -> None:
    """
    Test my_func call without arguments passed, but with different number of inject and provider decorators.

    Args:
        di: FastDI instance fixture
        calls_data: List of dictionaries with different arguments passed
        inject_decorators_number: Number of inject decorators to apply
        provider_decorators_number: Number of provider decorators to apply

    Examples:

        # >>> @di.inject
        # >>> @di.inject
        # >>> @di.inject
        # >>> def my_func(...): ...
        # >>>
        # >>> @di.provider(my_func)
        # >>> @di.provider(my_func)
        # >>> def provider_func(): ...
        # >>>
        # >>> my_func()

    Returns: None

    """

    def my_func(arg1: Type1, arg2: Type2, arg3: Type3) -> tuple[Type1, Type2, Type3]:
        return arg1, arg2, arg3

    for _ in range(inject_decorators_number):
        my_func = di.inject(my_func)

    def provide_type1_instance() -> Type1:
        return Type1(field=1)

    def provide_type2_instance() -> Type2:
        return Type2(field="a")

    def provide_type3_instance() -> Type3:
        return Type3(field=True)

    for _ in range(provider_decorators_number):
        provide_type1_instance = di.provider(
            my_func, kwarg_name="arg1" if use_kwarg_name is True else None
        )(provide_type1_instance)
        provide_type2_instance = di.provider(
            my_func, kwarg_name="arg2" if use_kwarg_name is True else None
        )(provide_type2_instance)
        provide_type3_instance = di.provider(
            my_func, kwarg_name="arg3" if use_kwarg_name is True else None
        )(provide_type3_instance)

    for data in calls_data:
        # call with different arguments passed and without dependency injection
        if (data["args"] or data["kwargs"]) and (
            len(data["args"]) + len(data["kwargs"]) == 3
        ):
            # call without dependency injection
            result = my_func(*data["args"], **data["kwargs"])

            if (data["args"] and not data["kwargs"]) and len(data["args"]) == 3:
                # check call with all the args manually passed
                assert result[0].field == data["args"][0].field
                assert result[1].field == data["args"][1].field
                assert result[2].field == data["args"][2].field

            elif (data["kwargs"] and not data["args"]) and len(data["kwargs"]) == 3:
                # check call with all the kwargs manually passed
                assert result[0].field == data["kwargs"]["arg1"].field
                assert result[1].field == data["kwargs"]["arg2"].field
                assert result[2].field == data["kwargs"]["arg3"].field

            else:
                # check call with mixed arguments passed without dependency injection
                try:
                    expected_arg_1_field = data["args"][0].field
                except IndexError:
                    expected_arg_1_field = data["kwargs"]["arg1"].field

                try:
                    expected_arg_2_field = data["args"][1].field
                except IndexError:
                    expected_arg_2_field = data["kwargs"]["arg2"].field

                try:
                    expected_arg_3_field = data["args"][2].field
                except IndexError:
                    expected_arg_3_field = data["kwargs"]["arg3"].field

                assert result[0].field == expected_arg_1_field
                assert result[1].field == expected_arg_2_field
                assert result[2].field == expected_arg_3_field

        elif not data["args"] and not data["kwargs"]:
            # call with dependency injection (no manually arguments passed at all)
            result = my_func()  # type: ignore

            assert result[0].field == 1
            assert result[1].field == "a"
            assert result[2].field is True

        else:
            # call with dependency injection and some manually passed arguments
            result = my_func(*data["args"], **data["kwargs"])

            # expected values in case of DI
            expected_arg_1_field = 1
            expected_arg_2_field = "a"
            expected_arg_3_field = True

            # determine which arguments were passed manually
            for arg in data["args"]:
                if isinstance(arg, Type1):
                    expected_arg_1_field = arg.field
                elif isinstance(arg, Type2):
                    expected_arg_2_field = arg.field
                elif isinstance(arg, Type3):
                    expected_arg_3_field = arg.field

            for key, value in data["kwargs"].items():
                if key == "arg1":
                    expected_arg_1_field = value.field
                elif key == "arg2":
                    expected_arg_2_field = value.field
                elif key == "arg3":
                    expected_arg_3_field = value.field

            assert result[0].field == expected_arg_1_field
            assert result[1].field == expected_arg_2_field
            assert result[2].field == expected_arg_3_field

        assert isinstance(result, tuple)
        assert len(result) == 3
        assert isinstance(result[0], Type1)
        assert isinstance(result[1], Type2)
        assert isinstance(result[2], Type3)
