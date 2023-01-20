from pandas import Series
from adapter.core.DbConnector import DbConnector
from entity.urban.Lot import Lot
from entity.urban.Block import Block
from entity.urban.Lot import Lot
import geopandas

from adapter.urban.LotSourceRepository import LotSourceRepository

class LotDbRepository(LotSourceRepository):

    def __init__(self, db_connector:DbConnector) -> None:
        self.__db_connector = db_connector

    def get_geometry_attribute_name(self) -> str:
        return "the_geom"
    
    def find_by_block(self, block:Block) -> any:

        sql = """
            select a.smp, a.the_geom, a.seccion, a.manzana, a.area, 
                b.uni_edif_1, b.uni_edif_2, b.uni_edif_3, b.uni_edif_4,
                b.dist_1_grp, b.dist_1_esp, b.dist_2_grp, b.dist_2_esp, b.dist_3_grp, b.dist_3_esp, b.dist_4_grp, b.dist_4_esp, 
                b.zona_1, c.tipo_c, 
                d.proteccion, 
                d.barrios,  d."1_calle", d."1_altura", d."1_direccio",
                d."2_calle", d."2_alt", d."2_direccio", d."3_calle", d."3_alt", d."3_direccio", 
                d."4_calle", d."4_alt", d."4_direccio", d.denominaci, d.catalogaci, d.aph_nro_y_, d.estado, d.ley_3056,
                b.alicuota, b.anac, b.apertura, b.barrio, b.catalogado, b.ci_digital, b.comuna, b.dist_cpu_1, b.ensanche, 
                b.fot_em_1, b.fot_em_2, b.fot_pl_1, b.fot_pl_2, b.fot_sl_1, b.dist_cpu_2, 
                b.fot_sl_2, b.inc_uva_21, b.lep, b.plano_l, b.rh, b.rivolta, b.tipo_mza, 
                b.uso_1, b.uso_2, b.uso_3,
                b.parcela, b.cpu_obs, b.plano_l_ob, b.ae_fot_bas, b.zona_2, b.adps, b.memo, b.microcentr 
                    from mo_parcelasmap a
                    left join cur_parcelas b on a.smp = b.smp
                    left join aph_ssregic d on a.smp = d.smp
                    left join (
                        select x.smp, min(tipo_c) tipo_c
                        from mo_parcelasmap x
                        left join frentesparcelas y on x.smp = y.smp
                        left join cur_callejero z on y.frente = z.nom_mapa
                        where (x.seccion || '-' || x.manzana)  = '{0}'
                        group by x.smp ) C on a.smp = c.smp
                where (a.seccion || '-' || b.manzana)  = '{0}'
              """
        sql = sql.format(block.get_name())

            #   select a.*, b.proteccion from cur_parcelas a 
            #   left join aph_ssregic b on a.smp = b.smp

        return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')

    def find_by_blocks(self, blocks:list[Block]) -> any:
            params = ','.join(["'" + o.get_name() + "'" for o in blocks])

            sql = """
            select a.smp, a.the_geom, a.seccion, a.manzana, a.area, 
                b.uni_edif_1, b.uni_edif_2, b.uni_edif_3, b.uni_edif_4,
                b.dist_1_grp, b.dist_1_esp, b.dist_2_grp, b.dist_2_esp, b.dist_3_grp, b.dist_3_esp, b.dist_4_grp, b.dist_4_esp, 
                b.zona_1, c.tipo_c, 
                d.proteccion, 
                d.barrios,  d."1_calle", d."1_altura", d."1_direccio",
                d."2_calle", d."2_alt", d."2_direccio", d."3_calle", d."3_alt", d."3_direccio", 
                d."4_calle", d."4_alt", d."4_direccio", d.denominaci, d.catalogaci, d.aph_nro_y_, d.estado, d.ley_3056,
                b.alicuota, b.anac, b.apertura, b.barrio, b.catalogado, b.ci_digital, b.comuna, b.dist_cpu_1, b.ensanche, 
                b.fot_em_1, b.fot_em_2, b.fot_pl_1, b.fot_pl_2, b.fot_sl_1, b.dist_cpu_2, 
                b.fot_sl_2, b.inc_uva_21, b.lep, b.plano_l, b.rh, b.rivolta, b.tipo_mza, 
                b.uso_1, b.uso_2, b.uso_3,
                b.parcela, b.cpu_obs, b.plano_l_ob, b.ae_fot_bas, b.zona_2, b.adps, b.memo, b.microcentr 
                    from mo_parcelasmap a
                    left join cur_parcelas b on a.smp = b.smp
                    left join aph_ssregic d on a.smp = d.smp
                    left join (
                        select x.smp, min(tipo_c) tipo_c
                        from mo_parcelasmap x
                        left join frentesparcelas y on x.smp = y.smp
                        left join cur_callejero z on y.frente = z.nom_mapa
                        where (x.seccion || '-' || x.manzana)  in ({0})
                        group by x.smp ) C on a.smp = c.smp
                where (a.seccion || '-' || b.manzana)  in ({0})
              """
            sql = sql.format(params)
            return geopandas.read_postgis(sql, self.__db_connector.get(), 'the_geom')