import osmnx as ox
from random import randrange

class GraphBuilder:
    """
    Builds a graph of a given city with all the needed data (nodes, POIs, distance between those
    measured in time units given a transport mode). It also provides a few useful methods to handle
    said graph.
    """

    def __init__(self, place, transportation_mode, travel_speed):
        """
        Initialized an empty graph. It's gonna use the following parameters to actually
        process it:

        place : str
            city name
        transportation_mode : str
            transportation mode code
        travel_speed : float
            in km/h
        """
        self.place = place
        self.transportation_mode = transportation_mode
        self.travel_speed = travel_speed # in km/h
        self.graph = None

    def initialize_graph(self):
        """
        Initialize graph by downloading it form OSM database with the adequate parameters.
        """
        self.graph = ox.graph_from_place(
            self.place,
            network_type=self.transportation_mode
        )
        return self.graph

    def calculate_centroid(self):
        """
        Calculates centroid of the whole graph.
        """
        gdf_nodes = ox.graph_to_gdfs(self.graph, edges=False)
        x, y = gdf_nodes["geometry"].unary_union.centroid.xy
        center_node = ox.distance.nearest_nodes(self.graph, x[0], y[0])
        return center_node

    def initialize_projected_graph(self):
        """
        Maps nodes in the graph to a cartersian coordiante system that can actually be 
        represented in an image with some sence of geographic distribution of the nodes.
        """
        self.projected_graph = ox.project_graph(self.graph)
        meters_per_minute = self.travel_speed * 1000 / 60  # km per hour to m per minute
        
        for _, _, _, data in self.projected_graph.edges(data=True, keys=True):
            data["time"] = data["length"] / meters_per_minute
        
        return self.projected_graph

    def get_random_node(self):
        """
        Returns a random node in the graph. Useful for testing.
        """
        nodes = list(self.graph.nodes)
        random_index = randrange(len(nodes))
        return nodes[random_index]
        
    def nearest_nodes_to(self, coordinates_list):
        """
        A way to convert coordiantes into nodes, by finding the nearest representation
        of said coordiante in the available nodes. 
        See https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.distance.nearest_nodes
        for more.
        """
        longitudes = [coordinate[0] for coordinate in coordinates_list]
        latitudes = [coordinate[1] for coordinate in coordinates_list]
        return ox.distance.nearest_nodes(self.graph, longitudes, latitudes)
