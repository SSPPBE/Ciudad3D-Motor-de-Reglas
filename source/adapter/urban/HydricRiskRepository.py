from pandas import Series
from entity.urban.HydricRisk import HydricRisk
from entity.urban.Block import Block
from entity.urban.HydricRisk import HydricRisk
from adapter.urban.HydricRiskSourceRepository import HydricRiskSourceRepository
from adapter.urban.HydricRiskDbRepository import HydricRiskDbRepository
from adapter.urban.HydricRiskFileRepository import HydricRiskFileRepository
from entity.geo.GeometryType import GeometryType
from usecase.core.ThreadService import ThreadService 

class HydricRiskRepository:

    def __init__(self, 
                 threadService:ThreadService, 
                 hydric_risk_db_repository:HydricRiskDbRepository , 
                 hydric_risk_file_repository:HydricRiskFileRepository, 
                 prop:dict) -> None:
        self.__threadService = threadService
        self.__hydric_risk_db_repository = hydric_risk_db_repository
        self.__hydric_risk_file_repository = hydric_risk_file_repository
        self.__prop = prop
    
    def map(self, item:Series, param) -> HydricRisk:

        it = HydricRisk()
        it.add_value(item[param['geometry_name']].wkt)
        return it

    def find_all(self) -> list[HydricRisk]:

        repo = self.__resolve_repository()
        items = repo.find_all()
        param = {'geometry_name':repo.get_geometry_attribute_name()}
        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def __resolve_repository(self) -> HydricRiskSourceRepository: 
        connector:str = self.__threadService.get('connector')
        if (connector == "db"):
            return self.__hydric_risk_db_repository
        elif (connector == "file"):
            return self.__hydric_risk_file_repository
