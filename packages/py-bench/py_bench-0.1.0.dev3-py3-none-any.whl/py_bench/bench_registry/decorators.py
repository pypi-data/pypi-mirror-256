from typing import TypeVar

from py_bench.bench_registry.bench_regisrty import BenchRegistry


TParam = TypeVar('TParam')


def benchmark(f):
    BenchRegistry.bench_marked_functions.append(f)
    return f


def param(*args: TParam):
    def dumb_wrapper(f) -> TParam:
        return BenchRegistry.save_param_marked_function(f, args)

    return dumb_wrapper


def case_setup(f):
    return BenchRegistry.save_case_setup_function(f)
