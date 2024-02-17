# Copyright 2020 Huawei Technologies Co., Ltd
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

"""BNTrainingUpdateV2 op"""
from mindspore.ops.op_info_register import op_info_register, TBERegOp, DataType

bn_training_update_v2_op_info = TBERegOp("BNTrainingUpdateV2") \
    .fusion_type("OPAQUE") \
    .async_flag(False) \
    .binfile_name("bn_training_update_v2.so") \
    .compute_cost(10) \
    .kernel_name("bn_training_update_v2") \
    .partial_flag(True) \
    .attr("epsilon", "required", "float", "all") \
    .input(0, "x", False, "required", "all", reshape_type="NC") \
    .input(1, "sum", False, "required", "all") \
    .input(2, "square_sum", False, "required", "all") \
    .input(3, "scale", False, "required", "all") \
    .input(4, "offset", False, "required", "all") \
    .output(0, "y", False, "required", "all", reshape_type="NC") \
    .output(1, "batch_mean", False, "required", "all") \
    .output(2, "batch_variance", False, "required", "all") \
    .is_dynamic_format(True) \
    .dtype_format(DataType.F16_None, DataType.F32_None, DataType.F32_None,
                  DataType.F32_None, DataType.F32_None, DataType.F16_None,
                  DataType.F32_None, DataType.F32_None) \
    .dtype_format(DataType.F32_None, DataType.F32_None, DataType.F32_None,
                  DataType.F32_None, DataType.F32_None, DataType.F32_None,
                  DataType.F32_None, DataType.F32_None) \
    .get_op_info()


@op_info_register(bn_training_update_v2_op_info)
def _bn_training_update_v2_tbe():
    """BNTrainingUpdateV2 TBE register"""
    return
