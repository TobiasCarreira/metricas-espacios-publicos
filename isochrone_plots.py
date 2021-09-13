import geopandas as gpd
import osmnx as ox
import networkx as nx
from networkx.classes.multidigraph import MultiDiGraph
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import Point

class IsochronePlots:
    INFINITY = 10000
    
    def __init__(self, trip_times: list):
        self.trip_times = trip_times
    
    def get_colors(self) -> list:
        return ox.plot.get_colors(
            n=len(self.trip_times),
            cmap="plasma",
            start=0,
            return_hex=True)
            
    def get_color_map(self):
        color_list = self.get_colors()
        color_map = {trip_time: color_list[idx] for idx, trip_time in enumerate(sorted(self.trip_times, reverse=True))}
        color_map[self.INFINITY] = "none"
        return color_map

    def plot_node_isochrones_from_list(self, G, center_node_list):
        minimum_trip_times = self.sub_graphs_for_trip_times_from_list(G, center_node_list)
        colors = self.get_color_map()
        nc = [colors[minimum_trip_times[node]] for node in G.nodes()]
        ns = [0 if minimum_trip_times[node] == self.INFINITY else 15 for node in G.nodes()]
        fig, ax = ox.plot_graph(
            G,
            node_color=nc,
            node_size=ns,
            node_alpha=0.4,
            edge_linewidth=0.2,
            edge_color="#999999",
        )
            
    def sub_graphs_for_trip_times_from_list(self, G, center_node_list):
        minimum_trip_times = {node_id: self.INFINITY for node_id in list(G.nodes())}
        for center_node in center_node_list:
            new_trip_times = self.sub_graphs_for_trip_times(G, center_node)
            for node_id, new_time in new_trip_times.items():
                minimum_trip_times[node_id] = min(minimum_trip_times[node_id], new_time)
        return minimum_trip_times
            
    def sub_graphs_for_trip_times(self, G, center_node):
        minimum_trip_times = {node_id: self.INFINITY for node_id in list(G.nodes())}
        for trip_time in sorted(self.trip_times, reverse=True):
            subgraph = nx.ego_graph(G, center_node, radius=trip_time, distance="time")
            for node, data in subgraph.nodes(data=True):
                minimum_trip_times[node] = trip_time
        return minimum_trip_times

    def plot_node_isochrones(self,G: MultiDiGraph ,center_node: int) -> None:
        node_colors = {}
        for trip_time, color in zip(sorted(self.trip_times, reverse=True), self.get_colors()):
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

    def convex_hulls_for_trip_times(self, G, center_node):
        isochrone_polys = []
        for trip_time in sorted(self.trip_times, reverse=True):
            subgraph = nx.ego_graph(G, center_node, radius=trip_time, distance="time")
            node_points = [Point((data["x"], data["y"])) for node, data in subgraph.nodes(data=True)]
            bounding_poly = gpd.GeoSeries(node_points).unary_union.convex_hull
            isochrone_polys.append(bounding_poly)
        return isochrone_polys
        
    def plot_convex_hull_isochrones(self, G, center_node):
        isochrone_polys = self.convex_hulls_for_trip_times(G, center_node)
        fig, ax = ox.plot_graph(
            G, show=False, close=False, edge_color="#999999", edge_alpha=0.2, node_size=0
        )
        for polygon, fc in zip(isochrone_polys, self.get_colors()):
            patch = PolygonPatch(polygon, fc=fc, ec="none", alpha=0.6, zorder=-1)
            ax.add_patch(patch)
        plt.show()
