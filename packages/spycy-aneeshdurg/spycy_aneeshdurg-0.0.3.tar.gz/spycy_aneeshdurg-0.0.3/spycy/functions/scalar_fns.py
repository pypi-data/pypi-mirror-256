from typing import List

import numpy as np
import pandas as pd

from spycy.errors import ExecutionError
from spycy.types import Edge, FunctionContext, Node, Path


def coalesce(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    data = []
    for i in range(len(params[0])):
        for param in params:
            if param[i] is not pd.NA:
                data.append(param[i])
                break
    return pd.Series(data)


def endNode(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    raise AssertionError("endNode unimplemented")


def head(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to id")
    output = []
    for el in params[0]:
        if el is pd.NA:
            output.append(pd.NA)
        elif isinstance(el, list):
            output.append(el[0] if len(el) else pd.NA)
        else:
            raise ExecutionError(f"TypeError::head expected list, got {type(el)}")
    return pd.Series(output)


def id_(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to id")
    output = []
    for el in params[0]:
        if not isinstance(el, Node):
            raise ExecutionError("TypeError::id got unexpected type")
        output.append(el.id_)
    return pd.Series(output)


def last(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    raise AssertionError("last unimplemented")


def length(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to length")

    output = []
    for el in params[0]:
        if el is pd.NA:
            output.append(pd.NA)
        elif isinstance(el, list):
            output.append(len(el))
        elif isinstance(el, Path):
            length_ = 0
            for edge in el.edges:
                if isinstance(edge, list):
                    length_ += len(edge)
                else:
                    length_ += 1
            output.append(length_)
        else:
            raise ExecutionError(f"TypeError::length expected list, got {type(el)}")
    return pd.Series(output, dtype="Int64")


def properties(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to type")

    output = []
    for el in params[0]:
        if el is pd.NA:
            output.append(pd.NA)
        elif isinstance(el, dict):
            output.append(el)
        elif isinstance(el, Edge):
            data = fnctx.graph.edges[el.id_]
            output.append(data["properties"])
        elif isinstance(el, Node):
            data = fnctx.graph.nodes[el.id_]
            output.append(data["properties"])
        else:
            raise ExecutionError(
                "TypeError - properties expects a node or an edge argument"
            )
    return pd.Series(output)


def size(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to tail")

    output = []
    for el in params[0]:
        if el is pd.NA:
            output.append(pd.NA)
            continue

        if isinstance(el, str) or isinstance(el, list):
            output.append(len(el))
        else:
            raise ExecutionError(
                f"TypeError - size expects a list-like argument, got {type(el)}"
            )
    return pd.Series(output)


def startNode(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    raise AssertionError("startNode unimplemented")


def timestamp(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    raise AssertionError("timestamp unimplemented")


def toBoolean(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to toBoolean")
    arg = params[0]
    output = []
    for i in range(len(arg)):
        if arg[i] is pd.NA:
            output.append(pd.NA)
        elif np.issubdtype(type(arg[i]), np.bool_):
            # could be numpy.bool_ or bool
            output.append(arg[i])
        elif isinstance(arg[i], str):
            if arg[i] == "true":
                output.append(True)
            elif arg[i] == "false":
                output.append(False)
            else:
                output.append(pd.NA)
        else:
            raise ExecutionError("TypeError::toBoolean got unexpected type")
    return pd.Series(output)


def toFloat(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to toFloat")
    arg = params[0]
    output = []
    for i in range(len(arg)):
        val = arg[i]
        if val is pd.NA:
            output.append(pd.NA)
        elif np.issubdtype(type(val), np.float_):
            output.append(val)
        elif np.issubdtype(type(val), np.integer):
            output.append(float(val))
        elif isinstance(val, str):
            try:
                output.append(float(val))
            except ValueError:
                output.append(pd.NA)
        else:
            raise ExecutionError("TypeError::toInteger got unexpected type")
    return pd.Series(output)


def toInteger(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to toInteger")
    arg = params[0]
    output = []
    for i in range(len(arg)):
        val = arg[i]
        if val is pd.NA:
            output.append(pd.NA)
        elif np.issubdtype(type(val), np.integer):
            output.append(val)
        elif np.issubdtype(type(val), np.float_):
            output.append(int(val))
        elif isinstance(val, str):
            try:
                output.append(int(float(val)))
            except ValueError:
                output.append(pd.NA)
        else:
            raise ExecutionError("TypeError::toInteger got unexpected type")
    return pd.Series(output)


def type_(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to type")

    output = []
    for edge in params[0]:
        if edge is pd.NA:
            output.append(pd.NA)
            continue

        if not isinstance(edge, Edge):
            raise ExecutionError("TypeError - type expects an edge argument")
        edge_data = fnctx.graph.edges[edge.id_]
        output.append(edge_data["type"])
    return pd.Series(output)


fn_map = {
    "coalesce": coalesce,
    "endnode": endNode,
    "head": head,
    "id": id_,
    "last": last,
    "length": length,
    "properties": properties,
    "size": size,
    "startNode": startNode,
    "timestamp": timestamp,
    "toboolean": toBoolean,
    "tofloat": toFloat,
    "tointeger": toInteger,
    "type": type_,
}
