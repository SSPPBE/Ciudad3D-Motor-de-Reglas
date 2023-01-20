from adapter.core.DbConnector import DbConnector
import geopandas

from adapter.urban.CustomBuildabilitySourceRepository import CustomBuildabilitySourceRepository
from entity.urban.Block import Block

class CustomBuildabilityDbRepository(CustomBuildabilitySourceRepository):

    def __init__(self, db_connector:DbConnector) -> None:
        self.__db_connector = db_connector

    def get_geometry_attribute_name(self) -> str:
        return "the_geom"
    
    def find_by_block(self, block:Block) -> any:

        sql = "select * from cur_volumenes_particularizados"
        sql = sql + " where smp like '" + block.get_name() + "%%'"

        return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')
