from pandas import Series
from entity.urban.CustomLotLine import CustomLotLine
from entity.urban.Block import Block
from entity.urban.CustomLotLine import CustomLotLine
from adapter.urban.CustomLotLineSourceRepository import CustomLotLineSourceRepository
from adapter.urban.CustomLotLineDbRepository import CustomLotLineDbRepository
from adapter.urban.CustomLotLineFileRepository import CustomLotLineFileRepository
from entity.geo.GeometryType import GeometryType
from entity.urban.Lot import Lot
from usecase.core.ThreadService import ThreadService 

class CustomLotLineRepository:

    def __init__(self, 
                 threadService:ThreadService, 
                 custom_line_db_repository:CustomLotLineDbRepository , 
                 custom_line_file_repository:CustomLotLineFileRepository, 
                 prop:dict) -> None:
        self.__threadService = threadService
        self.__custom_line_db_repository = custom_line_db_repository
        self.__custom_line_file_repository = custom_line_file_repository
        self.__prop = prop
    
    def map(self, item:Series, param) -> CustomLotLine:

        it = CustomLotLine()
        lot = Lot()
        lot.set_name(item["smp"])
        it.set_lot(lot)
        it.set_type_custom_line(item["tipo"])
        it.add_value(item[param['geometry_name']].wkt)
        return it

    def find_by_block(self, block:Block) -> list[CustomLotLine]:

        repo = self.__resolve_repository()
        items = repo.find_by_block(block)
        param = {'geometry_name':repo.get_geometry_attribute_name()}
        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def __resolve_repository(self) -> CustomLotLineSourceRepository: 
        connector:str = self.__threadService.get('connector')
        if (connector == "db"):
            return self.__custom_line_db_repository
        elif (connector == "file"):
            return self.__custom_line_file_repository
