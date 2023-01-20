from collections import defaultdict
import traceback
import uuid

from platformdirs import os
from entity.urban.Lot import Lot
from entity.urban.BuildType import BuildType
from usecase.urban.BuildTypeService import BuildTypeService
from usecase.core.LogService import LogService
from usecase.urban.CornerAreaService import CornerAreaService
from usecase.core.DictUtil import DictUtil
from entity.urban.Block import Block
from adapter.urban.BlockRepository import BlockRepository
from entity.urban.Restriction import Restriction
from adapter.geo.GisLibrary import GisLibrary
from usecase.urban.FabricService import FabricService
from usecase.urban.RestrictionService import RestrictionService
from usecase.urban.LotService import LotService
from usecase.urban.CustomLineService import CustomLineService
from usecase.core.ThreadService import ThreadService

class BlockService:

    def __init__(self,
                 block_repository:BlockRepository,
                 lot_service:LotService,
                 gis_library:GisLibrary,
                 restriction_service:RestrictionService,
                 fabric_service:FabricService,
                 dict_util:DictUtil,
                 corner_area_service:CornerAreaService,
                 custom_line_service:CustomLineService,
                 thread_service:ThreadService,
                 log_service:LogService,
                 build_type_service:BuildTypeService,
                 prop:dict) -> None:

        self.__block_repository = block_repository
        self.__lot_service = lot_service
        self.__gis_library = gis_library
        self.__restriction_service = restriction_service
        self.__fabric_service = fabric_service
        self.__dict_util = dict_util
        self.__corner_area_service = corner_area_service
        self.__custom_line_service = custom_line_service
        self.__thread_service = thread_service
        self.__log_service = log_service
        self.__build_type_service = build_type_service
        self.__all_blocks:list[Block] = []
        self.__prop = prop

    def run_algorythms(self, blocks:list[Block])-> list[Block]:

        block_new_list = []
        for block in blocks:
            try:
                self.__log_service.add({'message':'process block', 'block':block.get_name()})

                # Armar validacion Tabla curparcelas campo dist_grp_1 = UP o Espacio Publico
                self.__find_complete(block)
                valid = self.__validate_block(block)
                if (valid):
                    block_new_list.append(block)
                    self.__restriction_service.build_with_restrictions(block, block, 'block_restrictions')
                    self.__build_line_block(block)
                    self.__build_base_lines(block)
                    self.__build_official_line(block)
                    self.__lot_service.build_official_line(block)
                    self.__resolve_ae26(block)
                    self.__build_minimal_band(block)
                    self.__fabric_service.build_consolidated(block)
                    self.__corner_area_service.build(block)
                    self.__lot_service.find_rivolta(block)
                    self.__lot_service.find_leveling(block)
                    valid = self.__lot_service.validate_buildability_block(block)
                    if (valid):
                        self.__lot_service.build_buildability(block)
            except Exception:
                self.__log_service.add({'message':'process ERROR block', 'error':traceback.format_exc()})

        return block_new_list

    def export_cad(self, layer: dict, blocks:list[Block], transformation = None) -> dict:

        # manzana
        # banda_minima
        # lfi
        # lib
        # e34m (linea)
        # parcela
        # linea_oficial (linea)
        # tejido (Ver como resolver)
        # volumen_edif (Ver como resolver)

        items = []
        for idx, block in enumerate(blocks):

            try:

                #manzana
                item = {}
                definition = {'name':'manzana', 'info':item}
                self.__cad_add_geom(item, items, definition, self.__gis_library.get_value(self.__gis_library.convert_one(block, 'MultiLineString')))

                #banda_minima
                item = {}
                definition = {'name':'banda_minima', 'info':item}
                self.__cad_add_geom(item, items, definition,  self.__gis_library.get_value(self.__gis_library.convert_one(block.get_geometry('minimal_band'), 'MultiLineString')))

                #lfi
                item = {}
                definition = {'name':'lfi', 'info':item}
                self.__cad_add_geom(item, items, definition, self.__gis_library.get_value(self.__gis_library.convert_one(block.get_geometry('lfi_extension'), 'MultiLineString')))

                #lib
                item = {}
                definition = {'name':'lib', 'info':item}
                self.__cad_add_geom(item, items, definition, self.__gis_library.get_value(self.__gis_library.convert_one(block.get_geometry('lbi'),'MultiLineString')))

                for corner_area in block.get_corner_areas():
                    #e34m
                    item = {}
                    definition = {'name':'e34m', 'info':item}
                    self.__cad_add_geom(item, items, definition, self.__gis_library.get_value(self.__gis_library.convert_one(corner_area,'MultiLineString')))

                for lot in block.get_lots():

                    #parcela
                    item = {}
                    definition = {'name':'parcela', 'info':item}
                    self.__cad_add_geom(item, items, definition, self.__gis_library.get_value(self.__gis_library.convert_one(lot,'MultiLineString')))

                    #linea_oficial
                    item = {}
                    definition = {'name':'linea_oficial', 'info':item}
                    self.__cad_add_geom(item, items, definition, self.__gis_library.get_value(self.__gis_library.convert_one(lot.get_geometry('official_line'),'MultiLineString')))

                    for fabric in lot.get_fabrics():
                        #tejido
                        item = {}
                        definition = {'name':'tejido', 'info':item}
                        self.__cad_add_geom(item, items, definition, self.__gis_library.get_value(self.__gis_library.convert_one(fabric, 'MultiLineString')))

                    #volumen_edif
                    #No se muestra. Verificar porque hay un corrimiento.
                    #for build in lot.get_buildabilities():
                        #item = {}
                        #definition = {'name':'volumen_edif', 'info':item}
                        #self.__cad_add_geom(item, items, definition, self.__gis_library.get_value(self.__gis_library.convert_one(build, 'MultiLineString')))

            except:
                self.__log_service.add({'message':'export ERROR block', 'block': block.get_name(), 'error':traceback.format_exc()})

        for definition in items:
            layer[definition['name']].append(definition['info'])

        return layer

    def __cad_add_geom(self, item, items, definition, geom):
        if geom:
            item['geom'] = geom
            items.append(definition)


    def export(self, layer: dict, blocks:list[Block], transformation = None) -> dict:

        # > Block
        #  manzana.mbtiles
        #  banda_minima.mbtiles
        #  lfi.mbtiles
        #  lib.mbtiles

        # > Corner Area
        #  e34m.mbtiles

        # > Lot
        #  parcela.mbtiles
        #  aph_ssregic.mbtiles
        #  linea_oficial.mbtiles >> Linea Oficial sobre Parcelas ????
        #  volumen_edif.mbtiles
        #  tejido.mbtiles
        #  riesgo_hidrico.mbtiles
        #  cur_riesgo_arqueologico.mbtiles
        #  restricciones.mbtiles

        #  codigo_urbanistico.mbtiles
        #  rivolta.mbtiles


        items = []
        for idx, block in enumerate(blocks):

            try:

                source = self.__prop['export']['source']
                id = idx + 1

                #manzana
                item = {}
                definition = {'name':'manzana', 'info':item}
                item['id'] = id
                item['sm'] = block.get_name()
                item['tipo'] = block.get_type_block()
                item['geom'] = self.__gis_library.project(block, transformation)
                items.append(definition)

                #banda_minima
                item = {}
                definition = {'name':'banda_minima', 'info':item}
                item['fuente'] = source
                item['id'] = id
                item['sm'] = block.get_name()
                item['geom'] = self.__gis_library.project(block.get_geometry('minimal_band'), transformation)
                items.append(definition)

                #lfi
                item = {}
                definition = {'name':'lfi', 'info':item}
                item['id'] = id
                item['sm'] = block.get_name()
                item['geom'] = self.__gis_library.project(block.get_geometry('lfi_extension'), transformation)
                items.append(definition)

                #lib
                item = {}
                definition = {'name':'lib', 'info':item}
                item['id'] = id
                item['sm'] = block.get_name()
                item['geom'] = self.__gis_library.project(block.get_geometry('lbi'), transformation)
                items.append(definition)

                for id_corner_area, corner_area in enumerate(block.get_corner_areas()):
                    #e34m
                    item = {}
                    definition = {'name':'e34m', 'info':item}
                    item['id'] = id
                    item['sm'] = block.get_name()
                    item['fuente'] = source
                    item['esquina'] = id_corner_area + 1
                    item['geom'] = self.__gis_library.project(corner_area, transformation)
                    items.append(definition)

                for idx_lot, lot in enumerate(block.get_lots()):

                    id_lot = (id * 10000) + idx_lot + 1
                    geom = self.__gis_library.project(lot, transformation)

                    #parcela
                    item = {}
                    definition = {'name':'parcela', 'info':item}
                    item['id'] = id_lot
                    item['smp'] = lot.get_name()
                    item['geom'] = geom
                    items.append(definition)

                    #aph_ssregic
                    item = {}
                    definition = {'name':'aph_ssregic', 'info':item}
                    item['proteccion'] = lot.get_protection()
                    item['geom'] = geom
                    items.append(definition)


                    #codigo_urbanistico
                    item = {}
                    definition = {'name':'codigo_urbanistico', 'info':item}
                    item['alicuota'] = lot.get_info()['alicuota']
                    item['anac'] = lot.get_info()['anac']
                    item['ensanche'] = lot.get_info()['ensanche']
                    item['catalgo'] = lot.get_info()['catalogado']
                    item['ci_digital'] = lot.get_info()['ci_digital']
                    item['comuna'] = lot.get_info()['comuna']
                    item['dist_1_esp'] = lot.get_info()['dist_1_esp']
                    item['dist_1_grp'] = lot.get_info()['dist_1_grp']
                    item['dist_cpu_1'] = lot.get_info()['dist_cpu_1']
                    item['ensanche'] = lot.get_info()['ensanche']
                    item['fot_em_1'] = lot.get_info()['fot_em_1']
                    item['fot_em_2'] = lot.get_info()['fot_em_2']
                    item['fot_pl_1'] = lot.get_info()['fot_pl_1']
                    item['fot_pl_2'] = lot.get_info()['fot_pl_2']
                    item['fot_sl_1'] = lot.get_info()['fot_sl_1']
                    item['fot_sl_2'] = lot.get_info()['fot_sl_2']
                    item['inc_uva_21'] = lot.get_info()['inc_uva_21']
                    item['lep'] = lot.get_info()['lep']
                    item['manzana'] = lot.get_info()['manzana']
                    item['plano_l'] = lot.get_info()['plano_l']
                    item['rh'] = lot.get_info()['rh']
                    item['rivolta'] = lot.get_info()['rivolta']
                    item['seccion'] = lot.get_info()['seccion']
                    item['smp'] = lot.get_info()['smp']
                    item['tipo_mza'] = lot.get_info()['tipo_mza']
                    item['uni_edif_1'] = lot.get_info()['uni_edif_1']
                    item['uni_edif_2'] = lot.get_info()['uni_edif_2']
                    item['uni_edif_3'] = lot.get_info()['uni_edif_3']
                    item['uni_edif_4'] = lot.get_info()['uni_edif_4']
                    item['uso_1'] = lot.get_info()['uso_1']
                    item['uso_2'] = lot.get_info()['uso_2']
                    item['uso_3'] = lot.get_info()['uso_3']
                    item['irregular'] = lot.get_irregular()
                    item['geom'] = geom
                    items.append(definition)

                    #linea_oficial
                    item = {}
                    definition = {'name':'linea_oficial', 'info':item}
                    item['calle'] = ''
                    item['fuente'] = source
                    item['id'] = id_lot
                    item['smp'] = lot.get_name()
                    item['geom'] = self.__gis_library.project(lot.get_geometry('official_line'), transformation)
                    items.append(definition)

                    consolidate = lot.get_consolidation().get_consolidated() if lot.get_consolidation() else False
                    type_consolidate = lot.get_consolidation().get_type_consolidated() if lot.get_consolidation() else ""

                    if consolidate:
                        item = {}
                        definition = {'name':'cur_consolidados', 'info':item}
                        item['gid'] = id_lot
                        item['smp'] = lot.get_name()
                        item['sm'] = block.get_name()
                        item['consol_txt'] = type_consolidate
                        item['porc_cons'] = lot.get_consolidation().get_percentage()
                        item['geom'] = geom
                        items.append(definition)

                    for idx_fabric, fabric in enumerate(lot.get_fabrics()):
                        id_fabric = (id_lot * 10000) + idx_fabric + 1
                        #tejido
                        item = {}
                        definition = {'name':'tejido', 'info':item}
                        item['altos'] = fabric.get_highs()
                        item['altura'] = fabric.get_height()
                        item['consolidado'] = consolidate
                        item['fuente'] = source
                        item['id'] = id_fabric
                        item['smp'] = lot.get_name()
                        item['tipo'] = type_consolidate
                        item['geom'] = self.__gis_library.project(fabric, transformation)
                        items.append(definition)

                    for idx_build, build in enumerate(lot.get_buildabilities()):
                        id_build = (id_lot * 100) + idx_build + 1
                        edif = build.get_build_type().get_code() if build.get_build_type().get_build_info().get_dist_grp() == None else build.get_build_type().get_build_info().get_dist_grp()
                        require_origen = False if build.get_build_type().get_build_info().get_dist_grp() == None else True
                        #volumen_edif
                        item = {}
                        definition = {'name':'volumen_edif', 'info':item}
                        item['altura_inicial'] = build.get_from()
                        item['altura_final'] = build.get_to()
                        item['altura_fin'] = build.get_to()
                        item['edificabil'] = edif
                        item['origen'] = edif if require_origen else ""
                        item['fuente'] = source
                        item['id'] = id_build
                        item['smp'] = lot.get_name()
                        item['tipo'] = build.get_descriptor()
                        item['geom'] = self.__gis_library.project(build, transformation)
                        items.append(definition)
            except:
                self.__log_service.add({'message':'export ERROR block', 'block': block.get_name(), 'error':traceback.format_exc()})

        for definition in items:
            layer[definition['name']].append(definition['info'])

        return layer

    def export_data(self, layer, blocks:list[Block], transformation = None) -> dict:

        # > Block
        #  manzana.mbtiles
        #  banda_minima.mbtiles
        #  lfi.mbtiles
        #  lib.mbtiles

        items = []
        for idx, block in enumerate(blocks):

            try:

                source = self.__prop['export']['source']
                id = idx + 1

                #manzana
                item = {}
                definition = {'name':'manzana', 'info':item}
                item['sm'] = block.get_name()
                item['tipo'] = block.get_type_block()
                item['geom'] = self.__gis_library.project(block, transformation)

                item['manzana'] = block.get_info()['manzana']
                item['seccion'] = block.get_info()['seccion']
                item['nivel'] = block.get_info()['nivel']
                item['cant_lados'] = block.get_info()['cant_lados']
                item['mz_sup'] = block.get_info()['mz_sup']
                item['cant_pa'] = block.get_info()['cant_parce']
                item['area_esp'] = block.get_info()['area_esp']
                item['uni_edif'] = block.get_info()['uni_edif']
                item['oferta'] = block.get_info()['oferta']
                item['obras'] = block.get_info()['obras']
                item['superficie'] = block.get_info()['superficie']
                item['trazado'] = block.get_info()['trazado']
                item['disposicio'] = block.get_info()['disposicio']
                item['parc_catal'] = block.get_info()['parc_catal']
                item['cant_parce'] = block.get_info()['cant_parce']
                item['pdf'] = block.get_info()['pdf']

                items.append(definition)

                for idx_lot, lot in enumerate(block.get_lots()):

                    id_lot = (id * 10000) + idx_lot + 1
                    geom = self.__gis_library.project(lot, transformation)

                    #parcela
                    item = {}
                    definition = {'name':'parcela', 'info':item}
                    item['id'] = id_lot
                    item['smp'] = lot.get_name()
                    item['geom'] = geom
                    item['barrios'] = lot.get_info()['barrios']
                    item['comuna'] = lot.get_info()['comuna']
                    item['1_calle'] = lot.get_info()['1_calle']
                    item['1_altura'] = lot.get_info()['1_altura']
                    item['1_direccio'] = lot.get_info()['1_direccio']
                    item['2_calle'] = lot.get_info()['2_calle']
                    item['2_alt'] = lot.get_info()['2_alt']
                    item['2_direccio'] = lot.get_info()['2_direccio']
                    item['3_calle'] = lot.get_info()['3_calle']
                    item['3_alt'] = lot.get_info()['3_alt']
                    item['3_direccio'] = lot.get_info()['3_direccio']
                    item['4_calle'] = lot.get_info()['4_calle']
                    item['4_alt'] = lot.get_info()['4_alt']
                    item['4_direccio'] = lot.get_info()['4_direccio']
                    item['denominaci'] = lot.get_info()['denominaci']
                    item['catalogaci'] = lot.get_info()['catalogaci']
                    item['aph_nro_y_'] = lot.get_info()['aph_nro_y_']
                    item['proteccion'] = lot.get_info()['proteccion']
                    item['estado'] = lot.get_info()['estado']
                    item['ley_3056'] = lot.get_info()['ley_3056']
                    item['area'] = lot.get_buildability_area()
                    item['area_parcela'] = lot.get_info()['area']

                    item['uni_edif_1'] = lot.get_info()['uni_edif_1']
                    item['uni_edif_2'] = lot.get_info()['uni_edif_2']
                    item['uni_edif_3'] = lot.get_info()['uni_edif_3']
                    item['uni_edif_4'] = lot.get_info()['uni_edif_4']
                    item['uso_1'] = lot.get_info()['uso_1']
                    item['uso_2'] = lot.get_info()['uso_2']
                    item['uso_3'] = lot.get_info()['uso_3']
                    item['dist_1_esp'] = lot.get_info()['dist_1_esp']
                    item['dist_1_grp'] = lot.get_info()['dist_1_grp']
                    item['dist_2_esp'] = lot.get_info()['dist_2_esp']
                    item['dist_2_grp'] = lot.get_info()['dist_2_grp']
                    item['dist_3_esp'] = lot.get_info()['dist_3_esp']
                    item['dist_3_grp'] = lot.get_info()['dist_3_grp']
                    item['dist_4_esp'] = lot.get_info()['dist_4_esp']
                    item['dist_4_grp'] = lot.get_info()['dist_4_grp']

                    item['anac'] = lot.get_info()['anac']
                    item['ci_digital'] = lot.get_info()['ci_digital']
                    item['rh'] = lot.get_info()['rh']
                    item['lep'] = lot.get_info()['lep']
                    item['ensanche'] = lot.get_info()['ensanche']
                    item['apertura'] = lot.get_info()['apertura']
                    item['rivolta'] = lot.get_info()['rivolta']
                    item['catalogado'] = lot.get_info()['catalogado']
                    item['incid_uva'] = lot.get_info()['inc_uva_21']
                    item['alicuota'] = lot.get_info()['alicuota']
                    item['dist_cpu_1'] = lot.get_info()['dist_cpu_1']
                    item['dist_cpu_2'] = lot.get_info()['dist_cpu_2']

                    item['seccion'] = lot.get_info()['seccion']
                    item['manzana'] = lot.get_info()['manzana']
                    item['parcela'] = lot.get_info()['parcela']
                    item['cpu_obvs'] = lot.get_info()['cpu_obs']

                    item['fot_em_1'] = lot.get_info()['fot_em_1']
                    item['fot_em_2'] = lot.get_info()['fot_em_2']
                    item['fot_pl_1'] = lot.get_info()['fot_pl_1']
                    item['fot_pl_2'] = lot.get_info()['fot_pl_2']
                    item['fot_sl_1'] = lot.get_info()['fot_sl_1']
                    item['fot_sl_2'] = lot.get_info()['fot_sl_2']

                    item['plano_l_ob'] = lot.get_info()['plano_l']
                    item['tipo_mza'] = lot.get_info()['tipo_mza']
                    item['ae_fot_bas'] = lot.get_info()['ae_fot_bas']
                    item['zona_1'] = lot.get_info()['zona_1']
                    item['zona_2'] = lot.get_info()['zona_2']

                    item['adps'] = lot.get_info()['adps']
                    item['memo'] = lot.get_info()['memo']
                    item['microcentr'] = lot.get_info()['microcentr']

                    item['irregular'] = lot.get_irregular()
                    item['enrase'] = lot.get_levelings() != None and len(lot.get_levelings()) > 0

                    items.append(definition)

            except:
                self.__log_service.add({'message':'export ERROR block', 'block': block.get_name(), 'error':traceback.format_exc()})

        for definition in items:
            layer[definition['name']].append(definition['info'])

        return layer

    def find_all(self) -> list[Block]:
        return self.__block_repository.find_all()

    def find_by_blocks_sections(self, blocks:list[str], sections:list[str]) -> list[Block]:
        return self.__block_repository.find_by_blocks_sections(blocks, sections)

    def __find_complete(self, block:Block) -> Block:

        # self.resolve_ae26(block)
        block.set_lots(self.__lot_service.find_complete_by_block(block))
        custom_lines = self.__custom_line_service.find_by_block(block)
        for custom_line in custom_lines:
            if custom_line.get_type_custom_line() == "LFI":
                block.add_geometry(self.__gis_library.poligonize(custom_line), "lfi_extension")
            elif custom_line.get_type_custom_line() == "LIB":
                block.add_geometry(custom_line, "lbi")

        return block

    def find_all_blocks(self):
        self.__all_blocks = self.__block_repository.find_all()

    def __resolve_ae26(self, block:Block):

        build_code = None
        rule = self.__block_repository.find_ae26(block)
        lot_code = defaultdict(dict)

        if rule:
            buffer_block = self.__gis_library.buffer(block, 100)
            block_relations = self.__gis_library.spatial_join([buffer_block], self.__all_blocks)
            if block_relations:

                block_list_to_find:list[Block] = []
                for block_relation in block_relations:
                    from_block, to_block, value = block_relation
                    block_list_to_find.append(to_block)

                if block_list_to_find:
                    join_lots = self.__lot_service.find_by_blocks(block_list_to_find)
                    lots:list[Lot] = []
                    block_lines_temp = self.__gis_library.disaggregate_list(block)
                    block_lines = []
                    for block_line in block_lines_temp:
                        block_lines.append(self.__gis_library.buffer(block_line, 0.2))

                    for lot in block.get_lots():
                        official_line_lot = lot.get_geometry("official_line")
                        intersection_line = None
                        for block_line in block_lines:
                            intersection_line = self.__gis_library.intersection(official_line_lot, block_line)
                            if intersection_line:
                                break
                        if intersection_line:
                            one_line = self.__gis_library.cast(intersection_line, 'LineString')
                            points = self.__gis_library.disaggregate_list(one_line, 'MultiPoint')
                            simple_line = self.__gis_library.merge([points[0], points[len(points) - 1]])
                            parallel_official_line_lot = self.__gis_library.parallel_offset(simple_line, -100)
                            parallel_center_point = self.__gis_library.find_point_center(parallel_official_line_lot)
                            center_point = self.__gis_library.find_point_center(simple_line)
                            line = self.__gis_library.merge([center_point, parallel_center_point])
                            line.set_attribute('lot', lot)
                            line.set_attribute('point', center_point)
                            lots.append(line)

                    lot_relations = self.__gis_library.spatial_join(lots, join_lots)
                    if lot_relations:
                        for lot_relation in lot_relations:
                            from_lot, to_lot, value = lot_relation
                            points = self.__gis_library.convert(value, 'Point')
                            if points:
                                distance_line = self.__gis_library.merge([from_lot.get_attribute("point"), points[0]])
                                length = self.__gis_library.length(distance_line)

                                info_lot = lot_code[from_lot.get_attribute("lot").get_name()]
                                if (not info_lot or length <= info_lot['length']) and from_lot.get_attribute("lot").get_block().get_name() != to_lot.get_block().get_name() :
                                    info_lot['length'] = length
                                    info_lot['build_info'] = from_lot.get_attribute("lot").get_build_infos()[0]
                                    info_lot['lot'] = to_lot.get_name()

            build_code = rule[0]['build_code']
            block.set_ae26(build_code)

            build_type_block =  self.__build_type_service.find_by_build_info(self.__build_type_service.find_by_code(build_code))

            for lot in block.get_lots():

                info_lot = lot_code[lot.get_name()]
                build_type = build_type_block
                if info_lot:
                    build_type_tmp:BuildType = self.__build_type_service.find_by_build_info(info_lot['build_info'])
                    if build_type_tmp.get_ae26() != None:
                        build_type_tmp = self.__build_type_service.find_by_build_info(build_type_tmp.get_ae26())
                        if build_type_tmp:
                            build_type = build_type_tmp.get_ae26()

                lot.set_build_types([build_type])
                lot.get_heights().append(build_type.get_height())

    def find_restrictions(self, blocks:list[Block], restrictions:list[Restriction]):
        intersections = self.__gis_library.spatial_join(blocks, restrictions,)

        for intersection in intersections:
            block, restriction, value = intersection
            restriction.set_values(value)
            block.get_restrictions().append(restriction)

        self.__restriction_service.validate(blocks)

    def __build_minimal_band(self, block:Block):

        buffer = self.__prop['minimal_band']['buffer']
        dissolve_lot = block.get_geometry('dissolve_lot')
        if (dissolve_lot):
            block_buffer = self.__gis_library.buffer(block, buffer, True, -1, 1)
            block_band = self.__gis_library.difference(block, [block_buffer])
            if (block_band):
                minimal_band = self.__gis_library.intersection(block_band, dissolve_lot)
                block.add_geometry(minimal_band,'minimal_band')

    def __build_official_line(self, block:Block):
        lots_dissolve = self.__gis_library.dissolve_union(block.get_lots())
        if (lots_dissolve is not None):
            found = self.__restriction_service.find_with_restrictions(block, lots_dissolve)
            if (found):
                block.add_geometry(found, 'dissolve_lot')
                cast = self.__gis_library.cast(found, 'LineString')
                if (cast):
                    block.add_geometry(cast, 'official_line')

    def __build_line_block(self, block:Block):
        block_lines = self.__gis_library.disaggregate(block.get_geometry('block_restrictions'), 'LineString')
        block.add_geometry(block_lines,'block_lines')

    def __build_base_lines(self, block:Block):

        lines = self.__validate_build_base_lines(block)
        for line in lines:
            self.__build_base_line(block, line)

    def __validate_block(self, block:Block) -> bool:

        result = False
        not_valid_build_type = self.__prop['not_valid_build_type']

        code = None
        for lot in block.get_lots():
            for build_type in lot.get_build_types():
                if build_type.get_code() not in not_valid_build_type:
                    code = None
                else:
                    code = build_type.get_code()
                    break

            if code is not None:
                break

        if code is None:
            result = True
        else:
            cause = {'cause':'not valid build type: ' + code}

        if (not result):
            self.__log_service.add({'message':'discard block for processing', 'block':block.get_name(), **cause})

        return result

    def __validate_build_base_lines(self, block:Block) -> list[str]:

        result = []
        cause = {}
        valid_type = self.__prop['base_line']['valid_type']
        valid_line_size = self.__prop['base_line']['valid_line_size']
        has_build_type = self.__build_type_service.has_build_type(block)

        if (has_build_type):
            if not block.has_geometry('lfi_extension') and not block.has_geometry('lbi'):
                if (block.get_type_block() in valid_type):
                    if (len(block.get_geometry('block_lines').get_values()) == valid_line_size):
                        found = self.__build_type_service.has_geometry(block, 'lfi_extension')
                        result = ['lbi']
                        if found:
                            result.append('lfi')
                    else:
                        cause = {'cause':'vertices <> ' + valid_line_size}
                else:
                    cause = {'cause':'type not valid'}
            else:
                cause = {'cause':'already has custom line'}
        else:
            cause = {'cause':'not have build type'}

        if (not result):
            self.__log_service.add({'message':'discard block for base line building', 'type_block':block.get_type_block() if block.get_type_block() is not None else "", **cause})

        return result

    def get_coordinates_from_point(self, intersection_point):
        """Función que recibe un objeto tipo POINT, y extrae las coordenadas del mencionado objeto."""
        if intersection_point:
            intersection_point = intersection_point.get_values()[0]
            splitted_point_data = intersection_point.split(' ')
            x = float(splitted_point_data[1].strip('('))
            y = float(splitted_point_data[2].strip(')'))
            coordinates = tuple([x, y])
            return coordinates
        return None

    def __build_base_line(self, block:Block, key:str):
        divided_by = self.__prop['base_line'][key]['divided_by']
        fscale = 1 / divided_by
        geo = block.get_geometry('block_lines')

        if geo:
            geo_lines = geo.get_values()
            # Juntamos las 4 LS para obtener un MultiLineString que sería el contorno de la manzana (Linea Oficial)
            geo_lo = self.__gis_library.merge(geo_lines)
            # Obtenemos los puntos medios de cada una de los LS (ordenados)
            centers = []

            for line in geo_lines:
                centers.append(self.__gis_library.find_point_center(line))
            # Obtenemos las lineas que unen los puntos medios de las aristas opuestas (LS)
            mid_lines = []

            for i in range(2):
                mid_opos_point = [centers[i].get_values(), centers[i+2].get_values()]
                mid_lines.append(self.__gis_library.merge(mid_opos_point))
            # obtenemos la interseccion de estas dos lineas, este será el 'origin' del metodo scale
            intersection_point = self.__gis_library.intersection(mid_lines[0], mid_lines[1])
            # Obtenemos las coordenadas provenientes de 'intersection_point', que será el valor asignado a 'origin'
            origin_coordinates = self.get_coordinates_from_point(intersection_point)
            # Aplicamos el scale y adosamos el resultado al objeto block
            result = self.__gis_library.scale(geo_lo, fscale, fscale, origin=origin_coordinates)
            block.add_geometry(result, key)

    def find_front_lot(self, blocks:list[Block]):
        lots = self.__block_repository.find_lots_ae26()
        for lot in lots:
            lot

        pass
