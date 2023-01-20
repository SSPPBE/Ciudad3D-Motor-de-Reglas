from adapter.core.DbConnector import DbConnector
import geopandas

from adapter.urban.CustomLineSourceRepository import CustomLineSourceRepository
from entity.urban.Block import Block

class CustomLineDbRepository(CustomLineSourceRepository):

    def __init__(self, db_connector:DbConnector) -> None:
        self.__db_connector = db_connector

    def get_geometry_attribute_name(self) -> str:
        return "the_geom"
    
    def find_by_block(self, block:Block) -> any:

        sql  = "select a.*, 'LIB' tipo from cur_lib_particularizadas a "
        sql += "where a.sm like '" + block.get_name() + "'"
        sql += "union all "
        sql += "select b.*, 'LFI' tipo from cur_lfi_particularizadas b "
        sql += "where b.sm like '" + block.get_name() + "'"

        return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')
