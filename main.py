from pathlib import Path
import json

import networkx as nx
from pyvis.network import Network


def main():

    G = nx.Graph()

    with Path("relationships.json").open("r") as f:
        relationships = json.load(f)["relationships"]
    G.add_edges_from(relationships)

    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    net.from_nx(G)
    net.force_atlas_2based()
    path_to_save = Path("_build")
    path_to_save.mkdir(parents=True, exist_ok=True)
    net.save_graph(str(path_to_save / "index.html"))


if __name__ == "__main__":

    main()
