from pandas import Series
from entity.urban.CustomBuildability import CustomBuildability
from entity.urban.Block import Block
from entity.urban.CustomBuildability import CustomBuildability
from adapter.urban.CustomBuildabilitySourceRepository import CustomBuildabilitySourceRepository
from adapter.urban.CustomBuildabilityDbRepository import CustomBuildabilityDbRepository
from adapter.urban.CustomBuildabilityFileRepository import CustomBuildabilityFileRepository
from entity.geo.GeometryType import GeometryType
from entity.urban.Lot import Lot
from entity.urban.BuildInfo import BuildInfo
from entity.urban.BuildType import BuildType
from usecase.core.ThreadService import ThreadService 

class CustomBuildabilityRepository:

    def __init__(self, 
                 threadService:ThreadService, 
                 custom_buildability_db_repository:CustomBuildabilityDbRepository , 
                 custom_buildability_file_repository:CustomBuildabilityFileRepository, 
                 prop:dict) -> None:
        self.__threadService = threadService
        self.__custom_buildability_db_repository = custom_buildability_db_repository
        self.__custom_buildability_file_repository = custom_buildability_file_repository
        self.__prop = prop
    
    def map(self, item:Series, param) -> CustomBuildability:

        it = CustomBuildability()
        lot = Lot()
        lot.set_name(item["smp"].upper())
        it.set_lot(lot)
        build_info = BuildInfo()
        build_info.set_dist_grp(item["edificabil"])
        build_type = BuildType()
        build_type.set_build_info(build_info)
        it.set_build_type(build_type)
        it.set_from(item["altura_ini"])
        it.set_to(item["altura_fin"])        
        it.set_type_buildability(item["tipo"])
        it.add_value(item[param['geometry_name']].wkt)
        return it

    def find_by_block(self, block:Block) -> list[CustomBuildability]:

        repo = self.__resolve_repository()
        items = repo.find_by_block(block)
        param = {'geometry_name':repo.get_geometry_attribute_name()}
        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def __resolve_repository(self) -> CustomBuildabilitySourceRepository: 
        connector:str = self.__threadService.get('connector')
        if (connector == "db"):
            return self.__custom_buildability_db_repository
        elif (connector == "file"):
            return self.__custom_buildability_file_repository
