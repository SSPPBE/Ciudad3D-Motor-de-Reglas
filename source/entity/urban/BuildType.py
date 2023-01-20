from numpy import number
from entity.geo.Geometry import Geometry
from entity.urban.BuildInfo import BuildInfo

class BuildType():

    def __init__(self) -> None:
        self.__code = None
        self.__build_info = None
        self.__height = None
        self.__components = list[dict]()
        self.__no_corner_area = None
        self.__consolidate_filter = None
        self.__accept_rivolta = False
        self.__ae26 = None
        pass

    def get_code(self) -> str: 
        return self.__code

    def set_code(self, value:str):
        self.__code = value

    def get_build_info(self) -> BuildInfo: 
        return self.__build_info

    def set_build_info(self, value:BuildInfo):
        self.__build_info = value

    def get_height(self) -> number: 
        return self.__height

    def set_height(self, value: number):
        self.__height = value

    def get_components(self) -> list[dict]: 
        return self.__components

    def set_components(self, value:list[dict]):
        self.__components = value

    def get_no_corner_area(self) -> number: 
        return self.__no_corner_area

    def set_no_corner_area(self, value: number):
        self.__no_corner_area = value

    def get_consolidate_filter(self) -> number: 
        return self.__consolidate_filter

    def set_consolidate_filter(self, value: number):
        self.__consolidate_filter = value

    def get_accept_rivolta(self) -> bool: 
        return self.__accept_rivolta

    def set_accept_rivolta(self, value: bool):
        self.__accept_rivolta = value
    
    def get_ae26(self) -> str: 
        return self.__ae26

    def set_ae26(self, value:str):
        self.__ae26 = value
