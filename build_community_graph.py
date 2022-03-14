import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# 原始网络
def build_origin_network(adj_path: str) -> nx.Graph:
    adj = np.loadtxt(adj_path, delimiter=',')
    for i in range(len(adj)):
        if adj[i][i]:
            adj[i][i] = 0
    graph = nx.from_numpy_array(adj)
    return graph


def get_community_partition(file_path: str) -> list:
    return list(np.loadtxt(file_path, delimiter=',', dtype=int))


def plot_community(graph: nx.Graph, node_label: list) -> None:
    nx.draw_spring(graph, cmap=plt.get_cmap("jet"), node_color=node_label)
    plt.show()


# 获取每个社区内部节点编号
def get_all_inner_node(graph: nx.Graph, labels: list) -> list:
    """获取每个社区内部的节点

    Args:
        graph (nx.Graph): 图
        labels (list): 图中每个节点的社区编号

    Returns:
        list: 图中每个社区内部节点列表
    """
    inner_node_list = []
    for i in range(int(max(labels))+1):
        node_list = []
        for j in range(len(labels)):
            if labels[j] == i:
                node_list.append(j)
        inner_node_list.append(node_list)
    return inner_node_list


# 获取社区内部的边
def get_inner_edge(graph: nx.Graph, inner_node: list) -> list:
    """获取社区内部的边

    Args:
        graph (nx.Graph): 图
        inner_node (list): 社区内部的节点

    Returns:
        list: 社区内部的边列表
    """
    inner_edge_list = []
    for i in range(len(inner_node)):
        for j in range(i+1, len(inner_node)):
            if graph.has_edge(inner_node[i], inner_node[j]):
                inner_edge_list.append([inner_node[i], inner_node[j]])
    return inner_edge_list


# 获取所有社区内部的边
def get_all_inner_edge(graph: nx.Graph, labels: list) -> list:
    """获取所有社区内部的边

    Args:
        graph (nx.Graph): 图
        labels (list): 图中每个节点所属的社区

    Returns:
        list: 图中所有社区内部的边
    """
    inner_node_list = get_all_inner_node(graph, labels)
    all_innner_edge_list = []
    for i in range(len(inner_node_list)):
        all_innner_edge_list.append(get_inner_edge(graph, inner_node_list[i]))
    return all_innner_edge_list

# 获取给定两个社区之间的边


def get_outer_edge(graph: nx.Graph, com1_inner_node: list, com2_inner_node: list) -> list:
    """获取给定两个社区之间的边

    Args:
        graph (nx.Graph): 图
        com1_inner_node (list): 社区1内部节点 
        com2_inner_node (list): 社区2内部节点

    Returns:
        list: 社区1与社区2之间的边
    """
    outer_edge_list = []
    for i in range(len(com1_inner_node)):
        for j in range(len(com2_inner_node)):
            if graph.has_edge(com1_inner_node[i], com2_inner_node[j]):
                outer_edge_list.append(
                    [com1_inner_node[i], com2_inner_node[j]])
    return outer_edge_list

# 构建社区图


def build_community_graph(origin_graph: nx.Graph, community_partition: list) -> nx.Graph:
    inner_node_list = get_all_inner_node(origin_graph, community_partition)
    inner_edge_list = get_all_inner_edge(origin_graph, community_partition)
    com_graph = nx.Graph()
    community_number = max(community_partition) + 1
    for i in range(community_number):
        com_graph.add_node(
            i, inner_node=inner_node_list[i], inner_edge=inner_edge_list[i],id=i)
    # 如果原始图中两个社区之间有边，则社区图中添加对应的边
    for i in range(community_number):
        for j in range(i+1, community_number):
            outer_edge_list = get_outer_edge(
                origin_graph, inner_node_list[i], inner_node_list[j])
            if outer_edge_list:
                com_graph.add_edge(i, j, outer_edge=outer_edge_list)
    return com_graph


def wtest():
    origin_graph = build_origin_network(
        r"D:\File\Paper\毕业论文\code\第四章实验\算法demo\Adj.csv")
    # nx.draw(origin_graph)
    community_partition = get_community_partition(
        r"D:\File\Paper\毕业论文\code\第四章实验\算法demo\community label.csv")
    # print(community_partition)
    # plot_community(origin_graph, community_partition)
    com_graph = build_community_graph(origin_graph, community_partition)
    labels = nx.get_node_attributes(com_graph, "id")
    pos = nx.spring_layout(com_graph)
    nx.draw_networkx_nodes(com_graph, pos=pos, cmap=plt.get_cmap('Wistia'))
    nx.draw_networkx_edges(com_graph, pos=pos, width=2, alpha=0.8)
    nx.draw_networkx_labels(com_graph, pos=pos, labels=labels)
    print(com_graph.edges())
    plt.show()


# wtest()
