from pandas import Series
from entity.urban.Block import Block
from entity.urban.Block import Block
from entity.urban.Lot import Lot
from adapter.urban.BlockSourceRepository import BlockSourceRepository
from adapter.urban.BlockDbRepository import BlockDbRepository
from adapter.urban.BlockFileRepository import BlockFileRepository
from entity.geo.GeometryType import GeometryType
from usecase.core.ThreadService import ThreadService 

class BlockRepository:

    def __init__(self, 
                 threadService:ThreadService, 
                 blockDbRepository:BlockDbRepository, 
                 blockFileRepository:BlockFileRepository, 
                 prop:dict) -> None:
        self.__threadService = threadService
        self.__blockDbRepository = blockDbRepository
        self.__blockFileRepository = blockFileRepository
        self.__prop = prop

    def map(self, item:Series, param) -> Block:

        it = Block()
        it.set_name(item["sm"])
        it.set_type_block(item["mz_tipo"])
        it.set_disposition(item["disposicio"])
        it.add_value(item[param['geometry_name']].wkt)

        info = {}
        for col in item.axes[0]:
            info[col] = item[col]

        it.set_info(info)
        return it

    def find_by_blocks_sections(self, blocks:list[str], sections:list[str]) -> list[Block]:
        repo = self.__resolve_repository()
        items = repo.find_by_blocks_sections(blocks, sections)
        param = {'geometry_name':repo.get_geometry_attribute_name()}

        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def find_all(self) -> list[Block]:

        repo = self.__resolve_repository()
        items = repo.find_all()
        param = {'geometry_name':repo.get_geometry_attribute_name()}

        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def find_ae26(self, block:Block) -> list[dict]:
        repo = self.__resolve_repository()
        items = repo.find_ae26(block)

        result = []
        for idx, item in items.iterrows():
            it = dict()
            it["name"] = item["name"]
            it["build_code"] = item["build_code"]
            it["group"] = item["group"]            
            result.append(it)
        return result


    def __resolve_repository(self) -> BlockSourceRepository: 
        connector:str = self.__threadService.get('connector')
        if (connector == "db"):
            return self.__blockDbRepository
        elif (connector == "file"):
            return self.__blockFileRepository
