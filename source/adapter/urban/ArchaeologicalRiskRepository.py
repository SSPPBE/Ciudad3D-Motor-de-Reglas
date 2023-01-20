from pandas import Series
from entity.urban.ArchaeologicalRisk import ArchaeologicalRisk
from entity.urban.Block import Block
from entity.urban.ArchaeologicalRisk import ArchaeologicalRisk
from adapter.urban.ArchaeologicalRiskSourceRepository import ArchaeologicalRiskSourceRepository
from adapter.urban.ArchaeologicalRiskDbRepository import ArchaeologicalRiskDbRepository
from adapter.urban.ArchaeologicalRiskFileRepository import ArchaeologicalRiskFileRepository
from entity.geo.GeometryType import GeometryType
from usecase.core.ThreadService import ThreadService 

class ArchaeologicalRiskRepository:

    def __init__(self, 
                 threadService:ThreadService, 
                 archaeological_risk_db_repository:ArchaeologicalRiskDbRepository , 
                 archaeological_risk_file_repository:ArchaeologicalRiskFileRepository, 
                 prop:dict) -> None:
        self.__threadService = threadService
        self.__archaeological_risk_db_repository = archaeological_risk_db_repository
        self.__archaeological_risk_file_repository = archaeological_risk_file_repository
        self.__prop = prop
    
    def map(self, item:Series, param) -> ArchaeologicalRisk:

        it = ArchaeologicalRisk()
        it.set_description(item["tipo"])
        it.add_value(item[param['geometry_name']].wkt)
        return it

    def find_all(self) -> list[ArchaeologicalRisk]:

        repo = self.__resolve_repository()
        items = repo.find_all()
        param = {'geometry_name':repo.get_geometry_attribute_name()}
        result = []
        for idx, item in items.iterrows():
            result.append(self.map(item, param))
        return result

    def __resolve_repository(self) -> ArchaeologicalRiskSourceRepository: 
        connector:str = self.__threadService.get('connector')
        if (connector == "db"):
            return self.__archaeological_risk_db_repository
        elif (connector == "file"):
            return self.__archaeological_risk_file_repository
