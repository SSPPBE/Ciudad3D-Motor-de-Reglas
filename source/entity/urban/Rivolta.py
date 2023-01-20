from numpy import number
from entity.geo.Geometry import Geometry

class Rivolta(Geometry):
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.Lot import Lot
        from entity.urban.BuildType import BuildType
        self.__lot:Lot
        self.__build_type:BuildType = None
        self.set_descriptor("rivolta")

    def get_lot(self): 
        return self.__lot

    def set_lot(self, value):
        self.__lot = value

    def get_height(self) -> number: 
        return self.__height

    def set_height(self, value: number):
        self.__height = value

    def get_build_type(self): 
        return self.__build_type

    def set_build_type(self, value):
        self.__build_type = value
        

