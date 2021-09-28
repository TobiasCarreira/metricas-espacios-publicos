import json, os

class ParkCoordinates:
    """
    Reads database as given in filename. Database contains coordiantes of the centroids of points of interest.
    """
    def __init__(self):
        self._dataset = {}
        
    def load_park_coordinates_from(self, filename):
        """
        Loads up filename nto a dictionary keyed with coordiante IDs and coordiantes as values.
        """
        with(open("data/parquesCorteArea2_5perc_CENTROIDES.geojson")) as f:
            self._dataset = json.loads(f.read())
        return self
            
    def coordinates_of(self, index):
        """
        Returns coordiantes of a given index (ID).
        """
        return self.feature_list()[index]["geometry"]["coordinates"]
        
    def all_coordinates(self):
        """
        Returns a list of all coordiantes, ordered as indexed.
        """
        return [self.coordinates_of(index) for index in range(len(self.feature_list()))]
    
    def feature_list(self):
        """
        Returns feature list of the dataset, features being for example parks.
        """
        return self._dataset["features"]
