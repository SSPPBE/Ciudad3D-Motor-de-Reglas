from numpy import number
from entity.geo.Geometry import Geometry

class Consolidation(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self.set_descriptor("consolidated")
        self.__touched = False

    def get_type_consolidated(self) -> str: 
        return self.__type_consolidated

    def set_type_consolidated(self, value: str):
        self.__type_consolidated= value

    def get_consolidated(self) -> bool: 
        return self.__consolidated

    def set_consolidated(self, value: bool):
        self.__consolidated= value        

    def get_percentage(self) -> number: 
        return self.__percentage

    def set_percentage(self, value: number):
        self.__percentage = value
    
    def get_touched(self) -> bool: 
        return self.__touched

    def set_touched(self, value: bool):
        self.__touched= value        

    def get_max_height(self) -> number: 
        return self.__max_height

    def set_max_height(self, value: number):
        self.__max_height = value
