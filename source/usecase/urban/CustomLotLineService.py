from collections import defaultdict
from adapter.urban.CustomLotLineRepository import CustomLotLineRepository
from entity.urban.Block import Block
from entity.geo.Geometry import Geometry
from usecase.core.LogService import LogService
from entity.urban.CustomLotLine import CustomLotLine
from adapter.geo.GisLibrary import GisLibrary

class CustomLotLineService:

    def __init__(self,
                 custom_line_repository:CustomLotLineRepository,
                 gis_library:GisLibrary) -> None:
        self.__custom_line_repository = custom_line_repository
        self.__gis_library = gis_library

    def find_by_block(self, block:Block)->list[CustomLotLine]:
        return self.__custom_line_repository.find_by_block(block)