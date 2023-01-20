from pandas import Series
from entity.urban.Lot import Lot
from entity.urban.Block import Block
from entity.urban.Lot import Lot
from adapter.urban.LotSourceRepository import LotSourceRepository
from adapter.urban.LotDbRepository import LotDbRepository
from adapter.urban.LotFileRepository import LotFileRepository
from entity.geo.GeometryType import GeometryType
from entity.urban.BuildInfo import BuildInfo
from usecase.core.ThreadService import ThreadService 

class LotRepository:

    def __init__(self, 
                 threadService:ThreadService, 
                 lotDbRepository:LotDbRepository , 
                 lotFileRepository:LotFileRepository, 
                 prop:dict) -> None:
        self.__threadService = threadService
        self.__lotDbRepository = lotDbRepository
        self.__lotFileRepository = lotFileRepository
        self.__prop = prop
    
    def map(self, item:Series, param) -> Lot:

        it:Lot = Lot()
        name_lot = item["smp"].upper()
        name_block = item["seccion"] + "-" + item["manzana"]


        it = Lot()
        block = Block()
        block.set_name(name_block)
        it.set_name(name_lot)
        it.set_block(block)
        it.get_zones().append(item["zona_1"])
        it.get_special_areas().append(item["dist_1_esp"])            
        it.set_protection(item["proteccion"])
        info = {}
        
        list_build = list[BuildInfo]()
        for col in item.axes[0]:
            info[col] = item[col]
            if (col.startswith('uni_edif_') and item[col] != 0):
                build_info = BuildInfo()
                build_info.set_uni_edif(item[col])
                list_build.append(build_info)

            elif (col.startswith('dist_') and item[col]):
                dists = col.split("_")
                if (len(dists) == 3 and dists[2] == 'esp'):
                    build_info = BuildInfo()
                    build_info.set_dist_esp(item[col])
                    build_info.set_dist_grp(item['dist_' + dists[1] + "_grp"])
                    if (item['zona_1']) :
                        build_info.set_zone_1(item['zona_1'])
                    list_build.append(build_info)

        it.set_build_infos(list_build)            
        it.add_value(item[param['geometry_name']].wkt)
        it.set_info(info)



        return it

    def find_by_blocks(self, blocks:list[Block]) -> list[Lot]:

        repo = self.__resolve_repository()
        items = repo.find_by_blocks(blocks)
        param = {'geometry_name':repo.get_geometry_attribute_name()}
        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result
        

    def find_by_block(self, block:Block) -> list[Lot]:

        repo = self.__resolve_repository()
        items = repo.find_by_block(block)
        param = {'geometry_name':repo.get_geometry_attribute_name()}
        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def __resolve_repository(self) -> LotSourceRepository: 
        connector:str = self.__threadService.get('connector')
        if (connector == "db"):
            return self.__lotDbRepository
        elif (connector == "file"):
            return self.__lotFileRepository
