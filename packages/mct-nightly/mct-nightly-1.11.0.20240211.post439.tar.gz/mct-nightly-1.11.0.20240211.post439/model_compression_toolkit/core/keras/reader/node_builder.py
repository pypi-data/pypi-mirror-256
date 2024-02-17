# Copyright 2021 Sony Semiconductor Israel, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from typing import Any, Callable, Dict
import inspect

import tensorflow as tf
import numpy as np
from packaging import version

from model_compression_toolkit.core.keras.custom_layer_validation import is_keras_custom_layer
from model_compression_toolkit.core.keras.tf_tensor_numpy import tf_tensor_to_numpy as to_numpy
from model_compression_toolkit.logger import Logger

if version.parse(tf.__version__) >= version.parse("2.13"):
    from keras.src.layers.core import TFOpLambda, SlicingOpLambda
    from keras.src.engine.keras_tensor import KerasTensor
    from keras.src.engine.node import Node as KerasNode
else:
    from keras.layers.core import TFOpLambda, SlicingOpLambda
    from keras.engine.keras_tensor import KerasTensor
    from keras.engine.node import Node as KerasNode

from model_compression_toolkit.core.common.graph.base_node import BaseNode
from model_compression_toolkit.core.common.graph.functional_node import FunctionalNode

keras = tf.keras
layers = keras.layers

REUSED_IDENTIFIER = '_reused_'


is_const = lambda x: isinstance(x, (tf.Variable, tf.Tensor, np.ndarray))
is_tensor = lambda x: isinstance(x, KerasTensor)


def get_kwargs2index(tf_func: Callable) -> Dict[str, int]:
    """
    Positional weights are saved according to their index in the node's call arguments, so
    need to know the function arguments' names in case the weights are in the kwargs.
    Args:
        tf_func: functional node function.

    Returns:
        A dictionary with argument number and index: {arg_name: arg_index}.
    """
    if tf_func in [tf.add, tf.subtract, tf.divide, tf.truediv, tf.multiply, tf.pow,
                   tf.matmul, tf.image.crop_and_resize, tf.image.combined_non_max_suppression]:
        return {arg_name: i for i, arg_name in enumerate(inspect.getfullargspec(tf_func).args)}
    else:
        return {}


def build_node(node: KerasNode,
               node_name_to_node: dict) -> BaseNode:
    """
    Build a node from a Keras node. A node contains all information to reconstruct the layer it's representing
    in a model:
    operation, layer configuration, path for instantiating the Keras layer the node has, weights, group of other
    nodes if it's a reused layer,
    input/output shape.
    Args:
        node: Node in the graph of a Keras model.
        node_name_to_node: Dictionary of already created nodes aims to identify reused layers.

    Returns:
        Graph node that was built from the Keras node.
    """
    keras_layer = node.layer  # get the layer the node represents.
    layer_config = keras_layer.get_config()  # layer configuration to reconstruct it.
    op_call_args = node.call_args
    op_call_kwargs = node.call_kwargs
    layer_class = type(keras_layer)  # class path to instantiating it in back2framework.
    weights = {v.name: v.numpy() for v in keras_layer.weights}  # layer's weights

    # If it's a node representing a reused layer, several nodes will contain the same layer instance.
    # Thus, the first time a node of a reused layer is being created, it's being build as a node of a non-reused layer,
    # while other nodes of this layer will be created as nodes of a reused layer with the suffix "_reused_i"
    # where i is the input/output index of the layer.
    is_reused = keras_layer.name in node_name_to_node
    if is_reused:
        # Mark the "base" node with its reused group.
        node_name_to_node[keras_layer.name].reuse_group = keras_layer.name
        io_index = 1
        while keras_layer.name + REUSED_IDENTIFIER + str(io_index) in node_name_to_node:  # find next unused io index
            io_index = io_index + 1
        reuse_group = keras_layer.name  # by the layer name we can gather nodes of this reused layer
        node_name = keras_layer.name + REUSED_IDENTIFIER + str(io_index)
    else:
        io_index = 0  # for non reused layers input/output index is 0
        reuse_group = None
        node_name = keras_layer.name
    input_shape = keras_layer.get_input_shape_at(io_index)
    output_shape = keras_layer.get_output_shape_at(io_index)

    if layer_class in [TFOpLambda, SlicingOpLambda]:
        # Some functional ops (such as tf.concat) should receive the input tensors as a list
        # and some are not (such as tf.multiply), so each FunctionalNode holds
        # a flag to indicate that.
        inputs_as_list = __is_functional_inputs_a_list(op_call_args)

        kwarg2index = get_kwargs2index(keras_layer.function)

        # Functional nodes do not have weights, but may have constants in their call_args and\or
        # call kwargs. Therefore, we extract these constants and save them in the node's weights as
        # positional weights. Positional weights are weights whose keys are the index of that constant
        # in the call_args.
        # All KerasTensor and positional weights are removed from the call_args\kwargs. They are restored
        # in the model builder.
        if len(weights) > 0:
            Logger.error('Functional nodes are not expected to have weights in framework')

        # read weights from call args
        for i, arg in enumerate(op_call_args[0] if inputs_as_list else op_call_args):
            if is_const(arg) or (keras_layer.function is tf.matmul and
                                 isinstance(arg, (tuple, list))):
                weights.update({i: to_numpy(arg, is_single_tensor=True)})
        # remove weights and KerasTensors and weights from op_call_args
        if inputs_as_list:
            op_call_args = tuple(op_call_args[1:])
        else:
            op_call_args = tuple([a for i, a in enumerate(op_call_args)
                                  if not(i in weights or is_tensor(a))])

        # read weights from call kwargs
        weight_keys = []
        for k, v in op_call_kwargs.items():
            if is_const(v) or (keras_layer.function is tf.matmul and
                               isinstance(v, (tuple, list))):
                weights.update({kwarg2index[k]: to_numpy(v, is_single_tensor=True)})
                weight_keys.append(k)
        # remove weights and KerasTensors and weights from op_call_kwargs
        op_call_kwargs = {k: v for k, v in op_call_kwargs.items()
                          if not(kwarg2index.get(k) in weights or is_tensor(v))}

        node = FunctionalNode(node_name,
                              layer_config,
                              input_shape,
                              output_shape,
                              weights,
                              layer_class,
                              op_call_args,
                              op_call_kwargs,
                              is_reused,
                              reuse_group,
                              functional_op=keras_layer.function,
                              inputs_as_list=inputs_as_list)
    else:
        # Read constant weights from layers such as layers.Add
        if len(op_call_args) > 0 and isinstance(op_call_args[0], (list, tuple)):
            for i, arg in enumerate(op_call_args[0]):
                if is_const(arg):
                    weights.update({i: to_numpy(arg, is_single_tensor=True)})

        node = BaseNode(node_name,
                        layer_config,
                        input_shape,
                        output_shape,
                        weights,
                        layer_class,
                        is_reused,
                        reuse_group,
                        is_custom=is_keras_custom_layer(layer_class))

    node_name_to_node[node_name] = node
    return node


def __is_functional_inputs_a_list(op_call_args: Any) -> bool:
    """
    Check whether the input tensors should be passed as a list
    or not.

    Args:
        op_call_args: Arguments list to check.

    Returns:
        Whether the input tensors should be passed as a list or not.
    """

    if len(op_call_args) > 0 and isinstance(op_call_args[0], list):
        inputs_as_list = True
        for arg in op_call_args[0]:
            inputs_as_list = inputs_as_list and (is_tensor(arg) or is_const(arg))
        return inputs_as_list
    return False
