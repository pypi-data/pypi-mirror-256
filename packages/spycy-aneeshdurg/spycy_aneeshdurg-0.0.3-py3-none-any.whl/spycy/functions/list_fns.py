from typing import List

import numpy as np
import pandas as pd

from spycy.errors import ExecutionError
from spycy.types import Edge, FunctionContext, Node, Path


def keys(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to keys")

    output = []
    for el in params[0]:
        if el is pd.NA:
            output.append(pd.NA)
        elif isinstance(el, dict):
            output.append(sorted(list(el.keys())))
        elif isinstance(el, Node):
            node_props = fnctx.graph.nodes[el.id_]["properties"]
            non_null_keys = [k for k, v in node_props.items() if v is not pd.NA]
            output.append(sorted(non_null_keys))
        elif isinstance(el, Edge):
            edge_props = fnctx.graph.edges[el.id_]["properties"]
            non_null_keys = [k for k, v in edge_props.items() if v is not pd.NA]
            output.append(sorted(non_null_keys))
        else:
            raise ExecutionError("TypeError - expected map-like type for keys")
    return pd.Series(output)


def labels(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to labels")

    output = []
    for node in params[0]:
        if node is pd.NA:
            output.append(pd.NA)
            continue

        if not isinstance(node, Node):
            raise ExecutionError("TypeError - labels expects a Node argument")
        node_data = fnctx.graph.nodes[node.id_]
        output.append(sorted(list(node_data["labels"])))
    return pd.Series(output)


def nodes(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to nodes")

    output = []
    for path in params[0]:
        if path is pd.NA:
            output.append(pd.NA)
            continue

        if not isinstance(path, Path):
            raise ExecutionError("TypeError - nodes expects a Path argument")

        num_edges = len(path.edges)
        path_nodes = []

        if len(path.nodes):
            src = path.nodes[0]
            path_nodes.append(Node(src))
            for i in range(num_edges):
                edges = path.edges[i]
                if not isinstance(edges, list):
                    edges = [edges]
                for edge in edges:
                    dst = edge[1] if edge[0] == src else edge[0]
                    path_nodes.append(Node(dst))
                    src = dst
        output.append(path_nodes)
    return pd.Series(output)


def range_(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) not in [2, 3]:
        raise ExecutionError("Incorrect argument count for range")

    output = []
    for i in range(len(params[0])):
        start = params[0][i]
        end = params[1][i]
        if not np.issubdtype(type(start), np.integer):
            raise ExecutionError(
                f"TypeError::range must take ints as arguments, got {type(start)}"
            )
        if not np.issubdtype(type(end), np.integer):
            raise ExecutionError(
                f"TypeError::range must take ints as arguments, got {type(end)}"
            )
        step = 1
        if len(params) == 3:
            step = params[2][i]
            if step == 0:
                raise ExecutionError("NumberOutOfRange::range's step must be > 0")
            if not np.issubdtype(type(step), np.integer):
                raise ExecutionError(
                    f"TypeError::range must take ints as arguments, got {type(step)}"
                )

        if start == end:
            output.append([start])
        else:
            end += 1 if step > 0 else -1
            output.append(list(range(start, end, step)))
    return pd.Series(output)


def relationships(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    raise AssertionError("relationships not implemented")


def reverse(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to reverse")

    output = []
    for el in params[0]:
        if el is pd.NA:
            output.append(pd.NA)
            continue

        if not isinstance(el, str) and not isinstance(el, list):
            raise ExecutionError(
                f"TypeError - reverse expects a list-like argument, got {type(el)}"
            )
        output.append(el[::-1])
    return pd.Series(output)


def tail(params: List[pd.Series], fnctx: FunctionContext) -> pd.Series:
    if len(params) > 1:
        raise ExecutionError("Invalid number of arguments to tail")

    output = []
    for el in params[0]:
        if el is pd.NA:
            output.append(pd.NA)
            continue

        if isinstance(el, str) or isinstance(el, list):
            if len(el) == 0:
                output.append(pd.NA)
            else:
                output.append(el[-1])
        else:
            raise ExecutionError("TypeError - tail expects a list-like argument")
    return pd.Series(output)


fn_map = {
    "keys": keys,
    "labels": labels,
    "nodes": nodes,
    "range": range_,
    "relationships": relationships,
    "reverse": reverse,
    "tail": tail,
}
