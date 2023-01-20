from numpy import number
from entity.geo.Geometry import Geometry
from entity.urban.Lot import Lot
from entity.urban.Restriction import Restriction
from entity.urban.CornerArea import CornerArea

class Block(Geometry):

    def __init__(self) -> None:
        super().__init__()
        self.__lots = list[Lot]()
        self.__restrictions = []
        self.__heights = []
        self.__corner_areas = []
        self.__disposition = None
        self.__info = {}
        self.set_descriptor("block")
        self.__ae26 = ""

    def get_name(self) -> str: 
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_lots(self) -> list[Lot]:
        return self.__lots

    def set_lots(self, value:list[Lot]):
        self.__lots = value      

    def get_restrictions(self) -> list[Restriction]:
        return self.__restrictions

    def set_restrictions(self, value:list[Restriction]):
        self.__restrictions = value      

    def get_heights(self) -> list[number]:
        return self.__heights

    def set_heights(self, value:list[number]):
        self.__heights = value      

    def get_type_block(self) -> str: 
        return self.__type_block

    def set_type_block(self, value: str):
        self.__type_block = value
    
    def get_corner_areas(self) -> list[CornerArea]:
        return self.__corner_areas

    def set_corner_areas(self, value:list[CornerArea]):
        self.__corner_areas = value    

    def get_disposition(self) -> str: 
        return self.__disposition

    def set_disposition(self, value: str):
        self.__disposition = value

    def get_info(self) -> dict:
        return self.__info

    def set_info(self, value:dict):
        self.__info = value        

    def get_ae26(self) -> str:
        return self.__ae26

    def set_ae26(self, value:str):
        self.__ae26 = value        
