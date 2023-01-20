from pandas import Series
from entity.urban.CustomLine import CustomLine
from entity.urban.Block import Block
from entity.urban.CustomLine import CustomLine
from adapter.urban.CustomLineSourceRepository import CustomLineSourceRepository
from adapter.urban.CustomLineDbRepository import CustomLineDbRepository
from adapter.urban.CustomLineFileRepository import CustomLineFileRepository
from entity.geo.GeometryType import GeometryType
from entity.urban.Lot import Lot
from usecase.core.ThreadService import ThreadService 

class CustomLineRepository:

    def __init__(self, 
                 threadService:ThreadService, 
                 custom_line_db_repository:CustomLineDbRepository , 
                 custom_line_file_repository:CustomLineFileRepository, 
                 prop:dict) -> None:
        self.__threadService = threadService
        self.__custom_line_db_repository = custom_line_db_repository
        self.__custom_line_file_repository = custom_line_file_repository
        self.__prop = prop
    
    def map(self, item:Series, param) -> CustomLine:

        it = CustomLine()
        block = Block()
        block.set_name(item["sm"])
        it.set_block(block)
        it.set_type_custom_line(item["tipo"])
        it.add_value(item[param['geometry_name']].wkt)
        return it

    def find_by_block(self, block:Block) -> list[CustomLine]:

        repo = self.__resolve_repository()
        items = repo.find_by_block(block)
        param = {'geometry_name':repo.get_geometry_attribute_name()}
        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def __resolve_repository(self) -> CustomLineSourceRepository: 
        connector:str = self.__threadService.get('connector')
        if (connector == "db"):
            return self.__custom_line_db_repository
        elif (connector == "file"):
            return self.__custom_line_file_repository
