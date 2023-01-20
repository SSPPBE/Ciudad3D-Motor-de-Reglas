from adapter.core.DbConnector import DbConnector
import geopandas

from adapter.urban.CustomLotLineSourceRepository import CustomLotLineSourceRepository
from entity.urban.Block import Block

class CustomLotLineDbRepository(CustomLotLineSourceRepository):

    def __init__(self, db_connector:DbConnector) -> None:
        self.__db_connector = db_connector

    def get_geometry_attribute_name(self) -> str:
        return "the_geom"
    
    def find_by_block(self, block:Block) -> any:

        sql  = "select a.* from cur_lineasparcelas a "
        sql += "where a.smp like '" + block.get_name() + "%%' and a.tipo = 'FONDO'"

        return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')
