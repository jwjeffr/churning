from pathlib import Path
import json

import networkx as nx
from pyvis.network import Network


def main():

    G = nx.DiGraph()

    with Path("relationships.json").open("r") as f:
        relationships = json.load(f)["relationships"]
    for source, target, label in relationships:
        G.add_edge(source, target, label=label)

    net = Network(
        height="600px",
        width="100%",
        bgcolor="#ffffff",
        font_color="black",
        directed=True,
    )
    net.set_options(
        """
        {
          "physics": {
            "enabled": false
          }
        }
        """
    )
    net.from_nx(G)
    nodes_by_id = {node["id"]: node for node in net.nodes}
    left_nodes = {"Award flights", "Alaska status credit"}
    head_order = {
      "Rent": 0,
      "Alaska Airlines Visa": 1,
      "Alaska Airlines": 2,
    }
    vertical_spacing = 240
    horizontal_spacing = 360

    for level, generation in enumerate(nx.topological_generations(G)):
      generation_nodes = sorted(
        generation,
        key=lambda node_id: (
          head_order.get(node_id, len(head_order)),
          node_id not in left_nodes,
          node_id,
        ),
      )
      for position, node_id in enumerate(generation_nodes):
        node = nodes_by_id[node_id]
        node["x"] = (
          -500
          if node_id in left_nodes
          else (position - (len(generation_nodes) - 1) / 2) * horizontal_spacing
        )
        node["y"] = level * vertical_spacing
        node["fixed"] = False

    for node in net.nodes:
        node["shape"] = "box"
        node["margin"] = 10
        node["font"] = {"color": "black", "size": 14}
    path_to_save = Path("_build")
    path_to_save.mkdir(parents=True, exist_ok=True)
    net.save_graph(str(path_to_save / "index.html"))


if __name__ == "__main__":

    main()
