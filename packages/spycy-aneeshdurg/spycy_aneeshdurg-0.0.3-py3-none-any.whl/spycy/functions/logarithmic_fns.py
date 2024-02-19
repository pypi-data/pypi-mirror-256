from typing import List

import numpy as np
import pandas as pd

from spycy.errors import ExecutionError
from spycy.functions.numeric_fns import _wrap_simple_fn
from spycy.types import FunctionContext


def e_(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) != 0:
        raise ExecutionError("Incorrect argument count")
    return pd.Series([np.e] * len(fnctx.table), dtype=float)


fn_map = {
    "e": e_,
    "exp": _wrap_simple_fn(np.exp),
    "log": _wrap_simple_fn(np.log),
    "log10": _wrap_simple_fn(np.log10),
    "sqrt": _wrap_simple_fn(np.sqrt),
}
