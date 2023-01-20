from numpy import number
from entity.geo.Geometry import Geometry
class BuildInfo():
    
    def __init__(self) -> None:
        self.__uni_edif = None
        self.__dist_esp = None
        self.__dist_grp = None
        self.__zone_1 = None
        self.__type_street = None
        pass

    def get_uni_edif(self) -> str: 
        return self.__uni_edif

    def set_uni_edif(self, value:str):
        self.__uni_edif = value

    def get_dist_esp(self) -> str: 
        return self.__dist_esp

    def set_dist_esp(self, value:str):
        self.__dist_esp = value
                 
    def get_dist_grp(self) -> str: 
        return self.__dist_grp

    def set_dist_grp(self, value:str):
        self.__dist_grp = value

    def get_zone_1(self) -> str: 
        return self.__zone_1

    def set_zone_1(self, value:str):
        self.__zone_1 = value

    def get_type_street(self) -> str: 
        return self.__type_street

    def set_type_street(self, value:str):
        self.__type_street = value
