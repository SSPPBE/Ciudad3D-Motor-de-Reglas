from pandas import Series
from adapter.core.DbConnector import DbConnector
from entity.urban.ArchaeologicalRisk import ArchaeologicalRisk
import geopandas

from adapter.urban.ArchaeologicalRiskSourceRepository import ArchaeologicalRiskSourceRepository

class ArchaeologicalRiskDbRepository(ArchaeologicalRiskSourceRepository):

    def __init__(self, db_connector:DbConnector) -> None:
        self.__db_connector = db_connector

    def get_geometry_attribute_name(self) -> str:
        return "the_geom"
    
    def find_all(self) -> any:

        sql = """
              select * from cur_riesgo_arqueologico
              """
        return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')
