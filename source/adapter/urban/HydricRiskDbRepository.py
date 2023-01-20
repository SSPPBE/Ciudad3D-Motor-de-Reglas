from pandas import Series
from adapter.core.DbConnector import DbConnector
from entity.urban.HydricRisk import HydricRisk
import geopandas

from adapter.urban.HydricRiskSourceRepository import HydricRiskSourceRepository

class HydricRiskDbRepository(HydricRiskSourceRepository):

    def __init__(self, db_connector:DbConnector) -> None:
        self.__db_connector = db_connector

    def get_geometry_attribute_name(self) -> str:
        return "the_geom"
    
    def find_all(self) -> any:

        sql = """
              select * from cur_riesgohidrico
              """
        return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')
