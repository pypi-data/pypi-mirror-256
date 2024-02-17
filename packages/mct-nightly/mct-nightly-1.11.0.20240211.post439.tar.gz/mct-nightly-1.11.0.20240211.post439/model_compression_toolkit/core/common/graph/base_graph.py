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
from collections import namedtuple

from copy import copy, deepcopy
from typing import List, Tuple, Any

import networkx as nx
import numpy as np

from networkx.algorithms.dag import topological_sort

from model_compression_toolkit.core.common.framework_info import FrameworkInfo
from model_compression_toolkit.core.common.graph.edge import EDGE_SINK_INDEX, EDGE_SOURCE_INDEX
from model_compression_toolkit.core.common.graph.edge import Edge, convert_to_edge
from model_compression_toolkit.core.common.graph.graph_searches import GraphSearches
from model_compression_toolkit.core.common.graph.base_node import BaseNode
from model_compression_toolkit.core.common.collectors.statistics_collector import BaseStatsCollector
from model_compression_toolkit.core.common.collectors.statistics_collector import scale_statistics, shift_statistics
from model_compression_toolkit.core.common.pruning.pruning_section import PruningSection
from model_compression_toolkit.core.common.user_info import UserInformation
from model_compression_toolkit.logger import Logger
from model_compression_toolkit.target_platform_capabilities.target_platform.targetplatform2framework import \
    TargetPlatformCapabilities, LayerFilterParams

OutTensor = namedtuple('OutTensor', 'node node_out_index')


