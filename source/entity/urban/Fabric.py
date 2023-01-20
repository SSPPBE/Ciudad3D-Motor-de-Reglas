from numpy import number
from entity.geo.Geometry import Geometry

class Fabric(Geometry):
    
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.Lot import Lot
        self.set_descriptor("fabric")
        self.__lot:Lot

    def get_lot(self): 
        return self.__lot

    def set_lot(self, value):
        self.__lot = value

    def get_height(self) -> number: 
        return self.__height

    def set_height(self, value: number):
        self.__height = value

    def get_highs(self) -> number: 
        return self.__highs

    def set_highs(self, value: number):
        self.__highs = value