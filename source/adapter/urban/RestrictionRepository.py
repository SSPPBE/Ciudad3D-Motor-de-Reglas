from pandas import Series
from entity.urban.Restriction import Restriction
from entity.urban.Block import Block
from entity.urban.Restriction import Restriction
from adapter.urban.RestrictionSourceRepository import RestrictionSourceRepository
from adapter.urban.RestrictionDbRepository import RestrictionDbRepository
from adapter.urban.RestrictionFileRepository import RestrictionFileRepository
from entity.geo.GeometryType import GeometryType
from usecase.core.ThreadService import ThreadService 

class RestrictionRepository:

    def __init__(self, 
                 threadService:ThreadService, 
                 restriction_db_repository:RestrictionDbRepository , 
                 restriction_file_repository:RestrictionFileRepository, 
                 prop:dict) -> None:
        self.__threadService = threadService
        self.__restriction_db_repository = restriction_db_repository
        self.__restriction_file_repository = restriction_file_repository
        self.__prop = prop
    
    def map(self, item:Series, param) -> Restriction:

        it = Restriction()
        it.set_order(item["nro_ord"])
        it.set_type_restriction(item["tipo"])
        it.set_observation(item["obs"])

        it.add_value(item[param['geometry_name']].wkt)
        return it

    def find_all(self) -> list[Restriction]:

        repo = self.__resolve_repository()
        items = repo.find_all()
        param = {'geometry_name':repo.get_geometry_attribute_name()}
        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def __resolve_repository(self) -> RestrictionSourceRepository: 
        connector:str = self.__threadService.get('connector')
        if (connector == "db"):
            return self.__restriction_db_repository
        elif (connector == "file"):
            return self.__restriction_file_repository
