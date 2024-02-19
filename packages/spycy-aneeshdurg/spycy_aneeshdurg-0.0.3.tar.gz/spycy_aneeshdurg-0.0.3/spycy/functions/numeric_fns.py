from typing import List

import numpy as np
import pandas as pd

from spycy.errors import ExecutionError
from spycy.types import FunctionContext


def _wrap_simple_fn(f):
    def wrapped(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
        if len(params) != 1:
            raise ExecutionError(f"Invalid number of arguments")
        return f(params[0].to_numpy(dtype=float))

    return wrapped


def rand(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) != 0:
        raise ExecutionError(f"Invalid number of arguments")
    return pd.Series(np.random.rand(len(fnctx.table)))


fn_map = {
    "abs": _wrap_simple_fn(np.abs),
    "ceil": _wrap_simple_fn(np.ceil),
    "floor": _wrap_simple_fn(np.floor),
    "rand": rand,
    "round": _wrap_simple_fn(np.round),
    "sign": _wrap_simple_fn(np.sign),
}
