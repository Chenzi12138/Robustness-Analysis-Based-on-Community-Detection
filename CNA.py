import networkx as nx
import numpy as np
from typing import Union

from matplotlib import pyplot as plt

from find_top_k_edge import find_top_k_com_edge
from build_community_graph import build_origin_network, build_community_graph, get_community_partition


def get_node_from_edge(edge: Union[tuple, list]) -> list:
    return [edge[0], edge[1]]


def CNA(origin_graph: nx.Graph, community_graph: nx.Graph) -> list:
    node_attacks = []
    com_edges = community_graph.edges()
    while com_edges:
        top_edge = find_top_k_com_edge(community_graph, 1)
        # print("top edge",top_edge)
        origin_nodes = community_graph.nodes()[get_node_from_edge(
            *top_edge)[0]]["inner_node"] + community_graph.nodes()[get_node_from_edge(*top_edge)[1]]["inner_node"]
        while origin_nodes:
            degree_sequence = [origin_graph.degree(i) for i in origin_nodes]
            v = origin_nodes[np.argmax(degree_sequence)]
            if v not in node_attacks:
                node_attacks.append(v)
            origin_nodes.remove(v)
        # pos = nx.spring_layout(community_graph)
        # labels = nx.get_node_attributes(community_graph, "id")
        # nx.draw_networkx_nodes(community_graph, pos=pos, cmap=plt.get_cmap('Wistia'))
        # nx.draw_networkx_edges(community_graph, pos=pos, width=2, alpha=0.8)
        # nx.draw_networkx_labels(community_graph, pos=pos, labels=labels)
        # plt.show()
        community_graph.remove_edge(top_edge[0][0], top_edge[0][1])
        # com_edges = community_graph.edges()
    # 将剩余的节点按照节点度大小进行排序
    nodes = origin_graph.nodes()
    remained_nodes = set(nodes).difference(set(node_attacks))
    remained_degree = [origin_graph.degree(i) for i in remained_nodes]
    remained_nodes_order = np.argsort(remained_degree)
    ordered_nodes = []
    for i in remained_nodes_order:
        ordered_nodes.append(i)
    node_attacks.extend(ordered_nodes)
    return node_attacks


# origin_graph = build_origin_network(
#     r"D:\File\Paper\毕业论文\code\第四章实验\算法demo\Adj.csv")
# community = get_community_partition(
#     r"D:\File\Paper\毕业论文\code\第四章实验\算法demo\community label.csv")
# com_graph = build_community_graph(origin_graph, community)
#
# # print(list(com_graph.edges()))
#
# # print(find_top_k_com_edge(com_graph,1))
#
# attack = CNA(origin_graph=origin_graph,community_graph=com_graph)
# print(len(origin_graph.nodes()))
# print(len(attack))
# print(len(set(attack)))
# print(attack)
