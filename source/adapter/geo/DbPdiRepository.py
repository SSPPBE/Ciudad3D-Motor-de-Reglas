from pyproj import CRS
from sqlalchemy import create_engine
from adapter.geo.PdiRepository import PdiRepository
from usecase.core.ConfigurationService import ConfigurationService
import geopandas as gpd

class DbPdiRepository(PdiRepository):
    
    def __init__(self, configurationService:ConfigurationService, block_name):
        self.configurationService = configurationService
        self.__prop = configurationService.get_prop()
        self.__conf = configurationService.get_conf()
        self.__block_name = block_name

        db_connection_url = "postgresql://usuario:password@my.ip:5432/public"
        self.__con = create_engine(db_connection_url)  

    def get_block_geometry_name(self) -> str:
        return "the_geom"

    def get_restriction_frame(self) -> any:
        sql = "select * from cur_restricciones"
        return gpd.read_postgis(sql, self.__con, 'the_geom')

    def get_lot_frame(self, param = {}) -> any:
        sql = """
              select a.*, b.proteccion from cur_parcelas a 
              left join aph_ssregic b on a.smp = b.smp
              """
        sql = sql + "where (a.seccion || '-' || a.manzana)  = '" + self.__block_name + "'"

        return gpd.read_postgis(sql, self.__con, 'the_geom')

    def get_block_frame(self) -> any:
        sql = "select * from mo_manzanasmap where sm = '" + self.__block_name + "'"
        return gpd.read_postgis(sql, self.__con, 'the_geom')

    def get_real_frame(self) -> any:
        sql = "where sm = '" + self.__block_name + "'"
        return gpd.read_postgis(sql, self.__con, 'the_geom')


    def get_crs(self, crs) -> any:
        crs = CRS.from_user_input("+proj=tmerc +lat_0=-34.629269 +lon_0=-58.4633 +k=0.9999980000000001 +x_0=100000 +y_0=100000 +ellps=intl +units=m +no_defs")
        return crs
