from numpy import number
from entity.geo.Geometry import Geometry

class Extension(Geometry):
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.CornerArea import CornerArea
        self.set_descriptor("extension")
        self.__corner_area: CornerArea

    def get_type_extension(self) -> str: 
        return self.__type_extension

    def set_type_extension(self, value: str):
        self.__type_extension = value

    def get_angle(self) -> number: 
        return self.__angle

    def set_angle(self, value: number):
        self.__angle = value


