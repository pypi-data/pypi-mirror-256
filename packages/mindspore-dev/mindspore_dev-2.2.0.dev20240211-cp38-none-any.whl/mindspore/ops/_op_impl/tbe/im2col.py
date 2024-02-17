# Copyright 2022 Huawei Technologies Co., Ltd
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

"""Im2Col op"""
from mindspore.ops.op_info_register import op_info_register, TBERegOp, DataType

im2col_op_info = TBERegOp("Im2Col") \
    .fusion_type("OPAQUE") \
    .async_flag(False) \
    .binfile_name("im2col.so") \
    .compute_cost(10) \
    .kernel_name("im2col") \
    .partial_flag(True) \
    .attr("ksizes", "required", "listInt", "all", "[]") \
    .attr("strides", "optional", "listInt", "all", "[1]") \
    .attr("dilations", "optional", "listInt", "all", "[1]") \
    .attr("padding_mode", "optional", "str", "all", "CALCULATED") \
    .attr("pads", "optional", "listInt", "all", "[0]") \
    .input(0, "x", False, "required", "all") \
    .output(0, "y", False, "required", "all") \
    .dtype_format(DataType.F16_5HD, DataType.F16_NHWC) \
    .dtype_format(DataType.I8_5HD, DataType.I8_NHWC) \
    .dtype_format(DataType.U8_5HD, DataType.U8_NHWC) \
    .get_op_info()


@op_info_register(im2col_op_info)
def _im2col_tbe():
    """Im2Col TBE register"""
    return
