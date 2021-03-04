"""
This module generates the network graph based on the python-igraph.
"""

from random import randrange, seed
from typing import Dict

import igraph as ig

from dependency_graph.constants import DISTINCT_COLOR_MAP

seed(42)


def generate(data: Dict, target: str, layout_algorithm: str = "fr", level: int = 0):
    """
    generate an igraph.Graph from the given imports (dict).
    :param data: dictionary of list of strings to generate nodes and edges from.
    :param target: target file to save resulting plot to. some of the possible extensions are: "pdf, svg, png".
    :param layout_algorithm: string describing what kind of layout algorithm to use.
    see https://igraph.org/python/doc/tutorial/tutorial.html#layout-algorithms for further info.
    :param level: import level in which to group nodes. on level 0 all nodes have the same color.
    e.g. this.is.my.module
    this -> level 0
    this.is -> level 1
    this.is.my -> level 2 ...
    """
    g = ig.Graph(directed=True)

    node_settings = {
        "size": 9,
        "label_size": 4,
    }
    add_nodes(data=data, graph=g, **node_settings)

    edge_settings = {
        "arrow_size": 0.5,
    }
    add_edges(data=data, graph=g, **edge_settings)

    post_creation_nodes_settings(data=data, graph=g, level=level)

    layout = g.layout(layout_algorithm)

    plot_settings = {"bbox": (1500, 1500), "layout": layout, "margin": 100}
    ig.plot(g, target=target, **plot_settings)


def add_nodes(data: Dict, graph: ig.Graph, **kwargs):
    """
    loop over the given data and create a lot of nodes inside the given graph
    :param data: dictionary containing nodes to create (each key = 1 node)
    :param graph: instance of igraph.Graph to create nodes in
    :param kwargs: keyword arguments that hold possible node settings
    """
    for source in data:
        add_node(name=source, graph=graph, **kwargs)


def add_node(name: str, graph: ig.Graph, **kwargs):
    """
    add a single node to the given graph. also pass given kwargs into it as settings.
    :param name: name of node to create
    :param graph: instance of igraph.Graph to create node in
    :param kwargs: keyword arguments that hold possible node settings
    """
    graph.add_vertex(name=name, **kwargs)


def add_edges(data: Dict, graph: ig.Graph, **kwargs):
    """
    loop over the given data and create a lot of edges inside the given graph
    :param data: dictionary containing information about every node and edge
    :param graph: instance of igraph.Graph to create edges in
    """
    for source, content in data.items():
        for target in content["targets"]:
            graph.add_edge(source=source, target=target, **kwargs)


def post_creation_nodes_settings(data: Dict, graph: ig.Graph, level: int = 0):
    """
    set and/or modify parameters of nodes after all have been created.
    :param data: dictionary containing information about every node and edge
    :param graph: instance of igraph.Graph to search for nodes to modify
    :param level: import level.
    """
    set_level_color(data=data, graph=graph, level=level)
    graph.vs["label"] = [name for name in graph.vs["name"]]  # set names

    for name, info in data.items():
        graph.vs.find(name)["label"] = name.replace(
            f"{info['levels'].get(level)}.",
            f"{info['levels'].get(level)}.\n",
        )

    for node in graph.vs:
        node["size"] += int(2.5 * len(node.in_edges()))


def set_level_color(data: Dict, graph: ig.Graph, level: int):
    """
    set color for every node depending on the desired level.
    uses DISTINCT_COLOR_MAP from constants.py.
    in case more colors than available are desired, generate random ones on the fly.
    :param data: dictionary containing information about every node and edge
    :param graph: instance of igraph.Graph to search for nodes to modify
    :param level: import level.
    """
    levels = list(set([info["levels"].get(level) for info in data.values()]))
    color_map = {
        level: DISTINCT_COLOR_MAP[num]
        if num < len(DISTINCT_COLOR_MAP)
        else random_color_generator()
        for num, level in enumerate(levels)
    }

    for node, info in data.items():
        graph.vs.find(node)["color"] = color_map[info["levels"].get(level)]


def random_color_generator():
    """
    creates and returns a random color.
    :return: string in hex format (e.g. #15ff0c)
    """
    return "#%02X%02X%02X" % (
        randrange(256),
        randrange(256),
        randrange(256),
    )
