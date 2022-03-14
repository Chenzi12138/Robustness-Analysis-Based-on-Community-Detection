"""
# File       : CEA.py
# Time       ：2022/3/11 21:27
# Author     ：Ming
"""
import networkx as nx
import numpy as np
from typing import Union

from matplotlib import pyplot as plt

from find_top_k_edge import find_top_k_com_edge
from build_community_graph import build_origin_network, build_community_graph, get_community_partition


def get_sum_degree_of_edge(graph: nx.Graph, edge: Union[tuple, list]) -> int:
    return graph.degree(edge[0]) + graph.degree(edge[1])


def CEA(origin_graph: nx.Graph, community_graph: nx.Graph) -> list:
    edge_attacks = []
    come_edges = community_graph.edges()
    while come_edges:
        top_edge = find_top_k_com_edge(community_graph, 1)
        print("top edge", top_edge)
        origin_edges = community_graph.edges()[top_edge[0]]["outer_edge"]
        # TODO: 检查下outer_edge是不是全部都存在，可能存在不是原始网络中的边的现象
        while origin_edges:
            degree_sequence = [get_sum_degree_of_edge(
                origin_graph, edge) for edge in origin_edges]
            e = origin_edges[np.argmax(degree_sequence)]
            if e not in edge_attacks:
                edge_attacks.append(e)
            origin_edges.remove(e)
        # pos = nx.spring_layout(community_graph)
        # labels = nx.get_node_attributes(community_graph, "id")
        # nx.draw_networkx_nodes(community_graph, pos=pos, cmap=plt.get_cmap('Wistia'))
        # nx.draw_networkx_edges(community_graph, pos=pos, width=2, alpha=0.8)
        # nx.draw_networkx_labels(community_graph, pos=pos, labels=labels)
        # plt.show()
        community_graph.remove_edge(top_edge[0][0], top_edge[0][1])
    # 将剩余的边按照sum degree进行排序
    nodes = community_graph.nodes()
    remained_edges = []
    for i in list(nodes):
        edge_list = nodes()[i]["inner_edge"]
        for edge in edge_list:
            remained_edges.append(edge)
    remained_sum_degree = [get_sum_degree_of_edge(
        origin_graph, edge) for edge in remained_edges]
    remained_edges_order = np.argsort(remained_sum_degree)
    ordered_edges = []
    for i in remained_edges_order:
        ordered_edges.append(list(remained_edges[i]))
    edge_attacks.extend(ordered_edges)
    return edge_attacks


# origin_graph = build_origin_network(
#     r"D:\File\Paper\毕业论文\code\第四章实验\算法demo\Adj.csv")
# community = get_community_partition(
#     r"D:\File\Paper\毕业论文\code\第四章实验\算法demo\community label.csv")
# com_graph = build_community_graph(origin_graph, community)
#
#
# attack = CEA(origin_graph=origin_graph, community_graph=com_graph)
# print(len(origin_graph.edges()))
# print(len(attack))
# print(attack)
#
#
# for edge in attack:
#     origin_graph.remove_edge(edge[0], edge[1])
# pos = nx.spring_layout(origin_graph)
# nx.draw(origin_graph,pos=pos)
# plt.show()
