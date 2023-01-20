from entity.gcba.geo.Geometry import Geometry
from entity.gcba.geo.Projection import Projection


class GeoData:
    """
    Represents structure required by library to process algorithms and manipulate geometries \n
    Data depends on Gis implementation library
    """

    def __init__(self) -> None:
        pass

    def get_projection(self) -> Projection:
        return self.__projection

    def set_projection(self, projection:Projection):
        self.__projection = projection    

    def get_geometries(self) -> list[Geometry]:
        return self.__geometries

    def set_geometries(self, geometries:list[Geometry]):
        self.__geometries = geometries    
                