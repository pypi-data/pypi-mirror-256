import os
from typing import Callable

import pytest
from pytest_benchmark.plugin import benchmark


# @pytest.mark.skipif(
#     condition=os.getenv("ENVIRONMENT") == "ci", reason="Skip in CI environment"
# )
# @pytest.mark.skip()
@pytest.mark.parametrize(
    "number_of_args, number_of_kwargs, number_of_inject_decorators, number_of_provider_decorators",
    [
        (1, 1, 1, 1),
        (10, 10, 10, 10),
        (20, 20, 20, 20),
        (30, 30, 30, 30),
        (40, 40, 40, 40),
        (50, 50, 50, 50),
        (60, 60, 60, 60),
        (70, 70, 70, 70),
        (80, 80, 80, 80),
        (90, 90, 90, 90),
        (100, 100, 100, 100),
    ],
)
def test_benchmark(
    benchmark: Callable,
    benchmark_use_case: Callable,
    number_of_args: int,
    number_of_kwargs: int,
    number_of_inject_decorators: int,
    number_of_provider_decorators: int,
) -> None:
    benchmark(
        benchmark_use_case,
        number_of_args=number_of_args,
        number_of_kwargs=number_of_kwargs,
        number_of_inject_decorators=number_of_inject_decorators,
        number_of_provider_decorators=number_of_provider_decorators,
    )
