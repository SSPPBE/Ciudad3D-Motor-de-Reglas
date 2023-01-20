from pandas import Series
from adapter.core.DbConnector import DbConnector
from usecase.core.ThreadService import ThreadService
from entity.urban.Block import Block
from entity.urban.Block import Block
from entity.urban.Lot import Lot
import geopandas

from adapter.urban.BlockSourceRepository import BlockSourceRepository

class BlockDbRepository(BlockSourceRepository):

    def __init__(self, 
                 db_connector:DbConnector,
                 thread_service:ThreadService) -> None:
        self.__db_connector = db_connector
        self.__thread_service = thread_service

    def get_geometry_attribute_name(self) -> str:
        return "the_geom"
    
    def find_by_blocks_sections(self, blocks:list[str], sections:list[str]) -> any:

        criteria = ""
        if (blocks):
            criteria += " a.sm in (" + ','.join(map(lambda e: "'" + e + "'", blocks)) + ")"
        if (sections):
            criteria += ("or" if criteria != "" else "") + " a.seccion in (" + ','.join(map(lambda e: "'" + e + "'", sections)) + ")"

        sql = self.__get_select() + " where " + criteria
        return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')

    def find_all(self) -> any:

        sql = self.__get_select()
        return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')

    def find_ae26(self, block:Block) -> any:

        sql =       "select distinct j.sm as name, j.\"UNIDADEDIFICABILIDAD\" as build_code, j.\"SUBGRUPO\" as \"group\", null as the_geom from"
        sql = sql + " (select * from ("
        sql = sql + " select (y.seccion || '-' || y.manzana) sm,  x.smp, x.frente, unnest(string_to_array(num_dom, '.')) num  from frentesparcelas x"
        sql = sql + " INNER JOIN mo_parcelasmap y on x.smp = y.smp"
        sql = sql + " where frente in (select trim(B.\"CALLE\") from cur_ae26 B)"
        sql = sql + " and x.smp like '" + block.get_name() + "%%'"
        sql = sql + " ) A inner join cur_ae26 C on trim(C.\"CALLE\") = A.frente and A.NUM >= C.\"DESDE\" AND A.NUM <= C.\"HASTA\") j"
        return geopandas.read_postgis(sql, self.__db_connector.get(), "the_geom")

    def __get_select(self) -> str:

        sql =       "select a.*, "
        sql = sql + " b.area_esp, b.cant_parce, b.cat, b.disposicio, "
        sql = sql + " b.featid1, b.fid, b.gid, b.lfi, b.lib, b.obras, "
        sql = sql + " b.oferta, b.parc_catal, b.pdf, b.superficie, b.trazado, "
        sql = sql + " b.uni_edif " 
        sql = sql + " from mo_manzanasmap a"
        sql = sql + " left join cur_manzanasatipicas b on a.sm = b.sm"
        return sql