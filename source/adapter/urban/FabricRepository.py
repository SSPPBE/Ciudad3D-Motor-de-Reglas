from pandas import Series
from entity.urban.Fabric import Fabric
from entity.urban.Block import Block
from entity.urban.Lot import Lot
from adapter.urban.FabricSourceRepository import FabricSourceRepository
from adapter.urban.FabricDbRepository import FabricDbRepository
from adapter.urban.FabricFileRepository import FabricFileRepository
from entity.geo.GeometryType import GeometryType
from adapter.geo.GisLibrary import GisLibrary
from usecase.core.ThreadService import ThreadService 

class FabricRepository:

    def __init__(self, 
                 thread_service:ThreadService, 
                 fabric_db_repository:FabricDbRepository , 
                 fabric_file_repository:FabricFileRepository, 
                 prop:dict) -> None:
        self.__thread_service = thread_service
        self.__fabric_db_repository = fabric_db_repository
        self.__fabric_file_repository = fabric_file_repository
        self.__prop = prop
    
    def map(self, item:Series, param) -> Fabric:

        it:Fabric = Fabric()
        vals = item["smp"].split('-')
        first_size = len(vals[0])
        name_lot = ("0" if first_size == 2 else "") + item["smp"].upper()
        name_block = item["sm"]

        block = Block()
        block.set_name(name_block)
        lot = Lot()
        lot.set_name(name_lot)
        lot.set_block(block)
        it.set_lot(lot)
        it.set_height(item["extr_2017"])
        it.set_highs(item["altos"])
        it.add_value(item[param['geometry_name']].wkt)
        return it

    def find_by_block(self, block:Block) -> list[Fabric]:

        repo = self.__resolve_repository()
        items = repo.find_by_block(block)
        param = {'geometry_name':repo.get_geometry_attribute_name()}
        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def __resolve_repository(self) -> FabricSourceRepository: 
        connector:str = self.__thread_service.get('connector')
        if (connector == "db"):
            return self.__fabric_db_repository
        elif (connector == "file"):
            return self.__fabric_file_repository
