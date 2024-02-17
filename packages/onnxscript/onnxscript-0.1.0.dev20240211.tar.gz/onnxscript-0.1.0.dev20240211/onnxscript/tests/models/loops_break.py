# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

from onnx import TensorProto
from onnx.helper import make_tensor

from onnxscript import script
from onnxscript.onnx_opset import opset15 as op
from onnxscript.onnx_types import FLOAT


@script()
def loop1(A: FLOAT["N"]) -> FLOAT["N"]:
    T = A
    for i in range(10):
        T = T + A * op.Cast(i, to=TensorProto.FLOAT)
    return T


@script()
def loop_range_cond(A: FLOAT["N"]) -> FLOAT["N"]:
    T = A
    cond = op.Constant(value=make_tensor("condcst", TensorProto.BOOL, [1], [1]))
    for i in range(10):
        T = T + A * op.Cast(i, to=TensorProto.FLOAT)
        cond = op.ReduceSum(T) <= -10
        if cond:
            break
    return T
