import igraph as ig
from typing import Dict


def generate(data: Dict, layout_algorithm: str = "fr"):
    """
    generate an igraph.Graph from the given imports (dict).
    :param data: dictionary of list of strings to generate nodes and edges from.
    :param layout_algorithm: string describing what kind of layout algorithm to use..
    see https://igraph.org/python/doc/tutorial/tutorial.html#layout-algorithms for further info.
    """
    g = ig.Graph(directed=True)
    add_nodes(data=data, graph=g)
    add_edges(data=data, graph=g)
    # g.vs["label"] = g.vs["name"]
    layout = g.layout(layout_algorithm)
    ig.plot(
        g, bbox=(1000, 1000), layout=layout,
        margin=50, vertex_size=7, edge_arrow_size=0.5,
        vertex_label_size=10,
    )


def add_nodes(data: Dict, graph: ig.Graph):
    """

    :param data:
    :param graph:
    :return:
    """
    for source in data:
        add_node(data=source, graph=graph)


def add_node(data: str, graph: ig.Graph):
    """

    :param data:
    :param graph:
    :return:
    """
    graph.add_vertex(name=data)


def add_edges(data: Dict, graph: ig.Graph):
    """

    :param data:
    :param graph:
    :return:
    """
    for source, targets in data.items():
        for target in targets:
            graph.add_edge(
                source=source,
                target=target,
            )
