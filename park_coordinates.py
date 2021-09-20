import json, os

class ParkCoordinates:
    def __init__(self):
        self._dataset = {}
        
    def load_park_coordinates_from(self, filename):
        with(open("data/parquesCorteArea2_5perc_CENTROIDES.geojson")) as f:
            self._dataset = json.loads(f.read())
        return self
            
    def coordinates_of(self, index):
        return self.feature_list()[index]["geometry"]["coordinates"]
        
    def all_coordinates(self):
        return [self.coordinates_of(index) for index in range(len(self.feature_list()))]
    
    def feature_list(self):
        return self._dataset["features"]
