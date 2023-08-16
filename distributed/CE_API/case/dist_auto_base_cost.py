#!/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
# ======================================================================
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
# ======================================================================
"""
/***************************************************************************
  *
  * Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
  * @file dist_auto_base_cost.py
  * @author liujie44@baidu.com
  * @date 2022-09-07 11:00
  * @brief
  *
  **************************************************************************/
"""
import json
import os
import tempfile

import paddle
import paddle.nn.functional as F
from paddle import nn, static, utils
from paddle.distributed import fleet
from paddle.distributed.auto_parallel.static.cluster import Cluster
from paddle.distributed.auto_parallel.static.completion import Completer
from paddle.distributed.auto_parallel.static.cost import (
    AllreduceSumOpCost,
    _g_op_cost_factory,
)
from paddle.distributed.auto_parallel.static.cost.base_cost import (
    build_comm_costs_from_descs,
    build_comm_desc_from_dist_op,
    build_comp_costs_from_descs,
    build_comp_desc_from_dist_op,
    build_dp_costs,
)
from paddle.distributed.auto_parallel.static.dist_context import (
    DistributedContext,
)
from paddle.distributed.auto_parallel.static.parallelizer import (
    AutoParallelizer,
)
from paddle.distributed.fleet import auto

from dist_auto_cluster import cluster_json
from utils import run_priority

paddle.enable_static()
_global_parallel_strategy = "dp_mp_pp"
_global_process_mesh = auto.ProcessMesh([[[0, 1], [4, 5]], [[2, 3], [6, 7]]], dim_names=["x", "y", "z"])
PP_MESH_0 = auto.ProcessMesh([[0, 1], [4, 5]], dim_names=["x", "y"])
PP_MESH_1 = auto.ProcessMesh([[2, 3], [6, 7]], dim_names=["x", "y"])


class MLPLayer(nn.Layer):
    """MLPLayer"""

    def __init__(
        self,
        hidden_size=1024,
        intermediate_size=4 * 1024,
        initializer_range=0.02,
    ):
        super().__init__()
        d_model = hidden_size
        dim_feedforward = intermediate_size
        weight_attr = paddle.ParamAttr(initializer=nn.initializer.Normal(mean=0.0, std=initializer_range))
        bias_attr = None

        self.linear0 = nn.Linear(d_model, dim_feedforward, weight_attr, bias_attr=bias_attr)
        self.linear1 = nn.Linear(dim_feedforward, d_model, weight_attr, bias_attr=bias_attr)
        self.norm = nn.LayerNorm(d_model, epsilon=1e-5)

    def forward(self, input):
        """forward"""
        auto.shard_tensor(self.linear0.weight, PP_MESH_0, [None, "y"])
        auto.shard_tensor(self.linear1.weight, PP_MESH_1, ["y", None])

        out = self.norm(input)
        out = self.linear0(out)
        out = F.gelu(out, approximate=True)
        out = self.linear1(out)

        return out


def mlp_forward(train_program, start_program):
    """mlp_forward"""
    with static.program_guard(train_program, start_program), utils.unique_name.guard():
        batch_size = 4
        hidden_size = 1024
        input = static.data(name="input", shape=[batch_size, hidden_size], dtype="float32")
        label = static.data(name="label", shape=[batch_size, 1], dtype="float32")
        fill_shape = [batch_size]
        fill_shape[0] = input.shape[0]
        fill_constant_out = paddle.full(fill_shape, 1, dtype="int32")
        embedding = paddle.nn.Embedding(10, hidden_size, sparse=True)
        embedding_out = embedding(fill_constant_out)

        auto.shard_tensor(input, PP_MESH_0, ["x", None])
        auto.shard_tensor(label, PP_MESH_1, ["x", None])

        mlp = MLPLayer(
            hidden_size=hidden_size,
            intermediate_size=4 * hidden_size,
            initializer_range=0.02,
        )

        predict = mlp(embedding_out)
        error_cost = paddle.nn.functional.square_error_cost(predict, label)
        loss = paddle.mean(error_cost)

    return loss, train_program, start_program


def get_prog(train_program, startup_program, dist_context, rank_id):
    """get_prog"""
    global _global_process_mesh
    dist_context.process_mesh = _global_process_mesh
    loss, train_program, startup_program = mlp_forward(train_program, startup_program)

    fleet._user_defined_strategy = fleet.DistributedStrategy()
    fleet.user_defined_optimizer = paddle.optimizer.Adam()
    parallelizer = AutoParallelizer(fleet)
    parallelizer._dist_context = dist_context

    # serial forward & backward completion
    completer = Completer(dist_context)
    complete_train_program = completer.complete_forward_annotation(train_program)
    dist_context.block_state.parse_forward_blocks(complete_train_program)
    params_grads = parallelizer._generate_backward(
        complete_train_program,
        startup_program,
        loss,
        parameter_list=None,
        no_grad_set=None,
        callbacks=None,
    )
    return train_program, startup_program, params_grads


@run_priority(level="P0")
def test_base_cost():
    """test_base_cost"""
    # setUp
    temp_dir = tempfile.TemporaryDirectory()

    # Build cluster
    cluster_json_path = os.path.join(temp_dir.name, "auto_parallel_cluster.json")
    cluster_json_object = json.loads(cluster_json)
    with open(cluster_json_path, "w") as cluster_json_file:
        json.dump(cluster_json_object, cluster_json_file)
    cluster = Cluster()
    cluster.build_from_file(cluster_json_path)

    train_program = paddle.static.Program()
    startup_program = paddle.static.Program()
    dist_context = DistributedContext()
    rank_id = 2
    train_program, startup_program, params_grads = get_prog(train_program, startup_program, dist_context, rank_id)

    for op in train_program.global_block().ops:
        dist_op = dist_context.get_dist_op_for_program(op)
        if dist_op:
            processes = dist_op.dist_attr.process_mesh.process_ids
            comp_descs = build_comp_desc_from_dist_op(dist_op, dist_context)
            assert isinstance(comp_descs, dict) is True
            assert comp_descs is not None
            var_names = None
            if op.input_arg_names:
                var_names = op.input_arg_names[0]
                comm_descs = build_comm_desc_from_dist_op(
                    "c_allreduce_sum",
                    dist_op,
                    dist_context,
                    var_names,
                    attrs=None,
                    parallel_axis=0,
                    group_ranks=None,
                )
                assert isinstance(comm_descs, dict) is True
                assert comm_descs is not None

                comm_descs = build_comm_desc_from_dist_op(
                    "c_allreduce_sum",
                    dist_op,
                    dist_context,
                    var_names,
                    attrs=None,
                    parallel_axis=None,
                    group_ranks=processes,
                )
                assert isinstance(comm_descs, dict) is True
                assert comm_descs is not None

                comm_costs = build_comm_costs_from_descs(
                    AllreduceSumOpCost,
                    dist_context,
                    processes,
                    comm_descs,
                    cluster,
                )
                assert comm_costs is not None

                comp_costs = build_comp_costs_from_descs(
                    _g_op_cost_factory[op.type],
                    dist_context,
                    processes,
                    comp_descs,
                    cluster,
                )
                assert comp_costs is not None

                result = []
                build_dp_costs(
                    result,
                    dist_op,
                    dist_context,
                    var_names[0],
                    None,
                    0,
                    cluster,
                )
                assert result is not None

    # Remove unnecessary files
    if os.path.exists(cluster_json_path):
        os.remove(cluster_json_path)

    # tearDown
    temp_dir.cleanup()
    print("test_base_cost ... ok")


if __name__ == "__main__":
    test_base_cost()