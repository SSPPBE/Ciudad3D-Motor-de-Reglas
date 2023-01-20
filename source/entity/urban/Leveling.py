from numpy import number
from entity.geo.Geometry import Geometry
from entity.urban.GeometryBuildType import GeometryBuildType

class Leveling(GeometryBuildType):
    
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.Lot import Lot

        self.set_descriptor("leveling")
        self.__retire = None
        self.__adjoining:Lot = None

    def get_retire(self) -> number: 
        return self.__retire

    def set_retire(self, value: number):
        self.__retire = value

    def get_adjoining(self): 
        return self.__adjoining

    def set_adjoining(self, value):
        self.__adjoining = value