class Graph(nx.MultiDiGraph, GraphSearches):
    """
    Base graph representing a model to be optimized.
    """

    def __init__(self,
                 name: str,
                 nodes: List[BaseNode],
                 input_nodes: List[BaseNode],
                 output_nodes: List[OutTensor],
                 edge_list: List[Edge],
                 fw_info: FrameworkInfo = None,
                 **attr):
        """
        Args:
            nodes: List of nodes the graph has.
            input_nodes: List of input nodes the model
            output_nodes: List of output nodes of the model to a list of their output indices.
            edge_list: List of edges the graph has between nodes.
            fw_info: FrameworkInfo object (needed for computing the graph's weights memory).
            **attr: Attributes to add to graph as key=value pairs.
        """

        super().__init__(**attr)
        self.name = name
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        self.node_to_out_stats_collector = dict()
        self.node_to_in_stats_collector = dict()
        self.add_nodes_from(nodes)
        for e in edge_list:
            self.add_edge(e.source_node,
                          e.sink_node,
                          **e.get_attributes())
        self.user_info = UserInformation()
        self.fw_info = fw_info
        self.fused_nodes = []

    def set_fw_info(self,
                    fw_info: FrameworkInfo):
        """
        Set the graph's framework info.
        Args:
            fw_info: FrameworkInfo object.
        """

        self.fw_info = fw_info

    def set_tpc(self,
                tpc: TargetPlatformCapabilities):
        """
        Set the graph's TPC.
        Args:
            tpc: TargetPlatformCapabilities object.
        """
        # validate graph nodes are either from the framework or a custom layer defined in the TPC
        # Validate graph nodes are either built-in layers from the framework or custom layers defined in the TPC
        tpc_layers = tpc.op_sets_to_layers.get_layers()
        tpc_filtered_layers = [layer for layer in tpc_layers if isinstance(layer, LayerFilterParams)]
        for n in self.nodes:
            is_node_in_tpc = n.type in tpc_layers or any([n.is_match_filter_params(filtered_layer)
                                                          for filtered_layer in tpc_filtered_layers])
            if n.is_custom:
                if not is_node_in_tpc:
                    Logger.error(f'MCT does not support optimizing Keras custom layers, but found layer of type {n.type}. '
                                 f'Please add the custom layer to TPC or file a feature request or an issue if you believe this is an issue.')
                if any([qc.default_weight_attr_config.enable_weights_quantization for qc in n.get_qco(tpc).quantization_config_list]):
                    Logger.error(f'MCT does not support optimizing Keras custom layers with weights quantization. Layer: {n.type}')

        self.tpc = tpc

    def get_topo_sorted_nodes(self):
        """
        Returns: a list of toposorted nodes.
        """

        return list(nx.algorithms.dag.topological_sort(self))

    def get_op_list(self) -> np.ndarray:
        """
        Returns: Set of operators in the graph.
        """

        return np.unique([n.op for n in self.nodes()])

    def get_inputs(self) -> List[BaseNode]:
        """
        Returns: List containing the model input nodes.
        """

        return self.input_nodes

    def get_outputs(self) -> List[OutTensor]:
        """
        Returns: Dictionary containing the model output nodes.
        """

        return self.output_nodes

    def set_inputs(self,
                   input_nodes: List[BaseNode]):
        """
        Set the graph inputs dictionary.
        Args:
            input_nodes: List of the model's inputs.
        """

        self.input_nodes = input_nodes

    def set_outputs(self,
                    output_nodes: List[OutTensor]):
        """
        Set the graph outputs dictionary.
        Args:
            output_nodes: Dictionary of the model's outputs.
        """

        self.output_nodes = output_nodes

    def set_out_stats_collector_to_node(self,
                                        n: BaseNode,
                                        stats_collector: BaseStatsCollector):
        """
        Set an output statistics collector of a node in the graph, and set this statistics collector as an input
        statistics collector of nodes next to this given node.

        Args:
            n: Node to set its output statistics collector.
            stats_collector: Output statistics collector to collect the node's output statistics.
        """

        n_outputs = 1 if isinstance(n.output_shape, tuple) else len(n.output_shape)

        if n_outputs != 1:  # Node has multiple outputs
            stats_collectors = [deepcopy(stats_collector) for i in
                                range(n_outputs)]  # Create multiple tensors to attach to each next
            # node
            out_edges = self.out_edges(n, sort_by_attr=EDGE_SOURCE_INDEX)
            for sc, oe in zip(stats_collectors, out_edges):  # Attach to each next node an input tensor
                in_nodes = [e.source_node for e in self.incoming_edges(oe.sink_node,
                                                                       sort_by_attr=EDGE_SINK_INDEX)]
                if len(in_nodes) != 1:  # Next node has multiple in_nodes (besides the passed node)
                    # so self.input_tensors_dict[dst_node] should be a list of tensors
                    if oe.sink_node not in self.node_to_in_stats_collector:
                        # first visit: init tensors list as a list of Nones
                        self.node_to_in_stats_collector.update({oe.sink_node: [None] * len(in_nodes)})
                    self.node_to_in_stats_collector[oe.sink_node][in_nodes.index(n)] = sc

                else:
                    self.node_to_in_stats_collector.update({oe.sink_node: sc})
            self.node_to_out_stats_collector.update(
                {n: stats_collectors})  # Attach the passed node a list of output tensors

        else:
            self.node_to_out_stats_collector.update({n: stats_collector})
            for oe in self.out_edges(n):
                in_nodes = [e.source_node for e in self.incoming_edges(oe.sink_node,
                                                                       sort_by_attr=EDGE_SINK_INDEX)]
                if len(in_nodes) != 1:  # Next node has multiple in_nodes (besides the passed node)
                    # so self.input_tensors_dict[dst_node] should be a list of tensors
                    if oe.sink_node not in self.node_to_in_stats_collector:
                        # first visit: init tensors list as a list of Nones
                        self.node_to_in_stats_collector.update({oe.sink_node: [None] * len(in_nodes)})
                    self.node_to_in_stats_collector[oe.sink_node][in_nodes.index(n)] = stats_collector

                else:
                    self.node_to_in_stats_collector.update({oe.sink_node: stats_collector})

    def get_out_stats_collector(self,
                                n: BaseNode) -> BaseStatsCollector:
        """
        Get the output statistics collector of a node containing output statistics of the node.
        Args:
            n: Node to get its output statistics collector.

        Returns:
            Tensor containing output statistics of the node.
        """
        return self.node_to_out_stats_collector.get(n)

    def get_in_stats_collector(self,
                               n: BaseNode) -> BaseStatsCollector:
        """
        Get the input statistics collector of a node containing input statistics of the node.
        Args:
            n: Node to get its input statistics collector.

        Returns:
            Statistics collector containing input statistics of the node.
        """

        sc = self.node_to_in_stats_collector.get(n)
        if sc is None:
            Logger.error(f'Input statistics collector of node {n.name} is None')  # pragma: no cover
        return sc

    def scale_stats_collector(self,
                              node: BaseNode,
                              scale_factor: np.ndarray):
        """
        Scale the output statistics of a node in the graph by a given scaling factor.
        The scaling factor can be a single value (scale per-tensor) or multiple values (scale per-channel).
        This is done in place.

        Args:
            node: Node to scale its output statistics.
            scale_factor: Scale factor to use for the statistics scaling.

        """

        sc = self.get_out_stats_collector(node)
        scaled_sc = scale_statistics(sc, scale_factor)
        self.set_out_stats_collector_to_node(node, scaled_sc)

    def shift_stats_collector(self,
                              node: BaseNode,
                              shift_value: np.ndarray):
        """
        Shift the output statistics of a node in the graph by a given value.
        The shifting value can be a single value (shifting per-tensor) or multiple values (shifting per-channel).
        This is done in place.

        Args:
            node: Node to scale its output statistics.
            shift_value: Value to use for the statistics shifting.

        """

        sc = self.get_out_stats_collector(node)
        shifted_sc = shift_statistics(sc, shift_value)
        self.set_out_stats_collector_to_node(node, shifted_sc)

    def find_node_by_name(self,
                          name: str) -> List[BaseNode]:
        """
        Find and return a list of nodes by a name.

        Args:
            name: Name to find nodes in the graph by.

        Returns:
            List of nodes named
        """

        return [n for n in self.nodes if n.name == name]

    def get_next_nodes(self,
                       node_obj: BaseNode) -> List[BaseNode]:
        """
        Get next nodes (in a topological order) of a node.

        Args:
            node_obj: Node to get its next nodes.

        Returns:
            List of output nodes objects.

        """

        return [edges_list.sink_node for edges_list in self.out_edges(node_obj)]

    def get_prev_nodes(self,
                       node_obj: BaseNode,
                       sink_index_sorted: bool = False) -> List[BaseNode]:
        """
        Get previous nodes (in a topological order) of a node.

        Args:
            node_obj: Node to get its previous nodes.
            sink_index_sorted: Whether to sort the returned list by the sink_index of the edges.

        Returns:
            List of input nodes objects.

        """
        if sink_index_sorted:
            sort_attr = 'sink_index'
        else:
            sort_attr = None
        return [edges_list.source_node for edges_list in self.incoming_edges(node_obj, sort_by_attr=sort_attr)]

    def reconnect_out_edges(self,
                            current_node: BaseNode,
                            new_node: BaseNode):
        """
        Connect all outgoing edges of a node to be outgoing edges of a different node
        (useful when replacing a node during substitutions).

        Args:
            current_node: Node to reconnect its outgoing edges.
            new_node: Node to connect the outgoing edges of the current node to.
        """

        for oe in self.out_edges(current_node):
            self.add_edge(new_node, oe.sink_node, **oe.get_attributes())
            self.remove_edge(current_node, oe.sink_node)

    def reconnect_in_edges(self,
                           current_node: BaseNode,
                           new_node: BaseNode):
        """
        Connect all incoming edges of a node to be incoming edges of a different node
        (useful when replacing a node during substitutions).

        Args:
            current_node: Node to reconnect its incoming edges.
            new_node: Node to connect the incoming edges of the current node to.
        """

        for ie in self.incoming_edges(current_node):
            self.add_edge(ie.source_node, new_node, **ie.get_attributes())
            self.remove_edge(ie.source_node, current_node)

    def add_node_with_in_edges(self, new_node: BaseNode, input_nodes: List[BaseNode],
                               input_nodes_output_index: List[int] = []):
        """
        Add node to graph and connect it to its input nodes
        (useful when adding a node during substitutions).

        Args:
            new_node: Node to add.
            input_nodes: A list of new_node input nodes. The order is the sink_index of the edge
             between the input node and new_node
            input_nodes_output_index: A list output indices from input nodes. The order is the
             source_index of the edge. Deafult is an empty list which means all output indices
             are zero
        """

        if len(input_nodes_output_index) == 0:
            input_nodes_output_index = [0] * len(input_nodes)

        if len(input_nodes_output_index) != len(input_nodes):
            Logger.error('Graph.add_node_with_in_edges: input_nodes & input_nodes_output_index must be the same '
                         'length')  # pragma: no cover

        self.add_node(new_node)
        for sink_index, (in_node, source_index) in enumerate(zip(input_nodes, input_nodes_output_index)):
            self.add_edge(in_node, new_node, source_index=source_index, sink_index=sink_index)

    def replace_output_node(self,
                            current_node: BaseNode,
                            new_node: BaseNode):
        """
        If a node is being substituted with another node and it is an output node, the graph's outputs
        should be updated as well. This function takes care of it by going over the graph's outputs, and
        replacing the current output node with a new output node.
        If current node is not an output node, nothing gets changed.

        Args:
            current_node: Node that (possibly) is an output node.
            new_node: New node to set as an output node if the current node is an output node.

        """

        graph_outputs = self.get_outputs()
        new_graph_outputs = copy(graph_outputs)
        for graph_ot_index, ot in enumerate(graph_outputs):
            if current_node == ot.node:
                new_graph_outputs[graph_ot_index] = OutTensor(new_node, ot.node_out_index)
        self.set_outputs(new_graph_outputs)

    def replace_input_node(self,
                           current_node: BaseNode,
                           new_node: BaseNode):
        """
        If a node is being substituted with another node, and it is an input node, the graph's input
        should be updated as well. This function takes care of it by going over the graph's inputs, and
        replacing the current input node with a new input node.
        If current node is not an input node, nothing gets changed.

        Args:
            current_node: Node that (possibly) is an input node.
            new_node: New node to set as an input node if the current node is an input node.

        """
        if new_node is None:
            Logger.error("Graph received a None value as a new input node.")

        graph_inputs = self.get_inputs()
        new_graph_inputs = copy(graph_inputs)
        if current_node in graph_inputs:
            new_graph_inputs.remove(current_node)
            new_graph_inputs.append(new_node)
        self.set_inputs(new_graph_inputs)

    def remove_node(self,
                    node_to_remove: BaseNode,
                    new_graph_inputs: List[BaseNode] = None,
                    new_graph_outputs: List[OutTensor] = None):
        """
        Remove a node from the graph. A new inputs/outputs lists can be passed in case the node is currently an
        input/output of the graph. If the node is an input/output and a new list wasn't passed an error is logged.

        Args:
            node_to_remove: Node to remove from the graph.
            new_graph_inputs: An inputs list to set as the graph's inputs.
            new_graph_outputs: An outputs list to set as the graph's outputs.

        """

        output_nodes = [ot.node for ot in self.get_outputs()]  # get output nodes from namedtuples
        if node_to_remove in output_nodes:  # If node is in the graph's outputs, the outputs should be updated
            if new_graph_outputs is None:
                Logger.critical(
                    f'{node_to_remove.name} is in graph outputs, but new outputs were not given.')  # pragma: no cover
            self.set_outputs(new_graph_outputs)

        if node_to_remove in self.get_inputs():  # If node is in the graph's inputs, the inputs should be updated
            if new_graph_inputs is None:
                Logger.critical(
                    f'{node_to_remove.name} is in graph inputs, but new inputs were not given.')  # pragma: no cover
            self.set_inputs(new_graph_inputs)

        # Make sure there are no connected edges left to the node before removing it.
        assert len(
            self.incoming_edges(node_to_remove)) == 0, f'There are {len(self.incoming_edges(node_to_remove))} ' \
                                                       f'incoming ' \
                                                       f'edges to node {node_to_remove}, and they should be removed ' \
                                                       f'before deleting the node from the graph.'
        assert len(self.out_edges(node_to_remove)) == 0, f'There are {len(self.out_edges(node_to_remove))} outgoing ' \
                                                         f'edges to node {node_to_remove}, and they should be removed ' \
                                                         f'' \
                                                         f'' \
                                                         f'before deleting the node from the graph.'
        #  Remove node
        super().remove_node(node_to_remove)

    def incoming_edges(self,
                       n: BaseNode,
                       sort_by_attr: str = None) -> List[Edge]:
        """
        Get a list of incoming edges of a node. If sort_by_attr is passed, the returned list
        is sorted by that edge's attribute.

        Args:
            n: Node to get its incoming edges.
            sort_by_attr: Attribute to sort the edges by.

        Returns:
            List of incoming edges of the node. Each incoming edge is a tuple of:
            (source node, destination node, edge data)
        """

        input_edges = [convert_to_edge(e) for e in super().in_edges(n, data=True)]
        if sort_by_attr is not None:
            input_edges.sort(key=lambda e: getattr(e, sort_by_attr))
        return input_edges

    def out_edges(self,
                  n: BaseNode,
                  sort_by_attr: str = None) -> List[Edge]:
        """
        Get a list of outgoing edges of a node. If sort_by_attr is passed, the returned list
        is sorted by that edge's attribute.

        Args:
            n: Node to get its outgoing edges.
            sort_by_attr: Attribute to sort the edges by.

        Returns:
            List of outgoing edges of the node.
        """

        output_edges = [convert_to_edge(e) for e in super().edges(n, data=True)]
        if sort_by_attr is not None:
            output_edges.sort(key=lambda e: getattr(e, sort_by_attr))
        return output_edges

    def get_memory(self) -> float:
        """

        Returns: Total memory consumption of the graph in bytes.

        """
        memory = 0
        for n in self.nodes:
            memory += n.get_memory_bytes(self.fw_info)
        return memory

    def get_float_memory(self) -> float:
        """

        Returns: Total memory consumption of the float graph in bytes.

        """
        memory = 0
        for n in self.nodes:
            memory += n.get_float_memory_bytes(self.fw_info)
        return memory

    def get_configurable_sorted_nodes_names(self,
                                            include_reused_nodes: bool = False) -> List[str]:
        """
        Get a list of nodes' names that can be configured (namely, has one or
        more weight qc candidate). The names are sorted according to the topological
        order of the graph.

        Args:
            include_reused_nodes: Whether or not to include reused nodes (False by default).

        Returns: List of nodes' names that can be configured (namely, has one or
        more weight qc candidate) sorted topology.

        """
        sorted_names = [n.name for n in self.get_configurable_sorted_nodes(include_reused_nodes=include_reused_nodes)]
        return sorted_names

    def get_weights_configurable_nodes(self,
                                       include_reused_nodes: bool = False) -> List[BaseNode]:
        """
        Get a list of nodes that their weights can be configured (namely, has one or
        more weight qc candidate and their weights should be quantized).

        Args:
            include_reused_nodes: Whether to include reused nodes (False by default).

        Returns:
            A list of nodes that their weights can be configured (namely, has one or more weight qc candidate).
        """
        return list(filter(lambda n: n.is_weights_quantization_enabled()
                                     and not n.is_all_weights_candidates_equal()
                                     and (not n.reuse or include_reused_nodes), list(self)))

    def get_sorted_weights_configurable_nodes(self,
                                              include_reused_nodes: bool = False) -> List[BaseNode]:
        """
        Get a list of sorted nodes that their weights can be configured (namely, has one or
        more weight qc candidate and their weights should be quantized).

        Args:
            include_reused_nodes: Whether to include reused nodes (False by default).

        Returns:
            A list of nodes that their weights can be configured (namely, has one or more weight qc candidate)
            sorted topologically.
        """
        return self._sort_nodes_in_list(self.get_weights_configurable_nodes(include_reused_nodes))

    def get_activation_configurable_nodes(self) -> List[BaseNode]:
        """
        Get a list of nodes that their activation can be configured (namely, has one or
        more activation qc candidate and their activation should be quantized).

        Returns:
            A list of nodes that their activation can be configured (namely, has one or more activation qc candidate).
        """
        return list(filter(lambda n: n.is_activation_quantization_enabled()
                                     and not n.is_all_activation_candidates_equal(), list(self)))

    def get_sorted_activation_configurable_nodes(self) -> List[BaseNode]:
        """
        Get a sorted list of nodes that their activation can be configured (namely, has one or
        more activation qc candidate and their activation should be quantized).

        Returns:
            A list of nodes that their activation can be configured (namely, has one or more activation qc candidate)
            sorted topologically.
        """
        return self._sort_nodes_in_list(self.get_activation_configurable_nodes())

    def get_configurable_sorted_nodes(self,
                                      include_reused_nodes: bool = False) -> List[BaseNode]:
        """
        Get a list of nodes that can be configured (namely, has one or
        more qc candidate and their weights or activations should be quantized).
        The nodes are sorted according to the topological order of the graph.

        Args:
            include_reused_nodes: Whether or not to include reused nodes (False by default).

        Returns:
             A list of nodes that can be configured (namely, has one or more qc candidate) sorted topology.

        """
        weights_configurable_nodes = self.get_weights_configurable_nodes(include_reused_nodes)
        activation_configurable_nodes = self.get_activation_configurable_nodes()

        # combine and remove duplications
        configurable_nodes = list(set(weights_configurable_nodes + activation_configurable_nodes))

        return self._sort_nodes_in_list(configurable_nodes)

    def _sort_nodes_in_list(self, nodes_list: List[BaseNode]) -> List[BaseNode]:
        """
        Sorts a list of graph nodes according to the order of the nodes in the topological sort of the graph's nodes.

        Args:
            nodes_list: A list of nodes to sort.

        Returns: nodes_list sorted topologically.

        """
        sorted_configurable_nodes = []
        sorted_nodes = list(topological_sort(self))
        for n in sorted_nodes:
            if n in nodes_list:
                sorted_configurable_nodes.append(n)
        return sorted_configurable_nodes

    def get_min_candidates_config(self) -> List[int]:
        """
        Builds a minimal configuration.
        Note: we assume that a minimal configuration exists, i.e., each configurable node has exactly one candidate
            with minimal n_bits (in both weight and activation if both are quantized, or in the relevant one if only
            one of them is quantized)

        Returns: A list of candidate for each node (list on indices)
        """

        conf_sorted_nodes = self.get_configurable_sorted_nodes()
        min_cfg_candidates = [n.find_min_candidates_indices() for n in conf_sorted_nodes]  # list of lists of indices

        assert all([len(lst) == 1 for lst in min_cfg_candidates]), \
            f"A minimal config candidate must be defined, but some node have multiple potential minimal candidates"

        return [lst[0] for lst in min_cfg_candidates]

    def get_max_candidates_config(self) -> List[int]:
        """
        Builds a maximal configuration.
        Note: we assume that a maximal configuration exists, i.e., each configurable node has exactly one candidate
            with maximal n_bits (in both weight and activation if both are quantized, or in the relevant one if only
            one of them is quantized)

        Returns: A list of candidate for each node (list on indices)
        """

        conf_sorted_nodes = self.get_configurable_sorted_nodes()
        max_cfg_candidates = [n.find_max_candidates_indices() for n in conf_sorted_nodes]  # list of lists of indices

        assert all([len(lst) == 1 for lst in max_cfg_candidates]), \
            f"A maximal config candidate must be defined, but some node have multiple potential maximal candidates"

        return [lst[0] for lst in max_cfg_candidates]

    def get_final_weights_config(self) -> List[Tuple[BaseNode, int]]:
        """
        Gets the final number of bits for quantization of each weights' configurable layer.

        Returns: A list of pairs of (node type, node's weights quantization bitwidth).

        """
        sorted_conf_weights = self.get_sorted_weights_configurable_nodes()
        return [(n, n.final_weights_quantization_cfg.weights_n_bits) for n in sorted_conf_weights]

    def get_final_activation_config(self) -> List[Tuple[BaseNode, int]]:
        """
        Gets the final number of bits for quantization of each activation configurable layer.

        Returns: A list of pairs of (node type, nod's activation quantization bitwidth).

        """
        sorted_conf_activation = self.get_sorted_activation_configurable_nodes()
        return [(n, n.final_activation_quantization_cfg.activation_n_bits) for n in sorted_conf_activation]

    def update_fused_nodes(self, fusion: List[Any]):
        """
        Updates the graphs fusions list with a new list of nodes that have been fused.

        Args:
            fusion: A list of nodes that have been fused.

        """
        self.fused_nodes.append(fusion)

    def is_single_activation_cfg(self):
        """
        Checks whether all nodes in the graph that have activation quantization are quantized with the same bit-width.

        Returns: True if all quantization config candidates of all nodes have the same activation quantization bit-width.

        """
        return all([n.is_all_activation_candidates_equal() for n in self.nodes])

    def replace_node(self, node_to_replace: BaseNode, new_node: BaseNode):
        """
        Replaces a node in the graph with a new node.

        Args:
            node_to_replace: The node to replace.
            new_node: The new node to replace with.

        """
        self.add_node(new_node)
        self.reconnect_out_edges(node_to_replace, new_node)
        self.reconnect_in_edges(node_to_replace, new_node)
        self.replace_output_node(node_to_replace, new_node)
        self.replace_input_node(node_to_replace, new_node)
        self.remove_node(node_to_replace)

    def get_pruning_sections(self,
                             fw_impl: Any) -> List[PruningSection]:
        """
        Constructs pruning sections for a given computational graph.
        Each section is created starting from an entry node and includes intermediate and exit nodes.

        Args:
            fw_impl (PruningFrameworkImplementation): Implementation of specific framework methods required for pruning.

        Returns: List of PruningSection in the graph.
        """
        entry_nodes = self.get_pruning_sections_entry_nodes(fw_impl)
        return [self._create_pruning_section(entry_node,  fw_impl) for entry_node in entry_nodes]

    def get_pruning_sections_entry_nodes(self, fw_impl: Any) -> List[BaseNode]:
        """
        Identifies entry nodes for pruning sections within the graph.
        Traverses the graph in a topological order, checking each node for prunability criteria.
        Returns a list of nodes that mark the beginning of a prunable section in the graph.

        Args:
            fw_impl (PruningFrameworkImplementation): Implementation of specific framework methods required for pruning.

        Returns: List of nodes that are entry nodes in the pruning sections of the graph.

        """
        prunable_nodes = []
        for n in list(topological_sort(self)):
            if fw_impl.is_node_entry_node(n) and self._is_node_topology_prunable(n, fw_impl):
                prunable_nodes.append(n)
        return prunable_nodes

    def _is_node_topology_prunable(self, entry_node: BaseNode, fw_impl: Any) -> bool:
        """
        Determines if the topology starting from a given entry node is suitable for pruning.
        Iteratively examines the graph structure, focusing on node connectivity and pruning criteria.
        Returns True if the topology is prunable, False otherwise.

        Args:
            entry_node (BaseNode): The node to start the topology check from.
            fw_impl (PruningFrameworkImplementation): Implementation of specific framework methods required for pruning.

        Returns: Whether this node is a start of a pruning section according to the graph topology or not.

        """
        next_node = entry_node

        # Continue iterating until the conditions for prunability are no longer met
        while len(self.out_edges(next_node)) == 1:
            next_node = self.out_edges(next_node)[0].sink_node

            # If next_node is an exit node and has only one incoming edge, the topology is prunable.
            if fw_impl.is_node_exit_node(next_node, entry_node, self.fw_info) and len(self.in_edges(next_node)) == 1:
                return True

            # If the next node is not an intermediate node or has more than one incoming/outgoing edge,
            # stop the check.
            if not fw_impl.is_node_intermediate_pruning_section(next_node) or len(self.in_edges(next_node)) != 1 or len(self.out_edges(next_node)) != 1:
                return False

        # If the loop exits normally, it implies that the topology is not prunable
        return False


    def _create_pruning_section(self, entry_node: BaseNode, fw_impl: Any) -> PruningSection:
        """
        Creates a PruningSection object starting from a given entry node.
        Includes logic to find intermediate and exit nodes to complete the section.
        Ensures the provided entry node is a valid starting point for pruning.

        Args:
            entry_node (BaseNode): The entry node to create the section it starts.
            fw_impl (PruningFrameworkImplementation): Implementation of specific framework methods required for pruning.

        Returns: The pruning section that starts with node entry_node.

        """
        if not fw_impl.is_node_entry_node(entry_node):
            Logger.error(f"Expected to find an entry node to create its pruning section,"
                         f"but node {entry_node} is not an entry node.")

        intermediate_nodes, exit_node = self._find_intermediate_and_exit_nodes(entry_node, fw_impl)

        if not fw_impl.is_node_exit_node(exit_node, entry_node, self.fw_info):
            Logger.error(f"Expected to find exit node when creating a pruning section,"
                         f"but node {exit_node} is not an exit node.")

        return PruningSection(entry_node=entry_node,
                              intermediate_nodes=intermediate_nodes,
                              exit_node=exit_node)

    def _find_intermediate_and_exit_nodes(self, entry_node: BaseNode, fw_impl: Any) -> Tuple[List[BaseNode], BaseNode]:
        """
        Identifies intermediate and exit nodes for a pruning section starting from an entry node.
        Iterates through connected nodes to build the complete structure of the pruning section.

        Args:
            entry_node (BaseNode): An entry node to find the intermediate and exit nodes of its section.
            fw_impl (PruningFrameworkImplementation): Implementation of specific framework methods required for pruning.

        Returns: A tuple containing a list of intermediate nodes and the exit node.

        """
        intermediate_nodes = []
        next_node = self.out_edges(entry_node)[0].sink_node
        while not fw_impl.is_node_exit_node(next_node, entry_node, self.fw_info):
            intermediate_nodes.append(next_node)
            next_node = self.out_edges(next_node)[0].sink_node

        return intermediate_nodes, next_node


