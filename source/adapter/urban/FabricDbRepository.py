from pandas import Series
from adapter.core.DbConnector import DbConnector
from entity.urban.Fabric import Fabric
from entity.urban.Block import Block
from entity.urban.Lot import Lot
import geopandas

from adapter.urban.FabricSourceRepository import FabricSourceRepository

class FabricDbRepository(FabricSourceRepository):

    def __init__(self, db_connector:DbConnector) -> None:
        self.__db_connector = db_connector

    def get_geometry_attribute_name(self) -> str:
        return "the_geom"
    
    def find_by_block(self, block:Block) -> any:

        sql = """
        select a.sm, a.smp, a.extr_2017, a.altos, a.the_geom from cur_tejido a 
        """
        sql = sql + " where a.sm = '" + block.get_name()[1:].upper() + "' and a.extr_2017 > 0"
        return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')
