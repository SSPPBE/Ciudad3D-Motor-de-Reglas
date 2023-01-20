from numpy import number
from entity.geo.Geometry import Geometry
from entity.urban.Fabric import Fabric
from entity.urban.Consolidation import Consolidation
from entity.urban.Rivolta import Rivolta
from entity.urban.Buildability import Buildability
from entity.urban.BuildInfo import BuildInfo
from entity.urban.BuildType import BuildType
from entity.urban.CustomLotLine import CustomLotLine

class Lot(Geometry):
    def __init__(self, name=None) -> None:
        super().__init__()
        from entity.urban.Block import Block
        from entity.urban.Leveling import Leveling

        self.__block: Block
        self.__zones = list[str]()
        self.__heights = list[number]()
        self.__special_areas = list[str]()
        self.__rivoltas = list[Rivolta]()
        self.__buildabilities = list[Buildability]()
        self.__fabrics = list[Fabric]()
        self.__consolidation = None
        self.__info = {}
        self.__cataloged = False
        self.__irregular = False
        self.__buildability_area = 0
        self.__leveling = False
        self.__custom_lot_lines = []
        self.__levelings:list[Leveling] = None
        self.set_descriptor("lot")
        if (name):
            self.set_name(name)

    def get_name(self) -> str: 
        return self.__name

    def set_name(self, value: str):
        self.__name = value

    def get_block(self):  
        return self.__block 

    def set_block(self, value):
        self.__block = value

    def get_build_infos(self) -> list[BuildInfo]: 
        return self.__build_infos

    def set_build_infos(self, value:list[BuildInfo]):
        self.__build_infos = value

    def get_build_types(self) -> list[BuildType]: 
        return self.__build_types

    def set_build_types(self, value:list[BuildType]):
        self.__build_types = value

    def get_special_areas(self) -> list[str]:
        return self.__special_areas

    def set_special_areas(self, value:list[str]):
        self.__special_areas = value

    def get_zones(self) -> list[str]:
        return self.__zones

    def set_zones(self, value:list[str]):
        self.__zones = value

    def get_protection(self) -> str:
        return self.__protection

    def set_protection(self, value:str):
        self.__protection = value

    def get_fabrics(self) -> list[Fabric]:
        return self.__fabrics

    def set_fabrics(self, value:list[Fabric]):
        self.__fabrics = value

    def get_consolidation(self) -> Consolidation:
        return self.__consolidation

    def set_consolidation(self, value:Consolidation):
        self.__consolidation = value

    def get_rivoltas(self) -> list[Rivolta]:
        return self.__rivoltas

    def set_rivoltas(self, value:list[Rivolta]):
        self.__rivoltas = value

    def get_buildabilities(self) -> list[Buildability]:
        return self.__buildabilities

    def set_buildabilities(self, value:list[Buildability]):
        self.__buildabilities = value

    def get_heights(self) -> list[number]:
        return self.__heights

    def set_heights(self, value:list[number]):
        self.__heights = value

    def has_heights(self) -> bool:
        return len(self.__heights) > 0

    def get_info(self) -> dict:
        return self.__info

    def set_info(self, value:dict):
        self.__info = value

    def get_cataloged(self) -> bool:
        return self.__cataloged

    def set_cataloged(self, value:bool):
        self.__cataloged = value        

    def get_irregular(self) -> bool:
        return self.__irregular

    def set_irregular(self, value:bool):
        self.__irregular = value          

    def get_buildability_area(self) -> number:
        return self.__buildability_area

    def set_buildability_area(self, value:number):
        self.__buildability_area = value          

    def get_levelings(self):
        return self.__levelings

    def set_levelings(self, value):
        self.__levelings = value          

    def get_custom_lot_lines(self) -> list[CustomLotLine]:
        return self.__custom_lot_lines

    def set_custom_lot_lines(self, value:list[CustomLotLine]):
        self.__custom_lot_lines = value