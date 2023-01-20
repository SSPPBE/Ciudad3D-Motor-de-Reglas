from numpy import number
from entity.geo.Geometry import Geometry

class CustomBuildability(Geometry):
    
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.Lot import Lot
        self.set_descriptor("custom_buildability")
        self.__lot:Lot

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

    def get_type_buildability(self) -> str: 
        return self.__type_buildability

    def set_type_buildability(self, value: str):
        self.__type_buildability = value

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