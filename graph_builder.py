import osmnx as ox

class GraphBuilder:
    def __init__(self, place, transportation_mode, travel_speed):
        self.place = place
        self.transportation_mode = transportation_mode
        self.travel_speed = travel_speed # in km/h
        self.graph = None

    def initialize_graph(self):
        self.graph = ox.graph_from_place(
            self.place,
            network_type=self.transportation_mode
        )
        return self.graph

    def calculate_centroid(self):
        gdf_nodes = ox.graph_to_gdfs(self.graph, edges=False)
        x, y = gdf_nodes["geometry"].unary_union.centroid.xy
        center_node = ox.distance.nearest_nodes(self.graph, x[0], y[0])
        return center_node
        
    def initialize_projected_graph(self):
        self.projected_graph = ox.project_graph(self.graph)
        meters_per_minute = self.travel_speed * 1000 / 60  # km per hour to m per minute
        
        for _, _, _, data in self.projected_graph.edges(data=True, keys=True):
            data["time"] = data["length"] / meters_per_minute
        
        return self.projected_graph
        
    
