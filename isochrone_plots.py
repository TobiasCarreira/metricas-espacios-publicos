import osmnx as ox
import networkx as nx
from networkx.classes.multidigraph import MultiDiGraph

class IsochronePlots:
    def __init__(self, trip_times: list):
        self.trip_times = trip_times
    
    def colors(self) -> list:
        self.colors = ox.plot.get_colors(
            n=len(self.trip_times),
            cmap="plasma",
            start=0,
            return_hex=True)
        return self.colors

    def plot_node_isochrones(self,G: MultiDiGraph ,center_node: int) -> None:
        node_colors = {}
        for trip_time, color in zip(sorted(self.trip_times, reverse=True), self.colors):
            subgraph = nx.ego_graph(G, center_node, radius=trip_time, distance="time")
            for node in subgraph.nodes():
                node_colors[node] = color
        nc = [node_colors[node] if node in node_colors else "none" for node in G.nodes()]
        ns = [15 if node in node_colors else 0 for node in G.nodes()]
        fig, ax = ox.plot_graph(
            G,
            node_color=nc,
            node_size=ns,
            node_alpha=0.8,
            edge_linewidth=0.2,
            edge_color="#999999",
        )
