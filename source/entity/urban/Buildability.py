from numpy import number
from entity.geo.Geometry import Geometry

class Buildability(Geometry):
    def __init__(self, descriptor:str) -> None:
        super().__init__()
        from entity.urban.Lot import Lot
        self.__lot:Lot
        self.set_descriptor(descriptor)
        self.__from = 0
        self.__to = 0
        from entity.urban.BuildType import BuildType
        self.__build_type = None

    def get_lot(self): 
        return self.__lot

    def set_lot(self, value):
        self.__lot = value

    def get_from(self) -> number: 
        return self.__from

    def set_from(self, value: number):
        self.__from = value

    def get_to(self) -> number: 
        return self.__to

    def set_to(self, value: number):
        self.__to = value

    def get_build_type(self): 
        return self.__build_type

    def set_build_type(self, value):
        self.__build_type = value

