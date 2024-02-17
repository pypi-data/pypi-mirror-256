# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Invert op"""
from mindspore.ops.op_info_register import op_info_register, TBERegOp, DataType

invert_ds_op_info = TBERegOp("Invert") \
    .fusion_type("OPAQUE") \
    .async_flag(False) \
    .binfile_name("invert.so") \
    .compute_cost(10) \
    .kernel_name("invert") \
    .partial_flag(True) \
    .dynamic_shape(True) \
    .input(0, "x", False, "required", "all") \
    .output(0, "y", False, "required", "all") \
    .op_pattern("formatAgnostic") \
    .dtype_format(DataType.I16_None, DataType.I16_None) \
    .dtype_format(DataType.U16_None, DataType.U16_None) \
    .get_op_info()


@op_info_register(invert_ds_op_info)
def _invert_ds_tbe():
    """Invert TBE register"""
    return
