import networkx as nx
import numpy as np


def find_top_k_com_edge(community_graph: nx.Graph, k: int) -> list:
    """寻找到社区图中权重最高的k个边

    Args:
        community_graph (nx.Graph): 社区图
        k (int): top k

    Returns:
        list: 返回社区图中权重最高的k个边列表
    """
    weights = [0] * len(community_graph.edges())
    sizes = [0] * len(community_graph.nodes())
    for i in range(len(community_graph.nodes())):
        sizes[i] = len(community_graph.nodes()[i]["inner_node"])
    apsp = nx.all_pairs_shortest_path(community_graph)
    for s, sp in apsp:
        for t in sp:
            if s == t:
                break
            #     用于在寻找最短路径时排除掉孤立点（好宝宝想出来的）
            factor = sizes[s] * sizes[t]
            for e in sp[t]:
                weights[e] += factor
    top_k = np.argmax(weights)
    return [list(community_graph.edges())[top_k]]
    # top_k = np.argsort(weights)[:k]
    # top_k_edge_list = []
    # for i in top_k:
    #     top_k_edge_list.append(list(community_graph.edges())[i])
    # return top_k_edge_list
